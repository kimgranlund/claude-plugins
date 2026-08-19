# One streaming contract, a declared backpressure policy, and per-transport constraints

> Axis: the top-level abstraction a chat product streams data through regardless of vendor
> transport (SSE, WebSocket, EventSource), the ONE turn-seam a conversation stack isolates its
> backends behind, and concrete transport-specific facts a consumer trips on if not warned.
> Grounded in a worked instance's own spec: `saas-data-utilities.spec.md` (SPEC-R12/R13a/R13b) +
> `@agent-ui`'s `data/src/stream/`, and in that repo's ratified transport-seam decisions
> (ADR-0137/ADR-0200, read via the GitHub API 2026-08-19).

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

## The NDJSON splitter's own contract — the same chunk-boundary law as SSE, one line at a time

**Claim — the one splitter above obeys the same discipline the SSE technique file teaches, with
`\n` as the frame boundary instead of a blank line: buffer the undelivered tail across reads, emit
only complete newline-terminated lines, flush any non-empty remainder when the stream ends — a
network `read()` boundary is NEVER a line boundary.** This primitive is exactly what makes NDJSON
the right agent-drivable wire: one JSON object per line parses incrementally with a trivial
splitter, needs no event-framing state machine, and stays curl-able end to end — the worked repo
chose `POST + application/x-ndjson` for its debug-orchestration seam over SSE/WebSocket precisely
because the whole stack already spoke NDJSON lines through this one reader idiom. **Failure mode
without it:** the same intermittent, chunking-dependent record corruption the SSE file describes —
passing every single-chunk fixture test and failing only against real network traffic.
· `data/src/stream/ndjson-lines.ts` (the hoisted body the one-splitter rule protects); the
transport choice: agent-ui ADR-0200, Alternatives ("reuses the exact reader idiom… and stays
curl-able for an agent driver") · 2026-08-19 · [verified]

## The turn seam — ONE `turn(input) → AsyncIterable<string>` every consumer binds to

**Claim — expose "run one model turn" to every consumer as ONE async-iterable seam —
`turn(input) → AsyncIterable<string>`, yielding the raw emitted lines/fragments — and make every
backend an implementation of that interface, so no consumer ever names a vendor or a transport.**
The worked repo pins this shape at two grains, both ratified: the provider grain, whose seam
shape [[llm-gateway-facts]]'s provider-adapter-seam reference owns (cited, not restated here) —
and the transport grain above it — `AgentTransport.turn(input): AsyncIterable<string>`, "the ONE interface
every consumer binds to" (ADR-0137 clause 2; restated as the load-bearing premise of ADR-0200).
**Failure mode:** without the single seam, each consumer couples to one backend's wire specifics,
and every backend swap — stub for test, proxy for live — becomes a consumer rewrite instead of a
constructor argument. · agent-ui ADR-0073 (accepted 2026-07-04) / ADR-0137 (accepted 2026-07-16) /
ADR-0200 (accepted 2026-08-17), read via the GitHub API · 2026-08-19 · [verified]

## The three-backend shelf — deterministic replay for CI, HTTP proxy for live, peer-over-protocol

**Claim — behind that one seam, ship a SHELF of backends, all implementing the same interface:
(1) replay/script transports playing canned timelines — deterministic by contract (two runs yield
byte-identical line sequences), no key, no network: the CI backbone and the fixture source;
(2) a proxy transport that POSTs the turn to the server-side mount and yields its streamed NDJSON
lines — the live path, over HTTP ONLY, so no key, provider adapter, or producer loop ever enters
the client-side package (the trust boundary stays where the gateway pattern put it); (3) a peer
transport framing the turn onto an agent-to-agent channel.** Swapping backends is a
one-construction-site edit, and a backend descriptor row (`{id, label, available()}`) feeds both a
picker UI and a status probe from ONE list — the gateway pack's one-list rule, applied to
backends. **Failure mode the shelf prevents:** a harness whose tests can only run against the live
model (flaky, slow, keyed), or whose deterministic path drifts from the live path because the two
were never the same interface. · agent-ui ADR-0200 clause 3 (`@agent-ui/devtools`) · 2026-08-19 ·
[verified]

## Pin the live backend's request-body fields — proxy drift is a spec diff, not a silent break

**Claim — a live HTTP backend is coupled to its proxy's request/response shape with no
compile-time check across the process boundary, so PIN the body fields the transport relies on in
the owning spec and keep a round-trip suite that exercises them — a server-side body change is
then forced to surface as a reviewable spec diff (and a red suite) rather than a silent runtime
break.** The tempting alternative — importing the server's own types/internals into the client for
compile-time safety — re-opens exactly the trust boundary the HTTP-only coupling exists to keep
closed. · agent-ui ADR-0200, Consequences ("a proxy body change can break `proxyTransport` without
a compile error… the SPEC pins the body fields the transport relies on, and the round-trip suite
catches drift") · 2026-08-19 · [verified]

## What this file does NOT cover

The PROVIDER-grain seam itself — per-vendor adapter shape, key custody, endpoint registry:
[[llm-gateway-facts]] (provider-adapter-seam) owns it; this file stops at the transport grain.
The SSE-specific chunk-buffering technique (a related but distinct transport, covered in more
depth): `sse-chunk-parsing-technique.md`. WebSocket's own reconnect/heartbeat lifecycle, a
genuinely different failure surface from SSE/EventSource's one-directional stream:
`websocket-reconnect-and-heartbeat.md`. What a streaming renderer does with content once
delivered (reveal order, view transitions): `streaming-render-reveal-and-anchors.md`. WHEN each
backend tier is the right proof — deterministic replay as the standing CI gate vs. a live turn
reserved for acceptance: [[chat-harness-logging-facts]] (this file owns how the seam and shelf are
SHAPED, not the testing discipline that chooses between them).
