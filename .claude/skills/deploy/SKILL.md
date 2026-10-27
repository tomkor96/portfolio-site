---
name: deploy
description: Deploy the current origin/main to production (mikr.us jeff190, https://tkoralewski.toadres.pl) with health checks and a server log entry.
disable-model-invocation: true
---

Production runs on mikr.us server `jeff190` in `/root/apps/portfolio-site`. Use the `mcp__mikrus__exec`
tool (`srv: "jeff190"`). Each call has a ~60 s limit and a `sleep` longer than ~30 s fails the
call, so long work runs in the background and is polled.

## 1. Preconditions — stop and report if any fails

- Locally: `git fetch origin` and confirm the target is `origin/main` (deploys come only from main).
- CI is green for that commit: `gh run list --branch main --limit 3` (status `completed`, conclusion
  `success` for the commit being deployed). Shortcut for a squash merge while that run is still
  going: take `N` from `(#N)` in the commit subject, `git fetch -q origin pull/N/head`, and when
  `git rev-parse origin/main^{tree}` equals `git rev-parse FETCH_HEAD^{tree}` and every check in
  `gh pr view N --json statusCheckRollup` is `SUCCESS`, the same files already passed CI — don't wait.
- On the server the working tree is clean: `cd /root/apps/portfolio-site && git status --porcelain`.

## 2. What changes

On the server: `git rev-parse --short HEAD` (the running version) and `git fetch -q && git log
--oneline HEAD..origin/main`. Show the user the list. There is no database, so no backup step.

## 3. Build and start (background)

```sh
cd /root/apps/portfolio-site && git pull -q && git log --oneline -1
(nohup sh -c 'docker compose build -q && docker compose up -d' > /tmp/portfolio-deploy.log 2>&1 &) && echo started
```

Poll with `sleep 25; tail -3 /tmp/portfolio-deploy.log; docker ps --filter name=portfolio --format
'{{.Names}} {{.Status}} {{.CreatedAt}}'` until the container is recreated and `healthy`. The old
container keeps serving while the image builds; the swap itself takes a few seconds.

## 4. Verify

- `docker logs --tail 20 portfolio`: no `[emerg]` or `[error]` lines.
- `curl -s -o /dev/null -w '%{http_code}' https://tkoralewski.toadres.pl/` → `200`, and the body
  contains a project title from `data.py` (`curl -s … | grep -c 'Python Digest Polska'`).
- `curl -sI https://tkoralewski.toadres.pl/ | grep -i content-security-policy` — the header comes
  from the container's `nginx.conf`.
- `curl -s -o /dev/null -w '%{http_code}' https://tkoralewski.toadres.pl/Tomasz_Koralewski_CV.pdf` → `200`.

## 5. Record

Append a dated section to `/root/MCP_documentation.md`: deployed commit, anything unusual. Then
clean up: `docker image prune -f` and `docker builder prune -f --filter until=168h`.

## Rollback

`git checkout <previous sha>` on the server, rebuild as in step 3, then `git checkout main` once a
fix is merged. The site is stateless, so a rollback never loses data.

## Live status cron (one-time setup, then only check it)

`scripts/live_status.py` (system `python3`, stdlib only) checks the projects and the latest Python
Digest issue and writes `runtime/live.json`, bind-mounted into the container at `/live/`. Set up once:

```sh
mkdir -p /root/apps/portfolio-site/runtime
cat > /etc/cron.d/portfolio-site <<'CRON'
# Portfolio: project status + latest Python Digest issue for the "live" badges
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/5 * * * * root cd /root/apps/portfolio-site && /usr/bin/flock -n /run/portfolio-live.lock /usr/bin/python3 scripts/live_status.py >> /var/log/portfolio-live.log 2>&1
CRON
cd /root/apps/portfolio-site && python3 scripts/live_status.py --verbose
```

Verify: `curl -s https://tkoralewski.toadres.pl/live/live.json` shows a fresh `checked_at`. The log
gets lines only on warnings (an app unreachable, the issue block not found).

## One-time switch from Streamlit (first deploy of the static site)

Until this is done the reverse proxy points at the old Streamlit container. Skip the section once
`grep -c streamlit /root/apps/nginx-proxy/nginx.conf` prints `0`.

1. Ask the user before touching nginx: it fronts other apps too and restarting it briefly
   interrupts them.
2. Run steps 1–3. `docker compose up -d` replaces `streamlit-portfolio` with `portfolio`; the site
   returns 502 until nginx is switched, so do the next step right away.
3. In the `server_name tkoralewski.toadres.pl` block of `/root/apps/nginx-proxy/nginx.conf`, set the
   upstream to `http://portfolio:8080` (rename the variable to `$portfolio_upstream`) and drop the
   Streamlit-only lines (`Upgrade`/`Connection` headers, `proxy_read_timeout 86400`,
   `proxy_buffering off`). Keep the rate limits and security headers. Write the whole file with
   `cat > file` (see server facts), test it, `docker restart nginx-reverse-proxy`.
4. Continue with step 4.

## Server facts

- nginx runs in the `nginx-reverse-proxy` container; `/root/apps/nginx-proxy/nginx.conf` is a
  single-file bind mount: edit with `cat > file` (never `sed -i` — new inode, the container keeps
  the old file; the guard hook blocks it), test in a throwaway container
  (`docker run --rm --network reverse-proxy-network -v /root/apps/nginx-proxy/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t`),
  then `docker restart nginx-reverse-proxy`. The default `return 444` server block stays; change it
  only with the user's consent.
- A new Mikrus subdomain (`mcp__mikrus__domains`, port 80) is validated against the bare IPv6,
  which `return 444` drops, so adding one fails. With the user's consent: switch the default block
  to `return 404`, restart, add the subdomain, restore `return 444`, restart (done for `tkstats`).
- Upstreams are resolved per request (`resolver 127.0.0.11` + a variable in `proxy_pass`), so a
  recreated container never needs an nginx reload.
- The same server runs home-library (`/root/apps/home-library`, has its own `/deploy`), Python
  Digest Polska (`pdp-web`, `pdp-db`) and `sqlite-web`. Don't touch their containers.
- `/etc/cron.d/portfolio-site` runs `scripts/live_status.py` every 5 minutes (log
  `/var/log/portfolio-live.log`); `runtime/` is not in git. A missing or stale `live.json` (>30 min)
  hides the badges instead of showing a false "live".
- Analytics: GoatCounter container `goatcounter` from `ops/goatcounter/compose.yaml` (run
  `docker compose up -d` in `/root/apps/portfolio-site/ops/goatcounter` when that file changes),
  data in the `goatcounter_goatcounter-data` volume, dashboard `https://tkstats.toadres.pl`
  (nginx-proxy server block, Mikrus subdomain → port 80). The portfolio forwards `/count` to it.
  Admin password: `/root/apps/goatcounter-admin-password` (root-only; never print it).
- The portfolio container is read-only (`read_only: true`, `/tmp` as tmpfs) and listens on 8080 as
  a non-root user; logs are capped at 3 × 10 MB.
