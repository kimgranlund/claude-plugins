---
name: mobilize-chores
description: >-
  Sweeps this repo's ops queue via /sweep-chores (or, given a ticket-id list instead of a scope,
  skips the sweep and mobilizes exactly those ids), then handles whatever's genuinely mobilizable —
  open tickets on the resolved backend (GitHub issues, local docs/tickets/, or an Option-C
  adapter) labeled feature, bug, or task with no build in flight and no open `Blocked-by:`
  dependency (#193) — never a `backlog`/`roadmap`-parked ticket (#611; a ticket-id list naming
  one still mobilizes it) — a blocked ticket whose blocker is itself mobilizable gets the blocker
  dispatched dependency-first instead of a bare skip (#558) — after one batched confirm (a
  leading `auto` argument skips it, for /goal loops and scheduled runs).
  Every confirmed ticket, regardless of kind, dispatches uniformly to the build-leader agent
  (ADR-0010), whose dispatch-ticket procedure owns the kind branch; an
  under-specified task comes back SKIPPED — no clarify round runs unattended. Everything else
  (ops/hygiene actions, human-decision items) is skipped, never mobilized.
  NOT for just checking the queue (/sweep-chores); NOT for building one specific,
  already-known ticket (/build-feature or /file-bug directly); NOT for filing a new bug or
  feature (/file-bug, /file-feature); NOT for the hygiene execution (repo-cleaner, already run
  inside the sweep this wraps).
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a full sweep-and-mobilize | 'auto' to skip the confirm round for unattended/loop use | a scope instruction, optionally prefixed with 'auto ' | a comma/space-separated ticket-id list ('423, 426' or 'auto 423 426') to mobilize only those ids, skipping the sweep]"
allowed-tools: ["Read", "Glob", "Write", "Edit", "Bash(gh issue list *)", "Bash(gh issue view *)", "Bash(gh issue comment *)", "Bash(gh api graphql *)", "Bash(gh repo view *)", "Bash(node harness/scripts/chore_sweep_apply.mjs *)", "Agent", "Workflow", "Skill", "AskUserQuestion"]
---

# mobilize-chores

`/sweep-chores` reports; this command reports AND drives. It wraps `/sweep-chores` unmodified —
never reimplements its fan-out — and adds one new, separately-gated step: mobilize whatever the
sweep surfaced that's actually buildable.

## Procedure

0. **Parse `$ARGUMENTS` for the unattended flag, then classify what's left.** If `$ARGUMENTS`
   starts with the literal whitespace-delimited token `auto` (case-sensitive) — bare `auto`, or
   `auto <scope instruction>` — this run is UNATTENDED: strip that leading token and carry only
   the remainder forward as the scope instruction (empty remainder → full sweep, same as blank
   `$ARGUMENTS` today). Skip step 4's `AskUserQuestion` entirely; see step 4's UNATTENDED branch.
   No leading `auto` token → this run is INTERACTIVE, today's existing behavior, completely
   unchanged: the whole of `$ARGUMENTS` is the remainder. This is the literal entry point a
   `/goal` loop or scheduled routine calls (`/mobilize-chores auto`) to get a confirm-free pass —
   never inferred from "no human appears to be watching," always this explicit token, so the same
   invocation behaves identically whether a human or a loop types it.

   **Then classify the remainder itself (#449).** Split it on commas and whitespace into tokens.
   A non-empty remainder where EVERY token matches a ticket-id shape — a bare integer, `#` +
   integer, or `tkt-####` (case-insensitive) — is a **TICKET FILTER**, never a scope instruction:
   `/mobilize-chores "423, 426, 427"` and `/mobilize-chores auto 423 426` both name tickets to
   mobilize, not a seat or hygiene scope for the sweep to narrow onto. Anything else (blank, a
   seat name — `reviewer`/`planner`/`product`/`repo-cleaner`/etc. — a prose hygiene instruction,
   or a MIX of id-shaped and non-id-shaped tokens) is a **SWEEP SCOPE**, forwarded to
   `sweep-chores` exactly as before this fix — only a seat-name (or other sweep-shaped) scope
   ever reaches step 1's `Skill` call. On a TICKET FILTER, step 1 does not run the sweep at all
   and step 2 discovers only the named ids, never the full backend listing.
1. **Sweep — SWEEP SCOPE only.** On a TICKET FILTER (step 0), skip this step entirely: report "0.
   sweep skipped — ticket filter `<ids>` named directly" and go straight to step 2's per-id
   discovery below. Otherwise invoke harness's `sweep-chores` skill directly —
   `Skill(skill: "harness:sweep-chores", args: "<the step-0 scope instruction>")` — carrying the
   step-0 scope instruction verbatim (empty → full sweep). Issue #266 retired the `chore-lead`
   coordinator agent this step used to dispatch
   (its whole job was a deterministic dispatch graph — #265 measured that model-in-the-loop chain
   at 1.92× output tokens / 3.6× wall-clock vs. solo for equivalent outcome quality); `sweep-chores`
   now carries that choreography directly and was reclassified from command-only
   (`disable-model-invocation: true`, unreachable via the Skill tool — verified 2026-08-08, issue
   #134) to a "both"-invocable procedural skill for exactly this reason, so this step can invoke
   the identical procedure by name instead of duplicating it (the same cross-plugin Skill-tool
   pattern `dispatch-ticket` itself already uses to hand a bug-kind ticket to docs' `file-bug`) —
   never a hardcoded `${CLAUDE_PLUGIN_ROOT}` path or a duplicated fan-out, which would be the
   hard-plugin-boundary defect `plan-plugin-split`'s `surface_map.py check` exists to catch. This
   IS running `/sweep-chores`, mechanically, not a workaround — its own banner check, scope
   resolution, Workflow-preferred/Agent-fallback fan-out, and `chore_sweep_apply.mjs` payload
   application all run inline in this session since a Skill-tool call has no isolated context of
   its own; relay `sweep-chores`' report as this step's findings.
2. **Find mobilizable tickets.** Resolve this repo's ticket backend once (`doc-writing-rules`'
   backend resolver, `references/backend-resolver.md`, where `docs` is installed; not installed,
   or no ruling → git-native, this workspace's own ADR-0002 instance, unchanged from before this
   resolver call). **On a TICKET FILTER (step 0), discovery is narrowed to exactly the named
   ids** — read each one directly (git-native: `gh issue view <id> --json
   number,title,labels,assignees`; local: `Read` that ticket's file; adapter: its own `read`
   operation) instead of listing the full backend by label; an id that fails to resolve (no such
   issue/file/record) is reported in step 6 as "not found," excluded, never silently dropped. Every
   other exclusion below (label ambiguity, active claim, in-flight PR, `Blocked-by:`) still applies
   to each named id exactly as it would in a full sweep — a filter only narrows WHICH ids are
   considered, never which checks run on them — with ONE deliberate exception (#611): the
   `backlog`/`roadmap` parking exclusion does NOT apply to a filter-named id. Naming a parked id
   explicitly is exactly how parked work gets picked up; every other check (label ambiguity,
   claim, in-flight PR, `Blocked-by:`) still runs on it, and its pickup pays `dispatch-ticket`'s
   Phase 3.5 de-stale before any build. Otherwise (SWEEP SCOPE) discover per the resolved
   backend:
   - **Git-native (Option B):** `gh issue list --state open --label feature --json
     number,title,labels,assignees`, the same for `--label bug`, and the same for `--label task`.
     For each candidate, check whether an open PR already references it via `gh api graphql`
     querying `closedByPullRequestsReferences { nodes { number state } }` for that issue
     (owner/repo from `gh repo view --json nameWithOwner`) — any node with `state: OPEN` means a
     PR is already in flight for it, exclude. **The flattened `gh issue view --json
     closedByPullRequestsReferences` form does NOT carry a `state` field at all** (verified
     2026-08-07: it silently returns exit 0 with no state key present, reading as "never in
     flight" regardless of the truth) — the GraphQL form is the only one that actually works; do
     not substitute the flattened form. **Branch-name fallback (#736, 2026-08-19)** — the
     GraphQL check above only sees a PR that actually carries a `Closes #<id>` (or
     `Fixes`/`Resolves`) reference; a peer PR whose own dispatch path never wired that link is
     invisible to it entirely. Live incident: an agent-ui `/goal` wave had five tickets in active
     build (worktrees + open PRs), none of the PR bodies carrying a `Closes` link and none of the
     tickets carrying an assignee (that dispatch path skipped the ADR-0005 claim too) — the
     GraphQL check read all five as "0 open PRs," and only a live worktree/branch listing caught
     the collision before double-dispatch. ALSO list every open PR's head branch (`gh pr list
     --state open --json number,headRefName,url`) and match the candidate id against it under
     one of this convention's three observed shapes — `bug/<id>` (this skill's own bug-kind claim
     convention, `dispatch-ticket` Phase 3), `<id>-*` (the feature/task claim convention, same
     phase), `fix-<id>-*` (a repo-observed variant) — any match excludes the candidate as
     **"in flight (branch-name match, no Closes link)"**, and separately queues a hygiene finding
     naming that PR for the missing `Closes` link (a finding for step 6's report, never a mutation
     this step performs). **False-positive guard, load-bearing:** an id-shaped substring match
     alone is not enough — id `42` must never match branch `423-fleet-bootstrap-phase1` (`42` is
     a true substring of `423`). Require a non-digit (or string-boundary) delimiter on the side of
     the id that isn't the pattern's own literal — the character immediately after `<id>` in the
     branch name must be non-digit or end-of-string, never another digit — so a match is
     word-boundary-discipline, never a bare substring test. **Also exclude a ticket carrying a non-empty `assignees`
     array** (2026-08-12, #184) — `dispatch-ticket`'s own Phase 3 now takes ADR-0005's `claim`
     operation (assignee + a timestamped comment) before any build effort starts, closing the
     window this check used to miss entirely: a ticket claimed but not yet PR-open was invisible
     to the old open-PR-only check, so two concurrent mobilize runs (or a mobilize run plus a
     human pickup) could double-dispatch it (staleness handling: Failure branches, below). **The
     `in-flight` label (`gh issue list --label in-flight`, #199) may ride along as a cheap
     pre-filter on top of this** — labels are exactly one `gh issue edit` away from being wrong, so
     this step still trusts the `assignees` array (and the GraphQL PR check above) as the actual
     correctness gate. A ticket the label flags still gets that confirmation before being excluded
     — the label only ever changes the order candidates get checked in, never the answer, so a
     stale hand-applied label can't silently drop a real candidate on its own.
   - **Local (Option A):** `Glob` `docs/tickets/*.md`, `Read` each file's frontmatter. A candidate
     carries `status: open` and a `kind` of `bug`/`feature`/`task` (the same convention
     `file-bug`/`file-feature`/`file-task` write under this option — `doc-writing-rules` SKILL.md's
     TICKET section). **Also exclude a candidate carrying `claimed-by` frontmatter** (2026-08-12,
     #184) — `dispatch-ticket`'s Phase 3 realizes ADR-0005's `claim` on this backend via that same
     pair. **No in-flight-PR check exists for local tickets** — there is no established local
     convention linking a TICKET file to an open PR, so a local ticket already being worked cannot
     be excluded that way (the claim check above narrows, but does not close, this gap: a claim
     only appears once a dispatch has actually started). This is a disclosed limitation, not a
     silent gap: name it in the step-6 report rather than skipping the check unremarked.
   - **External adapter / Option C (e.g. Linear):** the seven-operation adapter interface
     (`backend-resolver.md`) has no "list open records filtered by kind" primitive today —
     ticket-discovery for this backend is **not yet supported**. Report it UNMEASURED, naming the
     resolved adapter, exactly like the `gh issue list` unreachable failure branch below; never
     silently return zero tickets found.

   Regardless of backend, a ticket is mobilizable only if: labeled/kinded exactly ONE of
   `feature`/`bug`/`task` (never unlabeled, and one carrying more than one of these three is
   ambiguous — exclude it, per the failure branch below), AND carries no active claim (git-native:
   empty `assignees`; local: no `claimed-by`), AND (git-native only) no
   `closedByPullRequestsReferences` node reads `OPEN`, **AND carries no open `Blocked-by:`
   dependency (#193)** — a THIRD, independent exclusion alongside the `in-flight` label pre-filter
   (#199) and the open-PR check just named; neither changes or subsumes this one, **AND carries
   neither parking label — `backlog`/`roadmap` (#611; git-native: the `labels` array already
   fetched by this step's `--json` calls, a post-filter costing zero new `gh` calls; local/adapter
   backends: no parking realization defined yet — disclosed in the step-6 report as N/A, never
   silently assumed) — SWEEP-DISCOVERED CANDIDATES ONLY: a TICKET FILTER-named id bypasses this
   one check per the exception carved out above, since naming a parked id explicitly is exactly
   how parked work gets picked up; verbatim application of this predicate to a filter-named id
   would silently defeat #611's entire pickup mechanism.** Cross-check
   `plan.md`'s own queue for the same ids; a ticket the sweep already flagged as a human-decision
   item or a blocker is excluded even if it carries a mobilizable label/kind — the sweep's own
   judgment on THAT item stands.

   **Reading the `Blocked-by:` dependency** — format and per-backend realization live once,
   canonically, in `references/blocked-by-convention.md` (this skill's own definition, cited here
   rather than restated — the same file harness's `chore-planner` cites for its own ordering
   rule): resolve each candidate's own `Blocked-by:` line and its named blockers' state per that
   file's realization table. ANY named blocker still open excludes the candidate from the PLAIN
   mobilizable set — it then enters chain resolution per `references/unstick-ordering.md`, which
   classifies each blocker (that file's B0–B5 taxonomy) and emits unstick candidates, sequenced
   dependents, and the still-stuck set (#558) — never silently dropped. All named blockers closed,
   or no line present → the exclusion doesn't apply; the candidate proceeds through the rest of
   this step's checks normally.
3. **Nothing mobilizable → stop here.** Stops only when the plain mobilizable set AND the unstick
   candidate set (`references/unstick-ordering.md`) are both empty. Report the sweep's own
   findings (step 1) plus "0 tickets mobilizable this run" and why (no open feature/bug/task
   tickets, or all already in flight or still-stuck with no unstick candidate). No confirm round,
   no further steps — an empty mobilize pass, including one that only surfaces a
   still-stuck-and-why report, is a normal, quiet outcome (#558).
4. **One batched confirm — INTERACTIVE only (step 0 found no `auto` token).** List every
   mobilizable ticket found (id, title, kind) in ONE `AskUserQuestion` round — never per-ticket,
   never split by kind. **The same round gains a second listed section for unstick chains
   (#558):** each chain resolved by `references/unstick-ordering.md` renders as ONE entry —
   "unstick chain: #B (blocker, dispatches now) → #A (sequenced; dispatches this run only if #B
   closes in-run via the ADR-0012 quick-build carve-out, else next run)", multi-level chains
   rendering the full ordered path (`#C → #B → #A`). Confirming the entry confirms the WHOLE
   chain — the blocker's dispatch plus the dependent's conditional dispatch — so no second round
   ever exists; declining declines the chain whole. A human wanting only one member of a chain
   re-runs with a ticket filter naming it directly. The human picks which entries (plain tickets
   and/or chains) to mobilize now, all, some, or none. Nothing
   dispatches before this round returns. A disclosed limitation of the uniform dispatch, stated
   here because this round is the one place to act on it: `dispatch-ticket`'s task-clarifying
   round requires an interactive user and `build-leader` is an unattended seat, so NO clarify round
   runs inside step 5's dispatches — an under-specified task comes back SKIPPED, and clarifying it
   means the human re-runs the named command interactively afterwards. Flag visibly
   under-specified task tickets IN this confirm round (one line each), so the human can decline
   them here instead of paying a dispatch that will skip.

   **UNATTENDED (step 0 found a leading `auto` token): skip `AskUserQuestion` entirely.** Every
   ticket step 2 found mobilizable, AND every unstick chain `references/unstick-ordering.md`
   resolved, is auto-confirmed — step 2's own filtering (label ambiguity
   excluded on every backend; on git-native, in-flight PRs also excluded via the GraphQL check
   AND the branch-name fallback (#736); the sweep's own human-decision/blocker items excluded on
   every backend), now including the
   unstick-ordering classification (#558), is the actual
   correctness gate, not this step, on either branch — this step was never the gate even for a
   human, only a selection point over an already-filtered set. **Option A (local tickets) has no
   in-flight-PR check at all — step 2's own disclosed limitation.** On that backend, UNATTENDED
   dispatches without the one guard INTERACTIVE mode also never had (the confirm round showed only
   id/title/kind, never in-flight state) — name that specific gap per ticket in the step-6 report
   rather than letting the summary imply a check that doesn't run there. An unattended dispatch's
   ceiling is **PR-opened by default, with ONE carve-out**: a dispatch meeting ADR-0012's
   quick-build predicate in full — the explicit `auto-merge: authorized` grant line this step
   placed (step 5), plus `size:small`, one plugin, one substantive file inside QB4's allow-list, a
   green critic, a green local gate, green CI, and no overlapping open PR — may land MERGED.
   Everything else still waits for a human, and merging stays a human act (ADR-0002's merge gate,
   unamended — the carve-out keeps the PR and every gate, it only pre-authorizes the click).
   Unsticking a blocker never widens this ceiling, never opens a second auto-merge path, and never
   automates review: nothing here, in `build-leader`, or in `dispatch-ticket`
   approves or reviews a PR on its own. Still
   name every visibly under-specified task ticket in the step-6 report exactly as the interactive
   branch would have flagged it in the confirm round — it comes back SKIPPED from `build-leader` (no
   clarify round runs unattended either way), never silently dispatched on a guess.
5. **Dispatch every confirmed ticket, uniformly.** Each confirmed ticket, regardless of kind →
   `Agent(subagent_type: "teamwork:build-leader")` carrying the confirmed ticket id. `build-leader`'s
   preloaded `dispatch-ticket` procedure (ADR-0010) owns the kind branch — its own body is the
   authoritative map, not restated here — and its unattended failure branches (an ambiguous
   record match reports as a named blocker; an under-specified task reports SKIPPED with no
   clarify round, never guessed at) apply automatically, since this dispatch never has an
   interactive user. Relay each returned typed result (path/URL, status, what shipped, a
   recorded blocker, a SKIPPED gap, or a `stale-premise` report with its evidence, #611) as that ticket's mobilized outcome — the same output a
   human running `/build-feature <id>` would see. `build-feature` stays
   `disable-model-invocation: true` — per-ticket dispatch genuinely needs `build-leader`'s own
   isolated agent context (parallel, independently-isolated builds), unlike step 1's sweep, which
   needs no isolation of its own and so was reclassified to a directly Skill-tool-reachable
   procedure instead (issue #266) rather than kept as a two-piece command+agent pair — two
   different fixes to the same disable-model-invocation-blocks-Skill-tool class (issue #134/#135).

   **On the UNATTENDED branch only, write the grant line into each dispatch prompt** — the literal
   text `auto-merge: authorized`, on its own line, typed out in the sealed prompt. It is a field
   this step SETS, never a property the receiving seat infers: `dispatch-ticket`'s stage 2b reads
   for that exact line and treats its absence as "this stage does not exist." Its authority traces
   to the `auto` token Kim typed at step 0 — the same explicit-never-inferred doctrine — and
   omitting the line is the entire revocation mechanism, needing no other edit. **The INTERACTIVE
   branch never places it**: a human who just sat through the confirm round is present to merge.
   The line authorizes only the merge CLICK on an all-green predicate; it grants nothing about
   review, and skips no critic, gate, or PR.

   Every dispatch is independent — one failing never blocks the others. **Isolation is no longer
   this step's decision** (2026-08-12, #183 — incident and rationale in this skill's own
   `intent.md`, not restated here): `dispatch-ticket`'s own Phase 3 now puts EVERY dispatch that
   can mutate the tree — a lone serial one included, and the bug-kind hand-off into `file-bug`
   too, since `file-bug`'s own Phase 5 can fix a root-cause-evident bug INLINE — inside its own
   git worktree, unconditionally, before any effort starts. This is structural inside
   `dispatch-ticket` now (its Phase 3 isolates before the bug hand-off itself, precisely because
   `file-bug`'s own body carries no worktree mechanics of its own to rely on), not a call this
   step makes per dispatch or per kind.

   What a named target path still decides — the one thing per-dispatch worktree isolation does
   NOT solve on its own — is PARALLEL-vs-SERIAL **timing**, never isolation-vs-none: two dispatches
   editing the SAME files in separate worktrees still build cleanly each, then produce two
   branches that conflict at PR/merge time. If each confirmed feature/task-kind ticket's own body
   already names a concrete edit target (the actual file(s) or leaf directory the change will
   touch — a doc-citation `## Links` section doesn't count, nor does a bare plugin-level
   directory) and those targets neither overlap nor contain one another, state that claimed
   ownership in the step-6 report and dispatch both concurrently — real parallel time, no expected
   merge conflict. Two tickets with no such named target on both sides, or overlapping ones — the
   common case, since a ticket's real footprint usually isn't known until `dispatch-ticket`'s own
   Phase 4 size/plan step actually runs, which hasn't happened yet at THIS dispatch point — run
   SERIALLY instead: this choice is purely about avoiding a self-inflicted, foreseeable merge
   conflict, not about tree-mutation safety, which per-dispatch isolation already guarantees on
   either branch. Each serial dispatch starts from a clean `main` HEAD — a predecessor that left
   the tree dirty or on its own feature branch is the NEXT dispatch's named blocker, never
   silently inherited (should no longer happen for a feature/task predecessor post-#183, since
   each retires its own worktree/branch per its own Phase 5 stage 3 — a bug-kind predecessor never
   reaches Phase 5 at all, so this is checked regardless of kind, never assumed clean either way).
   Never assume
   disjointness without a named, non-overlapping target on both sides — `parallel-work-rules`' own
   rule holds here too: unconfirmed disjointness routes to the safer (serial) default, not to an
   assumption.

   **Wave re-check (#558) — bounded, read-only, never a wait.** After all of a wave's dispatches
   RETURN, run one read-only re-check pass over any sequenced dependents from an unstick chain
   (`references/unstick-ordering.md`): re-read each named blocker's state once. All named
   blockers now CLOSED → the dependent was already confirmed conditionally in step 4, so it
   dispatches in the next wave; anything short of all-CLOSED stays sequenced-for-next-run. Max 3
   waves total; a pass that unlocks nothing ends the loop immediately. Never sleep, never watch a
   PR (`gh pr checks --watch` or equivalent), never re-poll an id already re-read this pass — a
   chain member's dispatch carries no extra authority of its own: the quick-build predicate and
   the `auto-merge: authorized` grant line are evaluated by `dispatch-ticket` stage 2b exactly as
   for any other ticket, and unsticking never constitutes a second auto-merge path or any review
   act.
6. **Report.** Verdict-first: name which branch ran — INTERACTIVE, or UNATTENDED with the exact
   `auto`-prefixed argument as parsed in step 0 — so a step-0 misparse (a scope instruction that
   happens to start with the literal word "auto") is observable in the artifact of record, never
   silent. Then the sweep's own findings, then a table of every ticket CONSIDERED this run —
   mobilized (dispatch + outcome: succeeded / failed / still in flight), a `stale-premise` result
   (#611 — a relayed `build-leader` outcome distinct from SKIPPED and from a named blocker; one-line
   evidence summary in the table, no breakdown paragraph — nothing is blocking it, the ticket
   itself is wrong, and the evidence already sits on the record), or skipped-and-why (not
   confirmed, in flight already — an open PR, or a claim with no PR open yet (#184) — blocked by
   an open `Blocked-by:` dependency (#193, naming the still-open blocker id) — parked
   (`backlog`/`roadmap` label, #611 — step 2's own label-list call fetches these ids same as any
   other candidate, then excludes them via its post-filter; this row is that exclusion made
   visible, not a stale hand-check — named here so a boundary case is observable, not invisible) —
   wrong/ambiguous label, too vague to build unattended — the seat SKIPPED, no clarify round
   available on this path — or excluded by the sweep's own judgment).

   **Unstick outcome vocabulary (#558).** A ticket caught by step 2's `Blocked-by:` exclusion is
   reported under exactly one of three classes instead of the old bare "blocked" row:
   `unstuck-this-run` (a dependent actually dispatched in wave ≥ 2, or a blocker whose own
   dispatch and dependent's dispatch both landed this run), `sequenced-for-next-run` (a blocker
   dispatched or already in-flight; the dependent waits on its close), or `still-stuck-and-why`
   (an unresolvable, cycle, too-deep, or human-shape blocker — `references/unstick-ordering.md`'s
   B1/B2/B4 classes). Each row cites the classifying B-class (B1–B5) so a misclassification is
   observable in the artifact of record. A cycle gets ONE paragraph naming every member, never one
   per member. A TICKET FILTER run that pulled in an off-filter blocker via a chain names it
   "pulled in by #A's chain" rather than reporting it as an unrelated candidate.

   **Blocker breakdown.** Every ticket whose outcome is a named blocker (`dispatch-ticket`'s own
   distinct outcome, not a plain SKIPPED) — plus, as of #558, every `still-stuck-and-why` ticket —
   gets one paragraph, not just a table row: the ticket id
   and title, what's actually blocking it (`build-leader`'s own stated reason, quoted or
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

- `/sweep-chores` itself fails to return (SWEEP SCOPE only) → report that failure plainly; never
  run steps 2–6 against a sweep that didn't happen. A TICKET FILTER run legitimately skips the
  sweep by design (step 1) — this branch never applies there.
- The resolved backend's own listing call is unreachable (`gh issue list` fails on git-native; a
  Glob/Read error on local; the adapter call errors on Option C) → report ticket-discovery as
  UNMEASURED for this run; the sweep's own report still stands on its own.
- Option C is resolved but the seven-operation adapter interface carries no listing primitive
  (today's state, per step 2) → report ticket-discovery UNMEASURED for that backend, naming the
  adapter; not a failure to fix here, a documented gap to close in the adapter interface later.
- A ticket's label or in-flight state is ambiguous (e.g. `linkedBranches` present but that branch
  has no open PR) → exclude it from the mobilizable set; ambiguity is never a license to dispatch.
- A ticket carries an active claim (non-empty `assignees`/`claimed-by`, per ADR-0005) with no open
  PR yet (2026-08-12, #184) → exclude it from the mobilizable set exactly like an open in-flight
  PR; report it as "in flight already" in step 6, not as a fresh candidate. A claim past its
  staleness window with no linked PR is `repo-cleaner`'s stale-claim finding to raise (ADR-0005
  Decision 6) — this step only excludes on the claim's presence, it never reclaims one.
- A ticket's `Blocked-by:` line names an id that doesn't resolve (deleted issue, typo, `gh`
  unreachable for that lookup) → treat as OPEN, the same fail-closed default
  `blocked-by-rules` uses on its own read side, and exclude — reported in step 6 as "blocked —
  #NN unresolvable, treated as open," never guessed at or silently dropped
  (`references/unstick-ordering.md`'s B1 class). All named blockers already closed → not blocking;
  the candidate proceeds normally (#193).
- A blocker chain contains a cycle, or exceeds the 5-level depth cap → report the whole cycle (or
  the too-deep chain) as one `still-stuck-and-why` paragraph, naming every member; NEVER dispatch
  any member of it (`references/unstick-ordering.md`'s B2 class, #558).
- The confirm round returns "none" → report 0 mobilized, same as step 3's empty case; not a
  failure.
- `build-leader` returns a SKIPPED (a task not concretely actionable — no clarify round runs in an
  unattended dispatch) → relay it as that ticket's outcome in the step-6 table; the skip
  discipline itself lives in `dispatch-ticket`'s own failure branches, not re-litigated here.
  A named blocker gets more than a table row — step 6's blocker-breakdown paragraph, not just
  the row.
- `build-leader` returns with no Findings-equivalent entry visible on the ticket read-back → one
  re-dispatch of the SAME seat with `dispatch-ticket`'s contract quoted, then a recorded loss on
  the ticket if still nothing — the caller-side check that the seat's own write-back contract
  actually landed.
- UNATTENDED run auto-confirms a ticket step 2 flagged as visibly under-specified (no human was
  there to decline it) → dispatch it anyway; it returns SKIPPED from `build-leader` per that seat's
  own unattended contract, the identical outcome a human declining it in step 4 would have
  produced — never treated as an error unique to the unattended path.
- **A TICKET FILTER names an id that doesn't resolve** (#449) → report "not found" for that id in
  step 6, exclude it, and continue with the rest of the filter; never fail the whole run over one
  bad id. A remainder MIXING id-shaped and non-id-shaped tokens (step 0) is a SWEEP SCOPE, not a
  filter — it forwards to `sweep-chores` whole, exactly like a seat name or prose scope.

Done when, on a SWEEP SCOPE, `/sweep-chores` has run (via the direct Skill-tool call step 1
names, not a duplicated fan-out) — or, on a TICKET FILTER (#449), step 1 states the sweep was
skipped and step 2 discovered each named id directly, never forwarding the id list into
`sweep-chores`' own seat-scope slot — and every ticket IN THIS RUN'S SCOPE has been considered
(a SWEEP SCOPE's scope is every open `feature`/`bug`/`task` ticket; a TICKET FILTER's scope is
exactly its named ids, plus any blocker ids its unstick chains pulled in per
`references/unstick-ordering.md`, each disclosed in step 6 as "pulled in by #A's chain" (#558))
with no build
in flight, no active
claim, AND no open `Blocked-by:` dependency (#193) left unresolved by chain classification, every
dispatch was gated
by the human's one batched confirm
(INTERACTIVE) or by step 2's own filtering under the explicit `auto` token (UNATTENDED) — never by
neither — and the final report names every considered ticket's outcome — a mobilized ticket's
relayed `build-leader` result, a skip-and-why, one of the three unstick outcome classes (#558:
unstuck-this-run / sequenced-for-next-run / still-stuck-and-why), or (for a named blocker or a
still-stuck ticket) the classified breakdown paragraph, never just a table row. NOT done while a
dispatch fires before the confirm round on an
INTERACTIVE run, a named blocker or still-stuck ticket gets only a table row with no classified
paragraph, a blocker
breakdown proposes a build attempt instead of the shape its category actually calls for, an
unlabeled item is mobilized, a confirmed ticket is dispatched anywhere but `build-leader` (the
per-kind routing that once lived here belongs to `dispatch-ticket` now — re-growing it here is the
regression), a ticket already in flight OR already claimed OR carrying an open `Blocked-by:`
dependency with no B5-mobilizable resolution is dispatched anyway, a cycle member or human-shape
(B2/B4) blocker is EVER dispatched, a dependent is dispatched while any of its named blockers
still reads OPEN, a second confirm round is opened for a chain, any wait/watch/poll on a PR runs
between waves, the wave loop runs past 3 waves, or any unstick action other than the single
`build-leader` dispatch is taken (a `Blocked-by:` line edited, a label changed, a stale claim
reclaimed, a ratify comment posted), two concurrent
feature/task dispatches with overlapping or unstated edit targets are pushed to run in parallel
instead of the safer serial default (isolation itself is no longer this step's call — that's
`dispatch-ticket`'s own unconditional Phase 3, per #183 — but a foreseeable merge conflict from
overlapping targets still is), a dispatch leaving no Findings-equivalent entry goes unnoticed, step
1 duplicates the fan-out in its own prose instead of the direct `Skill(harness:sweep-chores)` call, or an UNATTENDED run
is inferred from context rather than the explicit `auto` token, or a TICKET FILTER (#449) is
forwarded into `sweep-chores`' own seat-scope slot instead of narrowing step 2's discovery
directly, or a parked (`backlog`/`roadmap`-labeled) ticket is mobilized from a SWEEP SCOPE (a
TICKET FILTER naming it explicitly is the one legitimate path, #611).
