---
name: team-or-solo-rules
description: >-
  Design or review orchestration — how skills, subagents, and teams compose, and their
  wiring frontmatter. Use when deciding skill vs subagent vs team, wiring
  capabilities, planning a fan-out worth its token cost, skills: preloads, or auditing
  an agent system's wiring — "should this be a subagent or a team", "how do my skills
  and agents connect". NOT a whole-corpus/team audit — "audit the agent team
  for duplicates", "do my agents leverage the right skills" (check-all-agents /
  check-all-skills);
  NOT a single agent definition (make-agent / agent-writing-rules); NOT next-turn
  timing (loop-rules); NOT the fleet's default coordination-scope/claim/comms/version-slot/
  pin-race protocol (fleet-rules).
disable-model-invocation: false
user-invocable: false
---

# Harness — Orchestration & Frontmatter Design & Review

Design how capabilities compose, or review an arrangement. The unit is chosen by task shape: skill (procedure), subagent (result-only delegation), team (collaboration).

## Operating model (essentials; depth in `references/foundations.md`)
- Discovery (descriptions select, every turn) vs continuation (`/goal`,`/loop`,hooks decide when the next turn fires) — never conflated.
- Descriptions are the connective tissue: the orchestrator routes on them, not on file cross-references.
- Static vs dynamic wiring: `skills:` preload hard-wires standing expertise; leave the rest to discovery.
- Composition is planes, not a pipeline: authority flows down, artifacts flow up, verdicts flow sideways — a failed verdict routes to the plane that caused it (loop mechanics live in `[[loop-rules]]`).
- Every dispatch is a sealed contract: charter + enumerated inputs + budget + typed return (`references/best-practices.md` "The dispatch is a sealed contract"); the worker never sees the host's deliberation or sibling transcripts.
- The return channel is session-bound, durable state isn't: a completion notification reaches only the live session that made that dispatch, and dies with it. A durable-effect dispatch (PR, branch, ticket) must be discoverable from that state alone by a later session — never solely from having witnessed the notification (`references/best-practices.md` "The return channel doesn't survive the session").

## Seat-access doors

A seat's own contract (what `dispatch-ticket` and its kin actually do) is one thing; HOW a
caller reaches it is a separate design question this skill owns too — three structurally
different doors, none a synonym for another, and nothing in a bare seat name reveals which one a
given caller gets:

1. **Session adoption** — a `/bind-*` command (`/bind-build`, `/bind-team`, `/bind-planning`) and
   its skill-as-command shape make the CURRENT session hold a standing agent's contract
   in-place, with no `Agent` spawn and no fork. Nothing left the session, so its interactive
   branches — a live clarifying question, an `AskUserQuestion` round — stay reachable turn after
   turn for as long as the session runs. Pick this door when a human is going to feed the seat
   more than one target in a row.
2. **`context: fork` execution** — a `disable-model-invocation: true`, `user-invocable: true`
   command (`/build-feature`) runs its target's procedure as a fork (background by default) off
   the caller's own session, one target at a time. Forking relieves the CALLER's context, not the
   human: a fork can still reach the live user directly via `AskUserQuestion` mid-run. Pick this
   door for one known target, right now, from a session that wants to stay clean for whatever
   comes next.
3. **`Agent`-tool dispatch via a `*-leader` agent** (`build-leader`, `planning-leader`,
   `review-leader`) — the only door open to a genuinely unattended, programmatic caller with no
   live user at all: a coordinator, `mobilize-chores`, a `/goal` loop. No clarify round is
   possible here, so the dispatched engine's own unattended failure branches take over instead
   (report a named blocker, report SKIPPED) rather than asking anyone.

**Why three doors exist instead of one command serving every caller.** A
`disable-model-invocation: true` command is invisible to the `Skill` tool (issue #134/#135's
shared defect class) and to any agent's `skills:` preload (the same platform rule
`skill-writing-rules` names). That combined mechanical fact is why a door-2 command can never BE
door 3: nothing with `Agent`-tool access can reach it directly. So
the actual procedure lives once in a plain, Skill-tool-reachable skill (e.g. `dispatch-ticket`),
and each door is a thin wrapper invoking that same engine inline — this is the **`*-leader` twin
rationale**: every command shaped like door 2 earns a same-shaped `*-leader` agent as door 3, not
because the two ever duplicate logic, but because a command's own `disable-model-invocation` flag
structurally forecloses the one door a programmatic dispatcher needs. Confusing the doors is a
recorded defect class, not a hypothetical: #134/#135 is the mechanical unreachability itself, and
the pattern recurs anywhere a new standing seat is designed without asking which callers need
which door. Rejected as a naming fix (ADR-0020, gh#518): renaming the doors doesn't change which
one a given caller can structurally use — the fix is knowing the three exist and picking by who's
calling, not a vocabulary change.

## Design
1. **Solo-first — the host inline is the null unit and wins by default.** A seat must buy
   something the host cannot provide: isolation (fresh context), parallelism (genuinely
   concurrent slices), or independence (generator≠critic on a high-stakes artifact). A team must
   buy it twice. A dispatch that costs more context and latency than doing the work inline is
   over-orchestration, whatever the task's step count — then match the unit to the task and
   justify team fan-out by genuine parallel value.
   **The job-evidence test (new seats/flows only) — modeled directly on `plan-plugin-split`'s
   job-evidence rule, same shape, same rigor:** before a NEW coordination seat or multi-seat flow
   is added, its design records the evidence for why the main loop plus at most one
   Explore/checker dispatch cannot hold the job. Evidence is a concrete, named gap — an isolation
   need the host provably lacks (its own context is polluted or must stay clean for a later step),
   a genuinely concurrent slice competing for the same turn, or a generator≠critic split a
   high-stakes artifact requires — a template default ("systems eventually get a
   coordinator") or the step count alone ("it's multi-step, so it needs orchestration") is a
   question, not evidence (#4 already rejects that reasoning for depth, this test rejects it for
   existence). No cited gap → the seat/flow doesn't earn a place; the solo-first default above
   stands. This test gates
   NEW seats and flows going forward only — an existing seat already in an estate is not
   retroactively re-justified by it.
2. Each description a precise interface; `tools` scoped, `model` to task class, `skills:` only for standing expertise; verify keys against the installed build.
3. Keep teammate roles as subagent definitions (teams compose them at runtime).
4. Dispatch sealed and shallow: enumerate inputs, state the budget, name the typed return; depth ≤ 2 (host → specialist) — a third level needs justification, a fourth means the decomposition under-cut.
5. For a parallel BUILD team, dispatch the disjoint same-tree fan-out (`references/best-practices.md`): file- and import-disjoint slices concurrently in one tree, each worker self-gating its own path, the host running the whole-tree gate + negative controls at the wave boundary; worktrees only when slices must mutate overlapping files. **Precondition — the HOST owns git; workers only edit files.** A worker that drives its own branch/commit/PR lifecycle (e.g. a `build-lead`/`dispatch-ticket` dispatch) is outside this shape entirely: two such workers race on the shared index/HEAD regardless of file disjointness, so they take per-worker worktree isolation whenever concurrent — file-disjointness licenses parallel timing there, never same-tree sharing (incident 2026-08-11: this step's conclusion copied without the precondition shipped a blocking same-tree race in a sibling skill).
6. Self-score (below); fix until every gate dimension (D2, D4) ≥ 3.

## Review
1. This skill's gates are systemic judgment, not a single-file mechanical check — there is no `harness_checks` subcommand: D2 is judgment because whether a description is a precise interface only shows against the sibling set (no string test sees it); D4's YAML-validity half IS mechanizable — its checker is queued, not built — so until it lands, score D4 by inspection and mark uninspected fields skipped-not-passed. Score against `references/rubric.md`, citing evidence on the 1–5 anchors.
2. Check plane separation first (the top failure: expecting `/goal` to select capabilities).
   For any NEW seat or multi-seat flow in the arrangement, check the job-evidence test (Design
   #1) was actually recorded — a cited gap, not an assumed one; an unjustified new seat is a D1
   finding.
3. Findings by severity; gate verdict; top issues with a concrete fix each. **Generator ≠ critic:** for a high-stakes system dispatch the independent **`wiring-checker`** (fresh context, scores this same rubric by inspection) rather than grading your own arrangement.

## Improve (repair an arrangement)
Review first, then close the gap — plane separation and connective tissue before polish. Fix the wiring, re-score, finalize only when every gate dimension (D2, D4) ≥ 3. (Improve = review + targeted redesign.)

## Update (re-sync after drift)
Wiring drifts two ways. The BUILD moves: frontmatter keys and `skills:` preload semantics change — re-verify every field against the installed build (the rubric's D4 "verified against build" anchor is the check). The CAPABILITY SET moves: a skill or agent is added, renamed, or retired — re-review every description, preload, and fence that referenced it. Either change re-opens the gate dimensions.

## Output contract (review)
```
Artifact: <system/frontmatter>  ·  Rubric: rubric-orchestration
| Dim | Type | Score | Finding | Evidence |
Gate (D2,D4): <pass/fail>
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `references/rubric.md` | Scoring dimensions and anchors (judgment-based) |
| `references/best-practices.md` | Design guidance / explaining a finding |
| `references/foundations.md` | When a finding turns on a shared model (discovery vs continuation) |
| `[[write-handoff]]` | The return contract a composed agent hands back — the other half of composition; its "Sealed vs. messaging" note states which channel carries the block (a sealed dispatch's Findings entry, or a named teammate's mailbox message) — never re-derive that split here |
| `references/handoff-fallback.md` | The inline eight-field fallback for an agent body when `write-handoff` isn't installed — the one referenced copy every teamwork agent cites instead of hand-restating the block |
| `[[loop-rules]]` | Continuation mechanics (`/goal`, `/loop`, hooks) and loop discipline — owns the self-orchestrated-looping canon (budgets, locus escalation, durable state) |
| `[[parallel-work-rules]]` | A relayed report needs the same independent-verification discipline as a self-report — this skill's "verify independently" rule extends to any intermediary, including your own dispatcher |

**Done** when every unit matches its task shape (the null unit respected — no seat doing host-inline work), every description is a precise fenced interface, frontmatter is verified against the build, dispatches are sealed and typed, both gate dimensions (D2, D4) score ≥ 3, and a high-stakes arrangement carries its independent wiring-checker pass. **NOT done** while any description starves the router, a fence is one-way, a dispatch leaks history or lacks a budget, planes are conflated — or the only score the arrangement has is its designer's.
