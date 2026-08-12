# .claude/ops/plan.md
# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-10 (23:50Z window close),
main @ eb3a27f, in sync with origin/main, working tree clean. Evidence: the three seat
reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner — none
UNMEASURED), plus the prior plan (2026-08-10, 06:23:59Z sweep) read as carry-forward
source. Nothing refetched. Six prior entries RESOLVED, two carried forward, four new
(including the recurring per-firing artifact commit).

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Commit this firing's applied ops artifacts to main — RESOLVED 2026-08-10 (between firings)
- **Movement:** committed as `1b7ccc4` ("ops: sweep #27") and pushed, exactly the five named paths.
- **Action (as queued):** Stage exactly the five ops paths —
  `git add .claude/ops/plan.md .claude/ops/watch-checkpoint.json
  .claude/ops/adr-checkpoint.json .claude/ops/adr-queue.json
  .claude/ops/reports/2026-08-10T23-50-17Z-repo-cleaner.md` — read the status output,
  then commit as a separate step (gate ≠ commit), then push. Safe as a plain sequence
  this firing: the tree was clean before the sweep and main is in sync with origin, so
  no quarantine or `sync_main.py` step is needed.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** repo-cleaner this sweep — main @ eb3a27f in sync, tree clean;
  chore-lead — all four seat payloads applied to disk this sweep (checkpoints, queue,
  report), plus this plan rewrite.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 2. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 9th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify the schedule
  is still armed — sweep dispatches advance `watch-checkpoint.json` themselves, so a
  checkpoint gap cannot prove the routine dead. Ninth consecutive plan appearance: if
  this is a deliberate no, record that instead so this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the prior plan's entry 4; no seat this sweep reported
  the prompt fixed (issue-sorter again ran as a sweep dispatch, not from the routine).
  Blocks unattended issue intake between sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 3. Batched confirm on the adr-0010 harvest candidate — one queue row, TWO separable asks (NEW)
- **Action:** Run the save-lessons Phase 3 confirm over the single pending
  `adr-queue.json` row for adr-0010, treating it as two independent accept/override/skip
  decisions (the merged row is a schema accommodation, not one ask): (a) a worked
  cross-plugin-boundary example of naming-rules' test-5 loud-contrast rule — ADR-0010's
  rejected "chores-lead" vs shipped "chore-lead"; (b) the surplus-side anti-matrix rule
  for plan-plugin-split — two seats built for the same job, per ADR-0010's Rejected
  Alternative #2. On accept: author inline via save-lessons Phase 4 as reference-file
  extends (escalate to `/make-pack` only if scope grows), run `release_gate.py harness`,
  land, then `python3 harness/scripts/adr_queue.py clear --ids adr-0010:harvest`. This
  confirm doubles as the second reader the solo firing lacked.
- **Owner:** human (the confirm and any override); the accepted halves then author via
  save-lessons Phase 4 in a normal session.
- **Evidence:** decision-watcher this sweep — both gaps grep-verified as zero-hit in the
  corpus; ADR text at `.claude/docs/adr/0010-generalize-feature-lead-to-build-lead.md:17-18,54-59`;
  the already-harvested rename mechanics deliberately NOT re-queued
  (`harness/skills/agent-writing-rules/SKILL.md:57` citation confirmed).
- **Size:** ~5 min (confirm) + ~30–45 min (authoring + gate, if accepted).

### 4. Decide the build route for the four open issues — #157 first (NEW, succeeds prior entry 5) — RESOLVED 2026-08-11 (between firings)
- **Movement:** routed through `/mobilize-chores` with a batched confirm, all four dispatched to
  `build-lead`: #167 built + closed (docs 1.4.3), #156 fixed + closed (harness 3.1.18), #157
  root-caused + fixed + closed (harness 3.1.19 — shared mechanism with #156), #151 correctly
  SKIPPED (its own body defers it until a real feature ticket exists; stays open by design).
- **Action (as queued):** The full open roster is #167, #157, #156, #151 — all unassigned, no stale
  claims. Decide: batch through `/mobilize-chores`, pick up individually, or defer with
  a dated note. Rank #157 first (bug + major: dispatched seats' SendMessage reports
  default to the root session instead of chore-lead — systematic ~100% across 3+ sweeps,
  a real recurring cost to every future sweep; workaround exists, hence major not
  blocker). #156 is bug + minor (teammate_id labeling/documentation gap, same dispatch
  mechanics). #151 is the last survivor of the prior #149–#152 set (its three siblings
  closed between firings). #167's content is not in this sweep's evidence — read it
  before routing it.
- **Owner:** human (the confirm gate is the human's by design).
- **Evidence:** issue-sorter this sweep — #157 and #156 resumed and now fully labeled
  (https://github.com/kimgranlund/claude-plugins/issues/157, /156); repo-cleaner —
  open-issue inventory in `.claude/ops/reports/2026-08-10T23-50-17Z-repo-cleaner.md`.
- **Size:** ~10 min (the decision incl. reading #167; builds sized by their tickets).

### 5. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  Fold into the same sitting as entry 3 — one save-lessons pass can settle both. Note
  the prior plan's "a no fully clears the decision-watcher surface" no longer holds:
  the queue now carries the adr-0010 row regardless.
- **Owner:** human (yes → save-lessons/`/make-pack` route; no → done, no record change).
- **Evidence:** carry-forward from the prior plan's entry 7; decision-watcher this sweep
  judged only the new adr-0010 delta, leaving the adr-0009 call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 6. Configure org Issue Types, or record a deliberate no (NEW)
- **Action:** `gh issue edit <id> --type Bug` failed identically on both resumes this
  firing — the org has no Issue Types schema configured, so every future mint/resume
  will retry and fail until it is. Either configure Issue Types at the org level on
  GitHub (Issue Types are org-level config — see harness `github-facts`,
  `references/issue-types-and-labels.md`), or record a deliberate labels-only decision
  so issue-sorter can stop attempting the native call. Cosmetic only — labels already
  carry kind + severity.
- **Owner:** human (org admin either way; the labels-only decision would then drive a
  small issue-sorter agent-file edit through the normal gate).
- **Evidence:** issue-sorter this sweep — identical `--type` failures on #156 and #157,
  labels applied and verified as the fallback.
- **Size:** ~10 min (configure) or ~2 min (record the no).

## Not queued (checked, found clean this sweep)

- PRs: 105 total, all 105 MERGED, zero open, zero surviving remote branches — no reap
  candidates (repo-cleaner).
- Local branches/worktrees: clean — the prior plan's `fix/154-...` orphan is gone, no
  successors (repo-cleaner).
- Issue-intake trust: every discovered item by the trusted author, nothing newly held,
  0 `needs-triage-approval` repo-wide; `friendlies.json` and `held-items.md` unchanged
  (issue-sorter).
- ADR-0010's rename mechanics and three-piece agent shape: already harvested — correctly
  NOT re-queued (decision-watcher).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`): long-standing,
  on-demand-generated paths, deliberately kept, no edit (repo-cleaner).

## Resolved since the prior plan (2026-08-10, 06:23:59Z sweep)

- Prior entry 1 (delete merged local `fix/154-...`) — RESOLVED: repo-cleaner reports the
  previously-orphaned local branch already cleaned up; zero orphans this firing.
- Prior entry 2 (commit the 06:23Z firing's artifacts) — RESOLVED: tree clean, main
  @ eb3a27f in sync; those ops paths sit committed.
- Prior entry 3 (disposition dirty main + sync) — RESOLVED: repo-cleaner explicitly
  names the dirty tree resolved; the docs/teamwork authoring landed within the
  PR #158–#170 window.
- Prior entry 5 (route #149–#152) — MOSTLY RESOLVED: #149, #150, #152 no longer in the
  open roster; #151 carries into entry 4.
- Prior entry 6 (apply/rescind the MCP offer) — RESOLVED: issue-sorter confirmed
  `.mcp.json` matches the recorded accepted decision.
- Prior entry 8 (disposition #139) — RESOLVED: closed between firings; absent from the
  open roster.
- Prior entry 9 (report-filename suffix) — RESOLVED: repo-cleaner itself computed the
  seat-suffixed path this firing (`2026-08-10T23-50-17Z-repo-cleaner.md`); note the
  collision case itself went untested (single report this firing).
- Prior entries 4 and 7 — carried forward as entries 2 and 5.
