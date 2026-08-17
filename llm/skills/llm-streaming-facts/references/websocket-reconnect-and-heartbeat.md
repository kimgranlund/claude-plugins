# WebSocket reconnect needs a generation counter; heartbeat law

> Axis: WebSocket is bidirectional and stateful in a way SSE/EventSource are not — reconnect and
> liveness need their own discipline. Grounded in a worked instance:
> `@agent-ui`'s `data/src/stream/from-web-socket.ts`.

## A socket-generation counter — a dying socket's late events must stay inert

**Claim — every listener is bound to the generation it attached under; abandoning a socket
(heartbeat death, reconnect, or consumer close) bumps the generation, making its late events
inert.** Without this, a dying socket's late `close` event can re-enter the dead-handler and
double-reconnect, spawning a second socket alongside a first that hasn't actually died yet.
Abandon means CLOSE the dead socket, never leak it alongside its replacement. ·
`from-web-socket.ts:52-138` · 2026-08-17 · [verified]

## Heartbeat law — any inbound message resets the clock, not just pongs

**Claim — ANY inbound message resets the dead-connection clock, not only pong frames; a consumer
close DURING the backoff wait wins (no zombie socket lingers past the consumer's own decision to
stop); a consumer-INITIATED close is code 1000 and NEVER triggers a reconnect** — "finished" and
"disconnected" are different stream ends, and conflating them would reconnect a socket the
consumer deliberately closed. Reconnect itself is opt-in with capped full-jitter backoff;
exhaustion ends the stream with a typed, retryable network error, never a bare `Error`. ·
`from-web-socket.ts:101-155` (SPEC-R13c) · 2026-08-17 · [verified]

## What this file does NOT cover

The transport-agnostic `Streamed<T>` abstraction and backpressure policy every transport,
including this one, is bridged into: `stream-abstraction-transport-constraints.md`.
