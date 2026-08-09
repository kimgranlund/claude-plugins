# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-09 (12:23Z window close). Evidence:
the three seat reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner —
none UNMEASURED), plus the prior plan (2026-08-08, second sweep) read as carry-forward source.
Nothing refetched. Four prior entries RESOLVED on fresh evidence, four carried forward, one new.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit the untracked ops report artifact(s) to main
- **Action:** `git add .claude/ops/reports/2026-08-09T12-13-06Z.md` plus this firing's own
  report file once landed, then commit — read the status output first, commit as a separate
  step (gate ≠ commit). Safe as a direct main commit: HEAD matches origin/main by SHA and the
  tree is otherwise clean, so this is the solo single-file-fix case, no branch needed.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** repo-cleaner report this sweep — the 12:13Z report sits untracked in the
  working tree; explicitly flagged for the dispatching session to commit; not git dirt
  (no `sync_main.py` needed).
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 2. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 4th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify in the routine
  config that the schedule is still armed. Sweep dispatches advance `watch-checkpoint.json`
  themselves, so a checkpoint gap cannot prove the routine dead — the config is the only
  place to verify. Fourth consecutive plan appearance: if this is a deliberate no, record
  that instead so the entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan via the prior plan's entry 1; no seat
  this sweep reported the prompt fixed. Blocks unattended issue intake between sweeps while
  dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 3. Apply or rescind the standing `github_mcp_offer:accepted` decision (carry-forward)
- **Action:** Either write the merged `.mcp.json` entry the accepted offer describes
  (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record with a dated
  rescinding note. One-time action — issue-sorter's step-8 gate correctly stays silent once
  "accepted" is recorded (it did again this firing), so no future firing will resurface this.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter report this sweep — step 8 skipped, "accepted" recorded
  2026-07-25; `friendlies.json` unchanged since; no `.mcp.json` write in evidence.
- **Size:** ~10 min.

### 4. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  decision-watcher chose not to queue it and flagged the call for review; with the adr queue
  now empty, a "no" fully clears the decision-watcher surface.
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record change).
- **Evidence:** carry-forward from the prior plan's entry 6; decision-watcher this sweep made
  no new judgments (clean unchanged firing, empty queue), leaving the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 5. Route the open backlog — #133, #135, #139 — toward triage or build
- **Action:** `/mobilize-chores` (or a direct human pass) over the three open issues. All
  three are kimgranlund-authored, kind-labeled, unclaimed (empty assignees, no 'doing'
  labels, no ADR-0005 claims) — triage-clean and waiting on a build decision only.
- **Owner:** human (launches `/mobilize-chores`; it gates any build behind one confirm).
- **Evidence:** issue-sorter and repo-cleaner reports this sweep, independently agreeing on
  the same three-issue roster.
- **Size:** ~10 min to launch and triage; build time per ticket varies (hours,
  ticket-dependent).

## Not queued (checked, found clean this sweep)

- PRs #143 and #145 — merged; their dangling remote branches were already closed out by the
  earlier 2026-08-09 sweep (12:13Z report); remote refs pruned to `origin/main` alone
  (repo-cleaner).
- 90 PRs all MERGED, zero open, zero orphaned; 1 worktree (main, healthy); 1 local branch,
  HEAD matches origin/main by SHA (repo-cleaner).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`) — re-judged this sweep as
  on-demand-generated paths, not genuine staleness; deliberately kept, no edit recommended
  (repo-cleaner). Retires the prior plan's entry 7.
- Zero raw untriaged filings, zero unknown-author items; `held-items.md` and
  `friendlies.json` unchanged; issue #144 filed and closed within the window via PR #145
  (issue-sorter).
- All 9 ADRs unchanged since the 2026-08-08 checkpoint; adr queue empty; checkpoint applied
  byte-identical (decision-watcher).

## Resolved since the prior plan (2026-08-08, second sweep)

- Prior entry 3 (adr-0006 stale-citation candidate, aging since 2026-07-30) — RESOLVED: the
  candidate queue is empty this firing ("resolved candidates" per decision-watcher);
  corroborated by PR #145's decision-watcher evidence-verification change.
- Prior entry 4 (issue #140 close-or-extend) — RESOLVED: #140 absent from both seats' open
  rosters; the chore-lead narrated-write check shipped in harness 3.1.8 (PR #143).
- Prior entry 5 (issue #138 charter expansion) — RESOLVED: accepted and shipped as the
  repo-cleaner widen in harness 3.1.8 (PR #143); #138 no longer open.
- Prior entry 7 (`.gitignore` WARN lines) — RESOLVED as "deliberately keep" per
  repo-cleaner's fresh on-demand-generated judgment (see Not queued).
- Prior entries 1, 2, 6, 8 — carried forward as entries 2, 3, 4, and 5 respectively.
