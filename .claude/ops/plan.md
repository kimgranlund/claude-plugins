# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-08. Evidence: the three seat reports
attached to this dispatch (decision-watcher 🟡, issue-sorter 🟢, repo-cleaner 🟢 — none
UNMEASURED), plus the prior plan (2026-07-25, standalone) read as carry-forward source. Nothing
refetched. Prior entries 1 and 2 verified resolved (see bottom); entry 3 carried forward and
regrown.

## Queue

**Class 1 — gated mutations verified safe: none left to queue.** PR #136's close was already
executed inside repo-cleaner's own gates this sweep: `campaign_close.py 136 --repo
kimgraund/claude-plugins --gate teamwork` → exit 0, C1 merged / C2 remote branch absent / C3
teamwork gate clean. All 78 PRs MERGED, zero open, remote branch surface clean after
`fetch --prune`.

**Class 2 — blockers: none.** No open PRs, no claimed issues, working tree clean, one primary
worktree only.

### 1. Batched confirm on the pending stale-citation candidate, then Phase 6 (human decision)
- **Action:** Run one batched AskUserQuestion round over the 1 pending candidate in
  `adr_queue.py pending` (adr-0006's find-the-ask row superseded by adr-0009). On confirm, run
  save-lessons Phase 6: re-open each cited file:line, confirm still-valid, fix or retire.
- **Owner:** human (the confirm) → save-lessons Phase 6 (the re-open pass) — never
  decision-watcher itself.
- **Evidence:** decision-watcher report this sweep: 3 citing files, 9+ lines —
  `harness/skills/big-change-git-rules/references/rename-execution-playbook.md:4,7,13,15,16,19,24,33,73`;
  `harness/skills/check-all-agents/references/standard-of-excellence.md:93`;
  `harness/skills/naming-rules/references/estate-rename-map.md:11,15,42` (this last is
  deliberately NOT stale — adr-0009 Decision 3 keeps that file byte-identical). Mixed staleness:
  2 of 3 files likely still valid; only Phase 6 resolves which.
- **Size:** ~15–25 min (one confirm round + 3-file re-open pass).

### 2. Sanity-check the not-queued adr-0009 harvest call (human decision)
- **Action:** Human yes/no: does adr-0009 deserve a harvest candidate for the
  "narrow-supersession, prose-scoped `supersedes:` beats mechanical extraction" pattern?
  decision-watcher chose NOT to queue it (reasoning: it is about classify_delta's own parsing,
  not a fact from the ADR corpus) and explicitly flagged the call for human review.
- **Owner:** human (if yes → `/make-pack` or `/save-lessons` route; if no → done, no record
  change).
- **Evidence:** decision-watcher report §Open questions, this sweep.
- **Size:** ~5 min to decide.

### 3. Fix the stale cloud-routine prompt AND verify the routine is still armed (carry-forward)
- **Action:** Edit the scheduled issue-sorter cloud routine's prompt to name
  `harness/agents/issue-sorter.md` (post ADR-0006/0007 rename), and while in the routine config,
  verify the schedule is still armed: issue-sorter's sweep window this dispatch opened at
  2026-07-25T17:08:34Z — no unattended firing appears to have advanced the checkpoint in the
  ~2 weeks since, which is consistent with the routine having stopped (inference from the
  checkpoint gap, not directly measured this sweep).
- **Owner:** human (`CronUpdate` / routine config edit — the routine cannot edit itself).
- **Evidence:** carry-forward from the 2026-07-25 plan entry 3 (evidence there:
  `.claude/ops/reports/2026-07-25T15-09-15Z.md` §Preflight + `watch-checkpoint.json`
  `last_firing_note`); staleness-gap inference from issue-sorter's report this sweep ("Full
  intake sweep since 2026-07-25T17:08:34Z"). No seat this sweep reported the prompt fixed.
- **Size:** ~5–10 min.

### 4. Update issue #140 with both new payload-discipline facts; decide close-or-extend (hygiene)
- **Action:** One `gh issue comment` on #140 recording: (a) repo-cleaner's 2026-08-08 firing
  demonstrated the fix in practice (clean fenced payload block, report landed at
  `.claude/ops/reports/2026-08-08T13-50-05Z.md`), and (b) issue-sorter exhibited a NEW instance
  of the same class this sweep — it named its report destination
  (`.claude/ops/reports/2026-08-08T13-47-59Z.md`) in prose instead of a fenced target-pathed
  block, chore-lead correctly refused the ambiguous payload, and that report file therefore does
  not exist on disk while `watch-checkpoint.json` DID advance to 2026-08-08T13:47:59Z (a
  checkpoint-without-report gap in the ledger). Then decide: close #140 (fixed-in-practice) or
  keep open until the seat contracts themselves are patched (candidate 7th instance for the
  silent-failure-catalog, cf. #127). Optionally backfill the missing report file from the seat
  text chore-lead holds.
- **Owner:** human (the comment + the close-or-extend decision; backfill via chore-lead's held
  text if chosen).
- **Evidence:** repo-cleaner report §Aside; issue-sorter report §Files/payload NOTE, both this
  sweep.
- **Size:** ~10 min.

### 5. Retire (or deliberately keep) the two no-match `.gitignore` lines (hygiene, propose-only)
- **Action:** Human or a `/clean-repo` pass judges the two WARN lines `gitignore_check.py`
  flagged as matching nothing in the current tree: `dist/` and `harness-audit-*/`. Caveat before
  deleting `dist/`: it is gate OUTPUT (`release_gate.py --package` writes `<plugin>/dist/`), so
  "matches nothing" only means no package has been built in this checkout — retiring it would
  let future gate artifacts land in git. `harness-audit-*/` has no such standing producer in
  evidence and looks genuinely dead.
- **Owner:** human or `/clean-repo` (repo-cleaner never hand-edits `.gitignore`; propose-only by
  its contract).
- **Evidence:** repo-cleaner report this sweep: gitignore_check.py, 2 WARN, no urgency.
- **Size:** ~5 min.

### 6. Route the 7 open, unclaimed issues toward triage or build (hygiene backlog)
- **Action:** `/mobilize-chores` (or a direct human pass) over the 7 open issues — #131, #133,
  #135, #137, #138, #139, #140 — all fully labeled (kind+scale, complete capture-record shape),
  all with empty assignees and zero comments, i.e. none claimed and none moving. #140 overlaps
  entry 4 above; resolve that entry first.
- **Owner:** human (launches `/mobilize-chores`; it gates any build behind one confirm).
- **Evidence:** issue-sorter report (labels/record-shape verified on #140, #131 read in full);
  repo-cleaner report (ADR-0005 stale-claim check: empty assignees, zero comments, no stale
  claims).
- **Size:** ~10 min to launch and triage; build time per ticket varies (hours, ticket-dependent).

## Not queued (checked, found clean this sweep)

- `held-items.md` unchanged and empty — nothing awaiting approve/deny (issue-sorter).
- `friendlies.json` current — `github_mcp_offer` recorded accepted with a 2026-07-25 override;
  no writes needed (issue-sorter).
- ADR checkpoint + queue current on disk — payloads applied by chore-lead this sweep
  (decision-watcher); adr-0009 itself judged and correctly not queued as a harvest candidate
  (subject to entry 2's sanity check).
- Branches, worktrees, remote refs, working tree — all healthy (repo-cleaner; the one stale
  local tracking ref was cleaned by `fetch --prune` itself, not a gated mutation).
- Unknown-author hold path — still unexercised by live traffic since bootstrap; design-reviewed
  only. Observation, not a defect (issue-sorter).

## Resolved since the prior plan (2026-07-25) — verified against this sweep's evidence, dropped

1. **`github_mcp_offer` decision (prior entry 1)** — resolved: recorded as accepted (with a
   2026-07-25 override) in `friendlies.json`'s policy block (issue-sorter report, step 8
   not-applicable gate).
2. **decision-watcher sweep of the untracked ADRs (prior entry 2)** — executed this sweep:
   full checkpoint delta judged over the 9-file corpus, checkpoint and queue advanced; its
   output is now entries 1–2 above.
3. Prior entry 3 (stale routine prompt) is NOT resolved — carried forward as entry 3.
