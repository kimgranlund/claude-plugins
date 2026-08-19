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

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`single-flight-401-refresh.md` and `retry-policy-and-streaming-passthrough.md` were added from
agent-ui#1115's "Scope-conformant revision v2" comment (posted 2026-08-17T17:14:57Z), the
litmus-filtered re-harvest of `@agent-ui/a2ui` lessons kept to web-based virtual-chat-harness
knowledge only (lessons 40-45 of that export — `packages/agent-ui/data/src/gateway/{auth,retry}.ts`,
a distinct source module from this pack's existing `tools/agent/` citations). No lesson routed to
this pack by that export overlapped this pack's PRE-EXISTING coverage — no dedup skip was needed
for lessons 40-45 themselves. This pack's OWN existing files, however, are cited AS the dedup
target for several other lessons the export routed elsewhere: lessons 6/7 (workflow), 18
(routing), 20 and 30 (tool and guardrail, both `[split]`) — see those packs' own `sources.md`
Provenance notes.

## Provenance — 2026-08-19 provider-doctrine fold (agent-ui field ops)

`live-ops-diagnostics-and-model-tiering.md` was added 2026-08-19, folding agent-ui's field-proven
gateway OPS doctrine: the per-model curl matrix (that project's 2026-07-16/17 live-agent triage,
recorded in its own debug-craft ledger), the 503-storm posture (its 2026-08-17 fleet-ops incident —
GraphQL-backed verbs dying while plain REST survived; writes verified landed before believed), and
planning-vs-execution model tiering (its standing seat config, owner-ruled 2026-06-29,
`.claude/agents/` frontmatter). The dev-proxy trust-boundary shape itself (registry with per-provider
`envKey`/`endpoint`, `{provider, model}` pair validation, no secret ever client-side, stateless proxy
with the client holding turn history) was diff-checked against agent-ui ADR-0073
(`0073-a2ui-live-model-provider-seam.md`, accepted 2026-07-04, read via the GitHub API 2026-08-19)
and found ALREADY fully covered by this pack's existing `registry-and-trust-boundary.md`,
`dev-proxy-and-bundler-footguns.md`, and `stateless-session-and-turn-model.md` — no restatement was
added; ADR-0073 stands as the ratified decision record BEHIND those files' worked instance.
