---
date: 2026-04-17
coverage: deep
peers:
  - ./css-text-properties.md
  - ./opentype-features.md
  - ./color-fonts.md
  - ./font-delivery.md
  - ../techniques/optical-size.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview
  - https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg
  - https://learn.microsoft.com/en-us/typography/opentype/spec/avar
  - https://learn.microsoft.com/en-us/typography/opentype/spec/fvar
  - https://learn.microsoft.com/en-us/typography/opentype/spec/stat
  - https://www.w3.org/TR/css-fonts-4/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts
  - https://github.com/harfbuzz/boring-expansion-spec/blob/main/avar2.md
  - https://github.com/googlefonts/roboto-flex
  - https://github.com/googlefonts/amstelvar
  - https://github.com/arrowtype/recursive
  - https://caniuse.com/variable-fonts
  - https://caniuse.com/colr-v1
---

# Variable Fonts

A variable font is a single OpenType/TrueType container exposing one or more continuous **design-variation axes** whose coordinates resolve to a specific glyph outline (and, optionally, color) at render time. Variable fonts were introduced in **OpenType 1.8 (September 2016)** as a joint Apple / Google / Microsoft / Adobe effort. The current baseline is **OpenType 1.9.1 (May 2024)**, which clarifies delta application, COLRv1 interaction, and normalization semantics. Web platform support for the CSS surface (`font-variation-settings`, `font-optical-sizing`, variable-font-aware `font-weight`/`font-style`/`font-stretch`) is near-universal on evergreen browsers as of **April 2026** (~95.9% global — caniuse 2026-04). Everything below assumes the font container is TrueType-flavoured with `gvar`/`glyf` or CFF2-flavoured; CFF2 is OpenType-only and is not handled by legacy TT processors.

Registered axes have **lowercase** 4-byte tags and carry interoperable semantics (`wght`, `wdth`, `ital`, `slnt`, `opsz`). Foundry-defined (custom) axes have **uppercase** 4-byte tags and are opaque to applications unless the foundry publishes their semantics (Microsoft OpenType Design-Variation Axis Tag Registry, 2024-05-29). **This uppercase/lowercase split is a hard requirement in the spec** — an application can always know if a tag is registered by checking the first byte.

## Registered Axes

| Tag | CSS property | Default | Typical range | What it controls | OT registration |
|---|---|---|---|---|---|
| `wght` | `font-weight` | 400 | 1–1000 (typical fonts: 100–900) | Stroke thickness / overall darkness | OT 1.8 (2016) |
| `wdth` | `font-stretch` / `font-width` | 100 | >0 (typical fonts: 50–200) | Horizontal proportion as % of "normal" | OT 1.8 (2016) |
| `ital` | `font-style` (`normal`/`italic`) | 0 | 0 or 1 (treated discretely) | Switch between Roman and italic subdesign | OT 1.8 (2016) |
| `slnt` | `font-style: oblique <deg>` | 0 | >-90 to <+90 degrees | Counter-clockwise degrees of slant from upright | OT 1.8 (2016) |
| `opsz` | `font-optical-sizing: auto` | designer's call | >0 (text sizes in typographic points) | Glyph proportions tuned to display size | OT 1.8 (2016) |

Sources for rows above: Microsoft Learn `dvaraxistag_*` pages, all updated 2024-05-29.

### `wght` (Weight)

- **Scale semantics**: numerically comparable to `OS/2.usWeightClass` and to CSS `font-weight`. 400 = Regular; 700 = Bold; 100 = Thin; 900 = Black. The spec allows 1–1000 but most production fonts stop at 100–900.
- **Interoperability caveat**: a value of 700 in font A is not guaranteed to have the same perceived darkness as 700 in font B. It is guaranteed to be heavier than 400 in the same family.
- **`OS/2.usWeightClass` invariance**: in a variable font, the `usWeightClass` value in the OS/2 table **must** match the default `wght` value declared in `fvar`. Non-default instances may derive their own `usWeightClass` from their `wght` setting.
- **CSS interaction**: `font-weight: 425` is a legitimate value when a `wght`-variable font is active. The browser maps it straight through to the axis; no nearest-100 snap.
- **Synthesis**: when `font-synthesis-weight: auto` (default) is set and the font does not cover the requested weight, the browser may synthesize. When the variable font covers the full range, synthesis is a no-op — but `font-synthesis-weight: none` is still recommended as a defensive fence, particularly when values are applied via `font-variation-settings` (see anti-patterns).

### `wdth` (Width)

- **Scale semantics**: percentage of "normal width" as the designer defines it. 100 = Regular; 50 = half-wide; 200 = double-wide. Different from `OS/2.usWidthClass`, which uses 9 enumerated integers — when mapping, interpolate and round/clamp to 1–9.
- **CSS interaction**: in CSS the value is written with a `%` in `font-stretch` and `font-width` (e.g., `font-stretch: 85%`); in `font-variation-settings` the bare number is used (`"wdth" 85`). This is a common source of bugs — do **not** write `"wdth" 85%` in `font-variation-settings`.
- **`font-stretch` vs `font-width`**: CSS Fonts L4 renamed `font-stretch` to `font-width` (CSS Fonts L4 WD 2026-03-03 §8.2). Both properties are aliases; `font-width` is the canonical name in L4, `font-stretch` remains for back-compat.
- **Programmatic use**: applications may nudge `wdth` to fit a span into a target width (Microsoft `dvaraxistag_wdth`). `wdth` adjustment is text-content-dependent because strings have different character compositions; expect 1–2 refinement iterations.

### `ital` (Italic)

- **Scale semantics**: 0 = Roman; 1 = fully italic. Spec allows fractional values but it is conventionally treated as **discrete** (a switch, not a dial). Intermediate values are rarely designed for and produce unpleasant half-italic outlines.
- **Why discrete**: italic is a *different design* — letterforms, terminals, and construction change. Interpolating across `ital 0 → 1` does not mean "get half as cursive"; it means linearly blending two different skeletons, which produces mush.
- **Common pattern**: most families ship a separate italic variable font file (e.g., `MyFont-Italic.woff2`) rather than bundling `ital` as an axis in one file. `@font-face` with the italic file bound to `font-style: italic` is the idiomatic wiring.
- **CSS mapping**: `font-style: italic` → `ital 1`. `font-style: normal` → `ital 0`. No intermediate CSS value exists for `ital`.

### `slnt` (Slant)

- **Scale semantics**: the angle of oblique slant in **counter-clockwise degrees from upright**. Range is strictly greater than -90 and strictly less than +90. `slnt 0` = upright. A typical right-leaning oblique has a **negative** slant value, e.g., `slnt -10` or `slnt -14` — this catches a lot of authors off-guard (Microsoft `dvaraxistag_slnt`, 2020-10-08, carried unchanged into 1.9.1).
- **Matches `post.italicAngle`**: in a variable font implementing `slnt`, the default `slnt` value must match `post.italicAngle`. Non-default instances derive their `post.italicAngle` from their current `slnt` setting.
- **CSS mapping**: `font-style: oblique 14deg` → `slnt -14`. Note the **sign flip**: CSS oblique uses positive degrees for rightward lean; `slnt` uses counter-clockwise, so CSS positive → `slnt` negative. (MDN "Variable fonts", retrieved 2026-04-17.)
- **`slnt` is not a substitute for `ital` when both exist in a family**: a slanted Roman is not an italic. Italics have different skeletons (`a` → single-storey, `g` → single-storey in many designs, `f` with descender, etc.). Using `slnt` to fake italic drops the designed italic glyphs and produces mechanical-looking text. Use `slnt` only on families that have no true italic cut.
- **When a family legitimately uses both `slnt` and `ital`**: rare but it happens — a family with an italic design that additionally varies in slant (e.g., a lighter italic at `slnt -8` and a heavier italic at `slnt -12`). In that case `slnt -10` + `ital 1` is a well-formed point in design space.

### `opsz` (Optical Size)

- **Scale semantics**: the value is interpreted as **text size in typographic points** (1 pt = 1/72 inch). An `opsz` value of 12 means the glyph is tuned for 12-point display, not 12 anything else. Valid range is strictly greater than zero. Typical design ranges: 8–144.
- **Recommended regular**: the spec recommends 10–16 for a "Regular" text variant (Microsoft `dvaraxistag_opsz`).
- **`font-optical-sizing: auto`** — the high-level CSS property. When `auto` and the font has an `opsz` axis, the browser sets `opsz` to the rendered `font-size` in points, clamped to the axis min/max (MDN, CSS Fonts L4 §8.1). When `none`, automatic selection is disabled and `opsz` stays at the font default.
- **Browser support for `font-optical-sizing`** (caniuse 2026-04): Chrome 79+, Firefox 62+, Safari 13.1+, Edge 17+. iOS Safari 13.4+. Global ~95.6%.
- **When `auto` picks wrong**: the browser uses the *rendered* size, but optical size is fundamentally about the **reader's perceived size** — distance × physical pixels × zoom. On TV-style displays viewed from 10 feet, the rendered pixel size is huge but the perceived size is small. In those cases, pin `opsz` manually. See `../techniques/optical-size.md`.
- **Manual pinning**: `font-variation-settings: "opsz" 18` forces the axis regardless of `font-size`. Useful for display headlines that should keep their delicate hairlines even at larger-than-"display"-cut sizes.
- **Sub-`opsz` tuning**: common pattern is to pin `opsz` below the actual `font-size` to get chunkier, legibility-first glyphs at display sizes; or above the `font-size` to get finer text-cut glyphs rendered small without `auto` kicking in the display cut.

## Custom Axes

Custom (foundry-defined) axes must start with an **uppercase ASCII letter** (0x41–0x5A) and use only uppercase letters or digits. Registered tags never collide with custom tags by construction. (Microsoft `dvaraxisreg`, §Syntactic requirements, 2024-05-29.)

| Tag | Source fonts | Conventional range | What it controls |
|---|---|---|---|
| `GRAD` | Roboto Flex, Amstelvar, Google Symbols | -200 to +150 (Roboto Flex); varies | Grade — stroke darkness *without* metric changes. Widths are preserved, so line breaks are stable under animation. |
| `MONO` | Recursive | 0.0 to 1.0 | Proportional (0) ↔ monospace (1). Glyph widths remain consistent across weight/slant in Recursive. |
| `CASL` | Recursive | 0.0 to 1.0 | Casual — linear / "rational" (0) ↔ casual / signpainter (1). Adjusts terminals, curvature, contrast. |
| `CRSV` | Recursive | 0.0 to 1.0 | Cursive — controls whether italic letterforms (single-storey a, g) appear. Distinct from `slnt`. |
| `XOPQ` | Amstelvar, Roboto Flex | varies per UPM | Parametric thick stroke (stems). Measured in font units per mille of UPM. |
| `YOPQ` | Amstelvar, Roboto Flex | varies per UPM | Parametric thin stroke (hairlines/bars). |
| `XTRA` | Amstelvar, Roboto Flex | varies | Parametric counter (inner whitespace) width. |
| `XOPQ`, `YOPQ`, `XTRA` together | Amstelvar, Roboto Flex | — | A "parametric triplet" that lets one manipulate weight, contrast, and width independently of the compound `wght`/`wdth` axes. Berlow's model (2017). |
| `YTLC` | Amstelvar, Roboto Flex | varies | Y-transparent lowercase — x-height adjustment. |
| `YTUC` | Roboto Flex | varies | Y-transparent uppercase — cap height adjustment. |
| `YTAS` | Roboto Flex | varies | Y-transparent ascenders. |
| `YTDE` | Roboto Flex | varies | Y-transparent descenders. |
| `YTFI` | Roboto Flex | varies | Y-transparent figures — numeral height. |

Conventions: `X` prefix = horizontal dimension; `Y` prefix = vertical. `OPQ` from "opaque" = the inked stem. `TRA` from "transparent" = the counter or whitespace. `YT` prefix = vertical-transparent metric per glyph class (UC=uppercase, LC=lowercase, AS=ascender, DE=descender, FI=figures). Convention established by David Berlow / TypeNetwork's parametric model (Amstelvar, 2017) and codified in Roboto Flex (Google Fonts, 2022).

**Google Symbols** (2022+) adds `FILL` (fill level 0–1), `GRAD` (grade), and `opsz` to the registered `wght` axis for icon fonts.

### Axis registration with the OpenType registry

- Four-byte ASCII tag; use only letters, digits, and trailing spaces; must start with a letter.
- Registered tags are always lowercase (registry defined); custom tags must be uppercase.
- Microsoft encourages registration of axes that (a) multiple foundries will adopt, and (b) applications will select programmatically. Registration requires: US English display name, description, numeric scale semantics with valid range, recommended "Regular" value.
- Not every worthwhile axis is registered — `GRAD` (widely used) remains custom because no objective measure exists. This is fine; custom axes work universally in variable fonts, they just require `font-variation-settings` in CSS.
- To propose a registration: open an issue at `MicrosoftDocs/typography-issues` on GitHub with rationale and cross-vendor consensus.

## CSS Surface

Two layers coexist: **high-level properties** (`font-weight`, `font-stretch`/`font-width`, `font-style`, `font-optical-sizing`) which map onto registered axes, and the low-level **`font-variation-settings`** which sets any axis by tag.

### When high-level wins vs `font-variation-settings`

| Scenario | Use this | Rationale |
|---|---|---|
| Setting registered axis (`wght`, `wdth`, `ital`, `slnt`, `opsz`) | High-level property | Composes with `font-synthesis`, respects user-agent stylesheets (`<strong>`, `<em>`), inherits correctly, works with `font` shorthand. |
| Setting a custom axis (`GRAD`, `MONO`, any uppercase tag) | `font-variation-settings` | No high-level property exists. |
| Animating registered axis smoothly | `font-variation-settings` via registered `@property` | High-level `font-weight` animates as discrete per current CSS; `font-variation-settings` interpolates when both endpoints have same axes in same order. |
| Mixed registered + custom axes | `font-variation-settings` for all, **or** high-level + FVS (accepting the override rule) | Spec: "Font characteristics set using `font-variation-settings` will always override those set using the corresponding basic font properties" (MDN). Safer to set all axes in one place. |
| Need `font-synthesis` to act correctly | High-level property | Synthesis rules key off `font-weight` / `font-style`, not FVS. |

### Precedence rule (load-bearing)

> `font-variation-settings` overrides the corresponding basic font properties, no matter where they appear in the cascade. (MDN, CSS Fonts L4 §7.2 "Feature and variation precedence".)

Consequence: if a stylesheet sets `font-weight: 700` and another class sets `font-variation-settings: "wght" 400`, the element renders at weight 400 — even if `font-variation-settings` is lower-specificity. This is counter-intuitive and a frequent bug source.

### `@font-face` descriptors for variable fonts

```css
@font-face {
  font-family: "Inter";
  src: url("Inter.var.woff2") format("woff2-variations"),
       url("Inter.var.woff2") format("woff2 supports variations");
  font-weight: 100 900;           /* min max — a range */
  font-stretch: 75% 125%;         /* min max — a range */
  font-style: oblique 0deg 12deg; /* slnt range */
  font-named-instance: "Regular"; /* optional; CSS Fonts L4 §4.7 */
  font-display: swap;
}
```

- `format("woff2-variations")` — original syntax. Deprecated in CSS Fonts L4 but still in use.
- `format("woff2 supports variations")` — canonical modern syntax.
- `font-named-instance` descriptor (CSS Fonts L4 §4.7) selects a named instance defined in the font's `fvar.namedInstance` records by its localized sub-family name. Implementation is uneven across engines; Safari has had partial support since 17 (2023), Chromium is in progress as of 2026-04 (csswg issue #10952).

### CSS wiring matrix

```css
/* Registered axes via high-level (preferred) */
.hl {
  font-weight: 450;                  /* wght */
  font-stretch: 85%;                 /* wdth */
  font-style: oblique -10deg;        /* slnt (CSS +10deg → slnt -10) */
  font-optical-sizing: auto;         /* opsz from font-size */
}

/* Custom axes via FVS (required) */
.custom {
  font-variation-settings:
    "GRAD" 88,
    "MONO" 0.4;
}

/* Mixed — one place */
.all-fvs {
  font-variation-settings:
    "wght" 450,
    "wdth" 85,
    "opsz" 18,
    "GRAD" 0;
  font-synthesis-weight: none; /* defensive: don't let the UA synthesize */
}
```

## Interpolation Semantics

A point in design space is an N-tuple of axis coordinates (one per `fvar` axis), e.g., `(wght=450, wdth=85, opsz=18)`. To render a glyph at that point:

1. **Normalize** each axis coordinate from its user-scale (what the author writes) to a normalized scale where min=-1, default=0, max=+1. Piecewise linear between min→default and default→max, using the `fvar` axis record's `minValue`, `defaultValue`, `maxValue` (Microsoft `otvaroverview` §Coordinate Scales and Normalization, 1.9.1).
2. **Apply `avar` remapping** (if present): remaps normalized values through a piecewise-linear segment map. `avar 1.0` requires three anchor points (-1→-1, 0→0, +1→+1); the designer can insert additional break-points to non-linearize the axis (e.g., make middle weights change faster than extremes).
3. **Apply `avar 2.0` axis-variation-store remapping** (if present — see below).
4. **Fetch deltas** from `gvar` (for TrueType outlines) or CFF2 VarStore (for CFF2). Each variation region in `gvar` defines a contribution to each glyph's control points; contributions are interpolated by the tent-function weight of each region relative to the current normalized point.
5. **Apply metric deltas** from `HVAR` (horizontal), `VVAR` (vertical), `MVAR` (font-wide metrics), `HVAR` for advance widths, etc.

### Discrete vs continuous axes

- **Continuous**: `wght`, `wdth`, `slnt`, `opsz`, `GRAD`, `MONO`, `CASL`, parametric axes. Any value in range is a legitimate point.
- **Discrete (by convention, not spec)**: `ital`. The axis is nominally 0.0–1.0 and an implementation must interpolate if an intermediate value is requested, but designers overwhelmingly author only at 0 and 1. Treat anything between as undefined behavior.

### Why `slnt` is not a substitute for `ital`

`slnt` interpolates the *same* Roman outlines at a slant angle. `ital` at 1 is a **different set of outlines** — cursive skeletons, different terminals, replacement glyphs (single-storey `a`, single-storey `g`, looped `f`, etc.). These are two different kinds of variation. Families like Source Sans 3 ship both because they're not interchangeable. Fonts that only have `slnt` (e.g., many sans-serifs designed as oblique-only) genuinely have no italic to fall back to — in those cases `slnt` is the italic surface.

### `avar 2.0` warping

Introduced via the **HarfBuzz Boring Expansion Spec** (2022–2023) and rolled into a subsequent OpenType revision; HarfBuzz implements it; Microsoft OT 1.9.1 (May 2024) notes the axis-variation-store extension. `avar 2.0` turns the per-axis piecewise-linear `avar` into a **many-to-many** warping: the output normalized coordinate on axis Y can depend on the current input on multiple axes (X1, X2, ...). Encoded by reusing the ItemVariationStore mechanism — an `axisIndexMap` and a `varStore` hang off the `avar` header alongside the legacy v1 segment maps.

Practical uses:
- **Design-space warping**: designers can author at virtual master positions that do not correspond to user-facing axis values. A "virtual `Black` master" at `wght=900, XOPQ=x` can be moved programmatically via `avar 2.0` so that `wght=900` on the user-facing axis corresponds to the designer's chosen internal point.
- **Axis synchronization**: `opsz` can be made to automatically adjust `YOPQ` for larger sizes (hairlines thinner at display) without needing two separate CSS writes.
- **Hidden-axis parametric fonts**: expose `wght`/`wdth` to users but drive `XOPQ`/`YOPQ`/`XTRA` internally.

Tooling: **Fencer** web app (released 2024-05-03) is the first interactive editor for `avar 2.0` mappings. Browser support: HarfBuzz (shipping in Chrome, Firefox) handles `avar 2.0` normalization; Safari / Core Text status uneven as of 2026-04.

## Optical Sizing

See also `../techniques/optical-size.md`.

- `font-optical-sizing: auto` is the default in modern UAs when a font has an `opsz` axis. It sets `opsz` = rendered `font-size` in CSS points.
- **When auto picks wrong**:
  - Zoomable viewports (the browser may or may not factor zoom — implementation-defined; Chrome does, Safari historically did not).
  - TVs / large wall displays where physical size ≠ reader-perceived size.
  - Screenshots / hi-DPI exports where CSS points and perceived size diverge.
  - Font-size set in `em`/`%` when the inherited size is tiny but the viewport is not.
- **Manual override**: `font-variation-settings: "opsz" 18` wins over `font-optical-sizing: auto` because FVS overrides high-level properties. Use this to pin.
- **Sub-`opsz` usage**: `opsz 10` on a 48px headline gives you chunky, reinforced letters — useful in display contexts where the "display" cut of a font is too delicate for the design. Conversely, pinning `opsz 48` on 14px body text gives hairlines at reading size (usually a mistake, occasionally a deliberate editorial choice).

## Animation

### Direct animation of `font-variation-settings`

```css
h1 {
  font-variation-settings: "wght" 400, "GRAD" 0;
  transition: font-variation-settings 400ms ease;
}
h1:hover {
  font-variation-settings: "wght" 700, "GRAD" 100;
}
```

WebKit implemented `font-variation-settings` interpolation in 2021 (WebKit Bug 162783, changeset 274235). **Interpolation requires endpoints to have the same axes listed in the same order with the same tags.** If the two endpoints differ in axis list, WebKit falls back to a discrete (step-change) animation. Chromium follows the same rule.

### Animation via `@property`-registered custom properties

Better pattern when only *one* axis should animate while others stay pinned:

```css
@property --wght {
  syntax: "<number>";
  initial-value: 400;
  inherits: true;
}

h1 {
  --wght: 400;
  font-variation-settings: "wght" var(--wght), "GRAD" 0;
  transition: --wght 400ms ease;
}
h1:hover {
  --wght: 700;
}
```

Without `@property`, CSS custom properties are *strings* — the browser cannot interpolate them, so `transition: --wght` is a no-op. `@property` with `syntax: "<number>"` (or `<integer>`, `<percentage>`, `<angle>` as appropriate) tells the engine the property has a typed value and enables interpolation on the custom property itself. The axis value can then be driven smoothly while the rest of the `font-variation-settings` string remains static.

Browser support for `@property`: Chrome 85+, Safari 16.4+, Firefox 128+ (landed 2024-07). Universal on evergreen by 2026-04.

### Named instances vs smooth axis values

A **named instance** (defined in `fvar.namedInstance`) is a preset point in design space — e.g., "Bold Condensed Display". CSS access via `font-named-instance: "Bold Condensed"` is in CSS Fonts L4. Named instances are not animation-friendly: they are *points*, not ranges. If you need smooth animation, ignore named instances and use axis values directly.

Named instances are, however, valuable for:
- Matching `OS/2.usWeightClass` / `OS/2.usWidthClass` expectations in legacy consumers (Word, InDesign).
- Surfacing to users in font pickers with human-readable names.
- Printing: named instances often correspond to static subsets that printers know.

## File Format and Rendering

### Core tables

| Table | Role | Required in var font |
|---|---|---|
| `fvar` | Font-variations header: axes list, min/default/max per axis, `namedInstance` array. | Yes |
| `gvar` | Glyph-variation deltas: for each TrueType glyph, delta vectors per variation region. | Yes (TT-flavored) |
| CFF2 `VarStore` | Glyph-variation deltas (CFF2 flavor). | Yes (CFF2-flavored) |
| `HVAR` | Horizontal metric variations — delta for advance-width, LSB per glyph. | Recommended |
| `VVAR` | Vertical metric variations (for vertical-writing fonts). | Conditional |
| `MVAR` | Font-wide metric variations: ascender, descender, x-height, cap-height, subscript/superscript positions, etc. | Recommended |
| `avar` | Axis variations: piecewise-linear normalization remapping. Required for `avar 2.0` warping. | Optional |
| `STAT` | Style-attributes table: axis records, axis-value labels, range labels ("Subhead" covers opsz 14–24). | **Required** in all variable fonts. |
| `cvar` | Control-value variations (TrueType instructions). | Optional |

Microsoft OT 1.9 (Dec 2021) added COLR to tables that can carry variation data — enabling animated/variable color fonts (see below). OT 1.9.1 (2024-05) clarified delta application rules and support for 32-bit deltas via `wordDeltaCount`.

### How the browser resolves an axis value

Every render with a variable font, per glyph:

1. Read user-scale values from CSS (either via high-level properties → axis lookup, or via `font-variation-settings`).
2. Clamp each value to axis `[minValue, maxValue]` from `fvar`.
3. Default-normalize each to [-1, +1]. (Formula in Microsoft `otvaroverview` §CSN.)
4. Apply `avar 1.0` segment map, if present.
5. Apply `avar 2.0` warp, if present.
6. For each variation region in `gvar`/CFF2 VarStore, compute the region's tent-function weight at the current normalized point.
7. Sum weight × delta vectors across regions to derive glyph control points.
8. Hint (TrueType) / flatten (CFF2) as usual; rasterize.

### Animation implementation cost

Smooth animation on `wght` alone: ~one additional multiply-add per control point per frame (per glyph). Modern browsers rasterize only the glyphs on screen; animating headlines or small text spans is cheap (<1ms per frame on a mid-range device). Animating thousands of glyphs at once is expensive. Performance caveat: Safari's font rasterizer caches by exact axis coordinate — continuous animation invalidates the cache constantly. WebKit and Blink both mitigate with glyph-atlas LRU caches.

## File Size and Delivery

See `./font-delivery.md` for the full delivery story.

Rule of thumb (2026-04, representative numbers):

| Scenario | Static WOFF2 total | Variable WOFF2 | Break-even |
|---|---|---|---|
| Regular 400 only | ~25 KB | ~90 KB | Static wins |
| Regular 400 + Bold 700 | ~50 KB | ~90 KB | Static wins (by a hair) |
| 3 weights (400/500/700) | ~75 KB | ~90 KB | Tied; variable wins on flexibility |
| 6 weights + italic | ~300 KB | ~180 KB | Variable wins |
| Full family (9 weights × 2 styles) | ~540 KB | ~180 KB | Variable wins by 3× |

Exact numbers vary enormously by family (Inter, Source Sans 3, Roboto Flex all differ). Variable fonts win when the design team will actually use the flexibility; they lose when only one or two cuts are needed.

### Subsetting a variable font

**Safe**: subsetting by Unicode range (`pyftsubset --unicodes=...`) and layout-feature trimming. All variation data is preserved — `fvar`, `gvar`, `HVAR`, `MVAR`, `avar`, `STAT` survive.

**Lossy**:
- Dropping glyphs also drops their `gvar` delta data (correctly — those glyphs no longer exist).
- Using `--no-layout-closure` or `--drop-tables` too aggressively can kill tables variable fonts depend on. Never drop `fvar`, `gvar` / CFF2 VarStore, `HVAR`, `STAT`, or `avar`.
- Instancing (freezing an axis to a single value) removes that axis from `fvar` and shrinks `gvar`. This is a legitimate shrink strategy — `fonttools varLib.instancer` is the tool. E.g., shipping a version with `opsz` locked to 16 removes the `opsz` axis entirely.

**Known sharp edges** (fonttools issue #1894): `pyftsubset --ignore-missing-glyphs` on a variable font can produce unexpectedly tiny output due to a bug in the delta-pruning pass. Check output size; a 2KB result is always a bug. Workaround: subset with an accurate unicode range, don't rely on `--ignore-missing-glyphs`.

**`unicode-range` splitting**: still works, and works well. Each split subset preserves the variable axes for its glyph range. A Latin-plus-Cyrillic variable font can be split into two subsets; the browser downloads only the ones matching used code points. See `./font-delivery.md` for the full pattern.

## Color Fonts + Variable Axes

OT 1.9 (Dec 2021) extended COLR to table list capable of variation, enabling **COLRv1 variable color fonts** (MS `otvarcommonformats` + COLR v1 header). The variation mechanism propagates to color stops, gradient geometry, and composed layers.

- **Browser support** (caniuse 2026-04): Chrome 98+, Firefox 107+, Edge 98+. **Safari: no support as of 26.5**. Safari's COLRv0 support is fine; COLRv1 remains unimplemented in WebKit.
- **Animation through axes**: because COLRv1 gradient geometry is variable, animating `font-variation-settings` on a COLRv1 font *does* interpolate color-stop positions and gradient angles smoothly. Example: a variable "sunset" color font with an `opsz`-linked hue shift, or a logo font where `GRAD` sweeps through a palette.
- **`font-palette` does NOT interpolate**: per CSS Fonts L4, transitions between `font-palette` values are discrete — the browser switches palette at the 50% mark (W3C CSS Fonts L4 §9.1; confirmed in Chromium impl notes 2023). If you want animated color across variable fonts, it must come through the axes, not through palette switching.

Reference fonts: Nabla (by Arthur Reinders Folmer & Just van Rossum, 2022) is the archetypal variable COLRv1 font with `wght`, `EDPT` (depth), `EHLT` (highlight) axes driving gradient geometry.

## Authoring Notes

### Toolchain (2026-04)

- **Fontmake** (Google Fonts, active; `fontmake --variable` produces a TTF from a `.designspace` / `.glyphs` source). Wraps `glyphsLib` (for `.glyphs` → UFO/designspace conversion) and `ufo2ft` (for UFO → OT/TT compilation). With `ufo2ft 3.0.0+`, feature writers generate **variable FEA** compiled once per VF, rather than per-master merge — fewer merge bugs, smaller output.
- **Glyphs 3** (macOS GUI app, Glyphs GmbH): `File → Export → Variable Font`. Smart compatibility check before export.
- **FontLab 8** (commercial, cross-platform): full variable authoring + interpolation preview.
- **fontTools / varLib** (Python, the library underneath all of them): `varLib.build` takes a designspace + UFOs and emits a variable font. `varLib.instancer` freezes or partially-instances axes.
- **Samsa / Axis-Praxis** (web-based inspection and playground): debug an existing variable font, read its `fvar`, `STAT`, `avar`, test axis values.

### Reference vehicles

- **Amstelvar** (David Berlow, 2017; googlefonts/amstelvar): the original parametric variable font. Exposes `wght`, `wdth`, `opsz` as user axes and the full parametric triplet `XOPQ`/`YOPQ`/`XTRA` + the Y-transparency bundle (`YTLC`, `YTUC`, `YTAS`, `YTDE`, `YTFG`) internally. Used as the didactic reference in TypeNetwork / Berlow's "parametric axes" papers.
- **Roboto Flex** (Google Fonts, 2022; googlefonts/roboto-flex): production-grade Roboto rebuilt on the parametric model. 13 axes. Demonstrates that the parametric approach scales to a general-purpose family.
- **Recursive** (Arrow Type, 2020–; arrowtype/recursive): `wght`, `slnt`, `MONO`, `CASL`, `CRSV`. Metric-stable across all axis moves — a reference for "animation without layout shift."

### Why designing for variable is harder than designing statics

- **Interpolation compatibility**: every glyph must have the same number of contours, points, and off-curve structure across all masters. A single mismatch anywhere breaks the whole font. Design tools (Glyphs, FontLab) have compatibility checkers but catching *every* mismatch across dozens of masters and thousands of glyphs is a persistent source of bugs.
- **Mid-axis quality**: statics let the designer hand-draw intermediate weights. Variable interpolation may produce ugly middle weights even when endpoints are good. Remedies: add intermediate masters, use `avar` to non-linearize, use `avar 2.0` warping.
- **Hinting**: TrueType hinting must work across the full design space. Autohinter coverage across variable ranges is imperfect; some foundries ship hinted statics alongside unhinted variable.
- **QA combinatorics**: testing every (wght × wdth × opsz × ital) combination is intractable. Named instances become the QA basis.

## Anti-patterns

| Pattern | Why it's wrong | Fix |
|---|---|---|
| Using `slnt` where `ital` exists, dropping designed italic glyphs | `slnt` just slants the Roman — the designed italic `a`, `g`, `f` etc. never render. Text looks mechanical. | Use `font-style: italic` so `ital 1` (or the italic @font-face) is selected. |
| Setting `font-variation-settings: "wght" 400` instead of `font-weight: 400` | FVS overrides high-level properties globally; breaks `font-synthesis`, `font` shorthand, UA stylesheet matching for `<strong>`/`<b>`, and inherits weirdly through the cascade. | Use `font-weight: 400`. Reserve FVS for custom axes only. |
| Animating `font-variation-settings` with mismatched axis lists | WebKit/Blink fall back to discrete (step) animation when start/end have different axes. | Make axis list identical in both endpoints; use `@property`-registered custom property for the changing value. |
| Transitioning a raw CSS variable (no `@property`) driving `font-variation-settings` | Raw `--foo` is a string; browsers can't interpolate strings. Transition is discrete. | Register with `@property { syntax: "<number>"; ... }`. |
| Writing `"wdth" 85%` in `font-variation-settings` | `font-variation-settings` takes bare numbers, not CSS percentages. Silently invalid. | Write `"wdth" 85`. In `font-stretch` / `font-width` use `85%`. |
| Forgetting `font-synthesis-weight: none` when driving weight via FVS on custom-axis fonts | Safari may synthesize fake-bold on top of FVS, double-weighting the text. | Set `font-synthesis-weight: none` on `body`/`:root`. |
| Over-subsetting a variable font | Dropping `HVAR`, `MVAR`, `STAT`, or `avar` breaks variation. `--ignore-missing-glyphs` produces truncated output (fonttools #1894). | Subset by Unicode range only. Keep all variation tables. Never drop `fvar`. |
| Dropping `STAT` | STAT is **required** in variable fonts (MS OT 1.9.1). Without it, UIs cannot label instances and some UAs reject the font outright. | Keep STAT. |
| Mapping CSS `oblique 10deg` to `slnt 10` | Sign flip: CSS positive = rightward, `slnt` positive = counter-clockwise (leftward). Result: font slants the wrong way. | CSS `oblique 10deg` → `slnt -10`. |
| Pinning `opsz` to a single value when the font has a real `opsz` axis | Wastes the axis. Headline and body both render at the same cut. | Use `font-optical-sizing: auto` and let it follow `font-size`. Override only when auto is wrong. |
| Using a variable font for a single weight | Variable overhead (`fvar`, `gvar`, delta tables) is pure waste when only one point is used. | Ship the static WOFF2 for the specific weight. |
| Relying on `font-named-instance` in production as of 2026-04 | Uneven cross-browser; Chromium partial, Safari partial, Firefox proposal stage. | Set axes explicitly with `font-weight` / `font-stretch` / `font-variation-settings`. Revisit `font-named-instance` in 2027. |
| Animating `font-palette` expecting smooth color transition | Per CSS Fonts L4, palette transitions are discrete. | Animate via `font-variation-settings` on a COLRv1 variable font, not via palette. |

## Sources

- Microsoft Learn. "OpenType Font Variations overview (OpenType 1.9.1)". 2024-05-30. https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview (retrieved 2026-04-17).
- Microsoft Learn. "OpenType Design-Variation Axis Tag Registry (OpenType 1.9.1)". 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg (retrieved 2026-04-17).
- Microsoft Learn. "'fvar' — Font Variations Table". 1.9.1, 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/fvar (retrieved 2026-04-17).
- Microsoft Learn. "'avar' — Axis variations table". 1.9.1, 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/avar (retrieved 2026-04-17).
- Microsoft Learn. "'STAT' — Style Attributes Table". 1.9.1, 2024. https://learn.microsoft.com/en-us/typography/opentype/spec/stat (retrieved 2026-04-17).
- Microsoft Learn. "'wght' design-variation axis tag". 1.9.1, 2020-10-08 (unchanged). https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_wght.
- Microsoft Learn. "'wdth' design-variation axis tag". 1.9.1, 2020-10-08. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_wdth.
- Microsoft Learn. "'ital' design-variation axis tag". 1.9.1, 2020-10-08. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_ital.
- Microsoft Learn. "'slnt' design-variation axis tag". 1.9.1, 2020-10-08. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_slnt.
- Microsoft Learn. "'opsz' design-variation axis tag". 1.9.1, 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz.
- Microsoft Learn. "OpenType change log (1.9.1)". 2024-05. https://learn.microsoft.com/en-us/typography/opentype/spec/changes.
- W3C. "CSS Fonts Module Level 4". W3C Working Draft, 2026-03-03. https://www.w3.org/TR/css-fonts-4/ (retrieved 2026-04-17).
- MDN Web Docs. "Variable fonts guide". Mozilla Contributors. https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts (retrieved 2026-04-17).
- MDN Web Docs. "`font-variation-settings`". https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variation-settings (retrieved 2026-04-17).
- MDN Web Docs. "`font-optical-sizing`". https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing (retrieved 2026-04-17).
- HarfBuzz Boring Expansion Spec. "avar2 specification". https://github.com/harfbuzz/boring-expansion-spec/blob/main/avar2.md (retrieved 2026-04-17).
- Google Fonts. googlefonts/roboto-flex GitHub repository. https://github.com/googlefonts/roboto-flex (retrieved 2026-04-17).
- Google Fonts. googlefonts/amstelvar GitHub repository. https://github.com/googlefonts/amstelvar (retrieved 2026-04-17).
- Arrow Type. arrowtype/recursive GitHub repository. https://github.com/arrowtype/recursive (retrieved 2026-04-17).
- caniuse.com. "Variable fonts". 2026-04. https://caniuse.com/variable-fonts.
- caniuse.com. "`font-optical-sizing`". 2026-04. https://caniuse.com/mdn-css_properties_font-optical-sizing.
- caniuse.com. "COLR/CPAL(v1) Font Formats". 2026-04. https://caniuse.com/colr-v1.
- Chrome for Developers. "COLRv1 Color Gradient Vector Fonts in Chrome 98". Dominik Röttsches, 2022. https://developer.chrome.com/blog/colrv1-fonts.
- Google Fonts. "Fontmake" (googlefonts/fontmake) + "ufo2ft 3.0.0 variable features" (2023+). https://github.com/googlefonts/fontmake.
- Nick Sherman. "v-fonts.com — Variable Fonts catalog". https://v-fonts.com/ (377 fonts listed, retrieved 2026-04-17).
- WebKit Bugzilla. "Bug 162783: Implement animation of font-variation-settings". Resolved; shipping since ~2021. https://bugs.webkit.org/show_bug.cgi?id=162783.
- W3C csswg-drafts issue #10952. "`font-named-instance` descriptor inconsistency". 2024.
- W3C csswg-drafts issue #2972. "[css-fonts-4] [varfont] Allow access to named instances outside of @font-face". Open.
- fonttools. varLib, pyftsubset issue tracker. https://github.com/fonttools/fonttools.
- Axis-Praxis / Samsa. avar 2.0 inspector. Laurence Penney, 2024. https://www.axis-praxis.org/samsa/samsa-avar2.html.
- Fencer (first interactive `avar 2.0` editor). Released 2024-05-03.
