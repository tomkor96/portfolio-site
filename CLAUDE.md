# Portfolio — instructions for Claude

A static one-page portfolio (https://tkoralewski.toadres.pl), built from `data.py` with Jinja2 and
served by nginx in Docker. The user writes in Polish; reply in Polish. Overview and commands: @README.md

## Workflow

- `main` changes only through pull requests. Work on a branch `feat/*`, `fix/*` or `chore/*`; the
  guard hook blocks pushes to `main`.
- Commits, PR titles and PR descriptions in English, as conventional commits with an optional scope,
  e.g. `feat(projects): add Python Digest`, `fix: …`, `chore: …`, `docs: …`, `ci: …`. PRs are
  squash-merged, so the PR title becomes the commit on `main`.
- Before opening a PR: content-only changes in `data.py` → `uv run pytest`; template, CSS, JS,
  Dockerfile or `nginx.conf` changes → full `/verify` and a look at the page (desktop + mobile,
  both themes); review non-trivial changes with the built-in `/code-review`.
- Open the PR with `/dev-kit:pr-open`; red CI → `/dev-kit:ci-fix`.
- Merge only with green CI (`gh pr merge --squash --delete-branch`). Commit, push, merge and deploy
  only when the user asks. Deploy is the user's `/deploy` command; before any other work on the
  server (nginx, cron) read the server facts in `.claude/skills/deploy/SKILL.md`.

## Conventions

- Content (texts, projects, dates) lives only in `data.py`; templates hold layout and fixed UI
  labels. UI text is Polish, lowercase headings are intentional.
- Optional project fields (`address`, `photo_urls`, `featured`) are read with `.get()` in
  templates: Jinja runs with `StrictUndefined`, so a missing key fails the build instead of
  rendering empty.
- Screenshots are stored in `static/img/` and referenced by relative path; no hotlinked images.
- Code comments in English, only where they explain something the code doesn't. Files use LF; the
  PostToolUse hook runs `ruff format` on every Python file Claude edits.

## Security

- The container sends `Content-Security-Policy: default-src 'self'`: no inline `<script>`, no
  `style=""` attributes, no third-party scripts, fonts or images. `tests/test_build.py` enforces it.
  Colors and themes go through CSS custom properties in `static/style.css`.
- Links that open a new tab carry `rel="noopener"`.
