---
name: run-brand-elicit
description: >-
  Builds a brand-guidelines section by guided 2x2 choice — presents four concrete options for a
  domain (mark, voice, color, type, expression, governance), the designer picks a quadrant +
  comments, and the choice accumulates into a provenance-traced corpus. Use when the user wants to
  build, elicit, or structure brand guidelines interactively — "build brand guidelines", "guide me
  through the brand design system", "give me a 2x2 for the brand voice", "elicit the color/type
  system", "help me decide the brand expression". Owned by brand-guidelines (cited, not restated)
  — this sets posture and resumes the frontier. NOT open strategy work (make-brand) or adversarial
  scoring (check-brand-rubric).
disable-model-invocation: false
user-invocable: true
argument-hint: "[domain — mark|voice|color|type|expression|governance; default: resume the frontier]"
---

# run-brand-elicit

Guided-choice mode: builds a brand-guidelines section by presenting a 2x2 of concrete options per
domain and letting the designer pick + comment. Posture is maker — options are proposed, the
designer supplies the taste, this never grades its own output (that's `check-brand-rubric`).

Domain to work, or resume the frontier if blank: `$ARGUMENTS` (one of `mark | voice | color | type
| expression | governance`).

## Procedure

1. **Resolve the domain.** Blank `$ARGUMENTS` → resume at the uncovered frontier; a named domain →
   work that one.
2. **Hand off to the mechanism.** Invoke the `brand-guidelines` skill — it owns the full loop (the
   six domains, the seven axes + default pair, the design-move card, the pick model, drill-down,
   coherence, the ledger CLI, coverage and assembly). This skill does not restate that mechanism —
   read `brand-guidelines`'s own body and
   `${CLAUDE_PLUGIN_ROOT}/skills/brand-guidelines/references/the-loop.md` for it.
3. **Ground in the corpus first.** Before generating any option, `brand-guidelines`'s own
   procedure reads `01-foundation` plus the existing choice-ledger under the default corpus root
   `./brand-corpus` (the same default `save-brand-corpus` and `make-brand-stack` use) — this skill
   doesn't re-check that; it's `brand-guidelines`'s own Step 2.
4. **Report the round.** Relay the domain worked, the pick captured, and the coverage state
   `brand-guidelines` returns; don't re-summarize the mechanism.

## Failure branches

- A card can only be written by asserting rather than tracing it to `01-foundation` → that's an
  undone foundation, not an elicitation problem: say so, and point at `make-brand` to ground it
  first, rather than forcing an ungrounded card.
- `$ARGUMENTS` names a domain outside the six → say so and list the six; don't guess the nearest
  one.

## Done / NOT done

Done when `brand-guidelines`'s own stopping condition for the round is met (a choice appended and
validated) and the coverage state is relayed. NOT done if a design-move card was generated without
tracing it to `01-foundation`, or this skill re-implemented any part of the loop `brand-guidelines`
already owns.
