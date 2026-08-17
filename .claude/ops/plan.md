# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-17T14:50:18Z** (UTC).
Evidence: all three seat reports attached, none UNMEASURED as seats — but the **#490 pin race
degraded 2 of 3 mid-firing** (decision-watcher: step 3 incomplete, checkpoint deliberately held;
repo-cleaner: gated executions blocked, then run clean by the coordinator in-firing — its report
applied at `reports/2026-08-17T14-50-18Z-repo-cleaner.md`). Issue-sorter fired clean: 36 issues
touched in-window, 25 closed via 19 merged PRs, 0 open PRs, checkpoint advanced to 14:50:18Z.
Open issue set: #490 (open by design) + #517–#527.

Prior plan (2026-08-17 ~11:42Z) is FULLY resolved: its ops commit landed; the 23-worktree/8-branch
batch cleanup and the `issue-475-teamwork-diet` ruling were consumed by the "34+ purged, main
synced" cleanup (repo-cleaner now counts 4 worktrees, 5 branches); #475 and #295 both closed
in-window; the stale-main refresh is moot (main synced). Queue rebuilds 5 → 11.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing. One
report-evidenced dependency ordered below anyway and named inline: the #517–#526 disposition
(entry 7) sits behind the ADR-0020 ruling (entry 3) — a held-state gate from issue-sorter's
report, not an inferred edge.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit + push this firing's ops artifacts — explicit pathspec only
- **Action:** `git status --porcelain` first, then stage exactly `.claude/ops/plan.md`,
  `.claude/ops/watch-checkpoint.json`, and this firing's report files
  (`.claude/ops/reports/2026-08-17T14-50-18Z-*.md`); read the status output, commit as a separate
  step (gate ≠ commit), push. **Never `git add -A`** — the primary checkout
  (`sweep-desk-to-seat` @ c393fcd) carries 13 modified + 1 untracked file that are HELD
  evidence for Kim (entry 6), not this firing's delta. `adr-checkpoint.json` is deliberately
  NOT advanced (decision-watcher held it pending step-3 re-fire) — stage it only if untouched
  since the prior firing's commit, else leave it.
- **Owner:** the dispatching session (coordinator).
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); repo-cleaner's held-untouched flag on the primary checkout's dirt.
- **Size:** ~2 min.

### 2. Append this firing's pin-race evidence to #490
- **Action:** `gh issue comment 490` with: firing 2026-08-17T14:50:18Z, 2 of 3 seats degraded
  mid-firing (decision-watcher blocked at step 3; repo-cleaner blocked on all 4 gated
  executions, signature "pinned to `.claude/worktrees/build-527`, never entered by the seat"),
  coordinator ran the four `campaign_close.py` gates itself — #506/#516/#513/#515 all clean.
  Append-only comment; safe now.
- **Owner:** coordinator.
- **Evidence:** repo-cleaner report §Tooling failure + coordinator addendum; decision-watcher's
  INCOMPLETE step 3 with the same signature.
- **Size:** ~5 min.

**Class 2 — items blocking other work:**

### 3. Ratify or reject ADR-0020
- **Action:** Kim reads `.claude/docs/adr/0020-fleet-vocabulary-and-binding-heads.md` (currently
  an UNTRACKED draft on the held `sweep-desk-to-seat` checkout — see entries 5/6) and rules.
  Status `proposed`/unratified; its supersession edges reverse fresh ADR-0015/0016/0017
  rulings, so decision-watcher correctly held them non-actionable. This single ruling gates
  ten held issues (entry 7).
- **Owner:** Kim (morning gate).
- **Evidence:** decision-watcher (edges held, unratified); issue-sorter (#517–#526 HELD on
  exactly this gate).
- **Size:** ~15–30 min.

### 4. Ticket + fix: `harness/workflows/chore-sweep.js` fails to launch
- **Action:** Mint the issue (`SyntaxError: Unexpected keyword 'export'` at launch — the
  skill's own "residual verification owed", now measured as a real defect), then dispatch the
  fix to a build seat, PR-opened ceiling. Until fixed, `/sweep-chores`' Workflow path is dead;
  every sweep rides the Agent-dispatch fallback (this firing did).
- **Owner:** coordinator mints the issue now; a teamwork build seat owns the fix.
- **Evidence:** dispatch standing context — launch failure reproduced this firing.
- **Size:** ~5 min ticket + ~30–60 min fix.

**Class 3 — human decisions:**

### 5. Identify the unidentified authoring session behind ADR-0020 / #517–#526
- **Action:** Kim traces which session authored the ADR-0020 draft and the #517–#526 family.
  Strong lead: the held primary-checkout state (branch `sweep-desk-to-seat` @ c393fcd, 13
  modified + 1 untracked — the untracked file IS the ADR-0020 draft) is the likely residue of
  that session. Rule takeover vs. abandon.
- **Owner:** Kim (morning gate).
- **Evidence:** issue-sorter ("authoring session unidentified"); repo-cleaner's held-untouched
  inventory naming the draft.
- **Size:** ~10 min.

### 6. Rule on the held desk→seat sweep evidence
- **Action:** Kim rules claim/land/discard on the `sweep-desk-to-seat` checkout's 13 modified +
  1 untracked files; snapshot preserved at
  `.claude/ops/reports/unclaimed-desk-seat-sweep-2026-08-17.diff.md`. Naturally follows
  entries 3 and 5 (same artifact cluster). No seat touches this state until ruled — entry 1's
  pathspec already excludes it.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Held, untouched.
- **Size:** ~10–15 min after entries 3/5.

### 7. Disposition #517–#526 — blocked by the ADR-0020 ruling (entry 3, open): do not start before it lands
- **Action:** After Kim rules on ADR-0020: ratified → release the ten for triage (issue-sorter
  re-classifies next firing); rejected → close the family with the ruling cited. Ten issues,
  one batched pass.
- **Owner:** Kim rules; issue-sorter applies the disposition next firing.
- **Evidence:** issue-sorter — #517–#526 HELD on the ratification gate.
- **Size:** ~10 min once unblocked.

### 8. Forward #490's platform report
- **Action:** Kim forwards the pin-race platform report upstream; entry 2's appended evidence
  (two more degraded seats in one firing) strengthens it — forward after entry 2 lands.
- **Owner:** Kim (morning gate).
- **Evidence:** #490 open by design as the tracking issue; two seats degraded this firing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 9. Ambiguous orphan worktree `verify-491-teamwork-hooks` — ancestry check, then remove
- **Action:** `git merge-base --is-ancestor e51c9f2 origin/main`; ancestor → `git worktree
  remove .claude/worktrees/verify-491-teamwork-hooks` + `git branch -D
  worktree-verify-491-teamwork-hooks`; NOT an ancestor → stop and escalate to Kim. Commit
  message duplicates merged PR #502's title under a different branch — likely duplicate, not
  yet verified.
- **Owner:** coordinator, or repo-cleaner next firing.
- **Evidence:** repo-cleaner §Proposed only (branch @ e51c9f2, no remote ref).
- **Size:** ~5 min.

### 10. Decision-watcher step-3-only re-fire — stale-citation check for adr-0011/adr-0016
- **Action:** Re-dispatch decision-watcher scoped to step 3 only (classify + harvest are done
  and correct: adr-0015..0019 → zero pack candidates). Checkpoint was deliberately held so
  this re-fire picks up cleanly. Pin-race mitigation: absolute-path Bash throughout.
- **Owner:** next firing, or coordinator re-dispatch sooner.
- **Evidence:** decision-watcher report — step 3 INCOMPLETE (Bash pin-race block), checkpoint
  not advanced.
- **Size:** ~10 min.

### 11. Re-measure `gitignore_check` + stale-claim survey
- **Action:** Both UNMEASURED this firing (#490 tool block mid-firing) — repo-cleaner runs them
  next firing. UNMEASURED is skipped-not-passed; carried here so the gap stays named.
- **Owner:** repo-cleaner, next firing.
- **Evidence:** repo-cleaner report §Inventory.
- **Size:** ~5 min next firing.

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **#527:** dispatched to a build seat by the coordinator, in flight — owns its own lifecycle;
  coordinator monitors the handback, nothing to queue.
- **#490 itself:** open by design (platform tracking issue) — only evidence entries (2, 8)
  queue; no local fix exists.
- **ADR harvest:** adr-0015..0019 judged, zero pack candidates (each names its canonical
  landing surface in its own ratifying change) — no confirm owed.
- **Coordinator's in-firing `campaign_close.py` runs** (#506/#516/#513/#515): all closed clean
  (merged, remote branch absent + reverified, gate clean) — recorded under Resolved, not queued.
- **Standing rulings carried:** root entry-file freshness CI gate = deliberate NO (Kim,
  2026-08-15); checkpoint-bypass = accepted one-off (Kim, 2026-08-14); `.gitignore`
  `harness-audit-*/` WARN = recorded judgment, no edit (re-verify rides entry 11's re-measure).

## Resolved since the prior plan (2026-08-17 ~11:42Z firing)

- Prior entry 1 (ops-artifacts commit) — landed.
- Prior entries 2 + 3 (23-worktree/8-branch batch cleanup; `issue-475-teamwork-diet` lock
  ruling) — consumed by the between-firings "34+ purged" cleanup; estate now 4 worktrees /
  5 branches.
- Prior entry 4 (build #475) — closed in-window (among the 25 closed via 19 merged PRs); #295
  also closed.
- Prior entry 5 (stale local `main`) — main synced between firings.
- New this firing, already executed in-firing by the coordinator: `campaign_close.py`
  #506/#516/#513/#515 — all clean, four remote branches deleted and reverified gone.
