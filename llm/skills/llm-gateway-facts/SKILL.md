---
name: llm-gateway-facts
description: >-
  The swappable multi-LLM-provider gateway pattern — project-agnostic. Use for multiple providers
  behind one interface, an API key off the client, a dev-time proxy for browser LLM calls, a key
  leaking into the bundle, one config as picker AND allowlist, a stateless conversation. Grounded
  in a shipped implementation (`@agent-ui/a2ui`). ANSWERS; does not build. NOT for the streamed
  wire format (llm-streaming-facts); NOT for A2UI-specific concerns (agent-protocols plugin).
disable-model-invocation: false
user-invocable: false
---

# llm-gateway-facts — the swappable-provider gateway pattern

Answers how to let an app call ANY of several LLM vendors behind one seam, safely — a client
never sees a key, a server-side proxy validates before it reads one, and the provider config is
a single source of truth for both the picker and the allowlist. This is a PATTERN pack: every
claim is grounded either in the underlying platform primitive (`fetch`, `ReadableStream`, a
bundler's own documented env-handling) or in a real shipped instance of the pattern
(`@agent-ui/a2ui`'s live-agent system, `packages/agent-ui/a2ui/tools/agent/` in that repo) —
cited as a worked example so a claim can be verified against running code, never as "the only way
to do this."

| Ask | Load |
|---|---|
| The adapter seam — "one interface per vendor", "swap providers with no driver change", "where do I inject the API key" | `references/provider-adapter-seam.md` |
| The registry + trust boundary — "one config for the picker AND the allowlist", "validate {provider,model} before reading a secret", "reject an unlisted pair safely" | `references/registry-and-trust-boundary.md` |
| The dev-proxy + bundler footguns — "keep the key out of the static build", "why did my key end up in the bundle", "the `.env` not landing in `process.env`" | `references/dev-proxy-and-bundler-footguns.md` |
| The conversation model — "keep the proxy stateless", "where does turn history live", "a pure reducer for the next turn" | `references/stateless-session-and-turn-model.md` |
| Provenance — worked-example source vs platform-primitive source | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`AgentProvider`, `resolvePair`, `envKey`, `VITE_`, `TurnInput`, …) and Read that section — the
   files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (a platform-primitive fact, a
   cited vendor-doc behavior, or the worked example's `file:line`) + the failure mode it
   prevents**. A pattern claim without the failure mode it exists to prevent is half an answer —
   these patterns all exist BECAUSE of a specific, real footgun, and the footgun is the point.
3. **Distinguish "this is how the platform/vendor behaves" (a fact, verify against current docs if
   stale-sensitive) from "this is how the worked example chose to implement it" (a design
   choice — a consumer's own project may reasonably choose differently, as long as the invariant
   the pattern protects still holds).**
4. Route output work at the boundary (see below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask is routed to the consumer's own build seat (this pack has none — it is project-agnostic).
**NOT done** while a claim ships without the failure mode it prevents, or a worked-example detail
is presented as a universal requirement rather than one valid implementation of the pattern.

## The core invariants (why these patterns exist)

- **A client-held secret is a compromised secret, eventually** — any code that ships to a browser
  is public, full stop; a bundler "inlining" an env var at build time does not create an
  exception. The dev-proxy + registry-validation pair exists entirely to keep secret custody
  server-side while still letting the client express a choice (which provider, which model).
- **A provider driver that names a vendor is not swappable** — the adapter seam's entire value is
  that the calling code (the turn loop, the chat UI) depends on ONE signature and never imports a
  vendor SDK; a "just add an `if (provider === 'openai')` branch in the caller" shortcut defeats
  this and should be named as a regression, not a quick fix.
- **One list, not two** — a provider registry that's hand-duplicated between a picker UI and a
  server allowlist WILL drift (the menu offers what the server rejects, or vice versa); a single
  committed config both read is the fix, not "keep them in sync manually."
- **The proxy is stateless because the client already holds the truth** — a server-side proxy
  that ALSO persists conversation history duplicates state the client owns, invites drift between
  the two copies, and turns a simple request/response boundary into a stateful service with its
  own lifecycle. The client sends its own history each turn; the server computes and forgets.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build or fix a provider adapter, a dev-proxy, or a turn/session model in YOUR project** → your
  project's own build seat/agent (this pack has none — it teaches the pattern, it does not own
  any codebase's source).
- **The concrete wire format a provider streams (SSE framing, JSONL structured output,
  validate-then-stream)** → [[llm-streaming-facts]] (the sibling pack in this plugin).
- **A2UI-specific concerns** (the wire protocol, catalog design, the training corpus, or
  `@agent-ui/a2ui`'s OWN shipped implementation as a repo-specific answer pack rather than a
  worked example) → the `agent-protocols` plugin's own packs, especially
  `a2ui-chat-agent-facts` (which documents that repo's actual system, dated and detailed,
  where this pack teaches the pattern generally).

## Extending this pack

A missing axis, a stale worked-example citation (the source repo's implementation moved), or a
second worked example from a different codebase proving the pattern generalizes — route to
`make-pack` (axis decomposition, grounded research waves, index discipline), where
installed; otherwise apply its discipline inline: one reference per distinct class of ask, every
claim grounded, never an uncited file bolted on.
