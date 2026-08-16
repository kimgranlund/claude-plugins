---
name: color-space-facts
description: >-
  Answers computational-color questions — spaces and math. Use for converting or comparing color
  spaces (OKLCH, OKLab, sRGB, HSL, CIELAB, CAM16/HCT, XYZ), gamut mapping + peak chroma,
  perceptually even gradients/ramps, ΔE color difference, white points, HDR tone mapping, CSS
  color syntax (color-mix, relative color, light-dark), extracting a palette from an image,
  quantization, picking a library. NOT for contrast/CVD/legibility (color-contrast-facts); NOT for vision
  mechanics (color-perception-facts); NOT for harmony/meaning (color-theory-facts); NOT for a
  color ramp or semantic tokens (make-palette; token-builder). ANSWERS, does not generate.
disable-model-invocation: false
user-invocable: false
---

# color-space-facts — the spaces and the math

The computational layer of color: spaces and conversions, gamut and interpolation, HDR/tone mapping,
CSS color syntax, image palettes and quantization, and the palette-generation/library catalog. Its
siblings answer adjacent questions about the *same* colors: [[color-perception-facts]] answers why
vision works that way, [[color-contrast-facts]] answers contrast standards and CVD,
[[physical-color-facts]] answers pigment/print/naming. Extracted 2026-07-06 from the monolithic
`color-science` pack; `references/INDEX.md` is the canonical manifest and owns the file count (72 at
this writing).

## Consult index — 6 axes

| Axis | Ask | Load |
|---|---|---|
| 1. Spaces & conversions | OKLab/OKLCH, CIELAB, CAM16/HCT, HSL/HSV limits, white points, adaptation, CIE 1931 | INDEX §Contemporary + §Techniques → Libraries & Code |
| 2. Gamut & interpolation | peak chroma, cusp, CSS gamut mapping, gradients, hue paths, ramps, splines, cubehelix, ΔE | INDEX §Techniques → Libraries & Code |
| 3. HDR & tone mapping | PQ/HLG, Jzazbz/ICtCp, Reinhard/ACES | INDEX §Techniques → Libraries & Code |
| 4. CSS color syntax & status | color-mix, relative color, light-dark, Baseline snapshot | INDEX §Techniques (Libraries & Code + Practical Methods) |
| 5. Image palettes & quantization | k-means, dithering, extraction tools, sorting | INDEX §Contemporary + §Techniques |
| 6. Palette-generation & library/tool catalog | IQ cosine, generative-artist techniques, Culori/Color.js, Tailwind/Radix | INDEX §Practical Methods + §Library & Tool Catalog |
| — | Provenance — where a claim comes from | `references/INDEX.md` (one row per file, with source links) |

## Load discipline

Grep the axis term in `references/INDEX.md` first, then Read only the matching row's file — several
techniques files run 150–300 lines of derivation; Read with `offset` for a specific section rather
than the whole file. The corpus is a catalog, not a linear read.

## Consult procedure

1. Classify the ask against the 6 axes above (an ask can span two — gamut mapping cites both axis 1
   and axis 2 files).
2. Answer with the **claim, its cited file, and the trap** — a bare formula without the failure mode
   it prevents is incomplete. Worked shape:
   > *"I'm building a CSS theme generator and want gradients that don't go muddy halfway through —
   > should I use OKLCH, Lab, or color-mix somehow?"* → gamut & interpolation ask →
   > `references/techniques/gradient-interpolation-math.md`: the muddy midpoint is gamma-compounding
   > — interpolating in encoded (gamma-companded) sRGB, or in raw HSL, dips perceived
   > lightness/chroma at the midpoint and reads as gray; interpolate in a perceptually uniform space
   > (OKLab/OKLCH) or let CSS `color-mix(in oklab, ...)` do it natively. **The trap**: switching to
   > HSL "because it has a hue channel" does not fix this — HSL is a geometric reparameterization of
   > encoded sRGB (see below), not a perceptually uniform space, so the muddy dip survives the switch.
3. Check the source-tracing rule before answering: every claim traces to a reference file; an answer
   the corpus cannot back is general knowledge and must be flagged as such.

## Standing distinctions & defaults

- **HSL/HSV are geometry, not perception** — cylindrical reparameterizations of encoded sRGB. Hue
  sectors are piecewise-linear; saturation and lightness don't track perceived colorfulness or
  lightness. Never present HSL as a fix for a perceptual problem (gradients, ramps, contrast) —
  route the fix to OKLab/OKLCH instead (`techniques/cylindrical-rgb-conversions.md`).
- **OKLCH/OKLab is the default for perceptual work, with rationale, not by reflex** — gradients,
  ramps, and gamut mapping default to OKLab/OKLCH because it outperforms CIELAB on combined
  lightness+chroma+hue predictions (`contemporary/bjorn-ottosson-oklab-articles.md`); CIELAB/CIELCH
  remain the right call when a spec or legacy pipeline requires ΔE76/94/2000 specifically
  (`techniques/cielab-xyz-conversion.md`, `techniques/delta-e-formulas.md`). State the rationale, not
  just the recommendation.

## Demo & implementation pointer

"Show me a live demo" / "where's the implementation" is owned here: the paired TypeScript library
(24 color spaces, gamut math, ΔE metrics, tone mapping, quantization, dithering) lives at
[`color-science-project-files/src/`](../../color-science-project-files/src/); live demo pages at
[`color-science-project-files/examples/pages/`](../../color-science-project-files/examples/pages/),
built into one IIFE bundle so every page works directly over `file://` — no server needed. If the
bundle is stale, `cd color-science-project-files/examples && ./build.sh` before opening a page. Each
techniques file's own "Implementation" section names its paired module.
**Mechanism-demo straddle note:** a few demo pages carry aesthetic-sounding names (a warm/cool
demo, a harmony-wheel demo) — these are *mechanism* demos, showing the math/pipeline behind the
effect. The aesthetic judgment ("does this look right, is this harmonious") is
[[color-theory-facts]]'s; this pack only demos the computation.

## Boundaries — this skill answers; it does not generate

- Contrast standards, WCAG/APCA, CVD simulation, low-vision color choices →
  [[color-contrast-facts]].
- Why vision works that way (cones, opponent process, appearance models, MacAdam/JND) →
  [[color-perception-facts]].
- Pigment mixing, print/ICC, color naming standards → [[physical-color-facts]].
- Harmony, the color wheel, meaning/mood → [[color-theory-facts]].
- Building a ramp, theme, or semantic token mapping → `make-palette` (design work) or the
  `token-builder` agent (realizing token layers in a repo) — never build one inline here, even
  though axis 6 documents the generation *methods*.
- Verifying a candidate palette end-to-end (ColorProof, pass/fail) → [[check-colors]].

## Extending this pack

Extension: governed by [[make-pack]]
