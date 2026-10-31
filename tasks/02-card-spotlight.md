# 02 — Card spotlight that follows the cursor

PR 1 · Status: removed — shipped in PR #5, taken out at the user's request (they didn't like it)

## Goal

A soft accent-colored glow under the cursor on project cards (and skill tiles), like rauno.me /
linear.app. Subtle in both themes.

## Plan

- `main.js`: on `pointermove` over `.card`/`.skill`, set `--x`/`--y` custom properties via
  `style.setProperty` (CSSOM — allowed by the CSP, unlike `style=""` attributes).
- CSS: `::before` with a `radial-gradient` at `var(--x) var(--y)`, fading in on hover; the border
  brightens under the cursor too.
- Off for touch devices (`@media (hover: hover)`) and `prefers-reduced-motion`.
