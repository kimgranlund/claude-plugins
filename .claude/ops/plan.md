# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-19T19:04Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
Two sub-measurements remain unmeasured by the seats' own admission: the primary checkout's
direct dirty-tree read (repo-cleaner: sandbox wall reconfirmed live from this fix-684-isolated
session; `primary_checkout_check.py` did return **clean, on `main`** — branch identity only),
and the fix-667 worktree's **live-occupancy** (git state alone says redundant; no session
signal available to the seat).

decision-watcher: 23 ADRs (22 known + **adr-0023 new**, accepted 2026-08-18) — ADR-0023 rules
the fleet stays canon over native `agent-teams`, fact-shaped re-eval trigger, write-gate
follow-up ticket; judged a **harvest candidate** (placement: extend `teamwork:fleet-rules`,
no existing coverage beyond a vocabulary-table mention); 1 pending in adr-queue; two payload
blocks (`adr-queue.json`, `adr-checkpoint.json`); confirm gate deferred to the dispatching
session (no AskUserQuestion in seat toolset).
issue-sorter: window 2026-08-18T22:00:25Z → 2026-08-19T18:59:21Z — 62 issues + 47 PRs touched
(the Track A–E campaign + chore waves), all 47 PRs MERGED, 56 issues closed by them; all 5
currently-open issues (#751, #750, #617, #609, #490) correctly labeled; 0 mints, 0 repairs,
0 held, 0 needs-ruling, 0 unknown authors; one payload block (`watch-checkpoint.json`).
repo-cleaner: `git fetch --prune` clean — **only `origin/HEAD` + `origin/main` remain**, zero
open PRs, every branch-associated PR MERGED, no `campaign_close.py` owed; stash@{0}
(`6d5a2801`, "sync_main quarantine") finally MEASURED and still undropped; 5 standing orphaned
worktrees + 10 dangling branches + 2 newly-reappraised worktrees (fix-667 redundant pending
occupancy confirm; fix-684 — this session's own — merged but carrying 2 uncommitted files);
one payload block (its report).

**Prior plan (2026-08-18T22:03Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(checkpoint continuity: this firing's issue-sorter window opens at exactly 22:00:25Z, the
applied value; decision-watcher reads 22 previously known). Entry 2 (sync_main, 42 behind) —
DONE BY EVENTS (primary reads clean on `main`, no behind-count flagged; the "sync_main
quarantine" stash on record is sync_main's own artifact; remote refs pruned to `main` only).
Entry 3 (review/merge PR #678) — DONE BY EVENTS (zero open PRs; its remote head gone from
`ls-remote`). Entry 4 (stash) — CARRIES FORWARD, upgraded from unmeasured to measured →
entry 4 below. Entry 5 (five worktrees + deferred fix-667) — still open, unactioned; fix-667
re-scoped (no longer the live session's worktree) → entries 5/6. Entry 6 (seven branches) —
still open, GROWN to ten dangling → entry 6.

**Parked-issue check:** no prior-plan entry id carries `backlog`/`roadmap` in this firing's
evidence — nothing dropped. #617 (the `backlog`-labeled fixture) appears in issue-sorter's
open-issue count as kind-labeled but was never a plan entry; stays excluded per the #611
parking rule.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline on their own entries:
entry 2 (persist) waits on entry 1 (apply); entry 4's drop waits on its own verify step;
entry 5's two reaps wait on the confirmations entry 5 itself names; the ADR-0023 harvest
execution waits on entry 3's confirm.

**needs-ruling lane:** empty — issue-sorter reports 0 needs-ruling, 0 held; no §3 reference
owed.

**Sandbox hazard, named:** this sweep runs inside `.claude/worktrees/fix-684`, whose branch
(PR #699) is already MERGED — a payload written to THIS worktree's relative `.claude/ops/`
path strands on a dead branch. Apply every fenced block at the SHARED checkout:
`/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`. (The dispatch context's stale
gitStatus — branch `fix-423-...`, dirty fleet-roster/settings/attention-trend — does not
match this worktree's real branch; noise, not state.)

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout, not this worktree)
- **Action:** write the fenced payloads verbatim at
  `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`: `adr-queue.json` (decision-watcher —
  1 pending candidate, adr-0023), `adr-checkpoint.json` (23 ADRs), `watch-checkpoint.json`
  (issue-sorter — both checkpoints → 2026-08-19T18:59:21Z),
  `reports/2026-08-19T19-04-43Z-repo-cleaner.md` (repo-cleaner), plus this rewritten
  `plan.md`. `friendlies.json`, `held-items.md`, `.mcp.json` explicitly unchanged — no blocks
  owed, none applied.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** all five fenced blocks present in this firing's reports (four seat payloads +
  this plan); narrated-but-absent audit below reads clean on all three seats.
- **Size:** ~2 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops-state paths from the primary — blocks the next scheduled firing
- **Action:** from a session actually checked into `/Users/kimba/Projects/nonoun/plugins`
  (NOT worktree-isolated — the sandbox wall refuses primary-targeting git ops from here):
  stage exactly entry 1's applied paths (never `git add -A`), read the status output, commit
  as a separate step (gate ≠ commit), push. State persists through the repo or the next
  firing starts blind (ops-write-sandbox-rules). Primary is clean on `main` and no longer
  behind — no sync_main needed first this time.
- **Owner:** Kim (the only actor with a non-worktree session at the primary).
- **Evidence:** repo-cleaner — sandbox wall reconfirmed live this firing;
  `primary_checkout_check.py` clean on `main`; prior firings' pattern (entry 1+2 landed,
  proven by this firing's checkpoint continuity).
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 3. Confirm the ADR-0023 harvest candidate (batched confirm, 1 pending) — then run the harvest
- **Action:** run the batched confirm over the queue (`adr_queue.py pending
  .claude/ops/adr-queue.json` after entry 1 applies it). On confirm: `/make-pack
  teamwork/skills/fleet-rules` (extend-reference-file wave, axis: "why the fleet stays canon
  over `agent-teams`, and what would flip it"). Harvest execution is blocked by this confirm
  (named inline) — decision-watcher queues, never authors.
- **Owner:** Kim (the confirm); the confirming session runs the named command.
- **Evidence:** decision-watcher — adr-0023 new this firing, Impact detector, placement check
  found no coverage beyond `teamwork/skills/fleet-rules/references/foundations.md:31` (bare
  vocabulary-table cell); seat carries no AskUserQuestion, confirm explicitly deferred.
- **Size:** ~5 min confirm; ~30–60 min harvest if confirmed.

### 4. Verify-then-drop stash@{0} at the primary — measured at last after four silent firings
- **Action:** at the primary: confirm `stash@{0}` is still `6d5a2801bc27ebea5cb17c5a2b746c70ec470ddf`
  ("On main: sync_main quarantine"), verify `.claude/ops/adr-checkpoint.json` / `plan.md` /
  `watch-checkpoint.json` on `main` already carry that stash's diff (the prior firing judged
  the landing done but the drop was never executed), then `git stash drop stash@{0}`. Stash
  resolution is judgment, outside repo-cleaner's gated calls — propose-only from the seat.
- **Owner:** Kim (same sitting as entry 2).
- **Evidence:** repo-cleaner — identical SHA to the one the 2026-08-18T22:15Z report flagged
  as "stash-drop owed once the landing is verified"; still present this firing.
- **Size:** ~4 min.

### 5. Rule on the two held worktrees: fix-667 (occupancy) and fix-684 (2 uncommitted files)
- **Action:** two decisions, then reap: (a) **fix-667** (branch now
  `fix-683-container-grammar-role-aliases`) — HEAD `83fade5` is a confirmed `origin/main`
  ancestor with zero unique commits, and #683 was closed by a DIFFERENT PR (#702, merged
  2026-08-19T04:04:24Z); confirm no live peer session owns it (blocked by that confirmation,
  named inline — git state alone can't see occupancy), then `git worktree remove` + branch
  delete. (b) **fix-684** (THIS session's worktree, PR #699 MERGED) — carries 2 uncommitted
  modified files (`docs/skills/artifact-rules/references/script-interface.md`,
  `docs/skills/make-artifact/scripts/css_build.py`); decide commit-elsewhere vs. discard,
  and reap only after this session exits (blocked by the live session, named inline).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §New this firing — merge-base ancestry check on fix-667, PR #702
  closing #683 via a different head; PR #699 MERGED 2026-08-19T03:53:19Z with the dirty pair
  enumerated.
- **Size:** ~5 min decisions + ~2 min reaps.

**Class 4 — hygiene debt:**

### 6. Reap five orphaned worktrees and fifteen merged branches — the seat's one-paste block
- **Action:** from the shared checkout, run repo-cleaner's proposed block verbatim (worktrees
  `629-self-improvement-retrospective` PR #645, `build-554` PR #646, `fix-647` PR #648,
  `fix-656-rdd-revalidation-rotation` PR #663, `fix-660` PR #661; branches — the five paired
  ones plus danglers `608-...` #610, `611-...` #621, `612-...` #614, `613-...` #615,
  `622-...` #641, `637-...` #643, `650-...` #651, and new this firing `657-scope-audience-
  frontmatter` #664, `670-unnamed-checker-dispatch` #689, `fix-667-build-feature-gh541-doctrine`
  #668; then `git worktree prune`). Verify with `git worktree list` / `git branch -vv`. All
  merged, all remotes already deleted; stays propose-only from the seat — no host-repo reap
  script exists to gate it. The fix-667/fix-684 worktrees are NOT in this block — entry 5
  gates them.
- **Owner:** Kim (or the coordinator session, same sitting as entries 2/4).
- **Evidence:** repo-cleaner §Reap candidates — per-item PR ids all MERGED, post-prune
  `ls-remote` shows only `main`; prior plan entries 5/6 carried forward two firings running.
- **Size:** ~5 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — both narrated state files (`adr-queue.json`,
  `adr-checkpoint.json`) have matching fenced, target-pathed blocks; no per-firing report
  path narrated, none owed.
- **issue-sorter:** clean — its one changed file (`watch-checkpoint.json`) has a matching
  fenced block; `friendlies.json` / `held-items.md` explicitly declared unchanged and
  omitted, no hedged report path.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block and its
  own prose names that block as "not yet written — awaiting the dispatching session";
  `campaign_close.py` and all reaps explicitly not-invoked / propose-only.

## Not queued (checked, found clean or deliberately left)

- **ADR-0023 Decision (c)** — the fleet-native plan-approval write-gate follow-up ticket
  (owner per the ADR: the marshal). An imperative inside evidence, noted as a finding:
  buildable intake routes through docs' `/file-task`, then `/mobilize-chores` — not an
  ops-queue entry.
- **Open issues #751, #750, #609, #490** — all kind/severity/size-labeled, 0 repairs needed;
  buildable backlog → `/mobilize-chores`. #490 open by design (upstream pin-race tracking).
- **#617** — `backlog`-labeled fixture, excluded per the #611 parking rule; never a plan
  entry.
- **`gitignore_check.py` WARNs** — same standing sets both roots (primary: `dist/`,
  `harness-audit-*/`; worktree adds `.DS_Store`, `.claude/worktrees/`); no FAIL, unchanged.
- **Stale-claim check** — no host-repo claim-convention ADR exists; degraded to git-surface
  hygiene per clean-git's own rule, skipped by the seat; nothing to queue.
- **Revalidation mode (decision-watcher)** — not run this firing by dispatch design (forward
  mode only); a separate invocation if wanted, not debt.

## Resolved since the prior plan (2026-08-18T22:03Z firing)

- Prior entry 1 (apply the 22:03Z payloads) — DONE (checkpoint continuity 22:00:25Z;
  decision-watcher 22 previously known).
- Prior entry 2 (sync_main, 42 behind) — DONE BY EVENTS (primary clean on `main`, gap gone;
  the quarantine stash it predicted is entry 4's object).
- Prior entry 3 (review/merge PR #678) — DONE BY EVENTS (zero open PRs; remote head gone).
- Prior entry 4 (stashes) — carried forward as entry 4, upgraded unmeasured → measured
  (`stash@{0}` = `6d5a2801`).
- Prior entry 5 (five worktrees + deferred fix-667) — still open → entries 5 (fix-667/fix-684
  decisions) and 6 (the five runnable).
- Prior entry 6 (seven branches) — still open, grown to ten dangling → entry 6.
