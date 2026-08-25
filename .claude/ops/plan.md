# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-25T17:19:54Z**. Evidence: all
three seat reports attached and complete — **no seat UNMEASURED this firing** (dispatch-named
UNMEASURED list: `[]`). Per this dispatch's own instruction, evidence is exactly the three attached
reports — no supplementary live `gh`/`git` fetch was used to *drive* queue decisions; the handful
of corroborating checks below (branch/behind-count, #611 park-label, prior-entry closure) verify
claims already made in the reports or the prior plan's own carried state, the same durable/live
cross-check latitude the prior firing's plan used.

decision-watcher: 26/26 ADRs scanned; one new ADR (adr-0026, ratified 2026-08-23) narrows IDR-0005's
zero-further-investment clause to audience-facing surface only, leaving cross-harness/agent-runtime
work under IDR-0001 instead — passes the impact bar (no `skills/*/references/*.md` anywhere cites
either IDR, checked against `origin/main`), queued as a harvest candidate. No amended/superseded
ADRs this firing. issue-sorter: window since 2026-08-24T03:52:28Z, 8 new issues (#919, #921, #922,
#924, #927, #929, #930, #932) + 8 PRs, all `kimgranlund`-authored and already correctly filed —
0 mints, 0 repairs, 0 held, 0 ruling-shaped; one cosmetic note (closed #929 missing a severity
label) explicitly left unactioned by issue-sorter itself. repo-cleaner: `git fetch --prune` (1 stale
ref pruned, matching merged PR #928); primary clean/PASS; classification set changed from prior
firing (new orphaned local branch, `main` now behind origin by 1, gitignore WARNs 4→3, issue churn)
— full report owed, not abbreviated; nothing executed beyond the standing `fetch --prune` exception.

**Payload audit (ops-write-sandbox-rules):**
- **decision-watcher — a real deviation, not a violation of "absent," but of "verbatim."** Its
  `adr-checkpoint.json` fence is explicitly disclosed as truncated (3 of 26 entries, "truncated for
  readability only") and its `adr-queue.json` fence — NOT disclosed as truncated — uses a different
  field shape (`adr`, no `plan`/`queued_at`, no `_comment`) than its own scratch file (`adr_id`,
  `plan`, `queued_at`, and the `_comment` preserving prior-harvest history). Both deviations are
  resolved by decision-watcher's own closing line naming both scratch paths as "full, exact content
  to apply." This firing's shared scratchpad made independent verification possible: both scratch
  files (`/private/tmp/claude-501/-Users-kimba-Projects-nonoun-plugins/7bec92f9-2a20-447a-8c98-585db0f5e3fa/scratchpad/adr-checkpoint.json`,
  `.../scratchpad/adr-queue.json`) read complete and self-consistent — 26 ADR entries; 1 queue
  candidate (adr-0026) matching the report's own evidence prose. Entry 1 below sources from those
  two scratch paths, not the fenced text shown in decision-watcher's report — applying that fenced
  text verbatim would have written a 3-entry checkpoint and a wrong-shaped queue file. Flagged as a
  new (first-occurrence, disclosed, not escalated) hygiene item, entry 5.
- **issue-sorter:** clean, and the prior firing's recurring gap is closed — both blocks (its own
  per-firing report, `watch-checkpoint.json`) are present, self-contained, and match its own stated
  paths/claims exactly (no external pointer, no hedge language).
- **repo-cleaner:** clean — its one block (`2026-08-25T17-21-55Z-repo-cleaner.md`) is present,
  self-contained, and matches its own stated path and "executed: nothing" claim.

**Prior plan (2026-08-24T03:51:50Z firing) reconciliation:** all four entries — **DONE**.
Entry 1 (apply payloads) — done, per-firing. Entry 2 (commit+push) — DONE: commits `0d60e08`
("persist 2026-08-24T03:51:50Z sweep state") and `a871ea9` ("record gitignore keep-all ruling on
plan entry 3"); confirmed via `git log -- .claude/ops/`. Entry 3 (gitignore review) — DONE, closed
within that same firing (Kim ruled keep all, commit `a871ea9`); the 3 WARNs repo-cleaner reports
this firing are the *same three* already ruled, `__pycache__` resolved itself off the list. Entry 4
(issue-sorter's recurring narrated-but-absent report gap) — DONE, two ways: infrastructure defense
landed (`#924` fix via PR #926, commit `7cad197` — `chore_sweep_apply.mjs`'s `WRITE_VERBS`
detection now catches "report target"-shaped phrasing with no write-verb, so a future regression
gets caught mechanically) **and** this firing's issue-sorter report itself complies (block emitted,
matches its own claimed path exactly) — no recurrence. Nothing else carries forward; this firing's
queue is built fresh from this firing's own three reports.

**Parked-issue check (#611):** #617 stays **dropped: parked #617** — live-checked this firing
(`gh issue view 617`) and confirmed still `backlog`-labeled; carried informationally only, never a
numbered entry. No focus instruction in this dispatch names #617, so it is not un-parked.

**Blocked-by (#193):** no `Blocked-by:` line in any of this firing's three attached reports or in
the issue bodies touched while corroborating them (#609, #932) — nothing reordered this firing.

**needs-ruling lane:** empty — issue-sorter's report states 0 ruling-shaped items this firing, and
no seat names a `needs-ruling`-labeled issue.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary names session `plugins-28`
(pid 73478, startedAt `2026-08-25T17:19:52.753Z` — ~2s ahead of this firing's own key, same-session
match; `ps -p 73478` finds no matching process, consistent with a just-started sweep, not a stale
lock). Never quarantine it via `sync_main.py`, never stage it in entry 3; it clears itself when the
sweep exits. Apply all fenced payloads at the shared checkout
`/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim, with one correction: for
  `.claude/ops/adr-checkpoint.json` and `.claude/ops/adr-queue.json`, source content from
  decision-watcher's two named scratch files (paths above under Payload audit), **not** the fenced
  text shown in its report — those two files are complete/verified, the report's own fences are
  truncated/mismatched. Also apply `.claude/ops/watch-checkpoint.json` (issue-sorter — github
  source advanced to 2026-08-25T17:20:49Z), `.claude/ops/reports/2026-08-25T17:20:49Z.md`
  (issue-sorter's own report), `.claude/ops/reports/2026-08-25T17-21-55Z-repo-cleaner.md`
  (repo-cleaner's own report), plus this rewritten `.claude/ops/plan.md`. No `friendlies.json`/
  `held-items.md` blocks (issue-sorter: explicitly unchanged).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** three seat reports' fenced blocks + verified scratch files + this plan; Payload
  audit section above names the one correction rather than applying corrupted content silently.
- **Size:** ~2 min.

### 2. Delete the orphaned local branch `927-dispatch-envelope-refspec`
- **Action:** `git branch -d 927-dispatch-envelope-refspec` — fully merged via PR #928, remote
  already deleted (confirmed: `git branch -vv` shows `[origin/927-dispatch-envelope-refspec: gone]`;
  `git fetch --prune` already pruned the matching remote-tracking ref this firing). No host-repo
  reap script exists, so repo-cleaner proposed only per its own local-branch rule.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's 2026-08-25T17:21:55Z report; `git branch -vv` output cross-checked
  this firing.
- **Size:** ~1 min.

**Class 2 — blocking other work:**

### 3. Pull `main` up to date, then commit + push this firing's applied ops state (recurring)
- **Action:** `main` is behind `origin/main` by exactly 1 commit (`0dcd3e3` — the #929 fix, merged
  as PR #931; confirmed via `git rev-list --count HEAD..origin/main` = 1; that commit touches only
  `harness/` files, not `.claude/ops/`, so no conflict risk with entry 1's writes). Once
  `sweep-in-flight.json` is confirmed cleared (this sweep's own marker, expected gone on exit):
  `git pull --ff-only`, then from `/Users/kimba/Projects/nonoun/plugins` on `main` stage exactly
  the ops-state paths entry 1 applied — never `git add -A`, never `sweep-in-flight.json` — read the
  status output, commit as a separate step, push.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's report + `git status --branch`/`git rev-list` cross-check this
  firing; ops-write-sandbox-rules (state persists through the repo or the next firing starts
  blind).
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 4. Confirm decision-watcher's one pending ADR-queue candidate (adr-0026, harvest)
- **Action:** one batched `AskUserQuestion` round covering the single pending candidate in
  `adr-queue.json` (adr-0026 — narrows IDR-0005's scope-narrowing clause to audience-facing surface
  only; no existing skill/references file cites either IDR, so this is genuinely new routing
  knowledge, not a duplicate). On confirm, the concrete next step is `/make-pack` or `/make-skill`
  placement (docs' `save-lessons` Phase 2) — likely a new reference file, since none currently owns
  IDR/ADR routing citations.
- **Owner:** Kim.
- **Evidence:** decision-watcher's 2026-08-25T17:19:54Z report; `adr-queue.json` (post entry-1
  apply) carries the one candidate.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 5. decision-watcher: emit complete, accurately-shaped fenced payload blocks directly (NEW — first occurrence, disclosed)
- **Action:** decision-watcher's report this firing shipped a truncated `adr-checkpoint.json` fence
  and an undisclosed field-shape mismatch in its `adr-queue.json` fence versus its own scratch
  source (see Payload audit above) — resolved only by a closing note redirecting to scratch paths.
  This is a softer variant of the narrated-but-absent class the prior plan escalated for
  issue-sorter (entry 4, now closed): the fence itself should be the complete, accurate write per
  ops-write-sandbox-rules ("the fenced block IS the write"), not a pointer requiring an out-of-band
  read this sweep's shared scratchpad happened to make possible but which the contract does not
  document as guaranteed. Whoever next revises decision-watcher's own procedure skill should make
  it emit the full, correctly-shaped content in-fence (or split across multiple correctly-headed
  fences) rather than truncating or drifting from its own scratch state.
- **Owner:** Kim (or whoever next touches decision-watcher's procedure skill).
- **Evidence:** this firing's Payload audit above; direct read of both scratch files versus both
  fenced blocks in decision-watcher's own report.
- **Size:** ~10 min.

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`** — this sweep's own lock (startedAt ~2s before the firing key, session
  `plugins-28`); flagged in the lock-file note and entry 3's exclusion; never queued as cleanup.
- **dropped: parked #617** — confirmed still `backlog`-labeled this firing; never a numbered queue
  entry; not un-parked (no focus instruction named it this dispatch).
- **#932 (NEW)** — `task`, `size:big`, zero assignees — buildable/tracked backlog, outside this
  queue (same treatment as prior firings' #914/#913/#609).
- **#609** — open bug/major, zero assignees, unchanged this firing — buildable/tracked backlog,
  outside this queue; `doing` label not treated as a claim absent a ruling naming it as one (same
  precedent as the prior two firings).
- **#490 — now CLOSED** (was tracked as open in the two prior plans; repo-cleaner's current
  open-issue count of exactly 3 — #932, #617, #609 — confirms it dropped off); no longer needs a
  "not queued" mention.
- **#914, #913 — now CLOSED** (open two firings ago; repo-cleaner confirms closed this firing).
- **issue-sorter's #929 label-completeness note** — closed issue #929 (already fixed/merged via PR
  #931) carries `bug` with no severity label; issue-sorter itself left this unactioned ("no triage
  decision pending" on resolved history) — noted here for visibility, not queued, respecting that
  judgment.
- **8 PRs merged this window** (#917, #918, #920, #923, #925, #926, #928, #931) — context only, all
  `kimgranlund`, all already reflected in the "Resolved since prior plan" section below.
- **1 pruned remote ref** (`origin/927-dispatch-envelope-refspec`, behind merged PR #928) — already
  gone; entry 2 covers the leftover local copy.
- **Gitignore 3 WARN** (`dist/`, `harness-audit-*/`, `.name-map.md`) — already RULED keep-all by Kim
  2026-08-24 (commit `a871ea9`); no new action, no re-review owed.
- **Stale-claim check** — clean: all 3 open issues (#932, #617, #609) carry zero assignees.
- **Off-main-primary** — none; `primary_checkout_check.py` reads PASS.

## Resolved since the prior plan (2026-08-24T03:51:50Z firing)

- Prior entry 2 (commit+push) — DONE, commits `0d60e08` + `a871ea9`; confirmed via `git log`.
- Prior entry 3 (gitignore review) — DONE, Kim ruled keep-all 2026-08-24 (commit `a871ea9`).
- Prior entry 4 (issue-sorter narrated-but-absent gap) — DONE: `#924` fix landed (PR #926, commit
  `7cad197`, widens `chore_sweep_apply.mjs`'s detection to catch report-target phrasing without a
  write-verb) and this firing's issue-sorter report complies directly — no recurrence, entry
  retired (not carried forward as a 3rd-consecutive escalation).
- `#929` (adr_checkpoint.py: hash the amendment ratification marker) — merged via PR #931 (commit
  `0dcd3e3`); this is the one commit `main` is currently behind `origin/main` by (entry 3).
- 8 new issues + 8 PRs processed this window by issue-sorter, all correctly self-filed, 0 new ops
  action.
- #914, #913, #490 — all closed since the prior plan; dropped from "Not queued" tracking.

Dispatch: 2026-08-25T17:19:54Z
