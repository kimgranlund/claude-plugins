# Message lifecycle — surface create/update/delete + progressive render

> Axis: the server→client message stream and how the renderer turns it into a live surface.
> Grounded in `packages/agent-ui/a2ui/src/renderer/{dispatch,surface,tree,parser}.ts`,
> `src/protocol.ts`, and `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R1–R4).
> A2UI is Google's Apache-2.0 protocol (a2ui.org); `@agent-ui/a2ui` is this repo's
> zero-dependency native renderer for it (no Lit/`web_core` — SPEC-N5).

## The stream shape

An A2UI payload is a **JSONL stream**: one JSON envelope per line, applied in **arrival order**
(SPEC-R1). Every envelope carries a top-level `version` string plus exactly **one** message-kind key.
The six server→client kinds are the closed set in `dispatch.ts:36` (`DISPATCHED_ENVELOPE_KEYS`) and
mirrored in `validate.ts:42` (`MESSAGE_KINDS`):

| envelope key | body | effect |
|---|---|---|
| `createSurface` | `{surfaceId, catalogId, surfaceProperties?, theme?, sendDataModel?}` — the two optional style fields are worked-instance tolerances only: upstream v1.0-RC removed `surfaceProperties` and the v0.9.1 machine schema defines neither (SPEC-R7 re-sync 2026-08-05; the drop is ruled, agent-ui GH #477) | stand up a surface |
| `updateComponents` | `{surfaceId, components: A2uiComponent[]}` | buffer/patch the component tree |
| `updateDataModel` | `{surfaceId, path?, value?}` | upsert the data model (see bindings-and-data-model) |
| `deleteSurface` | `{surfaceId}` | release the surface |
| `actionResponse` | `{surfaceId, actionId, value?, error?}` | correlate a server reply (see actions-and-two-way-input) |
| `callFunction` | `{functionCallId, wantResponse?, callFunction}` | server-initiated RPC (see functions-and-checks) |

**Caveat — `callFunction` is envelope-level, not surface-scoped.** Its `functionCallId` is a
**top-level sibling** of `callFunction`, not nested in a body, and it carries **no `surfaceId`**
(`protocol.ts:149-150`, `dispatch.ts:102-107`). Every other kind's identifying fields live inside
its body. A validator or parser that assumes "all fields are in `msg[kind]`" mis-reads it — this is
why `validate.ts:142` checks `functionCallId` against `msg`, not `body`.

## Dispatch: version gate, then a pure switch

`dispatch(msg, handlers)` (`dispatch.ts:72`) does exactly two things, in order:

1. **Version gate** (SPEC-R13): if `msg.version` is not in `SUPPORTED_VERSIONS`
   (`protocol.ts:160` = `{'v1.0','v0.9.1'}`), it returns a `VERSION_UNSUPPORTED` error and the
   message never reaches a handler. See errors-and-versioning.
2. **Envelope-key routing**: an `in`-narrowed switch to the matching handler; no known key →
   a `SCHEMA` error (`dispatch.ts:110-111`).

**Claim — dispatch is side-effect-free and does NOT re-validate body shape.** It returns an
`A2uiError` rather than emitting one; the host emits it and skips the message (`dispatch.ts:14-15`).
Body-shape validation is `validate.ts`'s SCHEMA stage, deliberately kept separate so dispatch stays
a trivially testable pure switch (`dispatch.ts:8-9`). **Failure mode this prevents:** the
`DISPATCHED_ENVELOPE_KEYS` / `MESSAGE_KINDS` drift bug (ADR-0055 §1.2) — `callFunction` was routed by
dispatch but unrecognized by the validator, so a spec-legal stream was called SCHEMA-invalid. A
`dispatch.test.ts` parity probe now asserts the two lists are equal; keep them in lockstep.

## Surface lifecycle (SPEC-R2)

`createSurface` builds a `Surface` (`surface.ts:40`) keyed by `surfaceId`, bound to one `catalogId`,
with **one ownership scope** (`createScope()`) + **one `AbortController`** — mirroring `UIElement`'s
lifetime discipline. The data model is a single `signal` (`surface.ts:26`); every binding effect is
created inside `scope`, so one `scope.dispose()` provably unsubscribes them all.

- **`SurfaceStore.create` disposes a pre-existing surface with the same id first** (`surface.ts:75`)
  — recreating a surface never leaks the old one.
- **`deleteSurface` releases everything**: `disposeSurface` calls `scope.dispose()` (→ 0 signal
  subscribers) **and** `ac.abort()` (→ 0 DOM listeners) (`surface.ts:61-64`). This is the leak-free
  teardown invariant SPEC-N3, provable via the kernel's `inspect()`.
- **Unknown `catalogId` is rejected before create** (SPEC-R2 AC3): the renderer host resolves
  `catalogId` against the registry and emits `CATALOG_UNKNOWN` **upstream** of `createSurface`
  (`surface.ts:8-10`) — an unknown-catalog surface is never stood up.

## Component tree: buffer, reconstruct, render-on-root (SPEC-R3/R4)

Components arrive as a **flat adjacency list** — each `A2uiComponent` (`protocol.ts:107`) has an
`id`, a `component` type string, an optional `child` (one id) or `children` (id array **or** a
dynamic-list template — see dynamic-lists), and arbitrary props. `updateComponents` buffers them by
`id` and reconstructs the tree via those references.

- **Render begins as soon as a valid `root` exists** — there is no explicit "begin" signal
  (SPEC-R3). Exactly **one** `root` per surface; a second `root` delivery is an `IDGRAPH` error and
  does **not** replace the existing root (SPEC-R3 AC2).
- **Out-of-order / incomplete tolerance is a MUST, not a nicety** (SPEC-R4): a `child`/`children` id
  not yet delivered, or a binding `path` not yet in the data model, is **held and patched in later**
  — never an error, never a teardown. An undefined binding renders an empty/placeholder value, not
  an error (SPEC-R4 AC2). **Caveat:** `surface.components` is a plain (non-reactive) `Map`, so a
  template/descendant arriving *after* its container mounts is a known deferred edge — it renders
  nothing until a length change re-pokes the list (ADR-0024 subtree amendment, "Out of scope").

## Fault isolation is a hard invariant (SPEC-N4)

One malformed line, one unknown component type, or one bad binding **MUST NOT** tear down the
surface or stop the stream. A malformed line emits `PARSE` and continues to the next
(SPEC-R1 AC2); an unknown component type emits `CATALOG` and renders a non-fatal placeholder while
the rest of the tree renders (SPEC-R9 AC2). This "emit + placeholder + continue" discipline is the
same one every error path in this protocol follows — see errors-and-versioning.

## What this file does NOT cover

Binding resolution and the data model (bindings-and-data-model) · dynamic list templates
(dynamic-lists) · actions, `actionResponse` correlation, two-way input
(actions-and-two-way-input) · function evaluation, `checks`, `callFunction` (functions-and-checks) ·
the error taxonomy and version rejection detail (errors-and-versioning).
