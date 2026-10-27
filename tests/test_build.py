import datetime as dt
from html.parser import HTMLParser
from pathlib import Path

import pytest

import data as site_data
from build import LANGUAGES, build, localize, month_year, slug, years_since
from texts import TEXTS


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.inline_styles: list[str] = []
        self.event_handlers: list[str] = []
        self.inline_scripts = 0
        self._in_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        for name in ("href", "src"):
            if values.get(name):
                self.refs.append(values[name])
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("style") or tag == "style":
            self.inline_styles.append(tag)
        self.event_handlers += [name for name in values if name.startswith("on")]
        # JSON-LD is a data block, not script: the CSP doesn't apply to it.
        self._in_script = (
            tag == "script" and "src" not in values and values.get("type") != "application/ld+json"
        )

    def handle_data(self, data: str) -> None:
        if self._in_script and data.strip():
            self.inline_scripts += 1

    def handle_endtag(self, tag: str) -> None:
        self._in_script = False


@pytest.fixture(scope="module")
def dist(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("dist")
    build(out)
    return out


@pytest.fixture(params=LANGUAGES)
def site(request: pytest.FixtureRequest, dist: Path) -> tuple[Path, str, LinkCollector]:
    """(directory of the page, its HTML, parsed links) — every page test runs for PL and EN."""
    page_dir = dist / TEXTS[request.param]["path"].strip("/")
    html = (page_dir / "index.html").read_text(encoding="utf-8")
    parser = LinkCollector()
    parser.feed(html)
    return page_dir, html, parser


def test_every_project_is_rendered(site):
    page_dir, html, _ = site
    lang = "en" if page_dir.name == "en" else "pl"
    for project in localize(site_data.PROJECTS, lang):
        assert project["title"] in html
        if project.get("address") and not project.get("offline"):
            assert f'href="{project["address"]}"' in html


def test_local_links_resolve(site):
    page_dir, _, parser = site
    local = [r for r in parser.refs if not r.startswith(("http", "mailto:", "#"))]
    assert local, "expected static assets and the CV"
    for ref in local:
        target = (page_dir / ref.split("?")[0]).resolve()
        assert target.is_file() or (target / "index.html").is_file(), f"missing {ref}"


def test_anchors_resolve(site):
    _, _, parser = site
    for ref in parser.refs:
        if ref.startswith("#") and len(ref) > 1:
            assert ref[1:] in parser.ids, f"no element with id {ref}"


def test_page_fits_the_csp(site):
    # nginx sends default-src 'self': no inline scripts or styles, no third-party assets.
    _, _, parser = site
    assert parser.inline_styles == []
    assert parser.event_handlers == []
    assert parser.inline_scripts == 0
    for ref in parser.refs:
        if ref.startswith("http"):
            assert not ref.endswith((".js", ".css", ".png", ".jpg", ".svg")), ref


@pytest.mark.parametrize(
    ("value", "expected"),
    [("2024-08-01", "sie 2024"), ("2016-10-01", "paź 2016"), ("2020", "2020"), (None, "obecnie")],
)
def test_month_year(value, expected):
    assert month_year(value) == expected


def test_gallery_links_open_the_lightbox(site):
    # main.js groups slides per gallery; a link without data-lightbox would open a new tab instead.
    _, html, parser = site
    images = [r for r in parser.refs if "static/img/" in r and "portrait" not in r]
    assert images
    assert html.count("data-lightbox") == len(images) // 2
    assert 'id="lightbox"' in html


def test_assets_are_cache_busted(site):
    _, _, parser = site
    assets = [r for r in parser.refs if r.endswith((".css", ".js")) or "?v=" in r]
    assert assets and all("?v=" in r for r in assets)


def test_build_refuses_to_clear_the_project():
    with pytest.raises(ValueError):
        build(Path(__file__).resolve().parents[1])


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Tailwind CSS", "tailwind-css"),
        ("Obsługa klienta", "obsluga-klienta"),
        ("API OpenAI", "api-openai"),
    ],
)
def test_slug(value, expected):
    assert slug(value) == expected


def test_offline_project_is_not_linked(site):
    _, html, _ = site
    for project in localize(site_data.PROJECTS, "pl"):
        if project.get("offline"):
            assert f'href="{project["address"]}"' not in html


def test_images_are_webp(dist):
    images = list((dist / "static" / "img").iterdir())
    assert images and all(image.suffix == ".webp" for image in images)


def test_link_preview(dist):
    site_url = site_data.PROFILE["site_url"]
    for lang, image in (("pl", "og.png"), ("en", "og-en.png")):
        html = (dist / TEXTS[lang]["path"].strip("/") / "index.html").read_text(encoding="utf-8")
        assert (dist / "static" / image).is_file()
        assert f'content="{site_url}/static/{image}"' in html
        assert f'hreflang="en" href="{site_url}/en/"' in html
        assert '"@type": "Person"' in html


def _half_translated(value, path="data"):
    """Paths of {"pl": ...} dicts that are missing the other language."""
    if isinstance(value, dict):
        if value and set(value) <= set(LANGUAGES):
            return [] if set(value) == set(LANGUAGES) else [path]
        return [p for k, v in value.items() for p in _half_translated(v, f"{path}.{k}")]
    if isinstance(value, list):
        return [p for i, v in enumerate(value) for p in _half_translated(v, f"{path}[{i}]")]
    return []


def test_translations_are_complete():
    content = [site_data.PROFILE, site_data.EDUCATION, site_data.EXPERIENCE]
    content += [site_data.SKILLS, site_data.CERTS, site_data.PROJECTS]
    assert _half_translated(content) == []
    assert set(TEXTS["pl"]) == set(TEXTS["en"])


def test_english_page_has_no_polish_ui(dist):
    html = (dist / "en" / "index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in html
    for label in ("napisz do mnie", "doświadczenie", "umiejętności", "obecnie", "Zrzut ekranu"):
        assert label not in html


def test_years_since():
    assert years_since("2024-08-01", dt.date(2026, 7, 31)) == 1
    assert years_since("2024-08-01", dt.date(2026, 8, 1)) == 2
    assert years_since("2026-01-01", dt.date(2026, 2, 1)) == 1
