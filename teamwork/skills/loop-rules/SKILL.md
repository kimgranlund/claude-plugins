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
  skill/agent wiring, dispatch, frontmatter (fleet-rules); NOT running or
  watching an already-written /goal, only designing or reviewing the
  pattern; this skill owns only when the next turn fires.
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
- An autonomous loop's budget is a ledger row too — each firing (build or sweep) it drives is priced in `.claude/ops/spend-ledger.csv` via `authorkit:spend-audit`'s close-out convention, and idr-0010 (LOCKED, `.claude/docs/idr/idr-0010-estate-economy.md`; cited, never restated) binds loop design: a turn/time cap set with no pricing on what it repeatedly fires is unaccountable by the same doctrine every other recurring seat answers to.

## Design
1. Pick the pattern: finish-line the agent can prove → `/goal`; recurring external check → `/loop`; enforced "until clean" → Stop hook + check; collaboration → team.
2. Write the `/goal` as a measurable end-state with the proof method named; make the proof land in the transcript; add a turn/time cap, a scope guard, and an escalation clause (the same check failing twice → triage, below — not a flat retry).
3. Self-score (below); fix until every gate dimension (C1, C3) ≥ 3.

## Escalation: triage-diagnostician + gate-repair privilege

The escalation clause (Design step 2) doesn't just stop at N=2 identical failures — it inserts one
structured diagnosis before the run halts, adapted from disler/fusion-harness's auto-validation
loop (`SYSTEM_PROMPT_TRIAGE.md`; `cmd-build.ts`'s gateBefore byte-diff + `VALIDATOR_TOOLS` →
`READONLY_TOOLS` flip):

1. **Triage diagnostician.** On the SAME check's second consecutive failure, dispatch a
   fresh-context checker-class seat (sonnet — a diagnosis is judgment, not building), starting
   READ-ONLY, to inspect the real project state directly, never the builder's claims about it, and
   compare what the gate demands against what was actually produced. It returns one bounded brief:
   **Diagnosis** (root cause) / **Do-exactly-this** (ordered steps) / **Do-NOT** (what the builder
   keeps doing wrong). The brief is advisory context handed back to the builder for its next try —
   the gate's own output stays the source of truth, never the diagnostician's opinion.
2. **Gate-repair privilege — exactly once per run, and only for a defective gate.** If and only if
   the diagnosis is that the gate itself is broken (impossible to satisfy as written, or demands
   something the original request never asked for), the diagnostician's tool allowlist is widened
   from read-only to write access scoped to the gate file alone (mirroring fusion-harness's
   `VALIDATOR_TOOLS` grant), and it may repair the gate. Spend the privilege deliberately:
   byte-diff the gate file before/after to detect that a repair was made, preserve the pre-repair
   version as an audit copy, then drop the seat's tool allowlist straight back to read-only the
   moment the one repair lands (mirroring fusion-harness's `VALIDATOR_TOOLS`→`READONLY_TOOLS`
   flip) — the widened grant never survives past that single write. Re-run the repaired gate
   immediately without charging the builder one of its capped tries. **Never-weaken rule:** every
   check that maps to a real requirement stays at full strength — this privilege fixes the gate's
   own bug, it never moves the goalposts to make a correct gate easier to pass. This is a
   prompt-level discipline in fusion-harness (no separate mechanical enforcement there beyond the
   byte-diff), and the canon states that honestly rather than implying a tool-level guarantee this
   stack doesn't yet have.

A second identical failure AFTER the diagnosis (same check, same root cause) escalates per the
existing rule — stop and report, not a second triage pass. This is the concrete `diagnose →
route the fix` mechanism for a single-check failure; `references/self-orchestrated-looping-agentic-systems.md`'s
credit-assignment model (execution/spec/plan routing) covers the broader multi-seat case where
the fix isn't a same-gate repair — read that reference when the diagnosis points past the gate
itself.

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
| [[fleet-rules]] | The loop delegates work — the dispatch/composition design belongs there |

## This workspace's gates as goal conditions

Every plugin in this workspace already ships deterministic, machine-checkable gates — exactly the
proof method a `/goal` needs, and mostly unused as one today. Reach for the gate, not a fresh
condition, whenever the work already has one:

| Gate | Verifiable end-state | Suggested cap |
|---|---|---|
| `release_gate.py <root>` | exits 0 (warnings allowed) | 3 tries, then stop and report the failing check |
| `skill_lint.py <file>` | 0 FAIL findings | 3 tries (matches make-skill's own three-strikes rule) |
| `doc_lint.py <file>` | 0 FAIL findings | 3 tries |
| `eval_check.py <suite>` | 0 FAIL findings | 3 tries |
| `handoff_check.py <block>` | H1 gate passes | 1 try — a malformed handback is a compose error, not a retry loop |
| a bug-shaped TICKET's `## Findings` section | gains a dated entry (file-bug's own dispatch contract) | 5 tries, per-investigation |
| a feature-shaped TICKET's `## Findings` section | gains a dated entry (the `/build-feature` dispatch contract) | 5 tries per build |

A cap that repeats the identical fix is thrashing, not iterating — the escalation clause (Design
step 2) fires on the *same* check failing twice, not merely on failing twice, and that firing is
the triage-diagnostician's cue (above), not an immediate halt.

## Worked example: proactive bug intake

Composing `/schedule` + `/goal` + `file-bug` turns the capture-loss fix into a recurring loop
instead of a per-invocation one — the same escalation this skill's canon (`references/self-orchestrated-looping-agentic-systems.md`) describes for any delegated, unattended run:

```
/schedule <interval>: check <source> for new reports.
/goal: every report found this run has a bug-shaped TICKET with a dated Findings entry
       (file-bug's own contract) — stop after 5 tries per report, escalate on a repeat failure.
```

`<source>` and `<interval>` are the operator's call, not this skill's — name a concrete source
(an inbox, a channel, a queue) before scheduling; a source too vague to poll is a design smell the
same way an unverifiable goal condition is. Composition (which agent watches, which agent
dispatches) belongs to `fleet-rules`; this skill owns only the trigger/stop shape above.

## Generator ≠ critic

A high-stakes loop design you authored gets an independent pass: dispatch the **doc-checker**
agent (goal conditions are in its charter) to score against `references/rubric.md` — and the
`wording-checker` agent where the wording itself is load-bearing; the maker applies the fix.

**Done** when the pattern fits the job, the condition is a verifiable end-state whose proof lands
in the transcript, the run is bounded with an escalation clause, every gate dimension (C1, C3)
scores ≥ 3, and a high-stakes design carries its independent doc-checker pass. **NOT done** while
the condition is process-shaped or self-graded, the run is uncapped, repeat failure spends the cap
on flat retries — or the only score the design has is its author's.
