# intent — brand-methodology-rules
status: shipped
species: knowledge
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability-uplift

## trigger
should:      ["brand strategy", "positioning", "cultural research", "brand archaeology",
              "brand identity", "expression system", "rebrand", "category design",
              "brand stewardship", "what should we stand for", "what's our point of view"]
should_not:  ["marketing tactics or performance media" (out of scope, adjacent discipline),
              "product strategy, management, or UX" (product-forge's domain)]

## delta
Retrospective record — no live forge interview exists; this skill was ported, not freshly minted.
Without it, "brand strategy" collapses into the artifacts that feel like strategy but commit to
nothing — archetypes, vision/mission/values triplets, personas, "brand DNA" word-clouds — because
they're easy and require no decisions. With it, a brand is built through a gated pipeline
(RESEARCH → STRATEGY → EXPRESSION → STEWARDSHIP, no skipping a gate), a load-bearing Foundation
Canon that actively rejects those four artifacts by name, and a three-seat discipline (Muse
aspires, Team makes, Council reviews) with one invariant: no seat judges its own work.

## fences
- NOT scoring or auditing brand work, or running the critic council — `brand-rubrics`
- NOT organizing brand documents into the corpus, or wiring the `brand-corpus` MCP — `brand-corpus`
- NOT marketing tactics, performance media, conversion, or PR
- NOT product strategy, product management, or UX — a different plugin's domain

## assertions
1. States the four-stage pipeline and that each stage gates the next (no position before research,
   no expression before strategy).
2. States the six load-bearing Foundation Canon components and the bullshit filter's four rejected
   artifacts.
3. States the three seats (Muse/Team/Council) and the one invariant (no seat judges its own work).
4. Routes scoring to `brand-rubrics` and corpus organization to `brand-corpus` rather than
   attempting either itself.

## gates
Forge event: the brand-forge → brand-design migration campaign, Phase 3 Track D (2026-08-19) —
ported from brand-forge's shipped `brand-methodology` skill, renamed `brand-methodology-rules` in
an earlier phase of this campaign (source
`/Users/kimba/Projects/nonoun/nonoun-plugins/brand-forge`, frozen SHA
`1e0d2d9e554b547f59260f63e31b4af2575196b0`, 2026-06-20), not authored fresh through make-skill's
P0-P5 ladder. Track D re-verified against pack-writing-rules — 9 reference files exceeded the
flat-consult-table threshold, so this pack is the one of the four that gained a
`references/INDEX.md` grouping them into 4 declared axes (Foundation Canon · foundation component
methods · creative collaboration & team operations · Brand Stack condensation) — stale
`brand-evaluate`/`/brand-council`/`/brand-muse`/etc. names repaired to their current forms, and
ran a fresh-context skill-checker pass over the whole 4-pack slice.

## rulings
- No live P0-P5 forge history exists for this skill; this record is written retrospectively from
  the shipped artifact, per this migration's convention for ported (not freshly forged) packs.
- Two external-citation claims in `references/creative-collaboration.md` (the Bernbach/DDB
  attribution, the Knapp/IDEO/Quiller-Couch citations) were marked `[inferred]` rather than
  `[verified]` — they are widely repeated in creative-industry lore but were not re-checked
  against a primary source this session.
