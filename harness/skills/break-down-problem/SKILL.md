---
name: break-down-problem
description: >-
  Decompose a problem along two crossing planes — OUTSIDE-IN (whole → parts) and
  INSIDE-OUT (actions → surfaces) — then cross-checked. Use when breaking down a
  technical or UX architecture, goal, or system into parts, or when a breakdown feels
  lopsided — structure with no behavior — or acceptance criteria don't map to any
  task. NOT for authoring PRD/SPEC/LLD; NOT authoring skills (make-skill); NOT a
  knowledge skill's split/merge (plan-skill-split / plan-skill-merge).
disable-model-invocation: false
user-invocable: true
---

# Harness — Decomposer

Decomposition fails in one of two ways, and running a single direction hides the other. This skill runs **both planes** and makes the gap between them visible and checkable.

## The two planes

- **OUTSIDE-IN** — start from the whole and divide into parts, top-down: context → regions → groups → atoms. Produces the **structure** (a node tree). Answers *"what are the parts, and how do they nest?"*
- **INSIDE-OUT** — start from the irreducible units and compose upward, bottom-up: actions/atoms → bindings → surfaces → coherence. Produces the **behavior/needs** (an action set). Answers *"what must this do, and where does each capability live?"*

They are not alternatives. A decomposition is sound only when they **cross-check**:

| | has a surface (OUTSIDE-IN node) | no surface |
|---|---|---|
| **has an action (INSIDE-OUT)** | ✅ load-bearing | ❌ **unhosted action** — a need with nowhere to live |
| **no action** | ⚠️ **unjustified structure** — decoration / gold-plating (unless a declared affordance) | n/a |

The defect quadrant is the point of the skill: a clean structure that can't host the behavior, or behavior with no surface, are the two silent failures a single-plane breakdown ships.

**Modes:** **DECOMPOSE** (the default — both planes → manifest → gate) · **PLAN** (`"plan": true` — the manifest feeds execution; every leaf then owes an `accept` predicate, gated as `NO-ACCEPT`) · **STRICT** (`--strict` — the advisories `UNJUSTIFIED-LEAF`/`EDGE-UNJUSTIFIED` become blocking).

## Process

1. **Pick the domain reference** (`references/<domain>.md`) for the concrete vocabulary of each plane; read `references/method.md` (procedure), `references/foundations.md` (the models it rests on), and `references/best-practices.md` (the do/don't); grade the result against `references/rubric.md`. If no domain fits, use `references/_template.md` to add one.
2. **Run OUTSIDE-IN** → a node tree. Mark leaf nodes; tag any pure-structure node with a `justify` (why it exists with no action — e.g. `affordance`, `grouping`).
3. **Run INSIDE-OUT** → an action/atom set (the verbs/needs/capabilities), independent of the structure so it can contradict it.
4. **Map** each action to the node(s) that host it.
5. **Check coverage** — write the decomposition to a manifest (this skill's card; schema below) and run `python scripts/coverage_check.py <manifest.json>`. It is deterministic; do not eyeball it. The checker's verdicts are two-tier: **gate** (exit 1) and **advisory** (blocking only under `--strict`); `python scripts/coverage_check.py selftest` proves both tiers bite.
6. **Fix** every `UNHOSTED` action (add or reshape structure), every `DANGLING` ref, every `EDGE-DANGLING`/`EDGE-CYCLE` (the edges must admit a build order), and — on a `plan` manifest — every `NO-ACCEPT` leaf; resolve each `UNJUSTIFIED-LEAF` (add the action it should host, add a `justify`, or delete the node) and justify or delete each `EDGE-UNJUSTIFIED`.
7. **Re-check; finalize only when the script exits 0.** The gate is code — independent by construction; for a high-stakes decomposition dispatch a fresh-context subagent (the critic seat) to score the breakdown against `references/rubric.md` rather than grading your own (generator ≠ critic). Once handed off, the manifest is versioned: a replan writes `manifest-v(n+1)` with a stated diff and reason, never an in-place mutation the record can't reconstruct. Hand the node tree + action map to whoever authors the downstream document; when the decomposition is for a new skill, that hand-off is `/make-skill` (whose intent interview also covers the greenfield grilling a largely-unmade design needs first). **If the decomposition feeds a parallel build,** slice it for the fan-out first — one writer per file, every shared/barrel edit deferred to one serial integration slice, a serial PREP slice ahead of a wide fan-out, and a negative control for each new gate/probe (`references/best-practices.md`).

## Manifest schema (what the check reads)

```jsonc
{
  "domain": "layout",
  "plan": false,                                                                       // true when the manifest feeds execution — every leaf then needs `accept`
  "nodes":   [{ "id": "n1", "label": "submit bar", "leaf": true, "justify": null,
                "accept": "`pnpm test submit-bar` exits 0" }],                         // OUTSIDE-IN; `accept` = checkable predicate, required on leaves when plan
  "actions": [{ "id": "a1", "label": "submit the form" }],                             // INSIDE-OUT
  "hosts":   [{ "action": "a1", "node": "n1" }],                                       // the crossing
  "edges":   [{ "from": "n2", "to": "n1", "why": "n1 renders the schema n2 pins" }]    // build-order constraints (`from` lands before `to`); default topology is parallel — each edge earns its place with a real data dependency
}
```

## Domains (references/)

| Domain | OUTSIDE-IN axis | INSIDE-OUT axis |
|---|---|---|
| `layout` | frame → regions → groups → atoms | feature-actions → bindings → surfaces |
| `components` | module → component → primitive (tier ladder) | geometry → element → semantics → interaction |
| `technical-architecture` | system → subsystems → modules → units | capabilities → interfaces → data → integration |
| `ux-architecture` | product → sections → screens → states | user-goals → tasks → interactions → feedback |
| `goals` | mission → outcomes → milestones → tasks | intent → acceptance criteria → checks |

Each reference gives that domain's two axes, the stop rule (when a part is atomic enough), and a worked pass, and is the canon for its domain within this pack. A cross-screen **journey** — entry, transitions, exits as a state machine — is out of scope: `ux-architecture` stops at what screens/states exist; model the journey separately when the work needs it. To add a domain, copy `references/_template.md`.

## Worked example (goals, abbreviated)

OUTSIDE-IN: `ship A2UI runtime` → `{renderer, default catalog, validation}` → `validation` → `{schema, catalog-conformance, id-graph}`.
INSIDE-OUT actions: `parse stream`, `render on root`, `reject invalid payload`, `bind data`.
Map → `reject invalid payload` hosts on `validation`; `bind data` finds **no node** → `UNHOSTED` → add `data-binding` under the renderer. Re-check → clean.

## Validation loop

draft both planes → write manifest → `python scripts/coverage_check.py <manifest.json>` → fix `UNHOSTED`/`DANGLING`/`UNJUSTIFIED-LEAF` → re-run → finalize at exit 0. The script is the gate; the prose is the method.

**Scope of the gate.** `coverage_check.py` verifies the two planes cross-check (node ↔ action) — it does NOT verify real-world completeness. A need that was never written as an action (e.g. a ratified ADR Decision) has nothing to leave `UNHOSTED`, so the manifest passes clean while the need ships nothing. Catch that upstream with the ADR-Decision → action completeness review (`references/best-practices.md`), a judgement step, not this gate.

## Report

```
Manifest: <path> (domain · mode) · coverage_check: <clean | gates: codes · advisories: codes>
OUTSIDE-IN (structure): <findings — MECE gaps, mis-cut granularity, unjustified structure>
INSIDE-OUT (behavior):  <findings — unhosted needs, actions naming solutions not needs, missing accepts>
Quadrant verdict: <load-bearing | unhosted action(s) | unjustified structure | both planes broken>
Hand-off: <who receives the node tree + action map next>
```

Gate findings first; the two planes are reported separately, never averaged — the quadrant, not a blended score, names the fix.

## Verify Target

The decomposition is **done** when: the manifest passes `coverage_check.py` at exit 0 (PLAN mode: with `accept` on every leaf; STRICT: advisories clear too); the two planes were derived independently and graded separately against `references/rubric.md` (D1 + D3 ≥ 3 to promote); and the report names the quadrant verdict and the hand-off owner. **NOT done** when coverage was eyeballed instead of run, when one plane was read off the other (the tautological pass D2 names), or when a finalized manifest was mutated in place instead of versioned to `manifest-v(n+1)`.
