# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T02:19Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
decision-watcher: clean no-op (20 ADRs scanned, 20 previously known, no delta, checkpoint
correctly not advanced, no payloads owed). issue-sorter: checkpoint-advance only (window
01:40:09Z→02:17:47Z; 4 new issues — #613/#612/#611 feature+size:big, #609 bug+major, all
already record-shaped and kind-labeled at discovery; #608 closed via merged #610; #607
merged; 0 unknown authors, 0 held, 0 needs-ruling; one payload block —
`watch-checkpoint.json`). repo-cleaner: gated `git fetch --prune` (pruned
`origin/608-...`), `primary_checkout_check.py` → clean on `main` @ `b18a011` (5 behind
`origin/main`, tree clean — not a sync_main case), `campaign_close.py 610` and `606` → all
checks pass, remotes confirmed gone; classification set changed, counter reset to 0; one
payload block (its report).

Prior plan (2026-08-18T01:44Z firing): entry 1 (apply the 01:44Z payloads + commit + push)
DONE — issue-sorter's window this firing opens at exactly 01:40:09Z, the prior firing's
checkpoint value, proving that payload landed and persisted; the remote `main` advanced
`7af35e7..315f66e`. Entry 2 (stash@{0} resolution) CARRIES FORWARD below — this firing's
repo-cleaner report carries no stash inventory, so its current state is unverified (not
evidence it resolved). Entry 3 (build-554 worktree removal) carries forward, now split per
repo-cleaner's fresh inventory: the worktree sits on a NEW since-merged branch (`608-...`),
and the old branch (`604-...`) survives as a stray local branch with no worktree.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing (no issue
bodies attached; no report names a #193 edge) — nothing reordered by the convention. One
operational dependency, named inline on its own entry: the build-554 worktree removal is
blocked by this live session's own close.

**needs-ruling lane:** empty — issue-sorter reports 0 needs-ruling, 0 held.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Pull the clean primary current, then apply this firing's payload blocks, commit + push
- **Action:** at `/Users/kimba/Projects/nonoun/plugins` (clean, on `main` @ `b18a011`, 5
  commits behind): `git pull --ff-only` first (repo-cleaner: tree clean, resolves on an
  ordinary pull — no quarantine case), then write the fenced payloads verbatim to their
  target paths: `.claude/ops/watch-checkpoint.json` (issue-sorter — checkpoint 02:17:47Z,
  strictly newer than the applied 01:40:09Z), `.claude/ops/reports/2026-08-18T02-19-25Z-repo-cleaner.md`
  (repo-cleaner), plus this rewritten `.claude/ops/plan.md`. Stage exactly those three paths
  (never `git add -A` — `stash@{0}`, if still present, stays out; see entry 2), read the
  status output, commit as a separate step (gate ≠ commit), push. decision-watcher owes no
  block — none staged. Apply at the shared checkout, not this worktree
  (ops-write-sandbox-rules stranding hazard).
- **Owner:** the dispatching session (coordinator); falls to Kim if writes to the shared
  checkout are blocked.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); both fenced blocks present in their seats' reports; repo-cleaner §Executed
  (primary clean on `main`, ff-pull safe, no dirt).
- **Size:** ~3 min.

**Class 2 — blocking other work:** none this firing — no open PRs, no seat blocked, nothing
measured as blocking anything queued.

**Class 3 — human decisions:**

### 2. Resolve `stash@{0}` ("sync_main quarantine") at the primary — carried forward, state unverified this firing
- **Action:** first `git -C /Users/kimba/Projects/nonoun/plugins stash list` — this firing's
  repo-cleaner report carries no stash inventory, so whether `stash@{0}` still exists is
  unmeasured. If gone, close this entry as resolved-by-events. If present, per the prior
  firing's per-file diff evidence: selectively restore ONLY
  `.claude/ops/sweep-in-flight.json` (foreign-only, session-matched live lock), then
  `git stash drop` — the other four stashed files were byte-identical to or superseded by
  HEAD. Stash resolution is judgment, outside repo-cleaner's gated calls.
- **Owner:** Kim (or the dispatching session, with Kim's confirm — one batched decision).
- **Evidence:** prior plan entry 2 (carried forward — the carry-forward source, not fresh
  evidence); prior firing's repo-cleaner §Stash diffs; this firing's repo-cleaner report is
  silent on the stash (unverified, not resolved).
- **Size:** ~3 min.

**Class 4 — hygiene debt:**

### 3. Delete stray local branch `604-repo-cleaner-off-main-finding` — runnable now
- **Action:** from the shared checkout: `git branch -D 604-repo-cleaner-off-main-finding`
  (@ `9d1f2f2`), then verify with `git branch -vv`. No worktree is attached, so this does
  not wait on session close. Stays propose-only from the seat: no host-repo reap script is
  named in this workspace's CLAUDE.md/README to gate it — a human or coordinator runs it
  deliberately.
- **Owner:** Kim (or the dispatching session, with Kim's confirm).
- **Evidence:** repo-cleaner §Inventory/§Proposed — PR #606 MERGED, `campaign_close.py 606`
  all checks pass, remote branch confirmed gone, no worktree attached.
- **Size:** ~1 min.

### 4. Remove worktree `build-554` + local branch `608-dispatch-ticket-file-bug-claim-fix` — blocked by this session's own close (named inline; do not start before it)
- **Action:** AFTER this live session closes: from the shared checkout root,
  `git worktree remove .claude/worktrees/build-554`, then
  `git branch -D 608-dispatch-ticket-file-bug-claim-fix`, then verify with
  `git worktree list` and `git branch -vv`. Carried forward from the prior plan's entry 3;
  the branch component changed this firing (the worktree moved from `604-...` to the
  since-merged `608-...`).
- **Owner:** Kim (or the next coordinator session, post-close).
- **Evidence:** repo-cleaner §Inventory/§Proposed — PR #610 MERGED, `campaign_close.py 610`
  all checks pass, upstream gone, worktree tree clean; same no-reap-script constraint.
- **Size:** ~2 min (post-session).

## Narrated-but-absent audit

- **decision-watcher:** clean — no-op clause cited explicitly ("no file-payload fences,
  names no report path"); no path narrated without a block.
- **issue-sorter:** clean — `watch-checkpoint.json` block present; `held-items.md` /
  `friendlies.json` explicitly declared unchanged and omitted; the per-firing report path
  explicitly declined ("this dispatch's own text response is the report"), not hedged.
- **repo-cleaner:** clean — its per-firing report block present; its gated git operations
  (fetch/campaign_close) are executed-and-evidenced git calls, not `.claude/ops/` writes —
  outside the sandbox contract, correctly narrated as executed.

## Not queued (checked, found clean or deliberately left)

- **4 new work items** (#613/#612/#611 feature+size:big, #609 bug+major): all fully
  record-shaped and kind-labeled at discovery, zero assignees, no stale claims under
  ADR-0005 — buildable backlog, not ops actions. The entry point to drive them to builds is
  teamwork's `/mobilize-chores` (with its own batched confirm), outside this queue's scope.
- **#605** — re-homed to `agent-ui`, pulled from this repo's queue (informational). **#490**
  — open by design (upstream pin-race tracking, anthropics/claude-code#87349), active
  evidence comments, not stale.
- **Open PRs:** none (`gh pr list --state open` → empty); `git ls-remote` shows only
  `refs/heads/main` — every merged PR's remote branch confirmed gone, nothing to reap
  remotely.
- **Primary 5 commits behind `origin/main`:** folded into entry 1's ff-pull, not its own
  entry — tree clean, no gate covers clean-but-stale, per repo-cleaner.
- **`gitignore_check.py` WARNs:** the two standing accepted WARNs (`dist/`,
  `harness-audit-*/`) at the primary; the worktree's two extras (`.DS_Store`,
  `.claude/worktrees/`) are nested-worktree artifacts — identical set to last firing, no
  G2 FAIL.
- **ADR corpus:** 20/20 previously known, no delta, checkpoint correctly un-advanced —
  clean no-op.

## Resolved since the prior plan (2026-08-18T01:44Z firing)

- Prior entry 1 (apply the 01:44Z payloads + commit + push) — DONE: checkpoint continuity
  proves it (this firing's issue-sorter window opens at the applied 01:40:09Z mark); remote
  `main` advanced `7af35e7..315f66e`.
- Prior entry 2 (stash@{0} resolution) — CARRIED FORWARD as entry 2, state unverified this
  firing (no stash inventory in this firing's evidence).
- Prior entry 3 (build-554 worktree + branch removal) — CARRIED FORWARD, split into entries
  3 and 4: the `604-...` branch is now stray with no worktree (runnable now); the worktree
  itself sits on since-merged `608-...` (post-session).
