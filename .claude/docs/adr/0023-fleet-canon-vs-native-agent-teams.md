---
doc-type: adr
id: adr-0023
status: accepted
date: 2026-08-18
owner: kim.granlund
supersedes: null
intent-refs: idr-0007 (solo-first composition — the isolation/parallelism/independence gate
  every added seat or substrate must buy; this ADR judges agent-teams against it), idr-0010
  (estate economy — recurring/standing decisions are priced and re-checked against evidence,
  never decided once and left to drift; this ADR's own re-evaluation trigger is that doctrine
  applied to a substrate choice), idr-0009 (doctrine truth maintenance — every accepted ADR
  Decision is periodically re-tested via decision-watcher's revalidation mode; that periodic
  sweep is the mechanism that checks whether this ADR's own fact-shaped trigger has fired, not
  a competing date-shaped re-read this ADR overrides)
scope: app
audience: human, product-seat
---
# ADR-0023 — Fleet stays canon over native `agent-teams`, pending a named re-evaluation trigger

> PROPOSED 2026-08-18 — drafted by build-leader (dispatch-ticket, ticket #672) from the
> marshal's 2026-08-18 lean. Ratification is a live `AskUserQuestion` round with Kim that no
> unattended dispatch can run; this record stays `status: proposed` until the marshal (or Kim
> directly) runs that round. Not yet append-only — editable until `status: accepted` lands.

## Context

The estate's fleet (`teamwork:fleet-rules`, `fleet.json`/`fleet-roster.md`, ADR-0005's claim
protocol) gives two structural guarantees no amount of prompting substitutes for: **worktree
isolation** — a hard, filesystem-level file-ownership boundary (`git worktree`), the precondition
`fleet-rules` Section 5's session-death resilience and the #180/#182 defect fix both depend on —
and a **durable, restart-surviving ledger** — `fleet.json`/roster/GitHub claims (assignee +
timestamped comment + `in-flight` label), readable by a successor session with no memory of the
one that wrote it (`fleet-rules` Section 5: "inventories from durable state, never from memory").

Claude Code's experimental `agent-teams` feature
(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) offers a different shape: a shared task list with
statuses, dependencies, and claiming; a peer mailbox; and a **plan-approval write-gate** — a
teammate is held read-only until the lead accepts its plan, before any mutating write lands. It
gives none of the fleet's two structural guarantees as shipped: file ownership is a **prompt-level
convention** only (no worktree-equivalent filesystem boundary), and the task list is in-memory,
not restart-survivable the way `fleet.json` plus GitHub claims are. It is also reported at **~15x**
the fleet's cost — a figure carried here as reported/folklore only, per the citation discipline
`file-task`'s sibling ticket #671 already applies to the same source document (harvest the
substance, never cite the source as authority): no first-party measurement of this multiple exists
yet. Track E (#673) is running that measurement now — a soft dependency on this ADR (see
`## Related`), not a hard `Blocked-by`.

The marshal's 2026-08-18 lean, which this ADR is drafted from: keep the fleet — real isolation
plus an auditable, restart-surviving ledger beats prompt-partitioned file ownership plus an
in-memory list — but the plan-approval write-gate **concept** (hold a dispatched worker's writes
un-landed until an explicit acceptance step) is structurally stronger than the estate's current
pre-merge posture, which has no equivalent in-loop write-hold: today a dispatched builder writes
freely inside its own isolated worktree, and the estate's only backstops are a fresh-context
checker pass (generator≠critic, `plugin-authoring.md`'s semantic-edit invariant) and the
human-gated PR merge (ADR-0002) — both post-hoc, after the writes already landed, never a
pre-write hold. (All plugin-shipped hooks were retired 2026-08-17, #466 — there is no
enforced deny-hook layer left to compare against; the estate's pre-merge posture today is the
checker-plus-human-merge pair above, not a hook wall.)

## Decision

**(a) The fleet stays canon.** `agent-teams` is not adopted now, for standing multi-agent
coordination in this estate. Rationale, against `idr-0007`'s job-evidence bar (every added seat
or substrate must buy isolation, parallelism, or independence the host provably lacks): the fleet
already buys real isolation (worktrees) and durable-ledger resumability that `agent-teams` does
not structurally provide as shipped, and the reported ~15x cost — even unmeasured — is a cost
signal `idr-0010`'s estate-economy doctrine requires this estate to weigh, not ignore, before
adopting a substrate replacement.

Alternatives considered:
1. **Adopt `agent-teams` now, estate-wide.** Rejected: no worktree-equivalent isolation (prompt-
   level file ownership is a convention, not a boundary — exactly the gap `fleet-rules` Section 5
   and the #180/#182 fix close for the fleet), an unmeasured but reported ~15x cost with no
   first-party data yet, and the feature is still behind an experimental flag with no stability
   guarantee.
2. **Hybrid — `agent-teams` for planning/discussion, fleet for build execution.** Rejected for
   now: this would run two parallel coordination substrates (`fleet.json`/roster vs. a native
   task list) with no `idr-0007` job-evidence gap the hybrid closes that the fleet alone doesn't
   already close; revisit only once `agent-teams` ships a worktree-equivalent isolation boundary,
   at which point the split might earn genuine parallelism value instead of just doubled
   vocabulary.
3. **No re-evaluation trigger — rule (a) once and leave it standing indefinitely.** Rejected:
   `idr-0010` requires recurring/standing decisions to be priced and re-checked against evidence
   as it arrives, not decided once and forgotten; an un-triggered "keep forever" default is
   itself the unpriced-automation failure mode that record names.

**(b) Re-evaluation trigger — a feature-stability condition, never a calendar date.** Re-open this
ADR (supersede, never edit in place, per the accepted-ADR append-only rule this record will carry
once ratified) when **either** of the following closes the isolation gap named in Context:
- `agent-teams` graduates out of the experimental flag into a stable, documented, non-experimental
  release, **or**
- the platform ships a worktree-equivalent (filesystem-level, not merely prompt-level)
  file-ownership boundary for `agent-teams` workers, whether or not the feature is still flagged
  experimental.

Independent of either firing: once **#673's measured cost gradient lands**, re-check this ruling
against the real figure even if neither bullet above has fired — a materially lower measured
multiple than the reported ~15x could shift the calculus on its own, and a materially higher one
confirms the caution. #673 is a soft dependency (see `## Related`), not a blocker on drafting or
ratifying this ADR itself. A calendar date passing with none of the above true is explicitly
**not** a supersession trigger — the *decision* is due for re-opening when the facts above
change, never on a schedule alone. `idr-0009`'s standing periodic revalidation loop
(decision-watcher's sampled re-test of accepted ADR Decisions) still applies to this ADR like
every other — that loop is the mechanism that PERIODICALLY CHECKS whether the fact-shaped
trigger above has fired; it is not a second, date-shaped trigger competing with it, and a
revalidation sampling round finding the trigger still unfired is a `confirmed` verdict, not a
supersession.

**(c) A fleet-native write-gate equivalent, meanwhile — pursue it, decoupled from (b)'s trigger.**
The plan-approval **concept** (hold a dispatched worker's mutating writes un-landed until an
explicit acceptance step, before they can affect anything outside the worker's own isolation) does
not require `agent-teams` itself or its experimental flag — it is a sequencing rule expressible
natively in the fleet's own dispatch contract (`dispatch-ticket`'s Phase 5 lifecycle stages),
independent of whichever substrate eventually wins. Ruling: **yes, pursue a fleet-native
equivalent**, scoped as a follow-up ticket — not designed in this ADR, which rules the substrate
choice and the re-evaluation condition, not the gate's own mechanics. **Ratification mints the
follow-up ticket** (owner: the marshal, per `fleet-rules` Section 7's routing seat) — no ticket id
exists yet as of this draft. The follow-up names, at
minimum: which dispatch-ticket stage the hold applies to (a natural candidate is inside Phase 5
stage 2 itself, between the push and the PR open — never blocking the worker's own isolated
worktree writes, only the point just before they become visible/mergeable outside it), who plays
the "lead" accepting role for an unattended dispatch with no live human (the marshal, per
`fleet-rules` Section 7's routing seat, is the natural candidate — never inferred to be the human
by default), and how it composes with the existing fresh-context checker pass and ADR-0012's
quick-build auto-merge predicate (QB5's critic-green conjunct) rather than duplicating either.

## Consequences

**Easier:** no second coordination substrate to stand up or maintain alongside `fleet.json`/
roster/GitHub claims; every existing `fleet-rules` mechanism — the claim-then-guard protocol
(Section 2), session-death resilience (Section 5), the pin-race playbook (Section 6), the
route-anything-incoming protocol (Section 7) — stays valid with no parallel `agent-teams`-native
shadow doctrine to keep in sync.

**Harder:** the estate forgoes `agent-teams`' native shared task list, peer mailbox, and
plan-approval UX until this ADR is superseded on its own trigger or a fleet-native write-gate
equivalent ((c)) is built and adopted; peers keep coordinating over durable records
(`fleet.json`/roster + GitHub claims + PR/Issue comments) rather than a built-in primitive.

**Irreversible:** none. This ADR is explicitly designed to be revisited — (b) names the exact
condition under which it is superseded, and nothing ruled here forecloses adopting `agent-teams`
(or a hybrid) once the isolation gap closes and #673's cost data lands.

## Related

- **#671** — sibling Track A task (canon-fold of four agent-classes adoptions into `fleet-rules`/
  `agent-writing-rules`); same review wave, no direct dependency either way.
- **#672** — this ADR's own drafting ticket.
- **#673** — Track E, the measured cost gradient this ADR's (b) names as a soft dependency
  ("re-check even if neither bullet has fired").
- **ADR-0002** — git-native execution (worktrees + PRs), the substrate the fleet's isolation
  guarantee is built on.
- **ADR-0005** — the ticket-claim protocol realizing the fleet's durable-ledger half.
- **ADR-0012** — quick-build auto-merge; (c)'s follow-up composes with its QB5 critic-green
  conjunct rather than duplicating it.
- **`teamwork:fleet-rules`** — the fleet's standing operating protocol this ADR rules stays canon.
- **`idr-0007`, `idr-0009`, `idr-0010`** — see `intent-refs` above.

<!-- LEDGER CLASS: once status: accepted, this file is append-only. To change the decision,
     write a new ADR with supersedes: this id — the hook blocks edits here. -->

## Ratification

Ratified by Kim Granlund via a live `AskUserQuestion` round on 2026-08-18 (marshal session), decision presented verbatim: (a) fleet stays canon, (b) fact-shaped re-evaluation trigger + #673 re-check, (c) fleet-native plan-approval write-gate pursued as a follow-up ticket minted by the marshal. Accepted → append-only from this point (T4).
