# 01 — Lighter screenshots

PR 1 · Status: done (PR #5)

## Goal

Screenshots are PNGs of 44 KB–1.1 MB (≈3.9 MB total). Serve WebP instead, with a small
thumbnail for the card and the full size for the lightbox.

## Plan

- `scripts/optimize_images.py` (Pillow, dev dependency only): for every source in `assets/img/`
  write `static/img/<name>.webp` (max 1600 px wide) and `static/img/<name>-thumb.webp` (640 px).
- Sources move from `static/img/*.png` to `assets/img/` (not shipped in the image).
- `data.py` keeps one name per screenshot; the template builds thumb/full URLs, with
  `width`/`height` attributes to avoid layout shift.
- Test: every referenced image exists; no PNG/JPG left under `static/img/`.

## Done when

Total `static/img/` size is a fraction of today's, cards load thumbnails, lightbox loads full size.
