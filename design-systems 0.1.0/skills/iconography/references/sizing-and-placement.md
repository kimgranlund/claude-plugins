# Sizing and placement — ladders, targets, alignment

Researched 2026-07-09 (m2/m3.material.io, carbondesignsystem.com, developer.apple.com,
fluent2.microsoft.design, w3.org; CSS-Tricks for the alignment math, corroborated practice).

## Published size ladders

| System | Ladder | Default | Notes |
|---|---|---|---|
| Material | 20 · 24 · 40 · 48 dp | 24 dp | the opsz axis range; 20 dp for dense desktop |
| Carbon | 16 · 20 · 24 · 32 px | 16 px | 16/20 px pair with 14/16 px IBM Plex |
| Apple | no fixed ladder | — | SF Symbols scale with text; contexts: nav/toolbar 22 pt, tab bar 25 pt, search 18 pt |
| Fluent 2 | 16 · 48 · 64 · 96 px (12 px informational) | 16 px | pixel-perfect sizes preferred over scaling |

## Icon ≠ target (the legal floor and the system translations)

- **WCAG 2.5.8 Target Size Minimum (AA, WCAG 2.2): 24×24 CSS px** or 24 px spacing between
  targets. **WCAG 2.5.5 (AAA): 44×44.** (w3.org Understanding pages.)
- System translations, all `target = icon + 2×padding`: Material 24 dp icon → **48 dp** target
  (20 → 40); Apple **44 pt** minimum; Carbon **44 px** minimum for any interactive icon;
  Fluent **40 epx**. The glyph is never the hit area — pad the target, don't inflate the glyph.

## Icon-with-text alignment

- Size icons in **em** relative to adjacent text: `1em` default; 0.875–1.25 em by weight needs.
  No system publishes a universal ratio — pick one per context and hold it.
- Prefer **cap-height/baseline alignment over naive vertical centering**: centering breaks on
  wrapped text. Offset math for web: `offset = (line-height − font-size) / 2` (16 px text at
  1.5 line-height → 4 px down-shift). SF Symbols do this automatically against SF Pro — the
  reason Apple contexts need no manual alignment.
- Icon↔label gap: 4–8 px by density (Material buttons 4–6 px).

## Density

Material's density scale (0/−1/−2…) shrinks **spacing and target first, glyph last** — compact
drops a 48 dp target to 40 dp with a 20 dp icon; the glyph never goes below its legibility floor
(the reason ladders bottom out at 16 px with technique changes, per grid-and-construction.md).
Sourcing note: the density mechanics here come from Google-adjacent practitioner writeups
(Material density on the web; a SAS tokens case study), not the M3 spec pages — trust
accordingly.

## Pixel fitting (why icons blur)

Vectors must land on whole-pixel coordinates (Carbon: no decimal X/Y). The half-pixel stroke
problem: a 1 px stroke centered ON a grid line splits 0.5 px each side and anti-aliases — put
1 px stroke centers on half-pixel coordinates (x=6.5) so edges land on pixels. SVG viewBox should
match the design grid (24×24 for a 24 dp icon). Browser sub-pixel layout can still blur at odd
zoom levels — a known, unresolved variance (W3C SVG hinting proposals).
