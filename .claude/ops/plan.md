# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-21T17:18:52Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing**
(dispatch-named UNMEASURED list: empty). One sub-measurement the seats' own content leaves
unmeasured again: the primary's ahead/behind count vs `origin/main` (repo-cleaner ran
`git fetch --prune` and `primary_checkout_check.py` → PASS, `main`, but reported no
behind-count).

decision-watcher: clean no-op — 23 ADRs scanned, all previously known, zero delta;
`adr-queue.json` already `{"candidates": []}`; per its no-op clause no payloads owed or
emitted. issue-sorter: window 2026-08-20T05:27:26Z→2026-08-21T17:19:43Z, 26 issues + 31 PRs
touched (#791–#850: brand-design overhaul waves, frontend knowledge-pack waves,
screens→frontend rename), all trusted-author; 0 label repairs needed, 0 mints, 0 held, 0
needs-ruling; 22/26 issues already closed, open remainder #850/#842/#849/#840; two payloads
(`watch-checkpoint.json`, its per-firing report). repo-cleaner: executed nothing (only the
standing `git fetch --prune`, pruning 9 already-deleted refs); **zero open PRs and zero
non-main remote branches** — no `campaign_close.py` target; classification set changed
materially — reap-safe set grew to 5 worktrees (`council-role-agents-840` new,
`fix-794-marketplace-drift` moved from open-PR to merged #795); one payload (its report).

**Prior plan (2026-08-20T05:30:00Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(issue-sorter's window opens at the applied 05:27:26Z checkpoint, and repo-cleaner finds both
prior payload reports present on disk at the primary). Entry 2 (commit+push ops state) —
**STILL OPEN, debt grown**: THREE prior firings' reports now sit untracked on `main`
(`2026-08-19T21-42-54Z-repo-cleaner.md`, `2026-08-20T05-27-26Z.md`,
`2026-08-20T05-30-31Z-repo-cleaner.md`) — the persist half has never happened → entry 2.
Entry 3 (three dirty worktrees) — still open, unchanged → entry 3. Entry 4 (fix-684 hold) —
**RESHAPED, block cleared as measured**: the prior blocking lock
(`fix-684-brand-design-session`) is gone; `sweep-in-flight.json` now names THIS sweep's own
session (`sweep-chores-2026-08-21`, pid 98732, startedAt 17:18:41.882Z), and the fix-684 dirt
set is unchanged — the peer session evidently exited without resolving it → entry 4, no
longer session-blocked. Entry 5 (stashes) — still open, unchanged → entry 5. Entry 6 (reap)
— RESHAPED: set grew to 5 clean worktrees + the same 10 branches; the two open-PR exceptions
(#795, #791) both merged since, zero open PRs remain → entry 6. Entry 7 (adr-0023 stale
PROPOSED blockquote) — still open: decision-watcher's zero-delta scan proves the ADR body
unchanged, still unrepaired → entry 7.

**Parked-issue check (#611):** no carried-forward entry id carries `backlog`/`roadmap` in
this firing's evidence — nothing dropped. #849's "parked by ruling" title was checked by
issue-sorter against the ruling-shaped test and left a plain buildable task; it was never a
plan entry and mints no lane here.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline on their own entries: the
dirty-worktree reaps wait on entries 3/4's decisions; entry 2 persists what entry 1 applies.

**needs-ruling lane:** empty — issue-sorter reports 0 ruling-shaped candidates (#849 and
#840 both checked and correctly left plain); no §3 reference owed.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary now names THIS sweep's
own session (`sweep-chores-2026-08-21`, startedAt 11s before this firing key). It is the
dispatching session's own coordination lock — never quarantine it via `sync_main.py`, never
stage it in entry 2; it clears itself when this sweep exits. Apply all fenced payloads at the
shared checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: `.claude/ops/watch-checkpoint.json`
  (issue-sorter — github source advanced to 2026-08-21T17:19:43Z, strictly newer than the
  applied 05:27:26Z), `.claude/ops/reports/2026-08-21T17:19:43Z.md` (issue-sorter report),
  `.claude/ops/reports/2026-08-21T17-21-08Z-repo-cleaner.md`, plus this rewritten
  `.claude/ops/plan.md`. decision-watcher owes no blocks this firing (clean no-op, declared).
  `friendlies.json` / `held-items.md` explicitly unchanged — no blocks owed, none applied.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** all four fenced blocks present (three seat payloads + this plan);
  narrated-but-absent audit below reads clean for all three seats.
- **Size:** ~2 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from the primary — three firings deep, the next scheduled firing starts blind until it lands
- **Action:** from `/Users/kimba/Projects/nonoun/plugins` on `main`: stage exactly the
  ops-state paths entry 1 applied PLUS the three still-untracked prior reports
  (`2026-08-19T21-42-54Z-repo-cleaner.md`, `2026-08-20T05-27-26Z.md`,
  `2026-08-20T05-30-31Z-repo-cleaner.md`) — never `git add -A`. **Exclude
  `sweep-in-flight.json`** (this sweep's own live lock) and judge the modified
  `brand-design/` files separately — they are source dirt, not ops state, and belong to
  their own flow. Read the status output, commit as a separate step, push. Behind-count
  unmeasured this firing — if the push is refused, `sync_main.py` first per the workspace
  campaign row (after this sweep's lock clears).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Primary main's own dirt — three prior firings' applied reports
  untracked on `main`; ops-write-sandbox-rules (state persists through the repo or the next
  firing starts blind). Carried from the prior plan's entry 2, debt grown.
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 3. Decide the three dirty worktrees — rescue (branch + PR) or discard, each (carried, unchanged)
- **Action:** unchanged from the prior firing: `629-self-improvement-retrospective` (merged
  #645; untracked `lld-0018-estate-maintenance-retrospective.md`);
  `fix-656-rdd-revalidation-rotation` (merged #663; `revalidation_checkpoint.py` +
  `watch-adrs/SKILL.md` modified); `fix-667` (checked out on
  `fix-683-container-grammar-role-aliases` — **no PR at all, orphaned work** — plus
  `css_build.py` modified). Inspect each diff; branch-and-PR what's live, discard what's
  dead. The fix-683 orphan remains the sharpest: real semantic edits with no record path.
  Gates their reaps (entry 6, named inline there).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §NOT safe to reap — explicitly unchanged from the prior firing.
- **Size:** ~10 min.

### 4. fix-684 worktree — session block cleared; decide the dirt
- **Action:** the prior firing held this behind a live `fix-684-brand-design-session` lock;
  that lock is gone (replaced by this sweep's own) and the dirt is unchanged: merged #699,
  2 modified (`script-interface.md`, `css_build.py`) + 3 untracked `overhaul-run-*.md`
  files. repo-cleaner still reads it as "looks actively in use" — verify no live session
  owns it (check for a newer lock/process first), then rescue-or-discard, then reap
  (entry 6, named inline).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §NOT safe to reap + the lock file's own new content
  (`sweep-chores-2026-08-21` — the fix-684 session no longer holds it).
- **Size:** ~5 min.

### 5. Resolve the 2 quarantine stashes at the primary — carried, unchanged
- **Action:** `git stash list` still shows 2 stashes, both `On main: sync_main quarantine`,
  unchanged across firings. Inspect each; selectively restore anything a live flow still
  owns, then drop. Judgment call — no gated script path exists for stash resolution; same
  sitting as entry 2 works.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Standing — unchanged.
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 6. Reap 5 clean worktrees + 10 merged local branches — one paste block; three worktrees deferred
- **Action:** from the primary checkout, reap the verified-clean set: worktrees `build-554`
  / `634-req-infix-prefix` (#646), `fix-647` (#648), `fix-660` (#661),
  `council-role-agents-840` / `worktree-council-role-agents-840` (#843, new this firing),
  `fix-794-marketplace-drift` (#795, now merged); branches
  `608-dispatch-ticket-file-bug-claim-fix` (#610), `611-backlog-roadmap-releases-loop`
  (#621), `612-harvest-domain-knowledge` (#614), `613-harvest-project-context` (#615),
  `622-feedback-intake-door` (#641), `637-drain-queue-command` (#643),
  `650-artifact-styling-rules` (#651), `657-scope-audience-frontmatter` (#664),
  `670-unnamed-checker-dispatch` (#689), `fix-667-build-feature-gh541-doctrine` (#668).
  Verify with `git worktree list` / `git branch -vv`. **Deferred, named inline:** worktrees
  `629-self-improvement-retrospective`, `fix-656`, `fix-667` — blocked by entry 3 (open);
  `fix-684` — blocked by entry 4 (open). Zero open PRs this firing — no healthy-in-flight
  exceptions remain. Stays propose-only from the seat (no host reap script exists).
- **Owner:** Kim (same sitting as entries 2/5).
- **Evidence:** repo-cleaner §Propose-only — every item independently verified merged with
  its PR id, remote gone, worktree clean.
- **Size:** ~5 min (+ later passes as entries 3/4 clear).

### 7. Repair adr-0023's stale PROPOSED blockquote — dated amendment, append-shaped (carried)
- **Action:** carried forward, re-evidenced a second time: decision-watcher's zero-delta
  scan proves every ADR body unchanged, so adr-0023 still reads `status: accepted` over a
  stale `> PROPOSED 2026-08-18 ...` blockquote. Repair per docs-mutability: append a dated
  correction note superseding the blockquote — never silently rewrite an accepted ADR.
- **Owner:** Kim (small doc fix; solo single-file, may commit to main per the campaign row).
- **Evidence:** prior plan entry 7 + decision-watcher (zero delta, all 23 previously known).
- **Size:** ~3 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — no-op clause explicitly invoked; no state paths narrated as
  written, no report path named, no blocks owed.
- **issue-sorter:** clean — both narrated paths (`watch-checkpoint.json`, the per-firing
  report `2026-08-21T17:19:43Z.md`) have matching fenced, target-pathed blocks;
  `friendlies.json` / `held-items.md` declared unchanged and omitted, no conditional naming.
  One data quirk, not a violation: its prose calls this "a standalone firing" — it ran
  inside this sweep; the payloads stand regardless.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block; nothing
  executed beyond the standing `git fetch --prune`; all reaps explicitly propose-only,
  `sync_main.py` explicitly withheld.

## Not queued (checked, found clean or deliberately left)

- **`sweep-in-flight.json` at the primary** — this sweep's own session lock, flagged in the
  lock-file note; deliberately never queued as cleanup.
- **Modified `brand-design/` files + `.claude/ops/plan.md` dirt at the primary** — the plan
  dirt is entry 1/2's own subject; the brand-design dirt is source-flow work, not ops debt —
  named in entry 2's exclusion, not separately queued.
- **#850, #842 (bug+major), #849, #840 (feature)** — open, correctly labeled, zero
  assignees; buildable backlog → teamwork's `/mobilize-chores`, outside this queue.
- **`gitignore_check.py` WARNs** — primary 3-WARN (new: `.name-map.md`, which repo-cleaner
  reads as an intentionally-forward-provisioned rule for a never-committed transient
  artifact, S6 #829); worktrees 4–5-WARN, expected partial-checkout shape; no FAIL anywhere.
- **9 pruned remote refs** — all behind merged-and-closed PRs; nothing left behind them.
- **31 PRs in issue-sorter's window** — discovery/context only; 22 of 26 touched issues
  already closed via their merges.
- **Stale session gitStatus** — the dispatch context's snapshot (branch `fix-423-...`)
  contradicts repo-cleaner's live check (primary on `main`); noise, not state — flagged,
  not acted on (same class as the prior plans' flag).

## Resolved since the prior plan (2026-08-20T05:30:00Z firing)

- Prior entry 1 (apply the 05:30Z payloads) — DONE (checkpoint continuity + both prior
  payload reports found on disk at the primary).
- Prior entry 4's live-session block — CLEARED BY EVENTS: the `fix-684-brand-design-session`
  lock is gone; the dirt decision itself carries forward as this plan's entry 4.
- Prior entry 6's open-PR exceptions — RESOLVED: #795 and #791 both merged; zero open PRs
  remain, and `fix-794-marketplace-drift` moved into the reap-safe set.

Dispatch: 2026-08-21T17:18:52Z
