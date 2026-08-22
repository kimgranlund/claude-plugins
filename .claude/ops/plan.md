# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-22T13:54:43Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing**
(dispatch-named UNMEASURED list: empty). One sub-measurement the seats' own content leaves
ambiguous: the liveness of the `plugins-marshal` session named in `sweep-in-flight.json`
(pid 14733 — `ps` found no matching process, but startedAt 2026-08-22T13:54:43.226Z is this
firing key itself; repo-cleaner correctly treated it as live-until-proven-dead — it is almost
certainly this sweep's own coordination lock).

decision-watcher: 25 ADRs scanned, 2 NEW (adr-0024, adr-0025), adr-0011 newly superseded on
two scoped edges (§6.1 closed set ← 0024; §8 agent frontmatter ← 0025); 3 candidates queued
(`adr-0024:harvest`, `adr-0025:harvest`, `adr-0011:stale-citation` — the latter naming
authorkit's `LAYOUT.md` + `FRONTMATTER.md` as stale against the superseded scopes, found via
content grep and flagged as outside the literal id-grep's letter); two payloads
(`adr-checkpoint.json`, `adr-queue.json`); the batched confirm round explicitly deferred (no
human in the dispatch loop). issue-sorter: window 2026-08-21T21:39:00Z→2026-08-22T13:55:27Z,
1 new issue (#866, trusted author, pre-filed correctly, feature-shaped — 0 mints, 0 repairs)
with a content-level provenance question queued to `held-items.md`'s Kim queue; three payloads
(`watch-checkpoint.json`, `held-items.md`, its per-firing report). repo-cleaner: executed
nothing beyond the standing `git fetch --prune` (pruned 3 stale refs behind merged
#867/#868/#869); primary `main` CLEAN and up to date — the prior firing's marshal-session dirt
all landed between firings; `sync_main.py` withheld with reasoning (nothing to pull; only the
ambiguous lock file remains); zero open PRs, no `campaign_close.py` target; reap sets
unchanged; one payload (its report).

**Prior plan (2026-08-21T21:37:39Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(issue-sorter's window opens exactly at the applied 21:39:00Z checkpoint; repo-cleaner cites
the applied `2026-08-21T21-39-51Z-repo-cleaner.md` as its prior-firing baseline). Entry 2
(commit+push ops state) — DONE BY EVENTS: repo-cleaner finds primary `main` clean, no
ahead/behind, prior dirt gone — persisted between firings; the obligation recurs for this
firing's payloads → entry 2. Entry 3 (four dirty worktrees) — still open, explicitly
unchanged → entry 5. Entry 4 (stashes) — still open, unchanged → entry 6. Entry 5 (reap) —
still open, sets explicitly unchanged → entry 7. Entry 6 (adr-0023 stale PROPOSED
blockquote) — still open: decision-watcher's scan shows adr-0023's body unchanged (hash
carried, no delta reported) → entry 8.

**Parked-issue check (#611):** no carried-forward entry id carries `backlog`/`roadmap` in
this firing's evidence — nothing dropped.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline: entry 2 persists what
entry 1 applies; entries 3/4's downstream dispatches wait on their own confirm gates; entry
7's deferred worktrees wait on entry 5.

**needs-ruling lane:** empty — no `needs-ruling`-labeled issue in evidence (#866 tested
feature-shaped, not ruling-shaped; its provenance question is a held-item, entry 3).

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary names session
`plugins-marshal` (pid 14733, startedAt equal to this firing key) — this sweep's own
dispatching session's coordination lock. Never quarantine it via `sync_main.py`, never stage
it in entry 2; it clears itself when the sweep exits. Apply all fenced payloads at the shared
checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: `.claude/ops/adr-checkpoint.json` +
  `.claude/ops/adr-queue.json` (decision-watcher — checkpoint advanced to 25 ADRs, 3 pending
  candidates), `.claude/ops/watch-checkpoint.json` (issue-sorter — github source advanced to
  2026-08-22T13:55:27Z, strictly newer than the applied 21:39:00Z), `.claude/ops/held-items.md`
  (issue-sorter — one new Kim-queue entry, #866 provenance),
  `.claude/ops/reports/2026-08-22T13:55:27Z.md` (issue-sorter report),
  `.claude/ops/reports/2026-08-22T13-56-17Z-repo-cleaner.md` (repo-cleaner report), plus this
  rewritten `.claude/ops/plan.md`. `friendlies.json` / `.mcp.json` explicitly unchanged — no
  blocks owed, none applied.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** all seven fenced blocks present (six seat payloads + this plan);
  narrated-but-absent audit below reads clean for all three seats.
- **Size:** ~2 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from the primary — the next scheduled firing starts blind until it lands (recurring)
- **Action:** from `/Users/kimba/Projects/nonoun/plugins` on `main`: stage exactly the seven
  ops-state paths entry 1 applied — never `git add -A`. **Exclude `sweep-in-flight.json`**
  (the live lock, per the lock-file note). Read the status output, commit as a separate step,
  push. Cleaner than last firing: main is otherwise clean, no peer-session dirt to route
  around.
- **Owner:** Kim.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); repo-cleaner — primary clean, up to date, prior firing's persist landed.
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 3. Rule on #866's request provenance — held-item, confirm before it's treated as prioritized (NEW)
- **Action:** issue #866 (fleet-bootstrap: cross-repo coordination channels in fleet.json) is
  correctly filed and labeled, but its own body discloses the request arrived secondhand — a
  cross-session relay from gen-ui-kit's marshal citing an unconfirmed instruction from Kim —
  and asks for a confirm before prioritization. issue-sorter queued it on `held-items.md`'s
  Kim queue rather than acting. Confirm (→ normal buildable backlog, `/mobilize-chores`
  territory) or deny (→ mark the held-items entry resolved with the decision); edit the
  entry's Status line in place either way.
- **Owner:** Kim.
- **Evidence:** issue-sorter report §New item + the held-items.md payload's queued entry
  (2026-08-22T13:55:27Z).
- **Size:** ~3 min.

### 4. Run the batched ADR-queue confirm round — 3 candidates, then dispatch save-lessons per verdict (NEW)
- **Action:** `python3 .../adr_queue.py pending .claude/ops/adr-queue.json` lists all 3:
  `adr-0024:harvest` and `adr-0025:harvest` (both covered-but-sharpens — extend authorkit's
  `naming-conventions/references/LAYOUT.md` and `FRONTMATTER.md` respectively, via
  save-lessons Phase 4 through its own Phase 3 confirm gate) and `adr-0011:stale-citation`
  (same two files stale against the superseded §6.1/§8 scopes — save-lessons Phase 6,
  fix/retire proposal, same gate). decision-watcher deferred the round correctly (no human in
  the sweep loop). Note the overlap: all three candidates land in the same two files — one
  save-lessons pass can carry all three verdicts.
- **Owner:** Kim (confirm round) → save-lessons dispatch (execution).
- **Evidence:** decision-watcher report — harvest judgments + the flagged-transparent
  stale-citation finding; adr-queue.json payload (3 candidates, evidence fields inline).
- **Size:** ~5 min confirm + ~20 min dispatch.

### 5. Decide the four dirty worktrees — rescue (branch + PR) or discard, each (carried, unchanged third firing)
- **Action:** unchanged dirt across three firings: `629-self-improvement-retrospective`
  (merged #645; untracked `lld-0018-estate-maintenance-retrospective.md`);
  `fix-656-rdd-revalidation-rotation` (merged #663; `revalidation_checkpoint.py` +
  `watch-adrs/SKILL.md` modified); `fix-667` (checked out on
  `fix-683-container-grammar-role-aliases` — HEAD `83fade5` fully contained in `origin/main`
  via #697 under a different branch name, **orphaned, no PR under this branch's own name** —
  plus `css_build.py` modified); `fix-684` (merged #699; 2 modified + 3 untracked
  `overhaul-run-*.md`, reads actively-in-use — verify no live session owns it first).
  Inspect each diff; branch-and-PR what's live, discard what's dead. Gates their reaps
  (entry 7, named inline there).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §NOT safe to reap — explicitly unchanged from the prior firing.
- **Size:** ~15 min.

### 6. Resolve the 2 quarantine stashes at the primary — carried, unchanged
- **Action:** `git stash list` still shows 2 stashes, both `On main: sync_main quarantine`,
  unchanged across firings. Inspect each; selectively restore anything a live flow still
  owns, then drop. Judgment call — no gated script path exists for stash resolution; same
  sitting as entry 2 works.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Standing — unchanged.
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 7. Reap 4 clean worktrees + 12 merged local branches — one paste block; four worktrees deferred (carried, unchanged)
- **Action:** from the primary checkout, reap the verified-clean set: worktrees `build-554`
  / `634-req-infix-prefix` (#646), `fix-647` (#648), `fix-660` (#661),
  `fix-794-marketplace-drift` (#795); branches `608-dispatch-ticket-file-bug-claim-fix`
  (#610), `611-backlog-roadmap-releases-loop` (#621), `612-harvest-domain-knowledge` (#614),
  `613-harvest-project-context` (#615), `622-feedback-intake-door` (#641),
  `637-drain-queue-command` (#643), `650-artifact-styling-rules` (#651),
  `657-scope-audience-frontmatter` (#664), `670-unnamed-checker-dispatch` (#689),
  `fix-667-build-feature-gh541-doctrine` (#668), `fix-850-fleet-bootstrap-phase5-wall`
  (#851), `post-series-cleanups` (#823). Verify with `git worktree list` / `git branch -vv`.
  **Deferred, named inline:** worktrees `629-self-improvement-retrospective`, `fix-656`,
  `fix-667`, `fix-684` — blocked by entry 5 (open). Zero open PRs this firing — no
  healthy-in-flight exceptions. Stays propose-only from the seat (no host reap script
  exists).
- **Owner:** Kim (same sitting as entries 2/6).
- **Evidence:** repo-cleaner §Propose-only — every item independently verified merged with
  its PR id, remote gone, worktree clean; sets explicitly unchanged from the prior firing.
- **Size:** ~5 min (+ a later pass as entry 5 clears).

### 8. Repair adr-0023's stale PROPOSED blockquote — dated amendment, append-shaped (carried)
- **Action:** carried forward a fourth time: adr-0023 still reads `status: accepted` over a
  stale `> PROPOSED 2026-08-18 ...` blockquote — decision-watcher's checkpoint carries
  adr-0023's hash unchanged this firing (no delta reported). Repair per docs-mutability:
  append a dated correction note superseding the blockquote — never silently rewrite an
  accepted ADR.
- **Owner:** Kim (small doc fix; solo single-file, may commit to main per the campaign row).
- **Evidence:** prior plan entry 6 + decision-watcher checkpoint (adr-0023 hash carried, no
  delta).
- **Size:** ~3 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — both narrated state paths (`adr-checkpoint.json`,
  `adr-queue.json`) have matching fenced, target-pathed blocks; the confirm round named as
  deferred, not narrated as run.
- **issue-sorter:** clean — all three narrated paths (`watch-checkpoint.json`,
  `held-items.md`, the per-firing report `2026-08-22T13:55:27Z.md`) have matching fenced
  blocks; `held-items.md`'s citation of the report path is backed by that report's own fenced
  block in the same firing (the later-payload-cites-earlier rule satisfied);
  `friendlies.json` / `.mcp.json` declared unchanged and omitted, no conditional naming.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block; nothing
  executed beyond the standing `git fetch --prune`; all reaps explicitly propose-only,
  `sync_main.py` explicitly withheld with its reasoning stated.

## Not queued (checked, found clean or deliberately left)

- **`sweep-in-flight.json`** — this sweep's own lock (startedAt equals the firing key);
  flagged in the lock-file note and entry 2's exclusion; never queued as cleanup.
- **#866 (pending entry 3's ruling) + #849, #617, #609, #490 (open, zero assignees)** —
  buildable/tracked backlog → teamwork's `/mobilize-chores`, outside this queue. (#490 is
  the upstream platform-bug tracker.)
- **3 pruned remote refs** (behind merged #867/#868/#869) — remote branches already gone,
  locals never existed at the primary; no reap items created.
- **5 merged PRs + 5 already-tracked issues in issue-sorter's window** — discovery/context
  only; no ticket-record action owed.
- **`gitignore_check.py` WARNs** — primary 3-WARN, all 8 worktrees uniform 4-WARN, all
  stale-rule/partial-checkout shapes, no FAIL anywhere; unchanged.
- **Stale-claim check** — clean: all 6 open issues carry zero assignees.
- **adr-0011's D8/D9 citations** (GRAMMAR.md, PLAN-TEMPLATE.md, estate-rename-map.md) —
  checked by decision-watcher, scopes unamended by either superseding ADR, not stale.

## Resolved since the prior plan (2026-08-21T21:37:39Z firing)

- Prior entry 1 (apply the 21:37:39Z payloads) — DONE (checkpoint continuity + the applied
  repo-cleaner report cited as this firing's prior baseline).
- Prior entry 2 (commit+push, with marshal-dirt exclusions) — DONE BY EVENTS: primary `main`
  now clean and up to date with `origin/main`; the marshal session's in-flight dirt
  (fleet-roster, brief, three `teamwork/` files) all landed between firings.
- PRs #867/#868/#869 merged with remote branches gone — no close targets remained.

Dispatch: 2026-08-22T13:54:43Z
