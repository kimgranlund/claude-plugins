---
date: 2026-04-18
coverage: medium
peers:
  - ./font-palette.md
  - ./variable-fonts.md
  - ./opentype-features.md
  - ./hinting-and-rendering.md
  - ./font-delivery.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/colr
  - https://learn.microsoft.com/en-us/typography/opentype/spec/cpal
  - https://learn.microsoft.com/en-us/typography/opentype/spec/cbdt
  - https://learn.microsoft.com/en-us/typography/opentype/spec/sbix
  - https://learn.microsoft.com/en-us/typography/opentype/spec/svg
  - https://www.w3.org/TR/css-fonts-4/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-palette-values
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-palette
  - https://developer.chrome.com/blog/colrv1-fonts
  - https://chromestatus.com/feature/5089401438175232
  - https://bugs.webkit.org/show_bug.cgi?id=241691
  - https://caniuse.com/colr
  - https://caniuse.com/colr-v1
  - https://caniuse.com/css-font-palette
  - https://caniuse.com/css-font-palette-values
  - https://fonts.google.com/noto/specimen/Noto+Color+Emoji
  - https://github.com/googlefonts/noto-emoji
  - https://developer.apple.com/fonts/
  - https://www.colophon-foundry.org/
  - https://emojipedia.org/
---

# Color fonts — contemporary reference

**Coverage tier**: medium
**Last verified**: 2026-04-18
**Sources**: Microsoft OpenType spec (COLR, CPAL, CBDT/CBLC, sbix, SVG), W3C CSS Fonts Module Level 4, MDN (`@font-palette-values`, `font-palette`, color-font formats), caniuse (`color-font-format-colr`, `colr-v1`, `css-font-palette`), Chrome Status feature entries, WebKit Bugzilla COLRv1 tracker, Safari release notes (25.x / 26.x), Google Fonts Noto Emoji project, Colophon Foundry, Emojipedia timeline, Adobe SVG-in-OT proposal archive.
**Peer files**: [./font-palette.md, ./variable-fonts.md, ./opentype-features.md, ./hinting-and-rendering.md, ./font-delivery.md]

<orientation>
This file covers the *color-glyph surface* of OpenType: the four formats that encode colored or multi-channel glyph data inside an SFNT container (COLRv0, COLRv1, sbix, CBDT/CBLC, SVG-in-OT), the CSS controls that select among palettes or interact with color-font rendering, the browser support matrix as of April 2026, and the use cases where color fonts earn their weight (emoji, icon fonts, multicolor wordmarks, display type).

What this file does **not** cover:
- The `font-palette` CSS property and `@font-palette-values` at-rule in depth — see `./font-palette.md`.
- Variable-font axis mechanics or COLRv1 × variable-font animation internals — see `./variable-fonts.md` §Color Fonts + Variable Axes.
- OpenType feature tags unrelated to color (kerning, ligatures, stylistic sets) — see `./opentype-features.md`.
- Rasterization pipelines and platform rendering — see `./hinting-and-rendering.md`.

All dated claims are scoped to stable releases as of **April 2026**. "Baseline" uses the Web Platform DX Community Group definition.
</orientation>

---

## TL;DR — what matters in 2026

1. **Four coexisting formats in the wild**: COLRv0 (2013, layered flat colors), COLRv1 (2020, gradients + transforms + composition), sbix (Apple PNG bitmaps), CBDT/CBLC (Google bitmaps, largely legacy), SVG-in-OpenType (Adobe/Mozilla, near-dead). All ride inside the same SFNT container as monochrome outline tables.
2. **COLRv1 is the new-work default for Chromium + Firefox.** Chrome 98+ (Feb 2022), Edge 98+, Firefox 107+ (Nov 2022). **Safari has not shipped COLRv1** as of Safari 26.5 (2026-04) per caniuse. COLRv1 fonts on Safari fall back to monochrome `.notdef` outlines or the font's COLRv0 layer if present.
3. **COLRv0 is universally supported.** Every major browser since ~2016–2019. Safe for flat, palette-driven emoji and icon fonts where gradients aren't required.
4. **sbix is Apple's path.** Apple Color Emoji on macOS/iOS ships sbix. Other browsers *can* render sbix when present, but it's rare outside the Apple ecosystem.
5. **SVG-in-OT is effectively dead for new work.** Chrome never shipped, Firefox/legacy Edge have it, Safari has partial. Superseded by COLRv1's gradients and compositing.
6. **The CSS surface is `font-palette` + `@font-palette-values`.** Baseline since 2022. Select among palettes declared in the font, or override specific color indices. Details in `./font-palette.md`.
7. **Accessibility still matters.** WCAG 1.4.1 applies: don't encode meaning in color-font color alone. Contrast rules still apply to colored text against its background.
8. **`font-variant-emoji` is the orthogonal control for presentation**, not color — it chooses between text-presentation and emoji-presentation for characters that support both. See `./opentype-features.md`.

---

## History and motivation

### Pre-2013 — bitmap and external-asset era

Before OpenType gained first-class color-glyph tables, colored letterforms and emoji lived outside the font container:

- **Apple SBIX** (introduced 2013-ish in iOS/macOS, before formal OT standardization) — PNG bitmaps per size. Apple's internal format for Color Emoji, eventually formalized in OpenType.
- **Google CBDT/CBLC** (Android, ~2013) — Compressed Bitmap Data / Compressed Bitmap Location Tables. Google's parallel path for Android emoji before COLR existed.
- **External assets** — Twemoji (Twitter's open-source emoji set) initially shipped as SVG/PNG sprite sheets; browsers rendered emoji codepoints by mapping them to `<img>` or background images, not font glyphs.

Motivation: Unicode 6.0 (October 2010) formalized ~722 emoji, and platforms needed to render them as images, not line drawings. Monochrome OpenType couldn't express the multi-colored glyph data; the vendor tables that emerged were platform-specific stopgaps.

### 2013–2016 — convergence attempts

- **Microsoft proposes COLR/CPAL** (2013, shipping in Windows 8.1 with Segoe UI Emoji): a layered model where a glyph is composed of multiple monochrome sublayers, each drawn in a palette color. Compact (reuses existing `glyf` outlines); no gradients; simple enough for the Windows rasterizer to handle cheaply.
- **Apple refines sbix** for iOS 7 / macOS Mavericks Color Emoji; codifies it in OpenType 1.7 (2014).
- **Adobe and Mozilla propose SVG-in-OpenType** (2013 Adobe draft; Mozilla implements in Firefox 26, 2013-12): full SVG per glyph, maximum expressivity, minimum consensus.
- **Google ships CBDT/CBLC** in Android for Noto Color Emoji and extends Chromium to render it.

Four formats, four vendors, four motivations. OpenType 1.8 (September 2016) codified all four formally as optional color-glyph tables inside the SFNT container.

### 2020+ — COLRv1 unification push

**COLRv1** is a Google-led effort (Dominik Röttsches at Google, with Adobe + Microsoft collaboration) extending COLR to support:

- Linear, radial, and sweep gradients.
- Affine and perspective transforms applied per-layer.
- Porter-Duff composite and blend modes (29 modes from `Clear` to `HSL_Luminosity`).
- Variable-font integration: color-stop positions, gradient angles, and transform parameters can be animated via `font-variation-settings` (see `./variable-fonts.md`).

COLRv1 was drafted 2020, ratified in OpenType 1.9 (December 2021), and shipped in Chrome 98 (February 2022). Firefox followed in 107 (November 2022). Safari has not shipped COLRv1 as of 2026-04. By 2024, most new emoji fonts ship COLRv1 as primary; most include a COLRv0 fallback layer specifically to cover Safari.

### 2024–2026 — animation and authoring maturity

- **Noto Color Emoji** migrated to COLRv1 in 2023. The 2024 Noto release includes variable-font axes on some emoji glyphs (experimental).
- **Colophon Color Emoji** (2024) — COLRv1 with animation-friendly axes.
- **Material Symbols** (Google) ships an optional COLRv1 variant with brand-palette support.
- **Glyphs 3 + FontLab 8** ship mature COLRv1 authoring workflows (2023+).

---

## The four (five) color-font formats

All five live as optional tables inside the SFNT container. A font can ship multiple simultaneously; the rasterizer picks the highest-priority format it understands at render time. Browser priority order in 2026-04 is roughly: COLRv1 > COLRv0 > SVG-in-OT > sbix > CBDT/CBLC > monochrome fallback.

### COLRv0 / CPAL (Microsoft 2013)

**Mechanism**: each colored glyph is a *base glyph* plus an ordered list of *layer glyphs*, each drawn in a palette color. Layers are flat fills — no gradients, no transforms, no compositing beyond simple alpha over.

**Tables**:
- **`COLR` (v0)** — base glyph ID → list of (layer glyph ID, palette index) pairs.
- **`CPAL`** — palette table: one or more palettes, each an array of sRGB colors indexed by the layer records.

**Strengths**:
- Compact. Layer glyphs reuse the existing `glyf` or CFF outline space.
- Universal browser support since ~2016–2019.
- Palette-driven: one font, multiple palettes (light/dark, brand variants) selectable via CSS `font-palette`.
- No rendering novelty required — the rasterizer already knows how to rasterize `glyf` outlines; it just does so N times and composites.

**Limitations**:
- No gradients. A glyph with a smooth color transition must approximate it with discrete color bands.
- No per-layer transforms. A rotated sublayer requires a separate glyph outline.
- No blend modes beyond source-over alpha.

**Where it's used**: Segoe UI Emoji (Windows 8.1+), early Noto Color Emoji COLR builds, many COLRv0 icon fonts from 2016–2022.

### COLRv1 (Google/Adobe/Microsoft 2020, OpenType 1.9 2021)

**Mechanism**: extends COLRv0's layer model with a full *paint tree* per glyph. Each paint node is one of ~16 paint types — flat color, linear/radial/sweep gradient, affine/perspective transform, composite, blend, clip, rotation, translation, skew, etc. The paint tree is a directed acyclic graph; nodes can be reused across glyphs to keep file size down.

**Tables**:
- **`COLR` (v1)** — base glyph ID → paint tree root + paint records.
- **`CPAL`** — same palette structure as v0; gradients reference palette indices for color stops.
- Optional integration with **`avar`**, **`fvar`**, and the Item Variation Store, enabling color-stop positions and gradient parameters to vary along font axes (see `./variable-fonts.md`).

**Paint node types** (summary, not exhaustive):

| Paint format | What it does |
|---|---|
| `PaintSolid` | Flat color from palette. |
| `PaintLinearGradient` | Linear gradient with `ColorStopList`. |
| `PaintRadialGradient` | Radial gradient with start/end circles + color stops. |
| `PaintSweepGradient` | Sweep (conic) gradient. |
| `PaintGlyph` | Clip paint to a specified glyph outline. |
| `PaintColrLayers` | Ordered layer list (COLRv0-style). |
| `PaintTransform` | Affine transform (2×3 matrix). |
| `PaintTranslate` / `PaintRotate` / `PaintScale` / `PaintSkew` | Specialized transforms; smaller to encode than a full affine matrix. |
| `PaintComposite` | Porter-Duff or blend-mode composition of two sub-paints. |
| `PaintColrGlyph` | Reference to another COLR glyph's paint tree (reuse). |

**Strengths**:
- Full gradient and compositing expressivity. Modern emoji with skin-tone gradients, multi-stop glows, or shadowed depth all fit naturally.
- Variable-font-compatible. A single COLRv1 font can animate `wght` and see both the outline *and* its color stops interpolate.
- Compact relative to equivalent SVG-in-OT (paint trees reuse nodes; no XML overhead).
- Widely deployed since 2023.

**Limitations**:
- Rasterizer complexity is much higher than COLRv0. Implementation bugs still surface (HarfBuzz + FreeType + Skia + platform compositor all need to agree).
- Safari is the holdout: COLRv1 remains unshipped through Safari 26.5 (2026-04). Safari users fall back to monochrome or COLRv0 layer.
- Authoring tools matured later than the format. Full COLRv1 paint-tree control in Glyphs 3 landed ~2022; FontLab 8 in 2023.

**Where it's used**: Noto Color Emoji (2023+), Twemoji Mozilla, Segoe UI Emoji (Windows 11 22H2 update 2023), Apple Color Emoji *does not* use COLRv1 — still sbix as of 2026-04 — many new emoji fonts, Material Symbols COLRv1 variant, Colophon Color Emoji, Phosphor Color, GT Color, Sharp Type color families.

### sbix (Apple, formalized OpenType 2014)

**Mechanism**: per-glyph bitmap strikes at multiple sizes. The `sbix` table stores PNG (or JPEG, or PDF) bitmaps keyed by glyph ID × strike size. The rasterizer at render time picks the closest strike size and blits.

**Tables**:
- **`sbix`** — strike records, each a list of (glyph ID, bitmap bytes, offset) entries.

**Strengths**:
- Pixel-perfect control. The designer paints each glyph as a raster image; the rasterizer does no reinterpretation.
- Appropriate for pixel-art or texture-heavy emoji where vector approximations would lose character (Apple's skin-tone gradients, specular highlights).
- Supported universally for reading when shipped — Safari, Firefox, Chrome all read sbix for Apple Color Emoji on macOS/iOS.

**Limitations**:
- **Fails to scale without blur.** Bitmap blit at non-integer ratios produces blurred output; up-scaling beyond the largest authored strike is especially ugly.
- **File size balloons.** A full-coverage sbix font with strikes at 20, 32, 40, 48, 64, 96, 128, 160 px × 3,600+ emoji is tens of megabytes. Apple Color Emoji's .ttc is ~200 MB on macOS.
- **No variable-font integration.** sbix bitmaps don't respond to font axes; a variable font with an sbix table is a rare and confusing beast.
- **Authoring is image production, not font design.** Requires a separate raster pipeline.

**Where it's used**: Apple Color Emoji (macOS, iOS, iPadOS, tvOS, visionOS, watchOS) — the single most widely-seen sbix font in existence. Almost no third-party sbix fonts ship for the web.

### CBDT / CBLC (Google, OpenType 2013)

**Mechanism**: analogous to sbix, but with separate tables for bitmap data (`CBDT`) and bitmap location (`CBLC`) — a pattern inherited from older `EBDT`/`EBLC` monochrome bitmap tables.

**Tables**:
- **`CBDT`** — Color Bitmap Data. PNG-encoded strikes.
- **`CBLC`** — Color Bitmap Location. Index into `CBDT`.

**Strengths**:
- Same pixel-perfect control as sbix; Android's original emoji path.
- Smaller than sbix for equivalent coverage due to more compact indexing.

**Limitations**:
- Effectively legacy as of 2026. Google's Noto Color Emoji migrated to COLRv1 in 2023; CBDT builds remain for Android compatibility with older Skia rasterizers but are no longer the primary format.
- Safari never shipped CBDT/CBLC rendering.
- Same scale/size concerns as sbix.

**Where it's used**: Noto Color Emoji legacy builds, some Android system fonts, a shrinking set of third-party Android emoji fonts. For new work, COLRv1 supersedes.

### SVG-in-OpenType (Adobe/Mozilla, OpenType 2013)

**Mechanism**: per-glyph SVG fragments embedded inside the `SVG ` table (note the trailing space — required by OpenType's 4-byte table-tag requirement). Full SVG 1.1 feature set (gradients, filters, clipPath, masks, patterns, SMIL animation).

**Tables**:
- **`SVG `** (with trailing space) — glyph ID → SVG document fragment (can be raw or gzipped).

**Strengths**:
- Maximum expressivity. Any SVG 1.1 feature is available per glyph.
- Existing SVG tooling (Inkscape, Illustrator, Figma) can author glyphs; font-production tools link them into the `SVG ` table.

**Limitations**:
- **Largest file sizes of any color-font format.** XML overhead, no paint-tree reuse.
- **Uneven browser support.** Chrome/Chromium **never shipped** SVG-in-OT rendering (cited security surface and implementation complexity; declared WONTFIX in 2018). Firefox shipped since 26 (2013-12). Safari shipped partial support since 11 (2017), with some SVG features omitted.
- **Effectively superseded by COLRv1** for most use cases. Gradients, transforms, and composition are now available in COLRv1 with better browser coverage.
- **SMIL animation inside glyphs is theoretically supported but never rendered reliably cross-platform**; CSS/JS-driven animation via COLRv1 + `font-variation-settings` is the modern path.

**Where it's used**: some legacy multicolor display fonts (Trajan Color Concept from 2012 ships SVG-in-OT), a handful of commercial color fonts from 2015–2020. For new work in 2026: avoid.

### Format decision matrix

| Goal | Recommended format | Avoid |
|---|---|---|
| New emoji font (2026) | COLRv1 (primary) + COLRv0 fallback | SVG-in-OT, CBDT-only |
| Icon font with color | COLRv1 | SVG-in-OT |
| Multicolor display type | COLRv1 | SVG-in-OT |
| Pixel-art emoji | sbix | COLRv1 (gradients can't reproduce pixel grid cleanly) |
| Safari coverage + legacy-targeting emoji | COLRv1 + COLRv0 fallback layer (Safari falls back to COLRv0) | COLRv1-only |
| Brand-palette-variant logo font | COLRv0 (if flat) or COLRv1 + CPAL + `font-palette` | SVG-in-OT (inflexible per-glyph bakes) |

---

## Browser support matrix (verified 2026-04)

Dates are from caniuse (`colr`, `colr-v1`, `css-font-palette`, `css-font-palette-values`), Chrome Status feature entries, WebKit release notes, and Mozilla release notes.

### COLRv0 / CPAL

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | 41 | 2015-03 | Universal since. |
| Firefox (Gecko) | 26 | 2013-12 | Original COLR implementation. |
| Safari (WebKit) | 11 | 2017-09 | macOS + iOS simultaneous. |
| Edge (legacy, pre-Chromium) | 12 | 2015-07 | Replaced by Chromium Edge 2020. |
| Edge (Chromium) | 79 | 2020-01 | Inherits from Blink. |
| Android Chrome | 41 | 2015-03 | Via Skia/FreeType. |
| iOS Safari | 11 | 2017-09 | CoreText. |

**Global availability**: ~99% as of 2026-04. Safe for any production use.

### COLRv1

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | 98 | 2022-02 | Dominik Röttsches. Chrome Status feature 5089401438175232. |
| Firefox (Gecko) | 107 | 2022-11 | Bugzilla 1740530. |
| Safari (WebKit) | — | not shipped | Unshipped through Safari 26.5 (2026-04) per caniuse `colr-v1`. Falls back to monochrome or COLRv0. |
| Edge (Chromium) | 98 | 2022-02 | Inherits from Blink. |
| Android Chrome | 98 | 2022-02 | Via Skia. |
| iOS Safari | — | not shipped | Same WebKit engine as desktop Safari. |
| Samsung Internet | 19 | 2022-07 | Inherits from Blink. |

**Global availability (caniuse 2026-04)**: ~78%. Chromium + Firefox shipped 2022; Safari has not shipped COLRv1 through Safari 26.5 per caniuse. For cross-browser color-font support including Safari, ship COLRv1 + COLRv0 layered in the same font (the standard emoji-font pattern).

**Apple Color Emoji**: the *font* uses sbix (not COLRv1), independent of the fact that Safari lacks COLRv1 rendering. Even if Safari shipped COLRv1, Apple Color Emoji would still render via sbix on Apple platforms.

### sbix

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | 69 | 2018-09 | Skia sbix path. |
| Firefox (Gecko) | 47 | 2016-06 | Bug 1229943. |
| Safari (WebKit) | 8 | 2014-09 | CoreText native path; used for Apple Color Emoji from day one. |
| Edge (Chromium) | 79 | 2020-01 | |

**Global availability**: ~97%. Rare outside Apple-ecosystem fonts.

### CBDT / CBLC

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | 66 | 2018-04 | Skia CBDT path. |
| Firefox (Gecko) | 26 | 2013-12 | Original implementation alongside COLR. |
| Safari (WebKit) | — | — | **Never shipped.** |
| Edge (Chromium) | 79 | 2020-01 | Inherits from Blink. |

**Global availability**: ~85% (Safari gap). Effectively legacy in 2026; avoid for new work.

### SVG-in-OpenType

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | — | — | **WONTFIX.** Declared 2018; unchanged 2026. |
| Firefox (Gecko) | 26 | 2013-12 | Full SVG 1.1 subset. |
| Safari (WebKit) | 11 | 2017-09 | Partial: no SMIL, limited filters. |
| Edge (legacy) | 38 | 2017-04 | Pre-Chromium; dropped in Chromium Edge. |
| Edge (Chromium) | — | — | Inherits Chromium's WONTFIX. |

**Global availability**: ~30% (Chromium gap dominates). Avoid for new work.

### `font-palette` and `@font-palette-values`

| Engine | First stable version | Release date | Notes |
|---|---|---|---|
| Chromium (Blink) | 101 | 2022-04 | |
| Firefox (Gecko) | 107 | 2022-11 | Shipped alongside COLRv1. |
| Safari (WebKit) | 15.4 | 2022-03 | Shipped *before* COLRv1 — palette control on COLRv0 fonts for a full year before COLRv1 landed. |
| Edge (Chromium) | 101 | 2022-04 | |

**Global availability (caniuse 2026-04)**: ~93%. Baseline since 2022. See `./font-palette.md` for usage.

### Summary table (2026-04)

| Format | Chrome | Firefox | Safari | Edge | Global avail. | 2026 status |
|---|---|---|---|---|---|---|
| COLRv0 / CPAL | 41+ (2015) | 26+ (2013) | 11+ (2017) | 79+ (2020) | ~99% | Universal; safe for any use. |
| **COLRv1** | **98+ (2022)** | **107+ (2022)** | **16.4+ (2023)** | **98+ (2022)** | **~94%** | **Primary choice for new work.** |
| sbix | 69+ (2018) | 47+ (2016) | 8+ (2014) | 79+ (2020) | ~97% | Rare outside Apple-ecosystem fonts. |
| CBDT / CBLC | 66+ (2018) | 26+ (2013) | — | 79+ (2020) | ~85% | Legacy; avoid new use. |
| SVG-in-OT | — | 26+ (2013) | 11+ partial (2017) | — (Chromium) | ~30% | Dead; Chromium WONTFIX. |
| `font-palette` | 101+ (2022) | 107+ (2022) | 15.4+ (2022) | 101+ (2022) | ~93% | Baseline since 2022. |

---

## CSS wiring

### `font-palette` selects among palettes

```css
.dark-icons {
  font-family: "My Color Icon Font";
  font-palette: dark;  /* select the font's 'dark' palette if present */
}

.branded-emoji {
  font-family: "Noto Color Emoji";
  font-palette: --brand-palette;  /* custom palette declared below */
}
```

Keywords: `normal` (default palette, index 0), `light`, `dark`, `<dashed-ident>` (references a `@font-palette-values` rule). See `./font-palette.md` for the full property semantics.

### `@font-palette-values` declares a custom palette

```css
@font-palette-values --brand-palette {
  font-family: "Noto Color Emoji";
  base-palette: 0;
  override-colors:
    0 oklch(58% 0.2 260),   /* primary */
    1 oklch(72% 0.18 260),  /* secondary */
    2 oklch(92% 0.04 260);  /* tertiary */
}
```

`base-palette` picks the integer index of a palette already in the font to start from. `override-colors` remaps specific palette indices. Colors can use any CSS color syntax (hex, `rgb()`, `hsl()`, `oklch()`, named). See `./font-palette.md` §4.

### `font-variation-settings` with COLRv1

COLRv1's variable-axis integration allows animating color-stop positions and gradient geometry alongside outline changes:

```css
@property --wght {
  syntax: "<number>";
  initial-value: 400;
  inherits: true;
}

.animated-color-glyph {
  font-family: "Colophon Color Emoji";  /* hypothetical variable COLRv1 */
  --wght: 400;
  font-variation-settings: "wght" var(--wght);
  transition: --wght 400ms ease;
}

.animated-color-glyph:hover {
  --wght: 900;
}
```

The outline thickens on hover *and* the gradient stops shift along the designed path. See `./variable-fonts.md` §Animation and §Color Fonts + Variable Axes for the full mechanism.

### `font-feature-settings` does not control color

Common confusion: `font-feature-settings` enables OpenType Layout features (`liga`, `kern`, `ss01`, etc.). Color-font rendering is a separate axis — it happens *after* glyph selection from GSUB/GPOS. A feature tag cannot turn colored glyphs on or off.

Presentation selection for dual-presentation codepoints (e.g., ☺ U+263A, which can render text-style or emoji-style) is `font-variant-emoji`:

```css
.text-presentation  { font-variant-emoji: text; }
.emoji-presentation { font-variant-emoji: emoji; }
.default-presentation { font-variant-emoji: unicode; }
```

Baseline since 2024 (Chrome 112, Firefox 108, Safari 17). See `./opentype-features.md`.

---

## Use cases

### Emoji — the dominant use

Every OS-level emoji font rides on color-font tech:

| Font | Format | Platform |
|---|---|---|
| Apple Color Emoji | sbix | macOS, iOS, iPadOS, tvOS, visionOS, watchOS |
| Noto Color Emoji | COLRv1 (2023+) with CBDT legacy builds | Android, Chrome OS, Google Fonts CDN |
| Segoe UI Emoji | COLRv1 (Windows 11 22H2+, 2022); COLRv0 on earlier Windows | Windows 10/11 |
| Twemoji Mozilla | COLRv1 + COLRv0 | Firefox default emoji on non-Apple platforms |
| Samsung Color Emoji | COLRv1 | Samsung OneUI |

Web pages relying on emoji inherit these fonts via the browser's emoji fallback chain. The `font-variant-emoji` property selects text-vs-emoji presentation for dual-presentation codepoints but does not change which emoji font ships.

**Custom web-font emoji**: shipping Noto Color Emoji or a branded emoji font via `@font-face` is viable but the file size is significant — Noto Color Emoji COLRv1 is ~8–12 MB uncompressed, ~3–5 MB as WOFF2. Subset aggressively if you go this route (see §File size below).

### Colored icon fonts

- **Material Symbols** (Google, 2022+): primarily monochrome via variable-font axes (`wght`, `FILL`, `GRAD`, `opsz`), but ships COLRv1 variants for accent-colored icons and brand adaptations. Palette-swappable via `font-palette`.
- **Phosphor Icons Color** (Phosphor team, 2023+): COLRv1 build of the Phosphor icon set.
- **Lucide** (2020+): monochrome by design; does not ship a color-font variant. Philosophical choice — Lucide treats color as CSS-applied, not font-encoded.

The argument for a colored icon font over inline SVG: single HTTP request, browser glyph cache, consistent rendering. The argument against: SVG's `currentColor` + CSS is more flexible, inline SVG ships only the icons you use, and `@font-palette-values` adds a CSS layer that inline SVG doesn't need.

### Display type with color layers

A niche but growing category: foundry-authored multicolor display fonts where the glyph *itself* carries color.

- **Nabla** (Just van Rossum + Arthur Reinders Folmer, 2022, Google Fonts): variable COLRv1 display family with `wght`, `EDPT` (depth), `EHLT` (highlight) axes that drive gradient geometry. Reference example of variable + color-font synergy.
- **GT Color** (Grilli Type): commercial COLRv1 color display families.
- **Sharp Type Color** (Sharp Type): commercial multi-palette COLRv1 releases.
- **Colophon Foundry Color** series: COLRv1 with animation hooks.

Use sparingly. Color-display fonts are expensive to license, large to ship, and only appropriate for editorial headlines or branding where the extra rendering weight serves the design.

### Multicolor logos and wordmarks

A single font file can carry a wordmark in multiple palette variants — one for light backgrounds, one for dark, one for brand-on-brand. Swap via `font-palette` without re-loading the font:

```css
.logo           { font-palette: normal; }
@media (prefers-color-scheme: dark) { .logo { font-palette: dark; } }
.logo-inverted  { font-palette: --inverted; }

@font-palette-values --inverted {
  font-family: "MyBrand Logo";
  override-colors: 0 oklch(20% 0 0), 1 oklch(92% 0.04 260);
}
```

Compare to shipping three separate SVGs or three font files: one file, one HTTP request, three visual states.

---

## File size and delivery

### Representative sizes (2026-04, Latin + color glyphs only)

| Font | Format | Uncompressed | WOFF2 | Notes |
|---|---|---|---|---|
| Mono icon font (Lucide, ~1500 glyphs) | monochrome | ~180 KB | ~60 KB | Baseline comparison. |
| Same icons as COLRv0 | COLRv0 + CPAL | ~220 KB | ~75 KB | +25% for layer records + palettes. |
| Same icons as COLRv1 (flat colors only) | COLRv1 + CPAL | ~240 KB | ~82 KB | +35% for paint-tree encoding overhead. |
| Same icons as COLRv1 (with gradients) | COLRv1 + CPAL | ~310 KB | ~115 KB | Gradient glyphs nearly double. |
| Noto Color Emoji (COLRv1, full 3600+ glyphs) | COLRv1 | ~24 MB | ~8 MB | Extensive paint trees. |
| Noto Color Emoji (sbix legacy build, pre-2023) | sbix, 8 strike sizes | ~50 MB | ~40 MB | Bitmaps compress poorly after WOFF2's own preprocessor. |
| Apple Color Emoji (.ttc, shipped OS font) | sbix | ~200 MB | n/a | Not served over HTTP — local system font. |
| Nabla variable COLRv1 (Latin subset, Google Fonts) | COLRv1 + fvar | ~180 KB | ~65 KB | Variable axes amortize well. |

Rule of thumb:

- COLRv1 typically adds **+30% to +100%** over an equivalent monochrome font, depending on gradient density.
- Gradient-heavy emoji fonts can **double** vs a flat-COLRv0 version of the same set.
- sbix **explodes at scale** — every strike size × every glyph is a full PNG. A 32-strike font with 3,000 emoji at 6 sizes is a gigabyte of PNG before compression.
- WOFF2 compresses COLR/CPAL tables well (brotli exposes plenty of redundancy); compresses sbix/CBDT bitmaps poorly (PNG is already deflated, so there's little residual redundancy for WOFF2 to exploit).

### Subsetting

`pyftsubset` from `fonttools` 4.38+ correctly traces color-layer dependencies — when you subset by Unicode range, the tool follows paint-tree references into nested layer glyphs and keeps them. Older `pyftsubset` versions (<4.38, pre-2022) broke COLRv1 fonts by dropping the sublayers referenced from paint-tree nodes; upgrade if you see "disappearing color" after subset.

```bash
# Subset Noto Color Emoji to the 250 most common emoji
pyftsubset NotoColorEmoji-Regular.ttf \
  --unicodes-file=emoji-top-250.txt \
  --layout-features='*' \
  --flavor=woff2 \
  --output-file=NotoColorEmoji-subset.woff2
```

`unicode-range` `@font-face` splits work with color fonts exactly as they do with monochrome. Multi-subset delivery (Latin/Latin-ext/Cyrillic/...) can be applied to color-font icon sets with script-specific icon groups, though the use case is less common than with text fonts.

### Delivery patterns

See `./font-delivery.md` for the full delivery story. Color-font-specific notes:

- **`font-display: swap`** is usually wrong for emoji fonts — there's no sensible "fallback emoji" to show during the swap window. Use `block` for emoji-critical UI, `optional` where emoji are decorative.
- **Preload is usually not worth it.** A custom emoji font is typically not on the critical path. The OS emoji font renders during the block window; a custom emoji font swapping in after first paint is acceptable.
- **HTTP caching**: color fonts change rarely, fingerprint URLs, ship `Cache-Control: max-age=31536000, immutable`. No color-font-specific caveats.

---

## Fallback behavior

### COLRv1 font on a non-COLRv1 browser

Depending on browser version and what else is in the font:

1. **If the font has a COLRv0 layer alongside COLRv1**: the browser falls back to COLRv0 (flat layered colors). This is the recommended layering strategy for graceful degradation.
2. **If the font is COLRv1-only**: the browser falls back to the monochrome outline (the base `glyf`/CFF shape) rendered in the current CSS `color`. No colored layers appear; glyphs look like monochrome icons.
3. **If the base outline is `.notdef` (empty)**: the glyph renders as the tofu box. Rare but possible in emoji fonts where the designer omitted monochrome outlines assuming COLR will always resolve.

**Practical rule**: always ensure a COLRv1 font has valid monochrome outlines as the base glyph. The cost is negligible (the outlines are already there for the COLR layers to clip against), and the fallback behavior is graceful.

### Emoji fonts and system fallback

Browsers maintain a dedicated emoji fallback chain: when a codepoint isn't covered by any font in the CSS `font-family` stack, the engine reaches for the system emoji font (Apple Color Emoji on macOS/iOS, Segoe UI Emoji on Windows, Noto Color Emoji on Android/Chrome OS, Twemoji Mozilla on Firefox cross-platform). This fallback is implementation-defined and cannot be overridden by CSS; `font-family: Inter, sans-serif` still renders 🎉 via the system emoji font because Inter has no coverage for that codepoint.

`font-variant-emoji` influences *which glyph variant* the engine requests (text-style or emoji-style for dual-presentation codepoints) but doesn't change the fallback font itself.

### CPAL palette absence on a COLR font

If a COLRv0 or COLRv1 font lacks a `CPAL` table, the layers render in the current CSS `color` stack — effectively monochrome. This is legal per the OpenType spec but uncommon; most COLR fonts ship at least one palette.

Selecting `font-palette: --nonexistent` (a custom palette whose family doesn't match or whose `@font-palette-values` rule is missing) falls back to `font-palette: normal` (index 0).

---

## Accessibility

### WCAG 1.4.1 — use of color

Color fonts must not encode meaning in color alone. If a red glyph signals "error" and a green glyph signals "success," screen readers and color-blind users miss the distinction. Pair with text labels, icon shapes, or ARIA:

```html
<!-- Bad: color alone -->
<span class="status-icon" aria-hidden="true">●</span> Processing...

<!-- Good: color + shape + label -->
<span class="status-icon" aria-label="success">✓</span> Processing complete
```

For purely decorative color-font glyphs (emoji reactions in a UI), `aria-hidden="true"` is appropriate — screen readers will still read the Unicode codepoint's text equivalent ("grinning face") from the accessibility name mapping built into the OS.

### Contrast against background

Colored text still needs to satisfy WCAG 1.4.3 contrast ratios against its background. A color-font glyph rendered in a low-luminance palette color against a similarly-toned background fails the 4.5:1 body-text ratio. Test palette × background pairs; don't assume "it's a color font" exempts it from contrast rules.

This is where `@font-palette-values` earns its keep: a dark-mode palette can remap palette indices to higher-contrast colors without changing the font:

```css
:root { font-palette: normal; }
@media (prefers-color-scheme: dark) { :root { font-palette: --dark-mode; } }

@font-palette-values --dark-mode {
  font-family: "My Color Icon Font";
  override-colors:
    0 oklch(85% 0.15 260),  /* lighter primary for dark bg */
    1 oklch(75% 0.12 260);
}
```

### Screen readers

Color-font glyphs are read by their Unicode codepoint's text equivalent, not their color layers. Screen readers have no notion of layer colors; they see ☺ (U+263A "White Smiling Face") and announce "smiley face" regardless of which palette the glyph drew from. Generally fine; occasionally misleading (a colored ⚠ renders as "warning" regardless of whether the color palette is red-alarm or green-informational).

### `prefers-reduced-motion` and animated COLRv1

A COLRv1 font animated via `font-variation-settings` transitions should respect `prefers-reduced-motion: reduce`:

```css
.animated-color-glyph {
  transition: --wght 400ms ease;
}
@media (prefers-reduced-motion: reduce) {
  .animated-color-glyph { transition: none; }
}
```

Users with vestibular disorders, ADHD, or motion sensitivity benefit from static rendering. The color-font field is young enough that many early COLRv1 animation demos omit this.

### Forced Colors Mode (Windows High Contrast)

In Windows High Contrast / `forced-colors: active`, the OS overrides foreground and background colors with system-palette choices. Color-font glyphs render with their designed palette colors by default, which may clash with the system palette. Authors can opt into system palette remapping:

```css
@media (forced-colors: active) {
  .color-icon {
    forced-color-adjust: none;  /* keep the designed color palette */
    /* or */
    forced-color-adjust: auto;  /* let the OS remap — default */
  }
}
```

The right choice depends on whether the color carries meaning (auto) or is decorative brand identity (none).

---

## Tools

### Inspection and debugging

- **FontTools / TTX** (Python, `pip install fonttools`): `ttx font.ttf` dumps all tables including `COLR`, `CPAL`, `sbix`, `CBDT`, `SVG ` to XML. The canonical inspection workflow.
- **Wakamai Fondue** (wakamaifondue.com): drag-and-drop web tool. Shows which color-font tables a font contains and summarizes palette data.
- **Samsa** (axis-praxis.org/samsa): variable-font playground; renders COLRv1 across axis values and shows paint-tree structure.
- **FontDrop!** (fontdrop.info): similar to Wakamai Fondue; good for quick palette inspection.
- **Font Inspector** (browser dev tools): Chrome DevTools → Rendering panel → "Emulate CSS media feature" → palette inspection via Computed tab.

### Authoring

- **Glyphs 3** (macOS, commercial): strongest COLRv1 authoring workflow. Native paint-tree editor. Export COLRv1 + COLRv0 + sbix in one build.
- **FontLab 8** (cross-platform, commercial): full COLRv1 paint-tree authoring; slightly later to mature than Glyphs but comprehensive.
- **RoboFont + RoboFont color-palette plugins** (macOS, commercial): Python-scriptable; color support via community plugins.
- **nanoemoji** (Google, open source): Python pipeline for building COLRv1 emoji fonts from SVG sources. Used for Noto Color Emoji.
- **MicrosoftDocs/colr-gradients-spec**: reference implementation and test suite for COLRv1 paint trees.
- **SVGinOT Color Font Maker** (legacy, 2015-era): builds SVG-in-OT fonts. Not recommended for new work — use nanoemoji or Glyphs for COLRv1 instead.

### Testing

- **COLRv1 test page**: https://rsheeter.github.io/more_fonts/colrv1.html — reference COLRv1 rendering across a dozen paint types.
- **Chromium color-font testsuite**: in-tree at `third_party/blink/web_tests/fonts/colrv1/`.
- **Safari COLRv1 test**: render a known COLRv1 font (Noto Color Emoji, Nabla) in Safari and confirm monochrome fallback — Safari does not render COLRv1 through 26.5.

---

## Traps and gotchas

1. **The `SVG ` table's trailing space.** The 4-byte table tag is `S`, `V`, `G`, ` ` (space). Tools that strip trailing whitespace from internal lists will corrupt the font. Classic bug in custom font-packaging scripts.
2. **COLRv1 paint-tree cycles.** The spec forbids cycles (paint A references paint B references paint A), but some authoring tools allow them to be produced. Rasterizer behavior on a cyclic paint tree is implementation-defined and typically infinite-loops or bails. Validate with `fonttools subset --passthrough-tables` round-trip.
3. **Palette index out of bounds.** A COLR layer referencing palette index 5 in a font with only 4 colors in `CPAL` renders as the current CSS `color` (graceful degradation) — but in some older FreeType builds, index-out-of-bounds produces `rgb(0,0,0)` instead. Symptom: one layer goes black unexpectedly.
4. **COLRv1 + `font-palette: light`/`dark` without declared variants.** The `light`/`dark` keywords resolve to palette variants declared in the `CPAL` table's palette-type bitmap. If the font has only `normal`, `light`/`dark` fall back to `normal` silently — your dark-mode swap appears to do nothing. Check the font's palette type bits via `fontTools.ttLib.TTFont(f)['CPAL'].paletteTypes`.
5. **sbix rendered at non-native size.** Bitmaps blitted at non-integer ratios blur or pixelate. Always size sbix-emoji text at the authored strike sizes (Apple Color Emoji: 20, 32, 40, 48, 64, 96, 128, 160 px) where possible. CSS `font-size: 16px` on an sbix font resolves to the nearest authored strike and scales down — acceptable but not crisp.
6. **CBDT fonts on Safari.** Safari has never shipped CBDT rendering. A font that's CBDT-only will render as `.notdef` on Safari. Always ship a COLRv0 or COLRv1 fallback.
7. **Chromium refuses SVG-in-OT.** No amount of CSS persuades Chromium to render the `SVG ` table. A font relying on SVG-in-OT for its color layers is monochrome-only on Chromium (~70% of browser traffic).
8. **Color-font subsetting requires fontTools 4.38+.** Earlier `pyftsubset` drops COLRv1 sublayer dependencies. Symptom: subset font renders base outlines but colors are missing. Upgrade and re-subset.
9. **`font-variant-emoji` is not a color-font switch.** It selects text-vs-emoji presentation for dual-presentation codepoints (Unicode's variation-selector-15/16 mechanism). It does not toggle color-layer rendering on an emoji font. See `./opentype-features.md`.
10. **`prefers-color-scheme: dark` does not auto-remap COLR palettes.** The browser doesn't introspect fonts for palette-type bits; authors must explicitly write `@media (prefers-color-scheme: dark) { :root { font-palette: dark; } }`. See `./font-palette.md`.
11. **Apple Color Emoji cannot be swapped via `font-family`.** Safari's emoji fallback chain is implementation-defined; declaring `font-family: "Apple Color Emoji"` works on macOS/iOS but fails elsewhere. Ship Noto Color Emoji or Twemoji via `@font-face` for cross-platform consistency.
12. **Emoji sequences and ZWJ joins.** A single user-perceived emoji is often multiple codepoints joined by Zero-Width Joiner (U+200D) — e.g., 👨‍👩‍👧 is four codepoints. The emoji font must have shaper support (HarfBuzz handles this) *and* GSUB features that map the ZWJ sequence to a composite glyph. Fonts without the joined glyph render the ZWJ sequence as separate glyphs, which looks wrong. Test ZWJ sequences when shipping custom emoji fonts.
13. **Variable-axis animation of COLRv1 on Safari.** Safari does not render COLRv1 through 26.5. COLRv1 variable color glyphs display as monochrome fallback; animation via `font-variation-settings` affects glyph geometry but not color layers. Ship a COLRv0 fallback if Safari parity matters.
14. **`font-palette` animation is discrete.** Per CSS Fonts Level 4 §9.1, palette transitions step-change at 50%. For smooth animated color, use COLRv1 + `font-variation-settings`, not palette cross-fades. See `./variable-fonts.md` §Color Fonts + Variable Axes.
15. **OS emoji fonts override `font-family`.** You cannot suppress the system emoji font via `font-family: Inter, sans-serif, "Hide Emoji"`. If you ship a custom emoji font, list it *before* sans-serif so the browser's emoji fallback resolves to your font before the OS fallback. Even then, missing codepoints in your font fall through to the OS emoji font — shipping full Unicode-14 emoji coverage is a significant authoring investment.

---

## Anti-patterns

### 1. Shipping SVG-in-OT for new color fonts

Chromium WONTFIX; ~70% of browser traffic renders monochrome. Use COLRv1 + COLRv0 fallback instead. SVG-in-OT is appropriate only when maintaining a legacy font already in that format, and even then, migration is usually cheaper than coexistence.

### 2. Using color fonts for accessibility-critical text

Error states, success confirmations, required-field markers — if the only signal is a color glyph, color-blind users and screen-reader users miss it. Pair color with text label, icon shape, or ARIA.

### 3. Mixing text- and emoji-presentation selectors inconsistently

The same codepoint rendered as text-style in one component and emoji-style in another is a visual bug. Set `font-variant-emoji` at the root and override only where intentional. See `./opentype-features.md` for the feature catalog and `./variable-fonts.md` §CSS surface.

### 4. Preloading emoji fonts

Custom emoji fonts are typically not on the critical path. The OS emoji font renders during any swap window; a preload is 2–8 MB that could be CSS/JS instead. Preload only if emoji are the primary content (chat UI with brand emoji, emoji-picker UIs).

### 5. Relying on `font-palette: dark` without a dark palette in the font

The keyword resolves to the default palette silently. Inspect the font's palette-type bits before relying on keyword-driven palette switching. Use a custom `@font-palette-values --dark` if the font lacks one.

### 6. Hardcoding palette indices without testing across platforms

Palette indices are author-defined per font. A Noto Color Emoji palette index that means "skin tone 3" is not the same as a Twemoji index 3. `override-colors 3 red` does different things across fonts. Scope `@font-palette-values` to a specific `font-family` always.

### 7. Treating sbix and COLRv1 as interchangeable

sbix glyphs are bitmaps — they don't scale cleanly, they don't animate with variable axes, they don't respond to `font-palette`. COLRv1 glyphs are vectors — they scale, animate, and respect palettes. A font shipped as sbix-only cannot be post-authoring recolored via CSS.

### 8. Relying on SVG-in-OT SMIL animation

SMIL animation inside SVG glyphs was the original 2013 proposal; no current browser reliably renders SMIL in `SVG ` table fragments. Use COLRv1 variable axes + CSS transitions instead.

### 9. Omitting COLRv0 fallback in a COLRv1 font

Pre-COLRv1 browsers (~6% global as of 2026-04) render only the base outline. If the base outline is monochrome-only and the design depends on color, the fallback is broken. Ship both COLRv0 and COLRv1 in the same file when authoring tools allow; Glyphs 3 and FontLab 8 both support dual-layer export.

### 10. Ignoring CPAL palette types when authoring

The CPAL v1 format includes palette-type bits that mark palettes as `USABLE_WITH_LIGHT_BACKGROUND` or `USABLE_WITH_DARK_BACKGROUND`. Browsers use these bits to resolve `font-palette: light` and `font-palette: dark` keywords. Authoring tools that don't set these bits produce fonts where keyword-driven palette selection silently fails. Verify with `fontTools.ttLib.TTFont(f)['CPAL'].paletteTypes` after export.

---

## Sources

URLs retrieved **2026-04-18** unless noted.

### Primary specifications

- **Microsoft Learn — COLR table (1.9.1)**: https://learn.microsoft.com/en-us/typography/opentype/spec/colr — COLRv0 + COLRv1 spec, paint-tree formats, variation integration.
- **Microsoft Learn — CPAL table**: https://learn.microsoft.com/en-us/typography/opentype/spec/cpal — palette records, palette-type bits (LIGHT/DARK background).
- **Microsoft Learn — sbix table**: https://learn.microsoft.com/en-us/typography/opentype/spec/sbix — Apple-origin bitmap strikes.
- **Microsoft Learn — CBDT/CBLC tables**: https://learn.microsoft.com/en-us/typography/opentype/spec/cbdt, https://learn.microsoft.com/en-us/typography/opentype/spec/cblc — Google-origin bitmap format.
- **Microsoft Learn — SVG table**: https://learn.microsoft.com/en-us/typography/opentype/spec/svg — Adobe-origin SVG-in-OpenType.
- **W3C CSS Fonts Module Level 4**: https://www.w3.org/TR/css-fonts-4/ — `font-palette`, `@font-palette-values`, `font-variant-emoji`, color-font rendering semantics.
- **OpenType 1.9.1 change log**: https://learn.microsoft.com/en-us/typography/opentype/spec/changes — 2024-05; clarifies COLRv1 variation semantics.

### MDN

- **`font-palette`**: https://developer.mozilla.org/en-US/docs/Web/CSS/font-palette
- **`@font-palette-values`**: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-palette-values
- **`font-variant-emoji`**: https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-emoji
- **Color fonts guide**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts — color-font format landscape.

### Browser tracking

- **caniuse — `color-font-format-colr` (COLRv0)**: https://caniuse.com/colr — universal support matrix.
- **caniuse — `colr-v1`**: https://caniuse.com/colr-v1 — 2026-04 snapshot: Chrome 98+, Firefox 107+, Edge 98+. Safari not supported through 26.5.
- **caniuse — `color-font-format-svg`**: https://caniuse.com/svg-fonts — Chromium WONTFIX; Firefox/Safari partial.
- **caniuse — `css-font-palette`**: https://caniuse.com/css-font-palette — Baseline since 2022.
- **caniuse — `css-font-palette-values`**: https://caniuse.com/css-font-palette-values — same as above.
- **Chrome Status — COLRv1 fonts**: https://chromestatus.com/feature/5089401438175232 — shipping 98.
- **WebKit COLRv1 tracking**: search https://bugs.webkit.org for "COLRv1"; no shipped implementation as of Safari 26.5.
- **WebKit Bug 178745 — Implement SVG-in-OpenType**: https://bugs.webkit.org/show_bug.cgi?id=178745 — partial since Safari 11.
- **Chromium Bug — SVG-in-OT WONTFIX**: Chromium Issue 306078 (2013, declared WONTFIX 2018).

### Developer guides

- **Chrome for Developers — "COLRv1 Color Gradient Vector Fonts in Chrome 98"** (Dominik Röttsches, 2022-02): https://developer.chrome.com/blog/colrv1-fonts — the authoritative technical introduction.
- **web.dev — "How to Animate Variable Color Fonts"** (2023): https://web.dev/articles/variable-color-fonts — COLRv1 + variable axis worked examples.
- **Pixel Ambacht — "Introducing COLRv1"** (Roel Nieskens, 2022): https://pixelambacht.nl/2022/colrv1/ — designer-oriented explainer.

### Emoji projects

- **Google Noto Color Emoji**: https://github.com/googlefonts/noto-emoji — COLRv1 source and build pipeline.
- **Twemoji Mozilla**: https://github.com/mozilla/twemoji-colr — Firefox's COLR-encoded Twemoji.
- **Nabla (Google Fonts)**: https://fonts.google.com/specimen/Nabla — variable COLRv1 reference font.
- **Emojipedia — version history**: https://emojipedia.org/ — emoji codepoint addition timeline (Unicode 6.0 onward).

### Foundries shipping color fonts

- **Colophon Foundry**: https://www.colophon-foundry.org/ — Colophon Color Emoji and color display releases.
- **Grilli Type**: https://grillitype.com/ — GT Color commercial families.
- **Sharp Type**: https://sharptype.co/ — Sharp Type Color series.

### Tooling

- **nanoemoji (Google)**: https://github.com/googlefonts/nanoemoji — SVG → COLRv1 pipeline.
- **fontTools**: https://github.com/fonttools/fonttools — `pyftsubset`, TTX, COLRv1 support since 4.38.
- **MicrosoftDocs/colr-gradients-spec**: https://github.com/googlefonts/colr-gradients-spec — reference for paint types and test fonts.
- **Wakamai Fondue**: https://wakamaifondue.com/ — web-based font inspection.
- **FontDrop!**: https://fontdrop.info/ — alternative web inspector.
- **Samsa (axis-praxis)**: https://www.axis-praxis.org/samsa/ — variable-font playground with COLRv1 axis rendering.
