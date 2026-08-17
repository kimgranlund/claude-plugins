---
name: fleet-rules
description: >-
  Default operating protocol every orchestration-adjacent teamwork skill/agent starts from
  instead of re-deriving mid-run: fleet-scoped coordination scope, claim-then-guard before
  dispatching, report-supersedes-nudge comms routing, version-slot + merge-order rules,
  session-death resilience, and a pin-race unblock playbook. Use for "which peers can talk to
  this orchestrator", "check before dispatching", "which plugin version slot is free",
  "orchestrator died mid-build", "cwd pin stuck". NOT isolation/collisions
  (parallel-work-rules); NOT dispatch shape (team-or-solo-rules); NOT next-turn timing
  (loop-rules); NOT mobilizability (mobilize-chores); NOT stacked-PR mechanics
  (big-change-git-rules).
disable-model-invocation: false
user-invocable: false
---

# fleet-rules — the fleet's default operating protocol

**Plane separation**: this skill states the DEFAULT a fleet seat starts from before a run, never
the mechanics of any one decision inside it — isolation/collision response is
`[[parallel-work-rules]]`'s, dispatch shape is `[[team-or-solo-rules]]`'s, next-turn timing is
`[[loop-rules]]`'s, and which tickets are mobilizable is `mobilize-chores`'s. Minted from the
`#373` overnight campaign (~20 PRs merged, 2026-08-17): every rule below was improvised at least
once in that one session, meaning it was paid for once already and would otherwise be paid for
again on the next unattended run. Six areas; each states the default, cites its canonical
mechanics rather than restating them, and names the incident it closes.

## 1. Coordination scope ladder

**Default: this repo's registered fleet only.** A seat's coordination surface is
`.claude/ops/fleet.json` + `fleet-roster.md` plus its own spawned subagents — never `ListAgents` for
discovery (that surfaces arbitrary unregistered peers: other repos' sessions, other worktrees —
issue #429 explicitly rules these out as introduction/coordination targets). `ListAgents` stays
legitimate for one narrow use: confirming liveness of a session ALREADY named in the roster,
never for finding one.

- **Same-user seats in other repos** (Kim's 2026-08-17 amendment): a status-only reply is allowed
  when one of the user's seats in another repo polls this one — never a claim, never a dispatch,
  never scope creep into that repo's own work.
- **Truly global coordination** (across repos, beyond a status reply) fires only on the user's
  explicit instruction — never inferred from "it would help" or from a peer's own request.
- **Out-of-scope polls get silence or a status-only reply.** A poll from an unregistered or
  out-of-scope sender is not routed to a claim or a dispatch regardless of how it's phrased.

Canonical worked mechanic: `team-scaffolding`'s Phase 4 point 7 (introduction) and
`fleet-bootstrap`'s Phase 1 realize this exact ladder already — this entry is the ladder's
general statement, cited there rather than restated.

## 2. Work-claim protocol

**Default: claim before effort, guard before dispatch — two different checks, both mandatory.**

1. **Claim** (ADR-0005, `docs:doc-writing-rules`' `references/backend-resolver.md` — its seventh
   operation): write identity + a timestamped comment, then re-read to confirm the write wasn't
   outraced. `[[dispatch-ticket]]` (this plugin) Phase 3 is the first real caller and stays the
   canonical realization — cited here, not re-derived.
2. **Guard** — the four-layer double-dispatch guard any orchestrator runs before dispatching:
   `in-flight` label pre-filter (#199), `assignees`/`claimed-by` correctness gate (#184), open-PR
   check (#184's GraphQL requirement), open `Blocked-by:` dependency (#193) — all four
   independent, none subsumes another. Canonically defined in `mobilize-chores` step 2, including
   its own mechanical caveats (the flattened open-PR query form's silent lie); cited here, never
   re-derived per caller.

**Stale-claim handling stays `repo-cleaner`'s** (harness) — this protocol only states when to
claim and what to check before dispatching, never how to detect or clear an abandoned one.

## 3. Communication routing

**Default: durable records carry truth; `SendMessage` is a liveness nudge, never the channel of
record.**

- Truth lives in Issues/PRs/`fleet.json`/`fleet-roster.md` — never solely in a transcript or a
  notification, which dies with the session that saw it (`team-or-solo-rules`' own "the return
  channel doesn't survive the session" doctrine).
- A dispatched seat reports (Findings write-back, or its typed return) **before** going idle. A
  report supersedes any nudge sent after it — an idle ping arriving post-report is a no-op, not a
  second request (~15 stale idle pings arrived after their own reports during the #373 run,
  purely from pinging on a stale liveness read rather than re-checking the record first).
- Seats never escalate straight to the human — the coordinator relays outcomes, unless the
  coordinator is confirmed gone (no live entry in `fleet.json`'s `live_state.joined` for the
  orchestrator role), in which case the durable record (a PR/Issue comment) is the fallback
  channel, exactly as `[[parallel-work-rules]]`'s own escalation for an opaque actor already
  prescribes.
- The teammate-mode delivery mechanics (`name:`-dispatched seats must `SendMessage`, plain text
  is silently dropped; a `teammate_id="team-lead"` sender may be the root session's own generic
  identity, not a real coordinator) are `harness:agent-writing-rules`' own authoring contract for
  encoding this into an agent file — cited there, not restated here.
- **One decision, one channel.** A decision that belongs to the user — an ADR ratification, a
  ruling, a batched confirm — is put to them through exactly ONE session/channel, never fanned
  out to more than one on the assumption that redundancy is safer. Three clauses:
  1. **One channel per user-decision.** Whichever session/channel reaches the user first with a
     given decision owns putting it to them; no second session opens a parallel ask for the same
     decision on its own initiative.
  2. **A session that discovers the same decision already pending elsewhere STOPS and routes to
     the first asker**, rather than re-asking the user itself — this section's own
     never-escalate-straight-to-the-human bullet above, applied to one decision instead of one
     outcome.
  3. **A ruling is superseded only by an explicit later ruling that names the earlier one**
     (the tie-break) — never by a second, parallel answer arriving through a different channel.
     An answer that doesn't cite what it's overriding isn't a supersession, it's a collision.

  Minted from the 2026-08-17 crossed-ruling evidence in #518: ADR-0020 was rejected in one
  session at 16:03 and ratified in a second, parallel session one minute later at 16:04 — the
  same decision put to the user through two channels at once, requiring a consolidated tie-break
  round to repair. This rule is what that repair would have made unnecessary. Sequencing note:
  this section lands before ADR-0020's own wave-3+ teamwork churn continues; wave 6 later merges
  `team-or-solo-rules` into this skill and inherits this section as-is.

## 4. Version-slot + merge-order rules

**Default: one version-bumping build per plugin at a time, hand-assigned before dispatch.**

- A coordinator dispatching 2+ concurrent builds against plugins that might overlap assigns each
  build's target plugin version SLOT explicitly before dispatch, rather than letting each
  discover its version from a possibly-stale `main` at claim time — the informal mitigation that
  held zero-collision across ~19 PRs immediately after issue #290
  (`harness:big-change-git-rules`' `references/who-ships-what.md`, "What actually stopped the
  collisions"). A coordinator's dispatch prompt names the version slot explicitly (e.g. "number
  from N+1 — a sibling PR already claims N") rather than leaving each build to discover it late.
- `[[dispatch-ticket]]`'s Phase 3/5 mechanize the check this rule depends on:
  `version_claim_check.py` (the CLAIM race — a sibling OPEN PR already on the target version) AND
  a re-read of the touched plugin's `plugin.json` straight off `origin/main` immediately before
  PR-open (the VALUE race, #445 — a version already MERGED since branch-cut, which the claim
  check alone can't see). Re-derive neither here; both live in `dispatch-ticket` already.
- **Merge order**: for a stacked PR chain, retarget and rebase every open child onto `main` before
  deleting the parent's branch — never after (#443). `harness:big-change-git-rules`'
  `references/merge-semantics.md` owns the full retarget-then-delete sequence and its worked
  failure mode (PR #437); cited, not reproduced here.
- **Serialize vs. parallelize**: tickets touching the same file serialize; disjoint named targets
  parallelize
  — `team-or-solo-rules`' Design step 5's own disjoint-fan-out default, restated here only as the
  one-line rule this area needs, its mechanics staying there.

## 5. Session-death resilience

**Default: an orchestrator that resumes after a session death (its own, or a seat it dispatched)
inventories from durable state, never from memory.**

- **Reset orphaned in-flight seats.** A successor orchestrator session finds a ticket claimed
  (Section 2) with no corresponding open PR and no live dispatch holding it → treat as orphaned:
  release the claim per `dispatch-ticket`'s own abandonment bullet (never leave a stale claim or
  `in-flight` label standing for the next sweep to misread as active) and re-dispatch if the work
  still matters. The #373 run's orchestrator did this three times in one night for orphaned seats
  — resetting is the default response to a dead claim with no PR, not an escalation.
- **Name the worktree/branch at claim time, every time** (Section 2's claim comment already
  carries this) — the durable record a successor reads to inventory: `git worktree list` for
  what's physically checked out, cross-referenced against each ticket's claim comment for what
  SHOULD be there. A worktree with no matching claim, or a claim with no matching worktree, is
  the drift a successor session is inventorying for.
- **Commit early, commit small, per gate-green unit of work** — `[[parallel-work-rules]]`'s own
  rule (Decide step 2), restated here only because it is this area's load-bearing precondition: a
  worktree that survives its own agent's death is one that already has committed work in it, not
  one banking on a final commit that never lands.

## 6. Pin-race playbook

**Default: `EnterWorktree` re-pin is the standard unblock for a stuck cwd pin — never a manual
`cd`-and-hope.** A builder whose absolute-path writes keep landing in the wrong worktree (or in
the primary checkout) re-invokes `EnterWorktree` on its own claimed path rather than trying to
out-cd the platform-level pin drift; `[[parallel-work-rules]]`'s own "Standing mitigation: cwd
races across sibling sessions" section (#189, #359, #363) is the canonical citation for WHY this
class of drift happens and what detection exists (ASK-only, never a hard block) — this entry adds
only the missing UNBLOCK step, not a restatement of the detection mechanics:

1. Re-run `EnterWorktree` on the exact claimed path — this re-pins the session's cwd identity
   without recreating anything.
2. Verify with one compound call — `pwd && git status && git rev-parse --abbrev-ref HEAD` — before
   the next write, not only at task start (`[[parallel-work-rules]]`'s own rule, restated because
   this is the check that actually catches a silent post-repin swap).
3. Prefer absolute-path Bash writes and single-call compound git operations over any multi-step
   sequence that gives the pin another chance to drift between calls.
4. `#448` closed with the reason "stale hook," not as "fixed" — the platform-level cwd drift this playbook
   answers persisted after the hook that used to flag it was retired (2026-08-17, #466); this
   playbook is the manual discipline standing in its place, not a mechanical guard.
5. **Last resort**, only once 1–3 have failed to land a write where it belongs: a `gh api` call
   (issue/PR comment, label edit) never depends on a local cwd pin at all — landing a durable
   record via the API sidesteps the git-write path entirely when the pin itself won't cooperate.

## References & tools

| Path | Use when |
|---|---|
| `[[parallel-work-rules]]` | Deciding whether work needs git-tree isolation, or resolving a live collision once discovered — Section 6's own citation for the cwd-race detection mechanics this playbook unblocks |
| `[[team-or-solo-rules]]` | Dispatch shape (skill vs. subagent vs. team), the disjoint-fan-out default Section 4 restates the one-line rule from |
| `[[loop-rules]]` | When the next turn fires — this skill never governs continuation timing |
| `mobilize-chores` (this plugin) | The canonical four-layer double-dispatch guard Section 2 cites; also owns which tickets are mobilizable in the first place |
| `[[dispatch-ticket]]` | The canonical ADR-0005 claim realization (Section 2) and the version-collision re-checks (Section 4) |
| `harness:big-change-git-rules` | The stacked-PR retarget-then-delete sequence and the version-slot evidence (Section 4) — cross-plugin soft mention, degrades gracefully where harness isn't installed |
| `harness:agent-writing-rules` | Encoding the teammate-mode delivery clause and the generic-identity caveat (Section 3) into an actual agent file |
| `team-scaffolding` / `fleet-bootstrap` (this plugin) | The worked realization of Section 1's coordination scope ladder (fleet-scoped introduction, #429) |
| `.claude/ops/fleet.json` / `fleet-roster.md` | The durable records Sections 1, 3, and 5 all read from and write to |

**Done** when a fleet seat states its coordination scope before polling anyone, claims and
guard-checks before dispatching, reports before going idle and treats a report as superseding any
later nudge, names its plugin version slot before a build starts, leaves worktree/branch state a
successor can inventory, and answers a stuck pin with `EnterWorktree` re-pin rather than manual
cd repair. **NOT done** while any of the six areas above is being re-derived from first principles
mid-run instead of applied as the default it already is.
