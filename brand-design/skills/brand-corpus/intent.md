# intent — brand-corpus
status: shipped
species: knowledge
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability-uplift

## trigger
should:      ["brand corpus", "organize brand files", "brand documentation structure",
              "set up brand docs", "where does this brand file go", "brand file naming",
              "ingest source docs", "keep the source material", "who added this",
              "brand attribution", "where did this come from"]
should_not:  ["write the brand strategy" (routes to brand-methodology-rules),
              "score this brand work" (routes to brand-rubrics)]

## delta
Retrospective record — no live forge interview exists for this skill; it was ported, not freshly
minted. Without it, a brand corpus accretes as an unstructured folder: no fixed layer order, no
naming split between a Claude Project (flat) and a filesystem (folder) destination, no maturity
signal to catch a team faking a late-stage artifact (guidelines) on an undecided foundation. With
it, every brand file has one of eight numbered homes (00-sources retained evidence, 01-08 the
brand itself), one of two naming conventions never mixed, a maturity stage (0-6), and provenance
frontmatter that survives a corpus with no git.

## fences
- NOT for writing the brand strategy itself — `brand-methodology-rules`
- NOT for scoring or auditing brand work — `brand-rubrics`
- NOT the interactive guidelines-elicitation loop — `brand-guidelines`

## assertions
1. States the eight numbered layers (00-sources retained/unscored, then 01-08) and their load order.
2. States both naming conventions (flat double-hyphen vs. folder path) and that mixing them is a corpus defect.
3. States the maturity stages 0-6 and "don't skip stages by faking artifacts."
4. States the read-before-write discipline (read before overwrite, confirm before write, supersede don't delete).

## gates
Forge event: the brand-forge → brand-design migration campaign, Phase 3 Track D (2026-08-19) —
ported from brand-forge's shipped `brand-corpus` skill (source
`/Users/kimba/Projects/nonoun/nonoun-plugins/brand-forge`, frozen SHA
`1e0d2d9e554b547f59260f63e31b4af2575196b0`, 2026-06-20), not authored fresh through make-skill's
P0-P5 ladder. Track D re-verified the shipped body against pack-writing-rules (axes declared,
consult table added, stale `bin/`/skill/command names repaired to their current forms, snapshot
provenance recorded) and ran a fresh-context skill-checker pass over the whole 4-pack slice.

## rulings
- No live P0-P5 forge history exists for this skill; this record is written retrospectively from
  the shipped artifact, per this migration's convention for ported (not freshly forged) packs.
