# Single-flight 401 refresh — one refresh, shared, replayed correctly

> Axis: when several concurrent requests all hit a 401 at once, how to refresh exactly once and
> replay every request correctly against the NEW token, including the specific case of a one-shot
> streaming body that can't simply be re-sent. Grounded in a worked instance: `@agent-ui/a2ui`'s
> `packages/agent-ui/data/src/gateway/auth.ts`.

## One in-flight refresh, one normalized rejection, no thundering herd

**Claim — concurrent 401s dedupe onto ONE in-flight refresh promise shared by every caller; if
that refresh rejects, every queued awaiter receives the SAME (`Object.is`-identical) typed error
object, never divergent per-caller errors.** · `auth.ts:44-56` (SPEC-R9) · 2026-08-17 · [verified]

## Replay with the token the refresh RESOLVED, not a second read

**Claim — a replay after refresh uses the token the refresh call actually RESOLVED, never a
second `getToken()` call — the getter may lag the refresh's own resolution.** The replay-capable
clone of the request must be taken BEFORE the first send, not after a failure is already known. A
second 401 after replay is returned as-is: no infinite loop. · `auth.ts:58-75` · 2026-08-17 ·
[verified]

## A one-shot streaming body is honestly unreplayable

**Claim — reject a streaming-body replay attempt with a typed error rather than teeing "just in
case."** Detect via a carrier header set at shaping time — testing `body instanceof
ReadableStream` is the WRONG check, because every bodied `Request` exposes its body as a stream;
that test would refuse replay even for plain JSON bodies that are genuinely replayable. ·
`auth.ts:14-30,59-68` (SPEC-R9 AC4) · 2026-08-17 · [verified]

## What this file does NOT cover

Retry policy for a request that failed for a reason OTHER than a 401 (5xx, network drop), and the
streaming pass-through law that governs every middleware in the chain, including this refresh
layer: `retry-policy-and-streaming-passthrough.md`. The provider-adapter seam and
registry/trust-boundary validation this auth layer sits alongside: `provider-adapter-seam.md`,
`registry-and-trust-boundary.md`.
