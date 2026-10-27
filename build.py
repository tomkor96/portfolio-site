"""Render the portfolio from data.py and templates/ into a static site in dist/."""

import argparse
import datetime as dt
import hashlib
import logging
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError

import data

ROOT = Path(__file__).resolve().parent
MONTHS = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]

logger = logging.getLogger("build")


def month_year(value: str | None) -> str:
    """Format "2024-08-01" as "sie 2024"; a bare year stays as it is, None means ongoing."""
    if not value:
        return "obecnie"
    try:
        date = dt.date.fromisoformat(value)
    except ValueError:
        return value
    return f"{MONTHS[date.month - 1]} {date.year}"


def years_since(value: str, today: dt.date | None = None) -> int:
    """Full years since an ISO date, at least 1."""
    start = dt.date.fromisoformat(value)
    today = today or dt.date.today()
    years = today.year - start.year - ((today.month, today.day) < (start.month, start.day))
    return max(1, years)


def asset_url(path: str) -> str:
    """Append a content hash so browsers refetch a changed asset despite the long cache."""
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]
    return f"{path}?v={digest}"


def build_context() -> dict:
    """Everything the templates read; projects marked featured come first."""
    projects = sorted(data.PROJECTS, key=lambda p: not p.get("featured", False))
    return {
        "profile": data.PROFILE,
        "experience": data.EXPERIENCE,
        "education": data.EDUCATION,
        "skills": data.SKILLS,
        "certs": data.CERTS,
        "projects": projects,
        "cv_file": Path(data.PROFILE["cv_path"]).name,
        "tech_years": years_since(data.EXPERIENCE[0]["start_date"]),
        "year": dt.date.today().year,
    }


def build(out: Path) -> Path:
    """Render index.html and copy static assets and the CV into out; returns the page path."""
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["month_year"] = month_year
    env.globals["asset_url"] = asset_url

    out = out.resolve()
    if out == ROOT or out in ROOT.parents:
        raise ValueError(f"refusing to clear {out}: it contains the project")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out / "static")

    cv = ROOT / data.PROFILE["cv_path"]
    shutil.copy2(cv, out / cv.name)

    page = out / "index.html"
    page.write_text(env.get_template("index.html").render(build_context()), encoding="utf-8")
    return page


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        page = build(args.out)
    except (TemplateError, OSError, KeyError, ValueError) as exc:
        logger.error("build failed: %s", exc)
        return 1
    logger.info("built %s", page)
    return 0


if __name__ == "__main__":
    sys.exit(main())
