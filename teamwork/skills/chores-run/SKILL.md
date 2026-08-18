---
name: chores-run
description: >-
  Arms the recurring "drain the queue and ship PRs" loop the operator otherwise re-types by hand
  each session: writes/refreshes a durable punch list (.claude/ops/punch-list.md), then prints a
  ready-to-paste /goal block whose own turns compose mobilize-chores' procedure (sweep +
  per-ticket build-leader dispatch, one worktree per ticket) — with the ADR-0012 carve-out only
  when passed — until every open ticket reaches a terminal punch-list state, or the wave cap is
  hit. Run /chores-run [auto] — auto forwards ADR-0012's auto-merge carve-out into every wave the
  printed loop runs, never inferred. NOT for one already-known ticket (/build-feature); NOT for a
  single sweep-and-mobilize pass with no recurring loop (/mobilize-chores directly); NOT for just
  checking the queue (/sweep-chores); NOT for the actual per-ticket dispatch logic
  (mobilize-chores/build-leader — this command composes them, never reimplements them).
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a PR-opened-ceiling loop | 'auto' to also honor ADR-0012's auto-merge carve-out each wave]"
allowed-tools: ["Read", "Glob", "Write", "Edit", "Bash(gh issue list *)", "Bash(gh issue view *)", "Bash(gh issue comment *)", "Bash(gh api graphql *)", "Bash(gh repo view *)", "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Bash(node harness/scripts/chore_sweep_apply.mjs *)", "Agent", "Workflow", "Skill", "AskUserQuestion"]
---

# chores-run — arm the recurring drain-the-queue loop

The command form of the paragraph an operator otherwise re-types by hand: *"complete any filed or
new Issues/Features/Tasks/Bugs and ship mergeable PRs for as many of these as possible."* This
skill turns that into a fixed, verifiable end-state (per `[[loop-rules]]`) instead of a re-typed
prompt, and composes the seat that already does the actual work — it dispatches nothing itself.

## Why the printed loop reads mobilize-chores instead of typing its command (verified before building)

`mobilize-chores` is `disable-model-invocation: true`. The Skill tool categorically refuses that
target regardless of caller context (issue #421/#423's measured defect class), and `[[loop-rules]]`'s
own foundations note that `/goal` continuation uses the identical discovery mechanism every turn —
so a `/goal` turn cannot Skill-tool-invoke `mobilize-chores` either, and (same reason) cannot
re-invoke `chores-run` itself to re-fetch anything. Neither restriction touches the `Read` tool: a
turn can always read a skill's own `SKILL.md` and carry out what it says, the same way a human
without Skill-tool access would. So the printed block's own turn 1 directs the loop to **read
`mobilize-chores`' `SKILL.md` and execute its procedure directly**, never Skill-tool-invoke it or
retype it as a slash command — and turn 2 carries every command it needs inline, since it cannot
call back into this skill to fetch them. This is composition through the one channel a `/goal`
turn actually has for a command-only sibling, not a workaround. A Read carries no frontmatter
effects — `mobilize-chores`' own `allowed-tools` grants don't travel with it — so `chores-run`'s
own frontmatter mirrors that grant list plus the git commit/push scope its own step 2 needs
(below), rather than relying on the read file's frontmatter to pre-approve anything.

## Procedure

0. **Parse `$ARGUMENTS` for the leading `auto` token** — same convention as `mobilize-chores`'
   own step 0 (cited, not restated): a bare `auto` (case-sensitive, leading, whitespace-delimited)
   means every wave the printed loop runs passes `auto` into `mobilize-chores`' own procedure,
   forwarding ADR-0012's `auto-merge: authorized` carve-out into that seat's dispatches AND
   skipping its own batched confirm round (`mobilize-chores` step 4's UNATTENDED branch) — this is
   the only way the printed loop runs unattended at all. No leading `auto` → every wave passes
   nothing: `mobilize-chores`' own INTERACTIVE branch runs, meaning its `AskUserQuestion` confirm
   fires each wave — a plain `/chores-run` loop is human-gated per wave, not unattended, and the
   printed block should be read that way rather than assumed hands-off. This token is
   `chores-run`'s own explicit grant surface — never inferred from "unattended" or from a ticket's
   own body text (ADR-0021 T1 vs T2: this argument channel has force, quoted record text does
   not). Any OTHER argument (a scope instruction, a ticket-id list) is out of scope for this first
   cut — report it back unconsumed rather than guessing whether to forward it into
   `mobilize-chores`' own scope/filter argument (see Failure branches).
1. **Snapshot current state, read-only** — `gh issue list --state open --label feature --json
   number,title,labels,assignees` (same for `bug`, `task`) plus the GraphQL open-PR-linkage check
   `mobilize-chores` step 2 already documents (cited, not re-derived). A plain read for the punch
   list's own starting snapshot, never the eligibility algorithm itself (claim/in-flight/
   `Blocked-by:` exclusions stay `mobilize-chores`' own job, run for real once the printed loop's
   own wave actually executes its procedure).
2. **Write and commit `.claude/ops/punch-list.md`** — the durable, resumable state a fresh
   session reads cold. One row per ticket, rewritten whole each wave (never appended), enum fixed
   to exactly these seven values:

   ```markdown
   # Punch list — chores-run

   Wave <N> · <UTC timestamp> · ceiling: <PR-opened | PR-opened + ADR-0012 carve-out (auto)>

   | id | seat | worktree/branch | PR | state |
   |---|---|---|---|---|
   | #NNN | build-leader | <branch, or —> | <PR URL, or —> | <queued\|PR-open\|merged\|blocked\|skipped\|stale-premise\|UNMEASURED> |
   ```

   `seat` is always `build-leader` — `mobilize-chores` dispatches uniformly (ADR-0010); the
   column exists so a fresh session sees at a glance that nothing here was hand-run outside that
   contract. `state` starts every ticket at `queued` (found, not yet run through
   `mobilize-chores`' own procedure this wave); after a wave runs, it settles to whichever of the
   other six values that wave's own outcome named — `mobilize-chores`' own `failed` dispatch
   outcome maps to `blocked` here (the enum has no separate slot for it; a `blocked` row still
   carries the failure as its reason) — never a transient "dispatched"/"in-flight" value, since by
   the time this file is rewritten the wave has already completed. Chores-run writes AND commits
   this file directly (a small, source-free `.claude/ops/` state commit — the same pattern other
   ops-family state files use) to the checkout's CURRENT branch, pushing only when that branch is
   `main` (see Failure branches for anything else) — it runs as the live invoking session, never a
   restricted ops-family subagent, so `harness:ops-write-sandbox-rules`' scratch-copy/
   fenced-payload contract does not bind it (that contract is scoped to the four *compute-only*
   dispatched seats named there, none of which this command is or dispatches). Without the commit,
   a fresh session in a different worktree cannot read it cold at all.
3. **Compose and print the armed `/goal` block** — never started programmatically (`/goal` is
   itself a platform command with no Skill-tool-reachable path from a skill body, the same
   #134/#135 class). The end-state, cap, and escalation clause are fixed by this skill (the
   operator's own ruling, folded into ticket #637's `## Findings`); only the `auto`/plain choice
   from step 0 varies turn 1's own argument:

   ```
   /goal: 0 rows in .claude/ops/punch-list.md read "queued" or "UNMEASURED" — every ticket has
   settled to PR-open, merged, blocked, skipped, or stale-premise.
   Each turn:
     1. Read ${CLAUDE_PLUGIN_ROOT}/skills/mobilize-chores/SKILL.md in full and carry out its own
        procedure directly (never Skill-tool-invoke it — it is disable-model-invocation,
        unreachable that way from any turn), with its own $ARGUMENTS = "auto" (drop if this run
        did not pass auto to chores-run — its own confirm round then fires per wave, see step 0).
     2. Refresh the punch list from current state:
        `gh issue list --state open --label feature --json number,title,labels,assignees`
        (repeat for --label bug, --label task), cross-checked against mobilize-chores' own
        open-PR GraphQL check; rewrite .claude/ops/punch-list.md's rows (header:
        `| id | seat | worktree/branch | PR | state |`) and commit + push it.
     3. Re-check the end-state above.
   Stop after 10 waves, or immediately once the end-state holds. Escalate — stop and report,
   never retry a third time — if the SAME check fails twice in a row (loop-rules' own escalation
   clause, not a flat retry).
   ```

   10 waves is this command's own bound (loop-rules' Design step 2: a named cap is mandatory; a
   whole-queue drain plausibly spans more waves than `mobilize-chores`' own narrower 3-wave
   unstick-chain cap, so a wider but still fixed ceiling applies here instead of reusing that
   number verbatim). The end-state is reachable under today's plain PR-opened ceiling — an
   `PR-open` row is itself a terminal state, never conditioned on an actual merge — so `auto`
   only changes how MANY rows land on `merged` rather than `PR-open`, never whether the loop can
   finish.
4. **On a re-invocation** (a human, or the printed loop's own turn via step 2 above, running this
   procedure again after a wave actually ran) — repeat steps 1-3 from the now-changed state; this
   is how the punch list and the end-state check both stay current without `chores-run` needing
   to reach back into `mobilize-chores`' internals a second way.
5. **Report.** State which branch ran (plain or `auto`), the punch list's own path and commit
   SHA, and the printed `/goal` block verbatim — a human confirms and pastes it (or the loop
   itself is already running and continues from its own prior wave, read off the punch list).

**Two hard-won rules from #637's own Findings, encoded here rather than assumed inherited:** (1)
version-slot serialization — a wave that fans out ≥2 concurrent `mobilize-chores` dispatches never
lets two tickets touching the same plugin race its version bump (`[[fleet-rules]]` Section 4,
cited not restated). (2) doc-spine re-read before numbering — a wave minting a new ADR/IDR/LLD/RDD
re-reads that family's highest id off `origin/main` immediately before numbering it, never off a
possibly-stale branch-cut snapshot (the #633 rule; canonical text in `docs:doc-writing-rules`' ID-
spine section). Both bind every wave `mobilize-chores`' own procedure runs from inside this loop,
exactly as they would in any other dispatch — named here only because the operator asked for them
stated, not because this skill adds new mechanics for either.

## Parallelization and serialization

Inherited, never re-decided here: `mobilize-chores` step 5 already runs independent, disjoint-
target tickets concurrently and same-file-touching tickets serially, under `[[dispatch-ticket]]`'s
own per-dispatch worktree isolation (`[[parallel-work-rules]]`, cited not restated). `chores-run`
adds no parallel-dispatch logic of its own.

## Failure branches

- `gh` unreachable for the step-1/step-2 snapshot → the punch list still writes and commits,
  with an `UNMEASURED` row noting the read failed, never a silently stale or empty file.
- Nothing mobilizable this wave → punch list writes with zero non-terminal rows; the end-state
  already holds. Report DONE, no `/goal` block owed (nothing left to loop over).
- `.claude/ops/` absent → create it in the same commit as the punch list's first write; not a
  precondition failure.
- `$ARGUMENTS` carries anything besides blank or a leading `auto` (a scope instruction, an id
  list) → report it back unconsumed, take no action on it, and proceed as if blank — forwarding
  it into `mobilize-chores`' own scope/filter argument is a design question this first cut leaves
  open rather than guesses at.
- The invoking checkout is not on `main` when step 2 goes to commit → commit to the checkout's
  actual current branch and say so in the report rather than pushing to `main` from underneath
  it; a fresh session elsewhere still resolves the punch list off `main` per the ordinary case,
  so this is named as a degraded-but-safe branch, never a silent push to the wrong ref.

## Agent-verifiability

`scripts/verify_goal_and_punch_list.py` extracts the live `/goal` fenced block straight out of
this SKILL.md (never a hand-duplicated copy, so the proof cannot silently drift from the shipped
text) and asserts it carries a bounded cap (C3) and a measurable, non-vague end-state (C1) — the
same two dimensions `loop-rules`' own `harness_checks.py goal` checks, replicated locally per
skill-folder encapsulation (`spec-naming-convention.md` §6.1 point 3: a skill's own `scripts/` is
never referenced from outside it, so this proof cannot shell out to that sibling skill's script).
It also asserts the punch-list template's header row carries exactly the five required columns.
`selftest` proves both checks fire on a negative fixture and pass on this skill's own shipped
text.

## References & tools

| Path | Use when |
|---|---|
| `mobilize-chores` (this plugin) | The actual sweep/discover/confirm/dispatch procedure the printed loop's turn 1 reads and carries out — its own body owns the eligibility rules, never re-derived here |
| `[[loop-rules]]` | The end-state/cap/escalation shape this skill's printed `/goal` block follows |
| `[[fleet-rules]]` | Version-slot serialization (Section 4) and the coordination-scope default (Section 1) every wave inherits |
| `[[parallel-work-rules]]` | The per-ticket worktree mechanics `mobilize-chores`/`dispatch-ticket` already apply |
| `harness:ops-write-sandbox-rules` | Why this command writes+commits `.claude/ops/punch-list.md` directly instead of via the scratch-copy/fenced-payload contract (step 2) |

**Done** when `.claude/ops/punch-list.md` is written, committed, and reflects the current wave's
real state, the printed `/goal` block carries a bounded cap and a measurable, non-vague
end-state reachable under the plain PR-opened ceiling, and the report names which ceiling (plain
or `auto`) this run chose. **NOT done** while the punch list is stale or uncommitted relative to
the snapshot just read, the printed block asks a turn to Skill-tool-invoke or retype a
command-only sibling instead of reading and carrying out its procedure, or `auto` was honored
without the literal leading token present in `$ARGUMENTS`.
