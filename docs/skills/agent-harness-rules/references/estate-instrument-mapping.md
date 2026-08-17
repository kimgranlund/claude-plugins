# Estate instrument mapping — what a testing foundation already IS for a plugin estate

Before designing any new harness, check what already exists. For an estate shaped like this one
(a Claude Code plugin workspace), a real testing foundation is not a gap to fill from scratch —
most of it already exists as this estate's own standing instruments. This axis is the doctrine
rule `## Agent verification` actually asks a SPEC to apply: **name which existing instrument
verifies each criterion, or name the harness to build first** — never silently assume nothing
exists.

## The four standing instruments (this estate, `[verified]` against its own scripts, 2026-08-17;
also `[drift-prone]` — a gate added or renumbered in a future harness release is not reflected
here automatically; re-verify against `harness/scripts/release_gate.py`'s own docstring at every
release boundary)

1. **`evals/evals.json` trigger suites** — routing verification: does a skill's description fire
   on the prompts it should and stay silent on its fenced neighbors' prompts. Run via
   `harness/scripts/eval_check.py`; swept by `release_gate.py`'s **G7** (every model-invocable
   skill without a suite WARNs). Answers ROUTING criteria — "does this get invoked when it
   should" — never content/behavior criteria.
2. **Bundled-script selftests** — every `scripts/*.py|.mjs|.js` in every plugin carries a
   `selftest` mode proving its own counters bite (`.claude/rules/scripts.md`); swept by
   `release_gate.py`'s **G4**, which fails the gate on any non-zero selftest exit. Answers
   MECHANICAL criteria for a script's own logic — the payload-layer assertion shape
   (`references/assertion-fixture-grammar.md`'s golden/schema/property/state-transition grammar)
   IS what a good selftest already is.
3. **`release_gate.py`'s full sweep (G1–G11)** — manifest validity, structure, lint, selftests,
   phantom-handle sweep, packaging, eval-suite presence, sibling-name collisions, docs freshness,
   pack corpus checks, style lint — one aggregate command per plugin. Answers PACKAGING and
   STRUCTURAL criteria: is this plugin shippable, not whether one feature inside it behaves
   correctly.
4. **`/check-routing`** — a blind LLM-judge routing simulation over a plugin's (or a bare
   project estate's) full skill menu, reporting stolen/leaked/dead routing. Answers the CROSS-SKILL
   routing question G7's per-suite check can't see: does this skill's description collide with a
   sibling's at menu scale.

## The mapping move

For each Acceptance/Outcome criterion, ask in order: (1) does an existing evals suite already
prove this (a routing claim)? (2) does an existing or buildable script selftest already prove this
(a mechanical claim about one script's own logic)? (3) does the release gate's own sweep already
prove this (a packaging/structural claim)? (4) none of the above — this is a genuine new-harness
gap, and `references/agent-native-harness-design.md` + `references/assert-layer-choice.md` are
where the design work happens. **A SPEC that reaches step 4 for every criterion without checking
1–3 first is very likely re-building an instrument that already exists.**

## Where the gap actually is

For THIS estate, steps 1–3 cover routing and packaging exhaustively — the estate has no standing
gap there. The gap this pack exists to close is entirely in **target systems this estate's own
agents build for other repos** (the Gen-UI case, `references/gen-ui-grounding-case.md`) — a chat
system, an API service, anything with its own runtime behavior beyond "does this plugin load and
route correctly." No new estate-level gate is scoped by this pack (PRD D4) — the estate's own
instruments are sufficient; a target system's own instrument set is what each SPEC for that system
must build or name.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Reinvented instrument | A new ad-hoc script built to prove something G4/G7/G1-G11 already proves | Run the mapping move before designing anything |
| Wrong-grain instrument | Using `/check-routing`'s cross-skill judgment to answer a single-skill mechanical question | Match the criterion's grain to the instrument's own grain (per-skill vs cross-skill vs per-script) |
| Estate/target confusion | Treating a target system's missing harness as an estate-level gate | This estate's own instruments are the answer for THIS estate; the target system earns its own |

## Sources

- `[verified]` G1–G11 gate contents, G4/G7 mechanics: `harness/scripts/release_gate.py`'s own
  module docstring and fail/warn call sites, read 2026-08-17 (this build).
- `[verified]` The selftest requirement's own path scope and rule: `.claude/rules/scripts.md`.
- `[inferred]` The mapping-move ordering (routing → mechanical → packaging → new-harness) is this
  pack's own synthesis for the agent-testability doctrine, not a pre-existing external citation.
