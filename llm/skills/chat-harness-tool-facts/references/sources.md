# Sources — provenance for the tools/resources/services claims

This pack teaches distinctions and a general pattern, not one repo's implementation — each claim
is grounded in one of three kinds, and the reference files say which for each claim.

## This harness's own live mechanics — directly inspectable, this session, not a citation to a
## separate document

The tool-calling contract shape (name + description + JSON-Schema `parameters`, `required` fields,
`enum`-constrained values) and the deferred-tool mechanism (`ToolSearch`, its exact tool
description, the `<system-reminder>` listing deferred tool names, the `"select:"` /
keyword-search / `"+term"` query forms) are facts about the very system this pack's author was
running inside while authoring it — verified by direct observation in the authoring session
(a real `ToolSearch` call, e.g. `query: "select:WebFetch"`, was made and its result observed
before this pack's `deferred-tool-loading.md` was written), not read off a separate spec document.
**Caveat, stated plainly:** this class of fact is specific to Claude Code's own harness
implementation and can change between versions; if a claim here disagrees with what a CURRENT
session actually shows (a different deferred-tool system-reminder shape, a different `ToolSearch`
query syntax), the live session wins and this pack needs repair.

## Model Context Protocol specification — a platform fact, verify against current docs if
## stale-sensitive

- **`docs/concepts/tools`** (fetched and quoted directly) — the tool data shape (`name`, `title`,
  `description`, `inputSchema`, `outputSchema`, `annotations`), the `tools/list`/`tools/call`
  protocol messages, and the explicit **model-controlled** interaction-model statement.
- **`docs/concepts/resources`** (fetched and quoted directly) — the resource data shape (`uri`,
  `name`, `mimeType`, text/binary contents, annotations), resource templates (RFC 6570), the
  `resources/list`/`resources/read`/`resources/subscribe` protocol messages, and the explicit
  **application-driven** interaction-model statement (the deliberate inverse of tools').
- MCP is an open, versioned specification (modelcontextprotocol.io) independent of any single
  vendor's harness; verify a claim here against the CURRENT spec if this pack has aged, the same
  discipline `llm-gateway-facts` applies to its own Vite-specific platform facts.

## Routed siblings — cited, never duplicated

- **[[llm-gateway-facts]]** (this plugin) — the fully worked instance of a18 (external-service
  integration) for the LLM-provider case: the adapter seam, the registry + trust boundary, the
  dev-proxy pattern, the stateless turn model. This pack's `external-service-integration-seam.md`
  states the general principle in two paragraphs and routes there; it does not restate the pattern.
- **[[chat-harness-routing-facts]]** — a skill library's own model-invoked routing/discovery
  mechanism, the SKILL-loading analogue of this pack's `deferred-tool-loading.md` (same cost
  shape, a different mechanism — a prose body loaded by its own routing surface, not a JSON Schema
  fetched via `ToolSearch`).
- **[[chat-harness-memory-facts]]** — persisting facts/preferences/state across turns or
  sessions; a distinct extension surface from a tool, a resource, or a service call and not
  covered by this pack at all.
- **[[llm-streaming-facts]]** (this plugin) — the wire format a tool's or service's result streams
  over once a call is already in flight; orthogonal to whether the thing streamed is a tool result,
  a resource fetch, or anything else.

## Boundary — layers owned elsewhere

This pack answers the tool/resource/service EXTENSION-SURFACE distinctions and the deferred-
loading technique; it does not restate the LLM-provider gateway pattern (route to
[[llm-gateway-facts]]), a skill library's own routing (route to
[[chat-harness-routing-facts]]), or cross-turn memory (route to
[[chat-harness-memory-facts]]) — when this pack and a routed sibling could both plausibly
answer, the sibling that OWNS the concrete mechanism wins, and this pack's job is to have routed
correctly, not to have half-answered first.

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`tool-registry-and-execution-loop.md` and `adapter-degradation-and-enablement-scaling.md` were
added from agent-ui#1115's "Scope-conformant revision v2" comment (posted
2026-08-17T17:14:57Z), the litmus-filtered re-harvest of `@agent-ui/a2ui` lessons kept to
web-based virtual-chat-harness knowledge only. Lesson 20 of that same v2 export ("one provider
seam, plain fetch, no vendor SDK") was evaluated and SKIPPED here as hard dedup — already
substantively covered by [[llm-gateway-facts]]'s `provider-adapter-seam.md`; it is not restated in
this pack even though v2's own section header filed it under this pack's axis (v2 itself marks
lesson 20 `[split]` — its CLI-tier grep-gate half is out of scope entirely, routed to the
teamwork/harness re-route ticket #543).
