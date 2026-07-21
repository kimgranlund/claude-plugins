---
name: make-rubric
description: >
  Author, evaluate, improve, or update a rubric so it produces consistent,
  actionable judgments, against the bundled rubric-for-rubrics. Use whenever
  building, scoring, fixing, or re-syncing a scoring rubric, eval criteria, a
  quality checklist, or a /goal completion condition: "write a rubric", "is this
  rubric any good", "my reviewers score differently", "tighten these anchors",
  "turn this into eval criteria", "which dimensions should gate promotion and
  at what threshold", "re-anchor this rubric — the artifact standard changed",
  "the level descriptors are vague — fix the anchors". NOT for the skill/agent
  carrying the rubric (forge's skill-forge / agent-forge) nor the /goal loop itself
  (loop-rules — this skill owns only the completion condition's quality).
disable-model-invocation: false
user-invocable: true
---

# Harness — Rubric Authoring & Review

A rubric is the verification artifact native to agentic systems: criteria × levels × descriptors × aggregation. It is **the standard** — the spine every generate → evaluate → improve loop turns on — which puts this skill **upstream of every other**: anything that ships a `references/rubric.md` depends on it, and forge's **skill-forge** builds skills *to* the rubric authored here. One rubric-for-rubrics drives four operations over a rubric: **create · evaluate · improve · update** — authored so two reviewers would score it the same way.

## Operating model (essentials; depth in `references/foundations.md`)
- `[gate]` = mechanically checkable; `[review]` = judgment against anchors with cited evidence. The tag must be accurate.
- Anchors, not adjectives: concrete 1/3/5 descriptors a reviewer can match to evidence.
- End with the aggregation/gate rule and the top failure to look for first.

## Create (a new rubric)
1. Name each dimension; type it correctly; write concrete 1/3/5 anchors and the measurement plan (the evidence).
2. Keep dimensions independent; make each failure imply a specific fix; state the gate set + threshold.
3. Self-score (below); fix until every gate dimension (D1, D3, D5, D8) ≥ 3.

## Evaluate (score an existing rubric)
1. Run the mechanical gates: `python scripts/harness_checks.py rubric <path>`.
2. Score the `[review]` dimensions against `references/rubric.md`. The top failure is bare scales with no anchors.
3. Emit the gap-map (contract below): each dimension **located, cited, prescriptive**. **Generator ≠ critic:** don't grade a rubric you just wrote in the same pass — dispatch the **doc-checker** agent (the document family's shared fresh-context critic; standalone rubrics are in its charter). A rubric that can't survive an independent read can't be trusted to judge anything else.

## Improve (repair a preexisting rubric)
Evaluate first, then close the gap — anchors before polish (a bare scale is the top defect). Fix the rubric, re-run the gates, finalize only when every gate dim ≥ 3 and two readers would score it the same. (Improve = evaluate + targeted regenerate.)

## Update (re-sync after drift)
A rubric drifts when what it grades changes — a new failure mode appears, a dimension stops discriminating, the artifact's standard moves. Re-derive the affected dimensions from the change (add the missing axis, re-anchor the stale one); never let a rubric certify against a bar the world has left behind. Its dependents — every skill scoring against it — re-Evaluate after.

## Output contract (review)
```
Artifact: <rubric>  ·  Rubric: rubric-rubric
| Dim | Type | Score | Finding | Evidence |
Gate (D1,D3,D5,D8): <pass/fail>   [harness_checks: <pass/fail>]
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `scripts/harness_checks.py rubric` | Mechanical gate checks (dims typed, gate rule present) |
| `references/rubric.md` | The `[review]` dimensions and anchors |
| `references/best-practices.md` | Authoring guidance / explaining a finding |
| `references/foundations.md` | When a finding turns on a shared model |

**Done** when the rubric passes the mechanical gates, every gate dimension (D1, D3, D5, D8) scores ≥ 3, and an independent read (doc-checker) converges on the same scores. **NOT done** while any scale is bare, a `[gate]` tag hides a judgment call, the aggregation rule is missing — or the only score the rubric carries is the one its own author gave it.
