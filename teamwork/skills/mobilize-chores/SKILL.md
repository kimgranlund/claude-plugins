---
name: mobilize-chores
description: >-
  Sweeps this repo's ops queue via /sweep-chores, then handles whatever's genuinely mobilizable —
  open tickets on the resolved backend (GitHub issues, local docs/tickets/, or an Option-C
  adapter) labeled feature, bug, or task with no build in flight — after one batched confirm. A bug ticket dispatches to /file-bug's own investigation; a feature
  ticket is named as the next /build-feature command for the human (build-feature is unreachable
  programmatically); a task ticket runs find-intent to clarify it, then an
  Agent dispatch executes it under a Findings write-back contract. Everything else (ops/hygiene
  actions, human-decision items) is skipped, never mobilized. Run /mobilize-chores [blank, or a
  scope instruction]. NOT for just checking the queue (/sweep-chores); NOT for building one
  specific, already-known ticket (/build-feature or /file-bug directly); NOT for filing a new bug
  or feature (/file-bug, /file-feature); NOT for the hygiene execution (repo-cleaner, already run
  inside the sweep this wraps).
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a full sweep-and-mobilize | a scope instruction for the underlying sweep]"
allowed-tools: ["Read", "Glob", "Bash(gh issue list *)", "Bash(gh issue view *)", "Bash(gh issue comment *)", "Bash(gh issue edit *)", "Bash(gh issue close *)", "Bash(gh api graphql *)", "Bash(gh repo view *)", "Skill", "Agent", "AskUserQuestion"]
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
4. **One batched confirm.** List every mobilizable ticket found (id, title, kind) in ONE
   `AskUserQuestion` round — never per-ticket, never split by kind. The human picks which to
   mobilize now, all, some, or none. Nothing dispatches before this round returns — including
   step 5's own `find-intent` clarifying round for tasks, which runs strictly AFTER this confirm,
   never before: clarifying a task nobody chose to mobilize wastes the human's attention on
   something that ends up skipped anyway.
5. **Dispatch by kind, per the confirmed selection only.**
   - `kind: bug` → `Skill(docs:file-bug)` carrying the ticket id (`file-bug` is
     `disable-model-invocation: false` — reachable via the Skill tool, verified live 2026-08-08);
     its own resume path dispatches investigation.
   - `kind: feature` → **KNOWN LIMITATION (tracked separately, not fixed by this change):**
     `build-feature` is ALSO `disable-model-invocation: true` — the same unreachable-via-Skill-tool
     problem step 1 had, but `build-feature` has no single wrapped agent to dispatch instead
     (unlike `chore-lead`, it is itself a multi-phase procedure that sizes and routes at dispatch
     time). Until that's resolved, report the confirmed feature ticket ids in the final report and
     name `/build-feature <id>` as the exact next command for the human to run — never silently
     fail, and never guess an invocation mechanism this skill hasn't verified works.
   - `kind: task` → **clarify, then dispatch — never blind.** Tasks carry no fixed execution verb
     the way features/bugs do (`file-task`'s own scope is deliberately heterogeneous: chores,
     follow-ups, research items, debts), so run `Skill(harness:find-intent)` on the confirmed
     ticket's full body first — its own contract caps this at ONE batched clarifying round, and
     only fires that round when something is genuinely ambiguous; a ticket that's already clear
     proceeds with zero rounds. Still not concretely actionable after that round (no clear "what
     would done look like") → report SKIPPED, name the gap, never dispatch on an unclear brief.
     Otherwise, dispatch via the `Agent` tool — `subagent_type: general-purpose` is the default
     (`team-or-solo-rules`' own solo-first/null-unit reasoning: no tool restriction, parallelism,
     or multi-skill preload is needed for a generic task, so no purpose-built agent earns its
     keep); reach for a specific named agent only when the clarified brief genuinely needs one of
     those three properties. The
     dispatch prompt carries the clarified brief plus the SAME Findings-write-back contract
     `file-bug`'s own investigation dispatch uses (its Phase 5/6): it names the record and the
     write-back verb **per the backend resolved in step 2** (git-native: the issue number,
     `gh issue comment`; local: the TICKET file's path, editing its `## Findings` section
     directly; Option C: the resolved adapter's `update` operation) and must leave a dated
     Findings-equivalent entry at each significant result — the stopping predicate includes at
     least one such entry before the work counts as done. Read the record back on return
     (git-native: `gh issue view --comments`; local: re-`Read` the file; Option C: the adapter's
     `read` operation); a Findings entry landed → advance status (`doing` label / frontmatter
     `open`→`doing` / the adapter's mapped state; `done` — close via `gh issue close` / frontmatter
     `status: done` / the adapter's close operation once genuinely finished; `wontfix` — add the
     label or set the equivalent status, comment the reason, then close — matching `file-bug`'s own
     Phase 6 status verbs for that same backend) and report it as mobilized; no entry landed → one
     re-dispatch with the contract quoted, then a recorded loss on the ticket if still nothing —
     same discipline as `file-bug`'s own Phase 6 failure branch.

   Every dispatch is independent; one failing never blocks the others.
6. **Report.** Verdict-first: the sweep's own findings, then a table of every ticket CONSIDERED
   this run — mobilized (dispatch + outcome: succeeded / failed / still in flight), or
   skipped-and-why (not confirmed, in flight already, wrong/ambiguous label, still too vague after
   clarification, or excluded by the sweep's own judgment).

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
- A confirmed task's `find-intent` round still leaves the brief unclear → report SKIPPED with the
  named gap; never dispatch on an unclear brief hoping the agent figures it out.
- A confirmed task's Agent dispatch returns with no Findings-equivalent comment on the ticket →
  one re-dispatch, the write-back contract quoted, before recording the loss — same discipline as
  `file-bug`'s own Phase 6 failure branch.

Done when `/sweep-chores` has run (via the direct `chore-lead` dispatch step 1 names, not a failed
Skill-tool call), every open `feature`/`bug`/`task` ticket with no build in flight has been
considered, the human's one batched confirm gated every dispatch, and the final report names
every considered ticket's outcome — a mobilized bug/task ticket's dispatch outcome, a confirmed
feature ticket's named next command, or a skip-and-why. NOT done while a dispatch fires before the
confirm round, an unlabeled item is mobilized, a bug ticket is routed to `build-feature` instead
of `file-bug`, a task ticket is dispatched without a `find-intent` pass first (or dispatched
anyway after that pass left it still unclear), a ticket already in flight is dispatched again, a
task dispatch leaves no Findings-equivalent entry unnoticed, or step 1 is attempted via the Skill
tool instead of the direct `chore-lead` dispatch.
