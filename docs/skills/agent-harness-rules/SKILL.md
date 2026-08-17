---
name: agent-harness-rules
description: >-
  Standards for designing agent-native verification — HOW an agent autonomously tests a system it
  just built, instead of a human eyeballing a screenshot. Assert-layer choice, driver agent harness
  design, assertion/fixture grammar, mapping this estate's own instruments onto a SPEC's criteria,
  the Gen-UI grounding case. Use when designing a test harness, picking an assert layer, or judging
  a criterion agent-runnable vs human-only. NOT the doctrine requiring the plan
  (doc-writing-rules' `## Agent verification`, check-doc's J7 — this is the HOW); NOT investigating
  an already-scorable system (research-methods); NOT this estate's own gate mechanics
  (script-writing-rules — cited, not re-derived).
disable-model-invocation: false
user-invocable: false
---

# agent-harness-rules — designing verification an agent can run alone

A system whose QA runs through a human clicking through screenshots was designed without this
question asked: **could a coding agent have exercised this alone?** Usually yes, at a cheaper,
faster, more deterministic layer than the one QA ended up using — the layer just wasn't chosen on
purpose. This pack is the design method for that choice: where to assert, how to build the driver
that exercises the system, what an assertion has to look like to be agent-runnable at all, how to
map an estate's existing instruments onto a spec's criteria before reaching for a new one, and one
fully worked case (Gen-UI) that motivated the doctrine this pack answers to
(`doc-writing-rules`' `## Agent verification` section, `check-doc`'s J7 — see the NOT-line above:
that doctrine asks the question, this pack answers it).

Provenance: minted from issue #542 / `prd-agent-testability.md` (PR #559, D5), grounded in the
Gen-UI chat system case that motivated the doctrine — a fleet of driver agents with custom
instructions, tools, services, and integrations driving chats, whose scenario verification is
asserted at the pure-JSON payload layer instead of `claude-in-chrome` browser automation and
human-in-the-loop screenshot review.

## The five axes (the operable index)

Five files, five question types — under the pack-writing-rules 3–7 axis threshold, so no
`references/INDEX.md`: this table IS the retrieval map (the 2026-07-09 flat-corpus ruling).

| Ask | Load |
|---|---|
| "Where should this scenario assert — payload, API, browser, or a human?" | `references/assert-layer-choice.md` |
| "How do I build the driver agent(s) that exercise this system like a user would?" | `references/agent-native-harness-design.md` |
| "What does an assertion or fixture need to look like to be agent-runnable at all?" | `references/assertion-fixture-grammar.md` |
| "What in THIS estate already verifies this — do I even need a new harness?" | `references/estate-instrument-mapping.md` |
| "Show me a real system that did this" | `references/gen-ui-grounding-case.md` |

## How to use it

1. **Classify the ask** against the table above; Read only the matching file — this is a catalog,
   not a linear read.
2. **Estate mapping first, always.** Before designing anything new, check
   `references/estate-instrument-mapping.md` — the answer is frequently "an instrument you already
   have covers this," and the harness/fixture design axes are for the real gap that's left.
3. **Cite the layer and the trap.** Every answer names the chosen assert layer and the failure
   mode it avoids (a browser-only harness that can't run headless in CI; a JSON-only harness that
   misses a real rendering regression) — the corpus exists to correct the reflex of reaching for
   the highest-fidelity layer by default, not to ban it outright.

## Composition

- **`doc-writing-rules`** owns the contract this pack answers to — the `## Agent verification`
  section on SPEC/PRD/LLD, and `check-doc`'s J7 judging its substance. This pack is consulted
  *from* that section's authoring, never the other way around.
- **`research-methods`** is the adjacent method corpus for an already-scorable system; this pack
  is upstream of it — it's how a system BECOMES scorable in the first place.
- **`make-doc`**'s Phase 2 SPEC/PRD/LLD slots point here for how to answer the question they ask.
- No builder peer owns turning these axes into an actual running harness in this estate today —
  a target system's driver agent scaffold and fixtures are derived inline from the design axes
  above, not dispatched to a named seat.

Extension: governed by `/make-pack`.
