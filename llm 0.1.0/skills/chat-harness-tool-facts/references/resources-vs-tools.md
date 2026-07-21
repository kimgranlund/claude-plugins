# Resources vs tools — read-only data vs an invoked action

> Axis: how a harness grants access to external files, documents, or structured data WITHOUT that
> access being an action the model takes. Grounded in the current Model Context Protocol resources
> specification (a platform fact, quoted from the spec as fetched).

## The core distinction — who decides, and what happens

**Platform fact (MCP, `docs/concepts/resources`, current as fetched):** "The Model Context
Protocol (MCP) provides a standardized way for servers to expose resources to clients. Resources
allow servers to share data that provides context to language models, such as files, database
schemas, or application-specific information. Each resource is uniquely identified by a
[URI]." **Platform fact — the interaction model is explicitly the INVERSE of a tool's:**
"Resources in MCP are designed to be **application-driven**, with host applications determining
how to incorporate context based on their needs" — contrast the tools spec's own language,
verbatim: "Tools in MCP are designed to be **model-controlled**, meaning that the language model
can discover and invoke tools automatically" (see tool-schema-and-typed-calling.md). **Why this
distinction is load-bearing, not cosmetic:** a tool call is a decision the MODEL makes, with a
return value it reasons about next; a resource entering context is a decision the HOST
APPLICATION makes (via a UI picker, a search/filter surface, or an automatic-inclusion heuristic)
— attaching a resource has no "return value" and is not something the model requests and receives
an answer from in the way a tool call is.

## The resource data shape

**Platform fact:** a resource definition carries a `uri` (its unique identifier, RFC 3986), a
`name`, an optional `title`, `description`, `mimeType`, and `size`. Its contents are either text
(`{"uri", "mimeType", "text"}`) or binary (`{"uri", "mimeType", "blob"}` — base64-encoded).
Resources also support optional **annotations** — `audience` (`"user"` and/or `"assistant"`),
`priority` (0.0–1.0, importance), and `lastModified` — that a client can use to filter, prioritize,
or display resources, without those annotations changing WHO decided to attach the resource in the
first place.

**Platform fact — resource TEMPLATES exist for parameterized access:** a server can expose a
`uriTemplate` (RFC 6570) rather than one fixed resource per file, so a whole class of resources
(e.g. every file under a project directory) is addressable without the server enumerating each one
individually. **Protocol fact:** discovery is `resources/list` (paginated), retrieval is
`resources/read` (returns the contents for a given `uri`) — two separate operations, so listing
what's available never implies having already read its content.

## Why a resource is not "a tool that happens to return data"

**Claim — the boundary is not about payload size or content type, it's about the control model:**
a tool that happens to fetch and return a file's contents IS still a tool (the model decided to
call it, mid-reasoning, based on the prompt) — a resource is something that was ALREADY placed
into context by the host, before or independent of the model asking for it. **Failure mode from
blurring this:** if "give the model read access to X" is implemented as a tool the model must
remember to call, but X was meant to be host-curated context always available when relevant (a
project's README, a schema file), the model may simply never think to call it — the access exists
but is never exercised. Conversely, if something that's genuinely an ACTION (fetching live,
possibly-changing data on demand, mid-task) is modeled as a static resource, the model has no way
to request a FRESH read at the moment it needs one — resources support an explicit
`resources/subscribe` + `notifications/resources/updated` pair for exactly this staleness concern,
but that is still host/server-driven change notification, not a model-initiated re-fetch the way a
tool call is.

## Security note — a resource still crosses a trust boundary

**Platform fact (the MCP spec's own security considerations for resources):** servers **MUST**
validate all resource URIs, access controls **SHOULD** be implemented for sensitive resources, and
resource permissions **SHOULD** be checked before operations — being read-only does not exempt a
resource from access control; "read-only" describes what the MODEL can do with it (nothing
mutates), not what the HOST must guarantee about who can attach it.

## What this file does NOT cover

What makes something a tool, and why a typed schema matters for THAT (tool-schema-and-typed-
calling.md) · deferring a large TOOL catalog's schemas (a model-controlled surface) until needed —
a distinct concern from resources, which are never "deferred" in that sense because the model
never decides to load them (deferred-tool-loading.md) · wiring an external network SERVICE behind
a trust boundary, as opposed to exposing already-available data as a resource
(external-service-integration-seam.md).
