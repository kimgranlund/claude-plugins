# Anthropic's Messages API SSE contract — a fully worked instance

> Axis: the exact event sequence Anthropic's `/v1/messages` streaming endpoint emits, as a
> concrete, fully worked application of the general chunk-buffering technique
> (sse-chunk-parsing-technique). Grounded in Anthropic's own publicly documented Messages API
> streaming format (a vendor fact — verify against Anthropic's current API docs if this pack is
> old) and a worked instance: `packages/agent-ui/a2ui/tools/agent/providers/anthropic.ts` +
> `packages/agent-ui/a2ui/src/live-agent/anthropic-sse.test.ts` (the fixture suite) in
> `@agent-ui/a2ui`.

## The request

**Vendor fact:** `POST https://api.anthropic.com/v1/messages`, headers `x-api-key: <key>` +
`anthropic-version: <date-versioned string, e.g. 2023-06-01>` + `content-type: application/json`,
body `{ model, system, messages, stream: true, max_tokens }`. `system` is a TOP-LEVEL request
param, not a message in the `messages` array — a common mistake when adapting code written for an
API where the system prompt IS a message. `max_tokens` is required. **Worked instance:**
`anthropic.ts:129-144` (the exact fetch call); `anthropic.ts:110-114,138` (the `system`-is-not-a-
message mapping); a fixed `MAX_TOKENS` constant as a runaway-response guard, not a per-call
config knob, at `anthropic.ts:117`.

## The response event sequence

**Vendor fact — the streaming event order Anthropic's Messages API emits per turn:**

```
message_start → content_block_start → content_block_delta(delta.type==="text_delta", text at
delta.text)* → content_block_stop → message_delta → message_stop
```

Only `content_block_delta` frames whose `delta.type === 'text_delta'` carry appendable text;
every other frame in the sequence is structural bookkeeping (start/stop markers, final metadata)
and should be ignored by a parser that only wants the accumulated text. A `ping` frame may appear
at any point (a keepalive, no payload) and is always ignored. A thinking/tool-use delta type
(`delta.type !== 'text_delta'`) is a real, documented Anthropic feature outside this worked
example's scope — a consumer that also wants those must branch on `delta.type` rather than
filtering to `text_delta` alone. **Worked instance:** `anthropic.ts:11-15` (the sequence,
documented as host-verified against the live API); enforced at `anthropic.ts:86` (the non-delta
frame-type filter) and `:103` (the `text_delta` check); a malformed/unexpected-shape delta is
silently skipped rather than thrown — a JSON parse failure at `anthropic.ts:89-94`, an
unexpected-shape no-op (the `delta` field missing or non-object) at `:95-101`.

## The two-line frame shape + the blank-line boundary

**Vendor fact, matching the general SSE spec exactly (no Anthropic-specific deviation):** one
frame is one `event: <name>` line plus one or more `data:` lines (multi-line data joined), frames
separated by a blank line. **Worked instance:** `anthropic.ts:41-68` (`splitFrames`); any other
SSE field (`id:`, `retry:`) is ignored — Anthropic's stream doesn't use them,
`anthropic.ts:63`.

## The buffering assumption — applying the general technique

**Claim — the pure per-chunk parser assumes it is only ever handed WHOLE frames** (documented at
`anthropic.ts:44-49`; the function itself, `:50-68`, carries no buffer state of its own — see
sse-chunk-parsing-technique for why this split between a pure parser and an impure
buffering caller is the reusable idea, not specific to Anthropic). The impure `stream()` function
satisfies the assumption by splitting on the last blank-line boundary per `fetch` read
(`anthropic.ts:163-176`) and flushing any trailing complete-but-unterminated buffer once the
stream ends (`:179-187`).

## The error sentinel — applying the general technique

**Worked instance of the sentinel technique:** the constant + rationale at `anthropic.ts:26-32`;
yielded (never thrown) inside the pure parser at `:82-84`, with the "why not throw here"
rationale at `:74-78`; checked and thrown from the ONE place that matters — `stream()`'s two yield
sites, `:172-174` (main loop) and `:182-184` (trailing flush).

## Cleanup on early exit

**Worked instance:** a `try/finally` around the whole read loop guarantees `reader.cancel()` runs
whether the loop exits normally, a consumer breaks early (e.g. the validate-then-stream driver
halts on the first fully valid payload — see validate-then-stream-self-correct), or an
error-sentinel throw unwinds the generator — rationale at `anthropic.ts:154-156`, the structure at
`:157-190`, the actual `reader.cancel().catch(() => {})` call at `:189`. **General principle
beyond this one vendor:** any stream consumer that can exit before the underlying source is
exhausted needs an explicit cleanup path (`finally`, `using`, or the equivalent in your
language/runtime) or the underlying connection/reader lock leaks.

## What this file does NOT cover

The reusable buffering/framing/sentinel TECHNIQUE, generalized beyond this one vendor
(sse-chunk-parsing-technique) · what happens to the accumulated text once assembled — is it
valid structured output, and the bounded retry loop if not
(validate-then-stream-self-correct) · a different vendor's own concrete contract (not yet
worked through in this pack — OpenAI and Gemini adapters are unimplemented in the cited worked
example as of this writing; a future addition earns its OWN reference here, never a retrofit of
this one, since each vendor's actual wire shape is genuinely its own contract).
