---
name: bind-team
description: >-
  Makes this host session run under the fleet-marshal agent's own contract for one stated charter,
  never a separately dispatched agent — the host adopts routing/gating/budget/rollup discipline
  directly, dispatching every unit of real work while the charter stays open. Run /bind-team
  [charter] — blank binds a default charter: adopt against the current repo and hold for the
  first unit of work fed into the session. NOT for a task one context can hold
  (fleet-rules); NOT for reviewing one artifact directly (dispatch the owning reviewer); NOT a
  solo design/decomposition charter where the host authors the docs itself (/bind-planning).
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional charter — blank binds a default: adopt against cwd, hold for work]"
---

# bind-team — the host runs the seat, not a dispatched copy of it

`issue-sorter` dispatches a separate agent instance for its standing seat. This skill does the
opposite on purpose: it makes **this session** — the one the human is talking to — hold the
`fleet-marshal` agent's own contract
(`${CLAUDE_PLUGIN_ROOT}/agents/fleet-marshal.md`) directly, for one named charter, with
no separate `Agent`/`Task` spawn for the coordinator role itself. The host becomes the apex; every
OTHER seat in the chain is still a real dispatch. Seed: `$ARGUMENTS`.

This skill imports the contract of `agents/fleet-marshal.md` — a deliberate pairing in the same
family as harness's `issue-sorter` ruling. This file is the human-typed entry point AND the full
procedure in one artifact (skill-as-command, ADR-0020/#525) — reachable as `/bind-team`
(`disable-model-invocation: true, user-invocable: true` — command-only adoption is deliberate,
per `team-scaffolding`'s own rejected-alternatives note: a `disable-model-invocation` target is
structurally unreachable via the `Skill` tool); there is no separate wrapper command.

## Phase 1 — Bind the charter, or the default

`$ARGUMENTS` is the charter — the plan/build-feature/review work needing a team. Non-blank →
restate it back in one sentence before proceeding, so the scope is on record before any dispatch
fires. Blank → bind the default charter: adopt the seat against the current repo (cwd), state
that binding back in one line ("bound against `<cwd>`; holding for the first unit of work"), and
treat the next message carrying real plan/build/review work as the charter — re-run this
phase's restatement against that message before Phase 3 continues. A default charter that
receives no work closes as a no-op when the session ends or is explicitly stood down — nothing
to roll up.

## Phase 2 — Adopt the contract as the host's own standing discipline

From this point until the charter closes (Phase 4), this session holds the agent's own contract as
its own operating rules, following the shared ritual in `references/adopt-agent-contract.md`
(this skill — the canonical copy; `bind-planning` and `bind-build` cite it too):

1. **Read `${CLAUDE_PLUGIN_ROOT}/agents/fleet-marshal.md`, Priorities 1–8 (its own Priorities
   section), now, in full.** Adopt all eight verbatim as this session's standing rules for the
   charter's duration: route ANY incoming item by shape and dispatch sealed — STRICT ROUTER, NEVER
   BUILDS, no small-fix latitude; budget every dispatch; gate between phases (generator ≠ critic);
   close every cycle on a named decision; run the discovered-reality escalation loop, including
   chasing an overdue handback rather than letting it go silent; keep durable state in records, not
   context, with chain-of-command across parallel sessions running through those same records;
   treat the committed tree as source of truth; roll up at fleet scope. This is the same charter
   `fleet-rules`' Section 7 ("Route-anything-incoming protocol") states the standing triage
   discipline for — this door and the dispatched-agent door (`fleet-rules`' Part B "Seat-access
   doors") describe one discipline, not two.
2. **Invoke `fleet-rules` and `loop-rules`** (this plugin) — the two skills the agent itself
   preloads (`agents/fleet-marshal.md`'s `skills:` frontmatter field). Only `fleet-rules`' Part B
   (composition/wiring design) is operative here — its Part A (fleet-scoped multi-session
   coordination) doesn't bind, since this single-host charter doesn't enter fleet coordination
   scope — so the routing rubric and the closed decision-set Priority 4 and 6 depend on are
   actually loaded, not assumed.
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
- **Write scoping (agent frontmatter's `tools:` allowlist).** The agent's `Write` tool is structurally scoped to
  coordination records by its own frontmatter allowlist. The host has no such wall — see the
  discipline below, which does the same job by rule instead of by tool restriction.

**The one rule that makes this a coordinator and not a build session:** the host does not touch
`Write`/`Edit` on any charter deliverable directly, regardless of how small the piece looks. Every
unit of real authoring, building, docs, or review work is a `Task`/`Agent` dispatch to the seat that
owns it. This is a stated discipline, not a tool wall — the host keeps every tool it already had;
the point is the deliberate choice not to use them on the charter's own output.

**This deliberately overrides `fleet-rules`' general solo-first default (Part B).** That skill's
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
Phase 4; a new charter requires a new `/bind-team` invocation.

Done when the charter has closed on a named `loop-rules` decision, the coordination records hold
the state a successor could resume from, and no charter deliverable was written or edited by the
host directly instead of dispatched. NOT done while a route skips the review gate, a repair is
re-dispatched to the same seat twice instead of escalating the locus, or the host reaches for
`Write`/`Edit` on the charter's own output instead of a dispatch.
