# The provider-adapter seam — one interface, every vendor implements it

> Axis: how to let application code call "an LLM" without naming a vendor, so adding or swapping
> a provider never touches the caller. Grounded in the general adapter/strategy pattern (a
> platform-agnostic design technique) + a worked instance:
> `packages/agent-ui/a2ui/tools/agent/agent-transport.ts` and `providers/anthropic.ts` in
> `@agent-ui/a2ui`.

## The seam shape

**Pattern — one narrow interface, implemented once per vendor, depended on everywhere else:**

```ts
interface LlmProvider {
  stream(req: { model: string; system: string; messages: Turn[]; signal?: AbortSignal }): AsyncIterable<string>
}
```

The calling code (a turn loop, a chat handler) depends ONLY on this signature and never imports a
vendor SDK or branches on a provider name. Each vendor gets its own isolated module that owns its
own endpoint, its own auth header shape, and its own wire-format-to-plain-text framing — the
caller never sees any of that. **Worked instance:** `agent-transport.ts:81-88` declares this exact
shape (`AgentProvider.stream`); `providers/anthropic.ts:124-192` is the one module implementing
it for Anthropic; the driver (`produce.ts`) depends only on the interface and never imports
`providers/anthropic.ts` directly — the concrete adapter is INJECTED, not imported by the caller.

## Secrets are injected via the factory, never read at module scope

**Claim — the adapter is constructed by a FACTORY function that takes the secret as a parameter**,
never reads `process.env`/`import.meta.env` at the top of its own module:

```ts
function anthropicProvider(opts: { apiKey: string; endpoint?: string }): LlmProvider { … }
```

**Why this matters (the failure mode it prevents):** a module-scope env read means the adapter's
OWN import graph decides where the key comes from — untestable without real env vars, and a
silent trap if the same module is ever imported into a context that shouldn't have the key (a
test file, a client bundle during a refactor). Factory injection makes the caller responsible for
sourcing the secret, which is exactly where the trust-boundary decision belongs (see
registry-and-trust-boundary). **Worked instance:** `anthropic.ts:124` (`opts.apiKey`, not a
module-scope `process.env.ANTHROPIC_API_KEY`) — the SAME adapter factory shape serves a
server-side dev-proxy (the key sourced from `process.env`) and would serve any future
client-direct call path unchanged, because the factory doesn't care where its caller got the key.

## Each adapter owns its own wire-format framing — isolation, not a shared parser

**Claim — every vendor's adapter is the SINGLE boundary between that vendor's actual wire format
(an SSE stream, a different streaming protocol, a batch response) and the plain
`AsyncIterable<string>` fragment stream every other adapter also produces.** No shared "universal
SSE parser" sits between two DIFFERENT vendors' streams, because their event shapes are not
guaranteed to agree (see llm-jsonl-streaming's sse-chunk-parsing-technique for the GENERAL
buffering technique every adapter can reuse — reuse the TECHNIQUE, never share a PARSED SCHEMA
across vendors). **Failure mode this isolation prevents:** a "helpful" shared parser that
special-cases two vendors' event names inside one function becomes a coupling point — a new
vendor's slightly different event shape either breaks the shared parser's assumptions or forces
an ad-hoc branch inside it, and the caller has no way to know which vendor's assumptions it's
currently trusting.

## Choosing the interface's shape — what to include, what to leave out

**Recommendation, not a universal law:** keep the interface to exactly what the calling code
needs (model id, a system prompt, the turn history, an abort signal, a plain fragment stream out)
and resist adding vendor-shaped optional fields "just in case" (tool-use configs, vendor-specific
sampling params) — those belong INSIDE each adapter's own request-building, translated from
whatever generic shape the interface does carry, not threaded through the shared interface as
optional per-vendor extras that only one implementation ever reads. An interface that grows a
field only one adapter uses is the interface leaking a vendor's shape back into the caller — the
exact thing the seam exists to prevent.

## What this file does NOT cover

The registry that decides WHICH adapter+model a given request may use, and the trust-boundary
validation before a secret is even read (registry-and-trust-boundary) · the dev-proxy that
hosts the factory server-side (dev-proxy-and-bundler-footguns) · the wire-format parsing
TECHNIQUE an individual adapter uses internally ([[llm-jsonl-streaming]]) · the conversation/turn
model the caller threads through `messages` (stateless-session-and-turn-model).
