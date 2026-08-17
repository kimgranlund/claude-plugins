# Assertion and fixture grammar — what makes a criterion agent-runnable

Not every acceptance criterion that SOUNDS testable actually is, at any layer. This file is the
grammar test: given a criterion, what shape must its assertion and fixtures take before an agent
can run it unattended.

## The agent-runnable test

A criterion is agent-runnable when it can be phrased as **one of these four assertion shapes**,
against **one named fixture or golden artifact** — anything else is eyeball-only until it's
rephrased:

1. **Golden-payload equality** — the system's output, at the chosen assert layer, matches (or
   structurally subsumes) a stored golden payload for a given fixed input. Best for: content and
   behavior questions ("the agent calls `search` with these arguments given this prompt").
2. **Schema assert** — the output validates against a declared schema (types, required fields,
   enum membership) regardless of the exact values. Best for: contract stability questions ("the
   response always carries a `status` field from this fixed vocabulary") — looser than golden
   equality, catches structural drift without over-fitting to one exact payload.
3. **Property assert** — a stated invariant holds across a generated or swept range of inputs
   ("total never exceeds the sum of its parts", "the response is always valid JSON") rather than
   one fixed example. Best for: questions a single example can't falsify.
4. **State-transition assert** — a before/after pair: the system's persisted or session state
   changes in a named way given a named action, checked by reading the state back at the chosen
   layer. Best for: "did the action actually happen" questions, independent of what got rendered.

A criterion that resists all four — "the response feels natural," "the layout looks right" — is
either (a) genuinely a human-review criterion (name it as the exception), or (b) under-specified
and needs a sharper requirement before it earns a criterion at all (`doc-writing-rules` practice
5: "author the evaluator with the artifact" — if the evaluator can't be written, the requirement
wasn't finished).

## Fixtures vs golden artifacts

- **Fixture** — the deterministic INPUT state a scenario starts from (a seeded database row, a
  frozen clock, a canned upstream response). Owned by the scenario, versioned with it.
- **Golden artifact** — the recorded EXPECTED output a golden-payload assertion compares against.
  Golden artifacts drift on purpose (the system's real behavior legitimately changes) and on
  accident (a regression) — the review discipline that tells those apart is: a golden-artifact
  update rides in the SAME change as the code change that caused it, with the diff visible in
  review, never regenerated silently by re-running the suite and committing whatever came out.
  **[inferred]**: same discipline this estate already applies to its own template
  self-consistency fixtures (`doc_lint.py`'s selftest) and script selftest fixtures generally —
  translated here to a target system's own golden artifacts.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Vibes criterion | "should feel responsive" has no assertion shape | Rephrase to a measurable property (p95 latency) or name it a human-review exception |
| Silent golden drift | Golden artifact regenerated and committed without review, hiding a real regression | Golden updates ride in the same reviewed change as the behavior change that caused them |
| Over-fit golden equality | Exact-match assertion breaks on every harmless formatting change | Prefer schema/property asserts for anything not genuinely content-fixed |
| Under-fixtured scenario | No named starting state; the scenario "just runs" against whatever state happens to exist | Every scenario names its fixture explicitly, versioned with the scenario |

## Sources

- `[inferred]` The four assertion shapes: synthesized for this pack from standard testing
  practice (example-based/golden testing, schema validation, property-based testing, state
  assertions) — not a verbatim citation of one external source, applied here to the specific
  question of "is this criterion agent-runnable."
- `[verified]` The golden-artifact review discipline, cross-checked against this repo's own
  `docs/scripts/doc_lint.py` `selftest()` (2026-08-17): every template fixture change in that
  script rides in the same commit as the assertion it's proving, never regenerated separately.
