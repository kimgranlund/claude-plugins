# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-14 ~02:42Z window (UTC),
main at `b4d1137`, tree clean except this sweep's own ops writes. Evidence: the three
seat reports attached to this dispatch (decision-watcher: sole delta adr-0011
proposed→accepted @ `65efbf2`, deliverables verified landed, queue empty; issue-sorter:
3 open issues / 0 open PRs, no state mutation; repo-cleaner: full report at
`.claude/ops/reports/2026-08-14T02-42-04Z-repo-cleaner.md`), with the prior plan
(2026-08-14 ~00:03Z) plus its appended session rulings as carry-forward source.
Clean, uneventful sweep: since the prior plan, ADR-0011 ratified and its whole
deliverable chain landed via #197 / merged PR #222 (branch 404-verified gone), the
orphaned worktree was removed, and the checkpoint-bypass question was ruled. Six of
the prior eight entries close below; the queue shrinks 8 → 3.

## Human-decision call-outs — nothing below executes autonomously next sweep

1. **#221 scheduling** (entry 2) — unassigned backlog task; only Kim assigns or
   batches it into a mobilize round.
2. **Ops commit** (entry 1) — human-run if the dispatching session lacks Bash.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Read `git status --porcelain` first, then stage exactly
  `git add .claude/ops/plan.md .claude/ops/adr-checkpoint.json
  .claude/ops/reports/2026-08-14T02-42-04Z-repo-cleaner.md`, read the status output,
  commit as a separate step (gate ≠ commit), push. `adr-checkpoint.json` IS part of
  this firing's delta (adr-0011 hash + status advanced, applied by chore-lead);
  issue-sorter reports no `watch-checkpoint.json` mutation — confirm via the status
  read, stage only what changed. Never `git add -A`.
- **Owner:** the dispatching session if Bash-capable, else human (Kim). Carried note:
  chore-lead's own grant is Read/Write/Task — no Bash/git — so this routes past it.
- **Evidence:** seat reports this sweep — chore-lead applied the checkpoint delta,
  repo-cleaner wrote a new report file, this plan rewrite once applied.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

(none this firing — the ADR-0011 chain that occupied this class ratified and landed
via #197 / PR #222.)

**Class 3 — human decisions:**

### 2. Schedule or assign #221 — watch-adrs supersession gap
- **Action:** #221 (task, backlog, size:small, unassigned) is the only open work item
  with no owner. Kim decides: assign it, fold it into the next mobilize batch, or
  leave it in backlog with that choice recorded here so it stops resurfacing as a
  question. No urgency signal from any seat — it blocks nothing.
- **Owner:** human (Kim) — assignment is the decision; execution then routes to a
  build seat under the normal batched confirm.
- **Evidence:** issue-sorter this sweep — #221 open, unassigned, `backlog` +
  `size:small`, matches expected state; repo-cleaner independently noted it unclaimed
  and routed it to triage.
- **Size:** ~2 min (the ruling); the task itself is size:small per its label.

**Class 4 — hygiene debt:**

### 3. Close out chain step 6 (exemption burn-down metric) — status UNMEASURED
- **Action:** The prior plan's entry 7 tracked ADR-0011 chain steps 2/3/4/6.
  Steps 2/3/4 (estate manifest, validator, naming-rules supersession note) are
  verified landed via PR #222 per decision-watcher. Step 6 (the exemption burn-down
  metric) was NOT in that verified list — UNMEASURED this sweep, not confirmed
  landed, not confirmed missing. Check PR #222's diff (or the spec's step-6 section)
  once; if landed, this entry closes on sight, if not, file its record via the
  file-task path.
- **Owner:** human (Kim) or the next sweep's decision-watcher firing with step-6
  named in its dispatch.
- **Evidence:** decision-watcher this sweep enumerated four landed deliverables;
  step 6 absent from the enumeration. Carried residue of prior entry 7, all other
  halves of which resolved.
- **Size:** ~5 min (the check); filing, if needed, ~10 min.

## Not queued (checked, found clean or deliberately left)

- **#207 / #189:** deliberately-open CLI-level tracking records per the standing
  ruling; estate-side work marked complete in latest comments, both healthy per
  issue-sorter. Untouched.
- **PR estate:** zero open PRs; #219, #220, #222 (new since prior plan) plus
  #209–#218 all MERGED with remote branches independently 404-verified. Nothing for
  `campaign_close.py`.
- **Orphaned worktree (prior entry 1):** confirmed resolved between firings —
  one worktree (primary), one local branch (main), one remote (origin/main).
- **Main:** clean, in sync with origin @ `b4d1137` — no `sync_main.py`.
- **`.gitignore` G1 WARNs** (`dist/`, `harness-audit-*/`): repeat, reviewed and
  accepted every firing. Recorded judgment, not a task.
- **Friendlies allowlist:** current — single author kimgranlund, allow-listed; no
  `needs-triage-approval` items.
- **decision-watcher harvest queue (`adr-queue.json`):** empty and CORRECTLY so —
  ADR-0011's ratification fired the impact detector, but its deliverable is already
  executed (PR #222) and D9 rules the spec non-routable; no candidate owed.
- **Checkpoint-bypass (prior entry 8):** ruled ACCEPTED AS ONE-OFF by Kim
  (2026-08-14 mobilize round); re-litigate only on recurrence. Recorded, closed.

## Resolved since the prior plan (2026-08-14, ~00:03Z sweep)

- Prior entry 1 (orphaned worktree + branch) — DONE per session ruling; repo-cleaner
  independently confirmed the estate clean this firing.
- Prior entry 2 (commit that firing's ops artifacts) — RESOLVED: main clean/in-sync;
  only this firing's own writes remain (entry 1 above).
- Prior entry 3 (ADR-0011 stale spec path) — DONE at `6bcbfbe` while still proposed.
- Prior entry 4 (ratify ADR-0011 + supersedes wiring) — RESOLVED: accepted at
  `65efbf2`; naming-rules carries the dated supersession note (verified by
  decision-watcher).
- Prior entry 5 (estate `naming.manifest.json`) — RESOLVED: exists, landed via
  #197 / PR #222 (verified by decision-watcher).
- Prior entry 6 (#197 next state) — RESOLVED: Kim mobilized it; campaign executed
  and merged as PR #222; #197 no longer open.
- Prior entry 7 (chain-step records) — MOSTLY RESOLVED: steps 2/3/4 landed inside
  PR #222 without separate records (acceptable — the work is the record's purpose);
  step 6 carried as entry 3 above, UNMEASURED.
- Prior entry 8 (checkpoint-bypass ruling) — RESOLVED: accepted one-off.
- New since prior plan: issue #221 opened (queued as entry 2); PRs #219/#220/#222
  merged and reaped clean.

## Session verification appended (2026-08-14, mobilize round)

- Entry 3 (ADR-0011 chain step 6): VERIFIED LANDED — validate.py emits exemption_burndown {count, notes} in --json output (validate.py:458), per-run count in human output (line 515), documented in authorkit/README.md. No gap.
- Entry 1 (ops artifacts): DONE — committed 7dbacf5.

## Ruling appended (2026-08-15, Kim)

- Root entry-file freshness (README/CHANGELOG/CONTRIBUTING plugin counts and rows): **deliberate NO to a CI gate** — the periodic manual sweep is the accepted mechanism. Drift was repaired 642c63f (seven→eight catch-up); do not re-propose a root-docs gate check.
