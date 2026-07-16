---
name: typography-system-design
description: >-
  Design a full, opinionated 11-voice typography system — font choices and pairing drama — from a
  brand concept or brief. Use when the user wants to design a typography system, pick or design a font pairing
  ("pick a body and display pairing", "is this pairing metric-compatible"), choose fonts for a
  brand, decide which typeface fills each voice (display, heading, body, ui, code), turn "modern and
  clean" into a specific point in design space, or make the distinctive-vs-neutral call per voice: territory, per-voice rationale, a coherence pass, and craft
  verification (metric compatibility, extremity, accessibility floor) — typography-tokens
  realizes it. NOT for color ramps (palette-design); NOT for
  realizing a decided system as tokens, or which font/voice an existing system's token already
  binds (typography-tokens); NOT for type-history knowledge (typography-lettering); NOT for
  Material's typescale (material-design-typography-tokens); NOT for a component (component-forge)
  or the export bundle (design-system-hub).
disable-model-invocation: false
user-invocable: true
---

# typography-system-design — the per-voice font-and-rationale decision

Generator peer of [[typography-tokens]]: this skill DECIDES which typeface fills each voice; the
tokens skill REALIZES that decision as bound `--font-*`/`--type-*` custom properties. Where
[[palette-design]] designs an OKLCH ramp before [[color-verify]] gates it, this skill designs a
typographic system before its own craft-correctness checks gate it — same shape, different
artifact. Its knowledge peer is [[typography-lettering]]: the world-model (why a face reads
neutral or distinctive, real design-history, metric science) this skill draws on but does not
re-narrate.

The discipline this skill exists to enforce: a typography system is a **coherent, opinionated
point in design space**, not five independently-plausible font picks. Most generic type systems
fail before a single font is chosen — the brief was never sharpened past an adjective list, so
every voice gets decided against a different, unstated mental image.

## Inputs (schemas + elicit fallback)

- **BrandSchema / creative brief** — a concept description, reference points (an existing brand,
  a decade, a named aesthetic), and any existing type commitments or hard constraints (heavy
  i18n/script coverage, an accessibility mandate, a locked brand font).
- **Neither exists, or the brief is adjectives only?** Elicit: what's the product, what should it
  feel like (push for a NAMED reference, not a mood), any existing type commitments, any hard
  constraints. Do not proceed on adjectives alone — step 1 below is this skill's own gate.

Classify the ask: design a full system from a brief (needs the BrandSchema above) · re-decide one
voice within an existing system (needs the existing decision doc + which voice changed — steps 2–4
still apply to that voice, step 3's coherence pass re-runs against the other 10) · design or pick
a type SCALE (the size ladder itself) — start from the house fixed typescale
([`references/house-typescale.md`](references/house-typescale.md)): treatments and brands vary
styling (font, weight, tracking, leading, case), never the numbers; deviate only for a stated
platform mandate · "what token for
this text" is not this skill — route to [[typography-tokens]] · "why does this font read neutral"
or "what's the history of X" is not this skill — route to [[typography-lettering]] · "verify this
palette/contrast" is a different artifact class — route to [[color-verify]].

## Procedure (territory → per-voice decisions → coherence → craft check → handoff)

1. **Interpret the territory into a specific point, not a region.** A named reference —
   "restrained Kinfolk-editorial quiet luxury," "1977 Swiss ski-poster energy," "a specific
   existing brand" — *presupposes* a point in design space a generating model can act on without
   guessing; "modern and premium" leaves the search space open and gets filled with the prior
   (`design-system-hub/references/context-potency.md`'s presupposition technique and
   generic-output clinic — cited, not re-derived here; worked point-vs-region transformations in
   [`references/territory-interpretation.md`](references/territory-interpretation.md)). A vague
   brief is this skill's own gate: push back and ask for the named reference before proceeding.

   **How the push-back asks** (canon: ui's layout-decompose `references/taste-elicitation.md`,
   where installed — five rules in one line: ask only genuine taste forks inside the verified
   envelope, options as artifacts not adjectives, one batched round, every option a committable
   plan, the answer locked durably): when the brief admits two or more live territory points —
   or the user cannot name a reference at all — do not ask for adjectives back. Render 2–3
   candidate directions as ONE private HTML artifact of type specimens (each direction's display
   + body faces set in the user's actual product copy, labeled A/B/C), then one AskUserQuestion
   whose options reference the labels, recommended first with what picking it commits ("Kinfolk
   editorial: <faces>, distinctive display, neutral ui"). The chosen territory point lands in the
   per-voice decision doc in the same change; a territory ruled once for this brand is never
   re-asked.
2. **Per-voice creative decisions.** Typography-tokens' five font-family roles (`display · heading
   · body · ui · mono`) are the concrete slots; its eleven voices ride on them (`headline`,
   `sub-heading`, and `title` take `heading`'s face, `kicker`, `code`, and `sub-title` take
   `mono`'s, `label` and `tiny` take `ui`'s, `lead` takes `body`'s — `typography-tokens/SKILL.md`'s
   voice table is canonical, not restated in full here). For each of the five slots: call
   distinctive or neutral against the
   interpreted territory (usually `display`/`headline`/`kicker`/`code` earn distinctiveness;
   `body`/`label`/`tiny` usually want neutrality — the judgment framework this skill
   deepens past `typography-tokens/references/font-selection.md`'s fallback heuristic lives in
   [`references/font-craft.md`](references/font-craft.md)), name a concrete font per slot with a
   rationale tied to the territory (never "this font is modern and clean" — that rationale fits
   any brief and therefore justifies none), and set the pairing drama: weight extremes, size-jump
   ratio, and classification distance, reusing the mechanics
   `typography-lettering/references/techniques/pairing.md`'s "Contrast Intensity and Perceived
   Intentionality" section already established (cited, not re-derived — summarized in the numbers
   table below).
3. **Coherence pass.** Read all 11 voices as one document: does it read as ONE opinionated system,
   or a grab-bag of individually-defensible, collectively-incoherent picks? This is a real, named
   failure mode — a display face chosen for 1970s ski-poster energy sitting over a body face
   chosen for enterprise-dashboard neutrality, with no bridging logic, is two systems wearing one
   README. Every slot's rationale should trace to the SAME interpreted territory from step 1.
4. **Craft-correctness verification.** Run [`scripts/typeface-check.py`](scripts/typeface-check.py)
   over every same-baseline pairing (a headline over its body, a lead pull-quote over its
   citation, a kicker over the display it introduces): x-height/cap-height ratio in tolerance or a stated
   `font-size-adjust` compensation, at least one real axis apart (classification, register, or a
   ≥300-unit weight gap) so a "contrast" pairing doesn't read as an accident, and — when the pair's
   actual sizes are known from `typography-tokens`' bound scale — the size-jump ratio (≥3× hierarchy
   or ≤1.5× rounding-range; the interval between is flagged). Check the
   accessibility floor separately: a distinctive choice on `label`/`body`/`tiny` needs a
   stated reason (a brand mandate, an explicit deliberate override) or it defaults to neutral —
   cite `typography-lettering/references/accessibility/low-vision.md` and
   `typography-lettering/references/accessibility/dyslexia.md` for why those voices carry the
   floor. If the brief names multi-script needs, confirm every chosen face actually ships the
   needed scripts (`typography-lettering/references/scripts/`) before finalizing.
5. **Handoff.** The output is a concrete per-voice font-and-rationale decision document — five
   family-slot decisions, their rationale, the pairing drama, the coherence read, and the checker's
   verdict on every pairing — routed to [[typography-tokens]] for REALIZATION as bound `--font-*`/
   `--type-*` custom properties. This skill never emits CSS or token names; typography-tokens
   consumes this skill's decision, it does not make it.

## The numbers (derived from the cited peers — not invented here)

| Parameter | Value |
|---|---|
| Metric compatibility tolerance | x-height AND cap-height (when both are known) within ±10% of each other at the same nominal size (ratio ≥ 0.90), else a stated `font-size-adjust` compensation — `typography-lettering/references/techniques/pairing.md` |
| "Real axis apart" — weight | ≥ 300 weight units apart reads as a considered, deliberate axis; chosen just above pairing.md's documented accidental bound (a 200-unit gap, "400 vs 600") and below its considered bound (an 800-unit gap, "100 vs 900") — it also coincides with the conventional regular(400)→bold(700) step. No exact boundary is given in the source, so this is a stated judgment call, not a re-derivation |
| "Real axis apart" — classification/register | family (serif/sans/mono) differs, OR register (neutral/distinctive/editorial/technical/code) differs — either alone satisfies the axis, independent of weight |
| Size-jump extremity | ≥ 3× ratio reads as hierarchy; ≤ 1.5× reads as a rounding error; the interval between is the "ambiguous" anti-pattern — mechanized in `typeface-check.py`'s optional `<sizeA> <sizeB>` args, see [`references/font-craft.md`](references/font-craft.md) |
| Accessibility floor | `label` / `body` / `tiny` default to the accessibility-safe (usually neutral) choice; a distinctive override needs a stated reason, never silence |

## Mechanism — `scripts/typeface-check.py`

Metric-ratio, axis-apart, and size-jump arithmetic is deterministic derivation once the inputs
(two named fonts, their chosen weights, and optionally their sizes) are fixed, so it routes to
code: `typeface-check.py pair <fontA> <weightA> <fontB> <weightB> [<sizeA> <sizeB>]` computes the
x-height/cap-height ratio against an embedded, cited metrics table (mirrors
[`references/font-craft.md`](references/font-craft.md)'s metrics table exactly — 7 rows inherited
from typography-tokens' pre-migration font-selection.md, 2 rows from
`typography-lettering/references/voice/neutral-by-design.md`'s Roboto/Arial figures — extend the
table only with a verified, cited source, never a guessed number; `selftest` mechanically checks
the two tables haven't drifted apart), reports tolerance pass/fail, reports the axis-apart verdict
(classification/register distance OR the weight gap), and — when sizes are given — reports the
size-jump verdict (hierarchy / rounding-range / ambiguous). Python, not `.mjs`: this is pure
numeric/classification computation over a small fixed table, not a scan of live UI source files
(the job typography-tokens' `type-check.mjs` does) — it matches the corpus's Python convention for
deterministic-derivation checkers (`ramp_build.py`, `contrast-check.py`, `routing_eval.py`).
`typeface-check.py selftest` locks it: the Inter/Fraunces worked pairing (ratio ≈ 0.908, in
tolerance, classification-distant), the IBM Plex Sans/Serif metric-matched pair (ratio 1.0,
classification-distant), a real out-of-tolerance pair (JetBrains Mono against Fraunces, ratio ≈
0.892, flagged), the near-identical anti-pattern (Inter 400 against Inter 600 — no real axis
apart), the considered-range pass (Inter 100 against Inter 900 — one family at real weight
extremes, axis apart on weight alone), a size-jump hierarchy pass (sizes 12/48, ratio 4.0), a
size-jump rounding-range pass (sizes 16/18, ratio 1.125), and the size-jump ambiguous anti-pattern
(sizes 16/32, ratio 2.0 — big enough to notice, too small to commit to).

## Detection catalog (generation anti-patterns)

An adjective-only territory ("modern and premium") accepted without pushback — the model fills the
region with its prior · a distinctive choice on `label`/`body`/`tiny` with no stated reason
· two near-identical fonts, or one font at two middling weights, standing in for "contrast" · a
same-baseline pairing with a computed ratio outside ±10% and no stated `font-size-adjust`
compensation · per-voice rationale that is generic ("this font is modern and clean") rather than
tied to the interpreted territory · a system that is individually defensible per voice but reads as
a grab-bag end to end · a font choice that hedges into the safest possible option on a voice
explicitly earmarked for distinctiveness · emitting a decision without running
`typeface-check.py` over every same-baseline pairing · doing typography-tokens' job (binding CSS
custom properties) instead of this skill's (deciding which typeface fills the role).

## Material & routing

| Path / peer | Use |
|---|---|
| [`references/rubric.md`](references/rubric.md) | the 6 scored dimensions + promote gate |
| [`references/font-craft.md`](references/font-craft.md) | the deepened per-voice distinctive-vs-neutral judgment, the metrics table, the categorized font register |
| [`references/territory-interpretation.md`](references/territory-interpretation.md) | worked point-vs-region transformations |
| [`references/house-typescale.md`](references/house-typescale.md) | the house fixed typescale — the 11-voice size table (per breakpoint) every ask about designing a type scale starts from |
| [`scripts/typeface-check.py`](scripts/typeface-check.py) | the metric-ratio + axis-apart + size-jump checker + selftest |
| `scripts/routing-corpus.json` | the checked-in M2 routing corpus |
| [[typography-tokens]] | the mandatory REALIZATION handoff — binds the decision as `--font-*`/`--type-*` |
| [[typography-lettering]] | the knowledge peer — voice/, techniques/pairing.md, accessibility/, metrics/, scripts/ |
| `design-system-hub/references/context-potency.md` | the presupposition / generic-output-clinic doctrine step 1 applies (read-only citation, not this skill's to edit) |
| ui's layout-decompose `references/taste-elicitation.md` (soft, where installed) | the asking discipline step 1's push-back wires — read-only citation; its five-rule one-liner is compressed inline |
| [[component-forge]] | NOT this skill's job — builds the component that consumes the type |

**Update:** when typography-tokens' voice table or five family-role slots change, or
typography-lettering's `voice/`, `techniques/pairing.md`, or `accessibility/` files move, re-derive
this skill's citations and the numbers table from the changed source — never patch the prose
independently — then re-run `typeface-check.py selftest` and the routing corpus. When ui's
taste-elicitation canon moves, re-derive step 1's "How the push-back asks" block (its five-rule
one-liner is a compression of that canon; the canon wins).

**Done** = every same-baseline pairing in the decision doc carries a computed ratio (in tolerance
or compensated) and an axis-apart verdict, the territory is a stated point with a named reference,
every voice's rationale traces to it, and typography-tokens has received the handoff. **NOT done**
= a decision emitted without a checker run, or a territory statement that is still a region.
