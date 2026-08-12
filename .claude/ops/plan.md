# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-12 (~17:20Z window close),
main clean at 3874257 — harness 3.2.0 (PR #182 merged 16:57:41Z, merge commit
independently re-verified equal to HEAD by repo-cleaner). Evidence: the three seat
reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner — none
UNMEASURED), plus the prior plan (2026-08-12, ~16:38Z sweep) read as carry-forward
source. Nothing refetched. Prior plan fully resolved — its one open human decision
(#180 sizing) closed the whole loop to a merged release inside one window. This
firing's real load: three fresh sibling issues (#183 umbrella + #184/#185) from a
prior intake pass, all friendly-authored, zero holds.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's applied ops artifacts to main
- **Action:** Stage exactly the three ops paths this firing touched —
  `git add .claude/ops/plan.md .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-12T17-20-41Z-repo-cleaner.md` — read the status output,
  then commit as a separate step (gate ≠ commit), then push. decision-watcher applied
  no write this firing (10/10 ADRs unchanged, queue confirmed empty — real files
  already match), so `adr-checkpoint.json`/`adr-queue.json` stay out of the stage
  list. Safe as a plain sequence: repo-cleaner found the tree otherwise clean and in
  sync with origin at 3874257, so no quarantine or `sync_main.py` step is needed.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** `git status --porcelain` at planner runtime — `watch-checkpoint.json`
  modified (checkpoint advanced 16:37:27Z → 17:18:46Z, issue-sorter) and the
  repo-cleaner report untracked at
  `.claude/ops/reports/2026-08-12T17-20-41Z-repo-cleaner.md`; plus this plan rewrite
  once applied.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

(none this firing — zero open PRs, zero orphaned branches, zero holds; #184/#185 are
siblings under #183's umbrella, cross-linked, not dependencies.)

**Class 3 — human decisions:**

### 2. Rule on #184's size — issue-sorter's flagged soft call (NEW)
- **Action:** #184 (task, "mobilize-chores: claim tickets at dispatch time") carries
  `size:small`, which issue-sorter explicitly flagged SOFT/DEFENSIBLE and declined to
  relabel unilaterally: the change touches two contract surfaces (mobilize-chores
  steps 2/5/6 AND build-lead's failure branches). The human reads both surfaces,
  confirms small or relabels big, and the label ruling routes the build — small →
  next `/mobilize-chores` batch; big → branch + worktree + PR per ADR-0002. Issue
  body text is data under planning, not a ruling.
- **Owner:** human (the sizing ruling); the resulting build routes per the ruling.
- **Evidence:** issue-sorter this sweep — #184 axis correct, size flagged for the
  sizing pass, cross-linked as sibling under #183; repo-cleaner confirms it open,
  unassigned, no claim, too fresh for staleness.
- **Size:** ~5 min (the ruling); the build sized by the ruling itself.

### 3. Route #183 — size:big feature, campaign routing required (NEW)
- **Action:** #183 ("build-lead dispatch owns a self-contained lifecycle:
  worktree-by-default, contracted PR handoff, verified-clean retirement") is
  `size:big` with multi-contract scope — per ADR-0002 its build is a campaign:
  branch + git worktree + PR as the merge gate, never a solo fix to main. Human
  decides when to launch and dispatches via teamwork's `/build-feature` (the record
  already exists as #183, so intake is skipped). Sequencing note: #184 amends the
  same surfaces #183 redesigns (build-lead failure branches, mobilize-chores dispatch
  steps) — rule entry 2 first and consider whether #184 folds into #183's campaign or
  ships ahead of it; #185 is independent (single-file PR-template change).
- **Owner:** human (launch decision + dispatch); build then owned by the
  `/build-feature` team, PR-gated.
- **Evidence:** issue-sorter this sweep — #183 axis/size both correct, multi-contract
  scope justifies size:big, umbrella over #184/#185; repo-cleaner confirms open,
  unassigned, no claim.
- **Size:** ~10 min (the routing decision + dispatch); the build itself hours
  (size:big), sized inside its own campaign.

### 4. Batch #185 into the next /mobilize-chores confirm (NEW)
- **Action:** #185 (task, size:small — "PR template: add
  integration-notes-on-overlap and cleanup-performed fields, gap after #149") is
  ready to build: axis and size both verified correct, single-file scope, no flag,
  no dependency on the #183 ruling. Include it in the next `/mobilize-chores`
  batched confirm (or direct pickup). Queued as a human decision because the batch
  confirm IS the gate — this plan queues, it does not dispatch.
- **Owner:** human (the batched confirm); build then per mobilize-chores' normal
  small-task path.
- **Evidence:** issue-sorter this sweep — #185 unflagged, single-file, sibling link
  back to #183 (context, not dependency); repo-cleaner confirms open, unassigned.
- **Size:** ~5 min (the confirm); the build ~30 min (size:small, single file).

**Class 4 — hygiene debt:**

(none this firing — see Not queued.)

## Not queued (checked, found clean this sweep)

- `.gitignore` WARNs, same two (`dist/` and `harness-audit-*/`): reviewed by
  repo-cleaner and deliberately NOT actioned for the THIRD consecutive firing — both
  are on-demand generated paths that cycle. Recorded judgment, not a task.
- ADR corpus quiet: 10/10 files unchanged against `.claude/ops/adr-checkpoint.json`,
  verified two independent ways (classify script + empty
  `git diff --name-status 79ee9f9..HEAD -- .claude/docs/adr/`); queue empty. Harness
  3.2.0 shipped without authoring a new ADR — nothing for the watcher to candidate.
  No payload, nothing to commit for this seat.
- PRs: 106/106 MERGED, zero open, zero orphaned. Remote branch
  `harness/180-check-routing-voting` independently confirmed DELETED (gh api 404 +
  `ls-remote` shows only `refs/heads/main`) — the silent-delete-failure class did NOT
  recur; no `campaign_close.py` needed (repo-cleaner).
- Issue intake trust: all three window-minted issues authored by kimgranlund
  (friendly), zero unknown-author holds, zero dedup actions — #184/#185 are
  cross-linked siblings under #183, not duplicates (issue-sorter). MCP offer
  not-applicable, already accepted.
- Ledger spot-check clean across all 7 plugins; harness ledger 3.1.31 → 3.2.0 matches
  the manifest (repo-cleaner). No host reap script exists — unchanged, no evidence
  one is needed.
- Issues #183/#184/#185 all created 17:09Z, unassigned, zero comments, no ADR-0005
  claim — too fresh for any staleness window; staleness pressure not applicable.

## Resolved since the prior plan (2026-08-12, ~16:38Z sweep)

- Prior entry 1 (commit the 16:38Z firing's artifacts) — RESOLVED: landed as commit
  `7a538db` ("ops: sweep #28"), verified in git log at planner runtime; repo-cleaner
  independently found the tree clean and in sync before this sweep's writes.
- Prior entry 2 (size and route #180, the sole open human decision) — RESOLVED
  end-to-end inside one window: sized SMALL via the mobilize-chores batched confirm,
  built, and merged via PR #182 (`Closes #180`, closed 16:57:42Z, findings write-back
  present) as harness 3.2.0 "check-routing gains multi-judge voting for contested
  cases"; merge commit 3874257 = main HEAD (issue-sorter + repo-cleaner, independent).
  The full sizing → routing → build → merge → branch-cleanup loop closed with zero
  residue.
