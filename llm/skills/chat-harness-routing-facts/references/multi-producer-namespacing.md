# Multi-producer orchestration — namespace ids, classify three ways

> Axis: when more than one producer can create surfaces/resources on the same session, how their
> ids are kept from colliding or being cross-mutated. Grounded in a worked instance:
> `@agent-ui/a2ui`'s `enforceSurfacePrefix`, `packages/agent-ui/a2ui/src/agent/session.ts`.

## Own / unprefixed / foreign — three classes, three responses

**Claim — namespace surface/resource ids deterministically and classify every incoming id three
ways: OWN ids pass idempotently; UNPREFIXED (model-authored) ids are rewritten onto the
namespace, deterministically, so a create and its same-batch populate stay paired; FOREIGN ids
(another producer's namespace) are REJECTED outright, never rewritten — a producer must never
patch or read a sibling's surfaces.** · `session.ts:110-208` (`enforceSurfacePrefix`, ecosystem
SPEC-R4/GH #475) · 2026-08-17 · [verified]

**Caveat worth naming explicitly:** rewriting only applies to CREATE operations, not updates — a
same-batch populate targeting an id that was just rewritten on create can be silently stranded as
a foreign reject if the rewrite and the populate don't agree on the final id. This is a real,
named edge the pattern must account for, not a hypothetical.

## What this file does NOT cover

The structural discriminator that tells a namespaced-surface line apart from an ordinary content
or meta line in the first place: `envelope-framing-and-out-of-band-signals.md`. Verifying a
model's own routing DECLARATION (an `ask` naming a surface) against what actually happened:
`model-declared-routing-integrity-check.md`.
