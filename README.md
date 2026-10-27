# portfolio-site

Tomasz Koralewski's portfolio (https://tkoralewski.toadres.pl). The content lives in `data.py`,
`build.py` renders `templates/` with Jinja2 into a static site in `dist/`, and the Docker image
serves it with unprivileged nginx on port 8080. The UI is in Polish.

## Getting started

```sh
uv sync
uv run python build.py                         # → dist/index.html
uv run python -m http.server -d dist 8000      # http://localhost:8000
```

Docker: `docker compose up -d --build` (needs the external `reverse-proxy-network`; the
container answers on `portfolio:8080`, health check at `/healthz`).

## Layout

| Path                     | What                                                      |
| ------------------------ | --------------------------------------------------------- |
| `data.py`                | profile, experience, projects, skills, education, certs   |
| `templates/`             | `index.html` (one page) and `icons.html` (inline SVG)     |
| `static/`                | CSS, JS (theme toggle, mobile menu), favicon, screenshots |
| `docs/`                  | the CV PDF, copied next to `index.html` on build          |
| `nginx.conf`             | in-container server: CSP, caching, `/healthz`             |

A new project: add a dict to `PROJECTS` in `data.py` (`"featured": True` puts it first with a
"live" badge); screenshots go to `static/img/` and are referenced as `static/img/<file>`.

## Checking changes

```sh
uv run ruff check . && uv run ruff format --check .
uv run pytest
uv run python build.py
docker build -t portfolio-site .
```

Changes go through pull requests (`feat/*`, `fix/*`, `chore/*` branches, conventional commits);
CI runs the same checks.
