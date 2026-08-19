# Remedy catalog — finding class → threshold → fix → warning tier

Every entry grounded in the 2026-08-19/20 load-108 incident (agent-ui, M4 MacBook Air, 10 cores:
load 108–180, ten suites red identically on clean main, root-caused live). Warning tiers:
**safe** (read-only or trivially reversible) · **needs-sudo** (privileged, user runs it) ·
**changes-system-behavior** (side effects beyond performance — the warning names them).

## F1 — Spotlight indexing dev churn
Trigger: `macos.indexers.cpuPct` ≥ 50, or any `worktreeHomes[].spotlightMarker == false`.
Mechanism: `mds_stores`/`corespotlightd` re-index every `npm install`'s tens of thousands of
files; incident measured 127% + 87% + 70% CPU on the indexer trio alone.
Fix (safe): `touch <each worktree home>/.metadata_never_index` — Spotlight skips the dir
recursively, covers future worktrees, needs no sudo. Sweep form:
`find ~/Projects -type d \( -path '*/.claude/worktrees' -o -path '*/.agents/worktrees' \) -prune -exec touch {}/.metadata_never_index \;`
Warning (changes-system-behavior): Finder/Spotlight search stops working inside excluded dirs.
The GUI alternative (System Settings → Spotlight → Search Privacy) takes literal paths only.

## F2 — Time Machine including dev trees
Trigger: `macos.tmExcluded.home == false` (and repoRoot false).
Mechanism: every node_modules churn becomes backup delta; `backupd` competes during fleet runs.
Fix (needs-sudo): `sudo tmutil addexclusion -p ~/Projects` (`-p` = sticky path exclusion,
visible in TM settings). Verify: `tmutil isexcluded ~/Projects` → `[Excluded]`.
Warning (changes-system-behavior): source under the path is NO LONGER BACKED UP — only safe when
repos live on a remote (verify `git remote -v` before recommending).

## F3 — Load over core capacity
Trigger: `load.perCore1m` ≥ 1.5 (incident: 10.8–18×).
Mechanism: N parallel lanes × workers-per-core test runners = N×cores runnable threads; hooks
and 10s test setups can't schedule — red gates that reproduce on clean main (contention
masquerading as regression: verify red-in-isolation before trusting ANY failure seen under load).
Fix (safe): cap concurrent gate-running lanes at ~`(cores − 2) / 3`; add `--maxWorkers=<4>` (or
the runner's equivalent) to each lane's test command; queue, don't fan out.
Warning: none — pure scheduling discipline.

## F4 — Orphaned dev processes
Trigger: `devProcs.browsers.oldestEtime` or `testRunners.oldestEtime` in hours while no session
that old is live; counts ≫ live lanes.
Mechanism: crashed/killed sessions leave headless browsers + runner workers consuming CPU/RAM.
Fix (safe, but match NARROWLY): identify by pid + etime (`ps -axo pid,etime,command | grep -E
'headless|vitest'`) and kill the specific pids.
Warning (changes-system-behavior): a broad `pkill node` kills LIVE agents including the one
running the audit; never suggest pattern-kills, only pid lists the user reviews.

## F5 — Per-lane npm install churn
Trigger: `worktreeHomes[].ownNodeModules` ≥ 2 with `parked` high.
Mechanism: each worktree install writes ~1–2 GB and re-triggers F1/F2; the incident ran seven.
Fix (safe): symlink the main checkout's node_modules into worktrees when the lockfile is
unchanged (`git diff --quiet origin/main -- package-lock.json && ln -s <root>/node_modules ...`);
`npm ci --prefer-offline` only when it changed.
Warning: resolution correctness depends on the lockfile check — a worktree that CHANGES deps
must install for real.

## F6 — Parked worktrees
Trigger: `gitWorktrees` ≫ live lanes, or `worktreeHomes[].parked` > 3.
Mechanism: every parked tree is a full node_modules the indexer/backup keep re-scanning.
Fix (safe): reap on lane-return — `git worktree remove <wt>` for clean trees on merged branches;
propose-only for anything dirty or locked.
Warning: verify `git -C <wt> status --porcelain` empty AND the branch provably merged first —
never reap a live lane.

## F7 — Memory pressure / swap
Trigger: `memory.freeMB` < 5% of total with `macos.pageouts` climbing, or swapUsed in GB.
Mechanism: each browser shard 0.3–1.5 GB, each runner worker 0.2–2 GB; paging multiplies every
other finding.
Fix (safe): same as F3 (fewer concurrent lanes/workers) — memory follows the process count.
Warning: none.

## F8 — Disk headroom
Trigger: `diskFreePct` < 15.
Mechanism: APFS slows markedly when nearly full; caches + parked worktrees are the usual bulk.
Fix (safe): F6's reap + cache pruning (`npm cache verify`, old playwright browser builds).
Warning: playwright cache purges force a large re-download on next run.

## F9 — File-descriptor ceiling
Trigger: `fdSoftLimit` ≤ 256 AND the user reports EMFILE/watcher flakes.
Mechanism: parallel vite dev servers + watchers + browsers exhaust the default soft limit.
Fix (safe): `ulimit -n 10240` in the shell profile.
Warning (changes-system-behavior): the LaunchDaemon route (`launchctl limit maxfiles`) needs a
reboot and SIP-aware setup — recommend the shell-profile form first.

## Non-macOS
Every threshold above except F3/F5/F6/F8/F9 leans on macOS-specific probes (mds, tmutil,
vm_stat). On linux/win32 the probe returns `verified: false` and `macos: null` — report the
portable findings (F3/F5/F6/F8/F9) and NAME the gap ("indexer/backup probes unverified on this
platform — contributions welcome"); never present improvised equivalents as verified.
