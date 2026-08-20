# The 3-tier declarative streaming stack, and the double-ownership hazard

Source: `gen-ui-kit` `packages/web-components/core/{data-stream,streams-bridge,transport}.js` +
`.claude/docs/specs/data-stream-protocol.md`. All claims [verified] against these files unless
marked [incident].

## Tier 1 — attribute-driven transport

An element opts into live data purely by carrying a `data-stream-src` attribute (plus optional
`data-stream-mode`/`-interval`/`-method`/`-body`/`-headers`/`-path`/`-target`/`-merge`/`-format`/
`-event`/`-id`); a document-level `MutationObserver` claims it, no imperative wiring required.
Three transport modes share one entry point (`startTransport`): `http` (poll on an interval, or a
single tick with `interval=0`), `sse` (`EventSource`), `ws`/`websocket`. Format detection falls
back through file extension → `Content-Type` → explicit `data-stream-format`, parsing
csv/tsv/jsonl/text/json. — `core/data-stream.js:219-319` [verified]

Any element with a settable property qualifies (`<chart-ui>`, `<table-ui>`, `<stat-ui>`,
`<text-ui>`, `<heatmap-ui>` are the file's own worked examples) — the mechanism is universal, not
tied to one component family. — `core/data-stream.js:1-48` [verified]

## Tier 2 — refcounted shared signal

Stream identity is either explicit (`data-stream-id`) or a stable hash of the config
(`src`/`mode`/`interval`/`method`/`body`/`headers`/`format`/`event`) — two elements with
attribute-identical configs automatically share ONE transport. A module-level `STREAMS` registry
(`Map<streamId, {signal, refs, transport, opts}>`) refcounts consumers: the first `acquireStream`
call for an id creates the transport and a `signal(null)`; each further ref just increments
`refs`; the last `releaseStream` call (refcount hits 0) stops the transport and deletes the
registry entry. Each consuming element subscribes via its own `effect()` on the shared signal, so
N elements sharing one stream id each re-render independently off the same underlying fetch/SSE/WS
connection rather than each opening its own. — `core/data-stream.js:72-85, 323-355` [verified]

A read-only `streams` view (`get`/`has`/`keys`/`size`) and a `whenStream(id)` promise (resolves
once a stream registers, for a consumer that may run before the DOM source connects) are the
sanctioned programmatic surface for app code or a cross-package adapter that wants to read a
stream's value without owning its lifecycle. — `core/data-stream.js:77-100` [verified]

## Tier 3 — one-way bridge

`streams-bridge.js` proxies a registered stream's signal into an A2UI surface's data model:
`bridgeStream(renderer, {surfaceId, streamId, path, select})` attaches an `effect()` that calls
`renderer.process({type: 'updateDataModel', surfaceId, path, value})` on every signal update. The
renderer is duck-typed (only needs `.process()`), so the bridge works with the real `A2UIRenderer`,
a custom renderer, or a test stub. `bridgeStreamAsync` awaits `whenStream` first, for a DOM source
that may register after the bridge call returns. — `core/streams-bridge.js:1-97` [verified]

**Contract: one-way only.** Stream → data model. A2UI's own writes back to its data model (e.g. via
`update-data-model` wiring actions) do NOT propagate back into the stream signal — if bidirectional
state is needed, the stream is the wrong substrate; use a wiring action instead. Disposing the
bridge detaches the effect only; it does NOT release the stream's refcount, because the bridge
isn't the stream's lifecycle owner (the DOM consumer or a separate `acquireStream` caller is). —
`core/streams-bridge.js:18-26` [verified]

## The transport wrapper underneath

`transport.js` is the zero-dependency fetch primitive the HTTP tier's `tick()` sits on: timeout via
`AbortController`, exponential-backoff retries on 5xx, and a normalized `TransportError` (`kind`:
`abort`/`timeout`/`network`/`http`, carrying `status`/`body` where applicable). It has no
dependency on the signal/stream layer above it — a plain `request()`/`json()` pair any caller can
use standalone. — `core/transport.js:1-78` [verified]

## The double-ownership hazard

**Anti-pattern:** an element carrying `data-stream-src` that ALSO has its own imperative
`fetch()`/`setInterval` loop targeting the same endpoint creates two sources of truth writing the
same property — the document-level observer still claims any element bearing the attribute, so
both the declarative runtime and the hand-rolled fetch run concurrently unless the element opts
out. — `data-stream-protocol.md` §10.1 [verified]

**The opt-out:** `data-stream-managed="false"` tells the document-level observer to skip an
element permanently (`isStreamingEl()`'s claim test is `hasAttribute('data-stream-src') && managed
!== 'false'`) — set as the first thing the component does on `connected()`, before its own fetch.
This lets an element keep `data-stream-src` as its own documented public attribute (for consistency
with other elements' API) while still fully owning its imperative refresh path. — gh#1760,
`core/data-stream.js:65-70`, `data-stream-protocol.md` §10.5/Anti-patterns [verified]

**Worked instance:** the four billing composites (`billing-overview-ui`, `invoice-history-ui`,
`invoice-detail-ui`, `plan-picker-ui`) are gen-ui-kit's own canonical example — each documents
`data-stream-src` as its own public attribute (response-envelope unwrapping, `load`/`error` events
with a `reason` field) and sets the `managed="false"` marker in `connected()` rather than renaming
an already-shipped, heavily-documented attribute. Left unset, the document-level observer would
double-fetch the same endpoint alongside each composite's own imperative refresh. — gh#1760,
`data-stream-protocol.md` §10.5 [verified]

**The general rule this generalizes to:** never mix an imperative fetch with an unmanaged
`data-stream-src` on the same element — pick exactly one owner, declarative or imperative, and if
imperative, disclose it via the opt-out rather than leaving the attribute ambiguous between the two
runtimes. — `data-stream-protocol.md` §10.1 [verified]
