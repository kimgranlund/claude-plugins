# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T22:03Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
Two sub-measurements remain unmeasured by the seats' own admission: the primary checkout's
direct dirty-tree read (repo-cleaner: sandbox blocks `-C`/`cd` to the primary from this
worktree-isolated session; `primary_checkout_check.py` did return **clean, on `main`**) and
the primary's **stash inventory** (silent a FOURTH consecutive firing).

decision-watcher: clean no-op — 22/22 ADRs match the checkpoint, nothing new/amended/
superseded, adr-queue empty (0 pending); no payload block owed, none emitted.
issue-sorter: window 17:18:08Z→22:00:25Z, 22 new issues (#649–#677 range) + 8 new PRs
(#651…#678; 7 merged, #678 open) + #648 merged closing #647 — every issue already
record-shaped and kind/severity/size-labeled at filing, trusted author, 0 mints, 0 held,
0 needs-ruling, 0 unknown authors; #672 checked for ruling-shape and cleared as a buildable
`task`; two payload blocks (`watch-checkpoint.json`, its per-firing report).
repo-cleaner: gated `git fetch --prune` pruned 4 stale remote refs, `origin/main` tracking
ref +42; primary clean on `main` but **behind 42**; SIX orphaned worktrees now (629,
build-554, fix-647, fix-656, fix-660, and fix-667 — the worktree this sweep itself runs in)
and SEVEN orphaned local branches, all merged with remotes gone; stale-claim check clean
(#658/#662 both freshly active); one payload block (its report).

**Prior plan (2026-08-18T17:20Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(checkpoint continuity: this firing's issue-sorter window opens at exactly 17:18:08Z, the
applied value; decision-watcher reads 22 previously known). Entry 2 (sync_main: 30 behind) —
NOT DONE, gap grew to 42 — RE-SCOPED as entry 2 below. Entry 3 (review/merge PR #648) —
DONE BY EVENTS (MERGED 17:17:52Z, #647 closed); its inline dependent — the fix-647 worktree
reap — is now UNBLOCKED and joins entry 5. Entry 4 (stash resolution) — CARRIES FORWARD,
still unverified (entry 4). Entry 5 (two orphaned worktrees) — still open, GROWN to five
runnable + one deferred (entry 5). Entry 6 (six orphaned branches) — still open, GROWN to
seven (entry 6).

**Parked-issue check:** no prior-plan entry id (#647/#648, #612, #645/#646, the branch PRs)
carries `backlog`/`roadmap` in this firing's evidence — nothing dropped. #617 (the
`backlog`-labeled fixture) is not in any attached report and was never a plan entry; stays
excluded per the #611 parking rule.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline on their own entries:
entry 1's persist half folds into entry 2 (worktree-isolation Bash wall); entry 4 waits on
entry 2 (sync_main may add a stash); the fix-667 worktree reap inside entry 5 is blocked by
THIS live session (reap only after it exits); PR #678's eventual `campaign_close.py` waits
on the merge in entry 3.

**needs-ruling lane:** empty — issue-sorter reports 0 needs-ruling, 0 held; #672 explicitly
checked and left as `task`, so no §3 reference is owed.

**Sandbox hazard, named:** this sweep runs inside `.claude/worktrees/fix-667`, whose branch
(PR #668) is already MERGED — any payload written to THIS worktree's `.claude/ops/` path is
stranded on a dead branch. issue-sorter's "Files touched" prose names worktree-rooted target
paths; the fenced blocks themselves are target-pathed relative (`.claude/ops/...`) — apply
them at the SHARED checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout, not this worktree)
- **Action:** write the fenced payloads verbatim: `.claude/ops/watch-checkpoint.json`
  (issue-sorter — checkpoint 22:00:25Z, strictly newer than the applied 17:18:08Z),
  `.claude/ops/reports/2026-08-18T22-00-25Z-issue-sorter.md` (issue-sorter),
  `.claude/ops/reports/2026-08-18T22-03-18Z-repo-cleaner.md` (repo-cleaner), plus this
  rewritten `.claude/ops/plan.md`. `adr-checkpoint.json`, `adr-queue.json`,
  `friendlies.json`, `held-items.md`, `.mcp.json` explicitly unchanged — no blocks owed,
  none applied. Target `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...` (the shared
  checkout) — this worktree's branch is merged; a write here strands. **Commit + push
  cannot run from this worktree-isolated session** (repo-cleaner: sandbox refuses git ops
  targeting the primary) — the persist step folds into entry 2's sitting; never improvise
  around the wall.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules); the
  commit/push lands with entry 2 (Kim).
- **Evidence:** all four fenced blocks present in this firing's reports (three seat
  payloads + this plan); repo-cleaner §Executed (`sync_main.py` not invocable from here);
  ops-write-sandbox-rules (state persists through the repo or the next firing starts blind).
- **Size:** ~2 min (apply only).

**Class 2 — blocking other work:**

### 2. Run `sync_main.py` at the primary from a non-worktree session — 42 behind; blocks ops-state persistence, entry 4, and the reaps in 5/6
- **Action:** from a session actually checked into `/Users/kimba/Projects/nonoun/plugins`
  (NOT worktree-isolated): run `sync_main.py` — quarantines any dirt as a named stash
  (`primary_checkout_check.py` read clean; direct `git status` unobtained — sync_main
  handles either case), `--ff-only` pulls the 42-commit gap (0 ahead per `branch -vv` — a
  clean fast-forward), reverifies HEAD by SHA. Then stage exactly this firing's applied
  payload paths (entry 1; never `git add -A`), read the status output, commit as a separate
  step (gate ≠ commit), push. Two firings' worth of checkpoints (17:20Z applied locally,
  22:03Z now) have not yet reached the repo — the next scheduled firing starts blind until
  they do.
- **Owner:** Kim (the only actor with a non-worktree session at the primary).
- **Evidence:** repo-cleaner §Proposed — `[origin/main: behind 42]`, named as merge-volume
  drift after 7 PR merges this window, not a defect; workspace CLAUDE.md names
  `sync_main.py` as the gate for exactly this case; prior plan entry 2 unexecuted (was 30).
- **Size:** ~5 min.

**Class 3 — human decisions:**

### 3. Review and merge open PR #678 (`fix-658-owed-chain-spec-lock`, closes #658) — held approval
- **Action:** review PR #678 and merge or bounce it. Unattended flows cannot merge (the
  classifier blocks `gh pr merge` in auto mode — standing rule); waits on a human by design.
  Once merged, close it with `campaign_close.py 678 --repo kimgranlund/claude-plugins
  --gate <touched-plugin-root>` per the workspace campaign row — verifies MERGED, deletes
  the remote branch and reverifies it gone. No local worktree/branch for it exists in this
  checkout (live elsewhere), so no reap follows here.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Healthy — PR #678 OPEN, remote branch present in
  `git ls-remote --heads origin` (one of only two heads left); issue #658 assigned to
  kimgranlund, linked by branch-name convention, fresh; issue-sorter — #678 the one
  unmerged PR of 8 discovered.
- **Size:** ~10–15 min (review-dependent).

### 4. Resolve the stash(es) at the primary — carried forward, unverified FOUR firings running; blocked by #2 above (named inline — sync_main may add one more)
- **Action:** after entry 2: `git stash list` at the primary. The old "sync_main
  quarantine" stash from the 02:32Z-era dirt is still unverified — no repo-cleaner firing
  since has carried a stash inventory. If empty, note resolved-by-events in the next plan
  and retire this entry. If populated: the tracked-file dirt it holds is long superseded by
  applied payloads — selectively restore only anything a live sweep still owns
  (`sweep-in-flight.json`), then drop. Stash resolution is judgment, outside repo-cleaner's
  gated calls.
- **Owner:** Kim (one batched decision, same sitting as entry 2).
- **Evidence:** prior plan entry 4 (carry-forward source, not fresh evidence); this firing's
  repo-cleaner report again silent on stash inventory (unmeasured).
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 5. Remove five orphaned worktrees and their branches now; fix-667 (this session's own) only after this session exits
- **Action:** from the shared checkout, for each: `git worktree remove <path>` then
  `git branch -d <branch>` —
  `.claude/worktrees/629-self-improvement-retrospective` / `629-self-improvement-retrospective`
  (PR #645 MERGED); `.claude/worktrees/build-554` / `634-req-infix-prefix` (PR #646 MERGED);
  `.claude/worktrees/fix-647` / `fix-647-attention-audit-dmi-drift` (PR #648 MERGED
  17:17:52Z — newly orphaned); `.claude/worktrees/fix-656-rdd-revalidation-rotation` /
  same-named branch (PR #663 MERGED 21:04:02Z); `.claude/worktrees/fix-660` /
  `fix-660-artifact-check-false-positives` (PR #661 MERGED 20:54:14Z). Verify with
  `git worktree list`. **Deferred, named inline:** `.claude/worktrees/fix-667` /
  `fix-667-build-feature-gh541-doctrine` (PR #668 MERGED 21:35:38Z) is the worktree this
  sweep is running in — blocked by the live session; reap it in the same way once the
  session is confirmed idle, never mid-session. All six remotes already pruned. Stays
  propose-only from the seat: no host-repo reap script exists in this workspace to gate it.
- **Owner:** Kim (or the coordinator session running entry 2, same sitting); the fix-667
  reap: Kim, after this session exits.
- **Evidence:** repo-cleaner §Proposed — merged-PR ids/timestamps per worktree, remote
  branches confirmed gone via `git ls-remote --heads origin` (only `main` and
  `fix-658-...` remain); prior plan entry 5 (629, build-554) carried forward.
- **Size:** ~5 min (+ ~1 min later for fix-667).

### 6. Batch-delete seven orphaned local branches — merged, no worktree, remotes gone
- **Action:** `git branch -d` each: `608-dispatch-ticket-file-bug-claim-fix` (PR #610),
  `611-backlog-roadmap-releases-loop` (PR #621), `612-harvest-domain-knowledge` (PR #614),
  `613-harvest-project-context` (PR #615), `622-feedback-intake-door` (PR #641),
  `637-drain-queue-command` (PR #643), `650-artifact-styling-rules` (PR #651 — new this
  firing). Verify with `git branch -vv`. Absorbs the prior plan's entry 6 (six → seven).
- **Owner:** Kim (or the coordinator session, same sitting as entries 2/5).
- **Evidence:** repo-cleaner §Proposed — all seven read merged into the history their PR
  closed against; remotes absent from `git ls-remote --heads origin`.
- **Size:** ~2 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — no-op firing, explicitly invokes the payload-fence rule
  ("no fenced target-pathed payload is included — there is nothing to apply"); no path
  narrated as written.
- **issue-sorter:** clean — both narrated paths (`watch-checkpoint.json`, the 22:00:25Z
  report) have matching fenced, target-pathed blocks; `friendlies.json` / `held-items.md` /
  `.mcp.json` explicitly declared unchanged and omitted. Note only: its prose names
  worktree-rooted absolute targets — apply at the shared checkout (entry 1).
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block;
  `sync_main.py`, `campaign_close.py`, and all worktree/branch deletions explicitly marked
  not-invoked / proposed-only.

## Not queued (checked, found clean or deliberately left)

- **Issue #662 claim** (`fix-662-token-naming-unprefix`) — active build, claimed 21:39Z,
  last comment 21:59Z; no local artifact here; not stale (ADR-0005). Its PR, once opened,
  is a future held approval.
- **Issue #658 claim** — backs PR #678 (entry 3); nothing separate to queue.
- **#672** ("Orchestration review Track A: ADR ruling native agent-teams vs hand-rolled
  fleet") — issue-sorter checked the body: buildable `task` (draft ADR via `/make-doc`,
  ratify live), NOT `needs-ruling`; buildable backlog routes through teamwork's
  `/mobilize-chores`, outside this queue.
- **Remaining open issues (19 per issue-sorter's sweep, incl. #609, #605, #490)** — all
  kind-labeled, 0 missing labels, only #658/#662 assigned; buildable backlog → `/mobilize-
  chores`. #490 open by design (upstream pin-race tracking).
- **#617** — `backlog`-labeled fixture, excluded per the #611 parking rule; not in this
  firing's evidence, never a plan entry.
- **Closed-not-merged PRs #437/#391** — standing finding, branches already absent from the
  remote, no gated close path; no action.
- **`gitignore_check.py` WARNs** — same standing sets both roots (primary: `dist/`,
  `harness-audit-*/`; worktree adds `.DS_Store`, `.claude/worktrees/`); no FAIL, unchanged.
- **ADR corpus** — 22/22 checkpointed, adr-queue empty; nothing to harvest.
- **Stale session gitStatus** — the dispatch context's gitStatus block (branch `fix-423-...`,
  dirty `fleet-roster.md`/`settings.json`/`attention-trend.csv`) does not match this
  worktree's real branch (`fix-667-...`); noise, not state — flagged, not acted on.

## Resolved since the prior plan (2026-08-18T17:20Z firing)

- Prior entry 1 (apply the 17:20Z payloads) — DONE (checkpoint continuity 17:18:08Z;
  decision-watcher 22 previously known).
- Prior entry 2 (primary 30 behind) — NOT DONE; re-scoped to 42 → entry 2.
- Prior entry 3 (review/merge PR #648) — DONE BY EVENTS (MERGED 17:17:52Z, #647 closed);
  fix-647 reap unblocked → entry 5.
- Prior entry 4 (stashes) — CARRIED FORWARD as entry 4, still unverified (fourth firing).
- Prior entry 5 (two orphaned worktrees) — still open, grown to five + one deferred → entry 5.
- Prior entry 6 (six orphaned branches) — still open, grown to seven → entry 6.
