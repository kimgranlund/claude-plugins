---
name: blocked-by-rules
description: >-
  How chore-planner reads a ticket's `Blocked-by: #NN` line and orders .claude/ops/plan.md so a
  blocked action queues behind its blocker, or names the dependency when the blocker isn't itself
  queued (issue #193). Use when asked how chore-planner orders blocked tickets, why one plan.md
  entry sits behind another, or how a `Blocked-by:` line affects queue ranking. NOT for the
  convention's own format or per-backend realization (teamwork's mobilize-chores,
  references/blocked-by-convention.md — the canonical definition); NOT for excluding a ticket from
  mobilize-chores' own mobilizable set (that skill's own step 2 — a different consumer, same
  convention).
disable-model-invocation: false
user-invocable: false
---

# blocked-by-rules

Preloaded by `harness:chore-planner`. Carries the operational half of issue #193's dependency
convention; the format itself is defined once, canonically, in teamwork's `mobilize-chores` skill
(`references/blocked-by-convention.md`) — this file cites it rather than re-defining it, so the
convention keeps exactly one source of truth across both plugins (a cross-plugin MENTION, never a
preload or a `${CLAUDE_PLUGIN_ROOT}` path — this skill stands on its own inside harness even where
teamwork isn't installed, per this workspace's own plugin-boundary rule).

## The format, restated only far enough to read it

A ticket's body may carry a line `Blocked-by: #NN` (or a comma-separated list, `#NN, #MM`) —
case-insensitive key, `#` plus digits per named blocker. No such line → the ticket declares no
blocker; order it exactly as `chore-planner`'s own Queue order section already ranks it.

## Reading it

For every ticket already in evidence — a seat report attached to the dispatch (sweep mode), or a
ticket read live via `gh issue view <id> --json body,state` (standalone mode) — grep its body for
the `Blocked-by:` line, parse the `#NN` list, then resolve each named blocker's own `state` (`gh
issue view <NN> --json state`; batch these, never re-fetch one already resolved this run).

## Ordering the queue

- **No line, or every named blocker is CLOSED** → this convention changes nothing for the entry;
  it orders per `chore-planner`'s existing ranking (gated-mutations → blocking-other-work →
  human-decision → hygiene-debt).
- **Any named blocker still OPEN** → the entry queues BEHIND that blocker's own entry when the
  blocker is itself in this plan; wherever it sits, its own action/owner line ALSO names the open
  dependency inline (e.g. "blocked by #196 (open) — do not start before it closes") so a human
  scanning `plan.md` never has to cross-reference to see why something sits where it does.
- **A named blocker isn't itself in this plan** (already closed, or simply not ops-family work) —
  name it in the entry's own line regardless; nothing here re-derives whether it's actually done,
  that is exactly the `state` check above, already run.

A named blocker's `state` fails to resolve (deleted issue, a reference into another repo, `gh` unreachable)
→ treat it as OPEN (the safer default) and say so in the entry's own line (e.g. "blocked by #NN
(state unresolved — treated as open)"), never silently drop the dependency.

## Non-goals

No auto-detection, no graph, no visualization — reading and ordering only, per #193's own
Scope/Open. Never infer a `Blocked-by:` edge from anything but the literal line.
