# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-17T22:49Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
decision-watcher: clean no-op (20 ADRs, zero classify delta vs. checkpoint, queue empty, both
state files explicitly declared unchanged — no payloads owed). issue-sorter: checkpoint advance
(window 18:30:59Z→22:48:04Z; 21 new issues, 18 already fully formed, 3 unlabeled ones labeled
directly via `gh issue edit` — #582 task+size:small, #583 bug+major, #584 task+size:small; 0
unknown authors, 0 held, 0 needs-ruling; one payload block, `watch-checkpoint.json`).
repo-cleaner: `git fetch --prune` cleared 1 dead ref; no gated script had eligible work
(`campaign_close.py` — both merged PRs' remote branches already gone per `git ls-remote`;
`sync_main.py` — main clean and exactly at `origin/main` @ `9ce9067`); worktree classification
reset (all five previously-tracked worktrees gone, two NEW merged-orphaned worktrees:
`build-554` / PR #556 MERGED and `build-558` / PR #594 MERGED); one payload block (its report).

Prior plan (2026-08-17T20:25Z firing): entry 1 DONE (ops commit pushed — this firing's
issue-sorter window opens at a later checkpoint, confirming persistence); entry 2 RULED by Kim
(#585 minted, stays open as size:small hardening — do not re-ask); entry 3 RESOLVED-BY-EVENTS
(peer session reaped all four worktrees + five branches; this firing's inventory confirms none
remain). Nothing carries forward as open.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing (no issue
bodies attached; no report names a dependency edge) — nothing reordered; every entry ranks
purely on class.

**needs-ruling lane:** empty — issue-sorter explicitly classified #582/#584 as already-decided
implementation work, not open decisions; no `needs-ruling` label exists on any open issue.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks AT THE SHARED CHECKOUT, then commit + push — explicit pathspec only
- **Action:** write the two fenced payloads verbatim to their target paths
  (`.claude/ops/watch-checkpoint.json` from issue-sorter;
  `.claude/ops/reports/2026-08-17T22-49-02Z-repo-cleaner.md` from repo-cleaner), plus this
  rewritten `.claude/ops/plan.md`. **Stranding hazard, named:** this sweep ran inside worktree
  `.claude/worktrees/build-554`, whose branch `worktree-build-554` has a MERGED PR (#556) and no
  remote branch — a write applied there lands on a dead branch and strands. Apply at the shared
  checkout root (`/Users/kimba/Projects/nonoun/plugins`, branch `main`, clean @ `9ce9067`).
  Then `git status --porcelain`, stage exactly those three paths, read the output, commit as a
  separate step (gate ≠ commit), push. Never `git add -A`. decision-watcher declared both its
  state files unchanged — no block owed, none staged.
- **Owner:** the dispatching session (coordinator).
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); both fenced blocks present in their seats' reports; repo-cleaner §Inventory
  (PR #556 MERGED 20:29:41Z, remote branch gone, main clean at origin's SHA).
- **Size:** ~3 min.

**Class 2 — items blocking other work:** none this firing.

**Class 3 — human decisions:** none this firing — decision-watcher 0 pending candidates,
issue-sorter 0 held / 0 needs-ruling, no batched confirm owed. (#585 already ruled 2026-08-17 —
carried as backlog work, not re-asked.)

**Class 4 — hygiene debt:**

### 2. Remove orphaned worktree `build-558` + its branch
- **Action:** `git worktree remove .claude/worktrees/build-558` +
  `git branch -D 558-mobilize-chores-unstick` (run from the shared checkout root). PR #594
  MERGED 2026-08-17T22:07:18Z, `headRefOid` exact match @ `01b6372`, remote branch already gone.
  Propose-only from repo-cleaner (no host reap script exists in this workspace's
  CLAUDE.md/README to gate it).
- **Owner:** coordinator (or Kim by hand).
- **Evidence:** repo-cleaner §Inventory + §Proposed only — post-fetch-prune, SHA/state-verified
  via `gh pr view` and `git ls-remote --heads origin` (only `main` remains remotely).
- **Size:** ~2 min.

### 3. Remove orphaned worktree `build-554` + its branch — AFTER the sweep session closes
- **Action:** `git worktree remove .claude/worktrees/build-554` +
  `git branch -D worktree-build-554`. PR #556 MERGED 2026-08-17T20:29:41Z, `headRefOid` exact
  match @ `3e9805a`, remote branch already gone. **Do not run mid-session** — this is the
  worktree the sweep itself ran in (repo-cleaner's own caveat); queue for after the live
  session ends, then verify with `git worktree list`.
- **Owner:** Kim (or the next coordinator session, post-close).
- **Evidence:** repo-cleaner §Proposed only — explicitly flagged as the sweep's own live
  worktree; merge and remote-branch absence independently reverified.
- **Size:** ~2 min (post-session).

## Narrated-but-absent audit

- **decision-watcher:** clean — both state files (`adr-checkpoint.json`, `adr-queue.json`)
  explicitly declared unchanged with the sandbox rule cited; no path named without a block.
- **issue-sorter:** clean — `watch-checkpoint.json` block present; `friendlies.json` /
  `held-items.md` explicitly declared unchanged and omitted; label edits were `gh` API actions,
  not filesystem writes (outside sandbox scope).
- **repo-cleaner:** clean — its per-firing report block present; the fetch-prune is a gated git
  mutation inside its own procedure, not a `.claude/ops/` file write.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **11 open unassigned issues (#581–#586, #588, #589, #592, #593, #490):** backlog work, zero
  assignees, no stale claims (no ticket-claim convention ruled here — repo-cleaner's carve-out);
  driving builds is `/mobilize-chores` territory, not this queue. #490 stays open by design
  (upstream tracking, anthropics/claude-code#87349). #585 ruled 2026-08-17 — open by Kim's
  tie-break, do not re-ask.
- **#582's cross-repo note:** its evidence claims `spec-ticketing-watch-triage.md` missing in
  gen-ui-kit; it exists here at `.claude/docs/spec/`. Cross-repo finding recorded in the issue
  itself — nothing for this repo's queue beyond the (already-applied) labels.
- **Open PRs:** none — the board is empty; both recently-merged PRs (#556, #594) verified MERGED
  with remote branches gone.
- **`gitignore_check.py` G1 WARNs (`dist/`, `harness-audit-*/`):** unchanged, pre-ruled accepted
  (2026-08-17-entry11 ruling carried; worktree-path run artifacts correctly discounted). No G2
  FAIL.
- **ADR corpus:** zero classify delta; candidate queue confirmed empty; no checkpoint advance
  needed (hashes already match).
- **Batched confirms:** none owed — decision-watcher 0 candidates, issue-sorter 0 held.

## Resolved since the prior plan (2026-08-17T20:25Z firing)

- Prior entry 1 (payload apply + commit) — DONE (checkpoint continuity proves persistence).
- Prior entry 2 (hedge-clause ruling) — RULED: #585 minted and held open by Kim's tie-break;
  closed as a plan item, lives on as backlog.
- Prior entry 3 (four worktrees + five branches) — RESOLVED-BY-EVENTS: peer session reaped all;
  this firing's inventory confirms none remain (fresh classification, counter reset to 0).
