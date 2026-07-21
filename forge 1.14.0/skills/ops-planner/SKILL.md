---
name: ops-planner
description: >-
  Run the standing ops-planner seat (agents/ops-planner.md) on demand — standalone, it plans from
  durable .claude/ops state plus live gh evidence and rewrites the prioritized action queue at
  .claude/ops/plan.md; every entry names action, owner, evidence, size. States the seat's
  operating contract as a fixed banner before the first-ever plan. Run /ops-planner [blank, or a
  focus instruction].
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank to (re)plan from current state | a focus instruction, e.g. 'branches and PRs first']"
allowed-tools: ["Read", "Glob", "Agent"]
---

# ops-planner

Dispatches the standing `ops-planner` agent (`agents/ops-planner.md`) on demand — the same
skill↔agent same-name pairing ruled for `/ops-issues` and shared by `/ops-orchestrator`:
`disable-model-invocation: true` keeps this command off every model-routed surface, and the
Agent tool's `subagent_type` namespace is disjoint from the Skill tool's; the ruling's full
mechanics live in `/ops-issues`'s body.

## Procedure

1. **Banner check, before anything.** Whenever `.claude/ops/plan.md` does not exist — this seat
   has never written a plan here — show the banner (text below) now, before the dispatch: the
   dispatched planner is what creates that file, so a post-dispatch check destroys its own
   condition. Once it exists, never show it again.
2. **Dispatch.** Call the `ops-planner` agent (Agent tool, `subagent_type: "forge:ops-planner"`),
   carrying `$ARGUMENTS` verbatim — blank to (re)plan from current durable + live state, or a
   focus instruction exactly as the agent's own contract defines (an emphasis, never a new entry
   contract). This command never pre-validates an agent-owned instruction shape; the one
   screening judgment it owns is failure branch 2's redirect.
3. **Relay.** Return the agent's own final report unmodified — verdict line plus its top three
   entries; the full queue lives in the plan file.

## The banner

```
ops-planner — the prioritization seat for this repo's ops backlog.

What it does: turns ops state + live gh evidence into one prioritized action queue
(.claude/ops/plan.md); every entry names action, owner, evidence, and size.
What it never does: execute anything it queues — that one plan file is its entire write surface.
```

## Failure branches

- The Agent tool dispatch itself fails to return (a tool error, not an agent-reported failure) →
  report the dispatch failure plainly; never fabricate a plan or a report.
- The ask is really a fresh sweep ("run everything, then tell me what's first") → name
  `/ops-orchestrator` as the right door and do not dispatch; chaining the fan-out from here would
  duplicate the orchestrator's contract in a second home.
- A human asks to see the banner again after a plan file exists → answer inline from the banner
  text above; a disclosure re-read never costs a dispatch.

Done when the banner was shown before the dispatch whenever step 1's condition held, the agent
has been dispatched, and its final report has been relayed unmodified. NOT done while the banner
check ran after the dispatch that creates the plan file, a dispatch failure reads as an agent
report, or the banner condition checked anything other than the plan file's existence.
