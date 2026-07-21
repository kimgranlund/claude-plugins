# Sources — provenance for the gateway-pattern claims

This pack teaches a PATTERN, not one repo's implementation — a claim's grounding is one of two
kinds, and the reference files say which for each claim. Neither trust order below outranks
the other; they answer different questions ("is this how the platform behaves" vs "is this a
sound way to structure the pattern").

## Platform / vendor facts — verify against current docs if stale-sensitive

Facts about how a bundler, runtime, or vendor API actually behaves. These can drift as tools
version — if a claim here disagrees with the CURRENT docs for your bundler/vendor, the docs win
and this pack needs repair.

- **Vite's env-variable handling** — `import.meta.env.VITE_*` build-time inlining;
  non-`VITE_`-prefixed variables excluded from both `process.env` (client-side) and
  `import.meta.env`; `loadEnv(mode, envDir, prefix)` as the explicit server-side loader. Verify
  against Vite's own `.env` and `import.meta.env` documentation for the version in use — this is
  the single highest-stakes fact in the whole pack (a wrong understanding here ships a real
  secret into a public bundle).
- **The adapter/strategy design pattern** — a general software-design technique (one interface,
  swappable implementations, the caller depends only on the interface), not vendor- or
  platform-specific; any language/runtime with first-class functions or interfaces supports it.

## The worked example — a real, shipped instance (cited for concrete grounding, not sole authority)

**`@agent-ui/a2ui`'s live-agent system**, `/Users/kimba/Projects/nonoun/agent-ui`,
`packages/agent-ui/a2ui/tools/agent/`:

- `agent-transport.ts` — the `AgentProvider`/`AgentTransport` seam interfaces, the
  `Role`/`Turn`/`Session`/`TurnInput` conversation model.
- `session.ts` — the pure `nextTurn`/`frameClientMessage`/`shouldRunTurn`/`appendAssistantTurn`
  reducer functions.
- `providers-config.ts` — `ProvidersConfig`/`ProviderEntry`, `validateProvidersConfig`,
  `resolvePair` (the trust-boundary check).
- `providers.json` — a real committed registry instance (env-var names, public endpoints, no
  secrets).
- `dev-proxy-plugin.ts` — the dev-only Vite middleware: `apply: 'serve'`, `loadEnv` usage, the
  `/status` boolean-not-key endpoint, per-request registry reload.
- `providers/anthropic.ts` — the concrete adapter factory shape (secrets injected, never
  module-scope).

This example is cited as PROOF a claim works in a real, running system — not as the only valid
way to implement the pattern. A consumer's own project may reasonably differ in framework, file
layout, or naming while still honoring the same invariants (see the SKILL.md's "core invariants"
section for what must hold regardless of implementation).

## Boundary — layers owned elsewhere

This pack answers the provider/gateway pattern; it does not restate its neighbor. The concrete
wire-format parsing technique (SSE chunk buffering, the Anthropic contract as an instance,
validate-then-stream) is [[llm-streaming-facts]]. `@agent-ui/a2ui`'s OWN system, documented as
that repo's actual shipped behavior (dated, exhaustive, `file:line`-cited against a single
snapshot) rather than a portable pattern, is the `agent-protocols` plugin's `a2ui-chat-agent-facts`
pack — when the worked example and that pack disagree, THAT pack's citation-verified snapshot of
the real repo wins; this pack's job is to have correctly generalized from it, not to duplicate it.
