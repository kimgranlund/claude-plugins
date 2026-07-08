# Dynamic lists — positional templates, no per-item key

> Axis: how a container's `children` iterates over a data array. Grounded in
> `packages/agent-ui/a2ui/src/renderer/list.ts`, `src/protocol.ts:95-104`,
> `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R6), and **ADR-0024** (the positional
> decision + its three amendments). This is the one axis where a common "best practice" (never key a
> list by index) is deliberately **reversed** — read the caveat.

## The template shape

A container's `children` is **either** a static `string[]` of component-id refs **or** a dynamic
template object `A2uiChildTemplate` (`protocol.ts:101`):

```ts
{ path: string; componentId: string }   // children as a template
```

The renderer instantiates `componentId` **once per element** of the array at `path`
(`protocol.ts:95-99`). `tree.ts` routes the object form to `list.ts`; the `string[]` form keeps the
static `#mountNode` child-walk (ADR-0024 build brief §4).

## Positional reconcile — index IS the key (ADR-0024)

**Claim — A2UI v1.0 defines NO per-item key; items match by array INDEX.** Verbatim from the spec
(via ADR-0024 Context, host-grounded from a2ui.org/specification/v1.0 + the data-binding concept
page): *"items are identified implicitly by array index, positional matching."* v1.0 has no
keyed-reconciliation concept at all.

**Caveat — this reverses the usual "never use the array index as a list key" heuristic, on
purpose.** The reasoning (ADR-0024 Decision + Alternatives): a positional list **never reorders**
(index *is* position), so the identity-preserving move that index-keying breaks in a keyed diff is
never exercised here. For v1.0 conformance the index **is** the spec-faithful key (Constraint C1 —
conform, don't add un-spec'd keying). Inventing a synthetic key (hashing an item field) was
explicitly **rejected** as non-conformant. So: do not reach for a keyed reconciler, and do not tell
a payload author to add an `id` field for keying — v1.0 grants no keying semantics.

## The vehicle: a bespoke kernel loop, NOT the `repeat` directive

`list.ts` is a `surface.scope` `effect` over a **length-computed**, not the components layer's
`repeat` directive (**vehicle B2**, user-ratified; ADR-0024 Decision):

- **length-computed** = `computed(() => Array.isArray(arr) ? arr.length : 0)` over the bound array
  (`list.ts:93-98`). The `Object.is` cutoff means a **same-length** edit (a mid-array element change)
  does **not** wake the reconcile effect — the array ref changes but the length value doesn't, so the
  effect stays asleep and the per-item bound-prop effects re-bind instead (`list.ts:11-16`).
- **grow / shrink at the boundary only** (`list.ts:135-137`): append a new instance while there are
  fewer than the length; dispose+detach the **trailing** instance while there are more (SPEC-R6 AC1).
- A **mid-array insert/remove** changes the length, so the boundary instance is added/removed and
  **every surviving instance re-binds reactively** (instance `i` re-resolves `/items/{i}`) — the DOM
  is never moved or re-created for an unaffected index (`list.ts:18-22`).

**Why not `repeat`** (ADR-0024): `repeat` exists for keyed, identity-preserving **moves** via
`moveBefore` (ADR-0022/#69) — a capability a positional list never uses. `repeat` remains the
**keyed**-list vehicle; the A2UI v1.0 list is just not a keyed list. SPEC-N5 (zero-dep) is honored
either way — B2 builds only on the `@agent-ui/components` kernel.

## Item scope: single-frame `{path, index}`, and it rewrites relative bindings both directions

Each instance is built in a **per-index child scope** with an `itemScope: { path, index }`
(`list.ts:100-104`). `scopedPointer(path, itemScope)` (`binding.ts:117`) rewrites a **relative**
binding (no leading `/`) to its absolute pointer:

- an empty relative path → `{itemScope.path}/{index}` (the item itself);
- else → `{itemScope.path}/{index}/{rest}`;
- an absolute path or absent itemScope → returned unchanged.

**Claim — read and write use the SAME rewrite, so a relative two-way binding is symmetric.** The
read side (`binding.ts:131`) and the write side (`input.ts:85`, `installInputBinding`) both route
through `scopedPointer` (ADR-0024 write-side amendment). **Failure mode before the amendment:** the
write half used the **raw** `node[value.prop].path`, so a relative `label` binding inside a list item
**read** from `/items/{i}/label` but **wrote** to the garbage key `abel` (because `setPointer` slices
the first token off a leading-slash pointer) — silent data-model corruption the moment a list item
carried an interactive input. Absolute-path bindings were always fine; the relative case was the trap.

**Single-frame, NOT a scope chain (deliberate; ADR-0024 subtree amendment + ADR-0026).** For binding
resolution the single frame composes because a **nested** list's inner `itemScope.path` is already
the fully-resolved absolute pointer (`scopedPointer('sublist', {path:'/items', index:i})` =
`/items/i/sublist`), so an inner relative `name` resolves to `/items/i/sublist/{j}/name` — the whole
collection-scope chain is baked into the pointer, no explicit chain object. A frame chain would only
be needed to address an **outer** loop's index, which v1.0's `@index` (innermost-only — see
functions-and-checks) never does. Promoting `ItemScope` to a chain is a future-protocol-version ADR,
not a v1.0 need (YAGNI).

## Item lifetime: the `(scope, ac)` pair (SPEC-N3, ADR-0024 amendment #140)

Each item owns a **per-index child scope AND a per-index `AbortController`** (`list.ts:48-52`,
`100-111`), mirroring the surface's own `(scope, ac)` pair at item granularity. `removeLast` does
both `scope.dispose()` (bound-prop effects) **and** `ac.abort()` (action + input DOM listeners)
(`list.ts:113-119`).

**Failure mode this fixed:** originally an item's action/input listeners registered on the
**surface-level** `surface.ac`, removed only at surface teardown — so a positionally-removed item
detached its DOM but its listener registration **accumulated unbounded over add/remove churn** (a
leak, not corruption). The subtree amendment promoted this from edge-case to common (every
Card-with-button row is now an item subtree). Nested lists compose for free: an inner list's teardown
carrier is owned by the outer item's child scope, so removing the outer item aborts every inner
item's ac (ADR-0024 #140 amendment).

**Teardown detail:** kernel scopes are **flat** (a child scope is not auto-disposed by its parent),
so a no-source `effect` in the parent scope carries teardown — its cleanup fires only on dispose and
disposes every still-live item scope (`list.ts:140-153`).

## What this file does NOT cover

`@index` (the system function that reads `itemScope.index`) and the function evaluator
(functions-and-checks) · the `{path}` read memo and `setPointer` internals
(bindings-and-data-model) · action/input listener wiring in general
(actions-and-two-way-input).
