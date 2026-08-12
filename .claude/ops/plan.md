# .claude/ops/plan.md
# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-12 (~13:56Z window close),
main clean and pushed — harness 3.1.22 / docs 1.4.4 / teamwork 2.7.3. Evidence: the three
seat reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner —
none UNMEASURED), plus the prior plan (2026-08-10, 23:50Z sweep) read as carry-forward
source. Nothing refetched. Five prior entries RESOLVED between firings, one carried
forward, four new (including the recurring per-firing artifact commit).

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's applied ops artifacts to main
- **Action:** Stage exactly the three ops paths this firing touched —
  `git add .claude/ops/plan.md .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-12T13-56-25Z-repo-cleaner.md` — read the status output,
  then commit as a separate step (gate ≠ commit), then push. decision-watcher had no
  payload this firing, so `adr-checkpoint.json`/`adr-queue.json` are untouched and stay
  out of the stage list. Safe as a plain sequence: the tree was clean and main pushed
  before the sweep, so no quarantine or `sync_main.py` step is needed.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** issue-sorter this sweep — watch-checkpoint payload already applied by
  chore-lead (advanced to 2026-08-12T13:54:11Z); repo-cleaner — report payload already
  applied to `.claude/ops/reports/2026-08-12T13-56-25Z-repo-cleaner.md`, working tree
  clean before the sweep; plus this plan rewrite.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 2. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 10th appearance) — RESOLVED 2026-08-12: deliberate NO (between firings)
- **Movement:** Kim ruled deliberate-no in the 2026-08-12 mobilize-chores confirm round: sweeps
  already run issue-sorter on demand and advance `watch-checkpoint.json` themselves; the
  unattended between-sweep intake gap is accepted. The stale routine is abandoned, not repaired —
  this entry retires permanently after ten appearances.
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify the schedule
  is still armed — sweep dispatches advance `watch-checkpoint.json` themselves, so a
  checkpoint gap cannot prove the routine dead. TENTH consecutive plan appearance: if
  this is a deliberate no, record that instead so this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the prior plan's entry 2; no seat this sweep reported
  the prompt fixed (issue-sorter again ran as a sweep dispatch, not from the routine);
  repo-cleaner explicitly confirmed this item is outside its charter and still standing.
  Blocks unattended issue intake between sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 3. Decide evals ownership for big-change-git-rules (#172) — a ruling, not routine cleanup (NEW)
- **Action:** #172's own title names an ownership DECISION for big-change-git-rules'
  evals, not a mechanical fix — settle who owns that suite first, then route the
  resulting edit through the normal small-task path. Its body is not in this sweep's
  evidence beyond label/author metadata — read it before ruling. Ranked ahead of the
  other four new issues because the ruling may shape how the check-routing follow-ups
  (#173–#175) land.
- **Owner:** human (the ruling); the resulting task then routes like entry 4's.
- **Evidence:** issue-sorter this sweep — #172 filed by kimgranlund after the dispatch
  brief was written, labeled task + size:small at creation, unassigned; repo-cleaner —
  read for classification only, no stale claims.
- **Size:** ~10 min (the ruling); the follow-on task is size:small by label.

### 4. Route the four remaining new issues — #171, #173, #174, #175 (NEW)
- **Action:** All task + size:small, human-filed, correctly labeled at creation,
  unassigned, no stale claims. Decide: batch through `/mobilize-chores`, pick up
  individually, or defer with a dated note. #171 is the rename-sweep counterexample
  guard; #173/#174/#175 are check-routing-report follow-ups and a natural batch. Bodies
  are not in this sweep's evidence — read before routing.
- **Owner:** human (the confirm gate is the human's by design).
- **Evidence:** issue-sorter this sweep — five new open issues verified and labeled,
  zero open PRs, zero held items; the dispatch brief undercounted the open set by four
  (#172–#175 postdate it), caught and corrected by the seat.
- **Size:** ~10 min (the routing decision); builds sized by their tickets.

### 5. Open question: is a broader /clean-repo corpus/automation sweep warranted? (NEW) — RESOLVED 2026-08-12: deliberate NO (between firings)
- **Movement:** Kim ruled no in the 2026-08-12 mobilize-chores confirm round — no drift evidence
  anywhere (repo-cleaner's own 7-plugin README/ledger spot-check clean), and the same day's
  repo-docs sweep had just repaired the root-level surfaces (seven-count, CHANGELOG catch-up,
  Map rows). Question retires with this dated record.
- **Action:** Human yes/no. repo-cleaner's charter is git-surface + ADR-0005 claim
  hygiene only; the broader "duplicated instruction trees / stale corpus / dead
  automation" sweep was NOT attempted this firing or any prior one. Yes → dispatch
  `/clean-repo` separately; no → record a dated deliberate-no so this question retires.
  Nothing in this sweep's evidence indicates drift (README/ledger spot-check across all
  7 plugins came back clean) — this queues the question, not a presumed sweep.
- **Owner:** human (the yes/no; a yes then dispatches `/clean-repo`).
- **Evidence:** repo-cleaner this sweep — open question (1) in its report,
  `.claude/ops/reports/2026-08-12T13-56-25Z-repo-cleaner.md`.
- **Size:** ~2 min (the decision); the sweep itself is hours if run.

**Class 4 — hygiene debt:**

(none this firing — see Not queued.)

## Not queued (checked, found clean this sweep)

- `.gitignore` `dist/` WARN: matches nothing in the tree, reviewed by repo-cleaner and
  deliberately NOT actioned — `dist/` is generated on demand by
  `release_gate.py --package`. Recorded judgment, not a task.
- ADR corpus quiet: 10/10 files unchanged against `.claude/ops/adr-checkpoint.json`,
  pending queue empty, no payload; adr-0010's harvest and the 0006/0007/0009 verification
  already closed out in prior firings (decision-watcher).
- PRs: 105/105 MERGED with remote branches already deleted, zero open — no reap
  candidates; working tree clean, no dirty main, no host reap script (repo-cleaner).
- Issue-intake trust: all five new issues by the trusted author, already correctly
  labeled at creation, zero held / needs-triage-approval repo-wide; watch-checkpoint
  payload already applied by chore-lead (issue-sorter).
- README/ledger spot-check across all 7 plugins: no drift (repo-cleaner).
- Process note: dispatch briefs are snapshots, not inventories — this one undercounted
  the open set by four issues filed after it was written; the seat caught it. No action.

## Resolved since the prior plan (2026-08-10, 23:50Z sweep)

- Prior entry 1 (commit the 23:50Z firing's artifacts) — RESOLVED 2026-08-10: committed
  as `1b7ccc4` ("ops: sweep #27") and pushed, exactly the five named paths.
- Prior entry 3 (adr-0010 harvest batched confirm) — RESOLVED 2026-08-12: both asks
  confirmed ACCEPT by Kim in one batched round; landed in naming-rules (test-5 row
  rewrite) and plan-plugin-split (anti-matrix surplus side); queue row cleared, gates
  green.
- Prior entry 4 (route #167/#157/#156/#151) — RESOLVED 2026-08-11: routed through
  `/mobilize-chores`; #167 built + closed (docs 1.4.3), #156 fixed + closed (harness
  3.1.18), #157 root-caused + closed (harness 3.1.19), #151 correctly SKIPPED then —
  and now closed too (issue-sorter this sweep confirms #151/#156/#157/#167 all closed).
- Prior entry 5 (adr-0009 harvest sanity check) — RESOLVED 2026-08-12: Kim ruled NO —
  the not-queuing call was right; entry retired permanently.
- Prior entry 6 (org Issue Types) — RESOLVED 2026-08-12: Kim ruled labels-only;
  issue-sorter's `--type` attempt retired from the agent body with the ruling dated in
  place and the reversal path named.
- Prior entry 2 — carried forward as entry 2 (10th appearance).
