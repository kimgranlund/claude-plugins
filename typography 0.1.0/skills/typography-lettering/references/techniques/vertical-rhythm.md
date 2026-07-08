---
date: 2026-04-18
coverage: deep
peers:
  - ./measure.md
  - ./modular-scale.md
  - ../contemporary/metric-overrides.md
  - ../contemporary/css-text-properties.md
  - ../metrics/metrics-glossary.md
  - ../metrics/units.md
primary_sources:
  - https://24ways.org/2006/compose-to-a-vertical-rhythm/
  - https://clagnut.com/blog/1942
  - https://markboulton.co.uk/journal/five-simple-steps-to-designing-grid-systems-part-4/
  - https://markboulton.co.uk/journal/incremental-leading/
  - https://book.webtypography.net/
  - https://v5.jasonsantamaria.com/articles/baseline-grids-on-the-web/
  - https://seek-oss.github.io/capsize/
  - https://github.com/seek-oss/capsize
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-trim
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-edge
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box
  - https://developer.chrome.com/blog/css-text-box-trim
  - https://caniuse.com/css-text-box-trim
  - https://medium.com/microsoft-design/leading-trim-the-future-of-digital-typesetting-d082d84b202
  - https://drafts.csswg.org/css-inline-3/
  - https://drafts.csswg.org/css-rhythm-1/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/line-height-step
  - https://developer.mozilla.org/en-US/docs/Web/CSS/baseline-source
  - https://spec.fm/specifics/8-pt-grid
  - https://basehold.it/
  - https://sassline.com/
notes:
  - This file is tier=deep. Voice matches measure.md and modular-scale.md — dense factual prose, dated browser-support claims, "traps and gotchas" framing.
  - Does not generate tokens. Rhythm-unit math is derived inline from this file's recipes (no generator skill is installed — a handled dead-end); realizing rhythm values as a project token layer belongs to the `token-builder` agent.
  - Metric theory (UPM, ascent, descent, x-height, cap-height, line-gap) is not repeated here; see ../metrics/metrics-glossary.md.
  - Fallback metric tuning is not repeated; see ../contemporary/metric-overrides.md.
---

# Vertical Rhythm

Vertical rhythm is the typographic convention that the baselines of consecutive lines of text fall on a consistent grid — a set of equidistant horizontal lines that governs line-height, margin, padding, and block-level vertical space. Inherited from metal typesetting, where the **leading** (strips of lead between lines) came in fixed gauges and a page had a fixed baseline pitch, the rule is: every vertical measure in the composition is a multiple or a clean fraction of a single **rhythm unit** (historically a line-height; on the web usually expressed in pixels or rem).

The 2026 reality is that the convention is half-achievable on the web. The CSS box model puts text inside a **line-box** of a height determined by font metrics and `line-height`, with the actual baseline sitting somewhere inside that box — not at its bottom, not predictably. Setting `line-height: 24px` on body text does not place the baseline at a `y`-position that is a multiple of 24 from the viewport top. It places the line-box there. The baseline floats inside the line-box according to ascent/descent metrics of whichever font wins the cascade at paint time. Change the font, change the baseline offset. Change the fallback, change the drift.

Two things changed between ~2022 and 2026 that make rhythm newly tractable: (1) **`text-box-trim` + `text-box-edge`** (Safari 18.2 Dec 2024, Chrome/Edge 133 Feb 2025, Firefox unshipped as of 2026-04) remove the half-leading padding above ascenders and below descenders, snapping the rendered text-box to the cap-height or x-height envelope. This restores print-like precision where supported. (2) **Subgrid and `grid-auto-rows`** let layout enforce rhythm independent of line-box internals. Both coexist with the older pre-2025 recipe of just tolerating metric wobble as invisible under reasonable conditions.

This file covers: the definition and historical genealogy, the mechanics and the mathematical trap, the 2026 solution stack, alternative philosophies (relative rhythm, rhythm-as-guideline, no-rhythm), working CSS recipes, interaction with dynamic type and mixed scripts, common failures, and an honest assessment of how much rhythm actually matters for reading comprehension versus how much it is an aesthetic convention. Metric theory (`sTypoAscender`, UPM, x-height) is not repeated; see `../metrics/metrics-glossary.md`. Fallback metric tuning is in `../contemporary/metric-overrides.md`.

---

## Definition and History

### Letterpress origin

In metal typesetting, each character is cast on a rectangular body whose height is fixed for a given point size. Lines stack by adjacency — each line's body butts against the next — and the compositor inserts **leads** (thin strips of lead, typically 1 pt, 2 pt, or 3 pt) between lines to open the spacing. The baseline pitch — the distance from one line's baseline to the next — is therefore **type size + leading**, measured in points, and it is constant across the page because the lead gauges are constant. A 10-on-12 setting (10 pt type, 12 pt leading, i.e. 2 pt of lead) has a 12 pt baseline pitch; every sixth line sits 72 pt (one inch) below the first. A book page is literally ruled by the compositor's gauge.

Vertical rhythm as a practice is *nothing more than* the transposition of this mechanical constraint into a design principle. The reason it "feels right" to a trained eye is the long exposure of the reading public to books set this way — the cue is cultural and technical, not perceptual in the eye-tracking sense.

### Bringhurst and the web-design revival

Robert Bringhurst's *The Elements of Typographic Style* (1st ed. 1992; 4th ed. 2013) devotes Chapter 2 ("Rhythm & Proportion") and Chapter 5 ("Structural Forms and Devices") to the argument that "[v]ertical rhythm is the single most important factor in the typographic appearance of a text block." Bringhurst's framing is print-native — he writes before the web has a typography culture — but his *Elements* became the single most cited reference when web designers in the mid-2000s began to argue for typographic discipline on screen.

The bridge from Bringhurst to CSS was built between 2005 and 2010 by a small set of writers:

- **Richard Rutter**, *24ways*, December 2006, [*Compose to a Vertical Rhythm*](https://24ways.org/2006/compose-to-a-vertical-rhythm/) — the canonical article. Rutter's recipe: pick a basic line-height (e.g., 24px for 16px body), set `line-height` on `body` to that value in em terms, and set every block-element's `margin-top` and `margin-bottom` to multiples of it. Rutter acknowledges that headings larger than the rhythm unit require either (a) sizing to a multiple of the unit, or (b) absorbing the overflow into asymmetric margins. The article is still widely linked in 2026 and the recipe still mostly works.
- **Mark Boulton**, *Five simple steps to designing grid systems* (2005–2007), with Part 4 dedicated to vertical rhythm; and *[Incremental leading](https://markboulton.co.uk/journal/incremental-leading/)* (2007), introducing the idea that leading can *grow* with font-size rather than being uniform — a concession that strict-constant leading looks dense at display sizes. Boulton's later writing shifts toward **rhythm as guideline, not constraint** (see "Alternative philosophies" below).
- **Richard Rutter**, *Web Typography* (2017, self-published; companion to [webtypography.net](https://book.webtypography.net/), his online "Elements of Typographic Style Applied to the Web"). Deepens the 2006 article into a book; concedes more cases where strict rhythm breaks on the web.
- **Jason Santa Maria**, *[Baseline Grids on the Web](https://v5.jasonsantamaria.com/articles/baseline-grids-on-the-web/)* (2007–2011) and *On Web Typography* (A Book Apart, 2014). Santa Maria's position: baseline grids are "incredibly difficult to maintain" on the web because of replaced content, browser rendering variance, and metric drift — treat rhythm as a *design target* rather than a *constraint that must not deviate*.
- **Oliver Reichenstein**, *Information Architects* blog and *[Web Design is 95% Typography](https://ia.net/topics/the-web-is-all-about-typography-period)* (2006), which made the cultural case for typography-first web design that Rutter's rhythm recipe operationalized.

### 8-point grid, 4-point grid, and Material/HIG adoption

Parallel to and overlapping with the baseline-rhythm tradition is the **point-grid** convention that dominates product UI from roughly 2014 onward:

- **Apple** introduced the 8-point grid in Human Interface Guidelines for iOS 7 (2013) and systematized it in iOS/HIG updates through 2014–2016. Elements size and space in multiples of 8 pt. Apple's own interfaces deviate routinely but the grid is the default.
- **Google** introduced Material Design in 2014 on an 8 dp grid for component spacing with a 4 dp baseline grid for typographic alignment — later (Material Design 3, 2021) codified as a 4 dp spatial system with 8 dp component increments. Material sets text on a 4 dp sub-grid specifically so that text baselines land on ruled positions.
- **Microsoft Fluent 2**, **IBM Carbon**, **Shopify Polaris**, **Atlassian Design System**, and most major product design systems adopted some variant of 4 or 8 as the base unit between 2015 and 2020.

The relationship between the point-grid convention and Bringhurst-style baseline rhythm is subtle. The point-grid enforces **block-level spacing** on a grid; it does *not* by itself enforce that text baselines land on the grid. That additional constraint — baselines on the grid — requires line-height-on-grid plus font-metric control. Most point-grid design systems *approximate* baseline alignment (e.g., Material sets `line-height` so that the baseline is within ~1 dp of a 4 dp gridline at body sizes) but do not guarantee it pre-`text-box-trim`.

The practical inheritance: when a 2026 designer says "we're on an 8-point grid," they usually mean the spacing scale is multiples of 8. Whether text sits on baselines that are multiples of 8 is a separate, often-unasked question.

---

## The Mechanics

### The rhythm unit

A vertical rhythm composition declares one number — the **rhythm unit** — and every vertical measure in the design is a multiple of it. Typical choices:

- `24px` — the canonical Rutter 2006 unit; 16px body × 1.5 line-height = 24px.
- `20px` — denser; 16px body × 1.25.
- `28px` or `32px` — looser editorial; 18 or 20px body at 1.5–1.6.
- `4px`, `8px` — sub-grid for smaller elements, with text landing on every 6th or 3rd line.

The rhythm unit is usually expressed in `rem` at author-time so that it scales with user font-size preferences: `--rhythm: 1.5rem;` on a 16px root gives 24px. Math in the stylesheet uses `calc(var(--rhythm) * N)`.

### Sizing block-level spacing

Every `margin-top`, `margin-bottom`, `padding-top`, `padding-bottom`, `border-block-start`, `border-block-end` on a block element must be a multiple of the rhythm unit. Borders and outlines count toward total vertical consumption; `box-sizing: border-box` does not help — border height is its own addition on top of content height. The compositor's usual move: wrap borders and shadows into the padding budget by adjusting padding to `calc(var(--rhythm) * N - var(--border-width))`.

### Sizing type

Body text is the anchor. With `line-height: 1.5` on a 16px body, the line-box is 24px — one rhythm unit. Subsequent paragraphs stack cleanly.

Headings complicate it. A 32px heading at `line-height: 1.2` has a 38.4px line-box — not a multiple of 24. Two options:

1. **Round the line-box to a multiple.** Set `line-height: 48px` (absolute) or `line-height: 1.5` unitless so the line-box is two rhythm units tall. Visually this means the heading occupies 48px of vertical space, which matches the grid but leaves a lot of air above and below the heading's visible strokes.
2. **Keep the line-height tight, absorb the delta in margins.** Set `line-height: 1.2` and adjust `margin-top` / `margin-bottom` so `margin-top + line-box + margin-bottom` is a multiple of 24. This keeps the heading visually dense but requires manual per-heading math.

Option 1 is the Rutter-canonical approach; option 2 is the Boulton *incremental leading* approach. A third option, **absorb in grid**, uses `display: grid; grid-auto-rows: var(--rhythm);` and makes each text block span the required number of rows — see Recipe C.

### Multi-line headings

A heading that wraps to two lines consumes two times its line-box height. If the grid counted on a one-line heading, the wrap breaks the rhythm downstream. Defenses:

- Cap heading measure so wraps are predictable (`h1 { max-width: 20ch }`; see `./measure.md`).
- Use `text-wrap: balance` on headings so that when they do wrap, the two-line case is a clean n-row consumption.
- Accept the rhythm break on wrap — most editorial systems do.

### Borders and shadows

Borders add to the block dimension. A `border-block-end: 1px solid` on an otherwise rhythm-sized element pushes everything below by 1px — rhythm breaks. Standard fix: subtract the border from padding: `padding-block-end: calc(var(--rhythm) - 1px);`. `outline` does not affect layout (it is drawn outside the box without reserving space), so outline-based focus rings are rhythm-safe. `box-shadow` likewise does not affect layout.

### Replaced elements

`<img>`, `<video>`, `<iframe>`, `<canvas>`, form controls (`<input>`, `<select>`, `<textarea>`), and `<svg>` size to their intrinsic content or attributes — not to the rhythm grid. A 300px-tall image inside a prose column breaks rhythm unless either (a) the image is sized to a multiple of the rhythm unit (`aspect-ratio` + `width: 100%` then clamp height), or (b) the image is wrapped in a container whose `min-height` snaps to a multiple, with centering inside. Form controls (`<input>`) have their own internal line-height and padding that varies per browser; a 24px-rhythm page typically needs explicit `height: calc(var(--rhythm) * 2)` on inputs with `padding-block: 0` and `box-sizing: border-box` to land them on the grid.

---

## The Mathematical Trap

The CSS `line-height` property does **not** place text baselines on a grid. It determines the height of the line-box. The baseline's position *inside* the line-box depends on the font's metrics, not on the author. This is the central technical fact about vertical rhythm on the web and it is the reason the 2006 Rutter recipe is an approximation rather than a guarantee.

### What `line-height` actually does

`line-height` sets the height of the inline-level line-box for text in an element. The browser lays out each line of text by:

1. Computing the **content area** — a box whose height is approximately `font-size × (ascent + descent) / upm`, using the font's metric tables (`OS/2.sTypoAscender`, `sTypoDescender`, etc. — see `../metrics/metrics-glossary.md`).
2. Computing **half-leading** — the difference between `line-height` and the content-area height, divided by two, applied above and below the content area.
3. The **line-box** is the content area plus half-leading on each side.
4. The **baseline** sits inside the content area, at a position determined by `(ascent / (ascent + descent)) × content-area-height` down from the content-area top.

Two fonts at identical `font-size` and `line-height` produce line-boxes of the same height but baselines at *different* positions inside the box. This is because their ascent/descent ratios differ.

Example (normalized to em, reading from `../contemporary/metric-overrides.md`'s Inter vs Arial table):

- **Inter 4.0**: ascent 0.968, descent 0.242 → ratio 0.8 : 0.2 → baseline sits 80% down the content area.
- **Arial 7.00**: ascent 0.905, descent 0.212 → ratio 0.810 : 0.190 → baseline sits 81% down.
- **Georgia**: ascent 0.917, descent 0.219 → ratio 0.807 : 0.193.

At 16px `font-size` and 24px `line-height`, the content area for each font is slightly different (19.36px for Inter, 17.87px for Arial, 18.18px for Georgia), and the half-leading differs (2.32px, 3.07px, 2.91px). The baseline's vertical offset from the top of the line-box is therefore:

```
Inter:   2.32 + (0.8  × 19.36)  = 17.81 px from top of line-box
Arial:   3.07 + (0.81 × 17.87)  = 17.55 px
Georgia: 2.91 + (0.807 × 18.18) = 17.58 px
```

These differ by up to 0.26 px per line. Over 40 lines of prose that is a ~10 px drift — visible if you overlay a ruled grid, invisible in normal reading. The effect compounds across fallback swaps (FOIT/FOUT on slow networks) and across mixed-font systems (body in Inter, heading in a serif — their baselines are misaligned by the combined ascent-ratio delta).

The author-controlled lever for this is **metric overrides** (`ascent-override`, `descent-override`, `line-gap-override`, `size-adjust`) on `@font-face`. See `../contemporary/metric-overrides.md` for the mechanism. These coerce a fallback's metrics to match the primary's, so baseline positions *converge* across the fallback-swap boundary. They do not give you an explicit "put the baseline at y = 24n" knob.

### `vertical-align: baseline` does not establish a grid

A common confusion: `vertical-align: baseline` aligns the baselines of inline-level siblings *within the same line-box*. It says nothing about where that line-box sits, and nothing about where successive line-boxes' baselines fall. It is an intra-line alignment property, not a cross-line grid primitive.

### `line-height-step` — removed from contention

The CSS Rhythmic Sizing module (CSS Rhythm 1) drafted a `line-height-step` property that rounded line-box heights *up* to the nearest multiple of a specified length — the explicit grid-snapping primitive that rhythm enthusiasts wanted. Chrome shipped it behind a flag in 2017 (Chrome 60, flagged; Intent to Ship approvals in April 2017). Mozilla and WebKit did not ship; the Latin use case was removed from the spec as "too controversial for Latin, demand from CJK is strong"; the CJK-focused version has not moved in years. As of 2026-04, **`line-height-step` is not shipped in any engine** and the spec is stalled. Do not use it.

The working replacement is `text-box-trim` plus explicit grid-based layout.

### `baseline-source` — alignment, not grid

`baseline-source: auto | first | last` (Chromium 111+ March 2023, Firefox 115+ July 2023, Safari unshipped as of 2026-04) selects *which* baseline of an inline-level box is used when aligning with sibling baselines. It matters for boxes with multiple possible baselines — multi-line inline-blocks, inline-flex containers — and is useful for aligning badges and icons with adjacent text. It does **not** establish a grid. It does not snap line-boxes to multiples of anything. File it under "inline alignment," not "vertical rhythm."

---

## Why Rhythm is Harder on the Web than in Print

Beyond the metric-trap, five structural reasons rhythm is harder in CSS than in a print compositor's galley:

### 1. Replaced elements

Images, iframes, canvases, form controls, and embedded video size to their content or attributes. A 300px-tall hero image inside a 24px-rhythm prose column creates a 300px gap that is not a multiple of 24. Compositors in print own the page and can make the image fit; a web author owns the template but not the content, and user-contributed images arrive at arbitrary dimensions.

### 2. Variable line-wrapping

A one-line heading becomes a two-line heading at a narrower viewport; a 45px vertical consumption becomes 90px; every block downstream shifts by 45px. Unless margins absorb the delta (Boulton-style asymmetric margins that vary with line count) or the entire column is placed on a grid-auto-rows scaffold that spans whole numbers of rows, the rhythm wobbles.

### 3. Borders, shadows, and dividers

Each `border-block-end: 1px` adds 1px to the block dimension. Every divider of a non-rhythm pixel count breaks the grid. Standard fix: always subtract borders from padding. Box-shadow and outline are rhythm-safe (drawn without reserving layout space). `filter: drop-shadow()` is also rhythm-safe.

### 4. Mixed inline content

A line of prose with an inline code span (`<code>` at `font-size: 0.9em`), an icon (`<svg>` at its own height), or a badge (`<span>` with padding) produces a line-box whose height is the max of all its inline participants. A body line that is normally 24px tall becomes 28px when an icon intrudes. The next line's baseline shifts.

### 5. Sub-pixel rounding

Browsers round final pixel positions at paint time. A grid with `--rhythm: 1.5rem` at 16px root gives 24px — clean. At 15px root (user preference) it gives 22.5px; across 20 lines the accumulated rounding error can reach 5–10px. Pinning the rhythm to an integer-px value (`--rhythm: 24px`) avoids the drift at the cost of not scaling with user font-size — an accessibility regression.

These are not bugs. They are structural properties of a flow-based layout engine rendering arbitrary content on arbitrary viewports with user-overridable settings. A strict baseline grid that holds under all conditions is not achievable in CSS without extraordinary measures (every element grid-laid-out, every image `aspect-ratio`-pinned, every font metric-overridden, `text-box-trim` applied everywhere, and even then — drift).

---

## Modern Solutions — 2022–2026

### `text-box-trim` + `text-box-edge` (the 2025 reset)

The CSS Inline Layout Module 3 shipped a pair of properties (originally `leading-trim` / `text-edge`; renamed to `text-box-trim` / `text-box-edge` in 2023) that let the author **remove half-leading on the first and last lines** of a block, snapping the rendered text-box to a specified typographic envelope (cap-height, x-height, ideographic box). This is the property Microsoft's Ethan Wang argued for in [*Leading-Trim: The Future of Digital Typesetting*](https://medium.com/microsoft-design/leading-trim-the-future-of-digital-typesetting-d082d84b202) (2020).

**Browser support (as of 2026-04):**

| Engine | Status | Version |
| --- | --- | --- |
| Safari | Shipped | 16.4 (March 2023, non-standard `leading-trim`) → 18.2 (December 2024, standardized) |
| Chrome / Edge | Shipped | 133 (February 2025) |
| Firefox | Unshipped | Standards-position positive, on Mozilla's "safe-to-release" list as of 2026-04; no ship commitment |

**Syntax.**

```css
/* Longhand */
.heading {
  text-box-trim: trim-both;
  text-box-edge: cap alphabetic;
}

/* Shorthand — equivalent to the above */
.heading {
  text-box: trim-both cap alphabetic;
}
```

`text-box-trim` values: `none` (default), `trim-start`, `trim-end`, `trim-both`. `text-box-edge` takes one or two `<text-edge>` values; the first is the over-edge (block-start), the second the under-edge (block-end). Valid over-edge values: `text | ideographic | ideographic-ink | cap | ex`. Valid under-edge values: `text | ideographic | ideographic-ink | alphabetic`.

**What it does.**

Without `text-box-trim`, a block of text has half-leading above the first line's ascender and below the last line's descender — visible as dead space when the block has a background color or sits next to a non-text element. `text-box-trim: trim-both; text-box-edge: cap alphabetic;` snaps the top of the block to the cap-line and the bottom to the baseline, producing a text-box whose height equals the cap-height across all first-to-last-line spans. Between lines, half-leading is preserved (lines still space normally); only the *edges* of the block are trimmed.

**Impact on rhythm.**

For single-line blocks (buttons, nav items, badges, headings-as-UI-elements), `text-box-trim` removes the ~6–12px of half-leading that was silently eating into the 8pt / 24px grid. A 48px button with body-sized text now actually has 48px of grid space for background and padding, instead of 36px plus 12px of hidden leading. The spacing scale finally means what it says.

For multi-line blocks (prose, headings that wrap), `text-box-trim` does the same on the first and last lines — middle lines remain unchanged. Combined with `line-height` in clean multiples of the rhythm unit, this is the first recipe where baseline grid and margin grid coincide reliably.

**Caveats (2026-04):**

- **Firefox unshipped.** Any production site with >1% Firefox traffic needs a graceful fallback: either provide pre-`text-box-trim` margins that "look close enough" on Firefox, or use feature queries to deliver different spacing to Firefox.
- **Ascender / descender trim is partial.** `text-box-edge: text` trims to the ascender top / descender bottom (the full content-area height) — this is effectively *no* trim beyond removing half-leading. Use `cap` / `ex` for the tight snap.
- **Per-font cap-height and x-height metrics required.** The browser reads `OS/2.sCapHeight` / `sxHeight` from the font file. If these fields are missing or zero (older or poorly-prepared fonts), browsers fall back to measuring the glyph bounding box of `H` / `x` or to heuristics — behavior is then not portable. Modern Google Fonts and most commercial fonts ship these metrics correctly; check with FontDrop or Wakamai Fondue if in doubt (see `../metrics/metrics-glossary.md`).
- **CJK and complex scripts.** `text-box-edge: ideographic alphabetic` is the CJK-appropriate choice; `cap` is Latin-specific. Mixed-script blocks need careful consideration.

**The shorthand consensus.** For Latin body text, `text-box: trim-both cap alphabetic;` is the modern default for single-line UI elements (buttons, labels, headings) where the rendered size must equal a grid-step. For multi-line prose, `text-box: trim-both cap alphabetic;` is also recommended but produces subtler visual effect.

### Grid-based rhythm

`display: grid; grid-auto-rows: var(--rhythm);` is the most reliable modern technique for enforcing rhythm *independent of font metrics*. Each row of the grid is one rhythm unit; text blocks span an explicit number of rows calculated from their content.

```css
.prose {
  display: grid;
  grid-auto-rows: var(--rhythm);
}

.prose > * {
  /* Each block spans n rows — calculated per element */
}

.prose > p {
  grid-row: span 3;  /* 3-line paragraph at 24px rhythm = 72px */
}

.prose > h2 {
  grid-row: span 2;  /* heading + margin fit in 48px */
}
```

The weakness: `grid-row: span N` must be calculated per element, and content-driven counts (how many lines does *this* paragraph wrap to?) are not known at author-time. The technique works best for fixed-content layouts (hero, marketing, print-destined) where line counts are predictable. For user-generated prose it degrades to "pick a sensible default N and let the grid fill in."

**Subgrid** improves it: a child grid can inherit its parent's rows. A multi-column editorial layout where each column wants the same baseline grid uses `grid-template-rows: subgrid` to inherit rows from a container whose rows are set to `var(--rhythm)`. Subgrid is Baseline 2023 (Firefox 71 Dec 2019, Safari 16 Sep 2022, Chrome 117 Sep 2023).

### Capsize-like negative-margin compensation

Pre-`text-box-trim`, the accepted way to remove half-leading was to compute it per-font and apply a negative `margin-top` / `margin-bottom` equal to the leading gap. The **Capsize** library ([seek-oss/capsize](https://github.com/seek-oss/capsize)) automates this.

Capsize's mechanism: read the font's `OS/2` table (UPM, sCapHeight, sxHeight, sTypoAscender, sTypoDescender, sTypoLineGap), compute the ratio `capHeight / em` and the gap between the cap-line and the top of the content area; generate CSS that applies a negative margin to pseudo-elements to absorb that gap.

Simplified sketch of the Capsize output (real output uses `::before` and `::after` with `display: table` as margin-collapse guards; see source):

```css
.capsized-text::before {
  content: '';
  display: table;
  margin-bottom: -0.1641em;  /* computed per font */
}

.capsized-text::after {
  content: '';
  display: table;
  margin-top: -0.1914em;
}

.capsized-text {
  /* font-size set to make cap-height equal to a desired pixel value */
}
```

The `display: table` on the pseudo-elements blocks CSS margin-collapse, which would otherwise cause the negative margins to escape and pull surrounding elements upward. Capsize's API takes a desired `capHeight` in px and emits `font-size`, `line-height`, and the compensating margins — producing text whose rendered height equals the requested cap-height exactly.

In 2026, `text-box-trim` does this natively. Capsize remains useful for:

- Firefox compatibility (Capsize is a pure CSS mechanism; works everywhere).
- Build-time / server-rendered cases where deterministic output is preferred.
- Pre-2025 design systems that have the Capsize CSS already baked in and don't want to migrate.

See `../contemporary/metric-overrides.md` for the related metric-override mechanism that stabilizes fallback fonts' line-box heights — complementary to Capsize and `text-box-trim`.

### Deprecated / removed

- **`leading-trim`** — the original name for `text-box-trim`; shipped in Safari 16.4–18.1 under the old name. Renamed in the CSS Inline 3 spec in 2023. Do not author against `leading-trim`; it is deprecated and will be removed.
- **`line-height-step`** — drafted in CSS Rhythm 1, shipped behind a flag in Chromium 2017, never standardized, effectively abandoned. Do not use.

---

## Alternative Philosophies

Vertical rhythm is a tradition, not a law. Multiple live alternatives coexist in 2026.

### Strict rhythm (the classical position)

The Bringhurst-Rutter position: every vertical measure on a page is a multiple of a single unit; text baselines fall on a ruled grid; deviation is a design failure. Works best for print, long-form editorial, and static marketing. Requires significant engineering to hold under responsive conditions, user font-size overrides, and replaced content.

### Relative rhythm (Tailwind / Tachyons / most product UI)

Maintain **proportional relationships** — `line-height` is a clean multiplier of `font-size`, `margin` is a clean multiplier of `line-height` — without trying for an absolute baseline grid. Tailwind's default spacing scale (`0.25rem` base unit, scale 0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16…) is proportional to its font-size scale but does not guarantee that body text baselines land on gridlines. Tachyons (the late-2010s utility-first predecessor) takes the same approach.

The pragmatic argument: readers don't notice a ruled grid; they notice inconsistent pacing. Proportional sizing guarantees consistent pacing without paying for the strict-grid engineering. This is the majority position in 2026 product design.

### Rhythm as guideline (Boulton's later writing)

Mark Boulton's *Incremental Leading* (2007) and later work explicitly reject the strict-grid position: treat rhythm as a **target that headings reset** rather than a constraint that must not deviate. Body text follows the rhythm; each heading "resets" the grid by landing on the next clean multiple, with its own margins consuming whatever overflow is needed. The grid is honored *between* headings but not *across* them.

This is the position most modern editorial CSS frameworks take (Sassline, Typesettings, etc. before they were superseded). It is also close to what readers actually perceive — strict alignment across headings is invisible; consistent within-section pacing is felt.

### No rhythm (brutalist / editorial-expressive)

A deliberate design stance: **break rhythm for expression**. Common in contemporary art-direction, small-batch editorial, and brand-forward marketing where the reader is expected to slow down and parse each page individually. Production Type's site, Dinamo's type specimens, Apple's marketing hero pages all routinely violate grids for visual tension. This is a valid choice but requires an editor/art-director-driven process — it does not survive a design system that must scale across dozens of templates authored by different people.

### Print-heritage (PDF, long-form)

For HTML rendered to PDF (paginated books, reports, legal documents), print conventions apply in full and the web's approximations do not. `text-box-trim` + strict line-height-on-grid is worth the engineering because the reader's expectation is print-grade. The CSS Paged Media Module plus Paged.js or Prince XML renders arbitrary HTML to PDF with print-faithful rhythm; in those pipelines the strict-grid position is the right default.

---

## Practical CSS Recipes

Four working recipes, ordered by progressive assumption about browser support and design discipline.

### Recipe A — pre-2025, no text-box-trim

The tolerate-the-wobble recipe. Works in every browser from 2015 onward.

```css
:root {
  --rhythm: 1.5rem;     /* 24px at default 16px root */
  --rhythm-sm: 0.75rem; /* half-unit for tighter spacing */
}

html {
  font-size: 100%;           /* respect user preference */
  line-height: var(--rhythm);
}

body {
  font-family: "Inter", "Inter Fallback", system-ui, sans-serif;
  font-size: 1rem;
  /* inherited line-height = 1.5rem */
}

/* Block elements stack on rhythm-unit margins. */
p, ul, ol, pre, blockquote, figure, hr {
  margin-block: 0 var(--rhythm);
}

/* Headings — size-to-multiple approach. */
h1 {
  font-size: 2rem;
  line-height: calc(var(--rhythm) * 2);  /* 48px line-box */
  margin-block: calc(var(--rhythm) * 2) var(--rhythm);
}

h2 {
  font-size: 1.5rem;
  line-height: calc(var(--rhythm) * 1.5);  /* 36px — on sub-grid */
  margin-block: calc(var(--rhythm) * 1.5) var(--rhythm);
}

h3 {
  font-size: 1.25rem;
  line-height: var(--rhythm);
  margin-block: var(--rhythm) var(--rhythm-sm);
}

/* Borders absorbed into padding. */
.bordered {
  border-block: 1px solid;
  padding-block: calc(var(--rhythm) - 1px);
}

/* Images snap to rhythm multiple via aspect-ratio wrapping. */
img {
  display: block;      /* removes descender-gap below */
  max-width: 100%;
  height: auto;
}
```

The metric-wobble from font-swap is invisible in this recipe because the eye tolerates 1–3px drift. Pair with metric overrides on fallbacks (see `../contemporary/metric-overrides.md`) to reduce the drift to sub-pixel levels on the FOUT boundary.

### Recipe B — 2025+, with text-box-trim

The tight recipe. Requires Safari 18.2+, Chrome/Edge 133+, with a Firefox fallback.

```css
:root {
  --rhythm: 1.5rem;
}

@supports (text-box: trim-both cap alphabetic) {
  h1, h2, h3, h4, h5, h6,
  .ui-label, .button-label, .nav-item {
    text-box: trim-both cap alphabetic;
  }

  /* With half-leading trimmed, margins can reduce — the block is now
     the size of the cap-height, not the line-box. */
  h1, h2, h3 {
    margin-block-start: var(--rhythm);
    margin-block-end: calc(var(--rhythm) / 2);
  }
}

@supports not (text-box: trim-both cap alphabetic) {
  /* Firefox path — use Recipe A margins with half-leading tolerance. */
  h1, h2, h3 {
    margin-block-start: calc(var(--rhythm) * 1.5);
    margin-block-end: calc(var(--rhythm) / 2);
  }
}

/* Body prose — trim-both is still useful at the block edges, removing
   the leading gap that otherwise eats into padding. */
@supports (text-box: trim-both cap alphabetic) {
  .prose {
    text-box: trim-both cap alphabetic;
  }
}
```

The `@supports` feature query is mandatory — without it, Firefox users see the tight layout without the trim and the rhythm breaks downward by the half-leading delta.

### Recipe C — grid-based rhythm

The layout-enforced recipe. Works everywhere subgrid is supported (Baseline 2023). Most reliable for fixed-content layouts.

```css
:root {
  --rhythm: 1.5rem;
}

.article {
  display: grid;
  grid-auto-rows: var(--rhythm);
  grid-template-columns: minmax(0, 65ch);
  justify-content: center;
  row-gap: 0;  /* rhythm lives in the row size */
}

.article > * {
  margin-block: 0;  /* no margins — grid rows are the rhythm */
}

/* Each block declares its row span. */
.article > p { grid-row: span 4; }
.article > h2 { grid-row: span 3; }
.article > h3 { grid-row: span 2; }
.article > figure { grid-row: span 8; }

/* Multi-column editorial — subgrid inherits rows. */
.article.multi-col {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: var(--rhythm);
}

.article.multi-col .column {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: 1 / -1;
}
```

The fragility: every block must have a correct `grid-row: span N` or the content either overflows its row allocation (no rhythm anyway) or leaves empty rows (visible gaps). Tools that auto-compute spans from line counts (Aleksandr Hovhannisyan's 2022 write-up, linked below) require measuring rendered text — a post-layout operation, not available to pure CSS.

### Recipe D — Capsize-like (build-time negative margins)

For Firefox-inclusive strict-rhythm UI without waiting for `text-box-trim` to ship universally.

```js
// Build-time — emit per-font CSS.
import { createFontStack, precomputeValues } from '@capsizecss/core';
import interMetrics from '@capsizecss/metrics/inter';

const values = precomputeValues({
  fontMetrics: interMetrics,
  capHeight: 16,      // target 16px cap-height
  lineGap: 8,         // target 8px line-gap
});

// values: { fontSize: '22.8px', lineHeight: '30px',
//           capHeightTrim: '-0.1641em', baselineTrim: '-0.1914em' }
```

Emit the returned values into per-component CSS; the negative-margin pseudo-elements absorb the leading gap at every block edge. Capsize's API also generates the full CSS string; see `seek-oss/capsize` README for current syntax.

This recipe has three properties `text-box-trim` does not yet match:

1. Works in Firefox today.
2. Deterministic at build time — no `@supports` feature queries needed.
3. Computes against the exact font you ship, not a fallback.

The downside: a bit more CSS (2 pseudo-elements per text block), and the values must be regenerated if the font changes.

---

## Vertical Rhythm in Mixed Scripts

Rhythm behaves differently per script because the underlying metrics differ.

### Latin, Cyrillic, Greek

The analysis above applies directly. Both `cap alphabetic` and `ex alphabetic` are meaningful `text-box-edge` values. x-height and cap-height are defined; ascender and descender lines are meaningful. A 24px rhythm unit with 16px body at 1.5 line-height works identically across these three scripts (metrics vary per font but the *shape* of the problem is the same).

### CJK (Han, Japanese, Korean)

CJK typography is built on the **ideographic em-box** — each character occupies a square approximately equal to the font size, and glyphs are designed to fit this box. Vertical rhythm in CJK horizontal text mode is therefore more naturally satisfied than in Latin: the em-box *is* the rhythm unit, and line-height at a clean multiple (typically 1.7–2.0 for CJK body) lands every line on a grid.

In CJK **vertical text** mode (`writing-mode: vertical-rl` or `vertical-lr`), "vertical rhythm" is replaced by **column count and character pitch**: how many full-width characters per column, and how tightly the characters pack. See `../scripts/japanese.md` and `../scripts/cjk-han.md` for tategaki-specific metrics. The Bringhurst-Rutter recipe does not transpose directly.

`text-box-edge: ideographic alphabetic` (or `ideographic-ink alphabetic`) is the CJK-appropriate trim edge; `cap` is Latin-specific and will fall back to heuristics on CJK fonts.

### Arabic, Hebrew

Right-to-left scripts run horizontally and stack lines top-to-bottom like Latin. Vertical rhythm concepts transpose: line-height governs baseline pitch, and the grid recipes apply. Two Arabic-specific considerations:

- **Marks above and below base characters** (shadda, fatha, kasra, damma, sukun; niqqud in Hebrew) extend outside the x-height envelope but are counted in the font's declared ascender/descender. A font with full marks ("Amiri" with `ligacal`) has larger effective ascent than a mark-minimal font; line-height must accommodate.
- **Nastaliq** (the Perso-Arabic slanting script) has extreme line-slope — characters within a ligature descend from upper-right to lower-left across a significant vertical range. Line-height must be substantially larger (typically 2.0–2.5× the font size) or lines collide. `text-box-trim` with `text` edges (not `cap`) is the safe choice.

### Devanagari, Thai, Lao, Burmese

Scripts with **stacked marks** (vowel signs, tone marks, subscript conjuncts) have per-line vertical budgets that vary with content. Devanagari's `shirorekha` (head line) is at a fixed position per font but **conjuncts below the baseline** can extend two or three rows below the descender line — a word with `क्र` (kra conjunct) sits taller than a word without. Thai's tone marks stack three deep: base + vowel + tone mark.

Rhythm fails in the strict sense for these scripts. A 24px rhythm unit set for Latin body will overlap marks when the content has heavy stacking. Recommended floor: **line-height at least 1.8× font-size** for Devanagari, **2.0× for Thai**, **2.2× for Burmese**, with checking on content samples. `text-box-edge: text alphabetic` is the only safe trim.

### Mixed-script UIs

A web app supporting English + Arabic + Hindi + Thai cannot strictly satisfy Latin rhythm and Thai rhythm in the same CSS. The usual compromise: set `line-height` per language via `:lang()` selectors, accept that different languages produce different baseline pitches, and lean on the point-grid (multiples of 8) at the block level rather than line-by-line rhythm.

```css
:root { --rhythm: 1.5rem; }
:lang(th), :lang(my), :lang(km) { --rhythm: 2rem; }
:lang(hi), :lang(mr), :lang(ne) { --rhythm: 1.75rem; }
```

---

## Interaction with Dynamic Type and User Overrides

Rhythm must scale with the user's font-size choice or it collapses for any user who resizes.

### `rem` vs `px` for the rhythm unit

- **`rem`-based rhythm** (`--rhythm: 1.5rem`) scales with the user's root `font-size`. A user who sets their browser to 200% text gets a 48px rhythm unit; every margin, padding, and line-height scales proportionally. This is the accessibility-correct default.
- **`px`-based rhythm** (`--rhythm: 24px`) does not scale. A 200% user gets 32px body text on a 24px rhythm — line-box (~48px) is nearly 2 rhythm units, margins are 0.5 or 1 unit, and the grid visibly breaks.

Always express rhythm in `rem`.

### iOS Dynamic Type

On iOS, the system text-size setting modifies the browser's root font-size via the `-apple-system-body` etc. text styles (native apps) and via the root size in Safari (web). A rem-based rhythm scales automatically. A pixel-based rhythm does not. WCAG 2.2 SC 1.4.4 (Resize text) effectively requires rem- or em-based sizing for text-adjacent measures, which rhythm margins and line-heights are.

### Android font-scale

Similarly, the system font-scale multiplier is applied to the browser's root font-size. Rem-based rhythm inherits.

### Zoom (Ctrl+ / Cmd+)

Browser zoom scales everything uniformly, including pixel values. Rhythm is preserved under zoom regardless of unit choice. Zoom is not the same as font-size increase — it zooms the layout; font-size increase shifts only text.

### The `em` vs `rem` gotcha for `line-height`

A body declaration of `line-height: 1.5rem` sets `line-height` to an absolute length that doesn't scale with the element's own font-size. A child `<code>` at `font-size: 0.9em` inherits `line-height: 1.5rem` — which means its line-box stays 24px even though the text is smaller. Usually fine; occasionally a cause of baseline drift.

The alternative, **unitless `line-height`** (`line-height: 1.5`), is computed per element against that element's own `font-size` and re-inherits as a number rather than a length. A `<code>` at 0.9em gets `line-height: 1.5 × 0.9em = 1.35em = 21.6px` — different from 24px, breaks rhythm.

**For rhythm, use `line-height` in `rem` or explicit length units on the block root; let children inherit the length.** Unitless is the correct default *in general* but breaks rhythm specifically.

---

## Common Failures

Named failure modes that recur across implementations.

### `line-height: 1` on headings

A reset that collapses every heading's line-box to the content area (no half-leading). Visible rhythm break: the heading's block size is different from what margins expect. Either keep `line-height` at a clean multiple of the rhythm unit, or apply `text-box-trim` everywhere (but `line-height: 1` removes the leading needed for multi-line heading wrapping).

### `line-height: 1` on buttons

Common in framework defaults. Buttons collapse to cap-height-ish content area, which throws off the 48px grid-step the design system expects. Fix: set explicit `line-height` in rem, or apply `text-box-trim` and compensate with padding.

### Image without `display: block`

An inline `<img>` participates in a line-box as an inline element and sits on the baseline — there is a descender-sized gap below it (usually 2–4px). Visible as a thin whitespace strip under every image in a prose column. Fix: `img { display: block; }` or `img { vertical-align: top; }`.

### Rich-text editor output

WYSIWYG editors (TinyMCE, Quill, TipTap, CKEditor) emit HTML with inline styles and arbitrary margin values that do not match any rhythm system. A CMS that lets editors paste from Word gets `<p style="margin-top: 18px; margin-bottom: 14px;">` — breaking rhythm on every paragraph. Defenses: sanitize editor output at save; strip inline margins on render; scope rhythm CSS with sufficient specificity to override inline styles.

### Tables without row-height discipline

A `<table>` layout ignores block-level margins and `line-height` at the cell level unless set explicitly. `tr`, `td`, `th` all carry their own heights. Fix: `td { line-height: var(--rhythm); padding-block: 0; }` plus explicit `height` on rows to snap.

### Fluid line-height with `clamp()`

`line-height: clamp(1.4, 1.2 + 0.5vw, 1.7)` produces a line-height that changes with viewport. Rhythm derived from line-height therefore changes with viewport. Either fix `line-height` to a constant multiplier and fluidize `font-size` only, or accept that the rhythm unit is viewport-variable and size everything in em relative to line-height.

### Borders on one side only

`border-block-start: 1px solid` without a compensating `padding-block-start` reduction pushes everything down by 1px. Fix: always compensate `padding` when adding a `border`.

### Letter-spaced ALL CAPS headings

Letter-spacing does not affect vertical rhythm directly, but ALL CAPS heading styles often also tweak `line-height`. A `line-height: 0.9` "tight caps" style removes ~10% of the line-box, breaking rhythm. Use `text-box-trim` or explicit grid-row-span instead.

### Subscripted / superscripted inline content

`<sub>` and `<sup>` at default browser styling apply `vertical-align: sub | super` and reduce `font-size` — which *can* push the line-box taller because the subscript/superscript glyph extends below the baseline or above the cap-line. Fix: `sub, sup { line-height: 0; position: relative; }` with explicit offsets.

### Form control heights

`<input>`, `<button>`, `<select>`, `<textarea>` have per-browser internal padding and border. An `<input>` nominally at `height: 2rem` may render at 34px in Safari, 33px in Chrome, 36px in Firefox. For rhythm, set all six: `box-sizing: border-box`, explicit `height`, `padding-block: 0`, `border`, `line-height`, and `font-size`. Do not rely on browser defaults.

---

## Does Rhythm Matter for Reading?

Honest assessment.

### No controlled evidence for comprehension gain

No peer-reviewed reading-science study has shown improved comprehension or reduced fatigue from strict baseline-grid adherence specifically. The closest is **Dyson (2004)** and the broader screen-reading literature (see `./measure.md` and `../science/legibility-vs-readability.md` for citations), which shows comprehension effects from line-length, line-height, and font-size — not from baseline alignment per se. A 1.5× line-height body at 65-character measure with predictable paragraph spacing outperforms a tight-line-height body regardless of whether the baselines hit a ruled grid.

The aesthetic/editorial argument for rhythm is real and cultural — books have been set on gauges for five centuries, and readers' expectation for "good typography" is shaped by that tradition. Rhythm satisfies an expectation; it does not improve comprehension measurably.

### What actually helps reading

From the reading-science literature:

- **Consistent line-height** (≥1.5 for body prose; see Rayner 1998).
- **Consistent paragraph spacing** (one-line-or-more visible break between paragraphs).
- **Predictable heading hierarchy** (size and weight telegraph the structural role).
- **Adequate measure** (45–75 CPL, see `./measure.md`).
- **High contrast and good font choice** (see `../science/legibility-vs-readability.md`).

Strict rhythm enforces some of these as byproducts. A 24px rhythm with 16px body automatically gives `line-height: 1.5`; multi-unit margins automatically give consistent paragraph spacing; grid-aligned headings automatically give predictable hierarchy. The rhythm is the mechanism; the reading benefits are from the side-effects.

**Implication:** the cost-benefit of strict rhythm is: pay the engineering cost (per-font metric tuning, `text-box-trim` adoption, image-height constraints, border compensation) to gain the cultural "feels right" effect plus the byproducts of consistent pacing — which you could have gotten cheaper with proportional spacing that doesn't enforce a strict grid.

### When to go strict

Editorial long-form, printed PDFs, brand-forward marketing, and any context where the reader's expectation is print-grade. The engineering cost is worth it because the cultural expectation is high.

### When to go relative

Product UI, dashboards, admin panels, and most content-light surfaces. The engineering cost exceeds the benefit; proportional spacing (Tailwind-style) is sufficient.

### When to break rhythm

Expressive / brand-forward one-off compositions where the visual tension *is* the point. Editorial art-direction. Rule-breaking is a legitimate stance when the system supports it (i.e. there is a designer in the loop, not a template filled by many authors).

---

## Summary Guidance

- **For product UI** (most apps, dashboards, forms): use a **proportional / relative rhythm** (Tailwind-style). 4- or 8-point grid for block spacing, `line-height` in clean multipliers (1.4 for UI labels, 1.5 for body, 1.2 for headings). Strict baseline grid is not worth the engineering cost.
- **For editorial long-form** (blogs, magazines, documentation): use **Recipe A** with metric overrides on fallbacks. If you can drop Firefox or provide feature-queried fallback, upgrade to **Recipe B** (`text-box-trim`). Pair with measure cap (65ch; see `./measure.md`) and a modular scale for type sizes (see `./modular-scale.md`).
- **For printed PDFs / paginated HTML**: go strict. **Recipe B** plus **Recipe C** plus metric overrides. Use CSS Paged Media (`@page`) and pagination-aware tooling (Paged.js, Prince XML). The print reader's expectation is print-grade; pay the cost.
- **For mixed-script apps**: do not try for strict rhythm across scripts. Set per-language `--rhythm` via `:lang()`, enforce block-level point-grid at 8px, and accept that Thai, Burmese, and Devanagari will have larger line-heights than Latin.
- **Never**: set `line-height: 1` on headings without compensating with `text-box-trim` or explicit margins; use `px` for the rhythm unit (breaks dynamic type); apply `grid-auto-rows` without checking row span per element (creates empty gaps); trust inherited rhythm across a rich-text editor boundary.

---

## Cross-references

- **`./measure.md`** — measure interacts with rhythm: line length governs how often wrapping breaks rhythm. Narrow measure + strict rhythm is the most forgiving combination because few headings wrap.
- **`./modular-scale.md`** — every step in the modular scale should be or relate to a multiple of the rhythm unit. `1.25` ratio with 16px anchor gives 16, 20, 25, 31.25, 39 — not clean multiples of 24. Pick the ratio and rhythm together, or accept that sub-grid math (line-height of 30px, 45px, 60px for the 20px / 30px / 40px rungs) is required.
- **`../contemporary/css-text-properties.md`** — `text-box-trim`, `text-box-edge`, `text-box` shorthand, `line-height-step` (deprecated), `baseline-source` — deeper coverage of the property surface.
- **`../contemporary/metric-overrides.md`** — the `@font-face` descriptors that let fallback fonts' line-boxes match the primary's. Required reading if strict rhythm must survive FOUT. Shares the rhythm vocabulary (UPM, ascent, descent, line-gap) without duplicating.
- **`../metrics/metrics-glossary.md`** — authoritative reference for the physical metrics (`sTypoAscender`, `sxHeight`, `sCapHeight`, UPM, baseline, ascender line, descender line) that rhythm math depends on.
- **`../metrics/units.md`** — `rem`, `em`, `lh`, `rlh`, `cap`, `ex`, `ic`. The `lh` unit (1 = one line-height on the element) is specifically useful for rhythm math but is Baseline 2024 and may not be safe on legacy browsers.
- **`token-builder` agent** — owns the project token layer. Derive the rhythm unit and line-height values inline from this file's recipes (no generator skill is installed); route only their realization as role-named tokens — spacing and leading ladders — to that seat.

---

## Sources

(Retrieval dates: 2026-04-18 except where noted.)

### Historical / editorial

- **Bringhurst, R. (2012).** *The Elements of Typographic Style.* 4th ed., Hartley & Marks. Chapter 2 ("Rhythm & Proportion") and Chapter 5 ("Structural Forms and Devices"). Canonical editorial argument.
- **Tschichold, J. (1991).** *The Form of the Book: Essays on the Morality of Good Design.* Hartley & Marks. Classical proportion and page-setting tradition from which baseline grids derive.

### Web-design canon (pre-2015)

- **Rutter, R. (2006).** ["Compose to a Vertical Rhythm."](https://24ways.org/2006/compose-to-a-vertical-rhythm/) *24ways,* December 2006. The canonical article.
- **Boulton, M. (2005–2007).** ["Five simple steps to designing grid systems — Part 4."](https://markboulton.co.uk/journal/five-simple-steps-to-designing-grid-systems-part-4/) Baseline grids for web.
- **Boulton, M. (2007).** ["Incremental leading."](https://markboulton.co.uk/journal/incremental-leading/) Argues for leading that grows with type size.
- **Santa Maria, J. (c. 2007–2011).** ["Baseline Grids on the Web."](https://v5.jasonsantamaria.com/articles/baseline-grids-on-the-web/) Skeptical position: rhythm is a target, not a constraint.
- **Santa Maria, J. (2014).** *On Web Typography.* A Book Apart. Responsive typography and baseline-grid practicality.
- **Reichenstein, O. (2006).** ["Web Design is 95% Typography."](https://ia.net/topics/the-web-is-all-about-typography-period) *Information Architects.* Cultural motivation.
- **Rutter, R. (2017).** *Web Typography: A Handbook for Designing Beautiful and Effective Responsive Typography.* Self-published / [webtypography.net](https://book.webtypography.net/). Companion to his ongoing "Elements of Typographic Style Applied to the Web" — updates 2006 recipe for responsive contexts.
- **Walker, A. (2012–2015).** ["Web Layout 101: Vertical Rhythm is a Drummer."](https://medium.com/sitepoint/web-layout-101-vertical-rhythm-is-a-drummer-19c4e61bfe68) SitePoint/Medium. Widely-cited intro piece.

### Modern CSS (2020+)

- **Wang, E. (2020).** ["Leading-Trim: The Future of Digital Typesetting."](https://medium.com/microsoft-design/leading-trim-the-future-of-digital-typesetting-d082d84b202) *Microsoft Design.* Original motivation for what became `text-box-trim`.
- **W3C CSS Inline Layout Module 3.** [`text-box`](https://drafts.csswg.org/css-inline-3/) and sub-properties. Editor's Draft (2026-04).
- **W3C CSS Rhythmic Sizing (CSS Rhythm 1).** [`line-height-step`](https://drafts.csswg.org/css-rhythm-1/) — moribund Latin use case; CJK-only case stalled. Not shipping.
- **MDN — [`text-box-trim`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-trim).** Current syntax and values.
- **MDN — [`text-box-edge`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-edge).** Over- and under-edge value grammar.
- **MDN — [`text-box`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box).** Shorthand reference.
- **MDN — [`baseline-source`](https://developer.mozilla.org/en-US/docs/Web/CSS/baseline-source).** Inline-alignment selector; not a grid primitive.
- **MDN — [`line-height-step`](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height-step).** Documented but not shipping.
- **Can I Use — [`text-box-trim`](https://caniuse.com/mdn-css_properties_text-box-trim).** Cross-browser status.
- **Can I Use — [CSS text-box property](https://caniuse.com/css-text-box-trim).** Shorthand support.
- **Chrome for Developers — [CSS text-box-trim](https://developer.chrome.com/blog/css-text-box-trim).** Chrome shipping post, 2025-02.
- **Nerdy.dev — [Text Box Trim](https://nerdy.dev/text-box-trim).** 2025-01-14 — Adam Argyle overview.
- **Piccalilli — [Why I'm excited about text-box-trim as a designer.](https://piccalil.li/blog/why-im-excited-about-text-box-trim-as-a-designer/)** Andy Bell, 2024–2025.
- **CSS-Tricks — [Two CSS Properties for Trimming Text Box Whitespace.](https://css-tricks.com/two-css-properties-for-trimming-text-box-whitespace/)** 2024.
- **Mozilla Standards Position — [Issue 1105: CSS text-box, text-box-trim, text-box-edge.](https://github.com/mozilla/standards-positions/issues/1105)** Firefox's implementation tracking as of 2026-04.

### Tools and frameworks (historical and current)

- **Capsize — [seek-oss/capsize](https://github.com/seek-oss/capsize).** 2020–2026. Cap-height-based type sizing with pseudo-element negative-margin trim. Still relevant for Firefox-inclusive sites.
- **[@capsizecss/metrics](https://www.npmjs.com/package/@capsizecss/metrics).** Pre-extracted font metrics.
- **[Capsize docs](https://seek-oss.github.io/capsize/).** API reference.
- **Compass Vertical Rhythm** (2008–2015, deprecated). Historical Sass reference: [establish-baseline, rhythm, leader, trailer mixins](https://atendesigngroup.com/articles/vertical-rhythm-compass). Superseded by native CSS.
- **Sassline** (Jake Giltsoff, 2014–2018). Canonical Sass framework for baseline rhythm. [sassline.com](https://sassline.com/). Historical reference.
- **Typesettings** (Ian Rose). Similar Sass-based rhythm framework; historical.
- **Basehold.it** (Dave Hamilton). [basehold.it](https://basehold.it/) — overlay tool for debugging baseline grids. Drops a CSS baseline-grid stylesheet onto any page.
- **Hovhannisyan, A. (2022).** ["Creating a Vertical Rhythm with CSS Grid."](https://www.aleksandrhovhannisyan.com/blog/vertical-rhythm-with-css-grid/) Grid-auto-rows recipe modernized.

### Grid-system context

- **Apple — Human Interface Guidelines (iOS 7, 2013–present).** 8-point grid convention introduced.
- **Google — Material Design 3 (2021–present).** 4 dp baseline grid, 8 dp spacing. [Material spatial system docs](https://m3.material.io/).
- **Spec.fm — [8pt Grid](https://spec.fm/specifics/8-pt-grid).** Community primer on 8pt adoption.
- **Cieden / various — 4pt vs 8pt practitioner comparisons (2022–2025).**

### Research context (for the "does rhythm matter" section)

- **Rayner, K. (1998).** "Eye movements in reading and information processing: 20 years of research-survey." *Psych. Bulletin* 124(3). Line-height matters; baseline-grid alignment specifically is not tested.
- **Dyson, M. C. (2004).** "How physical text layout affects reading from screen." *Behaviour & Information Technology* 23(6). Line-length and line-height effects on screen reading.
- **Larson, K.** ["The Science of Word Recognition."](https://www.microsoft.com/typography/ctfonts/WordRecognition.aspx) Microsoft Advanced Reading Technologies. Parallel-letter recognition, not word-shape; tangentially relevant to the "rhythm is cultural not perceptual" argument.
