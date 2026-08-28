# Ops plan: kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-28T01:01:40Z**. Evidence: all
three seat reports attached and complete, no seat UNMEASURED this firing (dispatch-named UNMEASURED
list: `[]`). Per this dispatch's own instruction, evidence is exactly the three attached reports;
no supplementary live `gh`/`git` fetch was used to *drive* queue decisions. The handful of
corroborating checks below (git log/branch/rev-list state, `sweep-in-flight.json`'s own content,
open-issue bodies checked for `Blocked-by:` lines) verify claims already made in the reports or the
prior plan's own carried state, the same durable/live cross-check latitude the prior firing's plan
used.

decision-watcher: clean no-op, 26/26 ADRs matched checkpoint exactly, no new/amended/superseded
ADRs, `adr-queue.json` empty (0 candidates); no payload fence, correctly per the no-op clause
(nothing changed to write). issue-sorter: window since 2026-08-25T17:20:49Z, 8 new issues (#933,
#936, #937, #938, #939, #945, #948, #949) plus PRs touched in-window (#934, #935, #940, #941, #942,
#943, #944, #946, #947, #950), all `kimgranlund`-authored and already correctly filed, 0 mints,
0 repairs, 0 held, 0 ruling-shaped; checkpoint advances to 2026-08-28T01:02:22Z. repo-cleaner:
`git fetch --prune` (4 stale refs pruned, all matching already-merged PRs #935/#946/#947/#950);
primary clean/PASS; classification set changed from prior firing (orphaned branch resolved, `main`
now `+0/-0` with origin, issue churn: #932 closed, #945/#948 new); full report owed, not
abbreviated; nothing executed beyond the standing `fetch --prune` exception.

**Payload audit (ops-write-sandbox-rules):**
- **decision-watcher**: clean; correctly invoked the no-op clause (nothing changed this firing, no
  file-payload fence, no report path named), not a narrated-but-absent violation, the contract
  explicitly permits this shape.
- **issue-sorter**: clean; both blocks (its own per-firing report, `watch-checkpoint.json`) present,
  self-contained, match its own stated paths/claims exactly; `friendlies.json`/`held-items.md`/
  `.mcp.json` correctly named as unchanged with no blocks (nothing to apply).
- **repo-cleaner**: clean; its one block (`2026-08-28T01-02-49Z-repo-cleaner.md`) present,
  self-contained, matches its own stated path and "executed: nothing" claim.

**Prior plan (2026-08-25T17:19:54Z firing) reconciliation:** four of five entries DONE, one still
open, carried forward.
- Entry 1 (apply payloads): DONE, per-firing (commit `9454145`, "persist 2026-08-25T17:19:54Z sweep
  state").
- Entry 2 (delete orphaned local branch `927-dispatch-envelope-refspec`): DONE, repo-cleaner
  confirms it is gone; `git branch -a` / `git ls-remote --heads origin` show only `main` on both
  sides this firing.
- Entry 3 (pull main, then commit/push applied ops state): DONE, `main` is `+0/-0` against origin;
  ops-state commits landed (`9454145`, `3e7ad38`). Unrelated ops activity from a different seat
  landed in between (fleet-bootstrap/marshal commits `b5fb68d`, `6c5f551`, outside chore-planner's
  own scope, noted only for context).
- Entry 4 (confirm adr-0026 harvest candidate): DONE, `adr-queue.json` is now empty; the candidate
  was filed as issue #933 (task+size:small, confirmed CLOSED by issue-sorter's own discovery this
  firing) and cleared from the queue (commit `3e7ad38`, "clear adr-0026 harvest candidate, filed as
  gh#933").
- Entry 5 (decision-watcher: emit complete, accurately-shaped fenced payload blocks directly):
  STILL OPEN, carried forward as entry 3 below. No commit since the prior firing touches
  decision-watcher's or `watch-adrs`' procedure, and this firing gave no opportunity to test the fix
  (clean no-op, nothing to write), unverified either way, so it carries forward rather than being
  marked resolved on silence.

**Parked-issue check (#611):** #617 stays dropped, parked #617, confirmed still `backlog`-labeled
this firing; carried informationally only, never a numbered queue entry. No focus instruction in
this dispatch names #617, so it is not un-parked.

**Blocked-by (#193):** no `Blocked-by:` line found in any of this firing's three attached reports,
or in the open-issue bodies checked while corroborating them (#609: none; #945: none; #948:
explicit "Blocked-by: none" in its own Scope/Open section). Nothing reordered this firing.

**needs-ruling lane:** empty. issue-sorter's report states 0 ruling-shaped items this firing (the
`needs-ruling` label does not yet exist in the repo), and no seat names a `needs-ruling`-labeled
issue.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` names session `plugins-62` (pid 66279,
`startedAt` `2026-08-28T01:01:40.502Z`, an exact match to this firing's own key). Never quarantine
it via `sync_main.py`, never stage it in entry 2; it clears itself when the sweep exits. Apply all
fenced payloads at the shared checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1, gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: issue-sorter's own report
  (`.claude/ops/reports/2026-08-28T01:02:22Z.md`), issue-sorter's `watch-checkpoint.json` (github
  source advanced to `2026-08-28T01:02:22Z`), repo-cleaner's own report
  (`.claude/ops/reports/2026-08-28T01-02-49Z-repo-cleaner.md`), plus this rewritten
  `.claude/ops/plan.md`. decision-watcher emits no block this firing (clean no-op, correctly
  invoked per the no-op clause), nothing to apply for it. No `friendlies.json` / `held-items.md` /
  `.mcp.json` blocks (issue-sorter: explicitly unchanged).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** three seat reports' fenced blocks; Payload audit section above finds all clean,
  nothing needing correction (unlike the prior firing's decision-watcher truncation).
- **Size:** ~2 min.

**Class 2, blocking other work:**

### 2. Commit and push this firing's applied ops state (recurring)
- **Action:** `main` is already `+0/-0` with `origin/main` (no pull needed first, per
  repo-cleaner). Once `sweep-in-flight.json` is confirmed cleared (this sweep's own marker,
  expected gone on exit), from `/Users/kimba/Projects/nonoun/plugins` on `main` stage exactly the
  ops-state paths entry 1 applied, never `git add -A`, never `sweep-in-flight.json`, read the
  status output, commit as a separate step, push, then re-verify via
  `git ls-remote origin refs/heads/main` against `git rev-parse HEAD` (push-verification
  convention, ops-write-sandbox-rules) before reporting it landed.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's report (`main` `+0/-0`, clean tree) plus `git rev-list` cross-check
  this firing; ops-write-sandbox-rules (state persists through the repo, or the next firing starts
  blind).
- **Size:** ~3 min.

**Class 3, human decisions:** none this firing. decision-watcher's queue is empty (no harvest
candidate to confirm), issue-sorter held 0 items, and repo-cleaner found no open PRs needing a
merge decision.

**Class 4, hygiene debt:**

### 3. decision-watcher: emit complete, accurately-shaped fenced payload blocks directly (carried forward, still open, 2nd firing)
- **Action:** unchanged from the prior plan's entry 5, decision-watcher's own procedure should emit
  full, correctly-shaped payload content in-fence rather than truncating or drifting from its own
  scratch state whenever it does have something to write. This firing gave no test of the fix
  (clean no-op, nothing to write), so it stays open on the same terms rather than being marked
  resolved on silence; watch it resolve or recur the next firing decision-watcher actually emits a
  payload.
- **Owner:** Kim (or whoever next touches decision-watcher's procedure skill).
- **Evidence:** prior plan's Payload audit (2026-08-25T17:19:54Z firing); no commit since then
  touches decision-watcher's or `watch-adrs`' procedure files.
- **Size:** ~10 min.

### 4. #945, adr_checkpoint.py's #929 hash-basis widening has no checkpoint migration path (NEW, referenced by id)
- **Action:** `harness/scripts/adr_checkpoint.py`'s `classify` command changed its checkpoint hash
  basis (introduced by issue #929) with no migration path shipped alongside it; an existing
  checkpoint written under the old formula reads as 100% amended in one flood against the new
  formula (observed in a sibling repo at 226 ADRs against a true delta of ~4; not yet triggered in
  this repo, whose 26-ADR checkpoint currently reads clean this firing). #945 is the complete
  record (repro, acceptance criteria, a verified-but-manual workaround), build against it directly,
  no restatement here. It directly affects decision-watcher's own evidence pipeline (`watch-adrs`),
  so it is ops-family hygiene debt even though it is filed as a standalone bug.
- **Owner:** Kim (or a dispatched builder seat, e.g. via `/mobilize-chores` or `dispatch-ticket`).
- **Evidence:** issue-sorter's report (#945 discovered, bug+major, OPEN); issue #945 itself.
- **Size:** ~30 to 60 min (#945 names three fix directions, any one closes it).

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`**: this sweep's own lock (session `plugins-62`, pid 66279, `startedAt`
  an exact match to this firing's key); flagged in the lock-file note and entry 2's exclusion;
  never queued as cleanup.
- **dropped: parked #617**: confirmed still `backlog`-labeled this firing; never a numbered queue
  entry; not un-parked (no focus instruction named it this dispatch).
- **#932**: now CLOSED (was open two firings ago as task/size:big backlog); dropped from tracking,
  resolved via merge (PR #935, per repo-cleaner's pruned-ref list).
- **#609**: open bug/major, zero assignees, unchanged this firing, buildable/tracked backlog
  (platform-defect consolidating record, not ops-sweep work), outside this queue; `doing` label not
  treated as a claim absent a ruling naming it as one (same precedent as prior firings).
- **#948**: open task/size:small, zero assignees, requires a human Figma seat (product/design work,
  explicitly "not automatable from this workspace"), outside this queue; tracked backlog, same
  treatment as #932/#609 in prior firings.
- **PRs merged this window** (#934, #935, #940, #941, #942, #943, #944, #946, #947, #950): context
  only, all `kimgranlund`, already reflected above.
- **4 pruned remote refs** (`origin/932-fleet-bootstrap-fleet-connect`,
  `origin/949-marshal-live-lane-delegation`, `origin/live/make-figma-skill`,
  `origin/live/make-figma-skill-agents-commands`): already gone, repo-cleaner's standing
  `fetch --prune` exception, no further action.
- **Gitignore 3 WARN** (`dist/`, `harness-audit-*/`, `.name-map.md`): already RULED keep-all by Kim
  2026-08-24 (commit `a871ea9`); unchanged this firing; no new action, no re-review owed.
- **Stale-claim check**: clean, all 4 open issues (#948, #945, #617, #609) carry zero assignees.
- **Off-main-primary**: none, `primary_checkout_check.py` reads PASS.
- **2 older issues touched again in-window, predating the checkpoint** (#932, #609): no new action
  (per issue-sorter).

## Resolved since the prior plan (2026-08-25T17:19:54Z firing)

- Prior entry 1 (apply payloads): DONE, commit `9454145`.
- Prior entry 2 (delete orphaned branch `927-dispatch-envelope-refspec`): DONE, confirmed gone.
- Prior entry 3 (pull main, then commit/push): DONE, `main` `+0/-0`, commits landed (`9454145`,
  `3e7ad38`).
- Prior entry 4 (confirm adr-0026 harvest candidate): DONE, filed as #933, queue cleared (commit
  `3e7ad38`).
- **#932**: closed since the prior plan (merged as PR #935); dropped from "Not queued" tracking.
- #929's underlying migration risk resurfaced as new issue #945 (see entry 4 above); the fix for
  #929 itself already merged (`0dcd3e3`, PR #931, noted resolved two firings ago); this is a fresh
  follow-on gap, not a reopening.

Dispatch: 2026-08-28T01:01:40Z
