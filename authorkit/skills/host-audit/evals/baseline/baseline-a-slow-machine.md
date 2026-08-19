Prompt: "My MacBook (M4, macOS) gets extremely slow whenever I run several Claude Code agent
sessions in parallel — load average climbs over 100, test suites start timing out with 'Hook
timed out in 10000ms'... how do I figure out what's actually wrong and improve performance?"

Answer (fresh general-purpose agent, 2026-08-20, abridged to the diagnostic skeleton): top -o cpu;
count vitest/chromium/node processes; look for orphans by etime; memory_pressure/vm_stat;
pmset -g thermlog; interpret hook-timeout as a load symptom; quantify per-session cost; fixes =
reap orphans, cap vitest workers, serialize the browser gate via lockfile, reduce sessions, slim
hooks. NOTABLY ABSENT: Spotlight/mds_stores as a cause, Time Machine inclusion, worktree/
node_modules churn as the indexing trigger, .metadata_never_index, tmutil isexcluded, any
machine-readable output, any warning-tier framing. (Full transcript in the session task log.)
