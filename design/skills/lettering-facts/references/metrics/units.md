---
date: 2026-04-18
coverage: deep
peers:
  - ./anatomy.md
  - ./metrics-glossary.md
  - ../techniques/measure.md
  - ../contemporary/css-text-properties.md
  - ../contemporary/metric-overrides.md
  - ../accessibility/wcag-type.md
primary_sources:
  - https://www.w3.org/TR/css-values-4/
  - https://www.w3.org/TR/css-values-4/#font-relative-lengths
  - https://www.w3.org/TR/css-values-4/#viewport-relative-lengths
  - https://www.w3.org/TR/css-values-4/#absolute-lengths
  - https://www.w3.org/TR/css-values-4/#ch
  - https://drafts.csswg.org/css-values-5/
  - https://www.w3.org/TR/css-contain-3/#container-lengths
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust
  - https://developer.mozilla.org/en-US/docs/Web/CSS/calc
  - https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
  - https://developer.mozilla.org/en-US/docs/Web/CSS/round
  - https://caniuse.com/mdn-css_types_length-percentage_cap
  - https://caniuse.com/mdn-css_types_length_lh
  - https://caniuse.com/mdn-css_types_length_rlh
  - https://caniuse.com/mdn-css_types_length_ic
  - https://caniuse.com/viewport-unit-variants
  - https://caniuse.com/css-container-query-units
  - https://caniuse.com/wf-round-mod-rem
  - https://caniuse.com/font-size-adjust
  - https://web.dev/blog/viewport-units
  - https://webkit.org/blog/16831/line-height-units/
  - https://meyerweb.com/eric/thoughts/2018/06/28/what-is-the-css-ch-unit/
  - https://ishadeed.com/article/css-cap-unit/
  - https://nerdy.dev/new-relative-units-ric-rex-rlh-and-rch
  - https://www.w3.org/TR/WCAG22/#resize-text
  - https://www.w3.org/TR/WCAG22/#reflow
notes:
  - Support dates reflect stable shipped versions as of 2026-04-18. Version/Baseline annotations are inline on each claim.
  - Tier=deep: CSS recipes are copy-pasteable; every behavioral claim traces to the spec or a listed caniuse entry.
---

# CSS Units for Typography — Reference

Typography on the web is a unit-selection problem as much as a font-selection problem. `font-size: 16px` vs `font-size: 1rem` is invisible until a user overrides their default font size for accessibility and the first is frozen at 16 pixels while the second scales. `max-width: 65ch` vs `max-width: 32em` is invisible until the font swaps and the digit width shifts.

This file covers how CSS consumes font and viewport metrics — units, syntax, browser support, practical use. For the font-internal metrics themselves (UPM, x-height, cap-height, advance width of `0`, ideographic advance), see `./metrics-glossary.md`.

---

## Taxonomy

CSS lengths fall into five families. Each ultimately reduces to a number of **reference pixels** (`px`) at layout time.

| Family | Members | Anchored to | Live? |
|--------|---------|-------------|-------|
| Absolute | `px`, `cm`, `mm`, `Q`, `in`, `pc`, `pt` | CSS reference pixel; in print, physical | No |
| Font-relative (local) | `em`, `ex`, `ch`, `cap`, `ic`, `lh` | Computed font of current element | Recomputes on font change |
| Font-relative (root) | `rem`, `rex`, `rch`, `rcap`, `ric`, `rlh` | Computed font of root element | Recomputes on root change |
| Viewport-relative | `vw/vh/vmin/vmax/vi/vb`, `svw/svh/...`, `lvw/lvh/...`, `dvw/dvh/...` | Viewport | `dv*` live; `sv*`/`lv*` static |
| Container-relative | `cqw`, `cqh`, `cqi`, `cqb`, `cqmin`, `cqmax` | Nearest container-query container | Recomputes on container resize |

`%` is not a length but resolves against a property-specific basis (usually parent's value). `calc()`, `clamp()`, `min()`, `max()`, `round()`, `mod()`, `rem()` are math functions that return lengths.

---

## Absolute Units

Seven members. Six are physical in print; all seven are locked by fixed ratios.

| Unit | Meaning | = `px` | Typical use |
|------|---------|--------|-------------|
| `px` | CSS reference pixel | 1 | Screen default |
| `in` | Inch | 96 | Print, signage |
| `cm` | Centimeter | 37.795 | Print (metric) |
| `mm` | Millimeter | 3.7795 | Print (metric, fine) |
| `Q` | Quarter-millimeter | 0.9449 | Japanese print |
| `pt` | Point | 1.3333 | Print typography |
| `pc` | Pica = 12pt | 16 | Print columns |

Full conversion: `1in = 2.54cm = 25.4mm = 101.6Q = 96px = 72pt = 6pc`.

### On screen, physical units are aliases

The browser does not know how big your monitor is. It assumes 96 device pixels per inch for the reference pixel, then derives everything else. `font-size: 12pt` on screen renders as `12 × 96/72 = 16px` regardless of actual display size. This is by design: the CSS reference pixel is an angular-size abstraction, not a physical measurement.

In `@media print`, physical units become physical — `margin: 2.54cm` really reserves one inch on paper. For PDF export and signage, `pt`/`pc`/`mm`/`cm`/`in` are correct.

**Avoid in web UI.** `font-size: 12pt` on screen is `16px` with extra cognitive load.

### `pt` in CSS ≠ `pt` in InDesign

A typographer saying "set this at 11 point" in InDesign produces a physical 11/72-inch glyph when printed. The same `font-size: 11pt` in CSS renders to screen as a 14.67px-tall line box — no physical measurement is involved. The two workflows converge only when both output to print at the same DPI, and only if the browser's print path honors the conversion faithfully.

### `Q`

Quarter-millimeter, traditional Japanese print sub-unit. 1Q = 0.25mm. Fine print measurement in metric regions; almost never in web work.

---

## The Reference Pixel

`px` is the foundation. CSS defines 1 reference pixel as the visual angle of 1 pixel on a device with 96 dpi at arm's length (CSS Values 4 § 5.1). An angular-size abstraction, not a count of device pixels.

### On modern hi-DPI displays

1 CSS `px` = N device pixels, where N is the device pixel ratio (DPR).

| Device class | Typical DPR |
|--------------|-------------|
| Non-retina desktop | 1 |
| Retina desktop / MacBook | 2 |
| Modern iPhone | 3 |
| Android high-DPI | 2.5–3.5 (often fractional) |
| Desktop at 125%/150% OS scaling | 1.25, 1.5 |

Read DPR in JS: `window.devicePixelRatio`. In CSS: `@media (resolution: 2dppx)` or `@media (min-resolution: 2dppx)`. `dppx` = dots per CSS pixel; prefer over `dpi`.

### Everything anchors to `px`

```
1in = 96px = 72pt = 6pc = 2.54cm = 25.4mm = 101.6Q
1pt = 1.333 px
1pc = 16px
```

Physical units on screen are just pretty aliases for `px` with an implicit DPI assumption.

### Hairline implication

`1px` borders render at different sub-pixel thicknesses across DPRs. DPR=1: one device pixel, crisp. DPR=2: two device pixels, thicker. Fractional DPRs (1.5, 2.625): antialiased gray. For truly thin hairlines at hi-DPI, a `rem` fraction (`0.0625rem` = 1px at default root) gives more consistent rendering than `0.5px` DPR-branches, and it scales with user font-size.

---

## Font-Relative Units — Local

Resolve against the **computed font of the current element**.

### `em`

- **Resolves to:** computed `font-size` of the current element for most properties; of the **parent** for the `font-size` property itself.
- **Confusion:** `padding: 1em` on an element with `font-size: 20px` is 20px. But `font-size: 1.2em` on the same element, inside a parent with `font-size: 16px`, computes to `16 × 1.2 = 19.2px` — relative to the **parent**.
- **Compounding:** nested `font-size: 1.2em` three levels deep compounds to `1.2³ = 1.728 × root`. Usually a bug. Prefer `rem` for `font-size`.

### `rem`

- **Resolves to:** computed `font-size` of the root (`:root`, `html`).
- Does not compound. `margin: 1rem` is the same pixel value anywhere.
- **Accessibility:** when the user overrides the browser's default 16px, every `rem`-based length scales with it. This is how `rem`-based layouts respect user font-size preferences.

### `ex`

- **Resolves to:** x-height of the element's font (see `./metrics-glossary.md#x-height`).
- Typical ~0.5em, but the range is wide: Frutiger ≈ 0.53em, Garamond ≈ 0.40em, Inter ≈ 0.515em. Do not assume `1ex ≈ 0.5em`.
- **Fallback:** when `OS/2.sxHeight` is absent, CSS mandates `0.5em`.
- **Use:** baseline-aligned inline icons. Often replaced by `cap` or explicit offsets.

### `ch`

- **Resolves to:** advance width of the `0` (U+0030) glyph in the element's font.
- **Common misconception:** not "average character width." See the dedicated section below.
- Typical 0.5–0.6em in most Latin text faces.
- **Exact for monospace.** `65ch` = exactly 65 characters in monospace.
- **Fallback:** `0.5em` horizontal, `1em` vertical when the glyph is absent.

### `cap`

- **Resolves to:** cap-height (`OS/2.sCapHeight / UPM × font-size`).
- **Browser support (2026-04-18):** Firefox 97+ (Feb 2022), Safari 16.3+ (Jan 2023), Chromium 133+ (Feb 2025). Baseline ~mid-2025.
- **Fallback:** browsers measure height of `H` when `sCapHeight` is missing.
- **Use:** aligning inline icons, drop-cap baselines, hairline underlines to cap-height rather than em-box.

### `ic`

- **Resolves to:** advance of the CJK water ideograph `水` (U+6C34).
- **Browser support:** Firefox 94+ (Nov 2021), Chromium 107+ (Oct 2022), Safari 16.4+ (Mar 2023). Interop 2022.
- **Fallback:** `1em` when `水` is absent.
- **Use:** CJK measure. One `ic` = one ideographic square. `max-block-size: 40ic` caps a vertical column at 40 full-width characters. `ic` is to CJK what `ch` is to monospace Latin.

### `lh`

- **Resolves to:** computed `line-height` of the element.
- **Browser support:** Chromium 109+ (Jan 2023), Safari 16.4+ (Mar 2023), Firefox 120+ (Nov 2023). Shipped all three in 2023.
- **Use:** vertical rhythm without arithmetic. `margin-top: 2lh` = two line-heights. Replaces `calc(var(--font-size) * var(--line-height) * 2)`.

### `rlh`

- **Resolves to:** computed `line-height` of the root.
- **Browser support:** same as `lh`.
- **Use:** document-wide baseline grid; consistent rhythm reference independent of the element's local line-height.

### `rex`, `rch`, `rcap`, `ric`

CSS Values 5 root-element analogs of the metric units.

| Unit | Resolves to | Browser support (2026-04-18) |
|------|-------------|------------------------------|
| `rex` | x-height of root | Chromium 117+, Safari 16.4+, Firefox 127+ |
| `rch` | `0` advance of root | same |
| `rcap` | cap-height of root | same |
| `ric` | ideographic advance of root | same |

Use when a font-relative measure shouldn't shift when local `font-size` changes. `gap: 1rch` keeps grid gaps consistent across nested blocks with different body fonts.

---

## The `ch` Trap

The most frequently mis-used unit in CSS typography. Deserves its own section.

### The claim

> `max-width: 65ch` yields 65 characters per line.

### What actually happens

In most Latin proportional text faces, `65ch` yields **approximately 70–80 characters per line**. Consistently more than 65.

### Why

`ch` is the advance of digit `0`. In Latin text fonts, `0` sits in a tabular-figure-compatible box and is typically 10–20% wider than the average lowercase advance. Compound across 65 units and the line fits ~70–80 lowercase characters.

Meyer (2018), Ishadeed (2023), and the web.dev *Sizing Units* module all make this point. See `../techniques/measure.md` for the CPL-range implication.

### Evidence (reproducible)

Render `max-width: 65ch` with a common sans (Inter, Source Sans, Helvetica) at 16px body. Count lowercase characters in a paragraph of real prose. The count consistently lands in the 72–82 range.

### Workarounds

1. **`max-width: 32em` or `36em`.** Font-agnostic: 65 × 0.5em ≈ 32em. Less tied to the running font; immune to `0`-width quirks.
2. **`max-width: calc(65 * 1ch * 0.9)`.** Empirical correction factor. 0.9 is a decent Latin-text default; drifts for heavier weights.
3. **Use `ic` for CJK**, where the character box IS the grid unit. `max-block-size: 40ic` = exactly 40 full-width characters.
4. **Accept the approximation.** `65ch` is "about 65–80 characters." Design tolerances around it. This is the Tailwind Typography / GOV.UK Frontend position.

### `ch` is not wrong for monospace

Every glyph in monospace shares the advance of `0`. `65ch` = 65 characters, exactly. The original 1990s use case.

### Standardization discussion

There has been intermittent CSSWG debate about redefining `ch` to mean "average character width" — perhaps the `x` advance or an a-z average. Backward compatibility has prevented change. Instead, `rch` was defined the same way and the problem is treated as author-education. No redefinition on a 2026 ship track. Track github.com/w3c/csswg-drafts.

---

## Viewport Units

### Classic `vw`, `vh`, `vmin`, `vmax`, `vi`, `vb`

| Unit | 1% of |
|------|-------|
| `vw` | Viewport width |
| `vh` | Viewport height |
| `vmin` | Smaller of `vw`, `vh` |
| `vmax` | Larger of `vw`, `vh` |
| `vi` | Viewport inline-size (writing-mode aware) |
| `vb` | Viewport block-size |

Baseline Widely Available since ~2015. The one persistent problem: mobile browser chrome. `100vh` on iOS Safari historically meant the viewport with URL bar hidden, so `height: 100vh` at the top of a page (with URL bar showing) produced a scrollbar. The 2022 variants fixed this.

### The 2022 variants: `sv*`, `lv*`, `dv*`

CSS Values 4 added three variants of every viewport unit.

| Prefix | Meaning | Live? |
|--------|---------|-------|
| `sv` | Small viewport — with browser chrome visible | No, static at load |
| `lv` | Large viewport — with chrome hidden | No, static |
| `dv` | Dynamic viewport — current state, updates with chrome | Yes |

Full family: `svw/svh/svmin/svmax/svi/svb`, `lvw/lvh/lvmin/lvmax/lvi/lvb`, `dvw/dvh/dvmin/dvmax/dvi/dvb`.

**Browser support (2026-04-18):** Chromium 108+ (Nov 2022), Firefox 101+ (May 2022), Safari 15.4+ (Mar 2022). Baseline Widely Available June 2025.

### Performance note

`sv*`/`lv*` are computed once at layout; `dv*` recomputes on every chrome state change. Use `dvh` only when content actually needs to follow mobile chrome in real time:

```css
.hero {
  min-height: 100vh;   /* legacy fallback */
  min-height: 100svh;  /* static at small state */
  min-height: 100dvh;  /* progressive enhancement */
}
```

### Typography use: fluid type

The `vw`-blended fluid-type recipe is the primary typographic use case.

```css
/* 16px at 320px viewport → 20px at 1280px */
:root {
  --fs-body: clamp(1rem, 0.8571rem + 0.7143vw, 1.25rem);
}
```

Arithmetic: two anchor points `(320, 16)` and `(1280, 20)` define a line; `clamp(lo, line, hi)` renders the line between two caps.

### Trap: pure `vw` ignores user font-size override

`font-size: 2vw` does **not** scale with the user's browser font-size preference — `vw` is a fraction of viewport, not user-preferred body size. A pure-vw scale ignores accessibility overrides.

```css
/* BAD — ignores user preference */
p { font-size: 1.5vw; }

/* GOOD — respects preference, scales with viewport */
p { font-size: clamp(1rem, 0.85rem + 0.6vw, 1.25rem); }
```

Always blend with `rem`.

---

## Container Query Units

Where viewport units ask "how big is the page?", container units ask "how big is my parent?".

| Unit | 1% of |
|------|-------|
| `cqw` | Container width |
| `cqh` | Container height |
| `cqi` | Container inline-size |
| `cqb` | Container block-size |
| `cqmin` | Smaller of `cqi`, `cqb` |
| `cqmax` | Larger of `cqi`, `cqb` |

**Requires:** `container-type: inline-size` (or `size`) on the ancestor.

**Browser support (2026-04-18):** Chromium 105+ (Aug 2022), Safari 16+ (Sep 2022), Firefox 110+ (Feb 2023). Baseline 2023.

### Typography use: component-relative fluid type

When a component (card, sidebar, modal) scales type to its own width:

```css
.card {
  container-type: inline-size;
  container-name: card;
}

.card-title {
  /* 1rem → 1.75rem based on card width, not viewport */
  font-size: clamp(1rem, 0.6rem + 2.5cqi, 1.75rem);
}

.card-body {
  max-inline-size: min(65ch, 100cqi);
  line-height: 1.55;
}
```

Most useful when the same component appears in article body, sidebar, and full-bleed hero; viewport units can't distinguish.

### Trap: forgetting `container-type`

`cq*` without a containing ancestor silently resolves to 0. The failure mode is usually a collapsed component that "just works" when you hover devtools onto its parent.

---

## `%` (Percentage)

Not a unit. Resolves against a property-specific basis.

| Property | `%` resolves against |
|----------|----------------------|
| `width`, `margin-*`, `padding-*` | Parent's width |
| `height`, `min-height`, `max-height` | Parent's height (requires parent resolved) |
| `font-size` | Parent's `font-size` |
| `line-height` | Element's own `font-size` — computed and **frozen** |
| `vertical-align` | Element's `line-height` |
| `top/right/bottom/left` | Containing block's width/height |

### The `line-height: %` trap

`line-height: 150%` computes to `1.5 × font-size` and **freezes the pixel value**. Descendants with a different `font-size` inherit the frozen px, not the ratio.

```css
/* BAD — computed at article level, frozen; h2 inside inherits the px */
article { font-size: 16px; line-height: 150%; }  /* = 24px, frozen */
article h2 { font-size: 32px; }                  /* line-height STILL 24px */

/* GOOD — unitless ratio, inherits as ratio */
article { font-size: 16px; line-height: 1.5; }   /* ratio */
article h2 { font-size: 32px; }                  /* line-height = 48px */
```

**Always prefer unitless for `line-height`.** This is the same trap as `line-height: 1.5em` — it too freezes.

---

## Unitless Values

Most length-accepting properties require a unit. The single exception where unitless is not just valid but preferred is `line-height`.

- `line-height: 1.5` — unitless ratio, inherits as ratio.
- `line-height: 1.5em` / `1.5rem` / `150%` / `24px` — frozen to px at the inheritance boundary.

Only unitless carries the ratio through. All other forms freeze.

Other unitless properties: `opacity`, `z-index`, `order`, `flex-grow`, `flex-shrink`. Custom properties (`--x: 12`) are unitless until consumed with `calc()` against a unit.

---

## Math Functions on Units

### `calc()`

Arithmetic with unit conversion handled by the browser.

```css
width: calc(100% - 2rem);
padding: calc(1rem + 0.5vw);
margin-block: calc(1lh + 4px);
line-height: calc(24 / 16);  /* still unitless */
```

**Support:** universal. Baseline since ~2014.

### `clamp(min, preferred, max)`

The fluid-type backbone. Returns `preferred`, bounded by `min` and `max`.

```css
font-size: clamp(1rem, 0.875rem + 0.75vw, 1.5rem);
```

**Support:** Baseline 2020.

### `min()`, `max()`

Layered floors and ceilings.

```css
max-inline-size: min(65ch, 100%);
margin-block-start: max(1.5lh, 2vw);
```

**Support:** Baseline 2020.

### `round()`, `mod()`, `rem()` — stepped values

CSS Values 4 stepping functions. Baseline 2024 (interop May 2024; Chromium 125+, Safari 15.4+, Firefox 118+).

- `round(<strategy>, value, step)` — rounds value to nearest `step`. Strategies: `nearest` (default), `up`, `down`, `to-zero`. `round(17px, 8px)` → `16px`.
- `mod(a, b)` — modulus, takes sign of **divisor**.
- `rem(a, b)` — remainder, takes sign of **dividend**. (The function, not the unit.)

Typographic use: snapping fluid values to a grid.

```css
/* Snap font-size to 2px increments */
font-size: round(clamp(1rem, 0.875rem + 0.75vw, 1.5rem), 2px);

/* Snap block size to whole line-heights */
min-block-size: round(up, var(--content-height), 1lh);
```

Trig (`sin`, `cos`, `tan`, etc.) also Baseline 2024; rarely used in typography.

---

## Font-Specific Unit Quirks

### `em` for margin/padding on text elements

Scales spacing with the element's own size — often deliberate. `h1 { margin-block: 0.75em }` and `h2 { margin-block: 0.75em }` produce proportional spacing without per-element arithmetic.

### `em` for `font-size` — the compounding bug

`font-size: 1.2em` three levels deep = `1.728 × root`. Usually a bug. **Prefer `rem` for `font-size`** unless you explicitly want compounding.

### `rem` depends on root `font-size`

User font-size overrides (exposed in every major browser's preferences) change the root. Every `rem`-based length scales. This is the mechanism by which `rem`-based layouts respect accessibility preferences. Test at 120% and 200%.

### Never set `html { font-size: 10px }` for "easier math"

A tempting old pattern: set root to 10px so `1.6rem = 16px`. This **discards user preference** — if the user sets their browser default to 20px, your 10px root overrides it. WCAG 1.4.4 violation.

**Correct alternatives:**

```css
/* Leave default — do nothing */
/* or */
:root { font-size: 100%; }   /* explicit equivalent */
:root { font-size: 93.75%; } /* slightly smaller but still relative */
```

---

## Interaction with `font-size-adjust`

Normalizes perceived size across font substitution — useful for fallback stacks where the fallback's x-height differs from the primary. See `../contemporary/metric-overrides.md` for the full recipe.

### Two-value syntax

```css
.body { font-size-adjust: ex-height 0.52; }
.display { font-size-adjust: cap-height 0.72; }
.tabular { font-size-adjust: ch-width 0.48; }
.body { font-size-adjust: ex-height from-font; }  /* pick from primary */
```

Accepted metrics: `ex-height`, `cap-height`, `ch-width`, `ic-width`, `ic-height`.

**Support (2026-04-18):** Chromium 127+ (Jul 2024), Firefox 118+ (Sep 2023), Safari 17+ (Sep 2023). Baseline 2024.

---

## Interaction with Zoom and Accessibility

### Browser zoom (Ctrl+/Cmd+) vs font-size override

Two different mechanisms.

- **Zoom** scales `px` and all dependent units uniformly. Equivalent to multiplying everything by a scale factor.
- **Font-size override** (browser preferences) scales **`em`/`rem`/`%`/`ex`/`ch`/`cap`/`ic`/`lh`/`rlh`** but **NOT `px`**.

A layout built entirely in `px` for font-size does not respond to font-size override and fails WCAG 1.4.4.

### WCAG 1.4.4 (Resize text) — Level AA

> Text can be resized without assistive technology up to 200 percent without loss of content or functionality.

`rem`, `em`, `%`, `cap`, `ex`, `ch` for font-size satisfy this via user override. `px` satisfies only via zoom, not font-size override. Mixed layouts are fine; purely `px` font-size throughout is the failure pattern.

### WCAG 1.4.10 (Reflow) — Level AA

> Content without loss of information or functionality, and without requiring scrolling in two dimensions for a width equivalent to 320 CSS pixels [at 400% zoom].

Combined with 1.4.4: at 200% font-size override **plus** 400% zoom, content must reflow to 320-CSS-pixel-wide viewport without horizontal scroll. A responsive-layout requirement. See `../accessibility/wcag-type.md`.

---

## Unit Conversion Reference

### Absolute

| From | = `px` | = `pt` | = `em` (at 16px base) |
|------|--------|--------|------------------------|
| 1 `in` | 96 | 72 | 6 |
| 1 `cm` | 37.795 | 28.346 | 2.362 |
| 1 `mm` | 3.7795 | 2.8346 | 0.2362 |
| 1 `Q` | 0.9449 | 0.7087 | 0.059 |
| 1 `pt` | 1.3333 | 1 | 0.0833 |
| 1 `pc` | 16 | 12 | 1 |
| 1 `px` | 1 | 0.75 | 0.0625 |

### Body-size cascade at default root `font-size: 16px`

| Expression | Pixels |
|------------|--------|
| `1rem`, `1em`, `16px`, `12pt`, `0.75pc`, `0.1667in`, `4.233mm` | 16 |

### Common gotcha

`1em` at 16px base = **1/6 in** = ~4.23mm. Not half an inch. Half-inch = 48px = 36pt.

---

## Legacy and Edge Cases

- **`ex`** historically used for baseline-aligned icons; `cap` is often better for cap-aligned icons and explicit offsets are more reliable for precise positioning.
- **`ch`** invented for monospace grids; the most common Latin use case (measure caps) misunderstands it. See the `ch` Trap.
- **`mozmm`** (Firefox, never stable) — attempt at a truly physical millimeter on mobile. Removed.
- **`-webkit-device-pixel-ratio`, `-webkit-min-device-pixel-ratio`** — legacy media queries; still accepted as aliases for `resolution` in Chromium/Safari. Prefer `dppx`.
- **CSS Values 5 drafts** — `em`/`lh` resolution at `@property` boundaries, viewport units in feature queries, and element-metric units are all in discussion. Watch drafts.csswg.org/css-values-5/.

---

## Unit Decision Cheatsheet

| Use case | Best unit | Why |
|----------|-----------|-----|
| Body font-size (global) | `rem` | Scales with user preference |
| Body font-size (fluid) | `clamp(<rem>, <rem+vw>, <rem>)` | Scales with viewport, respects preference |
| Heading font-size | `rem` or `clamp()` | Never nest `em`-based |
| Line-height | unitless (`1.5`) | Inherits as ratio |
| Paragraph measure (Latin) | `ch` (approx) or `em`/`rem` (agnostic) | See `ch` Trap |
| Paragraph measure (CJK) | `ic` | Ideographic square = character |
| Baseline grid spacing | `lh`, `rlh` | Rhythm without arithmetic |
| Icon to caps | `cap` | Exact cap-height match |
| Icon to x-height | `ex` | Lowercase optical mass |
| Fluid spacing | `clamp(<rem>, <rem+vw>, <rem>)` | Same reasoning as type |
| Full-height hero | `svh` → `dvh` | Chrome-aware on mobile |
| Component-relative font | `cqi`-based `clamp` | Scales with container |
| Hairlines | `px` or `rem` fraction | Device-pixel predictable |
| Print layout | `pt`, `pc`, `mm`, `cm`, `in` | Honored in `@media print` |
| Never | `font-size: Npx` globally | Breaks user override |
| Never | `html { font-size: 10px }` | Same, disguised as convenience |

---

## Anti-patterns Summary

- **Pixels for font-size** in body/heading. WCAG 1.4.4 violation. Use `rem`.
- **`html { font-size: 10px }`** for math convenience. Overrides user preference.
- **`em` for nested `font-size`.** Compounds unpredictably. Use `rem`.
- **`line-height: 150%` or `1.5em`.** Freezes to px. Use unitless.
- **`max-width: 65ch` taken literally.** It's 70–80 in Latin prose. Approximate; plan tolerances.
- **`cq*` without `container-type`.** Silently zero.
- **Pure `vw` fluid type.** Brittle at viewport extremes. Always `clamp`.
- **`font-size: 2vw`** alone. Ignores user font-size override.
- **`dvh` on static hero.** Pays for real-time recomputation when `svh` suffices.
- **`ch` for CJK prose.** `ch` is the Latin `0`. Use `ic`.

---

## Cross-references

- **Font-internal metrics** the font-relative units resolve against: `./metrics-glossary.md`.
- **Letterform anatomy** for what the metrics measure: `./anatomy.md`.
- **Measure (CPL) recipes** applying `ch`, `em`, `rem`, `cqi` to prose: `../techniques/measure.md`.
- **Modern CSS text properties** interacting with these units: `../contemporary/css-text-properties.md`.
- **`@font-face` overrides** for metric-compatible fallbacks: `../contemporary/metric-overrides.md`.
- **WCAG text requirements** (1.4.4, 1.4.10, 1.4.12): `../accessibility/wcag-type.md`.
- **Vertical rhythm** applications of `lh` and `rlh`: `../techniques/vertical-rhythm.md` (planned).

---

## Sources

Retrieval date 2026-04-18 for all.

- **W3C CSS Values and Units Module Level 4** (CR). https://www.w3.org/TR/css-values-4/ — canonical for every length unit; reference-pixel definition; conversion table.
- **W3C CSS Values and Units Module Level 5** (ED). https://drafts.csswg.org/css-values-5/ — `rex`, `rch`, `rcap`, `ric`; further math functions.
- **W3C CSS Containment Module Level 3** (CR). https://www.w3.org/TR/css-contain-3/#container-lengths — container query units.
- **MDN — `<length>`.** https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length
- **MDN — `font-size-adjust`.** https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust
- **MDN — `calc()`, `clamp()`, `min()`, `max()`, `round()`, `mod()`, `rem()`.** https://developer.mozilla.org/en-US/docs/Web/CSS/calc
- **caniuse — `cap` unit.** https://caniuse.com/mdn-css_types_length-percentage_cap — Firefox 97+, Safari 16.3+, Chromium 133+.
- **caniuse — `lh` unit.** https://caniuse.com/mdn-css_types_length_lh — Chromium 109+, Firefox 120+, Safari 16.4+.
- **caniuse — `rlh` unit.** https://caniuse.com/mdn-css_types_length_rlh — same as `lh`.
- **caniuse — `ic` unit.** https://caniuse.com/mdn-css_types_length_ic — Firefox 94+, Chromium 107+, Safari 16.4+.
- **caniuse — viewport unit variants (svh/lvh/dvh).** https://caniuse.com/viewport-unit-variants — Safari 15.4+, Firefox 101+, Chromium 108+. Baseline Widely Available June 2025.
- **caniuse — container query units.** https://caniuse.com/css-container-query-units — Chromium 105+, Safari 16+, Firefox 110+. Baseline 2023.
- **caniuse — `round()`, `mod()`, `rem()`.** https://caniuse.com/wf-round-mod-rem — Chromium 125+, Safari 15.4+, Firefox 118+. Baseline 2024.
- **caniuse — `font-size-adjust`.** https://caniuse.com/font-size-adjust — Firefox 118+, Safari 17+, Chromium 127+. Baseline 2024.
- **web.dev — "The large, small, and dynamic viewport units."** https://web.dev/blog/viewport-units
- **web.dev — "CSS stepped value math functions in Baseline 2024" (May 2024).** https://web.dev/blog/css-stepped-value-functions
- **web.dev — "CSS font-size-adjust is now in Baseline."** https://web.dev/blog/font-size-adjust
- **WebKit blog — "Polishing your typography with line-height units" (2024).** https://webkit.org/blog/16831/line-height-units/
- **Adam Argyle — "New CSS Relative Units: rex, rch, rcap, ric, rlh" (nerdy.dev, 2023).** https://nerdy.dev/new-relative-units-ric-rex-rlh-and-rch
- **Eric Meyer — "What is the CSS 'ch' Unit?" (meyerweb.com, 2018).** https://meyerweb.com/eric/thoughts/2018/06/28/what-is-the-css-ch-unit/ — canonical explanation of the `0`-glyph definition.
- **Ahmad Shadeed — "CSS cap Unit" (2023).** https://ishadeed.com/article/css-cap-unit/
- **CSSWG Drafts issue tracker.** https://github.com/w3c/csswg-drafts — `ch`-redefinition history.
- **W3C WCAG 2.2 SC 1.4.4 (Resize text).** https://www.w3.org/TR/WCAG22/#resize-text
- **W3C WCAG 2.2 SC 1.4.10 (Reflow).** https://www.w3.org/TR/WCAG22/#reflow
