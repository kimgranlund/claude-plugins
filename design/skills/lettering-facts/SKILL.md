---
name: lettering-facts
description: >-
  Use for typography/lettering questions — comparing, explaining, classifying, specifying type:
  "my headings jump when the webfont swaps in", "does OpenDyslexic actually help", "why does
  this font look boring/generic", "why does text-wrap: balance not work in my browser", CSS
  `text-wrap: balance`/`pretty` support — covers type anatomy, classification (Vox-ATypI,
  humanist/geometric/grotesque), metric-compatible fallback stacks, font personality, world
  scripts, OpenType features, variable-font axes, text accessibility. NOT a brand's font pairing
  (pick-fonts); NOT generating a type scale/tokens (font-token-rules); NOT building components
  (make-component). ANSWERS, does not generate.
disable-model-invocation: false
user-invocable: false
---

# lettering-facts — the cited type corpus

Answers typography and lettering questions from a dated, cited reference corpus: 63 markdown
files under `references/` (62 references across ten axes plus the `references/INDEX.md`
manifest, ~30k lines). "Lettering" rides the stem because the corpus covers letterform
construction itself — anatomy, classification, per-script letterforms — not just typesetting;
no separate lettering-practice (sign-painting, calligraphy) axis is claimed. It answers and
explains; it does not generate scales, tokens, or components. One typed index, one consult
discipline:

| Ask | Load |
|---|---|
| Craft technique — measure/CPL, pairing, modular scale, vertical rhythm, fallback stacks, figures, small caps, optical size, hanging punctuation | `references/techniques/` (9 files) |
| Typeface voice — why a face reads neutral/generic vs distinctive/impactful, when each is the right choice, contrast intensity in pairing | `references/voice/` (2 files) |
| Web platform — CSS text properties, variable fonts, OpenType features, font delivery, metric overrides, color fonts, font-palette, hinting/rendering, Custom Highlights API, Interop 2026 | `references/contemporary/` (10 files) |
| Reading science — legibility vs readability, crowding, word-shape vs parallel-letter recognition, optical-size research | `references/science/` (4 files) |
| Script norms — any non-generic-Latin ask routes to its per-script metrics file: arabic, cjk-han, japanese, hangul, devanagari, thai, hebrew, cyrillic, greek, ethiopic, latin | `references/scripts/<script>.md` (11 files) |
| Text accessibility — dyslexia, low vision, cognitive load, WCAG type criteria | `references/accessibility/` (4 files) |
| Classifying a typeface — Vox-ATypI, Bringhurst, DIN 16518, Thibaudeau (name the system when systems disagree) | `references/classification/` (4 files) |
| Era / lineage — blackletter through the variable era, one file per era | `references/historical/` (12 files) |
| Metrics + anatomy — UPM, x-height, overshoot, sidebearings, units (ch/cap/ic), metric compatibility | `references/metrics/` (4 files) |
| Designer / foundry lookup | `references/foundries/` (2 files) |
| Full manifest, coverage tiers, per-file purpose | `references/INDEX.md` |

## Consult procedure

1. Classify the ask to one axis and load only that axis. The corpus is not a linear read —
   files run up to ~900 lines. Grep the axis directory for the term first, then Read the matching
   file with offset/limit at the hit; never load a whole file into context.
2. Answer as **claim + cited file + the file's date header**. Every reference opens with a
   date and coverage tier; for volatile claims (browser support, CSS specs, variable-font
   registry) check that date against the question and quote it — if it is stale, say so
   rather than citing blindly.
3. Worked shape:
   > *"My headings jump when the webfont swaps in — how do I stop the layout shift?"* →
   > technique ask → Grep `references/techniques/fallback-stacks.md` for `size-adjust` →
   > answer: compute `size-adjust = primary x-height ÷ fallback x-height` (Capsize method),
   > add `ascent-override` / `descent-override` / `line-gap-override` on the fallback
   > `@font-face`, and set `font-size-adjust` as the per-element safety net — cited to
   > `references/techniques/fallback-stacks.md` with `references/contemporary/metric-overrides.md`
   > for the override algorithm, dates quoted.

Pinned routes (the asks that recur): layout shift on font swap / metric-compatible stacks →
`references/techniques/fallback-stacks.md` then `references/contemporary/metric-overrides.md`;
measure and characters-per-line → `references/techniques/measure.md`; Arabic contextual forms,
CJK line-breaking, Devanagari conjuncts → the matching `references/scripts/` file, always.

## Honesty rule

Distinguish corpus-backed answers from general-knowledge answers, and say which is which.
Coverage is declared, not assumed — `references/INDEX.md` carries a tier per file (Latin deep;
most scripts medium; Hangul light; Ethiopic a stub). When the corpus is lighter than the
question warrants, say so and point at the authoritative external source instead of
extrapolating; when answering beyond the corpus entirely, flag the answer as uncited.

The same doctrine governs the corpus's numbers and its taxonomies: numeric norms are defaults
with rationales, not laws — CPL 45–75 and the line-height floors exist to prevent named failure
modes (fatigue, crowding, mark clipping), so judge a deviation against the failure mode it
risks, not against the number; and where classification systems disagree, name the system —
the contested-knowledge form of the same rule.

## Boundaries

- **This skill answers; it does not generate.** No token sheets, no scale output, no CSS
  deliverables — the answer is a claim with a citation.
- **Type scale / tokens** — realizing a type choice (voice × step, the concrete font per family
  slot, the size/leading/tracking ladder) is token work → route to [[font-token-rules]]. This
  file still answers the typographic question inline — which ratio, why neutral vs. distinctive,
  what a script needs — from `references/techniques/modular-scale.md` and `references/voice/`;
  font-token-rules owns turning that answer into bound `--type-*` tokens.
- **Building components** → [[make-component]].
- **Locale formatting, bidi, Intl, pluralization** → [[check-translations]] — script *metrics and
  typographic norms* stay here.
- **Color pairing and contrast math** → [[color-contrast-facts]].
- **Measure, legibility, and readability questions stay here** — answered from
  `references/techniques/measure.md` and `references/science/legibility-vs-readability.md`.

## Extending this pack

Extension: governed by [[make-pack]]
