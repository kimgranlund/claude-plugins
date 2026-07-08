---
date: 2026-04-17
coverage: deep
peers:
  - ./anatomy.md
  - ./units.md
  - ./metric-compatibility.md
  - ../contemporary/metric-overrides.md
  - ../contemporary/variable-fonts.md
  - ../techniques/fallback-stacks.md
  - ../techniques/vertical-rhythm.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2
  - https://learn.microsoft.com/en-us/typography/opentype/spec/hhea
  - https://learn.microsoft.com/en-us/typography/opentype/spec/vhea
  - https://docs.microsoft.com/en-us/typography/opentype/spec/recom
  - https://github.com/googlefonts/gf-docs/tree/main/Spec
  - https://github.com/googlefonts/fontbakery/blob/main/Lib/fontbakery/checks/vertical_metrics.py
  - https://simoncozens.github.io/fonts-and-layout/
  - https://glyphsapp.com/learn/vertical-metrics
  - https://www.w3.org/TR/css-values-4/#font-relative-lengths
  - https://www.w3.org/TR/css-inline-3/#font-line-gap-metrics
  - https://drafts.csswg.org/css-fonts-4/#font-face-rule
  - https://www.sparkbox.com/foundry/typography_units_css_baseline_alignment
---

# Metrics Glossary

Typography runs on two kinds of names. **Anatomy** (see `./anatomy.md`) is what a letterform *is made of*. **Metrics** are what it *measures* — the quantities that determine how glyphs occupy space, how lines stack, and how a browser, OS, or print engine decides where the baseline sits. Every metric in this glossary lives in a specific binary table of an OpenType font (`head`, `hhea`, `OS/2`, `post`, `vhea`, `name`, `MVAR`) or is derived by the text-rendering engine.

This file is the deep reference for **measurement quantities** and their platform politics. For the named parts of a letterform, see `./anatomy.md`. For CSS-unit behavior in detail, see `./units.md`. For practical override recipes, see `../contemporary/metric-overrides.md`.

---

## The Vertical Canvas — Prose Diagram

Imagine a single line of text rendering a typeface drawn against a 1000-UPM grid (a common industry default; 2048 is the TrueType default). Five invisible horizontal lines govern every glyph:

```
                            ┌───────────────────────────┐
                            │          Hd              │  ← ascender-line
   ascender-line ────────── │  ├┐ ├─┐                   │     (top of `h`, `l`, `k`, `d`, `b`)
                            │  │ │ │                    │
     cap-line ───────────── │  │ │ │                    │  ← cap-line
                            │  │ │ │                    │     (top of `H`, `I`, `X`, usually)
                            │  │ │ │                    │
     x-line ─────────────── │  │  x n o                 │  ← x-line (mean-line)
                            │  │  │ │                   │     (top of `x`, `n`, `o`, non-ascending lc)
                            │  │  │ │                   │
     baseline ───────────── │  │  │ │ p y               │  ← baseline (y = 0)
                            │         │ │               │     (reference line for all glyphs)
     descender-line ─────── │         │ │               │  ← descender-line
                            └───────────────────────────┘     (bottom of `p`, `g`, `j`, `y`, `q`)
```

The **UPM** (Units Per Em, aka em-square) defines the vertical coordinate system. The **baseline** is always `y = 0`. Everything else is positive (above) or negative (below).

Above the x-line live **ascenders** (see `./anatomy.md#ascender`). Below the baseline live **descenders** (see `./anatomy.md#descender`). The **x-height** is the distance from baseline to x-line; the **cap-height** is the distance from baseline to cap-line. Round glyphs (`o`, `O`, `e`, `c`, `G`, `S`) extend slightly beyond these lines as an optical correction called **overshoot**. In display space, line stacking is governed by a taller ruler: the **ascent metric**, **descent metric**, and **line gap** stored in `OS/2` / `hhea` — which, as we will see, are a political and cross-platform mess.

---

## Master Metrics Table

Grouped by layer — from the font-internal coordinate system up through the rendering stack.

### Font-internal geometry (drawn quantities)

| Term | Definition | Where it lives | Typical range |
|------|------------|----------------|---------------|
| **UPM (Units Per Em)** | Integer size of the internal design grid | `head.unitsPerEm` | 1000 (PostScript / Adobe / Google Fonts default), 2048 (TrueType / Microsoft default). Legacy / display: 1024, 4000, 8192 |
| **em** | The UPM-sized square; the font's native coordinate unit | Derived — the grid itself | 1 em = UPM units internally; 1 em = `font-size` in CSS |
| **cap-height** | Distance from baseline to the top of flat-topped caps (`H`, `I`, `X`) | `OS/2.sCapHeight` (OT 1.3+) | ~700 on UPM=1000; ~1400 on UPM=2048 |
| **x-height** | Distance from baseline to the top of `x` (and by convention other flat-topped lowercase) | `OS/2.sxHeight` (OT 1.3+) | ~450–560 on UPM=1000 (higher = more legible at small size; cf. Frutiger vs Garamond) |
| **ascender height (drawn)** | Height of lowercase ascenders (`h`, `l`, `k`, `b`, `d`) | Drawn, not tabled — inferred from glyph outlines | Usually equal to cap-height or slightly higher (classical) |
| **descender depth (drawn)** | Depth of lowercase descenders (`p`, `g`, `j`, `y`, `q`) | Drawn, inferred from outlines | ~200–300 below baseline on UPM=1000 |
| **overshoot** | Extension of round/pointed glyphs beyond flat metric lines, as an optical correction | Drawn — glyph-by-glyph | ~8–15 units on UPM=1000 for body; larger at display |
| **weight axis mapping (`wght`)** | OpenType registered axis mapping stroke weight | `fvar`, `gvar`, `HVAR`, `MVAR` | 1–1000; 400 = normal, 700 = bold (conventional) |
| **width axis mapping (`wdth`)** | OpenType registered axis mapping horizontal scaling | `fvar`, `gvar` | 50–200 (percent of normal); 100 = normal |
| **optical-size axis (`opsz`)** | OpenType registered axis for size-specific optical cuts | `fvar`, `STAT` | Design-defined; typical 6–144 pt; see `../techniques/optical-size.md` |

### Horizontal glyph geometry

| Term | Definition | Where it lives | Why it matters |
|------|------------|----------------|-----------------|
| **sidebearing (LSB / RSB)** | Space between the glyph outline and its advance box, left and right | `hmtx` (derived from `glyf`/`CFF` outlines + `hmtx.leftSideBearing`) | Letter spacing without tracking |
| **advance width** | Total horizontal step from origin to next glyph's origin | `hmtx.advanceWidth` | Foundation of the CSS `ch` unit (nominally width of `0`) |
| **set width** | Historical print-era term for advance width | Legacy | Old metal-type literature; synonym |
| **kerning** | Pairwise advance-width adjustment for specific letter pairs | `kern` (legacy), `GPOS` (modern OpenType positioning) | Optical spacing of pairs like `AV`, `Ty`, `Wo` |
| **tracking** / **letter-spacing** | Uniform adjustment to advance widths across a run | Applied at runtime (CSS `letter-spacing`, InDesign tracking) | Global density |
| **horizontal axis alignment** | The distribution of sidebearings within the advance box | Drawn | Determines the "color" (evenness) of a typeface in a block |

### Vertical rendering metrics (display stack)

These govern line-stacking and vertical positioning — and this is where the cross-platform divergence begins.

| Term | Definition | Where it lives | Tables involved |
|------|------------|----------------|-----------------|
| **ascent** | Distance from baseline to the top of the line box | Multiple — see "Metric Wars" below | `hhea.ascent`, `OS/2.sTypoAscender`, `OS/2.usWinAscent` |
| **descent** | Distance from baseline to the bottom of the line box | Multiple | `hhea.descent`, `OS/2.sTypoDescender`, `OS/2.usWinDescent` |
| **line gap** | Extra vertical space added between lines (external leading) | `hhea.lineGap`, `OS/2.sTypoLineGap` | Added on top of ascent+descent |
| **default line-height** | Browser-computed line-height when CSS `line-height: normal` | Derived from metrics above, platform-dependent | Varies across engines; cause of "why does my line-height look different on Windows?" |
| **vertical advance** | Line-to-line step in vertical text modes (CJK tategaki) | `vhea.ascent`, `vhea.descent`, `vhea.lineGap`, `vmtx` | Used when `writing-mode: vertical-rl` / `vertical-lr` |
| **`USE_TYPO_METRICS`** flag | Instructs text engines to prefer `OS/2.sTypo*` over `OS/2.usWin*` | `OS/2.fsSelection` bit 7 (value 0x80) | The single most important metric-politics flag — see below |
| **MVAR metric deltas** | Variable-font per-instance overrides of metrics (ascent, descent, line-gap, x-height, cap-height, strikeout, etc.) | `MVAR` table | Necessary when metrics change across variable-font axes |

### Table-location cheatsheet

| Quantity | Table | Field |
|----------|-------|-------|
| UPM | `head` | `unitsPerEm` |
| Typographic ascender | `OS/2` | `sTypoAscender` |
| Typographic descender | `OS/2` | `sTypoDescender` (negative) |
| Typographic line gap | `OS/2` | `sTypoLineGap` |
| Win ascent | `OS/2` | `usWinAscent` (unsigned — always positive, never trims descender) |
| Win descent | `OS/2` | `usWinDescent` (unsigned — positive number representing depth) |
| hhea ascent | `hhea` | `ascent` / `ascender` |
| hhea descent | `hhea` | `descent` / `descender` (negative) |
| hhea line gap | `hhea` | `lineGap` |
| Cap height | `OS/2` (v2+) | `sCapHeight` |
| x-height | `OS/2` (v2+) | `sxHeight` |
| USE_TYPO_METRICS | `OS/2` | `fsSelection` bit 7 (mask 0x0080) |
| Italic angle | `post` | `italicAngle` |
| Underline position/thickness | `post` | `underlinePosition`, `underlineThickness` |
| Variable-font metric overrides | `MVAR` | Value records keyed by tag (`hasc`, `hdsc`, `hlgp`, `xhgt`, `cpht`, etc.) |
| Horizontal advance widths | `hmtx` | `advanceWidth`, `leftSideBearing` |
| Vertical advance heights | `vmtx` | `advanceHeight`, `topSideBearing` |
| Kerning | `GPOS` (modern), `kern` (legacy) | Subtables |

---

## Per-Term Entries

### UPM (Units Per Em)

- **Definition:** The integer resolution of a font's internal design grid — the number of font-units in one em. All other metrics are expressed relative to this.
- **Where it lives:** `head.unitsPerEm` (OpenType `head` table).
- **Typical values:** 1000 (PostScript / CFF, Adobe, Google Fonts default), 2048 (TrueType, Microsoft default), legacy 1024, 4000, 8192 for high-fidelity work.
- **Why it matters:** Metrics from two fonts with different UPMs are **not directly comparable** — you must normalize by UPM first. `ascent / unitsPerEm = 0.82` is comparable across fonts; `ascent = 1800` is not.
- **Related:** All metric overrides in CSS (`ascent-override`, `descent-override`) are expressed as percentages of 1 em, not raw units, specifically to avoid UPM confusion.

### em

- **Definition:** The font's native unit — a square whose side equals the UPM. Internally measured in font-units; externally rendered at the current `font-size`.
- **Where it appears:** Everywhere in typesetting; name survives from metal type, when the em was the width of a cast capital `M`.
- **Why it matters:** In CSS, `1em = current font-size`. In font-internal space, `1 em = 1000 units` (UPM=1000) or `2048 units` (UPM=2048). The dual meaning trips new practitioners.
- **Related:** `rem` (root em), `ex`, `ch`, `cap`, `ic`, `lh`, `rlh` — all defined against `em` or a font metric. See `./units.md`.

### x-height

- **Definition:** Vertical distance from the baseline to the x-line; the height of `x` (and by convention `n`, `m`, `o`, `u`, non-ascending lowercase).
- **Where it lives:** `OS/2.sxHeight` (added in OpenType 1.3 / OS/2 table v2 — if absent, must be inferred by the rendering engine).
- **Typical range:** 450–560 units on UPM=1000. Frutiger ~530, Helvetica ~530, Garamond ~400, Bodoni ~430, Inter ~515.
- **Why it matters:** The single most important metric for perceived size and legibility at small sizes. A large x-height at 12px UI feels like a 14px UI in a small-x-height face.
- **Related:** `font-size-adjust: ex-height <ratio>` (CSS) uses this value to normalize perceived size across families. See `../contemporary/metric-overrides.md`.

### cap-height

- **Definition:** Distance from baseline to top of flat-topped caps (`H`, `I`, `X`, `E`).
- **Where it lives:** `OS/2.sCapHeight` (OpenType 1.3+).
- **Typical range:** 650–750 units on UPM=1000.
- **Why it matters:** Governs cap alignment with icons, drop-caps, and all-caps rendering. The CSS `cap` unit is defined against this metric. When it's missing from the font, browsers fall back to measuring the height of `H`.
- **Related:** `font-size-adjust: cap-height <ratio>` normalizes by cap-height; useful for all-caps UI.

### Ascender height (drawn)

- **Definition:** Height of lowercase ascenders (`h`, `l`, `k`, `b`, `d`, `f`, `t`).
- **Where it lives:** Not stored as a single metric; inferred from glyph outlines. Sometimes (loosely) equated with `OS/2.sTypoAscender`, but that metric is the *line-box* ascent, not the drawn ascender height.
- **Typical range:** Classically equal to or slightly taller than cap-height.
- **Why it matters:** Determines how `h`/`l`/`k` relate visually to `H`/`L`/`K`. In some humanist faces (Caslon, Garamond) ascenders outrank caps; in Didone and geometric faces they're equal or shorter.
- **Related:** Don't confuse drawn ascender height with the `ascent` line-metric used for line-stacking.

### Descender depth (drawn)

- **Definition:** Depth of lowercase descenders (`p`, `g`, `j`, `y`, `q`) below baseline.
- **Where it lives:** Drawn, not tabled as a single metric.
- **Typical range:** 200–300 units below baseline on UPM=1000.
- **Why it matters:** Shallow descenders (Roboto, SF Pro Text) fit tighter UI; deep descenders (Garamond, Caslon) need more leading.
- **Related:** The line-metric `descent` (`hhea.descent` / `OS/2.sTypoDescender` / `OS/2.usWinDescent`) is usually larger than drawn descender depth — it pads the line box.

### Overshoot

- **Definition:** The amount by which round or pointed glyphs extend beyond the flat-topped metric line — an optical correction so that `O` looks the same height as `H`, and `o` looks the same height as `x`.
- **Where it lives:** Drawn — glyph-level outline data.
- **Typical range:** 8–15 units on UPM=1000 for text sizes; 20+ for display.
- **Why it matters:** Mathematically, `O` and `H` look different heights even when their bounding boxes are identical — the curve receives less visual "weight" than a flat top. Type designers add 1–2% overshoot to compensate. If a designer forgets to add overshoot, round glyphs look shorter than flat ones.
- **Related:** Overshoot does *not* extend the font's line-box metrics — it's purely optical. See `../techniques/optical-size.md` for size-specific overshoot tuning.

### Sidebearing (LSB / RSB)

- **Definition:** The horizontal space between the glyph outline and the edge of its advance box. LSB = Left Side Bearing; RSB = Right Side Bearing.
- **Where it lives:** `hmtx.leftSideBearing` for LSB; RSB derived as `advanceWidth − glyph-bounding-box.xMax`.
- **Why it matters:** Governs inter-glyph spacing without tracking — the "color" evenness of a typeface. Modifying sidebearings is how designers achieve consistent spacing across a font.
- **Related:** Kerning adjusts spacing *between* specific pairs on top of sidebearings. See `../contemporary/opentype-features.md#kern`.

### Advance width

- **Definition:** Distance from glyph origin to the next glyph's origin — the horizontal step after rendering a glyph.
- **Where it lives:** `hmtx.advanceWidth`.
- **Why it matters:** (1) Foundation of the CSS `ch` unit (nominally the advance of `0` in the current font). (2) Determines whether a font is monospaced (uniform advance) or proportional (variable advance). (3) Basis of tabular figures (`tnum` OpenType feature forces all digits to share advance).
- **Related:** `set width` is the historical print-era term. `em-square` describes the drawing space; advance width describes the horizontal metric.

### Kerning

- **Definition:** Per-pair horizontal adjustment to advance widths — so `AV`, `Ty`, `Wo`, `Av` don't look gapped.
- **Where it lives:** Modern: `GPOS` table (OpenType Positioning). Legacy: `kern` table (still present in many fonts; deprecated for new designs).
- **Why it matters:** Without kerning, even well-drawn fonts look sloppy at display sizes. Browsers apply `GPOS` kerning when `font-kerning: normal` (default in modern CSS).
- **Related:** CSS `font-kerning` controls on/off/auto. Prefer `auto` unless you know the font lacks GPOS.

### Tracking / letter-spacing

- **Definition:** Uniform horizontal adjustment to advance widths across a run — global density control.
- **Where it lives:** Applied at runtime — CSS `letter-spacing`, InDesign tracking, Figma letter-spacing.
- **Why it matters:** All-caps runs benefit from positive tracking (~+50 to +100 in InDesign units, ~0.05–0.1em in CSS). Body prose should use 0 except for explicit correction.
- **Related:** Kerning is per-pair; tracking is uniform. `letter-spacing` in CSS adds to (after) kerning.

### Leading (line-height)

- **Definition:** Vertical distance between successive baselines. Originally from metal type — literal strips of lead inserted between lines of type.
- **Where it lives:** In CSS, `line-height` property. In fonts, a default is computed from `hhea`/`OS/2` ascent + descent + line gap.
- **Why it matters:** Inadequate leading (< 1.2× font-size in body) causes crowding; excessive leading (> 1.8×) breaks paragraph cohesion.
- **Related:** See `../techniques/vertical-rhythm.md` for modular scale interactions. The default browser line-height varies by metric source — see "Metric Wars" below.

### Baseline

- **Definition:** The horizontal reference line at `y = 0` in font-internal space; the line on which most Latin letters sit.
- **Where it lives:** Implicit — all vertical metrics are measured relative to it.
- **Why it matters:** The canonical alignment reference for text and adjacent elements (icons, math, subscripts/superscripts). CSS `vertical-align: baseline` aligns to this line.
- **Related:** Non-Latin scripts have different baseline conventions: **hanging baseline** (Devanagari shirorekha), **ideographic baseline** (CJK center), **mathematical baseline** (offset for math glyphs). The `BASE` table in OpenType stores these per-script. See `../scripts/devanagari.md`, `../scripts/cjk-han.md`.

### Ascent / Descent / Line gap (the line-box trio)

- **Definition:** The three line-stacking metrics. **Ascent** = baseline → top of line box. **Descent** = baseline → bottom of line box. **Line gap** = extra space between successive line boxes.
- **Where they live:** This is where it gets hairy. They exist in three places:
  - `hhea.ascent` / `hhea.descent` / `hhea.lineGap` (used by macOS and some engines)
  - `OS/2.sTypoAscender` / `OS/2.sTypoDescender` / `OS/2.sTypoLineGap` (used by anything honoring `USE_TYPO_METRICS`)
  - `OS/2.usWinAscent` / `OS/2.usWinDescent` (used by Windows GDI and several browsers historically — *no line gap component*)
- **Why it matters:** Different platforms read different tables → line-heights differ between macOS, Windows, and older browsers → layout shifts across platforms. See "The Metric Wars" below.
- **Related:** Historically, `ascent + descent + lineGap` = default line-height on macOS; `winAscent + winDescent` = default on Windows (with no line gap added).

### USE_TYPO_METRICS flag (fsSelection bit 7)

- **Definition:** A 1-bit flag in `OS/2.fsSelection` (bit 7, mask `0x0080`) instructing text-rendering engines to use the `OS/2.sTypo*` metrics for line-height, rather than the platform-specific default.
- **Where it lives:** `OS/2.fsSelection` bit 7.
- **History:** Defined in OpenType to let designers enforce consistent vertical metrics across platforms. Google Fonts began mandating this flag in 2018–2019 as part of their metric-normalization work, which meaningfully reduced cross-platform layout divergence for fonts they host.
- **Why it matters:** With the flag set, and a rendering engine that honors it (most do in 2024–2026), the browser uses `sTypoAscender + sTypoDescender + sTypoLineGap` regardless of OS — predictable line heights everywhere. Without the flag, platform-specific defaults apply (Windows/usWin*, some macOS engines/hhea*, etc.).
- **Related:** `../contemporary/metric-overrides.md` explains how to bypass this entirely via `@font-face` overrides. See "Metric Wars" below.

### Optical size (`opsz`)

- **Definition:** The OpenType registered axis (`opsz`) exposing multiple design variants tuned for different rendering sizes. Small-size "text" cuts have larger x-heights, more open apertures, and heavier hairlines; "display" cuts have finer contrast and tighter spacing.
- **Where it lives:** `fvar` axis record; per-instance details in `STAT`; glyph deltas in `gvar`; metric deltas in `MVAR`.
- **Why it matters:** Enables proper typesetting — a single variable font serves as both a 9pt text face and a 96pt display face, correctly tuned to each size. CSS `font-optical-sizing: auto` (default) activates the axis from `font-size`.
- **Related:** `../techniques/optical-size.md` has the composition story; `../contemporary/variable-fonts.md` has the axis mechanics.

### Italic angle

- **Definition:** The slant angle (in degrees, measured counterclockwise from vertical) of a font's italic cut.
- **Where it lives:** `post.italicAngle`.
- **Typical range:** 0° (upright), -8° to -12° (typical italic), down to -25° (aggressive italic).
- **Why it matters:** Used by rendering engines to compute italic rise; by variable fonts to drive the `slnt` axis; and by layout engines for caret positioning. A positive `italicAngle` is exceedingly rare — italics lean right, which in this coordinate system is a negative rotation.
- **Related:** See `./anatomy.md#italic-specific` for true-italic vs oblique distinction.

### `slnt` vs `ital` axis

- **Definition:** Two different OpenType variable-font axes. **`slnt`** is a continuous axis expressing geometric slant (typically -15° to 0°). **`ital`** is a binary switch (0 or 1) between two structurally distinct cuts.
- **When each applies:** Use `slnt` when the italic is a slanted roman (oblique). Use `ital` when the italic has distinct lowercase construction (single-storey `a`, different `e`, entry/exit strokes).
- **Why it matters:** Many sans families (Helvetica, DIN, Inter) have oblique → `slnt`. Most serif families (Garamond, Caslon, Adobe Caslon Pro) have true italic → `ital`. A variable font can expose both (Roboto Flex does).
- **Related:** See `./anatomy.md#italic-specific`. CSS: `font-style: italic` maps to `ital=1`; `font-style: oblique <deg>` maps to `slnt`.

---

## The Metric Wars

A recurring source of cross-platform layout confusion. Fonts define vertical metrics in three places, and the platforms can't agree on which to read. This section summarizes the history and current best practice.

### The three metric sources

OpenType specifies three places to record line-stacking metrics:

1. **`hhea`** table — `ascent`, `descent`, `lineGap`. Originally the Apple / TrueType metrics. Historically respected by macOS.
2. **`OS/2` typographic metrics** — `sTypoAscender`, `sTypoDescender`, `sTypoLineGap`. Designed to be the canonical cross-platform metrics, but only honored when `USE_TYPO_METRICS` (bit 7 of `fsSelection`) is set.
3. **`OS/2` Windows metrics** — `usWinAscent`, `usWinDescent`. Required by Windows GDI; **no line gap component**. Both values are unsigned — Windows historically used these to determine "no glyph clips", so setting them too low truncates descenders.

### Why the divergence

- When OpenType was standardized in the 1990s, font vendors were already shipping fonts with `hhea` metrics for Mac and `usWin*` metrics for Windows — typically **with different values**, chosen to give equivalent line-heights on each platform's rendering pipeline.
- Browsers, operating systems, and layout engines all picked different sources:
  - **Windows GDI / older Edge / IE** → `usWinAscent` + `usWinDescent` (no line gap).
  - **macOS / CoreText / Safari on macOS** → `hhea.ascent` + `hhea.descent` + `hhea.lineGap`.
  - **Chrome on Windows / Firefox** → historically switched between sources; modern behavior honors `USE_TYPO_METRICS`.
  - **Android / DirectWrite on modern Windows** → more consistent with typo metrics when the flag is set.
- Result: the *same font at the same size on the same web page* could produce different line-heights on Windows vs macOS — sometimes off by 20% or more.

### Why it matters in practice

- Layout shift between macOS and Windows: designs built on a Mac showing extra white space or clipping on Windows.
- Grid rhythm breaks: baseline grids that align on one platform drift on another.
- Multi-font pages: each font's metric choices compound; some fonts look tight, others loose.
- Foundries sometimes deliberately ship `usWin*` values large enough to prevent clipping on Windows, which inflates line-heights relative to `hhea`.

### The fix (2018–present)

Multiple remediation approaches, ordered by durability:

1. **Set `USE_TYPO_METRICS`** (bit 7 of `OS/2.fsSelection`). Tells the rendering engine to honor the `OS/2.sTypo*` values regardless of platform. Modern browsers (as of 2024) all respect this flag.
   - **Google Fonts' metric normalization project** (launched ~2018, ongoing): they re-compile hosted fonts with standardized `sTypoAscender`, `sTypoDescender`, `sTypoLineGap` values and enforce `USE_TYPO_METRICS`. Source: github.com/googlefonts/gf-docs/tree/main/Spec and fontbakery vertical-metrics checks.
   - **Karolina Lach ("Mismatched Font Metrics", 2018)** and other practitioners documented the practical fix and the per-font overrides needed.
   - **Sparkbox posts (2019)** on CSS baseline alignment and vertical-metric mismatches gave the web community a vocabulary for the problem.
2. **`@font-face` metric overrides** (`ascent-override`, `descent-override`, `line-gap-override`). These let CSS bypass the font's metrics entirely — compute your own line-box. Critical for metric-compatible fallback stacks. See `../contemporary/metric-overrides.md`.
3. **`size-adjust`** (`@font-face`) to scale a fallback font's em-square to match the primary font's x-height, so fallback and primary occupy the same box. Used for zero-CLS font loading.
4. **Use `font-size-adjust: ex-height <ratio>`** at the consumption site — CSS normalizes perceived size by x-height ratio. See `../contemporary/metric-overrides.md`.

### Practitioner cheatsheet — reading `hhea` + `OS/2` table values

When auditing a font for metric issues, check these in `OS/2` and `hhea` (tools: FontDrop, Wakamai Fondue, Samsa, `ttx` from fonttools, Glyphs):

| Question | Field to check | Expected behavior |
|----------|----------------|-------------------|
| Is `USE_TYPO_METRICS` set? | `OS/2.fsSelection` bit 7 (0x80) | **Should be 1** for modern fonts |
| What is the "honored" line height? | `OS/2.sTypoAscender` + `|OS/2.sTypoDescender|` + `OS/2.sTypoLineGap` / UPM | Typical ~1.15–1.35 |
| What does Windows GDI see? | `OS/2.usWinAscent` + `OS/2.usWinDescent` / UPM | Should be **≥** the typo-metrics sum (to avoid clipping); often inflated |
| What does classical macOS see? | `hhea.ascent` + `|hhea.descent|` + `hhea.lineGap` / UPM | Compare to typo-metrics; mismatch → cross-platform issues |
| Are line-gap and ascender consistent? | Compare `sTypoLineGap + sTypoAscender` to `usWinAscent` | Discrepancy > 10% = likely inconsistent defaults |
| Is the font variable? | Presence of `fvar` + `MVAR` | Check `MVAR` for per-instance ascent/descent deltas |

### Dated notes

- **Pre-2018:** Wild-west. Fonts shipped divergent `hhea` / `usWin*` / `sTypo*`; `USE_TYPO_METRICS` was rarely set. Cross-platform layout was inconsistent.
- **2018–2019:** Google Fonts launches metric normalization. Karolina Lach, Mark Boulton, and H&Co writeups standardize practitioner understanding.
- **2020–2021:** `@font-face` metric overrides (`ascent-override`, `descent-override`, `line-gap-override`, `size-adjust`) reach Chrome and Firefox. Enables true CLS-free font loading.
- **2023–2024:** `USE_TYPO_METRICS` is the de-facto default for new commercial fonts from major foundries. Modern browsers and OS text engines all honor it.
- **2026 (current):** For fonts you control, setting `USE_TYPO_METRICS` is table-stakes. For fonts you don't control (especially older licensed fonts), `@font-face` metric overrides are the reliable cure. For maximum portability, use both approaches together with `font-size-adjust`.

---

## CSS-Unit Derivation Table

Every CSS font-relative unit maps to one of the metrics above.

| CSS unit | Resolves to | Spec source | Fallback when missing |
|----------|-------------|-------------|------------------------|
| **`em`** | `font-size` (computed, of current element) | CSS Values 4 § font-relative | Always resolvable (inherits from root) |
| **`rem`** | `font-size` of the root element (`:root`, `html`) | CSS Values 4 | Same |
| **`ex`** | x-height of current font — equal to `sxHeight / UPM * font-size` | CSS Values 4 | 0.5em (spec fallback when `sxHeight` absent) |
| **`ch`** | Advance width of `0` (U+0030) in the current font | CSS Values 4 | 0.5em (when glyph is not renderable) |
| **`cap`** | Cap-height of current font = `sCapHeight / UPM * font-size` | CSS Values 4 | Defined in CSS Values 4; fallback to measurement of `H` |
| **`ic`** | Advance of the ideographic water glyph `水` (U+6C34) | CSS Values 4 | 1em (when glyph is not in font) |
| **`lh`** | Line-height of current element | CSS Values 4 | Computed from `line-height` |
| **`rlh`** | Line-height of root element | CSS Values 4 | Same |
| **`%`** (on `font-size`) | Percentage of parent element's `font-size` | CSS Values 4 | — |
| **`rex`** | Root-element `ex` | CSS Values 5 draft (2025) | Draft — check browser support |
| **`rch`** | Root-element `ch` | CSS Values 5 draft | Draft |
| **`rcap`** | Root-element `cap` | CSS Values 5 draft | Draft |
| **`ric`** | Root-element `ic` | CSS Values 5 draft | Draft |

### Unit decision cheatsheet

| Use case | Best unit | Why |
|----------|-----------|-----|
| Body font-size anchor | `rem` | Root-relative, user-zoom-safe |
| Icon sized to match caps | `1cap` | Exactly matches cap-height |
| Icon sized to match x-height | `1ex` | Exactly matches lowercase optical mass |
| CJK layout (character grid) | `ic` | The ideographic square |
| Measure (CPL) | `ch` | Approximate — `ch` is only exact for monospaced; for proportional, multiply by ~2 for the 65ch ≈ 75-char target |
| Line-height math (`margin-top` on first line) | `lh`, `rlh` | Makes rhythm adjustments first-class |
| Spacing that scales with font | `em` (local), `rem` (global) | `em` scales with current element; `rem` with root |
| Line-grid rhythm | `rlh` | Root line-height provides a consistent grid |

For deeper unit coverage and font-relative vs viewport-relative interactions, see `./units.md`.

---

## Anti-patterns and Common Confusions

### Comparing raw font-units across fonts

- Wrong: "Garamond has 450 x-height, Frutiger has 530 — Frutiger is ~18% taller."
- Right: "Garamond x-height = 450 / 1000 = 0.45. Frutiger x-height = 530 / 1000 = 0.53. Frutiger is ~18% taller **per em**."
- Always normalize by UPM.

### Conflating drawn ascender-height with line-metric ascent

- Drawn ascender height = where `h`/`l`/`k` reach. Inferred from glyph outlines.
- Line-metric ascent (`hhea.ascent`, `sTypoAscender`, `usWinAscent`) = where the line-box top sits. Almost always *taller* than drawn ascender-height, to leave headroom for diacritics.
- In OpenType spec, line-metric ascent is supposed to include at least the tallest diacritic above the tallest ascender. In practice, foundries vary.

### Assuming `hhea` and `OS/2` metrics agree

- They very often don't. A font can have `hhea.ascent = 950` and `OS/2.sTypoAscender = 780`, deliberately, for historical platform-specific reasons.
- Always check `USE_TYPO_METRICS` flag and compare the values before assuming behavior.

### Using `ch` for Latin-script measure without correcting

- `ch` = advance of `0`. For most proportional fonts, `0` is ~50% wider than an average letter. So `65ch` targets ~65 × 1 × fudge ≈ 65 characters-per-line of *digits*, but ~90–100 characters of mixed prose.
- Rule of thumb for body prose: target `65ch` for a ~75-CPL measure. Or use absolute ch counts from `../techniques/measure.md`.

### Treating `line-height: normal` as stable

- It isn't. `line-height: normal` delegates to font metrics — and we just saw those are a political mess.
- For predictable cross-platform rhythm, always set `line-height` to a unitless number (e.g., `line-height: 1.5`).

### Setting `@font-face` ascent-override without UPM-normalizing first

- `ascent-override: 95%` = 95% of 1em. It is *not* 95% of some font's UPM. Always convert from font-units to em-percentage: `override = (ascent_units / upm) * 100%`.

### Confusing `slnt` with italic

- `slnt` is *geometric slant*. `ital` is a *binary cut switch*. Most serif families have structurally distinct italic cuts (use `ital`); most sans families only have oblique (use `slnt`). Using `slnt` on a serif that has true-italic design loses the italic's distinct letterforms.

### Using ascender height to compute line-gap

- `line-gap` is an independent metric, not a function of ascender or descender height. It's the *external* leading — the extra padding above and below the glyph's ascent/descent extremes. `line-height = ascent + descent + lineGap` (in most rendering stacks that honor the `hhea`/`sTypo*` sources).

### Treating `cap` and `ex` as universally available

- CSS Values 4 defines them, but browsers may fall back when the font lacks `sCapHeight` or `sxHeight` (OS/2 table v2+ only). Verify by checking font tables.
- `rex`, `rch`, `rcap`, `ric` are in CSS Values 5 *drafts* — check support before shipping.

---

## Cross-references

- For **named letterform parts** (stem, bowl, counter, apex, vertex, ear, eye, terminal, finial, swash, etc.), see the companion anatomy reference: `./anatomy.md`.
- For **CSS font-relative units** in depth, see `./units.md`.
- For **practical fallback-stack construction** with metric overrides, see `../techniques/fallback-stacks.md` and `../contemporary/metric-overrides.md`.
- For **variable-font axis mechanics** (wght, wdth, ital, slnt, opsz), see `../contemporary/variable-fonts.md`.
- For **measure (CPL) derivation** using `ch`, see `../techniques/measure.md`.
- For **baseline-grid rhythm**, see `../techniques/vertical-rhythm.md`.
- For **non-Latin script baselines** (hanging, ideographic, mathematical), see per-script files in `../scripts/`.

---

## Sources

- Microsoft OpenType spec — `OS/2` table (https://learn.microsoft.com/en-us/typography/opentype/spec/os2, accessed 2026-04-17). Canonical spec for `sTypoAscender`, `sTypoDescender`, `usWinAscent`, `usWinDescent`, `fsSelection`, `sxHeight`, `sCapHeight`.
- Microsoft OpenType spec — `hhea` table (https://learn.microsoft.com/en-us/typography/opentype/spec/hhea, accessed 2026-04-17).
- Microsoft OpenType spec — `vhea` table (https://learn.microsoft.com/en-us/typography/opentype/spec/vhea, accessed 2026-04-17).
- Microsoft OpenType font development recommendations (https://learn.microsoft.com/en-us/typography/opentype/spec/recom, accessed 2026-04-17).
- Google Fonts — metric normalization spec and fontbakery checks (https://github.com/googlefonts/gf-docs/tree/main/Spec, https://github.com/googlefonts/fontbakery — vertical-metrics checks, accessed 2026-04-17).
- Glyphs.app — "Vertical Metrics" (https://glyphsapp.com/learn/vertical-metrics, accessed 2026-04-17). Practitioner-facing walkthrough of the metric wars and best-practice values.
- Simon Cozens — *Fonts and Layout for Global Scripts* (https://simoncozens.github.io/fonts-and-layout/, accessed 2026-04-17). Authoritative on the metric wars from the engineering side.
- W3C CSS Values 4 — font-relative lengths (https://www.w3.org/TR/css-values-4/#font-relative-lengths, accessed 2026-04-17). Spec for `em`, `rem`, `ex`, `ch`, `cap`, `ic`, `lh`, `rlh`.
- W3C CSS Inline 3 — line metrics and line-box computation (https://www.w3.org/TR/css-inline-3/#font-line-gap-metrics, accessed 2026-04-17).
- W3C CSS Fonts 4 — `@font-face` overrides (https://drafts.csswg.org/css-fonts-4/#font-face-rule, accessed 2026-04-17). Spec for `ascent-override`, `descent-override`, `line-gap-override`, `size-adjust`.
- Sparkbox — "Typography Units and CSS Baseline Alignment" (https://www.sparkbox.com/foundry/typography_units_css_baseline_alignment, accessed 2026-04-17).
- Karolina Lach — "Mismatched Font Metrics" and follow-up posts (2018–2020). Practitioner documentation of the metric wars.
- Mark Boulton — "Setting Type on the Web to a Baseline Grid" (A List Apart, revisited 2019).
- Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012). Canonical for leading, measure, and traditional typographic vocabulary.
