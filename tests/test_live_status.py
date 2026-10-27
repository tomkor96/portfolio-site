import json
from pathlib import Path

from scripts.live_status import is_up, parse_latest_issue, write_atomic

FIXTURES = Path(__file__).parent / "fixtures"


def test_latest_issue_from_saved_home_page():
    html = (FIXTURES / "pythondigest-home.html").read_text(encoding="utf-8")
    issue = parse_latest_issue(html, "https://pythondigest.toadres.pl/")
    assert issue == {
        "number": 13,
        "title": "Jak zbudować agenta AI w czystym Pythonie, projektować wtyczki i uruchamiać "
        "duże modele na słabym GPU",
        "url": "https://pythondigest.toadres.pl/wydania/jak-zbudowac-agenta-ai-w-czystym-pythonie"
        "-projektowac-wtyczki-i-uruchamiac-duze-modele-na-slabym-gpu/",
        "date": "17 października 2026",
    }


def test_no_issue_block_gives_none():
    assert parse_latest_issue("<html><body>przerwa techniczna</body></html>", "https://x/") is None


def test_is_up():
    assert is_up(200) and is_up(303)
    assert not is_up(0) and not is_up(404) and not is_up(502)


def test_write_atomic_replaces_the_file(tmp_path):
    target = tmp_path / "runtime" / "live.json"
    write_atomic(target, {"a": 1})
    write_atomic(target, {"a": 2})
    assert json.loads(target.read_text(encoding="utf-8")) == {"a": 2}
    assert [p.name for p in target.parent.iterdir()] == ["live.json"]
