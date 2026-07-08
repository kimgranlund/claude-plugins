# The naming law

What a bindable catalog prop is named, and why the answer is a contract — not a style choice.
Sourced from ADR-0053 (the law's origin) + `catalog/naming.ts` (the identifier rule) +
`catalog/default/factories.ts` (the shipped rows). Normative in catalog SPEC-R2 (identifiers) and
ADR-0053 fork F2 (the bindable-naming law). All paths relative to `packages/agent-ui/a2ui/src/`.

## The law: a bindable prop is named by the CONTROL's own prop

A bindable catalog property is named by the control's own prop — NOT by A2UI's Basic-catalog name
(ADR-0053 cl.1 / fork F2). The shipped precedents: `Tabs.selected`, `Modal.open` — each named after
the control's reflecting prop, each with a matching `value:{prop,event}` mark
(`default/factories.ts:180`, `:186`). So the form family follows: `Checkbox.checked`,
`Switch.checked` (NOT Basic's `value`), `Select.value` (`factories.ts:215-235`, SPEC §5.2 rows).

**Why it is load-bearing, not taste** (ADR-0053 Context): the renderer's two-way input controller
(input.ts, ADR-0019) requires `value.prop` to name BOTH the A2UI node prop AND the DOM commit prop —
one name, one round-trip. `ui-checkbox` carries BOTH a `value` prop (the submitted string `'on'`)
AND a `checked` prop (the bindable boolean). A Basic-aligned `Checkbox.value: boolean` row would
commit the string `'on'` into a boolean data path. The naming question is a correctness bug waiting
to happen, so the law resolves it structurally.

- **Basic alignment is a SHOULD that YIELDS.** SPEC-R3 says names SHOULD align with A2UI's Basic
  catalog for LLM familiarity — but Basic alignment yields to the seam contract and SPEC-R8's
  direct-design-system doctrine wherever they collide (ADR-0053 cl.1). The cost, consciously paid: an
  agent fine-tuned on Basic payloads must learn our names from the catalog document (ADR-0053
  Consequences).

## One `value:{prop,event}` mark per component

The ADR-0019 seam permits exactly ONE two-way mark per component. This forces real design calls when
a control has two commit-worthy states:

- **`SliderMulti`** — two committed values (`valueLo`/`valueHi`), so NO top-level `value` mark;
  both are bindable ONE-WAY only (`factories.ts:366-374`; SPEC §5.2 SliderMulti row; ADR-0087 Fork C).
- **`ComboBox`** — binds the FORM value (`value`/`change`), NOT the disclosure `open`/`toggle`;
  `open` remains a real control prop but carries no catalog property at all (`factories.ts:383-397`;
  ADR-0087 Fork D/combobox).
- **`Select`** — declares `value`/`select`, and `open` is deliberately NOT declared: a one-way `open`
  would silently desync on platform light-dismiss (`factories.ts:231-235`, ADR-0053 cl.4).

## The naming law in practice — `RadioGroup.value`

`RadioGroup` is the freshest worked example. It carries a real `value:{prop:'value',event:'change'}`
mark: `UIRadioGroupElement` exposes a public `value` getter/setter delegating to its private
`#selectedValue` signal (the `UICheckboxElement.checked` precedent), and `change` is the sole
user-driven commit event (`factories.ts:321-335`; SPEC §5.2 RadioGroup row; ADR-0087 Fork B). Verify
this against the source when citing it live: check `packages/agent-ui/components/src/controls/radio/radio-group.ts`
for the public `value` accessor + the catalog row that binds to it.

- **Documented gap (cite it, don't hide it):** the setter's "value matches no child `Radio`" path
  silently CLEARS the selection with no `change` — a data write racing an unmatched value ahead of
  the `Radio` children would blank a valid prior selection with nothing to reconcile (SPEC §5.2
  RadioGroup row; `factories.ts:329-334`).

## Identifier discipline — UAX-31, no reserved `@`

Independent of the naming *law*, every declared component / function / property name MUST be a valid
A2UI v1.0 identifier: a UAX-31 identifier (start ∈ ID_Start, rest ∈ ID_Continue) that does NOT use
the reserved `@` namespace (reserved for system context like `@index`). Enforced by `validName`
(`catalog/naming.ts:14-16`) at load; a violation is `CATALOG_NAME_INVALID` (SPEC-R2, SPEC §5.3).

## Type ↔ tag bijection

A catalog type name and its `ui-*` tag are a bijection: `FormProvider` ↔ `ui-form-provider` — NOT a
friendlier alias like `Form`, which would be the catalog's only non-derivable name (ADR-0053
Alternatives). Keep new type names mechanically derivable from the tag (`ui-{kebab}` → PascalCase,
the same map the coverage gate walks, `default/index.test.ts:110-114`).
