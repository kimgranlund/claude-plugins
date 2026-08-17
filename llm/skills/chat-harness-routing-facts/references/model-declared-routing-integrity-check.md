# A model-declared routing fact must be checked against reality, then silently degrade

> Axis: a model can DECLARE where something should route (e.g. "focus surface X") — that
> declaration is not automatically trusted just because the model said it. Grounded in a worked
> instance: `@agent-ui/a2ui`'s `produce.ts`.

## Integrity-check the declaration; drop it, don't halt the turn

**Claim — an `ask` naming a surface no payload line actually creates, or colliding with a
session-known surface id, is DROPPED from the outgoing envelope (the prose reply stands, the turn
ships) — a wrong routing declaration never halts or retries a turn whose CONTENT is valid.**
Policy violations (out-of-scope component types on the ask surface) instead retry, via
produce-layer-only failure codes that never join the protocol's closed error union. ·
`produce.ts:25-36,704-773` (ADR-0097) · 2026-08-17 · [verified]

**Why this matters:** conflating "the model's routing metadata was wrong" with "the model's
content was wrong" would retry (or fail) a turn that didn't actually need it — the content is
fine, only the ask about where to point the user's attention was stale or mistaken. Degrading the
routing declaration alone, silently, is the narrower and more correct fix.

## What this file does NOT cover

The reserved-envelope discriminator this `ask` field rides inside of:
`envelope-framing-and-out-of-band-signals.md`. The DIFFERENT, later-observed UX-closing pattern of
client-side auto-attach on an exact label match: `client-side-label-auto-attach.md`. The
trust-boundary precedent this pattern generalizes — a server's own validated selection beating a
client-supplied field — already covered in [[llm-gateway-facts]]'s `registry-and-trust-boundary.md`
(a v2-harvest dedup: this pack does not restate that file's `resolvePair` story).
