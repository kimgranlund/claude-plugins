# Changelog

## [3.0.0] — 2026-07-06 — Extraction: folder renamed, reference corpus split into four packs

### Changed

- **Folder renamed** `color-science` → `color-science-project-files`. It registers
  no skill: `SKILL.md` is retired (`git rm`; content superseded by the four packs
  below, preserved in git history).
- **Reference corpus (159 files) extracted** into four sibling `color-science-*`
  packs, each self-contained (own `SKILL.md`, `references/`, `scripts/routing-
  corpus.json`, `evals/`, `CHANGELOG.md`):
  - `color-science-spaces` (72 files) — spaces & conversions, gamut & interpolation,
    HDR/tone mapping, CSS color syntax, image palettes/quantization, palette-
    generation methods & the library/tool catalog.
  - `color-science-perception` (49 files) — terminology & dimensions, vision
    mechanics, appearance science, plus the huevaluechroma and colorandcontrast
    scrapes whole.
  - `color-science-accessibility` (8 files) — contrast standards (APCA/WCAG 2.2)
    and CVD.
  - `color-science-materials` (30 files) — pigment & mixing physics, reproduction
    & measurement, naming standards & datasets.
- **`ARCHITECTURE.md` and `MATH-ROADMAP.md` moved** from `references/` to this
  folder's root — they document `src/` and stay co-versioned with the code, not
  the reference packs. Internal paths repointed to the new pack locations.
- **`scripts/routing-corpus.json` retired** (`git rm`); each pack re-derives its
  own from its own charter.
- **README.md and CLAUDE.md rewritten** to describe this folder truthfully: the
  color-math TypeScript library and 54-demo showcase site, no skill registered
  here, reference corpus named to its four owning packs. Stale claims dropped
  (no PDFs on disk, no "159 references here", no "loaded when color work is
  detected").

## [2.0.1] — 2026-07-03 — Deep-review fixes: INDEX parity, corpus relocation, declared defaults

### Fixed

- **INDEX.md one-row-per-file parity restored (159/159).** The five files parked in the
  "Additional Reference Files… not yet folded" appendix got full rows in their axis tables
  (`material-hct-color-space`, `ciecam16-cam16-ucs`, `cvd-simulation-canonical`,
  `huevaluechroma/links`, `radix-themes-3-p3`) and the appendix was removed; three files that
  had no INDEX row at all were added (`css-color-2026-snapshot`, `wcag-2-2-current-legal-floor`,
  `tailwind-v4-oklch-palette`). Verified: 159 INDEX links = 159 reference files on disk.
- **2.0.0 entry corrected:** the rebuilt SKILL.md was 98 lines, not 90 (now 103 with the
  declared-defaults clause below).

### Changed

- **Routing corpus relocated and re-derived**: `color-science.corpus.json` →
  `scripts/routing-corpus.json`. Negatives citing ghost skills (the retired `*-decomposer`
  family, `ui-build-*`, `extract-ui-css`, `skills-studio`) deleted; negatives re-drawn from the
  live neighborhood — color-theory, color-verify ("does this palette pass contrast"),
  palette-design ("build me a ramp"), typography-lettering, ui-patterns, knowledge-author,
  the token-builder agent. 15 positives (four phrasing classes) / 13 negatives.
- **SKILL.md declares its deviation doctrine**: the standing defaults (OKLCH/OKLab for
  perceptual work; APCA design standard over the WCAG 2.2 legal floor) promoted to an explicit
  defaults-with-rationale clause under Standing distinctions; description gains the print
  symptom token ("print proof duller than the mockup").

## [2.0.0] — 2026-07-02 — Split: color-theory pack extracted

### Changed

- **Pack split along the judgment boundary.** color-science keeps perception/math/standards
  ("what is perceptually true"); the new sibling `color-theory` pack takes aesthetics/meaning/
  history ("what reads as intended"). 28 reference files moved (12 `historical/` wheel-history
  and colorist files, 5 `contemporary/`, 11 `techniques/` harmony/practice files) — see
  color-theory's CHANGELOG for the full manifest. References now count **159** (was 190).
- **SKILL.md rebuilt net-new** (297 → 98 lines; this entry originally claimed 90 — corrected
  2026-07-03): identity → typed consult index → worked
  consult → source-tracing rule → boundaries. Harmony and wheel-history trigger vocabulary
  removed from the description; "NOT for color harmony, the color wheel, or color meaning
  (color-theory)" added.
- **Straddle rule:** files carrying a perceptual mechanism under an aesthetic consequence
  (Albers simultaneous contrast, Goethe edge colors, opponent process, warm/cool spectra) stay
  here; color-theory cites them from its INDEX — never duplicated.
- INDEX.md, README.md, CLAUDE.md counts and axis descriptions re-synced; cross-pack links
  rewired (`rybitten-ryb-color-space.md`, `colorpalette-pro-synthesizer.md`); stale
  `ui-verify-focus` link fixed to `focus-verify`; routing corpus + task prompts updated so
  harmony asks are expected to route to color-theory.

## [1.20.1] — 2026-05-23 — Maintenance: skill name + stale notes

### Fixed

- **`CLAUDE.md`** — stale skill-name reference: `expert-color` → `ref-color`
  (the actual skill name). Old name predates a rename; new authors reading
  CLAUDE.md would have been told the wrong name.

### Changed

- **`CLAUDE.md`** — SKILL.md size guideline rewritten. Was "~200 lines"; the
  actual SKILL.md is ~280 lines and the rich content is load-bearing. New
  guidance preserves the intent (load-bearing body, deep content in
  `references/`) without imposing a brittle line count.
- **`skill.json`** — `notes` field removed. Was dated v1.1.0 (2026-04-26)
  and 17 minor cuts stale. CHANGELOG is canonical for version history.

No content removed from SKILL.md or references. No skill capabilities changed.

## [1.20.0] — 2026-05-17 — Josef Albers teaching arc (16 pages)

A 16-page educational section on Josef Albers' perceptual color method,
threaded as a coherent teaching arc from Bauhaus → Black Mountain → Yale →
*Interaction of Color* → Homage to the Square → modern OKLCh design systems.
Each page is a focused intent with a single primary demo, not a biography.

### Added — 16 new pages

- **`pages/albers-who.html`** (01) — Albers as teacher first, painter second.
  Timeline of Bauhaus → BMC → Yale lineage. Lead Homage canvas.
- **`pages/albers-relational.html`** (02) — The central claim. Same chip
  in two surrounds, reveal proves equality.
- **`pages/albers-book.html`** (03) — *Interaction of Color* as a lab manual.
  Plate IV-1 recreation.
- **`pages/albers-deception.html`** (04) — Five families of perceptual effects
  (simultaneous contrast / White's illusion / illumination shift / memory /
  Mach bands) in a tap-to-reveal grid.
- **`pages/albers-simultaneous.html`** (05) — Live chip-on-two-grounds
  composer with full controls.
- **`pages/albers-one-as-two.html`** (06) — The classic Albers exercise.
- **`pages/albers-two-as-one.html`** (07) — The inverse, with live ΔE_ok
  readout between chips.
- **`pages/albers-homage.html`** (08) — Six Homage variants showing the
  same composition with wildly different palettes.
- **`pages/albers-square.html`** (09) — Same colors arranged as squares,
  circles, and petals; non-square arrangements drag in associations.
- **`pages/albers-proportion.html`** (10) — Area slider showing how the
  same color's perception shifts with area share.
- **`pages/albers-warm-cool.html`** (11) — Quiz format: the same chip is
  "the warm one" in some pairs and "the cool one" in others.
- **`pages/albers-transparency.html`** (12) — Three-rectangle composer with
  RGB-midpoint vs OKLab-midpoint snap buttons.
- **`pages/albers-afterimage.html`** (13) — 20-second stare trial with
  auto-switch to white field.
- **`pages/albers-vs-science.html`** (14) — Same illusion read through
  RGB, CIELAB, and OKLab — all confirm physical sameness.
- **`pages/albers-digital.html`** (15) — Brand-500 shown in six UI contexts.
- **`pages/albers-lab.html`** (16) — Capstone: configurable Homage canvas
  with OKLCh sliders per layer, randomize/reset/copy-CSS controls.

### Added — 4 new custom-element components

- `<chip-composer>` — workhorse for pages 02, 05, 06, 07, 14.
- `<homage-canvas>` — Albers' nested-square composition with 3- or 4-square
  layout. Used by 01, 08, 16.
- `<afterimage-trial>` — 20-second stare countdown with white-field reveal.
- `<transparency-composer>` — Three overlapping rectangles with OKLab vs
  RGB midpoint snap.

### Changed

- `examples/lib/js/shell.js` — Added "Josef Albers" group with 16 entries.
- `examples/index.html` — Added "Josef Albers — color is relational" section
  with 16 demo cards.
- `examples/lib/dist/refcolor.bundle.js` — Now ~255 KB.

### Why this matters

Albers (1888-1976) is the bridge between the perceptual color tradition
(Goethe, Hering, Chevreul) and the modern color-system practice (Material 3,
Tailwind v4, OKLCh tokens). His exercises predicted every "this color reads
wrong in dark mode" conversation by 60 years. Threading the existing
math-first showcase with Albers-style perception exercises gives the skill
the same dual identity — quantitative *and* perceptual — that the field
itself developed.

---

## [1.19.0] — 2026-05-16 — Examples site v5.1: research-driven up-level of waves 1-2

Up-leveled the first 14 demos based on 2026 SOTA research (Evil Martians,
oklch.fyi, Coolors, Gamutvision, ColorAide). 38 demos remain in place;
eight were materially expanded.

### Changed — 8 up-leveled demos

- **`pages/picker.html`** — Added interactive L×C slice canvas (click to
  set L+C at current hue, out-of-gamut regions dimmed), inline contrast
  preview against white + black, copy-to-clipboard buttons for hex /
  oklch() / rgb(), and APCA Lc readouts on both reference backgrounds.
- **`pages/gradient.html`** — Added native CSS Color 4 output
  (`linear-gradient(in oklch shorter hue, ...)`) per space with
  copy-paste examples + a per-space ΔE_ok between-adjacent-stops table
  that surfaces perceptual uniformity numerically.
- **`pages/contrast.html`** — Added live text-preview panel rendering
  "The quick brown fox" at 6 font-size × weight combos in the chosen
  colors, plus a "suggested fixes" panel finding 3 alternative
  foregrounds passing APCA Lc ≥ 75 when the current pair doesn't.
- **`pages/palette.html`** — Multi-k comparison row (k = 3, 5, 8
  stacked simultaneously) and export buttons producing CSS variables /
  Tailwind config / JSON for the extracted palette.
- **`pages/mapping.html`** — Each of the 4 mapping strategies now
  applies to an uploaded image, not just a swatch. Chroma-boost slider
  drives synthetic out-of-gamut and lets you see strategy differences
  on real photo data.
- **`pages/harmony.html`** — Full UI mockup (nav + card + primary/
  secondary buttons + stat tiles) rendered with the chosen OKLCh scheme.
- **`pages/deltae.html`** — "Drift" slider pushes color B away from A
  in OKLab space (1× → 5×), animating all 5 ΔE metrics so you can see
  how each grows at different rates.
- **`pages/imagestats.html`** — Stats grid below the histograms:
  average chromaticity (x, y), correlated color temperature (CCT via
  McCamy), percentage of vivid pixels (OKLCh C > 0.10), sample count.

### Research basis

- [Evil Martians OKLCh picker](https://oklch.com/) — set the bar for
  contrast indicators, P3 fallback, multi-format output.
- [oklch.fyi](https://oklch.fyi/), [oklch.xyz](https://oklch.xyz/) —
  copy buttons and click-canvas patterns.
- [Coloraide interpolation docs](https://facelessuser.github.io/coloraide/interpolation/)
  — perceptual-uniformity-via-ΔE_ok analysis is standard in colour-science.
- [Coolors](https://coolors.co/) — multi-format export as baseline.
- [Gamutvision](http://www.gamutvision.com/) — image-level gamut stats.

### Unchanged (already strong)

`gamut.html` (fixed earlier this session for DPR bug),
`chromaticity.html`, `transfer.html`, `wheel.html`, `ramp.html`,
`cvd.html` — left as v1.15 / v1.17 shipped.

---

## [1.18.0] — 2026-05-16 — Examples site v5: 8 more demos (38 total)

Wave 5 adds the foundational color-science visualizations that the
earlier waves didn't cover — the iconic teaching diagrams from MacAdam
(1942) onwards, plus a color-matching game, an APCA reading-table tool,
and three more dither algorithms.

### Added — 8 new demos

- **`pages/macadam.html`** — MacAdam ellipses on the CIE xy diagram. 25
  just-noticeable-difference regions from the 1942 paper, with adjustable
  scale factor (1× actual, 10× canonical visualization).
- **`pages/illusions.html`** — Color illusions gallery. Simultaneous
  contrast, White's illusion, Helmholtz-Kohlrausch — each with explicit
  hex readouts proving identical RGB values.
- **`pages/volume.html`** — Color volume comparison. Monte Carlo
  estimation of OKLab perceptual volume for sRGB, P3, Adobe RGB, Rec.2020,
  ProPhoto, Rec.709. Bar chart normalized to sRGB = 1.0×.
- **`pages/cube3d.html`** — 3D sRGB cube embedded in OKLab. Rotatable
  wireframe of edge-sampled cube points showing perceptual non-linearity.
- **`pages/match.html`** — Color matching game. Random target color,
  OKLCh sliders, scored by ΔE_ok with JND-based tiers.
- **`pages/apcatable.html`** — APCA reading table. Live PASS/CLOSE/FAIL
  grid of font sizes × weights for a fg/bg pair, against approximated
  Bronze Simple Mode thresholds.
- **`pages/multidither.html`** — Multi-dither comparison. Floyd-Steinberg,
  Atkinson, Bayer 4×4 ordered, and Jarvis-Judice-Ninke applied to the
  same image with the same OKLab-quantized palette.
- **`pages/scatter.html`** — Image chromaticity scatter. Drop image,
  every pixel plotted on the xy diagram in its actual color. The "gamut
  analysis" view photographers use.

### Added — 5 new custom-element components

- `<macadam-ellipses>` — 25 ellipses on CIE xy with sRGB triangle + locus.
- `<volume-bars>` — Monte Carlo gamut volume bar chart with table.
- `<color-cube-3d>` — Rotatable 3D wireframe of sRGB cube in OKLab/CIELAB.
- `<multi-dither>` — 4-way dither algorithm comparison (FS / Atkinson /
  Bayer 4×4 / Jarvis-Judice-Ninke), all implemented inline.
- `<image-scatter>` — Image pixels as colored dots on the xy diagram.

### Changed

- `examples/lib/js/shell.js` — DEMO_GROUPS adds a 6th group "Foundations
  & illusions" with the 8 new entries.
- `examples/index.html` — Sixth section "Foundations & illusions" added.
- `examples/lib/dist/refcolor.bundle.js` — Now ~240 KB unminified.

### Research basis

Wave 5 picks were validated by web research:
- **MacAdam 1942** — every color-science textbook references the ellipses;
  the canonical 25-point dataset is widely tabulated. Almost no interactive
  web visualization exists.
- **Adelson, White, Helmholtz-Kohlrausch** — three of the most-cited color
  illusions. Putting them together with hex-value proofs makes the
  perception-vs-measurement gap unmistakable.
- **Color volume in HDR workflows** — increasingly discussed in 2026
  display industry (HDR1000 vs HDR400 tiers, Display P3 over sRGB).
  Quantifying perceptual volume directly is more useful than 2D triangle
  area for these conversations.
- **Bayer (1973) + Atkinson (1980s) + Jarvis-Judice-Ninke (1976)** —
  classic dither algorithms cited alongside Floyd-Steinberg in every
  graphics textbook. Putting them side-by-side reveals each one's
  signature texture.

---

## [1.17.0] — 2026-05-16 — Examples site v4: 8 more demos (30 total)

Wave 4 focuses on the 2026 design-system / modern-CSS frontier plus the
foundational color-science visualizations the earlier waves hadn't covered.

### Added — 8 new demos

- **`pages/csscolor5.html`** — CSS Color 5/6 playground. Live `color-mix()`
  in 6 spaces, relative color syntax (`oklch(from base ...)`), `light-dark()`,
  and `contrast-color()` — the modern CSS toolbox with generated copy-paste
  CSS for every result.
- **`pages/tonal.html`** — Material 3 tonal palette generator. Source color
  → primary / secondary / tertiary / neutral / neutral-variant palettes
  at 13 tones each, with gamut-aware chroma reduction. Dogfoods
  `src/spaces/hct.ts`.
- **`pages/kelvin.html`** — Color temperature picker. Blackbody color from
  1500 K to 15000 K, plotted as a dot moving along the Planckian locus on
  a mini xy diagram with reference illuminant points (A, D50, D65, D75).
- **`pages/okhsl.html`** — OKHSL picker (Ottosson's perceptual HSL). Fixed-
  hue (S, L) slice next to the matching HSL slice for visual comparison.
  Dogfoods `src/spaces/okhsl.ts`.
- **`pages/blendwhite.html`** — Ottosson's canonical "blend through white"
  visualization. Same blue→white blend in 5 spaces (encoded sRGB, linear
  sRGB, OKLab, CIELAB, HSL) showing the iconic "hue shift toward purple"
  bug fixed in OKLab.
- **`pages/cvdsafe.html`** — CVD-safe palette designer. Greedy hue
  optimization to maximize worst-case ΔE_ok across normal + 3 CVD types.
  Dogfoods `src/cvd/machado-2009.ts` + `src/metrics/deltaE.ts`.
- **`pages/wavelength.html`** — Wavelength → color. 380-700nm slider →
  spectral color + chromaticity dot on the locus + in-sRGB status.
- **`pages/cmf.html`** — CMF + LMS cone fundamentals. Plot of x̄/ȳ/z̄ + LMS
  curves with a wavelength selector showing each cone's response value.

### Added — 6 new custom-element components

- `<tonal-palette>` — Material 3 palette table with chroma-reduction logic.
- `<kelvin-picker>` — Blackbody color + mini Planckian locus diagram.
- `<okhsl-picker>` — Side-by-side OKHSL vs HSL slice rendering.
- `<blend-through-white>` — Five horizontal gradient strips, one per space.
- `<cvd-safe-palette>` — Optimization + per-CVD min-ΔE table.
- `<cmf-chart>` — CMF + LMS curves with wavelength indicator.

### Changed

- `examples/lib/js/shell.js` — DEMO_GROUPS reorganized into 5 categories
  with 30 total entries (renamed "Pigments & palettes" → "Tokens, schemes
  & CSS" to better describe its contents after additions).
- `examples/index.html` — All 30 demo cards visible; description copy
  updated for the wider scope.
- `examples/lib/dist/refcolor.bundle.js` — Now ~213 KB unminified.

### Research basis

Wave 4 demos were selected after research on the 2026 SOTA:
- **W3C CSS Color 5/6 spec** — `color-mix()`, relative color syntax,
  `contrast-color()`, `light-dark()` are widely shipped; demoing these is
  more valuable now than even at v1.15.
- **Material 3 / HCT** — Google's tonal-palette approach is the alternative
  paradigm to Tailwind v4's OKLCh; showing both is educational.
- **Ottosson's color-blog posts** — "Color Wrong" and the OKLab paper
  feature the "blend through white" visualization as iconic; we now have
  the only interactive version of it on the web.
- **DaltonLens + Adobe Leonardo** — CVD-aware palette design is the most-
  requested accessibility tool; `cvdsafe.html` is the first open-source
  optimizer demo I'm aware of.

---

## [1.16.0] — 2026-05-16 — Examples site v3: 8 more demos (22 total)

Builds on v1.15.0 with a third wave of demos covering modules the earlier waves
hadn't showcased — pigment mixing, chromatic adaptation, HDR tone mapping,
spatial dithering, spectral illuminants, color appearance models, and
procedural palettes.

### Added — 8 new demos

- **`pages/pigment.html`** — Kubelka-Munk paint mixer. Mix two pigment
  reflectance spectra; compare with naive RGB midpoint. Dogfoods
  `src/pigment/kubelka-munk.ts`.
- **`pages/adapt.html`** — Chromatic adaptation viewer. Drop an image,
  see it under D65 / D50 / A / F2 illuminants via Bradford CAT. Dogfoods
  `src/adaptation/bradford.ts`.
- **`pages/tonemap.html`** — HDR tone mapping comparison. Five operators
  on the same synthetic HDR gradient (naive clip, Reinhard simple/extended/
  luminance-preserving, ACES Narkowicz). Dogfoods `src/tonemap/*`.
- **`pages/dither.html`** — Floyd-Steinberg dithering. Quantize an image
  to k colors via k-means in OKLab, then compare nearest-neighbor mapping
  to error-diffused output. Dogfoods `src/dithering/floyd-steinberg.ts`.
- **`pages/illuminants.html`** — Spectral illuminants explorer. SPD curves
  for D65/D50/A/F2/E + sample-color grid showing how 8 surface reflectances
  render under each. Dogfoods `src/spectral/*`.
- **`pages/ciecam16.html`** — CIECAM16 viewing-conditions explorer.
  Adjust adapting luminance, background L*, and surround; see how a fixed
  XYZ stimulus's J/M/h attributes change. Dogfoods `src/spaces/ciecam16.ts`.
- **`pages/procedural.html`** — Procedural palette generator. Cubehelix
  (Green 2011) + iq cosine (Quilez) with sliders and a relative-luminance
  monotonicity plot. Dogfoods `src/interpolation/cubehelix.ts`.
- **`pages/namer.html`** — Color namer. Find the closest CSS named color
  to any hex, ranked by ΔE_ok (perceptual) vs RGB Euclidean. Dogfoods
  `src/metrics/deltaE.ts`.

### Added — 6 new custom-element components

- `<pigment-mixer>` — Two-pigment K-M blend with side-by-side RGB-midpoint
  comparison and reflectance-spectrum chart.
- `<adaptation-viewer>` — Bradford CAT applied to an image with split-view.
- `<tonemap-strip>` — Renders 5 tone-mapping operators on a synthetic HDR
  gradient.
- `<dither-compare>` — Palette + nearest-neighbor + Floyd-Steinberg view.
- `<spd-chart>` — Multi-illuminant SPD plot + sample-color grid.
- `<procedural-palette>` — Smooth ramp + sampled palette + luminance plot.

### Added — illuminant

- `F2` SPD added to `src/spectral/illuminants.ts` — CIE F2 cool-white
  fluorescent at 380-730nm, 10nm intervals. Characteristic mercury-vapor
  spikes near 405, 435, 545, 580nm visible in the SPD chart.

### Changed

- `examples/lib/js/shell.js` — DEMO_GROUPS expanded to 5 categories with
  22 entries total (added "Pigments & palettes" group).
- `examples/index.html` — All 22 demo cards across 5 sections.
- `examples/lib/dist/refcolor.bundle.js` — Now ~183 KB unminified (was
  ~143 KB at v1.15.0).

---

## [1.15.0] — 2026-05-16 — Examples site v2: 8 new demos + bundle build flow

Expanded the `examples/` showcase from 6 to 14 demos and shipped a classic-script
bundle build flow so every page works directly over `file://` (no dev server,
no CORS issues).

### Added — 8 new demos

- **`pages/cvd.html`** — Color-blindness simulator. Drop an image, switch
  between protan/deutan/tritan, slide severity 0–100%. Uses Machado 2009
  matrices from `src/cvd/machado-2009.ts`.
- **`pages/ramp.html`** — Tailwind-style ramp generator. Pick a hue + lightness
  curve, get a copy-paste 11-stop OKLCh ramp at the peak chroma each row
  supports. Uses `peakC` from `src/gamut/oklch-peak.ts`.
- **`pages/chromaticity.html`** — CIE xy diagram. Horseshoe locus + gamut
  triangles for sRGB, P3, Rec.2020, Adobe RGB, ProPhoto + D50/D65/D55 white
  points. Click to read xyY → all spaces. Dogfoods `src/spaces/xyy.ts`.
- **`pages/deltae.html`** — ΔE metric comparator. Two colors, six metrics
  side-by-side (CIE76, CIE94, CIEDE2000, ΔE-ok, HyAB, ΔE-CAM16). Dogfoods
  `src/metrics/deltaE.ts`.
- **`pages/mapping.html`** — Gamut mapping playground. Pick an out-of-gamut
  OKLCh color, see chroma-compression / MINDE / clip / CSS Color 4 mapping
  side-by-side. Fills the demo gap Ottosson left in his gamut-clipping article.
- **`pages/harmony.html`** — Color harmony generator. Base color + scheme
  (complementary, analogous, triadic, tetradic, split-complementary), all
  rotated in perceptual OKLCh hue (uniform — no HSL hue distortion).
- **`pages/wheel.html`** — Perceptual hue wheel. OKLCh vs HSL vs HCT at fixed
  lightness, rendered as three concentric rings. Visceral demo of HSL's
  hue compression and OKLCh's uniformity.
- **`pages/imagestats.html`** — Image color analysis. Drop an image, see hue
  ring histogram, lightness histogram, gamut coverage stats, and auto-extracted
  palette. Composes `kmeans` + multiple space modules.

### Added — 6 new custom-element components

- `<cvd-simulator>` — Canvas-based image filter; observes image-src / type / severity.
- `<token-ramp>` — Flexbox grid of 11 chips with hex + OKLCh labels.
- `<chromaticity-diagram>` — Horseshoe locus + gamut polygons + white points.
- `<gamut-strip>` — Four side-by-side strips showing each mapping strategy.
- `<hue-wheel>` — Three concentric perceptual hue rings.
- `<image-histograms>` — Hue ring + lightness bar histograms.

### Changed

- `examples/lib/css/shell.css` — Tokens inlined; `tokens.css` removed.
  WebKit was emitting "Unsafe attempt to load URL" warnings for CSS `@import`
  chains under `file://` (each file is its own security origin).
- `examples/lib/js/components/gamut-envelope.js` — Fixed two bugs: the
  DPR-vs-imageData mismatch that was clipping the envelope to the top-left
  quadrant on retina displays, and replaced the arbitrary "tints"
  visualization with actual sRGB-mapped colors + stroked boundary curves.
- `examples/lib/dist/refcolor.bundle.js` — Single classic-script IIFE bundle
  (~140 KB unminified), exposes `window.RefColor`. Every demo page consumes
  this; no ES module imports under `file://`.
- `examples/build.sh` — Two-step build (optional `tsc` + always `esbuild`).
  Falls back gracefully when no local `tsc` is present.

### Why this matters

The examples site is the canonical reference for "what does this skill
actually do?" Other agents and humans skimming the skill in 2 minutes form
their first opinion from the demos — not the README, not the source. 14
demos covering every major capability gives the skill a credible surface.

---

## [1.14.0] — 2026-05-16 — Feature complete: close 8 type↔module asymmetries

The lateral sweep at v1.13.0 surfaced that 8 branded types in `src/types.ts`
had no implementing space module — the type system promised spaces that
couldn't actually compose. v1.14.0 closes all 8.

After this release, **every branded color type in this skill has a working
implementation** with `toXYZ`/`fromXYZ` (or `encode`/`decode` for transfers).
Composition via `convert(value, from, to)` works for any pair of the 24
implemented color spaces.

260 tests passing (up from 209 at v1.13.0).

### Added — 8 new space modules

- **`src/spaces/rec709.ts`** — Linear Rec.709 (BT.709-6). Same primaries as
  sRGB; matrices reused. The distinction is the transfer (BT.709 OETF, in
  `src/transfer/rec2020.ts` which covers both).
- **`src/spaces/adobe-rgb.ts`** — Linear Adobe RGB (1998). Wider gamut than
  sRGB. D65 white. Bruce Lindbloom matrices.
- **`src/spaces/prophoto.ts`** — Linear ProPhoto / ROMM RGB. Very wide
  gamut. **D50-native** — hub conversion bridges through Bradford CAT to
  D65 transparently.
- **`src/spaces/cielab-d50.ts`** — Traditional CIELAB at D50 (ICC PCS
  convention). Bridges through Bradford to/from the D65 hub.
- **`src/spaces/cielch-d50.ts`** — Polar form of CIELAB_D50.
- **`src/spaces/ictcp.ts`** — BT.2100 HDR opponent encoding. Composes
  Rec.2020 + PQ + opponent matrix. Different from Jzazbz (uses actual
  SMPTE 2084 PQ, not Safdar's adjusted PQ-like).
- **`src/spaces/lms.ts`** — LMS cone response (Ottosson's M1 basis).
  Previously internal to OKLab; now exposed as a first-class space for
  cone-response work.
- **`src/spaces/okhsv.ts`** — Ottosson's perceptual HSV (companion to
  OKHSL). Cusp-shaped Value axis instead of Lightness.

### Added — 2 new transfer modules

- **`src/transfer/adobe-rgb.ts`** — Pure 2.2 gamma (no piecewise).
  Sign-preserving.
- **`src/transfer/prophoto.ts`** — ROMM RGB piecewise: linear (slope 16)
  for $L < 1/512$, power $1/1.8$ above.

### Updated

- **`src/test/roundtrip.ts`** — Registered 8 new space modules (now 24
  total).
- **`src/test/transfers.ts`** — Registered 2 new transfer modules (now 6
  total).
- **`skill.json`** — 10 new files added; version bumped 1.13.0 → 1.14.0.

### Test status

```
roundtrip.ts: 123 passed, 0 failed  (24 space modules)
metrics.ts:    89 passed, 0 failed  (18 modules)
transfers.ts:  48 passed, 0 failed  ( 6 transfer modules)
                                    ────────────────────────────────────────
TOTAL:        260 passed, 0 failed  (48 registered modules)
```

### Feature completeness

**Every** branded color type in `src/types.ts` now has a working space module:

| Type | Module |
|---|---|
| XYZ_D65, LinearSRGB/EncodedSRGB, LinearP3/EncodedP3, LinearRec2020/EncodedRec2020, LinearRec709, **LinearAdobeRGB**, **LinearProPhoto** | ✅ all implemented |
| OKLab, OKLCH, OKHSL, **OKHSV** | ✅ all implemented |
| CIELAB_D65, CIELCH_D65, **CIELAB_D50**, **CIELCH_D50** | ✅ all implemented |
| HSL, HSV, xyY | ✅ |
| CIECAM16_JMh, CAM16_UCS, HCT | ✅ |
| Jzazbz, **ICtCp** | ✅ |
| **LMS** | ✅ |
| SPD | ✅ |

(Bold = new in v1.14.0.)

### Intentionally out of scope (separate domains)

- **CMYK** — print workflows; different color model.
- **YCbCr** — video/JPEG; luma + chroma encoding.
- **CIELUV** — older perceptual lineage; CIELAB is the standard.
- **ICC profile parsing** — requires lcms or equivalent; not pure math.
- **DCI-P3 (theater white)** vs Display P3 — only Display P3 covered.

## [1.13.0] — 2026-05-16 — Lateral sweep: close test-coverage asymmetries

Post-creation audit. Found three asymmetries between TS modules and test
runners, plus a missing transfer-module runner. Closed all gaps. Test count
209/209 passing (up from 165 in v1.12.0).

### Fixed — Orphan test data

Three modules exported test data but no runner consumed them:

- **`src/gamut/oklch-peak.ts`** — Had `testVectors` in a custom shape (with
  `fn: 'peakL_sRGB'` as a string). Converted to standard `MetricTest`
  shape and registered in `metrics.ts`. Now contributes 5 tests including
  P3-wider-than-sRGB sanity check.

- **`src/transfer/{srgb,rec2020,pq,hlg}.ts`** — Had `testVectors` of
  (linear, encoded) pairs but no runner. Created new
  `src/test/transfers.ts` that verifies forward / inverse / round-trip for
  every transfer module. 33 tests across the 4 modules.

### Added — Test coverage for untested modules

- **`src/metrics/luminance.ts`** — Added 6 `testCases`: Y extraction from
  XYZ, BT.709 luminance coefficients, WCAG contrast at extremes (white-on-
  black = 21, identity = 1), and symmetry.

### Added — Transfer test runner

- **`src/test/transfers.ts`** — Third test runner alongside `roundtrip.ts`
  (space modules) and `metrics.ts` (metric/gamut/interp modules). Handles
  the `encode/decode` pair pattern used by transfer functions. Same
  pass/fail formatting and CLI exit codes.

### Acceptable residuals

- **`src/spectral/cmf.ts`** and **`src/spectral/illuminants.ts`** — Pure
  data tables (CIE 1931 CMF, standard illuminant SPDs). Indirectly tested
  by `src/spectral/spd.ts` which integrates them. No direct testCases.
- **`src/types.ts`**, **`src/convert.ts`**, **test runners** — meta /
  infrastructure files; no testCases by design.

### Lateral sweep findings (no action needed)

- **0 broken cross-references** in any math doc I authored.
- **All 32 TS modules** are in `skill.json` files array.
- **All 30 techniques markdowns** are in `skill.json` files array.
- **All 29 branded types** in `src/types.ts` are imported by at least one
  module (verified via grep across `src/`).
- **Markdown ↔ TS pairing**: 26 of 32 TS modules have dedicated math
  markdown companions. Remaining 6 (cielch, oklch, okhsl, xyy, xyz,
  cam16-ucs) are covered transitively in their parent space's doc
  (e.g., `cielch.ts` → covered in `cielab-xyz-conversion.md`). Acceptable.

### Test status (final)

```
roundtrip.ts:  87 passed, 0 failed  (16 space modules)
metrics.ts:    89 passed, 0 failed  (18 metric/gamut/interp/cvd/spectral modules)
transfers.ts:  33 passed, 0 failed  ( 4 transfer modules)
                                    ────────────────────────────────────────
TOTAL:        209 passed, 0 failed  (38 modules registered for test)
```

## [1.12.0] — 2026-05-16 — Closing wave: Tiers 7, 8, 10 + deferred items

Completes the math roadmap. 8 new TS modules + 10 new markdown companions
across spectral colorimetry, pigment mixing, image processing, HDR uniform
spaces, spline interpolation, and esoterica. 165 tests passing.

### Added — Spectral colorimetry (Tier 7)

- **`src/spectral/illuminants.ts`** — Standard illuminant SPDs (36 samples,
  380-730nm @ 10nm): D65, D50, A, E equal-energy, plus the canonical
  `WAVELENGTHS_NM` axis.
- **`src/spectral/cmf.ts`** — CIE 1931 2° color matching functions
  ($\bar{x}, \bar{y}, \bar{z}$) at 10nm steps.
- **`src/spectral/spd.ts`** — `emissiveToXYZ(spd)` and `reflectiveToXYZ
  (reflectance, illuminant)`. Rectangle-rule integration normalized to
  Y = 1 at D65 white. 4 tests passing.
- **`references/techniques/spectral-to-xyz-integration.md`** — Math
  companion covering continuous and discrete forms.

### Added — Pigment mixing (Tier 7)

- **`src/pigment/kubelka-munk.ts`** — Single-constant K-M.
  `reflectanceToKS`/`KSToReflectance`, `mix(a, b, c)`, `mixN(spectra,
  concentrations)`. Blue+yellow really makes green. 5 tests passing
  including the classic white+4%-black → R ≈ 0.074 K-M signature.
- **`references/techniques/kubelka-munk-single-constant.md`** — Math
  companion explaining why RGB averaging fails for paint and what K-M
  fixes.

### Added — Image processing (Tier 8)

- **`src/quantize/kmeans.ts`** — k-means quantization in OKLab.
  k-means++ initialization (deterministic via seeded LCG), Lloyd
  iterations with convergence detection. 2 tests passing including
  cluster recovery on synthetic data.
- **`src/dithering/floyd-steinberg.ts`** — Floyd-Steinberg error
  diffusion. Standard 7/16, 3/16, 5/16, 1/16 distribution applied in
  OKLab for perceptual error metric. 2 tests passing.
- **`references/techniques/color-quantization-math.md`** — k-means
  formulation, Lloyd iteration, k-means++ initialization, comparison
  with octree / median-cut / Wu's algorithm.
- **`references/techniques/dithering-algorithms.md`** — Floyd-Steinberg
  formulas, Bayer matrices, blue noise. The quantize+dither pipeline.

### Added — HDR uniform space (Tier 5 completion)

- **`src/spaces/jzazbz.ts`** — Safdar 2017 Jzazbz forward/inverse with
  PQ-like nonlinearity. Registered in `roundtrip.ts`. 3 tests passing.
  ICtCp deferred (composable from existing PQ + Rec.2020 matrix work).
- **`references/techniques/jzazbz-ictcp-math.md`** — Math companion
  covering both Jzazbz and BT.2100 ICtCp.

### Added — Spline interpolation (Tier 4 completion)

- **`src/interpolation/spline.ts`** — Catmull-Rom cubic in any color
  space. `catmullRomScalar`, `catmullRomTuple`, `catmullRomCurve`
  (through N controls), `catmullRomSamples`. 5 tests passing.
- **`references/techniques/spline-interpolation-color.md`** — Math
  companion explaining why Catmull-Rom over linear, the C1 continuity
  property, and the uniform parameterization.

### Added — Esoterica (Tier 10)

- **`references/techniques/hsluv-hpluv-math.md`** — Boronine's
  CIELUV-normalized HSL. Math only (no TS — OKHSL supersedes for
  modern UI work).
- **`references/techniques/macadam-ellipses-math.md`** — Historical
  context for color-space uniformity. Math + data sources (no TS — ΔE_ok
  / ΔE2000 supersede for practical use).
- **`references/techniques/white-point-conversion.md`** — Standard
  illuminant table + cross-illuminant adaptation via existing Bradford
  CAT. CCT approximation referenced.
- **`references/techniques/pointers-gamut-math.md`** — The empirical
  surface-color gamut. Math + data sources (no TS — specialized use case).

### Test status (final)

```
roundtrip.ts:  87 passed, 0 failed  (16 space modules — adds jzazbz)
metrics.ts:    78 passed, 0 failed  (16 modules — adds spd, kubelkaMunk,
                                     kmeans, floydSteinberg, spline)
                                    ────────────────────────────────────────
TOTAL:        165 passed, 0 failed  (32 modules)
```

### Roadmap status (final)

| Tier | Status |
|---|---|
| **Foundation** | ✅ Complete |
| **Tier 1** (foundational transforms) | ✅ Complete |
| **Tier 2** (comparison & measurement) | ✅ Complete |
| **Tier 3** (gamut operations) | ✅ Done (Pointer math-only) |
| **Tier 4** (generation & interpolation) | ✅ Complete |
| **Tier 5** (appearance models) | ✅ Complete (HSLuv math-only) |
| **Tier 6** (CVD simulation) | ✅ Done (Brettel/Viénot math-only) |
| **Tier 7** (pigment / spectral) | ✅ Done (single-constant K-M; Saunderson and 2-constant deferred) |
| **Tier 8** (image processing) | ✅ Done (k-means + Floyd-Steinberg; Bayer/blue-noise deferred) |
| **Tier 9** (tone mapping / HDR) | ✅ Done (SDR-HDR inverse deferred) |
| **Tier 10** (esoterica) | ✅ Done (MacAdam, white point, Pointer math-only) |

### Known deferrals (intentional, scoped)

- ICtCp TS module (composable from PQ + Rec.2020 matrix)
- HSLuv / CIELUV TS modules (OKHSL supersedes)
- Brettel 1997 / Viénot 1999 TS modules (Machado supersedes)
- Pointer's gamut lookup table (specialized; data is public)
- Uncharted 2 tone-mapping TS (ACES supersedes for production)
- Bayer / blue noise dithering modules (Floyd-Steinberg covers most use)
- Saunderson correction + two-constant K-M (translucent paints)
- SDR → HDR inverse tone mapping (less common direction)

All deferred items have their math documented; TS can be added if
concrete use cases arise.

## [1.11.0] — 2026-05-16 — Tier 9: HDR tone mapping (Reinhard + ACES)

Adds the HDR → SDR compressors that any modern rendering or HDR-content
pipeline needs. Reinhard for prototyping and provable properties; ACES
(Narkowicz) for production use matching cinema/game industry convention.
144 tests total, all passing.

### Added — Tone mapping modules

- **`src/tonemap/reinhard.ts`** — Reinhard 2002 in three variants:
  - `reinhardSimple(x)` — $y = x / (1 + x)$; asymptotic to 1 but never reaches it
  - `reinhardExtended(x, whitePoint)` — maps a chosen $W$ exactly to 1
  - `applyLuminancePreserving(rgb, whitePoint)` — compress Y only, scale RGB
    by the gain (preserves hue at cost of chroma fidelity)
  Per-channel wrappers `applySimple` / `applyExtended`. 6 tests passing
  including endpoint behavior and asymptotic verification.

- **`src/tonemap/aces.ts`** — ACES filmic via Narkowicz's 5-parameter
  rational fit:
  $$y = \frac{x(2.51 x + 0.03)}{x(2.43 x + 0.59) + 0.14}$$
  - `acesNarkowicz(x)` — scalar operator
  - `applyACES(rgb)` — per-channel wrapper
  Asymptotes to $a/c \approx 1.033$ (small overshoot; clip post-tone-map
  for display). 4 tests passing including monotonicity verification.

### Added — Markdown companion

- **`references/techniques/tone-mapping-operators.md`** — Full math doc:
  Reinhard (3 variants), ACES filmic (Narkowicz form), Uncharted 2 (Hable
  6-parameter reference, math only). Includes:
  - Per-channel vs luminance-preserving trade-offs
  - Comparison table at common inputs (Reinhard simple, extended W=4, ACES)
  - Full HDR pipeline: scene-linear → tone-map → defensive clip → sRGB encode
  - Cross-references to PQ/HLG transfers for HDR display output

### Test status (combined runs)

```
roundtrip.ts:  84 passed, 0 failed  (15 space modules)
metrics.ts:    60 passed, 0 failed  (11 modules — adds reinhard, aces)
                                    ────────────────────────────────────────────
TOTAL:        144 passed, 0 failed  (26 modules)
```

### Known gaps (intentional)

- **Uncharted 2 (Hable) TS module** — documented in the markdown for
  reference but not implemented. ACES has superseded Uncharted 2 in most
  modern pipelines.
- **SDR → HDR inverse tone mapping** — the harder direction (expanding
  SDR content to fill HDR range). Useful for legacy-content upscaling;
  deferred.
- **Gamut expansion sRGB → Rec.2020** — composed of chromatic adaptation
  (none needed, both D65) + matrix conversion (already in
  `src/spaces/{srgb,rec2020}.ts`). Trivially composable from existing parts.
- **ACES full pipeline** (input transforms + RRT + ODT) — use the Academy's
  official reference or OpenColorIO. The Narkowicz fit is sufficient for
  99% of cases that aren't VFX color-managed production.

## [1.10.0] — 2026-05-16 — Tier 6: CVD simulation (Machado 2009)

Adds color vision deficiency simulation — the modern accessibility-review
primitive. Machado 2009 (what Chrome DevTools uses) with severity parameter.
50 metrics tests passing; 134 tests total across all modules.

### Added — CVD module

- **`src/cvd/machado-2009.ts`** — Machado 2009 severity-parameterized CVD.
  - `M_PROTANOPIA`, `M_DEUTERANOPIA`, `M_TRITANOPIA` — published severity-1.0 matrices
  - `simulationMatrix(type, severity)` — build matrix for type + severity
  - `simulate(rgb, type, severity)` — apply to a linear sRGB color
  - `simulateProtanopia`, `simulateDeuteranopia`, `simulateTritanopia` — wrappers
  - Linear-interpolation severity approximation against identity for severities
    in (0, 1); note that the Machado paper's full table is non-linear for
    strict-precision intermediate-severity use
  6 test vectors: identity at severity=0, achromatic preservation, white
  preservation, the published pure-red protanopia value (0.152286), and
  severity-midpoint behavior. All passing.

### Added — Markdown companion

- **`references/techniques/cvd-simulation-algorithms.md`** — Consolidated math
  doc covering all three CVD algorithms:
  - **Brettel 1997**: full LMS confusion-line plane projection (foundational).
  - **Viénot 1999**: simplified single-matrix version (legacy compatibility).
  - **Machado 2009**: severity-parameterized matrices (modern default).
  
  All three Machado matrices published in full. Includes the encoded → linear
  → CVD → encoded pipeline (gamma decode before applying matrices is critical).
  Recommends deuteranopia default at severity 0.6 for first-pass accessibility
  review, matching the existing `cvd-simulation-canonical.md` positioning doc.

### Test status (combined runs)

```
roundtrip.ts:  84 passed, 0 failed  (15 space modules)
metrics.ts:    50 passed, 0 failed  ( 9 metric/gamut/adaptation/interp/cvd modules)
                                    ────────────────────────────────────────────
TOTAL:        134 passed, 0 failed  (24 modules)
```

### Known gaps (intentional)

- **Brettel 1997 TS module** — full LMS-confusion-line projection. The math
  is documented; TS implementation deferred because Machado covers ~95% of
  typical accessibility-review use.
- **Viénot 1999 TS module** — superseded by Machado for most practical use.
  Math documented; TS deferred.
- **Anomalous trichromacy** (protanomaly, deuteranomaly, tritanomaly) —
  approximated by severity < 1.0 in the current implementation. Machado's
  paper publishes separate tables; consider adding a dedicated anomalous-
  trichromacy lookup if needed.
- **Full Machado severity table** (33 matrices) — only severity 1.0
  matrices are included; intermediate severities use linear interpolation.
  For strict-precision intermediate-severity use, look up the published
  table from the 2009 paper.

## [1.9.0] — 2026-05-15 — Tier 5: CAM16 family math docs + CAM16-UCS module

Closes the CAM16 family by adding the three math companion docs (CIECAM16,
Material HCT, CAM16-UCS) and a new CAM16-UCS space module with the
ΔE_CAM16 metric. 128 total tests passing (was 125 in v1.8.0).

### Added — CAM16-UCS module

- **`src/spaces/cam16-ucs.ts`** — CAM16 Uniform Colour Space.
  - `fromJMh(jmh)`, `toJMh(ucs)` — direct conversion from/to CIECAM16 JMh
  - `fromXYZ(xyz)`, `toXYZ(ucs)` — hub conversion through CIECAM16
  - `deltaECAM16(a, b)` — Euclidean distance in the UCS (the third major ΔE
    metric alongside ΔE2000 and ΔE_ok)
  - Li et al. 2017 constants: $c_1 = 0.007$, $c_2 = 0.0228$
  Registered in `src/test/roundtrip.ts`; 3 round-trip tests passing.

### Added — Tier 5 markdown companions

- **`references/techniques/ciecam16-forward-inverse.md`** — Full CIECAM16 math:
  CAT16 chromatic adaptation, viewing condition scalar precomputation
  (D, F_L, n, N_bb, N_cb, A_w, z, c), post-adaptation cone response,
  opponent (a, b) signals, J/M/h derivation. Documents the Material
  convention (no +0.1 offset) vs CIE 248 (with offset). Comparison table
  with OKLab and CIELAB.

- **`references/techniques/material-hct-math.md`** — How HCT combines CAM16
  H + CAM16 C + CIELAB L*. Why the inverse is iterative (non-orthogonal
  hybrid). The +40/+50 tone-delta contrast guarantee derivation. Material's
  13-step tonal palette convention. Edge cases for the iterative solver.

- **`references/techniques/cam16-ucs-math.md`** — The (J', a', b') Cartesian
  uniform space. Hyperbolic J rescaling, log-compressed M', polar-to-Cartesian
  for (M, h) → (a', b'). The CAM16-LCD/SCD variant constants for
  large-/small-difference judgment.

### Updated

- **`references/INDEX.md`** — 3 new entries in the techniques table for the
  CAM16 family math docs.
- **`references/MATH-ROADMAP.md`** — Tier 5 status: 3 of 5 ✅ (CAM16 family
  done; HSLuv/HPLuv and Jzazbz/ICtCp still pending). Wave 7 marked DONE.

### Test status (combined runs)

```
roundtrip.ts:  84 passed, 0 failed  (15 space modules — adds cam16-ucs)
metrics.ts:    44 passed, 0 failed  ( 8 metric/gamut/adaptation/interp modules)
                                    ────────────────────────────────────────────
TOTAL:        128 passed, 0 failed  (23 modules)
```

### Known gaps (intentional)

- **HSLuv / HPLuv** — Alexei Boronine's CIELUV-normalized HSL variant.
  No TS yet; markdown deferred until concrete need.
- **Jzazbz / ICtCp** — HDR uniform spaces (Safdar 2017, BT.2100). Useful
  for HDR pipelines; not critical for typical UI work. Deferred.

## [1.8.0] — 2026-05-15 — Tier 4: interpolation (linear + hue paths + cubehelix + lightness ramps)

Closes the gap from "convert single colors" to "produce useful sequences of colors."
The actual workflow for design tokens, ramps, and palettes. 125 total tests, all passing.

### Added — Interpolation modules

- **`src/interpolation/linear.ts`** — Linear interpolation in any color space.
  - `lerpTuple`, `lerpOklab`, `lerpCielab`, `lerpOklch`, `lerpCielch`
  - `lerpHue(h1, h2, t, path)` — all four CSS Color 4 hue paths: `shorter` /
    `longer` / `increasing` / `decreasing`
  - `mixVia(a, b, t, sourceSpace, viaSpace)` — CSS `color-mix(in oklab, ...)` semantics
  - `stops(n)`, `rampOklab(a, b, n)`, `rampOklch(a, b, n, huePath?)` — palette helpers
  9 test vectors covering all four hue paths at the 350°/10° boundary case.

- **`src/interpolation/cubehelix.ts`** — D. A. Green's 2011 perceptually-monotonic
  colormap.
  - `cubehelix(t, opts?)` — single sample → `LinearSRGB`
  - `cubehelixPalette(n, opts?)` — n equally-spaced colors
  - Configurable `start`, `rotations`, `hue`, `gamma`. Defaults match Green's paper.
  5 test vectors verify black/white endpoints and mid-tone luminance ≈ 0.5.

- **`src/interpolation/lightness-curves.ts`** — Ramp curves for design tokens.
  - `linearRamp(t, lMin?, lMax?)` — uniform-step
  - `gammaRamp(t, gamma, lMin?, lMax?)` — γ > 1 slow start, γ < 1 fast start
  - `perceptualRamp(t, lMin?, lMax?)` — alias for linear (OKLab L is already perceptual)
  - `smoothstepRamp(t, lMin?, lMax?)` — soft endpoints
  - `TAILWIND_V4_L_STOPS` + `tailwindV4LAtStep(step)` — published 11 stops
    (50, 100, 200, ..., 950) in OKLab L
  - `RADIX_THEMES_3_L_STOPS_LIGHT` + `radixLightLAtStep(step)` — published 12-step
    semantic palette
  10 test vectors covering all four curve types and published stop accuracy.

### Added — Markdown companions

- **`references/techniques/gradient-interpolation-math.md`** — The
  perceptual-vs-physical interpolation argument, why OKLab is the default, full
  hue-path formulas (folds in the planned `hue-interpolation-paths.md` and
  `color-mix-algorithm.md`).

- **`references/techniques/cubehelix-formula.md`** — Green's three RGB equations,
  parameter table with effects, worked 5-step palette, why it beats "jet" /
  "rainbow" for scientific viz.

- **`references/techniques/lightness-ramp-curves.md`** — Curve comparison,
  Tailwind v4 and Radix Themes 3 published stop tables with semantic role
  explanations, worked example of building an 11-step palette in OKLCh.

### Updated — Test infrastructure

- **`src/test/metrics.ts`** — Registered `linearInterp`, `cubehelix`,
  `lightnessCurves` modules. Now covers 8 modules / 44 tests (up from 5/20).

### Test status (combined runs)

```
roundtrip.ts:  81 passed, 0 failed  (14 space modules)
metrics.ts:    44 passed, 0 failed  ( 8 metric/gamut/adaptation/interp modules)
                                    ────────────────────────────────────────────
TOTAL:        125 passed, 0 failed  (22 modules)
```

### Known gaps (intentional)

- **Spline interpolation** (`src/interpolation/spline.ts`) — Catmull-Rom and
  Bezier in OKLab. Useful for non-uniform palette stops; deferred until needed.
- **Pointer's gamut** — still pending from Tier 3.
- **Tier 5 markdown companions** (CIECAM16, HCT, CAM16-UCS math docs) — TS
  already exists; markdown could be written from existing TS header comments.

## [1.7.0] — 2026-05-15 — Tier 3: gamut mapping + Ottosson cusp algorithm

Adds the hue-preserving gamut mapping infrastructure that design-token work needs:
the CSS Color 4 normative algorithm + Ottosson's closed-form cusp solver. 94/94
prior tests remain passing; metrics runner now covers 5 modules (20 tests total
across deltaE, apca, bradford, cusp, mapping).

### Added — Gamut operations

- **`src/gamut/cusp.ts`** — Ottosson's closed-form cusp algorithm for sRGB.
  - `maxSaturationSRGB(a, b)` — max $C/L$ along a unit-norm hue ray
  - `findCuspSRGB(a, b)` — $(L_{cusp}, C_{cusp})$ at hue direction
  - `findCuspSRGBFromHueDeg(hueDeg)` — convenience over degrees
  Faithful port of Ottosson 2021 reference C++ — three-face polynomial selection
  + one Halley's-method refinement step. Test vectors verified at the
  red/green/blue hue extrema.

- **`src/gamut/mapping.ts`** — CSS Color 4 gamut mapping (W3C normative algorithm).
  - `mapToGamutOklch(origin, toRGBMatrix, inGamutFn)` — generic mapper
  - `mapToSRGB(oklch)`, `mapToP3(oklch)`, `mapToRec2020(oklch)` — wrappers per gamut
  - `inGamutSRGB`, `inGamutP3`, `inGamutRec2020` — predicates
  - `clipNaive(rgb)` — for comparison / last-mile float-drift trimming
  Binary search on OKLCh chroma with $\Delta E_{ok} < 0.02$ JND early-exit. Hue
  and lightness preserved; only chroma is reduced. Test vectors verify in-gamut
  passthrough, out-of-gamut reduction lands in $[0, 1]^3$, $L \ge 1$ → white,
  $L \le 0$ → black.

- **`src/gamut/oklch-peak.ts`** updated — exported the `inGamut` helper for reuse
  across modules (previously local).

### Added — Markdown companions

- **`references/techniques/css-color-4-gamut-mapping.md`** — Full algorithm walkthrough.
  Why naive clipping shifts hue, the JND optimization, two-phase binary search (strict
  in-gamut, then JND-tolerant), and a comparison table for clipping vs mapping.
  Folds in the planned `gamut-clipping-vs-mapping.md` content.

- **`references/techniques/ottosson-cusp-algorithm.md`** — Why a closed form exists
  (cubic-in-$L$ gamut boundary), three-face selection criterion with polynomial
  coefficients, Halley's-method refinement equations, and a precomputed cusp
  table for selected sRGB hues.

### Updated — Test infrastructure

- **`src/test/metrics.ts`** — Registered `cusp` and `mapping` modules. Now covers
  5 modules / 20 tests (was 3 modules / 13 tests in v1.6.0).

### Test status (combined runs)

```
roundtrip.ts: 81 passed, 0 failed  (14 space modules)
metrics.ts:   20 passed, 0 failed  ( 5 metrics/gamut/adaptation modules)
                                   ────────────────────────────────────
TOTAL:       101 passed, 0 failed  (19 modules)
```

### Known gaps (intentional)

- **Cusp for P3 / Rec.2020** — same algorithm structure with re-derived polynomial
  coefficients per face. Deferred until concrete need.
- **Pointer's gamut** — empirical real-surface gamut boundary; useful for
  print/physical-media work. Not implemented.
- **Cusp-based analytic gamut mapping** — Ottosson's faster alternative to the
  binary search; would compose cusp + linear interpolation. Deferred.

## [1.6.0] — 2026-05-15 — Tier 2: ΔE family + APCA + chromatic adaptation

Adds the three high-leverage Tier 2 metric modules with their markdown
companions. All 13 metrics tests pass alongside the 81 space round-trip tests
from v1.5.0 (94 total tests, all passing).

### Added — Metrics

- **`src/metrics/deltaE.ts`** — Five color-difference formulas:
  - `deltaE76(a, b)` — Euclidean CIELAB (CIE 1976)
  - `deltaE94(a, b, textiles?)` — CIE 1994 with graphic-arts / textile weights
  - `deltaE2000(a, b, kL?, kC?, kH?)` — Sharma/Wu/Dalal 2005 implementation
    with rotational term; the current gold standard
  - `deltaEOK(a, b)` — Euclidean in OKLab; modern recommended default
  - `hyAB(a, b)` — Hybrid Euclidean-L + city-block-(a, b) for large differences

  Test vectors include Sharma 2005 Table 1 pairs 1 and 2 (the canonical
  numerical-correctness check). All 7 tests pass.

- **`src/metrics/apca.ts`** — APCA L^c contrast (APCA-W3 v0.1.9 constants).
  Polarity-sensitive: positive for dark-text-on-light, negative for
  light-text-on-dark. Uses simplified 2.4 power gamma with near-black soft
  clamp. Exports `apcaY`, `apcaContrast`, and `readabilityTier` (Bronze
  Simple Mode tier labels). Verified against APCA-W3 reference outputs
  (pure black-on-white ≈ 106, pure white-on-black ≈ -107.88).

### Added — Chromatic adaptation

- **`src/adaptation/bradford.ts`** — Bradford CAT (the ICC / CSS Color 4
  standard). Exports `M_BRADFORD` / `M_BRADFORD_INV`, pre-computed
  illuminant XYZ values (`D65`, `D50`, `A`, `F2`), the generic
  `bradfordMatrix(srcWhite, dstWhite)` builder, single-color `adapt()`,
  and `d50ToD65` / `d65ToD50` convenience wrappers with pre-computed
  matrices `M_D50_TO_D65` / `M_D65_TO_D50`. Round-trip verified within
  $10^{-6}$ tolerance (published Bradford matrices are 7-digit precision).

### Added — Test infrastructure

- **`src/test/metrics.ts`** — Test runner for non-space modules (ΔE, APCA,
  Bradford). Iterates each module's `testCases: ReadonlyArray<MetricTest>`,
  formats pass/fail per module, CLI exit code reflects status.

### Added — Markdown companions (Tier 2)

- **`references/techniques/delta-e-formulas.md`** — Full mathematical
  treatment of all five ΔE variants. ΔE2000 with all 19 sub-steps including
  the rotational term and JND-magnitude guidance. Cross-references Sharma
  2005 Table 1 test data.

- **`references/techniques/apca-lc-formula.md`** — The L^c formula in full,
  with BoW / WoB polarity branches, near-black soft clamp derivation, and
  the Bronze Simple Mode readability tier table. Positions APCA as the
  modern design standard per the existing skill direction.

- **`references/techniques/chromatic-adaptation-matrices.md`** — Bradford
  and CAT16 matrices, the von Kries diagonal-scaling rationale, white-point
  reference values for D50/D55/D65/A/F2, and the Bradford-vs-CAT02-vs-CAT16
  comparison table.

### Updated

- **`references/INDEX.md`** — 3 new techniques table entries with markdown
  ↔ TS pairings.
- **`references/MATH-ROADMAP.md`** — Tier 2 marked ✅ (4 of 4 effective
  files; `wcag-contrast-ratio-math.md` consolidated into
  `relative-luminance-derivation.md`). Wave 4 noted DONE.

### Test status (combined runs)

```
roundtrip.ts: 81 passed, 0 failed  (14 space modules)
metrics.ts:   13 passed, 0 failed  ( 3 metrics modules)
                                   ──────────────────────
TOTAL:        94 passed, 0 failed  (17 modules)
```

### Known gaps (intentional)

- **CAT02 and Von Kries** — not yet implemented as separate modules.
  CAT16 is embedded in `src/spaces/ciecam16.ts`. Future:
  `src/adaptation/{cat02,cat16,vonkries}.ts`.
- **CIELAB-D50 module** — once Bradford exists, a CIELAB-D50 variant becomes
  straightforward; not yet written. Same for `xyy-D50`.
- **APCA font-size × weight tables** — only the Bronze Simple Mode tier
  labels are implemented. The full lookup table (per font weight × size)
  belongs in a future `apca-font-tables.ts` data module.

## [1.5.0] — 2026-05-15 — CIECAM16/HCT refinement + 6 Tier 1 markdown companions

Completes Wave 1/2 markdown companions and stabilizes the 🟡 modules. All 14 TS
modules now pass round-trip identity tests (81/81 passing, up from 74/75).

### Fixed — CIECAM16

- **Post-adaptation cone response** (`adaptResponse` / `unadaptResponse`): dropped the
  `+0.1` offset specified in CIE 248:2022. Standard formula gives non-zero achromatic
  response at black; Material color-utilities convention drops the offset so $J = 0$
  at black. This skill follows Material for HCT compatibility.
- **Default viewing condition white point**: was using ASTM-rounded $(95.047, 100,
  108.883)$, which mismatches the W3C high-precision D65 used by `src/types.ts:xyz(...)`
  by ~0.02 in Z and produced spurious residual chroma at the white point. Now uses the
  matching W3C values.
- **Default adapting luminance**: clarified the derivation — $L_a = (200/\pi) \cdot
  Y(L^*\!=\!50) / 100 \approx 11.72$ cd/m² — matching Material's default.

### Documented — HCT white-point residual chroma

HCT under `discountingIlluminant: false` produces ~2.3 residual chroma at the D65
white point. This is mathematically correct for partial chromatic adaptation but
differs from Material's HCT solver, which biases toward zero for near-achromatic
inputs. For Material-faithful behavior, either set `discountingIlluminant: true` or
use a gamut-aware HCT solver (planned: `src/gamut/hct-solver.ts`).

### Added — Tier 1 markdown companions (6 files)

Each pairs with its canonical TS module per `ARCHITECTURE.md`:

- **`references/techniques/gamma-transfer-functions.md`** — sRGB / P3 / Rec.709 /
  Rec.2020 / PQ / HLG with formulas, sign-preserving implementation pattern, edge
  cases, primary sources (IEC 61966-2-1, BT.2020, BT.2100, ST 2084, ARIB STD-B67).
  Paired with `src/transfer/{srgb,rec2020,pq,hlg}.ts`.

- **`references/techniques/xyz-rgb-conversion-matrices.md`** — sRGB / Display P3 /
  Rec.2020 ↔ XYZ-D65 matrices at W3C high precision, derivation from primaries +
  white point, why D65 universally. Paired with `src/spaces/{srgb,p3,rec2020}.ts`.

- **`references/techniques/cielab-xyz-conversion.md`** — $f(t)$ cube-root
  nonlinearity, D65 reference white, polar CIELCH, when to prefer OKLab. Paired with
  `src/spaces/{cielab,cielch}.ts`.

- **`references/techniques/relative-luminance-derivation.md`** — Y from XYZ / linear
  sRGB / encoded sRGB, the WCAG $(L_1 + 0.05)/(L_2 + 0.05)$ formula, AA/AAA thresholds,
  why APCA is better. Paired with `src/metrics/luminance.ts`.

- **`references/techniques/cylindrical-rgb-conversions.md`** — HSL/HSV ↔ encoded sRGB,
  hue-sector formulas, why these aren't perceptual. Paired with `src/spaces/{hsl,hsv}.ts`.

- **`references/techniques/oklab-xyz-math.md`** — Ottosson's $M_1$/$M_2$ matrices
  (forward and inverse), cube-root nonlinearity, polar OKLCH form, sign-preserving
  cube root requirement. Paired with `src/spaces/{oklab,oklch}.ts`.

### Updated

- **`references/INDEX.md`** — 6 new entries in the techniques table cross-linking
  markdown ↔ TS pairs.
- **`references/MATH-ROADMAP.md`** — Tier 1 fully complete (all 6 files ✅). Wave 3
  marked DONE. CIECAM16/HCT status note updated (🟡 → ✅).

### Test status

```
✓ xyz: 3 passed       ✓ srgb: 15 passed       ✓ p3: 6 passed
✓ rec2020: 6 passed   ✓ oklab: 12 passed       ✓ oklch: 3 passed
✓ cielab: 9 passed    ✓ cielch: 6 passed       ✓ hsl: 3 passed
✓ hsv: 3 passed       ✓ xyy: 6 passed          ✓ okhsl: 3 passed
✓ ciecam16: 3 passed  ✓ hct: 3 passed
TOTAL: 81 passed, 0 failed
```

## [1.4.0] — 2026-05-15 — Color math system: foundation + 14 space modules + 4 transfer functions

Demonstrates the architecture end-to-end. Adds 20 TypeScript modules implementing the
contract from `ARCHITECTURE.md` (`toXYZ()` / `fromXYZ()` + `testVectors`). All modules
compose through the XYZ_D65 hub via `src/convert.ts`. The `src/test/roundtrip.ts` runner
verifies forward and round-trip identity for every registered module.

### Added — Foundation

- **`src/convert.ts`** — Generic registry-based conversion. `convert(value, fromMod, toMod)`
  composes through XYZ_D65 hub. Establishes `SpaceModule<T>` contract.
- **`src/test/roundtrip.ts`** — Test runner. For every registered module, checks
  three properties per test vector: forward (`fromXYZ(input) ≈ output`), round-trip
  from input (`toXYZ(fromXYZ(input)) ≈ input`), round-trip from output. Formats
  results with module-level pass/fail and per-vector failure details. CLI exit code
  reflects status. Currently registers 14 modules.

### Added — Spaces

- **`src/spaces/xyz.ts`** — Identity module for XYZ_D65. Makes the hub a uniform
  participant in the registry.
- **`src/spaces/srgb.ts`** — Linear sRGB ↔ XYZ_D65 (IEC 61966-2-1 matrices).
- **`src/spaces/p3.ts`** — Linear Display P3 ↔ XYZ_D65 (W3C CSS Color 4).
- **`src/spaces/rec2020.ts`** — Linear Rec.2020 ↔ XYZ_D65 (ITU-R BT.2020).
- **`src/spaces/oklch.ts`** — OKLCH polar form, composes via OKLab.
- **`src/spaces/cielab.ts`** — CIELAB_D65 ↔ XYZ_D65 (CIE 015:2018, cube-root nonlinearity).
- **`src/spaces/cielch.ts`** — CIELCH polar form, composes via CIELAB.
- **`src/spaces/hsl.ts`** — HSL ↔ XYZ_D65 via encoded sRGB. CSS-convention cylindrical.
- **`src/spaces/hsv.ts`** — HSV ↔ XYZ_D65 via encoded sRGB.
- **`src/spaces/xyy.ts`** — xyY chromaticity + luminance form.
- **`src/spaces/okhsl.ts`** — Ottosson's perceptual HSL with cusp finding. 🟡 loose
  tolerance — port of Ottosson's reference JS; cross-check against canonical for
  strict-precision use.
- **`src/spaces/ciecam16.ts`** — CIECAM16 (JMh form). Forward and inverse with
  configurable `ViewingConditions`; defaults baked in for Material HCT setup
  (D65, average surround, La≈64, Yb≈18). 🟡 cross-check against CIE 248:2022.
- **`src/spaces/hct.ts`** — Material Design 3 HCT (Hue + Chroma + Tone). Combines
  CAM16 hue/chroma with CIELAB L*. 🟡 simple iterative inverse — for adversarial
  inputs prefer material-color-utilities reference.

### Added — Transfer functions

- **`src/transfer/srgb.ts`** — IEC 61966-2-1 piecewise transfer. Also used by Display P3.
  Sign-preserving for out-of-range values.
- **`src/transfer/rec2020.ts`** — ITU-R BT.2020 OETF (also covers Rec.709).
- **`src/transfer/pq.ts`** — SMPTE ST 2084 / BT.2100 PQ. Absolute HDR (1.0 = 10,000 nits).
  Includes `encodeNits` / `decodeNits` for cd/m² inputs.
- **`src/transfer/hlg.ts`** — BT.2100 HLG (Hybrid Log-Gamma). Relative HDR with
  log-gamma upper segment.

### Added — Metrics

- **`src/metrics/luminance.ts`** — Relative luminance Y from XYZ / linear sRGB /
  encoded sRGB. WCAG 2.x contrast ratio. `passesAA` / `passesAALarge` / `passesAAA`
  threshold helpers.

### Updated — Types

- **`src/types.ts`** — Added `xyY`, `OKHSL`, `OKHSV` branded types and construction
  helpers; added `hct`, `ciecam16_JMh`, `xyY`, `okhsl`, `okhsv` construction helpers
  for existing brands.

### Updated — Roadmap

- **`references/MATH-ROADMAP.md`** — Wave 0/1/2 marked DONE. Status flags updated
  for all 14 spaces + 4 transfer + 1 metrics + 1 gamut module. Existing
  markdown-only references re-categorized (`brucelindbloom-color-math.md` is now
  superseded by the per-space TS modules).

### How to use

```ts
import * as srgb from './src/spaces/srgb.js';
import * as oklab from './src/spaces/oklab.js';
import * as srgbTransfer from './src/transfer/srgb.js';
import { convert } from './src/convert.js';

// Encoded sRGB → OKLab via the hub
const encoded = [0.5, 0.3, 0.8] as EncodedSRGB;
const linear = srgbTransfer.decode(encoded);
const oklabValue = convert(linear, srgb, oklab);
```

```bash
# Run round-trip verification:
bun src/test/roundtrip.ts
# or tsx / ts-node
```

## [1.3.0] — 2026-05-15 — System architecture: XYZ-D65 source of truth + TypeScript foundation

### Architecture decisions

Math references are now part of a coherent, bidirectional, typed system — not a
collection of disparate explanations. Locked decisions:

1. **Source of truth**: CIE XYZ at D65. Every space converts to/from this hub.
2. **Optional richer SoT**: Spectral SPD (36 samples, 380–730nm @ 10nm) for pigment
   and metamerism work, bridges via `spectrumToXyzD65()`.
3. **Language**: TypeScript with branded types. Space-mixing fails at compile time.
4. **Bidirectionality contract**: every space module exports `toXYZ()` + `fromXYZ()`.
5. **Composition**: A → B is always `B.fromXYZ(A.toXYZ(value))` through the hub.
6. **Prose in `references/`, code in `src/`**. Markdown explains; TS executes.
7. **No automatic gamut clipping** inside conversions. Out-of-gamut values stay as
   numbers; clipping is a separate explicit concern.

### Added

- **`references/ARCHITECTURE.md`** — The 10 architectural decisions with rationale,
  the `src/` directory layout, the bidirectionality contract, the markdown ↔ TS
  pairing pattern, and the checklist for a complete new math reference.

- **`src/types.ts`** — Branded color types for every space (`XYZ_D65`, `OKLab`,
  `OKLCH`, `LinearSRGB`, `EncodedSRGB`, `LinearP3`, `LinearRec2020`, `CIELAB_D65`,
  `CIELAB_D50`, `HSL`, `HSV`, `CIECAM16_JMh`, `CAM16_UCS`, `HCT`, `Jzazbz`, `ICtCp`,
  `LMS`, `SPD`), construction helpers, `Matrix3x3` type with `mulMat3Vec3` /
  `mulMat3Mat3`, sign-preserving `cbrt`, hue-wrapping `wrapHueDeg`, `TestVector`
  contract, and tolerance constants.

- **`src/spaces/oklab.ts`** — Canonical example of a space module. OKLab ↔ XYZ_D65
  via Ottosson's $M_1$ / $M_2$ matrices (forward and inverse). Test vectors from
  Ottosson 2020. Demonstrates the bidirectionality + branded-type pattern every
  future space module follows.

- **`src/gamut/oklch-peak.ts`** — Canonical example of a gamut module. `peakL(C, h,
  toRGB)`, `peakC(L, h, toRGB)`, `peakLOverHue(C, toRGB)`, plus gamut-specific
  wrappers (`peakL_sRGB`, `peakC_P3`, `peakL_Rec2020`, etc.). Exports the three
  XYZ → linear-RGB matrices for sRGB, Display P3, and Rec.2020. Composes with
  `src/spaces/oklab.ts`.

### Updated

- **`references/techniques/oklch-gamut-peak-math.md`** — "Implementation" section
  now links to `src/gamut/oklch-peak.ts` as the canonical TS implementation;
  production-library table updated with "This skill" as the first row.

- **`references/MATH-ROADMAP.md`** — Authoring conventions split into "what goes in
  markdown" and "what goes in TypeScript." Status legend extended (✅ docs+code, 🟡
  markdown only, 🔲 planned, ⚙️ partial). Wave 0 (foundation) marked DONE.
  Existing math references re-evaluated: `oklch-gamut-peak-math.md` is the only one
  with paired TS as of v1.3.0; others are markdown-only and have TS work pending.

### Why this matters

Before v1.3.0, each math reference was a standalone explainer. They couldn't
compose; nothing prevented an agent from passing OKLab values where the function
wanted CIELAB; round-trip identity was an aspiration, not a verifiable property.

After v1.3.0, every future math reference plugs into a system where conversion
between any two spaces is one line, type errors catch space-mixing at compile time,
and `testVectors` make round-trip identity mechanically checkable.

## [1.2.0] — 2026-05-15 — Math algorithms: OKLCH gamut boundary + math roadmap

### Added

- **`references/MATH-ROADMAP.md`** — Prioritized 10-tier roadmap of 41 color-math references for future authoring. Documents what's already covered (4 files), what's planned (34 new), and what's partially covered as tooling that could be split out into dedicated math docs (7 topics). Includes authoring conventions established by `oklch-gamut-peak-math.md` (LaTeX format, full matrices not pointers, pseudocode per algorithm, edge cases, production-library map, primary-source citations) and a suggested 6-wave execution plan.

- **`references/techniques/oklch-gamut-peak-math.md`** — Mathematical derivation for $L_\text{peak}(C, h)$ and $C_\text{peak}(L, h)$ in OKLCH against sRGB, Display P3, and Rec.2020 gamuts. Covers: the full OKLCH → linear-RGB pipeline with Ottosson's $M_1$ and $M_2$ matrices (and their inverses); the three XYZ → linear-RGB matrices (sRGB / P3 / Rec.2020); why each channel is a cubic polynomial in $L$ at fixed $(C, h)$; binary-search and analytic algorithms for both peak directions; the symmetric $C_\text{peak}(L, h)$ problem (more useful for design tokens than $L_\text{peak}$); peak across all hues; production-library map (Culori, @texel/color, Color.js, Ottosson's reference C); edge cases and numerical notes; primary-source citations to Ottosson 2020/2021, W3C CSS Color 4, IEC 61966-2-1, SMPTE EG 432-1, ITU-R BT.2020.

- **SKILL.md "Gamut Math — Peak Lightness and Peak Chroma in OKLCH" section** — Concise summary of the misconception (no closed-form $L_\text{peak}(C)$), the underlying reason (cubic-in-$L$ envelope from the LMS³ nonlinearity), the binary-search algorithm, and a pointer to the full math reference. Positioned between "Color Spaces" and "Implementation Guidance" — establishes the computational context for the rest of the implementation guidance.

### Source

User-provided derivation (OKLCH peak component derivations) cleaned up and extended:
- Replaced broken `[...]` math notation with proper LaTeX `$$...$$` / `$...$`.
- Added the missing Ottosson $M_1$ and $M_2$ matrices and their inverses (the source referenced them but didn't provide values).
- Added the Rec.2020 XYZ→linear-RGB matrix.
- Added the symmetric $C_\text{peak}(L, h)$ problem with implementation.
- Added the linear-vs-gamma-encoded distinction (gamut test on linear; gamma encoding is for display).
- Added Ottosson's analytic cusp algorithm reference for fast $C_\text{peak}$ in production.
- Added the production-library map (Culori, @texel/color, Color.js, reference C).

## 0.3.0 — 2026-05-07 — Improved Naming Convention

- Renamed from `expert-color` to `ref-color` per the ref- domain/verb convention.
- All cross-references updated.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `color-expert` to `expert-color` per the `expert-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

All notable changes to the local copy of the `expert-color` skill are tracked here. Upstream changelog (if any) lives in the source repo at https://github.com/meodai/skill.expert-color.

## [1.1.0] — 2026-04-26 — Modern color stack refresh (APCA-as-standard + CSS Color 4/5/6 + Tailwind v4 + Material HCT)

### Position change (per user direction)

**APCA is now positioned as the modern contrast standard.** WCAG 2.2 is the current legal floor. Stop waiting for WCAG 3 to bless APCA — the algorithm is mature and the W3C draft has no contrast algorithm at all (realistic Recommendation: 2027–2028). Use APCA as the design standard; clear WCAG 2.2 AA for compliance.

### Added (7 new files)

- **`references/techniques/css-color-2026-snapshot.md`** — L4/L5/L6 spec map; per-feature baseline-interop snapshot (oklch / color-mix / relative color syntax / light-dark / contrast-color all Baseline by Apr 2026); the modern token recipe (one OKLCH anchor → full dual-mode palette via `oklch(from …)` + `color-mix` + `light-dark` + `contrast-color`); known gotchas.
- **`references/techniques/wcag-2-2-current-legal-floor.md`** — WCAG 2.2 as the legal floor; new SCs (2.4.11/2.4.12/2.4.13 Focus Not Obscured/Appearance, 2.5.8 Target Size); what 2.x does NOT address (polarity, spatial frequency, modern color spaces); honest WCAG 3 status; recommended stance (use APCA for design + WCAG 2.2 for compliance).
- **`references/contemporary/material-hct-color-space.md`** — HCT = CAM16 hue + CAM16 chroma + CIE L\* tone; +40/+50 tone-delta contrast guarantee; vs OKLCH; Material 3 tonal palettes; `material-color-utilities`.
- **`references/techniques/tailwind-v4-oklch-palette.md`** — Tailwind v4 (Jan 2025) OKLCH-based default palette targeting Display P3; v4.2 added Mauve/Olive/Mist/Taupe; the largest design-system migration of 2025.
- **`references/techniques/radix-themes-3-p3.md`** — Radix Themes 3.0 (Mar 2024) added P3 wide-gamut + alpha versions; 12-step semantic scales mapped to UI states; custom palette generator.
- **`references/contemporary/cvd-simulation-canonical.md`** — Brettel-1997, Viénot-1999, Machado-2009; Chrome DevTools "Emulate vision deficiencies"; recommended stance (default to deuteranopia, severity 0.6 not 1.0, pair color with non-color cues).
- **`references/contemporary/ciecam16-cam16-ucs.md`** — CIECAM16 (CIE 2022) fixes CIECAM02's matrix-inversion issue; CAM16-UCS recommended by CIE TC 8-11 as the official Uniform Colour Space; how HCT relates.

### Fixed (existing-file patches)

- **`references/techniques/apca-myndex-contrast.md` "What APCA Is" section.** Reframed: APCA is the **modern contrast standard for design work**. Use APCA; treat WCAG 2.2 as legal floor only. Honest note on W3C status (removed from WCAG 3 in 2023; no contrast algorithm in March 2026 draft) but emphasizes APCA's substance is unchanged and adoption is mature.
- **`references/techniques/w3c-css-color-4-and-5.md` spec map.** Was: lumped `contrast-color()` under L5. Fixed: `contrast-color()` is L6 (Chrome 147 / Firefox 146 / Safari 26). L5 originally had `color-contrast()` which was dropped from CSS. Added L6 section. File now covers L4 + L5 + L6.

### Policy change

- **`skill.json` `status`**: `external` → `external-with-local-additions`. Per user direction, the strict upstream-first policy is relaxed for this refresh. Local additions cover the modern color stack; upstream sync remains the goal where it doesn't conflict with this refresh.

### Could-not-verify (flagged in files)

- `apca-w3` npm package version as of Apr 2026 — likely 0.1.x family but unverified.
- Color Buddy active maintenance status — unverified.
- `@texel/color` perf claims — repo's own benchmark; no third-party verification.
- "281T hex pairs" study — math checks out but underlying Rust code link not verified.

### Bookkeeping

- `skill.json` → v1.1.0; description rewritten to surface APCA-as-standard, CSS Color 4/5/6, Tailwind v4, Radix Themes 3, Material HCT, CIECAM16, CVD math; tags expanded.
- `references/INDEX.md` row additions deferred to a follow-up bookkeeping pass — INDEX has 148 existing rows and the new files are surfaced via cross-references in the patched apca / css-color files.

---

## [1.0.0] — 2026-04-17

### Added

- Initial import from upstream https://github.com/meodai/skill.expert-color (main branch, shallow clone, `.git` stripped).
- Added local `skill.json` and this `CHANGELOG.md` to satisfy the team's skill-directory convention. Neither exists upstream.

### Notes

- This skill is maintained **upstream**, not in-tree. Resync with upstream via git rather than hand-editing files here. If local divergence becomes necessary, document it in this changelog and fork the upstream repo cleanly.
- Peers with the internal `ui-verify-color` skill. They cover different surfaces: `expert-color` is broad knowledge (color science, history, pigment mixing, CVD, APCA vs WCAG); `ui-verify-color` is a narrow OKLCH-ramp derivation tool. Both can be active.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.
