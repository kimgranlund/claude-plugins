# The Anthropic SSE wire contract — the exact event sequence the adapter parses

> Axis: what Anthropic's `/v1/messages` streaming response actually looks like on the wire, and how
> `parseAnthropicSSE` turns it into plain text fragments — a distinct class of ask from "how do I
> wire a new provider" (provider-model-seam-and-trust-boundary) or "how does the loop consume a
> fragment stream" (produce-loop): this is what breaks, and why, when Anthropic's OWN response
> shape is the suspect. Grounded in
> `packages/agent-ui/a2ui/tools/agent/providers/anthropic.ts`,
> `packages/agent-ui/a2ui/src/live-agent/anthropic-sse.test.ts` (the fixture suite — SPEC-R11 AC3).
> Verified against source as of 2026-07-13.

## The request shape (host-verified, SPEC §6, 2026-07-04)

**Claim — `POST /v1/messages`**, headers `x-api-key: <key>` + `anthropic-version: 2023-06-01` +
`content-type: application/json`, body `{ model, system, messages, stream: true, max_tokens }`
(`anthropic.ts:129-144`). **Claim — `system` is a top-level request param, never a message** —
`toAnthropicMessages` maps only the `user`/`assistant` turns; the caller's `system` string is passed
separately in the fetch body (`anthropic.ts:110-114,138`). `max_tokens` is a fixed sane cap
(`MAX_TOKENS = 4096`, `anthropic.ts:117`), not a modeled/configurable value — a runaway-response
guard, not a per-call knob.

## The response event sequence

**Claim — the exact SSE event order Anthropic emits per turn**:

```
message_start → content_block_start → content_block_delta(delta.type==="text_delta", text at
delta.text)* → content_block_stop → message_delta → message_stop
```

(`anthropic.ts:11-15`, host-verified against the live API, SPEC §6.) **Claim — only
`content_block_delta` frames whose `delta.type === 'text_delta'` yield text**; every other frame in
the sequence (`message_start`/`content_block_start`/`content_block_stop`/`message_delta`/
`message_stop`) is silently ignored by `parseAnthropicSSE`, as is a bare `ping` frame and any
thinking/tool-use delta type (`delta.type !== 'text_delta'`) — documented at `anthropic.ts:70-78`,
enforced at `:86` (the non-delta filter) and `:103` (the `text_delta` check). **Failure mode — a
delta whose JSON fails to parse, or whose shape doesn't match `{ delta: { type, text } }`, is
silently skipped, never thrown** (`anthropic.ts:89-94`): a malformed data line is not this parser's
failure to report.

## The two-line SSE frame shape + the blank-line boundary

**Claim — one frame is one `event: <name>` line plus one or more `data:` lines** (multi-line data
joined, per the SSE spec's own accumulation rule), and frames are separated by a blank line
(`splitFrames`, `anthropic.ts:41-68`). Any other SSE field (`id:`, `retry:`, a bare comment) is
ignored — Anthropic's stream doesn't use them (`anthropic.ts:63`).

## The buffering assumption — why a naive per-chunk parse silently drops text

**Claim — `parseAnthropicSSE` assumes it is only ever handed WHOLE frames** (no event split
mid-frame across two chunks) — a documented assumption (`anthropic.ts:44-49`); the function itself
carries no buffer state (`anthropic.ts:50-68`).
**Claim — `stream()` satisfies this by splitting on the LAST blank-line boundary per `fetch` read**:
everything before it is a complete frame set, handed to the parser; everything after (a possibly
still-arriving partial frame) stays buffered for the next read (`anthropic.ts:163-176`). **Failure
mode / caveat — a naive "parse every chunk as it arrives" implementation will silently drop or
mis-parse a frame that happens to split across a `ReadableStream` chunk boundary** (a real risk:
network chunking is not aligned to SSE frame boundaries) — this is the exact defect the
buffer-until-blank-line technique exists to prevent. **Claim — any trailing complete-but-
unterminated buffer (a stream that ends without a final blank line) is flushed once after the read
loop exits** (`anthropic.ts:179-187`), so a response whose very last frame has no trailing blank
line is not silently lost.

## The error sentinel — an observable failure without a per-caller try/catch

**Claim — `event: error` does NOT throw inside `parseAnthropicSSE`**; it yields ONE sentinel string
(`ANTHROPIC_SSE_ERROR_PREFIX`, declared + explained at `anthropic.ts:26-32`; yielded at `:82-84`) so
the function stays a plain generator with no try/catch obligation on every caller — the rationale is
spelled out at `:74-78`. **Claim — `stream()` is the one place that checks the prefix and throws**
(`fragment.startsWith(ANTHROPIC_SSE_ERROR_PREFIX)` →
`throw new Error('anthropicProvider: upstream error event — ' + …)`, at BOTH the main-loop yield site
(`anthropic.ts:172-174`) and the trailing-flush yield site (`:182-184`))
— a distinguishable, observable failure, never a silently dropped mid-stream error. **Pattern
worth reusing beyond this adapter:** a sentinel VALUE through the same iterable contract, checked at
one boundary, is cheaper than threading an exception channel through a generator a pure-function
fixture suite needs to stay synchronous and side-effect-free.

## Cleanup on early exit (the consumer stops before the stream ends)

**Claim — a `try/finally` around the read loop guarantees `reader.cancel()` runs** whether the loop
exits normally, the consumer breaks early (the produce loop halts on the first valid payload — see
produce-loop), or an error-sentinel throw unwinds the generator — the rationale is documented at
`anthropic.ts:154-156`, the `try`/`finally` structure spans `:157-190`, and the actual
`reader.cancel().catch(() => {})` call sits at `:189`. `cancel()` is a documented safe no-op once
the stream already ended normally — no dangling network connection either way.

## What this file does NOT cover

The `AgentProvider` seam itself, the trust boundary, and the multi-provider registry
(provider-model-seam-and-trust-boundary) · how the loop consumes the resulting fragment stream and
turns it into validated A2UI JSONL (produce-loop) · OpenAI/Gemini's own wire contracts (not yet
implemented — `providers.json`'s `implemented: false`; a future adapter earns its own reference
here, not a retrofit of this one, since each provider's SSE shape is its own contract per SPEC-N5's
per-provider isolation).
