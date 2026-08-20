# Font craft — per-voice judgment, metrics, and the categorized register

This file is the deepened home of the per-voice distinctive-vs-neutral judgment, the verified
metric data, and the categorized font register that used to live in
`font-token-rules/references/font-selection.md`. That file now carries only a short fallback
heuristic for when no brief exists at all; this file is where the full treatment lives once a
brand concept or creative brief is in play. Nothing here is re-derived from nothing — the
distinctiveness mechanics cite `lettering-facts/references/voice/neutral-by-design.md` and
`lettering-facts/references/voice/distinctive-and-impactful.md`; the pairing mechanics cite
`lettering-facts/references/techniques/pairing.md`. Consult those for the design-history and
research grounding; this file states only the operational judgment and the data the checker uses.

## The judgment, deepened per voice (not just per family-role slot)

`font-token-rules`' five font-family roles (`display · heading · body · ui · mono`) are the
concrete binding slots, but the fifteen voices riding on them don't all carry identical stakes:

| Voice | Family role | Distinctiveness earns its keep when… | Neutrality wins when… |
|---|---|---|---|
| `display` | display | the one big statement IS the product — marketing, editorial, portfolio | the "hero" is itself dense information, or the brand wants restraint |
| `headline` | heading | headings carry brand voice/personality (editorial, content brands) | heavy i18n, or headings must match body rhythm closely |
| `sub-heading` | heading | rides the heading face's call — rarely decided independently | rides the heading face's call |
| `title` | heading | rides the heading face's call — a smaller headline, same register | rides the heading face's call |
| `sub-title` | mono (prose) | rides the mono face's call — an alternate-typeface small heading, by design | rides the mono face's call |
| `kicker` | mono | a considered overline is part of the brand's texture (dev-tool, editorial) | the mono face is purely functional (code, tabular data) |
| `lead` | body | an editorial standfirst or pull-quote wants a touch more presence than body | matches body's neutrality call — it's still a reading voice |
| `body` | body | long-form editorial reading where a text face sets tone | dense data UI, enterprise products, heavy i18n, extended reading at small sizes (incl. its fine-print SM step) |
| `body-mono` | mono | a code-aesthetic brand (dev tools, terminal-flavored products) — code-adjacent prose, technical excerpts, docs and terminal content | rarely a concern — mono faces are already a narrow, legibility-first category |
| `label` | ui | rarely — chrome legibility usually outweighs personality | almost always: dense tables, forms, admin consoles, accessibility-first products |
| `label-mono` | mono | a considered technical/data aesthetic is part of the brand (dev tools, data products) naming machine-adjacent values — table keys, hashes, IDs at label sizes | almost always — legibility for keys/hashes/IDs outweighs personality, same call as `label` |
| `tiny` | ui (as prose) | almost never — captions are read, not felt | almost always — captions and small supporting text want to disappear |
| `tiny-mono` | mono | almost never — timestamps and fine technical data are read, not felt | almost always — same as `tiny`, at technical/data content (timestamps, fine data) |
| `ui-control` | ui (box voice) | rarely — chrome legibility outweighs personality, same call as `label` | almost always: every interactive control a user operates (buttons, inputs, selects) — the full 6-step ramp; a change here moves control geometry |
| `ui-widget` | ui (box voice) | rarely — same call as `ui-control` | almost always — compact, dense widget chrome (tags, badges, switches); one register under `ui-control` (9–14 vs. 12–20), same box (single-line) behavior |

The pattern font-token-rules' fallback heuristic already names — display/headline/kicker/body-mono
earn distinctiveness most often, body/label/tiny (and their mono siblings, and the two UI voices)
want neutrality most often — holds here too; what this table adds is that `sub-heading`, `title`,
`sub-title`, `lead`, and `tiny` don't get an independent call: they inherit their family role's
decision, and stating that inheritance explicitly (rather than silently picking a sixth font) is
itself part of the coherence pass (SKILL.md step 3). `label-mono`/`tiny-mono`/`kicker` also inherit
their non-mono sibling's font choice by the aliasing law (mono role, never a distinct size or font
story) — the source of record for these five newer voices' intended use is ultimate-tokens'
`docs/reference/typography/intended-use.md`.

## The metrics table (verified, cited — the checker's canon)

Every figure below is inherited from a corpus source that verified it; extending this table
requires a verified, cited source, never a guessed number (the grounding rule this skill's own
craft-correctness gate exists to enforce on itself). `scripts/typeface-check.py` embeds this same
table for computation — keep the two in sync when either changes.

| Font | x-height | cap-height | Family | Register | Source |
|---|---|---|---|---|---|
| Inter | 0.545 | 0.73 | sans | neutral | inherited¹ |
| Fraunces | 0.495 | 0.72 | serif | editorial | inherited¹ |
| Source Serif 4 | 0.515 | — (unverified) | serif | editorial | inherited¹ |
| IBM Plex Sans | 0.516 | 0.70 | sans | technical | inherited¹ |
| IBM Plex Serif | 0.516 | 0.70 | serif | technical | inherited¹ |
| Geist | 0.52 | — (unverified) | sans | distinctive | inherited¹ |
| JetBrains Mono | 0.555 | 0.73 | mono | code | inherited¹ |
| Roboto | 0.528 | — (unverified) | sans | neutral | `lettering-facts/references/voice/neutral-by-design.md` |
| Arial | 0.519 | — (unverified) | sans | neutral | `lettering-facts/references/voice/neutral-by-design.md` |

¹ Inherited from `font-token-rules/references/font-selection.md`'s **pre-migration revision**
(2026-07-05) — that file has since been thinned to a no-brief fallback and no longer carries these
figures; this table is their canonical home now. Cross-checked where a second corpus source exists:
Roboto (0.528) and Arial (0.519) match `lettering-facts/references/metrics/metric-compatibility.md`
exactly; Inter's 0.545 here is consistent with, but not identical to, that file's 0.546 (a
documented Inter 3.x/4.x cut difference, not a transcription error). The remaining inherited
figures (Fraunces, Source Serif 4, IBM Plex, Geist, JetBrains Mono) rest on this table alone —
re-verify against the type foundry's published metrics before a high-stakes ship.

A dash means the source didn't state that figure — the checker treats a missing cap-height as
"unmeasured" for that half of the ratio rather than inventing one; a same-baseline pairing that
needs the cap-height check and doesn't have it on both sides gets flagged as unverifiable on that
axis, not silently passed.

**Worked example** (the mechanic, not just the claim): Inter (x-height 0.545) against Fraunces
(x-height 0.495) → ratio 0.495 ÷ 0.545 = 0.908 — within the ±10% band despite the strong
classification contrast (neutral grotesque sans vs. editorial wonky serif). IBM Plex Sans against
IBM Plex Serif → ratio 1.0 exactly (metric-matched by design) — the safest metric-compatible
contrast pairing available, because classification alone (sans vs. serif) already clears the
axis-apart bar. JetBrains Mono (x-height 0.555) against Fraunces (x-height 0.495) → ratio 0.495 ÷
0.555 = 0.892 — OUTSIDE the ±10% band; classification distance (mono vs. serif) clears the
axis-apart bar, but that does not rescue the metric mismatch — a pairing can read as intentional
and still fight the baseline (`lettering-facts/references/techniques/pairing.md`'s own
caveat: "a high-contrast pair that fails those checks still looks like a mistake — just a louder
one").

## The categorized register (refreshable — a register guide, not a fixed roster)

Named fonts date fast; every entry is a *category example*. The rows with verified metrics above
also appear here with their register; the right-hand column extends the register with faces that
carry real, cited design-history provenance but no published x-height/cap-height figures — most
from `lettering-facts/references/voice/distinctive-and-impactful.md`'s case studies, two
(Crimson Pro, Source Sans 3) from `lettering-facts/references/historical/` or external
sources cited per-row — they inform the *classification* and *register* call, not the metric-ratio
check, until a verified figure is added.

| Register | Faces with verified metrics | Faces with verified history, no metrics yet |
|---|---|---|
| Neutral (the deliberate-disappear choice) | Inter, Roboto, Arial | Open Sans, Lato, San Francisco (`lettering-facts/references/voice/neutral-by-design.md`) |
| Editorial | Fraunces, Source Serif 4 | Newsreader — reading-optimized AND distinctive at once, the honest middle case (`lettering-facts/references/voice/distinctive-and-impactful.md`); Crimson Pro — Jacques Le Bailly's professional redesign of Sebastian Kosch's original Crimson (2009/2010), commissioned by Google³ |
| Technical | IBM Plex Sans, IBM Plex Serif | Source Sans 3 — Paul D. Hunt, Adobe's first open-source typeface (2012), humanist proportions, open apertures, companion to Source Serif (`lettering-facts/references/historical/humanist-sans.md`) |
| Code | JetBrains Mono | Fira Code |
| Distinctive (brand-forward) | Geist | Bricolage Grotesque, Space Grotesk, Playfair Display (`lettering-facts/references/voice/distinctive-and-impactful.md`) |

³ Crimson Pro is new to this corpus (not yet in `lettering-facts`) — verified via Google Fonts'
specimen page and TypeDrawers' designer-history discussion (both accessed 2026-07-05), not an
internal cross-reference. No x-height/cap-height figure was found from a reliable, unit-unambiguous
source for Crimson Pro or Source Sans 3 — one web result claimed Source Sans 3 figures but couldn't
confirm its em-square unit (478/1000 vs. 478/1024 differ enough to matter), so it was deliberately
not used. Both stay in the no-metrics column until a verified figure surfaces.

## Pairing drama — reusing the mechanic, not re-deriving it

`lettering-facts/references/techniques/pairing.md`'s "Contrast Intensity and Perceived
Intentionality" section is the mechanic this skill's craft-correctness step applies: the wider the
gap between two paired voices — weight-axis span, classification distance, or both — the more the
pairing reads as a deliberate decision rather than an accident. Two concrete thresholds this skill
carries forward into `scripts/typeface-check.py` (see SKILL.md's numbers table for the exact
values and the judgment-call note on the weight threshold): a weight gap wide enough reads as
"considered range" even within one family used at its own extremes; a gap that sits in the
ambiguous middle reads as an accident no matter how metric-compatible it is. Classification or
register distance (serif vs. sans vs. mono; neutral vs. distinctive) satisfies the same axis-apart
requirement independent of weight — a pairing only needs ONE real axis apart, not all of them, but
needs at least one.

**Size-jump extremity** is a separate axis from weight/classification — inherited² from
font-selection.md's pre-migration revision, not from pairing.md (that file's own "Contrast
Intensity" section covers weight-axis and classification-distance span only, not size ratios). A
≥ 3× size jump between a kicker and the display it introduces reads as intentional hierarchy; a
≤ 1.5× jump reads as a rounding error the browser default could have produced by accident; the
open interval between the two — big enough to notice, too small to commit to — is its own
anti-pattern. `scripts/typeface-check.py pair <fontA> <weightA> <fontB> <weightB> <sizeA> <sizeB>`
mechanizes all three verdicts (pass the two voices' actual sizes at the step in question,
sourced from `font-token-rules`' bound scale — sizes are optional; omit them to skip this axis).

² Same provenance class as the metrics table above: `font-token-rules/references/font-selection.md`'s
pre-migration revision (2026-07-05).

## Boundary

This file states the operational judgment and the checker's data; it does not re-narrate why a
typeface reads neutral or distinctive (`lettering-facts/references/voice/`), the pairing
research (`lettering-facts/references/techniques/pairing.md`), or how to bind the resulting
decision as CSS custom properties (`font-token-rules`). Read those for the "why"; this file is
the "which, and is it in tolerance."
