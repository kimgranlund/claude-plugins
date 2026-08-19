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
  must be a valid UAX-31 non-`@` identifier (`catalog.ts:134-136`; see `references/naming-law.md`).
- **`children`** — the child model, one of `'child' | 'children' | 'ChildList'`
  (`catalog.ts:26`, `catalog.ts:141-146`). Absent ⇒ a leaf (no children). `child` = exactly one
  wrapped node (e.g. `Field`, SPEC §5.2 / ADR-0053 cl.2); `ChildList` = an ordered list (the
  containers, `Select`→`Option`, `Tabs`→`Tab`/`TabPanel`). These are the A2UI structural types, so
  payloads stay structurally validatable (SPEC-R1).
- **`value`** — `{ prop, event }`, present ONLY on input components (`catalog.ts:27`). It is the
  two-way-binding contract the renderer's input controller reads (renderer LLD-C8): the control's
  bindable DOM prop + the DOM event that commits it. See `references/factory-and-widget-resolution.md` and
  `references/naming-law.md`.

## The `PropDef` shape — `{ type, bindable?, mapsTo }`

Defined at `catalog.ts:29-33`; validated by `validatePropDef` (`catalog.ts:158-166`).

- **`type`** — a JSON-Schema fragment (`JsonSchema = Record<string,unknown> | boolean`,
  `catalog.ts:11`). The conformance validator checks only the primitive `type` keyword against the
  JS runtime type (see `references/security-allowlist-and-conformance.md`).
- **`mapsTo`** (REQUIRED, a string — `catalog.ts:161`) — the control-side target the factory writes.
  When `mapsTo` **equals** the property name, the factory sets `el[prop]` directly (the 1:1
  reflection, SPEC-R8); when it **differs** (e.g. `Button.label` → `textContent`,
  `catalog.json`), the row needs a **bespoke factory** — routing it through the generic
  `accessorFactory` is the documented factories.ts INVARIANT violation (`default/factories.ts:143-144`).
  This is why `mapsTo` is load-bearing, not cosmetic — see `references/factory-and-widget-resolution.md`.
- **`bindable`** — marks the prop as accepting a `{path}` data reference or `{call}` function-call
  binding (`catalog.ts:32`). Only a bindable prop may carry a binding through conformance
  (`conformance.ts:49-52`). A prop is bindable iff the control can actually reflect a runtime write
  to it.

## The component-level `checks` array — NOT a property

`checks` is a **component-level construct, not a bindable catalog property** (SPEC-R4). It is a
`[{call,args,message}]` validation array evaluated renderer-side, surfaced inline (an input → its
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

## UPDATE 2026-08-17 — the CSS-less-consumer law (ADR-0102) — no CSS verb, three-lane chooser (issue #512)

**[inferred]** from `agent-ui` ADR-0102 (accepted 2026-07-08, + lane exemplars in 0103/0106), cited
here from that report (memory `css-less-consumer-law`) — re-verify against the accepted ADR text at
the next refresh wave rather than trusting this restatement cold. This is the definition the
"UPDATE 2026-07-08" section below already assumed when it said "route through ADR-0102's
CSS-less-consumer chooser" — stated here explicitly, once, so a reader doesn't have to already know
the ADR to use that reference.

**The law:** an A2UI catalog consumer has **NO CSS verb at all** — there is no stylesheet, no class
attribute, no inline-style prop the renderer honors. So any component contract that assumes "the
page author supplies layout/spacing/surface via CSS" **deterministically fails** on an A2UI surface;
this is not a bug to patch per instance, it is a structural fact about the consumer that every new
component or prop decision has to route through.

**The three-lane chooser** — for every "how should this rendered-correctness gap be closed" ask:

- **Lane A — component-owned default.** The component itself picks a sane default (spacing,
  emphasis, wrapping) when composition alone cannot express the intent. No new prop, no catalog
  change.
- **Lane B — a catalog prop.** A boolean/enum prop for **per-instance intent** — e.g. `Text.truncate`
  — only when the concern is genuinely per-instance and a safe default (Lane A) isn't enough (see
  the "intake test" bullet below, already in this file).
- **Lane C — a taught idiom.** Composable but non-obvious layout (e.g. `FormProvider` declaring zero
  layout of its own) is taught via an exemplar or prompt guidance — the payload author composes it
  from existing primitives, the catalog doesn't grow a new mechanism.

**Routing rule — route new instances through the chooser; never re-litigate the law per bug.** Each
"a component looks wrong without CSS" report is an instance of this one gap class, not a fresh
design question; the chooser (Lane A before B before C — cheapest, least-catalog-surface fix first)
is the answer every time, and the ADR is the place a genuinely new lane would be proposed, not a
one-off exception argued in a bug thread.

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

---

## UPDATE 2026-08-19 — the wire-mark shape law, append-only enum widening, and two validates-cleanly defect classes

**[verified]** 2026-08-19 against the ADR texts fetched verbatim from `kimgranlund/agent-ui`
(ADR-0211, ADR-0207 — both `accepted`), `catalog/conformance.ts` read at head `26742a9c`, and the
GH #1328/#1329 → PR #1404 field wave.

**The wire-mark shape law (ADR-0211): a `value` mark is legal ONLY where a real readback accessor
exists.** The `value: {prop, event}` contract above has a precondition the row author must verify,
not assume: the renderer's generic two-way controller reads `el[prop]` SYNCHRONOUSLY at the commit
event. If the control never writes its committed state back onto that accessor, the mark does not
merely fail — it **corrupts the data model**, writing `undefined` (uncontrolled) or the STALE
pre-commit value (controlled) on every commit. ADR-0211's Drill mint is the worked proof: a jsdom
probe against the real control showed `commit()` writes only a private signal in uncontrolled mode
and never self-mutates in controlled mode, so the row ships `path` as a FORWARD-ONLY bindable prop
with **no value mark** — the agent drives navigation by writing the bound pointer via
`updateDataModel` on its own turn. "Not a style choice; a data-corruption class" (ADR-0211 Alt. A).
Sibling precedent, different root cause: the Toggle mint's Fork T1 (pre-commit event ordering).
Re-entry condition, recorded in the ADR: a future public readback accessor reopens the mark by
amendment. Answer conduct: "should this prop get a value mark?" is answered by probing the
control's readback, never by symmetry with sibling rows.

**Append-only enum widening (ADR-0207, the second application of the GH #808 mechanism).** A wire
enum widens by APPENDING members, preserving every existing member's position — `Text.variant` grew
`h1…label` → `+ kicker · overline · quote · lead` this way. Why append-only is load-bearing, not
pedantry: (1) every existing payload, exemplar, fixture, and corpus shard stays byte-identical;
(2) an unanchored drift pin (`toContain('variant: h1|h2|…|body')`) passes UNEDITED — the pin is
verified, never loosened; (3) the byte-pinned prompt's golden baseline recaptures ONCE, deliberately
(`RECAPTURE_BASELINE=1`), with the delta verified to be exactly the widening; (4) ADR-0098's generic
enum gate covers the new members with ZERO validator code — an excluded value keeps failing
`CATALOG` exactly as any unknown member does.

**Two validates-cleanly-still-renders-wrong classes** — both answer "the payload passed validation,
why is the render wrong?":

- **The schema-omission class.** Conformance's `matchesSchemaType` checks `enum` membership plus the
  PRIMITIVE `type` keyword only (`conformance.ts:115-130`) — it never descends into an object/array
  prop's inner keys (`properties`/`required`/`additionalProperties` are outside the declared minimal
  subset). A typo'd inner key (`rows: [{lable: …}]`) therefore validates cleanly; the component's
  hardening codec then DROPS the malformed entry (the ADR-0201 `cleanDescriptionRows` posture:
  malformed → `[]`/omitted, never a throw), so the defect presents as silently-missing content, not
  an error. Never claim conformance checks object shape — the codec is the safety net, and the fix
  is producer-side.
- **The mount-context probe-artifact class.** Before blaming a render path, EQUALIZE the mount
  context of the two sides of the comparison — a shared page shell's ambient CSS and differing mount
  roots manufacture path-specific illusions. Worked instances (GH #1328/#1329, both closed by
  PR #1404, 2026-08-19): the "Ladder degrades on the A2UI path" report was the docs shell's unscoped
  `[data-part='bar']` CSS leaking into the card — the comparison shot mounted the native control
  OUTSIDE the shell, manufacturing a "native right / A2UI wrong" illusion (fix: a zero-specificity
  `:where` fence in the SHELL; no A2UI defect existed); the "Drawer panel empty" report was not
  reproducible at head — the renderer builds subtrees detached, so child adoption is order-safe by
  construction.
