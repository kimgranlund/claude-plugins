# Sources — provenance for the streaming-pattern claims

This pack teaches technique, not one repo's implementation — each claim is grounded in one of
two kinds, and the reference files say which.

## Spec / vendor facts — verify against current docs if stale-sensitive

- **The WHATWG/W3C Server-Sent Events (SSE) spec** — event/blank-line framing, the `data:`
  multi-line accumulation rule, the standard field set (`event:`, `data:`, `id:`, `retry:`).
  Platform-standard, vendor-independent.
- **The Streams API (`fetch`, `ReadableStream`, `TextDecoder`)** — chunk boundaries are
  network-determined, not application-framing-aware. Platform-standard.
- **Anthropic's Messages API streaming contract** (`POST /v1/messages`, `stream: true`) — the
  `message_start`/`content_block_start`/`content_block_delta`/`content_block_stop`/
  `message_delta`/`message_stop` event sequence, `ping` keepalives, the `text_delta` vs
  thinking/tool-use delta distinction. A vendor fact — verify against Anthropic's current public
  API documentation if this pack has aged; the sequence is independently corroborated (not solely
  read off one adapter's interpretation) by the worked example's own host-verification note.

## The worked example — a real, shipped instance (cited for concrete grounding, not sole authority)

**`@agent-ui/a2ui`'s live-agent system**, `/Users/kimba/Projects/nonoun/agent-ui`,
`packages/agent-ui/a2ui/tools/agent/`:

- `providers/anthropic.ts` — `parseAnthropicSSE`/`splitFrames` (the pure frame parser),
  `anthropicProvider().stream()` (the impure buffering + fetch loop), the
  `ANTHROPIC_SSE_ERROR_PREFIX` sentinel.
- `packages/agent-ui/a2ui/src/live-agent/anthropic-sse.test.ts` — the fixture suite proving
  `parseAnthropicSSE` against static SSE text, no network.
- `produce.ts` — the bounded self-correct loop (`produce()`), `assembleFromRaw`/`stripOuterFence`
  (heal-then-parse), `messagesFor` (failure feedback), `ProduceHalt` (the halt-and-report type).

Cited as PROOF the pattern works in a real, running, tested system — not as the only valid
implementation. A consumer's own project may reasonably differ in language, structured-output
format (JSONL is one instance of "structured, streamable, line-delimited"; the validate-then-
stream PATTERN applies to any format with a clear "is this one record complete and valid yet"
check), or retry-bound policy, while still honoring the invariants in each reference file.

## Boundary — layers owned elsewhere

This pack answers streaming/validation technique; it does not restate its neighbor. The
provider-adapter seam this streaming logic lives behind, the secret trust boundary, and the
conversation/session model are [[llm-gateway-facts]]. `@agent-ui/a2ui`'s OWN system, documented
as that repo's actual shipped behavior (dated, exhaustive, cited against a single snapshot) rather
than a portable pattern, is the `agentic-ui` plugin's `a2ui-conversational-agent` pack
(`produce-loop.md`, `anthropic-sse-wire-contract.md`) — when the worked example and that pack
disagree, that pack's citation-verified snapshot of the real repo wins; this pack's job is to have
correctly generalized from it, not to duplicate it.
