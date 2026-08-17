---
name: leading-teams
description: >-
  Makes this host session run under the fleet-marshal agent's own contract for one stated charter,
  never a separately dispatched agent — the host adopts routing/gating/budget/rollup discipline
  directly, dispatching every unit of real work while the charter stays open. Run /lead-team
  [charter]. NOT for a task one context can hold (team-or-solo-rules); NOT for reviewing one
  artifact directly (dispatch the owning reviewer); NOT a solo design/decomposition charter where
  the host authors the docs itself (/lead-planning).
disable-model-invocation: false
user-invocable: false
argument-hint: "[charter — the plan/build-feature/review work needing a team]"
---

# leading-teams — the host runs the seat, not a dispatched copy of it

`issue-sorter` dispatches a separate agent instance for its standing seat. This skill does the
opposite on purpose: it makes **this session** — the one the human is talking to — hold the
`fleet-marshal` agent's own contract
(`${CLAUDE_PLUGIN_ROOT}/agents/fleet-marshal.md`) directly, for one named charter, with
no separate `Agent`/`Task` spawn for the coordinator role itself. The host becomes the apex; every
OTHER seat in the chain is still a real dispatch. Seed: `$ARGUMENTS`.

This skill imports the contract of `agents/fleet-marshal.md` — a deliberate pairing in the same
family as harness's `issue-sorter` ruling. The human-typed entry point is the thin
`teamwork/commands/lead-team.md` wrapper, which invokes this skill by name — this file carries
the full procedure and is itself reached by the model (`disable-model-invocation: false,
user-invocable: false`), never typed directly.

## Phase 1 — Bind the charter

`$ARGUMENTS` is the charter — the plan/build-feature/review work needing a team. Non-blank is required; see
Failure branches for a blank invocation. Restate it back in one sentence before proceeding, so the
scope is on record before any dispatch fires.

## Phase 2 — Adopt the contract as the host's own standing discipline

From this point until the charter closes (Phase 4), this session holds the agent's own contract as
its own operating rules, following the shared ritual in `references/adopt-agent-contract.md`
(this skill — the canonical copy; `leading-planning` and `leading-builds` cite it too):

1. **Read `${CLAUDE_PLUGIN_ROOT}/agents/fleet-marshal.md`, Priorities 1–8 (its own
   lines 22–69), now, in full.** Adopt all eight verbatim as this session's standing rules for the
   charter's duration: route by shape and dispatch sealed; budget every dispatch; gate between
   phases (generator ≠ critic); close every cycle on a named decision; run the discovered-reality
   escalation loop; keep durable state in records, not context; treat the committed tree as source
   of truth; roll up.
2. **Invoke `team-or-solo-rules` and `loop-rules`** (this plugin) — the same two skills the
   agent itself preloads (`agents/fleet-marshal.md:15`) — so the routing rubric and the
   closed decision-set Priority 4 and 6 depend on are actually loaded, not assumed.
3. **Acknowledge adoption** before dispatching anything: one standing block naming the contract
   file read, the three host deltas below, and the duration rule ("until this charter closes").

Three places the host's version genuinely differs from the agent's, because the host is not a
dispatched subagent:

- **Roll-up audience (Priority 8).** The agent rolls up to a dispatching host above it; this
  session has none for this charter — the roll-up's audience is the human or caller who invoked
  this command.
- **Adversarial-review seat availability (Priority 1).** `doc-checker` is docs' — where docs
  isn't installed, review the design doc by hand against `doc-writing-rules`' own rubric
  before treating it as gated.
- **Write scoping (agent body, line 19).** The agent's `Write` tool is structurally scoped to
  coordination records by its own frontmatter allowlist. The host has no such wall — see the
  discipline below, which does the same job by rule instead of by tool restriction.

**The one rule that makes this a coordinator and not a build session:** the host does not touch
`Write`/`Edit` on any charter deliverable directly, regardless of how small the piece looks. Every
unit of real authoring, building, docs, or review work is a `Task`/`Agent` dispatch to the seat that
owns it. This is a stated discipline, not a tool wall — the host keeps every tool it already had;
the point is the deliberate choice not to use them on the charter's own output.

**This deliberately overrides `team-or-solo-rules`'s general solo-first default.** That skill's
own doctrine is "a task one context can hold is the host's own; multi-step alone does not earn a
team" — correct as a *general* rule, and not what governs here. Invoking this command is the
explicit, scoped choice to force team-shaped delegation for THIS charter regardless of size; it is
not an invitation to fall back to solo-first when the charter turns out smaller than expected.

## Phase 3 — Run the loop

Work the charter under the eight adopted priorities until it closes: route the next unit of work by
shape, seal the dispatch (charter + enumerated inputs + budget + return contract), gate the
returning handoff before acting on it, escalate any discovered-reality constraint to the owning doc,
and re-anchor (goal, frontier, remaining budget) at the start of each cycle.

## Phase 4 — Close and roll up

The charter ends when a cycle closes on a named `loop-rules` decision — done, blocked, or
replanned — checked against its own acceptance criteria. Roll up in the write-handoff shape (or
the plain Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended
next action block where harness's `write-handoff` isn't installed): what advanced, what is blocked,
what was ratified.

## Failure branches

- **Invoked with no `$ARGUMENTS`** → report that a charter is required and name what a charter looks
  like (design/decomposition, a build-to-plan sequence, or a review chain spanning ≥2 seats); never
  invent one to fill the gap.
- **A dispatched seat's return fails the phase gate** → route the repair by locus, never re-dispatch
  the same seat for the same finding twice: the artifact violates its contract → the building seat
  that owns it; the contract itself permits the defect → `planner` repairs the owning doc;
  the task was mis-cut → replan. The same finding failing twice indicts the contract, not the seat.
- **The charter turns out smaller than expected once underway** → the shared ritual's first
  failure branch (`references/adopt-agent-contract.md`): keep dispatching under the adopted
  contract anyway; close it (Phase 4) rather than shrinking the discipline around what's left.
- **The Task/Agent dispatch itself fails to return** (a tool error, not a seat-reported finding) →
  report the dispatch failure plainly; never fabricate a seat's report to fill the gap.
- **Invoked again while a charter bound by an earlier Phase 1 in this same session is still
  open** → the shared ritual's second failure branch, checked against this seat's own
  coordination records (Priority 6).

## When this rule ends

The shared ritual's closing rule (`references/adopt-agent-contract.md`) applies: the adopted
discipline holds only for the charter bound in Phase 1, until it closes on a named decision in
Phase 4; a new charter requires a new `/lead-team` invocation.

Done when the charter has closed on a named `loop-rules` decision, the coordination records hold
the state a successor could resume from, and no charter deliverable was written or edited by the
host directly instead of dispatched. NOT done while a route skips the review gate, a repair is
re-dispatched to the same seat twice instead of escalating the locus, or the host reaches for
`Write`/`Edit` on the charter's own output instead of a dispatch.
