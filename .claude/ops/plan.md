# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-22T23:49:26Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing** (dispatch-named
UNMEASURED list: empty). `gh` reachable and cross-checked live (issue/PR state, labels, PR #879
checks) — standalone-grade confirmation layered on top of the attached reports, not a refetch of
their judgments. Sub-measurement: `.claude/ops/sweep-in-flight.json` (pid 42266, `session:
plugins-marshal`, `startedAt: 2026-08-22T23:49:26.776Z` — this firing key itself) is this sweep's
own coordination lock, live-until-proven-dead; never touched, never staged.

decision-watcher: clean no-op — 25/25 ADRs hash-match the checkpoint, nothing new/amended/
newly-superseded; checkpoint correctly NOT advanced (nothing to advance over); per the no-op
clause, no fenced payload and no report path are owed this firing. issue-sorter: window
2026-08-22T13:55:27Z→2026-08-22T23:49:48Z, 1 new issue (#878, trusted author, already filed
correctly, task-shaped not ruling-shaped — 0 mints, 0 repairs); 4 already-tracked issues touched
by close activity (#873/#866/#849 closed via merged PRs, #490 updated); one payload
(`watch-checkpoint.json`, checkpoint → 23:49:48Z). repo-cleaner: `git fetch --prune` only (5 stale
refs pruned, all behind merged PRs); primary `main` clean and up to date; all worktree/stash/reap
debt from every prior firing is now gone; one payload (its own report).

**Narrated-but-absent audit (ops-write-sandbox-rules):**
- **decision-watcher:** clean — no-op firing invoked its own documented no-op clause; nothing
  narrated as written that isn't backed (nothing was owed).
- **issue-sorter:** **NOT clean.** Its own report names its per-firing report's target path in
  prose — "default bare path per the standing convention: `.claude/ops/reports/
  2026-08-22T23-49-48Z.md`" — but never emits a matching fenced, target-pathed block for it; only
  `watch-checkpoint.json`'s block is present. This is the textbook narrated-but-absent shape
  (path claimed, no fence behind it) — named explicitly per the rule rather than silently
  absorbed. **No content exists to apply for that path this firing** — entry 1 below applies only
  the block that was actually emitted. Not queued as a human action (nothing for Kim to do); the
  gap is procedural feedback for issue-sorter's next firing to close.
- **repo-cleaner:** clean — its per-firing report is present as a fenced, target-pathed block
  matching its own stated path exactly (`.claude/ops/reports/2026-08-22T23-51-13Z-repo-cleaner.md`);
  "executed: nothing" matches its own actions (fetch --prune only).

**Prior plan (2026-08-22T13:54:43Z firing) reconciliation:** entry 1 (apply payloads) + entry 2
(commit+push) — DONE, persisted (`git log`: `812b69f ops: persist 2026-08-22T13:54:43Z sweep
state...`; `main` clean, up to date with `origin/main`, zero ops/-path diff against HEAD). Entry 3
(rule on #866 provenance) — **DONE BY EVENTS**: #866 closed via merged PR #871
(`f499ed4`); the persist commit's own message records "#866 provenance hold — resolved live same
session." Its `held-items.md` ledger line was never edited to match (`Status: queued`, stale) →
carried forward as a hygiene item, entry 4. Entry 4 (ADR-queue confirm round, 3 candidates) —
**DONE**: `adr-queue.json` now reads `candidates: []`, its own `_comment` confirming the harvest
landed in authorkit 0.26.4 via merged PR #876 (`c3fa327`). Entry 5 (four dirty worktrees) —
**DONE**: `git worktree list` shows only the primary checkout; all four (629-…, fix-656-…, fix-667/
fix-683-…, fix-684) are gone. Entry 6 (2 quarantine stashes) — **DONE**: `git stash list` empty.
Entry 7 (reap 4 clean worktrees + 12 branches) — **DONE / moot**: `git branch -vv` now lists only
`main` and `fleet-bootstrap-address-roster` (PR #879's own branch) — nothing left to reap,
including the four entry-5 holdouts. Entry 8 (adr-0023 stale PROPOSED blockquote) — **still open**,
confirmed unchanged by direct read (`status: accepted` over the unamended `> PROPOSED 2026-08-18…`
blockquote, `.claude/docs/adr/0023-fleet-canon-vs-native-agent-teams.md:4,21-24`) and by
decision-watcher's hash-match this firing → carried forward a **fifth** time, entry 3.

**Parked-issue check (#611):** issue #617 ("FIXTURE #611 — de-staling probe (do not build)") now
carries the `backlog` label (confirmed live: `gh issue view 617`) — **dropped: parked #617**. It
was never a numbered queue entry (only named in the prior plan's informational Not-queued list),
but per #611's own rule it is excluded from this firing's live-`gh` evidence and from the
Not-queued bucket below rather than silently vanishing. No dispatch focus instruction named #617
this firing, so it stays parked. No other id in evidence carries `backlog`/`roadmap`.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing (#878's body
checked directly — none) — nothing reordered by the convention.

**needs-ruling lane:** empty — no `needs-ruling`-labeled issue in evidence this firing (checked
live across all 4 open issues: #878, #609, #490, and the now-parked #617 — none carry it).

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary names session
`plugins-marshal` (pid 42266, startedAt equal to this firing key) — this sweep's own dispatching
session's coordination lock. Never quarantine it via `sync_main.py`, never stage it in entry 2; it
clears itself when the sweep exits. Apply all fenced payloads at the shared checkout
`/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: `.claude/ops/watch-checkpoint.json`
  (issue-sorter — github source advanced to 2026-08-22T23:49:48Z, strictly newer than the applied
  13:55:27Z), `.claude/ops/reports/2026-08-22T23-51-13Z-repo-cleaner.md` (repo-cleaner report),
  plus this rewritten `.claude/ops/plan.md`. No decision-watcher blocks (clean no-op, nothing
  owed), no `held-items.md`/`friendlies.json`/`.mcp.json` blocks (issue-sorter: explicitly
  unchanged), no issue-sorter per-firing report block (narrated but never emitted — see audit
  above; nothing to apply).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** two fenced seat blocks + this plan, all present; narrated-but-absent audit above
  names the one gap and excludes it rather than fabricating content for it.
- **Size:** ~1 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from the primary — the next scheduled firing starts blind until it lands (recurring)
- **Action:** from `/Users/kimba/Projects/nonoun/plugins` on `main`: stage exactly the three
  ops-state paths entry 1 applied — never `git add -A`. **Exclude `sweep-in-flight.json`** (the
  live lock, per the lock-file note). Read the status output, commit as a separate step, push.
- **Owner:** Kim.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing starts
  blind); repo-cleaner — primary clean, up to date, prior firing's persist landed
  (`812b69f`).
- **Size:** ~2 min.

**Class 3 — human decisions:** none pending this firing. The one held item on `held-items.md`
(#866's provenance) was resolved live in the prior sweep's own session — only its ledger
paperwork remains, moved to Class 4 (entry 4) since no decision is left to make. The ADR-queue
confirm round is empty (`candidates: []`). No `needs-ruling`-labeled issue in evidence.

**Class 4 — hygiene debt:**

### 3. Repair adr-0023's stale PROPOSED blockquote — dated amendment, append-shaped (carried a fifth firing)
- **Action:** adr-0023 still reads `status: accepted` over a stale `> PROPOSED 2026-08-18 ...`
  blockquote (`.claude/docs/adr/0023-fleet-canon-vs-native-agent-teams.md:4,21-24`) —
  decision-watcher's checkpoint carries its hash unchanged again this firing. Repair per
  docs-mutability: append a dated correction note superseding the blockquote — never silently
  rewrite an accepted ADR.
- **Owner:** Kim (small doc fix; solo single-file, may commit to main per the campaign row).
- **Evidence:** prior plan entries 6→8→8 (three prior carries) + this firing's decision-watcher
  no-delta scan + direct file read confirming the blockquote is still live.
- **Size:** ~3 min.

### 4. Clear the stale #866 entry on `held-items.md`'s ruling queue — decision already made, only the ledger line is stale (NEW)
- **Action:** `held-items.md`'s "2026-08-22T13:55:27Z — issue #866's request provenance" entry
  still reads `Status: queued`, but #866 is closed (merged via PR #871, `f499ed4`) and the prior
  sweep's own persist commit records the call was made live ("#866 provenance hold — resolved
  live same session"). Edit the Status line in place per the ledger's own contract (`Status:
  resolved 2026-08-22 — confirmed/built via #871`) — this seat cannot write that file itself
  (compute-only; not its own target path either).
- **Owner:** Kim.
- **Evidence:** `held-items.md` current content (Status: queued, unchanged); issue-sorter report
  ("#866... now closed... that queue entry's Status: queued line is Kim's own to clear, left
  untouched"); `gh issue view 866` state=CLOSED; commit `812b69f` message.
- **Size:** ~1 min.

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`** — this sweep's own lock (startedAt equals the firing key); flagged in
  the lock-file note and entry 2's exclusion; never queued as cleanup.
- **dropped: parked #617** — now `backlog`-labeled (#611); excluded from live-`gh` evidence and
  from this list per the standing rule; not un-parked (no focus instruction named it).
- **#878 (NEW)** — task-shaped issue posing a two-option schema design fork
  (`cross_repo_coordination` sub-app-seat modeling); its own body's "Design call owed" imperative
  is a finding to queue, not an instruction this seat follows — the decision itself is feature/
  schema design work (teamwork's planner territory), not ops debt; not queued here. Routes to
  `/mobilize-chores` / teamwork's own planning surface.
- **#609, #490** — open bugs, zero assignees, unchanged this firing (platform-defect trackers,
  #490's own upstream issue already filed) → buildable/tracked backlog, outside this queue.
- **PR #879** (`fleet-bootstrap-address-roster`) — OPEN, both checks (`claude-review`, `gate`)
  SUCCESS, ~1.5 hrs old at repo-cleaner's check — healthy in-flight, no action; will close on its
  own once merged.
- **5 pruned remote refs** (behind merged PRs #870–#872, #875, #876) — remote branches already
  gone, locals never existed at the primary; no reap items created.
- **`gitignore_check.py` WARNs** — primary 3-WARN, unchanged, all stale-rule/matches-nothing
  shapes, no FAIL.
- **Stale-claim check** — clean: all open issues (#878, #609, #490; #617 excluded, parked) carry
  zero assignees.

## Resolved since the prior plan (2026-08-22T13:54:43Z firing)

- Prior entries 1+2 (apply + persist) — DONE, commit `812b69f` and clean `main` confirm it.
- Prior entry 3 (#866 ruling) — DONE BY EVENTS (resolved live, shipped via merged PR #871); paper
  trail carried forward as entry 4 above.
- Prior entry 4 (ADR-queue confirm round) — DONE (harvested into authorkit 0.26.4 via merged PR
  #876; `adr-queue.json` now `candidates: []`).
- Prior entries 5+7 (four dirty worktrees + reap set) — DONE (all worktrees and all
  branches beyond `main`/`fleet-bootstrap-address-roster` are gone).
- Prior entry 6 (2 quarantine stashes) — DONE (`git stash list` empty).
- Issues #866, #849, #873 closed via merged PRs #871, #877, #874; PRs #870–#877 all merged.

Dispatch: 2026-08-22T23:49:26Z
