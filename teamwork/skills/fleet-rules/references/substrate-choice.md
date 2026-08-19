# Substrate choice — fleet canon vs. native `agent-teams`, and the re-evaluation shape

> `fleet-rules` domain reference (Part A, Sections 1/5). Harvested from ADR-0023 (accepted
> 2026-08-18) — cited throughout, never restated in full; read the ADR itself for the Context/
> Alternatives-considered detail this file only summarizes the ruling and pattern of. Adjacent to
> `references/organizing-axis.md` (#671/PR #690's four agent-classes canon adoptions) but does
> **not** overlap it: that file tables *which unit holds the plan* across this estate's own
> archetypes; this file rules *which coordination substrate* the fleet itself runs on. Filed via
> #696, 2026-08-19.

## The fleet-canon-vs-native-agent-teams ruling

Claude Code's experimental `agent-teams` (a shared in-memory task list, a peer mailbox, and a
plan-approval write-gate) is **not adopted** as this estate's standing coordination substrate
(ADR-0023 Decision (a)). The fleet — `fleet.json`/`fleet-roster.md`, ADR-0005's claim protocol,
`git worktree` isolation — stays canon, because it already buys the two structural guarantees
`agent-teams` gives only as a prompt-level convention:

- **Worktree isolation** is a hard, filesystem-level file-ownership boundary (`git worktree`) —
  the precondition Section 5's session-death resilience and the #180/#182 defect fix both depend
  on. `agent-teams`' file ownership is a prompt-level convention only, no filesystem-equivalent
  boundary.
- **A durable, restart-surviving ledger** (`fleet.json`/roster/GitHub claims — assignee +
  timestamped comment + `in-flight` label) is readable by a successor session with no memory of
  the one that wrote it (Section 5: "inventories from durable state, never from memory").
  `agent-teams`' shared task list is in-memory, not restart-survivable the same way.

Judged against `idr-0007`'s job-evidence bar (every added seat or substrate must buy isolation,
parallelism, or independence the host provably lacks), the fleet already buys what `agent-teams`
would need to re-buy from scratch — plus a reported (unmeasured, folklore-tier) ~15x cost signal
`idr-0010`'s estate-economy doctrine requires weighing, not ignoring. Full alternatives-considered
reasoning (adopt now; hybrid planning/build split) lives in ADR-0023 Decision (a) itself.

## The FACT-shaped-never-calendar re-evaluation trigger — a reusable doctrine shape

ADR-0023 Decision (b) re-opens the substrate ruling on **named facts**, never a calendar date:
`agent-teams` graduating out of the experimental flag, or the platform shipping a
worktree-equivalent filesystem-level isolation boundary for it — either closes the isolation gap
Decision (a) rules on. Independently, `#673`'s measured cost gradient landing is a soft
re-check trigger even absent either fact firing. A calendar date passing with none of these true
is **explicitly not** a supersession trigger.

This shape generalizes beyond ADR-0023 and is worth naming as reusable doctrine for any standing
decision an estate expects to revisit: **state the re-open condition as a fact the world must
produce (a capability shipping, a stability signal, a measured data point landing), never as a
date on a calendar.** `idr-0009`'s periodic revalidation loop (decision-watcher's sampled re-test
of accepted ADR Decisions) is the *mechanism* that periodically checks whether a fact-shaped
trigger like this one has fired — it is not a second, competing date-shaped trigger, and a
revalidation round finding the trigger still unfired is a `confirmed` verdict, not a supersession.
A decision ruled with no fact-shaped trigger at all defaults to standing indefinitely, which is
itself the unpriced-automation failure mode `idr-0010` names — so a decision an estate expects to
revisit earns this shape explicitly, the same way ADR-0023 (b) does, rather than being left to a
"revisit sometime" default with nothing concrete to check it against.

## The fleet-native write-gate — landed, not pending

ADR-0023 Decision (c) ruled that the plan-approval write-gate **concept** (hold a dispatched
worker's mutating writes un-landed until an explicit acceptance step) is worth pursuing natively
in the fleet's own dispatch contract, decoupled from `agent-teams` or its experimental flag, as a
follow-up ticket. That follow-up (#686) has **shipped**: `teamwork` 2.28.0 (PR #701,
`lld-0022-fleet-native-write-gate.md`) realizes it as `[[dispatch-ticket]]` Phase 5 stage 2a — an
unconditional hold between the branch push and PR-open, released by an accept marker (a durable
comment naming the pushed branch's HEAD SHA) from the marshal (`fleet-rules` Section 7's routing
seat), fail-closed (`write-gate-blocked`) when no live marshal is present, and composing on top of
— never bypassing — ADR-0012's quick-build auto-merge predicate (stage 2b). Read
`[[dispatch-ticket]]`'s own Phase 5 stage 2a and its `references/plan-approval-write-gate.md` for
the mechanics; this file only points there so a reader of the substrate ruling above doesn't read
(c) as still open.
