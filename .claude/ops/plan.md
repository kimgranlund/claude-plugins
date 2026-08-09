# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-09 (13:03Z window close), main
@ d6e4366. Evidence: the three seat reports attached to this dispatch (decision-watcher,
issue-sorter, repo-cleaner — none UNMEASURED), plus the prior plan (2026-08-09, 12:23Z
sweep) read as carry-forward source. Nothing refetched. One prior entry RESOLVED, four
carried forward (one split into three per-issue entries), two new.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Delete the merged local branch `mobilize-chores-backend-resolve`
- **Action:** `git branch -d mobilize-chores-backend-resolve` from the main worktree. `-d`
  (not `-D`) — git's own merged-check is a second gate on top of the seat's verification.
- **Owner:** chore-lead (the dispatching session), else human — repo-cleaner is propose-only
  here by contract (`campaign_close.py` never touches local branches; no host-owned reap
  script exists yet).
- **Evidence:** repo-cleaner this sweep — fully merged into main (`git branch --merged main`
  confirms), remote branch independently reverified gone via direct `gh api` 404, no
  leftover worktree; PR #146 MERGED.
- **Size:** ~1 min.

### 2. Commit this firing's applied ops artifacts to main
- **Action:** `git add` the payloads chore-lead applied this firing —
  `.claude/ops/reports/2026-08-09T13-03-43Z.md`, `.claude/ops/adr-checkpoint.json`
  (reformatted), `.claude/ops/watch-checkpoint.json` (advanced), and this rewritten
  `plan.md` — read the status output first, then commit as a separate step (gate ≠ commit).
  Direct-to-main is the solo ops-artifact case per the prior sweeps' precedent.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** all three seat reports name their applied payloads this firing; the report
  file was written fresh (no prior file at that path).
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 3. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 5th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify in the routine
  config that the schedule is still armed — sweep dispatches advance
  `watch-checkpoint.json` themselves, so a checkpoint gap cannot prove the routine dead.
  Fifth consecutive plan appearance: if this is a deliberate no, record that instead so
  this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan via the prior plan's entry 2; no
  seat this sweep reported the prompt fixed. Blocks unattended issue intake between sweeps
  while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 4. Decide issue #135 — the mobilize-chores/build-feature dispatch gap (design question)
- **Action:** Answer the open design question and route it: build via `/build-feature`
  (record-first), or record the resolution on the issue. Freshest human signal in the
  backlog — the owner added a `doing` label inside this sweep's window, so direction here
  unblocks the issue the owner is already circling.
- **Owner:** human (design decision; a build then routes through `/build-feature`'s own
  confirm gate).
- **Evidence:** issue-sorter this sweep — `doing` added to already-triaged #135 by the
  trusted owner, no re-classification needed; repo-cleaner confirms it open with no
  ADR-0005 claim (label is an attention signal, not a claim).
- **Size:** ~15 min to decide; build time ticket-dependent (hours) if yes.

### 5. Decide issue #133 — close-session/file-leftovers feature request
- **Action:** Build it (route through `/mobilize-chores` or `/build-feature`, each gated by
  one confirm) or explicitly defer with a note on the issue. Triage-clean and waiting on a
  build decision only.
- **Owner:** human.
- **Evidence:** issue-sorter and repo-cleaner this sweep, independently agreeing: open,
  fully triaged, unclaimed.
- **Size:** ~10 min to decide; build hours if yes.

### 6. Apply or rescind the standing `github_mcp_offer:accepted` decision (carry-forward)
- **Action:** Either write the merged `.mcp.json` entry the accepted offer describes
  (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record with a
  dated rescinding note. One-time action — issue-sorter's step-8 gate correctly stayed
  silent again this firing ("accepted" recorded), so no future firing will resurface this.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter this sweep — step 8 not-applicable, `github_mcp_offer`
  already recorded accepted; still no `.mcp.json` write in evidence since 2026-07-25.
- **Size:** ~10 min.

### 7. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  A "no" fully clears the decision-watcher surface (its queue is empty).
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record
  change).
- **Evidence:** carry-forward from the prior plan's entry 4; decision-watcher this sweep
  made no new judgments (zero delta, all 9 ADRs hash-identical to checkpoint, empty
  queue), leaving the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 8. Disposition issue #139 — platform-level gap, not actionable from this repo
- **Action:** Decide: keep #139 open as a tracking marker for the upstream platform gap,
  or close it with a pointer to wherever the gap is actually actionable. Either outcome is
  fine; the debt is that it sits in the open roster looking like local work.
- **Owner:** human.
- **Evidence:** issue-sorter this sweep — owner Finding on the issue marks it
  not-actionable from this repo (quoted as data under coordination, relayed as a finding);
  repo-cleaner confirms open, unclaimed.
- **Size:** ~5 min.

## Not queued (checked, found clean this sweep)

- ADR review: quiescent — all 9 ADRs content-hash-identical to the checkpoint, no
  new/amended Decisions, no stale-citation grep needed, candidate queue empty, no batched
  confirm (decision-watcher).
- Issue intake: quiescent — zero new filings, zero unknown authors in the
  12:23:41Z→13:03:44Z window; checkpoint advanced; zero items in `needs-triage-approval`
  (issue-sorter).
- PR #146 (teamwork 1.2.1) — merged, trusted author, closure independently reverified
  clean: remote branch 404-confirmed gone, no leftover worktree (repo-cleaner). Only its
  local branch remains — that is entry 1.
- All 91 PRs MERGED, zero open; no stale ADR-0005 claims on any open issue (repo-cleaner).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`) — re-reviewed again,
  confirmed on-demand-generated paths, deliberately kept, no edit (repo-cleaner).

## Resolved since the prior plan (2026-08-09, 12:23Z sweep)

- Prior entry 1 (commit the 12:13Z untracked ops report) — RESOLVED: repo-cleaner's full
  inventory this firing reports no untracked-artifact finding ("everything healthy or
  already-closed except one small, low-risk proposed action"); succeeded by entry 2 for
  this firing's own artifacts.
- Prior entry 5 (route #133/#135/#139 as one block) — SPLIT into per-issue entries 4, 5,
  and 8 on this firing's finer classification (#135 design question with fresh owner
  attention, #133 build decision, #139 not-actionable-here).
- Prior entries 2, 3, 4 — carried forward as entries 3, 6, and 7 respectively.
