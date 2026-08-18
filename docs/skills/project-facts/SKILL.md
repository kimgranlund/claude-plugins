---
name: project-facts
description: >
  Harvest a project's DOMAIN KNOWLEDGE corpus — business logic, architectures, unique-IP
  structures — for a human/business reader. Discovers topic zones from prototypes, PRDs,
  brief/IDRs, ADRs, roadmaps; scores each zone two-axis (Outside-In x Inside-Out, weighted
  Outside-In-higher). Use for "extract domain knowledge from this project", "write up the
  business logic as a reference doc", "what this codebase does, for a non-engineer". NOT a plain
  reference doc with no discovery/scoring (docs:make-reference); NOT an already-scorable system's
  investigation (docs:research-methods); NOT the agent-facing sibling corpus (project-context,
  #613 — shares `references/harvest-core.md`, opposite weighting).
disable-model-invocation: false
user-invocable: true
---

# Docs — Domain-Knowledge Harvest (`project-facts`)

Extracts a project's domain-knowledge corpus: the business logic, technical architectures, and
unique-IP structures a human or business reader needs, discovered from the project's own sources
rather than forced into a fixed template.

## Operating model (essentials; depth in `references/`)

- Two siblings, one core: this skill and the project-context capability (#613) share ONE
  definition + rubric core (`references/harvest-core.md`) — cited by both, duplicated by neither.
- Topic zones are **discovered per project**, never a fixed taxonomy — a zone earns its place by
  recurring across at least two independent harvest sources.
- Every zone is scored through **both** axes, every time — Outside-In and Inside-Out — this corpus
  weighted Outside-In 60/Inside-Out 40 (`harvest-core.md`'s R5).
- The corpus is not done until an eval run proves it's *valuable*, not merely rubric-clean
  (`references/eval-harness.md`) — a payload-layer Q&A run against the corpus, scored against a
  known-answer key.

## Procedure

1. **Gather** the five harvest sources in intent-first order (prototypes → brief/IDRs → PRDs →
   ADRs → roadmaps) — `references/extraction-procedure.md` Step 1.
2. **Discover** topic zones from what recurs across those sources — Step 2.
3. **Score** every zone on both axes, citing the source passage for each finding — Step 3.
4. **Weight** each zone's score per this corpus's Outside-In-higher ratio and rank the corpus by
   it — Step 4.
5. **Write** the corpus as a `docs:make-reference`-shaped doc (one topic, headed, dated,
   canonical) — Step 5.
6. **Self-score** against `references/harvest-core.md`'s rubric (gate: R1, R4, R5, R7 ≥ 3), then
   **run the eval** (`references/eval-harness.md`) — Step 6. A corpus that fails the gate or the
   eval returns to the step that produced the gap; it does not ship as a partial read.

## Output contract (a harvest run)

```
Project: <root>  ·  Rubric: harvest-core (project-facts weighting: Outside-In 60/Inside-Out 40)
Corpus: <path to the produced reference doc>
| Zone | Outside-In | Inside-Out | Weighted | Source |
Gate (R1,R4,R5,R7): <pass/fail>
Eval (eval-harness.md): <pass/fail> — <top misses, if any>
```

## References & tools

| Path | Use when |
|---|---|
| `references/harvest-core.md` | The shared definition core (both corpora) + the two-axis rubric — canonical, cited by the project-context sibling too |
| `references/extraction-procedure.md` | This corpus's own step-by-step harvest procedure and weighting arithmetic |
| `references/eval-harness.md` | Deliverable (c): the eval prompt set, sample project, and scored-report shape |

## Composition

- `docs:make-reference` — the final write-up (Step 5) is authored and reviewed to that skill's
  own shape; this skill does not re-derive make-reference's own authoring standards.
- `docs:make-rubric` — `harvest-core.md`'s table follows make-rubric's own criteria × levels ×
  descriptors × aggregation shape; consulted, not restated.
- `docs:research-methods` / `docs:agent-harness-rules` — the eval harness's payload-layer choice
  and scored-report shape follow `agent-harness-rules`' design method; a genuinely open-ended
  investigation of *why* a harvest underperforms is `research-methods`' territory, not this
  skill's.

**Done** when the corpus's every discovered zone carries both axis scores with a cited source, the
corpus gates clean (R1, R4, R5, R7 ≥ 3), and an eval run against it scores at or above the
project's own bar with no unresolved top miss. **NOT done** while a zone carries only its
"obvious" axis, a finding has no source citation, or the corpus was never actually asked the eval's
own prompts.
