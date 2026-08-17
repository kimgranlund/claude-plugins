# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-17 ~11:42Z window (UTC).
Checkout at plan time: branch `fix-423-fleet-bootstrap-phase1` @ `fc3942c` (NOT main; local
`main` is behind `origin/main` by 31 — see entry 5). Evidence: all three seat reports attached,
none UNMEASURED — decision-watcher (`reports/2026-08-17T11-39-56Z-decision-watcher.md`: 0
candidates, adr-0014 rejected as already-harvested duplicate, checkpoint advanced, ADR queue
empty), issue-sorter (`reports/2026-08-17T11-39-41Z-issue-sorter.md`: 92 issues touched
in-window, 90 closed; exactly 2 open — #475 small/unclaimed/buildable, #295 big/active-WIP;
0 open PRs; nothing minted or held), repo-cleaner
(`reports/2026-08-17T11-41-41Z-repo-cleaner.md`: executed `campaign_close.py 441` clean —
merged PR's remote branch deleted and reverified gone; 23 fully-merged worktrees + ~8
superseded scratch branches PROPOSED for human cleanup; locked `issue-475-teamwork-diet`
worktree flagged distinctly; gitignore WARN `harness-audit-*/` stale, no edit proposed).

Prior plan (2026-08-16 ~01:12Z) is fully resolved: ops commit landed; the adr-0013+adr-0012
batched confirm EXECUTED between sweeps (decision-watcher: queue still empty, 0 pending);
#258 CLOSED (its defer-ruling retires with it); the 11-issue backlog drained to 2 (90 closed
in-window). Queue rebuilds 4 → 5.

**Blocked-by (#193):** no `Blocked-by:` line in any evidence this sweep — ordering below is
pure class ranking.

**Drain note (this dispatch):** unattended overnight drain, PR-opened ceiling, no auto-merge.
Class-3 entries below WAIT for Kim — the drain skips them and proceeds to entry 4, the sole
buildable item. Skipping a human-decision entry to reach a buildable one is expected, not a
violation of queue order.

## Human-decision call-outs — nothing below executes autonomously

1. **Worktree/branch batch cleanup** (entry 2) — propose-only per repo-cleaner's contract (no
   host reap script named in this repo's docs); only Kim runs the removals.
2. **Locked-worktree ruling** (entry 3) — a lock is normally deliberate; only Kim decides
   stale vs. intentional.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Read `git status --porcelain` first, then stage exactly
  `git add .claude/ops/plan.md .claude/ops/adr-checkpoint.json
  .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-17T11-39-56Z-decision-watcher.md
  .claude/ops/reports/2026-08-17T11-39-41Z-issue-sorter.md
  .claude/ops/reports/2026-08-17T11-41-41Z-repo-cleaner.md`, read the status output, commit
  as a separate step (gate ≠ commit), push. Never `git add -A` — the same checkout carries
  this session's own live edits (`.claude/ops/fleet-roster.md`, `.claude/settings.json`,
  `attention-trend.csv`), which repo-cleaner classified as in-progress session state, not
  this firing's delta. Note the commit rides branch `fix-423-fleet-bootstrap-phase1`, not
  main — it reaches main with that branch's own PR.
- **Owner:** the dispatching session if Bash-capable, else human (Kim).
- **Evidence:** repo-cleaner's checkout inventory names exactly these seat-payload files +
  reports as this sweep's delta and the three session-live files as out of scope.
- **Size:** ~2 min.

(`campaign_close.py 441` — the only other class-1 candidate this sweep — was already executed
by repo-cleaner and reverified clean. Recorded under Resolved, not queued.)

**Class 2 — items blocking other work:**

(None. Zero open PRs, zero `Blocked-by:` edges, nothing named as blocking anything.)

**Class 3 — human decisions:**

### 2. Batched confirm + run: remove 23 fully-merged worktrees and ~8 superseded scratch branches
- **Action:** One batched confirm over repo-cleaner's proposed list, then human-run
  `git worktree remove` + `git branch -D` per item. The full itemized list (each independently
  diffed 0-unique-commits vs. `origin/main`, remote branches already pruned) lives in
  `.claude/ops/reports/2026-08-17T11-41-41Z-repo-cleaner.md` — 23 worktrees under
  `.claude/worktrees/` plus scratch branches `build-425-work`, `restack-425-work`,
  `build-429-orchestrator-introduction`, `build-430-work`, `build-432-work`,
  `restack-432-work`, `restack-437-work`, `worktree-build-426-seat-retirement`, and the
  `pr442-finalize` worktree/branch (5 "ahead" commits are pre-squash lineage of merged #442 —
  superseded, same disposition). EXCLUDES `issue-475-teamwork-diet` (entry 3 owns it).
- **Owner:** human (Kim) — no gated mutation path exists for local worktrees/branches here.
- **Evidence:** repo-cleaner this sweep — per-item merge verification, `gh pr list --state
  open` → zero, both fetch-prunes clean.
- **Size:** ~10–15 min.

### 3. Locked worktree `issue-475-teamwork-diet` — rule the lock stale or intentional
- **Action:** Decide whether the lock is a live claim or leftover. Commit evidence says safe
  (0 unique commits vs. `origin/main`, content fully merged), but issue #475 is open and was
  updated 10 min before the sweep — if the lock was a deliberate claim, removing it destroys
  a signal. If ruled stale: unlock + remove alongside entry 2. Until ruled, entry 4's build
  must not reuse or remove this worktree.
- **Owner:** human (Kim).
- **Evidence:** repo-cleaner's distinct flag (locked, 0 unique commits, matching open issue).
- **Size:** ~2 min.

**Class 4 — hygiene debt / backlog drain:**

### 4. Build #475 — teamwork residual description diet (size:small, unclaimed, buildable)
- **Action:** Dispatch via teamwork's `build-leader`, ceiling PR-opened (no auto-merge — no
  `auto-merge: authorized` grant in this dispatch). Fresh branch + fresh worktree ONLY: the
  existing locked `issue-475-teamwork-diet` worktree is entry 3's to rule on — do not reuse,
  unlock, or remove it. Description edits are routing-surface edits: same-change
  `evals/evals.json` updates and the fresh-context checker pass per the semantic-edit
  invariant apply inside the build loop.
- **Owner:** dispatching session → teamwork `build-leader` seat.
- **Evidence:** issue-sorter this sweep — #475 open, size:small, unclaimed, buildable; the
  only idle buildable item (the other open issue, #295, is active WIP — see Not queued).
- **Size:** ~30–60 min.

### 5. Refresh local `main` — behind `origin/main` by 31
- **Action:** In an ATTENDED session, `python3 harness/scripts/sync_main.py` (quarantine any
  dirt as a named stash, `--ff-only` pull, reverify HEAD by SHA). Interactive-only per its
  contract — repo-cleaner correctly skipped it unattended; not for the overnight drain.
- **Owner:** human (Kim), or any attended session.
- **Evidence:** repo-cleaner inventory — `main` behind by 31, no worktree of its own, healthy
  but stale.
- **Size:** ~2 min.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **#295 (Doctrine ablation program):** open and size:big but carrying active in-progress
  ablation-agent Findings under a standing overnight directive — NOT idle. Do not dispatch
  build-leader at it; it owns its own lifecycle. Issue-sorter re-checks each sweep.
- **ADR queue:** empty — adr-0014 correctly rejected as duplicate (already harvested verbatim
  into authorkit's GRAMMAR.md). No confirm owed.
- **PR estate:** zero open; #437 CLOSED-unmerged is a recorded duplicate of merged #439, not
  a finding.
- **Session-live tracked edits** (`fleet-roster.md`, `settings.json`, `attention-trend.csv`)
  on `fix-423-fleet-bootstrap-phase1`: live in-progress state, not cruft (repo-cleaner
  concurs); excluded from entry 1's pathspec.
- **`.gitignore` WARN `harness-audit-*/`:** stale-looking (matches nothing in-tree) but
  on-demand-generated; no edit proposed (repo-cleaner concurs). If the generating path is
  ever retired for real, repair the rule in that same change per
  `.claude/rules/gitignore-repair.md`. Recorded judgment, not a task.
- **Root entry-file freshness CI gate:** deliberate NO (Kim, 2026-08-15) — ruling carried, do
  not re-propose.
- **Checkpoint-bypass:** accepted one-off (Kim, 2026-08-14); re-litigate only on recurrence —
  ruling carried.
- **#258 defer-ruling:** RETIRED — the issue closed between sweeps; nothing left to defer.

## Resolved since the prior plan (2026-08-16 ~01:12Z sweep)

- Prior entry 1 (commit ops artifacts) — DONE.
- Prior entry 2 (adr-0013 harvest + adr-0012 stale-citation batched confirm) — EXECUTED
  between sweeps; decision-watcher confirms the ADR queue empty, 0 pending.
- Prior entry 3 (#258 bloat-audit, deferred by ruling) — issue CLOSED between sweeps.
- Prior entry 4 (11-issue backlog tracking) — drained 11 → 2 open (90 issues closed
  in-window, all by trusted author).
- New this sweep, already executed by its seat: `campaign_close.py 441` — merged PR #441's
  remote branch deleted and reverified gone; 24 stale remote-tracking refs pruned.
