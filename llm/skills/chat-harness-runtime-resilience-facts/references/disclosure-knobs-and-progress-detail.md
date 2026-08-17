# Disclosure knobs and progress detail in a deployed chat runtime

> Axis: how much of the runtime's own internal state a disclosure knob may reveal to a consumer —
> distinct from failure-surfacing.md's axis (how a runtime that already committed a response must
> still surface a FAILURE loudly and safely). Un-bundled 2026-08-17 from
> `disclosure-and-failure-surfacing-in-a-chat-runtime.md`, which the 2026-08-17 knowledge-harvest
> fold had deliberately bundled two concerns into (see this pack's own `sources.md` for the
> `plan-skill-split` provenance) — `pack-writing-rules` names literature-shaped bundling of two
> genuinely different question types directly as a failure this un-bundle now corrects. Grounded
> in a worked instance: `@agent-ui/a2ui`'s `produce.ts`.

## Every disclosure knob is fail-closed and independent — no accidental ladder

**Claim — progress detail defaults to stage transitions only (no reasoning text); `'full'`
(bounded reasoning excerpts, capped ~200 chars) and `'source'` (raw payload lines behind
validate/retry stages, capped 16 KB with an EXPLICIT truncation marker, never a silent cut) are
separate opt-ins where one never implies the other.** A consumer needing both is a deliberate
future member, not a ladder accident. · `produce.ts:139-207` (ADR-0146 F3, GH #240/ADR-0159) ·
2026-08-17 · [verified]

## What this file does NOT cover

The "browser cannot hold a secret" invariant — already covered by [[llm-gateway-facts]]'s
`dev-proxy-and-bundler-footguns.md` and `provider-adapter-seam.md` (a v2-harvest dedup: lesson 30
of the same source export is not restated here). How a runtime must surface a FAILURE once it has
already committed to a response (the terminal error line, the retry-bound halt, redacting raw
upstream text) — this pack's own `failure-surfacing-in-a-chat-runtime.md`, a related but distinct
question (how much to REVEAL vs. how to FAIL loudly).
