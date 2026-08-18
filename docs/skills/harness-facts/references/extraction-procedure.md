# Extraction procedure — harvesting a project's harness-context corpus

This corpus (`harness-facts`) extracts the same harvestable substance as `project-facts`,
reframed for a coding agent's own harness — CLAUDE.md-grade sections, path-scoped rules,
knowledge-pack seeds, dispatch context. Shared definitions and the scoring rubric live once in
`../project-facts/references/harvest-core.md`; this file is the step-by-step procedure specific to
this corpus's own weighting and output shape.

## Step 1 — Gather the harvest sources

Read the same five harvest source kinds `harvest-core.md` defines, in the same intent-first order:
functional prototypes → intent records (brief/IDRs) → PRDs → ADRs → roadmaps/PLANs. A source that
doesn't exist for this project is skipped, not faked — name the gap in the run manifest
(`output-artifacts.md`) rather than silently backfilling it.

**Zero-source exit.** Same rule as the sibling: if none of the five source kinds exist for this
project at all, stop here and report the gap; never discover zones from application code alone —
`harvest-core.md`'s discovery rule is what a from-scratch, code-only pass would substitute
inference for, and that's a materially different procedure this skill doesn't perform.

## Step 2 — Discover topic zones

Per `harvest-core.md`'s discovery rule: a zone earns its place by recurring across at least two
independent harvest sources (a prototype alone naming something is a candidate, not yet a zone).
**Naming register differs from the sibling here.** Name each zone mechanism-honest — the way a
coding agent would recognize it operationally — not the business-facing gloss the sibling uses for
the same substance: this corpus might name a zone "release gate (G1–G11)" where the sibling would
say "quality assurance," or "worktree-scoped campaign execution" where the sibling would say
"delivery process." The discovery rule itself — recurrence across ≥2 sources — is unchanged; only
the label register moves with the consumer.

## Step 3 — Score every zone on both axes

For each discovered zone, fill in both lenses from `harvest-core.md`'s rubric, citing the source
passage for each finding (R6):

- **Inside-Out**: the zone's actual operations, what it binds to (files, other zones, external
  systems/tools), what feedback or failure signal it surfaces — the mechanism a coding agent would
  need to invoke or obey correctly.
- **Outside-In**: why the zone exists, what a reader unfamiliar with the mechanism would need to
  know before touching it — thinner for this corpus by design (the mirror of the sibling's own
  Inside-Out axis being the thinner one there), a fact this corpus's weighting (Step 4) makes
  explicit rather than leaves implicit.

## Step 4 — Apply this corpus's weighting

`harness-facts` weights **Inside-Out 60 / Outside-In 40** (per `harvest-core.md`'s R5 — the exact
mirror of the sibling's Outside-In 60/Inside-Out 40). Compute each zone's weighted score as
`0.6 * InsideOut + 0.4 * OutsideIn`; rank zones by this weighted score so the emitted artifacts
prioritize the mechanism-first ordering a harness actually needs, not the business-relevance
ordering the sibling's human/business reader needs.

## Step 5 — Emit the artifacts

Unlike the sibling (whose Step 5 writes one reference doc), this corpus's write step emits four
artifact classes plus a run manifest — see `output-artifacts.md` for each artifact class's own
conformance contract and the manifest's shape. Every emitted artifact must trace back to a scored
zone from Step 3/4; a zone that never earns a place in any artifact is named in the manifest as
"discovered, not surfaced" rather than silently dropped.

## Step 6 — Score the corpus, then run the eval

Self-score the run's manifest against `harvest-core.md`'s rubric (R1–R7); gate on R1, R4, R5, R7 ≥
3 per its own promote rule. Then run `eval-harness.md`'s WITH-vs-WITHOUT eval — the harness for
deliverable (c), proving the emitted artifacts measurably improve a coding agent's task
performance, not merely that the run passed its own rubric.
