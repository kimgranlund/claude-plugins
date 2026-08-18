# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T01:44Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
The prior firing's one UNMEASURED fact is now measured: `primary_checkout_check.py` ran
against the primary for the first time (wrapping `git -C` in a Python `subprocess` call is
not caught by the Bash-tool isolation guard — verified live by repo-cleaner) → `clean`, on
`main`. decision-watcher: clean no-op (20 ADRs, hashes match checkpoint, candidate queue
empty — no payloads owed). issue-sorter: checkpoint advance only (window 00:19:09Z→01:40:09Z;
2 new PRs — #606 merged closing #604, #607 open docs-authoring with nothing TICKET-shaped;
no new issues; 0 unknown authors, 0 held, 0 needs-ruling; one payload block —
`watch-checkpoint.json`). repo-cleaner: **executed `sync_main.py` at the primary** (gated,
interactive dispatch, main genuinely dirty — 5 files quarantined as `stash@{0}`, 10 commits
pulled, HEAD reverified by SHA at `b18a011b0`, exact match to `origin/main`); counter reset
to 0; one payload block (its report).

Prior plan (2026-08-18T00:22Z firing): entry 1 (sync main) DONE — repo-cleaner ran
`sync_main.py` this firing, primary now clean on `main` @ `b18a011b0`. Entry 2 (apply the
00:22Z payloads + commit) RESOLVED-BY-EVENTS — a parallel session already committed the same
content via merged PRs (repo-cleaner diffed the stash: both report files byte-identical to
HEAD, checkpoint/plan at HEAD strictly newer than the stashed copies; checkpoint continuity —
this firing's window opens at the applied 00:19:09Z mark — proves persistence). Entry 3
(build-554 worktree removal) carries forward below.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing (no issue
bodies attached; no report names a #193 edge) — nothing reordered by the convention. No
operational dependency edges between this firing's entries either: main is already synced,
so the payload apply (entry 1) is unblocked.

**needs-ruling lane:** empty — no `needs-ruling` label on either open issue (#605, #490);
issue-sorter reports 0 held / 0 needs-ruling.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks AT THE SHARED CHECKOUT, commit + push
- **Action:** write the fenced payloads verbatim to their target paths at
  `/Users/kimba/Projects/nonoun/plugins` (freshly-synced `main` @ `b18a011b0`, working tree
  clean — dirt already quarantined as `stash@{0}`):
  `.claude/ops/watch-checkpoint.json` (issue-sorter — new checkpoint 01:40:09Z, strictly
  newer than HEAD's 00:19:09Z), `.claude/ops/reports/2026-08-18T01-44-06Z-repo-cleaner.md`
  (repo-cleaner), plus this rewritten `.claude/ops/plan.md`. Then `git status --porcelain`,
  stage exactly those three paths, read the output, commit as a separate step (gate ≠
  commit), push. Never `git add -A` — `stash@{0}` and `sweep-in-flight.json` handling stay
  out of this commit (entry 2). decision-watcher declared both its state files unchanged —
  no block owed, none staged. Apply at the shared checkout, not this worktree (the
  write-sandbox stranding hazard, per ops-write-sandbox-rules).
- **Owner:** the dispatching session (coordinator); falls to Kim if the coordinator's writes
  to the shared checkout are blocked.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); both fenced blocks present in their seats' reports; repo-cleaner §Executed
  (primary clean on `main` @ `b18a011b0` post-sync, exact match to `origin/main`).
- **Size:** ~3 min.

**Class 2 — blocking other work:** none this firing — main already synced by repo-cleaner's
gated `sync_main.py` run; nothing measured as blocking anything queued.

**Class 3 — human decisions:**

### 2. Resolve `stash@{0}` ("sync_main quarantine") at the primary checkout
- **Action:** per repo-cleaner's per-file diff evidence: selectively restore ONLY
  `.claude/ops/sweep-in-flight.json` (foreign-only, a live lock file whose session UUID
  matches this very sweep's dispatching session — safe to reapply as-is), then
  `git -C /Users/kimba/Projects/nonoun/plugins stash drop`. The other four stashed entries
  need nothing reapplied: both report files are byte-identical to HEAD (already committed by
  a parallel session), and the stashed `watch-checkpoint.json`/`plan.md` are strictly older
  than HEAD's freshly-pulled versions. Stash resolution is judgment, outside repo-cleaner's
  gated calls — it diffed and recommended, never popped or dropped.
- **Owner:** Kim (or the dispatching session, with Kim's confirm — one batched decision).
- **Evidence:** repo-cleaner §Stash — OVERLAP set (2 report files + `watch-checkpoint.json`)
  diffed byte-identical or superseded; foreign-only set (`plan.md` superseded,
  `sweep-in-flight.json` live and session-matched).
- **Size:** ~3 min.

**Class 4 — hygiene debt:**

### 3. Remove orphaned worktree `build-554` + local branch — AFTER this session closes
- **Action:** from the shared checkout root: `git worktree remove
  .claude/worktrees/build-554`, then delete local branch
  `604-repo-cleaner-off-main-finding` (upstream already gone, PR #606 MERGED), then verify
  with `git worktree list` and `git branch -vv`. **Do not run mid-session** — the directory
  is this live session's own worktree. Carried forward from the prior plan's entry 3; the
  branch component re-appeared this firing (the worktree now sits on
  `604-repo-cleaner-off-main-finding` @ `9d1f2f2`, tracking a gone remote).
- **Owner:** Kim (or the next coordinator session, post-close).
- **Evidence:** repo-cleaner §Inventory/§Classification — orphaned (remote branch gone, PR
  #606 MERGED, working tree clean); no host-repo reap script named in this workspace's
  CLAUDE.md/README, so this stays propose-only.
- **Size:** ~2 min (post-session).

## Narrated-but-absent audit

- **decision-watcher:** clean — no-op firing, both state files declared unchanged with the
  no-op clause cited; no path named without a block.
- **issue-sorter:** clean — `watch-checkpoint.json` block present; `friendlies.json` /
  `held-items.md` / `.mcp.json` explicitly declared unchanged and omitted, no conditional
  hedging, no per-firing report path narrated.
- **repo-cleaner:** clean — its per-firing report block present. Its `sync_main.py` run is a
  gated git mutation at the primary (executed and evidenced by SHA), not a `.claude/ops/`
  file write — outside the sandbox contract, correctly narrated as executed.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PR #607** (`docs: IDR-0007 solo-first composition`): OPEN, brand-new, healthy,
  no closing-issue reference, nothing TICKET-shaped — a doc-authoring PR awaiting its own
  ratification flow, not ops work.
- **2 open unassigned issues:** #605's latest comment (01:15:20Z) re-homes the work to the
  `agent-ui` repo and pulls it from this repo's queue — not stale, not this repo's action.
  #490 stays open by design (upstream pin-race tracking, anthropics/claude-code#87349;
  active evidence comment 23:51:07Z). No stale claims under ADR-0005.
- **Merged-PR branch reaping:** nothing pending — #606/#602/#601 remote branches already
  gone; `git ls-remote` shows only `main` and `docs-idr-0007-solo-first-composition`.
- **`gitignore_check.py` WARNs:** the two standing accepted WARNs (`dist/`,
  `harness-audit-*/`) unchanged at the primary; the worktree's two extra WARNs
  (`.DS_Store`, `.claude/worktrees/`) are nested-worktree run artifacts. No G2 FAIL.
- **ADR corpus:** 20 ADRs, all hashes match the checkpoint, candidate queue empty — clean
  no-op, no payload owed.
- **Batched confirms:** one owed and queued above (entry 2, the stash resolution); nothing
  else held by any seat.

## Resolved since the prior plan (2026-08-18T00:22Z firing)

- Prior entry 1 (run `sync_main.py` at the primary) — DONE: repo-cleaner executed it this
  firing (gated; 5 dirty files quarantined, 10 commits pulled, HEAD `b18a011b0` verified by
  SHA against `origin/main`).
- Prior entry 2 (apply the 00:22Z payloads + commit + push) — RESOLVED-BY-EVENTS: a parallel
  session already committed identical content (stash diffs prove it); checkpoint continuity
  (this firing's issue-sorter window opens at 00:19:09Z) proves persistence.
- Prior entry 3 (build-554 worktree removal) — CARRIED FORWARD as entry 3, now including the
  reborn local branch `604-repo-cleaner-off-main-finding` (upstream gone).
