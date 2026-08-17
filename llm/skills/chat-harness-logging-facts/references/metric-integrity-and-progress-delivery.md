# Don't let a metric saturate on noise; decouple progress delivery from yield cadence

> Axis: two adjacent measurement-integrity failure modes in a chat product's own producer loop —
> a repair-rate metric that measures nothing because it counts mechanical noise, and a progress
> signal that goes invisible because it's tied to the wrong event. Grounded in a worked instance:
> `@agent-ui/a2ui`'s `produce.ts`.

## Exclude mechanical normalization from a repair-rate metric

**Claim — the healed-line count counts only REAL form repairs, explicitly excluding the envelope
normalization that fires on every well-formed line.** Without this exclusion the metric saturates
to line-count on every clean turn and measures nothing at all — a metric that can never read zero
even on a perfectly healthy turn has stopped being a metric. · `produce.ts:554-581` · 2026-08-17 ·
[verified]

## Progress delivery must not wait on the provider's own yield cadence

**Claim — a provider can run a whole tool round without yielding a text fragment while its event
callback fires in real time; draining events only BETWEEN fragments buffers a round's progress
invisibly.** The fix races the iterator's `next()` against a wakeable push channel so events
surface the instant they happen, with any queued progress always yielded before the fragment
that followed it. · `produce.ts:217-279` (GH #290) · 2026-08-17 · [verified][incident]

**Why this matters:** a progress UI that only updates when text happens to stream is silently
wrong during any tool-heavy round — the user sees nothing move for the whole round's duration,
then a burst of fragments, which reads as "stuck" even though real work was happening the whole
time.

## What this file does NOT cover

Assembling the per-turn trace itself and the diagnostic-message format a failure renders in:
`turn-trace-and-failure-diagnostics.md`. This harness's own hook-based tracing mechanism, a
distinct system: this pack's own `logging-and-tracing.md`.
