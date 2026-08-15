# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-15 ~21:15Z window (UTC),
main at `99702e3`, sweep scope-weighted "authorkit hardening" (a lens, not a filter).
Evidence: all three seat reports attached (none UNMEASURED) — decision-watcher (sole
delta adr-0012 new; one harvest candidate queued in `adr-queue.json`), issue-sorter
(20 open issues / 0 open PRs, all labeled and healthy, zero triage debt), repo-cleaner
(full report at `.claude/ops/reports/2026-08-15T21-15-37Z-repo-cleaner.md`; PRs
#279/#278/#275 all `campaign_close.py`-clean incl. the authorkit gate; zero stale
branches/worktrees). Prior plan (2026-08-14 ~02:42Z) fully resolved — all three
entries closed per its own appended session notes; nothing carries forward except
standing rulings (see Not queued). Queue rebuilds 3 → 9.

**Blocked-by (#193):** no `Blocked-by:` line appears in any evidence this sweep —
issue-sorter read #265/#257/#282/#276/#283/#258 bodies in full and named no
dependency edge. Ordering below is pure class ranking + the authorkit lens.

## Human-decision call-outs — nothing below executes autonomously next sweep

1. **adr-0012 harvest confirm** (entry 3) — one AskUserQuestion round; only Kim
   confirms before `/make-pack` touches `who-ships-what.md`.
2. **#276 routing** (entry 2) — Kim picks solo-direct vs. next mobilize batch.
3. **Ops commit** (entry 1) — human-run if the dispatching session lacks Bash.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Read `git status --porcelain` first, then stage exactly
  `git add .claude/ops/plan.md .claude/ops/adr-checkpoint.json
  .claude/ops/adr-queue.json .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-15T21-15-37Z-repo-cleaner.md`, read the status
  output, commit as a separate step (gate ≠ commit), push. All five paths are this
  firing's delta (applied by chore-lead per the write-sandbox contract). Never
  `git add -A`.
- **Owner:** the dispatching session if Bash-capable, else human (Kim).
- **Evidence:** chore-lead applied all four seat payloads + this plan rewrite;
  repo-cleaner confirms main otherwise clean and in sync.
- **Size:** ~2 min.

(No other class-1 work: repo-cleaner verified all three merged PRs' remote branches
already gone — cache-prune only, nothing left to mutate.)

**Class 2 — items blocking other work:**

### 2. #276 — naming-grammar PostToolUse hook blind to EnterWorktree sessions (bug, major)
- **Action:** Fix the hook so it validates the session's actual checkout, not the
  main one — EnterWorktree sessions currently bypass naming-grammar enforcement
  entirely. Proven live during the attention-audit build (PR #275). Blocks safe
  worktree-based hardening work generally (issue-sorter's judgment — no literal
  `Blocked-by:` edge), which is why it leads every other work item this cycle.
  Route as a `/mobilize-chores` build item or a solo-direct bug fix — Kim's call
  (call-out 2).
- **Owner:** build seat via teamwork `/mobilize-chores` (Kim's batched confirm),
  or Kim solo-direct.
- **Evidence:** issue-sorter this sweep — bug + major labels, body read in full,
  named HIGHEST-relevance item in the 20-issue queue.
- **Size:** hours.

**Class 3 — human decisions:**

### 3. Confirm or reject the adr-0012 harvest candidate
- **Action:** One AskUserQuestion round on the single pending candidate in
  `adr-queue.json`: extend `harness/skills/big-change-git-rules/references/`
  `who-ships-what.md`, whose "who is allowed to merge" fact still reads as an
  absolute human-only rule with no ADR-0012 quick-build exception noted. If
  confirmed, `/make-pack` extends the pack (extend-in-place, not a new file);
  target-file placement (who-ships-what.md vs. merge-semantics.md) is
  decision-watcher's judgment — Kim may override at the gate. Run via the next
  interactive decision-watcher firing, or directly: `adr_queue.py pending`.
- **Owner:** human (Kim) — the confirm; then `/make-pack` executes.
- **Evidence:** decision-watcher this sweep — adr-0012 ratified (PR #248, merged
  2026-08-14), mechanism already threaded into teamwork's four artifacts, grep
  confirmed zero QB/auto-merge/quick-build hits in big-change-git-rules.
- **Size:** ~2 min (confirm); ~30–60 min (the harvest edit + checker pass).

**Class 4 — hygiene debt (authorkit-weighted first):**

### 4. #283 — model pins missing on naming-audit-agent and bloat-audit-agent (task, small)
- **Action:** Pin models on both authorkit agents — the A7 defect class (PR #126's
  pattern, `model: inherit` letting Fable dispatch Fable). Direct authorkit-agent
  hardening; natural batch-mate for entry 2's mobilize round.
- **Owner:** build seat via `/mobilize-chores`.
- **Evidence:** issue-sorter this sweep — task + small, body read in full.
- **Size:** ~30 min.

### 5. #282 — fence the three remaining baseline routing-collision pairs (task, big)
- **Action:** Close reciprocal description fences on the three collision pairs, one
  of which is harness `naming-rules` ↔ authorkit `naming-conventions`. Description
  edits ⇒ same-change `evals.json` updates + `/check-routing` per invariant.
- **Owner:** build seat via `/mobilize-chores`.
- **Evidence:** issue-sorter this sweep — task + big, body read in full.
- **Size:** hours.

### 6. #280 — centralize two description-boilerplate families
- **Action:** De-duplicate the `ops-write-sandbox-rules` and plan-plugin-split
  NOT-clause boilerplate families across descriptions. Kind/size labels not
  restated in this sweep's evidence (repo-cleaner surfaced it for visibility only)
  — take sizing from the issue's own labels at pickup.
- **Owner:** build seat via `/mobilize-chores`.
- **Evidence:** repo-cleaner this sweep — named in the authorkit-relevant
  visibility list; issue-sorter confirms it labeled and healthy (all 20 are).
- **Size:** per its own labels (not in evidence this sweep — est. small-to-medium).

### 7. #257 — authorkit-relevant open item, verified well-formed
- **Action:** Include in the next mobilize round's candidate set. Spot-checked
  directly by issue-sorter (well-formed, no unresolved placeholders — the earlier
  repair holds); body detail beyond that not carried in this sweep's evidence.
- **Owner:** build seat via `/mobilize-chores`.
- **Evidence:** issue-sorter (spot-check) + repo-cleaner (visibility list), this
  sweep.
- **Size:** per its own labels (not in evidence this sweep).

### 8. #258 — bloat-audit sweep of the four never-audited plugins (task, small) — DEFERRED BY RULING
- **Action:** Run authorkit's `/bloat-audit` over screens/design/agent-protocols/llm
  — in a FUTURE mobilize round. Kim's explicit 2026-08-15 ruling: defer; recorded
  here so it stops resurfacing as a question. Do not start this cycle.
- **Owner:** build seat via a future `/mobilize-chores` round (Kim batches it in).
- **Evidence:** issue-sorter this sweep — task + small, ruling cited in its report.
- **Size:** ~30–60 min when it runs.

### 9. Remaining 14 open issues — healthy labeled backlog
- **Action:** #256, #260, #262, #265, #266, #267, #268, #269, #271, #272, #273,
  #274, #277, #281 — all correctly labeled (kind + size/severity), zero triage
  debt, none stuck or held. Outside this sweep's authorkit lens; drain via future
  `/mobilize-chores` rounds in normal priority order. No per-item entry owed until
  a sweep's lens or a `Blocked-by:` edge elevates one.
- **Owner:** Kim batches into mobilize rounds; issue-sorter re-triages each sweep.
- **Evidence:** issue-sorter this sweep — full 20-issue enumeration, all labeled,
  held-items.md empty, no needs-triage-approval.
- **Size:** n/a (tracking entry; each item sized by its own label at pickup).

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PR estate:** zero open; #279/#278/#275 MERGED, `campaign_close.py`-clean
  (authorkit gate clean on #275), remote branches verified gone.
- **Worktrees/branches:** one worktree (primary), no stale locals; 3 stale
  remote-tracking refs pruned (metadata only).
- **ADR-0005 ticket claims:** zero open (#207, #189 both now CLOSED — the prior
  standing exception has fully retired).
- **`.gitignore` G1 WARNs** (`dist/`, `harness-audit-*/`): repeat, reviewed and
  accepted every firing. Recorded judgment, not a task.
- **Friendlies/held items:** all 20 issues by kimgranlund (allow-listed);
  held-items.md empty; no unknown authors.
- **Root entry-file freshness CI gate:** deliberate NO (Kim, 2026-08-15) — manual
  sweep is the accepted mechanism; do not re-propose (ruling carried from prior
  plan).
- **Checkpoint-bypass:** accepted one-off (Kim, 2026-08-14); re-litigate only on
  recurrence (ruling carried).

## Resolved since the prior plan (2026-08-14, ~02:42Z sweep)

- Prior entry 1 (commit ops artifacts) — DONE, committed 7dbacf5 (session note).
- Prior entry 2 (#221 scheduling) — RESOLVED: issue closed; the prior 3-open-issue
  state fully cleared between sweeps.
- Prior entry 3 (ADR-0011 chain step 6) — VERIFIED LANDED (validate.py
  exemption_burndown, session verification 2026-08-14).
- New since prior plan: ADR-0012 ratified (PR #248); issue queue grew to 20 open
  (all healthy); PRs #275/#278/#279 merged and reaped clean; adr-0012 harvest
  candidate queued (entry 3).
