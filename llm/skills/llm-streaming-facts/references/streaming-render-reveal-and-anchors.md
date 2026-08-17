# Streaming render — first-paint exclusivity, opt-in reveal ordering, pending anchors

> Axis: once validated content is streaming down (see `validate-then-stream-self-correct.md`),
> how the RENDERER should paint it — when a whole-document transition is safe, whether to hold
> back an arrived sibling for reveal ordering, and how to render a reference to something that
> hasn't arrived yet. Grounded in worked instances: `@agent-ui/a2ui`'s ADR-0183 amendment,
> ADR-0194, and `renderer/tree.ts`.

## Never animate first-paint streaming; detect "already painted" with a settled-once boundary

**Claim — whole-document view transitions and streaming paint are mutually exclusive: wrapping
per-streamed-chunk in a transition would strobe whole-document snapshots.** The event actually
worth a transition is the RE-render of an already-fully-painted surface — the host's first
finalize marks it "settled," every ingest before that is first-paint (never transitions), every
one after is a re-render (may transition). A validation-stage hook is the wrong grain for this
decision: the DOM painted progressively before that hook ever fires, so wrapping finalize
animates nothing that hasn't already appeared. · ADR-0183 amendment (2026-08-12); wired in
`packages/agent-ui/app/src/controls/surface-host/` · 2026-08-17 · [verified]

## Coordinated top-down reveal trades away liveness — ship it opt-in, default OFF

**Claim — holding an already-arrived later sibling until earlier siblings arrive fixes reveal
jitter (components popping at random positions), but a never-arriving earlier sibling then
strands every later one — a real, accepted regression against "render what is available,"
shipped only behind a flag, default OFF.** The default path's own greedy-reveal tests pass
unmodified. Structural resends must resync the order bookkeeping, or a removed blocking sibling
permanently strands the cursor (a defect caught by review and regression-tested). · ADR-0194;
`packages/agent-ui/a2ui/src/renderer/tree.ts` · 2026-08-16 · [verified]

## Unresolved references are position-preserving anchors, patched in on arrival

**Claim — a streaming renderer holds unresolved references as position-preserving anchors and
patches them in on arrival, never blocking or erroring on a not-yet-defined reference.** Buffering
by id decouples arrival order from mount order, which is what makes an out-of-order stream
renderable at all — a strict "everything must arrive in dependency order" renderer would need to
either block or reject, and a live stream can't guarantee that order. · `a2ui-runtime.spec.md`
SPEC-R4; `renderer/tree.ts` (`#pendingParents`) · 2026-08-17 · [verified]

## What this file does NOT cover

Framing/backpressure at the transport-abstraction level, below the renderer:
`stream-abstraction-transport-constraints.md`. Validating the content before it ever reaches this
render layer: `validate-then-stream-self-correct.md`.
