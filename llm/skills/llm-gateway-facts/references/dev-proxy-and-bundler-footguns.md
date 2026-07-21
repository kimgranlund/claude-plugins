# The dev-proxy pattern + the bundler env-inlining footgun

> Axis: how to let a browser app call an LLM without ever shipping a real API key to the browser,
> and the specific bundler behavior that silently defeats a naive attempt at this. Grounded in
> Vite's own documented env-variable handling (a platform fact, verifiable against current Vite
> docs) + a worked instance: `packages/agent-ui/a2ui/tools/agent/dev-proxy-plugin.ts` in
> `@agent-ui/a2ui`.

## The footgun — a bundler that inlines env vars at BUILD time

**Platform fact (verify against your bundler's current docs — this exact prefix convention is
Vite's, but the CLASS of footgun is common to build-time env-inlining bundlers generally):** Vite
replaces `import.meta.env.VITE_*` references with their literal values AT BUILD TIME, into the
static output — not read at runtime. **Failure mode this causes:** any code path that references
`import.meta.env.VITE_ANTHROPIC_API_KEY` (or an equivalent build-time-inlined variable in another
bundler's convention) bakes the ACTUAL SECRET VALUE into the shipped JS bundle the moment that
code is reachable from the build's entry point — even if the code "only runs in dev" by intent,
if it's not ALSO excluded from the production build graph (tree-shaken or behind a genuinely
dev-only guarded module), the secret ships. This is not a runtime leak to guard against; it is a
build-time bake-in that happens whether or not the vulnerable code path ever executes.

**The only reliable fix:** never let a real secret reach a `VITE_`-prefixed (or your bundler's
equivalent build-time-inlined) variable name at all. Read the secret through a NON-prefixed name,
server-side only, in code that is provably excluded from the client build graph (see the dev-only
proxy below).

## The dev-only proxy — server-side key custody

**Pattern — a middleware/server plugin that ONLY attaches to the dev server, never to the
production build**, holding the key server-side and forwarding only the (already validated, see
registry-and-trust-boundary) request:

1. Attaches with a build-tool hook that fires ONLY under the dev server, never under a production
   build (Vite: `apply: 'serve'` on the plugin object) — this is the mechanism that keeps the
   proxy, and therefore the key-reading code path, entirely out of the static build's module
   graph. **Worked instance:** `dev-proxy-plugin.ts:70,83` (`apply: 'serve'`).
2. Reads the secret from a NON-prefixed environment variable name (e.g. `ANTHROPIC_API_KEY`, not
   `VITE_ANTHROPIC_API_KEY`) — server-side Node code, never inlined by the bundler because it was
   never referenced via the bundler's own env-access convention.
3. Responds to a status/health check with a BOOLEAN (key present or not) and never the value
   itself. **Worked instance:** `dev-proxy-plugin.ts:7` ("`/status` answers a boolean + count; a
   key value is NEVER sent to the browser").
4. Validates the client-supplied `{provider, model}` against the registry (see
   registry-and-trust-boundary) BEFORE reading any env var for that provider — an unlisted or
   unimplemented pair never triggers a secret read at all.

## The `.env`-not-in-`process.env` trap (Vite-specific, but check your own tool's equivalent)

**Platform fact:** Vite does NOT automatically load a bare `.env` file's non-prefixed variables
into `process.env` — only `VITE_`-prefixed variables reach `import.meta.env` on the client, and
Node's own `process.env` is populated only by however the PROCESS itself was started (shell
exports, a process manager), not by Vite reading `.env` on your behalf. **Failure mode:** a naive
`process.env[envKey]` read inside dev-server code silently returns `undefined` even when the key
IS correctly set in a `.env` file — producing a confusing "no API key found" degrade that looks
like a missing/wrong key when the key is actually present, just not loaded into the process the
naive way. **The fix:** load the env file explicitly, server-side, using the bundler's own
provided loader (Vite: `loadEnv(mode, envDir, prefix='')` — an empty prefix means "load every
variable, not just the `VITE_`-prefixed ones"), merged over `process.env` so a real shell export
still wins. **Worked instance:** `dev-proxy-plugin.ts:71-79,85` — note also that `envDir` must be
pointed at wherever the `.env` actually lives (the repo root), not wherever the bundler's own
`root` config option points, if those differ.

## The degrade path — an unimplemented or missing-key provider must not crash

**Recommendation:** a provider that's registered (see registry-and-trust-boundary) but has no
adapter built yet, or has no key set in the environment, should degrade to a distinguishable,
handled response (a clear "not available" status, a fallback to a default/backbone path) — never
an unhandled exception that surfaces a raw stack trace to the client. The registry's
`implemented: boolean` and the `resolvePair` discriminated-reason result (both in
registry-and-trust-boundary) exist specifically so this degrade can be precise about WHY a
request didn't proceed, rather than a generic 500.

## What this file does NOT cover

The registry/allowlist validation that runs BEFORE any env read happens
(registry-and-trust-boundary) · the adapter interface the resolved credentials ultimately
construct (provider-adapter-seam) · the wire-format parsing an adapter does once it actually
has a validated key and starts streaming ([[llm-streaming-facts]]).
