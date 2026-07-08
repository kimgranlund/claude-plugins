# Actions & two-way input — the client→server round-trip

> Axis: how a user interaction becomes an `action` message, how `actionResponse` correlates back,
> and how an input widget writes its value into the data model. Grounded in
> `packages/agent-ui/a2ui/src/renderer/{action,input}.ts`, `src/protocol.ts:166-182`,
> `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R7, SPEC-R8). ADR-0011 = the action-prop
> shape; ADR-0019 = the input `value` mark.

## The `action` message (SPEC-R8)

On a triggered action the renderer emits an `action` client→server envelope
(`protocol.ts:167-182`, `A2uiAction`):

```ts
{ surfaceId, actionId, name, sourceComponentId, timestamp,
  context: Record<string, unknown>, wantResponse?, dataModel? }
```

Built by `ActionDispatcher.emitAction` (`action.ts:85`):

- **`actionId` is client-generated and globally unique** (a v1.0 requirement, SPEC-R8) — via an
  **injected** `newId()` provider, never ambient `Math.random()` (`action.ts:26-33`). Likewise
  `timestamp` comes from an injected `now()`. **Why:** determinism — tests pin a fake id/clock and
  assert an exact message shape + round-trip (`action.ts:9-11`).
- **`wantResponse: true`** is emitted only when a reply is expected; the dispatcher registers a
  correlation slot keyed by `actionId` **before** emitting, so even a synchronous response
  correlates (`action.ts:100-106`).
- **`dataModel` is attached only when `surface.sendDataModel` was set** on `createSurface`
  (SPEC-R8 AC2), and is **peeked untracked** so building the message never subscribes to the data
  signal (`action.ts:97-98`).

**Caveat — `context` is collected upstream, not by the dispatcher.** `action.ts` assembles the
message and owns the correlation map; the `context` (resolved bound paths + input values) is
collected by the host/widget (`collectContext`, LLD-C9) and handed in via `opts.context`, defaulting
to `{}` (`action.ts:16-18`, `36`). List-item **relative-path** context resolution through `itemScope`
is a separately-tracked concern (ADR-0024 #140, "action *context* … is a SEPARATE concern") — the
listener-lifetime fix landed, but relative-context resolution in `collectContext` was not part of it.

## `actionResponse` correlation (SPEC-R8 AC1)

An inbound `actionResponse{surfaceId, actionId, value?, error?}` (`protocol.ts:136-141`) is matched
back by `actionResponse` (`action.ts:116`):

- found slot → **reject with `error` if present, else resolve with `value`**; the slot is removed
  either way (`action.ts:122-125`).
- **unknown `actionId` → dropped with a logged warning, never thrown** (`action.ts:117-120`) — a late
  or duplicate response is inert, not fatal.

## Two-way input binding (SPEC-R7) — the ONE `value: {prop, event}` mark

An input widget (TextField, Select, Slider, …) **displays** the bound value, **updates the local
data model optimistically** on user input, and **surfaces the current value in the action context**
on commit (SPEC-R7 AC1). The write side is `installInputBinding` (`input.ts:71`), a **single generic
controller** — every branch is driven by the catalog factory mark + the node binding, **never** by a
component name (`input.ts:6-9`).

**Claim — a component gets exactly ONE two-way `value` mark** (ADR-0019/0053 F4). The catalog's
`WidgetFactory` carries `value: { prop, event }`; `value.prop` names **both** the A2UI node prop that
carries the bind (`node[prop]` → the `{path}` writeback target) **and** the DOM value property read
off the control on commit (`el[prop]`) (`input.ts:33-37`). **Failure mode / caveat:** a control
needing two committed values (e.g. a dual-thumb slider) **cannot** get a two-way mark for both — one
binds two-way, the rest bind one-way read-only `{path}`. If a control's commit/value shape can't be
expressed by `{prop, event}`, that is a **catalog SPEC gap**: the renderer honours exactly one
`{prop, event}` mark and cannot express a second, so the fix lives in the catalog SPEC, not the
renderer (`input.ts:35-37`).

## Opt-in, optimistic, leak-free — the three load-bearing properties

`installInputBinding` is a no-op unless **both** hold (`input.ts:79-83`):

1. **the factory marks a `value`** (a non-input control like `ui-button` has none → no listener), AND
2. **the node's `value.prop` is a `{path}` binding, not a literal** — a literal has no writeback
   target, so two-way binding is vacuous. The controller never installs a listener it can't honour.

On commit it writes the control's current `value.prop` into `surface.data` via the structural-sharing
`setPointer` (`input.ts:92`), so per-path waking holds (SPEC-N2) — a sibling field's bound-prop
effect stays asleep. The write is **optimistic and synchronous**: the new value lands in
`surface.data` immediately, so a subsequent action's `collectContext` reads it straight off the data
model — input feeds action with no extra wiring (`input.ts:19-25`).

**Leak-free (SPEC-N3):** the listener is registered with an `AbortController` signal — `surface.ac`
for a static node, or a **per-item** ac for a list item (`input.ts:71-77`, `86-98`). Either abort
removes it; a late commit after teardown is inert. See dynamic-lists for the per-item ac.

**Caveat — a relative two-way binding with no `itemScope` writes to a garbage key**, exactly as it
reads to `undefined`. This is a pre-existing, strictly-out-of-scope asymmetry for a malformed input
outside any list (ADR-0024 write-side amendment, "Out of scope") — inside a list the `itemScope`
rewrite makes read and write symmetric.

## `wantResponse` is wired end-to-end but not used for routing (a design seam, not a shipped feature)

The action envelope carries `wantResponse` from control → renderer → client message, but in the
shipped live-agent demo **every** client message triggers a full turn regardless. Routing on
`wantResponse` (true → visible dialog; false/absent → silent data update) is a **proposed** design,
not implemented — that belongs to the conversational-agent layer, not this protocol pack. Treat
`wantResponse` here as: emitted correctly, correlated correctly, and available to a consumer who
chooses to route on it.

## What this file does NOT cover

Function-call bindings, `checks`, and the server-initiated `callFunction` RPC
(functions-and-checks) · the `{path}` read memo and `setPointer` (bindings-and-data-model) · list
item scope and per-item lifetime (dynamic-lists) · the wire error shape of an `actionResponse.error`
(errors-and-versioning).
