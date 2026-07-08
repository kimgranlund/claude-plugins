# Factory pattern & widget resolution

How a catalog type becomes a live `ui-*` control, and who owns the resolution. Sourced from
`catalog/types.ts`, `catalog/default/factories.ts`, and the renderer's `renderer/widget.ts`.
Normative in catalog SPEC-R4 (definition contract) + runtime SPEC-R9 / renderer LLD-C7 (resolution).
All paths relative to `packages/agent-ui/a2ui/src/`.

## The `WidgetFactory` contract — `{ tag, create, applyProp, value?, submitGate? }`

Defined at `catalog/types.ts:19-40`. One factory per component type turns an A2UI type DIRECTLY into
a live control — no Basic-catalog adapter (SPEC-R8):

- **`tag`** — the custom-element tag produced (e.g. `ui-button`, `catalog/types.ts:20`), OR a
  sanctioned non-`ui-*` primitive selector (`div[role=option]`, `default/factories.ts:245-264`).
- **`create()`** — constructs a fresh unparented instance (`types.ts:22`). Importing `factories.ts`
  imports `@agent-ui/components` (`default/factories.ts:50`), whose control modules
  `customElements.define` as a load-time side effect — so `create()` returns the REAL upgraded
  control, not an inert `HTMLUnknownElement` (`default/factories.ts:5-8`).
- **`applyProp(el, prop, value)`** — maps ONE A2UI property (per the row's `PropDef.mapsTo`) onto the
  control as a prop or attribute (`types.ts:24`).
- **`value?: { prop, event }`** — input widgets only: the DOM value prop + commit event the
  renderer's input controller (LLD-C8) wires for two-way binding (`types.ts:26-30`). Absent on
  non-inputs.
- **`submitGate?: true`** — marks the control a submit-action gate (ADR-0054); the registry
  aggregates it into a derived selector (`types.ts:32-39`; see [[two-tier-extensibility]]).

## Resolution is the RENDERER's job, not the catalog's

The catalog OWNS the factory table; the renderer OWNS resolution. A node's control is resolved by
`registry.get(surface.catalogId)?.factories[node.component]` (`renderer/widget.ts:108-109`; the
contract is restated at `catalog/types.ts:46-48` and `renderer/widget.ts:83`). The resolver
(`makeCreateWidget`, `widget.ts:104`) ALWAYS returns an element: on an unknown type it emits a
`CATALOG` error and returns a placeholder so sibling nodes still mount — non-fatal (`widget.ts:110-120`,
runtime SPEC-R9 AC2). This is the security-allowlist enforcement point — see
[[security-allowlist-and-conformance]].

- **Caveat:** a catalog author never writes resolution code. Adding a row = a `catalog.json` entry +
  a `factories.ts` factory + the derived-gate coverage (see [[coverage-policy-and-drift-gates]]);
  the renderer picks it up through `registry.get` with zero renderer edits.

## The `accessorFactory` vs bespoke split — the load-bearing INVARIANT

`accessorFactory(tag, value?, submitGate?)` (`default/factories.ts:156-165`) builds a factory whose
`applyProp` sets `el[prop] = value` directly. It is correct ONLY when every property's `mapsTo`
EQUALS its name (the SPEC-R8 1:1 reflection). The INVARIANT (`default/factories.ts:143-144`):

> a property whose `mapsTo` differs from its name (a non-identity mapping, like `Button.label` →
> `textContent`) needs a BESPOKE factory — it must NOT route through `accessorFactory`.

Worked contrast:
- `Row`/`Column`/`Card`/`TextField`/`Field`/`Select` etc. — all-1:1 ⇒ `accessorFactory`
  (`factories.ts:168-235`).
- `Button` (`label`→`textContent`), `Text` (`text`→`textContent` + `variant` fan-out through
  `TEXT_VARIANT_TABLE`), `Checkbox`/`Switch` (`label`→`textContent`) — bespoke
  (`factories.ts:69-130`, `217-229`). Setting `el.label = "x"` on a checkbox would target a
  non-existent prop instead of the slotted light-DOM text.

Failure mode the invariant prevents: a non-identity prop silently routed through `accessorFactory`
writes to a phantom JS property, so the value never reaches the DOM and the control renders blank —
with no error (it's a valid property set on a live object).

## Sanctioned non-`ui-*` primitives

Not every type binds to a custom element. `Option` → `div[role=option]` (`factories.ts:245-264`) and
`MenuItem` → `div[role=menuitem]` (`factories.ts:287-306`) are **sanctioned NON-`ui-*` primitives**
(the pre-`ui-text` `Text` precedent, SPEC-R3 AC1). The parent control moves these light-DOM children
into its panel at connect (`ui-select` / `ui-menu`). Note the value mapping differs per parent:
`Option.value` → the `value` attribute; `MenuItem.value` → the `data-value` attribute (verified
against `menu.ts` `#commit`, `factories.ts:281-286`). These carry NO `value:{prop,event}` mark —
they are passive list items, not bindable components.

## The catalog↔factory bijection is gated

Every declared type MUST have a factory: `registry.register` throws `CATALOG_FACTORY_MISSING`
(SPEC-R7 AC1) on a gap (`registry.ts:47-54`), and the reverse ("no extra factory-less type") is held
by the derived coverage gate. The `defaultFactories` table (`factories.ts:418-451`) is keyed by
A2UI type and must be 1:1 with `catalog.json`'s components. See [[coverage-policy-and-drift-gates]].
