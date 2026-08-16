# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-16 ~01:12Z window (UTC),
main at `0dd62b6`, in sync with origin, no scope lens this sweep. Evidence: all three
seat reports attached (none UNMEASURED) — decision-watcher (adr-0013 new, one narrow
Consequences-bullet supersession of adr-0012; TWO candidates queued in `adr-queue.json`),
issue-sorter (12 open issues / 0 open PRs, all labeled, zero triage debt, 20 issues +
15 PRs closed in-window all by trusted author), repo-cleaner (abbreviated report at
`.claude/ops/reports/2026-08-16T01-12-00Z-repo-cleaner.md`; zero stray branches,
worktrees, or stale claims; nothing executed, nothing proposed). Prior plan
(2026-08-15 ~21:15Z) is 7/9 resolved between sweeps — the Batch C/D/E mobilize
campaign drained #276/#283/#282/#280/#257 and PRs #288/#291/#292 landed; the executed
adr-0012 harvest was cleared from the queue (commit `c2d248a`). Carried forward: the
#258 deferred-by-ruling entry and the standing rulings (see Not queued). Queue
rebuilds 9 → 4.

**Blocked-by (#193):** no `Blocked-by:` line appears in any evidence this sweep —
issue-sorter names zero dependency edges across the 12 open issues. Ordering below is
pure class ranking.

**In-flight context (not a queue item):** `.claude/ops/charter-batch-cde.md` is the
LIVE coordination record for the in-progress Batch C/D/E mobilize campaign (Batch C
closed, Batch D in progress). It stays untracked and untouched; the campaign owns its
lifecycle. Entry 1's commit pathspec deliberately excludes it.

## Human-decision call-outs — nothing below executes autonomously next sweep

1. **ADR-queue batched confirm** (entry 2) — one AskUserQuestion round covering BOTH
   pending candidates; only Kim confirms before anything touches
   `who-ships-what.md`.
2. **Ops commit** (entry 1) — human-run if the dispatching session lacks Bash.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Read `git status --porcelain` first, then stage exactly
  `git add .claude/ops/plan.md .claude/ops/adr-checkpoint.json
  .claude/ops/adr-queue.json .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-16T01-12-00Z-repo-cleaner.md`, read the status
  output, commit as a separate step (gate ≠ commit), push. These five paths are this
  firing's whole delta (seat payloads applied by chore-lead per the write-sandbox
  contract). Never `git add -A` — and never sweep in `charter-batch-cde.md` (live
  campaign record, see In-flight context above).
- **Owner:** the dispatching session if Bash-capable, else human (Kim).
- **Evidence:** `git status --porcelain` at plan time shows exactly the three
  modified state files + the one untracked report (+ the excluded charter file);
  repo-cleaner confirms main otherwise clean and in sync at `0dd62b6`.
- **Size:** ~2 min.

(No other class-1 work: zero open PRs, zero surviving remote branches, zero stale
worktrees — repo-cleaner verified all clean; nothing left to mutate.)

**Class 2 — items blocking other work:**

(None this sweep. Prior entry #276 — the EnterWorktree naming-hook blindspot that led
the last plan — is CLOSED. No open item is named as blocking any other.)

**Class 3 — human decisions:**

### 2. Batched confirm of the two pending ADR-queue candidates (adr-0013 + adr-0012)
- **Action:** One AskUserQuestion round on both rows in `adr-queue.json`, surfaced
  via `adr_queue.py pending` in a session that HAS AskUserQuestion (decision-watcher
  deferred — its seat lacks the tool). The two candidates converge on one file and
  are almost certainly ONE edit:
  (a) **adr-0013 harvest** — extend
  `harness/skills/big-change-git-rules/references/who-ships-what.md` with the
  empirical finding: the auto-mode classifier denies the Agent tool call at
  dispatch-creation time the moment the sealed prompt carries
  `auto-merge: authorized` — earlier and stricter than ADR-0012 predicted.
  Dispatch-tier is verified; merge-tier (the `autoMode.allow` rule, commit
  `40dd5c3`) remains UNMEASURED and the harvested text must say so.
  (b) **adr-0012 stale citation** — the same file's lines 88–92 quote verbatim the
  exact Consequences bullet adr-0013 supersedes ("deployment prerequisite...
  theoretical pending that rule"); repair or retire the quote via save-lessons
  Phase 6 routing. Lines 38–81 (QB0–QB7 predicate) are unaffected — do not touch.
  If confirmed: `/make-pack` extend-in-place (or `/make-skill` if Kim's Phase 2
  pass judges otherwise), then a fresh-context checker pass per the semantic-edit
  invariant before the loop closes.
- **Owner:** human (Kim) — the confirm; then `/make-pack` executes the combined
  edit.
- **Evidence:** decision-watcher this sweep — adr-0013 ratified ~1h before the
  sweep (`0013-adr-0012-automode-allow-verification.md:44-58`); both candidates
  queued 2026-08-16T01:12:21Z, queue previously empty; stale-citation scope
  verified narrow (single bullet, every other ADR-0012 line stands).
- **Size:** ~2 min (confirm); ~30–60 min (the combined edit + checker pass).

**Class 4 — hygiene debt:**

### 3. #258 — bloat-audit sweep of the four never-audited plugins — DEFERRED BY RULING
- **Action:** Run authorkit's `/bloat-audit` over screens/design/agent-protocols/llm
  — in a FUTURE mobilize round. Kim's explicit 2026-08-15 ruling: defer; recorded
  here so it stops resurfacing as a question. Do not start this cycle.
- **Owner:** build seat via a future `/mobilize-chores` round (Kim batches it in).
- **Evidence:** still open in issue-sorter's 12-issue enumeration this sweep;
  ruling carried from the prior plan (task + small per its own labels).
- **Size:** ~30–60 min when it runs.

### 4. Remaining 11 open issues — healthy labeled backlog
- **Action:** #265, #266, #273, #274, #286, #293, #294, #295, #296, #297, #300 —
  every open issue carries a correct kind label, zero unlabeled findings, none held
  or stuck; #300 and #297 spot-checked well-formed. Drain via future
  `/mobilize-chores` rounds in normal priority order (the in-flight Batch C/D/E
  campaign is already consuming this backlog — 20 issues closed in-window). No
  per-item entry owed until a sweep lens or a `Blocked-by:` edge elevates one.
- **Owner:** Kim batches into mobilize rounds; issue-sorter re-triages each sweep.
- **Evidence:** issue-sorter this sweep — full 12-issue enumeration, backlog-only
  state matches expectation, held-items.md and friendlies.json unchanged.
- **Size:** n/a (tracking entry; each item sized by its own label at pickup).

## Not queued (checked, found clean or deliberately left — standing rulings carried)

- **PR estate:** zero open; all in-window PRs (15) MERGED clean; no surviving remote
  branches.
- **Worktrees/branches:** zero beyond main; zero stray locals or remotes.
- **ADR-0005 ticket claims:** zero — all 12 open issues have empty assignees.
- **`charter-batch-cde.md`:** live Batch C/D/E campaign record — in-flight context,
  not cruft, not this plan's to commit or clean (repo-cleaner concurs).
- **`.gitignore` G1 WARNs** (`dist/`, `harness-audit-*/`): same two repeats,
  on-demand-generated, reviewed and accepted every firing. Recorded judgment, not a
  task.
- **Friendlies/held items:** all in-window activity by kimgranlund (allow-listed);
  held-items.md unchanged, nothing held.
- **Root entry-file freshness CI gate:** deliberate NO (Kim, 2026-08-15) — do not
  re-propose (ruling carried).
- **Checkpoint-bypass:** accepted one-off (Kim, 2026-08-14); re-litigate only on
  recurrence (ruling carried).

## Resolved since the prior plan (2026-08-15, ~21:15Z sweep)

- Prior entry 1 (commit ops artifacts) — DONE (state files tracked and clean at this
  sweep's start).
- Prior entry 2 (#276 EnterWorktree hook blindspot) — CLOSED between sweeps.
- Prior entry 3 (adr-0012 harvest confirm) — EXECUTED and cleared from the queue
  (commit `c2d248a`); who-ships-what.md now carries the harvest — which is exactly
  where this sweep's new stale-citation candidate landed (entry 2b).
- Prior entries 4–7 (#283, #282, #280, #257) — all CLOSED (PRs #288/#291/#292
  among the 15 merged in-window).
- Prior entry 8 (#258) — carries forward as entry 3, ruling intact.
- Prior entry 9 (backlog tracking) — drained 20 → 12 open; rebuilt as entry 4.
- New since prior plan: ADR-0013 ratified (~1h pre-sweep), superseding one ADR-0012
  Consequences bullet; two fresh ADR-queue candidates (entry 2); Batch C/D/E
  mobilize campaign live (Batch C closed, Batch D in progress).
