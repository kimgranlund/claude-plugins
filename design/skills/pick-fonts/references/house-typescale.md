# The house typescale — the fixed 15-voice size table

Ratified 2026-07-12 (standing user ruling; source of record: the ultimate-tokens type engine,
`src/engine/type.mjs` `SIZES`, shipped in PR #279). The scale is a **fixed, hand-authored table**,
not a modular scale — matching Material 3's own approach: one fixed scale; treatments and brands
vary *styling* (font, weight, tracking, leading, case), **never the numbers**. `ratio` is retired.

**Re-snapshotted 2026-08-20 (TKT-0008, closes #792):** the table grew from 11 to **15 voices** —
five Material 3 baseline (`display`, `headline`, `title`, `label`, `body`) plus ten nonoun
extensions (`sub-heading`, `sub-title`, `lead`, `kicker`, mono siblings of body/label, a `tiny`
micro-voice + its mono sibling, and two dedicated interactive-text voices). **13 of the 15 ride a
uniform 3-step SM/MD/LG ramp; `ui-control` and `ui-widget` are the exception** — they ride the
full 6-step XS…2XL ramp, because control geometry needs a size at every one of its six steps.
`bodyBase`'s default moved 15→16 (Body MD) in the same engine cycle.

Every scale-design ask starts here. Deviations: a platform-owned scale overrides on its own turf
(Material's `--md-sys-typescale-*` typescale, Apple HIG text styles); a producer may ship
Base-only (no breakpoint modes); anything else needs a stated reason, never silence.

## The table (LG / MD / SM per breakpoint, px)

| Voice | Desktop ≥1280 | Tablet ≥992 | Mobile (base) |
|---|---|---|---|
| **Display** | 120 / 96 / 72 | 96 / 80 / 64 | 80 / 72 / 56 |
| **Headline** | 48 / 40 / 32 | 44 / 36 / 32 | 40 / 36 / 28 |
| **Sub-heading** | 40 / 34 / 28 | 36 / 32 / 28 | 36 / 32 / 24 |
| **Title** | 40 / 32 / 24 | 36 / 32 / 24 | 36 / 28 / 22 |
| **Sub-title** | 32 / 24 / 18 | 32 / 24 / 18 | 28 / 22 / 18 |
| **Lead** | 28 / 24 / 20 | 28 / 24 / 20 | 24 / 22 / 20 |
| **Body** | 18 / 16 / 14 | = Desktop | = Desktop |
| **Body-mono** | = Body | = Body | = Body |
| **Label** | 14 / 13 / 12 | = Desktop | = Desktop |
| **Label-mono** | = Label | = Label | = Label |
| **Kicker** | = Label (mono role, uppercase/wide-tracked — its own voice, not a size alias in name only) | = Label | = Label |
| **Tiny** | 11 / 10 / 9 | = Desktop | = Desktop |
| **Tiny-mono** | = Tiny | = Tiny | = Tiny |

| Interactive voice (XS · SM · MD · LG · XL · 2XL) | All breakpoints (frozen — see below) |
|---|---|
| **UI-control** | 12 · 13 · 15 · 16 · 18 · 20 |
| **UI-widget** | 9 · 10 · 11 · 12 · 13 · 14 |

## Breakpoint mechanism (ratified 2026-07-10, `modeFactor`)

Desktop is the **designed layer** (×1 — the hand-authored `SIZES` literals); Tablet and Mobile are
**derived**, not separate hand-authored rows: each step's size scales by a factor
log-interpolated from ×1 at `bodyBase` up to ×`modeFactor` at the ramp's top, so compression is
**hierarchy-aware** — body-class voices (Body · Label · Tiny and their mono/Kicker siblings) stay
frozen or near-frozen, Display compresses the most, mid-scale voices partially. Canonical factors:
**Tablet ×5/6, Mobile ×2/3**. Compressed sizes snap to the nice-number ladder; line-height/tracking/
paragraph rhythm re-derive from the compressed size, never carried as a separate hand-authored set.
`ui-control`/`ui-widget` are effectively frozen across breakpoints because their whole ramp already
sits near `bodyBase`.

CSS emission is **separate self-contained files per breakpoint** (`typeTokensBreakpointCSS`,
#264) — a desktop-anchored base file plus bounded min/max-width override files — not one
mobile-first `@media` sheet.

## Aliases and scaling knobs

- **Body-mono/Label-mono/Tiny-mono/Kicker are not separate size registers** — they ride their
  sibling voice's numbers at every breakpoint; only the 9 non-mono/non-alias voices + the 2
  interactive voices exist as literals in `SIZES`. The mono siblings and Kicker differ by font
  and (Kicker) case/tracking only.
- **`bodyBase` (default 16 = Body MD)** scales the WHOLE table proportionally
  (factor = bodyBase/16 — unscaled literals pass through EXACT) — one knob, every voice together,
  snapping to a nice-number ladder when the factor ≠ 1. Per-cell `overrides` are the escape hatch
  for modifying a single default.
- Leadings are fixed per role family, not derived from size: Display 0.8; heading-family
  (Headline/Sub-heading/Title) 1.125; prose voices 1.4–1.5 (Body-mono 1.5); the box voices
  (Kicker/UI-control/UI-widget) also carry a 1.0 single-line-height for their `-line-single` mode.

## Voice roles (the taxonomy this table sizes)

**Material 3 baseline (5):** Display · Headline · Title · Label · Body.
**Nonoun extensions (10):** Sub-heading (a bold all-caps CONTEXT heading above a list/grid — not
a subordinate h2) · Sub-title (a smaller sub-heading, mono-by-default, prose flow) · Lead
(standfirst + pull-quotes) · Kicker (overline) · Body-mono / Label-mono (mono siblings, same
numbers as their base voice) · Tiny + Tiny-mono (captions, small supporting text, and its mono
sibling) · UI-control / UI-widget (dedicated interactive-text voices, the full 6-step ramp).

The consumption rules — which voice for which text, the box-voice `-line-single` set, paragraph
rhythm — are `font-token-rules`' canon; this file carries only the design-time size table.
