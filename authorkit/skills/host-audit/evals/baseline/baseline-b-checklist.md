Prompt: "I'm a developer running multi-agent AI coding fleets locally (many git worktrees, each
with its own node_modules, parallel vitest runs with browser shards). Give me a practical
checklist to audit my macOS dev machine's performance and the top actionable fixes, with
warnings."

Answer (fresh general-purpose agent, 2026-08-20, abridged): 8 read-only checks (memory pressure,
orphans, load-vs-cores, disk/worktree sprawl, mds_stores/XProtect, thermal, fd limits, cache
sizes) + 8 fixes with warnings (orphan reaper, global concurrency cap, Spotlight Privacy pane +
tmutil, worktree pruning, fd limits, caffeinate, disk headroom, pnpm). STRONG — but this agent
had inherited the project's memory (it cites our own recorded traps verbatim), i.e. it was
answering with the incident's lessons already in context. Still absent: a runnable probe
producing machine-readable evidence, the .metadata_never_index recursive-marker mechanism,
tmutil ISEXCLUDED as a check (only the fix), branch-merged-vs-parked worktree census, and a
uniform finding schema (measured number → mechanism → command → severity → tier).
