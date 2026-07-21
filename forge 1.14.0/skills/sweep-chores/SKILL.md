---
name: chore-lead
description: >-
  Run one ops-family sweep on demand against this repo — dispatches the standing chore-lead
  agent (agents/chore-lead.md), which fans out decision-watcher + issue-sorter + repo-cleaner in parallel
  and returns chore-planner's single prioritized queue. States the agent's operating contract as a
  fixed banner before the first ops queue exists here. Run /sweep-chores [blank, or a scope
  instruction].
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a full sweep | a scope instruction, e.g. 'repo hygiene only']"
allowed-tools: ["Read", "Glob", "Agent"]
---

# chore-lead

Dispatches the standing `chore-lead` agent (`agents/chore-lead.md`) for an on-demand
sweep — the same skill↔agent same-name pairing ruled for `/sort-issues`, whose body records the
two load-bearing mechanics (exclusion from model routing; disjoint tool namespaces), cited here
rather than restated.

## Procedure

1. **Banner check, before anything.** Whenever `.claude/ops/plan.md` does not exist — no ops
   queue has ever been produced here — show the banner (text below) now, before the dispatch:
   the sweep itself is what creates that file, so a post-dispatch check destroys its own
   condition. Once a plan file exists, never show it again.
2. **Dispatch.** Call the `chore-lead` agent (Agent tool, `subagent_type:
   "harness:chore-lead"`), carrying `$ARGUMENTS` verbatim as the dispatch context — blank for
   a full sweep, or a scope instruction exactly as the agent's own description describes. Which
   seats a scope instruction names is the agent's judgment, never validated here; the one
   screening judgment this command owns is failure branch 2's redirect.
3. **Relay.** Return the agent's own final report unmodified. The banner is the only content this
   command owns; everything else is the agent's report, passed through as-is.

## The banner

```
chore-lead — one-pass sweep coordinator for this repo's ops-* seats (intake · ADR review · repo hygiene).

What it does: fans out the three standing seats in parallel, then chore-planner turns their reports
into one prioritized action queue (.claude/ops/plan.md).
What it never does: edit source, or mutate anything outside a dispatched seat's own gates —
coordination is its entire write surface.
```

## Failure branches

- The Agent tool dispatch itself fails to return (a tool error, not an agent-reported failure) →
  report the dispatch failure plainly; never fabricate a sweep report to fill the gap.
- `$ARGUMENTS` carries one seat's own job with no sweep intent (e.g. "file this bug" — intake, or
  "delete that stale branch" — hygiene) → name the direct door (`/sort-issues`, `repo-cleaner`,
  `decision-watcher`) and do not dispatch; a sweep that exists to wrap one seat's single task is fan-out
  overhead with no roll-up value.
- A human asks to see the banner again after a plan file exists → answer inline from the banner
  text above; a disclosure re-read never costs a three-seat sweep.

Done when the banner was shown before the dispatch whenever step 1's condition held, the agent
has been dispatched, and its final report has been relayed unmodified. NOT done while the banner
check ran after the dispatch that creates the plan file, a dispatch failure reads as an agent
report, or the banner condition checked anything other than the plan file's existence.
