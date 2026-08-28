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
| 957 | harness | build-957 | turn 2 | MERGED via PR #971 (harness 3.18.11) | #971 | yes |
| 958 | harness | build-958 | turn 4 | MERGED via PR #975 (harness 3.18.12) | #975 | yes |
| 959 | harness | build-959 | turn 6 | held at write-gate, accept-marker posted, opening PR (last ticket) | — | — |
| 960 | teamwork | build-960 | turn 2 | MERGED via PR #970 (teamwork 2.29.4) | #970 | yes |
| 961 | docs | build-961 | turn 1 | MERGED via PR #969 (docs 1.21.15) | #969 | yes |
| 962 | teamwork | (none) | — | CLOSED as duplicate of #965, citing PR #966 | — | n/a |
| 963 | teamwork | build-963 | turn 3 | MERGED via PR #972 (teamwork 2.29.5) | #972 | yes |

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

- 2026-08-28 turn 3: found an uncommitted edit to harness/skills/check-routing/SKILL.md sitting
  directly in the shared PRIMARY checkout (not build-957's isolated clone) while verifying
  build-960's branch. Content matches #957 exactly. Real isolation violation risk (fleet-rules
  §4/§5) — my own trial-merge git gymnastics run in this same shared directory. Paused further
  primary-checkout branch operations until build-957 confirms/relocates. #960's own verification
  was unaffected (already complete, safe) before this was found.

- 2026-08-28 turn 4: build-963 flagged a real, out-of-scope finding — stage 2b's QB3 auto-merge
  conjunct (allow-list R = {plugin.json, README.md}) predates this workspace's now-routine
  harness-overlay regen convention (G15), so any normal single-skill edit trips 4 changed files
  (plugin.json/.codex-plugin/plugin.json/HARNESS-NOTES.md/plugin.yaml) and QB3 always fails —
  every PR this run needed a human/marshal merge for exactly this reason. Worth a follow-up
  ticket updating QB3's allow-list; not filed here (out of scope, would be scope creep on this
  run) but noted for a later sweep.
- 2026-08-28 turn 4: build-963 independently observed the primary checkout in a transient
  detached-HEAD state while checking host-checkout cleanliness — correctly identified as the
  marshal's own trial-merge verification dance (tmp-verify-963/963b), already resolved by its next
  check. Confirms the trial-merge pattern is safe under concurrent build activity as long as no
  seat writes into the primary checkout directly (the one real violation this run, #957, is
  already fixed/documented above).

- 2026-08-28 turn 6: Kim gave a direct live ruling ("fold #966 into your loop") — genuine
  first-hand authorization, distinct from the earlier declined unregistered-peer relay (see the
  turn-3/turn-6 held-items entries above; that queued item is now resolved by this direct
  instruction, though the specific "is agent-ui's relayed ruling real" question was never answered
  and stays moot since Kim ruled directly here instead). Rebased PR #966 (Kim's own authored fix
  for #965) onto current main in an isolated worktree (.claude/worktrees/pr966-fold, never the
  primary checkout): resolved two README ledger conflicts, renumbered past two of my own
  already-landed slots (harness 3.18.12 taken by #975 -> 3.18.13; teamwork 2.29.5 taken by #972 ->
  2.29.6; docs 1.21.16 was already free, no change needed), fixed a self-introduced ledger-order
  bug (newest-entry-on-top violated after the first conflict resolution, caught by G14/G10 FAIL,
  fixed before push), regenerated overlays, verified all three plugins' release_gate.py clean, and
  the harness_checks.py selftest passes. Force-pushed to Kim's own branch (a rebase of an
  already-open PR, not a rewrite of shipped history). This crossed the sizing tripwire (3 plugins)
  even under direct authorization to fold it in — asked one AskUserQuestion confirm before
  merging, per this run's own NEVER list; confirmed, merged. #962 (already dropped as a
  duplicate) closed citing #965/#966 once #966 actually landed.
- 2026-08-28 turn 6: sync_main after the #966 merge surfaced one genuinely foreign-only dirty
  file (a spend-ledger row for PR #975 I'd appended but never committed before the #966 detour
  started) — quarantined to a stash automatically, verified as my own missed row (not a collision
  with anyone else's work), popped and committed. No data lost; a reminder to commit tracking
  rows before starting a multi-step detour, not after.
- 2026-08-28 turn 6: declined a cross-session handoff of PR #966 from an unregistered peer
  (agent-ui-93, agent-ui-marshal) relaying "Kim's ruling" secondhand — not a registered
  cross_repo_coordination participant in this repo's fleet.json, and the relay contained a
  factual error (misattributed PR #969's closure to #965). Queued in held-items.md for Kim to
  confirm directly rather than acting on an unverified relay; Kim's own direct instruction later
  in this same turn superseded the need for that confirmation on #966 itself specifically (the
  broader question of whether to register agent-ui as a coordination peer stays queued).

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

## Run closed 2026-08-28 — end-state met, 7 turns, well under the 40-turn/4h cap

Final verification: `gh issue list --state open` for feature/bug/task labels shows only #973/#974
(new, created 18:50-51Z mid-run by unrelated concurrent activity, never part of this run's named
scope) and the two explicitly-excluded #617 (backlog, untouched)/#609 (doing, untouched). Zero
open PRs. All 8 named tickets CLOSED.
