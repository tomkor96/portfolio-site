# Portfolio — instructions for Claude

Static one-page portfolio of Tomasz Koralewski (https://tkoralewski.toadres.pl): `data.py` →
`build.py` (Jinja2) → `dist/` → nginx in Docker on mikr.us `jeff190`. The user writes in Polish;
reply in Polish. Code, comments, commits and PRs in English.

## Commands

```sh
uv sync                                        # deps (uv only, no pip)
uv run python build.py                         # build → dist/index.html
uv run python -m http.server -d dist 8000      # preview
uv run ruff check . && uv run ruff format --check .
uv run pytest                                  # tests/test_build.py
```

`/verify` runs the whole matrix (including `docker build`); `/deploy` is the user's command.

## Where things live

- `data.py` — all content: profile, projects, experience, skills, education, certificates.
- `templates/index.html` — the page; `templates/icons.html` — inline SVG icon macro.
- `static/` — `style.css` (theme tokens), `theme.js` (runs in `<head>`), `main.js`, `img/`.
- `nginx.conf` — the in-container server: CSP and other headers, caching, `/healthz`.
- `.claude/skills/deploy/SKILL.md` — server facts; read it before any work on the server.

## Rules

- IMPORTANT: the CSP is `default-src 'self'`. No inline `<script>` (JSON-LD data blocks excepted),
  no `style=""` (set custom properties from JS via `style.setProperty`), no third-party scripts,
  fonts or images; `tests/test_build.py` fails on them.
- Images: add the PNG to `assets/img/`, run `scripts/optimize_images.py`, reference
  `static/img/<name>.webp` in `data.py` (cards load `-thumb.webp` automatically). Profile, tagline
  or portrait change → rerun `scripts/og_image.py`. Pillow is a dev dependency only.
- Planned work lives in `tasks/NN-*.md`; update the task's status when its PR merges.
- Content changes go to `data.py` only; templates hold layout and fixed UI labels. UI text is
  Polish and headings are lowercase on purpose.
- Jinja runs with `StrictUndefined`: read optional keys with `.get()` (`address`, `photo_urls`,
  `featured`, `end_date`). `"featured": True` puts a project first with the "live" badge.
- Theme colors are CSS custom properties: change both the dark defaults and the light block
  (it appears twice: under `prefers-color-scheme` and under `[data-theme="light"]`).
- New-tab links carry `rel="noopener"`. Don't add runtime dependencies without asking.

- "live" badges and the latest Python Digest issue come from `/live/live.json`, written on the
  server by `scripts/live_status.py` (cron, stdlib only, must run on the server's Python 3.12).
  Its HTML parser is tested against `tests/fixtures/pythondigest-home.html`; refresh the fixture
  when the newsletter's home page markup changes. Tests never hit the network.

## Workflow

- `main` changes only through PRs from `feat/*`, `fix/*` or `chore/*`; the guard hook blocks pushes
  to `main`. Conventional commits (`feat(projects): …`, `fix: …`, `ci: …`); squash-merged.
- Before a PR: `data.py`-only changes → `uv run pytest`; template, CSS, JS, Dockerfile or
  `nginx.conf` → `/verify` plus a look at the page in both themes at 1280 px and 390 px.
  Headless Edge/Chrome won't render narrower than ~500 px: for 390 px load the page in a 390 px
  `<iframe>`. Below-the-fold images are `loading="lazy"` and look empty in full-page screenshots.
- Open PRs with `/dev-kit:pr-open`; red CI → `/dev-kit:ci-fix`. Commit, push, merge and deploy only
  when the user asks.

## Environment quirks

- Windows dev machine: files are LF (`.gitattributes`); the PostToolUse hook runs `ruff format`
  on edited Python files. Docker Desktop is often off locally — CI builds and smoke-tests the image.
- On the server never `sed -i` `nginx.conf` (bind mount; the guard hook blocks it).
