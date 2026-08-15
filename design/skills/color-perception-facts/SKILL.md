---
name: color-perception-facts
description: >-
  Answers vision and color-appearance science — what the eye and brain do with light.
  Use for chroma vs saturation, lightness vs brightness, why two colors of equal
  saturation aren't equally vivid; cones, opponent process, afterimages, simultaneous
  contrast; metamerism — swatches matching under one light but not another; appearance
  models (Fairchild, CIECAM02); MacAdam ellipses; warm/cool as a perceptual axis,
  tetrachromacy, OLO. NOT space-conversion math or CSS (color-space-facts); NOT contrast
  or CVD checks (color-contrast-facts); NOT pigment, print, or naming
  (physical-color-facts); NOT harmony or meaning (color-theory-facts). ANSWERS, does not
  generate.
disable-model-invocation: false
user-invocable: false
---

# color-perception-facts — what the eye and brain do

The vision-science layer of color: terminology, mechanism, and appearance — what is perceptually
true, independent of any particular color space's math. Extracted 2026-07-06 from the `color-science`
pack (split into four: `color-space-facts`, `color-perception-facts`,
`color-contrast-facts`, `physical-color-facts`); `references/INDEX.md` is the canonical
manifest and owns the file count (49 at this writing).

| Ask | Load |
|---|---|
| Terminology & dimensions — chroma vs saturation, lightness vs brightness | INDEX §Terminology & Dimensions |
| Vision mechanics — cones, opponent process, afterimages, metamerism, tetrachromacy, JPEG subsampling | INDEX §Vision Mechanics |
| Appearance science — Fairchild, CIECAM02, viewing conditions, MacAdam/JND, Koenderink, warm-cool | INDEX §Appearance Science |
| Textbook layer — Briggs lectures, color philosophy/education, the huevaluechroma + colorandcontrast whole scrapes | INDEX §Textbook Layer |
| Provenance — where a claim comes from | `references/INDEX.md` (one row per file, with source links) |

## Load discipline (read this before opening a scrape chapter)

The two textbook scrapes are large, and three chapters exceed 1000 lines:
`contemporary/huevaluechroma/ch11-afterthoughts.md` (~3050 lines), `ch01-dimensions-of-colour.md`
(~1611 lines), `ch07-hue.md` (~1006 lines). **Never Read a chapter start-to-finish for a
single-term ask.** Grep the chapter (or `glossary.md`) for the term first, then Read with an offset
around the match. This corpus is a catalog to consult, not a book to read linearly.

## Consult procedure

1. Classify the ask against the four axes above. Open `references/INDEX.md`, Grep the axis section
   for the term, then Read only the matching file (with offset for the long transcripts).
2. Answer with the **claim and its cited file** — every claim traces to a reference file; an answer
   the corpus cannot back is general knowledge and must be flagged as such. Worked shape:
   > *"My teammate says two colors are equally vivid because they're both HSL saturation 100%."* →
   > terminology ask → `references/contemporary/chroma-vs-saturation.md`: saturation is the angle
   > from white in a color's own lightness plane, not distance from the neutral axis — two hues at
   > HSL S=100% can have very different perceived vividness (chroma) because HSL's cylinder is not
   > perceptually uniform. **The trap:** HSL's S is a geometric artifact of the RGB cube, not a
   > vision-science quantity — citing "100% saturation" as a vividness guarantee is exactly the
   > confusion `contemporary/chroma-vs-saturation.md` exists to correct. The underlying non-uniform
   > geometry is `color-space-facts`'s to explain (HSL-is-geometry-not-perception); this pack
   > answers only what the terms *mean* perceptually.
3. Check the boundary before answering: if the ask turned into space-conversion math, gamut, or CSS
   syntax, it was `color-space-facts`'s; if it turned into a contrast ratio or CVD check, it was
   `color-contrast-facts`'s.
4. Route output work at the boundary: never produce a palette, ramp, or token sheet here — hand
   making to `make-palette` and end-to-end proof to `check-colors`.

## Standing distinctions (each traces to its file)

- **Chroma ≠ saturation** — chroma is distance from the neutral axis; saturation is the angle from
  white in a color's own lightness plane (`contemporary/chroma-vs-saturation.md`). Never use one
  term to explain the other.
- **Lightness ≠ brightness** — lightness is contextual (relative to the illuminant); brightness is
  an absolute percept (`contemporary/lightness-vs-brightness.md`).
- **Warm/cool is a phenomenological axis, not a hue rotation** — green and purple sit on the
  warm/cool boundary; spectral reflectance alone does not decide it
  (`contemporary/koenderink-warm-cool-chromatic-gestalt.md`, `contemporary/green-warm-or-cool-spectral.md`).

## Straddle rule with color-theory-facts

`color-theory-facts` documents harmony, meaning, and the history of the wheel; three files in this pack
carry the *perceptual mechanism* under one of its aesthetic claims and are cited (never duplicated)
from its INDEX: `historical/albers-interaction-of-color.md` (simultaneous contrast — the mechanism
behind "these colors vibrate side by side"), `contemporary/koenderink-warm-cool-chromatic-gestalt.md`
and `contemporary/green-warm-or-cool-spectral.md` (warm/cool as phenomenology, not hue rotation — the
empirical basis under "warm palette" talk). If an aesthetic-judgment question arrives here citing one
of these files, answer the mechanism and route the judgment itself to `color-theory-facts`.

## Boundaries

- **This skill answers; it does not generate.** No ramps, no palettes, no token sheets — name the
  vision-science claim and its evidence; hand making to `make-palette` and proof to `check-colors`.
- **Space-conversion math, gamut, gradients, and CSS color syntax belong to `color-space-facts`**
  — including the HSL/HSV-is-geometry-not-perception distinction (this pack explains *why* geometry
  isn't perception; spaces explains the geometry itself).
- **Contrast standards and color-vision-deficiency checks belong to `color-contrast-facts`**
  — APCA/WCAG, CVD simulation, and CVD-safe pairs (including `opponent-process-color-blindness.md`,
  one of the family's five straddle files, which lives there because its load-bearing claim is CVD
  pairs, not pure vision science).
- **Pigment, print, and color naming belong to `physical-color-facts`** — including the
  huevaluechroma subtractive-mixing chapters (ch05, ch06), which materials cross-cites from this
  pack rather than duplicating.
- **Harmony, the color wheel, and meaning belong to `color-theory-facts`** — see Straddle rule, above.

## Extending this pack

A missing axis, a stale reference, or "add X to this pack" is authoring work — route to
[[make-pack]] (axis decomposition, grounded research waves, index discipline); never bolt an
uncited file onto the corpus inline.
