# 03 — Photo in the hero

PR 1 · Status: done (PR #5)

## Goal

The user's portrait next to the name, styled to fit the site rather than look like a pasted ID photo.

## Plan

- Source: `assets/photo-source.jpg` (1786×2500, provided by the user; EXIF stripped on export).
- `scripts/optimize_images.py` crops a square on head and shoulders and exports
  `static/img/portrait.webp` (480 px) — enough for a ~160 px circle at 3× density.
- Styling: circle with an accent ring and a slightly offset dashed outer ring, always in full
  color (a muted/grey filter was tried and rejected by the user); gentle float-in on load.
- Layout: photo beside the name on desktop, above it on mobile.
