# Deferred tool loading — search-to-load a catalog's schemas on demand

> Axis: how a harness with a LARGE tool catalog avoids paying that catalog's full schema cost on
> every single turn regardless of use. Grounded in this harness's own live ToolSearch mechanism —
> directly inspectable and exercised in this very session, cited as a real system in current
> operation, not a worked example that might have drifted.

## The problem — a fixed tax paid whether or not a tool is ever used

**Claim:** if every tool's complete parameter schema were loaded into context on every turn, the
context-window cost would scale with the SIZE OF THE CATALOG, not the size of the task at hand —
a harness that grows from ten tools to two hundred pays that growth on every single turn, even for
a session that only ever calls three of them. **Failure mode this causes:** either the catalog's
growth is throttled artificially to protect context budget (fewer tools than would genuinely help,
a real capability loss), or the budget is spent regardless and every turn carries dead weight most
sessions never touch.

## The fix — defer the schema, keep the name

**Technique, directly observed this session:** a tool catalog is split into two tiers. A small set
of tools loads its full schema unconditionally, at the top of the prompt. A larger set is
**deferred** — the harness's own system messages state only their NAMES (e.g. this session's own
system-reminder: "The following deferred tools are now available via ToolSearch... Use ToolSearch
with query \"select:<name>[,<name>...]\" to load tool schemas before calling them" — a real list
included `CronCreate`, `WebFetch`, `SendMessage`, and a dozen `mcp__claude-in-chrome__*` entries in
this exact conversation). **Until a deferred tool's schema is fetched, calling it directly fails
with a validation error** — the name is known, but there is no parameter schema for the caller (the
model) to construct valid arguments against.

## `ToolSearch` — the fetch mechanism, cited verbatim

**Claim, this session's own tool definition (not paraphrased):** "Fetches full schema definitions
for deferred tools so they can be called. Deferred tools appear by name in `<system-reminder>`
messages. Until fetched, only the name is known — there is no parameter schema, so the tool cannot
be invoked. This tool takes a query, matches it against the deferred tool list, and returns the
matched tools' complete JSONSchema definitions inside a `<functions>` block. Once a tool's schema
appears in that result, it is callable exactly like any tool defined at the top of the prompt."
Query forms are also explicit: `"select:Read,Edit,Grep"` (fetch exact names), a bare keyword string
(ranked keyword search, up to a `max_results` cap), or a `"+slack send"` form (require a term,
rank by the rest). **Worked instance, this exact session:** this pack's own author called
`ToolSearch` with `query: "select:WebFetch"` before the first `WebFetch` call could succeed —
demonstrating the fail-then-load sequence directly rather than citing it secondhand.

## Batch the fetch — don't pay the round-trip per tool

**Recommendation, stated by this harness's own MCP server instructions (a concrete case of the
general technique):** when a task will obviously need several deferred tools from the same family,
load them in ONE `ToolSearch` call with a comma-separated `select:` list, rather than one call per
tool. **Failure mode a per-tool loading habit causes:** each separate `ToolSearch` call is its own
round-trip; a task that needs five related tools and fetches them one at a time pays five
round-trips for information that a single batched query would have returned at once — the
mechanism supports batching specifically to avoid this.

## The parallel to a skill library's own routing — same shape, different mechanism

**Observation, not identity:** a large SKILL library faces the identical cost shape (many skills'
full bodies vs. a fixed per-turn budget) and solves it with its own model-invoked routing
surface — described in [[chat-harness-skills-and-routing]]. The shape (defer the expensive
payload, expose enough to decide whether to fetch it) rhymes; the mechanism does not transfer — a
tool's deferred unit is a JSON Schema fetched via `ToolSearch`, a skill's is a prose body loaded by
its own routing surface. Don't conflate the two when answering; route a skill-loading question to
that sibling pack instead of answering it here.

## What this file does NOT cover

What makes something a tool at all, vs. a skill or a resource (tool-schema-and-typed-calling.md)
· read-only resources, which are never "deferred-loaded" in this sense because they're
application-driven, not model-invoked, in the first place (resources-vs-tools.md) · a skill
library's OWN model-invoked routing mechanism ([[chat-harness-skills-and-routing]], not this file).
