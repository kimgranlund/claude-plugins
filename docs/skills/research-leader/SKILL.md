---
name: research-leader
description: >-
  The deliverable schema and rubric research-leader's typed findings are authored to and
  graded against — six required fields per finding, a four-axis rubric (knowledge, actionable,
  grounding, novelty-vs-known). Use when the user asks to dispatch research-leader, author or
  review one of its deliverable files, or score a research deliverable with doc-checker. NOT
  general rubric authoring (make-rubric); NOT a fixed-scorer investigation loop
  (research-methods/experiment-runner); NOT a gather-only /make-pack ledger (harness:fact-finder).
disable-model-invocation: false
user-invocable: false
---

# research-leader — deliverable schema and rubric

`lld-0023-research-specialist-deliverable-plan` resolved the schema and rubric a synthesis-
permitted, web-search research agent's output is held to. This skill is where the resolution
lives once built — `docs:agents/research-leader.md`'s owning skill, and the artifact
`docs:doc-checker` reads when dispatched at one of its deliverables (its own charter already
covers "a reference doc... scored against the owning skill's bundled `references/rubric.md`"
generically; nothing here edits that charter).

Reading test: *consult this for the research-leader deliverable's own shape and standard.*

## References
| File | Read when |
|---|---|
| `references/DELIVERABLE-SCHEMA.md` | Authoring or auditing a research-leader deliverable's six required fields per finding |
| `references/rubric.md` | Grading a deliverable — the four axes (knowledge, actionable, grounding, novelty-vs-known), their 1/3/5 anchors, the accept gate, and the confidence-marker vocabulary |

## Relationship to `harness:fact-finder`

Disjoint by design (`lld-0023-research-specialist-deliverable-plan` Resolution 1) — no shared
code, no shared file, no call from one to the other. The only relationship is the confidence-
marker vocabulary `research-leader` reuses verbatim (a citation, not a coupling).
`fact-finder`'s own no-synthesis contract stays untouched; dispatch `research-leader` instead
whenever the ask needs judgment (best practices, case studies, unique insight), not a plain
gather-only ledger.

**Done** when a research-leader deliverable's six fields per finding match
`DELIVERABLE-SCHEMA.md` and its rubric self-score, later confirmed by an independent
`doc-checker` pass, converges on `rubric.md`'s own four axes. **NOT done** while a finding is
missing a required field, a `[verified]` marker doesn't match its own definition, or a novelty
flag is asserted with no checkable citation or search scope behind it.
