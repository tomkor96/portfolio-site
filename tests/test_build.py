import datetime as dt
from html.parser import HTMLParser
from pathlib import Path

import pytest

import data as site_data
from build import build, month_year, years_since


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.inline_styles: list[str] = []
        self.inline_scripts = 0
        self._in_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        for name in ("href", "src"):
            if values.get(name):
                self.refs.append(values[name])
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("style"):
            self.inline_styles.append(tag)
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
        if project.get("address"):
            assert f'href="{project["address"]}"' in html


def test_new_projects_are_listed(site):
    _, html, _ = site
    assert "https://pythondigest.toadres.pl/" in html
    assert "https://biblioteczka.toadres.pl/" in html


def test_local_links_resolve(site):
    out, _, parser = site
    local = [r for r in parser.refs if not r.startswith(("http", "mailto:", "#"))]
    assert local, "expected static assets and the CV"
    for ref in local:
        assert (out / ref).is_file(), f"missing {ref}"


def test_anchors_resolve(site):
    _, _, parser = site
    for ref in parser.refs:
        if ref.startswith("#") and len(ref) > 1:
            assert ref[1:] in parser.ids, f"no element with id {ref}"


def test_skills_order(site):
    _, html, _ = site
    names = [skill["name"] for skill in site_data.SKILLS]
    assert "MS Excel" not in names
    assert "<h3>Claude i Claude Code</h3>" in html


def test_page_fits_the_csp(site):
    # nginx sends default-src 'self': no inline scripts or styles, no third-party assets.
    _, _, parser = site
    assert parser.inline_styles == []
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


def test_years_since():
    assert years_since("2024-08-01", dt.date(2026, 7, 31)) == 1
    assert years_since("2024-08-01", dt.date(2026, 8, 1)) == 2
    assert years_since("2026-01-01", dt.date(2026, 2, 1)) == 1
