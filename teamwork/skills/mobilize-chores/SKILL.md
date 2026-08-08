---
name: mobilize-chores
description: >-
  Sweeps this repo's ops queue via /sweep-chores, then handles whatever's genuinely buildable —
  open GitHub issues labeled feature or bug with no build in flight yet — after one batched human
  confirm. A bug ticket dispatches straight to /file-bug's own investigation; a feature ticket is
  named as the next /build-feature command for the human to run (build-feature's own
  disable-model-invocation dial makes it unreachable programmatically — tracked separately, not a
  silent gap). Everything else in the queue (ops/hygiene
  actions, human-decision items, kind: task) is reported as skipped, never mobilized. Run
  /mobilize-chores [blank for a full sweep-and-mobilize, or a scope instruction]. NOT for just
  checking the queue (/sweep-chores); NOT for building one specific, already-known ticket
  (/build-feature or /file-bug directly); NOT for filing a new bug or feature (/file-bug,
  /file-feature); NOT for the hygiene execution itself (repo-cleaner, already run inside the
  sweep this wraps).
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a full sweep-and-mobilize | a scope instruction for the underlying sweep]"
allowed-tools: ["Read", "Glob", "Bash(gh issue list *)", "Bash(gh api graphql *)", "Bash(gh repo view *)", "Skill", "Agent", "AskUserQuestion"]
---

# mobilize-chores

`/sweep-chores` reports; this command reports AND drives. It wraps `/sweep-chores` unmodified —
never reimplements its fan-out — and adds one new, separately-gated step: mobilize whatever the
sweep surfaced that's actually buildable.

## Procedure

1. **Sweep.** `/sweep-chores` is `disable-model-invocation: true` — command-only, unreachable via
   the Skill tool from inside another skill's procedure (verified 2026-08-08, issue #134: every
   attempt fails immediately with "cannot be used with Skill tool due to disable-model-invocation").
   `/sweep-chores`' own body names exactly what it wraps: it dispatches the `chore-lead` agent
   (Agent tool, `subagent_type: "harness:chore-lead"`), carrying `$ARGUMENTS` verbatim, then shows
   the banner (if `.claude/ops/plan.md` doesn't exist yet) and relays the report unmodified. Do
   that dispatch directly — the agent, not the command — with the identical contract: banner check
   first when the plan file is absent, `$ARGUMENTS` passed through, the report relayed as this
   step's own findings. This IS running `/sweep-chores`, mechanically, not a workaround.
2. **Find mobilizable tickets.** `gh issue list --state open --label feature --json
   number,title,labels` and the same for `--label bug`. For each candidate, check whether an open
   PR already references it via `gh api graphql` querying `closedByPullRequestsReferences { nodes
   { number state } }` for that issue (owner/repo from `gh repo view --json nameWithOwner`) — any
   node with `state: OPEN` means a PR is already in flight for it, exclude. **The flattened `gh
   issue view --json closedByPullRequestsReferences` form does NOT carry a `state` field at all**
   (verified 2026-08-07: it silently returns exit 0 with no state key present, reading as "never
   in flight" regardless of the truth) — the GraphQL form is the only one that actually works; do
   not substitute the flattened form. A ticket is mobilizable only if: labeled exactly ONE of
   `feature`/`bug` (never `task`, never unlabeled, and a ticket carrying BOTH labels is ambiguous
   — exclude it, per the failure branch below), AND no `closedByPullRequestsReferences` node reads
   `OPEN`. Cross-check `plan.md`'s own queue for the same ids; a ticket the sweep already flagged
   as a human-decision item or a blocker is excluded even if it carries a buildable label — the
   sweep's own judgment on THAT item stands.
3. **Nothing mobilizable → stop here.** Report the sweep's own findings (step 1) plus "0 tickets
   mobilizable this run" and why (no open feature/bug tickets, or all already in flight). No
   confirm round, no further steps — an empty mobilize pass is a normal, quiet outcome.
4. **One batched confirm.** List every mobilizable ticket found (id, title, kind) in ONE
   `AskUserQuestion` round — never per-ticket. The human picks which to mobilize now, all, some,
   or none. Nothing dispatches before this round returns.
5. **Dispatch by kind, per the confirmed selection only.** `kind: bug` → `Skill(docs:file-bug)`
   carrying the ticket id (`file-bug` is `disable-model-invocation: false` — reachable via the
   Skill tool, verified live 2026-08-08); its own resume path dispatches investigation.
   `kind: feature` → **KNOWN LIMITATION (tracked separately, not fixed by this change):**
   `build-feature` is ALSO `disable-model-invocation: true` — the same unreachable-via-Skill-tool
   problem step 1 had, but `build-feature` has no single wrapped agent to dispatch instead (unlike
   `chore-lead`, it is itself a multi-phase procedure that sizes and routes at dispatch time). Until
   that's resolved, report the confirmed feature ticket ids in the final report and name
   `/build-feature <id>` as the exact next command for the human to run — never silently fail, and
   never guess an invocation mechanism this skill hasn't verified works. Every dispatch is
   independent; one failing never blocks the others.
6. **Report.** Verdict-first: the sweep's own findings, then a table of every ticket CONSIDERED
   this run — mobilized (dispatch + outcome: succeeded / failed / still in flight) or
   skipped-and-why (not confirmed, in flight already, wrong label, excluded by the sweep's own
   judgment).

## Failure branches

- `/sweep-chores` itself fails to return → report that failure plainly; never run steps 2–6
  against a sweep that didn't happen.
- `gh issue list` unreachable → report ticket-discovery as UNMEASURED for this run; the sweep's
  own report still stands on its own.
- A ticket's label or in-flight state is ambiguous (e.g. `linkedBranches` present but that branch
  has no open PR) → exclude it from the mobilizable set; ambiguity is never a license to dispatch.
- The confirm round returns "none" → report 0 mobilized, same as step 3's empty case; not a
  failure.

Done when `/sweep-chores` has run (via the direct `chore-lead` dispatch step 1 names, not a failed
Skill-tool call), every open `feature`/`bug` ticket with no build in flight has been considered,
the human's one batched confirm gated every bug-ticket dispatch, and the final report names every
considered ticket's outcome — a mobilized bug ticket's dispatch outcome, or a confirmed feature
ticket's named next command, or a skip-and-why. NOT done while a dispatch fires before the confirm
round, a `kind: task` or unlabeled item is mobilized, a bug ticket is routed to `build-feature`
instead of `file-bug`, a ticket already in flight is dispatched again, or step 1 is attempted via
the Skill tool instead of the direct `chore-lead` dispatch.
