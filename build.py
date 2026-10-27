"""Render the portfolio from data.py and templates/ into dist/: PL at /, EN at /en/."""

import argparse
import datetime as dt
import hashlib
import json
import logging
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError

import data
from texts import MONTHS, TECH_LABELS, TEXTS

ROOT = Path(__file__).resolve().parent
LANGUAGES = ("pl", "en")

logger = logging.getLogger("build")


def localize(value, lang: str):
    """Resolve {"pl": ..., "en": ...} values anywhere in a data structure to one language."""
    if isinstance(value, dict):
        if set(value) == set(LANGUAGES):
            return value[lang]
        return {key: localize(item, lang) for key, item in value.items()}
    if isinstance(value, list):
        return [localize(item, lang) for item in value]
    return value


def month_year(value: str | None, lang: str = "pl") -> str:
    """Format "2024-08-01" as "sie 2024"; a bare year stays as it is, None means ongoing."""
    if not value:
        return TEXTS[lang]["present"]
    try:
        date = dt.date.fromisoformat(value)
    except ValueError:
        return value
    return f"{MONTHS[lang][date.month - 1]} {date.year}"


def tech_label(name: str, lang: str = "pl") -> str:
    return TECH_LABELS.get(lang, {}).get(name, name)


def slug(value: str) -> str:
    """CSS class name for a label: "Tailwind CSS" -> "tailwind-css", "Obsługa" -> "obsluga"."""
    ascii_text = unicodedata.normalize("NFKD", value.replace("ł", "l").replace("Ł", "L"))
    ascii_text = ascii_text.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


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


def person_json_ld(profile: dict) -> str:
    """schema.org Person for search engines; "</" is escaped so the data can't close the tag."""
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile["name"],
        "jobTitle": profile["role"],
        "url": profile["site_url"],
        "image": f"{profile['site_url']}/static/img/portrait.webp",
        "email": f"mailto:{profile['email']}",
        "sameAs": [profile["linkedin"], profile["github"]],
    }
    return json.dumps(person, ensure_ascii=False).replace("</", r"<\/")


def build_context(lang: str) -> dict:
    """Everything the templates read for one language; projects marked featured come first."""
    profile = localize(data.PROFILE, lang)
    projects = sorted(localize(data.PROJECTS, lang), key=lambda p: not p.get("featured", False))
    return {
        "lang": lang,
        "t": TEXTS[lang],
        "texts": TEXTS,
        # Relative prefix from the page to the site root (static/, the CV).
        "root": "" if lang == "pl" else "../",
        "profile": profile,
        "experience": localize(data.EXPERIENCE, lang),
        "education": localize(data.EDUCATION, lang),
        "skills": localize(data.SKILLS, lang),
        "certs": localize(data.CERTS, lang),
        "projects": projects,
        "cv_file": Path(data.PROFILE["cv_path"]).name,
        "json_ld": person_json_ld(profile),
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
    env.filters["slug"] = slug
    env.filters["tech_label"] = tech_label
    env.globals["asset_url"] = asset_url

    out = out.resolve()
    if out == ROOT or out in ROOT.parents:
        raise ValueError(f"refusing to clear {out}: it contains the project")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out / "static")

    cv = ROOT / data.PROFILE["cv_path"]
    shutil.copy2(cv, out / cv.name)

    template = env.get_template("index.html")
    for lang in LANGUAGES:
        page = out / TEXTS[lang]["path"].strip("/") / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(template.render(build_context(lang)), encoding="utf-8")
    return out / "index.html"


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
