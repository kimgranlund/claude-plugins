# Errors & versioning — the two-code wire contract + the version pin

> Axis: the internal 10-code diagnostic taxonomy, its map to the v1.0 two-code wire contract, and
> protocol-version handling. Grounded in `packages/agent-ui/a2ui/src/protocol.ts:9-74`,
> `src/renderer/validate.ts` (symbols `ErrorCode`, `toWireError`; cite by symbol, line numbers drift), and **ADR-0031** (error-vocab reconciliation). SPEC-R11/R13, SPEC-N6.

## Two vocabularies: internal (rich) vs wire (two codes)

**Claim — A2UI v1.0 defines EXACTLY TWO renderer→agent error codes, and governs ONLY the wire; the
repo keeps a richer INTERNAL taxonomy** (ADR-0031 fact 1, verbatim from a2ui.org v1.0: *"the spec
defines only WIRE-level error messages; INTERNAL validation is NOT part of the protocol
specification"*). So the internal codes are legitimately the repo's own.

- **Internal `ErrorCode`** (10 codes, the `ErrorCode` union in `protocol.ts`): `PARSE`, `SCHEMA`, `CATALOG`,
  `CATALOG_UNKNOWN`, `IDGRAPH`, `POINTER`, `VERSION_UNSUPPORTED`, `FUNCTION`, `DEPTH_EXCEEDED`,
  `CONTAINMENT` (the last two were added after the original 8; a doc comment near `toWireError`
  may still say "9 codes", trust the union). Used by the renderer,
  the validator's `Failure`, and corpus admission — a corpus record's admission distinguishes a
  `SCHEMA` from an `IDGRAPH` failure, so collapsing the codes would gut that diagnostic
  (`protocol.ts:12-14`).
- **Wire `WireErrorCode`** (2 codes, `protocol.ts:44`): `VALIDATION_FAILED` | `INVALID_FUNCTION_CALL`.

**The contextID is TIED to the code, not a free XOR** (`protocol.ts:53-55`, ADR-0031 fact 2):
`VALIDATION_FAILED` **requires `surfaceId`** (excludes `functionCallId`); `INVALID_FUNCTION_CALL`
**requires `functionCallId`** (excludes `surfaceId`). **There is NO `path` field on the wire** — the
v1.0 wire shape is exactly `{code, message, surfaceId ⊕ functionCallId}`.

## The map at ONE boundary (`toWireError`, ADR-0031 Fork B)

`toWireError(e)` (`protocol.ts:67`) maps an internal `A2uiError` to the wire shape at the **single**
`renderer.ts #emit` chokepoint — the validator and corpus never see the map (`protocol.ts:58-59`,
ADR-0031 clause 5).

- **All 10 internal codes → `VALIDATION_FAILED` + `surfaceId` this wave** (`protocol.ts:70-73`,
  ADR-0031 clause 2). Including `FUNCTION`: a render-time binding-evaluation failure (`@index` misuse,
  an unknown/throwing catalog function *referenced in a binding*) is a **message-validation** failure,
  exactly parallel to `CATALOG` — **not** the spec's `INVALID_FUNCTION_CALL`, which is an
  agent-initiated call rejection.
- **A present `path` is FOLDED into `message`** (`"… (at <path>)"`, `protocol.ts:69`) so the locus
  survives for the agent, then dropped — the wire has no `path` field (ADR-0031 clause 4).

**Caveat — `INVALID_FUNCTION_CALL` is modeled but reached from ONE place only.** `toWireError` never
emits it (`protocol.ts:66`); it is emitted **directly** (bypassing `toWireError`) by the
agent-initiated `callRendererFunction` RPC handler, which carries a `functionCallId`, not a `surfaceId`
(`protocol.ts:238-241`; ADR-0034 activates ADR-0031's reserved arm). So: a **binding-eval** function
error is `VALIDATION_FAILED`; only an **agent `callRendererFunction`** rejection is `INVALID_FUNCTION_CALL`.
Conflating them mis-maps the wire code (a binding-eval failure would emit the agent-only
`INVALID_FUNCTION_CALL`) — ADR-0031 rejected the "`FUNCTION` → `INVALID_FUNCTION_CALL`, use `node.id`
as `functionCallId`" lean precisely because `node.id` is not a call id and render-time errors are not
agent-initiated.

## The stage→code map (validator, `validate.ts`)

The shared validator's pipeline (`validate.ts:6-16`) — MIME/shape → schema (per version) →
catalog-conformance → id-graph → JSON-pointer validity — assigns:

| stage / defect | internal code |
|---|---|
| raw-string parse fail | `PARSE` |
| not object/array, bad envelope, missing/typed-wrong field | `SCHEMA` |
| version not in the pinned set | `VERSION_UNSUPPORTED` |
| unknown component type / prop / type mismatch | `CATALOG` |
| missing `root`, second `root`, cycle, dangling ref | `IDGRAPH` |
| malformed JSON-Pointer in a binding / data path | `POINTER` |

**Claim — `validateA2ui` is the ONE shared implementation, pure and TOTAL** (`validate.ts:47`,
SPEC-N6): it is total — a safety net converts any unforeseen input to a `SCHEMA` verdict rather than
throwing (`validate.ts:48-53`) — and it is imported by **both** the renderer and corpus admission so both return
the identical verdict (parity is itself a standing test). **Failure mode a forked validator would
cause:** the renderer and the corpus gate disagreeing on whether a payload is valid — SPEC-N6 exists
to forbid exactly that.

**Caveat — id-graph is a FINALIZE-granularity judgment, not per-message.** Missing-root and dangling
refs are legal *transient* states mid-stream (SPEC-R4), so the host must call `validate` at finalize
granularity, never per incremental `updateComponents` (`validate.ts:18-23`, `182-189`). A second
`root` and a cycle are always invalid. The corpus passes a complete `a2uiOutput`, so both callers
judge the same set → identical verdict.

## Versioning (SPEC-R13)

**Claim — the supported set is pinned and SHARED.** `SUPPORTED_VERSIONS`
(in `protocol.ts`, cite by symbol = `{'v1.0', 'v0.9.1'}`) is the single source imported by both the dispatch router
(`dispatch.ts:76`) and the validator (`validate.ts:24`, `109`), so the two can't drift on which
versions are routable (SPEC-N6). Every inbound message's `version` is gated against it.

- **An unsupported version → `VERSION_UNSUPPORTED`, message skipped** (SPEC-R13 AC2;
  `dispatch.ts:76-78`) — it never reaches a handler. On the wire this maps to `VALIDATION_FAILED`
  (the two-code enum offers no "capability" bucket — ADR-0031 records it as a forced mapping, as with
  `CATALOG_UNKNOWN`).
- **Version drives semantics** (SPEC-R13 AC1): the `version` is threaded to each handler so it can
  apply version-specific semantics (`dispatch.ts:48-49`). **Correction (2026-08-05, SPEC-R7 re-sync,
  agent-ui's `a2ui-ecosystem-alignment.spec.md`):** this line previously claimed "v1.0 uses
  `surfaceProperties`; v0.9.x uses `theme`" — STALE against upstream. Upstream's v1.0-RC **removed
  `surfaceProperties` entirely** ("Decoupled Branding"), and the v0.9.1 machine schema
  (`specification/v0_9_1/json/common_types.json`, a2ui-project/a2ui@main, fetched 2026-08-04/05)
  defines neither field. **Update 2026-10-03:** the worked instance has since DROPPED the field:
  its `A2uiCreateSurface` type has no `surfaceProperties` and the renderer reads none (the drop
  was ruled, agent-ui GH #477, 2026-08-06). Do not claim tolerant inbound handling; the code
  does not show it. [verified] 2026-10-03.

**Caveat, versioning here is a defect-shaped concern, not a full migration story.** The pack answers
"which versions are accepted and what happens to an unsupported one," not "how do I migrate a v0.9
payload to v1.0" — no transform layer exists; an out-of-set version is simply rejected.

## Depth cap and containment are validate-time failures (2026-10-03)

**Claim, render depth and region (Card anatomy) rules are structural checks the validator
reports, not render-time surprises.** A render depth cap (`MAX_RENDER_DEPTH = 64`) yields
`DEPTH_EXCEEDED`; Card region rules (`checkContainment` in `renderer/validate.ts`) yield
`CONTAINMENT`. Both map to `VALIDATION_FAILED` at `toWireError` like every other internal code.
**Failure mode:** a payload that nests past the cap or breaks the Card region contract is rejected
whole at validate time, so a producer's self-correct loop can see and fix it before anything
paints. [verified] agent-ui `protocol.ts` (`MAX_RENDER_DEPTH`), `renderer/validate.ts`, 2026-10-03.

## Wire tolerances are a registry, not ad-hoc branches (2026-10-03)

**Claim, every accepted-but-non-spec shape (a Postel-style leniency, a narrowing, a
harness-only allowance) must be a registered row with an owner.** A renderer that grows
tolerances as scattered `if` branches loses the answer to "what do we accept that the spec does not
define, and who decided"; keep one registry (agent-ui: `references/wire-tolerances.md`, ADR-0169
cl.10) so tolerance never grows unrecorded. **Failure mode:** an unregistered leniency becomes an
accidental contract that a second renderer or a producer then depends on. [verified] 2026-10-03.

## What this file does NOT cover

Where each error is produced (message-lifecycle for `PARSE`/`SCHEMA`/`IDGRAPH`; functions-and-checks
for `FUNCTION`/`INVALID_FUNCTION_CALL`; bindings-and-data-model for `POINTER`) · the `callRendererFunction`
rejection triggers in full (functions-and-checks) · corpus admission's use of the internal codes
(that is the corpus subsystem, routed to a2ui-training-facts once it exists — not this pack).
