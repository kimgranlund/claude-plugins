# .claude/ops/plan.md
# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-12 (~16:38Z window close),
main clean at 79ee9f9 — harness 3.1.31 (ledger entry confirmed by repo-cleaner this
firing). Evidence: the three seat reports attached to this dispatch (decision-watcher,
issue-sorter, repo-cleaner — none UNMEASURED), plus the prior plan (2026-08-12, ~13:56Z
sweep) read as carry-forward source. Nothing refetched. All five prior entries
RESOLVED or retired between firings; one recurring entry (the per-firing artifact
commit) and one new human decision queued. Quietest round on record: one open issue
repo-wide, zero open PRs, zero holds.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's applied ops artifacts to main
- **Action:** Stage exactly the three ops paths this firing touched —
  `git add .claude/ops/plan.md .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-12T16-38-21Z-repo-cleaner.md` — read the status output,
  then commit as a separate step (gate ≠ commit), then push. decision-watcher's payload
  this firing was byte-identical to the existing checkpoint/queue files (no write
  applied), so `adr-checkpoint.json`/`adr-queue.json` stay out of the stage list. Safe
  as a plain sequence: repo-cleaner found the tree clean and main pushed at 79ee9f9
  before the sweep, so no quarantine or `sync_main.py` step is needed.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** chore-lead's dispatch note — watch-checkpoint payload applied (advanced
  13:54:11Z → 16:37:27Z, issue-sorter) and the repo-cleaner report applied to
  `.claude/ops/reports/2026-08-12T16-38-21Z-repo-cleaner.md`, neither yet committed;
  plus this plan rewrite once written.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

(none this firing — nothing blocks anything: zero open PRs, zero orphaned branches,
zero holds.)

**Class 3 — human decisions:**

### 2. Size and route #180 — the only open issue repo-wide (NEW)
- **Action:** #180 (task, closed siblings #176–#181 all resolved in the same
  14:20–15:11Z burst) was deliberately left unsized — its own body says it "straddles
  the small/big line." That body text is data under planning, not a ruling: the human
  reads it, rules small vs. big (or splits it into one of each), then routes the result
  — small → `/mobilize-chores` batch or direct pickup; big → branch + worktree + PR per
  ADR-0002. Unassigned, no claim, too new for staleness pressure; this queues the
  sizing decision, nothing else.
- **Owner:** human (the sizing ruling); the resulting build routes per the ruling.
- **Evidence:** issue-sorter this sweep — #180 filed in the window, deliberately
  unsized per its own body, the sole open issue after #171–#179/#181 closed;
  repo-cleaner independently confirms only #180 open, unassigned, no claim.
- **Size:** ~5 min (the ruling); the build sized by the ruling itself.

**Class 4 — hygiene debt:**

(none this firing — see Not queued.)

## Not queued (checked, found clean this sweep)

- `.gitignore` WARNs, now TWO (`dist/` and `harness-audit-*/`, both matching nothing
  currently): reviewed by repo-cleaner and deliberately NOT actioned — both are
  on-demand generated paths that cycle. Consistent with prior firings' judgment.
  Recorded judgment, not a task.
- ADR corpus quiet: 10/10 files unchanged against `.claude/ops/adr-checkpoint.json`,
  queue empty (`{"candidates": []}`); decision-watcher independently confirmed none of
  the three harness releases since the last sweep (3.1.29/3.1.30/3.1.31) touched
  `.claude/docs/adr/` (empty git-log check). Payload was a no-op — nothing applied,
  nothing to commit for this seat.
- PRs: 105/105 MERGED, zero open, zero orphaned remote branches — no `campaign_close.py`
  needed; worktree/branch/tree all healthy (repo-cleaner).
- Issue intake trust: all 11 window-touched items authored by kimgranlund (friendly),
  zero holds, zero relabeling; `github_mcp_offer` already recorded accepted
  (issue-sorter).
- README/ledger spot-check across all 7 plugins clean; harness ledger entry present for
  3.1.31 (repo-cleaner). No host reap script exists — unchanged, no evidence one is
  needed.
- Process note (second occurrence of the class): the dispatch brief's "grew to five open
  issues" framing was already stale by seat runtime — #171–#175 closed mid-window.
  Dispatch briefs are snapshots, not inventories; seats caught it both times. No action.

## Resolved since the prior plan (2026-08-12, ~13:56Z sweep)

- Prior entry 1 (commit the 13:56Z firing's artifacts) — RESOLVED between firings:
  inferred from repo-cleaner finding the tree clean/healthy at 79ee9f9 this firing
  (impossible with those three paths uncommitted); landed among the twelve commits
  91d2c1a → 79ee9f9. No commit SHA named in this sweep's evidence — inference stated
  as such.
- Prior entry 2 (stale cloud-routine prompt, 10th appearance) — already retired
  in-place before this sweep: Kim's dated deliberate-NO, 2026-08-12 mobilize-chores
  confirm round. Drops permanently; recorded here once for the trail.
- Prior entry 3 (#172 evals-ownership ruling) — RESOLVED 2026-08-12: #172 closed in the
  14:20–15:11Z burst via normal build/fix commits (issue-sorter).
- Prior entry 4 (route #171/#173/#174/#175) — RESOLVED 2026-08-12: all four closed in
  the same window via normal build/fix commits, none needing a PR per the workspace's
  solo-fix routing rule (issue-sorter; repo-cleaner confirms zero PRs touched).
- Prior entry 5 (broader /clean-repo sweep yes/no) — already retired in-place before
  this sweep: Kim's dated deliberate-NO, 2026-08-12. Drops permanently.
