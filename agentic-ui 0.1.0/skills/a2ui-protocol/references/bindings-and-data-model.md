# Bindings & the data model — the `Binding` union + reactive resolution

> Axis: how a component prop gets its value — literal, `{path}` pointer, or `{call}` function — and
> how the data model updates propagate. Grounded in
> `packages/agent-ui/a2ui/src/renderer/binding.ts`, `src/protocol.ts:83-93`, and
> `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R5, SPEC-N2). ADR-0026 adds the `{call}` arm.

## The three-armed `Binding` union

A bound prop value is one of **three** kinds (`protocol.ts:93`, `Binding<T> = T | { path: string }
| FunctionCall`):

1. **A literal** — any concrete JSON value; returned as-is, no reactive dependency.
2. **A `{path}` reference** — an RFC-6901 JSON-Pointer into the surface data model.
3. **A `{call, args?}` function-call binding** (ADR-0026) — evaluated at render time; see
   functions-and-checks for the evaluator. `args` is a **named** object, each arg itself a `Binding`
   resolved recursively.

A literal **string** is additionally a **DynamicString**: if it contains an unescaped `${…}` it is
an interpolation template, not opaque text (SPEC-R10, ADR-0027) — covered in functions-and-checks.

**Claim — the arm is chosen by SHAPE, opt-in.** `widget.ts`'s `isBinding` splits literal vs
`{path}` vs `{call}`; every literal and `{path}` path is byte-for-byte unchanged when the `{call}`
arm was added (ADR-0026 Consequences). **Failure mode before this was modeled:** a `{call,args}`
object on a string-typed prop fell to the literal branch and was applied **raw** to the DOM prop, or
raised a false `CATALOG` type-mismatch at conformance (ADR-0026 Context). If you author a payload,
a binding object must be exactly `{path}` **or** `{call,…}` — any other object shape is treated as a
literal and rendered raw.

## `updateDataModel` — upsert at a pointer (SPEC-R5)

`updateDataModel{surfaceId, path?, value?}` applies **upsert** semantics at the JSON-Pointer `path`;
with `path` omitted it replaces/merges the **whole** surface data model (SPEC-R5 AC2). The write goes
through `setPointer` (`binding.ts:67`).

**Claim — `setPointer` is IMMUTABLE with structural sharing, and this is load-bearing, not an
optimization.** It copies only the nodes **along** the written path; every untouched sibling subtree
is carried over **by reference** (`binding.ts:71-80`). **Why it matters:** an unrelated binding
re-resolves to the *same object* after a write to a different path, so the kernel's `Object.is`
cutoff keeps it asleep (SPEC-N2). **Failure mode if violated:** a `setPointer` that deep-clones would
change every subtree's reference identity on every write, waking every binding on the surface and
defeating per-path reactivity. The module header states the rule explicitly: `setPointer` must
**never deep-clone** (`binding.ts:16-17`).

## Per-path reactive waking (SPEC-N2)

There is **one** writable signal per surface (`surface.data`). Every distinct pointer is a
memoized `computed(() => resolvePointer(surface.data.value, pointer))` over it
(`binding.ts:95-106`), cached in a module-private `WeakMap<Surface, Map<pointer, signal>>`
(`binding.ts:86`).

- **The mechanism is per-path WAKING, not per-path invalidation** (`binding.ts:9-17`). A write marks
  every path-computed possibly-stale, but each one whose re-resolved value is `Object.is`-equal to
  before does **not** bump its version, so its downstream bound-prop effect concludes "unchanged" and
  skips. A `updateDataModel` to `/a` updates only the widgets bound to `/a` (SPEC-N2 AC1).
- **Each path-computed is created inside `surface.scope`** (`binding.ts:103`), so `deleteSurface`
  disposes every one and the data signal drops to zero subscribers (SPEC-N3, leak-free).
- **Reuse across widgets:** every widget reading the same pointer shares the one computed, so a data
  change drives at most one pointer-walk per distinct path (`binding.ts:88-94`).

## Pointer resolution + placeholder discipline

`resolvePointer(doc, pointer)` (`binding.ts:46`) walks an **absolute** RFC-6901 pointer, decoding
`~1`→`/` and `~0`→`~` per token (`binding.ts:39-40`). If any step is absent it returns `undefined`
— **a render-time placeholder, never an error** (SPEC-R4 AC2). The empty pointer `""` resolves to
the whole document (`binding.ts:47`).

**Caveat — a bare relative pointer resolves to `undefined` outside a list scope.** A path with no
leading `/` only resolves inside a dynamic-list item, where `scopedPointer` (`binding.ts:117`)
rewrites it to `{itemScope.path}/{index}/…` **before** the memo (so `/items/0/x` and `/items/1/x`
are distinct computeds). With no `itemScope`, `resolvePointer` returns `undefined` for it. See
dynamic-lists for the list-scope rewrite in both read and write directions.

## Pointer VALIDITY vs pointer RESOLUTION (a distinction the validator draws)

The shared validator (`validate.ts`) checks pointer **syntax**, never resolution — an undefined but
well-formed path is legal (SPEC-R4 AC2). Two rules:

- **`updateDataModel.path` is absolute-only** (`isValidPointer`, `validate.ts:236`): must be `""` or
  `/`-led; a data-model write addresses the root directly, so there is no enclosing list scope and a
  relative form is rejected.
- **A component-prop binding's `{path}` may be absolute OR list-item-relative**
  (`isValidBindingPointer`, `validate.ts:254`): any non-`/`-led string is legal (a plain identifier
  like `{path:'name'}`, or a `/`-separated chain). Both arms share the "`~` escape must be `~0`/`~1`"
  rule. **Caveat — this is deliberately lenient:** an earlier "relative path must start with a digit"
  rule flagged the shipped `/site` list pages' plain relative names (`{path:'title'}`, `{path:'items'}`)
  as POINTER-invalid even though the renderer resolved them fine at runtime (`validate.ts:248-252`).
  The validity rule was widened to match the shipped resolver, not the resolver narrowed.

## What this file does NOT cover

The `{call}` evaluator, `@index`, DynamicString `${…}` interpolation, and `checks`
(functions-and-checks) · dynamic-list templates and the relative-path rewrite mechanics
(dynamic-lists) · how a bound value flows back on user input (actions-and-two-way-input).
