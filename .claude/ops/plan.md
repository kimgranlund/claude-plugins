# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-08 (second sweep this day). Evidence:
the three seat reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner —
none UNMEASURED), plus the prior plan (2026-08-08, earlier sweep) read as carry-forward source.
Nothing refetched. No prior queue entry resolved this sweep; all six carried forward. One prior
"Resolved" claim is REOPENED on fresh evidence (entry 2).

## Queue

**Class 1 — gated mutations verified safe: none left to queue.** The two merged PRs this window
(#141, #142) had their remote branches confirmed already-absent via `campaign_close.py` inside
repo-cleaner's own charter (gates clean: harness+teamwork for #141, teamwork for #142);
`sync_main.py` not needed — main already clean at tip.

**Class 2 — items blocking other work:**

### 1. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 3rd appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify in the routine config
  that the schedule is still armed. Note: sweep dispatches now advance `watch-checkpoint.json`
  themselves, so a checkpoint gap can no longer prove the routine dead — the config is the only
  place to verify.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan via the prior plan's entry 3; no seat this
  sweep reported the prompt fixed. Blocks unattended issue intake between sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 2. Apply or rescind the standing `github_mcp_offer:accepted` decision (REOPENED)
- **Action:** Decide the follow-through: either write the merged `.mcp.json` entry the accepted
  offer describes (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record
  with a dated note rescinding it. One-time action — issue-sorter's step-8 gate correctly stays
  silent once "accepted" is recorded, so no future firing will surface this again.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter report this sweep: "accepted" has stood in `friendlies.json` since
  2026-07-25 with no `.mcp.json` ever written. Reopens the prior plan's Resolved item 1, which
  recorded the decision but not the unapplied payload.
- **Size:** ~10 min.

### 3. Batched confirm + Phase 6 on the adr-0006 stale-citation candidate (aging since 2026-07-30)
- **Action:** One batched confirm round over the single pending candidate in `adr_queue.py
  pending` (adr-0009 narrowly supersedes adr-0006's find-the-ask rename-map row). On confirm,
  save-lessons Phase 6 re-open pass — the live work is
  `harness/skills/big-change-git-rules/references/rename-execution-playbook.md` (Decisions
  2/3/4/6 + Acceptance, likely still valid but unchecked);
  `harness/skills/check-all-agents/references/standard-of-excellence.md:93` is already judged
  unaffected, and `harness/skills/naming-rules/references/estate-rename-map.md:11,15,42` is
  deliberately byte-identical per adr-0009 Decision 3 — NOT stale by design.
- **Owner:** human (the confirm) → save-lessons Phase 6 (the re-open pass) — never
  decision-watcher itself.
- **Evidence:** decision-watcher report this sweep (candidate untouched, per-file judgments
  refined; "not urgent but aging since 2026-07-30").
- **Size:** ~15–25 min.

### 4. Close-or-extend decision on issue #140 (payload-discipline contract)
- **Action:** One `gh issue comment` recording that a second consecutive firing returned its
  report as a proper payload block (repo-cleaner explicitly notes #140's underlying complaint is
  satisfied by this sweep's return), then decide: close as fixed-in-practice, or keep open until
  the seat contracts themselves are patched (candidate 7th silent-failure-catalog instance,
  cf. #127).
- **Owner:** human.
- **Evidence:** repo-cleaner report this sweep; prior plan entry 4 (the issue-sorter instance
  from the earlier sweep).
- **Size:** ~10 min.

### 5. Triage issue #138's charter-expansion proposal
- **Action:** Human evaluates adding gen-ui-kit's `ops:reap-branches` to repo-cleaner's
  narrow-action set. Repo-cleaner surfaced it and is barred from adopting it unilaterally.
- **Owner:** human (accept → charter edit via the normal agent-change path; reject → close #138
  with the reasoning).
- **Evidence:** repo-cleaner report this sweep (finding unchanged from the prior firing).
- **Size:** ~10 min to decide.

### 6. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  decision-watcher chose not to queue it and flagged the call for review.
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record change).
- **Evidence:** carry-forward from the prior plan's entry 2; decision-watcher this sweep made no
  new judgments, leaving the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 7. Retire (or deliberately keep) the two no-match `.gitignore` lines (propose-only)
- **Action:** Human or `/clean-repo` judges the two WARN lines matching nothing in the tree:
  `dist/` and `harness-audit-*/`. Caveat before deleting `dist/`: it is gate OUTPUT
  (`release_gate.py --package` writes `<plugin>/dist/`) — "matches nothing" only means no package
  is built in this checkout; retiring it would let future gate artifacts land in git.
  `harness-audit-*/` has no standing producer in evidence.
- **Owner:** human or `/clean-repo` (repo-cleaner is propose-only on `.gitignore`).
- **Evidence:** repo-cleaner report this sweep (finding unchanged from the prior firing).
- **Size:** ~5 min.

### 8. Route the remaining open backlog — #133, #135, #139 — toward triage or build
- **Action:** `/mobilize-chores` (or a direct human pass) over the three open issues not already
  queued above (#138 → entry 5, #140 → entry 4). All five open issues have empty assignees and no
  stale ADR-0005 claims. Roster note: #131 and #137 no longer appear in repo-cleaner's open list —
  inferred closed by the #141/#142 merges (inference, not measured by any seat this sweep).
- **Owner:** human (launches `/mobilize-chores`; it gates any build behind one confirm).
- **Evidence:** repo-cleaner report (5 open issues, empty assignees); issue-sorter report
  (nothing needed triage; all activity trusted-author).
- **Size:** ~10 min to launch and triage; build time per ticket varies (hours,
  ticket-dependent).

## Not queued (checked, found clean this sweep)

- PRs #141 and #142 — merged, remote branches verified absent, touched plugins gate-clean
  (repo-cleaner, via `campaign_close.py` within its own charter).
- Main clean at tip; worktrees, local branches, remote refs post-prune, open-PR surface all
  healthy (repo-cleaner).
- Zero unknown-author items, zero held items, zero new friendlies this firing (issue-sorter).
- ADR checkpoint reformatted only — no data change; 0 new/amended/newly-superseded ADRs
  (decision-watcher).

## Carried and reopened since the prior plan (2026-08-08, earlier sweep)

- Prior entries 1–6: none resolved — carried forward as entries 3, 6, 1, 4, 7, and 5+8
  respectively (several with refined evidence).
- Prior Resolved item 1 (`github_mcp_offer`) — REOPENED as entry 2: the acceptance was recorded,
  but the `.mcp.json` payload was never applied (issue-sorter, this sweep).
- Prior Resolved items 2–3 and the PR #136 close — still resolved; no contrary evidence.
