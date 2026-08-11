---
name: mobilize-chores
description: >-
  Sweeps this repo's ops queue via /sweep-chores, then handles whatever's genuinely mobilizable —
  open tickets on the resolved backend (GitHub issues, local docs/tickets/, or an Option-C
  adapter) labeled feature, bug, or task with no build in flight — after one batched confirm (a
  leading `auto` argument skips it, for /goal loops and scheduled runs).
  Every confirmed ticket, regardless of kind, dispatches uniformly to the build-lead agent
  (ADR-0010), whose dispatch-ticket procedure owns the kind branch; an
  under-specified task comes back SKIPPED — no clarify round runs unattended. Everything else
  (ops/hygiene actions, human-decision items) is skipped, never mobilized.
  NOT for just checking the queue (/sweep-chores); NOT for building one specific,
  already-known ticket (/build-feature or /file-bug directly); NOT for filing a new bug or
  feature (/file-bug, /file-feature); NOT for the hygiene execution (repo-cleaner, already run
  inside the sweep this wraps).
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a full sweep-and-mobilize | 'auto' to skip the confirm round for unattended/loop use | a scope instruction, optionally prefixed with 'auto ']"
allowed-tools: ["Read", "Glob", "Edit", "Bash(gh issue list *)", "Bash(gh issue view *)", "Bash(gh issue comment *)", "Bash(gh api graphql *)", "Bash(gh repo view *)", "Agent", "AskUserQuestion"]
---

# mobilize-chores

`/sweep-chores` reports; this command reports AND drives. It wraps `/sweep-chores` unmodified —
never reimplements its fan-out — and adds one new, separately-gated step: mobilize whatever the
sweep surfaced that's actually buildable.

## Procedure

0. **Parse `$ARGUMENTS` for the unattended flag.** If `$ARGUMENTS` starts with the literal
   whitespace-delimited token `auto` (case-sensitive) — bare `auto`, or `auto <scope
   instruction>` — this run is UNATTENDED: strip that leading token and carry only the remainder
   forward as the scope instruction in step 1 (empty remainder → full sweep, same as blank
   `$ARGUMENTS` today). Skip step 4's `AskUserQuestion` entirely; see step 4's UNATTENDED branch.
   No leading `auto` token → this run is INTERACTIVE, today's existing behavior, completely
   unchanged: `$ARGUMENTS` forwards whole, step 4 runs as written. This is the literal entry point
   a `/goal` loop or scheduled routine calls (`/mobilize-chores auto`) to get a confirm-free pass —
   never inferred from "no human appears to be watching," always this explicit token, so the same
   invocation behaves identically whether a human or a loop types it.
1. **Sweep.** `/sweep-chores` is `disable-model-invocation: true` — command-only, unreachable via
   the Skill tool from inside another skill's procedure (verified 2026-08-08, issue #134: every
   attempt fails immediately with "cannot be used with Skill tool due to disable-model-invocation").
   `/sweep-chores`' own body names exactly what it wraps: it dispatches the `chore-lead` agent
   (Agent tool, `subagent_type: "harness:chore-lead"`), carrying the scope instruction from step 0
   verbatim, then shows the banner (if `.claude/ops/plan.md` doesn't exist yet) and relays the
   report unmodified. Do that dispatch directly — the agent, not the command — with the identical
   contract: banner check first when the plan file is absent, the step-0 scope instruction passed
   through, the report relayed as this step's own findings. This IS running `/sweep-chores`,
   mechanically, not a workaround.
2. **Find mobilizable tickets.** Resolve this repo's ticket backend once (`doc-writing-rules`'
   backend resolver, `references/backend-resolver.md`, where `docs` is installed; not installed,
   or no ruling → git-native, this workspace's own ADR-0002 instance, unchanged from before this
   resolver call). Then discover per the resolved backend:
   - **Git-native (Option B):** `gh issue list --state open --label feature --json
     number,title,labels`, the same for `--label bug`, and the same for `--label task`. For each
     candidate, check whether an open PR already references it via `gh api graphql` querying
     `closedByPullRequestsReferences { nodes { number state } }` for that issue (owner/repo from
     `gh repo view --json nameWithOwner`) — any node with `state: OPEN` means a PR is already in
     flight for it, exclude. **The flattened `gh issue view --json closedByPullRequestsReferences`
     form does NOT carry a `state` field at all** (verified 2026-08-07: it silently returns exit 0
     with no state key present, reading as "never in flight" regardless of the truth) — the
     GraphQL form is the only one that actually works; do not substitute the flattened form.
   - **Local (Option A):** `Glob` `docs/tickets/*.md`, `Read` each file's frontmatter. A candidate
     carries `status: open` and a `kind` of `bug`/`feature`/`task` (the same convention
     `file-bug`/`file-feature`/`file-task` write under this option — `doc-writing-rules` SKILL.md's
     TICKET section). **No in-flight-PR check exists for local tickets** — there is no established
     local convention linking a TICKET file to an open PR, so a local ticket already being worked
     cannot be excluded this way. This is a disclosed limitation, not a silent gap: name it in the
     step-6 report rather than skipping the check unremarked.
   - **External adapter / Option C (e.g. Linear):** the seven-operation adapter interface
     (`backend-resolver.md`) has no "list open records filtered by kind" primitive today —
     ticket-discovery for this backend is **not yet supported**. Report it UNMEASURED, naming the
     resolved adapter, exactly like the `gh issue list` unreachable failure branch below; never
     silently return zero tickets found.

   Regardless of backend, a ticket is mobilizable only if: labeled/kinded exactly ONE of
   `feature`/`bug`/`task` (never unlabeled, and one carrying more than one of these three is
   ambiguous — exclude it, per the failure branch below), AND (git-native only) no
   `closedByPullRequestsReferences` node reads `OPEN`. Cross-check `plan.md`'s own queue for the
   same ids; a ticket the sweep already flagged as a human-decision item or a blocker is excluded
   even if it carries a mobilizable label/kind — the sweep's own judgment on THAT item stands.
3. **Nothing mobilizable → stop here.** Report the sweep's own findings (step 1) plus "0 tickets
   mobilizable this run" and why (no open feature/bug/task tickets, or all already in flight). No
   confirm round, no further steps — an empty mobilize pass is a normal, quiet outcome.
4. **One batched confirm — INTERACTIVE only (step 0 found no `auto` token).** List every
   mobilizable ticket found (id, title, kind) in ONE `AskUserQuestion` round — never per-ticket,
   never split by kind. The human picks which to mobilize now, all, some, or none. Nothing
   dispatches before this round returns. A disclosed limitation of the uniform dispatch, stated
   here because this round is the one place to act on it: `dispatch-ticket`'s task-clarifying
   round requires an interactive user and `build-lead` is an unattended seat, so NO clarify round
   runs inside step 5's dispatches — an under-specified task comes back SKIPPED, and clarifying it
   means the human re-runs the named command interactively afterwards. Flag visibly
   under-specified task tickets IN this confirm round (one line each), so the human can decline
   them here instead of paying a dispatch that will skip.

   **UNATTENDED (step 0 found a leading `auto` token): skip `AskUserQuestion` entirely.** Every
   ticket step 2 found mobilizable is auto-confirmed — step 2's own filtering (label ambiguity
   excluded on every backend; on git-native, in-flight PRs also excluded via the GraphQL check;
   the sweep's own human-decision/blocker items excluded on every backend) is the actual
   correctness gate, not this step, on either branch — this step was never the gate even for a
   human, only a selection point over an already-filtered set. **Option A (local tickets) has no
   in-flight-PR check at all — step 2's own disclosed limitation.** On that backend, UNATTENDED
   dispatches without the one guard INTERACTIVE mode also never had (the confirm round showed only
   id/title/kind, never in-flight state) — name that specific gap per ticket in the step-6 report
   rather than letting the summary imply a check that doesn't run there. An unattended dispatch's
   ceiling is PR-opened, never merged — merging stays a human act (ADR-0002's merge gate); nothing
   in this mode, or in `build-lead`/`dispatch-ticket`, attempts a merge or review on its own. Still
   name every visibly under-specified task ticket in the step-6 report exactly as the interactive
   branch would have flagged it in the confirm round — it comes back SKIPPED from `build-lead` (no
   clarify round runs unattended either way), never silently dispatched on a guess.
5. **Dispatch every confirmed ticket, uniformly.** Each confirmed ticket, regardless of kind →
   `Agent(subagent_type: "teamwork:build-lead")` carrying the confirmed ticket id. `build-lead`'s
   preloaded `dispatch-ticket` procedure (ADR-0010) owns the kind branch — its own body is the
   authoritative map, not restated here — and its unattended failure branches (an ambiguous
   record match reports as a named blocker; an under-specified task reports SKIPPED with no
   clarify round, never guessed at) apply automatically, since this dispatch never has an
   interactive user. Relay each returned typed result (path/URL, status, what shipped, a
   recorded blocker, or a SKIPPED gap) as that ticket's mobilized outcome — the same output a
   human running `/build-feature <id>` would see. This is the same
   `chore-lead`/`sweep-chores` shape step 1 already uses: the command stays
   `disable-model-invocation: true`, the agent carries the reachable procedure (issue
   #134/#135's shared fix pattern).

   Every dispatch is independent — one failing never blocks the others — but independence is
   not a parallelism license: mutating dispatches share this one checkout, so run them
   SERIALLY, or give each `isolation: "worktree"` on the Agent call per `parallel-work-rules`'
   own overlap test. The bug path (a hand-off, no tree mutation) is safe to overlap; anything
   that builds is not.
6. **Report.** Verdict-first: name which branch ran — INTERACTIVE, or UNATTENDED with the exact
   `auto`-prefixed argument as parsed in step 0 — so a step-0 misparse (a scope instruction that
   happens to start with the literal word "auto") is observable in the artifact of record, never
   silent. Then the sweep's own findings, then a table of every ticket CONSIDERED this run —
   mobilized (dispatch + outcome: succeeded / failed / still in flight), or skipped-and-why (not
   confirmed, in flight already, wrong/ambiguous label, too vague to build unattended — the seat
   SKIPPED, no clarify round available on this path — or excluded by the sweep's own judgment).

   **Blocker breakdown.** Every ticket whose outcome is a named blocker (`dispatch-ticket`'s own
   distinct outcome, not a plain SKIPPED) gets one paragraph, not just a table row: the ticket id
   and title, what's actually blocking it (`build-lead`'s own stated reason, quoted or
   paraphrased — never re-derived from scratch), which shape it is (name the shape in the
   paragraph, not just internally), and a proposed action that fits that shape. Classify before
   proposing — never propose a build attempt for any of these, and never blend two shapes into
   one paragraph:
   - **A judgment call** only a live conversation resolves → propose having it, and what happens
     on either answer.
   - **A protocol/ratification action** only a real human utterance satisfies (an ADR ratify
     comment, a sign-off) → describe what it unblocks once posted, but don't inline the command
     itself here (bad: "run `gh issue comment 142 --body 'ratified'`" — good: "post a ratify
     comment on ADR-0012's issue; once posted, the two citing skills unblock" — the verbatim
     command is the follow-up pass's job, below).
   - **Concurrent or in-flight work someone else owns** → name whose it is; propose checking in or
     waiting, never touching it directly.
   - **A mechanical human action** — a permission grant, a missing credential, a tool install —
     only a human can perform → name the exact action in plain language (still no inline command
     here; that's the follow-up pass).
   - **An external dependency with no lever here** (an upstream repo, a pending signature) → name
     what it's waiting on; the honest proposal is "nothing to do but watch."
   - **Fits none of the five cleanly** → say so plainly and propose the nearest honest action;
     never force a real blocker into the wrong bucket just to keep the list closed.

   Prose only in this pass, even where a command exists — end with one offer to do legwork that
   spares the human a file open or a terminal (e.g. reading a linked doc so they can decide
   without opening it themselves).

   **On request ("give commands" or equivalent) — a follow-up, commands-only pass.** For each
   blocker from the breakdown: a real, copy-pasteable command if the proposed action has one
   (verbatim, plus any caveat on what it does and doesn't unblock by itself) — or state plainly
   "nothing to run" if it doesn't, naming the one status-check command that inspects the
   external/concurrent state where one exists. Never invent a command that wouldn't actually do
   anything just to look complete — an honest "nothing to run except watching" beats a busywork
   command.

## Failure branches

- `/sweep-chores` itself fails to return → report that failure plainly; never run steps 2–6
  against a sweep that didn't happen.
- The resolved backend's own listing call is unreachable (`gh issue list` fails on git-native; a
  Glob/Read error on local; the adapter call errors on Option C) → report ticket-discovery as
  UNMEASURED for this run; the sweep's own report still stands on its own.
- Option C is resolved but the seven-operation adapter interface carries no listing primitive
  (today's state, per step 2) → report ticket-discovery UNMEASURED for that backend, naming the
  adapter; not a failure to fix here, a documented gap to close in the adapter interface later.
- A ticket's label or in-flight state is ambiguous (e.g. `linkedBranches` present but that branch
  has no open PR) → exclude it from the mobilizable set; ambiguity is never a license to dispatch.
- The confirm round returns "none" → report 0 mobilized, same as step 3's empty case; not a
  failure.
- `build-lead` returns a SKIPPED (a task not concretely actionable — no clarify round runs in an
  unattended dispatch) → relay it as that ticket's outcome in the step-6 table; the skip
  discipline itself lives in `dispatch-ticket`'s own failure branches, not re-litigated here.
  A named blocker gets more than a table row — step 6's blocker-breakdown paragraph, not just
  the row.
- `build-lead` returns with no Findings-equivalent entry visible on the ticket read-back → one
  re-dispatch of the SAME seat with `dispatch-ticket`'s contract quoted, then a recorded loss on
  the ticket if still nothing — the caller-side check that the seat's own write-back contract
  actually landed.
- UNATTENDED run auto-confirms a ticket step 2 flagged as visibly under-specified (no human was
  there to decline it) → dispatch it anyway; it returns SKIPPED from `build-lead` per that seat's
  own unattended contract, the identical outcome a human declining it in step 4 would have
  produced — never treated as an error unique to the unattended path.

Done when `/sweep-chores` has run (via the direct `chore-lead` dispatch step 1 names, not a failed
Skill-tool call), every open `feature`/`bug`/`task` ticket with no build in flight has been
considered, every dispatch was gated by the human's one batched confirm (INTERACTIVE) or by step
2's own filtering under the explicit `auto` token (UNATTENDED) — never by neither — and the final
report names every considered ticket's outcome — a mobilized ticket's relayed `build-lead` result,
a skip-and-why, or (for a named blocker) the classified breakdown paragraph, never just a table
row. NOT done while a dispatch fires before the confirm round on an INTERACTIVE run, a named
blocker gets only a table row with no classified paragraph, a blocker breakdown proposes a build
attempt instead of the shape its category actually calls for, an unlabeled item is mobilized, a
confirmed ticket is dispatched anywhere but `build-lead` (the per-kind routing that once lived
here belongs to `dispatch-ticket` now — re-growing it here is the regression), a ticket already
in flight is dispatched again, a dispatch leaving no
Findings-equivalent entry goes unnoticed, step 1 is attempted via the Skill tool instead of the
direct `chore-lead` dispatch, or an UNATTENDED run is inferred from context rather than the
explicit `auto` token.
