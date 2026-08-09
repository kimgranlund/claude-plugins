# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-09 (13:18Z window close), main
@ a65f0a0. Evidence: the three seat reports attached to this dispatch (decision-watcher,
issue-sorter, repo-cleaner — none UNMEASURED), plus the prior plan (2026-08-09, 13:03Z
sweep) read as carry-forward source. Nothing refetched. Three prior entries RESOLVED
(branch reap, artifact commit, #133 — built and merged as PR #147), four carried forward,
two new.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Delete the merged local branch `close-session-file-leftovers`
- **Action:** `git branch -d close-session-file-leftovers` from the main worktree. `-d`
  (not `-D`) — git's own merged-check is a second gate on top of the seat's verification.
- **Owner:** chore-lead (the dispatching session), else human — repo-cleaner is
  propose-only here by contract (`campaign_close.py` never touches local branches; its
  reap-script check this firing confirmed no host-repo reap script exists — no
  `package.json` in this repo at all).
- **Evidence:** repo-cleaner this sweep — fully merged into main (`git branch --merged
  main` confirms), remote branch independently reverified gone via direct `gh api` 404
  (not trusted from `campaign_close.py`'s own report), no leftover worktree; PR #147
  MERGED at 2026-08-09T13:15:31Z. Same class as the prior firing's now-resolved
  `mobilize-chores-backend-resolve`.
- **Size:** ~1 min.

### 2. Commit this firing's applied ops artifacts to main
- **Action:** `git add` the payloads chore-lead applied this firing —
  `.claude/ops/watch-checkpoint.json` (advanced to 13:18:48Z),
  `.claude/ops/reports/2026-08-09T13-18-55Z.md` (new), and this rewritten `plan.md` —
  read the status output first, then commit as a separate step (gate ≠ commit). The two
  adr payloads are byte-identical to committed state (decision-watcher's idempotency
  check) — nothing to stage there. Direct-to-main is the solo ops-artifact case per the
  prior sweeps' precedent.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** issue-sorter names the checkpoint advance and recommends exactly this
  commit; repo-cleaner's report file is new at its path; decision-watcher confirms its
  payloads match committed state byte-for-byte (baseline committed at a65f0a0).
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 3. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 6th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify in the routine
  config that the schedule is still armed — sweep dispatches advance
  `watch-checkpoint.json` themselves, so a checkpoint gap cannot prove the routine dead.
  Sixth consecutive plan appearance: if this is a deliberate no, record that instead so
  this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan via the prior plan's entry 3; no
  seat this sweep reported the prompt fixed. Blocks unattended issue intake between
  sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 4. Decide issue #135 — the mobilize-chores/build-feature dispatch gap (carry-forward)
- **Action:** Answer the open design question and route it: build via `/build-feature`
  (record-first), or record the resolution on the issue. It still carries the owner's
  `doing` label from the prior window — direction here closes out the issue the owner is
  already circling. Now the only open design item in the backlog.
- **Owner:** human (design decision; a build then routes through `/build-feature`'s own
  confirm gate).
- **Evidence:** issue-sorter this sweep — open, already triaged, unchanged in the
  13:03:44Z→13:18:48Z window; repo-cleaner — open, empty assignees array (a label alone
  is not an ADR-0005 claim), unchanged in substance.
- **Size:** ~15 min to decide; build time ticket-dependent (hours) if yes.

### 5. Apply or rescind the standing `github_mcp_offer:accepted` decision (carry-forward)
- **Action:** Either write the merged `.mcp.json` entry the accepted offer describes
  (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record with a
  dated rescinding note. One-time action — issue-sorter's step-8 gate correctly stayed
  silent again this firing ("accepted" recorded), so no future firing will resurface
  this.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter this sweep — step 8 not-applicable, `github_mcp_offer`
  already terminal "accepted"; still no `.mcp.json` write in evidence since 2026-07-25.
- **Size:** ~10 min.

### 6. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  A "no" fully clears the decision-watcher surface (its queue is empty).
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record
  change).
- **Evidence:** carry-forward from the prior plan's entry 7; decision-watcher this sweep
  made no new judgments (zero delta, all 9 ADRs hash-identical to checkpoint, empty
  queue), leaving the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 7. Disposition issue #139 — platform-level gap, not actionable from this repo (carry-forward)
- **Action:** Decide: keep #139 open as a tracking marker for the upstream platform gap
  (the cd-into-primary compound-command escape of the git-only worktree guard), or close
  it with a pointer to wherever the gap is actually actionable. Either outcome is fine;
  the debt is that it sits in the open roster looking like local work.
- **Owner:** human.
- **Evidence:** carry-forward from the prior plan's entry 8; issue-sorter and
  repo-cleaner this sweep both confirm it open, unclaimed, unchanged.
- **Size:** ~5 min.

## Not queued (checked, found clean this sweep)

- ADR review: quiescent — all 9 ADRs content-hash-identical to the checkpoint, no
  new/amended/superseded Decisions, candidate queue empty, idempotency confirmed against
  a scratch checkpoint copy (decision-watcher). PR #147 touched no ADR file.
- Issue intake: quiescent — the 13:03:44Z→13:18:48Z window returned exactly the #133
  closure and PR #147's merge, both traced to the trusted owner; zero new filings, zero
  unknown authors, zero held items; the prior checkpoint note's stale "#133 open"
  description corrected in this firing's note (issue-sorter).
- PR #147 (teamwork 1.2.2) — merged, closure independently reverified clean: remote
  branch 404-confirmed gone by direct `gh api` re-read, no leftover worktree
  (repo-cleaner). Only its local branch remains — that is entry 1.
- All 92 PRs MERGED, zero open; no stale ADR-0005 claims on any open issue
  (repo-cleaner).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`) — re-reviewed again,
  confirmed on-demand-generated paths, deliberately kept, no edit (repo-cleaner).

## Resolved since the prior plan (2026-08-09, 13:03Z sweep)

- Prior entry 1 (delete `mobilize-chores-backend-resolve`) — RESOLVED: gone from disk;
  repo-cleaner's branch inventory this firing lists only `main` and the new
  `close-session-file-leftovers`.
- Prior entry 2 (commit the 13:03Z firing's applied artifacts) — RESOLVED: main advanced
  d6e4366 → a65f0a0 and decision-watcher confirms the checkpoint baseline committed at
  a65f0a0; succeeded by entry 2 for this firing's own artifacts.
- Prior entry 5 (decide issue #133) — RESOLVED by building it: PR #147 (teamwork 1.2.2,
  close-session invokes file-leftovers) MERGED 2026-08-09T13:15:31Z, #133 CLOSED and
  labeled `done`, remote branch reverified gone. Local-branch remainder is entry 1.
- Prior entries 3, 4, 6, 7, 8 — carried forward as entries 3, 4, 5, 6, and 7
  respectively.
