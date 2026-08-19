# Message lifecycle — surface create/update/delete + progressive render

> Axis: the agent→renderer message stream and how the renderer turns it into a live surface.
> Grounded in `packages/agent-ui/a2ui/src/renderer/{dispatch,surface,tree,parser}.ts`,
> `src/protocol.ts`, and `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R1–R4).
> A2UI is Google's Apache-2.0 protocol (a2ui.org); `@agent-ui/a2ui` is this repo's
> zero-dependency native renderer for it (no Lit/`web_core` — SPEC-N5).

## The stream shape

An A2UI payload is a **JSONL stream**: one JSON envelope per line, applied in **arrival order**
(SPEC-R1). Every envelope carries a top-level `version` string plus exactly **one** message-kind key.
The six agent→renderer kinds are the closed set in `dispatch.ts:36` (`DISPATCHED_ENVELOPE_KEYS`) and
mirrored in `validate.ts:42` (`MESSAGE_KINDS`):

| envelope key | body | effect |
|---|---|---|
| `createSurface` | `{surfaceId, catalogId, surfaceProperties?, theme?, sendDataModel?}` — the two optional style fields are worked-instance tolerances only: upstream v1.0-RC removed `surfaceProperties` and the v0.9.1 machine schema defines neither (SPEC-R7 re-sync 2026-08-05; the drop is ruled, agent-ui GH #477) | stand up a surface |
| `updateComponents` | `{surfaceId, components: A2uiComponent[]}` | buffer/patch the component tree |
| `updateDataModel` | `{surfaceId, path?, value?}` | upsert the data model (see bindings-and-data-model) |
| `deleteSurface` | `{surfaceId}` | release the surface |
| `actionResponse` | `{surfaceId, actionId, value?, error?}` | correlate an agent reply (see actions-and-two-way-input) |
| `callRendererFunction` | `{functionCallId, wantResponse?, callRendererFunction}` | agent-initiated RPC (see functions-and-checks) — Candidate splits this by direction; the mirror `callAgentFunction`/`agentFunctionResponse` (renderer calling a function that executes on the agent) is a new capability this pack does not yet document |

**Caveat — `callRendererFunction` is envelope-level, not surface-scoped.** Its `functionCallId` is a
**top-level sibling** of `callRendererFunction`, not nested in a body, and it carries **no `surfaceId`**
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
`DISPATCHED_ENVELOPE_KEYS` / `MESSAGE_KINDS` drift bug (ADR-0055 §1.2) — `callRendererFunction` was routed by
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

---

## UPDATE 2026-08-19 — surface lifecycle as producer CONDUCT: root-once, scene swaps, slot retirement

**[verified]** 2026-08-19 against the shipped producer grammar
(`packages/agent-ui/a2ui/src/agent/prompts/grammar.md`, byte-pinned), `renderer/validate.ts`'s
`checkContainment`, ADR-0198's ratified 2026-08-18 amendment (B1), and the field wave
PR #1326 / GH #1262. The renderer facts above (one root, IDGRAPH on a second delivery) have
hardened into producer LAWS, and grammar.md adds the whole-record replacement rule the renderer
never states — answer payload-lifecycle asks from these, not just from the renderer's tolerance:

- **Root-once / root-immutability.** `id:"root"` is delivered ONCE per surface; resending it is an
  id-graph error that **silently keeps the OLD root, never your change** (the SPEC-R3 AC2 fact
  above, stated as the failure a producer actually experiences). The conduct: give root one stable
  wrapper child up front and put every growing container under ITS OWN id one level down — never
  root itself (grammar.md's root-immutability rule).
- **Scene swaps are whole-container resends, never appends.** Resending an id REPLACES its ENTIRE
  record — every prop still wanted plus the FULL children list; there is no partial-prop patch
  (grammar.md's output rules — a producer law the renderer's buffer-by-id merge realizes but never
  states). A continuing flow (wizard step, game round, dashboard refresh) REUSES its surface: the
  producer swaps the scene container's children with one `updateComponents` on the SAME
  `surfaceId`, resends ONLY the changed subtree, and reserves `createSurface` for a genuinely
  PARALLEL artifact (grammar.md's surface-reuse law; ADR-0198 amendment B1 rules mid-flow Next/Back
  as exactly this — scene transitions, with draft state under a `/draft/*` data-model prefix
  surviving each swap; the ask-freeze half of that same B1 law — WHEN the answered-ask freeze
  begins — lives with [[a2ui-chat-agent-facts]]'s flow-completion section).
- **The wire has no node-delete verb — retiring a slot needs a referenced-but-EMPTY node.**
  `updateComponents` only upserts; a node dropped from a parent's `children` still sits in the
  merged component set. For a Card region that matters concretely: `checkContainment`
  (`validate.ts:332`) fails ANY `CardHeader`/`CardContent`/`CardFooter` whose parent in the merged
  set is not a `Card` — an UNREFERENCED region counts as parentless and fails `CONTAINMENT` too. So
  "remove the footer's buttons" is a resend of the footer with its children emptied — the
  CONTAINMENT-safe empty node — never dropping the footer id from the Card (the worked instance:
  PR #1326's "CONTAINMENT-safe empty footer on its summary scene").

## UPDATE 2026-08-19 — card anatomy as conduct (the P9 wave)

**[verified]** 2026-08-19 against grammar.md's card-anatomy clause, Kim's 2026-08-18 ruling
(PR #1342), and the GH #1262 rubric fold + PR #1326 repair wave — the anatomy is graded corpus
doctrine (rubric dimension P9), not style advice:

- **`CardFooter` is THE action row.** Every action `Button` rides it — one solid primary, at most
  one ghost secondary — never scattered loose in `CardContent` (the field instance that minted P9:
  `frontier-image-hero-card`'s View-listing Button sat in CardContent with no footer and the record
  FAILED its re-judge, GH #1262).
- **Identity titles ride `CardHeader`, never `CardContent`** (Kim's ruling, one grammar sentence +
  a 7-record convergence sweep, PR #1342). A single-fact card may omit the header entirely —
  nothing requires all three regions.
- **A gated card is FormProvider-as-root, Card-non-root.** Two constraints compose: the
  `FormProvider` submit gate blocks only `submit:true` actions among its DESCENDANTS, and the Card's
  regions must be the Card's DIRECT children (`CONTAINMENT` above — `ui-card`'s region CSS assumes
  the same). A FormProvider wrapped around the fields only, sitting BESIDE the footer that holds the
  submit Button, leaves the gate inert — the button submits regardless of validity. The repaired
  shape is `FormProvider > Card > (CardHeader · CardContent · CardFooter)`; PR #1326's wave
  converted the gated records to exactly this ("FormProvider-as-root/Card-non-root … gating
  verified preserved"), and the seed family is named after it (PR #1342).

## What this file does NOT cover

Binding resolution and the data model (bindings-and-data-model) · dynamic list templates
(dynamic-lists) · actions, `actionResponse` correlation, two-way input
(actions-and-two-way-input) · function evaluation, `checks`, `callRendererFunction` (functions-and-checks) ·
the error taxonomy and version rejection detail (errors-and-versioning) · WHERE the producer
grammar teaching itself lives — grammar clause vs mini-skill vs exemplar
([[a2ui-training-facts]]'s teaching-lane rubric; the live agent's prompt composition is
[[a2ui-chat-agent-facts]]).
