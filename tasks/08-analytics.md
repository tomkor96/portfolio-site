# 08 — Private analytics (GoatCounter)

PR 4 · Status: todo

## Goal

Cookie-free visit stats: pages, referrers, CV downloads, outbound clicks to projects.

## Plan

- GoatCounter in its own container on jeff190 (`/root/apps/goatcounter`, SQLite volume, ~20–30 MB
  RAM), on `reverse-proxy-network`; dashboard at `stats.tkoralewski.toadres.pl` (to confirm).
- Counting without breaking the CSP: the portfolio's nginx proxies `/count` to GoatCounter and
  serves `count.js` from `static/` → everything stays `'self'`.
- Events: CV download, project link clicks, lightbox opens (`goatcounter.count({event: true})`).
- No IP storage beyond GoatCounter defaults; mention analytics in the footer.

## Open

- Subdomain spelling (answer was "statstkoralewski.toadres.pl") and how `*.toadres.pl` DNS is
  managed — needed before the nginx server block.
