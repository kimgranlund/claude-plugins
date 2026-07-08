# Two-tier extensibility

How a downstream app extends or replaces the default catalog with zero package edits. Sourced from
`catalog/registry.ts` + `catalog/catalog.ts`; normative in catalog SPEC-R6 / SPEC-N1 (two-tier) and
SPEC-R5 / ADR-0034 (the function collision floor). All paths relative to
`packages/agent-ui/a2ui/src/`.

## The two tiers

Tier 1 is the **default catalog** (`catalog/default/`, `catalogId: 'agent-ui'`) that ships with
`@agent-ui/a2ui`. Tier 2 is any **project catalog** an app registers at runtime. SPEC-R6: a
downstream app MUST be able to register a project catalog + its factories through the public
`CatalogRegistry`, announce them via `supportedCatalogIds`, and target one via
`createSurface.catalogId` — **without editing `@agent-ui/a2ui`** (SPEC-N1: 0 edits, no package
rebuild). Project catalogs MAY extend OR wholly replace the default (SPEC-R6).

## `register` is the public seam

`Registry.register(catalog, factories)` (`registry.ts:39-62`) is the entire extension point. It:

1. **Re-loads + narrows** the untyped input through `loadCatalog` (`registry.ts:42`) — the loader is
   the single shape gate (LLD-C1), so a stored entry is always structurally valid.
2. **Enforces the bijection** — every declared component type must have a factory, else
   `CATALOG_FACTORY_MISSING` (`registry.ts:47-54`, SPEC-R7 AC1). The `Object.hasOwn` check
   (`registry.ts:48`) is deliberate: a type named like an `Object.prototype` key (`toString`,
   `constructor`) cannot spuriously satisfy the lookup via the prototype chain.
3. **Stores last-wins** on a duplicate `catalogId` (`registry.ts:58-61`) — a project catalog MAY
   intentionally shadow a prior registration (its own id, or the default's). The override is
   `console.warn`'d so it is never silent (`registry.ts:59`).

- **Caveat:** last-wins means registering a catalog with `catalogId: 'agent-ui'` REPLACES the
  default wholesale — that is the sanctioned "wholly replace" path, not a merge. There is no
  row-level merge; to extend, register under a NEW `catalogId` and point the surface at it.

## The registry IS the allowlist

`registry.get(id)` returns `undefined` for an unregistered id (`registry.ts:64-66`). A
`createSurface.catalogId` not in the registry makes the renderer emit `CATALOG_UNKNOWN` (SPEC-R6 AC3)
— the registry is the allowlist of catalogs a client supports. `supportedCatalogIds()`
(`registry.ts:68-70`) feeds the renderer's capabilities announcement (renderer LLD-C12).

## `submitGateSelector` aggregates across ALL registered catalogs

`submitGateSelector()` (`registry.ts:72-84`) returns a CSS selector matching every `submitGate`
factory's tag across EVERY registered catalog (ADR-0054, two-tier) — so a project catalog MAY mark
its own submit gate alongside the default's `FormProvider` (`ui-form-provider`,
`default/factories.ts:206`). It returns the empty string when no factory carries the mark; callers
MUST treat that as "no gate anywhere" and skip `Element.closest` (an empty selector is a
`SyntaxError`) — the renderer's `#wireAction` guards this (`types.ts:64-69`).

## Function `callableFrom` — a security floor that TIGHTENS across tiers

Catalog functions carry a `callableFrom` enum (`clientOnly | remoteOnly | clientOrRemote`,
`catalog.ts:45`) governing the server-initiated `callFunction` RPC (SPEC-R5, ADR-0034). Two-tier
rule (SPEC-R5, its AC3): when a name is declared in more than one registered catalog, the effective
`callableFrom` is the **MOST RESTRICTIVE** across them — `clientOnly` is a HARD FLOOR, independent of
registration order. A sibling catalog may *tighten* a security boundary, never *loosen* it.

- **Default:** an omitted `callableFrom` defaults to `clientOnly` (`catalog.ts:182-185`) — least
  authority; a function is not server-invocable unless explicitly opted in.
- **Failure mode this prevents:** a permissive project catalog cannot re-declare the default's
  `clientOnly` validator (`required`/`email`/`regex`) as `clientOrRemote` to gain server-invoke — the
  floor wins. This is NOT first-match / most-permissive.

## Worked example — extending, not replacing

```ts
const registry = new Registry()
registry.register(defaultCatalog, defaultFactories)     // tier 1
registry.register(myCatalog, myFactories)               // tier 2, NEW catalogId
// agent targets it:  createSurface({ catalogId: 'my-app', ... })
```

Claim: two catalogs coexist, each resolved by its own `catalogId`. Cited: `registry.ts:36-70` +
SPEC-R6. Caveat: reusing `catalogId: 'agent-ui'` for `myCatalog` replaces the default instead of
adding to it (last-wins, `registry.ts:58`).
