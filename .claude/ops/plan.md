# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-10 (06:23:59Z window close),
local main @ cf8acb7 (origin @ 0827b72 — 2 ahead, PR #155). Evidence: the three seat
reports attached to this dispatch (decision-watcher, issue-sorter, repo-cleaner — none
UNMEASURED), plus the prior plan (2026-08-09, 13:44Z sweep) read as carry-forward source.
Nothing refetched. Two prior entries RESOLVED, four carried forward, three new (plus the
recurring per-firing artifact commit).

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Delete the merged local branch `fix/154-chore-lead-dispatch-namespace`
- **Action:** `git branch -d fix/154-chore-lead-dispatch-namespace` from the main
  worktree at /Users/kimba/Projects/nonoun/plugins — AFTER entry 3's sync, because local
  main (cf8acb7) does not yet contain PR #155's merge commit, so `-d`'s own merged-check
  will refuse until main catches up. That refusal is a second gate, not a bug; do not
  escalate to `-D`.
- **Owner:** chore-lead (the dispatching session), else human — repo-cleaner is
  propose-only here by contract (no host-repo reap script exists; re-searched all
  CLAUDE.md/README.md + package.json this firing).
- **Evidence:** repo-cleaner this sweep — verified merged via PR #155 (MERGED, merge
  commit = origin/main HEAD), remote branch already deleted and reverified gone. Same
  class as the three prior firings' now-resolved branch reaps.
- **Size:** ~1 min (after entry 3).

### 2. Commit this firing's applied ops artifacts to main
- **Action:** Stage ONLY the ops paths — `git add .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-10T06-23-59Z-issue-sorter.md
  .claude/ops/reports/2026-08-10T06-23-59Z-repo-cleaner.md .claude/ops/plan.md` — the
  working tree also carries 9 files of unrelated live authoring (entry 3); a bare
  `git add -A` would sweep that in. Read the status output first, then commit as a
  separate step (gate ≠ commit). The adr payloads are byte-identical to committed state
  (decision-watcher: no-op) — nothing to stage there. Push only after entry 3's sync —
  local main is 2 behind and the push will be rejected until then.
- **Owner:** chore-lead (the dispatching session), else human.
- **Evidence:** issue-sorter — watch-checkpoint.json advanced to 2026-08-10T06:23:59Z,
  applied; chore-lead notes — both seat reports written (seat-name-suffixed) and applied
  to disk; this plan.md rewritten by this dispatch.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 3. Disposition the dirty main, then sync the 2-behind checkout (NEW)
- **Action:** Human reviews the 9 uncommitted files (163+/75−) across docs/ (plugin.json,
  README.md, file-bug/file-feature/file-task SKILL.md) and teamwork/ (plugin.json,
  README.md, build-feature/dispatch-feature SKILL.md) — sampled diff reads as live
  in-progress authoring (new `context: fork` frontmatter, rewritten clarifying-questions
  section), so the owning session should commit it to a campaign branch or stash it
  deliberately; then run `sync_main.py` to pull PR #155's two commits (it quarantines any
  remaining dirt as a named stash, `--ff-only` pulls, reverifies HEAD by SHA). Blocks
  entry 1 (branch `-d` refuses against stale main) and the push in entry 2.
- **Owner:** human (repo-cleaner explicitly withheld `sync_main.py` this firing —
  substantive uncommitted work must not be auto-quarantined without review).
- **Evidence:** repo-cleaner this sweep — local main @ cf8acb7, origin @ 0827b72, tree
  DIRTY with the file list above; "reads as live authoring, not cruft."
- **Size:** ~15 min (review + disposition) + ~2 min (sync).

### 4. Fix the stale cloud-routine prompt AND verify the schedule is armed (carry-forward, 8th appearance)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and verify the schedule
  is still armed — sweep dispatches advance `watch-checkpoint.json` themselves, so a
  checkpoint gap cannot prove the routine dead. Eighth consecutive plan appearance: if
  this is a deliberate no, record that instead so this entry can retire.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the prior plan's entry 3; no seat this sweep reported
  the prompt fixed (issue-sorter ran on-demand, not from the routine). Blocks unattended
  issue intake between sweeps while dead.
- **Size:** ~5–10 min.

**Class 3 — human decisions:**

### 5. Decide the build route for tickets #149–#152 (NEW)
- **Action:** Four fully-formed, size:small, kind-labeled task issues sit open,
  unassigned, zero comments (created 2026-08-09 by a prior capture-skill pass). Decide:
  batch them through `/mobilize-chores` (the named route for driving buildable tickets
  to build, one confirm), pick them up individually, or explicitly defer with a note.
  Precedent: prior plan's #135 entry resolved exactly this way (built as PR #148).
- **Owner:** human (the confirm gate is the human's by design).
- **Evidence:** issue-sorter + repo-cleaner this sweep — #149, #150, #151, #152 all open,
  triage-complete, unassigned, no stale claims.
- **Size:** ~5 min (the decision; builds are separately sized by their tickets).

### 6. Apply or rescind the standing `github_mcp_offer:accepted` decision (carry-forward)
- **Action:** Either write the merged `.mcp.json` entry the accepted offer describes
  (read-only-scoped, `${GITHUB_MCP_PAT}`), or amend the `friendlies.json` record with a
  dated rescinding note. Issue-sorter's step-8 gate correctly stayed silent again this
  firing ("accepted" recorded) — no future firing will resurface this on its own.
- **Owner:** human (the decision and the write — outside any seat's charter).
- **Evidence:** issue-sorter this sweep — step 8 not applicable, offer terminal
  "accepted"; still no `.mcp.json` write in evidence since 2026-07-25.
- **Size:** ~10 min.

### 7. Sanity-check the not-queued adr-0009 harvest call (carry-forward)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  A "no" fully clears the decision-watcher surface (its queue is empty).
- **Owner:** human (yes → `/make-pack` or `/save-lessons` route; no → done, no record
  change).
- **Evidence:** carry-forward from the prior plan's entry 5; decision-watcher this sweep
  made no new judgments (0/0/0 delta across all 9 ADRs, `adr-queue.json` pending 0),
  leaving the call standing.
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

### 8. Disposition issue #139 — platform-level gap, not actionable from this repo (carry-forward)
- **Action:** Decide: keep #139 open as a tracking marker for the upstream platform gap
  (the cd-into-primary compound-command escape of the git-only worktree guard), or close
  it with a pointer to wherever the gap is actually actionable. Either outcome is fine;
  the debt is that it sits in the open roster looking like local work.
- **Owner:** human.
- **Evidence:** carry-forward from the prior plan's entry 6; repo-cleaner this sweep —
  open, unassigned, owner comment 2026-08-08 ("not repo-actionable"), unchanged across
  every prior firing.
- **Size:** ~5 min.

### 9. Harden the seat report-filename convention against collisions (NEW)
- **Action:** Two seats fired in the same second and computed the identical default
  report path `.claude/ops/reports/2026-08-10T06-23-59Z.md`; chore-lead had to
  disambiguate by hand (seat-name suffixes). Make the suffix the contract: file it via
  docs' `/file-bug` (lands as a GitHub Issue per ADR-0002), fix = each ops seat's agent
  file names its report `<timestamp>-<seat-name>.md` by default.
- **Owner:** human (files the issue; the fix is a small harness agent-file edit that
  rides the normal gate).
- **Evidence:** chore-lead notes this sweep — collision observed and hand-resolved this
  firing; both suffixed reports already applied to disk.
- **Size:** ~10 min (file) + ~15 min (fix, when picked up).

## Not queued (checked, found clean this sweep)

- ADR review: quiescent — 9/9 ADRs classified, zero delta (0 new / 0 amended / 0
  newly-superseded), no harvest or stale-citation candidates, queue pending 0, checkpoint
  payload byte-identical (decision-watcher).
- Issue intake: quiescent — the window since 13:44:32Z returned #154 (filed and resolved
  same day, closed via PR #155's merge), #149–#152 (already fully-formed — entry 5), and
  merged PRs #153/#155, all by the trusted author; nothing held, 0
  `needs-triage-approval` repo-wide (issue-sorter).
- PRs: 95 total, all 95 MERGED, zero open, no orphans (repo-cleaner).
- The two `.gitignore` WARN lines (`dist/`, `harness-audit-*/`) — re-reviewed again,
  on-demand-generated paths, deliberately kept, no edit (repo-cleaner).

## Resolved since the prior plan (2026-08-09, 13:44Z sweep)

- Prior entry 1 (delete `mobilize-chores-feature-dispatch`) — RESOLVED: gone between
  firings; repo-cleaner's full branch scan this sweep reports exactly one orphaned local
  branch, and it is the new `fix/154-...` (entry 1's successor).
- Prior entry 2 (commit the 13:44Z firing's applied artifacts) — RESOLVED: repo-cleaner's
  dirty-file list this firing contains no `.claude/ops/` path (all 9 dirty files are
  docs/ and teamwork/ authoring); the ops state sits committed on main @ cf8acb7.
  Succeeded by entry 2 for this firing's own artifacts.
- Prior entries 3, 4, 5, 6 — carried forward as entries 4, 6, 7, and 8 respectively.
