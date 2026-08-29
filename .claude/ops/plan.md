# Ops plan: kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-28T22:57:00Z**. Evidence:
three seat reports attached and complete; UNMEASURED this firing: **[]** (all three seats fired
and returned full reports — decision-watcher, issue-sorter, repo-cleaner). This dispatch's own
instruction was explicit and stricter than the prior firing's: judge exactly the three attached
reports, refetch nothing — no supplementary live `gh`/`git` corroboration was run this firing
(unlike the prior firing's own latitude). The only reads performed beyond the three reports were
this repo's own durable `.claude/ops/` state (prior `plan.md`, `adr-checkpoint.json`,
`adr-queue.json`, `watch-checkpoint.json`, `sweep-in-flight.json`) — required for the
prior-plan carry-forward and target-path/shape checks below, never used to override or second-guess
a seat's own judgment.

**Payload audit (ops-write-sandbox-rules):**
- **decision-watcher**: clean. Two blocks (`adr-checkpoint.json`, `adr-queue.json`), both present,
  self-contained, match its own report's claims exactly (27 entries, `formula_version: 2`, one
  harvest candidate `adr-0027`). One data-quality artifact riding inside the payload, not a
  shape violation: `adr-0027`'s `status` field carries the un-stripped template placeholder
  comment (`"accepted        # proposed | accepted | superseded"`) — the report's own "Secondary
  finding" section names this as a live reproduction of a checkpoint-script extraction defect, not
  hand-fixed by this agent (correct — it is not this agent's job to silently launder the tool's
  own output); flagged again below as hygiene debt rather than absorbed silently.
- **issue-sorter**: clean. Both blocks (own report, `watch-checkpoint.json`) present,
  self-contained, checkpoint timestamps agree (`2026-08-29T00:11:19Z` on both `issues_checkpoint`
  and `prs_checkpoint`); `friendlies.json`/`held-items.md`/`.mcp.json` correctly named unchanged
  with no blocks (nothing to apply).
- **repo-cleaner**: clean. One block (own report), present, self-contained, matches its stated
  path and "executed: nothing beyond the standing `fetch --prune` exception" claim.

No narrated-but-absent violations this firing.

**Prior plan (2026-08-28T01:01:40Z firing) reconciliation:** all 4 entries + the 1 carried hygiene
item resolved.
- Entry 1 (apply payloads): DONE — confirmed via this repo's own durable state:
  `watch-checkpoint.json`'s `issues_checkpoint`/`prs_checkpoint` already read `2026-08-28T01:02:22Z`
  (issue-sorter's own prior-firing stamp) before this firing touched it; `adr-checkpoint.json` held
  exactly the pre-migration 26-entry shape decision-watcher's report expected.
- Entry 2 (commit and push applied ops state): DONE — repo-cleaner's report confirms `main` is
  `+0/-0` against `origin/main` with a clean tree, which only holds if the prior firing's commit
  landed and pushed.
- Entry 3 (decision-watcher: emit complete, accurately-shaped fenced payload blocks directly,
  carried 2 firings): **RESOLVED this firing** — the prior no-op firing gave no test; this firing
  did (a real candidate, adr-0027), and both blocks landed complete and shape-correct per the
  Payload audit above. Closing the carried item; not re-opening it over the separate
  script-behavior defect noted below (that is the underlying tool's bug, not decision-watcher's
  own payload-shaping).
- Entry 4 (#945, adr_checkpoint.py hash-basis migration had no path): DONE — repo-cleaner confirms
  #945 is now CLOSED; decision-watcher's own report independently confirms the migration executed
  cleanly this firing (0/26 hash diffs, lossless re-baseline to `formula_version: 2`).

**Parked-issue check (#611):** #617 stays dropped, parked #617 — not independently reconfirmed as
still `backlog`-labeled this firing (this dispatch's refetch-nothing instruction precluded a live
label check), carried forward from the prior plan's own state per the carry-forward contract; no
seat's report this firing contradicts the parked classification. No focus instruction in this
dispatch names #617, so it is not un-parked.

**Blocked-by (#193):** no `Blocked-by:` line appears anywhere in the text of this firing's three
attached reports — the only issue-body excerpt quoted verbatim (#987's cross-repo provenance note)
carries none. Per this dispatch's own refetch-nothing instruction, open-issue bodies were not
independently fetched live to check further this firing (stricter than the prior firing's own
corroboration latitude). Nothing reordered on this basis.

**needs-ruling lane:** empty. No seat names a `needs-ruling`-labeled issue this firing;
issue-sorter's report explicitly classifies #987 (its one unlabeled discovery) as "not
ruling-shaped."

**Lock-file note:** `.claude/ops/sweep-in-flight.json` names session `plugins-c4` (pid 81159,
`startedAt` `2026-08-29T00:09:56.524Z`) — repo-cleaner's own report independently classifies this
as this firing's own coordinator lock, the same live-coordinator-state pattern every prior firing
has read it as, not cruft. Never quarantine it via `sync_main.py`, never stage it in entry 2; it
clears itself when the sweep exits. Apply all fenced payloads at the shared checkout
`/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1, gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: decision-watcher's `adr-checkpoint.json`
  (27 entries, `formula_version: 2`) and `adr-queue.json` (1 candidate, `adr-0027`); issue-sorter's
  own report (`.claude/ops/reports/2026-08-29T00:11:19Z.md`) and `watch-checkpoint.json`
  (github source advanced to `2026-08-29T00:11:19Z`); repo-cleaner's own report
  (`.claude/ops/reports/2026-08-29T00-12-29Z-repo-cleaner.md`); plus this rewritten
  `.claude/ops/plan.md`. No `friendlies.json` / `held-items.md` / `.mcp.json` blocks
  (issue-sorter: explicitly unchanged).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** the three seats' fenced blocks; Payload audit above finds all clean.
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
- **Evidence:** repo-cleaner's report (`main` `+0/-0`, clean tree); ops-write-sandbox-rules (state
  persists through the repo, or the next firing starts blind).
- **Size:** ~3 min.

**Class 3, human-decision items:**

### 3. Confirm decision-watcher's adr-0027 harvest candidate
- **Action:** decision-watcher's queued candidate (`adr-queue.json`, `adr_id: adr-0027`) proposes
  extending `docs/skills/doc-writing-rules/references/`'s existing T4/ledger-lock material with
  ADR-0027's narrow carve-out (an already-accepted ADR may move `intent-refs:` from empty/`null`
  to a non-empty citation, verified as a single-field diff). Verified genuinely new — grepped
  against `origin/main` this firing found the general T4 lock/unlock mechanic and `intent-refs:`
  as a field, but no existing reference names this specific single-field backfill exception. No
  human was present at dispatch (unattended firing), so the batch `AskUserQuestion` confirm was
  deferred rather than attempted blind. On confirm: `/make-pack docs` targeting
  `docs/skills/doc-writing-rules/references/`, extend (not new-skill).
- **Owner:** Kim (confirm), then Kim or a dispatched builder (the `/make-pack` extend itself).
- **Evidence:** decision-watcher's report (Placement check, Phase 2, resolved against
  `origin/main`); ADR-0027 itself
  (`.claude/docs/adr/0027-narrow-t4-carve-out-for-intent-refs-backfill.md`).
- **Size:** ~5 min (confirm) + ~15-20 min (the extend-reference change itself, once confirmed).

### 4. Batch-confirm repo-cleaner's proposed local-disk cleanup
- **Action:** two destructive-but-verified-clean proposals, neither backed by a gated script in
  this repo (hence propose-only, not Class 1): (a) `git worktree remove
  .claude/worktrees/plugins-reviewer` — a registered worktree, detached HEAD `878a3c29`, no
  branch, no PR references it, clean tree; (b) `rm -rf` each of
  `.claude/worktrees/claude-plugins-{958,959,963,964,973,974,977,978,979,980}` — ten leftover
  full-clone scratch dirs (not `git worktree`-registered), each clean, each on a branch whose
  remote ref this firing's own `fetch --prune` just confirmed already gone (remote-side close
  already happened). A human confirms before either runs.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's report (`git worktree list`, individual per-directory
  `git status`/`git ls-remote` checks, e.g. `claude-plugins-978`'s branch traced to merged PR #988
  with its remote ref confirmed gone).
- **Size:** ~5 min (confirm) + ~2 min (execute both).

**Class 4, hygiene debt:**

### 5. #987 — adr_checkpoint.py periodically truncates a stored sha256 to 57 hex chars (referenced by id)
- **Action:** `harness/scripts/adr_checkpoint.py` truncates a recorded hash on write/merge in some
  runs (filed against a cross-repo occurrence, `adr-0065` in gen-ui-kit, relayed via the
  adia-marshals channel; dedup-checked by issue-sorter against #945/#956, distinct symptom, no
  duplicate). #987 is the record — build against it directly. Corroborating evidence found live in
  THIS repo this same firing: decision-watcher's payload for `adr-0027` carries an un-stripped
  template placeholder comment inside its `status` field
  (`"accepted        # proposed | accepted | superseded"`, from the ADR frontmatter's own inline
  comment at line 4) — a different manifestation (comment-not-trimmed vs. hash-truncated) but the
  same script, same class of field-extraction/normalization defect, and not yet its own ticket.
  Whoever builds #987 should check whether both symptoms share one root cause in the same
  extraction path before treating them as unrelated.
- **Owner:** Kim (or a dispatched builder seat, e.g. via `/mobilize-chores` or `dispatch-ticket`)
  — same precedent as the prior plan's #945 entry.
- **Evidence:** issue-sorter's report (#987 discovered unlabeled, dedup-checked, labeled
  `bug`+`major`, OPEN); decision-watcher's report "Secondary finding" section; issue #987 itself;
  this repo's own `.claude/ops/adr-checkpoint.json` post-apply (entry 1).
- **Size:** ~30-60 min for #987 itself (per its own filed repro/acceptance criteria); +~10 min to
  assess whether the live status-field corruption is the same root cause.

### 6. #978 — tracking issue may be stale-open after its own branch merged
- **Action:** `#978` ("sweep 22 orphan ADRs") already carries a correct label per issue-sorter's
  classification this firing (no repair needed) and its own working branch
  (`978-sweep-22-orphan-adrs`) traced to merged PR #988, with the remote ref confirmed gone by this
  firing's own `fetch --prune` — repo-cleaner independently verified it is not live
  work-in-progress despite the name coincidence. A routine post-merge close-out (or a status
  comment naming what remains) looks pending on the issue itself; read the issue, confirm whether
  all of its own listed sub-items are done, close or comment accordingly.
- **Owner:** Kim (or issue-sorter's next firing, once it re-touches #978).
- **Evidence:** repo-cleaner's report (`claude-plugins-978`'s branch → merged PR #988, remote ref
  gone, "not live work-in-progress on the still-open tracking issue #978"); issue-sorter's report
  (#978 in the 21/22 correctly-labeled touched set).
- **Size:** ~5 min.

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`**: this firing's own lock (session `plugins-c4`, pid 81159); see
  Lock-file note; never queued as cleanup.
- **dropped: parked #617**: see Parked-issue check above; not a numbered entry, not un-parked.
- **#945, #948**: both now CLOSED this window (repo-cleaner) — dropped from tracking; #945's
  underlying gap is entry 5 above's own record now (#987), a distinct follow-on, not a reopening.
- **#932**: closed several firings ago; fully out of scope, no longer tracked.
- **#609**: open bug/major, zero assignees, unchanged this firing, buildable/tracked backlog
  (platform-defect record, not ops-sweep work), outside this queue; `doing` label not treated as a
  claim absent a ruling naming it as one (same precedent as every prior firing).
- **18 PRs merged this window** (#951, #953, #955, #966, #967, #969, #970, #971, #972, #975, #976,
  #981, #982, #983, #984, #985, #986, #988): context only, all `kimgranlund`, already reflected
  above.
- **18 pruned remote refs** (see repo-cleaner's report for the full list): already gone,
  repo-cleaner's standing `fetch --prune` exception, no further action.
- **Gitignore 2 WARN** (`harness-audit-*/`, `.name-map.md`): already RULED keep-all by Kim
  2026-08-24 (commit `a871ea9`, then covering 3 entries including `dist/`); `dist/` has since
  gained real tree content and dropped off the stale-match list on its own — nothing to action;
  the remaining 2 inherit the same keep ruling, no new review owed.
- **Stale-claim check**: clean, all 4 open issues (#987, #978, #617, #609) carry zero assignees
  under ADR-0005.
- **Off-main-primary**: none — `primary_checkout_check.py` reads PASS.
- **2 older issues touched again in-window, predating the checkpoint, already actioned prior
  firing**: no new action (per issue-sorter).

## Resolved since the prior plan (2026-08-28T01:01:40Z firing)

- Prior entry 1 (apply payloads): DONE.
- Prior entry 2 (commit and push): DONE, `main` `+0/-0` with origin.
- Prior entry 3 (decision-watcher payload completeness, carried 2 firings): RESOLVED this firing —
  first real test since opening, passed clean.
- Prior entry 4 (#945): DONE, closed; follow-on gap now tracked as #987 (entry 5 above), a fresh
  ticket, not a reopening.
- **#948**: also closed this window (was tracked backlog outside the queue, not a queue entry) —
  dropped from "Not queued" tracking.

Dispatch: 2026-08-28T22:57:00Z
