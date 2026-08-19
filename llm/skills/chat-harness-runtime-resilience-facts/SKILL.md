---
name: chat-harness-runtime-resilience-facts
description: >-
  How a deployed chat runtime's producer loop stays honest across turns and failures. Use for a
  per-turn validator judging the session's accumulated state, a cross-payload violation caught
  producer-side, a disclosure knob that must stay fail-closed and independent (no accidental
  ladder), a stream that already committed 200 needing a reserved terminal error line, halting
  loudly at a retry bound, and redacting raw upstream text from errors. Grounded in
  @agent-ui/a2ui's producer loop; answers, no build. NOT an implementation ask
  (implement/build/write the code — route to your own project's build seat). NOT for the
  instruction/config layer (chat-harness-guardrail-facts); NOT for retry-feedback prompt design
  (chat-harness-workflow-facts); NOT for provider/secret trust (llm-gateway-facts).
disable-model-invocation: false
user-invocable: false
---

# chat-harness-runtime-resilience-facts — a deployed chat runtime's producer loop stays honest

Answers how a deployed chat runtime's producer loop keeps its promises across turns and across
failures — not necessarily an enterprise platform. Split out of `chat-harness-guardrail-facts`
2026-08-17 (`plan-skill-split`, issue #552) once that pack's axis count drifted to 8, one past the
`pack-writing-rules` 3-7 target: these two axes are grounded in a genuinely different worked
system (a deployed A2UI chat runtime's producer loop) than that pack's CLI-instruction-layer
axes, and use genuinely different trigger vocabulary (validator/disclosure-knob/terminal-error-line
vs. layering/precedence/risk-tier) — a real split, not a forced one. Every claim is grounded either
in a real, directly-verified worked instance (`@agent-ui/a2ui`'s `produce.ts`/`meta-line.ts`/
`validate.ts`) or a general platform fact — cited so a claim can be checked against a real, running
instance, never presented as the only valid way to build this layer.

| Ask | Load |
|---|---|
| Multi-turn validation gates — "my per-turn validator contradicts the consumer's cross-turn rules", "the model keeps re-sending what it was told not to", "validate against the session's accumulated state", "catch violations producer-side instead of shipping the error" | `references/multi-turn-validation-and-state-seeded-gates.md` |
| Disclosure knobs — "a progress/reasoning disclosure knob shouldn't leak more than intended", "should 'full' detail imply 'source' detail too" | `references/disclosure-knobs-and-progress-detail.md` |
| Failure surfacing — "a stream that already sent 200 needs to fail loudly", "halt at the retry bound instead of widening it", "an evolving seam must stay byte-identical when a new flag is absent", "don't leak raw upstream text in a user-visible error" | `references/failure-surfacing-in-a-chat-runtime.md` |
| Provenance — verified `file:line` vs. platform fact | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`sessionSeed`, `meta-line`, `ProduceHalt`, `progress`, …) and Read that section — the files are
   cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (a verified `file:line` or a
   platform fact) + the failure mode it prevents**. A resilience claim without the failure mode it
   exists to prevent is half an answer.
3. **Frame every claim at its right scale** — name explicitly when a full worked-instance pattern
   is complexity a mini/portable runtime can validly skip, versus when it's load-bearing the
   instant the runtime streams to a real client at all (most of this pack's content is the
   latter).

## The core invariants (why these patterns exist)

- **A per-payload validator in a multi-turn loop must judge the state the consumer will hold** — a
  session-blind gate and a stateful consumer guard can each be correct alone and still leave the
  model no legal output; persistent "misbehavior" is a harness question before it is a model
  question (multi-turn-validation-and-state-seeded-gates).
- **Every disclosure knob is fail-closed and independent — no accidental ladder** — a consumer
  needing more than one detail level is a deliberate future member, never an implied default
  (disclosure-knobs-and-progress-detail).
- **A stream that already committed 200 needs a reserved terminal error line** — otherwise a
  mid-stream halt reads client-side as a silently-empty success (failure-surfacing-in-a-chat-runtime).
- **Halt loudly at the round bound — a loud halt is a feature, never widen the bound to chase a
  misbehaving model** (failure-surfacing-in-a-chat-runtime).
- **An evolving producer/provider seam must stay byte-identical when a new opt-in flag is absent,
  and that guarantee must be TESTABLE, not just asserted** (failure-surfacing-in-a-chat-runtime).

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build or fix a deployed chat runtime's actual producer loop in YOUR project** → your project's
  own build seat (this pack teaches the pattern, it owns no codebase's source).
- **The instruction, safety, and config-authoring layer** (layering precedence, injection defense,
  action risk tiers, hook vs. prose, config precedence, config-schema/prompt-externalization) →
  [[chat-harness-guardrail-facts]] (the sibling pack this pack split out of) — a distinct concern
  from a deployed runtime's own producer-loop resilience.
- **The self-correct feedback loop's own prompt design** (what the retry-bound halt above is the
  backstop for) → [[chat-harness-workflow-facts]]'s `self-correct-feedback-design.md`.
- **The provider/secret trust-boundary pattern** (registry validation, dev-proxy, adapter
  injection, "a browser cannot hold a secret") → [[llm-gateway-facts]] — a narrower, different
  concern than this pack's runtime-resilience scope.

## Extending this pack

Extension: governed by [[make-pack]]
