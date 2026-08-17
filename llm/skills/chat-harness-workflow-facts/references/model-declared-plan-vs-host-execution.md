# Let the model declare its own plan as data — keep execution host-side

> Axis: when a model wants to communicate a multi-step intent to the host, what shape that
> declaration should take and who is trusted to actually run the steps. Grounded in a worked
> instance: `@agent-ui/a2ui`'s reserved meta envelope, `packages/agent-ui/a2ui/src/agent/
> meta-line.ts`.

## Declaring intent and executing it are different trust levels

**Claim — a `plan: {steps:[{id, description}]}` declaration rides the reserved meta envelope,
model-authored, passed through unchanged with no runtime rewriting; the host-side
plan→execute→synthesize loop is a SEPARATE contract the model's declaration does not itself
trigger or control.** · `packages/agent-ui/a2ui/src/agent/meta-line.ts:76-90` (ADR-0174/SPEC-R20)
· 2026-08-17 · [verified]

**Why this matters (the failure mode it prevents):** if a model's own declared plan were also
what DROVE execution, a hallucinated or malformed plan step could directly cause host-side
action — separating "the model says what it intends" from "the host decides what actually runs"
means a plan is always a proposal the host is free to validate, reject, or execute deliberately,
never an implicit command.

## What this file does NOT cover

The envelope's own structural discriminator and how a plan line is told apart from ordinary
content (a distinct, wire-level concern): [[chat-harness-routing-facts]]'s
`envelope-framing-and-out-of-band-signals.md`. The non-destructive merge law governing a
DIFFERENT kind of model-authored declaration (a memory/persona patch, not a plan):
[[chat-harness-memory-facts]]'s `model-authored-memory-patch-non-destructive-writes.md`.
