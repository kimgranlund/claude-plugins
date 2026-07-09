# Transport — JSON-RPC methods, streaming, push

> **GAP (one residual, 2026-07-08):** push-notification callback semantics (the webhook contract,
> when it beats polling) and `tasks/resubscribe` resumption semantics are not HV-quoted — needs a
> spec fetch before answering those; everything else below is grounded.

Estate paths relative to `agent-ui/packages/agent-ui/`; HV rows live in SPEC §2
(`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## Transport posture `[spec — HV-2]`

"A2A communication **MUST** occur over **HTTP(S)**." v0.3.0 defines **three equal-status core
transports** (JSON-RPC 2.0 · gRPC · HTTP+JSON/REST); "Agents **MUST** implement at least one" and
**MAY** choose JSON-RPC — so a JSON-RPC-only implementation is compliant. `AgentCard.
preferredTransport` defaults to `"JSONRPC"`. The estate scopes to JSON-RPC as a deliberate,
recorded choice (SPEC-R7).

## The v0.3.0 JSON-RPC method set — EXACT `[spec §3.5.6 — HV-3]`

Naming pattern: "Method names follow the pattern `{category}/{action}`". The full surface:

```
message/send        message/stream       tasks/get       tasks/cancel
tasks/resubscribe   tasks/pushNotificationConfig/set | get | list | delete
agent/getAuthenticatedExtendedCard
```

(`tasks/list` exists but is "gRPC/REST only".) This casing is the wire-breaking surface: **v1.0
renames these to PascalCase** — see `versioning-and-conformance.md` before quoting any name
against a non-0.3.0 peer.

**Estate scope** `[estate — a2a/src/rpc/frame.ts:10-43]`: `SUPPORTED_METHODS = ['message/send',
'tasks/get', 'tasks/cancel']` (what B1 frames + serves); `KNOWN_METHODS` = the full HV-3 surface,
so `classifyMethod` can distinguish **known-but-unsupported → `-32004`** from **unknown →
`-32601`** `[estate — a2a/tools/http/core.ts:48-56]`.

## Per-method params/results `[spec — HV-12]`

| Method | params | result |
|---|---|---|
| `message/send` | `{ message, configuration?, metadata? }` | `Message \| Task` ("a direct reply Message or the initial Task object") |
| `tasks/get` | `{ id, historyLength?, metadata? }` (TaskQueryParams extends TaskIdParams) | `Task` |
| `tasks/cancel` | `{ id, metadata? }` (TaskIdParams) | `Task` ("the final state of the canceled Task") |

`MessageSendConfiguration = { acceptedOutputModes?; historyLength?; pushNotificationConfig?;
blocking? }` — typed in the estate except `pushNotificationConfig: unknown` (known-unsupported)
`[estate — a2a/src/rpc/frame.ts:47-72]`. Every response is the success shape `| JSONRPCErrorResponse`.

## Framing, errors, correlation `[estate]`

- Envelopes are plain JSON-RPC 2.0 (`jsonrpc: '2.0'`, `id`, `method`/`params` | `result`/`error`)
  `[estate — a2a/src/rpc/frame.ts:78-109]`.
- `parseFrame(text)` is total: `{ok: true, frame} | {ok: false, failures}`; raw-parse failure →
  `A2A_RPC` with `parse: true`; malformed envelope → the validator's `A2A_RPC` failures
  `[estate — a2a/src/rpc/frame.ts:119-130]`.
- Error table (both directions, one `as const` map): standard `-32700/-32600/-32601/-32602/-32603`
  + the seven A2A codes `-32001 TaskNotFound … -32007 AuthenticatedExtendedCardNotConfigured`
  `[spec §8.2 — HV-9; estate — a2a/src/rpc/errors.ts:12-25]`. Outbound mapping is 3-tier:
  `parse: true` → `-32700`; non-parse `A2A_RPC` → `-32600`; everything schema-shaped → `-32602`;
  `-32603` is reserved for handler throws caught at the `createRpcCore` boundary
  `[estate — a2a/src/rpc/errors.ts:40-44, a2a/tools/http/core.ts:65-70]`.
- Correlation: `createRpcCorrelator()` — monotonic integer ids from 1 + a pending map;
  deterministic by design (byte-stable transcripts sit on it); an orphan response id → `A2A_RPC`
  at `/id`, dropped-with-record `[estate — a2a/src/rpc/frame.ts:149-172]`.

## SSE streaming `[spec — HV-6]` — spec facts; NOT implemented in the estate

- Streaming methods: `message/stream` and `tasks/resubscribe` `[spec — HV-3]`.
- Event shapes: `TaskStatusUpdateEvent` (`kind: "status-update"`) carries `final: boolean` — "If
  true, this is the final event in the stream for this interaction."; `TaskArtifactUpdateEvent`
  (`kind: "artifact-update"`) carries `append?: boolean` + `lastChunk?: boolean` — "If true, this
  is the final chunk of the artifact."
- Carriage: SSE per [S] §3.3.1 — **each SSE `data` field = one complete JSON-RPC response**.
- Estate posture: streaming is deliberately unbuilt — the server answers `-32004
  UnsupportedOperationError`, and the event types are deliberately NOT typed (no consumer yet;
  typing unconsumed shapes is gold-plating) `[estate — a2a/src/protocol/types.ts:141-142]`.

## Push notifications

The four `tasks/pushNotificationConfig/*` methods exist at v0.3.0 `[spec — HV-3]` and the card
declares `capabilities.pushNotifications?` `[spec — HV-7]`; `-32003
PushNotificationNotSupportedError` is the dedicated code `[spec — HV-9]`. The estate does not
implement them (config methods answer `-32004`) `[estate — a2a/src/rpc/frame.ts:15-26,
a2a/tools/http/core.ts:52-56]`. Callback-contract semantics: see the GAP banner.

## The estate's transports `[estate]`

- **Channel contract**: `A2aChannel { send; receive(): AsyncIterable; close() }`
  `[estate — a2a/src/channel/loopback.ts:7-11]`. `close()` is behavioral contract: buffered
  messages drain then iterators complete; `send` after close (own or peer) rejects with a typed
  `A2aChannelClosedError` — loud, never a silent drop `[estate — a2a/src/channel/loopback.ts:50-66]`.
- **Loopback** (`createLoopbackPair`): two FIFO inboxes, microtask-only, zero timers/IO — the
  arena's isolation boundary and CI's transport `[estate — a2a/src/channel/loopback.ts:85-89]`.
- **HTTP** (dev/Node, never in a consumer bundle): a socket-free total core —
  `createRpcCore(handlers).handleRpc(body)` owns parse → validate → dispatch → respond
  `[estate — a2a/tools/http/core.ts:31-71]` — plus a thin `node:http` shell: POST `/a2a` →
  `handleRpc`; GET the well-known path → the served card; the ONLY socket-touching file, exercised
  by a manual smoke, never a standing test (SPEC-N2/N3)
  `[estate — a2a/tools/http/server.ts:16-39]`. Transport-invariance is proven through the
  injectable `post` seam wired straight to `handleRpc` (SPEC-R8 AC1).
