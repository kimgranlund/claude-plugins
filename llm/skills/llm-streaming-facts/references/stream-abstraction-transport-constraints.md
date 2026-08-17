# One streaming contract, a declared backpressure policy, and per-transport constraints

> Axis: the top-level abstraction a chat product streams data through regardless of vendor
> transport (SSE, WebSocket, EventSource), and two concrete transport-specific facts a consumer
> trips on if not warned. Grounded in a worked instance's own spec:
> `saas-data-utilities.spec.md` (SPEC-R12/R13a/R13b) + `@agent-ui`'s `data/src/stream/`.

## `Streamed<T> = AsyncIterable<T>`, with a declared backpressure policy

**Claim — ONE streaming contract underlies every transport: `Streamed<T> = AsyncIterable<T>`,
bridged from a push producer via a single push→pull bridge under a DECLARED backpressure policy.**
Default is buffer-with-high-water-mark where `push` returns `false` as the producer's cue (never
throws) — dropping is a semantic decision an adapter cannot make for the consumer, so drop
policies exist only for telemetry-shaped feeds that explicitly opt into losing data.
`iterator.return()` and `signal.abort()` each end the stream and fire teardown exactly once;
push-after-end is a no-op, never an error. · `saas-data-utilities.spec.md` SPEC-R12;
`data/src/stream/bridge.ts` · 2026-08-17 · [verified]

## EventSource's own auth constraint — cookie or query-ticket only, no custom headers

**Claim — EventSource's platform constraint, stated in the export's own docs because every
consumer trips on it otherwise: no custom headers are possible — auth must be cookie-based or a
query-ticket; `Last-Event-ID` resume is the platform's own mechanism, not something the
application implements.** A grep-gated doc-comment requirement exists specifically because this
constraint is easy to forget and expensive to discover late. · SPEC-R13b + `data/src/stream/
from-event-source.ts` · 2026-08-17 · [verified]

## Exactly ONE NDJSON line-splitter — old locations become re-exports

**Claim — keep exactly ONE NDJSON line-splitter implementation; old call-site locations become
one-line re-exports with an IDENTICAL name and signature**, with the original call-site's
chunk-boundary tests re-run against the hoisted body — behavior parity pinned by tests, type
parity by the compiler. A second, independently-drifting NDJSON splitter is exactly the kind of
duplicate this rule exists to prevent. · SPEC-R13a AC1; `data/src/stream/ndjson-lines.ts`
(re-export at `site/lib/ndjson-lines.ts`) · 2026-08-17 · [verified]

## What this file does NOT cover

The SSE-specific chunk-buffering technique (a related but distinct transport, covered in more
depth): `sse-chunk-parsing-technique.md`. WebSocket's own reconnect/heartbeat lifecycle, a
genuinely different failure surface from SSE/EventSource's one-directional stream:
`websocket-reconnect-and-heartbeat.md`. What a streaming renderer does with content once
delivered (reveal order, view transitions): `streaming-render-reveal-and-anchors.md`.
