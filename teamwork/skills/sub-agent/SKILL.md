---
name: sub-agent
description: >-
  Dispatches one named agent unattended via the `Agent` tool — the caller's session keeps
  running; the dispatch returns a single completion, exactly like any other `Agent`-tool call.
  Run /sub-agent {agent-name} [task/charter]. NOT the forked form (`/fork-agent {agent-name}` —
  runs inline in a background fork of the caller's own session, not a real subagent instance);
  NOT the host-session-adopts-the-contract form (`/bind-{seat}` — no dispatch at all, the host
  itself holds the contract); NOT a per-seat alias — this command takes any registered agent
  name as its argument and mints none of its own; NOT arbitrary unregistered instructions with
  no agent name to resolve (`/sub-task {instructions}`).
disable-model-invocation: true
user-invocable: true
argument-hint: "{agent-name} {task/charter for the agent}"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
---

# sub-agent — the `sub-` mechanic, named and parameterized

ADR-0020 D3's third command head: `sub-` names a real, unattended `Agent`-tool dispatch — a
genuinely separate context, not this session and not a fork of it. Every seat in the estate that
already has a standing dispatched twin (`build-leader`, `planning-leader`, `review-leader`,
`product-leader`, `fleet-marshal`, and the rest) was already reachable via the `Agent` tool by
name; this command is the generic, parameterized front door to that same mechanic, so a caller
never has to know each seat's own tool-call shape to reach it. Per D4, no per-seat alias is minted
here — `/sub-agent {name}` is the whole surface.

## Phase 1 — Resolve the target

`$ARGUMENTS`' first token is the agent name; everything after it is the task/charter the dispatch
carries. `${CLAUDE_PLUGIN_ROOT}` resolves to only this plugin's own root, not a cross-plugin
search path, so resolve against the three real agent homes instead: every installed plugin's
cache (`~/.claude/plugins/cache/*/*/*/agents/<name>.md`), the current project's own
`.claude/agents/<name>.md`, and the user's own `~/.claude/agents/<name>.md` — exact match only,
case-sensitive, no fuzzy resolution.

## Phase 2 — Seal and dispatch

Invoke the `Agent` tool against the resolved agent, carrying the task/charter as its prompt —
sealed the way any dispatch is: the task stated once, enough context that the agent doesn't have
to guess scope, and nothing this session should have done itself instead. This command's own job
ends at the seal; it does not narrate the dispatched agent's internal turns.

## Phase 3 — Relay the return

The `Agent` tool's own completion is the caller's answer — relay it, don't re-summarize it away or
add unearned framing. Where the dispatched agent is a NAMED teammate (long-lived, addressable),
its report may instead arrive via `SendMessage`; state which delivery path this dispatch used so
the caller knows whether to expect a synchronous return or a later message.

## Failure branches

- **No agent name resolves** → report the miss and name the closest candidates found, if any.
- **The name matches more than one installed plugin's `agents/`** → report the collision; never
  guess.
- **`$ARGUMENTS` carries no task after the agent name** → report that a task/charter is required;
  never invent one to fill the gap.
- **This session itself is a nested dispatch and holds no `Agent` tool of its own** → this command
  cannot run at all; report the capability gap plainly rather than attempting a dispatch, and name
  the resume path (return to a session that does hold the tool).
- **This session itself is a nested dispatch AND holds the `Agent` tool** → the no-nested-wait
  rule: do not dispatch and then end this turn waiting on a background callback for the
  sub-agent's completion — the `Agent` tool's own return is synchronous from this call's
  perspective; act on it directly.

## Done

Done when the dispatch was sealed once, its completion relayed verbatim (verdict/result first),
and the delivery path used is stated. NOT done while a dispatch sits unrelayed, a collision was
silently resolved by guessing, or this session narrates the sub-agent's own internal work instead
of its return.
