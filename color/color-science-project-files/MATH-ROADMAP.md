# Color Math References — Roadmap

A prioritized roadmap of math-algorithm reference files, now distributed across the
four `color-*-facts` packs' `references/techniques/` (split 2026-07-06), **paired
with** TypeScript implementations under `src/` (kept here, in
`color-science-project-files`). The goal: each file is a markdown description
(natural language + LaTeX) **plus** a working TS module (branded-typed,
bidirectional, test-vector-verified) that fits into the system defined by
[`ARCHITECTURE.md`](ARCHITECTURE.md).

**Every new file must satisfy the contract in `ARCHITECTURE.md`:**
- ✅ Source of truth is `XYZ_D65`
- ✅ Every space module exports `toXYZ()` and `fromXYZ()`
- ✅ Composition is `B.fromXYZ(A.toXYZ(value))` through the hub
- ✅ Branded types catch space-mixing at compile time
- ✅ `testVectors` array with primary-source citations
- ✅ Round-trip identity verified within stated tolerance

**Status legend**: ✅ documented (markdown + TS) · 🟡 markdown only · 🔲 planned ·
⚙️ partial (covered as tooling, math could be split out)

---

## Foundation (must exist for the system to compose)

| File | What it covers |
|---|---|
| ✅ `ARCHITECTURE.md` | The 10 architectural decisions: XYZ-D65 source of truth, branded types, bidirectionality contract, src/ layout, prose-vs-code split. |
| ✅ `src/types.ts` | Branded color types (22+ spaces), Matrix3x3, mulMat3Vec3/mulMat3Mat3, sign-preserving cbrt, wrapHueDeg, TestVector contract, tolerance constants. |
| ✅ `src/convert.ts` | Generic registry-based conversion: `convert(value, fromModule, toModule)` through the XYZ_D65 hub. |
| ✅ `src/test/roundtrip.ts` | Test runner: every registered module's testVectors checked for forward + round-trip identity. CLI exit code reflects pass/fail. |

## Spaces (Wave 0 — DONE 2026-05-15)

Every entry has both markdown (or TS-header equivalent) and TypeScript implementation,
with forward + inverse and primary-source-cited test vectors.

| Module | Hub direction | Status |
|---|---|---|
| ✅ `src/spaces/xyz.ts` | XYZ_D65 identity | Trivial — for registry uniformity |
| ✅ `src/spaces/srgb.ts` | Linear sRGB ↔ XYZ_D65 | IEC 61966-2-1 matrices |
| ✅ `src/spaces/p3.ts` | Linear Display P3 ↔ XYZ_D65 | W3C CSS Color 4 / SMPTE EG 432-1 |
| ✅ `src/spaces/rec2020.ts` | Linear Rec.2020 ↔ XYZ_D65 | ITU-R BT.2020 |
| ✅ `src/spaces/oklab.ts` | OKLab ↔ XYZ_D65 | Ottosson 2020 matrices |
| ✅ `src/spaces/oklch.ts` | OKLCH (polar) ↔ XYZ_D65 | via OKLab |
| ✅ `src/spaces/cielab.ts` | CIELAB_D65 ↔ XYZ_D65 | CIE 015:2018 |
| ✅ `src/spaces/cielch.ts` | CIELCH_D65 (polar) ↔ XYZ_D65 | via CIELAB |
| ✅ `src/spaces/hsl.ts` | HSL ↔ XYZ_D65 | via encoded sRGB |
| ✅ `src/spaces/hsv.ts` | HSV ↔ XYZ_D65 | via encoded sRGB |
| ✅ `src/spaces/xyy.ts` | xyY (chromaticity) ↔ XYZ_D65 | CIE 1931 |
| 🟡 `src/spaces/okhsl.ts` | OKHSL ↔ XYZ_D65 | Ottosson 2021 — cusp-mapped; loose tolerance |
| 🟡 `src/spaces/ciecam16.ts` | CIECAM16 (JMh) ↔ XYZ_D65 | CIE 248:2022 — default viewing conditions baked in |
| 🟡 `src/spaces/hct.ts` | Material HCT ↔ XYZ_D65 | Material Design 3 — naive iterative inverse |

## Transfer functions (Wave 0 — DONE 2026-05-15)

| Module | Covers | Source |
|---|---|---|
| ✅ `src/transfer/srgb.ts` | sRGB + Display P3 (shared transfer) | IEC 61966-2-1 |
| ✅ `src/transfer/rec2020.ts` | Rec.2020 + Rec.709 (shared formula) | ITU-R BT.2020 / BT.709 |
| ✅ `src/transfer/pq.ts` | BT.2100 PQ (Perceptual Quantizer) | SMPTE ST 2084 |
| ✅ `src/transfer/hlg.ts` | BT.2100 HLG (Hybrid Log-Gamma) | ARIB STD-B67 |

## Metrics (Wave 0 — DONE 2026-05-15)

| Module | What |
|---|---|
| ✅ `src/metrics/luminance.ts` | Relative luminance Y, WCAG 2.x contrast ratio, AA/AAA pass helpers |

## Gamut (Wave 0 — DONE 2026-05-15)

| Module | What |
|---|---|
| ✅ `src/gamut/oklch-peak.ts` | Peak L(C, h) and C(L, h) against sRGB/P3/Rec.2020 |

## Already documented (markdown only — TS pending)

| File | Markdown | TypeScript |
|---|---|---|
| `../color-space-facts/references/techniques/brucelindbloom-color-math.md` | 🟡 | (superseded by `src/spaces/srgb.ts` etc.) |
| `../color-space-facts/references/techniques/iq-cosine-palette-formula.md` | 🟡 | 🔲 `src/interpolation/iq-cosine.ts` |
| `../color-material-facts/references/contemporary/iridescent-color-math.md` | 🟡 | 🔲 `src/spectral/thin-film.ts` |
| `../color-space-facts/references/techniques/oklch-gamut-peak-math.md` | ✅ | ✅ `src/gamut/oklch-peak.ts` |

## Already documented

| File | Markdown | TypeScript |
|---|---|---|
| `../color-space-facts/references/techniques/brucelindbloom-color-math.md` | 🟡 | 🔲 `src/spaces/{srgb,p3,rec2020,adobe-rgb,prophoto}.ts`, `src/adaptation/bradford.ts` |
| `../color-space-facts/references/techniques/iq-cosine-palette-formula.md` | 🟡 | 🔲 `src/interpolation/iq-cosine.ts` |
| `../color-material-facts/references/contemporary/iridescent-color-math.md` | 🟡 | 🔲 `src/spectral/thin-film.ts` |
| `../color-space-facts/references/techniques/oklch-gamut-peak-math.md` | ✅ | ✅ `src/gamut/oklch-peak.ts` |
| `../color-space-facts/references/techniques/oklab-xyz-math.md` | 🔲 | ✅ `src/spaces/oklab.ts` (markdown still to write) |

---

## Tier 1 — Foundational transforms (highest leverage, daily use)

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/gamma-transfer-functions.md` | sRGB segmented transfer, P3 transfer (= sRGB), Rec.709/2020 OETF, PQ (BT.2100), HLG (BT.2100). Linear ↔ encoded round-trip. Paired with `src/transfer/{srgb,rec2020,pq,hlg}.ts`. |
| ✅ `../color-space-facts/references/techniques/xyz-rgb-conversion-matrices.md` | XYZ↔sRGB / Display P3 / Rec.2020 / Rec.709 at D65 with W3C high-precision values. Paired with `src/spaces/{srgb,p3,rec2020}.ts`. |
| ✅ `../color-space-facts/references/techniques/cielab-xyz-conversion.md` | Lab/LCh ↔ XYZ with the cube-root nonlinearity, D65 (D50 future), hue from atan2. Paired with `src/spaces/{cielab,cielch}.ts`. |
| ✅ `../color-contrast-facts/references/techniques/relative-luminance-derivation.md` | Y from linear RGB per gamut, the WCAG L formula, gamma-encoded vs linear inputs. Paired with `src/metrics/luminance.ts`. |
| ✅ `../color-space-facts/references/techniques/cylindrical-rgb-conversions.md` | HSL/HSV ↔ RGB exact formulas, hue-sector math, why these aren't perceptual. Paired with `src/spaces/{hsl,hsv}.ts`. |
| ✅ `../color-space-facts/references/techniques/oklab-xyz-math.md` | Ottosson's perceptual space; $M_1$/$M_2$ matrices, cube-root, polar OKLCH. Paired with `src/spaces/{oklab,oklch}.ts`. |

## Tier 2 — Comparison & measurement

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/delta-e-formulas.md` | ΔE76, ΔE94, ΔE2000 (CIEDE2000 with rotations), ΔE_ok, HyAB. When each is correct. Paired with `src/metrics/deltaE.ts`; Sharma 2005 test pairs verified. |
| 🟡 `wcag-contrast-ratio-math.md` (planned → accessibility) | Already covered in `relative-luminance-derivation.md`; standalone file deferred. |
| ✅ `../color-contrast-facts/references/techniques/apca-lc-formula.md` | The actual Lc formula (polarity-sensitive), BoW/WoB branches, Bronze Simple Mode readability tiers. Paired with `src/metrics/apca.ts`. |
| ✅ `../color-space-facts/references/techniques/chromatic-adaptation-matrices.md` | Bradford, CAT16 — matrix forms, generic adaptation procedure, why diagonal scaling works. Paired with `src/adaptation/bradford.ts`. CAT02 / VonKries still pending. |

## Tier 3 — Gamut operations

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/css-color-4-gamut-mapping.md` | Binary search reducing OKLCh chroma with ΔE_ok ≤ JND clamp. Paired with `src/gamut/mapping.ts`. |
| ✅ `../color-space-facts/references/techniques/ottosson-cusp-algorithm.md` | Closed-form max-chroma cusp per hue (sRGB). Paired with `src/gamut/cusp.ts`. |
| 🔲 `../color-material-facts/references/techniques/pointers-gamut-math.md` | Real-surface gamut boundary as a function of (Y, hue). |
| 🟡 `gamut-clipping-vs-mapping.md` (consolidated, no separate file) | Consolidated into `css-color-4-gamut-mapping.md` "Comparison: clipping vs. mapping" section. |

## Tier 4 — Generation & interpolation

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/gradient-interpolation-math.md` | Linear interp across color spaces, gamma-compounding "muddy gradient" problem, CSS color-mix semantics. Paired with `src/interpolation/linear.ts`. |
| 🟡 `hue-interpolation-paths.md` (consolidated, no separate file) | CSS Color 4 hue paths consolidated into `gradient-interpolation-math.md`. |
| ✅ `../color-space-facts/references/techniques/cubehelix-formula.md` | D. A. Green's perceptual-brightness ramp. Paired with `src/interpolation/cubehelix.ts`. |
| 🔲 `../color-space-facts/references/techniques/spline-interpolation-color.md` | Catmull-Rom and Bezier in OKLab; monotone cubic. Deferred. |
| ✅ `../color-space-facts/references/techniques/lightness-ramp-curves.md` | Linear / gamma / smoothstep + Tailwind v4 + Radix step math. Paired with `src/interpolation/lightness-curves.ts`. |
| 🟡 `color-mix-algorithm.md` (consolidated, no separate file) | Consolidated into `gradient-interpolation-math.md` (mixVia helper). |

## Tier 5 — Appearance models

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/ciecam16-forward-inverse.md` | Full CIECAM16 math: viewing conditions, CAT16, cone response, opponent signals, JMh output. Paired with `src/spaces/ciecam16.ts`. |
| ✅ `../color-space-facts/references/techniques/cam16-ucs-math.md` | Jab UCS coordinates with Li 2017 constants; ΔE_CAM16. Paired with `src/spaces/cam16-ucs.ts`. |
| ✅ `../color-space-facts/references/techniques/material-hct-math.md` | CAM16 H + CAM16 C + CIELAB L* hybrid; iterative inverse; +40/+50 tone-delta guarantee. Paired with `src/spaces/hct.ts`. |
| 🔲 `../color-space-facts/references/techniques/hsluv-hpluv-math.md` | CIELUV normalized saturation; chroma-per-(hue,lightness) lookup. |
| 🔲 `../color-space-facts/references/techniques/jzazbz-ictcp-math.md` | HDR uniform spaces. Jzazbz forward/inverse; ICtCp constant-luminance encoding. |

## Tier 6 — Color vision deficiency simulation

| File | Content |
|---|---|
| ✅ `../color-contrast-facts/references/techniques/cvd-simulation-algorithms.md` | Consolidated doc covering Brettel 1997, Viénot 1999, and Machado 2009 (severity-parameterized). Paired with `src/cvd/machado-2009.ts`. Brettel and Viénot covered as math reference; only Machado has TS implementation. |
| 🔲 Separate Brettel TS module (`src/cvd/brettel-1997.ts`) | LMS confusion-line projection. Math documented; TS deferred (Machado covers ~95% of use cases). |
| 🔲 Separate Viénot TS module (`src/cvd/vienot-1999.ts`) | Matrix-based simplified version. Math documented; TS deferred (Machado supersedes). |

## Tier 7 — Pigment & spectral

| File | Content |
|---|---|
| ⚙️ `../color-material-facts/references/techniques/kubelka-munk-single-constant.md` | The K/S function; mixing in K/S space; R → K/S → R round-trip. Math companion to existing `spectraljs-pigment-mixing.md`. |
| 🔲 `kubelka-munk-two-constant.md` (planned → materials) | Separate K and S coefficients for opaque paints. |
| 🔲 `saunderson-correction.md` (planned → materials) | Air-paint surface reflection correction applied to K-M. |
| 🔲 `../color-space-facts/references/techniques/spectral-to-xyz-integration.md` | CIE 1931 (2°) and 1964 (10°) color matching functions; integration against an illuminant SPD. |
| 🔲 `metamer-construction.md` (planned → perception) | How to construct spectra that produce identical XYZ values; metamerism math. |

## Tier 8 — Image processing

| File | Content |
|---|---|
| 🔲 `../color-space-facts/references/techniques/color-quantization-math.md` | k-means in Lab/OKLab, octree, median-cut, Wu's algorithm. |
| 🔲 `../color-space-facts/references/techniques/dithering-algorithms.md` | Floyd-Steinberg error diffusion, Bayer/ordered, blue noise. |
| 🔲 `image-palette-extraction.md` (planned → spaces; distinct from the existing `image-color-extraction-tools.md`) | Histogram quantization, salience-weighted clustering, perceptual palette embeddings. |

## Tier 9 — Tone mapping / HDR

| File | Content |
|---|---|
| ✅ `../color-space-facts/references/techniques/tone-mapping-operators.md` | Reinhard (simple/extended/luminance-preserving), ACES filmic Narkowicz fit, Uncharted 2 reference. Paired with `src/tonemap/{reinhard,aces}.ts`. |
| 🟡 `pq-hlg-transfer-functions.md` (consolidated, no separate file) | Consolidated into `gamma-transfer-functions.md`. TS modules in `src/transfer/{pq,hlg}.ts`. |
| 🔲 `sdr-hdr-conversion-math.md` (planned → spaces) | Inverse tone mapping, gamut expansion sRGB → Rec.2020, BT.2390 conversion. |

## Tier 10 — Specialized / niche

| File | Content |
|---|---|
| 🔲 `../color-perception-facts/references/techniques/macadam-ellipses-math.md` | The JND ellipses on the 1931 chromaticity diagram — coordinate forms and modern OKLab analogue. |
| 🔲 `spectral-upsampling.md` (planned → spaces) | Meng et al. RGB → spectrum; Smits method. |
| 🔲 `retinex-algorithms.md` (planned → perception) | Single-Scale, Multi-Scale Retinex; the math behind color constancy algorithms. |
| 🔲 `../color-space-facts/references/techniques/white-point-conversion.md` | D65↔D50↔A↔E with Bradford; when each conversion is needed in real pipelines. |

---

## Totals

- ✅ **4** math references documented (including `oklch-gamut-peak-math.md`, added 2026-05-15)
- 🔲 **34** new math references planned
- ⚙️ **7** topics partially covered as tooling, with math extractable into a dedicated file

**41 total** planned math references across 10 tiers.

---

## Authoring conventions

**The canonical pair is `../color-space-facts/references/techniques/oklch-gamut-peak-math.md` +
`src/gamut/oklch-peak.ts`.** Every new math reference follows this pattern.

### What goes in markdown (`<owning-pack>/references/techniques/<name>.md`)

1. **TL;DR** — the key result and the misconception it corrects (if any).
2. **Natural-language description** — what the space/algorithm is, when to use it,
   edge cases, intuition.
3. **Formulas** — proper LaTeX. Display math `$$...$$`, inline `$...$`. Full matrices
   written out, not referenced.
4. **Implementation** — link to the canonical TS module
   (`../../../color-science-project-files/src/...`). Inline critical functions as
   fenced TS code blocks for in-context reading.
5. **Edge cases** — numerical precision, hue wrapping, sign-preserving cube roots,
   out-of-gamut handling.
6. **Production-library map** — Culori, @texel/color, Color.js, plus this skill.
7. **Primary sources** — every factual claim traces to one.

### What goes in TypeScript (`src/<category>/<name>.ts`, this repo)

1. **Branded-typed input and output** — never raw `number[]`.
2. **Forward and inverse functions** for any transform (`toXYZ` + `fromXYZ` for
   spaces; `encode` + `decode` for transfer functions).
3. **Full matrices as `Matrix3x3` constants** with primary-source attribution in
   comments.
4. **`testVectors` array** of input/output pairs from primary sources, with
   tolerance and `source` field per vector.
5. **Header comment** that points back to the markdown reference file (in its
   owning pack) and cites the primary source.
6. **No automatic gamut clipping** — return raw numbers; clipping is a separate
   concern.

### Checklist for a complete new file

- [ ] `<owning-pack>/references/techniques/<name>.md` written
- [ ] `src/<category>/<name>.ts` written (this repo)
- [ ] Forward and inverse exported with branded types
- [ ] `testVectors` exported with citations
- [ ] Markdown's "Implementation" section links to the TS file
  (`../../../color-science-project-files/src/...`)
- [ ] Markdown inlines key functions
- [ ] Owning pack's `references/INDEX.md` table updated
- [ ] `CHANGELOG.md` entry written: this repo's `CHANGELOG.md` for the TS change,
  the owning pack's `CHANGELOG.md` for the reference change
- [ ] This roadmap's (`MATH-ROADMAP.md`, this repo root) status flag updated (🔲 → 🟡 → ✅)

---

## Wave plan (suggested)

**Wave 0 (DONE 2026-05-15):** Foundation — `ARCHITECTURE.md`, `src/types.ts`,
`src/convert.ts`, `src/test/roundtrip.ts`.

**Wave 1 (DONE 2026-05-15):** Core spaces — `xyz`, `srgb`, `p3`, `rec2020`, `oklab`,
`oklch`, `cielab`, `cielch`, `hsl`, `hsv`, `xyy`. Transfer functions — `srgb`,
`rec2020`, `pq`, `hlg`. Metrics — `luminance`. Gamut — `oklch-peak`.

**Wave 2 (DONE 2026-05-15):** Perceptual + appearance — `okhsl`, `ciecam16`, `hct`.
🟡 → ✅ promoted (2026-05-15): CIECAM16 black-point fix (drop +0.1 offset per
Material convention); HCT white-point residual chroma documented as a property of
partial adaptation (`discountingIlluminant: false`). All 81 round-trip tests pass.

**Wave 3 (DONE 2026-05-15):** Tier 1 markdown companions — `gamma-transfer-functions.md`,
`xyz-rgb-conversion-matrices.md`, `cielab-xyz-conversion.md`, `relative-luminance-derivation.md`,
`cylindrical-rgb-conversions.md`, `oklab-xyz-math.md`. Each paired with its canonical TS
module, citing the production-library map and primary sources.

**Wave 4 (DONE 2026-05-15):** Tier 2 metrics + chromatic adaptation. New TS:
`src/metrics/deltaE.ts` (5 ΔE variants), `src/metrics/apca.ts` (L^c formula),
`src/adaptation/bradford.ts` (CAT). New test runner `src/test/metrics.ts` (13/13 passing).
New markdown: `delta-e-formulas.md`, `apca-lc-formula.md`, `chromatic-adaptation-matrices.md`.
All Tier 2 markdown ✅ except `wcag-contrast-ratio-math.md` (consolidated into
`relative-luminance-derivation.md`).

**Wave 5 (DONE 2026-05-15):** Tier 3 gamut operations. New TS: `src/gamut/cusp.ts`
(Ottosson cusp, sRGB), `src/gamut/mapping.ts` (CSS Color 4 binary search + naive clip).
Refactored `src/gamut/oklch-peak.ts` to export `inGamut` helper. Metrics runner extended
(20/20 passing). New markdown: `css-color-4-gamut-mapping.md`, `ottosson-cusp-algorithm.md`.
`gamut-clipping-vs-mapping.md` folded into the CSS Color 4 doc. `pointers-gamut-math.md`
still pending.

**Wave 6 (DONE 2026-05-15):** Tier 4 generation & interpolation. New TS:
`src/interpolation/linear.ts` (lerp + 4 CSS hue paths + mixVia), `src/interpolation/cubehelix.ts`
(D. A. Green's algorithm), `src/interpolation/lightness-curves.ts` (linear/gamma/smoothstep +
published Tailwind v4 and Radix Themes 3 L stops). Metrics runner now covers 8 modules
(44/44 passing). New markdown: `gradient-interpolation-math.md` (folds in `hue-interpolation-paths.md`
+ `color-mix-algorithm.md`), `cubehelix-formula.md`, `lightness-ramp-curves.md`.
`spline-interpolation-color.md` still pending.

**Wave 7 (DONE 2026-05-15):** Tier 5 appearance models — markdown harvesting.
New TS: `src/spaces/cam16-ucs.ts` (CAM16 J,M,h → J',a',b' uniform space + ΔE_CAM16).
roundtrip runner extended (84/84 passing across 15 space modules). New markdown:
`ciecam16-forward-inverse.md`, `material-hct-math.md`, `cam16-ucs-math.md` — full
math docs for the CAM16 family. HSLuv/HPLuv and Jzazbz/ICtCp markdown still pending.

**Wave 8 (DONE 2026-05-16):** Tier 6 CVD simulation. New TS: `src/cvd/machado-2009.ts`
(severity-parameterized; matches Chrome DevTools convention). Metrics runner now covers
9 modules (50/50 passing). New markdown: `cvd-simulation-algorithms.md` — consolidated
doc covering Brettel 1997, Viénot 1999, and Machado 2009 with full matrices + pipeline
guidance (encoded → linear → CVD → encoded). Brettel and Viénot TS modules deferred
(Machado supersedes both for typical accessibility-review use).

**Wave 9 (DONE 2026-05-16):** Tier 9 HDR tone mapping. New TS:
`src/tonemap/reinhard.ts` (simple, extended, luminance-preserving variants),
`src/tonemap/aces.ts` (Narkowicz fit). Metrics runner now covers 11 modules
(60/60 passing). New markdown: `tone-mapping-operators.md` — Reinhard + ACES +
Uncharted 2 with the full HDR scene-linear → display-encoded pipeline.
SDR-HDR conversion math still pending.

If executing the math docs as a batch effort, suggested wave order to maximize
early payoff:

**Wave 1 — Tier 1 foundations (5 files):** these unblock everything else. Without
gamma transfer functions and XYZ↔RGB matrices documented, every other math file ends
up repeating itself.

**Wave 2 — Tier 2 comparison (4 files):** ΔE and contrast math are the most-requested
formulas. High value, well-defined scope per file.

**Wave 3 — Tier 3 gamut + Tier 4 interpolation (10 files):** CSS Color 4 algorithms
and gradient math. Practical for daily design-system work.

**Wave 4 — Tier 5 appearance models (5 files):** CIECAM16 and Material HCT. Higher
complexity, less daily use, but important for principled color decisions.

**Wave 5 — Tier 6–7 CVD + spectral (8 files):** specialized but well-bounded.

**Wave 6 — Tier 8–10 (12 files):** image processing, HDR, niche — fill in as needed.

Estimated effort per file: 1–3 hours including primary-source verification. Tier 1–2
files (9 total) ≈ 1–2 days of focused work.
