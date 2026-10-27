# 05 — "live" badge from the real application status

PR 2 · Status: in review

## Goal

The green badge shows only when the app actually responds; otherwise "offline".

## Plan

- `scripts/live_status.py` (stdlib only), run by cron on jeff190 every 5 minutes: requests each
  project's `address`, records HTTP status, response time and check time, writes
  `/root/apps/portfolio-site/runtime/live.json` atomically (write temp file, rename).
- The file is bind-mounted read-only into the container at `/usr/share/nginx/html/live/`;
  nginx serves it with `Cache-Control: no-cache`. Same origin → CSP unchanged.
- `main.js` fetches `/live/live.json` and switches each badge: live (2xx/3xx) / offline /
  unknown (no data or older than 30 min). Without data the badge stays neutral, never green.
- Cron file `/etc/cron.d/portfolio-site`; documented in the deploy skill's server facts.

## Open

- Projects flagged `offline` in `data.py` stay offline regardless of the check.
