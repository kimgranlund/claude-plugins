---
date: 2026-04-18
coverage: medium
peers:
  - ./phototype-era.md
  - ./desktop-publishing.md
  - ./sans-grotesque.md
  - ./humanist-renaissance.md
  - ../contemporary/variable-fonts.md
  - ../contemporary/color-fonts.md
  - ../contemporary/font-delivery.md
  - ../techniques/optical-size.md
  - ../techniques/fallback-stacks.md
  - ../metrics/metrics-glossary.md
primary_sources:
  - Meggs, Philip B. & Purvis, Alston W. *Meggs' History of Graphic Design* (6th ed., Wiley, 2016)
  - https://opensource.googleblog.com/2016/09/introducing-opentype-font-variations.html
  - https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview
  - https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg
  - https://atypi.org/conferences-events/atypi-warsaw-2016/
  - https://github.com/googlefonts/amstelvar
  - https://github.com/googlefonts/roboto-flex
  - https://github.com/arrowtype/recursive
  - https://caniuse.com/variable-fonts
  - https://caniuse.com/colr-v1
  - https://caniuse.com/mdn-css_at-rules_font-face_opentype_colrv1
  - https://www.w3.org/TR/IFT/
  - https://www.w3.org/news/2025/w3c-invites-implementations-of-incremental-font-transfer/
  - https://en.wikipedia.org/wiki/IBM_Plex
  - https://en.wikipedia.org/wiki/Inter_(typeface)
  - https://rsms.me/inter/
  - https://klim.co.nz/
  - https://commercialtype.com/
  - https://grillitype.com/
  - https://abcdinamo.com/
  - https://pangrampangram.com/
  - https://ohnotype.co/
---

# Variable-font Era (2016-present) — historical reference

The variable-font era is the period opening at **ATypI Warsaw, September 14, 2016**, when Peter Constable (Microsoft), Ned Holbrook (Apple), Behdad Esfahbod (Google), and David Lemon (Adobe) jointly announced **OpenType 1.8** — the first time the four companies that between them own the majority of type-technology IP had shared a stage. The joke "the font wars are over" captures the significance. OpenType 1.8 unified **Apple's TrueType GX variations** (1991–2007), **Adobe's Multiple Masters** (1991–1998, a commercial failure), and **Microsoft's OpenType Font Variations** (in development since the early 2000s) into a single cross-vendor variable-font specification. Ten years later, variable fonts are a Baseline web-platform feature (caniuse 2026-04 global ~95.9%) and the default format for new type releases from most major foundries.

This file is the **medium-coverage historical reference** for the 2016-onwards era. For the deep **technical reference** on variable-font mechanics (axis registration, `fvar`/`gvar`/`avar`, interpolation semantics, CSS `font-variation-settings`, animation), see `../contemporary/variable-fonts.md` — this file focuses on the historical and market framing and cross-refs the technical reference whenever mechanics are relevant.

For the predecessor **desktop-publishing era** see `./desktop-publishing.md`; for the **phototype era** it inherited optical-sizing problems from, see `./phototype-era.md`.

---

## Origins — Multiple Masters, GX, OT 1.8

### Adobe Multiple Masters (1991–1998)

Adobe's **Multiple Masters** (MM) format was announced in March 1991 as an extension to PostScript Type 1. A Multiple Master font had two or more **master designs** at extreme points in a multi-dimensional design space (e.g., a Regular master at `wght=400, wdth=100` and a Bold master at `wght=900, wdth=100`); user software could blend between them to produce any intermediate weight, width, or both. Adobe released about 35 MM families between 1991 and 1998 — **Minion MM**, **Myriad MM**, **Jenson MM**, **Kepler MM**, **Cronos MM**, **Warnock MM**, **Tekton MM**, and others. Multiple Masters ran on Adobe Type Manager on Mac and Windows.

Multiple Masters was a commercial failure. Reasons commonly cited:
- **User-interface complexity.** Applications had to expose axis sliders to users; few did well.
- **Service-bureau incompatibility.** Imagesetters and RIPs often did not handle MM fonts correctly, producing output that didn't match the design-space instance the user had set.
- **Font-management complexity.** ATM, Suitcase, and other font managers handled MM fonts with bugs and quirks.
- **Adobe's own retreat.** Adobe stopped issuing new MM families after 1998, shipping only static instances from the MM masters.

By about 2000 Multiple Masters was dormant. Adobe's subsequent OpenType releases were static cuts drawn from the MM masters; the variable-interpolation capability was retained internally at Adobe but not exposed to the public. The format's value carried into OpenType 1.8 variable fonts in 2016.

### Apple TrueType GX (1991–2007)

Apple's **TrueType GX Variations** (announced 1991, shipped in QuickDraw GX on Mac OS 8 in the mid-1990s) was a parallel technology — design-space variations as a TrueType extension. GX introduced the core concepts (axes, masters, deltas) that would later become OpenType 1.8's vocabulary. GX was used internally at Apple for some system fonts and by a few foundries (Skia by Matthew Carter was an early GX font, 1994) but never gained wide adoption. QuickDraw GX itself was deprecated in Mac OS X. GX's specification survived as a document that informed later OpenType-variation work.

### OpenType 1.8 (September 2016)

OpenType 1.8 unified the GX and MM approaches into a single specification:
- **`fvar`** table declares the axes and named instances.
- **`gvar`** (for TrueType-flavor outlines) or **CFF2** (for PostScript-flavor outlines) stores variation deltas per glyph.
- **`avar`** allows per-axis non-linear remapping.
- **`HVAR`/`VVAR`/`MVAR`** handle metric variations.
- **`STAT`** declares axis value semantics (required).
- **Registered axes** (`wght`, `wdth`, `ital`, `slnt`, `opsz`) have interoperable semantics; **custom axes** (uppercase tag) are foundry-defined.

The full technical treatment is in `../contemporary/variable-fonts.md`. For historical framing it suffices to note that OT 1.8 in 2016 was the first cross-vendor, OS-level, browser-supportable variable-font specification — the technology MM and GX had prefigured, finally shipped as a platform primitive.

---

## First variable fonts (2016–2019)

### Decovar (David Berlow, Google Fonts + Font Bureau, 2017)

**Decovar** (Type Network and Font Bureau for Google Fonts; released early 2017) is an **experimental decorative** variable font with about 15 axes controlling skeleton style, terminal treatment, and inline detail. Decovar is not a production text face — it is a **showpiece** for what is mechanically possible in OpenType 1.8: extreme axis counts, continuous morphology, near-typographic-monster transitions between Roman capital, blackletter, rounded, and stenciled skeletons.

### Amstelvar (David Berlow, Google Fonts + Font Bureau, 2017–2018)

**Amstelvar** (Type Network / Font Bureau; Alpha release early 2017, 1.0 release 2018) is the **canonical parametric variable font** and the single most influential technical reference in the field. Amstelvar exposes `wght`, `wdth`, `opsz` as user-facing axes, plus a large set of **parametric axes** (the Berlow family: `XOPQ` thick stem, `YOPQ` thin stem, `XTRA` counter width, `YTLC` lowercase height, `YTUC` uppercase height, `YTAS` ascenders, `YTDE` descenders, `YTFG` figure height). The parametric model lets an end user manipulate stem weight, counter width, and per-class vertical metric independently of the compound `wght`/`wdth` axes. Amstelvar is the didactic reference cited in every OpenType 1.8 tutorial — see `googlefonts/amstelvar` on GitHub.

### Roboto Flex (Google + Font Bureau + Type Network, 2022)

**Roboto Flex** (first released September 2021 per Google Fonts; version 1.0 September 2022) takes the Amstelvar parametric approach and applies it to Google's workhorse **Roboto** family. Thirteen axes: `wght`, `wdth`, `slnt`, `opsz`, plus `GRAD` (grade) and the full Berlow parametric set (`XOPQ`, `YOPQ`, `XTRA`, `YTLC`, `YTUC`, `YTAS`, `YTDE`, `YTFI`). Demonstrates that the parametric-axes model can scale from a research-survey showcase (Amstelvar) to a production general-purpose family. Open-source under Apache 2.0 — see `googlefonts/roboto-flex`.

### Other early variable releases

- **Source Sans Variable** (Adobe, 2019) — variable version of Source Sans Pro (2012). One `wght` axis.
- **Source Serif Variable** (Adobe, 2020) — variable Source Serif 4. `wght` and `opsz`.
- **Fraunces** (Phaedra Charles + Undercase, 2020) — a "neoclassical" variable display family with `wght`, `opsz`, `SOFT` (soft/sharp treatment of terminals), and `WONK` (irregularity) axes. A good demonstration of idiosyncratic custom axes alongside registered axes.
- **Commissioner** (Kostas Bartsokas, 2020) — variable with `wght`, `wdth` and four custom axes (`FLAR` flare, `VOLM` volume, `SLNT`, and more). Released on Google Fonts.
- **Recursive Sans & Mono** (Stephen Nixon / Arrow Type, 2019–onwards) — variable with `wght`, `slnt`, `CASL` (casual — rational→signpainter), `MONO` (proportional→monospace), `CRSV` (cursive, controls italic letterforms separately from slant). Thesis project commissioned for completion by Google Fonts in 2019. Notable for being **metric-stable** across all axis moves — character widths don't change under `CASL` or `wght` adjustments, which makes Recursive animation-safe and code-safe.
- **Inter** (Rasmus Andersson, variable in 3.19, 2020) — the de-facto web-UI sans. See §Inter below.

---

## Browser support timeline (verified 2026-04)

**Variable fonts.** Per caniuse 2026-04, variable fonts are supported and are Baseline since approximately 2019. Specific browser shipping milestones:

- **Chrome / Chromium 62+** — October 17, 2017 (Chrome 62 beta released on that date with variable-fonts support, shipped stable by end of 2017).
- **Safari 11.1+** — March 2018 (on macOS 10.13 High Sierra and iOS 11; OS-dependent because Core Text handles variation).
- **Firefox 62+** — September 2018 (Gecko implementation, similarly OS-dependent for older Mac/Windows versions).
- **Edge 17+** — April 2018 (Edge on Windows 10; older EdgeHTML-based, shipped before the 2020 Chromium-Edge transition).

By 2020 variable fonts were effectively universal on evergreen browsers; 2026 global support is ~95.9%.

**`font-optical-sizing: auto`** (CSS Fonts L4). Per caniuse 2026-04:

- **Chrome 79+** (December 2019)
- **Firefox 62+** (September 2018)
- **Safari 13.1+** (March 2020); iOS Safari 13.4+
- **Edge 79+** (January 2020, Chromium-based)

Global support ~95.6%. See `../techniques/optical-size.md` for semantics.

**`@property` for custom properties driving `font-variation-settings` animation.** Per caniuse:

- **Chrome 85+** (August 2020)
- **Safari 16.4+** (March 2023)
- **Firefox 128+** (July 2024)

By 2026-04 `@property` is universal on evergreen browsers, which makes smooth per-axis variable-font animation practical cross-browser.

---

## COLRv1 color fonts

**COLRv1** (the color-font format published in OpenType 1.9, December 2021) extends the older **COLRv0** format (which had simple flat-color glyph layers) to support gradients, transforms, alpha blending, and composed-layer graphics inside a glyph. COLRv1 glyphs can contain linear, radial, and sweep gradients; affine transforms on layers; multiple blending modes; and — in conjunction with variable-font axes — animated color (axis value drives color-stop position, gradient angle, or layer transform).

### Browser support (verified 2026-04 from caniuse)

- **Chrome 98+** — February 2022 (COLRv1 rendering shipped).
- **Edge 98+** — February 2022.
- **Firefox 107+** — November 2022.
- **Safari**: **not supported as of 2026-04** per caniuse (`caniuse.com/colr-v1` and `caniuse.com/mdn-css_at-rules_font-face_opentype_colrv1`). Apple's position has been reluctant; the WebKit standards-positions discussion (`WebKit/standards-positions` issue #415) notes engagement but no ship. The practical effect in 2026: COLRv1 fonts render as **single-color** in Safari (all glyph layers composed to one ink color), whereas Chrome, Firefox, and Edge render them with full gradient/layer color.

### Fallback stack

Most 2024+ emoji fonts (Noto Color Emoji, Twemoji, Google Emoji) ship **dual COLRv1 + COLRv0** in the same file — COLRv1 primary, COLRv0 fallback. A browser that supports COLRv1 uses it; a browser with only COLRv0 support reads the COLRv0 table. Safari today falls back to COLRv0 if present (Apple Emoji system font uses sbix, a separate Apple format). For full COLRv1-specific detail see `../contemporary/color-fonts.md`.

---

## Open-source foundries and the open-source era

The variable-font era coincides with a substantial expansion of open-source typography. Key initiatives:

### IBM Plex (Mike Abbink + Bold Monday, 2017)

**IBM Plex** is IBM's corporate typeface, released under the SIL Open Font License in 2017 — replacing Helvetica as IBM's corporate face after more than fifty years. Plex is a superfamily designed by Mike Abbink at IBM in collaboration with **Bold Monday** (Dutch foundry, Paul van der Laan and Pieter van Rosmalen). The family:
- **IBM Plex Sans** (the workhorse)
- **IBM Plex Serif** (serif companion)
- **IBM Plex Mono** (monospace)
- **IBM Plex Sans Condensed**
- **IBM Plex Sans Arabic**, **IBM Plex Sans Devanagari**, **IBM Plex Sans Thai**, **IBM Plex Sans Hebrew**, **IBM Plex Sans KR/JP/SC/TC** (Korean, Japanese, Simplified Chinese, Traditional Chinese — the CJK cuts via Adobe)

All cuts variable (`wght`) since 2022. The Plex release is the clearest case of a major corporation publishing its brand face as open-source — a significant break from the 20th-century tradition of jealously-guarded corporate types.

### Google Noto (continuous expansion, 2010–onwards)

**Google Noto** is the ongoing initiative to provide font coverage for every Unicode script. "Noto" = "no tofu" (the placeholder square rendered for missing glyphs). As of 2026, Noto covers 150+ scripts and is substantially variable — Noto Sans, Noto Serif, Noto Emoji, Noto Color Emoji, and most script-specific cuts have variable variants. Released under the SIL Open Font License. See fonts.google.com/noto.

### Inter (Rasmus Andersson, 2016 onwards)

**Inter** (founded as "Interface" by Rasmus Andersson while at Figma, 2016; renamed Inter in 2017) has become the de-facto web-UI sans. Variable since 3.19 (2020). Version 4.0 (released 2023) integrated Inter Display into the main family as an `opsz` axis — the `opsz` variable Inter spans optical sizes roughly 14–32. Axes: `wght` (100–900), `slnt` (0° to -10°, right-leaning oblique), `opsz` (14–32). Open-source under SIL OFL. Adopted by GitHub, Mozilla, Vercel, the Linear app, Figma, and hundreds of design systems.

### Public Sans (US Government, 2020)

**Public Sans** is the US Web Design System's default sans. A modified fork of Libre Franklin. Public domain / MIT license. Variable `wght` axis. Released 2020 by the USWDS team.

### Google Fonts variable-first policy

Google Fonts' internal policy from about 2022 onwards prioritizes variable-font additions over static-only additions. As of 2026, the Google Fonts catalog has several hundred variable families. The Roboto family has been continuously redesigned and extended: **Roboto** (2011, original), **Roboto Condensed**, **Roboto Slab**, **Roboto Mono**, **Roboto Serif**, and **Roboto Flex** (2022). All major cuts are variable.

### Other notable open-source releases

- **JetBrains Mono** (JetBrains, 2020) — developer monospace. Variable `wght`.
- **Geist** (Vercel, 2023) — geometric sans. Variable.
- **Fira Code** (Nikita Prokopov, 2014, continued) — programming ligatures monospace. Variable since 2022.
- **DM Sans** (Colophon Foundry for Google, 2019) — geometric sans.
- **Spectral** (Production Type for Google, 2017) — serif.
- **Source Sans 3** and **Source Serif 4** (Adobe, variable) — open-source under Apache 2.0.

The cumulative effect: professional-grade variable-font typography is available at zero cost for most mainstream use cases.

---

## Generative and AI type tools (2022–2026)

A newer strand of typography tooling uses algorithmic or AI-driven generation:

- **Metaflop** (Alexis Reigel + Marco Müller, ~2014) — earlier parametric-typeface generation, based on Metafont (Donald Knuth, 1977). Web interface for manipulating Metafont-style parameters.
- **Prototypo** (2015 onwards; Yannick Mathey + Louis-Rémi Babé) — web-based parametric-typeface editor. Exports to Type 1 / OpenType. Aimed at non-type-designers producing custom faces.
- **Fontue** and related — small 2020s tools continuing the parametric approach.
- **Glyphs 3 and variable-font tooling** (Glyphs GmbH, 2020 onwards) — the macOS type-design application added sophisticated variable-font export, interpolation-compatibility checking, and `fvar`/`STAT` authoring.
- **FontLab 8** (2022) — cross-platform type-design tool with comparable variable-font authoring.
- **Generative AI typefaces** — experimental only as of 2026-04. Examples: Speculum (experimental, 2023), various OpenAI and Google Research demonstrations of text-to-font generation. Current quality of AI-generated fonts is mixed — novelty display faces can be produced convincingly, but text-quality body fonts still require human refinement.
- **Hybrid workflow** — a commonly-cited pattern is AI-generated exploration (initial alphabet, display variants) followed by human refinement in Glyphs or FontLab. Several 2024–2026 releases are documented as using this pattern. No canonical AI-generated commercial release has yet entered mainstream use.

---

## Characteristics and uses of variable-era type

### One file, many instances

A variable font ships as one file (typically WOFF2 on the web; OTF/TTF for install). That file contains axis records (`fvar`), variation deltas (`gvar`/CFF2), and named instances (preset points in design space). Selecting weight, width, slant, and optical size at render time is a continuous operation, not a discrete font-switch.

For technical detail on CSS wiring (`font-weight`, `font-stretch`, `font-variation-settings`, `font-optical-sizing`) and animation semantics (`@property`, interpolation rules), see `../contemporary/variable-fonts.md` §CSS-surface and §animation.

### File size

Variable fonts are larger than a single-weight static cut but smaller than a multi-weight family-total. Representative numbers (see `../contemporary/variable-fonts.md` §file-size):

- 1 weight static WOFF2: ~25 KB
- 2 weights static (regular + bold): ~50 KB
- Variable WOFF2 with `wght` axis: ~90 KB
- 6 weights + italic static bundle: ~300 KB
- Variable WOFF2 with `wght` + `ital`: ~180 KB

The break-even point is roughly 3 weights. For typical web-UI usage (body regular + bold, maybe semi-bold and an italic) variable is neutral or slightly smaller. For editorial or display usage with many weights, variable wins decisively.

### Optical sizing returns

`opsz` (registered in OT 1.8) is the variable-font answer to the phototype era's loss of optical sizing (see `./phototype-era.md` §optical-sizing-loss). Faces shipping useful `opsz` axes in 2026:

- **Roboto Flex** — `opsz` 8–144
- **Inter 4.0+** — `opsz` 14–32
- **Source Serif 4 Variable** — `opsz` full range
- **Helvetica Now Variable** (Monotype, 2019 initial; variable 2024) — Micro / Text / Display cuts as `opsz` axis
- **Myriad Variable** (Slimbach, 2023) — `opsz` axis across the Myriad family
- **Literata Variable** (Type Network for Google, 2019 onwards) — editorial serif with `opsz`
- **Minion 3 / Minion Variable** (Slimbach, Adobe, 2020 onwards) — classic Aldine with `opsz` restored

The combination of `font-optical-sizing: auto` in CSS + an `opsz`-axis variable font automatically restores size-specific refinement that was universal in metal, lost in phototype, and absent from most digital fonts of 1990–2015.

### Responsive typography

Variable fonts make fluid typographic adjustment cheap. A `wght` axis linked to viewport size via CSS:

```css
body {
  font-weight: calc(400 + (500 - 400) * ((100vw - 320px) / (1440 - 320)));
}
```

...lets body weight scale continuously from 400 on narrow viewports (where thinner weight improves screen-readability at small sizes) to 500 on larger viewports. Similar for `opsz`, `wdth`, `GRAD`. Entire design approaches ("fluid typography," "responsive type") are variable-font-era patterns.

---

## Custom vs registered axes — a practical note

OpenType 1.8 splits axis tags at the **first-letter case**:
- **Lowercase registered axes** (`wght`, `wdth`, `ital`, `slnt`, `opsz`) have high-level CSS properties (`font-weight`, `font-stretch`, `font-style`, `font-optical-sizing`). Setting these properties applies to the registered axis idiomatically, inherits correctly, composes with `font-synthesis`, and respects user-agent stylesheets (`<strong>`, `<em>`).
- **Uppercase custom axes** (`GRAD`, `MONO`, `CASL`, `CRSV`, `XOPQ`, `YOPQ`, `XTRA`, `YTLC`, `YTUC`, and foundry-specific axes) have **no high-level CSS properties**. They must be set via `font-variation-settings: "TAG" value`.

The **practical gotcha**: the CSS property `font-variation-settings` is treated atomically by the cascade. Writing `font-variation-settings: "GRAD" 100` on an element **resets all other axes** (including `wght`, `wdth`, `opsz`) to their axis defaults, because the entire FVS value is replaced. This is a major source of bugs.

The correct idiom for mixed registered + custom axes is to **set all axes together in one `font-variation-settings` value**, or use `@property`-registered CSS custom properties to drive individual axes. See `../contemporary/variable-fonts.md` §CSS-wiring-matrix for the full pattern.

---

## 21st-century foundries active in the variable era

An incomplete list of foundries whose output defines variable-era 2020s typography. For each, see the foundry's site for current catalog.

- **Klim Type Foundry** (New Zealand; **Kris Sowersby**, founded 2005) — **Söhne** (2019, neo-grotesque Akzidenz/Helvetica revisit), **Signifier** (2020, didone/transitional hybrid), **Epicene** (2021, Didone), **Untitled Sans / Untitled Serif**, **National 2**, **Söhne Breit / Mono**. Klim's Söhne and National are ubiquitous in 2020s editorial and brand design (NYTimes, The Verge, Shopify, many startups). klim.co.nz.
- **Commercial Type** (New York / London; **Paul Barnes** + **Christian Schwartz**, founded 2004) — **Graphik** (Schwartz, 2009), **Lyon** (Kai Bernau, 2009, editorial serif), **Marian** (Barnes, 2012), **Druk** (Schwartz, extreme condensed display), **Stanley** (2018), **Larish Neue** (2023). commercialtype.com.
- **Grilli Type (GT)** (Zurich; **Thierry Blancpain** + Reto Moser, founded 2009) — **GT America** (2016, American-grotesque × European-neo-grotesque synthesis, six widths), **GT Sectra** (2014, angular Venetian-inspired serif), **GT Walsheim** (2010, geometric sans), **GT Cinetype** (2023), **GT Pressura** (2019). grillitype.com.
- **Dinamo** (Basel / Berlin; founded 2016, **Johannes Breyer** + **Fabian Harb**) — **ABC Diatype**, **ABC Gravity**, **ABC Monument Grotesk**, **ABC Arizona**, **ABC Repro**. Swiss-aesthetic with technical precision. abcdinamo.com.
- **Pangram Pangram** (Quebec; founded 2018) — **Neue Machina** (2019), **Editorial New** (2020), **Migra**, **Object Sans**. Notable for accessible licensing model (personal-use free, commercial paid). pangrampangram.com.
- **Displaay** (Prague; founded 2015) — **Harbour** (2017), **Dinosaur**, **Reckless Neue** (2020 onwards), **Pangea** (2022). displaay.net.
- **Production Type** (Paris; founded 2014, **Jean-Baptiste Levée**) — **Spectral** (2017, for Google Fonts, variable editorial serif), **Messina** (2018), **Gerstner Programm** revivals (2020 onwards of Karl Gerstner's 1960s Programm), **Mongoose**, **Gemeli**. productiontype.com.
- **Hoefler & Co.** (New York; see `./desktop-publishing.md` for pre-2014 history) — **Obsidian** (2015, a variable-like decorative Didone with optically-aware terminals predating OT 1.8), **Operator** (2016, monospace), **Peristyle**, **Decimal**. typography.com.
- **Frere-Jones Type** (New York; Tobias Frere-Jones, founded 2015 after the 2014 split) — **Mallory** (2015), **Retina** (re-released 2016 after the original's 1999 WSJ commission ended), **Empirica** (2018). frerejones.com.
- **OH no Type Co** (California; **James Edmondson**, founded 2015) — **Obviously** (a variable-font-era variable-width display family), **Eksell Display** (2019 revival of Olof Eksell), **Hobeaux**. ohnotype.co.
- **Sharp Type** (New York; Chantra Malee + Lucas Sharp, founded 2015) — **Sharp Grotesk** (2017, massive 126-font family), **Sharp Sans**, **Beatrice** (2019). sharptype.co.
- **Milieu Grotesque** (Berlin) — **Patron**, **Generika**, **Programm**, **Lacrima**.
- **Colophon Foundry** (London; founded 2009) — **Monument Grotesk** (distinct from Dinamo's Monument Grotesk; Colophon's was earlier), **Reader**, **Panel Sans**, **Apercu**. Also author of **DM Sans** (for Google, 2019). colophon-foundry.org.
- **Emigre** (Berkeley; see `./desktop-publishing.md` §Emigre) — continues publishing. Notable anniversaries: 40th in 2024.
- **Lineto** (Zurich / Berlin; **Stephan Müller**, **Cornel Windlin**, **Laurenz Brunner**, founded 1998) — **Akkurat** (Brunner, 2004), **Circular** (Brunner, 2013, widely used in tech-brand identity), **Replica** (Norm, 2008), **Brown** (Brunner, 2011). lineto.com.

---

## The future — 2025–2030 signals

### Incremental Font Transfer (IFT)

**W3C Incremental Font Transfer** is a standards effort to enable **glyph-level streaming** of variable fonts — delivering only the glyphs actually used by a page, over HTTPS, progressively as content renders. Without IFT, a browser must download every byte of a font before rendering any character with it (subsetting by `unicode-range` helps but has granularity and script-safety limits). IFT would replace that with a request/response protocol where the client receives only the glyphs it needs.

**Status as of 2026-04** (verified against W3C, caniuse, and W3C news): IFT was published as a **W3C Candidate Recommendation Draft on November 18, 2025** (W3C News, November 2025; `w3c/IFT` GitHub repo). W3C invited implementations on that date. A Chrome feature flag for IFT support is planned for 2026 per Chrome's public roadmap (April 2026 note). No browser has shipped IFT to stable as of 2026-04; the feature is experimental-behind-flag in Chromium-based builds. No implementation in Firefox or Safari stable.

### COLRv1 Safari parity

The major outstanding browser gap in variable-era typography is **Safari COLRv1**. Chrome, Firefox, Edge have shipped it (2022). Safari has not shipped it by 2026-04. Until Safari ships COLRv1, COLRv1-only color fonts will render single-color on Safari — which makes COLRv1-first designs a risky choice for general-web use. Dual-delivery (COLRv1 + COLRv0 + sbix fallback) remains the safe pattern.

### Parametric axes formalization

David Berlow's parametric-axes model (`XOPQ`, `YOPQ`, `XTRA`, `YTLC`, `YTUC`, `YTAS`, `YTDE`, `YTFG`), which is custom in 2026, could plausibly be formalized as registered axes in a future OpenType revision. Formal registration would give the parametric model high-level CSS properties and standard interoperable semantics. As of 2026-04, no such registration is announced; Microsoft's axis registry documentation encourages registration proposals when multi-foundry adoption and application-level selection make the case.

### AI-generated fonts

Expect the quantity of AI-generated font releases to increase substantially 2026–2030; expect the quality to bifurcate (AI for exploratory drafts and novelty display faces, human-refined for production text faces). Hybrid human+AI workflows are likely to dominate production work.

### Variable Color Fonts

Variable + COLRv1 (color stops, gradient angles, layer transforms as animation-driven axes) is a combined frontier. Nabla (Arthur Reinders Folmer + Just van Rossum, 2022) is the archetypal variable-color font with `wght`, `EDPT` (depth), `EHLT` (highlight) driving gradient geometry. See `../contemporary/color-fonts.md`.

---

## How type-design practice changed

The variable-font era has changed how type is designed, not only how it is delivered. A few of the practitioner-level shifts:

### From static cuts to design-space authoring

Pre-2016 type design produced a discrete set of static weights (Light, Regular, Medium, Bold, Black; maybe Italic variants of each). A designer drew each weight, checked optical consistency pairwise, and shipped them as separate files.

Variable-font design is **design-space authoring**. Masters at the design-space extremes (Thin + Black, say) are drawn; the tool (Glyphs 3, FontLab 8, Fontmake via UFO + designspace) interpolates every intermediate weight. This changes the design process:

- **Every glyph must be interpolation-compatible across all masters**: same number of contours, same point count, same off-curve structure. A mismatch anywhere — one stray point, one reordered contour — breaks the font.
- **Intermediate weights may need designer intervention.** Linear interpolation between Thin and Black rarely produces a perfectly-tuned Medium. Designers add intermediate masters (Light, Regular, Medium, Bold as supplementary points in design space) or use `avar` to non-linearize the axis.
- **Hinting is harder.** TrueType instructions must work across the full design space. Auto-hinting coverage for variable ranges remains imperfect; some foundries ship hinted statics alongside an unhinted variable.
- **QA combinatorics explode.** Testing every (wght × wdth × opsz × ital) combination is intractable. Named instances become the testable basis; continuous interpolation is tested statistically.

See `../contemporary/variable-fonts.md` §authoring-notes for practitioner detail.

### Font-specimen culture evolves

Font specimens — the foundry's promotional pages showing a typeface's character set, weight range, and editorial personality — have evolved to **interactive specimens**. A 2020s specimen page (e.g., Recursive's recursive.design, Inter's rsms.me/inter, Dinamo's abcdinamo.com) offers real-time axis sliders, letting the visitor manipulate `wght`, `wdth`, `opsz`, `GRAD`, `MONO`, `CASL` directly and see typed text re-render. This is a direct consequence of variable-font shipping and browser rendering.

Specimens have also become more technically transparent: published `fvar` axis definitions, named-instance lists, `STAT` tables, code examples for CSS `font-variation-settings`. Foundries with deeply-documented technical specimens (Klim, Grilli Type, Production Type, Arrow Type) contrast with legacy foundries (Monotype, ITC) whose specimen pages are often still static-font-catalog-style.

### Licensing evolution

Variable fonts complicate traditional font licensing. A legacy per-weight license (common in the 1990s–2000s: "license 4 weights") doesn't fit a variable file that exposes any weight on a continuous axis. Foundries have moved toward:

- **Per-family licenses** covering the full variable file with all axes.
- **Per-usage tiers** (desktop, web, app, ebook) rather than per-weight.
- **Volume-based pricing** (audience size, page-views, app-installs) for web and app use.
- **Subscription** models (Adobe Fonts / Typekit, Monotype Fonts, Klim's Klim+, Hoefler's Cloud.typography) that sidestep per-file licensing entirely.

Open-source release (SIL OFL for Inter, IBM Plex, Roboto, Public Sans; Apache 2.0 for Source Sans / Serif; MIT for Public Sans) has expanded substantially. The variable-era open-source catalog covers most mainstream use cases without commercial licensing.

---

## Anti-patterns for the variable-font era

| Pattern | Why it's wrong | Fix |
|---|---|---|
| Shipping a variable font without subsetting unused glyph ranges | Variable delivers tens of kilobytes of delta data per unused glyph. Shipping full Latin + Cyrillic + Greek ranges when only Latin is used bloats transfer. | Subset by `unicode-range` per `@font-face`, split into Latin / Cyrillic / Greek subsets. Browser downloads only what the page uses. See `../contemporary/font-delivery.md`. |
| Animating `font-variation-settings` on a large body of text without `will-change` | Continuous axis animation invalidates glyph caches frame-by-frame; can cost significant repaint time on large documents. | Limit animation to headlines or small spans. Use `will-change: font-variation-settings`. Use `@property`-registered custom property driving a single axis rather than animating the full FVS string. See `../contemporary/variable-fonts.md` §animation. |
| Setting a custom axis via `font-variation-settings` without re-specifying registered axes | FVS replaces all axes; registered axes (wght, wdth, etc.) snap back to axis defaults. Visible as unwanted weight/width changes. | Include *all* axes in every FVS value, or set registered axes with high-level properties and custom axes with FVS in the same rule. |
| Using a variable font for only one point in its design space | Variable delta data (fvar, gvar, HVAR tables) is pure overhead when a single weight is all that's used. | Ship a static single-cut WOFF2 for the specific weight. Use `fonttools varLib.instancer` to freeze axes. |
| Variable fonts as a brand "statement" without exercising the range | A variable font labeled "variable" but used at one weight is typographically identical to the equivalent static, with extra file size. | Either use the range (animations, responsive weight, `opsz` auto), or ship static cuts. |
| Relying on `font-named-instance` in production (2026) | Cross-browser implementation uneven; Chromium partial, Safari partial, Firefox proposal stage. | Set axis values explicitly via `font-weight` / `font-stretch` / `font-variation-settings`. Revisit named instances when implementation consolidates. |
| Pairing a non-`opsz` variable font with `font-optical-sizing: auto` expectation | `font-optical-sizing: auto` is a no-op on fonts without an `opsz` axis — no error, no surprise, but also no optical adjustment. | Check font for `opsz`-axis support (fvar inspector, v-fonts.com). Use fonts with actual `opsz` for optical-sizing workflows. |
| Treating `slnt` (oblique) as italic substitute when the font also has an `ital` axis or an italic cut | A slanted Roman lacks the designed italic glyphs (single-storey `a`, `g`, different `f`, etc.). | Use `font-style: italic`, which maps to `ital 1` or to a separately-loaded italic cut. See `../contemporary/variable-fonts.md` §slnt-vs-ital. |
| Assuming Safari supports COLRv1 in 2026 | Safari still does not support COLRv1 as of 2026-04 per caniuse — COLRv1 glyphs render flat/single-color. | Ship dual COLRv1 + COLRv0 fonts. Test on Safari. See `../contemporary/color-fonts.md`. |
| Mapping CSS `oblique 10deg` to `slnt 10` in `font-variation-settings` | Sign flip: CSS positive degrees = rightward slant; `slnt` is counter-clockwise, so rightward slant = negative `slnt` value. Result: font slants the wrong way. | CSS `oblique 10deg` → `"slnt" -10`. See `../contemporary/variable-fonts.md` §slnt-axis. |

---

## Cross-references

- For the **deep technical mechanics** of variable fonts — axis registration, `fvar`/`gvar`/`avar`/`STAT`, interpolation, CSS surface, animation — see `../contemporary/variable-fonts.md`. This is the authoritative technical reference; the current file is the historical/era framing.
- For **COLRv1 color fonts** in depth, see `../contemporary/color-fonts.md`.
- For **font delivery, subsetting, `unicode-range`, IFT** — see `../contemporary/font-delivery.md`.
- For the **phototype-era optical-sizing loss** that `opsz` restores, see `./phototype-era.md`.
- For the **desktop-publishing era** that preceded and set up the variable-font era, see `./desktop-publishing.md`.
- For **contemporary sans-serifs** actively using variable axes (Inter, Söhne, Roboto Flex, SF Pro, Geist, Recursive), see `./sans-grotesque.md` §21st-century-sans.
- For **optical-size technique and `font-optical-sizing` semantics**, see `../techniques/optical-size.md`.

## Sources

- **Google Open Source Blog**, "Introducing OpenType Font Variations" (Behdad Esfahbod, September 14, 2016). https://opensource.googleblog.com/2016/09/introducing-opentype-font-variations.html.
- **Microsoft Learn**, "OpenType Font Variations overview" (OT 1.9.1, 2024-05-30). https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview.
- **Microsoft Learn**, "OpenType Design-Variation Axis Tag Registry" (2024-05-29). https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg.
- **ATypI Warsaw 2016** conference program. https://atypi.org/conferences-events/atypi-warsaw-2016/.
- **Type Network / Font Bureau**, "Finesse and Express" — David Berlow on parametric axes. https://typenetwork.com/articles/finesse-and-express.
- **Google Fonts** — `googlefonts/amstelvar`, `googlefonts/roboto-flex` GitHub repositories.
- **Arrow Type** — `arrowtype/recursive` GitHub repository; recursive.design process notes.
- **caniuse.com**: Variable fonts (https://caniuse.com/variable-fonts), COLR/CPAL(v1) (https://caniuse.com/colr-v1), @font-face opentype colrv1 (https://caniuse.com/mdn-css_at-rules_font-face_opentype_colrv1), `font-optical-sizing` (https://caniuse.com/mdn-css_properties_font-optical-sizing). Retrieved 2026-04-18.
- **WebKit Standards Positions**, "COLRv1 fonts" — WebKit/standards-positions issue #415. https://github.com/WebKit/standards-positions/issues/415.
- **W3C Incremental Font Transfer (IFT)** — https://www.w3.org/TR/IFT/ (Candidate Recommendation Draft, 2025-11-18) and W3C news https://www.w3.org/news/2025/w3c-invites-implementations-of-incremental-font-transfer/.
- **IBM Plex** — https://www.ibm.com/plex/, https://en.wikipedia.org/wiki/IBM_Plex.
- **Inter** (Rasmus Andersson) — https://rsms.me/inter/, https://en.wikipedia.org/wiki/Inter_(typeface), `rsms/inter` GitHub issues and discussions (including #411 `opsz` axis request, discussion #463 v4 release).
- **Klim Type Foundry** — https://klim.co.nz/. Kris Sowersby's essays are the best contemporary foundry-practitioner documentation.
- **Commercial Type** — https://commercialtype.com/.
- **Grilli Type** — https://grillitype.com/.
- **Dinamo** — https://abcdinamo.com/.
- **Production Type** — https://productiontype.com/.
- **OH no Type Co** — https://ohnotype.co/.
- **Hoefler & Co.** — https://www.typography.com/.
- **Frere-Jones Type** — https://frerejones.com/.
- **v-fonts.com** (Nick Sherman) — variable-fonts catalog, 377+ families as of 2026-04. https://v-fonts.com/.
- **Philip Meggs & Alston Purvis**, *Meggs' History of Graphic Design* (6th ed., Wiley, 2016) — historical context.
- Wikipedia pages on named faces, foundries, and technologies referenced above. Current articles on *OpenType*, *Variable font*, *TrueType GX*, *Multiple Masters*, *OpenType Font Variations* are reasonably sourced.
