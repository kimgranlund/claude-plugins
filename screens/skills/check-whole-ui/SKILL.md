---
name: check-whole-ui
description: >-
  Audit a whole product UI — every screen, flow, and surface — for cross-cutting findings no
  single screen review catches: pattern drift, token misuse, repeated defect quadrants. Use for
  a pre-launch or post-redesign sweep: "audit this UI", "sweep for accessibility / i18n /
  latency / safety", "how consistent is this UI". Composes break-down-layout, break-down-flow,
  the five verifiers, and ui-pattern-facts/ui-genre-facts conformance. NOT for one screen
  (break-down-layout, layout-checker); one flow (break-down-flow); one component
  (make-component); naming a pattern/genre in the abstract (ui-pattern-facts, ui-genre-facts);
  one invariant (the five verifiers); or fixing findings — route to owners.
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
   (break-down-layout's axes: A = space outside-in, B = behavior inside-out; A1/A2 = its axis-A
   gates) is inherited, never re-reported per screen. Then run [[break-down-layout]] GRADE mode on each
   screen's view-owned regions — gates first, two axes separately, quadrant (break-down-layout's 2×2
   defect cell) named. Dispatching the `layout-checker` agent is mandatory when the layout is your
   own work (generator ≠ critic), optional otherwise; when two reviewers split on a gate, the
   auditor rules and documents the ruling in the report.
3. **Flow pass.** Declare each core flow as a `*.flow.json` card (the inventory's declared flows
   are the list); run [[break-down-flow]] GRADE —
   `python3 ../break-down-flow/scripts/flow-check.py <card|dir>` gates reachability/dead-ends/
   exit-truth mechanically; then walk each success exit's asserts against rendered truth (the
   probe, or hands-on) — an exit assert that fails is a gate finding. A flow you designed goes to
   the `flow-checker` agent (generator ≠ critic), as with layout in step 2.
4. **Invariant pass.** Build each verifier's card — its per-surface JSON input artifact — from the
   inventory, then run every invariant verifier: [[check-colors]] · [[check-focus]] ·
   [[check-translations]] · [[check-speed]] · [[check-safety]] (each description carries its own scope).
   Each has a deterministic checker — run it; a checker FAIL is a gate finding, not an opinion.
   When the app RUNS, generate the cards from rendered truth:
   `node scripts/ui-probe.mjs <baseURL> --inventory inventory.json` (needs playwright — the target
   repo's install works) — probed cards supersede hand-built ones; author by hand only what the probe
   can't reach, and report those as computed-not-measured.
5. **Pattern conformance.** Anchor the genre first — [[ui-genre-facts]] names what THIS category's
   users expect, so conformance asks "the right pattern for this kind of product", and a deliberate
   genre-convention violation is judged against the failure it courts, not flagged as drift. Then
   check the shared modules against [[ui-pattern-facts]]: is each module the
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
   `make-component` (or the repo's
   builder agent); tokens → the `token-builder` agent; copy/brand → out of scope, flagged.
   Persist the run: cards, checker outputs, inventory.json, and the `findings.jsonl` ledger
   (opened at step 1) — into a dated `audits/<date>/` dir in the target repo; then
   `python3 scripts/audit-diff.py <prev> <current>` — NEW findings are regressions and lead the
   report; a first run has no baseline: `--first-run` reports everything NEW with the gate off
   and establishes the baseline.

## Output contract

```
Inventory: <N screens · M flows · K shared modules>   [bounded? what was dropped]
Genre anchor: <genre>   (ui-genre-facts — the category whose conventions judged conformance)
Gate failures (all verifiers + layout gates), each: <inventory-ID · [RULE_ID] finding · owner · fix>  (rule IDs per references/verify-mechanics.md)
| Screen | Axis A | Axis B | Quadrant |
| Flow | gates | asserts verified | verdict |
Cross-cutting: 1) <[RULE_ID] finding — spread: which IDs — criticality (or "no tasks.json: spread-only") — systemic fix + owner> …  (this sweep's own judgment slugs: `audit.pattern-drift` · `audit.token-systemic` · `audit.quadrant-repeat`)
Verifier summary, three-valued: color <pass|fail|UNMEASURED(what's missing)> · focus <…> · i18n <…> · perf <…> · safety <…>
  (a card that could not be built reports UNMEASURED — skipped is never laundered into pass)
Delta vs baseline: <N new · M resolved · K still-failing · W waived (each: [RULE_ID] · reason · date — visible, never deleted)>   (or: first run — baseline established)
```

## Boundaries

- This sweep OWNS the verify-family canon — `references/verify-mechanics.md` (rule-ID'd findings,
  the scope ladder, monotonicity, repair-scope, the waiver ladder with its anti-sycophancy
  clause, armed mode, symptom indexes). The sibling verifiers cite it; disputes about a finding
  route through its waiver ladder. `audit-diff.py` mechanizes §3's never-regress side at sweep
  scope (NEW findings gate); STILL_FAILING carries the addressed-gone side to the auditor's
  judgment. The GATE findings enter `findings.jsonl` and the delta; cross-cutting judgment
  findings carry their rule IDs in the report and are compared by hand. A partial re-audit
  verifies at fix scope (canon §2/§3) and is NEVER persisted as an `audits/<date>/` baseline —
  diffing a partial run against a full baseline mints false RESOLVED entries. Waived findings
  stay in the ledger and the gate count; the report's W row annotates them from the project's
  DESIGN.md — a waiver is visible, never a deletion.

- One screen, not the set → [[break-down-layout]]. One component → the `component-checker` agent.
- This skill orders the instruments and synthesizes; each instrument's depth stays its own — never
  restate a verifier's rules here, run it.
- Finding ≠ fix: the audit report routes work, it performs none. Re-audit only the failed IDs after
  fixes land, not the whole set.

**Done** = every inventory ID graded or stated dropped · all five verifiers reported three-valued ·
every finding routed to an owner · the delta diffed against baseline. **NOT done** = a sample
posing as a sweep · an UNMEASURED reported as pass · a finding with no owner.
