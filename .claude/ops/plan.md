# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-09 (13:44Z window close), main
@ e2147cd. Evidence: the three seat reports attached to this dispatch (decision-watcher,
issue-sorter, repo-cleaner — none UNMEASURED), plus the prior plan (2026-08-09, 13:18Z
sweep) read as carry-forward source. Nothing refetched. Three prior entries RESOLVED
(branch reap, artifact commit, and #135 — built and merged as PR #148), four carried
forward, one new.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Delete the merged local branch `mobilize-chores-feature-dispatch`
- **Action:** `git branch -d mobilize-chores-feature-dispatch` from the main worktree at
  /Users/kimba/Projects/nonoun/plugins. `-d` (not `-D`) — git's own merged-check is a
  second gate on top of the seat's verification.
- **Owner:** chore-lead (the dispatching session), else human — repo-cleaner is
  propose-only here by contract (no script in its gate set covers local-branch deletion,
  and it re-confirmed this repo ships no host-owned reap script — no `package.json`
  anywhere).
- **Evidence:** repo-cleaner this sweep — fully merged into main, remote branch
  independently reverified gone via `git ls-remote` + `git fetch --prune`, no worktree
  attached. Same class as the two prior firings' now-resolved
  `mobilize-chores-backend-resolve` and `close-session-file-leftovers`.
- **Size:** ~1 min.

### 2. Commit this firing's applied ops artifacts to main
- **Action:** `git add` the payloads chore-lead applied this firing —
  `.claude/ops/watch-checkpoint.json` (timestamp advanced past 13:18:48Z; issue-sorter
  names this advance as its only change), `.claude/ops/reports/2026-08-09T13-44-58Z.md`
  (new), and this rewritten `plan.md` — read the status output first, then commit as a
  separate step (gate ≠ commit). The adr payloads are byte-identical to committed state
  (decision-watcher: confirmed no-op) — nothing to stage there. Direct-to-main is the
  solo ops-artifact case per the prior sweeps' precedent.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** issue-sorter — "watch-checkpoint.json timestamp advance is the only
  change, already applied"; repo-cleaner's full report is new at its named path;
  decision-watcher — checkpoint payload byte-identical to checked-in state.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 3. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 7th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify in the routine
  config that the schedule is still armed — sweep dispatches advance
  `watch-checkpoint.json` themselves, so a checkpoint gap cannot prove the routine dead.
  Seventh consecutive plan appearance: if this is a deliberate no, record that instead so
  this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan via the prior plan's entry 3; no
  seat this sweep reported the prompt fixed. Blocks unattended issue intake between
  sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 4. Apply or rescind the standing `github_mcp_offer:accepted` decision (carry-forward)
- **Action:** Either write the merged `.mcp.json` entry the accepted offer describes
  (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record with a
  dated rescinding note. One-time action — issue-sorter's step-8 gate correctly stayed
  silent again this firing ("accepted" recorded), so no future firing will resurface
  this on its own.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter this sweep — step 8 not-applicable, `github_mcp_offer`
  already terminal "accepted" in `friendlies.json`'s policy block; still no `.mcp.json`
  write in evidence since 2026-07-25.
- **Size:** ~10 min.

### 5. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  A "no" fully clears the decision-watcher surface (its queue is empty).
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record
  change).
- **Evidence:** carry-forward from the prior plan's entry 6; decision-watcher this sweep
  made no new judgments (zero delta across all 9 ADRs, `adr-queue.json` empty), leaving
  the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 6. Disposition issue #139 — platform-level gap, not actionable from this repo (carry-forward)
- **Action:** Decide: keep #139 open as a tracking marker for the upstream platform gap
  (the cd-into-primary compound-command escape of the git-only worktree guard), or close
  it with a pointer to wherever the gap is actually actionable. Either outcome is fine;
  the debt is that it sits in the open roster looking like local work — now the ONLY
  open item in the entire repo.
- **Owner:** human.
- **Evidence:** carry-forward from the prior plan's entry 7; issue-sorter and
  repo-cleaner this sweep both confirm it open (labels task/size:small), unassigned,
  last updated 2026-08-08, fully triaged, unchanged.
- **Size:** ~5 min.

## Not queued (checked, found clean this sweep)

- ADR review: quiescent — all 9 ADRs classified against `adr-checkpoint.json` with zero
  delta, no harvest or stale-citation candidates, queue empty, checkpoint payload
  byte-identical (decision-watcher).
- Issue intake: quiescent — the window since 13:18:48Z returned exactly the #135 closure
  and PR #148's merge, both by the trusted author; #135's comment thread checked
  directly: complete design→build→merge→close arc, no untriaged remainder; zero new
  filings, zero held items, `friendlies.json` and `held-items.md` unchanged
  (issue-sorter).
- PR #148 (teamwork 1.3.0, resolving #135) — MERGED 2026-08-09T13:41:47Z; its
  `campaign_close.py` closure independently reverified: merge commit e2147cd matches
  current main HEAD, remote branch confirmed gone (repo-cleaner). Only its local branch
  remains — that is entry 1.
- All 93 PRs MERGED, zero open; one open issue total (#139 — entry 6) (repo-cleaner).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`) — re-reviewed again,
  confirmed on-demand-generated paths, deliberately kept, no edit (repo-cleaner).

## Resolved since the prior plan (2026-08-09, 13:18Z sweep)

- Prior entry 1 (delete `close-session-file-leftovers`) — RESOLVED: gone from disk
  between firings (repo-cleaner); succeeded by entry 1 for the newly-appeared
  `mobilize-chores-feature-dispatch`.
- Prior entry 2 (commit the 13:18Z firing's applied artifacts) — RESOLVED: repo-cleaner
  found no dirty main this firing and its prior report sits committed at its path;
  succeeded by entry 2 for this firing's own artifacts.
- Prior entry 4 (decide issue #135) — RESOLVED by building it: PR #148 (teamwork 1.3.0)
  MERGED 2026-08-09T13:41:47Z, #135 CLOSED and labeled `done`, remote branch reverified
  gone, comment thread shows the full arc closed (issue-sorter, repo-cleaner).
  Local-branch remainder is entry 1.
- Prior entries 3, 5, 6, 7 — carried forward as entries 3, 4, 5, and 6 respectively.
