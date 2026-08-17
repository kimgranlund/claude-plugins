# Retry policy defaults, and the streaming pass-through law every middleware obeys

> Axis: how a gateway decides WHETHER to retry a failed request, and the separate, stricter rule
> that no middleware in the chain — including the retry layer itself — may read or buffer a
> streaming response body it isn't the terminal consumer of. Grounded in a worked instance:
> `@agent-ui/a2ui`'s `packages/agent-ui/data/src/gateway/retry.ts`.

## Idempotent-only by default, full jitter, `Retry-After` wins when larger

**Claim — retry defaults to idempotent methods only (GET/HEAD/OPTIONS/PUT/DELETE) or an explicit
opt-in; backoff is full jitter (`random(0, min(cap, base·2^n))`); a server's `Retry-After` header
overrides the computed backoff only when it's LARGER; the backoff wait itself is abortable via
the request's own signal.** A retryable-but-non-idempotent POST fails after one attempt by
design — the caller must opt in explicitly, since retrying a non-idempotent request blind risks a
duplicate side effect. · `retry.ts` (SPEC-R10) · 2026-08-17 · [verified]

## Cancel a discarded response's body; skip cloning when retry can't happen

**Claim — cancel the body of a response you're about to discard on retry; cancel is not a read,
and leaving the stream open holds the underlying connection until GC.** Skip cloning entirely
when retry cannot happen at all (a single attempt, or a non-idempotent method with no opt-in),
and hand the ORIGINAL request (never a clone) to the LAST permitted attempt — there is nothing
left to preserve a body for once no further retry is possible. · `retry.ts:56-99` · 2026-08-17 ·
[verified]

## The streaming pass-through law — no middleware reads, tees, or buffers the body

**Claim — retry classification reads status/headers ONLY, never the body (a 5xx WITH a body
retries unread); the caller receiving the final response sees `bodyUsed === false` and
`body.locked === false` all the way through the middleware chain; any body-consuming helper is
TERMINAL, never middleware.** Enforced with a negative-control test: a planted `await
res.text()` inside a middleware must turn the gate RED — proving the check actually catches a
violation, not just that it passes today. · `saas-data-utilities.spec.md` SPEC-R11 +
`gateway/passthrough.test.ts` · 2026-08-17 · [verified]

## What this file does NOT cover

The 401-specific single-flight refresh-and-replay mechanism (a narrower case of "retry," with its
own dedup and token-freshness rules): `single-flight-401-refresh.md`. What happens to the body's
CONTENT once a consumer legitimately reads it (chunk framing, backpressure): [[llm-streaming-facts]].
