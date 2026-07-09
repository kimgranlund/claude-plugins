# Grid and construction — how the major systems build an icon

Researched 2026-07-09 from primary sources (m2/m3.material.io, fonts.google.com,
developer.apple.com, carbondesignsystem.com, atlassian.design, fluent2.microsoft.design).
Unverified edges at the bottom — don't invent them.

## Per-system construction table

| System | Canvas | Live area / margin | Stroke | Terminals | Corners |
|---|---|---|---|---|---|
| Material Symbols | 24×24 dp | 2 dp padding | 2 dp (1.5 dp only for complex multi-curve icons) | — | 2 dp on silhouettes; NOT on strokes ≤2 dp |
| SF Symbols | 100×100 pt template (1000×1000-unit grid) | 8-unit safe margin | 10 units at Regular; scales with weight | — | 10 units (rounded) |
| Carbon | 16 px primary (20/24/32 variants) | 2 px padding at 32 | **filled at 16 px** (strokes break at glyph size); 2 px stroke at 20+ | square | not published |
| Atlassian | 16 px (12 px small; 24 px legacy, deprecated as "visually heavy") | — | 1.5 px | square | rounded EXTERNAL, sharp INTERNAL |
| Fluent 2 | 16 px system / 48 px product base (4 px base grid) | — | token-driven, values unpublished | — | not published |
| Phosphor (house default — see style-and-metaphor.md) | 16×16 px | — | six weights: Thin/Light/Regular/Bold/Fill/Duotone; "raw stroke information retained" | — | not published |

Keyline shapes (Material): circle, square, rectangle plus orthogonals/diagonals — geometric
guides that keep different silhouettes at equal visual weight; circles overshoot the grid edge
for optical balance (m1.material.io metrics-keylines). Carbon's mechanical version of the same
idea: no decimal X/Y coordinates — every vector lands on the pixel grid.

## The two variable-icon models

- **Material Symbols — four variable-font axes** (m3.material.io/blog/introducing-symbols;
  fonts.google.com glossary): **weight** 100–700 (default 400) · **fill** 0–1 (0 outlined, 1
  filled — one file, animatable state) · **grade** −25–200 (default 0; emphasis without size
  change, matches text grades) · **optical size** 20–48 px (default 24; stroke auto-compensates
  per size, no manual correction).
- **SF Symbols — 9 weights × 3 scales** (Ultralight→Black; Small/Medium/Large; Regular+Medium
  the defaults), drawn to align with San Francisco: symbols auto-center to cap height, and the
  baseline is deliberately flexible per glyph (∞ floats, folder descends) — optical balance
  outranks the grid (developer.apple.com HIG sf-symbols).

## Cross-system laws worth stating as defaults

1. **One stroke weight per family** — every system holds stroke uniform within a size; weight
   changes come from the system's axis/weight mechanism, never per-icon.
2. **Small sizes change technique, not just scale**: Carbon switches 16 px icons to FILLED;
   Fluent simplifies detail below 48 px; Material moves the opsz axis. Scaling a 24 px outline
   down to 16 px is the documented failure mode.
3. **Optical beats mathematical**: circles overshoot, SF baselines flex — a custom icon matched
   numerically to the grid but visually lighter/heavier than its peers is wrong (Carbon states
   equal-visual-weight as a rule).

## Unverified (2026-07-09)

Fluent 2 stroke-weight token values; Material's exact overshoot dimensions; Carbon corner radii;
Atlassian keyline dimensions; SF Symbols margin-asymmetry worked examples.
