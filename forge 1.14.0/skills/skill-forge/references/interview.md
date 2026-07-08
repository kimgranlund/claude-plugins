# The intent interview — question bank and record schema

One question per turn. Skip any slot the user's opening request already answers — re-asking answered questions is interview theater. A slot is closed when its "complete when" condition holds, not when an answer of any kind exists.

## Slot 1 — Trigger

- "What will you (or Claude) say or be doing when this skill should fire? Give me the actual words you'd type."
- "Give me two or three more phrasings of the same request — different words, same intent."
- For model-invocable candidates: "What nearby request should this skill NOT fire on?"

Complete when: ≥ 3 verbatim should-trigger phrasings and ≥ 1 should-not-trigger neighbor are recorded.

## Slot 2 — Behavior delta (the grilling)

- "What does Claude do today, without this skill, that this skill fixes? Show me a wrong output if you have one."
- "If you deleted this skill after a month, what would break or degrade?"
- Challenge, stated plainly when it applies: "The behavior you described is something Claude already does correctly — this skill would restate model knowledge. What's the piece Claude actually gets wrong?"

Complete when: a concrete wrong-vs-desired contrast is recorded (an example pair, or a crisp description of the failure). No demonstrable delta → recommend stopping; record the recommendation and the user's decision.

## Slot 3 — Species and dials

- "Does running this have side effects — deploys, commits, messages, anything you'd want to time yourself?" (yes → command)
- "Is this a meaningful action for a person to type as `/name`, or background knowledge Claude should apply when relevant?" (knowledge → model-only)
- "Will an agent need this preloaded?" (yes → it must stay model-invocable; `disable-model-invocation: true` blocks preloads)

Complete when: species named, both dial values chosen, and the name's grammar agrees (verb head for invocables, knowledge noun for model-only).

## Slot 4 — Degrees of freedom

- "Are there many valid ways to do this, one preferred pattern, or exactly one fragile sequence that must not vary?"
- Low freedom → "What's the exact sequence? We'll bundle it as a script rather than describe it."

Complete when: high / medium / low recorded, and low-freedom answers include the script's spec.

## Slot 5 — Type

- "Can Claude already do each piece of this, and the skill just sequences them your way (encoded preference) — or is there a step Claude can't do reliably at all (capability uplift)?"

Complete when: one of the two is recorded. Preference skills get the brevity note: state the sequence and stop.

## Slot 6 — Fences

- "What adjacent requests will people aim at this skill that belong elsewhere? Where do those belong?"

Complete when: each fence is recorded in the parseable form `NOT for <thing> (<owner>)`, ready to paste into the description.

## Slot 7 — Done-when

- "How will we know the skill works? Name 3+ checkable statements about its output." (These become Phase 2's behavioral assertions.)

Complete when: ≥ 3 assertions recorded, each checkable against an output artifact.

## The intent record — `<skill-dir>/intent.md`

```markdown
# intent — <skill-name>
status: forging          # forging | parked | shipped
species: <procedural | knowledge | command>
dials: { disable-model-invocation: <bool>, user-invocable: <bool> }
freedom: <high | medium | low>
type: <capability-uplift | encoded-preference>

## trigger
should:      ["<verbatim>", "<verbatim>", "<verbatim>"]
should_not:  ["<verbatim>"]

## delta
<wrong-vs-desired contrast, or example pair paths>

## fences
- NOT for <thing> (<owner>)

## assertions
1. <checkable statement>
2. <checkable statement>
3. <checkable statement>

## gates
P0 route:      PENDING
P1 intent:     PENDING
P2 evals:      PENDING
P3 draft:      PENDING
P4 language:   PENDING
P5 validate:   PENDING

## rulings
<accepted-with-note findings; auditor/author arbitrations; parked-gap notes>
```

The record is living state while forging and ships inside the skill directory as provenance when done — future maintainers read why the skill exists and what it promised before editing it.
