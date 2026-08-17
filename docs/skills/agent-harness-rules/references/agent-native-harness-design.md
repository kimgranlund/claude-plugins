# Agent-native harness design — driver agents that exercise the system like a user would

Once the assert layer is chosen (`references/assert-layer-choice.md`), the harness itself is a
**fleet of driver agents** — not a human, not a hand-scripted macro — each with its own scoped
instructions, tools, and integrations, exercising the target system the way a real user or a real
upstream service would.

## The driver agent shape

A driver agent for verification carries four things, each scoped down from what the target
system's real users get:

1. **Custom instructions** — a persona and a goal ("you are a user trying to accomplish X"), not
   the target system's own system prompt reused verbatim; the driver's job is to probe, not to
   perform the target's own role.
2. **Scoped tools** — only what's needed to drive the scenario (send a message, read the payload
   back, assert a field) — never the target's own full tool surface, which would let the driver
   silently do the target's job instead of exercising it.
3. **Services and integrations** — the real (or a faithful fixture) backing services the target
   depends on, wired so the scenario runs deterministically — see Determinism below.
4. **A scenario, not a script** — a stated goal and success condition, letting the driver's own
   reasoning generate the interaction path, which surfaces failure modes a fixed click-sequence
   script never would (the target misbehaving on an input the scripted path never tries).
   **[inferred]**: this is the core distinction between "browser automation" (a fixed script) and
   "agent-native harness design" (a reasoning driver) — the latter costs more to build per
   scenario but finds more of the failure space per scenario run.

## Scenario definition

A scenario states: the driver's goal, the fixtures/starting state, the assert layer
(`references/assert-layer-choice.md`), and the success/failure condition in the assertion grammar
(`references/assertion-fixture-grammar.md`). A scenario with no stated success condition is not
verification, it's a transcript.

## Determinism and isolation

Two requirements a verification harness cannot skip, or every run becomes a coin flip:

- **Determinism** — the same scenario run twice produces the same verdict. Fixture the driver's
  own inputs where the target's response is itself variable (seed a model call, freeze a clock,
  pin a random seed) — an assertion that only sometimes fails on the same bug is worse than no
  assertion, because it teaches the team to ignore red.
- **Isolation** — one scenario's driver agent never shares mutable state with another's running
  concurrently (a shared database row, a shared session) — the same contention-vs-regression
  discipline this estate applies to its OWN test suite (a red result under concurrent load reads
  as a contention verdict, not a regression verdict, until reproduced in isolation), generalized
  here to a target system's own harness. **[inferred]**, translated from that adjacent discipline
  rather than independently re-derived; no dedicated skill file names it in this estate today, so
  it is cited as a discipline, not as a specific document.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Scripted, not reasoning | A fixed click/call sequence never explores an input the script's author didn't anticipate | Give the driver a goal and let it reason the path, assert on the outcome |
| Full-tool-surface driver | The driver agent gets the target's own tools and starts doing its job instead of testing it | Scope the driver's tools to probe-only actions |
| Non-deterministic fixtures | Same scenario, different verdict run to run — team learns to ignore red | Seed/freeze every source of the target's own variability before asserting |
| Shared mutable state | Two scenarios racing on the same row/session produce a false failure under concurrency | Isolate scenario state; never assume serial execution |

## Sources

- `[inferred]` The driver agent shape and scenario-definition discipline: distilled for this pack
  from the Gen-UI grounding case (issue #542, 2026-08-17) — see
  `references/gen-ui-grounding-case.md`. Not independently verified against a published external
  framework; treat as this estate's own applied synthesis, not an industry-standard citation.
- `[inferred]` Determinism/isolation requirements translated from this estate's own
  `flaky-gates` doctrine (harness plugin) applied to a target system's harness rather than this
  estate's own test suite.
