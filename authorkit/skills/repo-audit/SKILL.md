---
name: repo-audit
kind: skill
description: >
  One umbrella sweep across the full audit battery — Phase-0-style discover/scope-confirm, then
  fans out all five authorkit instruments plus, where installed, harness's cross-plugin axes —
  into ONE verdict-first 🟢/🟡/🔴 roll-up per estate per axis. Read-only: reports, never mutates.
  Use for "audit this repo", "run the full audit battery", "give me one verdict across naming,
  bloat, attention, and routing". Ships with an identical-name command wrapper (/repo-audit). NOT
  for one instrument alone (naming-audit/bloat-audit/attention-audit/pattern-audit/doctrine-audit,
  or estate-audit's single-instrument index — this skill composes all five, never reimplements);
  NOT for driving an approved overhaul's execution waves (overhaul-execute mutates through gated
  waves, this one only ever reports); NOT for the ops chore queue (harness:sweep-chores — live
  work-state, not static audit instruments); NOT for a point-in-time work-state report
  (harness:check-state — branches/PRs/drift, not audit axes).
author: kim
created: 2026-08-16
last_updated: 2026-08-16
requires: [naming-audit, bloat-audit, attention-audit, pattern-audit, doctrine-audit, estate-audit]
disable-model-invocation: false
user-invocable: false
disallowed-tools: [Write, Edit, NotebookEdit]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Agent
  - AskUserQuestion
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
  - Bash(python3 */scripts/rent.py *)
  - Bash(python3 */scripts/collide.py *)
  - Bash(python3 */scripts/usage.py *)
  - Bash(python3 */scripts/trend.py *)
  - Bash(python3 */scripts/scan.py *)
  - Bash(python3 */scripts/sweep.py *)
---

# repo-audit

The full-battery counterpart to `estate-audit`'s single-instrument index: where that skill only
names which ONE instrument fits an ask, this skill runs ALL of them plus the cross-plugin axes
and rolls the result into one verdict. Ships as a skill with an identically-named command wrapper
(`/repo-audit`, `commands/repo-audit.md`) per the reverse-wrapper grammar amendment
(`.claude/docs/spec/spec-naming-convention.md` §14.1, issue #241). **Structurally read-only**: the
tool grants above carry no `Write`/`Edit`/`Bash(git *)` — this skill cannot mutate the target even
if a composed instrument's own output suggests a fix. Compose the existing instruments; never
reimplement one of their sweeps inline.

## Phase 0 — DISCOVER + SCOPE CONFIRM (one gate)

Reuse `overhaul-execute`'s own Phase 0 scan exactly — its markers, auto-excludes, and governed
vs. ungoverned classification, cited not restated (`authorkit/skills/overhaul-execute/SKILL.md`
Phase 0). Present ONE table — root / markers found / classification /
recommended in-or-out / one-clause why — and take the user's picks in ONE `AskUserQuestion` round
before any instrument spends a token. No live user (dispatched unattended, e.g. from
`mobilize-chores` or a cron routine) → skip the round and scope to every governed estate the scan
found, reporting that the round was skipped and why — never block a read-only report on a
question nobody can answer. An ungoverned in-scope estate is reported UNGOVERNED for the naming
axis (its own instrument's own contract) rather than routed through `manifest-authoring` — this
skill never mutates, so it never seeds governance on an estate's behalf.

## Phase 1 — FAN OUT the five authorkit instruments

Per in-scope estate: `naming-audit`, `bloat-audit`, `attention-audit`, `pattern-audit` (only when
the dispatch or the user supplied a concrete pattern/instruction to sweep — otherwise skip it,
named as SKIPPED no-pattern-supplied, never invented), and `doctrine-audit` (only on a target
carrying a `doctrine.manifest.json` — otherwise SKIPPED no-manifest, mirroring that skill's own
contract). More than 3 estates in scope, or any single estate over 40 members, dispatches
`estate-audit-agent` (Agent tool) once per applicable instrument with the batch — the same
threshold `overhaul-execute`'s own Phase 1 and `estate-audit`'s own routing note use. Record each
axis's raw finding count per estate for Phase 3's roll-up.

## Phase 2 — CROSS-PLUGIN AXES, where installed

- **harness installed** → run `harness:check-routing` on every touched plugin boundary (its own
  blind routing-simulation contract), plus a FLOOR-depth `harness:skill-checker` and
  `harness:agent-checker` sweep over any skill/agent this run's own Phase 1 findings flagged as
  changed or suspect since the last audit — never a full-corpus DEEP sweep (that's
  `check-all-skills`/`check-all-agents`'s own campaign, out of scope here). **harness absent** →
  report `check-routing: UNMEASURED (harness not installed)` and
  `skill-checker/agent-checker: UNMEASURED (harness not installed)` by name — the same
  degraded-mode pattern `overhaul-execute`'s own Degraded modes section uses; never silently drop
  the axis from the roll-up.
- No other cross-plugin axis is in scope for this pass — `teamwork:wiring-checker` and
  `docs:check-doc` are per-artifact critics, not estate-wide sweeps, and stay each their own
  caller's job to dispatch.

## Phase 3 — ONE verdict-first roll-up

Render exactly one table: rows = in-scope estates, columns = every axis that ran this pass
(naming, bloat, attention, pattern, doctrine, check-routing, skill-checker, agent-checker) —
🟢 clean / 🟡 attention (named findings, non-blocking) / 🔴 blocked (errors, violations, or a
failed gate) / `UNMEASURED (<reason>)` for a degraded or skipped axis. Below the table: one
sentence per non-🟢 cell citing its instrument's own evidence (error count, exemption count,
routable chars, match count, finding count — never restated prose, cite the number). Never a
narrative summary in place of the table — this skill's entire deliverable IS the table plus its
citations.

## Failure branches

- No estates found in scope → report that plainly; nothing runs.
- An instrument's own script errors → that cell reads 🔴 with the error message quoted, never
  silently blank.
- `estate-audit-agent` returns a partial aggregate (a skipped target inside its own batch) → the
  roll-up's cell for that estate/axis carries the sub-skip reason verbatim, not just a blank.

Done when every in-scope estate carries a cell for every axis that ran (🟢/🟡/🔴 or a named
`UNMEASURED`), every non-🟢 cell cites its own evidence, and no absent instrument or plugin was
silently omitted rather than named UNMEASURED. NOT done while any cell is inferred rather than
measured, or the roll-up is prose instead of the table.
