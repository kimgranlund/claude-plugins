# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-18T17:20Z** (UTC,
repo-cleaner's report timestamp — the latest seat). Evidence: all three seat reports attached
and complete — **no seat UNMEASURED this firing** (dispatch-named UNMEASURED list: empty).
Two sub-measurements are named unmeasured by the seats themselves: the primary checkout's
direct dirty-state read (repo-cleaner: sandbox refused `git status` at the primary —
`primary_checkout_check.py` did return **clean, on `main`**, but the seat flags the direct
read as unobtained) and the primary's **stash inventory** (silent a third consecutive firing).

decision-watcher: 2 new ADRs judged (adr-0021 trust tiers, adr-0022 repo-is-the-backup) —
both already covered by existing citations/instruments, **no harvest candidates queued**,
adr-queue unchanged; one payload block owed (`adr-checkpoint.json`, 20→22 entries).
issue-sorter: window 02:28:59Z→17:18:08Z, 17 issues + 18 PRs touched — all but **#647**
already closed by the intervening build-drain; #647 (bug/minor) already record-shaped and
labeled at filing, trusted author, PR #648 open against it — resumed, not re-minted; 0 held,
0 needs-ruling, 0 unknown authors; one payload block (`watch-checkpoint.json`).
repo-cleaner: gated `git fetch --prune` pruned 8 stale remote-tracking refs; primary clean on
`main` but **behind 30**; two orphaned worktrees (629, build-554) and six orphaned local
branches, all merged with remotes already gone; current worktree fix-647 healthy backing open
PR #648; stale-claim check clean (0 assignees on 5 open issues); one payload block (its
report).

**Prior plan (2026-08-18T02:32Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(checkpoint continuity: this firing's issue-sorter window opens at exactly 02:28:59Z, the
applied value). Entry 2 (sync_main: dirty + 8 behind) — the dirt RESOLVED
(`primary_checkout_check.py` → clean this firing); the behind-gap grew to 30 — RE-SCOPED as
entry 2 below. Entry 3 (stash resolution) — CARRIES FORWARD, still unverified (entry 4).
Entry 4 (delete stray `608-...` branch) — still open, FOLDED into the six-branch batch
(entry 6). Entry 5 (remove build-554 worktree, blocked by #612) — UNBLOCKED BY EVENTS: the
#612 build landed (PR #614 MERGED), the worktree was reused once more onto
`634-req-infix-prefix`, and that PR (#646) also MERGED — now runnable (entry 5).

**Parked-issue check:** no prior-plan entry id carries `backlog`/`roadmap` — nothing dropped.
#617 (backlog-labeled fixture) stays correctly excluded per the #611 parking rule; it was
never a plan entry.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Two operational dependencies named inline on their own entries:
entry 1's commit/push step folds into entry 2 (the worktree-isolation Bash wall), and the
fix-647 worktree's eventual reap is blocked by open PR #648 (named on entry 3; the reap
itself is deliberately NOT queued — see Not queued).

**needs-ruling lane:** empty — issue-sorter reports 0 needs-ruling, 0 held.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths
- **Action:** write the fenced payloads verbatim: `.claude/ops/adr-checkpoint.json`
  (decision-watcher — 22 ADR entries, adds adr-0021/adr-0022),
  `.claude/ops/watch-checkpoint.json` (issue-sorter — checkpoint 17:18:08Z, strictly newer
  than the applied 02:28:59Z), `.claude/ops/reports/2026-08-18T17-20-06Z-repo-cleaner.md`
  (repo-cleaner), plus this rewritten `.claude/ops/plan.md`. `adr-queue.json`,
  `friendlies.json`, `held-items.md` explicitly unchanged — no blocks owed, none applied.
  Target the SHARED checkout's paths, not this worktree's (ops-write-sandbox-rules stranding
  hazard). **Commit + push cannot run from this worktree-isolated session** (repo-cleaner:
  the sandbox refuses git ops targeting the primary) — the persist step folds into entry 2's
  sync_main sitting; do not improvise around the wall.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules); the
  commit/push lands with entry 2 (Kim).
- **Evidence:** all four fenced blocks present in this firing's reports; repo-cleaner
  §Executed (sync_main not invocable from here); ops-write-sandbox-rules (state persists
  through the repo or the next firing starts blind).
- **Size:** ~2 min (apply only).

**Class 2 — blocking other work:**

### 2. Run `sync_main.py` at the primary from a non-worktree session — 30 behind; blocks ops-state persistence
- **Action:** from a session actually checked into `/Users/kimba/Projects/nonoun/plugins`
  (NOT worktree-isolated): run `sync_main.py` — it quarantines any dirt as a named stash
  (`primary_checkout_check.py` read clean this firing, but the seat could not confirm by
  direct `git status`; sync_main handles either case), `--ff-only` pulls the 30-commit gap,
  reverifies HEAD by SHA. Then stage exactly this firing's applied payload paths (entry 1;
  never `git add -A`), read the status output, commit as a separate step (gate ≠ commit),
  push. This entry blocks entry 1's persist half — the next scheduled firing starts blind if
  the checkpoints never reach the repo — and entry 4's stash assessment (sync_main MAY add a
  stash).
- **Owner:** Kim (the only actor with a non-worktree session at the primary).
- **Evidence:** repo-cleaner §Proposed — `[origin/main: behind 30]` from `branch -vv`, named
  as normal merge-volume drift, not a defect; workspace CLAUDE.md names `sync_main.py` as
  the gate for exactly this case.
- **Size:** ~5 min.

**Class 3 — human decisions:**

### 3. Review and merge open PR #648 (authorkit 0.22.1, closes #647) — held approval
- **Action:** review PR #648 ("attention-audit demote-to-wiring no longer prescribes
  dmi:true for dispatch-reached sides") and merge or bounce it. Unattended flows cannot
  merge (the classifier blocks `gh pr merge` in auto mode — standing rule); this waits on a
  human by design. Once merged, close it with `campaign_close.py 648 --repo <owner/repo>
  --gate authorkit` per the workspace campaign row — that also frees the fix-647 worktree
  and its branch (the reap is blocked by this PR while open, named here inline; not queued
  as its own entry).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Current worktree — fix-647 clean, in sync, backing open #648;
  issue-sorter — #647 fully record-shaped, PR already targeting it, intake confirmed state
  and correctly took no action.
- **Size:** ~10–15 min (review-dependent).

### 4. Resolve the stash(es) at the primary — carried forward, unverified three firings running; blocked by #2 above (named inline — sync_main may add one more)
- **Action:** after entry 2: `git stash list` at the primary. The old "sync_main
  quarantine" stash from the 02:32Z-era dirt is still unverified — no repo-cleaner firing
  since has carried a stash inventory. If empty, note resolved-by-events in the next plan.
  If populated: the tracked-file dirt it holds is long superseded by applied payloads —
  selectively restore only anything a live sweep still owns (`sweep-in-flight.json`), then
  drop. Stash resolution is judgment, outside repo-cleaner's gated calls.
- **Owner:** Kim (one batched decision, same sitting as entry 2).
- **Evidence:** prior plan entry 3 (carry-forward source, not fresh evidence); this
  firing's repo-cleaner report again silent on stash inventory (unmeasured).
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 5. Remove the two orphaned worktrees and their branches — runnable now (unblocked by events)
- **Action:** from the shared checkout: `git worktree remove
  .claude/worktrees/629-self-improvement-retrospective` + `git branch -d
  629-self-improvement-retrospective` (PR #645 MERGED 14:51Z); `git worktree remove
  .claude/worktrees/build-554` + `git branch -d 634-req-infix-prefix` (PR #646 MERGED
  15:37Z). Verify with `git worktree list`. build-554 carried forward from the prior plan's
  entry 5, its #612 blocker long since landed; its third occupant branch (634) is also
  merged. Both remotes already pruned this firing. Stays propose-only from the seat: no
  host-repo reap script is named in this workspace's CLAUDE.md/README to gate it.
- **Owner:** Kim (or the coordinator session running entry 2, same sitting).
- **Evidence:** repo-cleaner §Proposed — merged-PR timestamps, remote branches confirmed
  gone via `git ls-remote --heads origin` (only `main` and `fix-647-...` remain).
- **Size:** ~3 min.

### 6. Batch-delete six orphaned local branches — merged, no worktree, remotes gone
- **Action:** `git branch -d` each: `608-dispatch-ticket-file-bug-claim-fix` (PR #610),
  `611-backlog-roadmap-releases-loop` (PR #621), `612-harvest-domain-knowledge` (PR #614),
  `613-harvest-project-context` (PR #615), `622-feedback-intake-door` (PR #641),
  `637-drain-queue-command` (PR #643). Verify with `git branch -vv`. Absorbs the prior
  plan's entry 4 (the 608 branch, now one of six).
- **Owner:** Kim (or the coordinator session, same sitting as entries 2/5).
- **Evidence:** repo-cleaner §Proposed — all six read merged into the history their PR
  closed against; all six remotes pruned by this firing's `git fetch --prune`.
- **Size:** ~2 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — `adr-checkpoint.json` payload present and target-pathed;
  `adr-queue.json` explicitly declared unchanged with the no-fence rule invoked by name.
- **issue-sorter:** clean — `watch-checkpoint.json` block present; `friendlies.json` /
  `held-items.md` explicitly declared unchanged and omitted; no per-firing report path
  narrated this firing, so none owed.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block;
  `sync_main.py`, `campaign_close.py`, and all worktree/branch deletions explicitly marked
  not-invoked / proposed-only (the opposite of a narrated write).

## Not queued (checked, found clean or deliberately left)

- **fix-647 worktree reap** — the CURRENT worktree, healthy and backing open PR #648; only
  reapable post-merge via `campaign_close.py` (entry 3 names it inline). Queuing its removal
  now would queue an action against live work.
- **#617** — `backlog`-labeled fixture, correctly excluded per the #611 parking rule (both
  by issue-sorter's sweep and by this plan's standalone-read rule).
- **Open issues #609, #605, #490** — kind-labeled, unassigned, no stale claims; buildable
  backlog routes through teamwork's `/mobilize-chores`, outside this queue. #490 open by
  design (upstream pin-race tracking).
- **Closed-not-merged PRs #437/#391** — branches already absent from the remote, no gated
  close path for a non-merged PR; no action.
- **`gitignore_check.py` WARNs** — same standing sets both roots (primary: `dist/`,
  `harness-audit-*/`; worktree adds `.DS_Store`, `.claude/worktrees/`); no FAIL, identical
  to the prior firing.
- **ADR corpus** — 22/22 checkpointed after entry 1 applies; both new ADRs already covered
  by existing citations/instruments, adr-queue still empty.
- **Stale session gitStatus** — repo-cleaner flagged its dispatch context's gitStatus block
  (branch `fix-423-...`, dirty ledgers) as mismatched against the worktree's real state
  (`fix-647-...`, clean); flagged-not-acted-on is correct; nothing to queue — noise, not
  state.

## Resolved since the prior plan (2026-08-18T02:32Z firing)

- Prior entry 1 (apply the 02:32Z payloads + persist) — DONE (checkpoint continuity: this
  firing's issue-sorter window opens at 02:28:59Z).
- Prior entry 2 (primary dirty + 8 behind) — dirt RESOLVED (`primary_checkout_check.py` →
  clean); behind-gap re-scoped to 30 → entry 2.
- Prior entry 3 (stashes) — CARRIED FORWARD as entry 4, still unverified.
- Prior entry 4 (stray `608-...` branch) — FOLDED into entry 6's six-branch batch.
- Prior entry 5 (build-554 worktree, blocked by #612) — UNBLOCKED BY EVENTS (#612 landed
  via PR #614; the reused occupant `634-...` landed via PR #646) → entry 5.
