---
name: sub-task
description: >-
  Dispatches arbitrary instructions to ONE fresh clean-context general-purpose subagent — a
  genuinely separate context carrying zero conversation history, not a fork of this one. Run
  /sub-task {instructions}. NOT a registered agent's own contract (`/sub-agent {agent-name}` — a
  named seat, not general-purpose); NOT a fork of this session's own context (`/fork-agent` — a
  fork INHERITS this session's history, the opposite of clean); NOT the host adopting a contract
  in place (`bind-*`).
disable-model-invocation: true
user-invocable: true
argument-hint: "{instructions for the subtask}"
allowed-tools:
  - AskUserQuestion
  - Agent
---

# sub-task — a fresh clean-context subagent, for arbitrary instructions

ADR-0020 D3's `sub-` head, generalized past `/sub-agent`'s registered-name front door: this
command carries no fixed contract of its own, only whatever `$ARGUMENTS` states. It exists for
the case `/sub-agent` and `/fork-agent` don't cover — a side question or side task with no
registered agent to name, run clean rather than inheriting this session's own context.

## Phase 1 — Seal the charter

The WHOLE of `$ARGUMENTS` is the charter; the dispatched subagent sees nothing else — no
conversation history, no implicit "this" or "the above". If `$ARGUMENTS` carries an unresolved
deictic reference (it points at something this conversation established but doesn't restate),
ask ONE inline clarifying question before dispatching — never dispatch a guess at what "this"
means. Empty `$ARGUMENTS` → ask what the subtask is; never invent one.

## Phase 2 — Dispatch, unnamed

One `Agent`-tool call, `subagent_type: general-purpose`, UNNAMED — synchronous, this call's own
return is the answer, never mailbox-routed (the never-name rule: a name buys teammate-mode
routing with nothing here to address it back to). The sole exception: the charter explicitly asks
for a continuable/addressable seat rather than a one-shot answer — only then name it, and state
the mailbox semantics in the reply. Pin `model: sonnet` per the ad-hoc-dispatch doctrine, unless the sealed charter
plainly earns a higher tier — state whichever choice was made.

## Phase 3 — Relay

Relay the result verbatim-in-substance, findings-first — no re-summarizing away the answer, no
unearned framing on top of it.

## Failure branches

- **Dispatch dies** (no return, an error) → report it, then one re-dispatch of the same sealed
  charter, max — never a silent retry loop.
- **The result contradicts a constraint the charter stated** (scope, format, a stated
  non-goal) → report the gap plainly; never silently accept a result that misses its own brief.
- **This session itself is a nested dispatch and holds no `Agent` tool of its own** → this command
  cannot run; report the capability gap rather than attempting a dispatch.
- **This session itself is a nested dispatch AND holds the `Agent` tool** → the no-nested-wait
  rule: the dispatch's return is synchronous from this call's own perspective — act on it
  directly, never end this turn waiting on a background callback.

## Done

Done when the charter was sealed from `$ARGUMENTS` alone (or one clarifying question resolved an
unstated deictic first), the dispatch ran unnamed and synchronous, and its result was relayed
verbatim-in-substance — findings first, never narrated away.
