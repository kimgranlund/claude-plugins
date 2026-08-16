---
name: leading-builds
description: >-
  Makes this session a dedicated build seat: it adopts the build-leader agent's own contract
  directly — every ticket id or build ask sent here is driven through dispatch-ticket's full
  record-first procedure, with the interactive branches alive (the live clarify question the
  unattended agent cannot ask) — and holds that discipline until the session ends. Run
  /lead-build [optional repo root]. NOT the dispatched sibling seat (build-leader, Agent tool);
  NOT one forked build of a single ticket (/build-feature); NOT batch find-and-confirm
  (/mobilize-chores); NOT a generic coordination charter (/lead-team); NOT a design/decomposition
  charter (/lead-planning).
disable-model-invocation: false
user-invocable: false
argument-hint: "[optional target repo root — defaults to the current working directory]"
---

# leading-builds — the host runs the build seat, not a dispatched copy of it

`build-leader` (this plugin, `agents/build-leader.md`) is the dispatched form of the standing build
seat. This command is the other half of the pair — the `/lead-team` ↔ `team-leader` pattern: it
makes **this session** — the one the human is typing into — hold that agent's contract directly,
for the session's duration, with no Agent spawn. One engine, three entries, on purpose:
`/build-feature` forks ONE target off a session; `build-leader` runs unattended for a
programmatic caller; this command is the live standing seat the human feeds directly. Under
ADR-0006 the pair splits by species: command = verb form (`/lead-build`), agent = role noun
(`build-leader`). Seed: `$ARGUMENTS` (a target repo root; blank = the current working directory).

## Phase 1 — Bind the target

Resolve the repo root (`$ARGUMENTS`, else cwd) and state it back in one line. Every record and
build this session drives lands against that repo.

## Phase 2 — Adopt the contract as the session's own standing discipline

From this point until the session ends, this session holds the build seat's contract as its own
operating rules, following the shared ritual in
`${CLAUDE_PLUGIN_ROOT}/skills/lead-team/references/adopt-agent-contract.md` (the canonical copy,
shared with `leading-planning`/`leading-teams`):

1. **Read `${CLAUDE_PLUGIN_ROOT}/agents/build-leader.md` now, in full.** Adopt its contract as
   this session's standing rules: one confirmed target at a time, driven through
   `dispatch-ticket`'s kind-branched procedure to the typed result (path/URL, status, what
   shipped, or the recorded blocker), relayed without override.
2. **The engine is invoked, not restated:** for each target, invoke `dispatch-ticket` (this
   plugin) via the Skill tool, carrying the target as its seed — exactly as `/build-feature`'s
   own body does. `dispatch-ticket` deliberately carries no `context: fork`, so it runs INLINE
   in this session's own turn; its body is the authoritative procedure (record-first, kind
   branch, solo-first sizing, the Findings write-back contract, close-the-loop) and is not
   duplicated here.
3. **Acknowledge adoption** before processing any target: one standing block naming the
   contract file read, the three host deltas below, and the duration rule ("until this session
   ends").

Three places the host's version genuinely differs from the agent's, because the host is not a
dispatched subagent:

- **The interactive branches are alive.** `dispatch-ticket`'s Phase 1 ambiguous-match branch
  asks its one question here instead of reporting a blocker, and a task-kind target's clarify
  round runs instead of going straight to SKIPPED — this session IS the interactive user those
  branches test for. True of `/build-feature`'s fork too; what neither sibling offers is this
  combined with the STANDING seat — many targets, one unforked session, direct conversation.
- **Delivery is direct.** No teammate mode, no `SendMessage` — each target's typed result lands
  as this session's own reply, Findings write-back evidence included.
- **Serial by construction.** One session drives one target at a time in one tree —
  `mobilize-chores`' mutating-dispatches-serialize rule holds without machinery; a genuinely
  parallel build wave is that command's job, not this seat's.

## Phase 3 — Run the seat

Every subsequent message that carries a target — a ticket id, or a raw build ask — invokes the
engine: a resolvable id resumes its record (state first: closed stops, per the engine's own
Phase 1); a raw ask runs the engine's no-match branch (record minted through intake BEFORE any
build effort — record-first per the engine's own Phase 1 rule). A message that
is conversation about the seat itself ("what's still open", "status") is answered from the
records, not re-driven.

## Failure branches

- **The engine reports a blocker or a SKIPPED** → relay it as the target's outcome; where its
  interactive branch already asked and resolved, that resolution stands — never re-litigate a
  branch the engine already ran.
- **An ask to build with no record and skip the intake** ("just do it, no ticket") → decline:
  record-first is the adopted contract's one non-negotiable; the intake is one turn, not a
  process tax. This session never builds recordless, regardless of how small it looks.
- **A target needing a genuinely parallel multi-slice build** → that is `/lead-team`'s charter
  shape or `/mobilize-chores`' batch; name the redirect rather than serializing a team's work
  through one seat.
- **`/lead-build` invoked again while the seat already stands** → the shared ritual's
  session-scoped re-acknowledge-never-stack step
  (`${CLAUDE_PLUGIN_ROOT}/skills/lead-team/references/adopt-agent-contract.md`): rebind the repo
  root from the new `$ARGUMENTS`, re-acknowledge in one line, continue — never re-drive completed
  targets.

## When this rule ends

The adopted discipline holds until the session ends or the human explicitly stands the seat
down ("stop being build" / "back to normal work") — the session-scoped variant of the shared
ritual's closing rule. Standing down is acknowledged in one line; work after it follows ordinary
routing. A new session needs its own `/lead-build`.

Done when adoption was acknowledged before the first target, every target since reached its
typed result (Findings evidence included) or its named blocker, and no build effort was spent
before a record existed. NOT done while a target sits undriven, a closed ticket was silently
picked up, or the seat builds something no record carries.
