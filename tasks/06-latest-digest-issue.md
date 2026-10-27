# 06 — Link to the latest Python Digest Polska issue

PR 2 · Status: in review

## Goal

Hero and project card show "ostatnie wydanie: #13 — <title> →" pointing at the current issue.

## What we know (checked 2026-10-27)

- No RSS/Atom feed (`/feed/`, `/rss/` → 404); `sitemap.xml` exists but has no titles.
- The home page has an "Ostatnie wydanie" section linking `/wydania/<slug>/` with the title.

## Plan

- The same cron job as task 05 reads the home page, extracts the first `/wydania/<slug>/` link,
  title and issue number (`html.parser`, stdlib) and adds `latest_issue` to `live.json`.
- `main.js` fills the hero line and the card; fallback text links to `/wydania/`.
- Parser tested against a saved copy of the page in `tests/fixtures/`.
- Better long term: a small JSON/RSS endpoint in the python-digest-polska app (separate repo).
