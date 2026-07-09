# Component definition contract

What one catalog row declares, and how each field constrains a payload node. Sourced from the
schema model in `catalog/catalog.ts` and the shipped rows in `catalog/default/catalog.json`;
normative in catalog SPEC-R4 + §5.1. All paths relative to
`packages/agent-ui/a2ui/src/`.

## The `ComponentDef` shape

A component definition is `{ name, properties, children?, value? }` — the typed interface at
`catalog/catalog.ts:22-27`. The loader (`loadCatalog`, `catalog.ts:82`) parses + structurally
validates a document into this shape and THROWS `CatalogError` on any defect; downstream code never
re-checks shape (the LLD-C1 load-time invariant, `catalog.ts:1-6`).

- **`name`** — the type identity a payload's `component` field references. Optional in the JSON
  document: it **defaults to the declaring key**, and if present MUST equal the key
  (`catalog.ts:124-130`). So `defaultCatalog.components[key].name === key` for every row
  (`default/index.test.ts:68-72`). *Caveat:* a `name` that disagrees with its key is a load-time
  `CATALOG_MALFORMED` throw, not a silent rename.
- **`properties`** — `Record<string, PropDef>`, the typed prop schema (below). Every property name
  must be a valid UAX-31 non-`@` identifier (`catalog.ts:134-136`; see [[naming-law]]).
- **`children`** — the child model, one of `'child' | 'children' | 'ChildList'`
  (`catalog.ts:26`, `catalog.ts:141-146`). Absent ⇒ a leaf (no children). `child` = exactly one
  wrapped node (e.g. `Field`, SPEC §5.2 / ADR-0053 cl.2); `ChildList` = an ordered list (the
  containers, `Select`→`Option`, `Tabs`→`Tab`/`TabPanel`). These are the A2UI structural types, so
  payloads stay structurally validatable (SPEC-R1).
- **`value`** — `{ prop, event }`, present ONLY on input components (`catalog.ts:27`). It is the
  two-way-binding contract the renderer's input controller reads (renderer LLD-C8): the control's
  bindable DOM prop + the DOM event that commits it. See [[factory-and-widget-resolution]] and
  [[naming-law]].

## The `PropDef` shape — `{ type, bindable?, mapsTo }`

Defined at `catalog.ts:29-33`; validated by `validatePropDef` (`catalog.ts:158-166`).

- **`type`** — a JSON-Schema fragment (`JsonSchema = Record<string,unknown> | boolean`,
  `catalog.ts:11`). The conformance validator checks only the primitive `type` keyword against the
  JS runtime type (see [[security-allowlist-and-conformance]]).
- **`mapsTo`** (REQUIRED, a string — `catalog.ts:161`) — the control-side target the factory writes.
  When `mapsTo` **equals** the property name, the factory sets `el[prop]` directly (the 1:1
  reflection, SPEC-R8); when it **differs** (e.g. `Button.label` → `textContent`,
  `catalog.json`), the row needs a **bespoke factory** — routing it through the generic
  `accessorFactory` is the documented factories.ts INVARIANT violation (`default/factories.ts:143-144`).
  This is why `mapsTo` is load-bearing, not cosmetic — see [[factory-and-widget-resolution]].
- **`bindable`** — marks the prop as accepting a `{path}` data reference or `{call}` function-call
  binding (`catalog.ts:32`). Only a bindable prop may carry a binding through conformance
  (`conformance.ts:49-52`). A prop is bindable iff the control can actually reflect a runtime write
  to it.

## The component-level `checks` array — NOT a property

`checks` is a **component-level construct, not a bindable catalog property** (SPEC-R4). It is a
`[{call,args,message}]` validation array evaluated client-side, surfaced inline (an input → its
validity message; a Button → auto-disable; ADR-0029). It is a `RESERVED` structural key
(`conformance.ts:14`) — any node may carry it without a `CATALOG` unknown-property failure, and it
is never `applyProp`'d.

- **Caveat / known gap:** a *per-component declaration* of which types accept `checks` is
  **deferred** — `validatePropDef` requires `mapsTo` on every declared property, so a no-`mapsTo`
  `checks` marker is infeasible without a validator extension (SPEC-R4, ADR-0029). A `checks` on a
  non-input/non-Button is accepted structurally and the controller no-ops.

## Worked example — a `Field` row

```jsonc
"Field": {
  "properties": {
    "label":       { "type": { "type": "string" }, "bindable": true, "mapsTo": "label" },
    "description": { "type": { "type": "string" }, "bindable": true, "mapsTo": "description" }
  },
  "children": "child"   // the ONE wrapped control (ADR-0053 cl.2)
}
```

Claim: `Field` wraps exactly one control and reflects two bindable strings 1:1. Cited:
`catalog/default/catalog.json` `Field` row + SPEC §5.2 `Field` row + ADR-0053 cl.2. Failure mode
this row avoids: giving `Field` a `ChildList` would let an agent stuff multiple controls into one
labelled field — the `child` model makes that a structural-validation failure, not a silent
mis-render.

---

## UPDATE 2026-07-08 — two prop idioms the chart/Text waves minted (ADR-0106/0109/0107)

- **Non-bindable presentation intent** (`Text.truncate`, `Text.emphasis`): per-instance INTENT that
  is not data state takes a boolean prop with **`bindable` ABSENT by key-omission** (never
  `"bindable": false`) — the fleet convention for "the model sets it, the data model never drives
  it". Rides the factory's generic `default:`→`setAttr` arm; NO factory code per prop.
- **Array-typed bindable props** (`Sparkline.values: number[]`, `BarChart.data: {label,value}[]` —
  the catalog's FIRST): declare the full item schema in the row; the shared validator accepts
  literal arrays at top-level type depth (deeper per-item checking permitted, not required — the
  component's own hardened codec is the safety net; `from(null) = []`, malformed JSON never
  throws). A `{path}` bind resolves to the same typed array and re-renders on `updateDataModel`.
- **The intake test for "should this become a catalog prop":** route through ADR-0102's
  CSS-less-consumer chooser — Lane B (a prop) only when the concern is per-instance intent over a
  safe default; component-owned defaults (Lane A) and taught idioms (Lane C) come first.
- **The §5.2 usage-guidance pattern** (ADR-0087 Fork-A style): a row that competes with existing
  vocabulary lands WITH a when-to-use note (the chart four-way: tile for a latest value ·
  Sparkline for a series' shape · BarChart for comparing magnitudes · List table for exact values).
