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
batched confirm — a human `AskUserQuestion` round (interactive), or, with a leading `auto` token
in `$ARGUMENTS`, step 2's own filtering stands in as the gate instead (unattended, 2026-08-11
addition, for `/goal` loops and scheduled routines) — then dispatches every confirmed ticket
uniformly to `build-lead` (ADR-0010; renamed from the original `feature-lead`, 2026-08-10), whose
preloaded `dispatch-ticket` procedure owns the per-kind branch: `feature` keeps the
find-or-make/size/dispatch/close-loop path; `bug` hands off to `file-bug`'s investigation (never
built inline); `task` runs `find-intent`'s clarify round FIRST, inside `dispatch-ticket` itself —
but that round requires an interactive user, and a `build-lead` dispatch never has one (it's
always an `Agent`-tool call, whether mobilize-chores itself ran interactive or `auto`), so a task
still too vague to act on comes back SKIPPED, never guessed at. Any ops/hygiene action or
human-decision item stays out of scope and reports as skipped.

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
2. No dispatch (`Agent(teamwork:build-lead)`) fires without one batched confirm first — a human
   `AskUserQuestion` round, or, on an explicit leading `auto` token in `$ARGUMENTS`, step 2's own
   filtering standing in as the gate (2026-08-11 exception, an unattended mode a `/goal` loop or
   scheduled routine invokes deliberately, never inferred from context) — never per-item confirms,
   never a silent auto-build on either branch.
3. A queue item mobilizes ONLY if it's a filed `kind: bug`/`kind: feature`/`kind: task` ticket,
   routed UNIFORMLY to `build-lead` (ADR-0010) regardless of kind — its own preloaded
   `dispatch-ticket` procedure owns the per-kind branch, never re-implemented here — and never an
   ops/hygiene action (agent dispatch, config edit) or a human-decision item, even one a
   reasonable ad hoc read would call "low-risk enough to just do." Every non-ticket item is
   reported as skipped, with the reason.
4. The report names which dispatches succeeded, failed, or are still in flight.
5. A `kind: task` ticket `dispatch-ticket` finds still too vague to act on is never dispatched
   blindly — no clarify round runs on that dispatch regardless of which confirm branch mobilized
   it (an `Agent`-tool call has no interactive user either way); it's reported SKIPPED, with the
   gap named, exactly like an unconfirmed or in-flight item.
6. A ticket returned as a named blocker (2026-08-11 addition) gets a classified breakdown
   paragraph, never just a table row: what's actually blocking it (quoted/paraphrased from
   `build-lead`, never re-derived), which shape it is — named in the paragraph, not just decided
   internally — from judgment call / protocol ratification / someone else's in-flight work /
   mechanical human action (permission, credential, tool install) / external dependency with no
   lever here / or an explicit "fits none, here's the nearest honest action" escape, and a
   proposed action that fits that shape — never a build attempt, on any of the six. Prose only;
   no raw commands in this pass, even for the ratification/mechanical shapes where one exists.
7. On a follow-up ask for commands, each blocker gets either a real, verbatim, copy-pasteable
   command, or an explicit "nothing to run" (naming a status-check command if one exists) — never
   an invented command that wouldn't actually do anything.

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
                RE-OPENED 2026-08-11 for the `auto` unattended-mode addition, RE-PASSED same day —
                lint clean. Fresh-context skill-checker FLOOR audit: PASS, no blocking findings;
                2 major + 1 minor + 1 nit, all fixed same-pass: (major) the UNATTENDED branch
                claimed "in-flight PRs excluded... on both branches" while step 2 discloses no
                such check exists for Option A (local tickets) — qualified to git-native and gave
                UNATTENDED an Option-A caveat naming the gap per ticket instead of implying a
                check that doesn't run; (major) intent.md's own delta/assertions 2/3/5 still
                described the pre-ADR-0010 per-kind routing (`build-feature`/`file-bug` direct,
                a find-intent clarify round inside the dispatch) after SKILL.md had long since
                moved to uniform `build-lead` dispatch with no clarify round ever — same stale
                living-spec class the 2026-08-08 audit already caught once, fixed here as this
                entry; (major) the "unattended dispatches never reach merge" ceiling was
                environmental (this workspace's permission classifier + ADR-0002's merge gate),
                not skill-text-borne, and `dispatch-ticket` itself names "merged" as an expected
                milestone — pinned with a one-line reference in SKILL.md step 4's UNATTENDED
                branch rather than restated; (minor) step 6 named no confirm-branch, so a scope
                instruction that happens to start with the literal word "auto" ("auto label
                tickets first") would silently flip a run unattended with nothing in the report
                to notice by — step 6 now opens by naming which branch ran and the token as
                parsed.
                RE-OPENED 2026-08-11 for the blocker-breakdown addition, RE-PASSED same day — lint
                clean. Fresh-context skill-checker FLOOR audit: PASS, no blocking findings; 1
                major + 1 minor + 1 nit, all fixed same-pass: (major) the original four-shape
                taxonomy had no escape hatch, and a real fifth shape exists — a mechanical human
                action (permission grant, missing credential, tool install) that `build-lead`'s
                open-ended "relay any other blocker" channel can genuinely return, which fit none
                of the four cleanly and would have been misfiled as "external dependency, nothing
                to do but watch" when a one-line grant is actually the lever — added as a fifth
                shape plus an explicit "fits none, propose the nearest honest action" escape so
                the list never forces a real blocker into the wrong bucket; (minor) assertion 6
                required the paragraph to name its shape but the SKILL.md paragraph-contents spec
                didn't say so — added; (nit) shape 2's "name the exact mechanism" pulled toward
                inlining a command despite the prose-only rule — added a labeled bad/good pair.

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
- 2026-08-11: `auto` unattended mode added (Kim's explicit request — a `/goal` loop needs to drain
  the ops queue overnight with no human to answer step 4's `AskUserQuestion`). Considered
  inferring unattended-ness from context (no interactive user detectable) vs. requiring an
  explicit token; chose the explicit token — inference is exactly the class of ambiguity
  `chore-lead`'s own `teammate_id="team-lead"` incident (gh#156) and its SendMessage-default
  incident (gh#157) both trace to (silently assuming a mode from context instead of being told
  it), and this workspace's standing doctrine reserves PR merge/review for a human in unattended
  runs regardless (`auto-mode-gh-permissions`) — this mode only ever reaches "built + PR opened,"
  never merge, so the blast radius the confirm round was guarding is unchanged; only which gate
  performs the filtering moves from a human glance to step 2's existing, already-safe criteria.
  Step 0 added as the single parse point so steps 1 and 4 both read one already-resolved flag
  rather than each re-deriving it from `$ARGUMENTS`.
- 2026-08-11: blocker breakdown format added (Kim's explicit request, after seeing a live example
  in a different repo's session — a per-blocker paragraph naming what's blocking it and a
  proposed action, classified into one of four shapes so the proposal never drifts into "just try
  to build it anyway," plus a commands-only follow-up pass on request). A plain SKIPPED (an
  under-specified task, no clarify round available) stays a table row — it has no "blocking
  reason" to break down, just an absent one; only a named blocker, which by definition carries a
  stated cause, earns the paragraph. The commands-only pass is a documented follow-up convention,
  not a new procedure step — mobilize-chores' own species is `disable-model-invocation: true`
  (command-only), so there's no re-invocation to hang a new step on; the body stays loaded for
  the rest of the conversation, so the convention still fires when asked.
