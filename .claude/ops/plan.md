# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-17T20:18Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
decision-watcher: clean no-op recheck (20 ADRs, zero delta vs. the 18:31Z checkpoint, 0
candidates pending, no state mutation needed). issue-sorter: clean checkpoint-advance (window
18:30:59Z→20:16:04Z; 19 issues + 17 PRs touched; 10 new issues all fully formed at mint; 0
unknown authors, 0 held; steps 7/8 not-applicable). repo-cleaner: executed its gated mutations
(`git fetch --prune` cleared 13 dead refs; `sync_main.py` ff'd a clean-but-1-behind main to
`32f417fd7`, SHA-reverified); independently reconfirmed the prior firing's C2 refusal resolved
(PR #544's `worktree-build-522` remote → 404); 3 orphaned post-merge worktrees proposed for
removal; no stale claims, no stale-open PRs, gitignore WARNs unchanged/pre-ruled.

Prior plan (2026-08-17T18:35Z firing): **all 6 entries resolved** (see Resolved below) — nothing
carries forward as an open entry.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing, and no
report-evidenced dependency either (the prior plan's entry-2→5 edge closed with build-522's
cleanup) — nothing reordered; every entry ranks purely on class.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit + push this firing's ops artifacts — explicit pathspec only
- **Action:** `git status --porcelain` first, then stage exactly `.claude/ops/plan.md`,
  `.claude/ops/watch-checkpoint.json`, and
  `.claude/ops/reports/2026-08-17T20-18-02Z-repo-cleaner.md` (the only payload blocks emitted
  this firing — decision-watcher declared unchanged-and-omitted for both its state files;
  issue-sorter emitted checkpoint only). Read the status output, commit as a separate step
  (gate ≠ commit), push. Never `git add -A`.
- **Owner:** the dispatching session (coordinator).
- **Evidence:** ops-write-sandbox-rules — state persists through the repo or the next firing
  starts blind; issue-sorter's and repo-cleaner's fenced blocks present in their reports.
- **Size:** ~2 min.

**Class 2 — items blocking other work:** none this firing.

**Class 3 — human decisions:**

### 2. Rule on decision-watcher's conditionally-named report path (fence-rule hedge clause)
- **Action:** decision-watcher's report names its own per-firing record path conditionally
  ("would land at `.claude/ops/reports/2026-08-17T19-XX-XXZ-decision-watcher.md` ... nothing new
  to persist") without emitting a block. Per ops-write-sandbox-rules' hedge clause, a seat with
  nothing to report for a path omits it entirely rather than naming it conditionally. No
  downstream payload cites the path, so nothing is stranded — but the pattern is the exact class
  the rule forbids. Kim rules: brush-noted only, or mint a small task to fix the seat's
  no-op-report phrasing (a semantic agent edit → rides with a checker per plugin-authoring rules).
- **Owner:** Kim.
- **Evidence:** decision-watcher report §Report (verbatim in this dispatch);
  ops-write-sandbox-rules "payload-fence rule binds regardless of hedge language."
- **Size:** ~3 min ruling (+~15 min fix if minted).

**Class 4 — hygiene debt:**

### 3. Batch-remove the three orphaned post-merge worktrees and their local branches
- **Action:** run repo-cleaner's proposed commands verbatim (propose-only from that seat — no
  host reap script exists in this workspace's CLAUDE.md/README to gate them):
  `git worktree remove .claude/worktrees/build-524-w6` + `git branch -D worktree-build-524-w6`;
  `git worktree remove .claude/worktrees/build-539` + `git branch -D worktree-build-539`;
  `git worktree remove .claude/worktrees/t9-agent-verification` + `git branch -D
  docs-542-t9-agent-verification`. All three verified: PRs #565/#569/#575 MERGED, remote
  branches already gone. Does NOT touch b548-teamwork (PR #573 open), build-554 (PR #556 open
  draft), or issue-576-sweep-skill (fresh, ~7 min old at inventory — too new to call orphaned).
- **Owner:** coordinator (or Kim by hand).
- **Evidence:** repo-cleaner §Inventory + §Proposed only — post-fetch-prune, SHA/state-verified.
- **Size:** ~3 min.

## Narrated-but-absent audit

- **issue-sorter:** clean — `watch-checkpoint.json` block present; `friendlies.json` /
  `held-items.md` / `.mcp.json` explicitly declared unchanged, no blocks owed.
- **repo-cleaner:** clean — its per-firing report block present; executed actions are gated
  git/gh mutations inside its own procedure, not `.claude/ops/` file writes.
- **decision-watcher:** state files explicitly declared unchanged (clean); its per-firing report
  path named conditionally without a block — flagged, not silently absorbed → entry 2.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PRs #573 (open) and #556 (open, draft):** fresh, active, own their lifecycles; merge is
  Kim's per the auto-mode ceiling.
- **Worktree `issue-576-sweep-skill`:** tracks `origin/main`, no divergent commits, issue #576
  minutes old at inventory — healthy, re-measure next firing.
- **6 open unassigned issues (#576, #574, #558, #554, #551, #490):** backlog work, no stale
  claims (zero assignees, ADR-0005); driving builds is `/mobilize-chores` territory, not this
  queue. #490 stays open by design (platform tracking issue, upstream filed as
  anthropics/claude-code#87349).
- **Prior entry 6's fix (clean-git fetch-prune step):** ticket minted last cycle; the build
  rides its own issue through the build pipeline — not ops-family execution.
- **`gitignore_check.py` G1 WARNs (`dist/`, `harness-audit-*/`):** unchanged, pre-ruled accepted
  (2026-08-17-entry11 ruling carried).
- **Batched confirms:** none owed — decision-watcher 0 candidates, issue-sorter 0 held.
- **ADR corpus:** zero delta; adr-0020 already harvested (reject-as-duplicate), adr-0015's
  superseded clause has no downstream citations.

## Resolved since the prior plan (2026-08-17T18:35Z firing)

- Prior entry 1 (ops-artifacts commit) — DONE (commit 85ba7b9, per that plan's dated amendment).
- Prior entry 2 (#544 C2 remote-branch delete + re-run) — RESOLVED: this firing's repo-cleaner
  independently reconfirmed `worktree-build-522` gone via `gh api` → 404.
- Prior entry 3 (#490 upstream forward) — RESOLVED-BY-EVENTS: already filed upstream
  (anthropics/claude-code#87349), cross-linked on #490.
- Prior entry 4 (orphaned worktrees/branches batch) — DONE (3 worktrees + 7 branches removed,
  per the dated amendment); repo-cleaner confirms none reappear in this firing's inventory.
- Prior entry 5 (build-522 worktree removal) — RESOLVED: gone from this firing's worktree
  inventory entirely.
- Prior entry 6 (clean-git fetch-prune ticket) — MINTED (dated amendment); the fix itself now
  rides its GitHub issue (see Not queued).
