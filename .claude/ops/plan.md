# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-17T20:25Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
decision-watcher: clean no-op (20 ADRs, zero classify delta, queue empty, no payloads owed —
and, unlike last firing, no conditionally-named report path; the hedge-clause pattern did not
recur). issue-sorter: clean checkpoint-advance (window 20:16:04Z→20:22:12Z; issue #551 CLOSED
and PR #573 MERGED, both pre-existing/already-classified; 0 unknown authors, 0 held; steps 7/8
not-applicable). repo-cleaner: executed its gated mutations (`git fetch --prune` cleared 1 dead
ref; `sync_main.py` ff'd a clean-but-3-behind main to `b05297f9`, SHA-reverified); PR #573's
merge newly orphans worktree `b548-teamwork`; a dead bare branch
(`worktree-t9-agent-verification`) surfaced; the three previously-proposed orphaned worktrees
remain unremoved (repeat proposals); no stale claims, no stale-open PRs, gitignore WARNs
unchanged/pre-ruled.

Prior plan (2026-08-17T20:18Z firing): entry 1 RESOLVED (issue-sorter's window opens exactly at
the prior checkpoint 20:16:04Z — the payload landed and advanced); entry 2 CARRIED (Kim never
ruled; new evidence weakens the fix case — see Queue 2); entry 3 NOT DONE — carried and grown
(the three worktrees repeat unresolved, plus one newly orphaned and one dead bare branch).

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing, and no
report-evidenced dependency edge — nothing reordered; every entry ranks purely on class.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks, then commit + push — explicit pathspec only
- **Action:** write the two fenced payloads verbatim to their target paths
  (`.claude/ops/watch-checkpoint.json` from issue-sorter;
  `.claude/ops/reports/2026-08-17T20-24-52Z-repo-cleaner.md` from repo-cleaner), plus this
  rewritten `.claude/ops/plan.md`. Then `git status --porcelain`, stage exactly those three
  paths, read the status output, commit as a separate step (gate ≠ commit), push. Never
  `git add -A`. decision-watcher declared unchanged-and-omitted for both its state files — no
  block owed, none staged.
- **Owner:** the dispatching session (coordinator).
- **Evidence:** ops-write-sandbox-rules — state persists through the repo or the next firing
  starts blind; both fenced blocks present in their seats' reports this firing.
- **Size:** ~2 min.

**Class 2 — items blocking other work:** none this firing.

**Class 3 — human decisions:**

### 2. Close or act on the carried decision-watcher hedge-clause ruling (prior entry 2)
- **Action:** Kim rules on the prior firing's finding (decision-watcher named its report path
  conditionally without a block). NEW EVIDENCE this firing: the seat's report omits the path
  entirely and cites the rule correctly — the pattern did not recur. Recommended: close as
  resolved-by-events / brush-noted; mint a phrasing-fix task only if it recurs (that fix is a
  semantic agent edit → rides with a checker per plugin-authoring rules).
- **Owner:** Kim.
- **Evidence:** prior plan entry 2 (2026-08-17T20:18Z firing) + this firing's decision-watcher
  report §Step 6/9 (clean omission, rule cited by name).
- **Size:** ~2 min ruling.

**Class 4 — hygiene debt:**

### 3. Batch-remove the four orphaned post-merge worktrees, their branches, and one dead bare branch
- **Action:** run repo-cleaner's proposed commands verbatim (propose-only from that seat — no
  host reap script exists in this workspace's CLAUDE.md/README to gate them):
  `git worktree remove .claude/worktrees/b548-teamwork` + `git branch -D worktree-b548-teamwork`
  (PR #573 MERGED — new this firing);
  `git worktree remove .claude/worktrees/build-524-w6` + `git branch -D worktree-build-524-w6`
  (PR #565 MERGED — repeat, 2nd firing unresolved);
  `git worktree remove .claude/worktrees/build-539` + `git branch -D worktree-build-539`
  (PR #569 MERGED — repeat, 2nd firing unresolved);
  `git worktree remove .claude/worktrees/t9-agent-verification` + `git branch -D
  docs-542-t9-agent-verification` (PR #575 MERGED — repeat, 2nd firing unresolved);
  `git branch -D worktree-t9-agent-verification` (dead bare branch, no worktree, no PR, tip
  `8df2261` confirmed ancestor of main — new finding). All merged-PR remote branches already
  gone per `git ls-remote --heads origin` (only `main` + `worktree-build-554` remain remotely).
  Does NOT touch `build-554` (PR #556 open draft, this session's own worktree) or
  `issue-576-sweep-skill` (tracks origin/main, 0 own commits, issue #576 fresh and unassigned —
  healthy, re-measure next firing).
- **Owner:** coordinator (or Kim by hand).
- **Evidence:** repo-cleaner §Inventory + §Proposed only — post-fetch-prune, SHA/state-verified;
  three of five items now repeat across two consecutive firings.
- **Size:** ~4 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — both state files explicitly declared unchanged with the rule
  cited; no path named without a block (the prior firing's hedge pattern did not recur).
- **issue-sorter:** clean — `watch-checkpoint.json` block present; `friendlies.json` /
  `held-items.md` explicitly declared unchanged, `.mcp.json` explicitly not-applicable — no
  blocks owed.
- **repo-cleaner:** clean — its per-firing report block present; executed actions are gated
  git mutations inside its own procedure, not `.claude/ops/` file writes.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PR #556 (open, draft):** this session's own active work; merge is Kim's per the auto-mode
  ceiling. PR #573 left the board — MERGED 20:19:21Z.
- **Worktree `issue-576-sweep-skill`:** tracks `origin/main`, no divergent commits — healthy,
  re-measure next firing (carried ruling).
- **5 open unassigned issues (#576, #574, #558, #554, #490):** backlog work, zero assignees, no
  stale claims (ADR-0005); driving builds is `/mobilize-chores` territory, not this queue. #490
  stays open by design (upstream tracking, anthropics/claude-code#87349). #551 left the board —
  CLOSED this window.
- **`gitignore_check.py` G1 WARNs (`dist/`, `harness-audit-*/`):** unchanged, pre-ruled accepted
  (2026-08-17-entry11 ruling carried). No G2 FAIL.
- **Batched confirms:** none owed — decision-watcher 0 candidates, issue-sorter 0 held.
- **ADR corpus:** zero classify delta vs. checkpoint; candidate queue confirmed empty.

## Resolved since the prior plan (2026-08-17T20:18Z firing)

- Prior entry 1 (ops-artifacts apply + commit) — RESOLVED: this firing's issue-sorter discovery
  window opens exactly at the prior checkpoint timestamp (20:16:04Z), proving the payload was
  applied and persisted.
- Prior entry 2 (hedge-clause ruling) — CARRIED as entry 2 above (unruled; recurrence did not
  happen — recommended close).
- Prior entry 3 (three orphaned worktrees) — NOT DONE: all three reappear in this firing's
  inventory as repeat proposals; carried and grown into entry 3 above.
