# Baseline (no concurrency-design skill) — "set up this repo so multiple Claude sessions don't collide"

Captured 2026-07-17, fresh general-purpose agent, no tools, no repo context beyond ambient memory.

## Response

Multiple Claude Code sessions colliding is almost always a **shared git working tree** problem — two sessions editing files, staging, and committing against the same index at once, or racing on build output (`dist/`, `node_modules/.vite`, etc.). The fix isn't a setting, it's giving each session its own physical workspace. A few layers, roughly in order of how much they buy you:

**1. Git worktree per session — the actual fix**
```
git worktree add ../agent-ui-tkt-0072 -b feat/tkt-0072
```
Each Claude session `cd`s into its own worktree on its own branch. They share the same `.git`, so history/objects are shared, but the working directory and index are separate — no more "session B's edit vanished because session A's commit raced it." When done: `git worktree remove` and normal PR/merge flow to get the branches back into `main`.

In this harness specifically, you get this almost for free:
- The `Agent` tool takes `isolation: "worktree"` — a subagent gets an auto-created worktree, cleaned up automatically if it made no changes.
- There are also standalone `EnterWorktree`/`ExitWorktree` tools if you want to manually park a whole session in an isolated worktree rather than delegate to a subagent.

If you're instead running several independent `claude` CLI processes by hand (separate terminal tabs, not subagents), you want the manual `git worktree add` version above — never point two live sessions at the same checkout.

**2. Non-overlapping work assignment, not file locking**
Worktrees solve the filesystem race but not "two sessions both decide to fix the same bug." [...] each session/subagent should be briefed by name with a specific ticket or scope, and should stay idle rather than grab unclaimed work.

**3. Guardrails around shared mutable state** — serialize installs, commit small and often per branch.

**4. What *not* to reach for** — `settings.json` permissions don't address concurrency; don't reach for a lockfile-in-the-repo convention.

## Gaps vs. the skill (annotated post-hoc)

- Frames `EnterWorktree` as something you "get almost for free" — misses that it's OPT-IN ONLY (its own tool contract requires an explicit trigger) and nothing routes a session into it automatically without a standing CLAUDE.md rule.
- No mention of ticket-status (`doing`) as a cheap pre-flight signal.
- No mention of the mid-task discovery branch (what to do when you're already elbow-deep and find a collision) — entirely a "set up in advance" answer.
- No distinction between subagents-I-spawned (addressable, controllable) vs. independent concurrent sessions (opaque, must route through the human) vs. sessions reachable as SendMessage teammates.
