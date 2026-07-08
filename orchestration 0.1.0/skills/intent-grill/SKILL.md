---
name: intent-grill
description: >-
  Proactively DERIVE the load-bearing design decisions for a greenfield system, component family, or
  feature whose decision space is mostly unmade. Use when designing or planning something new and largely
  open; when the user says "grill me", "plan this", "design this family", "what do we need to decide
  here", "walk me through the choices", or "interrogate the design space"; before running
  system-decompose or drafting a PRD/SPEC/LLD on a fresh domain — grill the decisions out of TWO
  reasoning axes (Structural / outside-in and Mechanism / inside-out) across cascading rounds, where each
  round's answers reshape the next, grounding every option in the actual codebase and constraints, until
  the surface is settled enough to decompose. NOT for sharpening one already-given ask (intent-extract);
  NOT for the decomposition itself (system-decompose); NOT for authoring the PRD/SPEC/LLD documents
  (scribe's `doc-forge`, governed by `doc-authoring-standards`).
disable-model-invocation: false
user-invocable: true
---

# Intent grilling

Derive the design decisions a greenfield *needs* before it can be decomposed — by interrogating two
reasoning axes across cascading rounds until the decision surface settles. Where
[[intent-extract]] *minimizes* questions for one given ask, grilling *derives* the questions a
mostly-unmade design implies.

## When to use / when not

- **Use** when designing or planning something **new with a large open decision space** — a system,
  component family, or feature where most decisions are unmade — and before running
  `system-decompose` or authoring a PRD/SPEC/LLD on that fresh domain. Triggers: "grill me", "plan
  this", "what do we need to decide".
- **Skip** when the decision space is small or already mostly settled — that is `intent-extract`'s
  job (resolve only the gaps in a given ask). And skip when a ratified design already exists.
- **The pipeline.** `intent-extract` sharpens *a given* intent → `intent-grill` *derives* the
  design decisions → both hand off to `[[system-decompose]]`. Extraction is **reactive, minimize** (one
  ask, one batched round, ask only what you must). Grilling is **proactive, derive** (a whole space,
  cascading rounds, derive what must be decided). Same closed-question discipline; opposite posture.

## The two reasoning axes — the core technique

These are `system-decompose`'s two planes (OUTSIDE-IN / INSIDE-OUT) applied to **question derivation**
instead of to structure. Every round, derive forks from **both**:

- **Structural** (whole → part / OUTSIDE-IN): scope & breadth · the consumer (who/what drives
  it) · the element/structure set · composition & nesting · where it sits + sequencing/phasing.
- **Mechanism** (part → whole / INSIDE-OUT): the load-bearing technical mechanisms · the
  capabilities · geometry/semantics · the platform primitives · fidelity / responsiveness / density.

**Why both.** A single axis is self-confirming — the same blindness a single-plane decomposition ships.
Structural-only yields a scope with no idea what's hard to build; Mechanism-only yields clever
primitives with no agreed shape. Crossing the planes is what surfaces the *load-bearing* forks — the
ones whose answers cascade into the rest.

## Method

1. **Frame the decision space.** Name what's being designed and why it's open (greenfield / high fork
   count). Sketch **both** axes — a few open forks each — no questions yet.
2. **Derive the question surface.** Enumerate the open forks per axis. Rank by **leverage** (an answer
   that *cascades* into other decisions) and **load-bearing-ness** (a wrong default does real damage).
   Pick the highest-leverage: **2 Structural + 2 Mechanism** for round 1.
3. **Ground the options in reality.** Investigate the codebase / catalog / tokens / constraints so each
   option is **concrete, not abstract** — with a recommendation + the tradeoff per option. Abstract
   forks get rubber-stamped; grounded ones get *decided*.
4. **Grill in cascading rounds.** `AskUserQuestion` (discipline below). Then **re-derive**: each answer
   reshapes the surface — a "full set" answer pulls in the stateful-composite + sequencing forks; a
   chosen mechanism closes some forks and opens others. Re-rank, ask the next round. (This is the
   inverse of extraction's single round.)
5. **Converge + synthesize.** Stop at the convergence rule (below); restate the **Ratified Design**
   across **both** planes, ready to hand to `system-decompose` or the document author — scribe's
   `doc-forge` (governed by `doc-authoring-standards`) — where installed; otherwise draft each
   document type's minimum contract inline.

## AskUserQuestion discipline (per [[intent-extract]] — the deltas only)

The closed-question mechanics are MCQ discipline per [[intent-extract]], applied verbatim — batching,
question/option counts, header chips, "(recommended)"-first, the automatic "Other" escape, previews
where an option is a concrete artifact. That skill is the canon; don't re-derive it here. Grilling
changes exactly this:

- **Cascade, not one-shot.** Extraction batches *everything* into one round; grilling runs
  *multiple* rounds because answers reshape the surface. Still never **drip** — each round is a full
  batch. You stop adding rounds when the surface **settles**, not when you run out of small doubts.
- **Every recommendation carries its tradeoff** — "(recommended) X — tradeoff: Y" — because a grill
  option commits a design decision, not a clarification.
- **Ground before you ask** — never present an abstract fork. Investigate first so the set is real ("the
  catalog already reserves these names"; "the token ladder stops here").

## Convergence rule — when to stop grilling

Stop when the surface is **settled enough to decompose**: every remaining open fork is either (a)
defaultable without cascading, or (b) downstream of a decision `system-decompose` will make anyway.
**Over-grilling is the mirror of over-extracting** — manufacturing rounds past convergence spends the
author's attention and stalls the design. If a fork stops cascading, default it (state the default) and
move to synthesis.

## Output contract — the "Ratified Design"

```
DECISION SPACE  — one line: what's being designed and why it's open (greenfield / large fork count).
AXES            — the two planes sketched: Structural forks · Mechanism forks.
DECISIONS       — each ratified decision, tagged [S]/[M], the option chosen, and the cascade it triggered.
GROUNDING       — the codebase/catalog/constraint facts the options were built on (so they were concrete).
OPEN (deferred) — forks intentionally left to a default or to system-decompose — each with its default.
RATIFIED DESIGN — both planes resolved: the structure (scope · element set · composition · sequencing) AND
                  the mechanisms (primitives · semantics · fidelity) — ready for system-decompose /
                  scribe's doc-forge (doc-authoring-standards).
```

## Validation loop (finalize only when clean)

Check the Ratified Design and fix what fails — re-check until all pass:

- **Both-planes test** — does it name decisions on **both** axes? Structure with no mechanism (or
  vice-versa) ran one plane and inherits its blindness → derive the missing axis.
- **Leverage test** — was each round the highest-leverage open forks, or did a *cascading* decision get
  left to a silent default? If a load-bearing fork was defaulted, surface it.
- **Grounding test** — was every option **concrete** (traceable to a codebase/catalog/constraint fact),
  not abstract? Abstract forks get rubber-stamped → re-ground and re-ask.
- **Convergence test** — did grilling stop at *settled*, not manufacture rounds past it (over-grilling)
  nor stop short (a load-bearing fork reaching `system-decompose` unhosted)? → adjust.
- **Handoff test** — could `system-decompose` run **both** planes from this without another grilling
  round? If not, a load-bearing fork is still open → one more round.

**Done** = all five validation tests pass: decisions tagged on both planes, every option grounded,
every deferred fork carrying its default, and `system-decompose` able to run both planes verbatim;
**NOT done** = a one-plane grill, an abstract fork rubber-stamped as decided, rounds manufactured past
a settled surface, or a cascading fork left to a silent default.

## Worked example — container/layout family (2026-06-28)

The teaching point: the **axes DERIVED the questions**, and each answer **RESHAPED the next round**.

**Decision space.** A new container/layout component family for agent-ui (G9) — greenfield, most
decisions unmade.

**Round 1 — 2 Structural + 2 Mechanism, the highest-leverage forks:**
- `[S]` *scope/breadth* — minimal stack primitives vs a full layout set?
- `[S]` *consumer* — author-facing (hand-written) vs A2UI-driven (catalog) vs **both**?
- `[M]` *nested-radius mechanism* — how does a child's corner radius relate to its parent's (the
  load-bearing geometry)?
- `[M]` *surface model* — light-DOM like the existing controls vs shadow encapsulation?

**Ground before round 2.** Inspected the A2UI catalog spec → `Row` / `Column` / `Card` / `Tabs` /
`Modal` are already **reserved** names (experimental/absent until layout primitives land). That fact
**reshaped** the element-set question: the names aren't free; the set must align with the reserved
catalog.

**Round 2** (reshaped by round 1's "both consumers" + the catalog fact):
- `[S]` *element set* — which of the reserved {Row, Column, Card, Tabs, Modal} land in this family, and
  in what order? A **"full set"** answer cascaded → pulled in the stateful composites.

**Round 3** (pulled in by the full-set answer):
- `[M]` *Tabs/Modal a11y* — roll our own vs native `<dialog>` for Modal; the focus/escape semantics.
- `[S]` *composition* — do containers nest arbitrarily, and how does the round-1 nested-radius decision
  propagate down the tree?

**Round 4** (the tail):
- `[S]` *phasing* — which primitives ship first (sequencing).
- `[M]` *density + binding* — density tokens; the per-prop binding slice.

**16 decisions over 4 rounds → a ratified design** (both planes: element set · composition · phasing on
Structural; nested-radius · native-`<dialog>` · density on Mechanism) handed to
planning / `system-decompose`. No round was a pre-planned checklist — each was *derived* from the two
axes and *reshaped* by the prior answers.

## References & tools

| Path | Use when |
|---|---|
| `AskUserQuestion` | Every grilling round — closed multiple-choice forks |
| `references/foundations.md` | The models behind design-time decision derivation |
| `references/best-practices.md` | The do/don't — deriving from both axes, cascading rounds, grounding |
| `references/rubric.md` | Score a Ratified Design (the skill's output) |

A Ratified Design is write-once: when the ground shifts — a constraint, the scope, a reserved name —
**re-grill the affected forks** on the live surface; never patch the old ratification, whose cascade
was derived from facts that no longer hold.
