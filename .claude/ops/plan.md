# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T00:22Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
One in-plan UNMEASURED fact: the primary checkout's `main` dirty/clean state (repo-cleaner
could not reach `/Users/kimba/Projects/nonoun/plugins` — the session-isolation guard refused
every git op targeting the shared checkout; ref-only reads show `main` behind `origin/main`
by 4). decision-watcher: clean no-op (20 ADRs, zero classify delta, queue empty, both state
files unchanged — no payloads owed; scratch idempotency check passed, formatting-only diff).
issue-sorter: checkpoint advance only (window 22:48:04Z→00:19:09Z; 3 new issues #603/#604/#605
all arrived fully formed via file-task, 7 new PRs #596–#602 all merged; 0 unknown authors,
0 held, 0 needs-ruling; two payload blocks — its report + `watch-checkpoint.json`).
repo-cleaner: nothing gate-eligible (no open PRs, remote carries only `main`); inventory
reset — `build-558` worktree + branch fully gone, `build-554`'s stale branch gone (worktree
dir remains, live-in-use); counter 0; one payload block (its report).

Prior plan (2026-08-17T22:49Z firing): entry 1 DONE (checkpoint continuity proves the ops
commit persisted — this firing's issue-sorter window opens at 22:48:04Z). Entry 2
RESOLVED-BY-EVENTS (`build-558` + `558-mobilize-chores-unstick` fully reaped — worktree,
local branch, remote branch all confirmed gone). Entry 3 HALF-RESOLVED: branch
`worktree-build-554` already cleared; the worktree DIRECTORY removal carries forward below
(still this session's own live worktree — post-session only).

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing (no issue
bodies attached; no report names a #193 edge) — nothing reordered by the convention. Entry 2
below carries an OPERATIONAL dependency on entry 1 (named inline both ways per
blocked-by-rules' ordering principle: a blocked entry never sits ahead of its own blocker).

**needs-ruling lane:** empty — no `needs-ruling` label on any open issue (#605, #604, #603,
#490 surveyed by repo-cleaner; issue-sorter reports 0 held / 0 needs-ruling).

## Queue

**Class 2 — blocking other work (ordered ahead of the Class-1 entry it blocks):**

### 1. Run `sync_main.py` at the primary checkout — main is 4 behind, dirty state UNMEASURED
- **Action:** from a session actually positioned at `/Users/kimba/Projects/nonoun/plugins`
  (NOT this sweep's worktree — the isolation guard refuses cross-checkout git ops from here),
  run `python3 harness/scripts/sync_main.py`: quarantines any dirt as a named stash,
  `--ff-only` pulls the 4 commits, reverifies HEAD by SHA. Blocks entry 2 — committing this
  firing's ops state onto a stale (possibly dirty) main risks a bad base.
- **Owner:** Kim (or any session opened at the primary checkout).
- **Evidence:** repo-cleaner §Executed/§Inventory — `git branch -a -vv` shows local `main`
  @ `12eb072`, behind 4 vs. `origin/main` @ `12f13af`; dirty/clean state explicitly
  UNMEASURED from the worktree; guard refusal consistent with the #592/PR #600
  primary-checkout-main-only rule, not the #490 pin race.
- **Size:** ~2 min.

**Class 1 — gated mutations verified safe:**

### 2. Apply this firing's payload blocks AT THE SHARED CHECKOUT, commit + push — after entry 1
- **Action:** blocked by entry 1 (open — sync main first). Write the three fenced payloads
  verbatim to their target paths: `.claude/ops/reports/2026-08-18T00-19-09Z-issue-sorter.md`
  and `.claude/ops/watch-checkpoint.json` (issue-sorter),
  `.claude/ops/reports/2026-08-18T00-22-03Z-repo-cleaner.md` (repo-cleaner), plus this
  rewritten `.claude/ops/plan.md`. **Stranding hazard, named:** this sweep ran inside
  worktree `.claude/worktrees/build-554` on a DETACHED HEAD (`12f13af`, no branch) — a
  commit applied there attaches to nothing and strands. Apply at the shared checkout root on
  a freshly-synced `main`. Then `git status --porcelain`, stage exactly those four paths,
  read the output, commit as a separate step (gate ≠ commit), push. Never `git add -A`.
  decision-watcher declared both its state files unchanged — no block owed, none staged.
- **Owner:** the dispatching session (coordinator); falls to Kim if the isolation guard also
  blocks the coordinator's writes to the shared checkout.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); all three fenced blocks present in their seats' reports; repo-cleaner
  §Inventory (build-554 detached at `12f13af`, working tree clean).
- **Size:** ~3 min.

**Class 3 — human decisions:** none this firing — decision-watcher 0 pending candidates,
issue-sorter 0 held / 0 unknown authors, no batched confirm owed by any seat.

**Class 4 — hygiene debt:**

### 3. Remove orphaned worktree directory `build-554` — AFTER this session closes
- **Action:** `git worktree remove .claude/worktrees/build-554` from the shared checkout
  root, then verify with `git worktree list`. Its branch (`worktree-build-554`) is already
  gone — only the directory remains, correctly left in place while this live session uses
  it. **Do not run mid-session.** Carried forward from the prior plan's entry 3 (branch half
  done by events).
- **Owner:** Kim (or the next coordinator session, post-close).
- **Evidence:** repo-cleaner §Inventory — build-554 detached at origin/main's exact tip,
  clean; former branch confirmed absent; no other worktrees or stray branches exist.
- **Size:** ~2 min (post-session).

## Narrated-but-absent audit

- **decision-watcher:** clean — both state files (`adr-checkpoint.json`, `adr-queue.json`)
  explicitly declared unchanged with the sandbox rule cited; scratch-only mutations; no path
  named without a block.
- **issue-sorter:** clean — report block AND `watch-checkpoint.json` block both present;
  `friendlies.json` / `held-items.md` / `.mcp.json` explicitly declared unchanged and
  omitted (no conditional hedging).
- **repo-cleaner:** clean — its per-firing report block present; no gated mutation executed,
  so nothing else owed.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **4 open unassigned issues (#605, #604, #603, #490):** backlog build work, zero assignees,
  no stale claims under ADR-0005 (all recent activity is Kim's own, within the hour);
  driving builds is `/mobilize-chores` territory, not this queue. #490 stays open by design
  (upstream tracking, anthropics/claude-code#87349). #604 (off-main primary-checkout
  finding-type) noted by repo-cleaner as not-fired here — main is on `main`.
- **Open PRs:** none — board empty; #596–#602 all verified MERGED, remote branches gone
  (`git ls-remote` shows only `refs/heads/main`).
- **`gitignore_check.py` WARNs:** the two standing accepted WARNs (`dist/`,
  `harness-audit-*/`, per 2026-08-17-entry11 ruling) unchanged; the two extra WARNs this
  firing (`.DS_Store`, `.claude/worktrees/`) are nested-worktree run artifacts, not
  findings. No G2 FAIL.
- **ADR corpus:** zero classify delta, candidate queue empty, checkpoint data already
  matches (formatting-only diff on the scratch advance — no content change, no payload).
- **Batched confirms:** none owed by any seat.

## Resolved since the prior plan (2026-08-17T22:49Z firing)

- Prior entry 1 (payload apply + commit) — DONE: checkpoint continuity (issue-sorter's
  window opened at the applied 22:48:04Z checkpoint) proves persistence.
- Prior entry 2 (build-558 worktree + branch) — RESOLVED-BY-EVENTS: worktree dir, local
  branch, and remote branch all confirmed gone this firing.
- Prior entry 3 (build-554 worktree + branch) — HALF-RESOLVED: branch gone by events;
  directory removal re-queued above as entry 3 (post-session).
