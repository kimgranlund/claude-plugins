# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T02:32Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
decision-watcher: clean no-op (20/20 ADR hashes+statuses match checkpoint, adr-queue empty,
checkpoint correctly not advanced, no payloads owed). issue-sorter: checkpoint-advance only
(window 02:17:47Z→02:28:59Z; 0 new issues/PRs; #612's `in-flight` label the only touch —
claimed by a build dispatch, already record-shaped; 0 unknown authors, 0 held, 0 needs-ruling;
two payload blocks — `watch-checkpoint.json` + its per-firing report). repo-cleaner: gated
`git fetch --prune` clean; `primary_checkout_check.py` → on `main` @ `b18a011`; **new finding:
the primary checkout is DIRTY** (` M plan.md`, ` M watch-checkpoint.json`, two untracked
report files name-identical to files already committed on `origin/main`, untracked
`sweep-in-flight.json`) and 8 commits behind `origin/main` — the sync_main execute case, but
this firing runs worktree-isolated and the Bash wall refuses mutating git at the shared
primary, so it is PROPOSED, not executed; stray local branch `608-...` found (PR #610 MERGED,
remote gone); build-554 worktree REUSED, now on `612-harvest-domain-knowledge` (clean, tip an
ancestor of `origin/main`); one payload block (its report).

Prior plan (2026-08-18T02:19Z firing): entry 1 (apply payloads + commit + push) — DONE on
`origin/main` (the 02-19-25Z report file is committed there; issue-sorter's window this firing
opens at exactly 02:17:47Z, the applied checkpoint value), but it left uncommitted dirt at the
primary (pin-race write-redirection, tracked at open #490) — that dirt becomes entry 2 below.
Entry 2 (stash@{0}) CARRIES FORWARD — this firing's repo-cleaner is again silent on stash
inventory (unverified, not resolved). Entry 3 (delete stray `604-...`) — RESOLVED BY EVENTS
(gone from the branch list). Entry 4 (remove build-554 + `608-...` branch) — SPLIT: the branch
is now stray with no worktree (runnable now, entry 4); the worktree itself is reused by the
in-flight #612 build and must NOT be removed yet (entry 5, blocked inline).

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Two operational dependencies named inline on their own entries:
entry 1's commit/push step folds into entry 2 (the Bash wall), and entry 5 is blocked by open
#612's in-flight build (a blocker not itself in this plan — not ops-family work).

**needs-ruling lane:** empty — issue-sorter reports 0 needs-ruling, 0 held.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths
- **Action:** write the fenced payloads verbatim: `.claude/ops/watch-checkpoint.json`
  (issue-sorter — checkpoint 02:28:59Z, strictly newer than the applied 02:17:47Z),
  `.claude/ops/reports/2026-08-18T02-28-59Z.md` (issue-sorter),
  `.claude/ops/reports/2026-08-18T02-32-43Z-repo-cleaner.md` (repo-cleaner), plus this
  rewritten `.claude/ops/plan.md`. decision-watcher owes no block — none applied. Target the
  SHARED checkout's paths, not this worktree's (ops-write-sandbox-rules stranding hazard).
  **Commit + push cannot run from this worktree-isolated session** (repo-cleaner: the Bash
  wall refuses mutating git at the primary) — the persist step folds into entry 2's
  sync_main run; do not chain or improvise around the wall.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules); the
  commit/push lands with entry 2 (Kim).
- **Evidence:** all four fenced blocks present in this firing's reports; repo-cleaner
  §finding (wall triggered twice, `cd`-prefixed and bare `-C` forms); ops-write-sandbox-rules
  (state persists through the repo or the next firing starts blind).
- **Size:** ~2 min (apply only).

**Class 2 — blocking other work:**

### 2. Run `sync_main.py` at the primary from a non-worktree session — the primary is dirty AND 8 behind; blocks state persistence
- **Action:** from a session actually checked into `/Users/kimba/Projects/nonoun/plugins`
  (NOT worktree-isolated): run `sync_main.py` — quarantine the found dirt as a named stash
  (` M .claude/ops/plan.md`, ` M .claude/ops/watch-checkpoint.json`, untracked
  `sweep-in-flight.json`; the two untracked report files are name-identical to files already
  on `origin/main` and reconcile on the pull), `--ff-only` pull the 8-commit gap, reverify
  HEAD by SHA. Then stage exactly this firing's applied payload paths (entry 1; never
  `git add -A`), read the status output, commit as a separate step (gate ≠ commit), push.
  This entry blocks: entry 1's persist half (next scheduled firing starts blind if the
  checkpoint never reaches the repo) and entry 3's stash assessment (sync_main ADDS a stash).
- **Owner:** Kim (the only actor with a non-worktree session at the primary).
- **Evidence:** repo-cleaner §finding — `git status --porcelain` output verbatim, 8-behind
  confirmed, pin-race pattern per open #490 (not a new defect to file); workspace CLAUDE.md
  names `sync_main.py` as the gate for exactly this case.
- **Size:** ~5 min.

**Class 3 — human decisions:**

### 3. Resolve the stash(es) at the primary — carried forward, state unverified two firings running; blocked by #2 above (named inline — sync_main adds one more)
- **Action:** after entry 2: `git -C /Users/kimba/Projects/nonoun/plugins stash list`. The
  prior `stash@{0}` ("sync_main quarantine") is unverified — neither this firing's nor the
  prior firing's repo-cleaner carried a stash inventory. If the old stash is gone, note
  resolved-by-events. For entry 2's fresh quarantine stash: per the 01:44Z firing's per-file
  diffs, selectively restore ONLY `.claude/ops/sweep-in-flight.json` if a live sweep still
  owns it, then `git stash drop` — the tracked-file dirt is superseded by this firing's
  applied payloads. Stash resolution is judgment, outside repo-cleaner's gated calls.
- **Owner:** Kim (one batched decision covering old + new stashes).
- **Evidence:** prior plan entry 2 (carry-forward source, not fresh evidence); this firing's
  repo-cleaner report silent on stash inventory; entry 2's sync_main mechanics.
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 4. Delete stray local branch `608-dispatch-ticket-file-bug-claim-fix` — runnable now
- **Action:** from the shared checkout: `git branch -D 608-dispatch-ticket-file-bug-claim-fix`,
  then verify with `git branch -vv`. No worktree attached (build-554 moved off it to
  `612-...`), so this does not wait on any session. Stays propose-only from the seat: no
  host-repo reap script is named in this workspace's CLAUDE.md/README to gate it.
- **Owner:** Kim (or the coordinator session running entry 2, same sitting).
- **Evidence:** repo-cleaner §Inventory/§Proposed — PR #610 MERGED, upstream
  `[origin/608-...: gone]`, `git ls-remote --heads origin` → only `refs/heads/main`.
- **Size:** ~1 min.

### 5. Remove worktree `build-554` — blocked by #612's in-flight build (open; named inline — do not start before it lands or is abandoned)
- **Action:** ONLY after the #612 build concludes (PR merged and closed via
  `campaign_close.py`, or the claim released): `git worktree remove
  .claude/worktrees/build-554`, verify with `git worktree list`. Carried forward from the
  prior plan's entry 4, re-scoped: the worktree was NOT removed — it was reused for the #612
  dispatch (second reuse in two firings: 604→608→612; named as a recurring pattern, no script
  gates a worktree-branch swap, no new class to file).
- **Owner:** Kim (or the next coordinator session, post-#612).
- **Evidence:** repo-cleaner §Inventory — build-554 on `612-harvest-domain-knowledge`, clean;
  issue-sorter — #612 labeled `in-flight`, assigned, updated 02:25:03Z (concurrent, not
  stale); blocked-by-rules (open blocker not in this plan — named inline, nothing to queue
  behind).
- **Size:** ~2 min (post-build).

## Narrated-but-absent audit

- **decision-watcher:** clean — the no-op clause invoked explicitly ("no payload fence is
  owed for either" state file); no path narrated without a block.
- **issue-sorter:** clean — `watch-checkpoint.json` block present; the per-firing report path
  named AND backed by its own fenced block (`2026-08-18T02-28-59Z.md`); `friendlies.json` /
  `held-items.md` explicitly declared unchanged and omitted.
- **repo-cleaner:** clean — its per-firing report block present; `sync_main.py` and the
  branch deletion explicitly marked NOT invoked / proposed-only (the opposite of a narrated
  write); its executed git calls (fetch, read-only surveys) are not `.claude/ops/` writes —
  outside the sandbox contract, correctly narrated as executed.

## Not queued (checked, found clean or deliberately left)

- **#612 build in flight** — a build dispatch's work item, not an ops action; it appears here
  only as entry 5's blocker.
- **Open issues #613/#611/#609/#605/#490** — all kind-labeled, no stale claims (only #612
  assigned, touched 02:25:03Z); buildable backlog routes through teamwork's
  `/mobilize-chores`, outside this queue. #490 open by design (upstream pin-race tracking) —
  and actively explanatory this firing (entry 2's dirt pattern).
- **Open PRs:** none; only `refs/heads/main` remote — nothing to reap remotely,
  `campaign_close.py` correctly not invoked.
- **`gitignore_check.py` WARNs:** same standing sets both roots (primary: `dist/`,
  `harness-audit-*/`; worktree adds `.DS_Store`, `.claude/worktrees/` — nested-worktree
  artifacts); no FAIL, identical to last firing.
- **ADR corpus:** 20/20 known, no delta, adr-queue empty — clean no-op.
- **The 608→612 worktree-reuse pattern:** named (entry 5), not actioned — same shape as the
  prior 604 stray, no gating script exists.

## Resolved since the prior plan (2026-08-18T02:19Z firing)

- Prior entry 1 (apply the 02:19Z payloads + commit + push) — DONE on `origin/main`
  (checkpoint continuity: this firing's issue-sorter window opens at 02:17:47Z; the 02-19-25Z
  report file committed on `origin/main`), with a side effect: uncommitted dirt stranded at
  the primary (pin-race redirection, #490) → now entry 2.
- Prior entry 2 (stash@{0}) — CARRIED FORWARD as entry 3, still unverified.
- Prior entry 3 (delete stray `604-...`) — RESOLVED BY EVENTS: gone from the branch list.
- Prior entry 4 (build-554 worktree + `608-...` branch) — SPLIT: branch now stray and
  runnable (entry 4); worktree reused by #612's build, removal re-blocked (entry 5).
