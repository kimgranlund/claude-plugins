# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-17T18:35Z** (UTC).
Evidence: all three seat reports attached and complete — **no seat UNMEASURED this firing**
(dispatch-named UNMEASURED list: empty). decision-watcher: 20 ADRs, adr-0020 ratified
(proposed→accepted, gh#518), already harvested, 0 candidates queued, checkpoint advanced.
issue-sorter: 22 issues + 15 PRs in window (14:50:18Z→18:30:59Z), 9 new issues all fully formed
at mint, 0 held, checkpoint advanced. repo-cleaner: full inventory after `git fetch --prune`
(17 stale refs cleared), `sync_main.py` ok (main @ `28c6b697f`), `campaign_close.py 544` refused
on C2 (remote `worktree-build-522` survives delete), no stale claims, no stale-open PRs.

Prior plan (2026-08-17T14:50:18Z) is 10/11 resolved (see Resolved below); its entry 8 (#490
upstream forward) carries — no completion evidence in this firing's reports.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing. One
report-evidenced dependency ordered anyway and named inline: build-522's local cleanup (entry 5)
sits behind the C2 remote-delete remediation (entry 2) — campaign_close's own printed
remediation, not an inferred edge.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit + push this firing's ops artifacts — explicit pathspec only
- **Action:** `git status --porcelain` first, then stage exactly `.claude/ops/plan.md`,
  `.claude/ops/adr-checkpoint.json`, `.claude/ops/watch-checkpoint.json`,
  `.claude/ops/reports/2026-08-17T18-31-58Z-decision-watcher.md`, and
  `.claude/ops/reports/2026-08-17T18-35-11Z-repo-cleaner.md` (issue-sorter emitted no per-firing
  report file — checkpoint only, per its payload-fence rule). Read the status output, commit as a
  separate step (gate ≠ commit), push. Never `git add -A`.
- **Owner:** the dispatching session (coordinator).
- **Evidence:** ops-write-sandbox-rules — state persists through the repo or the next firing
  starts blind; all payload blocks present in the seat reports.
- **Size:** ~2 min.

### 2. Complete campaign_close #544 — delete the surviving remote branch, re-run
- **Action:** `gh api -X DELETE repos/kimgranlund/claude-plugins/git/refs/heads/worktree-build-522`,
  then re-run `campaign_close.py 544 --repo kimgranlund/claude-plugins --gate teamwork --gate
  harness`. This is the script's own printed remediation after its C2 refusal; PR #544
  independently verified MERGED twice (script + `git ls-remote` reconfirm), C1/C3/C4/C5 already
  clean. Unblocks entry 5.
- **Owner:** coordinator (or repo-cleaner next firing).
- **Evidence:** repo-cleaner §Executed — C2 FAILED, refusal reported not overridden; remediation
  named by the script itself.
- **Size:** ~5 min.

**Class 2 — items blocking other work:** none this firing (the one live dependency, entry 2 → 5,
already ranks in class 1 by its own gated-remediation status).

**Class 3 — human decisions:**

### 3. Forward #490's pin-race evidence upstream — carried from the prior plan
- **Action:** Kim confirms the 14:50Z firing's degradation evidence (2 of 3 seats blocked
  mid-firing) reached the upstream platform report; forward if not. Carried: the prior plan's
  entry 8, with no completion evidence in this firing's reports (only same-session comment
  activity on #490 is visible). Note this firing itself had zero pin-race degradation — all
  three seats ran clean.
- **Owner:** Kim.
- **Evidence:** prior plan entry 8 (open, unconfirmed); issue-sorter — #490 open by design,
  comment activity in-window.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 4. Batch-remove the orphaned post-merge worktrees and bare branches
- **Action:** run repo-cleaner's proposed commands verbatim (propose-only from that seat — no
  host reap script exists to gate them):
  ```
  git worktree remove .claude/worktrees/build-520 && git branch -D build-521-fleet-marshal-rename
  git worktree remove .claude/worktrees/build-541 && git branch -D worktree-build-541
  git worktree remove .claude/worktrees/build-548-docs && git branch -D fix-548-docs-batch
  git branch -D build-525-authorkit-skill-as-command worktree-build-520 worktree-build-529 worktree-build-548-docs
  ```
  All verified by repo-cleaner: PRs #540/#549/#545/#538/#546 MERGED with remotes gone, or content
  an ancestor of `origin/main` (build-541, worktree-build-529 — the former held-evidence branch,
  now landed; its snapshot at `.claude/ops/reports/unclaimed-desk-seat-sweep-2026-08-17.diff.md`
  stays untouched). Does NOT touch build-522 (entry 5) or build-523-w5 (active, PR #550 open).
- **Owner:** coordinator (or Kim by hand).
- **Evidence:** repo-cleaner §Inventory + §Proposed only — post-fetch-prune, accurate.
- **Size:** ~5 min.

### 5. Remove `.claude/worktrees/build-522` + its local branch — blocked by entry 2 (open): do not start before it lands
- **Action:** after entry 2's re-run of `campaign_close.py 544` passes C2, `git worktree remove
  .claude/worktrees/build-522 && git branch -D worktree-build-522`.
- **Owner:** coordinator (or repo-cleaner next firing).
- **Evidence:** repo-cleaner — worktree left as-is pending the C2 refusal's resolution.
- **Size:** ~2 min once unblocked.

### 6. Mint infrastructure ticket: clean-git must mandate `git fetch --prune` before inventory
- **Action:** file the issue (docs `file-task` shape): repo-cleaner found 17 stale `origin/*`
  tracking refs and a falsely-clean `main` read — any prior firing without a fetch/prune first
  worked from stale inventory. Fix = an explicit fetch-prune step at the top of harness's
  `clean-git` procedure skill (semantic edit → rides with a checker per plugin-authoring rules).
  Incident → infrastructure, same day, per workspace invariant.
- **Owner:** coordinator mints; a harness build seat owns the fix.
- **Evidence:** repo-cleaner §Tooling note — measured this firing, not hypothesized.
- **Size:** ~5 min ticket + ~15–30 min fix.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PR #550 / #523 (wave 5, mid-build):** OPEN, fresh (17:55Z), healthy — owns its own lifecycle;
  merge is Kim's per the auto-mode ceiling. #524/#525 likewise open mid-build (#525 carries a
  fresh assignee claim, ~40 min old — not stale per ADR-0005).
- **#490 itself:** open by design (platform tracking issue) — only entry 3's forward queues.
- **ADR-0020 waves 3–7:** open execution work per the ADR's own Consequences table, tracked by
  the open wave issues and driven by the in-flight builds — not a knowledge-pack gap
  (decision-watcher: already harvested, reject-as-duplicate).
- **adr-0015 partial supersession:** zero downstream citations of the superseded clause
  (decision-watcher grepped the full corpus) — nothing to repair.
- **decision-watcher confirm:** 0 candidates pending — no batched confirm owed.
- **gh GraphQL 503s:** transient, all calls retried to success, no inventory gap — nothing to fix.
- **Narrated-but-absent audit:** clean — every claimed ops write in all three reports is backed
  by a fenced, target-pathed block (or explicitly declared unchanged-and-omitted).
- **Standing rulings carried:** `.gitignore` G1 WARNs (`dist/`, `harness-audit-*/`) pre-ruled
  on-demand-generated/accepted, no edit; root entry-file freshness CI gate = deliberate NO (Kim,
  2026-08-15); checkpoint-bypass = accepted one-off (Kim, 2026-08-14).

## Resolved since the prior plan (2026-08-17T14:50:18Z firing)

- Prior entry 1 (ops-artifacts commit) — landed (this firing's seats diffed against those files).
- Prior entry 2 (#490 evidence comment) — landed (issue-sorter: in-window comment activity on #490).
- Prior entry 3 (ratify/reject ADR-0020) — RESOLVED: accepted, Kim's live tie-break per gh#518
  (commit `06c95df`); decision-watcher re-judged the ratified body, already harvested.
- Prior entry 4 (chore-sweep.js launch failure) — fixed and closed (#529 via merged PR #530,
  harness 3.8.34).
- Prior entries 5 + 6 (authoring-session trace; held desk→seat evidence ruling) — resolved: the
  held content landed on `origin/main` (repo-cleaner: `worktree-build-529`'s commit is now an
  ancestor); snapshot preserved untouched; only the branch delete remains (rides entry 4).
- Prior entry 7 (#517–#526 disposition) — resolved by the ADR-0020 wave merges: #517–#522, #526,
  #527 closed; #523/#524/#525 open mid-build, in flight.
- Prior entry 8 (#490 upstream forward) — CARRIED as entry 3 (no completion evidence).
- Prior entry 9 (verify-491 orphan worktree) — gone from this firing's inventory; resolved.
- Prior entry 10 (decision-watcher step-3 re-fire) — resolved: full clean firing, checkpoint
  advanced.
- Prior entry 11 (gitignore + stale-claim re-measure) — resolved: both measured clean this firing.
