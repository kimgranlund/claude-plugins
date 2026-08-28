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
| 956 | harness | build-956 | turn 1 | MERGED via PR #967 | #967 | yes |
| 957 | harness | build-957 | turn 2 | dispatched, slot 3.18.11 | — | — |
| 958 | harness | build-958 | — | queued (wave 3) | — | — |
| 959 | harness | build-959 | — | queued (wave 4) | — | — |
| 960 | teamwork | build-960 | turn 2 | dispatched, slot 2.29.4 | — | — |
| 961 | docs | build-961 | turn 1 | MERGED via PR #969 (docs 1.21.15) | #969 | yes |
| 962 | teamwork | (none) | — | DROPPED — duplicate of #965/PR #966 (live human PR) | — | — |
| 963 | teamwork | build-963 | — | queued (wave 4) | — | — |

- 2026-08-28 turn 2: PR #966 (opened directly by kimgranlund, live-lane, NOT a build-seat
  dispatch — outside the standing merge grant, never touched by this run) fixes harness_checks.py
  across docs/harness/teamwork for issue #965, which is a byte-for-byte duplicate of #962 (same
  repro, same root cause: OSError File name too long on a long inline goal arg). #966 is now
  STALE on harness (3.18.9->3.18.10, but main is already at 3.18.10 via #967) and teamwork
  (2.29.2->2.29.3, main already at 2.29.3 via gh#968) — the human's own PR to rebase when they
  merge it, not mine to touch. Decision: #962 dropped from this run's dispatch queue as a
  duplicate; will close it citing #965/#966 once #966 merges (or note it now if #966 stalls).
  957/960 dispatched anyway with FRESH hand-assigned slots off current main (harness 3.18.11,
  teamwork 2.29.4) per fleet-rules' hot-shared-file/rebase-next doctrine — not blocking on
  another actor's PR.

- 2026-08-28 turn 2: build-956 flagged its own stranded-fork routing (its Skill-tool invocation of
  docs:file-bug delivered its completion to the marshal instead of back to build-956 itself) as a
  real instance of the no-nested-wait failure class dispatch-ticket already documents
  (#257/#282/#269/#280) — and structurally the same shape as #959 (already queued, wave 4:
  check-routing's judge-verdict stranding). Corroborating evidence, not a new ticket — noted here
  for #959's build to pick up if useful; not filed separately (would be scope creep on this run).
- 2026-08-28 turn 2: build-961 independently re-ran the mandatory version-collision check before
  PR-open, caught the real docs 1.21.14 collision against PR #966 itself (predicted in this file's
  turn-2 entry above), and self-corrected to 1.21.15 with a mechanical-only re-commit (no new
  checker pass owed, content unchanged). Marshal verified the new SHA (trial merge clean) and
  posted a fresh accept marker superseding the stale one. Textbook execution of the SHA-staleness
  rule on both sides.

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
