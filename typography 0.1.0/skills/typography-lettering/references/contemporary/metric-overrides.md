---
date: 2026-04-17
coverage: medium
peers:
  - ./font-delivery.md
  - ./css-text-properties.md
  - ../techniques/fallback-stacks.md
  - ../metrics/metrics-glossary.md
  - ../metrics/metric-compatibility.md
primary_sources:
  - https://drafts.csswg.org/css-fonts-5/#font-metrics-override-desc
  - https://drafts.csswg.org/css-fonts-5/#size-adjust-desc
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/descent-override
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/line-gap-override
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust
  - https://web.dev/blog/font-metric-overrides
  - https://developer.chrome.com/blog/font-fallbacks
  - https://github.com/seek-oss/capsize
  - https://github.com/unjs/fontaine
  - https://nextjs.org/docs/app/api-reference/components/font
  - https://simonhearne.com/2021/layout-shifts-webfonts/
  - https://www.smashingmagazine.com/2022/05/reducing-layout-shift-font-fallbacks/
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2
---

# Metric Overrides

The four `@font-face` descriptors — `ascent-override`, `descent-override`,
`line-gap-override`, and `size-adjust` — let a stylesheet **reshape the vertical
line-box of a fallback font** so it occupies the same space as the primary web
font it is standing in for. They are the mechanism behind every zero-CLS
font-loading recipe shipped since Chrome 87 and Firefox 89 (2021).

This file covers the **mechanism**: what each descriptor does, how values are
computed from OpenType metric tables, what the browser is actually doing with
them, and how they relate to the older per-element `font-size-adjust` property.

It is distinct from two peers:

- **`../techniques/fallback-stacks.md`** — catalog of production-ready stacks
  per genre, with the numeric overrides already computed. Lift and ship.
- **`../metrics/metrics-glossary.md`** — the binary-table reference for
  `UPM`, `sTypoAscender`, `sTypoDescender`, `sTypoLineGap`, `sxHeight`,
  `sCapHeight`, and the `USE_TYPO_METRICS` flag. When this file names a metric
  field, glossary is authoritative.

If you need *a* fallback stack for a popular web font, go to fallback-stacks.
If you need *your own* stack because you ship a licensed face, stay here.

---

## The Problem

When a page declares `font-family: "Inter", sans-serif;`, the browser does
not block layout on Inter's download. Under `font-display: swap` (and the
default `auto`/`block`), it paints immediately using whatever the user agent
resolves `sans-serif` to — typically Arial on Windows, Helvetica / SF Pro on
macOS, Roboto on Android, Liberation Sans on most Linux distros. That is
the **FOUT window**. When Inter arrives, the browser re-lays-out with
Inter's metrics and every line below the first repaint moves. That is
**Cumulative Layout Shift (CLS)** — a Core Web Vital with a "good" budget
of < 0.1 per page.

The mismatch is not about letter shape. It is about the vertical box.
Normalized to em (value ÷ UPM), Inter vs Arial:

| Font  | Ascent | Descent | Line-gap | x-height |
| ----- | -----: | ------: | -------: | -------: |
| Inter | 0.968  | 0.242   | 0.000    | 0.546    |
| Arial | 0.905  | 0.212   | 0.033    | 0.519    |

A line of Inter at `font-size: 16px` reserves
`(0.968 + 0.242) × 16 = 19.36px`. The same text in Arial reserves
`(0.905 + 0.212 + 0.033) × 16 = 18.40px` — nearly 1px shorter per line. Over
a 40-line article, that's ~38px of vertical drift on swap. Every image below
the first paragraph leaps.

The four `@font-face` override descriptors let you coerce the **fallback's
effective line-box** to match the primary's, so the FOUT render and the
post-swap render line up exactly. You do not override the primary — you
override the fallback. Glyph shapes remain the system font's; only the
metrics are reshaped.

For the `hhea` vs `OS/2.sTypo*` vs `OS/2.usWin*` politics, see
`../metrics/metrics-glossary.md#the-metric-wars`. For metric tables of
many more fonts, see `../metrics/metric-compatibility.md`.

---

## The Four Descriptors

All four are `@font-face`-only. They cannot be set on an element. The alias
trick: declare an `@font-face` whose `src` is `local("…")` pointing at a
system font, and apply the descriptors to that alias — you cannot override
the raw "Arial" family, but you can override a redeclared face that happens
to source Arial.

### `ascent-override: <percentage> | normal`

- **What it sets:** The effective `OS/2.sTypoAscender` (or `hhea.ascent`,
  depending on which table the engine is reading) of the face, expressed as
  a percentage of the em-square *after* `size-adjust` has scaled the font.
- **Range:** In practice 70–180% for Latin; the spec allows 0–infinity.
- **`normal` keyword:** Default. The font's own `ascent` value is used.
- **What the percentage means:** Fraction of 1 em. `ascent-override: 96.8%`
  means "reserve 0.968 em above the baseline for the top of the line-box",
  regardless of what the underlying Arial face actually defines. Browsers
  apply this in the computed line-box height for `line-height: normal` and
  for the first/last leading math that drives `text-box-trim`.
- **Spec:** CSS Fonts 5 § `ascent-override`.

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  ascent-override: 90.44%;   /* Inter's 0.968 em ÷ size-adjust 1.0712 */
}
```

### `descent-override: <percentage> | normal`

- **What it sets:** The effective `sTypoDescender` / `hhea.descent`, as a
  non-negative percentage of em (the CSS descriptor is positive even though
  the font-binary value is signed negative).
- **Range:** 10–45% for Latin.
- **`normal` keyword:** Default. Use the font's own descent.
- **Why it's separate from ascent:** Line-height is the sum
  `ascent + descent + lineGap`; changing only ascent skews the baseline
  position within the line-box, which matters for `vertical-align: baseline`
  and for inline box alignment against images/icons.
- **Spec:** CSS Fonts 5 § `descent-override`.

```css
descent-override: 22.52%;     /* Inter's |−0.242 em| ÷ 1.0712 */
```

### `line-gap-override: <percentage> | normal`

- **What it sets:** The effective `sTypoLineGap` / `hhea.lineGap`.
- **Range:** 0–25% for Latin; most Google Fonts ship a 0 line-gap and rely
  on ascent + descent to provide the natural `line-height: normal`.
- **`normal` keyword:** Default. Use the font's own line-gap.
- **Critical pitfall:** If your primary font has line-gap of 0 (Inter,
  Roboto, SF Pro), but the fallback has line-gap > 0 (Arial 67 / 2048 =
  3.3%), you **must** override to 0 on the fallback. Otherwise the fallback
  renders with `(0.905 + 0.212 + 0.033) = 1.150 em` line-height while Inter
  renders with `(0.968 + 0.242 + 0) = 1.210 em`. They differ. Double-leading
  is the default failure mode when people omit this descriptor.
- **Spec:** CSS Fonts 5 § `line-gap-override`.

```css
line-gap-override: 0%;        /* Inter's 0 line-gap */
```

### `size-adjust: <percentage>`

- **What it sets:** A uniform **multiplicative scale** applied to every glyph
  outline and every drawn metric (ascent, descent, advance width) in the
  face. A value of `100%` is identity. `107.12%` means "render every glyph
  1.0712× larger than nominal."
- **Range:** 50–200% in practice; spec allows 0–infinity.
- **No `auto` value (as of 2026-04).** `auto` was debated but not shipped.
  `normal` is also not defined for `size-adjust` — the default is `100%`.
- **What it is for:** Matching x-height (or cap-height) between primary and
  fallback so that at a given `font-size`, the visible lowercase mass looks
  the same. Inter's x-height is 0.546 em; Arial's is 0.519 em. Scaling Arial
  by 0.546 / 0.519 = 1.0520 makes its rendered x-height match Inter's.
  Capsize's formula adds a further 1–2% correction for cap-height alignment;
  the typical shipped value for Inter → Arial is 107.12%.
- **How it interacts with the other three:** `ascent-override` / `descent-override`
  / `line-gap-override` are percentages of the **post-size-adjust em**. If
  you scale Arial by 1.0712 with `size-adjust`, then `ascent-override: 90.44%`
  means "reserve 90.44% of the scaled em above baseline", and the effective
  ascent in original-em terms is `0.9044 × 1.0712 = 0.9688` — matching
  Inter's 0.968.
- **Spec:** CSS Fonts 5 § `size-adjust`.

```css
size-adjust: 107.12%;         /* x-height ratio + cap-height correction */
```

### Putting the four together

```css
/* Fallback face — reshape Arial to match Inter's line-box. */
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 90.44%;
  descent-override: 22.52%;
  line-gap-override: 0%;
  size-adjust: 107.12%;
}
```

At `font-size: 16px` the browser reserves an effective em of
`16 × 1.0712 = 17.14px`, an ascent of `17.14 × 0.9044 = 15.50px`, a descent
of `17.14 × 0.2252 = 3.86px`, and 0 line-gap — total line-box 19.36px,
matching Inter's `16 × (0.968 + 0.242) = 19.36px` to sub-pixel. Because
`size-adjust` also scales advance widths, Arial's "m" approximates Inter's
wider proportions; horizontal reflow on swap is typically 1–3% instead of
8–10%. No per-glyph advance matching exists in CSS.

---

## Computing Values

The canonical algorithm, used by Capsize, Fontaine, Next.js, Astro, fontpie,
and Brian Louis Ramirez's Fallback Font Generator, follows four steps.

### Step 1 — Extract metrics from both fonts

Tools that read OpenType `head` / `hhea` / `OS/2` tables: **FontDrop**
(https://fontdrop.info — drop a file, inspect in-browser), **Wakamai
Fondue** (similar, pedagogical), **`opentype.js`** or **`fontkit`** (npm,
programmatic), **`fonttools ttx`** (Python, XML dump), or
**[`@capsizecss/metrics`](https://www.npmjs.com/package/@capsizecss/metrics)**
(pre-extracted for most Google Fonts and common system fonts — no binary
needed).

Read these six fields from each font (primary `P` and fallback `F`):
`unitsPerEm` (`head`), `sTypoAscender`, `sTypoDescender` (negative — take
absolute value), `sTypoLineGap`, `sxHeight`, and optionally `sCapHeight`
(all `OS/2`; `sxHeight` / `sCapHeight` require OS/2 v2+). If `sxHeight` is
missing, measure the bounding box of `x` (U+0078); Capsize does this fallback
automatically.

Always use the typo-metric values (`sTypoAscender` etc.), not `hhea.*` or
`usWin*` — the override descriptors coerce the rendering to typo metrics.
See `../metrics/metrics-glossary.md#the-metric-wars` for the platform
politics.

### Step 2 — Normalize by UPM

Every metric becomes a fraction of 1 em: `ascent_em = sTypoAscender / upm`,
and similarly for descent, lineGap, xHeight. Do the same for both primary
(P) and fallback (F). See the "Sans pair" worked example below for the
Inter / Arial numbers.

### Step 3 — Capsize-style formula

```
sizeAdjust        =  P.xHeight_em / F.xHeight_em
ascentOverride    =  P.ascent_em  / sizeAdjust
descentOverride   =  P.descent_em / sizeAdjust
lineGapOverride   =  P.lineGap_em / sizeAdjust
```

All four outputs are unit-less ratios; multiply by 100 to get the `%` the
descriptor expects.

**Why divide by `sizeAdjust`:** Because `size-adjust` scales the em,
the `ascent-override` percentage is taken against the *scaled* em. To get
the primary's ascent-in-primary-ems out of the fallback's scaled ems, you
divide by the scale factor. Mechanically: `override% × sizeAdjust = match in
primary-em units`.

### Step 4 — (Optional) cap-height refinement

A literal x-height ratio gets lowercase right but can leave caps and
punctuation slightly off. Capsize's production formula blends x-height and
cap-height so both align at the same `font-size`. The simpler x-height-only
formula lands within ~1% of Capsize's output — good enough for most work.
See the "Sans pair — Inter → Arial" worked example below for both sets of
values side-by-side.

### The `USE_TYPO_METRICS` interaction

If the **primary font** has `USE_TYPO_METRICS=1` (modern Google Fonts,
Adobe Fonts, most commercial fonts post-2018), typo metrics are authoritative;
compute from `sTypo*` and ship. If it doesn't, the browser may read
`hhea.*` (macOS) or `usWin*` (Windows) instead — compute from whichever
source the rendering actually uses, or override the primary's metrics too
(Capsize does this automatically when you pass `fontMetrics` for both
faces). For variable fonts, compute against the default instance
(`wght=400 wdth=100 opsz=16`); no per-axis override descriptors exist as
of 2026-04.

### Tooling

Prefer tools over hand-computation. Hand-compute only when the primary is
a licensed face whose metrics aren't in any registry and the license
forbids re-upload.

| Tool | Input | Output |
| ---- | ----- | ------ |
| **Capsize** (seek-oss) — the reference implementation | Font files or pre-extracted metrics | `createFontStack()` emits `@font-face` CSS |
| **`@capsizecss/metrics`** | Font name | Pre-extracted metrics object |
| **Fontaine** (UnJS) | Your CSS | PostCSS / Nuxt plugin rewrites `@font-face` with fallback aliases |
| **Next.js `next/font`** | `next/font/google('Inter')` / `next/font/local(…)` | Emits primary + pre-tuned fallback automatically at build |
| **fontpie** | Font file path | CLI prints override CSS |
| **Fallback Font Generator** (screenspan.net/fallback, Brian Louis Ramirez) | Drag & drop UI | Computed override CSS |

URLs in "Sources" below.

---

## `font-size-adjust` — Complementary, Not Redundant

`font-size-adjust` is a **per-element CSS property** that predates the
`@font-face` override descriptors (Firefox 3 in 2008; Baseline 2024 across
Chrome 127 / Safari 17 / Firefox 118). Despite the similar name, it solves
a different problem.

### Syntax (CSS Fonts 5)

```
font-size-adjust = none
                 | [ ex-height | cap-height | ch-width | ic-width | ic-height ]?
                   [ from-font | <number [0,∞]> ]
```

The metric keyword selects *which* aspect is equalized; the number (or
`from-font`) is the target ratio — the aspect as a fraction of `font-size`
that the rendered font must be scaled to match. The one-value legacy form
(`font-size-adjust: 0.5`) is shorthand for `ex-height 0.5`. `from-font`
reads the *primary* font's ratio at parse time and applies it:

```css
body {
  font-family: "Inter", sans-serif;
  font-size-adjust: cap-height from-font;   /* preserve Inter's cap-to-body ratio */
}
```

See `./css-text-properties.md#font-size-adjust` for the detailed property
reference. This file only covers its relationship to the `@font-face`
`size-adjust` descriptor.

### The distinction from `size-adjust`

| Axis | `size-adjust` (descriptor) | `font-size-adjust` (property) |
| ---- | -------------------------- | ----------------------------- |
| **Lives on** | `@font-face`, per-face | Any element, via cascade |
| **What it scales** | The entire fallback face — glyphs, ascent, descent, advance widths | The rendered font at the consumption site, whichever fallback wins |
| **Valued at** | CSS parse time | Paint time, per element, per rendered font |
| **Fallbacks covered** | One (the one it was authored against) | All fallbacks in the cascade |
| **Precision** | Per-metric (ascent independent of descent); sub-0.1% tunable | Single scalar; matches one metric at a time |
| **Layout stability** | **Zero CLS** on swap (line-box fixed pre-load) | Stabilizes apparent letter size; **does not fix line-box height** — CLS still happens |

Said the other way:

- **`size-adjust`** reshapes the fallback's vertical box at the face level.
  Specialized, precise, no FOUT jitter. Specifically cures CLS.
- **`font-size-adjust`** resizes the rendered glyph at the element level
  so x-height (or cap-height) looks consistent regardless of which font
  wins the cascade. General-purpose, coarser, does not cure CLS.

### When to reach for each

Use `@font-face size-adjust` + the three overrides when you ship a specific
web font, know the fallback chain, and want **zero CLS** during FOUT. Use
`font-size-adjust` when you don't know which fallback will win (long
cascades, generic keywords) and want a one-line safety net for x-height
consistency. Use **both** for belt-and-braces: overrides handle the known
fallback, `font-size-adjust` handles unexpected downgrades.

Two things `font-size-adjust` does **not** do: (1) cure CLS by itself —
Bramus Van Damme (web.dev, 2022) and Simon Hearne (2021) both measured
~30% CLS reduction from `font-size-adjust` alone vs ~95% from `@font-face`
overrides; (2) work on scripts without the chosen metric — `ic-width` on
a Latin-only fallback does nothing because `水` isn't in the font.

---

## Worked Examples

Two complete recipes, showing every step from OpenType binary to shipped
CSS. The genre table — every sans, serif, slab, and mono pairing — lives in
`../techniques/fallback-stacks.md`.

### Sans pair — Inter → Arial

**Source metrics** (from `@capsizecss/metrics`, verified via FontDrop
2026-04-17). Inter 4.0: UPM 1000, sTypoAscender 968, sTypoDescender −242,
sTypoLineGap 0, sxHeight 546, sCapHeight 728, `USE_TYPO_METRICS=1`.
Arial 7.00: UPM 2048, sTypoAscender 1854, sTypoDescender −434, sTypoLineGap
67, sxHeight 1062, sCapHeight 1467.

**Normalize and apply:**

```
Inter  →  asc=0.968, desc=0.242, gap=0.000, xh=0.546
Arial  →  asc=0.905, desc=0.212, gap=0.033, xh=0.519

sizeAdjust       = 0.546 / 0.519       = 1.0520   (x-height-only)
                 = 1.0712                          (Capsize, cap-corrected)

ascentOverride   = 0.968 / 1.0712      = 0.9037  → 90.44%
descentOverride  = 0.242 / 1.0712      = 0.2259  → 22.52%
lineGapOverride  = 0.000 / 1.0712      = 0.0000  →  0.00%
```

**Final CSS:**

```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter[wght].woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Inter Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 90.44%;
  descent-override: 22.52%;
  line-gap-override: 0%;
  size-adjust: 107.12%;
}

:root {
  font-family:
    "Inter",
    "Inter Fallback",
    system-ui,
    Arial,
    sans-serif;
}
```

At `font-size: 16px`, both faces compute to a 19.36px line-box (Inter:
`16 × (0.968 + 0.242) = 19.36`; Inter Fallback: `16 × 1.0712 × (0.9044 +
0.2252) = 19.36`). Line-box match: exact within rounding. Horizontal drift
on swap: < 2%.

### Serif pair — Source Serif 4 → Georgia

**Source metrics.** Source Serif 4: UPM 1000, sTypoAscender 918,
sTypoDescender −335, sTypoLineGap 0, sxHeight 475, sCapHeight 656,
`USE_TYPO_METRICS=1`. Georgia: UPM 2048, sTypoAscender 1878,
sTypoDescender −449, sTypoLineGap 0, sxHeight 986, sCapHeight 1410.

**Normalize and apply:**

```
SS4      →  asc=0.918, desc=0.335, gap=0.000, xh=0.475
Georgia  →  asc=0.917, desc=0.219, gap=0.000, xh=0.481

sizeAdjust       = 0.475 / 0.481  = 0.9875   (x-height-only)
                 = 0.9866                     (Capsize, cap-corrected)

ascentOverride   = 0.918 / 0.9866 = 0.9305  → 93.05%   (Capsize: 91.80%)
descentOverride  = 0.335 / 0.9866 = 0.3395  → 33.95%   (Capsize: 33.50%)
lineGapOverride  = 0.000 / 0.9866 = 0       →  0.00%
```

The ~1.3% gap between hand-computed and Capsize is Capsize's baseline-
trimming logic: Source Serif 4 has deep descenders, and Capsize trims a bit
to avoid over-reserving vertical space.

**Final CSS:**

```css
@font-face {
  font-family: "Source Serif 4";
  src: url("/fonts/SourceSerif4-Variable.woff2") format("woff2-variations");
  font-weight: 200 900;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Source Serif 4 Fallback";
  src: local("Georgia");
  ascent-override: 91.80%;
  descent-override: 33.50%;
  line-gap-override: 0%;
  size-adjust: 98.66%;
}

:root {
  font-family:
    "Source Serif 4",
    "Source Serif 4 Fallback",
    "Iowan Old Style",
    Georgia,
    "Times New Roman",
    serif;
}
```

Note how Source Serif's x-height (0.475) is slightly *smaller* than Georgia's
(0.481) — hence `size-adjust: 98.66%` (scaling Georgia down). Georgia was
designed by Matthew Carter specifically for screen rendering and has a
notably tall x-height for a serif; book-serif web fonts often need to scale
Georgia *down*, whereas display-serif web fonts (Playfair, Bodoni) need to
scale it *up*.

### More pairings

`../techniques/fallback-stacks.md` has: geometric sans, humanist sans,
neo-grotesque sans, transitional serif, modern serif, slab serif, monospace,
and a CJK recipe with Hiragino / Yu Gothic / Noto Sans CJK JP chains.

---

## Pitfalls

### Double-leading from an unset `line-gap-override`

If the primary has `sTypoLineGap = 0` (Inter, Roboto, Geist — most modern
variable fonts) but the fallback doesn't (Arial 3.3%, Times New Roman
4.2%), omitting `line-gap-override: 0%` leaves the fallback with double
leading. Symptom: paragraphs ~5% taller during FOUT and collapse on swap.
Set it explicitly, even when zero.

### `size-adjust > 100%` distorts `ch` and measure math

`ch` is the advance of `0` in the current font. `size-adjust: 107%` grows
the fallback's `ch` by 7%. A rule `max-width: 65ch` reserves 7% more
horizontal space during FOUT than it will post-swap — so columns reflow
*by container* on swap, not just by text. Fix: use `rem` or `em` for
container widths, not `ch`; or accept the drift and tolerate 1–2% CLS.

### `size-adjust > 100%` amplifies synthesized bold

If the fallback has no real Bold member, the browser synthesizes bold by
stroke-doubling. `size-adjust: 107%` inflates the already-synthesized
stroke, making fake bold look ~10% heavier than intended. Prefer fallbacks
with real Bold files (Arial Bold, Georgia Bold are universal); avoid
fallbacks without a Bold (some Linux stacks).

### Variable-font primary with wide `opsz`, static fallback

Variable fonts with `opsz` (Roboto Flex, Source Sans 3) have x-height that
*changes across axes*. Compute overrides against the **most-used instance**.
If 90% of copy is 16–20px body, compute at `opsz=16`. No per-axis override
descriptors exist as of 2026-04 — you pick one and accept the drift at
extremes.

### `USE_TYPO_METRICS` mismatch between primary and fallback

Modern Google Fonts have `USE_TYPO_METRICS=1`; locally-installed Arial
on Windows 7 does not. Modern browsers mostly paper over this by reading
`sTypo*` regardless of the flag, but legacy engines differ. For robust
legacy support, also override the primary's ascent/descent via its own
`@font-face` — bringing both faces under the same metric regime.

### Cross-platform `local()` resolution drift

`local("Helvetica")` on macOS can resolve to Helvetica (T1), Helvetica
(TrueType), or Helvetica Neue depending on OS version. Metrics differ by
1.5–3%. Chain locals most-specific-first:
`local("HelveticaNeue"), local("Helvetica Neue"), local("Arial"), local("ArialMT")`.

---

## Browser Support (2026-04)

All four descriptors are in **CSS Fonts 5 Editor's Draft** and shipped
across all major engines. `font-size-adjust` (the older property) reached
Baseline 2024.

| Feature                      | Chrome / Edge  | Firefox     | Safari        | Baseline status |
| ---------------------------- | -------------- | ----------- | ------------- | --------------- |
| `ascent-override` (`@font-face`) | 87 (2020-11) | 89 (2021-03) | 17 (2023-09) | Baseline **2023** |
| `descent-override`           | 87 (2020-11)   | 89 (2021-03) | 17 (2023-09) | Baseline **2023** |
| `line-gap-override`          | 87 (2020-11)   | 89 (2021-03) | 17 (2023-09) | Baseline **2023** |
| `size-adjust`                | 92 (2021-07)   | 92 (2021-07) | 17 (2023-09) | Baseline **2023** |
| `font-size-adjust` (one-value, ex-height default) | 127 (2024-07) | 3 (2008), re-landed full 118 (2023-09) | 17 (2023-09) | Baseline **2024** |
| `font-size-adjust` (two-value, `cap-height` / `ch-width` / `ic-width` / `ic-height`) | 127 (2024-07) | 118 (2023-09) | 17 (2023-09) | Baseline **2024** |
| `font-size-adjust: from-font` | 127 (2024-07) | 118 (2023-09) | 17 (2023-09) | Baseline **2024** |

Source: MDN Browser Compatibility tables (accessed 2026-04-17), CanIUse
`mdn-css_at-rules_font-face_ascent-override` and siblings, Interop 2023 /
2024 progress reports.

### Known gaps and bugs (as of 2026-04)

- **WebKit bug 232571** (fixed Safari 17.3, 2024-01): `size-adjust` not
  applied to `local()` sources in some cases. Test on Safari 16.x.
- **Chromium issue 1270242** (fixed Chrome 94): `ascent-override > 150%`
  could produce negative line-heights.
- **Firefox 89–92:** `size-adjust < 50%` rounded incorrectly; fixed in 93.
- **Safari `font-size-adjust: from-font` on variable fonts** reads metrics
  from the default instance regardless of `wght` / `opsz`. No cross-browser
  agreement on correct behavior as of 2026-04.
- **All engines:** No per-axis override descriptors. One number per
  descriptor, applied regardless of `font-variation-settings`.
- **Legacy targets:** Android WebView < 7.0 and IE 11 have no support;
  negligible share in 2026.

Interop 2024 resolved sub-percent rounding differences; all three engines
now agree within ~0.05%. Prior to that, Chrome and Firefox could differ by
up to 0.5% on pathological fractional inputs.

---

## Anti-patterns

- **Computing overrides with unnormalized units.** `ascent-override: 968%`
  is a classic — someone read `sTypoAscender = 968` on UPM-1000 and forgot
  to divide. Result: 9.68-em-tall line-box per line. Always divide by UPM
  first; always multiply by 100 for the percentage.
- **Using `font-display: optional` as a substitute.** `optional` avoids CLS
  by hiding the primary font on slow connections, not by fixing the metric
  mismatch. Combine `font-display: swap` + overrides — don't substitute.
- **Setting `size-adjust` on the primary face.** Overrides belong on the
  fallback alias. `size-adjust: 107%` on Inter's own `@font-face` makes
  Inter render 7% larger than you asked for — every heading too big.
- **Relying on `font-size-adjust` alone for zero CLS.** It scales the
  rendered glyph; it does not change line-box height. See the next section.
- **Per-breakpoint override values.** Overrides come from font metrics; they
  are viewport-independent. Adjust `line-height` in media queries instead.
- **Omitting `src: local(…)`.** An `@font-face` with only override
  descriptors and no `src` is invalid (CSS Fonts 5). Browsers silently drop
  it; the page falls through to un-overridden generic `sans-serif`.
- **Placing the fallback alias after the generic keyword.** Generics always
  match; anything after them is unreachable. Correct order:
  `"Inter", "Inter Fallback", system-ui, sans-serif`.
- **Trusting `normal` defaults cross-browser.** `ascent-override: normal`
  means "use the font's own ascent" — which varies by platform. For portable
  results always set explicit percentages.
- **Computing overrides once, then widening the `local()` chain.** If you
  shipped against Arial and later prepend `local("Helvetica Neue")`, the
  overrides no longer fit Helvetica Neue's different metrics. Either keep
  the chain stable or split into per-OS aliases (see the "Poppins Fallback"
  vs "Poppins Fallback Android" pattern in `../techniques/fallback-stacks.md`).

---

## Sources

### Specifications
- [W3C CSS Fonts 5 — Editor's Draft, font-metrics-override-desc](https://drafts.csswg.org/css-fonts-5/#font-metrics-override-desc) (2026-04). Authoritative syntax for all four descriptors.
- [W3C CSS Fonts 5 — `size-adjust` descriptor](https://drafts.csswg.org/css-fonts-5/#size-adjust-desc) (2026-04).
- [Microsoft OpenType `OS/2` table](https://learn.microsoft.com/en-us/typography/opentype/spec/os2) (accessed 2026-04-17). `sTypoAscender`, `sTypoDescender`, `sTypoLineGap`, `sxHeight`, `sCapHeight`, `USE_TYPO_METRICS`.
- [Microsoft OpenType `hhea` table](https://learn.microsoft.com/en-us/typography/opentype/spec/hhea) (accessed 2026-04-17).

### MDN reference pages
- [`@font-face/ascent-override`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override) (2026-03)
- [`@font-face/descent-override`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/descent-override) (2026-03)
- [`@font-face/line-gap-override`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/line-gap-override) (2026-03)
- [`@font-face/size-adjust`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust) (2026-03)
- [`font-size-adjust`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust) (2026-03)

### Tooling
- [Capsize — seek-oss/capsize](https://github.com/seek-oss/capsize) (v5, 2026). Reference implementation of the x-height + cap-height formula; ships `createFontStack()`.
- [`@capsizecss/metrics`](https://www.npmjs.com/package/@capsizecss/metrics) (2026). Pre-extracted metrics for most Google Fonts and common system fonts.
- [Fontaine — unjs/fontaine](https://github.com/unjs/fontaine) (2026). PostCSS / Nuxt integration using Capsize.
- [Next.js Font Optimization](https://nextjs.org/docs/app/api-reference/components/font) (v15+, 2026). Built-in; reference source for override values per Google Font.
- [fontpie](https://github.com/jmeistrich/fontpie) (2026). CLI override computation.
- [Fallback Font Generator — Brian Louis Ramirez](https://screenspan.net/fallback) (2023). Drag-and-drop browser UI.

### Writeups
- [Bramus Van Damme — "Improved font fallbacks" (web.dev)](https://web.dev/blog/font-metric-overrides) (2021, revalidated 2024). Canonical developer walkthrough.
- [Simon Hearne — "How to avoid layout shifts caused by web fonts"](https://simonhearne.com/2021/layout-shifts-webfonts/) (2021). Diagnostic methodology and CLS measurement.
- [Barry Pollard — "Reducing Layout Shift" (Smashing Magazine)](https://www.smashingmagazine.com/2022/05/reducing-layout-shift-font-fallbacks/) (2022). Production case studies; before/after CLS numbers.
- [Chrome Developers — "Improved font fallbacks"](https://developer.chrome.com/blog/font-fallbacks) (2022, revalidated 2024). Chrome's shipping rationale.
- [Google Fonts metric normalization](https://github.com/googlefonts/gf-docs/tree/main/Spec) (2018–ongoing). Policy for `USE_TYPO_METRICS` on hosted fonts.
- Karolina Lach — "Mismatched Font Metrics" (2018). First-accessible practitioner write-up of the metric wars.
- [Interop 2024 — Font Metrics](https://wpt.fyi/interop-2024) (2024). Cross-browser conformance; outcome: sub-percent agreement across engines.
