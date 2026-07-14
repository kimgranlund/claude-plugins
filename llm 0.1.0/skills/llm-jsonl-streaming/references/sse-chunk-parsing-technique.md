# The SSE chunk-buffering technique — correctly parsing ANY vendor's event stream

> Axis: the general technique for turning a chunked byte stream into whole Server-Sent Events,
> regardless of vendor. Grounded in the WHATWG/W3C Server-Sent Events spec (a platform fact) + the
> Streams API (`ReadableStream`/`fetch`, also platform facts) + a worked instance:
> `packages/agent-ui/a2ui/tools/agent/providers/anthropic.ts` in `@agent-ui/a2ui` (the full
> vendor-specific contract lives in anthropic-sse-worked-example — this file is the REUSABLE
> technique, generalized).

## The core problem — a network chunk boundary is not an event boundary

**Platform fact:** an SSE stream is plain text, one or more events separated by a BLANK LINE; one
event is one-or-more `field: value` lines (commonly `event:` and `data:`, `data:` lines
accumulating if repeated). **Platform fact (the Streams API):** `fetch`'s
`response.body.getReader().read()` returns chunks whose byte boundaries are determined by the
network stack, NOT by the application-level event framing — nothing guarantees a `read()` call
returns text ending exactly at a blank-line event boundary. **Failure mode this causes:** a naive
parser that treats every `read()` result as "one complete unit to parse right now" will,
intermittently and only under certain chunking patterns, receive a frame that's been split in
half across two reads — silently dropping or mis-parsing the tail of one event and the head of
the next. This bug is exactly the kind that passes every test written against small, single-chunk
fixtures and then fails unpredictably against real network traffic.

## The fix — buffer until you have a genuinely whole set of frames

**Technique:** accumulate incoming chunk text into a buffer; after each read, find the LAST
blank-line boundary in the accumulated buffer; parse everything up to and including that boundary
(a complete set of whole frames); keep everything after it (a possibly still-arriving partial
frame) buffered for the next read. Only when the stream itself ends do you flush any remaining
buffered text (which, if the stream ended without a final blank line, is still one complete,
unterminated-but-parseable frame).

Illustrative pseudocode, not the cited code verbatim (the worked instance below uses real
TypeScript with its own variable names):

```
buffer += decode(chunk)
lastBoundary = buffer.lastIndexOf(BLANK_LINE)
if lastBoundary == -1: continue        // no complete frame yet, keep buffering
complete = buffer[:lastBoundary]        // hand this, and ONLY this, to the frame parser
buffer = buffer[lastBoundary+len:]      // keep the remainder for the next read
… on stream end: if buffer.trim() non-empty, parse it too (the final, blank-line-less frame)
```

**Worked instance:** `anthropic.ts:163-176` (the split-on-last-boundary logic + the per-read
parse loop) and `:179-187` (the end-of-stream flush of any trailing unterminated buffer). **Why
"last" boundary, not "first":** splitting on the first boundary would parse one frame per read at
best and leave the rest sitting in the buffer needlessly — splitting on the LAST boundary found
extracts every complete frame currently available in one pass.

## Frame parsing — one `event:`/`data:` pair per blank-line-delimited block

**Technique:** within a "complete" text block (already assumed whole per the buffering above),
split on blank lines to get individual frames; within each frame, split on newlines and dispatch
each line by its `field:` prefix (`event:`, `data:`, others ignored unless your vendor uses them);
multiple `data:` lines within one frame are joined (per the SSE spec's accumulation rule) — most
vendors don't emit multi-line `data`, but a parser that assumes single-line will silently
mis-handle the (rare, spec-legal) case where one does. **Worked instance:** `anthropic.ts:41-68`
(`splitFrames`) — note the function is PURE (no network, no state) and therefore trivially
fixture-testable in isolation from the network/buffering concern above; keeping frame-parsing and
chunk-buffering as two separate functions (one pure, one impure) is itself the reusable structural
idea — test the parsing logic exhaustively with static fixtures, and keep the buffering
plumbing thin enough that it barely needs its own tests.

## The error-sentinel technique — an observable failure without a try/catch on every caller

**Technique:** when the stream itself signals an error frame (an `event: error` or vendor
equivalent), don't throw INSIDE the pure per-chunk parser (a `function*` generator) — yield a
distinguishable SENTINEL value through the SAME iterable contract every normal fragment rides
(e.g. a fixed string prefix no legitimate model output would produce), and let exactly ONE
caller — the outer consumer that's already wrapping the whole stream in error-handling — check for
the sentinel and throw from there. **Why this is cheaper than threading an exception channel
through a generator:** a generator that might throw mid-iteration forces every consumer to wrap
its iteration in try/catch; a generator that never throws and instead yields an occasional
sentinel value keeps the iteration protocol uniform, and concentrates the "is this actually an
error" check at exactly one boundary. **Worked instance:** `anthropic.ts:26-32` (the sentinel
constant + rationale), `:82-84` (yielded, not thrown, inside the pure parser), `:172-174,182-184`
(the ONE place — the impure `stream()` function — that checks the prefix and throws).

## What this file does NOT cover

Anthropic's OWN concrete event names/sequence, wired up as a full worked example
(anthropic-sse-worked-example) · what happens to the accumulated text once you have it — is it
valid structured output yet, and what if it isn't (validate-then-stream-self-correct) · the
provider-adapter interface this parsing logic lives inside
([[llm-provider-gateway]]'s provider-adapter-seam).
