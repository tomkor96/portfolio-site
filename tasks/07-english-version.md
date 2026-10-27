# 07 — English version

PR 3 · Status: done (PR #8; latest issue hidden on /en/ in PR #9)

## Goal

`/en/` with the full content in English and a PL/EN switch in the top bar.

## Plan

- `data.py` → content per language (`pl`/`en`); UI labels move from the template into a small
  `TEXTS` dict per language. `build.py` renders `index.html` and `en/index.html`.
- `<html lang>`, `hreflang` alternates, `og:locale`, a separate OG image text if needed.
- CV: EN links the Polish PDF, labelled "CV (PL)" (user's choice).
- Translation drafted by Claude; the user reviews before merge.
- Tests: both pages build, every PL key has an EN counterpart, links resolve from `/en/`.
