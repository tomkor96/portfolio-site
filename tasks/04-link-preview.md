# 04 — Link preview (Open Graph) and structured data

PR 1 · Status: in review

## Goal

A link pasted into LinkedIn, Slack or Messenger shows a designed card instead of bare text.

## Plan

- `scripts/og_image.py` (Pillow, dev only) renders `static/og.png` 1200×630 in the site style:
  dark background, portrait, name, tagline, domain. Committed; rerun when the profile changes.
- `<head>`: absolute `og:image` (+ width/height/alt), `og:url`, `og:locale`, `twitter:card`,
  canonical URL. `PROFILE["site_url"]` holds the domain.
- JSON-LD `Person` (name, jobTitle, url, sameAs LinkedIn/GitHub, image). JSON-LD is a data block,
  not script, so the CSP doesn't block it; the CSP test allows only that type inline.
- Check with LinkedIn Post Inspector after deploy (LinkedIn caches previews for ~7 days).
