---
name: loop-rules
description: >
  Design or review continuation patterns — /goal, /loop, Stop hooks, auto mode —
  that drive autonomous work, scoring against the bundled rubric. Use whenever
  writing or auditing autonomous loops: "write a /goal", "should I use /goal
  or /loop", "write a verifiable end-state condition", "add a turn cap / bound
  an autonomous run", "my goal loop never stops / spins", "it keeps retrying
  the same failure", "the agent spins / thrashes and burns turns", "make it
  keep working until clean". NOT for how the delegated work composes —
  skill/agent wiring, dispatch, frontmatter (team-or-solo-rules); this skill
  owns only when the next turn fires.
disable-model-invocation: false
user-invocable: false
---

# Harness — Control Patterns (/goal, /loop) Design & Review

**Plane separation**: these patterns decide *when the next turn fires*, never *what runs on it* — discovery handles selection underneath, every turn. Design a pattern that finishes (or polls) correctly, or review one.

## Operating model (essentials; depth in `references/foundations.md`)
- Plane separation (above) is the first check on any design or review — a goal text that tries to select skills or agents fails it.
- Objective mode: a goal is a verifiable end-state, not a process; a separate fast evaluator judges only what the transcript surfaces.
- Hard "don't finish until X" is a Stop hook (exit 2) + a deterministic check, not a sentence.
- A loop that delegates work is an orchestrated system: hierarchical budgets, a closed continuation-decision set, locus escalation on repeat failure, durable state — the canon is `references/self-orchestrated-looping-agentic-systems.md`.

## Design
1. Pick the pattern: finish-line the agent can prove → `/goal`; recurring external check → `/loop`; enforced "until clean" → Stop hook + check; collaboration → team.
2. Write the `/goal` as a measurable end-state with the proof method named; make the proof land in the transcript; add a turn/time cap, a scope guard, and an escalation clause (the same check failing twice → stop and report, not retry).
3. Self-score (below); fix until every gate dimension (C1, C3) ≥ 3.

## Review
1. Run the mechanical gates on the goal string: `python scripts/harness_checks.py goal "<goal text>"`.
2. Score the `[review]` dimensions against `references/rubric.md`. The top failure is an unverifiable or self-graded condition.
3. Findings by severity; gate verdict; top issues with a concrete fix each.

## Improve (repair a preexisting loop design)
Review first, then close the gap — the condition before polish (an unverifiable or self-graded condition is the top defect). Fix the goal text or pattern choice, re-run the gates, finalize only when every gate dimension (C1, C3) ≥ 3. (Improve = review + targeted redesign.)

## Update (re-sync after the build changes)
Continuation mechanics drift with the harness build. The `△ verify against your build` markers in `references/best-practices.md` are the micro-mechanism — when the build changes, re-verify every △-marked mechanic (version floors, /loop availability, approval-mode toggles) and re-derive any design that leaned on a changed one. △ markers mitigate drift between passes; this pass is what closes it.

## Output contract (review)
```
Artifact: <goal/loop setup>  ·  Rubric: rubric-control-pattern
| Dim | Type | Score | Finding | Evidence |
Gate (C1,C3): <pass/fail>   [harness_checks: <pass/fail>]
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `scripts/harness_checks.py goal` | Mechanical gate checks (bounded, measurable, no vague terms) |
| `references/rubric.md` | The `[review]` dimensions and anchors |
| `references/best-practices.md` | Design guidance / explaining a finding |
| `references/foundations.md` | When a finding turns on a shared model |
| `references/self-orchestrated-looping-agentic-systems.md` | Designing an orchestrated / multi-agent loop (host + planner/creator seats), or diagnosing a loop that spins, thrashes, or can't resume across sessions |
| [[team-or-solo-rules]] | The loop delegates work — the dispatch/composition design belongs there |

## This workspace's gates as goal conditions

Every plugin in this workspace already ships deterministic, machine-checkable gates — exactly the
proof method a `/goal` needs, and mostly unused as one today. Reach for the gate, not a fresh
condition, whenever the work already has one:

| Gate | Verifiable end-state | Suggested cap |
|---|---|---|
| `release_gate.py <root>` | exits 0 (warnings allowed) | 3 tries, then stop and report the failing check |
| `skill_lint.py <file>` | 0 FAIL findings | 3 tries (matches skill-forge's own three-strikes rule) |
| `doc_lint.py <file>` | 0 FAIL findings | 3 tries |
| `eval_check.py <suite>` | 0 FAIL findings | 3 tries |
| `handoff_check.py <block>` | H1 gate passes | 1 try — a malformed handback is a compose error, not a retry loop |
| a bug-shaped TICKET's `## Findings` section | gains a dated entry (bug-report's own dispatch contract) | 5 tries, per-investigation |
| a feature-shaped TICKET's `## Findings` section | gains a dated entry (the `/build-feature` dispatch contract) | 5 tries per build |

A cap that repeats the identical fix is thrashing, not iterating — the escalation clause (Design
step 2) fires on the *same* check failing twice, not merely on failing twice.

## Worked example: proactive bug intake

Composing `/schedule` + `/goal` + `bug-report` turns the capture-loss fix into a recurring loop
instead of a per-invocation one — the same escalation this skill's canon (`references/self-orchestrated-looping-agentic-systems.md`) describes for any delegated, unattended run:

```
/schedule <interval>: check <source> for new reports.
/goal: every report found this run has a bug-shaped TICKET with a dated Findings entry
       (bug-report's own contract) — stop after 5 tries per report, escalate on a repeat failure.
```

`<source>` and `<interval>` are the operator's call, not this skill's — name a concrete source
(an inbox, a channel, a queue) before scheduling; a source too vague to poll is a design smell the
same way an unverifiable goal condition is. Composition (which agent watches, which agent
dispatches) belongs to `team-or-solo-rules`; this skill owns only the trigger/stop shape above.

## Generator ≠ critic

A high-stakes loop design you authored gets an independent pass: dispatch the **doc-reviewer**
agent (goal conditions are in its charter) to score against `references/rubric.md` — and the
`linguistics-reviewer` agent where the wording itself is load-bearing; the maker applies the fix.

**Done** when the pattern fits the job, the condition is a verifiable end-state whose proof lands
in the transcript, the run is bounded with an escalation clause, every gate dimension (C1, C3)
scores ≥ 3, and a high-stakes design carries its independent doc-reviewer pass. **NOT done** while
the condition is process-shaped or self-graded, the run is uncapped, repeat failure spends the cap
on flat retries — or the only score the design has is its author's.
