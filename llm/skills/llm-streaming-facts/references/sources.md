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
than a portable pattern, is the `agent-protocols` plugin's `a2ui-chat-agent-facts` pack
(`produce-loop.md`, `anthropic-sse-wire-contract.md`) — when the worked example and that pack
disagree, that pack's citation-verified snapshot of the real repo wins; this pack's job is to have
correctly generalized from it, not to duplicate it.

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`stream-abstraction-transport-constraints.md`, `websocket-reconnect-and-heartbeat.md`, and
`streaming-render-reveal-and-anchors.md` were added from agent-ui#1115's "Scope-conformant
revision v2" comment (posted 2026-08-17T17:14:57Z), the litmus-filtered re-harvest of
`@agent-ui/a2ui` lessons kept to web-based virtual-chat-harness knowledge only (lessons 46-53 of
that export, grounded in `data/src/stream/*`, `SPEC-R12/R13a/R13b/R13c`, ADR-0183/0194 —
transport/render facts distinct from this pack's existing SSE/Anthropic/validate-then-stream
citations). Lessons 1 and 5 of that same v2 export ("validate-then-stream", "empty ≠ invalid")
were confirmed as ALREADY covered by this pack's own pre-existing
`validate-then-stream-self-correct.md`, even though v2's own section header filed them under
`chat-harness-workflow-facts` — see that pack's own Provenance note for the corresponding skip.

## Provenance — 2026-08-19 provider-doctrine fold (agent-ui ADR-0073/0137/0200)

Two files extended 2026-08-19, folding agent-ui's ratified transport-seam doctrine (the ADRs read
via the GitHub API, never from recall): `stream-abstraction-transport-constraints.md` gained the
ONE `turn(input) → AsyncIterable<string>` seam (ADR-0073 clause 1 at the provider grain, ADR-0137
clause 2 at the transport grain), the three-backend shelf — deterministic replay/script as the CI
backbone, HTTP-only proxy for live, peer-over-protocol (ADR-0200 clause 3) — the pinned
request-body-fields rule (ADR-0200 Consequences), and the NDJSON splitter's own chunk-boundary
contract (the existing one-splitter rule taught only the dedup law, not the split mechanic).
`validate-then-stream-self-correct.md` gained the latency-cost/leading-meta-line section (worked
instance: `produce.ts:297` + `src/agent/meta-line.ts`, post-ADR-0137 paths; the `flowEnd` addition
riding the envelope per agent-ui #1101's closing comment, read 2026-08-17 evidence via the GitHub
API 2026-08-19). Diff-checked before writing: validate-then-stream's core ordering, the bounded
self-correct loop, the note-only-round success, and the one-NDJSON-splitter law were all already
covered — extended around, never restated.
