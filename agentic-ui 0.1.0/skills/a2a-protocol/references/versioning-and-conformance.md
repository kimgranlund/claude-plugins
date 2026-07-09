# Versioning & conformance — the pin, and why drift is wire-breaking

> **GAP (one residual, 2026-07-08):** the FULL v0.3.0 → v1.0 method-name mapping table is not
> HV-quoted (the ledger carries only three PascalCase examples) — needs a spec fetch of [S1] §5.3
> before publishing a complete side-by-side table. Everything else below is grounded.

Estate paths relative to `agent-ui/packages/agent-ui/`; HV rows live in SPEC §2
(`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## The pin `[estate]`

`@agent-ui/a2a` pins **A2A spec v0.3.0**: `PROTOCOL_VERSION = '0.3.0'`
`[estate — a2a/src/protocol/types.ts:8]` — a deliberate, recorded choice (PRD-D3), not lag.
Upstream context `[spec — HV-1]`: releases are `v0.3.0` (2025-07-30), `v1.0.0` (2026-03-12),
`v1.0.1` (2026-05-28, current stable); v0.3 remains the assumed-default prior lineage — "Agents
MUST interpret empty value as 0.3 version." ([S1] §3.6.2). `AgentCard.protocolVersion` is a
required field with upstream default `"0.3.0"` `[spec — HV-7]`.

## Why 1.0.x is wire-breaking `[spec — HV-3]`

**v1.0 renames the JSON-RPC methods to PascalCase** matching gRPC conventions — the HV-quoted
examples are `SendMessage`, `GetTask`, `SubscribeToTask` ([S1] §5.3/§9: "Method Naming: PascalCase
method names matching gRPC conventions"). A v0.3.0 client calling a 1.0.x server (or vice versa)
fails at the METHOD level (`-32601`) before any payload semantics engage. The v0.3.0 names are in
`transport-and-streaming.md`; the full pairing table awaits the fetch (banner above).

Other HV-grounded 1.0.x deltas:
- Error codes `[spec — HV-9]`: `-32007` renamed `ExtendedAgentCardNotConfiguredError`; NEW
  `-32008 ExtensionSupportRequiredError` and `-32009 VersionNotSupportedError`.
- The well-known path was ALREADY renamed at v0.3.0 (`agent.json` → `agent-card.json`, a listed
  v0.3.0 breaking change) and is unchanged in v1.0.1 `[spec — HV-7]`.

Any "upgrade the pin" ask is therefore a migration project: every method name, the error table,
plus a re-verification sweep of the whole HV ledger against the new spec text. The estate isolated
the version-sensitive surface into two `as const` tables (`KNOWN_METHODS`/`SUPPORTED_METHODS` in
frame.ts, `RPC_ERROR_TABLE` in errors.ts) precisely so that fork touches two modules + fixtures
`[estate — a2a/src/rpc/frame.ts:10-26, a2a/src/rpc/errors.ts:12-25]`.

## Conformance — the `validateA2a` error taxonomy `[estate]`

One judging subsystem, one closed code set, one failure shape
`{ code, path, detail, parse? }` (`path` is JSON-Pointer style, `/parts/0/file`)
`[estate — a2a/src/protocol/validate.ts:11-20]`:

| Code | Meaning | Emitted by |
|---|---|---|
| `A2A_SCHEMA` | message/task/part shape defect; also unparseable JSON at decode (`parse: true`) | validate.ts / codec.ts |
| `A2A_PIN` | `protocolVersion` present but ≠ the expected pin (at `/protocolVersion`) | validate.ts:255-270 |
| `A2A_CARD` | AgentCard/skill field defect; also discovery fetch/status failures | validate.ts:180-223, wellknown.ts:39-55 |
| `A2A_RPC` | JSON-RPC envelope defect, frame parse failure, orphan correlation id | validate.ts:227-251, frame.ts:119-172 |
| `A2A_STATE` | illegal lifecycle transition — ONLY from `guardTransition`, never validate.ts | task-state.ts:44-53 |

Properties `[estate — a2a/src/protocol/validate.ts:29-44]`: **total** (no throw; even an
unforeseen exception becomes an `A2A_SCHEMA` verdict via the safety net), **batch** (every failure
collected, not first-only), `expect` explicit per artifact kind (`message · task · card ·
rpc-request · rpc-response`) with `'auto'` detection as a gates-over-mixed-artifacts convenience
only `[estate — a2a/src/protocol/validate.ts:70-77]`. `decodeA2a` composes the validator — decode
never skips judgment `[estate — a2a/src/protocol/codec.ts:10-24]`. Pin rule: only pin-BEARING
artifacts are checked (the card); bare messages/tasks are version-silent upstream — their pin is
owned by the containing artifact `[estate — a2a/src/protocol/validate.ts:261]`.

## What is deliberately NOT validated `[estate — observed in a2a/src/protocol/validate.ts]`

- **Metadata contents** — open maps at every level, never walked (extension surface by design).
- **Lifecycle legality** — a task at any KNOWN state is shape-valid; transition legality is the
  guard's job (an out-of-union state string IS caught, as `A2A_SCHEMA` at `/status/state`,
  validate.ts:170-176).
- **RPC `params`/`result` payloads** — only the envelope (`jsonrpc`, `method`, `id`,
  result-xor-error, error shape) is judged (validate.ts:227-251); per-method param shapes are
  types, not runtime checks.
- **Card optionals' internals** — `capabilities` is only checked to be an object;
  `securitySchemes`/`security`/`signatures` ride as `unknown`.
- **`Task.artifacts`** — not walked by the shipped validator (only `history` recurses,
  validate.ts:148-155).

## Conformance is gated, not aspirational `[estate]`

A standing test re-validates every committed fixture under the pin (`encodeA2a(decodeA2a(raw)) ===
raw` byte-fidelity holds because fixtures are committed in encode-canonical form — compact,
key-order-preserving, integer-like keys banned). Corpus admission reuses the same validator
(`E_REPLAY`) and pin check (`E_PIN`) — SPEC-R14/N4: a local re-implementation fails a parity test.
