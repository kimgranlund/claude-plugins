# The typed tool contract — a tool is neither a skill nor a resource

> Axis: what makes something a "tool" specifically, as opposed to a skill (prose instructions the
> model reads and follows) or a resource (inert data attached to context). Grounded in the current
> Model Context Protocol tools specification (a platform fact) + this harness's own live tool
> definitions (directly inspectable, this session).

## The three-way distinction

**Claim — a skill, a tool, and a resource are three structurally different extension surfaces,
not three names for the same idea:**

- **A skill is PROSE** — a block of instructions the model reads and follows; invoking it changes
  what the model does next, but a skill has no typed input contract and returns nothing itself.
- **A tool is an ACTION with a TYPED CONTRACT** — a name, a human-readable description, and a
  schema (typically JSON Schema) describing its parameters; the model calls it with structured
  arguments and receives a return value it did not already have.
- **A resource is DATA, not an action** — inert content (a file, a document, a query result)
  attached to context with no return value to reason about and no side effect from attaching it.

**Why this matters (the failure mode it prevents):** treating a resource as if reading its
description were "calling" it (or a tool as if its description alone answered the question,
without actually invoking it) blurs who bears responsibility for correctness, side effects, and
cost — a skill's prose can be wrong, a tool's call can fail or mutate state, a resource's content
can be attached without either.

## The MCP tool contract, verbatim

**Platform fact (Model Context Protocol, `docs/concepts/tools`, current as fetched):** "The Model
Context Protocol (MCP) allows servers to expose tools that can be invoked by language models.
Tools enable models to interact with external systems, such as querying databases, calling APIs,
or performing computations. Each tool is uniquely identified by a name and includes metadata
describing its schema." A tool definition carries: `name` (unique identifier), an optional
`title`, `description` (human-readable functionality), `inputSchema` (a JSON Schema defining
expected parameters), an optional `outputSchema`, and optional `annotations` describing behavior.
**Platform fact — the interaction model is explicit:** "Tools in MCP are designed to be
**model-controlled**, meaning that the language model can discover and invoke tools automatically
based on its contextual understanding and the user's prompts" — contrast this with resources,
which the spec calls **application-driven** (see resources-vs-tools.md).

## Worked instance — this harness's own tool definitions, this session

**Claim, directly inspectable in this very conversation:** every tool this harness exposes carries
exactly the MCP shape's spirit — a `name`, a `description` (prose explaining when/why to call it,
often with worked examples embedded), and a `parameters` object that is itself a full JSON Schema
document (`"$schema": "https://json-schema.org/draft/2020-12/schema"`), with `required` vs
optional properties, typed fields (`string`, `boolean`, `number`, `object`, `array`), and
`enum`-constrained values where the contract is closed (e.g. a `mode` or `subagent_type` field).
**Why this is the SAME idea as MCP's `inputSchema`, not a coincidence:** any system that lets a
model call a typed action converges on the same shape — a schema is what lets the CALLER (the
model) construct valid arguments and lets the RECEIVER (the tool's implementation) reject malformed
ones before doing anything, rather than trusting free-text and parsing it defensively.

## Why a schema, not free-text arguments

**Claim — a typed schema exists to make an invalid call FAIL BEFORE it does anything, not after:**
a `required` field missing, or a value outside an `enum`, is caught by argument validation at the
call boundary — the tool's own implementation never has to defensively re-parse or guess what a
free-text argument meant. **Failure mode this prevents:** a tool that accepted free-text arguments
(no schema) would need its own ad-hoc parsing and error-recovery for every malformed call, and a
subtly-wrong call (a typo'd field name, a string where a number was meant) would either silently
misbehave or fail deep inside the tool's logic instead of at the boundary where the mistake is
cheap to explain.

## What this file does NOT cover

Deferring a large catalog's schemas from loading until actually needed (deferred-tool-loading.md)
· read-only resources and how they differ from an invoked tool (resources-vs-tools.md) · wiring an
external network service behind the tool boundary ([[llm-gateway-facts]] for the LLM-provider
instance; external-service-integration-seam.md for the general shape).
