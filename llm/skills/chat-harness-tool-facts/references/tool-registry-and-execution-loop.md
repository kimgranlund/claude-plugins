# A caller-owned tool registry, and where the tool-execution loop actually runs

> Axis: once a chat harness exposes tools to a model, who owns the tool DEFINITIONS and where the
> multi-round tool-call/tool-result loop physically executes relative to the provider adapter.
> Grounded in a worked instance: `@agent-ui/a2ui`'s `packages/agent-ui/a2ui/tools/agent/
> agent-transport.ts`.

## The model never invents a tool; a failed tool degrades the answer, never the turn

**Claim — `ToolDef`s are sourced from a caller-owned registry, never invented by the model;
`executeTool` rejections surface to the model as error-text results (not a thrown exception that
kills the turn); the turn's abort signal threads into in-flight tool work so an aborted turn
cancels its tools too.** · `agent-transport.ts:107-163` (GH #49) · 2026-08-17 · [verified]

**Why this matters:** a tool failure is routine (a network call times out, a downstream service
4xxs) — treating it as a turn-ending exception means one flaky tool call can take down an
otherwise-healthy conversation; feeding the failure back as a normal tool result lets the model
reason about it and try something else, the way it would reason about any other tool output.

## Run the provider-native tool loop INSIDE the adapter, never above it

**Claim — the adapter executes tool calls, feeds results back to the provider, and yields ONLY
text fragments throughout, bounded by its own round cap — the orchestration loop above the
adapter stays provider-agnostic and never sees a tool-call event directly.** Lifecycle events
(progress, tool-call-started, …) ride an optional side CALLBACK rather than a union-yielding
stream, specifically because there is exactly one caller and the text-fragment contract must
never change shape underneath it. · `agent-transport.ts:146-163` (ADR-0146 F1) · 2026-08-17 ·
[verified]

**Why keep the loop inside the adapter:** each provider's native tool-calling protocol (how a
tool call and its result are represented on THAT vendor's wire) differs; running the round-trip
loop inside the adapter means the driver above it depends on one interface
(text fragments in, text fragments out) regardless of which vendor's tool-calling shape is
underneath — the exact isolation the provider-adapter seam already provides for streaming text,
extended to tool rounds. See [[llm-gateway-facts]]'s `provider-adapter-seam.md` for that seam's
own general shape (a v2-harvest dedup: lesson 20 of the same source export, "one provider seam, no
vendor SDK," is already covered there and is not restated here).

## What this file does NOT cover

An individual adapter's own inability to map a specific dial (effort/reasoning knob) onto its
provider's request shape: `adapter-degradation-and-enablement-scaling.md`. The typed
JSON-Schema contract that makes something a "tool" at all, as opposed to a skill or a resource:
`tool-schema-and-typed-calling.md`.
