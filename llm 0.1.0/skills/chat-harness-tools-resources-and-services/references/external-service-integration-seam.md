# External service integration — the general shape (routes to the worked instance)

> Axis: what ANY integration of an external network service into an agent harness wants,
> independent of which service. This file states the general principle only — the fully worked
> instance, for the specific and most common case (an LLM provider), is a sibling pack in this
> plugin; read that instead of expecting this file to re-derive it.

## The general principle

**Claim, in general terms — any external network service an agent harness calls wants three
things:** a **swappable interface** so the calling code never hardcodes a specific vendor or
endpoint (adding or replacing the service means writing one new adapter, not touching every call
site); a **place where secrets or credentials are validated and injected**, rather than read
ad hoc wherever the call happens to be made (so a credential's custody is one deliberate decision,
not scattered); and a **clear boundary about what is allowed to cross** from a less-trusted context
(a browser client, a user-supplied choice) to a more-trusted one (a server holding the actual
secret) — a client-supplied selection gets validated against an explicit allowlist BEFORE any
secret is read on its behalf, never after.

**Why these three, not an arbitrary list:** they map directly onto the three ways this class of
integration typically fails — a hardcoded vendor call makes swapping providers a rewrite instead
of an addition; a credential read at the point of use (rather than injected by a controlling
caller) makes it untestable and risks leaking into a context that shouldn't have it; and a missing
validate-before-trust step lets an unvetted client choice reach a secret-bearing code path.

## The fully worked instance — read it, don't wait for this file to repeat it

**Route, not a summary:** the exact, complete version of this pattern — for the specific and by
far most common case an agent harness integrates (an LLM provider) — is already fully authored as
[[llm-provider-gateway]] in this same plugin. That pack covers, in full and with a real worked
codebase cited (`file:line`): the provider-adapter seam (one interface, one factory per vendor,
secrets injected not read at module scope), the registry + trust-boundary validation
(`resolvePair`, the one-list rule, load-time invariant checks), the dev-proxy pattern (server-side
secret custody, the bundler env-inlining footgun and its fix), and the stateless
session/turn model that rides alongside a resolved provider selection. **Read those four reference
files rather than expecting this one to restate them** — duplicating that content here across two
skills in the same plugin would be exactly the kind of drift risk this plugin's own discipline
exists to prevent (a fix or an update to the pattern would have to land in two places instead of
one, and eventually wouldn't).

**When the service ISN'T an LLM provider:** the same three requirements above still apply — a
non-LLM external API (a search index, a payments processor, an internal microservice) wants the
identical shape (swappable seam, deliberate secret custody, validate-before-trust). Adapt
`llm-provider-gateway`'s pattern to the new domain rather than inventing a new one from scratch;
the invariants it documents (see its own SKILL.md's "core invariants" section) are general software
design principles illustrated through the LLM case, not LLM-specific facts.

## What this file does NOT cover

The adapter seam, the registry/trust-boundary validation, the dev-proxy pattern, or the
stateless session/turn model themselves — all fully owned by [[llm-provider-gateway]] · the wire
format a service's response streams over once a call is already underway ([[llm-jsonl-streaming]])
· what makes something a callable tool vs. a resource vs. a service call in the first place
(tool-schema-and-typed-calling.md · resources-vs-tools.md).
