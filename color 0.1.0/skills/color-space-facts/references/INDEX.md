# Color Science — Spaces References

Curated transcripts, notes, and source material for the `color-space-facts` pack — computational
color: spaces, conversions, gamut, gradients/ramps, ΔE, HDR/tone mapping, CSS color syntax,
quantization/dithering/extraction, palette-generation methods, and the library/tool catalog.

**72 files** across 2 categories: `contemporary/` (11 — modern space/pipeline explainers) and
`techniques/` (61 — math references and technique/tool notes). No `historical/` files live in this
pack (the 5 historical files split to `color-material-facts` and `color-perception-facts`); no
scrape sites live here either (the David Briggs huevaluechroma.com and colorandcontrast.com scrapes
moved whole to `color-perception-facts`).

**Lineage (2026-07-06):** extracted from the monolithic `color-science` pack alongside three
siblings — `color-perception-facts` (vision/appearance science), `color-contrast-facts`
(contrast standards & CVD), `color-material-facts` (pigment, print, naming) — plus the earlier
`color-theory-facts` split (2026-07-02, harmony/meaning/history). Full prior history lives in
`color-science-project-files`'s changelog; the
TypeScript library + demo site this pack's math files pair with now live at
[`color-science-project-files/src/`](../../../color-science-project-files/src/) (see each techniques
file's own "Implementation" section for the paired module).

## Consult map — the pack's 6 axes

| Axis | Ask | Where |
|---|---|---|
| 1. Spaces & conversions | OKLab/OKLCH, CIELAB, CAM16/HCT, HSL/HSV limits, white points, adaptation, CIE 1931 | §Contemporary + §Techniques → Libraries & Code (space-math rows) |
| 2. Gamut & interpolation | peak chroma, cusp, CSS gamut mapping, gradients, hue paths, ramps, splines, cubehelix, ΔE | §Techniques → Libraries & Code |
| 3. HDR & tone mapping | PQ/HLG, Jzazbz/ICtCp, Reinhard/ACES | §Techniques → Libraries & Code (jzazbz-ictcp-math, tone-mapping-operators) |
| 4. CSS color syntax & status | color-mix, relative color, light-dark, Baseline snapshot | §Techniques → Libraries & Code (w3c-css-color-4-and-5, css-color-2026-snapshot, css-color-generation-technique) |
| 5. Image palettes & quantization | k-means, dithering, extraction tools, sorting | §Techniques (color-quantization-math, dithering-algorithms, image-color-extraction-tools, colorsort-js, censor-palette-analyser) + §Contemporary (palette-based-photo-recoloring, gao-color-palette-generation-review) |
| 6. Palette-generation methods & library/tool catalog | IQ cosine, generative-artist techniques, Culori/Color.js, Tailwind/Radix | §Techniques → Practical Methods & Design Application + §Library & Tool Catalog |

Grep the axis term in this file first, then Read only the matching row's file (with offset for long
files) — this corpus is a catalog, not a linear read.

## Contemporary

| File | Summary | Source |
|---|---|---|
| [Web-Safe Colors](contemporary/web-wheel-web-safe-colors.md) | 216 colors (6 hex values per channel). Linda Weinman 1996. Relevant ~1996–2006. | [Color Nerd](https://www.youtube.com/shorts/B1tfImuPTcA) |
| [CIECAM16 & CAM16-UCS — Positioning](contemporary/ciecam16-cam16-ucs.md) | Why CIECAM16 supersedes CIECAM02 (CAT16 fixes the non-invertible adaptation matrix) and CAM16-UCS is the CIE-recommended uniform space. Positioning companion to the `techniques/` math files. | [CIE 248:2022](https://cie.co.at/publications/cie-2016-colour-appearance-model-colour-management-systems-ciecam16) |
| [Material HCT — Positioning](contemporary/material-hct-color-space.md) | HCT = CAM16 hue + CAM16 chroma + CIE L\* tone: Google's Material 3 dynamic-color space, among the most-deployed perceptual spaces in production. Companion to `techniques/material-hct-math.md`. | [Material 3](https://m3.material.io/styles/color/system) |
| [Palette-based Photo Recoloring](contemporary/palette-based-photo-recoloring.md) | Interactive recoloring by editing a compact palette. Lab-space transfer, smooth falloff, gamut handling, and luminance constraints make palette editing practical for non-experts. | PDF (not shipped with this pack; canonical at Chang et al. 2015) |
| [Gao — Palette Generation Review](contemporary/gao-color-palette-generation-review.md) | 2025 review of image-derived palette generation. Compares color spaces, histogram/clustering/neural methods, and evaluation metrics for palette quality. | [DOI](https://doi.org/10.1002/col.22975) |
| [Colourspaces — Computerphile](contemporary/computerphile-colourspaces.md) | RGB, CMYK, YCbCr explained. Chroma subsampling. 251K views. | [Computerphile](https://www.youtube.com/watch?v=LFXN9PiOGtY) |
| [Your Colors Suck — Acerola](contemporary/your-colors-suck-acerola.md) | Full pipeline: CIE matching → XYZ → sRGB → HSL (broken) → OKLAB. 628K views. | [Acerola](https://www.youtube.com/watch?v=fv-wlo8yVhk) |
| [Everything About Color 25 Min](contemporary/everything-about-color-25min.md) | Full pipeline overview. OKLCH recommended. Display tech. 471K views. | [Juxtopposed](https://www.youtube.com/watch?v=srRI7yMjGz0) |
| [Björn Ottosson — OKLAB Articles](contemporary/bjorn-ottosson-oklab-articles.md) | All 4 foundational posts: OKLAB (outperforms CIELAB on L+C+H), "How Software Gets Color Wrong" (blend in linear not sRGB), OKHSV/OKHSL (8 picker properties, 3-point chroma interpolation), Gamut Clipping (adaptive α=0.05). | [bottosson.github.io](https://bottosson.github.io/posts/) |
| [OKLAB in Minecraft](contemporary/oklab-perceptual-color-space-minecraft.md) | Best perceptual uniformity demo. Conversion pipeline. 201K views. | [Gneiss Name](https://www.youtube.com/watch?v=nJlZT5AE9zY) |
| [CIE 1931 — Standard Observer, XYZ, and Color Matching Functions](contemporary/cie-1931-standard-observer.md) | Foundational reference for the 2° standard observer, XYZ, xyY, metamerism, and spectral-to-tristimulus conversion. The base layer under Lab, ICC workflows, and most modern color libraries. | [CIE DOI](https://doi.org/10.25039/CIE.DS.xvudnb9b) |

## Techniques (Tools, Libraries, Methods)

### Libraries & Code

| File | Summary | Link |
|---|---|---|
| [@texel/color](https://github.com/texel-org/color) | Minimal, 5–125× faster than Color.js. Zero deps, tree-shakeable (~3.5kb). OKLab/OKLCH/OKHSL/sRGB/P3/Rec2020. Fast gamut mapping. For real-time/generative art. | [GitHub](https://github.com/texel-org/color) |
| [Bruce Lindbloom — Color Math](techniques/brucelindbloom-color-math.md) | THE reference for color conversion equations: RGB↔XYZ matrices, chromatic adaptation (Bradford), Lab/LCH conversions, spectral→XYZ. Online calculators, Lab gamut visualization. | [brucelindbloom.com](http://www.brucelindbloom.com/) |
| [OKLCH Gamut Peak Math](techniques/oklch-gamut-peak-math.md) | Mathematical derivation for $L_\text{peak}(C, h)$ and $C_\text{peak}(L, h)$ in OKLCH against sRGB / Display P3 / Rec.2020 gamuts. Ottosson $M_1$/$M_2$ matrices, XYZ→RGB matrices, the cubic-in-$L$ envelope, binary search + analytic algorithms, production library map. | [Ottosson](https://bottosson.github.io/posts/oklab/) / [Gamut clipping](https://bottosson.github.io/posts/gamutclipping/) |
| [OKLab ↔ XYZ Math](techniques/oklab-xyz-math.md) | Ottosson's perceptual color space. $M_1$/$M_2$ matrices (and inverses), cube-root nonlinearity, polar OKLCH form, edge cases. Paired with `src/spaces/oklab.ts` + `src/spaces/oklch.ts`. | [Ottosson 2020](https://bottosson.github.io/posts/oklab/) |
| [CIELAB ↔ XYZ Conversion](techniques/cielab-xyz-conversion.md) | The canonical 1976 perceptual space. $f(t)$ cube-root nonlinearity, D65/D50 white-point handling, polar CIELCH form, when to use OKLab instead. Paired with `src/spaces/cielab.ts`. | [CIE 015:2018](https://www.w3.org/TR/css-color-4/#lab-colors) |
| [Gamma Transfer Functions](techniques/gamma-transfer-functions.md) | The piecewise gamma functions for sRGB / Display P3 / Rec.2020 / Rec.709 / PQ / HLG. Sign-preserving formulas, edge cases, when to apply each. Paired with `src/transfer/{srgb,rec2020,pq,hlg}.ts`. | [IEC 61966-2-1](https://www.w3.org/TR/css-color-4/) / [BT.2100](https://www.itu.int/rec/R-REC-BT.2100/) |
| [XYZ ↔ RGB Conversion Matrices](techniques/xyz-rgb-conversion-matrices.md) | The 3×3 matrices for sRGB / Display P3 / Rec.2020 / Rec.709 ↔ XYZ-D65. W3C CSS Color 4 high-precision values. Derivation from primaries + white point. Paired with `src/spaces/{srgb,p3,rec2020}.ts`. | [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/) |
| [Cylindrical RGB Conversions (HSL & HSV)](techniques/cylindrical-rgb-conversions.md) | Non-perceptual cylindrical reparameterizations of encoded sRGB. Hue sector formulas, HSL vs HSV geometry, why neither is perceptual. Paired with `src/spaces/{hsl,hsv}.ts`. | [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/#the-hsl-notation) |
| [Color Difference (ΔE Formulas)](techniques/delta-e-formulas.md) | The five ΔE variants — ΔE76, ΔE94, ΔE2000 (with full rotational term), ΔE_ok, HyAB. Sharma test pairs verified. When to use which; the termination criterion `css-color-4-gamut-mapping`'s binary search uses. Paired with `src/metrics/deltaE.ts`. | [Sharma/Wu/Dalal 2005](http://www2.ece.rochester.edu/~gsharma/ciede2000/) |
| [Chromatic Adaptation Matrices](techniques/chromatic-adaptation-matrices.md) | Bradford and CAT16. D50 ↔ D65, generic illuminant adaptation, pre-computable matrices, why diagonal scaling works. Paired with `src/adaptation/bradford.ts`. | [CIE 159:2004](http://brucelindbloom.com/Eqn_ChromAdapt.html) / [CIE 248:2022](https://www.w3.org/TR/css-color-4/) |
| [CSS Color 4 Gamut Mapping](techniques/css-color-4-gamut-mapping.md) | Normative hue-preserving chroma reduction. Binary search with ΔE_ok ≤ JND early exit, when to prefer over naive clip, sRGB/P3/Rec.2020 wrappers. Paired with `src/gamut/mapping.ts`. | [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/#binsearch) |
| [Ottosson Cusp Algorithm](techniques/ottosson-cusp-algorithm.md) | Closed-form max-chroma cusp at any sRGB hue. Three-face polynomial + Halley refinement, basis for OKHSL and fast gamut mapping. Paired with `src/gamut/cusp.ts`. | [Ottosson 2021](https://bottosson.github.io/posts/gamutclipping/) |
| [Gradient Interpolation & Hue Paths](techniques/gradient-interpolation-math.md) | Linear interpolation across color spaces; the gamma-compounding "muddy gradient" problem; CSS Color 4 hue paths (shorter/longer/increasing/decreasing); CSS color-mix semantics. Paired with `src/interpolation/linear.ts`. | [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/#interpolation) |
| [Cubehelix Colormap](techniques/cubehelix-formula.md) | D. A. Green's perceptually-monotonic colormap for scientific viz. Black-to-white anchored with smoothly rotating hue; 4 parameters (start, rotations, hue, gamma). Paired with `src/interpolation/cubehelix.ts`. | [D. A. Green 2011](https://astron-soc.in/bulletin/11June/289392011.pdf) |
| [Lightness Ramp Curves](techniques/lightness-ramp-curves.md) | Linear / gamma / smoothstep ramps + Tailwind v4 and Radix Themes 3 published L stops. The curve choice that determines design-token palette feel. Paired with `src/interpolation/lightness-curves.ts`. | [Tailwind v4](https://tailwindcss.com/) / [Radix Themes 3](https://www.radix-ui.com/colors) |
| [Tailwind v4 — Default OKLCH Palette](techniques/tailwind-v4-oklch-palette.md) | Tailwind v4 (Jan 2025) ships its default palette generated in OKLCH targeting Display P3 — the first mainstream design system to default to a perceptual space. Migration notes from the HSL-derived v3 palette. | [Tailwind v4](https://tailwindcss.com/blog/tailwindcss-v4) |
| [Radix Themes 3 + Radix Colors P3](techniques/radix-themes-3-p3.md) | Display P3 wide-gamut versions of every 12-step semantically-named scale + custom palette generator (March 2024). The most semantically-organized open color system. | [Radix Colors](https://www.radix-ui.com/colors) |
| [CIECAM16 Forward / Inverse](techniques/ciecam16-forward-inverse.md) | The CIE 2016 color appearance model — viewing condition setup, CAT16 adaptation, post-adaptation cone response, opponent (a, b) signals, JMh output. Material convention notes. Paired with `src/spaces/ciecam16.ts`. | [CIE 248:2022](https://cie.co.at/publications/cie-2016-colour-appearance-model-colour-management-systems-ciecam16) |
| [Material HCT — Math](techniques/material-hct-math.md) | Hue (CAM16) + Chroma (CAM16) + Tone (CIELAB L*). The non-orthogonal hybrid that powers Material Design 3's tonal palettes. Iterative inverse explained. Paired with `src/spaces/hct.ts`. | [Material 3](https://m3.material.io/styles/color/system) |
| [CAM16-UCS — Math](techniques/cam16-ucs-math.md) | Uniform Colour Space companion to CIECAM16. (J, M, h) → (J', a', b') for Euclidean ΔE_CAM16. Li et al. 2017 constants. Paired with `src/spaces/cam16-ucs.ts`. | [Li et al. 2017](https://onlinelibrary.wiley.com/doi/10.1002/col.22131) |
| [Tone Mapping Operators](techniques/tone-mapping-operators.md) | HDR → SDR compression: Reinhard (simple, extended, luminance-preserving), ACES filmic (Narkowicz fit), Uncharted 2 (Hable). The pipeline from scene-linear HDR to display-ready encoded sRGB. Paired with `src/tonemap/reinhard.ts` and `src/tonemap/aces.ts`. | [Reinhard 2002](https://www.cs.utah.edu/docs/techreports/2002/pdf/UUCS-02-001.pdf) / [Narkowicz 2015](https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/) |
| [Spectral → XYZ Integration](techniques/spectral-to-xyz-integration.md) | The physical bridge from a Spectral Power Distribution to CIE XYZ via CMF integration. Reflectance × illuminant × CMF, the 10nm sampling convention, standard illuminants D65/D50/A/F2. Paired with `src/spectral/{cmf,illuminants,spd}.ts`. | [CIE 015:2018](https://cie.co.at/publications/colorimetry-4th-edition) |
| [Color Quantization (k-means)](techniques/color-quantization-math.md) | k-means in OKLab for palette extraction. k-means++ initialization, perceptual-uniform distance, alternative algorithms (octree, median cut, Wu). Paired with `src/quantize/kmeans.ts`. | [Lloyd 1957](https://ieeexplore.ieee.org/document/1056489) / [Arthur & Vassilvitskii 2007](http://ilpubs.stanford.edu:8090/778/) |
| [Dithering Algorithms](techniques/dithering-algorithms.md) | Floyd-Steinberg error diffusion in OKLab. Bayer ordered dithering and blue noise as alternatives. The quantize+dither pipeline for limited-palette outputs. Paired with `src/dithering/floyd-steinberg.ts`. | [Floyd & Steinberg 1976](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) |
| [Jzazbz & ICtCp — HDR Uniform Spaces](techniques/jzazbz-ictcp-math.md) | PQ-like nonlinear color spaces calibrated for HDR (10,000 nits). Safdar 2017 Jzazbz and Dolby/BT.2100 ICtCp. Paired with `src/spaces/jzazbz.ts`. | [Safdar 2017](https://www.osapublishing.org/oe/abstract.cfm?uri=oe-25-13-15131) / [BT.2100](https://www.itu.int/rec/R-REC-BT.2100/) |
| [HSLuv & HPLuv](techniques/hsluv-hpluv-math.md) | Boronine's CIELUV-normalized HSL. Saturation always [0, 100] regardless of hue/lightness. Math only (no TS; use OKHSL for modern UI work). | [hsluv.org](https://www.hsluv.org/) |
| [Spline Interpolation in Color Spaces](techniques/spline-interpolation-color.md) | Catmull-Rom cubic for smooth ramps through multiple anchor colors. C1 continuity at every interior anchor, exact endpoint anchoring. Paired with `src/interpolation/spline.ts`. | [Catmull & Rom 1974](https://www.engr.colostate.edu/ECE572/Anatomy/catmullrom.pdf) |
| [White Point Conversion](techniques/white-point-conversion.md) | Standard illuminant chromaticity table (D65, D50, D55, D75, A, F2). Bradford CAT for cross-illuminant XYZ adaptation. Robertson CCT approximation. Composable with `src/adaptation/bradford.ts`. | [CIE 015:2018](https://cie.co.at/publications/colorimetry-4th-edition) |
| [W3C CSS Color 4 and 5](techniques/w3c-css-color-4-and-5.md) | Normative browser color specs. CSS Color 4 covers lab/lch/oklab/oklch, `color()`, interpolation, and gamut mapping; Color 5 adds `color-mix()`, relative colors, `contrast-color()`, `light-dark()`, ICC-backed custom spaces, and `device-cmyk()`. | [W3C](https://www.w3.org/TR/css-color-4/) / [W3C](https://www.w3.org/TR/css-color-5/) |
| [CSS Color 2026 — Spec & Baseline Snapshot](techniques/css-color-2026-snapshot.md) | Dated spec map (April 2026): OKLCH, `color-mix()`, relative color, `light-dark()`, `contrast-color()` all Baseline; CSS Color 4 CR / Color 5 WD / WCAG 3 Working Draft status. The pack's verify-current-status file. | [W3C](https://www.w3.org/TR/css-color-5/) / [Baseline](https://webstatus.dev/) |
| [Color.js](https://colorjs.io/) | By Lea Verou & Chris Lilley (CSS Color spec editors). CSS Color 4 compliant. Lab/OKLab/P3/Jzazbz/Rec.2100. Gamut mapping, ΔE (76/CMC/2000/Jz), chromatic adaptation (Bradford/CAT16). 154M+ npm downloads. Used by Sass, axe. | [colorjs.io](https://colorjs.io/) |
| [Culori — Color Spaces & API](techniques/culori-color-spaces-api.md) | Foundational color library: 30 spaces (sRGB→OKLCH→Jzazbz→ICtCp), 10 distance metrics (CIEDE2000, HyAB...), interpolation (7 spline methods), gamut mapping, CVD simulation, blending, WCAG. Used by most tools in this collection. | [culorijs.org](https://culorijs.org/) |
| [RampenSau](techniques/rampensau-palette-generation.md) | Color ramps via hue cycling + easing. HSL/OKLCH. harveyHue. colorHarmonies. | [GitHub](https://github.com/meodai/rampensau) |
| [FettePalette](https://github.com/meodai/fettepalette) | Predecessor to RampenSau. Curve-based ramps in HSV with hue cycling. Lamé/arc/power curves. Returns light/dark/base arrays. Tint/shade hue shifting. | [Demo](https://meodai.github.io/fettepalette/) |
| [Poline](techniques/poline-esoteric-palette-generator.md) | Anchor-based palette gen. Per-axis position functions. 1.2K stars. | [GitHub](https://github.com/meodai/poline) |
| [RYBitten](techniques/rybitten-ryb-color-space.md) | RGB↔RYB conversion. 26 historical color cubes. p5.js colorMode(RYB). | [GitHub](https://github.com/meodai/RYBitten) |
| [Color Palette Shader](techniques/color-palette-shader.md) | WebGL2 Voronoi viz across 30+ color models. 11 distance metrics. | [GitHub](https://github.com/meodai/color-palette-shader) |
| [Color Buddy — Palette Lint](techniques/color-buddy-palette-lint.md) | ESLint for color palettes. 38 lint rules: WCAG contrast, CVD safety (3 types), distinctness at thin/medium/wide sizes, fairness, affect (serious/playful/calm), sequential/diverging order, ugly color avoidance. DSL for custom rules. LLM auto-fixes. Research-backed. | [GitHub](https://github.com/mcnuttandrew/color-buddy) |
| [Censor — Palette Analyser](techniques/censor-palette-analyser.md) | Rust CLI for palette analysis. 20+ viz widgets all using CAM16UCS. Close color detection, similarity metrics, spectral plots, 3D cubes, dithering (Bayer/blue noise). Lospec integration. | [GitHub](https://github.com/Quickmarble/censor) |
| [colorsort-js](techniques/colorsort-js.md) | Perceptual color sorting. FFT spectral processing. Powers PickyPalette. | [GitHub](https://github.com/darosh/colorsort-js) |
| [palette-aldente](https://github.com/meodai/palette-aldente) | Palette management: YAML/JSON validation, multi-format export (JSON/JS/HTML/PNG/SVG/ASE/ACO), auto-naming, Photoshop/Illustrator/GIMP/Sketch export. npm + GitHub Pages. | [GitHub](https://github.com/meodai/palette-aldente) |
| [FarbVelo](techniques/farbvelo-random-palette-generator.md) | "Color bicycle" — random palette generator with dark→light structure. HSLuv hue selection + CIE L\*a\*b\* interpolation. Min hue angle control. Color naming via API. | [Demo](https://farbvelo.elastiq.ch/) |
| [dittoTones](techniques/dittotones-palette-from-systems.md) | Generate full shade scales by extracting "perceptual DNA" (lightness/chroma curves) from Tailwind/Radix and applying to your hue. Smart ramp blending, neutral detection, OKLCH. 116 stars. | [GitHub](https://github.com/meodai/dittoTones) |
| [Color Router](techniques/color-router.md) | Reactive color management for design systems. Spreadsheet-like: palettes=sheets, colors=cells, functions=formulas. Theme inheritance, auto-cascading, contrast guarantees. CSS variables + JSON output. | [GitHub](https://github.com/meodai/color-router) |
| [DesignBook — Reactive Design Token Spec](techniques/designbook-reactive-design-token-spec.md) | Architecture spec for reactive design tokens. Separates reference, semantic, and derived tokens; models scopes, dependency graphs, function tokens, and multi-format rendering. Useful for themeable color systems that want to preserve intent, not just final hex values. | original |
| [Color Palette Pro](techniques/colorpalette-pro-synthesizer.md) | Synthesizer-style palette generator. 6 types × 4 styles. OKLCH primary, Color.js. CSS/PNG export, UI mode (Material Design naming), shareable URLs. Free, no ads. | [colorpalette.pro](https://colorpalette.pro/) |
| [HSLuv](techniques/hsluv-better-than-hsl.md) | Normalized CIELUV chroma as 0–100% saturation. HPLuv pastel mode. | [hsluv.org](https://www.hsluv.org) |
| [Ardov Color Lab](techniques/ardov-color-lab.md) | Deep analysis: Edge Seeker LUT gamut mapping, OKLCH blue glitch workaround, OKLrCH (toe-adjusted OKLCH), perceptual gradient subdivision, alpha color reverse-engineering, contrast-targeted color search, dependency-graph theme tokens, 16 color spaces in 3D, semantic harmony generator. | [lab.ardov.me](https://lab.ardov.me/) |

### Practical Methods & Design Application

| File | Summary | Source |
|---|---|---|
| [PickyPalette](techniques/pickypalette-interactive-tool.md) | Interactive palette sculpting on color space canvas. Voronoi territories. | [Demo](https://pickypalette.color.pizza/) |
| [coolors.co — Not Generative (proof)](techniques/coolors-co-not-generative.md) | 7,821 pre-made palettes hardcoded in JS bundle (`on=[[...]]`, 445KB of hex strings). `generatePalette` picks from this list. No algorithm, no color science. | — |
| [Pixel Art Color Palettes](techniques/pixel-art-color-palettes.md) | 3 sources combined: Slynyrd (hue-shifting ramps, Mondo 128-color palette), OpenGameArt Xenodrogen method (consistent direction, no yoyo), Kiwinuptuo (dark→blue, light→yellow = natural light). Universal: always hue-shift, saturation peaks mid-tone. | [Slynyrd](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes) |
| [Book of Shaders — Color](techniques/book-of-shaders-color.md) | Ch.6: color as vec3, swizzling, mix() + shaping functions for gradients, HSB→polar for color wheels, LYGIA shader library. Foundation for all procedural color in GLSL. | [thebookofshaders.com/06](https://thebookofshaders.com/06/) |
| [Cubehelix](techniques/cubehelix-color-scheme.md) | Dave Green's helical color scheme: spiral through RGB cube = monotonic brightness + hue variation. 4 params (start, rotations, saturation, gamma). Grayscale-safe. Foundation for viridis/magma. Same principle as Goethe edge colors. | [Cambridge](https://people.phy.cam.ac.uk/dag9/CUBEHELIX/) |
| [Pasma — Tweaked Rainbow Formula](techniques/piterpasma-tweaked-rainbow-palette.md) | Single GLSL function: warped sine rainbow + cross-channel suppression + min3 subtraction. Less greens, tonal consistency. Used in Blokkendoos. Inner sine warps hue spacing; min3(C) removes whiteness. Compact alternative to Fontana's pipeline. | [Shadertoy](https://shadertoy.com/view/lcf3Rr) |
| [Fontana — Fully Generative Color](techniques/fontana-generative-color-approach.md) | Harvey Rayner's 6-step approach: tonally balanced spectrum → kill green/purple → antique lights (→yellow) + darks (→blue) → background island → foreground hue/tonal modulation → 3 accent types (salt/herbs/spices). "Color and form are not two." | [Medium](https://medium.com/@harvey.rayner/the-fontana-approach-to-fully-generative-color) |
| [CSS-Native Color Generation](techniques/css-color-generation-technique.md) | @meodai technique: generate base OKLCH colors, fill intermediates with CSS `color-mix(in oklab)`. Browser does perceptual mixing natively. scaleSpreadArray, hardStopsGradient, invertible chroma ramps. Zero dependencies for output. | original |
| [Tyler Hobbs — Generative Color](techniques/tyler-hobbs-generative-color.md) | Practical techniques: HSB not RGB, selective randomization, gradients mapped to variables, probability-weighted palettes, **gradient the probabilities** (shift distribution not colors). Composable layers. Code examples. | [Article](https://www.tylerxhobbs.com/words/working-with-color-in-generative-art) |
| [color-spd — Spectral Picker](techniques/color-spd-spectral-picker.md) | Create colors by editing spectral power distributions directly. Physics-level color creation. Explore metamers, spectral mixing, bridge physics↔perception. Unique tool. | [GitHub](https://github.com/mattdesl/color-spd) |
| [color-wander](https://github.com/mattdesl/color-wander) | mattdesl's generative art with seeded random color. 1.6K stars. Browser + Node canvas. Deterministic seeds for reproducibility. | [GitHub](https://github.com/mattdesl/color-wander) |
| [glsl-lut — LUT Color Grading](techniques/glsl-lut-color-grading.md) | GLSL shader for LUT-based color transforms. 512×512 texture encodes entire color grading. One lookup per pixel. Create LUTs from Photoshop or programmatically (OKLAB-based). Film industry standard. 184 stars. | [GitHub](https://github.com/mattdesl/glsl-lut) |
| [mattdesl — Generative Color Workshop](techniques/mattdesl-generative-color-workshop.md) | Hands-on workshop: Color.js + Spectral.js + Mixbox. Custom tools: Color Grab, Color Swatch, Color SPD (spectral). Curated links: palette libraries (nice-color-palettes, chromotome, riso-colors, Wada Sanzō dictionary), pickers, education. | [GitHub](https://github.com/mattdesl/workshop-generative-color) |
| [Image Color Extraction](techniques/image-color-extraction-tools.md) | Four tools + palette search: **img-colors.com** (7 clustering algorithms, 3D point cloud, mesh gradients) + **okpalette.color.pizza** (OKLCH extraction, bias controls, analysis metrics) + **colorgram-js** (1 kB, 64-bucket quantization, ~15 ms) + **Art Palette** (Google Arts & Culture — JS palette extractor + TensorFlow perceptual palette embeddings for nearest-neighbor artwork search). | [img-colors](https://img-colors.com/) / [okpalette](https://okpalette.color.pizza/) / [Art Palette](https://github.com/googleartsculture/art-palette) |
| [IQ Cosine Palette Formula](techniques/iq-cosine-palette-formula.md) | Inigo Quilez's `color(t) = a + b*cos(2π(c*t+d))` — 12 floats define infinite palettes. GPU-friendly, smooth by construction, intuitive parameters (brightness, contrast, frequency, phase). Ubiquitous in shader art. 52K views. | [IQ Shorts](https://www.youtube.com/shorts/TH3OTy5fTog) |
| [Goethe Edge Colors = Design Hack](techniques/goethe-edge-colors-design-hack.md) | Reverse-engineering Goethe's prism edge colors into readable gradient palettes. Edge sequences = helices through color space (hue+lightness+chroma shift together). Satisfies all 3 readability requirements. Viridis/Magma/Cubehelix use same principle. Colorbox tool. 26K views. | [Color Nerd](https://www.youtube.com/watch?v=qiXHiABcl-I) |
| [Francis — Balanced Generative Palettes](techniques/francis-balanced-generative-palettes.md) | George Francis's two composable JS tricks: `createWeightedSelector` turns a palette into a probability distribution (60/30/10 rule by weights), and `modulateColorHSL` nudges each placed color by a small random HSL delta for "hand-mixed paint" variance. Best combined. | [Francis](https://georgefrancis.dev/writing/balanced-generative-color-palettes/) |
| [Francis — Coloring With Code (LCH)](techniques/francis-coloring-with-code-lch.md) | Three LCH palette generators via Culori: **Scientific** (hue rotation for classic harmonies), **Discovery** (nearest-match harmony from any color pool — e.g. an image palette), **Hue Shift** (pixel-art technique: shift hue with lightness for vivid tints/shades, not gray). | [Codrops](https://tympanus.net/codrops/2021/12/07/coloring-with-code-a-programmatic-approach-to-design/) |

## Library & Tool Catalog (online tools, no local file)

Axis 6's tool catalog. Filtered from the pre-split Online Tools table to pickers/palette/gamut tools;
naming pickers (color.pizza API, 147colors, ISCC-NBS picker) moved to `color-material-facts`
§naming; the huevaluechroma.com/handprint.com entries moved with the vision-science and
pigment-data content they front (`color-perception-facts` / `color-material-facts`); pure
contrast/CVD tools (APCA Calculator, RandomA11y, Components.ai Color) moved to
`color-contrast-facts`.

| Tool | URL | Description |
|---|---|---|
| OSA-UCS Picker | https://petertdonahue.com/osa-ucs-picker.html | OSA Uniform Color Scales |
| Spiral Palette Generator | https://petertdonahue.com/Spiral-Palette-Generator.html | Spiral palette gen |
| HSLuv | https://www.hsluv.org | Perceptually uniform HSL |
| OKLCH Picker | https://oklch.com | OKLCH color picker |
| Realtime Colors | https://realtimecolors.com | Live palette testing on UI |
| Color Gamuts | https://colorgamuts.com | Compare gamuts visually |
| Hue Plot | https://hueplot.ardov.me/ | Visualize hue distributions across color spaces |
| Wide Gamut Test | https://wide-gamut.com | Test display gamut support |
| random-display-p3-color | https://github.com/mrmrs/random-display-p3-color | Generate random Display P3 colors constrained by named hue/saturation/lightness. Defines named hue ranges (red 345–15°, orange 15–45°, etc.). Zero deps, ESM, TypeScript. By mrmrs / mrmrs.cc |
| RampenSau | https://meodai.github.io/rampensau/ | Hue cycling ramp generator |
| Poline | https://meodai.github.io/poline/ | Anchor-based palette gen |
| Color Palette Shader | https://meodai.github.io/color-palette-shader/ | Voronoi palette viz |
| PickyPalette | https://pickypalette.color.pizza/ | Interactive palette sculpting |
| RYBitten | https://github.com/meodai/RYBitten | RGB↔RYB with historical cubes |
| View Color | https://view-color.com | Real-time color analysis: every major color space, WCAG 2.1 & APCA contrast, CVD preview, tints/shades, accessible palettes. Built on Color.js |
| img-colors | https://img-colors.com | Image → palette via 7 clustering algorithms (K-Means, DBSCAN, Median-Cut...) + 3D point cloud + mesh gradients |
| OKPalette | https://okpalette.color.pizza | Image → OKLCH palette with muted/saturated + dark/light bias sliders; analysis metrics; SVG/PNG export |
| Components.ai Color Scale | https://components.ai/color-scale/ | Parametric color scale generator: 6 color spaces (RGB/HSL/HSV/LAB/LCH/P3), 4 curve methods (linear/B-spline/natural/monotone), scale/shadow-tint/freeform modes, WCAG contrast pairs, CVD preview. By mrmrs / mrmrs.cc |
| Colorbox | https://colorbox.io | Build helical gradient palettes with easing curves (Lyft/Kevyn Arnott) |
| IQ Palette Explorer | https://iquilezles.org/articles/palettes/ | Inigo Quilez cosine palette formula — interactive demo |
| Color Grab | https://mattdesl.github.io/colorgrab/ | Extract colors from images (mattdesl) |
| Color Swatch | https://mattdesl.github.io/colorswatch/ | Multi-space color picker (mattdesl) |
| Color SPD | https://mattdesl.github.io/color-spd/ | Create colors from spectral power distributions (mattdesl) |
| color-input | https://color-input.netlify.app/ | Web component color picker: wide-gamut (P3, Rec2020), OKLCH/OKLAB/LAB/LCH/HSL/HWB, gamut detection, eyedropper, contrast calc. Uses Color.js |
| Huetone | https://huetone.ardov.me/ | Build accessible color systems in LCH/OKLCH with real-time contrast checking. Built-in palettes, Figma export. By Alexey Ardov |
| colorspace.dev | https://www.colorspace.dev/ | Explore color in OKLCH/OKHSL/CIELAB with 3D visualization; generate harmonious palettes for design systems |
| ArtBuddy Ramp Grid | https://artbuddy.urlich.ch/rampgrid/ | Grid-based color ramp creation |
| ArtBuddy Color Grid | https://artbuddy.urlich.ch/colorgrid/ | Mix colors on an interactive grid |
| ArtBuddy Gradients | https://artbuddy.urlich.ch/gradientpalette/ | Color gradient palette creator |
| Colormind | http://colormind.io/ | GAN-based palette generator trained on Adobe Color + Dribbble + photos/movies; lock colors for partial infill |
| Lospec | https://lospec.com/palette-list | Pixel art palette database |
| Color Buddy | https://color-buddy.netlify.app/ | Palette linting — 38 rules for accessibility, CVD, distinctness, fairness |
| Francis Weighted Palette | https://codepen.io/georgedoescode/pen/OJQRxZr | George Francis CodePen — weighted selector applied to a generative composition (60/30/10 on/off toggle) |
| Francis Color Modulation | https://codepen.io/georgedoescode/pen/XWeBapd | George Francis CodePen — per-object HSL color modulation demo (subtle variance on/off toggle) |
| LYGIA Color Shaders | https://lygia.xyz/color | Reusable shader library: mixOklab, mixSpectral, mixRYB, hueShiftRYB, daltonize, LUT, dither, tonemap. GLSL/HLSL/Metal/WGSL |
| Color Palette Pro | https://colorpalette.pro/ | Synthesizer-style palette generator. 6 types (ANA/COM/SPL/TRI/TET/TAS) × 4 styles (square/triangle/circle/diamond). OKLCH primary. Color.js. CSS export, PNG, UI mode. By Ryan Feigenbaum |

## Cited from other packs

Per the straddle rule (D4): the `colorandcontrast.com` scrape moved whole to
`color-perception-facts` (a scraped site is one cited source, never split by chapter). Its
space-conversion chapter is cross-cited here rather than duplicated:

| Chapter | Topics |
|---|---|
| *Color Spaces* (colorandcontrast.com, in `color-perception-facts`) | sRGB, P3, LMS, XYZ, CIELAB, OKLAB, CAM16 — the space-conversion chapter of the colorandcontrast scrape; full site lives in `color-perception-facts` |
