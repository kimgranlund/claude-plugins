---
name: ui-audit
description: >-
  Audit a whole product UI — every screen, flow, and surface — for cross-cutting findings no
  single screen review catches. Use when sweeping a product before launch or after a redesign:
  "audit this UI", "review the whole app's UX", "sweep this product for accessibility / i18n /
  latency / safety issues", "how consistent is this UI", "pre-launch UI review", "the same data
  table paginates on one page and infinite-scrolls on another". Composes the owned design
  instruments over the SET: layout-decompose per screen, flow-decompose per flow, the invariant
  verifiers (color-verify · focus-verify · i18n-verify · perf-verify · safety-verify), and
  ui-patterns conformance anchored to the product's genre (ui-genres) — then
  synthesizes what only the whole reveals (pattern drift across screens, systemic token misuse,
  repeated defect quadrants). NOT for grading one screen, shell, or wireframe (layout-decompose /
  the layout-reviewer agent); NOT for one flow (flow-decompose); NOT for one component
  (component-author / component-reviewer); NOT for naming a pattern or genre in the abstract —
  master-detail or list-detail (ui-patterns / ui-genres); NOT for one invariant in isolation
  (the five verifiers); NOT for fixing what it finds — findings route to owners.
disable-model-invocation: false
user-invocable: true
---

# UI audit — the set-scoped sweep

A screen-by-screen review is blind to the product: pattern drift, systemic token misuse, and a
defect quadrant that repeats on every page exist only across the set. This audit runs the owned
instruments over every surface, then synthesizes the cross-cutting findings.

## Procedure

1. **Inventory + ledger (the spine).** Enumerate the auditable set: screens/routes, flows (the 3–7
   core user journeys), and shared modules (nav, tables, forms, dialogs). Number them — every later
   finding cites an inventory ID. Open `findings.jsonl` beside the inventory — the normalized
   ledger, one JSON object per gate finding `{checker, gate, id, screen?, detail?}`, appended as
   each finding lands from step 2 on; jointly they are the spine: the inventory names what was
   audited, the ledger what was found. An audit without an inventory is a sample pretending to be a sweep; if you
   bound the set (top-N screens), say so in the report. Mechanize it where source is available:
   `python3 scripts/inventory-scan.py <src>` emits the scanned inventory (+ `--manifest` for
   declared flows/screens); scanned inventory is assisted, not gospel — confirm module identities
   before grading. Optionally declare `tasks.json` — `[{id, task, criticality: 1|2|3, flows: [],
   screens: []}]`, auditor-declared or derived from the PRD (3 = the product's reason to exist:
   money, core loop; 2 = supporting; 1 = peripheral) — step 6's ranking weight.
2. **Per-screen layout pass.** Grade the SHELL once, as its own inventory item — its A1/A2 verdict
   (layout-decompose's axes: A = space outside-in, B = behavior inside-out; A1/A2 = its axis-A
   gates) is inherited, never re-reported per screen. Then run [[layout-decompose]] GRADE mode on each
   screen's view-owned regions — gates first, two axes separately, quadrant (layout-decompose's 2×2
   defect cell) named. Dispatching the `layout-reviewer` agent is mandatory when the layout is your
   own work (generator ≠ critic), optional otherwise; when two reviewers split on a gate, the
   auditor rules and documents the ruling in the report.
3. **Flow pass.** Declare each core flow as a `*.flow.json` card (the inventory's declared flows
   are the list); run [[flow-decompose]] GRADE —
   `python3 ../flow-decompose/scripts/flow-check.py <card|dir>` gates reachability/dead-ends/
   exit-truth mechanically; then walk each success exit's asserts against rendered truth (the
   probe, or hands-on) — an exit assert that fails is a gate finding. A flow you designed goes to
   the `flow-reviewer` agent (generator ≠ critic), as with layout in step 2.
4. **Invariant pass.** Build each verifier's card — its per-surface JSON input artifact — from the
   inventory, then run every invariant verifier: [[color-verify]] · [[focus-verify]] ·
   [[i18n-verify]] · [[perf-verify]] · [[safety-verify]] (each description carries its own scope).
   Each has a deterministic checker — run it; a checker FAIL is a gate finding, not an opinion.
   When the app RUNS, generate the cards from rendered truth:
   `node scripts/ui-probe.mjs <baseURL> --inventory inventory.json` (needs playwright — the target
   repo's install works) — probed cards supersede hand-built ones; hand-build only what the probe
   can't reach, and report those as computed-not-measured.
5. **Pattern conformance.** Anchor the genre first — [[ui-genres]] names what THIS category's
   users expect, so conformance asks "the right pattern for this kind of product", and a deliberate
   genre-convention violation is judged against the failure it courts, not flagged as drift. Then
   check the shared modules against [[ui-patterns]]: is each module the
   canonical pattern for its job, and is it the SAME pattern everywhere it recurs — where "same"
   includes the same *behavior contract*: a module that looks identical but acts differently across
   screens (a door that opens a real intake on one screen and an empty modal on four) is the
   set-level defect, and a presence-regex gate that blesses it is a gamed gate? A data table
   paginated on one screen and infinite-scrolled on its twin is a set-level defect no single screen
   shows.
6. **Synthesize.** Roll up gate failures first, then cross-cutting findings: patterns that drift
   across screens, a verifier failure that recurs (systemic, fix at the token/module level, not
   per-screen), quadrant cells that repeat. Rank by severity × spread × task-criticality (from
   `tasks.json` when declared; absent → severity × spread only, and the report says so) — one
   finding touching a criticality-3 flow outranks a wider finding on criticality-1 surfaces.
   Route every finding to its owner: layout → the screen's maker; component internals →
   `component-author` (or the repo's
   builder agent); tokens → the `token-builder` agent; copy/brand → out of scope, flagged.
   Persist the run: cards, checker outputs, inventory.json, and the `findings.jsonl` ledger
   (opened at step 1) — into a dated `audits/<date>/` dir in the target repo; then
   `python3 scripts/audit-diff.py <prev> <current>` — NEW findings are regressions and lead the
   report; a first run has no baseline: `--first-run` reports everything NEW with the gate off
   and establishes the baseline.

## Output contract

```
Inventory: <N screens · M flows · K shared modules>   [bounded? what was dropped]
Genre anchor: <genre>   (ui-genres — the category whose conventions judged conformance)
Gate failures (all verifiers + layout gates), each: <inventory-ID · finding · owner · fix>
| Screen | Axis A | Axis B | Quadrant |
| Flow | gates | asserts verified | verdict |
Cross-cutting: 1) <finding — spread: which IDs — criticality (or "no tasks.json: spread-only") — systemic fix + owner> …
Verifier summary, three-valued: color <pass|fail|UNMEASURED(what's missing)> · focus <…> · i18n <…> · perf <…> · safety <…>
  (a card that could not be built reports UNMEASURED — skipped is never laundered into pass)
Delta vs baseline: <N new · M resolved · K still-failing>   (or: first run — baseline established)
```

## Boundaries

- One screen, not the set → [[layout-decompose]]. One component → the `component-reviewer` agent.
- This skill orders the instruments and synthesizes; each instrument's depth stays its own — never
  restate a verifier's rules here, run it.
- Finding ≠ fix: the audit report routes work, it performs none. Re-audit only the failed IDs after
  fixes land, not the whole set.

**Done** = every inventory ID graded or stated dropped · all five verifiers reported three-valued ·
every finding routed to an owner · the delta diffed against baseline. **NOT done** = a sample
posing as a sweep · an UNMEASURED reported as pass · a finding with no owner.
