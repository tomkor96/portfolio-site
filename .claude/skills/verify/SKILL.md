---
name: verify
description: Run the full check matrix (ruff lint + format, pytest, site build, Docker image build) and report pass/fail per step. Use before opening a pull request or when asked to verify the whole project.
---

Run from the repository root, in this order, stopping at the first failure:

1. `uv sync --locked`
2. `uv run ruff check .` and `uv run ruff format --check .`
3. `uv run pytest`
4. `uv run python build.py`
5. `docker build -t portfolio-site:verify .` — skip with "not run (Docker not available)" when
   `docker version` fails; CI builds the image and smoke-tests it (`/healthz`, CSP header, CV) anyway.

Then report:

- one line per step: pass, fail, or not run (because an earlier step failed or Docker is missing);
- for a failure: the failing file and line or test name, the relevant output, and the root cause.

Fix the root cause rather than loosening a check. If a fix needs a change to a test's expectations,
say why the old expectation was wrong.

For template or CSS changes also look at the page: `uv run python -m http.server -d dist 8000`, or
a headless screenshot (desktop 1280 px and mobile 390 px — headless Edge/Chrome won't shrink the
window below ~500 px, so render the page inside a 390 px `<iframe>` for the mobile check). Check both
themes. A `ruff format` failure on a file you didn't touch usually means CRLF line endings.
