---
name: color-science-materials
description: >-
  Answers physical-color and color-naming questions — pigment, print, and the standards that
  catalog color. Use for paint mixing (Kubelka-Munk, why blue+yellow makes green while RGB
  or opacity blending makes gray/mud; Spectral.js, Mixbox), pigment history and historical paint
  datasets (manufacturer swatches, watercolours, skin tones), print-vs-screen mismatch (the print
  proof duller than the mockup or monitor), ICC profiles, rendering intents, and color
  management, iridescence and thin-film color (color that shifts with viewing angle), Pointer's
  gamut of physically real surface colors (paint, dye, ink), and color naming (ISCC-NBS,
  Munsell, Ridgway names, hex→name, naming across languages). NOT for space-conversion math or
  gradients (color-science-spaces); NOT for vision/appearance science (color-science-perception);
  NOT for contrast or CVD (color-science-accessibility); NOT for palette mood or meaning
  (color-theory); NOT for building palettes (palette-design). ANSWERS, does not generate.
disable-model-invocation: false
user-invocable: false
---

# color-science-materials — pigment, print, and the names for color

The physical-and-named layer of color: what a pigment does when it mixes with another pigment,
what happens when a color leaves the screen for paper or paint, and what a color is *called*.
Its siblings [[color-science-spaces]] (space-conversion math), [[color-science-perception]]
(vision/appearance science), and [[color-science-accessibility]] (contrast/CVD) answer the rest
of what was one `color-science` pack before the 2026-07-06 split; `references/INDEX.md` is the
canonical manifest and owns the file count.

| Ask | Load |
|---|---|
| Pigment & mixing physics — paint mixing, Kubelka-Munk, Spectral.js/Mixbox, skin tones, pigment history | `references/{historical,contemporary,techniques}/` — see INDEX §Pigment |
| Reproduction & measurement — print-vs-screen, ICC profiles, Pointer's gamut | INDEX §Reproduction |
| Naming standards & datasets — ISCC-NBS, Munsell, Ridgway, hex→name, cross-language naming | INDEX §Naming |
| Subtractive-mixing mechanism under an aesthetic effect | INDEX §Cited-from-color-science-perception (huevaluechroma ch05/ch06 — the mixing physics is cited, never duplicated) |
| Provenance — where a claim comes from | `references/INDEX.md` (one row per file, with source links) |

## Consult procedure

1. Classify the ask: pigment/mixing · reproduction/measurement · naming. Open
   `references/INDEX.md`, Grep the axis section for the term, then Read only the matching file
   (with offset for long transcripts) — the corpus is a catalog, not a linear read.
2. Answer with the **claim, its cited file, and the trap** — the corpus exists to correct the
   naive digital intuition, so an answer that reaches for RGB math uncorrected is a failure.
   Worked shape:
   > *"What model should I use so mixing blue and yellow paint feels like paint, not Photoshop
   > opacity?"* → pigment/mixing ask → `references/techniques/kubelka-munk-single-constant.md`:
   > RGB averaging of pure blue (0,0,1) and pure yellow (1,1,0) gives a medium gray (0.5,0.5,0.5)
   > — that's the trap. Real pigments mix by absorption, not by averaging: each paint absorbs its
   > own band of wavelengths, and only the wavelengths *both* paints reflect survive, which is
   > green. Kubelka-Munk linearizes this in K/S space (`K/S = (1-R)²/2R`); mixing is linear in
   > K/S, then converted back to reflectance. For production code, don't hand-roll it — Spectral.js
   > (open-source, GLSL) and Mixbox (commercial, rod-and-cone pigment model derived from K-M) are
   > the shipped routes; both are cited alongside the math file.
3. Check the source-tracing rule before answering: every claim traces to a reference file; an
   answer the corpus cannot back is general knowledge and must be flagged as such. Re-check the
   boundary — if the answer turned into space-conversion math or a gradient, the ask was
   [[color-science-spaces]]'s; if it turned into contrast numbers, [[color-science-accessibility]]'s.
4. Route output work at the boundary: build a ramp, theme, or palette from these colors →
   [[palette-design]]; judge harmony or mood → [[color-theory]]; realize token layers in a repo →
   the `token-builder` agent.

## Standing distinction: pigment mixing ≠ RGB averaging

Digital color intuition treats mixing as interpolation — average two RGB triples, get the
midpoint. Real pigments don't work that way: each pigment absorbs light at specific wavelengths,
and mixing combines absorption profiles, not colorimetric coordinates. Blue paint + yellow paint
gives green because green is what's left after *both* pigments' absorption is applied — RGB
averaging of the same two colors gives gray, the wrong answer, because it treats color as an
additive-light problem when pigment mixing is subtractive-absorption. This is why every credible
paint-mixing tool (Spectral.js, Mixbox, FocalPaint) implements Kubelka-Munk or an equivalent
spectral model instead of blending RGB or HSL — never advise RGB/HSL interpolation for a
"real paint" or "pigment" mixing ask; it produces physically implausible colors even when it
looks reasonable in isolation.

## Extending this pack

A missing axis, a stale reference, or "add X to this pack" is authoring work — route to
[[knowledge-forge]] (axis decomposition, grounded research waves, index discipline); never bolt
an uncited file onto the corpus inline.

## Boundaries

- **This skill answers; it does not generate.** No ramps, no palettes, no token sheets — name the
  physical fact and its evidence, hand the making to [[palette-design]].
- **Space-conversion math, gamut, gradients, and CSS color syntax belong to
  [[color-science-spaces]]** — this pack answers what a pigment or print process *does*, not how
  to convert or interpolate a color space.
- **Vision and appearance science belong to [[color-science-perception]]** — this pack cites its
  huevaluechroma subtractive-mixing chapters (ch05/ch06) rather than re-deriving the vision-side
  mechanism.
- **Contrast standards and color-vision deficiency belong to [[color-science-accessibility]]** —
  never answer an APCA/WCAG/CVD question from this pack.
- **Harmony, mood, and meaning belong to [[color-theory]]** — a naming or pigment-history answer
  should not drift into aesthetic judgment about whether the result "looks good."
- Verifying a candidate palette end-to-end (ColorProof) is [[color-verify]]'s job, not this
  pack's.
