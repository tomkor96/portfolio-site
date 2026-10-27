# 08 — Private analytics (GoatCounter)

PR 4 · Status: done (PR #9)

## Goal

Cookie-free visit stats: pages, referrers, CV downloads, outbound clicks to projects.

## Plan

- GoatCounter 2.6 in its own container (`ops/goatcounter/compose.yaml`, run from that directory
  on jeff190; SQLite in the `goatcounter-data` volume, `mem_limit: 128m`), on `reverse-proxy-network`.
- Dashboard: `https://tkstats.toadres.pl` — free Mikrus subdomain (labels are 4–12 characters, so
  the requested "statstkoralewski" didn't fit; the user picked `tkstats`) → port 80 → nginx-proxy
  server block → `goatcounter:8080`.
- Counting without breaking the CSP: the portfolio's nginx proxies `/count` to GoatCounter with
  `Host: tkstats.toadres.pl`; `main.js` sends hits with `sendBeacon` — no third-party script.
- Pageviews plus events: `cv-download`, `mailto`, `gallery: <project>`, `out: <host/path>`.
  Skipped off HTTPS (local previews) and when the browser sends Do Not Track.
- Footer mentions cookie-free stats.
- Admin account: created on the server; the password is in a root-only file (never printed).
