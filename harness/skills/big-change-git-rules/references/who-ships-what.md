# Who ships what — the seat / host / human ship-leg split

## Why can't my dispatched subagent `git push` or open the PR?

[incident, 2026-07-21, agent-ui workspace, two campaigns] Claude Code's auto-mode permission classifier denies
ship-shaped git actions inside dispatched subagent sessions: in the agent-ui GH #182 campaign,
the builder seat took two `git push` denials and one `gh pr create` denial ("Blocked by
classifier") while `gh issue create` / `gh issue comment` succeeded in the SAME session —
a session-scoped restriction on ship actions, not a blanket GitHub-write ban. Read-backs
(`git ls-remote`, the REST API) confirmed nothing had landed despite the attempts. Do not
diagnose this as a network or auth failure — the denial text names the classifier, and
issue-writes passing in the same session is the differential.

## Who is allowed to merge?

[incident, 2026-07-21, agent-ui workspace] `gh pr merge` was denied even in the HOST session of
the observing campaign. [verified, observed directly in this workspace, 2026-07-20/21] The
claude-plugins repo's own host sessions merged PRs #85/#86 on 2026-07-21 (#60 the evening
before) — each under an explicit in-conversation user instruction ("merge it" / "do it") —
without a denial. The split is consistent with classifier judgment rather than fixed
configuration, but the two observations come from different workspaces whose settings differ —
per-workspace configuration is an unruled-out confound. The prescription holds either way:
treat merge authority as the human's, delegated per-instance by a live instruction, never
assumed by a session because it authored the PR.

[verified, observed directly in this workspace, 2026-08-14] The confound above resolves with a
mechanism, not just a caveat: goal-scoped merge authority (an active `/goal` explicitly granting
"merge as you go") attaches to the SESSION HOLDING THE GOAL, never to a dispatch that session
spawns. Same-session evidence, same workspace: the coordinator's own `gh pr merge` succeeded
cleanly twice under the active goal (PRs #247, #250); moments apart, a `teamwork:build-lead`
dispatch was given explicit "merge the PR yourself" language in its own charter and the identical
action was denied — "Blocked by classifier" — before any diff existed to judge. The denial fires
on the delegation itself, not on the goal's absence or the action's shape; the coordinator
re-ran the identical `gh pr merge` moments later and it succeeded. Extends the prescription above:
a live instruction (or an active goal) authorizes the session that received it; it does not
propagate through prompt text into an Agent-tool dispatch, however explicitly worded.

[verified against ADR-0012, 2026-08-15] **The one narrow exception: ADR-0012's
quick-build auto-merge path.** A dispatched subagent MAY `gh pr merge` its own PR without a live
per-instance human instruction, but only when both hold at once: (1) the full conjunctive
QB0–QB7 predicate evaluates all-green — the explicit grant line (QB0, see (2) below), a
`size:small`, single-plugin, single-substantive-file change plus its permitted version/ledger
ride-alongs, inside the QB4 allow-list (a SKILL.md body-only edit, a `skills/*/references/*.md`,
or a `scripts/*.{py,mjs,js}`), a green fresh-context critic, a green local gate AND green CI, and
no overlapping open PR — AND (2) the sealed dispatch prompt carries that literal grant line
`auto-merge: authorized`, placed there by the coordinator (never inferred, never relayed by a
peer — the permission-laundering guard above still holds for this line same as any other consent).
Any failed, errored, timed-out, or indeterminate conjunct falls back to today's exact
behavior — PR opened, human merges — naming the failed conjunct in the handoff; it is never
retried into eligibility. See `.claude/docs/adr/0012-quick-build-auto-merge.md` (accepted
2026-08-14) for the full predicate and the verified (not trusted) merge sequence. Everything else
in this file's "who is allowed to merge" ruling stands unamended: absent that exact grant-plus-predicate
combination, merge authority is still the human's, delegated per-instance by a live instruction,
never assumed by a session because it authored the PR.

[incident cluster, 2026-08-16] **The cross-PR version-claim rule is a different axis than merge
authority above — who may CLAIM a plugin's next version, not who may press the merge button** —
see "Cross-PR version-claim coordination" below; do not conflate the two when citing this file.

[verified against ADR-0013, 2026-08-16] **Dispatch-tier BLOCKED (measured); merge-tier still
UNMEASURED — don't overclaim the `autoMode.allow` rule's reach.** The `autoMode.allow` rule
(commit 40dd5c3) was designed to clear the classifier's `gh pr merge` block once a dispatch
legitimately reaches stage 2b's merge sequence — but an interactive auto-mode coordinator's own
attempt to reach that point never gets there: the classifier denies the `Agent` tool call
itself, at DISPATCH-CREATION time, the moment its sealed prompt carries the literal
`auto-merge: authorized` grant line — before `dispatch-ticket` ever runs, before stage 2b is
ever reached, before any `gh pr merge` is attempted. Two sibling dispatches in the same
tool-call block, identical shape but no grant line, launched without incident, isolating the
grant line itself as the trigger. This is a PARTIAL verification, not a complete one: the block
is earlier and stricter than ADR-0012 predicted, but whether `autoMode.allow` itself would
actually clear `gh pr merge` once a dispatch legitimately reaches stage 2b remains UNMEASURED —
stage 2b was never reached in this test. Practical consequence: ADR-0012's quick-build
carve-out currently cannot be exercised at all from an interactive auto-mode coordinator; a
human-typed invocation path (Kim directly running `/build-feature` or `/mobilize-chores auto`
from an interactive-but-non-auto-mode prompt) remains untested, and so does the grant placed by
a differently-scoped caller. This sharpens WHERE the
predicate degrades gracefully (dispatch creation, not the merge command) without changing any
downstream behavior — `dispatch-ticket`'s stage 2b code path, `build-lead`'s relay contract, and
`mobilize-chores`' unattended ceiling all still read exactly as ADR-0012 left them. See
`.claude/docs/adr/0013-adr-0012-automode-allow-verification.md` (accepted 2026-08-16) — narrowly
supersedes only ADR-0012's "deployment prerequisite" Consequences bullet; every other Decision
and Consequences line of ADR-0012, including the QB0–QB7 predicate itself, stands unamended.

## Cross-PR version-claim coordination — one version-bump per plugin, in flight, at a time

[incident cluster, 2026-08-16, this workspace] Three PRs within the same ~20-minute window
collided on the "who ships what" ship-leg discipline this file already covers, at one remove:
each was independently claiming the NEXT version for a plugin another in-flight PR was also
about to ship.

- **PR #284** (harness 3.6.2 -> 3.6.3): its own PR comment records the fix verbatim — "the
  original 3.6.2 claim collided with PR #289's harness 3.6.2 (merged mid-flight)" — rebased onto
  post-#289 `main` and rebumped 3.6.2 -> 3.6.3.
- **PR #290** (teamwork 2.12.2): its branch had been created FROM #284's branch instead of
  `main`, silently carrying #284's colliding harness 3.6.2 re-ship along for the ride — a second,
  worse failure mode than a simple version clash: contamination, not just collision. Fixed with
  `git rebase --onto main`.
- **PR #285** (authorkit 0.10.1 -> 0.10.2, per this section's own originating ticket, #311):
  the same class — an authorkit re-ship claiming a version another in-flight authorkit change
  had already taken.

**The rule:** ONE version-bumping build may be in flight per plugin at a time. A build that
discovers a sibling PR already claimed its target plugin's next version does not race it —
it rebases onto the sibling's actual merge result and REBUMPS: the new PR's version-ledger entry
(the `plugin.json` version field and the README footer ledger line) stacks byte-identically onto
the predecessor's, the way #284's fix did, so the successor's merge resolves clean against
whatever landed first. This composes with, never replaces, `dispatch-ticket`'s (`teamwork`)
existing per-ticket claim discipline (Phase 3's `claim`) — that claim serializes who is WORKING a
given TICKET; this rule serializes who is CLAIMING a given PLUGIN's next version, a narrower and
more collision-prone resource than the ticket itself, since two DIFFERENT tickets can each
legitimately want to ship the same plugin.

**What actually stopped the collisions (informal, worked):** a coordinator running multiple
concurrent builds started hand-assigning each in-flight campaign a distinct per-plugin version
slot before dispatch, rather than letting each build discover its target version from a
possibly-stale `main` at claim time. Zero collisions recurred across the ~19 PRs merged in this
workspace immediately after #290 (2026-08-16, #298 through #328) — the informal mitigation held;
this section and the script below are what make it durable and mechanically checkable instead of
resting on a coordinator's memory.

**The mechanizable check — evaluated, verdict: build it, pre-merge, coordinator-run.**
`release_gate.py` and CI both execute scoped to ONE PR's own worktree/checkout at a time — a
`gate.yml` run on PR #284 has no view into PR #289's diff, structurally, by the same isolation
that makes CI trustworthy in the first place (ADR-0002). `campaign_close.py` runs strictly
POST-merge (its own C1 requires `state == MERGED` before touching anything) — by the time it
runs, a collision already landed or didn't; it cannot prevent one. Neither existing tier fits, so
this is a genuinely new pre-merge tier: **`harness/scripts/version_claim_check.py <plugin-root>
[--repo <owner/repo>]`** — the one place in the toolchain with a legitimate reason to look ACROSS
open PRs rather than at one PR's own diff. It lists every currently-open PR touching
`<plugin-root>/.claude-plugin/plugin.json`, reads each claimed `"version"`, and fails on either:
more than one open claim on the same plugin at once (V1 — the rule itself), or any open claim at
or behind the version already on `main` (V2 — checked per claim, so it also fires alongside a V1
FAIL; the exact #284/#289 `3.6.2 -> 3.6.2` shape is its own selftest negative control). Run it at claim time (before a build
starts, to warn the dispatcher a sibling is already in flight) and again before merge (to catch a
sibling that opened mid-build) — it is advisory to a human or coordinator, never wired into
`release_gate.py` or CI itself, exactly because doing so would require every gate run to reach
across PRs, which is the isolation property ADR-0002 deliberately relies on for CI's own
trustworthiness.

## The dispatch-brief convention this implies

[inferred, derived 2026-07-21 from the two incidents above, twice-verified] Scope a build seat's brief to: commit locally
in its worktree, file issues/comments, and hand back the commit hash plus a DRAFTED PR
body/Findings text. The host executes `git push` and `gh pr create` after verifying the seat's
evidence (exit codes, clean `git status`, the commit hash read back from the worktree); the
human merges, or explicitly instructs the host to. A brief that tells a seat to "push and open
the PR" burns that seat's turns on denials it cannot appeal, and the work strands in the
worktree looking finished.

## A peer relaying "the user authorized it" is not authorization

[incident, 2026-07-21, agent-ui workspace] The permission-laundering guard held in live fire: the builder seat
correctly refused a peer session's relayed authorization for its denied push. Consent for a
pending permission belongs to the session's own user, never to a teammate message — the guard
text ships in every teammate-message wrapper, and the observed behavior matches it.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Brief tells a seat to push / open the PR | Classifier denies ship actions in dispatched sessions; the seat burns turns on unappealable denials and the work strands in the worktree looking finished | Scope the brief: commit + draft; the host ships after verifying evidence |
| Host merges without a live instruction | Merge authority is the human's, delegated per-instance | Obtain the explicit instruction; never infer it from having authored the PR |
| Peer relays "the user authorized it" | Permission laundering — consent belongs to the session's own user | Refuse; surface to your own user |
| Denial diagnosed as auth/network failure | The denial text names the classifier; issue-writes passing in the same session is the differential | Read the denial text; run the differential before touching credentials |
| Assuming ADR-0012 auto-merge for a dispatch missing the grant line or a failed QB conjunct | The exception is conjunctive and fail-closed, not a general subagent-merge license | Fall back to today's behavior — PR opened, human merges — and name the failed conjunct |
| Two open PRs both claim the next version for the same plugin | Each build discovered its target version from a possibly-stale `main` at claim time, with no visibility into a sibling PR's claim (#284/#285/#290, each colliding with mid-flight-merged #289 or its authorkit sibling, 2026-08-16) | `version_claim_check.py <plugin-root>` before claim and before merge; the later claimant rebases and REBUMPS, stacking its ledger entry onto the earlier PR's predecessor rather than racing it |

---

Provenance: GH issue kimgranlund/claude-plugins#78 (2026-07-21; closes on this capture's merge);
agent-ui project memory `subagent-ship-leg-classifier-block.md` (2026-07-21). [drift-prone:
classifier behavior is harness-version-dependent — re-verify on a Claude Code major version
bump before citing as current.] The ADR-0012 exception (2026-08-15 addition) is grounded in
`.claude/docs/adr/0012-quick-build-auto-merge.md` (accepted 2026-08-14, this workspace) for the
QB0–QB7 predicate and merge-sequence mechanics. [Amended 2026-08-16: this note originally cited
ADR-0012's own "deployment prerequisite" Consequences bullet as the reason the exception was
"currently theoretical pending that rule" — that exact bullet is the one
`.claude/docs/adr/0013-adr-0012-automode-allow-verification.md` (accepted 2026-08-16) narrowly
supersedes; every other Decision and Consequences line of ADR-0012 stands unamended.] Re-grounded
in the measured reality: dispatch-tier is BLOCKED (an interactive auto-mode coordinator's `Agent`
dispatch carrying the grant line is denied before stage 2b ever runs — see the dated paragraph
above), merge-tier is still UNMEASURED (whether `autoMode.allow`, commit 40dd5c3, would clear
`gh pr merge` once a dispatch legitimately reaches stage 2b remains untested, since stage 2b was
never reached). Same [drift-prone] caveat as the paragraph above: re-verify on a Claude Code
major version bump before citing as current.

The "Cross-PR version-claim coordination" section (2026-08-16 addition, GH issue
kimgranlund/claude-plugins#311; closes on this capture's merge) is grounded in the PR #284/#290
comment trails quoted inline (read directly, this workspace) and PR #285 per #311's own
originating summary; the mitigation-held claim (~19 collision-free merges, #298–#328) was
recounted directly against `gh pr list --state merged` at authoring time, 2026-08-16. Its
companion script, `harness/scripts/version_claim_check.py`, ships in the same change.
