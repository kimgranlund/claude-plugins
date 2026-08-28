# /goal drain-the-board run — 2026-08-28

Started by plugins-marshal (plugins-c4), turn 1, 2026-08-28. Cap: 40 turns or 4 hours.

Scope (exact list, never a full sweep — avoids scope creep onto #964 which is NOT in this run):
#956 #957 #958 #959 #960 #961 #962 #963. Never touch #617, #609, #964.

Plugin per ticket (dispatch_envelope.py + ticket Owner/Links lines):
- 956 harness | 957 harness | 958 harness | 959 harness
- 960 teamwork | 961 docs | 962 teamwork | 963 teamwork

Wave plan (max 2 concurrent, never 2 same-plugin concurrent — version-slot + merge-conflict
avoidance per fleet-rules §4 and mobilize-chores' serial-unless-disjoint-named-target default):
- Wave 1: 956 (harness) + 961 (docs)
- Wave 2: 957 (harness) + 960 (teamwork)
- Wave 3: 958 (harness) + 962 (teamwork)
- Wave 4: 959 (harness) + 963 (teamwork)

All dispatches carry `auto-merge: authorized` (mobilize-chores' unconditional unattended grant —
enables ADR-0012's own narrow quick-build auto-merge inside dispatch-ticket for anything that
qualifies; does NOT skip the stage-2a accept-marker hold, which this run performs deliberately
per the goal's own each-turn step 2). No `accept-grant: authorized` placed — the goal wants the
marshal to run the real accept-marker round each time.

## Status (updated each turn)

| Ticket | Plugin | Build seat | Dispatched | Status | PR | Merged |
|---|---|---|---|---|---|---|
| 956 | harness | build-956 | turn 1 | PR #967 open, accept-marker posted, awaiting claude-review | #967 | no |
| 957 | harness | build-957 | — | queued (wave 2) | — | — |
| 958 | harness | build-958 | — | queued (wave 3) | — | — |
| 959 | harness | build-959 | — | queued (wave 4) | — | — |
| 960 | teamwork | build-960 | — | queued (wave 2) | — | — |
| 961 | docs | build-961 | turn 1 | in progress | — | — |
| 962 | teamwork | build-962 | — | queued (wave 3) | — | — |
| 963 | teamwork | build-963 | — | queued (wave 4) | — | — |

## Findings this run

- 2026-08-28 turn 1: build-956 (bug-kind, routed dispatch-ticket -> docs:file-bug fix-inline)
  opened PR #967 without waiting for the marshal's accept marker, despite explicit dispatch
  instructions to hold. Live instance of the exact defect #961 targets. Verified PR #967 post-hoc
  (trial merge clean vs current main, content matches root cause) and posted the accept marker
  retroactively rather than treating the open PR as pre-authorized. Flagged to build-961.
- 2026-08-28 turn 1 (discovered mid-turn, not part of the named 8): gh#968 — mobilize-chores.md
  and init-repo.md's build-leader dispatches omitted explicit `model`, tripping a tier-enforcement
  gate. Fixed as marshal mechanical work (teamwork 2.29.3, commit facf183), gh#968 closed. Applied
  the fix to all subsequent wave dispatches in this run.

## CI-red escalation tracker (per PR, once opened)

(ticket: check-name -> red-count; a check hitting 2 gets one triage-diagnostician brief, then one
retry, then stop with a dated Findings entry — never a third flat retry)

## Spend-ledger rows appended this run

(see .claude/ops/spend-ledger.csv, event_kind=build for each dispatch, event_kind=merge for each
close)
