# API & library policy — the Compose axis, made concrete

The Compose axis (A1–A5) is about the *abstraction*: layer, anatomy, API surface, composition,
coherence. This file is the policy library it draws on — the decision rules, anti-patterns, naming,
governance, and the definition-of-done. The spine across every source: **push variation outward —
composition over configuration.**

## A1 · The layering model & the primitive-vs-composition rule

Five tiers, bottom-up: **tokens → primitives → components → patterns → templates/pages.**

- **Tokens** — raw → semantic → component. Keep primitives private; the **semantic layer is the
  governed contract** (theming = re-pointing semantic tokens, touching zero components).
- **Primitives** — token-only API, no domain meaning: `box`, `stack`, `cluster`, `grid`, `pressable`.
  This is where the **no-outer-margin** rule lives: spacing between things is a *layout primitive's*
  `gap`, never a margin a component sets on itself.
- **Components** — named, skinned widgets built from primitives: `button`, `select`, `card`, `field`.
- **Patterns** — reusable compositions solving a recurring UX problem: a modal *card*
  (header+body+actions), a form *field* (label+control+hint+error), an empty state. The most
  valuable and most under-documented tier.
- **Templates/pages** — structure skeletons → real-content instances.

> **It's a PRIMITIVE when ALL hold:** token-only API · no baked-in visual identity · single
> structural/behavioral responsibility · a structural name (`box`, not `card`) · composes nothing
> *named*.
> **It's a COMPONENT/PATTERN when ANY fires:** a domain name / fixed meaning · fully skinned ·
> assembles ≥ 2 named parts · encodes behavior spanning parts. If that behavior is reusable *guidance*
> rather than one widget → it's a **pattern**, not a component.

Separate gate — *does it belong in the system at all?* **Rule of Three** (proven across ≥ 3 distinct
uses before promotion); reuse costs ~3× to build; "well-crafted ≠ belongs."

## A3 · API surface

- **Slots vs props.** Prop for the common, finite, predictable (`size`, a label); **slot** for
  open-ended/structural variation you can't enumerate. A `headerContent` / `footerActions` *prop* is
  the smell that a slot is warranted.
- **Variants & sizes are orthogonal enums** (`variant` × `size`), never multiplied booleans. Keep
  them separate so they compose instead of exploding.
- **Boolean-prop explosion is the canonical anti-pattern** — `n` booleans = `2^n` mostly-invalid
  states. Fix in order: (1) a single `variant` enum for mutually-exclusive options, (2) composition
  into named components, (3) slots. Keep genuinely-independent booleans (`disabled`, `loading`).
  `component-contract-check.py` warns past 6 boolean props.
- **Compound components** for tightly-coupled parts sharing implicit state (`<x-select>` ·
  `<x-option>`); meaningless apart. This is the structural answer to prop-explosion.
- **Controlled vs uncontrolled** — support both: `value` + change-event (controlled) / `defaultValue`
  (uncontrolled). Hard rules: never switch modes at runtime; `value` and the change event travel
  together; `value` and `defaultValue` are mutually exclusive. In the signals idiom, the value is a
  `signal`; "controlled" means the consumer owns it and the element reflects.
- **Future-proof the shape**: `type="warning"` (string, extensible) over a `warning` boolean.
  *"Make the common configurable, make the uncommon composable."*
- **Attributes ARE the API, for a custom element.** Prop-counting is incomplete — a custom element's
  public surface is its typed **attributes**, its **properties** (declared vs hand-written), their
  **reflection** direction, its semantic **events**, and (for a control) the **form-value** channel.
  Grade that platform-precise surface, not just the prop list — including the lazy-upgrade hazard that
  caps A3 at <5 when a hand-written accessor has no `upgradeProperty` story. Full model + the
  mechanized checks: `attributes-as-api.md`.

## A2 · Anatomy — name the parts

Borrow the part vocabulary from a consistent source (Radix-style anatomy is the most consistent;
roles + keyboard come from the APG). Every styleable element gets a `part` (consumers can't reach
descendants of a part). Anatomy is the crossing point with Realize — each named part must map to a
real, embodiable DOM shape (a `::part`, a slot, a `:state()`), or it's fiction.

## A4 · Composition

Does it nest? A button is also the trigger of a select, the item of a menu, the action in a modal
card — one geometry (see `geometry-system.md`), reused. Does it avoid owning outer margin, leaking
compound state, or hard-coding what a parent should decide (width, placement, spacing)?

## A5 · Coherence & governance

- **Naming.** Tag prefix/suffix consistent with the library (`x-button` / `button-ui`); attributes
  kebab-case, properties camelCase; events are semantic (`change`, `value-change`, `open-change`).
  Pick one house style for booleans (`disabled` vs `isDisabled`) and hold it.
- **Token contract.** Components consume *semantic* tokens only; expose deliberate
  custom-property injection points (enough to theme, not so many they can't be maintained).
- **Versioning.** SemVer; tokens version separately from components (different owners, cadence).
- **Deprecation.** Communicate → timeline → docs notice → repo flag → migration guide + codemod *at
  deprecation time* → delete. Carry `Deprecated date · Replacement · Reason · Migration` on the
  notice. Windows aren't standardized — require *a defined timeline*, not a fixed number.
- **Documentation per component**: labeled anatomy, when-to-use / when-not, do/don't, token refs,
  a11y requirements, an explicit **maturity status** (e.g. Experimental → Stable → Deprecated).

## Component definition-of-done (the rubric checklist)

A component is production-ready when all hold (synthesized from Carbon, GOV.UK, Atlassian, WCAG 2.2,
APG — the Realize items are gated by `scripts/`):

1. **Layer + anatomy named** — right tier; every part named and `::part`/slot/`:state()`-exposed.
2. **Geometry on the ramp** — `geometry-check.py` passes: heights/glyphs/font/spacer on the ramp,
   derived paddings, glyph-only square, container insets composed.
3. **All states built** — default, hover, focus, active, selected, disabled, read-only, loading,
   empty, error — enumerated, not emergent.
4. **Keyboard & focus** — fully operable, no trap (or a deliberate one for dialogs); APG pattern for
   the role; visible, unobscured focus.
5. **Programmatic semantics** — correct role + name/state/value via `ElementInternals`; form controls
   are FACE with a `setValidity` story.
6. **Forced-colors + contrast + target size** — `@media (forced-colors: active)`; text ≥ 4.5:1,
   non-text ≥ 3:1; targets ≥ 24×24; `prefers-reduced-motion` honored.
7. **API reviewed** — names match siblings; controlled/uncontrolled consistent and mode-stable;
   decomposed not prop-bloated; public surface typed.
8. **Composes** — no outer margin; nests as a part of higher components; theming via tokens/`::part`.
9. **SSR + theming + icons** — DSD/light-DOM hydration declared; `@layer`-wrapped; inline-SVG icons.
10. **Documented + status** — anatomy, usage, a11y, maturity status whose promotion gate is met.

## The contract card

The artifact DESIGN emits and GRADE re-derives — a `*.contract.json` checked by
`component-contract-check.py`:

```json
{
  "component": "x-select",
  "layer": "component",
  "form_associated": true,
  "replaces_native": true,
  "role": "combobox",
  "parts": ["trigger", "value", "listbox", "option", "indicator"],
  "props": ["size", "variant", "disabled", "invalid", "open"],
  "boolean_props": ["disabled", "invalid", "open", "required"],
  "slots": ["option"],
  "states": ["open", "disabled", "invalid"],
  "keyboard": ["ArrowDown", "ArrowUp", "Enter", "Escape", "Home", "End"],
  "forced_colors": true,
  "owns_outer_margin": false,
  "validity": true,

  "attributes": {
    "size":  { "type": "enum", "values": ["sm", "md", "lg"], "reflect": true },
    "value": { "type": "string", "reflect": false }
  },
  "properties": [ { "name": "value", "manual": true }, { "name": "open", "readonly": false } ],
  "upgrades_manual_props": true,
  "events": ["change", "input"]
}
```
The linter gates: hyphenated tag, valid layer, role present for interactive, FACE for controls,
APG-keyboard minimum, forced-colors for native-replacing controls, and an **enum attribute with no
`values[]`**; and warns on boolean-prop explosion, self-owned outer margin, a **`manual:true`
property with no upgrade story**, an **implementation-named event**, and a **form control reflecting
its `value`**. The `attributes` / `properties` / `events` / `upgrades_manual_props` block is the
attributes-as-API surface (`attributes-as-api.md`) — **optional and additive**: an old card with only
the flat `props` / `boolean_props` still lints clean.
