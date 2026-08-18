# Orchestration rubric — A8: `/batch` (partitioned parallel mutation, PR-per-unit)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here). Taxonomy amendment (2026-08-18, verified via
`claude-code-guide`, folded into #666 via #677): Claude Code ships a bundled `/batch
<instruction>` skill — research → decompose 5–30 independent units → plan-approval gate → one
subagent per unit in its own worktree (`acceptEdits`, inherited allowlist) → PR per unit. This
is the eighth archetype, not a sub-case of an existing one — an **A2×A7 hybrid lineage**:
A2's independent-verification shape (each unit's own PR gets its own review, generator ≠
critic per unit) crossed with A7's script-driven topology (a deterministic decompose→spawn→
verify pipeline, no judgment in the OUTER control flow — the judgment lives inside each
spawned unit, same split A7-R1 already states). The wiring ticket this section anticipated
(#677) landed 2026-08-18: `harness:pattern-sweeping`'s "3 — Act per disposition" Transform
sub-section now carries the scoring instance directly — cited per criterion below, never
restated.

## Architecture & intended use

Research → decompose into 5–30 independent units → a plan-APPROVAL gate (human or a named
grant, never silently skipped) → one subagent per unit, each in its OWN worktree, each running
`acceptEdits` under the inherited tool allowlist → one PR per unit. Intended use: a genuinely
partitionable body of parallel mutation where each unit stands alone (no shared-file
contention, no cross-unit ordering dependency) and needs independent verification before its
own merge — distinct from A2 (read/judge only, results return to the caller, nothing is
mutated) and A7 (one script-driven topology producing one verified result, not N independent
PRs).

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A8-R1 | Decompose-approval gate honored: the plan (unit list + scope) is put to a human or carries an explicit grant BEFORE any subagent spawns — never inferred from "the units look independent" | `harness:pattern-sweeping` "3 — Act per disposition": "`/batch` … presents the plan for approval"; same non-inference doctrine as ADR-0012's A6-R2 | mechanizable — not built (would check the invoking transcript/log for an approval step — a live confirm, or a named grant string — preceding the first subagent-spawn timestamp) |
| A8-R2 | Unit-independence proven PRE-spawn: no two units touch the same file, and no unit's correctness depends on another unit's output — checked before spawn, not discovered after | `harness:pattern-sweeping`'s own routing guidance: "`/batch` when the classified hits partition into independent units"; the same same-file-serializes default `fleet-rules` Part A §4 states for any parallel fan-out | mechanizable — not built (would diff each unit's declared target-file set pairwise for intersection; a non-empty intersection is a FAIL, named with both unit ids) |
| A8-R3 | Per-PR verification evidence: each unit's own PR carries real gate output before merge — no unit rides on a sibling unit's green | ADR-0002's per-PR gate discipline; `harness:pattern-sweeping`: "Verify runs per-PR (each `/batch` unit's own PR carries step 4's verification evidence for its slice)" | mechanizable — not built (would confirm each unit's PR has its own `release_gate.py` output attached, never a shared/copied one) |
| A8-R4 | N-PR version-slot / merge-load discipline: concurrent units touching the same plugin's `plugin.json` are hand-assigned distinct version slots before dispatch, same as any other concurrent-build fan-out | `fleet-rules` Part A §4 (version-slot rules); `dispatch-ticket`'s CLAIM-race and VALUE-race re-checks; `harness:pattern-sweeping`'s own Cautions: "N parallel PRs against ONE plugin's version slot collide … partition units by plugin" | mechanizable — not built (would confirm, for units sharing a target plugin, that each claims a DISTINCT next version number pre-dispatch — never discovered as a collision at merge time) |
| A8-R5 | `acceptEdits` pilot-scope rule: a first `/batch` run against a new target scope pilots on ONE directory before the full unit count runs unattended | `harness:pattern-sweeping`'s own Cautions, verbatim: "`/batch`'s acceptEdits mode plus its inherited allowlist is a pilot-scope rule, same as any other acceptEdits dispatch — scope the pilot before trusting the full sweep to it" | judgment |

**Owning checker for A8:** none dedicated yet — `code-checker` grades each unit's own PR
individually (A8-R3's evidence), but no seat currently grades the OUTER decompose/approval/
spawn topology as a whole; X-R3 reports this as a named gap for A8, mirroring A3's gap above.
`harness:pattern-sweeping` itself is the canon home now that #677 has landed — a future
`orchestration-audit` change may mechanize A8-R1..R4 against a real `/batch` run's own
artifacts (its plan-approval transcript, its N PRs) once that shape is observable; none of
the four is mechanized today, whatever a plausible-sounding check description might imply.
