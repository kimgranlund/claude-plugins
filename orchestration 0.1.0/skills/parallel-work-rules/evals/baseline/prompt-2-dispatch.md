# Baseline (no concurrency-design skill) — "I'm about to dispatch two builder subagents that will both touch files in the same area — should I do anything special?"

Captured 2026-07-17, fresh general-purpose agent, no tools, no repo context beyond ambient memory.

## Response

Yes — running two builder subagents against overlapping territory is exactly the setup that causes silent collisions [...]

1. **Partition by file, not just by "area."** [...] If the honest answer is "no, they really do need to touch the same file," don't parallelize — serialize them instead.
2. **Use isolated worktrees if the areas can't be cleanly partitioned.** The `Agent` tool's `isolation: "worktree"` option [...]
3. **Tell each agent about the other.** [...]
4. **Re-run the full gate after both land, not just per-agent.** [...]
5. **Don't let a shared task list become an open queue.** [...] each agent should only touch items explicitly assigned to it by name [...]

If the two builders' work is genuinely independent [...] plain background dispatch is fine [...]

## Gaps vs. the skill (annotated post-hoc)

- **Scoped entirely to subagents the user spawns themselves.** The prompt didn't restrict to that case, but the answer never considers that OTHER, non-spawned, fully independent Claude Code sessions might also be concurrently active in the same checkout — which is exactly the actual incident's shape (a third, unrelated session with uncommitted persona-seam edits, discovered mid-build, not one the orchestrating session spawned or could message in advance).
- No mention of ticket-status as a pre-flight check before assuming a scope is safe to claim.
- Solid on same-session multi-agent partitioning (this part the model already does well — not a gap); the gap is entirely at the boundary this skill actually targets: cross-process, not-spawned-by-me concurrency.
