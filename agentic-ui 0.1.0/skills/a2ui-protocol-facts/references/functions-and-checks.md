# Functions & checks — client-side evaluation vs server-initiated RPC

> Axis: the two DISTINCT function surfaces (local binding-eval vs the server `callFunction` RPC),
> `${…}` DynamicString interpolation, and the `checks` inline-validation construct. Grounded in
> `packages/agent-ui/a2ui/src/renderer/{functions,interpolate,fn-expr,checks,call-function}.ts` and
> `.claude/docs/specs/specs/a2ui-runtime.spec.md` (SPEC-R10, SPEC-R14). ADR-0026 = function-call
> bindings + `@index`; ADR-0027/0028 = `${…}`; ADR-0029 = `checks`; ADR-0034 = `callFunction`.

## The load-bearing distinction: two surfaces, one registry

There are **two spec-distinct function surfaces** (ADR-0034 fact 6, verbatim from a2ui.org v1.0):

- **Client-side binding evaluation** — a `{call}` in a binding, DynamicString, or `checks`, *"invoked
  locally during component rendering — no network round-trip."* Reactive, surface-scoped, args
  resolved recursively as bindings. Owned by `functions.ts` `evaluate`.
- **Server-initiated `callFunction` RPC** — *"an envelope-level message requiring `functionCallId`
  tracking, bidirectional RPC."* Flat, surfaceless, args are concrete literals. Owned by
  `call-function.ts` `handleCallFunction`.

**Claim — they share the function REGISTRY, not the dispatch, and MUST NOT be merged**
(`call-function.ts:2-13`). Both read the same `catalog.functions` metadata + `catalogFunctions` pure
impls (ADR-0026's registry). But `evaluate` does `@`-system dispatch + recursive `resolveValue`;
`handleCallFunction` does a flat gated call with concrete args and zero surface coupling. **Failure
mode a maintainer must avoid:** routing one through the other — e.g. resolving `callFunction` args via
`resolveValue` (there is no surface/data-model to resolve a `{path}` against — ADR-0034 fork 1) or
giving `evaluate` a `callableFrom` gate (a local binding is the client surface, always allowed).

## Client-side `evaluate` (ADR-0026, LLD-C10)

`resolveValue(value, surface, itemScope?, emitError, registry)` (`functions.ts:67`) is the single
dispatcher `widget.ts`'s bound-prop effect calls for every dynamic prop, with four cases
(`functions.ts:74-81`): `{call}` → `evaluate`; `{path}` → `resolve` (the per-path memo); a template
string → `interpolate`; any other literal → as-is. `evaluate` (`functions.ts:94`) dispatches on the
call name's namespace and resolves each **named** arg recursively **before** the body runs, so a
`{path}` arg propagates reactivity through the call (`functions.ts:104-108`).

### SYSTEM functions: `@index` is the only one in v1.0, innermost-only

`@`-prefixed names hit the system table (`functions.ts:111`, `117`). v1.0 defines **exactly one**:
`@index` returns `itemScope.index + (args.offset ?? 0)` (`functions.ts:125-138`).

**Claim — `@index` is INNERMOST-ONLY and `offset` is a numeric addend, NOT outer-scope addressing**
(ADR-0026 fact 4, verbatim: *"MUST ONLY be available when evaluating template items within a list
rendering context (Collection Scope); outside iteration the client MUST treat it as an error"*).
`offset` is for 1-based display (`{call:'@index', args:{offset:1}}` → index+1), not ancestor
addressing (`functions.ts:135-137`). **Failure mode:** `@index` outside a list → `FUNCTION` error +
`undefined` (`functions.ts:127-133`). This settles the ADR-0024 deferral: single-frame `ItemScope`
is sufficient, no scope chain — see dynamic-lists.

### CATALOG functions: declared in the bound catalog, impl in the shared table

A non-`@` name is looked up in the bound catalog's `functions` map (existence gate,
`functions.ts:160-168`) **and** the pure impl in `catalogFunctions` (`functions.ts:173`). The default
catalog ships exactly three — `required`, `email`, `regex` (pure validators; `functions.ts:23-26`).

**Caveat — a from-scratch payload will `FUNCTION`-error on functions the default catalog doesn't
ship.** `now`, `formatDate`, `and`/`or`/`not`, `formatString` are NOT in the default catalog — a
project catalog may register them (the registry is open), but against the default they emit
`FUNCTION` + `undefined`, conformantly (ADR-0026 Consequences; ADR-0029 §1). String composition is
**not** a `formatString` function — it's `${…}` interpolation (below), which supersedes the earlier
planned `formatString` (ADR-0026 fact 6).

### FUNCTION errors never throw

Unknown system name, unknown catalog function, declared-but-unimplemented, or a **throwing** impl all
→ `emitError({code:'FUNCTION'})` + `undefined` (`functions.ts:140-193`). Non-fatal, sibling props and
widgets unaffected (SPEC-N4). On the wire, `FUNCTION` maps to `VALIDATION_FAILED` — see
errors-and-versioning.

## DynamicString `${…}` interpolation (ADR-0027/0028)

Any bindable **string** containing an unescaped `${…}` is a template (`interpolate.ts:92`,
`isInterpolated` gate at `functions.ts:79`). A single escape-aware scan splits it into segments
(`interpolate.ts:108-167`); each `${expr}` body is classified (`interpolate.ts:16-22`):

- **no `(`** → a JSON-Pointer path (absolute `${/user/name}` or relative `${name}` in item scope),
  resolved through the same per-path memo as `{path}` (`interpolate.ts:154-160`).
- **has `(`** → a **function-expression** `${fn(arg:value,…)}` (ADR-0028): parsed by
  `parseFunctionExpr` into a `FunctionCall`, then routed through the **same** `evaluate`
  (`interpolate.ts:144-153`) — no second evaluator.

**Coercion is spec-exact** (`interpolate.ts:73-78`, SPEC-R10 table): number/boolean → `String(v)`;
`null`/`undefined` → `""` (empty sentinel, **not** the literal `"null"`); object/array →
`JSON.stringify`; string → itself. **Caveats:** the only defined escape is `\${` (→ literal `${`);
`\\` is not un-escaped (spec-silent, documented limitation, `interpolate.ts:35-38`). A **malformed**
or unterminated `${…}`, or a positional-arg function-expression, renders **literally with no error**
(`interpolate.ts:141-153`, ADR-0027 render-literally model) — consistent with SPEC-N4 placeholder
discipline. Reactivity is free: `interpolate` runs inside the bound-prop effect, so each embedded
`${/path}` wakes it per-path (SPEC-N2).

## `checks` — client-side inline validation, NO server error (ADR-0029)

A component-level `checks` array runs each entry's `{call,args}` through the **same** `evaluate` and
drives the control's validity/disabled state — entirely client-side (`checks.ts:1-6`).

**Claim — a failed check emits NO server error, ever** (ADR-0029 fact 4, verbatim: *"Servers never
receive notifications of failed checks unless explicitly included in an action's context"*).
`VALIDATION_FAILED` is the **schema**-validation wire code, **not** a form-validation channel
(SPEC-R10; ADR-0029 §4). This is the sharp line for a "why did validation not reach my server"
question: a check failure is UI-only.

Mechanics:

- **`checks` is a RESERVED component-level key, never a bindable prop** (`checks.ts` + `validate.ts`
  `RESERVED`, ADR-0029 §2). **Caveat:** per-component *declaration* of which components accept
  `checks` is **deferred** — the catalog loader requires `mapsTo` on every property, so there's no
  `mapsTo`-less marker yet; a `checks` on a non-input, non-Button component is accepted structurally
  and the controller **no-ops** on it (ADR-0029 Consequences).
- **Two wire shapes, Postel-read** (`checks.ts:51-80`): flat `{call,args?,message}` (canonical,
  TextField) and `condition`-wrapped `{condition:{call,args},message}` (Button). Both normalize to one
  internal `Check`. The unwrap keys on the `condition` wrapper only — a combinator check
  `{call:'and',…}` is a flat check whose call is `and`, not a wrapper.
- **Result interpretation** (`checks.ts:96-101`): `{valid}` shape → `.valid`; bare boolean → direct;
  `undefined` (a FUNCTION error) → treated as **invalid** (fault-gate, ADR-0029 §8).
- **Target dispatch** (`checks.ts:166-179`): an element with `setCustomValidity` (a UIFormElement like
  TextField) → first failing check's message via `setCustomValidity`, `''` when all pass; a Button
  (no `setCustomValidity`, has `disabled`) → **any** failing check auto-disables it, restoring the
  node's declared `disabled` on pass. Neither → no-op.
- **Reactive + leak-free:** one `scope`-owned effect evaluates all checks and surfaces the first
  failure, re-running when a `{path}` arg changes (SPEC-N2); the scope is the surface scope or a
  per-item child scope, so a list item's checks die with the item (`checks.ts:19-25`, `154`).

## Server-initiated `callFunction` RPC (ADR-0034, SPEC-R14)

An inbound envelope `{version, functionCallId, wantResponse?, callFunction:{call, args?}}`
(`protocol.ts:149-150`, `197-212`) — envelope-level, **no `surfaceId`**, `functionCallId`
**top-level**. `handleCallFunction` (`call-function.ts:35`) looks the function up across **all**
registered catalogs and gates on `callableFrom`.

- **Args are CONCRETE LITERALS, not binding-resolved** (`protocol.ts:196-199`, ADR-0034 fork 1) — the
  server provides flat values per the function's catalog schema; there is no data model to resolve a
  `{path}`/`{call}` arg against.
- **`callableFrom` enum: `clientOnly` | `remoteOnly` | `clientOrRemote`; default `clientOnly`**
  (ADR-0034 fact 5, verbatim: *"If omitted, it defaults to `clientOnly`"*). This is the **spec's**
  default (least-authority: not server-invocable unless opted in), not a repo choice. The default
  catalog's `required`/`email`/`regex` are `clientOnly` — so every `callFunction` against the default
  catalog **rejects** until a project registers a `remoteOnly`/`clientOrRemote` function.
- **`clientOnly` is a HARD FLOOR — most-restrictive-wins, order-independent** (ADR-0034 amendment;
  `call-function.ts:43-79`). If **any** active catalog declares the function `clientOnly`, the call is
  rejected regardless of a permissive sibling. **Failure mode this fixed (a real defect, #30):** the
  first build did first-**allows**-match — it skipped a `clientOnly` declaration and took the first
  permissive catalog, citing a **fabricated** "ADR-0034 clause 4b" that never existed. That fails
  OPEN on a security gate. A `callableFrom` check is a security gate and MUST fail closed.
- **Emission** (`call-function.ts:97-116`, ADR-0034 forks 4/5): success + `wantResponse:true` →
  `functionResponse{functionCallId, call, value}` with `functionCallId` copied **verbatim**; success +
  `wantResponse` false/absent → fire-and-forget; **reject** (unregistered / `clientOnly` /
  no-impl / **throwing** impl) → `error{code:'INVALID_FUNCTION_CALL', functionCallId}` (no
  `surfaceId`) — **always** emitted, not gated on `wantResponse` (the server must learn its
  invocation was invalid). `@index`, being a system helper not in `catalog.functions`, is
  **unregistered** for `callFunction` → rejected (correct — a collection-scope helper is never
  server-invocable).

## What this file does NOT cover

The wire error taxonomy and the `FUNCTION`→`VALIDATION_FAILED` vs `INVALID_FUNCTION_CALL` mapping
(errors-and-versioning) · the `{path}` read memo / `setPointer` (bindings-and-data-model) · list
`@index` scope mechanics (dynamic-lists) · what functions a specific catalog SHOULD declare (that is
catalog design, routed to the a2ui-builder/a2ui-catalog-facts owners — not this pack).
