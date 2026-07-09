---
name: color-theory
description: >-
  Answers color-theory questions — harmony, meaning, and history: whether a color choice reads as
  intended, and why. Use when asked about color harmony ("why do these colors clash", complementary
  / triadic / analogous schemes, 60-30-10 dominant/accent proportion), the color wheel and its
  history (Newton, Goethe, Itten's seven contrasts, Albers, Ostwald, RYB vs CMY), what a color
  communicates (symbolism, palette mood / feel / vibe, pale-muted-vivid character), or designers'
  colour programmes (Gerstner, Reilly). NOT for perceptual mechanisms — vision science
  (color-science-perception); NOT for color-space math, OKLCH, or gamut (color-science-spaces);
  NOT for contrast/APCA/WCAG or CVD (color-science-accessibility); NOT for pigment physics
  (color-science-materials); NOT for building a ramp, theme, or semantic mapping (palette-design);
  NOT for verifying a palette (color-verify). ANSWERS aesthetic-judgment questions; it does not
  generate palettes.
disable-model-invocation: false
user-invocable: false
---

# color-theory — what reads as intended

The judgment layer of color: harmony, meaning, and the history of the ideas designers still argue
with. Its primary sibling [[color-science-perception]] answers *what is perceptually true*
(vision science); the wider `color-science-*` family (spaces, accessibility, materials) covers
the rest of the math and standards. This pack answers *what a color choice communicates* — and its
corpus is deliberately revisionist: it documents where folk color theory is wrong and what the
evidence supports instead. Extracted 2026-07-02 from the color-science pack (since split into the
`color-science-*` family, 2026-07-06); `references/INDEX.md` is the canonical manifest and owns
the file count (28 at this writing).

| Ask | Load |
|---|---|
| Harmony & combination — "why do these clash?", schemes, dominant/accent proportion | `references/techniques/` + `references/contemporary/` — see INDEX §Harmony |
| The color wheel & its history — Newton, Goethe, Itten, Albers, Ostwald, RYB vs CMY | `references/historical/` — see INDEX §Wheel |
| Colorists' programmes & practice — Gerstner, Reilly, painters, pixel artists | INDEX §Programmes |
| Meaning, mood & expression — "what does this color communicate?", palette feel | INDEX §Meaning |
| Perceptual mechanism under an aesthetic effect — simultaneous contrast, warm/cool, opponent pairs | INDEX §Cited-from (straddle files live in the color-science-* packs) |
| Provenance — where a claim comes from | `references/INDEX.md` (one row per file, with source links) |

## Consult procedure

1. Classify the ask: harmony · wheel/history · programme · meaning. Open `references/INDEX.md`,
   Grep the axis section for the term, then Read only the matching file (with offset for long
   transcripts) — the corpus is a catalog, not a linear read.
2. Answer with the **claim, its cited file, and the correction the corpus carries** — this corpus
   exists to correct folk theory, so an answer that repeats the folk rule uncited is a failure.
   Worked shape:
   > *"Should I use complementary colors for my brand palette?"* → harmony ask →
   > `references/techniques/youre-wrong-about-color-harmony.md`: hue-interval schemes
   > (complementary/triadic) are weak predictors of mood or legibility — *character* (chroma ×
   > lightness: pale/muted/deep/vivid/dark) predicts how a palette feels;
   > `references/contemporary/schloss-palmer-color-combinations.md` adds that rated pair harmony
   > actually rises with hue *similarity*, while figural pop can rise with hue contrast. So:
   > complementary is a fine *contrast* device, not a harmony guarantee — and any legibility
   > claim exits to [[color-science-accessibility]]'s APCA/WCAG contrast math.
3. Check the source-tracing rule before answering: every claim traces to a reference file; an
   answer the corpus cannot back is general knowledge and must be flagged as such. Re-check the
   boundary — if the answer turned into contrast numbers, the ask was
   [[color-science-accessibility]]'s; if it turned into gamut or ΔE numbers, it was
   [[color-science-spaces]]'s.
4. Route output work at the boundary: build the ramp/theme/semantic mapping → [[palette-design]];
   prove a candidate palette (ColorProof, WCAG/APCA pass-fail, CVD) → [[color-verify]]; realize
   token layers in a repo → the `token-builder` agent.

## Load-bearing corrections (each traces to its file)

- **Hue-first harmony is weak; character-first works** — chroma + lightness predict emotional
  response better than hue (`techniques/youre-wrong-about-color-harmony.md`; Divers).
- **"Blue is calm" is a chroma/lightness effect misattributed to hue** (same file).
- **The RYB wheel is a 1769 error** — Moses Harris spaced RYB at equal 120°; 250 years of bad
  theory followed (`historical/moses-harris-1769-color-wheel.md`).
- **Proportion beats selection**: 60-30-10 / dominant-tonic-accent — vivid color works because it
  is rare (`techniques/florent-farges-color-harmony-painters.md`,
  `techniques/drawing-codex-color-proportion.md`).
- **Color meaning is context-dependent, not a lookup table** — concept associations shift with
  context ("quiet" vs "lively" forest) (`contemporary/gencolor-color-concept-association.md`).
- **Corrections are defaults-with-rationale, not bans** — when the folk rule remains the right
  answer for the job (complementary as a figural *contrast/pop* device,
  `contemporary/schloss-palmer-color-combinations.md`), say so and cite why it holds here;
  correcting folk theory never means reflex-contradicting it.

## Extending this pack

A missing axis, a stale reference, or "add X to this pack" is authoring work — route to
[[knowledge-forge]] (axis decomposition, grounded research waves, index discipline); never bolt
an uncited file onto the corpus inline.

## Boundaries

- **This skill answers; it does not generate.** No ramps, no palettes, no token sheets — name the
  judgment and its evidence, hand the making to [[palette-design]] and the proof to
  [[color-verify]].
- **Mechanism and math belong to the `color-science-*` family** — simultaneous contrast and
  warm/cool spectra → [[color-science-perception]]; opponent process → [[color-science-accessibility]]
  (the straddle files this pack cites); space/conversion/gamut → [[color-science-spaces]]; pigment
  → [[color-science-materials]]. Never duplicate its files; cite them.
- Cultural/brand voice beyond color (naming, tone, identity systems) is the brand corpus's
  domain, not this pack's.
