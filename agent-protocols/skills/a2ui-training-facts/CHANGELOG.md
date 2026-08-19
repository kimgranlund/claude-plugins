# Changelog — a2ui-training-corpus

## 2026-08-19 — field-doctrine harvest (agent-ui ADR wave)

- `judge-and-verdict-adapter.md` UPDATE: ADR-0165's durable admission disposition (the archived
  `VerdictsFile`, latest-date precedence, refusals never expire, the `unjudgedAdmissions` gate leg),
  the GH #1346 fail-closed importer law (a bare run is legal only as the all-`E_DUP` no-op), the
  MIN-fold in the field (GH #1262's P9 rubric fold + re-judge), and repair-then-replace over
  discard (PR #1326's nine-record wave).
- `canonicalization-and-dedup.md`: the ID-spelling bullet gains its drift consequence (ids-only
  edits hash identical → `E_DUP`, PR #1342 instance).
- `retrieval-and-repair-loop.md` UPDATE: producer-grammar teaching — bind BOTH axes (the GH #1279
  sentence-length-badge lesson) and the four teaching lanes (grammar clause / mini-skill /
  node-idioms card / judged exemplar), with ADR-0207 A2 as the worked lane-choice decision.
- No description/evals change (routing surface untouched).

## 2026-07-07 — minted (v1.0)

Net-new global knowledge pack, one of the 4-way A2UI split (siblings: `a2ui-protocol`,
`a2ui-catalog-design`, `a2ui-conversational-agent`). Documents the realized A2UI training-corpus
subsystem of `agent-ui` — `packages/agent-ui/a2ui/src/corpus/**` + `tools/corpus/**`, governed by
ADR-0060/0061/0062/0063/0064/0068 and `a2ui-training-corpus.spec.md` (v0.5).

- Six axes → one reference each: record schema & provenance · exemplar/eval split & no-leak ·
  canonicalization & dedup · admission gate & healing · judge/verdict adapter · retrieval & repair
  loop. Plus `sources.md` (provenance) and `scripts/routing-corpus.json`.
- `user-invocable: false` — ANSWERS from a cited repo corpus, routes all making to
  `a2ui-corpus-curate` (skill), the `a2ui-builder` / `a2ui-reviewer` agents.
- Every claim cites `file:line` or an ADR/SPEC clause, verified against the working tree.
- Honesty flag: SPEC-R13 `repair()`, SPEC-R14 `score()`, SPEC-R15 lift are **specced, not built**
  (grep-clean); the state machine + the LLD-C15 standing re-validation gate do the SPEC-R13 work today.
- Gates: skill-author harness 15/15; routing_eval F1 0.85 (clear). Reviewed by `skill-reviewer`
  (FLOOR pass, ~30 citations spot-checked, no dim < 3) and `linguistics-reviewer` (L1/L3/L6 gate pass);
  their minor refinements applied (frame-led frontier line, explicit answer-complete predicate,
  redundant negations flipped to affirmative, designed-not-built flag added to the description).
