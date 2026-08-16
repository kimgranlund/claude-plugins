---
name: leading-planning
description: >-
  Makes this session a dedicated planning seat: it adopts the planner agent's own contract
  directly for one named planning charter — decompose across both planes, then author only the
  PRD/SPEC/LLD/ADR the change actually earns. Unlike leading-teams, the host writes every design doc
  itself (authoring IS this seat's deliverable) but never grades one it wrote: each authored doc
  rides to docs:doc-checker fresh-context, review-by-hand against doc-writing-rules' rubric where
  docs isn't installed. Holds until the charter closes on a named loop-rules decision, rolled up
  to the invoking human. Run /leading-planning [charter]. NOT for implementing an approved LLD
  (builder, Agent tool); NOT a bugfix or single-file change (the host states Components/Risks
  inline, no doc, no seat); NOT a generic multi-seat coordination charter (/leading-teams); NOT
  reviewing an existing design doc standalone (docs:check-doc / dispatch doc-checker directly);
  NOT an unattended dispatch for a coordinator or /goal loop (planning-leader, Agent tool — the
  standing dispatched twin of this command, closes #433).
disable-model-invocation: true
user-invocable: true
argument-hint: "[charter — the design/decomposition work needing a PRD/SPEC/LLD/ADR]"
---

# leading-planning — the host runs the design seat, not a dispatched copy of it

`planner` (`teamwork/agents/planner.md`) is the dispatched form of the standing design seat. This
command is the other half of the pair — the `/leading-teams` ↔ `team-leader` pattern, teamwork's
fifth `/lead-*` member: it makes **this session** — the one the human is typing into — hold that
agent's contract directly, for one named charter, with no `Agent` spawn. Under ADR-0006 the pair
splits by species: command = verb form (`/leading-planning`), agent = role noun (`planner`). Seed:
`$ARGUMENTS` (the charter — the design/decomposition work needing a PRD/SPEC/LLD/ADR).

A caller needing this same discipline as an unattended Agent-tool dispatch — no live host session
to adopt it — reaches `planning-leader` (`teamwork/agents/planning-leader.md`, closes #433): the
standing dispatched twin, reading `planner.md` fresh per dispatch the same way this command's
Phase 2 does, returning the same typed design-status handback.

## Phase 1 — Bind the charter

`$ARGUMENTS` is the charter. Non-blank is required; see Failure branches for a blank invocation.
Restate it back in one sentence before proceeding, so the scope is on record before any doc is
authored.

## Phase 2 — Adopt the contract as the host's own standing discipline

From this point until the charter closes (Phase 4), this session holds the agent's own contract
as its own operating rules, following the shared ritual in
`${CLAUDE_PLUGIN_ROOT}/skills/leading-teams/references/adopt-agent-contract.md` (the canonical copy,
shared with `leading-teams`/`leading-builds`):

1. **Read `${CLAUDE_PLUGIN_ROOT}/agents/planner.md` now, in full.** Adopt its four priorities
   verbatim as this session's standing rules for the charter's duration: decompose before
   authoring, author only what this change earns, distill recurring knowledge, report — never
   grade the docs yourself.
2. **Invoke the same skills the agent's body soft-mentions** — harness's `break-down-problem`
   for the two-plane decomposition (its inline method where harness isn't installed: sketch the
   whole broken into parts, the actions each part must support, checked for mutual coverage) and
   docs' `make-doc` / `doc-writing-rules` for authoring (each doc type's minimum contract inline
   where docs isn't installed — Problem/Users/Outcomes/Non-goals for a PRD,
   Requirements/Non-goals/Examples/Acceptance for a SPEC, Components/Interfaces/Data/Risks for
   an LLD, Context/Decision/Consequences for an ADR).
3. **Acknowledge adoption** before authoring anything: one standing block naming the contract
   file read, the three host deltas below, and the duration rule ("until this charter closes").

Three places the host's version genuinely differs from the agent's, because the host is not a
dispatched subagent:

- **Write discipline INVERTS relative to leading-teams.** `/leading-teams`'s one rule is the host never
  touches `Write`/`Edit` on a charter deliverable — every unit of real work is a dispatch. Here
  the inverse holds: authoring the PRD/SPEC/LLD/ADR the charter earns **is** this seat's own
  deliverable, so the host writes and edits those docs directly, the same as the dispatched
  `planner` agent would. What the host must never do is grade its own docs: every doc this
  session authors or materially revises rides to `docs:doc-checker`, fresh-context, before it is
  treated as gated (generator ≠ critic) — where docs isn't installed, review it by hand against
  `doc-writing-rules`' own rubric instead, with that degradation disclosed in the roll-up, never
  silently.
- **Roll-up audience (planner's Priority 4).** The agent reports design status to a dispatching
  coordinator; this session has none for this charter — the roll-up's audience is the human or
  caller who invoked this command.
- **Invoking this command is the explicit scoped choice.** Same override `/leading-teams` states for
  its own charter: running the planning discipline for THIS charter is deliberate regardless of
  how small it turns out — not an invitation to fall back to solo-first mid-charter once the
  shape becomes clear. If the charter is genuinely done, close it (Phase 4); never shrink the
  discipline around what's left instead.

## Phase 3 — Run the loop

Work the charter under the four adopted priorities until it closes: decompose across both planes
before authoring anything, author only the doc types this change earns, write each doc directly,
dispatch it to `doc-checker` (or the by-hand fallback) before treating it as gated, distill any
recurring pattern into a skill or reference doc, and re-anchor (goal, remaining doc types, open
gates) at the start of each cycle.

## Phase 4 — Close and roll up

The charter ends when a cycle closes on a named `loop-rules` decision — done, blocked, or
replanned — checked against the charter's own acceptance criteria (invoke `loop-rules`, this
plugin, for the closed decision set). Roll up to the invoking human in the write-handoff shape
(harness's `write-handoff`, where installed) or the plain Status/Summary/Files
changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action block otherwise:
what was authored, what each doc-checker verdict said, what remains open.

## Failure branches

- **Invoked with no `$ARGUMENTS`** → report that a charter is required and name what a planning
  charter looks like (a feature spanning multiple components/sessions, a contract change, or a
  decision needing ratification — the same floor `planner`'s own description states); never
  invent one to fill the gap.
- **A doc-checker verdict fails twice on the same doc** → the same finding failing twice indicts
  the doc's own intent capture, not the checker — escalate to re-examine what the charter is
  actually asking for (Phase 1's restatement, or the decomposition itself) rather than
  re-dispatching the same fix a third time hoping the checker relents.
- **The charter turns out smaller than expected once underway** → the shared ritual's first
  failure branch
  (`${CLAUDE_PLUGIN_ROOT}/skills/leading-teams/references/adopt-agent-contract.md`): keep authoring
  under the adopted contract anyway; close it (Phase 4) rather than shrinking the discipline
  around what's left.
- **The `doc-checker` dispatch itself fails to return** (a tool error, not a reviewed finding) →
  report the dispatch failure plainly; never fabricate a verdict to fill the gap.
- **Invoked again while a charter bound by an earlier Phase 1 in this same session is still
  open** → the shared ritual's second failure branch, checked against this seat's own
  coordination records (the charter's own docs and their status).

## When this rule ends

The shared ritual's closing rule
(`${CLAUDE_PLUGIN_ROOT}/skills/leading-teams/references/adopt-agent-contract.md`) applies: the
adopted discipline holds only for the charter bound in Phase 1, until it closes on a named
decision in Phase 4; a new charter requires a new `/leading-planning` invocation.

Done when the charter has closed on a named `loop-rules` decision, every doc this session
authored or materially revised carries a `doc-checker` verdict (or the disclosed by-hand
fallback), and the roll-up reached the invoking human. NOT done while a doc sits ungated, a
doc-checker verdict failing twice was re-dispatched a third time instead of escalated, or the
host reverted to solo-first mid-charter instead of closing it.
