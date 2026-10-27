"""Check whether the portfolio's projects are up and find the latest Python Digest issue.

Runs on the server from cron (every 5 minutes, see .claude/skills/deploy/SKILL.md) with the
system Python 3.12 and the standard library only. Writes runtime/live.json, which nginx serves
at /live/live.json and main.js reads to switch the "live" badges and show the latest issue.
"""

import argparse
import datetime as dt
import json
import logging
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import data  # noqa: E402

USER_AGENT = "tkoralewski-portfolio-status/1.0 (+https://tkoralewski.toadres.pl)"
TIMEOUT = 10

logger = logging.getLogger("live_status")


def fetch(url: str) -> tuple[int, bytes, int]:
    """GET a URL; returns (HTTP status, body, elapsed ms). Status 0 means no response at all."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read(512_000)
            status = response.status
    except urllib.error.HTTPError as exc:
        status, body = exc.code, b""
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.warning("%s unreachable: %s", url, exc)
        status, body = 0, b""
    return status, body, round((time.monotonic() - started) * 1000)


def is_up(status: int) -> bool:
    # urllib follows redirects, so a 3xx here means a redirect loop or a refused hop.
    return 200 <= status < 400


class LatestIssueParser(HTMLParser):
    """Reads the "Ostatnie wydanie" block of the Python Digest home page."""

    def __init__(self) -> None:
        super().__init__()
        self.number: int | None = None
        self.title = ""
        self.href = ""
        self.date = ""
        self._field: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        if "preview-issue-number" in classes and self.number is None:
            self._field = "number"
        elif "preview-issue-title" in classes and not self.title:
            self._field = "title"
            self.href = dict(attrs).get("href") or ""
        elif "preview-issue-date" in classes and not self.date:
            self._field = "date"

    def handle_endtag(self, tag: str) -> None:
        self._field = None

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not self._field or not text:
            return
        if self._field == "number":
            digits = text.lstrip("#")
            self.number = int(digits) if digits.isdigit() else None
        elif self._field == "title":
            self.title += text
        elif self._field == "date":
            self.date = text


def parse_latest_issue(html: str, base_url: str) -> dict | None:
    parser = LatestIssueParser()
    parser.feed(html)
    if not (parser.title and parser.href):
        return None
    return {
        "number": parser.number,
        "title": parser.title,
        "url": urljoin(base_url, parser.href),
        "date": parser.date,
    }


def collect() -> dict:
    projects = {}
    for project in data.PROJECTS:
        url = str(project.get("address") or "")
        if not url or project.get("offline"):
            continue
        status, body, elapsed = fetch(url)
        projects[url] = {"up": is_up(status), "status": status, "ms": elapsed}
        if url == data.PROFILE["newsletter"] and is_up(status):
            latest = parse_latest_issue(body.decode("utf-8", "replace"), url)
            if latest is None:
                logger.warning("no latest issue found on %s", url)
            projects[url]["latest_issue"] = latest
    return {
        "checked_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "projects": projects,
    }


def write_atomic(path: Path, payload: dict) -> None:
    """Write next to the target and rename, so nginx never serves a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".live-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=1)
        os.chmod(tmp, 0o644)  # nginx in the container runs as a non-root user
        os.replace(tmp, path)
    except OSError:
        Path(tmp).unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parents[1] / "runtime" / "live.json"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    payload = collect()
    try:
        write_atomic(args.out, payload)
    except OSError as exc:
        logger.error("cannot write %s: %s", args.out, exc)
        return 1
    logger.info("wrote %s: %s", args.out, json.dumps(payload["projects"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
