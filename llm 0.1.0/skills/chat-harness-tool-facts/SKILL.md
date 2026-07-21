---
name: chat-harness-tool-facts
description: >-
  How a chat-agent harness reaches outside its context window — typed tools, deferred
  tool-catalog loading, read-only resources, external services behind a swappable seam. Use for
  "tool vs skill vs resource", "design a typed tool schema", "defer a huge tool catalog so it
  doesn't tax every turn", "a tool call fails before it's loaded", "read-only access without an
  action", "MCP resources vs tools", "external API trust boundary". Covers typed tool contracts
  (JSON-Schema params, vs. a skill's prose or resource's inert data), search-to-load catalogs,
  read-only resources (MCP's application-driven capability), and external-service shape —
  LLM-provider specifics route to llm-gateway-facts. Grounded in this harness's live
  ToolSearch mechanics + the MCP spec. Answers from a cited corpus, no build. NOT the
  LLM-provider pattern (llm-gateway-facts); NOT skill routing/memory
  (chat-harness-routing-facts / chat-harness-memory-facts); NOT a wire format
  (llm-streaming-facts); NOT implementing any of this.
disable-model-invocation: false
user-invocable: false
---

# chat-harness-tool-facts — reaching outside the context window

Answers how a chat-agent harness extends what a model can DO and KNOW beyond the text already in
its context: a **tool** (a callable action with a typed contract), a **resource** (read-only data
attached without an action), and an **external service** (a network dependency behind a seam) are
three distinct extension surfaces, easy to blur but structurally different in who controls them
and what they cost. This pack is grounded in two kinds of source: this very harness's own live
tool-calling and deferred-tool mechanics (directly inspectable in this session, cited as a real
system not a worked example that might drift) and the current Model Context Protocol
specification (a platform fact, verify against current docs if this pack has aged).

| Ask | Load |
|---|---|
| Tool vs skill vs resource — "what's the actual difference", "design a typed schema for this action" | `references/tool-schema-and-typed-calling.md` |
| Deferred/search-to-load tool catalogs — "why did calling this tool fail before I searched for it", "amortize a big catalog's schema cost" | `references/deferred-tool-loading.md` |
| Read-only resources — "attach a file/doc as context, not an action", "MCP resources capability" | `references/resources-vs-tools.md` |
| External service integration — "wire in a network dependency behind a seam" (routes to the LLM-specific worked pack) | `references/external-service-integration-seam.md` |
| Provenance — this-session platform fact vs MCP spec fact vs routed sibling | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`inputSchema`, `ToolSearch`, `resources/read`, `model-controlled`, `application-driven`, …) and
   Read that section — the files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (this session's own directly
   observed mechanics, or the MCP spec's `file`/section, or a routed sibling's citation) + the
   failure mode it prevents**. A claim about "why deferred loading exists" or "why a resource
   isn't a tool" without the failure mode it prevents is half an answer.
3. **Distinguish "this is how the Model Context Protocol defines it" (a spec fact, verify against
   current MCP docs) from "this is how this particular harness implements the idea" (this
   session's own ToolSearch mechanism is one implementation of the deferred-loading idea, not the
   only possible one).**
4. For a18 (external services) specifically: state the general principle in one or two sentences,
   then **route** — do not re-derive the adapter-seam/registry/dev-proxy pattern that
   `llm-gateway-facts` already owns in full.
5. Route output work at the boundary (see below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask is routed to the consumer's own build seat. **NOT done** while a claim ships without the
failure mode it prevents, or this pack's external-service file re-explains what
`llm-gateway-facts` already teaches instead of routing to it.

## The core invariants (why these distinctions exist)

- **A tool, a skill, and a resource differ in WHO invokes them and WHAT they cost, not just in
  what folder they live in.** A skill is prose the model reads and follows; a tool is an action
  with a typed contract the model calls and gets a return value from; a resource is data attached
  to context with no action taken and no return value to reason about. Collapsing this distinction
  (e.g. treating a resource as if calling it were an action, or a tool as if reading its
  description were sufficient without calling it) misleads whoever is reasoning about cost, side
  effects, or trust.
- **Loading every tool's full schema on every turn is a fixed tax paid whether or not the tool is
  ever used.** A large catalog wants its full parameter schemas loaded ONLY for the tools a given
  session actually needs — the alternative is a permanent, unavoidable context-window cost that
  scales with the SIZE of the catalog, not the size of the task.
- **A resource is application-driven; a tool is model-controlled.** Who decides a resource enters
  context (the host application, by policy or user action) is a DIFFERENT actor than who decides a
  tool gets called (the model, reasoning from the user's prompt) — a design that lets the model
  freely "invoke" something meant to be host-controlled erodes the boundary the distinction exists
  to protect (see resources-vs-tools.md for the exact MCP language).
- **An external network service is a trust boundary, not just an implementation detail.** Any
  integration that reaches outside the harness's own process wants a swappable seam (so the caller
  never hardcodes one vendor) AND an explicit boundary about what crosses from a less-trusted
  context to a more-trusted one (a secret, a credential) — the fully worked version of this, for
  the specific case of an LLM provider, already exists; this pack routes to it rather than
  restating it.

## Boundaries — this pack ANSWERS; it routes ALL making

- **The swappable LLM-provider adapter, its registry/trust-boundary validation, its dev-proxy, or
  its stateless turn model** → [[llm-gateway-facts]] — the fully worked instance of a18's
  general principle, for the specific and most common external-service case. This pack's own
  `external-service-integration-seam.md` states the general shape and ROUTES here; it does not
  duplicate the adapter seam, the registry, or the dev-proxy pattern.
- **A skill's own model-invoked routing/discovery** (how a large skill LIBRARY, as opposed to a
  tool catalog, decides what loads into context) → [[chat-harness-routing-facts]] — a
  distinct axis (skills = instructions, this pack's a16 = tools/actions) that happens to share the
  "defer loading until needed" SHAPE without sharing the mechanism.
- **Persisting facts, preferences, or state across turns/sessions** (memory) →
  [[chat-harness-memory-facts]] — memory is neither a callable tool, a static resource,
  nor a network service; it is its own extension surface.
- **The wire format a tool's or resource's result is streamed over** (SSE framing,
  validate-then-stream) → [[llm-streaming-facts]] (the sibling pack in this plugin) — a transport
  concern orthogonal to whether the thing being streamed is a tool result or anything else.
- **Implement a tool, a resource server, or a service integration in YOUR project** → your
  project's own build seat/agent (this pack has none — it teaches the distinctions, it does not
  own any codebase's source).

## Extending this pack

A missing axis, a stale citation (this session's ToolSearch mechanics or the MCP spec moved), or a
second worked example proving one of these patterns generalizes beyond this harness — route to
`pack-forge` (axis decomposition, grounded research waves, index discipline), where installed;
otherwise apply its discipline inline: one reference per distinct class of ask, every claim
grounded, never an uncited file bolted on.
