---
date: 2026-04-18
coverage: deep
peers:
  - ./font-delivery.md
  - ./variable-fonts.md
  - ./css-text-properties.md
  - ./metric-overrides.md
  - ../metrics/metrics-glossary.md
  - ../science/legibility-vs-readability.md
primary_sources:
  - https://freetype.org/freetype2/docs/documentation.html
  - https://freetype.org/freetype2/docs/hinting/text-rendering-general.html
  - https://freetype.org/freetype2/docs/subpixel-hinting.html
  - https://freetype.org/ttfautohint/doc/ttfautohint.html
  - https://learn.microsoft.com/en-us/typography/cleartype/
  - https://learn.microsoft.com/en-us/windows/win32/directwrite/direct-write-portal
  - https://learn.microsoft.com/en-us/typography/opentype/spec/
  - https://developer.apple.com/documentation/coretext
  - https://developer.apple.com/design/human-interface-guidelines/typography
  - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/third_party/blink/renderer/platform/fonts/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-smooth
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-rendering
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning
  - https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering
  - https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-font-smoothing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/forced-color-adjust
  - https://www.w3.org/TR/css-fonts-4/
  - https://drafts.csswg.org/css-fonts-4/#font-rend-props
  - https://caniuse.com/colr-v1
  - https://caniuse.com/mdn-css_properties_font-smooth
  - https://caniuse.com/text-size-adjust
  - https://fonts.google.com/knowledge/glossary/hinting
  - https://googlefonts.github.io/docs/
  - https://typedrawers.com/discussion/3387/rendering-differences-between-macos-and-windows
  - https://typography.guru/journal/hinting-explained/
  - https://adactio.com/journal/2146
  - https://www.smashingmagazine.com/2012/04/a-closer-look-at-font-rendering/
  - https://www.zachleat.com/web/fonts-smoothing/
  - https://infinnie.github.io/blog/2017/font-rendering.html
  - https://en.wikipedia.org/wiki/Font_hinting
  - https://en.wikipedia.org/wiki/ClearType
  - https://en.wikipedia.org/wiki/Subpixel_rendering
---

# Font hinting and rendering — contemporary reference

**Coverage tier**: deep
**Last verified**: 2026-04-18
**Sources**: FreeType documentation, ttfautohint manual, Microsoft ClearType/DirectWrite docs, Apple CoreText programming guide, Chromium Blink font code, MDN (text-rendering, font-smooth, webkit-font-smoothing, font-kerning), W3C CSS Fonts Level 4, caniuse COLRv1 + font-smooth, Google Fonts knowledge base, Typography.guru, Typodrome, Hrant Papazian's writings on platform rendering, Zach Leatherman on font smoothing, Smashing Magazine rendering explainers.
**Peer files**: [./font-delivery.md, ./variable-fonts.md, ./css-text-properties.md, ./metric-overrides.md, ../metrics/metrics-glossary.md]

<orientation>
This file covers the *rendering pipeline* surface: how typeface outlines become lit pixels, what "hinting" is, which rasterizer runs on which OS, how ClearType / grayscale / sub-pixel anti-aliasing differ, and which CSS controls exist to nudge the result. Focus is on what a web author needs to know to reason about text rendering across Windows, macOS, Linux, Android, and iOS in 2026.

What this file does **not** cover:
- Color-font rasterization internals (COLRv0/v1, SVG-in-OT, sbix, CBDT) — see `./color-fonts.md` (planned).
- Variable-font axis mechanics — see `./variable-fonts.md`.
- Network delivery and `@font-face` descriptors — see `./font-delivery.md`.
- Metric overrides and fallback alignment — see `./metric-overrides.md`.
- Raw metric definitions (x-height, cap-height, advance, UPM) — see `../metrics/metrics-glossary.md`.

All dated claims are scoped to stable releases as of **April 2026**. "Baseline" uses the Web Platform DX Community Group definition.
</orientation>

---

## TL;DR — what matters in 2026

1. **Three rasterizers run the world**: FreeType (Linux, Android, ChromeOS, embedded), CoreText (macOS, iOS, iPadOS, tvOS, visionOS), DirectWrite (Windows 8.1+). Chrome ships its own text layer (HarfBuzz + Skia) that uses the platform rasterizer for final pixel output.
2. **Hinting is instructions baked into a font** that tell the rasterizer how to snap outlines to the pixel grid at small sizes. Three flavors: TrueType bytecode (maximally controllable), PostScript/CFF declarative stem hints, or unhinted (heuristic autohinting by the rasterizer).
3. **Windows respects hinting aggressively + uses sub-pixel (ClearType) by default**. macOS ignores hints and uses grayscale anti-aliasing only (no sub-pixel since 10.14 Mojave, 2018). Linux/Android sit between — configurable, but contemporary defaults match macOS.
4. **The same font looks different on Windows vs macOS** — typically thicker and sharper on Windows. This is not a bug in either OS; it is a 30-year design schism: *hinting over fidelity* (MS) vs *fidelity over hinting* (Apple).
5. **High-DPI displays obsolete most of the argument.** At 2×+ device-pixel-ratio the outline has enough pixels that grid-fitting contributes marginal sharpness. Hinting matters on eInk, embedded, legacy 1× external monitors, and low-DPI Windows laptops.
6. **CSS controls are limited and non-standard.** `-webkit-font-smoothing` + `-moz-osx-font-smoothing` are vendor-prefixed and only meaningful on macOS. `text-rendering` is defined but implementation-varied. `font-smooth` (the only proposed standard) is deprecated and unshipped.
7. **Don't globally force `-webkit-font-smoothing: antialiased`.** It thins body text on low-DPI Windows where users view content through Chromium or Edge — the OS's sub-pixel thickening is doing useful work. Use it on display text (>30 px) where outline fidelity matters more than grid-snap.

---

## The rendering pipeline

Typeface data takes a long path from the font file to the pixel grid. The stages:

```
Font file (SFNT, WOFF2)
    │
    ├── Font table parser           — TTF/OTF outline tables, GPOS/GSUB, color tables
    │
    ├── Shaping engine (HarfBuzz)   — script/language-aware glyph selection, positioning,
    │                                 ligature + kerning + mark attachment
    │
    ├── Rasterizer                  — Outline → grayscale/subpixel bitmap at target ppem
    │     ├── Hinting interpreter   — TrueType VM, PostScript stems, or autohinter
    │     ├── Scaler                — UPM → device pixels
    │     ├── Positioner            — sub-pixel placement
    │     └── Anti-aliasing         — grayscale or sub-pixel (RGB/BGR)
    │
    ├── Glyph cache                 — OS-level glyph atlas (WIC / CTLine / Skia atlas)
    │
    └── Compositor                  — places rasterized glyph into the layer tree,
                                      applies transforms, composites with background
```

Every modern browser uses **HarfBuzz** for shaping (Blink, Gecko, WebKit all link HarfBuzz as of 2020+). Rasterization diverges by platform: Blink delegates to the OS rasterizer on macOS and Windows, but ships FreeType on Linux and Android. WebKit on macOS uses CoreText end-to-end. Gecko on Windows historically shipped a GDI codepath but moved to DirectWrite by Firefox 4 (2011) and has tracked DirectWrite features since.

**Key responsibilities of the rasterizer:**
- *Hinting interpretation* — executing or inferring the instructions that align outlines to the pixel grid.
- *Scaling* — converting from font-design-units (UPM, typically 1000 for CFF and 2048 for TrueType) to device pixels at the current ppem (pixels-per-em).
- *Positioning* — whether the glyph origin snaps to a whole pixel, or is allowed to land at a fractional offset (sub-pixel positioning).
- *Anti-aliasing* — smoothing the hard edge of the outline against the background grid. Grayscale AA uses luminance alone; sub-pixel AA uses the separate R/G/B channels as if they were three narrower pixels.
- *Compositing hints* — some rasterizers pre-multiply alpha differently for dark-on-light vs light-on-dark, producing perceptually different stroke weights at the same outline (the "stem darkening" trick).

---

## What hinting is (and isn't)

**Hinting** = instructions stored inside a font file that tell the rasterizer how to snap outline coordinates to the pixel grid at specific pixel-per-em (ppem) sizes, so that:

- All vertical stems in the font are the same pixel thickness at a given size.
- Letterforms retain their designed proportions at small sizes where sub-pixel blur would otherwise distort them.
- Critical features — counter openings, x-height, serif attachment — remain legible at 9–14 ppem where each pixel matters.

Hinting is *not* anti-aliasing, sub-pixel rendering, or kerning. It is the stage that happens **before** anti-aliasing; it modifies which pixels the rasterizer considers inside/outside the outline, and anti-aliasing then smooths the edge it found.

**Hinting matters most** at 8–20 ppem on non-HiDPI displays (roughly 6–15 px CSS on a 1× monitor). Above ~40 ppem the outline has enough pixels that grid-snap is visually indistinguishable from unhinted rendering. Below ~7 ppem no amount of hinting rescues legibility; bitmap replacements dominate.

### Three hinting models

#### TrueType hinting (`glyf` + `prep` + `fpgm` + `cvt`)

Stack-based bytecode executed by the TrueType VM inside the rasterizer. The font ships:

- `fpgm` (font program) — procedures that run once when the font is loaded.
- `prep` (control-value program) — runs once per ppem change; sets up the CV table for that size.
- `cvt` (control-value table) — named control values (standard stem widths, x-height reference, cap-height reference, etc.).
- `glyf` — per-glyph instructions that move outline points to the pixel grid.

The TrueType VM has ~200 opcodes. A serious hinting job for a single Latin master can run 20–40 KB of bytecode across all glyphs. Authors: Monotype, Microsoft, Adobe in the 1990s; Autodesk (for technical drafting fonts), ParaType (Cyrillic), Dalton Maag (commercial commissions), and specialized house shops today. Maximally controllable; laborious to author; expensive to maintain.

TrueType hints are *pixelwise* — the font can say "at 13 ppem, round the left sidebearing of 'a' to the nearest pixel but round the right stem up half a pixel." This level of control is why Microsoft stuck with TrueType: hinted TT can make a font snap cleanly at 11 px on a 96-DPI display, which CFF cannot match without a heroic autohinter.

#### PostScript hinting (Type 1, CFF, CFF2)

Declarative. The font contains **stem hints** (`stemh` for horizontal, `stemv` for vertical, plus `hstem3`/`vstem3` ghost hints for counter-preservation) that describe where major stems *are*, not how to move them. The rasterizer decides interpretation.

- Smaller to author (a font designer can auto-generate stem hints with tools like Adobe's `autohint` or FontLab's built-in hinter).
- Less control (the rasterizer may not snap exactly where the designer wished).
- Critically: modern PostScript-style hinting in CFF2 interpolates along variable-font axes natively. TrueType hinting has this via the newer `cvar` table but is brittle to author.

PostScript hints work well in CoreText (which ignores much of the hint data anyway, so the declarative model aligns with Apple's philosophy). On Windows, CFF + PostScript hints render through DirectWrite's CFF codepath; the result is typically softer than TT-hinted output.

#### Unhinted — heuristic autohinting by the rasterizer

Many fonts, especially variable fonts and recent releases from small foundries, ship with no hinting instructions at all. The rasterizer applies its own autohinter:

- **FreeType's autohinter**: deterministic, cross-platform, called when the `prep`/`fpgm` tables are missing or when the user configures `hintstyle=auto`.
- **CoreText's internal heuristics**: largely sidesteps hinting in favor of stem-darkening + grayscale AA (since macOS 10.6, 2009).
- **DirectWrite's fallback**: applies lightweight outline-snap for CFF fonts without stem hints.

Unhinted is the **modern default for macOS** (hints are mostly ignored anyway) and increasingly for variable fonts shipped through Google Fonts. On Windows the difference between a hinted and unhinted Latin font at 12 px is still perceptible — hinted renders crisper, unhinted renders softer but preserves letterform proportions more faithfully.

---

## Auto-hinting

Hand-hinting is expensive — days to weeks per family per script. Automated tools narrow the gap:

### `ttfautohint` (FreeType project)

`ttfautohint` takes an unhinted TTF and emits a TTF with deterministic TrueType hints. Workhorse of the Google Fonts pipeline; most fonts in the library are autohinted by it at build time. Result: markedly better than unhinted on Windows DirectWrite at 11–14 ppem (stems snap consistently, x-height aligns); "good enough" at 8–10 ppem, inferior to hand-hinted; indistinguishable from unhinted above 20 ppem.

Key flags: `--hinting-range-min=8 --hinting-range-max=50` (default range); `--default-script=latn` (change to `cyrl`/`grek`/`arab` for non-Latin — wrong script gives wrong stem hinting); `--windows-compatibility` adjusts vertical metrics so Windows `usWin*` doesn't clip ascenders/descenders.

### Adobe's CFF autohinter (AFDKO)

`autohint` inside Adobe's Font Development Kit for OpenType. Handles PostScript-style stem hints for CFF. Glyphs, FontLab, and RoboFont all wrap AFDKO-derived logic in their built-in hinters.

### Practical autohinter advice (2026)

For new web fonts: use `ttfautohint` with the default range if your audience includes low-DPI Windows; skip if macOS/iOS/Retina-only. For variable fonts: `ttfautohint-vf` is experimental with partial coverage; most shipping variable fonts are unhinted. Google Fonts runs variable fonts through a conservative autohinter that emits flat (non-interpolating) hints — works on Windows, imperfect at weight extremes. Cross-check by rendering at 12/14/16 px on Chrome Windows 11 and Chrome macOS.

---

## OS-specific rendering — the big split

The two philosophies have remained stable since ~2009:

- **Microsoft**: *hinting over fidelity*. Text should look sharp on the pixel grid, even if the glyph shape drifts slightly from the designer's outline.
- **Apple**: *fidelity over hinting*. Text should match the designer's intent, even if that means softer edges on low-DPI displays.

Linux inherited FreeType's configurable middle ground; contemporary distros (Ubuntu 22.04+, Fedora 38+, Arch rolling) default to an Apple-like grayscale setup, but the user can switch.

### Windows (DirectWrite, 2009+)

Shipped in Windows 7 (2009), delivered to the web via IE9 (2011). Replaced GDI as the modern text API.

- **Respects TrueType hinting aggressively at small sizes.** A well-hinted TT font at 12 px snaps to crisp vertical stems; PostScript/CFF renders softer.
- **ClearType (sub-pixel AA) on by default on LCDs.** Detected via display metadata; disabled in Settings → Fonts → ClearType. Users almost never disable it.
- **GDI (legacy, pre-DirectWrite)** forced stems to integer pixel widths regardless of outline — the "aggressive Windows" look people remember. Still runs for Notepad and parts of Explorer. Modern browsers all use DirectWrite.
- **DirectWrite "outline-faithful mode"** (Windows 8.1, 2013): sub-pixel positioning honored, hint-based grid-snap relaxed. Exposed via `DWRITE_RENDERING_MODE`. Chrome and Edge use it for large text (>30 px); smaller sizes still grid-snap.
- **GDI ClearType vs DirectWrite ClearType**: different sub-pixel filters. DirectWrite is slightly thicker with less color fringing. Users don't notice; technical testers do.

Windows 11 retains ClearType as default. Microsoft trialed grayscale-by-default in Insider builds (2019) but reverted after low-DPI laptop user backlash. No public roadmap change as of 2026-04.

### macOS (CoreText, 10.6+)

CoreText replaced ATSUI in Mac OS X 10.5 (2007), became the only text API in 10.6 (2009).

- **Ignores most TrueType hints since ~10.6.** `prep`/`fpgm` are parsed but a simplified interpretation skips most grid-snap logic.
- **Grayscale anti-aliasing with "stem darkening"** — slightly thickens strokes for dark-on-light to compensate for perceptual thinning from AA. Makes text look bolder on macOS than Windows would predict from the same outline.
- **No sub-pixel anti-aliasing since macOS 10.14 Mojave (September 2018).** Apple cited: Retina obsoletes sub-pixel; external non-Retina displays now rare; sub-pixel breaks with any transform, scroll, or animation.
- **Sub-pixel positioning remains** — glyph origins can land at fractional x-pixels. Different from sub-pixel anti-aliasing.
- **Legacy preference key**: `defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO` partially re-enables some pre-Mojave rendering quirks in some apps but does not restore sub-pixel AA. Community folklore overstates what it does.

Practical consequence: on 1× external displays, Mac-rendered text looks softer than Windows; users switching across platforms complain in both directions. Both are correct.

### Linux (FreeType)

De-facto rasterizer for GNOME, KDE, XFCE, Wayland compositors, and Android. Configurable via fontconfig:

- `hintstyle`: `hintnone` | `hintslight` | `hintmedium` | `hintfull`
  - `hintnone`: pure outline-derived bitmap.
  - `hintslight`: vertical hinting only. **Modern default on most 2020s distros.**
  - `hintmedium`: vertical + horizontal grid-snap with moderation.
  - `hintfull`: aggressive grid-snap; equivalent to classic Windows GDI. Rare outside embedded.
- `hinting`: master switch.
- `antialias`: enables grayscale AA.
- `rgba`: `none` | `rgb` | `bgr` | `vrgb` | `vbgr` — sub-pixel panel order. `rgb` is overwhelmingly most common.
- `lcdfilter`: `lcddefault` | `lcdlight` | `lcdlegacy` | `lcdnone` — sub-pixel filter kernel.

Contemporary defaults (Ubuntu 24.04, Fedora 40, Debian 12 as of 2026-04): `hintstyle=hintslight`, `antialias=true`, `rgba=rgb`, `lcdfilter=lcddefault` — matches CoreText's general approach (light hinting + grayscale-ish sub-pixel). Pre-2020 distros often shipped `hintfull` for a sharper, Windows-like look. Embedded Linux (Yocto, buildroot) frequently ships `hintfull` + LCD sub-pixel on low-DPI targets.

Microsoft's ClearType patents expired in 2019; FreeType's LCD filter now ships enabled by default.

### Android (Skia → FreeType)

FreeType via Skia. Most 2016+ mid-range-and-above devices have DPRs of 2.0–4.0, so hinting and sub-pixel contribute marginally. Defaults: grayscale AA, slight hinting — similar to modern Linux. Older/cheap 1.0–1.5 DPR devices may use sub-pixel based on OEM config.

### iOS / iPadOS / tvOS / visionOS (CoreText)

Same pipeline as macOS: grayscale AA, no sub-pixel, stem darkening, minimal hinting. Every shipping device since iPhone 4 (2010) is Retina (2×+). Hinting practically irrelevant; fidelity dominates.

### Summary matrix

| OS | Rasterizer | Hinting respected | Default AA | Sub-pixel AA | Stem darkening |
|---|---|---|---|---|---|
| Windows 10/11 | DirectWrite | Yes (TT aggressive) | ClearType (sub-pixel) | Yes (RGB) | No |
| Windows 11 (tablet mode, HDR, some configs) | DirectWrite | Yes | ClearType or grayscale | Sometimes | No |
| macOS ≥ 10.14 | CoreText | Minimal | Grayscale | **Never** | Yes |
| iOS / iPadOS / tvOS / visionOS | CoreText | Minimal | Grayscale | Never | Yes |
| Ubuntu 24.04 / Fedora 40 / Arch 2026 | FreeType | Slight (default) | Grayscale or sub-pixel | User-configurable | No (stem-snap instead) |
| Android 12+ | FreeType via Skia | Slight | Grayscale | Rare | No |
| ChromeOS | FreeType | Slight | Grayscale | No | No |
| Embedded / eInk / kiosk | FreeType | Full (often) | Grayscale or 1-bit | Rarely | No |

---

## Sub-pixel rendering

An LCD (or OLED with RGB stripes) panel has three sub-pixels per logical pixel. A white pixel = R on + G on + B on. By addressing R, G, B independently, the rasterizer gets **~3× horizontal resolution** at the cost of introducing colored fringes if the content isn't static.

### ClearType (Windows)

Microsoft's sub-pixel algorithm, released in 2000 with Windows XP, matured in Vista/7 with per-user calibration. Key points:

- Uses a configurable LCD filter (blur kernel) to tame color fringing.
- Calibrated per-user via the ClearType Text Tuner — users pick sharpest-looking of 4 test pages. Settings persist in registry.
- On by default on all LCDs since Windows 7.
- Fundamentally incompatible with: (a) any CSS transform on a text element (including `opacity < 1.0`), (b) scrolling on GPU-composited layers (during scroll, text may temporarily fall back to grayscale in Chrome), (c) rotation.

### macOS 10.14 Mojave removed it (2018)

Apple's reasoning, per 2018 WWDC session notes and developer docs:

- Retina displays have enough pixels per em that sub-pixel AA's benefits are invisible.
- Sub-pixel AA fights with the compositor; any layer transform breaks it, causing "color shimmer" during animation.
- Apple's user base is mostly on Retina MacBooks; external non-Retina displays are a shrinking minority.

The removal was silent — no API deprecation warning, just different pixels. Third-party apps didn't need to change code; the rasterizer stopped emitting sub-pixel output. Users on 1× external displays protested. Apple did not relent.

### Chromium and Firefox sub-pixel behavior

- **Chromium (Blink + Skia)**: respects the OS-level sub-pixel preference. On macOS, grayscale only (inherits from CoreText). On Windows, ClearType by default. On Linux, follows fontconfig.
- **Firefox (Gecko)**: same approach. On Windows, DirectWrite + ClearType. On macOS, CoreText grayscale.
- **Incompatibility with compositing**: when an element has a CSS transform, `opacity < 1.0`, or is on a GPU-composited layer, browsers disable sub-pixel AA for that element and fall back to grayscale. This is visible as a rendering "shift" at the start of a scroll or animation.

### `-webkit-font-smoothing` and `-moz-osx-font-smoothing`

Non-standard, vendor-prefixed CSS properties that *only* affect rendering on macOS:

```css
/* macOS WebKit + Blink */
-webkit-font-smoothing: auto | none | antialiased | subpixel-antialiased;

/* macOS Firefox */
-moz-osx-font-smoothing: auto | grayscale;
```

- `-webkit-font-smoothing: antialiased` — forces grayscale AA; bypasses CoreText's stem darkening. Text renders **thinner** than default macOS rendering. This is the infamous "dark mode text looks better" trick.
- `-webkit-font-smoothing: subpixel-antialiased` — the pre-Mojave default; on ≥ 10.14 treated as equivalent to the default (grayscale with stem darkening).
- `-webkit-font-smoothing: none` — disables AA entirely. Produces pixelated 1-bit text. Never useful except for intentional retro/8-bit effects.
- `-webkit-font-smoothing: auto` — initial. Defers to platform.

**Firefox's `-moz-osx-font-smoothing: grayscale`** is the Gecko analog of `antialiased`. The two properties are often paired:

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

Neither property has any effect on Windows, Linux, Android, or iOS. (iOS WebKit does expose `-webkit-font-smoothing` but it is largely a no-op since iOS CoreText already does grayscale with stem darkening.)

### The `antialiased` trick — why designers use it

Before Mojave (2018), Safari on macOS used **sub-pixel anti-aliasing + stem darkening**, producing text that rendered noticeably heavier than on Windows or Linux. Designers writing CSS for brand sites noticed that their display fonts looked "chunky" on macOS and "correct" everywhere else. The workaround became:

```css
body { -webkit-font-smoothing: antialiased; }
```

This disabled sub-pixel AA on macOS (leaving grayscale) and implicitly disabled stem darkening, producing thinner text that matched the designer's outline. The trick was viral in 2014–2018 design circles.

**After Mojave**, sub-pixel AA is gone but stem darkening remains. `antialiased` still disables stem darkening — text renders thinner than default. On Retina displays the difference is subtle but visible, especially on light text over dark backgrounds.

**The cost on Windows**: since `-webkit-font-smoothing` is a no-op on Windows, setting it globally doesn't *hurt* Windows — but the CSS rule is frequently paired with `font-weight` adjustments that *do* affect Windows. The common pattern "set weight 300 with `antialiased`" produces legible text on macOS and near-illegible thin text on low-DPI Windows.

### `font-smooth` (deprecated standard)

CSS Fonts Level 3 proposed a standardized `font-smooth` property:

```
font-smooth: auto | never | always | <absolute-size> | <length>
```

**Status (2026-04)**: deprecated. Only Safari ever shipped a partial implementation (Safari 6–7, circa 2012). The CSS Fonts Level 4 working draft omits `font-smooth` entirely. MDN marks it deprecated. Do not author it.

The practical standard surface remains the vendor-prefixed `-webkit-font-smoothing` / `-moz-osx-font-smoothing` pair — which is ironic given CSS's move away from vendor prefixes everywhere else.

---

## Variable fonts and hinting

Variable fonts complicate hinting because the outline changes with axis settings. A stem that's 80 units wide at `wght=400` might be 160 at `wght=700`; the hint that snaps the 80-unit stem to 1 pixel at 12 ppem does not transparently work for the 160-unit stem.

### TrueType hinting in variable fonts

OpenType 1.8 (2016) introduced the `cvar` table, which interpolates control values across axes. A variable font with TrueType hints ships:

- `glyf` — base-master outlines + `gvar` deltas.
- `cvt` — base-master control values.
- `cvar` — axis deltas for the control values.
- `prep` / `fpgm` — unchanged; same bytecode runs.

This is hard to author. Microsoft Sitka and Cambria ship hinted variable fonts; Monotype has a few. Most variable fonts ship unhinted or with `ttfautohint-vf`-generated flat hints that don't interpolate but render acceptably across the axis space.

### PostScript/CFF2 hinting in variable fonts

CFF2 (OpenType 1.8) was designed with variable fonts in mind. Stem hints interpolate natively via the `VVAR` / `HVAR` and axis-based hint dictionaries. In principle, this is cleaner than TrueType's bolted-on `cvar`. In practice, few CFF2 variable fonts are shipped in 2026 — most variable fonts use TrueType outlines for compatibility.

### What to ship in 2026

- **High-DPI-heavy audience (Retina Macs, modern iOS, flagship Android)**: ship unhinted variable fonts. The lack of aggressive hinting is imperceptible above 2× DPR.
- **Low-DPI Windows audience (enterprise laptops, call centers, kiosk PCs)**: consider an autohinted static fallback alongside the variable font. Example: `@font-face` block for a ttfautohint-generated static regular + static bold, then a separate `@font-face` for the variable font gated on `@supports (font-variation-settings: normal)`. Most authors skip this; users on 1× Windows screens notice.
- **Google Fonts variable**: Google's variable pipeline runs a conservative autohinter. Good enough for most cases. Verify by rendering at 12/14/16 px on Windows Chrome.

### The soft-rendering trap

On low-DPI Windows, an unhinted variable font at 12 px can look 15–20% softer than a hinted TT static. Content-heavy sites with long-form body text on laptop Windows will get user complaints ("the text looks blurry"). This is the single biggest rendering complaint in 2023–2026 Google Fonts support forums.

---

## Text rendering CSS controls

### `text-rendering`

```
text-rendering = auto | optimizeSpeed | optimizeLegibility | geometricPrecision
```

CSS Fonts Level 4. Values: `auto` (browser chooses; typically `optimizeLegibility` ≥20 px, `optimizeSpeed` below), `optimizeSpeed` (suppress kerning/ligatures, fastest), `optimizeLegibility` (enable kerning + ligatures at render time independent of `font-kerning`/`font-variant-ligatures`), `geometricPrecision` (SVG: sub-pixel-exact glyph positions and no font-size rounding; HTML: most browsers treat it as `optimizeLegibility`).

**Folklore**: 2011–2013, `optimizeLegibility` was notorious for blocking paint on huge text because kerning was serialized with layout. Fixed 2015–2018. Old blog posts still top Google; in 2026 the cost is negligible on ordinary content, measurable only on virtualized lists of hundreds of small text elements.

**Recommendation**: set `optimizeLegibility` on body if you want kerning + ligatures without relying on `auto`'s size threshold. Measure before applying on high-volume UI.

### `font-kerning`

```
font-kerning = auto | normal | none
```

Baseline since 2018. `auto` = browser decides (~20 px threshold, varies). Kerning is shaping-time (HarfBuzz), not rasterization. Interacts with `text-rendering: optimizeLegibility` — if legibility forces kerning, `font-kerning: none` may be overridden in some engines. `font-kerning` is the standard control; prefer it.

### `font-variant-ligatures`

See `./css-text-properties.md`. Shaping-time, not rasterization. Mentioned here because `text-rendering: optimizeLegibility` can override it in some engines (Blink historically; fixed in ~Blink 110+).

### `image-rendering`

Applies to `<img>` and `background-image`, plus emoji/fonts rendered via bitmap tables (sbix, CBDT). `image-rendering: pixelated` preserves sharp-edge look on bitmap emoji at large sizes. Rarely relevant for body text.

### `text-size-adjust`

WebKit invention for iOS Safari auto-inflation on narrow viewports. Standardized CSS Text 4, Baseline ~2020. `html { -webkit-text-size-adjust: 100%; }` prevents iOS Safari inflation. Legacy hygiene on modern responsive designs with `<meta name="viewport">`.

### `forced-color-adjust`

Part of Forced Colors Mode (Windows High Contrast). In `forced-colors: active` the OS typically suppresses sub-pixel AA and renders with system palette colors; font-smoothing tweaks have no effect.

### `-webkit-font-smoothing` / `-moz-osx-font-smoothing`

Covered above under sub-pixel rendering. Non-standard; only meaningful on macOS.

---

## Kerning and ligatures at the rendering layer

Kerning and ligatures are applied during **shaping** (HarfBuzz), not rasterization. They interact with rendering at compositing time only indirectly: a font with a heavy hand-hinted stem may shift sub-pixel placement enough that kerning pairs look slightly different after hinting snaps. For practical purposes:

- Set `font-kerning: normal` explicitly if you want to guarantee kerning at all sizes.
- Set `font-variant-ligatures: common-ligatures` if your font has ligatures you want preserved (standard fi/fl/ffi/ffl; Baseline since 2018).
- Avoid `letter-spacing` on text with ligatures — Blink and WebKit disable `liga`/`clig` when `letter-spacing` is non-zero unless `font-variant-ligatures: common-ligatures` is explicitly set.

See `./opentype-features.md` for the feature catalog and `./css-text-properties.md` for full syntax and browser support.

---

## Color fonts and rendering

Color fonts ride on the same rasterization pipeline but add a color-layer composition step:

- **COLRv0** (2013, Microsoft) — base + layers of flat colors. Supported in all major browsers since ~2016–2019.
- **COLRv1** (2022, Google + Adobe + Microsoft) — gradients, transforms, composite modes, variable-axis animation. Chromium 98+ (2022-02), Firefox 107+ (2022-11), Safari 16.4+ (2023-03). As of 2026-04, all three engines ship COLRv1 stable.
- **SVG-in-OT (SVG OpenType)** — full SVG per glyph. Firefox 26+, Safari 11+. Chromium has refused to ship (WONTFIX, citing security surface). Effectively dead for the web in 2026.
- **CBDT/CBLC** — Google's pre-COLRv1 Android emoji format. Chromium 66+, Firefox 26+. Being phased out in favor of COLRv1.
- **SBIX** — Apple's bitmap color format. Apple Color Emoji uses SBIX. Safari 8+, Firefox 47+, Chromium 69+.

**Rendering implication**: color-font rasterization is more expensive than monochrome because each layer composes separately. For emoji-heavy content (chat UIs, social feeds), this matters; the glyph cache helps, but first-paint of a novel emoji still touches the color pipeline.

Depth on color-font authoring and per-layer compositing lives in **`./color-fonts.md` (planned)**; this file cross-references.

---

## Rendering and accessibility

### Forced Colors Mode (Windows High Contrast)

Activated via Windows Settings → Accessibility → Contrast themes. In this mode:

- The OS overrides all foreground/background colors with system palette choices.
- Sub-pixel anti-aliasing is typically suppressed by the OS.
- CSS authors can detect via `@media (forced-colors: active)` and adjust.
- `-webkit-font-smoothing` and similar are no-ops.

Practical rule: don't rely on font-smoothing tweaks to communicate hierarchy; test in Forced Colors Mode.

### `prefers-contrast`

```css
@media (prefers-contrast: more) { /* tune weight, thickness, tracking */ }
```

Does not directly affect rendering, but informs authors that users want high-contrast output. A pragmatic response: bump font weight by one step (regular → medium) for text under this media query.

### Dyslexia and rendering

See `../accessibility/dyslexia.md`. The dyslexia-friendly font literature is about letterform design, not rendering. Rendering tweaks (AA style, hinting) have no measured effect on dyslexic reading outcomes. Don't disable AA as an accessibility treatment.

---

## Modern state and convergence (2024–2026)

Several trends have reduced the practical importance of hinting:

1. **High-DPI displays dominate desktop and mobile.** MacBook Pros are Retina since 2012; iPads since 2014; iPhones since 2010. Windows laptops above $800 ship 2× or higher DPR. Flagship Androids are 3–4× DPR. Hinting matters on the remaining 1× displays: budget Windows laptops, office external monitors driven at native resolution, and legacy kiosks.
2. **Apple's 2018 removal of sub-pixel AA** signaled industry direction. No major OS has added sub-pixel since; none removed grayscale.
3. **Variable fonts, largely unhinted.** Google Fonts ships autohinted variable fonts, but many commercial foundries (Grilli Type, KLIM, Pangram Pangram, Displaay) ship variable fonts unhinted. On Retina this is invisible; on low-DPI Windows the softness shows.
4. **Windows 11 and expected 12**: ClearType retained. Microsoft has been internally testing grayscale-by-default since 2019 (Insider builds, reverted) and as of 2026-04 no public plan to switch.
5. **Chromium convergence**: Chrome on macOS uses CoreText grayscale; Chrome on Windows uses DirectWrite + ClearType; Chrome on Linux uses FreeType per fontconfig. Chrome does not override the platform rasterizer's AA model.
6. **Designer CSS**: specifying `-webkit-font-smoothing: antialiased` in CSS to make macOS match designer outline is common but controversial. It "flattens" fonts designed with stem darkening in mind — authors like Matthew Carter have objected that the fonts weren't designed to be rendered that way.

The rough consensus in 2026: **let the OS rasterize**. Override only for specific display-text use cases where the designer's outline matters more than grid-snap.

---

## Common gotchas

1. **Windows vs macOS weight mismatch.** Same `font-weight: 400` looks heavier on Windows (DirectWrite sub-pixel thickening) than macOS (CoreText stem darkening goes the other direction). Designs balanced on Mac look thin on Windows and vice versa. Test both; variable fonts help — pick a `wght` that reads on both, even if non-standard.
2. **`-webkit-font-smoothing: antialiased` on body text.** Thins macOS text; no effect on Windows. Paired with `font-weight: 300` (common) → near-illegible thin Windows text. Apply `antialiased` only to display text (>30 px).
3. **`text-rendering: optimizeLegibility` folklore.** Old blogs say it blocks layout on huge text. Fixed 2016–2018. Safe on body text in 2026; measure only in extreme cases.
4. **WOFF2 decompression doesn't affect rendering.** Network compression only; decompressed to full TTF in memory. Hinting preserved exactly.
5. **Variable font `HVAR`/`VVAR` subset.** Stripping these during subsetting breaks advance-width interpolation — `wght=700` may overflow containers sized for `wght=400`. Verify `pyftsubset` keeps them (default yes; custom pipelines sometimes drop). See `./font-delivery.md` §Subsetting.
6. **Sub-pixel AA flicker during animation.** Elements with running transform/transition/animation drop to grayscale and snap back. Visible on Windows Chrome. `will-change: transform` pins to GPU layer → permanently grayscale, no snap, marginally softer text.
7. **Emoji + text mixing.** Two rasterization paths — Latin text (grayscale/sub-pixel) and emoji (color-font per-layer composite). Emoji glyph cache miss adds ~1–3 ms first-render. Pre-warm cache in chat UIs via off-screen string render.
8. **`font-synthesis` synthetic bold interaction with hinting.** On low-DPI Windows, synthetic bold looks coarser than a real bold cut. Retina: indistinguishable.
9. **Sub-pixel positioning ≠ sub-pixel rendering.** Positioning = fractional glyph origin (x=10.25 px; compatible with grayscale). Rendering = R/G/B channels as separate columns (the controversial one). macOS kept positioning, removed rendering in Mojave.
10. **`@media (resolution)` as a gate.** `@media (min-resolution: 2dppx) { body { -webkit-font-smoothing: antialiased; } }` applies the thinning trick only on Retina; skips it on 1× Windows. Reasonable cross-platform pattern.

---

## Tools and diagnostics

### Browser-side inspection

- **`chrome://gpu`** — reports GPU vendor, rasterizer, AA state, ANGLE backend. In the "Graphics Feature Status" section, look for "Rasterization" and "Text Rendering." Confirms whether sub-pixel AA is in use.
- **`about:support`** (Firefox) — similar diagnostics. Look under "Graphics" → "Features" for sub-pixel AA state.
- **Safari Web Inspector** → Elements → Computed → filter "smooth" — shows resolved `-webkit-font-smoothing` per element.

### OS-side tools

- **macOS Font Book** (`/Applications/Font Book.app`) — per-font preview; compare at multiple ppem sizes. Does not show hinting data. For hinting inspection, use a tool like Glyphs or FontLab.
- **Windows Font Settings** (Settings → Personalization → Fonts) — per-font preview; "ClearType Text Tuner" for calibration. Classic `charmap.exe` for code-point inspection.
- **Linux `ftview`** (FreeType utility) — renders a font at configurable ppem + hinting mode. The canonical tool for FreeType rendering inspection.
- **Linux `ftstring`** — renders test strings with configurable FreeType settings. Essential for LCD filter testing.

### Font-inspection web tools

- **Wakamai Fondue** (https://wakamaifondue.com/) — drag-and-drop font inspection. Shows OpenType tables including hinting (`prep`, `fpgm`, `cvt`, `gasp`). Tells you *whether* a font is hinted; doesn't show the bytecode.
- **FontDrop** (https://fontdrop.info/) — similar. Good for quick metrics + feature inspection.
- **Samsa** (https://www.axis-praxis.org/samsa/) — variable-font playground; renders across axis values. Useful for checking variable-font rendering at weight/width extremes.

### Authoring-side hinting tools

- **Glyphs** (macOS) — commercial font editor; built-in hinter for TT and CFF. Autohint button works reasonably; manual hinting UI is the best in the industry.
- **FontLab 8** (macOS/Windows) — commercial; most powerful manual hinting UI. Used by Monotype, ParaType.
- **RoboFont** (macOS) — commercial; Python-scriptable. Relies on external hinters (`ttfautohint`, `autohint`).
- **`ttfautohint` CLI** — FreeType project; open source. Deterministic batch autohinting for TTF.
- **AFDKO `autohint`** — Adobe; open source. Batch autohinting for CFF/OTF.

---

## Practical recommendations

### Body text

- Don't force `-webkit-font-smoothing: antialiased`. Let the OS rasterize natively.
- `font-kerning: normal` and `font-variant-ligatures: common-ligatures` — explicit, no folklore dependency.
- Keep font-weight close to 400–500 for body; avoid `300` unless you're certain your audience is Retina-only.
- For web fonts, ensure autohinting is enabled (Google Fonts pipeline does this by default).

### Display text (≥ 30 px)

- `-webkit-font-smoothing: antialiased` is often preferable here. Outline fidelity matters more than grid-snap.
- Consider pairing with `text-rendering: geometricPrecision` for letter-perfect positioning.
- Stem darkening on macOS can make display text look unintentionally heavy; the `antialiased` thinning trick compensates.

### UI chrome at small sizes (10–12 px)

- Ship an autohinted static as a fallback if your variable font is unhinted.
- Test on low-DPI Windows (1920×1080 at 100% scaling). If stems are inconsistent, the font's hinting is inadequate.
- Consider a font designed for small sizes (Inter, IBM Plex, Roboto, SF Pro Text, Noto Sans UI).

### Cross-platform testing

- **Minimum test matrix**: macOS Safari, Windows 11 Chrome, Ubuntu 24.04 Firefox. These three represent the three rasterization philosophies.
- **Add if possible**: Windows 10 Chrome (DirectWrite on slightly older configs), iOS Safari (CoreText on Retina), Android Chrome (FreeType via Skia).
- **Don't assume macOS rendering is universal truth.** Mac-first design teams frequently ship websites that look thin on Windows and soft on Linux because they only tested on Mac.

### Variable fonts

- **Windows-heavy audience**: use Google Fonts autohinted variable builds, or ship an autohinted static fallback.
- **Retina-heavy audience**: unhinted variable is fine.
- **Mixed audience**: test at 12 and 14 px on a low-DPI Windows laptop. If acceptable, ship variable; if not, ship static + variable.

### Dark mode

- Apple's own apps and sites often use `-webkit-font-smoothing: antialiased` on dark mode body text specifically, to counteract the perceptual thickening of light-on-dark rendering.
- This is one of the few places where the `antialiased` trick is unambiguously justified: light-on-dark grayscale AA without stem darkening matches the designer's intended outline weight.

```css
@media (prefers-color-scheme: dark) {
  body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}
```

---

## Anti-patterns

### 1. Globally setting `-webkit-font-smoothing: antialiased`

Thin body text on macOS. On low-DPI Windows, no effect — but commonly paired with `font-weight: 300` that *does* affect Windows, producing unreadable thin Windows text.

### 2. Relying on `font-smooth` (the deprecated standard)

Never shipped in any modern engine. Only Safari 6-7 supported a partial implementation. Modern spec omits it. Vendor-prefixed `-webkit-font-smoothing` is the only practical control.

### 3. Assuming macOS rendering = cross-platform truth

The three rasterizers produce visibly different output from the same outline. Design with the middle in mind and test the extremes.

### 4. Disabling AA for "pixel-perfect" looks

`-webkit-font-smoothing: none` gives 1-bit rasterization. Ugly on every modern display. Only ever useful for intentional retro/8-bit aesthetics.

### 5. Over-hinting variable fonts

Aggressive autohinting across a variable axis produces "stair-stepping" — the rendered weight jumps at integer ppem transitions as hints snap different stems. Keep `--hinting-range-max` conservative for variable fonts (say, 30 ppem).

### 6. Shipping TTF with broken hinting tables

Subsetting tools that don't handle variable fonts correctly can corrupt `prep`/`fpgm`/`cvar` tables, producing a font that renders fine at most sizes but goes catastrophic at specific ppem. Symptom: the font looks fine at 14 px but letters overlap at 13 px. Fix: regenerate subset with `fonttools >= 4.43` and `pyftsubset` with `--layout-features='*'`.

### 7. `text-rendering: optimizeSpeed` on modern pages

Originally a performance tweak for low-end devices; in 2026 it suppresses kerning and ligatures for negligible perf win on desktop. Avoid. Use `auto` or `optimizeLegibility`.

### 8. `font-weight: 100` or `200` on low-DPI screens

Hairline weights rendered on 1× Windows displays with or without ClearType appear "gappy" — strokes become sub-pixel fragments. Ultra-light weights are Retina-only in practice.

### 9. Testing only on one monitor

Designers frequently test on their external 4K or MacBook Retina, missing how the site looks on an office 1080p monitor. Keep a low-DPI testing surface.

### 10. Mixing `text-rendering` levels within a page

Different elements at `optimizeLegibility` vs `optimizeSpeed` within the same text block can produce inconsistent kerning. Set `text-rendering` at `body` level and don't override unless you have a measured reason.

### 11. Forcing sub-pixel AA

There is no CSS to force sub-pixel AA where the OS has it off. `-webkit-font-smoothing: subpixel-antialiased` on macOS ≥ 10.14 is silently treated as default (grayscale + stem darkening). Don't rely on it to "bring back" the old Mac rendering.

### 12. Embedding `<meta name="theme-color">` and expecting it to affect text

Theme color affects browser chrome (toolbar, address bar), not text rasterization. Separate concerns.

### 13. Assuming Retina on mobile means rendering is "better"

Mobile Safari on iOS uses CoreText with no sub-pixel AA — fine on Retina. But Chrome Android uses FreeType, which may use sub-pixel on low-DPI devices. Cross-platform mobile rendering is not uniform.

### 14. Ignoring the `gasp` table

The `gasp` (grid-fitting and scan-procedure) table tells the rasterizer which behaviors to enable at which ppem. Tools that strip `gasp` (rare but possible with aggressive subsetting) produce fonts that render with the rasterizer's defaults everywhere, which may be wrong. Keep `gasp` intact.

---

## Sources

URLs retrieved **2026-04-18** unless noted.

### Primary specifications and documentation

- **FreeType documentation (main)**: https://freetype.org/freetype2/docs/documentation.html
- **FreeType hinting and text rendering**: https://freetype.org/freetype2/docs/hinting/text-rendering-general.html
- **FreeType sub-pixel hinting**: https://freetype.org/freetype2/docs/subpixel-hinting.html
- **FreeType `FT_LcdFilter` reference**: https://freetype.org/freetype2/docs/reference/ft2-lcd_rendering.html
- **`ttfautohint` documentation**: https://freetype.org/ttfautohint/doc/ttfautohint.html — covers `--hinting-range-min`, `--hinting-range-max`, `--windows-compatibility`, `--default-script`.
- **Microsoft Typography — ClearType portal**: https://learn.microsoft.com/en-us/typography/cleartype/ — historical whitepapers + current guidance.
- **Microsoft DirectWrite overview**: https://learn.microsoft.com/en-us/windows/win32/directwrite/direct-write-portal — `DWRITE_RENDERING_MODE`, `IDWriteRenderingParams`.
- **Microsoft OpenType spec (full)**: https://learn.microsoft.com/en-us/typography/opentype/spec/ — `gasp`, `cvt`, `cvar`, `fpgm`, `prep`, `gvar`, `HVAR`, `VVAR` reference tables.
- **Apple CoreText Programming Guide**: https://developer.apple.com/documentation/coretext
- **Apple Human Interface Guidelines — Typography**: https://developer.apple.com/design/human-interface-guidelines/typography
- **Chromium Blink `FontPlatformData`** (source reference): https://chromium.googlesource.com/chromium/src/+/refs/heads/main/third_party/blink/renderer/platform/fonts/
- **W3C CSS Fonts Module Level 4**: https://www.w3.org/TR/css-fonts-4/ — `font-kerning`, `font-variant-*`; `font-smooth` absent (deprecated).

### MDN browser compat

- **`text-rendering`**: https://developer.mozilla.org/en-US/docs/Web/CSS/text-rendering
- **`font-kerning`**: https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning
- **`font-smooth` (deprecated)**: https://developer.mozilla.org/en-US/docs/Web/CSS/font-smooth
- **`-webkit-font-smoothing` (non-standard)**: https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-font-smoothing
- **`image-rendering`**: https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering
- **`forced-color-adjust`**: https://developer.mozilla.org/en-US/docs/Web/CSS/forced-color-adjust
- **`text-size-adjust`**: https://developer.mozilla.org/en-US/docs/Web/CSS/text-size-adjust

### caniuse

- **`font-smooth`**: https://caniuse.com/mdn-css_properties_font-smooth — "deprecated; non-standard."
- **`text-size-adjust`**: https://caniuse.com/text-size-adjust
- **COLRv1**: https://caniuse.com/colr-v1 — all three engines ship stable as of 2026-04.

### Community writing

- **Typography.guru — "Font hinting explained"** (Ralf Herrmann): https://typography.guru/journal/hinting-explained/ — clear primer on TT vs CFF vs autohinting.
- **Smashing Magazine — "A Closer Look at Font Rendering"** (Tim Ahrens, 2012; still cited): https://www.smashingmagazine.com/2012/04/a-closer-look-at-font-rendering/ — definitive side-by-side of Windows vs Mac rendering. Predates Mojave.
- **Hrant Papazian — various writings on platform rendering** (TypeDrawers, Medium) — the most opinionated voice on the "hinting vs fidelity" schism.
- **Jeremy Keith (adactio)**: https://adactio.com/journal/2146 — notes on cross-browser rendering.
- **Zach Leatherman — "Web Fonts and font smoothing"**: https://www.zachleat.com/web/fonts-smoothing/ — the `-webkit-font-smoothing: antialiased` trick, dissected.
- **infinnie — "A programmer's guide to font rendering"**: https://infinnie.github.io/blog/2017/font-rendering.html — technical deep-dive on rasterization stages.
- **TypeDrawers discussion — macOS vs Windows rendering**: https://typedrawers.com/discussion/3387/rendering-differences-between-macos-and-windows — community consensus on what the philosophical split means for designers.

### Reference

- **Wikipedia — Font hinting**: https://en.wikipedia.org/wiki/Font_hinting
- **Wikipedia — ClearType**: https://en.wikipedia.org/wiki/ClearType
- **Wikipedia — Subpixel rendering**: https://en.wikipedia.org/wiki/Subpixel_rendering

### Authoring / pipeline

- **Google Fonts knowledge — Hinting**: https://fonts.google.com/knowledge/glossary/hinting — plain-language primer tied to the Google Fonts pipeline.
- **Google Fonts developer docs**: https://googlefonts.github.io/docs/ — pipeline details including autohinting invocation.
- **AFDKO (Adobe Font Development Kit for OpenType)**: https://github.com/adobe-type-tools/afdko — `autohint` tool for CFF.
