---
name: check-state
description: >-
  Read-only project work-state report: bundled collectors sweep git (branches, worktrees,
  stashes), tickets/PRs, and ROADMAP/PLAN/TICKET docs, cross-reference the layers, and
  report verdict-first — Blocked-on-you, Ready-to-close, Drift, Delta since last run —
  every finding naming its owning command. Use for "what's the state of the project",
  "where are we", "what's blocked on me", "give me a project state report", "what can be
  merged or deleted", "catch me up on this repo", or reviewing all roadmap/plan/backlog
  items and open tickets. NOT for choosing next work (chore-planner), executing cleanup
  (repo-cleaner), plugin health (/check-everything), one PR/issue's status (plain gh
  lookup), or which lifecycle loop/build-turn stage the project is in — the
  lifecycle-POSITION axis, not work-state (docs:check-stage, where installed).
disable-model-invocation: false
user-invocable: true
argument-hint: "[repo-root] [--artifact]"
---

# check-state

One verdict-first report of everything in flight — docs, tickets, git — cross-referenced
and delta'd, mutating nothing. The run's ONLY write is the checkpoint at
`.claude/ops/state-checkpoint.json`; it never issues a mutating git/gh command, and every
proposed action names the owner that executes it.

## Procedure

1. **Collect.** Run the three collectors against the repo root (default `.`), capturing
   each JSON to the scratchpad:
   - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-state/scripts/git_state.py <root>`
   - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-state/scripts/ticket_state.py <root>`
   - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-state/scripts/doc_state.py <root>`
   A collector exiting 2 marks its section UNMEASURED with the script's stated reason —
   the report still renders from the sections that ran.
2. **Delta.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-state/scripts/state_diff.py
   <git.json> <ticket.json> <doc.json> --checkpoint <root>/.claude/ops/state-checkpoint.json`
   — an UNMEASURED collector's slot takes `-` (its layers report as
   measurability transitions, never add/remove noise); first run reports itself as such;
   the checkpoint write is the run's one file write.
3. **Standing automation.** Where the session exposes CronList, list armed jobs; the
   report names which standing seats (decision-watcher, repo-cleaner, issue-sorter) are
   armed vs dormant. No CronList available → the section reads "unknown (no session
   cron visibility)", never a guess.
4. **Cross-reference.** The judgment pass, over the collector JSON only — no re-running
   git/gh by hand. It answers, per layer pair:
   - doc ↔ ticket: plan/roadmap items whose spine IDs match no open ticket; open tickets
     no plan doc references.
   - ticket ↔ git: merged PRs whose remote branch survived (collector's
     `merged_branch_survivors`); branches/worktrees with no open PR or issue naming them.
   - blocked-on-you: quarantine stashes, `blocked`-labeled tickets, and the collector's
     measured ownership classes — `awaiting_my_review`, `mine_failing_ci`,
     `changes_requested` on the viewer's PRs. `awaiting_review` PRs by others are
     attention, not blockage; with no `viewer` in the JSON, ownership reads "unmeasured".
5. **Report** in the Output contract's order. With `--artifact`, additionally render the
   same content as a single-scroll narrative page via `session-review-artifact` where
   installed (terminal report still delivered when it isn't). Findings are proposals —
   acting on any of them is a separate, user-initiated step.

## Output contract

Sections in this order, each headed 🟢 (nothing to do), 🟡 (attention), or 🔴 (blocked);
a 🟢 header licenses skipping that section, not the rest of the report:

1. **Blocked on you** — leads even when empty ("nothing blocked on you"). Quarantine
   stashes, review-waiting PRs, failing CI, blocked tickets.
2. **Ready to close** — evidence-backed candidates: merged-PR surviving branches
   (`campaign_close.py <pr> --repo <owner/repo>`), merged-but-undeleted local branches,
   prunable worktrees (repo-cleaner proposes removal).
3. **Drift** — the cross-reference findings; each names its repair owner
   (/file-task for an untracked plan item, issue-sorter for triage, docs' /check-doc
   for a stale plan).
4. **Delta** — added/removed per layer since the checkpoint, or "first run — no delta".
5. **Counts** — one line per layer: branches / worktrees / stashes / issues / PRs /
   docs / release drift / armed automation.

Every 🟡/🔴 line carries `→ <owning command or seat>`. A finding with no owner is
reported as exactly that — "no owner in the routing table" — which is itself a finding.

## Failure branches

- Not a git repo → report that and stop; nothing else is measurable.
- `gh` absent, unauthenticated, or non-GitHub backend → ticket section UNMEASURED with
  the collector's reason line; git + doc sections still report.
- A collector exits 1 or 2 → quote its FAIL/SKIP line in the report, mark the section
  UNMEASURED, and pass `-` in its state_diff slot; do not substitute hand-run git/gh
  output for the missing JSON.
- Checkpoint unwritable → deliver the report with the Delta section marked "not saved";
  never skip the report over its bookkeeping.

Done when the report is delivered with all five sections present (UNMEASURED counts as
present) and the checkpoint reflects this run — or the not-a-repo stop is reported.

## Example

Good (a Ready-to-close line):
`🟡 PR #109 merged 2026-07-28 but branch 'fix-gate' still on origin → campaign_close.py 109 --repo nonoun/plugins`

Counter-example — do not imitate:
`- some branches look stale and could probably be cleaned up`
(no evidence, no owner, and "probably" invites the model to act on it itself).
