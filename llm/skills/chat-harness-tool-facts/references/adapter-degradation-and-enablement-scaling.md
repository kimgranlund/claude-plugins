# Degrade a dial you can't map; widen enablement's VOCABULARY, not its shape

> Axis: two distinct scaling problems a multi-provider tool seam runs into as it grows — a
> per-request tuning knob one adapter can't honor, and a per-tool enablement LIST that rots as a
> server's tool catalog churns. Grounded in a worked instance: `@agent-ui/a2ui`'s
> `agent-transport.ts` and ADR-0185.

## An unmappable dial degrades; it is never forwarded blindly

**Claim — the seam's contract is that an effort/reasoning knob an adapter can't map should be
IGNORED (a degraded DIAL) rather than sent upstream anyway (a degraded REQUEST).** The shipped
Anthropic adapter's unconditional `thinking` send is documented as latent debt precisely because
it violates this: a future non-thinking model would 400 instead of degrading cleanly. ·
`agent-transport.ts:138-144` (code-review finding, recorded at the seam) · 2026-08-17 · [verified]

**Why degrade rather than forward:** a caller that sets a dial has no way to know, per-provider,
whether that dial is honored — if an unmappable dial is forwarded and the provider rejects the
whole request over it, the caller's unrelated, valid request fails for a reason it never
controlled. Silently ignoring what can't be mapped keeps the request shape stable across
providers, which is the entire point of having one seam.

## Widen the wire's vocabulary, not its shape, when a fixed per-tool list rots

**Claim — pinned per-tool enablement ids rot across `tools/list` churn and can't express a
30-tool server under a wire cap; the fix is one grammar member `mcp:<server-id>:*` (anchored
whole-string against the server-id charset, so a real tool id ending in `:*` stays individually
enablable), expanded SERVER-side against the registry as it stands each turn, fail-closed (no
manifests registered ⇒ refs resolve to nothing, inert).** Persisting refs in per-agent stores is
the reversal cost that made this ADR-worthy — once a project stores raw per-tool ids per agent, a
server's tool-list churn breaks every stored agent silently. · ADR-0185 (amending four prior
pinned fences by version, append-only) · 2026-08-12 · [verified]

## What this file does NOT cover

Where the tool-execution loop itself runs relative to the provider adapter, and the caller-owned
tool registry's own failure-handling contract: `tool-registry-and-execution-loop.md`.
