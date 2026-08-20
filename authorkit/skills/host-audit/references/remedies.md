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
Trigger: `worktreeHomes[].ownNodeModules` ≥ 2 with `parked` high; `nodeModulesDiskMB` states the
measured aggregate cost (null = du exceeded the probe budget — report the gap, don't guess).
Mechanism: each worktree install writes ~1–2 GB and re-triggers F1/F2; the incident ran seven;
a second live census (gen-ui-kit, 2026-08-20) found 17 worktrees, 7 with their own node_modules.
Fix (safe): symlink the main checkout's node_modules into worktrees when the lockfile is
unchanged (`git diff --quiet origin/main -- package-lock.json && ln -s <root>/node_modules ...`);
`npm ci --prefer-offline` only when it changed.
Fix (changes-system-behavior, pnpm repos): a shared lockfile-hash-keyed pnpm virtual store
(`pnpm config set store-dir <shared path>` per worktree, keyed so a changed lockfile gets its own
store) — designed live on the 2026-08-20 gen-ui-kit host but NOT yet built there; it named two
verification steps as prerequisites (prove hard-links survive the worktree filesystem layout;
prove a concurrent install in two worktrees doesn't corrupt the store). Side effect: every
worktree's installs now share one on-disk store — a corruption or manual deletion there breaks
ALL worktrees at once, not one. Recommend only as the structural option with those prerequisites
stated — never as a one-command fix.
Warning: resolution correctness depends on the lockfile check — a worktree that CHANGES deps
must install for real. A mixed `pkgManagers` census (some homes pnpm, some npm) is additionally
the precondition for local-vs-CI dist drift (pnpm-bootstrapped bundles measured 25–30% larger
than npm-ci builds, gen-ui-kit P4) — that drift is a REPO gate's job to catch, not this audit's;
report the mix as informational and name the missing parity check.

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

## F10 — Gate-lane oversubscription (the cause-side twin of F3)
Trigger: `devProcs.testRunners.count` ≥ `cores` while `load.perCore1m` ≥ 1.5 — runnable test
workers at or above core count, live at probe time (both fields already in the probe JSON; no
new probe needed).
Mechanism: the host repo's own check chain fans out N gate lanes with no concurrency cap, each
lane spawning workers-per-core — F3 measures the resulting load; this class names the config
that produces it. Incident: a 7-minute contended run observed directly (gen-ui-kit, 2026-08-20)
on a chain with no self-limit; the forging incident's 7 lanes × workers-per-core is the same
shape.
Fix (safe): the durable form is REPO-side — add a lane cap to the repo's own check chain (a
`--maxWorkers` / `-j` flag, or a queue wrapper) so the fix survives this host; the session-side
stopgap is F3's cap. Both are scheduling discipline, no side effects.
Fence: whether a RED run under this contention is trustworthy is the host repo's `flaky-gates`
call (red-under-load vs green-in-isolation) — this class only reports that the host is
oversubscribed by design; it never judges a specific red.

## Non-macOS
Every threshold above except F3/F5/F6/F8/F9/F10 leans on macOS-specific probes (mds, tmutil,
vm_stat). On linux/win32 the probe returns `verified: false` and `macos: null` — report the
portable findings (F3/F5/F6/F8/F9/F10) and NAME the gap ("indexer/backup probes unverified on
this platform — contributions welcome"); never present improvised equivalents as verified.
