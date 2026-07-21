# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `ops-planner`, standalone dispatch (no seat reports attached), 2026-07-20.
First-ever plan file — no prior `.claude/ops/plan.md` existed, so there is no carry-forward set
of still-open entries to fold in.

**Evidence sources consulted** (standalone precedence: durable state + live state, no reports
attached to judge instead): `.claude/ops/` (adr-checkpoint.json, held-items.md,
watch-checkpoint.json, reports/ — 6 files, latest 2026-07-18T17:33:02Z), `gh` (issues, PRs, both
reachable — `gh auth status` confirmed logged in as `kimgranlund`, `repo`/`workflow` scopes
present), `git` (branches, worktrees, remote refs). **No source was UNMEASURED this dispatch** —
`gh` was reachable throughout, so nothing here is stale-by-necessity, only stale-by-elapsed-time
(named per entry below).

## Queue

### 1. Delete merged PR #53's surviving remote branch
- **Action:** Run `campaign_close.py 53 --repo kimgranlund/claude-plugins --gate <touched-plugin-roots>`
  to independently verify PR #53 is `MERGED` and delete + reverify removal of its remote branch.
- **Owner:** `ops-repo` (its one gated mutation for exactly this case), or a human running
  `campaign_close.py` directly.
- **Evidence:** `gh pr list --state merged` shows #53 "ADR-0004 dual-write: forge 1.34.10, scribe
  0.19.0 (closes #44)", `headRefName: worktree-issue-44-adr-0004-dual-write`, merged
  2026-07-19T01:09:40Z. `git ls-remote --heads origin` still lists that branch today
  (2026-07-20). `ops-repo`'s last sweep (`.claude/ops/reports/2026-07-18T13-19-41Z.md`, scheduled
  firing) ran *before* the merge and never caught it — no `ops-repo` firing has happened since,
  so nothing has caught it since.
- **Size:** ~5 min (one script run).

### 2. Finish and ship the in-progress ops-family-seats campaign
- **Action:** Complete the `ops-orchestrator`/`ops-planner` build already drafted on this branch,
  run `release_gate.py "forge 1.14.0" --package` and a scoped `/eval-run`, then open the PR.
- **Owner:** current session / human continuing the campaign.
- **Evidence:** `git status` on branch `ops-family-seats` (HEAD `d2ac486`, not pushed —
  `git ls-remote --heads origin` has no `ops-family-seats` ref) shows 3 modified agent files
  (`ops-adr.md`, `ops-issues.md`, `ops-repo.md` — each gained a reciprocal NOT-for fence pointing
  at the two new seats) plus 4 untracked files: `agents/ops-orchestrator.md` (75 lines),
  `agents/ops-planner.md` (71 lines), and command skills `skills/ops-orchestrator/SKILL.md` +
  `skills/ops-planner/SKILL.md` (both `disable-model-invocation: true`, `user-invocable: true` —
  each already has an `evals/audit-report.md` but no `evals.json`, consistent with not being
  model-routed). `gh pr list --state open` = 0 — no PR yet.
- **Size:** 1–2 hours (gate + eval-run + PR write-up).

### 3. Investigate issue #58's two blind-judge routing failures
- **Action:** Re-run `/eval-run` scoped to `feature` + `reference-forge` together (the reporter's
  own suggested next step) to settle whether `reference-forge` legitimately wins the `feature:t07`
  boundary case or `feature`'s own fence needs tightening; annotate both suites' `evals/evals.json`
  with the dated finding either way. `research-methods:n13` needs no fix — it matches the
  already-accepted leak pattern in `rubric-forge`'s `n06`/`n07`.
- **Owner:** human/session running the scoped `/eval-run`.
- **Evidence:** Issue #58 (open, `task` label, filed by `kimgranlund` 2026-07-20T06:52:38Z,
  updated 07:11:09Z) — full body already contains the root-cause analysis: 253/255 cases passed
  across 13 suites/255 cases, 2 failures detailed with the reporter's own diagnosis.
- **Size:** ~20–30 min (scoped eval-run + judgment read + evals.json annotation).

### 4. Push local `main` (1 commit ahead of `origin/main`, unpushed)
- **Action:** Verify the commit was an intended direct-to-main single-file change (per this
  workspace's solo-fix exception), then `git push origin main`.
- **Owner:** human decision (the verify step, before the mechanical push).
- **Evidence:** `git log --oneline origin/main..main` = exactly 1 commit, `d2ac486`
  "orchestration-coordinator agent: effort high→xhigh (orchestration 0.7.8)"; `git branch -vv`
  shows `main ... [origin/main: ahead 1]`.
- **Size:** <5 min once verified.

### 5. Refresh ops-issues' watch-checkpoint (2 days stale)
- **Action:** Dispatch an on-demand `/ops-issues` sweep (or arm its hourly routine via
  `CronCreate` for this session) to advance `issues_checkpoint`/`prs_checkpoint` past issue #58.
- **Owner:** `ops-issues`.
- **Evidence:** `.claude/ops/watch-checkpoint.json` — `issues_checkpoint: 2026-07-18T17:33:02Z`.
  Issue #58 was created 2026-07-20T06:52:38Z and is still open — undiscovered by the last sweep.
  `.claude/ops/reports/` holds exactly one `ops-issues` report (the 2026-07-18 bootstrap); none
  since.
- **Size:** ~5–10 min (bounded/idempotent per its own contract).

### 6. Delete stale local branch `worktree-session-close-skill`
- **Action:** `git branch -d worktree-session-close-skill` — a manual/human action; no `ops-repo`
  gated script covers local-branch deletion (`ops-repo`'s contract explicitly excludes it: "it
  does not touch worktrees or local branches").
- **Owner:** human.
- **Evidence:** `git branch -vv` shows `worktree-session-close-skill 6f03352
  [origin/worktree-session-close-skill: gone]` — remote already deleted post-merge (PR #56,
  merged 2026-07-19T20:59:12Z); only the local branch is left over.
- **Size:** <1 min.

### 7. Run ops-adr's first-ever sweep now that it shipped
- **Action:** Dispatch `ops-adr` on-demand (or arm via `CronCreate`) to validate
  `adr-checkpoint.json` against the live ADR corpus and queue any `pack-forge`/`skill-forge`
  candidates.
- **Owner:** `ops-adr`.
- **Evidence:** PR #59 "Add ops-adr: standing periodic ADR-review agent" merged
  2026-07-20T14:04:22Z. `.claude/ops/reports/` holds zero `ops-adr` reports.
  `.claude/ops/adr-checkpoint.json` carries hashes/status for 5 accepted ADRs but no recorded
  sweep timestamp — never validated against a live run.
- **Size:** ~10–15 min.

## Not queued (checked, found clean)

- `held-items.md` — empty ledger, nothing held.
- `.claude/worktrees/` — empty, no dangling worktrees.
- Issues #33/#34 (the only two tracked in the prior `ops-issues` report) — both closed since
  (2026-07-18T20:40:29Z and 2026-07-18T18:00:01Z respectively); no longer live.
