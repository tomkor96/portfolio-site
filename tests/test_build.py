import datetime as dt
from html.parser import HTMLParser
from pathlib import Path

import pytest

import data as site_data
from build import build, month_year, slug, years_since


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
        self._in_script = tag == "script" and "src" not in values

    def handle_data(self, data: str) -> None:
        if self._in_script and data.strip():
            self.inline_scripts += 1

    def handle_endtag(self, tag: str) -> None:
        self._in_script = False


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str, LinkCollector]:
    out = tmp_path_factory.mktemp("dist")
    page = build(out)
    html = page.read_text(encoding="utf-8")
    parser = LinkCollector()
    parser.feed(html)
    return out, html, parser


def test_every_project_is_rendered(site):
    _, html, _ = site
    for project in site_data.PROJECTS:
        assert project["title"] in html
        if project.get("address") and not project.get("offline"):
            assert f'href="{project["address"]}"' in html


def test_local_links_resolve(site):
    out, _, parser = site
    local = [r for r in parser.refs if not r.startswith(("http", "mailto:", "#"))]
    assert local, "expected static assets and the CV"
    for ref in local:
        assert (out / ref.split("?")[0]).is_file(), f"missing {ref}"


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
    images = [r for r in parser.refs if r.startswith("static/img/")]
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
    for project in site_data.PROJECTS:
        if project.get("offline"):
            assert f'href="{project["address"]}"' not in html


def test_years_since():
    assert years_since("2024-08-01", dt.date(2026, 7, 31)) == 1
    assert years_since("2024-08-01", dt.date(2026, 8, 1)) == 2
    assert years_since("2026-01-01", dt.date(2026, 2, 1)) == 1
