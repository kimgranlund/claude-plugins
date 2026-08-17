---
name: overhaul-execute
kind: skill
description: >
  Drive an approved estate overhaul end to end — scope confirm, measure, plan, then gated wave
  execution through rename-planning/rename-execute, reshape-skill, and build-lead. The execution
  counterpart of overhaul-planning: that skill generates the plan, this one drives it, through
  three confirm gates that each need a live user (no user -> stops SKIPPED, never self-approves).
  Use for driving or running an already-approved overhaul plan through its execution waves, or
  via /overhaul-execute directly. NOT for generating the plan
  (overhaul-planning); NOT for one artifact rename (rename-planning, rename-execute); NOT for a
  plain audit (naming-audit, bloat-audit).
author: kim
created: 2026-08-14
last_updated: 2026-08-17
requires: [naming-audit, bloat-audit, overhaul-planning, rename-planning, rename-execute, manifest-authoring, fix-old-names, pattern-audit, doctrine-audit]
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Agent
  - AskUserQuestion
  - Write
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
  - Bash(python3 */scripts/scan.py *)
  - Bash(python3 */scripts/sweep.py *)
  - Bash(gh issue *)
---

# overhaul-execute

The DRIVES half of the `overhaul-planning` pair: that skill generates the plan; this skill runs
the campaign — discover, measure, plan, execute approved waves — composing the existing
instruments and reimplementing none. Ships `user-invocable: true` directly — `/overhaul-execute`
is this skill, no separate command wrapper (issue #525: skill-as-command is the estate's
dual-access successor to the command-wrapper pattern §14.1 originally licensed this name shape
through; §14.9 extends that licence to cover this exact shape — a verb-terminal skill name with
no sibling command at all — and the superseded `commands/overhaul-execute.md` retired in the
same change). The three gates below all need
a live user regardless of which surface invoked this procedure: a run where `AskUserQuestion` is
unavailable, errors, or gets auto-answered under momentum counts as no live user — it stops at
its first open gate and reports SKIPPED, leaving the decision to a human. This procedure is
never run unattended for that reason.

## Run ledger

First act of every run: `Write` `<target>/.claude/overhaul-run-<YYYY-MM-DD>.md` — scope table,
per-wave status, the emergent-item queue, gate outcomes — updated at every phase boundary. A
resumed run reads this file before doing anything else.

## Phase 0 — DISCOVER + SCOPE CONFIRM (gate 1 of 3)

Resolve the target only by scanning — from `$ARGUMENTS` (blank = the current project root):

- Markers: `**/.claude-plugin/plugin.json` (a plugin root), `*/skills/*/SKILL.md` and
  `.claude/skills/*/SKILL.md` (skill trees), `.claude/` dirs holding `skills|agents|commands`,
  bare `agents/`/`commands/` dirs beside them, `**/naming.manifest.json` (governance).
- Auto-excluded, reported as one noise count only: any path under `.claude/worktrees/`,
  `node_modules/`, `.git/`, `dist/`, `.refactor-attic/`.
- Classify each surviving root: **governed estate** (a manifest at its root, its `.claude/`, or
  an ancestor manifest inside the scan root) or **ungoverned candidate** (estate markers, no
  manifest in reach).

Present ONE table — root / markers found / classification / recommended in-or-out / one-clause
why — and take the user's picks in ONE `AskUserQuestion` round before any audit spends a token.
An explicit member-list argument narrows the scan to the estates containing those members; it
still gets this round. Ungoverned in-scope estates route through `manifest-authoring` (Skill
tool) FIRST — governance before measurement.

## Phase 1 — MEASURE

Per in-scope estate: `naming-audit`, `bloat-audit`, and `attention-audit` (Skill tool), plus two
conditional instruments mirroring `overhaul-planning`'s own Phase 0 composition (its steps 3-4 —
cite, don't restate):

- **doctrine-audit**, always fires when the estate carries a `doctrine.manifest.json`:
  `authorkit:doctrine-audit`. No manifest on the estate → report the doctrine axis `absent` for
  that estate, mirroring Phase 6's own routing-report `absent` handling below — never invent
  edges to fill the gap.
- **pattern-audit**, conditional on the approved plan's own statement of intent naming a
  pattern none of the other four instruments owns: `authorkit:pattern-audit` with that pattern
  statement as its instruction. No such pattern named → report the pattern axis `absent` for
  that estate.

More than 3 estates in scope, or any single estate over 40 members, dispatches
`estate-audit-agent` (Agent tool) once per instrument — `naming`, `bloat`, `attention`, plus
`doctrine` and `pattern` wherever their trigger fired above — with the batch instead (the same
threshold governs all five). On the pattern-audit batch leg specifically, this procedure's own
live user is present by contract (Phase 0's gate) — compile the probes per pattern-audit's own
step 2 with its veto round still running there, then dispatch the agent with the compiled
`LABEL=REGEX` probes, never the raw statement; `estate-audit-agent` accepts only pre-compiled
probes on this instrument, same rule its planning-side precedent already follows. Record each
estate's baseline in the run ledger — error count, exemption count, routable/agent description
chars (attention-audit's rent figures), doctrine finding counts by edge type, pattern-audit's
verdict line (record-only — Phase 6 burns down naming, attention, and doctrine, not pattern) —
the Phase 6 burn-down starts here for those three axes;
an `absent` axis is recorded as `absent`, not omitted.

## Phase 2 — PLAN

Per in-scope estate: `overhaul-planning` (Skill tool), full procedure. Its plan doc and waved
ticket seeds are Gate A's material as delivered — its kill-switch analysis stands.

## Phase 3 — GATE A: findings + wave map (gate 2 of 3)

ONE batched `AskUserQuestion` round carrying:

1. **Systemic problems** — one row each: evidence (cited numbers from Phase 1–2 output), the
   problem, a proposed solution, the owning instrument. The same violation class recurring
   across 3+ members or estates is a spec/template problem, not a member problem. No solution
   attached → the row is malformed; fix it before presenting.
2. **Wave map** — per wave: id, rows (member → action), risk tier, Blocked-by edges. Options
   per wave: approve / amend (the user states the change; re-render and resolve in-round) /
   kill.
3. **Emergent queue** — the ledger rows accumulated so far (schema below).

Nothing mutates before this round returns. Killing every wave is a normal outcome (the #197
campaign killed 7 of 8 proposed moves).

## Phase 4 — EXECUTE, wave by wave

Run only Gate-A-approved waves, in plan order. Per row kind:

- **rename** → `rename-planning` (Skill tool) for the plan, then `rename-execute` (Skill tool)
  for the confirmed mutation — both are `user-invocable: true` skills as of issue #525 (no more
  command-only `rename-execute`, no more reading a command file's body by hand); its own
  touched-file confirm still runs, verifying the enumerated blast radius the Gate-A decision
  already approved.
- **merge/split (Wave 0 seeds)** → `harness:reshape-skill` where harness is installed and the
  command is Skill-tool-reachable; where it is `disable-model-invocation: true` or harness is
  absent, name the exact `/reshape-skill …` invocation for the human to run now and hold the
  wave until they report done.
- **move/build** → mint the approved seed through its owning intake skill first (record before
  build: `docs:file-feature`/`docs:file-task` where docs is installed, a plain `gh issue create`
  otherwise), then dispatch `teamwork:build-lead` (Agent tool) with the ticket id — worktree
  isolation is `dispatch-ticket`'s own call (conditional since #204, never this skill's to
  decide), and the ceiling is PR-opened: merges stay the human's unless that dispatch clears
  ADR-0012's quick-build predicate in full, which no overhaul row does — a wave spans many files
  across more than one plugin and rewrites contracts by definition, so it never places the
  `auto-merge: authorized` grant line and never becomes eligible. teamwork absent → emit the seed
  only and state plainly the wave will not build.
- **after every wave containing a rename** → a `fix-old-names` sweep (Skill tool).

Two rows run in parallel only when both name concrete, non-overlapping edit targets
(`mobilize-chores`' disjointness rule); otherwise serial. Close each wave in the run ledger:
per-row outcome, PRs opened, failures (a failed `rename-execute` reverts per its own contract).

## Phase 5 — GATE B: premise change only (gate 3 of 3)

Fire this gate when — and only when — a wave's outcome changes a later wave's premise:

1. execution discovered a rename/merge/split target the Gate-A plan does not name;
2. a kill-switch verdict flips from proceed to no-go on execution-revealed blast radius;
3. a wave's actual touched-file count diverges from its plan enumeration by more than 25% of
   its rows or 10 files, whichever bound is lower;
4. a failed or reverted row invalidates a later wave's precondition.

None of the four tripped → the next wave runs on Gate A's approval, no gate. Firing → ONE
batched `AskUserQuestion` round: the trigger tripped (name which of the four), what changed,
which waves it invalidates, a proposed re-plan per affected wave (approve/amend/kill), plus the
emergent queue since the last gate.

## Emergent items — throughout

Anything off-plan — a bug, question, or finding — enters the run ledger's queue the moment it
appears: evidence, a blocker shape per `mobilize-chores`'s own five-shape taxonomy (that skill
owns the enumeration; consult it rather than restating it here), a PROPOSED SOLUTION
(mandatory — every row reaches its gate carrying one), and
its owning intake route (`docs:file-bug`/`docs:file-task`/`docs:file-feature` where docs is
installed; `gh issue create` otherwise). The queue is confirmed at the NEXT gate — Gate B if
firing, else the next wave close, else Phase 6 — and approved rows are minted through their
route then: one batched confirmation, and the ledger row survives to it even when no gate
fires in between.

## Phase 6 — PROVE + REPORT

1. `harness:check-routing` on every touched boundary (harness absent → routing proof reported
   UNMEASURED, named as such).
2. Re-run `naming-audit` per estate: the burn-down scoreboard, baseline → now.
3. Re-run `attention-audit`'s rent measurement and append its trend row (trend.py) per estate:
   the dated row IS the baseline → now evidence for the attention axis; a repo with no routing
   report records those columns `absent`.
4. Re-run `doctrine-audit` on every wave-touched estate that had a Phase 1 doctrine baseline
   (an estate with no `doctrine.manifest.json` stays `absent` here too — a wave never seeds one
   from this step). Diff against the Phase 1 baseline: any new finding not present at baseline is
   drift a wave introduced — Gate-B-adjacent evidence, named in the roll-up below by estate and
   edge type, whether or not Gate B actually fired (this is a report finding, not a fourth gate).
   No new findings → the estate's doctrine axis reports clean, baseline to now.
5. Verdict-first roll-up: 🟢/🟡/🔴 per estate; waves run/killed/pending; PRs open awaiting the
   human's merge; emergent items minted (ids) or declined; new doctrine drift since baseline
   (estate, edge type) or none; every degraded or skipped step named with its reason; the
   run-ledger path.

## Degraded modes

- harness absent → no `reshape-skill`, no `check-routing`: merge/split rows stay seeds; Phase
  6's routing proof is UNMEASURED.
- docs absent → no intake skills: emergent items mint via `gh issue create`, proposed solution
  in the body.
- teamwork absent → no `build-lead`: move/build rows emit seeds only; the wave says so plainly.
- `gh` unreachable → emergent items stay ledger-only, flagged 🔴 manual-filing; nothing drops.

## Failure branches

- A composed instrument fails mid-wave → its own contract governs (`rename-execute` reverts
  itself); the row is a ledger failure; test Gate B trigger 4.
- Every wave killed at Gate A → Phase 6 still runs; the measure/plan artifacts ARE the
  deliverable.
- No live user at any gate → stop, report that gate SKIPPED and the run blocked on a human —
  this procedure never self-approves.

Done when every in-scope estate was scope-confirmed before measurement, every mutation traces
to a Gate-A (or Gate-B re-plan) approval, every emergent item holds a ledger row with a
proposed solution and reached a gate or the final report, the burn-down scoreboard compares
baseline to now, and the roll-up names every skip with its reason. NOT done while a mutation
precedes its gate, a gate is answered by anyone but the live user, an emergent item exists only
in conversation, or a degraded step is silently absent from the report.
