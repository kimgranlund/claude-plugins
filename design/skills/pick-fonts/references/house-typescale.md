# The house typescale — the fixed 11-voice size table

Ratified 2026-07-12 (standing user ruling; source of record: the ultimate-tokens type engine,
`src/engine/type.mjs` `SIZES`, shipped in PR #279). The scale is a **fixed, hand-authored table**,
not a modular scale — matching Material 3's own approach: one fixed scale; treatments and brands
vary *styling* (font, weight, tracking, leading, case), **never the numbers**. `ratio` is retired.
Every voice is a uniform 3-step **SM / MD / LG** ramp.

Every scale-design ask starts here. Deviations: a platform-owned scale overrides on its own turf
(Material's `--md-sys-typescale-*` typescale, Apple HIG text styles); a producer may ship
Base-only (no breakpoint modes); anything else needs a stated reason, never silence.

## The table (LG / MD / SM per breakpoint, px)

| Voice | Desktop ≥1280 | Tablet ≥992 | Mobile ≤476 |
|---|---|---|---|
| **Display** | 120 / 96 / 72 | 88 / 72 / 60 | 64 / 56 / 48 |
| **Headline** | 48 / 40 / 32 | 44 / 36 / 30 | 40 / 32 / 28 |
| **Sub-heading** | 40 / 34 / 28 | 36 / 32 / 26 | 32 / 28 / 24 |
| **Title** | 40 / 32 / 24 | 36 / 30 / 24 | 32 / 28 / 22 |
| **Sub-title** | 32 / 24 / 18 | 28 / 22 / 18 | 24 / 20 / 16 |
| **Lead** | 28 / 24 / 20 | 26 / 22 / 20 | 24 / 20 / 18 |
| **Body** | 16 / 15 / 14 | 16 / 15 / 14 | 16 / 15 / 14 |
| **Code** | = Body | = Body | = Body |
| **Label** | 14 / 13 / 12 | 14 / 13 / 12 | 13 / 12 / 12 |
| **Kicker** | = Label | = Label | = Label |
| **Tiny** | 12 / 11 / 10 | 12 / 11 / 10 | 11 / 11 / 10 |

The engine's authored `SIZES` table is the Desktop column (SM/MD/LG ascending); the Tablet and
Mobile columns are its hierarchy-aware breakpoint compression — **body-class voices (Body · Label
· Tiny · Code) are frozen or near-frozen across breakpoints, headings compress partially, Display
compresses steeply.** That asymmetry is the system, not a defect to normalize.

## Aliases and scaling knobs

- **Code aliases Body's triplet; Kicker aliases Label's** — same numbers, mono font only; they are
  not separate size registers.
- **Label sits a deliberate step below Body, above Tiny** (explicit 2026-07-12 ruling — a
  Label-equals-Body variant was considered and rejected).
- **`bodyBase` (default 15 = Body MD)** scales the WHOLE table proportionally
  (factor = bodyBase/15) — one knob, every voice together, snapping to a nice-number ladder when
  the factor ≠ 1. Per-cell `overrides` are the escape hatch for modifying a single default.

## Voice roles (the taxonomy this table sizes)

Display · Headline · Sub-heading (a bold all-caps CONTEXT heading above a list/grid — not a
subordinate h2) · Title (a smaller headline) · Sub-title (a smaller sub-heading, mono-by-default,
prose flow) · Lead (standfirst + pull-quotes) · Body (prose + fine-print at its SM step) · Code ·
Label (interface chrome) · Kicker (overline) · Tiny (captions, small supporting text). The
consumption rules — which voice for which text, the box-voice `-line-single` set, paragraph
rhythm — are `font-token-rules`' canon; this file carries only the design-time size table.
