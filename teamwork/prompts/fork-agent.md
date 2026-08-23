---
description: "Runs one named agent's own contract as a background fork off the caller's session — the fork runs the target agent's definition inline, in the forked context, and only its final typed result reaches the caller. Run /fork-agent {agent-name} [task]. NOT the standing dispatched form (`/sub-agent {agent-name}`, Agent tool — no forked context, runs as a real subagent instance); NOT the host-session-adopts-the-contract form (`/bind-{seat}` — no fork, no spawn, the host itself holds the contract until it stands down); NOT a per-seat alias — this command takes any registered agent name as its argument and mints none of its own."
argument-hint: "{agent-name} [task/charter for the agent]"
---

# fork-agent — the `fork-` mechanic, named and parameterized

ADR-0020 D3 names three command heads after the platform mechanic they trigger, not the seat they
reach: `bind-` (the host adopts a contract in place), `fork-` (a background fork runs one target
and dies, this command), `sub-` (`/sub-agent`, an `Agent`-tool dispatch runs unattended). Before
this command, the `fork-` mechanic had no generic entry point — `/build-feature` is the one
concrete instance (it forks `dispatch-ticket`), hardcoded to that one target. This command
generalizes the mechanic to any registered agent.

Per D4, `/fork-agent` and `/sub-agent` are parameterized-only — no per-seat aliases are minted
for either, regardless of how often a given agent name is used through them; an alias is only
ever earned by a `/bind-*` seat (D4's own hybrid-shape ruling).

## Phase 1 — Resolve the target

`$ARGUMENTS`' first token is the agent name; everything after it is the task/charter passed to
that agent. `${CLAUDE_PLUGIN_ROOT}` resolves to only THIS plugin's own root, not a cross-plugin
search path, so a name search needs the installed-plugin cache directly: glob
`~/.claude/plugins/cache/*/*/*/agents/<name>.md` across every installed plugin, plus, when the
charter is scoped to a specific project, that project's own `.claude/agents/<name>.md`. Exact
match only, case-sensitive, no fuzzy resolution — an agent name collision across plugins is a
named blocker, not a guess.

## Phase 2 — Run the target's contract, in this forked context, once

Read the resolved agent file in full. Adopt its contract as this fork's own operating rules for
the duration of this one invocation — same posture harness's `issue-sorter`-style dispatch would
use if it ran inline, except here the isolation is the fork boundary, not a separate `Agent` call.
Work the task under that contract to its own stated completion condition (the agent file's own
"done when" language, where it states one; otherwise, the task as scoped in `$ARGUMENTS`).

## Phase 3 — Return only the typed result

The fork's own final text is the entire deliverable the caller sees — no partial narration, no
intermediate tool noise. Shape it the way the resolved agent's own contract would shape a report
(its own report contract, where stated; otherwise the plain Status/Summary/Files
changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action shape).

## Failure branches

- **No agent name resolves** → report the miss and name the closest candidates found (if any);
  never silently fall back to a different agent.
- **The name matches more than one installed plugin's `agents/`** → report the collision and both
  paths; never guess which one the caller meant.
- **`$ARGUMENTS` carries no task after the agent name** → run the resolved agent's own
  no-task/blank-seed branch if it states one; otherwise report that a task is required.
- **The resolved agent itself holds the `Agent` tool** (a further nested dispatch) → the
  no-nested-wait rule applies exactly as it would for a real `Agent`-tool dispatch of that same
  agent: act on a nested dispatch's own return value directly, never end this fork's turn waiting
  on a separate notification.
- **This fork edits files** (it holds `Edit`/`Write`) — a background fork is not a checkpoint
  boundary the way a foreground turn is (`/rewind` does not undo it); git is the only revert path
  for anything this fork writes, same as any other background dispatch.

## Done

Done when the resolved agent's own completion condition was reached (or a named blocker reported)
and the fork's final text is the caller's entire deliverable. NOT done while the fork narrates
intermediate progress instead of returning the typed result, or silently substitutes a different
agent than the one named.
