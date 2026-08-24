# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-24T03:51:50Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing** (dispatch-named
UNMEASURED list: `[]`). Per this dispatch's own instruction, evidence is exactly the three
attached reports — **no supplementary live `gh` cross-check performed** this firing (a deliberate
difference from the 2026-08-22T23:49:26Z firing's plan, which layered one on top); carry-forward
status of the *prior plan's own* queue entries was confirmed via local `git log`/`git status`/file
reads only (durable state, not a refetch of gh issue/PR evidence).

decision-watcher: 25/25 ADRs scanned; one delta — adr-0023's stored checkpoint hash was stale
relative to the file's actual current content (the correction note appended 2026-08-22 landed via
a direct commit, `b176b1d`, outside decision-watcher's own harvest flow, so its checkpoint never
advanced at the time). This firing recomputes and syncs it; the amendment itself is a stale-header
correction only, judged against save-lessons' Phase 1/2 bar as already fully covered by
`teamwork/skills/fleet-rules/references/substrate-choice.md` — reject as duplicate, no ADR-queue
candidate. One payload (`adr-checkpoint.json`). issue-sorter: window since 2026-08-22T23:49:48Z, 21
new issues + 17 PRs from a dense self-driven build campaign, every one already correctly filed by
`kimgranlund` (trusted author) with correct kind label and full record shape — 0 mints, 0 repairs,
0 held, none ruling-shaped; one payload (`watch-checkpoint.json`, checkpoint → 03:52:28Z).
repo-cleaner: `git fetch --prune` (17 stale refs pruned, all behind merged PRs); primary clean, up
to date, zero open PRs; classification set changed from prior firing (gitignore WARNs 3→4,
open-issue set turned over) so a full report is owed, not abbreviated; one payload (its own
report).

**Narrated-but-absent audit (ops-write-sandbox-rules):**
- **decision-watcher:** clean — its `adr-checkpoint.json` fenced block is present and matches its
  own claim; explicitly states `adr-queue.json` is unchanged and carries no block (correct — not a
  violation).
- **issue-sorter:** **NOT clean, and recurring.** Its report names a per-firing report target path
  in prose — "Report target (standalone firing, sole seat in scope):
  `.claude/ops/reports/2026-08-24T03:52:28Z.md`" — but never emits a matching fenced block; only
  `watch-checkpoint.json`'s block is present. This is the *same* narrated-but-absent shape the
  prior plan (2026-08-22T23:49:26Z firing) already named for issue-sorter's prior-firing report
  path — it recurred rather than closing. Per that rule, named explicitly rather than silently
  absorbed; entry 1 below applies only the block actually emitted. Given it recurred despite being
  named last time, this is escalated from feedback-only to a queued hygiene item this firing
  (entry 4).
- **repo-cleaner:** clean — its per-firing report is present as a fenced, target-pathed block
  matching its own stated path exactly (`.claude/ops/reports/2026-08-24T03-52-33Z-repo-cleaner.md`);
  "executed: nothing" matches its own stated actions (fetch --prune only).

**Prior plan (2026-08-22T23:49:26Z firing) reconciliation:** all four entries — **DONE, persisted**.
Entry 1 (apply payloads) + entry 2 (commit+push) — commit `c9f74bd` ("ops: persist
2026-08-22T23:49:26Z sweep state..."), `main` clean and up to date with `origin/main`. Entry 3
(adr-0023 stale-blockquote repair) — DONE: commit `b176b1d` appended the dated correction note over
the retained PROPOSED-era blockquote (`.claude/docs/adr/0023-fleet-canon-vs-native-agent-teams.md`,
verified by direct read this firing — the correction is live). Entry 4 (clear stale #866
held-item line) — DONE: same commit `b176b1d`; `held-items.md` now reads `Status: resolved
2026-08-22 — Kim confirmed... built and merged as PR #871`. Nothing carries forward from the prior
queue — this firing's queue is built fresh from this firing's own three reports.

**Parked-issue check (#611):** #617 stays **dropped: parked #617** — carried forward from the
prior firing's own confirmed `backlog`-labeled read (2026-08-22); it was never a numbered queue
entry, only named informationally, so there is no entry to re-drop. No focus instruction in this
dispatch names #617, so it is not un-parked. No other id in this firing's evidence (the two new
issues #914/#913, or #609/#490) is reported carrying `backlog`/`roadmap`.

**Blocked-by (#193):** no `Blocked-by:` line surfaced in any of this firing's three attached
reports (none quote issue-body text containing one) — nothing reordered by the convention this
firing.

**needs-ruling lane:** empty — issue-sorter's report explicitly states no item this firing read as
ruling-shaped, and no seat names a `needs-ruling`-labeled issue.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary names session `plugins-28`
(pid 36713, startedAt `2026-08-24T03:51:44.364Z` — 6 seconds ahead of this firing's own key,
same-session match) — this sweep's own dispatching session's coordination lock. Never quarantine
it via `sync_main.py`, never stage it in entry 2; it clears itself when the sweep exits. Apply all
fenced payloads at the shared checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: `.claude/ops/adr-checkpoint.json`
  (decision-watcher — adr-0023 hash resynced to its current post-amendment content, all other 24
  hashes unchanged), `.claude/ops/watch-checkpoint.json` (issue-sorter — github source advanced to
  2026-08-24T03:52:28Z), plus `.claude/ops/reports/2026-08-24T03-52-33Z-repo-cleaner.md`
  (repo-cleaner's own report), plus this rewritten `.claude/ops/plan.md`. No `adr-queue.json`
  block (unchanged, still `candidates: []`), no `held-items.md`/`friendlies.json` blocks
  (issue-sorter: explicitly unchanged), no issue-sorter per-firing report block (narrated but
  never emitted — see audit above; nothing to apply, tracked instead as entry 4).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** three fenced seat blocks + this plan, all present; narrated-but-absent audit above
  names the one gap and excludes it rather than fabricating content for it.
- **Size:** ~1 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from the primary — the next scheduled firing starts blind until it lands (recurring)
- **Action:** from `/Users/kimba/Projects/nonoun/plugins` on `main`: stage exactly the three
  ops-state paths entry 1 applied — never `git add -A`. **Exclude `sweep-in-flight.json`** (the
  live lock, per the lock-file note). Read the status output, commit as a separate step, push.
- **Owner:** Kim.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing starts
  blind); repo-cleaner — primary clean, up to date, prior firing's persist already landed
  (`c9f74bd`, `b176b1d`).
- **Size:** ~2 min.

**Class 3 — human decisions:** none pending this firing. `held-items.md`'s ruling queue carries no
open entry (the one prior entry, #866, is fully resolved and cleared). The ADR-queue confirm round
is empty (`candidates: []`). No `needs-ruling`-labeled issue in evidence.

**Class 4 — hygiene debt:**

### 3. Review the 4 stale-matching `.gitignore` rules — RESOLVED 2026-08-24: Kim ruled keep all (dist/ and __pycache__/ guard future build output; zero cost to keep). No edit made.
- **Action:** `gitignore_check.py` now reports 4 WARN (up from 3): `dist/`, `harness-audit-*/`,
  `.name-map.md`, and newly `__pycache__/` (added via commit `696f120`, now matches nothing
  tracked — no `__pycache__` dirs exist anywhere in the tree). All are G1
  stale-rule-matches-nothing shapes, no FAIL. Review each and decide keep-vs-prune; per
  `.claude/rules/gitignore-repair.md` no ops-family seat hand-edits `.gitignore` itself.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's 2026-08-24T03:52:33Z report (`.claude/ops/reports/
  2026-08-24T03-52-33Z-repo-cleaner.md`), `gitignore_check.py` output cited there.
- **Size:** ~5 min.

### 4. Fix issue-sorter's recurring narrated-but-absent per-firing report gap (NEW — 2nd consecutive firing)
- **Action:** issue-sorter has now named a per-firing report target path in prose without emitting
  the matching fenced block on two consecutive firings (2026-08-22T23:49:26Z and this firing,
  2026-08-24T03:51:50Z) — see the narrated-but-absent audit above. Naming it as procedural feedback
  alone didn't close it last time; this firing escalates it to a queued item. Whoever next revises
  issue-sorter's own procedure skill should either make it actually emit the block it claims, or
  drop the claim when the bare-report-path convention doesn't apply this run.
- **Owner:** Kim (or whoever next touches issue-sorter's procedure skill).
- **Evidence:** this firing's audit above; prior plan's 2026-08-22T23:49:26Z firing's own
  identical finding (`.claude/ops/reports/` — no `2026-08-22T23-49-48Z.md` or
  `2026-08-24T03:52:28Z.md` exists at either claimed path).
- **Size:** ~10 min.

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`** — this sweep's own lock (startedAt ~6s before the firing key, session
  `plugins-28`); flagged in the lock-file note and entry 2's exclusion; never queued as cleanup.
- **dropped: parked #617** — carried forward from the prior firing's confirmed `backlog` label;
  never a numbered queue entry; not un-parked (no focus instruction named it this dispatch).
- **#914, #913 (NEW)** — `task`, `size:small`, zero assignees, no comments — buildable/tracked
  backlog, outside this queue (same treatment as #878/#609/#490 in the prior firing's plan).
- **#609, #490** — open bugs, zero assignees, unchanged this firing — buildable/tracked backlog,
  outside this queue.
- **No open PRs this firing** (`gh pr list --state open` returned empty per repo-cleaner) —
  nothing in-flight to note, unlike the prior firing's PR #879 (now merged).
- **17 pruned remote refs** (behind merged PRs through #916) — remote branches already gone,
  locals never existed at the primary; no reap items created.
- **Stale-claim check** — clean: all 5 open issues (#914, #913, #617, #609, #490) carry zero
  assignees.
- **adr-0023 amendment content** — duplicate of already-harvested material
  (`teamwork/skills/fleet-rules/references/substrate-choice.md`, ADR-0023 harvest); no ADR-queue
  candidate.

## Resolved since the prior plan (2026-08-22T23:49:26Z firing)

- Prior entries 1+2 (apply + persist) — DONE, commit `c9f74bd`; `main` clean, up to date with
  `origin/main`.
- Prior entry 3 (adr-0023 stale-blockquote repair) — DONE, commit `b176b1d`; correction note
  confirmed live by direct file read this firing.
- Prior entry 4 (clear stale #866 held-item line) — DONE, same commit `b176b1d`; `held-items.md`
  now reads `Status: resolved 2026-08-22`.
- 21 new issues + 17 PRs processed this window by issue-sorter, all correctly self-filed, 0 new
  ops action.

Dispatch: 2026-08-24T03:51:50Z
