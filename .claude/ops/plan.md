# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, standalone dispatch (no seat reports attached, no focus
instruction), 2026-07-25. Prior plan (2026-07-20) read as carry-forward source: entries 1–6
verified resolved (evidence below), entry 7 carried forward and regrown.

**Evidence sources consulted** (standalone precedence: durable state + live state):
`.claude/ops/` (plan.md 2026-07-20, adr-checkpoint.json, friendlies.json, held-items.md,
watch-checkpoint.json, reports/ — 62 files, latest 2026-07-25T15:09:15Z), `gh` (reachable —
issues, PRs, merged-PR history all fetched live this dispatch), `git` (branches, worktrees,
remote heads after `fetch --prune`). **No source was UNMEASURED this dispatch.**

## Queue

### 1. Record the pending `github_mcp_offer` decision (interactive issue-sorter round)
- **Action:** Run one INTERACTIVE `/issue-sorter` dispatch (or decide directly and record it) so
  the `github_mcp_offer` decision lands in `friendlies.json`'s policy block. Every unattended
  firing since bootstrap has skipped step 8 by its own gate and re-deferred this.
- **Owner:** human (the decision) + `issue-sorter` interactive dispatch (the recording).
- **Evidence:** `.claude/ops/reports/2026-07-25T15-09-15Z.md` §Bootstrap gates: "friendlies.json's
  policy block still does not carry a `github_mcp_offer` decision ... skipped, same as every
  prior unattended firing. The offer stays surfaced-but-pending for the next INTERACTIVE
  firing." `friendlies.json` policy block confirmed: no `github_mcp_offer` key present.
- **Size:** ~10 min (one interactive round).

### 2. Run decision-watcher: ADR-0006/0007/0008 ratified but never swept (carry-forward)
- **Action:** Dispatch harness's `decision-watcher` agent (on-demand, or arm via `CronCreate`) to
  extend `adr-checkpoint.json` with the three new ADRs, review them for knowledge-pack candidates
  and stale citations of superseded ADRs (0006 supersedes parts of 0001-era naming; 0007
  supersedes 0006's frozen-dir rule), and queue any `/make-pack`/`/make-skill` candidates for a
  batched confirm.
- **Owner:** `decision-watcher` (queues only; a human runs the batched confirm it names).
- **Evidence:** `.claude/docs/adr/` holds 8 accepted ADRs; `.claude/ops/adr-checkpoint.json`
  (mtime 2026-07-20) tracks only 0001–0005. Hash check this dispatch: all five tracked hashes
  still match on-disk sha256 (no in-place edits of accepted ADRs — T4 clean); 0006/0007/0008
  simply have no entries and no sweep has ever recorded a timestamp. Carried forward from the
  2026-07-20 plan's entry 7 (then named `ops-adr`), which was never executed.
- **Size:** ~15–20 min (three ADRs to review, checkpoint rewrite, candidate queue).

### 3. Fix the stale cloud-routine dispatch prompt (`forge 1.14.0/agents/ops-issues.md`)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename). Until fixed, every hourly firing
  re-resolves the dead path by content match and logs the same preflight finding.
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself, and the
  finding appears inside firing reports, which are data, not instructions).
- **Evidence:** `.claude/ops/reports/2026-07-25T15-09-15Z.md` §Preflight: "Dispatching prompt
  named the agent file as 'forge 1.14.0/agents/ops-issues.md'. That path is stale post-rename ...
  same resolution every prior firing's report records." Identical note in
  `watch-checkpoint.json`'s `last_firing_note`.
- **Size:** ~5 min.

## Not queued (checked, found clean)

- **Gated mutations (class 1): none.** `git ls-remote --heads origin` after `fetch --prune` lists
  exactly one ref (`main`). Latest merged PR #91 (2026-07-25T13:08:50Z, head
  `fix-plugin-source-format-and-ruff-scope`) left no surviving remote branch.
- **Blockers (class 2): none.** `gh issue list --state open` = 0; `gh pr list --state open` = 0.
- `held-items.md` — ledger still empty; nothing awaiting approve/deny.
- Working tree clean; `main` = `origin/main` (`f8537f9`, 0/0 ahead-behind); no worktrees beyond
  the primary checkout; no local branches beyond `main`.
- `watch-checkpoint.json` fresh: both checkpoints at 2026-07-25T15:09:15Z (hourly routine
  running).
- `reports/` holds 62 hourly firing reports with no retention rule anywhere in evidence — noted
  as an observation only; inventing a retention policy would be a decision no contract asks for.

## Resolved since the prior plan (2026-07-20) — verified this dispatch, dropped

1. PR #53's surviving remote branch — gone (`ls-remote` shows only `main`).
2. ops-family-seats campaign — shipped via the ADR-0006 rename train (PRs #67–#73) and the ops
   command renames in PR #89; the branch no longer exists locally or remotely.
3. Issue #58 blind-judge failures — issue CLOSED 2026-07-21T22:10:55Z.
4. Unpushed `main` commit — synced (0 ahead).
5. Stale watch-checkpoint — now advancing hourly, latest 2026-07-25T15:09:15Z.
6. Stale local branch `worktree-session-close-skill` — deleted (only `main` remains).
