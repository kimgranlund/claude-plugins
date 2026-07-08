# The provider/model seam & the dev-proxy trust boundary

> Axis: how a real model call sits behind an injected `AgentProvider`, how `providers.json` is the
> single source of truth for both the switcher and the proxy allowlist, and how the dev-only Vite
> proxy holds the key server-side and validates the `{provider,model}` PAIR before ever reading it.
> Grounded in `packages/agent-ui/a2ui/tools/agent/agent-transport.ts`,
> `packages/agent-ui/a2ui/tools/agent/providers.json`,
> `packages/agent-ui/a2ui/tools/agent/providers-config.ts`,
> `packages/agent-ui/a2ui/tools/agent/dev-proxy-plugin.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R11/R12/N1/N2/N5). ADR-0073 = the
> model-provider seam + the trust boundary. Verified against source as of 2026-07-07.

## The provider seam (SPEC-R11 / ADR-0073)

```ts
interface AgentProvider {
  stream(req: { model: string; system: string; messages: Turn[]; signal?: AbortSignal }): AsyncIterable<string>
}
```

(`agent-transport.ts:81-88`.) **Claim — one isolated module PER provider** implements this; each
owns its endpoint, auth, and SSE-→-text framing (SPEC-N5). The `produce()` driver depends ONLY on
this signature and never names a vendor (`produce.ts:119`; see produce-loop). **Claim — the key is
passed IN via the factory, never read at module scope** (`agent-transport.ts:78-80`). **Claim —
Anthropic is implemented this wave with plain `fetch`, no LLM SDK** (SPEC-N1: no `@anthropic-ai/sdk`
anywhere); OpenAI/Gemini are config-present, adapter-pending. **Failure mode / caveat — defensive
dispatch:** an allowlisted-but-unimplemented provider must degrade exactly like the no-key path (a
distinguishable "provider not yet available" → backbone-only), never an unhandled crash
(`dev-proxy-plugin.ts:125-129`, SPEC-R11 AC4).

## The registry — `providers.json`, no secrets (SPEC-R11/R12)

The committed registry carries `defaultProvider` + a `providers` map; each entry has `label`,
`envKey`, `endpoint`, `defaultModel`, a `models[]` list, and an **`implemented: boolean`**
(`providers.json`). **Claim — the registry holds env-var NAMES + public endpoints/model-ids only,
no secret value** (`providers.json:6` is `"envKey": "ANTHROPIC_API_KEY"`, not a key). Today: `anthropic`
`implemented: true`; `openai`/`gemini` `implemented: false` (`providers.json:15,26,37`).
**Claim — the registry is the SINGLE source of truth for BOTH the switcher menu AND the proxy
allowlist** — no hand-listed second list (`providers-config.ts:9-13`; see
switcher-and-live-overlay).

`providers-config.ts` is a pure-core helper module (no I/O — the Node shell does the read, the
ADR-0062 pure-core/Node-shell split). `validateProvidersConfig` asserts the registry's own
invariants at load (every entry complete; each `defaultModel ∈` its own `models`; `defaultProvider`
exists AND is `implemented`) and throws on the first violation (`providers-config.ts:42-80`).

## The trust boundary — `resolvePair` is the ONE allowlist check (SPEC-R12 / ADR-0073 clause 5)

**Claim — `resolvePair(cfg, provider, model)` is the ONLY place a client-supplied
`{provider, model}` is validated before a key is read** (`providers-config.ts:96-108`). It returns
the matched entry + its env-var NAME only when the provider is registered, `implemented`, AND the
model is one of that provider's own `models`; otherwise a **discriminated** rejection reason —
`'unknown-provider' | 'unknown-model' | 'unimplemented'` (`providers-config.ts:82-108`). **Why
discriminated, not a bare boolean:** the proxy's degrade path and the switcher's disabled-state
both need to distinguish the cause. **Failure mode:** it never trusts an arbitrary client string
past this check — an out-of-allowlist pair is rejected before any `env[…]` read.

## The dev-only proxy — the key lives server-side (SPEC-R9/N2)

`a2uiDevProxyPlugin()` is a Vite middleware with **`apply: 'serve'`** — it attaches ONLY under
`vite dev`; `vite build` never runs it, so the static build carries no proxy and no key path
(`dev-proxy-plugin.ts:54-67`, SPEC-R3/N2). Per POST it: reads the body, runs `resolvePair`
(→ 400 on rejection, the client falls back to the backbone), reads `env[pair.envKey]`
(→ 503 `no-key` if unset), dispatches to the matched adapter (→ 503 on unimplemented), then runs
`produce(input, deps, { maxRounds: 3, model })` and streams each line `res.write(line + '\n')`
(`dev-proxy-plugin.ts:106-144`). **`GET /status` answers a boolean + a count, NEVER the key value**
(`dev-proxy-plugin.ts:98-104`).

**Claim — the allowlist-validated `model` is passed as the AUTHORITATIVE `opts.model`**
(`dev-proxy-plugin.ts:140`), which `produce()` prefers over any client `input.model`
(`produce.ts:113`) — so a crafted request body cannot escape the PAIR check (SPEC-R12; see
produce-loop). **Claim — the endpoint comes from the MATCHED registry row, not a client value**
(`dev-proxy-plugin.ts:123-125`).

## Two footguns that bite silently (SPEC-N2)

- **The `VITE_`-prefix inline footgun — the single highest-stakes fact in the design.** Vite
  INLINES `import.meta.env.VITE_*` at build time; any such reference bakes a real secret into the
  static build unless it lives only inside a dev-only-guarded, tree-shaken overlay module (SPEC-N2).
  The proxy sidesteps it entirely: it reads the **non-prefixed** `ANTHROPIC_API_KEY` server-side.
- **The `.env`-not-in-`process.env` false-negative.** Vite does NOT auto-load a bare `.env` into
  `process.env` (non-`VITE_` vars are kept out of both `process.env` and `import.meta.env`), so a
  bare `process.env[envKey]` read misses a `.env`-only key — the "no live API key found" degrade
  when a key IS set. Fix: the proxy loads env server-side via `loadEnv(mode, process.cwd(), '')`
  (prefix `''` ⇒ all vars) merged over `process.env` (`dev-proxy-plugin.ts:54-69`; SPEC-N2). Note
  `envDir` is the repo root (`process.cwd()`), not Vite's `root: 'site'`.

**Caveat — reload `providers.json` per request.** The proxy re-reads + re-validates the registry
per request (`dev-proxy-plugin.ts:85-96`) so an edit takes effect without a dev-server restart and
the allowlist stays in lockstep with the HMR-reloaded switcher — otherwise the menu offers a model
the proxy rejects with a 400 (the observed "Haiku-4.5" symptom).

## What this file does NOT cover

The seam the transport swaps on (agent-transport-seam) · the loop that consumes `deps.provider`
(produce-loop) · the switcher UI that renders from the same registry + the DEV-guarded overlay
wiring (switcher-and-live-overlay) · `ProviderSelection` on the turn model
(turn-session-and-input-intent) · retrieval internals of the judged shard the proxy loads
([[a2ui-training-corpus]]).
