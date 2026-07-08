---
date: 2026-04-18
coverage: deep
peers:
  - ../contemporary/variable-fonts.md
  - ../contemporary/metric-overrides.md
  - ./measure.md
  - ./modular-scale.md
  - ./fallback-stacks.md
  - ./pairing.md
  - ../science/optical-size-research.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt  # OT 'size' feature
  - https://www.w3.org/TR/css-fonts-4/  # §8.1 font-optical-sizing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts
  - https://caniuse.com/mdn-css_properties_font-optical-sizing
  - https://fonts.google.com/knowledge/glossary/optical_size_axis
  - https://pixelambacht.nl/2021/optical-size-hidden-superpower/  # Roel Nieskens
  - https://blog.adobe.com/en/publish/2021/03/04/source-serif-gets-optical-sizes  # Frank Grießhammer
  - https://github.com/googlefonts/amstelvar  # Berlow
  - https://github.com/googlefonts/roboto-flex
  - https://github.com/googlefonts/literata
  - https://github.com/adobe-fonts/source-serif
  - https://github.com/undercasetype/Fraunces
  - https://github.com/rsms/inter/discussions/463  # Inter v4 opsz discussion
  - https://v-fonts.com/tags/C36  # v-fonts.com "optical sizes" tag listing
  - https://github.com/google/fonts/issues/5973  # Which GF VFs carry opsz
  - https://www.axis-praxis.org/  # Laurence Penney, axis playground
notes:
  - Font inventory in §6 was spot-checked 2026-04-18 against v-fonts.com, individual Git repos, and Google Fonts. Axis ranges are correct at that date; confirm before citing to a client.
  - Peer ../science/optical-size-research.md is planned (not yet on disk); ./modular-scale.md, ./fallback-stacks.md, ./pairing.md, ../contemporary/variable-fonts.md, ./measure.md are present.
---

# Optical size (opsz) — technique reference

Optical sizing is the practice of designing a typeface so the glyph shapes at each rendered size are tuned to the reader's eye at *that* size, rather than scaled geometrically from a single master. The short form: display cuts have thin serifs, tight spacing, high contrast; caption/footnote cuts have sturdier serifs, looser spacing, lower contrast, larger apertures, and taller x-heights. On a variable font with the registered `opsz` axis, the tuning is continuous rather than stepped, and the browser can drive it automatically from `font-size` via `font-optical-sizing: auto`.

This file covers: the definition and history of optical sizing (punchcutting → phototype regression → Multiple Master → OpenType → variable fonts), the `opsz` axis specifically (units, range semantics, CSS surface, browser behavior), the current font inventory (what ships `opsz` as of 2026-04), how designers use it, distinctions from `font-size` and `font-weight`, and the traps. Variable-font axis mechanics in general live in `../contemporary/variable-fonts.md` and are cross-referenced rather than duplicated.

## Definition

**Optical size** is the property of a type design being tuned for a particular rendered physical size. A 6-point glyph is not a scaled-down 72-point glyph — the stroke contrast, spacing, x-height, aperture, and serif robustness of each size were historically all drawn differently so the reader's perceptual experience would be comparable across sizes. The variable-font era reformulates this as an axis: a single font container holds a continuous spectrum of cuts, and a single coordinate on that axis selects the one appropriate to the rendered size.

Four attributes generally move together along the opsz axis:

- **Stroke contrast** (ratio of thick to thin). High at display sizes; low at small sizes. Hairlines that look elegant at 72pt disappear or fringe at 8pt.
- **Aperture** (openness of letter terminals in `c`, `e`, `s`, `a`). Open at small sizes (so the reader's eye separates the letter from its neighbors); more closed at display sizes (where tight construction reads as elegance).
- **Spacing** (sidebearing and default tracking). Loose at small sizes (to defeat crowding — see `../science/crowding.md`); tight at display sizes.
- **x-height** (relative to cap height). Tall at small sizes (more ink in the reading zone, better stroke discrimination); shorter at display sizes, where the designer can let ascenders and descenders have their full elegance without hurting legibility.

Serifs, terminals, weight, and even construction can shift along the axis. A well-executed opsz family feels like one design at every size; a naively scaled single master feels bloated at large sizes and fragile at small ones.

## History

### Metal type — optical sizing by necessity

In hand punchcutting (15th–19th centuries), every point size of a family was a separate hand-cut punch. A 6-point Garamond cut was not a pantograph reduction of a 12-point cut — the punchcutter thickened strokes, opened counters, widened sidebearings, and often adjusted the skeleton outright for the smaller size. This was not a stylistic option; it was how the technology worked. Each size was therefore inherently optically sized, and every sizeable foundry that sold metal type in the pre-industrial era shipped implicit opsz as a function of having to cut every size separately.

The word "optical" in this context comes from the way punchcutters talked about their craft: adjustments were made so the letters looked right to the eye at the intended size, not so that a geometric scaling was preserved. The apparent contradictions between sizes — why is the 6-point stem proportionally so much heavier than the 72-point stem? — were optical compensations for reader perception, low-contrast inking, ink spread on absorbent paper, and the limits of the human visual system at foveal reading distance.

Pantographic scaling (Benton pantograph, 1884, Wade–Pelouze) mechanized the reduction of a master drawing to multiple sizes. This was faster and cheaper, and drove down the cost of multi-size families. It also began the industrial-scale erosion of optical sizing: a pantographed family might be optically adjusted at only a few master sizes and linearly interpolated for the rest. The empirical optical-sizing tradition survived in foundries that cared, and weakened in those that didn't.

### Phototype and early digital — opsz collapses

Phototypesetting (1950s–1980s) and early PostScript (1984 onward) replaced metal type with a single outline that could be projected or rasterized at any size. Foundries had the economic incentive to ship *one* master per style and scale it uniformly. The consequence, predictable in retrospect: large-size rendering looked bloated and loose (strokes that were correct for 12pt read as too thick at 72pt; sidebearings that were correct for 12pt read as too loose at 72pt), and small-size rendering looked fragile and tight (hairlines that were correct for 12pt vanished at 6pt on coarse paper; sidebearings that were correct for 12pt crowded at 6pt).

This is the era to which complaints about "soulless digital type" track. Tschichold, Zapf, and Slimbach all wrote about the regression. The book-page designers who grew up on metal-set Garamond could tell, even if they couldn't name why: the digital version, scaled uniformly to their body-text size, was both thicker and looser than it should have been.

### PostScript Multiple Master (1991–1999)

Adobe's Multiple Master technology (Adobe Type 1 extension, 1991) was the first format attempt to restore optical sizing as a parametric axis. A Multiple Master font contained two or more axis "masters" — endpoints in a design space — and an interpolation engine that could resolve any intermediate coordinate into a weight-class-1 Type 1 instance. Designers authored families like **Adobe Jenson MM** (Slimbach, 1996), **Adobe Garamond Premier Pro** / predecessor cuts, **Minion Pro** (with opticals), and **Warnock Pro** with opsz as a formally declared axis.

Adobe discontinued MM in 1999 under user-support and application-support pressure (applications had to know what MM was, and most didn't). The fonts themselves did not vanish; Adobe re-released most MM families as static OpenType families with discrete opsz subfamilies — e.g., Minion Pro Caption / Regular / Subhead / Display. The optical design survived; the parametric interface did not.

For almost two decades after MM's withdrawal, opsz was a per-cut affair: **Caption** at ~6–8pt, **Text** or **Regular** at ~9–13pt, **Subhead** at ~14–24pt, **Display** at ~25–72pt, shipped as four (or more) static fonts. Workflows in InDesign and Illustrator could pick the right cut automatically via the OT `size` feature (see §9), but on the web the choice was manual `@font-face` wiring per size bracket.

### OpenType 'size' feature (2000–)

OpenType 1.2 (2000) formalized the `size` feature as a GPOS lookup carrying five `uint16` values: the design size in decipoints (720 units/inch = 1/10 pt), a subfamily identifier, a subfamily string ID, and the inclusive low and exclusive high of the size range for which the cut is appropriate (Microsoft Typography, OT 1.9.1 `features_pt`, retrieved 2026-04-18). The feature let one font in a multi-optical-size family declare "use me between 6pt and 8pt; my cousin file is appropriate between 8pt and 14pt." InDesign and Illustrator honored it. Browsers never did. The `size` feature is a deeply plumbing-level mechanism and its practical effect on web type was near-zero.

### OpenType 1.8 (2016) — Variable Fonts and `opsz` as an axis

OpenType 1.8 (September 2016) introduced Variable Fonts and the registered `opsz` axis tag. Optical sizing returned as a first-class spectrum — a single file, a continuous axis, automatic browser-driven selection from the rendered size — rather than discrete cuts selected manually. This is the current state. See `../contemporary/variable-fonts.md` for the axis mechanics overall; the rest of this file is the opsz-specific story.

## The `opsz` axis

### Units: points, not pixels

The `opsz` axis is one of only a handful of registered axes whose value is a *physical* unit: typographic points, where 1 point = 1/72 inch. Microsoft's axis registration is unambiguous: "Values can be interpreted as text size, in typographic points, as defined in the OpenType specification: a physical unit equal to 1/72 of a standard physical inch" (`dvaraxistag_opsz`, OT 1.9.1, updated 2024-05-29). Typical axis ranges map to real-world type sizes: **8, 14, 24, 72, 144** are all common design sizes along an axis span of **6–144** or a narrower band.

This is *unusual* among variable-font axes. `wght` is a dimensionless number (100–900 the typical range) without physical meaning. `wdth` is a percentage. `slnt` is degrees. `opsz` alone is anchored to a rendered-size unit, because the design intent is *to match the rendered size*. The axis value at which the font is tuned and the rendered size at which it should appear are numerically the same.

### Range semantics

An `opsz` axis value of *N* means: "this glyph is tuned for rendering at *N* points." So an axis range of 8–144 means the font covers design sizes from 8-point text up through 144-point display. The axis is continuous — any value in the declared range is legal — but most fonts are actually designed at a small number of master sizes (commonly 4: caption, text, subhead, display) and interpolated between those masters.

The opsz axis record in `fvar` carries `minValue`, `defaultValue`, `maxValue`. The default is the designer's call and is usually the body-text master size (10–16 is a common range per Microsoft's recommendation in the axis registry). If you query the font's opsz axis and see `min=8 default=14 max=144`, this means: the font is designed to cover 8–144 pt, the "Regular" or default-instance glyph set is tuned for ~14 pt, and you can set `opsz` anywhere in between.

### Automatic browser behavior

`font-optical-sizing: auto` (CSS Fonts Module Level 4 §8.1) is the high-level property. When `auto` and the active font has an `opsz` axis, the browser sets `opsz` equal to the *rendered `font-size` in CSS points*, clamped to the axis `[minValue, maxValue]`. This is the default for variable fonts that declare `opsz`. Authors who do nothing get automatic optical sizing for free.

The CSS-point conversion is specified but implementation-dependent in its details. A rough equivalence: 1 CSS pixel = 0.75 CSS points on default-DPI displays (because CSS was anchored to 96dpi while 1pt = 1/72 inch, so 96/72 = 1.333 px/pt → 0.75 pt/px). Thus `font-size: 16px` → `opsz 12`; `font-size: 48px` → `opsz 36`. At high DPI and with browser zoom, the actual mapping varies per engine (Chrome and Safari differ in whether zoom is reflected into opsz); see §Interaction with zoom below.

### Manual override

Two ways to drive opsz by hand:

```css
/* Manual via font-variation-settings — overrides any font-optical-sizing */
.display-with-body-cut {
  font-size: 72px;
  font-variation-settings: "opsz" 14;  /* force the 14-point cut */
}

/* Manual via font-variation-settings — forces display cut at body size */
.body-with-display-cut {
  font-size: 16px;
  font-variation-settings: "opsz" 72;  /* force the 72-point cut */
}
```

Both are deliberate editorial moves, not mistakes. See §How designers use opsz.

## CSS controls

Three related properties:

```css
/* 1. Auto — the default when the font has opsz */
.auto {
  font-optical-sizing: auto;    /* browser drives opsz from font-size */
}

/* 2. None — disables auto; opsz sticks at the font's default */
.off {
  font-optical-sizing: none;    /* opsz = default-instance value, regardless of font-size */
}

/* 3. Manual — overrides auto */
.manual {
  font-variation-settings: "opsz" 18;   /* pin opsz at 18, irrespective of font-size */
}
```

### The precedence trap

The same precedence rule that bites everywhere in variable-font CSS bites doubly here: **`font-variation-settings` overrides `font-optical-sizing`**, even if `font-variation-settings` is setting a *different* axis.

```css
/* Trap: FVS that sets wght happens to also override font-optical-sizing */
.wrong {
  font-optical-sizing: auto;                    /* intent: auto */
  font-variation-settings: "wght" 500;          /* accidentally pins opsz to default */
}
```

Per CSS Fonts L4 §7.2 and the MDN rule: "Font characteristics set using `font-variation-settings` will always override those set using the corresponding basic font properties." Setting *any* `font-variation-settings` declaration without re-asserting `"opsz"` in the same declaration causes `opsz` to drop to the font's default-instance value, because the entire `font-variation-settings` list is the resolved variation state and any axis not listed takes its default. Fix: list every axis you care about, including opsz, in one FVS declaration; or avoid FVS for registered axes entirely and use the high-level property (`font-weight`, `font-style`, `font-stretch`, `font-optical-sizing`, `font-size`).

```css
/* Correct: use high-level properties for registered axes */
.right-hl {
  font-optical-sizing: auto;
  font-weight: 500;
}

/* Correct: use FVS and include every registered axis you care about */
.right-fvs {
  font-variation-settings:
    "opsz" 18,       /* explicit — otherwise drops to default */
    "wght" 500;
}
```

### Writing opsz into `@font-face`

The opsz axis range is declared in `@font-face` via `font-variation-settings` descriptors or via the explicit properties. Most UAs will read the range from the `fvar` table directly, and no `@font-face` declaration is required. For clarity and to avoid UA surprises:

```css
@font-face {
  font-family: "Fraunces";
  src: url("Fraunces.var.woff2") format("woff2 supports variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  /* opsz range is carried by fvar — no descriptor needed.
     If you want to limit the axis programmatically, slice the font
     with varLib.instancer before hosting. */
}
```

No `opsz-range` descriptor exists in CSS Fonts L4; the range is the font's inherent property.

## Browser support

As of **2026-04-18**:

| Engine / browser | First shipped | Notes |
|---|---|---|
| Chrome (Blink) | 79 | November 2019 |
| Edge (Chromium) | 79 | Ported from Chrome |
| Safari (WebKit) | 13.1 | March 2020 |
| iOS Safari | 13.4 | March 2020 |
| Firefox (Gecko) | 62 | September 2018, but with the bug below |
| Samsung Internet | 12 | March 2020 |

- `font-optical-sizing` is **Baseline** and has been since ~2021 (caniuse `mdn-css_properties_font-optical-sizing`, 2026-04). Global support ~95.6%.
- **Firefox had a known rendering bug** (`Bugzilla 1856035`, filed 2023): variable fonts under `font-optical-sizing: auto` rendered at the *maximum* opsz regardless of font-size. The bug tracked for multiple releases; fixed in Firefox 120 (November 2023) per the canonical fix. Always test Firefox-specific renderings if shipping to audiences on older (pre-120) Firefox — ESR channels lag.
- **All three engines differ** in exactly how they convert `font-size` px to opsz pt under browser zoom and high-DPI. Chromium factors browser zoom into the conversion; Safari historically did not (fixed later); Firefox's conversion was inconsistent pre-120. None of these differences are typically user-visible — the glyph tuning is gentle enough that a ~10% error in opsz position does not produce a clear visual distinction — but when auditing pixel-perfect cross-browser output, this is a real source of subtle drift.
- **Having the property is not having the feature**. `font-optical-sizing: auto` applied to a font without an `opsz` axis is a no-op — the property simply has nothing to drive. Most variable fonts on the web do not carry `opsz`; see §Fonts with opsz axis.

Browser support for **reading** the `opsz` axis via `font-variation-settings: "opsz" N` is the same as variable-font support generally — universal on evergreen engines since ~2019 per caniuse `variable-fonts` (global ~95.9%, 2026-04). If you can use variable fonts at all, you can use `opsz` at all.

## Fonts with `opsz` axis

**Most variable fonts do not ship `opsz`.** The registered axes that overwhelmingly dominate the VF catalog are `wght` and `wdth`; `ital` and `slnt` next; `opsz` is far down. The reason is design-cost: drawing a true opsz range requires separate design masters tuned for each size bracket, and that is labor-intensive. Foundries ship it when the design intent demands it; they omit it when it doesn't.

Spot-checked **2026-04-18** against v-fonts.com, individual Git repos, and Google Fonts:

**Google Fonts / open-source with `opsz`**:

| Font | `opsz` range | Notes |
|---|---|---|
| **Roboto Flex** | 8–144 | 13 total axes; opsz the headline feature. Google Fonts' parametric reference. |
| **Roboto Serif** | 8–144 | Mirrors Roboto Flex on the serif side. |
| **Amstelvar** (Roman + Italic) | 8–144 (default 12) | Berlow's parametric reference font. |
| **Literata** | 7–72 | TypeTogether, commissioned originally for Google Play Books; static cuts tuned at 7, 12, 36, 72. |
| **Source Serif 4** | 8–60 | Adobe-authored, open-source 2021+. Five static cuts (Caption, Small Text, Text, Subhead, Display) map onto the axis. |
| **Fraunces** | 9–144 | Undercase Type; wide aesthetic range. "As opsz decreases, x-height increases, spacing opens, characters widen" (Undercase specimen). |
| **Inter** (Inter 4.0+) | 14–32 | Added in the Inter 4.0 rewrite, 2023 (Hultén; `rsms/inter` discussion #463). Absorbs the previously-separate "Inter Display" family into the axis. Narrower range than the Google Fonts parametric families because Inter is explicitly a screen-UI font. |
| **Nunito** | limited | Nunito variable ships opsz in some axis-range builds but not the baseline; verify at point of use. |
| **Work Sans** | limited | Similar caveat — some builds carry opsz, some don't. |
| **Google Symbols** | — | Carries `wght`, `FILL`, `GRAD`, and `opsz` on icon glyphs (icon optical tuning). Not a text font. |

**Google Fonts / open-source without `opsz`** (common misconceptions):

| Font | Why it lacks opsz |
|---|---|
| **Recursive** | Has `wght`, `slnt`, `MONO`, `CASL`, `CRSV`. No opsz. Recursive's design is explicitly screen-UI; the design team prioritized other axes. |
| **IBM Plex Sans Variable** / **IBM Plex Serif Variable** | Only `wght` on the current open-source releases. |
| **Roboto (classic, not Flex)** | No opsz on the original Roboto variable. |
| **Inter 3.x and earlier** | opsz arrived in Inter 4.0. |
| **DM Serif Display / DM Serif Text** | Two *static* cuts, not a variable font with opsz. Pre-opsz approach (see §Display sub-family). |
| **Playfair Display / Playfair (2.0)** | Playfair 2.0 is variable but ships `wght` and `wdth` only. |

**Commercial**: many foundries ship `opsz`-equipped families. Frere-Jones Type (Retina, Exchange, et al.), Commercial Type (Marr Sans, Publico, Graphik opticals), Grilli Type (GT Flexa opticals), and Typotheque (several) all offer variable or sub-family opticals; KLIM, Dinamo, Displaay similar. Check the per-family specimen: foundries tend to market opsz prominently where it exists.

## How designers use opsz

### 1. Automatically — the default

```css
:root {
  /* Any variable font with opsz behaves correctly with zero effort */
  font-family: "Roboto Flex", sans-serif;
  /* font-optical-sizing: auto is the UA default when the font has opsz */
}
h1 { font-size: 64px; }   /* uses the ~48pt cut */
p  { font-size: 16px; }   /* uses the ~12pt cut */
.caption { font-size: 12px; }  /* uses the ~9pt cut */
```

This is the right default for most work. The axis does what it's designed to do; the reader sees correct-for-size glyphs at every level of the type scale. If the design brief does not have an explicit reason to override, don't.

### 2. Manually — for stylistic reasons

Deliberate mismatches between `font-size` and `opsz` are a legitimate typographic move. Two directions:

**Display size + body-cut opsz** ("chunky big type"):

```css
/* 72-pixel headline rendered with the 14-point cut — thicker strokes,
   slightly opened apertures, heavier feel. Useful when the display cut's
   hairlines feel too delicate for the brand. */
.hero {
  font-size: 72px;
  font-variation-settings: "opsz" 14, "wght" 700;
}
```

**Body size + display-cut opsz** ("editorial fragility"):

```css
/* 18-pixel body rendered with the 72-point cut — thinner strokes,
   tighter spacing, a fragile editorial feel. Useful in art-directed prose.
   Often paired with increased line-height and generous measure. */
.editorial-intro {
  font-size: 18px;
  line-height: 1.7;
  max-width: 55ch;
  font-variation-settings: "opsz" 72;
}
```

Neither is "wrong" — both are within the range the font declares — but each is a deliberate choice that a designer owns. Leaving `font-optical-sizing: auto` is the neutral position; overriding says "I want this specific texture."

### 3. Mapped to role rather than size — type-system discipline

In a mature type system, opsz can be bound to a *semantic role* rather than the literal CSS `font-size`:

```css
:root {
  --font-opsz-caption: 9;
  --font-opsz-body: 14;
  --font-opsz-subhead: 22;
  --font-opsz-display: 72;
}

.role-caption   { font-size: 13px;  font-variation-settings: "opsz" var(--font-opsz-caption); }
.role-body      { font-size: 16px;  font-variation-settings: "opsz" var(--font-opsz-body); }
.role-subhead   { font-size: 22px;  font-variation-settings: "opsz" var(--font-opsz-subhead); }
.role-display   { font-size: 48px;  font-variation-settings: "opsz" var(--font-opsz-display); }
```

This detaches the optical choice from the CSS font-size. A subhead role always reads as "subhead" — correctly weighted and spaced — even if a layout decision nudges its actual size up or down a few pixels. The cost is losing the automatic tracking to user zoom and browser font-size preferences, because opsz is pinned. For UI-chrome contexts this is fine; for prose contexts `font-optical-sizing: auto` is usually better. See §Anti-patterns.

## Distinctions

### opsz is not font-size

Two headlines at the same 48-pixel rendered size can use different `opsz` values (say, 24 vs 72) and look noticeably different. The `opsz 72` version will have thinner serifs, tighter spacing, lower x-height-to-cap ratio; the `opsz 24` will have sturdier serifs, looser spacing, higher x-height. `font-size` is geometric; `opsz` is tonal. The two axes are orthogonal.

### opsz is not weight

Stroke darkness is the `wght` axis. Opsz changes contrast between thick and thin strokes (the ratio), not overall darkness (the absolute). An `opsz 8` cut is lower-contrast than `opsz 72`: its hairlines are thicker *relative to* its stems, but both stems and hairlines may be similar in absolute terms. Going `opsz 72 → 8` is not "going bolder"; it is "evening out the contrast." Stepping up `wght 400 → 700` at a fixed `opsz` is genuinely "going bolder."

In practice the two axes interact. Most fonts' `opsz 8` master has both lower contrast and fractionally heavier absolute stems than the `opsz 72` master at the same `wght` setting, because small-size legibility needs both effects. But the effects are logically separable and separately designed.

### opsz is not spacing

Tracking is `letter-spacing` in CSS. Opsz adjusts the designer's *default* sidebearings and kerning for the target size; it does not expose a knob for the reader or author to set. The correct way to think about it: the designer is moving the baseline from which `letter-spacing` adds or subtracts. Authors may still want to add explicit `letter-spacing` for all-caps runs, small-cap runs, or tight display work, and that stacks on top of the opsz-determined defaults.

## Interaction with zoom and media queries

`font-optical-sizing: auto` has one load-bearing virtue: it tracks the *computed* `font-size` at render time, not the authored one. This means:

- **User font-size preferences** (e.g., the accessibility setting that multiplies default text by 150%) change `font-size` on every element and therefore change `opsz` correspondingly, without any media-query logic.
- **Browser zoom** likewise changes computed `font-size` and therefore `opsz` — in engines that factor zoom (Chromium does; WebKit's historical quirk discussed above).
- **Container-query-driven font sizing** works the same way. A paragraph whose font-size is computed via `cqi` picks up a correspondingly computed opsz as the container grows or shrinks.
- **Viewport resize** is handled. No JavaScript listener, no media query, no breakpoint — the opsz tracks.

This is why `auto` is usually correct for prose. Any resize, any zoom, any accessibility override — opsz follows.

The wrinkle: **Chromium, WebKit, and Gecko convert `font-size` px to `opsz` pt differently.** As of 2026-04, the differences are small (single-digit percent in most cases), but present. Generally invisible to the reader; occasionally visible in cross-browser screenshot diffs when a design team is counting hairlines. If pixel-identical cross-browser output matters, pin opsz with `font-variation-settings` for the spans where it matters; for everything else, `auto` is the right call.

## Related pre-variable-font OpenType mechanisms

### The `size` feature

OpenType defined a GPOS feature `size` (OT 1.2, 2000) carrying five `uint16` values that declare an individual static font's design size (in decipoints = 1/720 inch) and its recommended usage range (inclusive-low to exclusive-high in decipoints). The registry positions: caption (6–8pt), regular (9–13pt), subhead (14–24pt), display (25–72pt). InDesign and Illustrator select the right cut from an optical family automatically via this feature; web browsers never implemented auto-selection. The feature is effectively legacy — supplanted by the variable-font `opsz` axis — but the four-bucket size classification it encodes (caption, regular, subhead, display) still shows up in the naming and master-selection of static optical families (e.g., Minion Pro Caption / Regular / Subhead / Display, Source Serif 4 Caption / Small Text / Text / Subhead / Display).

### Proposed `@font-face font-size` descriptor

Various W3C drafts over the years proposed an `@font-face` descriptor to declare the size at which a static font was designed, letting browsers auto-select among a group of static fonts — essentially bringing the OT `size` feature to CSS. The proposal never shipped; variable fonts with `opsz` subsumed the use case.

## Related mechanisms that are not opsz

- **`font-size-adjust`** (CSS Fonts L4 §5) normalizes the x-height across fonts so a fallback has the same apparent size as the primary. Independent of opsz.
- **`size-adjust`** (`@font-face` descriptor) scales the entire em-box of a face. Independent of opsz.
- **`ascent-override`, `descent-override`, `line-gap-override`** (`@font-face` descriptors) override the vertical metrics used for line-box calculation. Independent of opsz.
- **`font-stretch` / `font-width`** drives the `wdth` axis (horizontal scaling of proportions). Independent of opsz.

opsz can coexist with any of these. A common stack: a primary variable font with opsz; a fallback with `size-adjust` and `ascent-override` tuned to match the primary's metrics (see `../contemporary/metric-overrides.md` and `./fallback-stacks.md`). The fallback does not need opsz itself — its job is only to hold the reader's space visually while the primary loads.

## Reading science — evidence for opsz benefits

The empirical case for opsz at small sizes is strong and old. Key findings relevant to web use:

- **Small-size legibility benefits from open apertures, low stroke contrast, and loose spacing.** Bernard et al. (2001, *Usability News* 3.2) measured reading speed and preference for different fonts at 10-point and 12-point screen sizes; fonts with opened apertures and lower contrast (e.g., Verdana's proportions, though not yet a VF) outscored more-traditional serif faces set at the same size. Chaparro et al. (2010, *Ergonomics*) extended this to sub-10-point sizes with similar findings.
- **Sofie Beier's *Reading Letters: Designing for Legibility* (BIS Publishers, 2012, rev. 2022)** is the consolidated practitioner reference; Beier's empirical work directly informs design decisions for small-size cuts. The recurring findings: aperture openness is a first-class legibility predictor at small sizes; crowding (Pelli-style) is a first-class inhibitor; x-height-to-cap ratio modulates both; contrast matters less than these three.
- **At display sizes (>36pt)**, thinner strokes and tighter spacing are aesthetically preferred without meaningful legibility cost. Legge & Bigelow (2011, *J. Vision*) did not find significant reading-speed differences between a well-designed display cut and its body cut at equal display size; the display cut is simply visually nicer.
- **Ink traps and bridges**, long a punchcutter's trick for tiny sizes (carving notches into a letter's joins so ink spread doesn't close the counter), are making a comeback in small-size opsz masters for high-density screens. Inter 4.0's 14-point master uses them explicitly (rsms `Inter 4.0` release notes, 2023).

The short form: opsz automates optical tuning type designers have known to do empirically for 500 years, and the reading-science literature broadly confirms the intuitions. See `../science/optical-size-research.md` (planned) for the citations in full.

## Anti-patterns

| Pattern | Why it's wrong | Fix |
|---|---|---|
| `font-optical-sizing: none` on `html` or `body` "for consistency" | Disables the axis globally. The font has carefully-tuned masters that now never render. | Allow opsz to work; override locally only when there's a specific reason. |
| Forcing one opsz across all sizes via `font-variation-settings: "opsz" 14` at `:root` | The same effect as `none`, slightly worse because it pretends to be deliberate. Headline and body both render at the same cut — display cut's elegance is lost, or body cut's robustness is lost. | Use `font-optical-sizing: auto`; override per-component, not globally. |
| Setting `font-variation-settings` for a different axis and forgetting to list `"opsz"` | Every registered axis not listed in FVS drops to its font-default, including opsz. Quiet loss of the axis. | Include every axis you care about in one FVS list, *or* use high-level properties (`font-weight`, `font-optical-sizing`, `font-style`, `font-stretch`, `font-size`). |
| Pairing a font with `opsz` against a font without `opsz` at large display sizes | The non-opsz font will render at its only master (typically text-sized); next to a properly-display-tuned opsz font at 72pt, it will look clumsy — strokes too thick, apertures too open, x-height too tall. | Pair fonts that either both carry opsz or neither carry opsz. If pairing across opsz asymmetry, pin the non-opsz font to its hero role and keep the opsz font at body. See `./pairing.md`. |
| Pinning opsz to the display value in a hero block that inherits to body paragraphs | `font-variation-settings` inherits through the cascade. A pinned display-opsz set on a `.hero` container propagates down to any `<p>` inside it. | Scope FVS to the element that actually needs it; reset opsz on child body paragraphs with `font-optical-sizing: auto` (caveat: FVS still wins, so set FVS explicitly on the child too). |
| Using opsz to fake a bolder weight | opsz changes contrast and spacing, not overall darkness. Reaching for opsz 8 to make display text feel heavier is a misuse — it also makes it wider and more-awkwardly-spaced. | Use `wght`. If both are wanted, combine them deliberately. |
| Relying on opsz to compensate for bad font-size choices | An 8-pixel body text is too small regardless of opsz. opsz 8 improves legibility *at* 8pt; it does not make 8pt a good choice for body copy on screen. | Set body text to a comfortable reading size first (14–16px); let opsz refine it. |
| Assuming a variable font has opsz because it's "modern" | Most don't. Check `fvar` via Wakamai Fondue, Axis-Praxis, or `fc-scan` before wiring a design that depends on it. | Verify the axis list. Plan for the font's actual axes; don't design to a feature it lacks. |
| Designing around a specific Firefox pre-120 opsz rendering | Pre-Firefox-120 rendering of `font-optical-sizing: auto` on variable fonts had a bug causing max-opsz always (Bugzilla 1856035); output looked "wrong" in that engine. Designing the visual to *match* the bug causes regressions when the user upgrades. | Design to the spec, not to the bug. Test on a current Firefox. Users on bugged versions are a shrinking minority by 2026-04. |
| Putting the opsz override in `font-variation-settings` on a pseudo-element where `font-size` differs from the parent | The pseudo's opsz is computed against its own `font-size`, but if you pin via FVS you're asserting a value unrelated to that. Visually strange. | Either inherit opsz and let auto do its work, or pin the pseudo's opsz to a value chosen for the pseudo's size specifically. |

## Display sub-family vs variable opsz

Many foundries still ship an optical family as **discrete static cuts** — e.g., DM Serif Display vs DM Serif Text, Playfair Display vs Playfair Text, Libre Caslon Display vs Libre Caslon Text — rather than a variable font with `opsz`. This is the pre-variable approach, and it is still valid:

- **Explicit control**: a designer chooses Display at any size they want, not at a size the axis predicts. The same glyph set can be rendered at 14pt (quite unusual but a deliberate choice) without first fighting `font-optical-sizing: auto`.
- **Discrete-tuning intent**: type designers often intend the masters as *specific points*, not as interpolated spectrums. A variable opsz axis gives the user the continuous interpolation between the designed masters; the interpolated middles may not be what the designer would have drawn if they'd been asked for that particular size.
- **Tooling compatibility**: legacy tools that don't support VFs still get a correctly-tuned family via the static cuts.
- **Performance at the extremes**: shipping only Text (if that's all the site needs) is a single small file; shipping a VF with a full opsz range is larger even if only the Regular master is ever used.

Variable `opsz` and discrete opticals are not mutually exclusive. Foundries often ship both: a variable font for continuous tuning, plus discrete static instances matching the variable masters for legacy pipelines. Web authors typically pick one layer and use it consistently.

## When to skip opsz

opsz is not always worth the effort. Cases where the feature adds little:

- **UI at fixed sizes 13–16px**. The opsz-axis movement within a narrow-band (10–18pt) is subtle enough that readers don't perceive the difference across component scale steps. The axis adds kilobytes to no effect.
- **Brand systems that want one "voice" across sizes**. If the brief calls for a single consistent texture at all sizes — a design choice with its own integrity — opsz is wrong for it. Pick a font without opsz, or `font-optical-sizing: none` and document the choice.
- **Performance-constrained delivery**. opsz adds variation-table deltas per master. For a variable font that spans opsz 8–144 with five masters, this is on the order of tens of kilobytes beyond a no-opsz VF. Usually negligible relative to total font weight (the primary driver is language coverage), but in aggressively subset delivery (display-only Latin Extended) it matters. Instancing — `fonttools varLib.instancer` — can freeze opsz to a single value and strip the axis entirely for delivery if the target doesn't need it.
- **Monospace typewriter-style fonts** — the design tradition is for a single master regardless of size. opsz on monospace is rare (Recursive's `MONO` axis does not carry opsz).
- **Single-size specimens** — an icon font or a logo-only font only ever renders at one size; opsz is theater.

## Testing and verification

### Inspecting a font's opsz axis

Tools as of 2026-04:

- **Wakamai Fondue** (`wakamaifondue.com`). Drag-drop a font file; reads `fvar` and reports axis tags, min/default/max, and named instances. Fast, browser-only. Jason Pamental maintains.
- **Axis-Praxis** (`axis-praxis.org`, Laurence Penney). Interactive playground for every axis in a font, including opsz. Useful for visually confirming "does opsz do what I think it does at 8pt vs 72pt?"
- **v-fonts.com** (Nick Sherman). Catalog of known variable fonts with searchable axis tags; filter by `opsz` to get the full listing.
- **`fc-scan` / `otfinfo`** (fontconfig / LCDF typetools). Command-line inspection. `otfinfo -f file.woff2` lists features; `fc-scan --format '%{variable}\n%{axis_ranges}\n' file.ttf` lists axis ranges.
- **fontTools `ttx`**. Decompile to XML; inspect the `fvar` table directly. Verbose but definitive.

### Confirming the browser is driving opsz

Dev tools alone don't expose the resolved opsz value per element. To verify:

```css
.debug-opsz {
  /* Apply at a series of different font-sizes; visually check the
     glyph rendering against Axis-Praxis's preview of the same font
     at the corresponding opsz values. */
  font-size: var(--test-size);
  font-optical-sizing: auto;
}
```

Or pin opsz to known values and compare against the auto version:

```css
.opsz-14-pinned { font-variation-settings: "opsz" 14; font-size: 14px; }
.opsz-14-auto   { font-optical-sizing: auto; font-size: 14px; /* should resolve to opsz ~10.5 */ }
```

The difference at small font-sizes will be subtle — heavier stems, slightly wider sidebearings, slightly larger x-height on the auto-resolved low-opsz cut. At display sizes the difference is more obvious.

### Cross-browser

Test on Chrome, Firefox ≥120, and Safari at a minimum. For pre-Firefox-120 ESR audiences, accept the rendering bug or disable opsz via `font-optical-sizing: none` for that target. Use the `@supports` query to detect:

```css
@supports (font-optical-sizing: auto) {
  /* Most UAs; rely on auto. */
}
@supports not (font-optical-sizing: auto) {
  /* Rare fallback. */
}
```

Note: this `@supports` check confirms the *property* is recognized. It does **not** confirm the UA correctly applies it to a font with `opsz`. The Firefox pre-120 bug passed the `@supports` check while misrendering.

## Sources

(Retrieval dates: all 2026-04-18.)

- **Microsoft Learn.** "`opsz` — design-variation axis tag (OpenType 1.9.1)." Updated 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz
- **Microsoft Learn.** "Registered features, p-t — 'size' feature (OpenType 1.9.1)." Updated 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt
- **Microsoft Learn.** "OpenType Design-Variation Axis Tag Registry (OpenType 1.9.1)." Updated 2024-05-29. https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg
- **W3C.** "CSS Fonts Module Level 4 — §8.1 Low-level font variation settings: the `font-optical-sizing` property." Working Draft 2026-03-03. https://www.w3.org/TR/css-fonts-4/
- **MDN Web Docs.** "`font-optical-sizing`." Mozilla Contributors. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing
- **MDN Web Docs.** "Variable fonts guide." Mozilla Contributors. https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts
- **caniuse.com.** "`font-optical-sizing`." 2026-04. https://caniuse.com/mdn-css_properties_font-optical-sizing
- **Roel Nieskens (Pixelambacht).** "Optical size, the hidden superpower of variable fonts." 2021-03-04. https://pixelambacht.nl/2021/optical-size-hidden-superpower/
- **Frank Grießhammer (Adobe).** "Source Serif gets optical sizes." Adobe Blog, 2021-03-04. https://blog.adobe.com/en/publish/2021/03/04/source-serif-gets-optical-sizes
- **Google Fonts Knowledge.** "Optical Size axis (opsz)." https://fonts.google.com/knowledge/glossary/optical_size_axis
- **David Berlow / TypeNetwork.** Amstelvar repository. https://github.com/googlefonts/amstelvar
- **Google Fonts.** Roboto Flex repository. https://github.com/googlefonts/roboto-flex
- **TypeTogether.** Literata repository (googlefonts/literata). https://github.com/googlefonts/literata
- **Adobe Originals.** Source Serif repository. https://github.com/adobe-fonts/source-serif
- **Undercase Type.** Fraunces repository. https://github.com/undercasetype/Fraunces
- **Rasmus Andersson.** Inter repository; v4 discussion #463 (opsz integration). https://github.com/rsms/inter/discussions/463
- **Nick Sherman (v-fonts.com).** "Optical sizes" tag listing. https://v-fonts.com/tags/C36
- **Laurence Penney.** Axis-Praxis variable-font playground. https://www.axis-praxis.org/
- **Mozilla Bugzilla 1856035.** "Variable fonts render in maximum optical size regardless of opsz axis value." Filed 2023; fixed in Firefox 120. https://bugzilla.mozilla.org/show_bug.cgi?id=1856035
- **Bernard, M., Liao, C. H., & Mills, M. (2001).** "The effects of font type and size on the legibility and reading time of online text by older adults." *Usability News* 3.2.
- **Chaparro, B., Shaikh, D., Chaparro, A. (2010).** "Keeping up with content on the web: Font size and reading comfort." *Ergonomics*.
- **Beier, S. (2012, rev. 2022).** *Reading Letters: Designing for Legibility.* BIS Publishers. https://www.bispublishers.com/reading-letters-revised.html
- **Legge, G. E., & Bigelow, C. A. (2011).** "Does print size matter for reading? A review of findings from vision science and typography." *Journal of Vision* 11(5):8. https://doi.org/10.1167/11.5.8
- **Adobe.** Multiple Master announcement, 1991. (Historical reference; primary sources limited to Adobe archived press.)
- **Google Fonts / Issue 5973.** "Which variable fonts include an Optical Size (opsz) axis?" https://github.com/google/fonts/issues/5973
