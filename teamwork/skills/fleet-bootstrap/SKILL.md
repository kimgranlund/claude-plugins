---
name: fleet-bootstrap
description: >-
  Full one-terminal fleet cold-start (#410 addendum 3, level 2 — composes team-scaffolding + the
  roster): adopts the orchestrator seat, dispatches the product seat to draft the intent layer,
  then HARD-GATES on human ratification of that draft (AskUserQuestion where reachable; no live
  user stops and names the pending gate). Seeds or updates the fleet manifest (roster, tier
  deviations with dated justification, manned-vs-background, live seat state). Run
  /fleet-bootstrap [spawn-list], a comma-separated subset of reviewer,planner (default empty —
  those two are manually operated per #410 addendum 3), always confirmed via one AskUserQuestion
  before spawning — the argument only pre-selects, it never skips that confirm. NOT a single seat's own bootstrap
  (team-scaffolding — reproduced inline here for the orchestrator seat, called directly for
  reviewer/planner spawns; alone correct for a human joining one seat by hand); NOT for redoing the
  gate after ratification (fires once per cold start).
disable-model-invocation: true
user-invocable: true
argument-hint: "[spawn-list - comma-separated subset of reviewer,planner; default empty]"
---

# fleet-bootstrap — one terminal, cold-start the whole fleet

The standing fleet is four seats (`{repo}-agent` / `{repo}-reviewer` / `{repo}-planner` /
`{repo}-product`), each already reachable one at a time via `/team-scaffolding <role>` (level 1).
This command is level 2: a single terminal drives the whole cold start — adopt orchestrator,
stand up the product seat, gate on human ratification of the intent layer that seat produces, then
spawn whichever remaining seats the human wants running in the background. `$ARGUMENTS`: an
optional comma-separated spawn-list, default empty (see Phase 5).

## Phase 0 — Seed or read the fleet manifest

Read `.claude/ops/fleet.json`. Absent → this is a virgin repo; seed it now with the schema in
`references/fleet-manifest-schema.md` (seat roster, canonical tier ladder with today's date as
`justification_date` for every seat still at its canonical tier, `mode: "manual"` for every seat,
empty `live_state.joined`) — no interview, matching `team-scaffolding`'s own rule that an explicit
command invocation with no role question asked is itself the human's act of declining one; running
`/fleet-bootstrap` at all is that same explicit act. Present → read it as the record of who has
already joined and at what tier/mode; do not overwrite existing `live_state` entries, only append.

## Phase 1 — Register this session as the orchestrator seat

This session registers itself as `{repo}-agent` by performing `team-scaffolding`'s own Phase 1–4
mechanics inline — role `agent`, canonical tier, no permission-profile deviation — rather than
running `/team-scaffolding agent` through the Skill tool. That path is structurally blocked:
`team-scaffolding` carries `disable-model-invocation: true` (command-only adoption is deliberate
there — see its own Rejected alternatives), and `/fleet-bootstrap` carries the same flag, so this
composition IS already the one explicit human-typed invocation `team-scaffolding`'s contract
requires; there is no second human turn to wait on (same defect class as #421/#422, team-scaffolding's
own Phase 5 fix — a skill claiming a Skill-tool hand-off against a `disable-model-invocation`
target).

1. Bind role `agent`. Validate against `.claude/ops/fleet.json` per `team-scaffolding` Phase 1's
   role-token branch — a still-live `agent` entry is a collision, not a choice: report the existing
   entry's date and stop (Failure branches) rather than layering a second holder over it.
2. Print `Seat: {repo}-agent`, and append the roster row to `.claude/ops/fleet-roster.md`
   (`team-scaffolding` Phase 2).
3. `agent` carries no permission-profile deviation (`team-scaffolding` Phase 3) — state that
   explicitly: `No permission-profile deviation for this role — full write access retained`.
4. Print the comms charter (`team-scaffolding` Phase 4): the `agent` seat-tier deviation
   (fable+low vs. the canonical sonnet+high orchestration tier, justified by forks being
   unpinnable per #313 — team-scaffolding Phase 4 point 1's own wording), the
   SendMessage-is-a-nudge doctrine, and the peer roster read from `fleet-roster.md`.
5. Append `live_state.joined` (`role: agent`, `mode: manual`, today's date) in `fleet.json`, per
   Phase 0.

This registers the seat; it does not separately adopt `teamwork:lead-team`'s contract via a
printed command the way a solo `/team-scaffolding agent` run would (its Phase 5 hands that off to
a second human-typed `/lead-team`). `/fleet-bootstrap`'s own remaining phases (2–6) ARE this
session's orchestration work for the cold start — Phase 6 names `/lead-team` as a follow-up the
human can run afterward for ongoing day-to-day orchestration, never claimed as already adopted here.

## Phase 2 — Dispatch the product seat

Dispatch a synchronous `Agent` call (subagent_type: general-purpose is fine — no dedicated agent
file exists for this seat; the dispatch prompt instructs it to adopt `docs:product-authoring`'s
contract for one charter: "produce or update the intent layer — product brief / PRD / IDRs — for
this repo, then report a summary of what it proposes, ready for human ratification. Do not treat
silence as approval; you are drafting for someone else's sign-off.") Record `live_state.joined`
(`role: product`, `mode: dispatched` — a synchronous `Agent` call, not a live terminal or a
long-lived background seat) once it reports back.

## Phase 3 — HARD GATE: human ratification of the intent layer

This is the one hard gate in the whole command. Present the product seat's proposed intent layer
via `AskUserQuestion` (options: Ratify / Revise — send back to the product seat with feedback /
Reject — stop the cold start here) whenever a live user is reachable.

**No live user reachable** (unattended dispatch, `AskUserQuestion` unavailable or would auto-answer
under momentum): STOP here. Report plainly that the fleet cold start is blocked on this gate, name
it explicitly ("intent-layer ratification — human required"), and do not proceed to Phase 4 or 5 —
mirrors `authorkit:overhaul-execute`'s own no-live-user rule: a run with no reachable human at a
hard gate reports SKIPPED/blocked.

Record the gate's outcome (`ratified` / `revised-and-reratified` / `rejected-stopped-here`) as
`live_state.gate` in `fleet.json` before continuing.

## Phase 4 — Determine and confirm the spawn list

`$ARGUMENTS`, comma-separated, restricted to `reviewer` and `planner` (the only two seats this
phase can spawn — `agent` is already this session, `product` was already dispatched in Phase 2).
**Default (no argument): empty.** Reviewer and planner are, per #410 addendum 3, the
seats Kim drives manually in a terminal — a background agent cannot be interactively steered the
way a live terminal seat can, so defaulting to spawning them would fight the human's own stated
operating mode.

**This command's one confirm** (#410 bare-invocation-UX addendum: "exactly ONE confirm — the
background-seat spawn list before creating them; fan-out is confirmed, never inferred"): present
the resolved list — the argument's value, or "none (default)" — via one `AskUserQuestion` before
spawning anything, options `None` / `reviewer` / `planner` / `reviewer + planner`, pre-selected to
match `$ARGUMENTS`. The human's answer here is final regardless of what `$ARGUMENTS` said — an
argument sets the pre-selection, it does not skip this confirm. No live user reachable here — a
rarer case than Phase 3's, since an unattended run already stopped at that earlier gate; this
branch only fires if the human became unreachable after ratifying — → do not spawn anything (an
unconfirmed fan-out is not "assume the argument's list"); report the spawn phase as skipped for
the same no-live-user reason, and proceed to Phase 6.

## Phase 5 — Spawn the confirmed seats as long-lived named background agents

For each role in the confirmed list (skip entirely if empty — proceed straight to Phase 6):

1. Dispatch via the `Agent` tool, `name: "{repo}-<role>"`, prompt instructing it to run
   `/team-scaffolding <role>` as its first action (so it inherits level 1's own
   naming/wall/charter discipline) then hold its adopted `/lead-review` or `/lead-planning`
   contract for the fleet's duration.
2. **Record the cloud-can't-message-back caveat explicitly in that dispatch's charter text**: "You
   are a background seat — if this session runs remotely, it cannot `SendMessage` back to a peer
   that has since exited. Route anything a peer needs to see through the durable channels
   (`fleet.json`'s live-seat state, `fleet-roster.md`, GitHub Issue/PR comments), never solely through a
   live nudge you cannot guarantee lands."
3. Append `live_state.joined` (`role`, `mode: "background"`, `agent_name`, today's date) in
   `fleet.json`.

**Hybrid swap**: any background seat spawned here is replaceable at any time by a human running
`/team-scaffolding <role>` in their own terminal — the roster (`fleet.json` + `fleet-roster.md`) is
what a rejoining session reads to discover it's taking over an existing seat, not starting fresh.

## Phase 6 — Report

One summary: which seats are live and how (manual/background), the gate's outcome, the spawn list
honored (one of: "none — confirmed default", "reviewer/planner — confirmed", or "confirm skipped —
no live user, nothing spawned"), the `fleet.json` path as the durable record a later session reads
to resume orientation, and — since Phase 1 only registered the orchestrator seat, not the
`teamwork:lead-team` contract itself — name `/lead-team` as the follow-up command for the human to
run in this session when they want that contract's ongoing day-to-day discipline.

## Failure branches

- **No live user at Phase 3** → stop there per Phase 3; nothing after it runs.
- **`fleet.json` malformed or unwritable** → stop at Phase 0, report the failure; do not proceed
  believing seat state is being tracked when it silently isn't (mirrors `lld-0006`'s C3 verification
  discipline for the reviewer wall).
- **Spawn-list argument names anything other than `reviewer`/`planner`** → report the invalid
  entries and proceed only with the valid ones (never silently drop the whole argument to the
  default).

## Done

Done when Phase 6's report has printed — never when the gate is still pending (a blocked run at
Phase 3 is its own valid terminal state, reported as blocked, not silently abandoned).
