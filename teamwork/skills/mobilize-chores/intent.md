# intent — mobilize-chores
status: shipped          # forging | parked | shipped
species: command
dials: { disable-model-invocation: true, user-invocable: true }
freedom: medium
type: encoded-preference

## trigger
should:      ["/mobilize-chores", "sweep and build whatever's ready", "work the ops queue", "run the sweep and start on what's actionable"]
should_not:  ["/sweep-chores", "what's in the ops queue?"]

## delta
Today `/sweep-chores` produces `.claude/ops/plan.md` (a prioritized queue via chore-lead ->
chore-planner) and stops — nothing acts on it. A human must separately read the queue, judge
what's build-ready, and manually invoke the right dispatch per item. `mobilize-chores` closes that
gap: after the sweep, it reads the queue, filters to genuinely mobilizable tickets, gets one
batched human confirm, then drives each confirmed item through its OWN kind's dispatch —
`kind: feature` -> `/build-feature <id>`; `kind: bug` -> `/file-bug <id>` (resuming an existing
bug record dispatches its investigation, per file-bug's own contract; build-feature explicitly
redirects bug-kind tickets away, it does not build them); `kind: task` -> `find-intent` clarifies
the confirmed ticket first (one round max, only if genuinely ambiguous), then an Agent-tool
dispatch (`general-purpose` as the default null case, a named agent only when tool restriction/
parallelism/multi-skill preload is actually needed) executes it under the same Findings-write-back
contract file-bug's own investigation dispatch uses (2026-08-08 addition — tasks have no fixed
execution verb the way features/bugs do, so clarify-then-dispatch is the shape, never a blind
dispatch on an unclarified brief). Any ops/hygiene action or human-decision item stays out of
scope and reports as skipped.

## fences
- NOT for just checking the queue/report (`sweep-chores`)
- NOT for building one specific, already-known ticket (`build-feature`/`file-bug` directly — this
  skill is for queue-driven multi-item pickup, not a single named item)
- NOT for filing a new bug/feature (`file-bug`/`file-feature`)
- NOT for the underlying hygiene execution itself (`repo-cleaner`, already run inside the sweep
  this wraps)

## assertions
1. The final report names every queue item considered, each with a verdict: mobilized, or
   skipped-and-why.
2. No dispatch (`build-feature` or `file-bug`) fires without one batched human confirm round
   first — never per-item confirms, never a silent auto-build.
3. A queue item mobilizes ONLY if it's a filed `kind: bug`/`kind: feature`/`kind: task` ticket,
   routed to its OWN kind's dispatch (`feature` -> `build-feature`, `bug` -> `file-bug`, `task` ->
   find-intent-clarify-then-Agent-dispatch, never crossed) — never an ops/hygiene action
   (agent dispatch, config edit) or a human-decision item, even one a reasonable ad hoc read would
   call "low-risk enough to just do." Every non-ticket item is reported as skipped, with the
   reason.
4. The report names which dispatches succeeded, failed, or are still in flight.
5. A `kind: task` ticket that's STILL too vague to act on after find-intent's one clarifying round
   is never dispatched blindly — it's reported skipped, with the gap named, exactly like an
   unconfirmed or in-flight item.

## gates
P0 route:      PASS — 2026-08-07 — primitive=skill, command species (real side effects: can
                trigger a build); dispatches existing capabilities (chore-lead, build-feature)
                rather than needing its own tool-walled identity, same shape as sweep-chores.
P1 intent:     PASS — 2026-08-07 — all 7 slots filled and confirmed by user.
P2 evals:      PASS — 2026-08-07 — trigger evals SKIPPED (disable-model-invocation: true, no
                model-routing decision to test); 4 behavioral assertions recorded (assertion 3
                sharpened post-baseline); baseline captured at evals/baseline/prompt-1-describe-
                plan.md against the real repo queue.
P3 draft:      PASS — 2026-08-07 — SKILL.md drafted from the Command skeleton, matching
                sweep-chores' own established shape (same plugin family); dials explicit; body
                well under the 500-line split threshold (no references/ needed).
P4 language:   PASS — 2026-08-07 — self-audited against the instantiation/affirmative-framing/
                numeric-anchor/contracts-in-head criteria; matches sweep-chores' own established
                Done/NOT-done pattern (an accepted house convention, not a hedge).
P5 validate:   PASS (2026-08-07 ship) — lint clean. Fresh-context skill-checker audit (FLOOR) found
                one blocking finding (R1): step 2's `linkedBranches`/`linked:<id>` mechanics were
                fictional against real `gh` — fixed with the auditor's verified fields, then
                RE-verified live against this repo's own real data (`gh api graphql` querying
                `closedByPullRequestsReferences{state}` — the flattened `gh issue view --json`
                form silently drops `state` entirely, a second real gotcha caught by hand-testing
                the "fix," not assumed correct). Live proof: issue #131 (kind: bug, filed since
                this forge started) correctly reads as mobilizable — empty
                closedByPullRequestsReferences. Two minor findings (allowed-tools gap,
                both-labels disposition) fixed same-pass. Fence closure: sweep-chores and
                build-feature both gained a one-line mobilize-chores mention for menu
                discoverability — no eval-suite reciprocity needed, all three siblings are
                disable-model-invocation: true (command-only, zero model-routing collision
                possible).
                RE-OPENED 2026-08-08 for the task-kind addition, RE-PASSED same day — lint clean.
                Fresh-context skill-checker re-audit (FLOOR) verdict PASS, no blocking findings;
                every gh CLI/tool reference in the new task branch verified against real behavior
                (including a live re-check of the closedByPullRequestsReferences state-field
                gotcha against issue #131). One major + three minor findings, all fixed same-pass:
                the fork-vs-agent purge had missed intent.md (delta + assertion 3 still said
                "fork/agent" after SKILL.md was already corrected to a concrete Agent-tool
                description — stale living-spec text, fixed); `gh issue close` was missing from
                allowed-tools (step 5 needs it to close done/wontfix tickets, distinct from
                `gh issue edit`); a null-unit-reasoning citation pointed at agent-writing-rules
                instead of team-or-solo-rules (this plugin's own solo-first doctrine); a
                misquote of file-task's scope ("chores, follow-ups, docs, decisions" vs. its real
                "chores, follow-ups, research items, debts") in both SKILL.md and intent.md.

## rulings
- 2026-08-07: considered folding this into `chore-lead`/`sweep-chores` directly instead of a new
  skill. Rejected — `chore-lead`'s own charter is explicit ("coordination only... mutates nothing
  itself") and that guarantee is what makes it safe to run unattended/scheduled. Folding execution
  in would break that guarantee for every existing caller, not just this new use. Decision:
  `mobilize-chores` wraps `sweep-chores` (calls it, doesn't reimplement it) and adds a new,
  separately-gated build step on top — composition, not a charter change.
- 2026-08-07: corrected during drafting — `build-feature`'s own body explicitly redirects
  `kind: bug` tickets away ("this is file-bug's work, hand it over"); it builds features only.
  Delta/fences/assertions updated to route by ticket kind: feature -> `build-feature`, bug ->
  `file-bug` (resuming a bug record dispatches its investigation, per that skill's own contract).
- 2026-08-07: owning plugin chosen as `teamwork` (not `harness`) — reinforces the same boundary:
  harness's ops-family stays plan/propose-only; teamwork is where build/execute orchestration
  (`build-feature`, `team-lead`) already lives. Cross-plugin calls to `harness:sweep-chores` are a
  soft, named mention (dispatched as a command), never a `skills:` preload — plugin boundaries stay
  hard for preloads, soft for mentions, per this workspace's CLAUDE.md invariant.
- 2026-08-08: task-kind mobilization added (Kim's explicit request, after first live run surfaced
  #138-140 as reported-skipped). Considered three shapes: (a) dispatch a general-purpose agent per
  task blind, (b) restrict to `size:small` tasks only, (c) run `find-intent` per confirmed task
  first, then dispatch based on what that clarifies. Kim chose (c) — tasks are deliberately
  heterogeneous (`file-task`'s own scope: chores, follow-ups, research items, debts), so no single fixed
  dispatch verb fits them the way `build-feature`/`file-bug` fit features/bugs; blind dispatch (a)
  risks executing a genuinely unclear brief, and size-gating (b) excludes big tasks that may be the
  most valuable to mobilize. Clarification runs ONLY on CONFIRMED tasks (after step 4's batched
  confirm, right before dispatch) — never on every discovered task — so no human attention is
  spent clarifying items that end up not selected. A task still vague after find-intent's one
  round is reported skipped rather than dispatched on an unclear brief (new assertion 5).
