# The registry + trust boundary — one config, validated before any secret is touched

> Axis: how a single committed config becomes BOTH a provider/model picker's menu AND a server's
> allowlist, and how a client-supplied `{provider, model}` pair gets validated before the server
> ever reads a secret. Grounded in a worked instance:
> `packages/agent-ui/a2ui/tools/agent/{providers.json,providers-config.ts}` in `@agent-ui/a2ui`.

## The registry shape — no secrets, ever

**Claim — the committed config carries env-var NAMES and public endpoints/model-ids, never a
secret VALUE.** A registry entry: `label` (display name), `envKey` (the name of the environment
variable holding the real key — a string like `"ANTHROPIC_API_KEY"`, not the key itself),
`endpoint` (the public API URL), `defaultModel`, `models[]`, and an `implemented: boolean` for
staged rollout (register a provider before its adapter is built; the menu can show it as coming
soon, the proxy degrades cleanly rather than crashing). **Worked instance:**
`providers-config.ts:17-34` (the `ProviderModel`/`ProviderEntry`/`ProvidersConfig` shapes);
`providers.json`'s own committed entries carry exactly this — an `envKey` field, never a key
value. **Why `implemented` matters as its own field, not just "present in the config or not":**
it lets the SAME config register a provider's picker-menu identity (so it's visible, so a user
knows it's coming) independently of whether its adapter exists yet — a provider can be `registered
but not implemented`, which is a different, safer failure mode than "not in the config at all"
(an unknown-provider path) or "silently crashes when selected" (no degrade path).

## Load-time invariant validation — fail loud, once, at startup

**Claim — the registry's OWN internal consistency is asserted once at load, not re-checked on
every lookup:** every entry has a non-empty `label`/`envKey`/`endpoint`/`defaultModel` and a
non-empty `models[]`; each entry's `defaultModel` is actually one of its own `models`; the
config's top-level `defaultProvider` names a real, `implemented` entry. Any violation throws
immediately with a specific message naming which invariant broke and which entry. **Worked
instance:** `providers-config.ts:42-80` (`validateProvidersConfig`) — throws on the FIRST
violation found, e.g. `providers.json: provider "gemini" has no models`. **Why fail loud at load
rather than defensively at each read:** a malformed registry is a deploy-time authoring mistake,
not a runtime condition to route around — every call site downstream can then assume the registry
is well-formed and skip re-validating it.

## `resolvePair` — the one place a client-supplied choice is checked

**Claim — a single function is the ONLY place a `{provider, model}` pair coming from outside the
server is validated, and it returns a DISCRIMINATED result, never a bare boolean:**

```ts
type ResolvePairResult =
  | { ok: true; entry: ProviderEntry; envKey: string }
  | { ok: false; reason: 'unknown-provider' | 'unknown-model' | 'unimplemented' }
```

It succeeds only when the provider is registered, `implemented`, AND the model is one of THAT
provider's own `models` — never a bare "does this provider exist" check that lets an arbitrary
model string through. **Worked instance:** `providers-config.ts:96-108`. **Why a discriminated
reason, not a bare boolean, matters:** a caller on the server side (the proxy) and a caller on the
client side (a picker UI greying out an option) both need to distinguish WHY a pair was rejected —
"this provider doesn't exist" is a different UI/log message than "this provider isn't wired up
yet," which is different again from "that's not one of this provider's models." A boolean throws
that distinction away at exactly the point two different consumers need it.

## The one-list rule — why a second hand-maintained list always drifts

**Claim — the SAME committed registry is read by BOTH the picker UI (to build its menu) and the
server-side gate (`resolvePair`) — there is no second, independently maintained list of "which
providers/models are allowed."** **Failure mode this prevents:** any manually-synced pair of
lists (one for the menu, one for the allowlist) drifts the moment either is edited alone — the
menu offers a model the server then 400s on, or the server accepts a pair the menu never exposed
(worse: a dead code path nobody notices is unreachable from the UI). **Design implication:** if a
project's picker and server-gate genuinely can't share the identical file (e.g. they're
build-time-separated), they must at minimum derive from ONE upstream source at build/generation
time — never two independently hand-edited copies.

## Reload discipline — a registry that's editable without a restart

**Claim (a design choice, not a universal law — state the trade-off if you deviate):** a
dev-time server can re-read + re-validate the registry PER REQUEST (cheap for a small config
file) so an edit (a new model row) takes effect without a restart, keeping an HMR-reloaded
picker's menu in lockstep with the server allowlist. **Failure mode if the two reload on
different cadences:** the picker offers a freshly-added model the server-side gate still rejects
(stale in-memory config) until the server restarts — a confusing, hard-to-diagnose 400 that looks
like a bug in the NEW model's config when it's actually a reload-timing mismatch.

## What this file does NOT cover

The adapter interface a resolved `{entry, envKey}` pair is ultimately used to construct
(provider-adapter-seam) · where the actual secret value is read from and how a static build
avoids ever bundling it (dev-proxy-and-bundler-footguns) · the conversation/turn model
threaded alongside a resolved provider selection (stateless-session-and-turn-model).
