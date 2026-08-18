---
name: harness-facts
description: >
  Harvest a project's context for a CODING AGENT'S OWN HARNESS. Zones from prototypes, PRDs,
  brief/IDRs, ADRs, roadmaps, scored two-axis (Inside-Out x Outside-In, Inside-Out-higher); emits
  install-ready artifacts: a CLAUDE.md-grade entry-file section, `.claude/rules/` files, pack seed
  candidates, a dispatch-context digest. Use for "harvest this project's context for the harness",
  "produce CLAUDE.md sections and rules from what this codebase does". NOT docs:project-facts
  (human/business corpus, shares `harvest-core.md`, opposite weight); NOT
  harness:entry-file-rules/check-entry-file (auditing an EXISTING CLAUDE.md); NOT
  harness:make-pack (filling a pack); NOT docs:agent-harness-rules (a NEW eval harness); NOT
  harness:save-lessons (fact durability).
disable-model-invocation: false
user-invocable: true
---

# Docs — Harness-Context Harvest (`harness-facts`)

Extracts a project's context for a coding agent's own harness: the same business logic, technical
architectures, and unique-IP structures a project's sources already state, discovered per-project
rather than forced into a fixed template, but reframed and staged as install-ready harness
artifacts rather than a document for a human to read.

## Operating model (essentials; depth in `references/`)

- Two siblings, one core: this skill and `project-facts` (#612) share ONE definition + rubric core
  (`../project-facts/references/harvest-core.md`) — cited by both, duplicated by neither.
- Topic zones are **discovered per project**, never a fixed taxonomy — a zone earns its place by
  recurring across at least two independent harvest sources, named here mechanism-honest (a zone
  may read "release gate (G1–G11)" where the sibling would read "quality assurance").
- Every zone is scored through **both** axes, every time — this corpus weighted
  **Inside-Out 60/Outside-In 40** (`harvest-core.md`'s R5 — the mirror of the sibling's own
  Outside-In 60/Inside-Out 40).
- The write step is not a prose corpus — it's ready-to-install harness artifacts (entry-file
  section, path-scoped rules, pack seeds, dispatch context) staged for the invoker to install;
  installation itself is always the invoker's own act, never this skill's.
- The corpus is not done until a **WITH-vs-WITHOUT eval** proves the emitted artifacts measurably
  improve a coding agent's task performance (`references/eval-harness.md`), not merely that the
  run is rubric-clean.

## Procedure

1. **Gather** the five harvest sources, intent-first order — `references/extraction-procedure.md`
   Step 1. Zero sources at all → stop and report the gap; never discover zones from application
   code alone.
2. **Discover** topic zones from what recurs across those sources, mechanism-honest naming
   register — Step 2.
3. **Score** every zone on both axes, citing the source passage for each finding — Step 3.
4. **Weight** each zone Inside-Out 60/Outside-In 40 and rank the run by it — Step 4.
5. **Emit** the four artifact classes plus the run manifest
   (`references/output-artifacts.md`) — Step 5.
6. **Self-score** against `references/harvest-core.md`'s rubric (gate: R1, R4, R5, R7 ≥ 3), then
   **run the eval** (`references/eval-harness.md`) — Step 6. A run that fails the gate or the eval
   returns to the step that produced the gap; it does not ship as a partial read.

## Output contract (a harvest run)

```
Project: <root>  ·  Rubric: harvest-core (harness-facts weighting: Inside-Out 60/Outside-In 40)
Staging path: <where the invoking session directed output>
| Artifact class | Path | Zones covered | Weighted score range | Source |
Manifest: <path to the run manifest — the gateable spine>
Gate (R1,R4,R5,R7): <pass/fail>
Eval (eval-harness.md, WITH vs WITHOUT): <pass/fail> — delta: <n>/6 improved — <top misses, if any>
```

## References & tools

| Path | Use when |
|---|---|
| `../project-facts/references/harvest-core.md` | The shared definition core + two-axis rubric — canonical, lives with the sibling, cited never duplicated |
| `references/extraction-procedure.md` | This corpus's own step-by-step harvest procedure and the Inside-Out 60/40 arithmetic |
| `references/output-artifacts.md` | The conformance contract for each emitted artifact class, plus the run-manifest shape |
| `references/eval-harness.md` | Deliverable (c): the WITH-vs-WITHOUT F1–F6 prompt set, sample project, isolation rule, and delta-scored report shape |

## Composition

- `project-facts` — the human/business-facing sibling; shares `harvest-core.md`, never its
  substance text or its output shape.
- `harness:entry-file-rules` — the residency-test standard the entry-file-grade artifact must
  pass; soft named mention only, no preload, no cross-plugin path (`.claude/rules/plugin-authoring.md`).
- `docs:agent-harness-rules` — the assert-layer design method behind this skill's payload-layer
  WITH-vs-WITHOUT eval choice.
- `docs:make-rubric` — `harvest-core.md`'s table follows make-rubric's own criteria × levels ×
  descriptors × aggregation shape; consulted, not restated.
- `harness:make-pack` — pack seed candidates name the target pack and the exact `/make-pack`
  invocation a human runs next; this skill never hand-scaffolds a pack itself.

**Done** when every discovered zone carries both axis scores with a cited source, the run gates
clean (R1, R4, R5, R7 ≥ 3), every emitted artifact traces to the run manifest, and the
WITH-vs-WITHOUT eval scores WITH strictly better than WITHOUT with every WITH answer traceable to
an emitted artifact. **NOT done** while a zone carries only its "obvious" axis, an artifact has no
manifest entry, this skill installed output into a live CLAUDE.md/`.claude/rules/` tree itself
(installation is always the invoker's act), or the eval never actually ran both arms.
