# Baseline — without mobilize-chores (2026-08-07)

Prompt: fresh general-purpose agent, given the real `.claude/ops/plan.md` queue, asked to
describe (not execute) what it would do to "mobilize whatever's ready to build."

## Raw output

Read `.claude/ops/plan.md` (75 lines, dispatched 2026-07-25 by `chore-planner`). Below is exactly what I would do — described, not executed.

### Classification: what's actually "ready to build"

The plan's own **Owner** field is the buildability test — an item is dispatchable only if its owner is an agent/seat, not a human judgment call.

| # | Item | Owner (as written) | Buildable now? |
|---|---|---|---|
| 1 | Record `github_mcp_offer` decision | human (the decision) + issue-sorter (the recording) | **No** |
| 2 | Decision-watcher sweep for ADR-0006/0007/0008 | decision-watcher | **Yes** — queues candidates, mutates nothing, no human input needed to start |
| 3 | Fix stale cloud-routine prompt path | human (CronUpdate) | **No** |

So exactly one item (#2) clears the bar.

### What I'd dispatch

Only #2 — `harness:decision-watcher`, on-demand direct dispatch.

### Confirmation

"#2: no confirmation needed before dispatch. It's non-mutating (queue-only) ... Auto-mode bias
toward action applies cleanly here since the action is reversible and low-blast-radius."

### How I'd report

Verdict-first 🟢/🟡/🔴 shape, per item.

## Gaps this exposes (why mobilize-chores exists)

1. **Skipped the confirm gate on its own judgment.** The baseline decided dispatch #2 needed no
   human confirmation because it judged the risk "low" — exactly the kind of per-dispatch risk
   call assertion 2 forbids. `mobilize-chores` must get ONE batched confirm before ANY dispatch,
   never skip it by its own risk assessment, however reasonable that assessment looks in isolation.
2. **Ad hoc buildability heuristic.** The baseline invented "is the Owner field an agent" as its
   test, re-derived fresh from plan.md's prose each time. That's inconsistent and re-litigated
   per run. `mobilize-chores` needs one crisp, stable rule tied to the actual TICKET kind (a filed
   `kind: bug`/`kind: feature` record), not a re-read of whichever prose happens to be in
   plan.md's Owner column this time.
3. **Scope-sharpening finding:** this particular queue had ZERO feature/bug ticket items — all
   three entries were ops/hygiene actions (agent dispatch, human decision, config edit), none of
   them build-feature-shaped. Confirms the fence is doing real work: `mobilize-chores` only ever
   mobilizes filed bug/feature tickets through `build-feature`; an ops-queue action like "run
   decision-watcher" is out of its scope entirely and reports as skipped, not mobilized — even
   though a reasonable ad hoc agent (this baseline) treated it as fair game.
