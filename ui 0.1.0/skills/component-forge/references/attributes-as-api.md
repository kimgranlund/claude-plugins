# Attributes as API — the A3 surface for a custom element

The Compose axis grades **A3 (API surface)** as slots-vs-props, variants-not-booleans, the
boolean-prop explosion, and controlled/uncontrolled (`api-policy.md`). That's correct but
*incomplete for a custom element*, whose public API **is** its attributes / properties / reflection /
events / form-value surface — a platform-precise contract with failure modes plain prop-counting
can't see. This file is the body of knowledge A3 grades, and the part of it
`scripts/component-contract-check.py` checks mechanically.

This is knowledge + technique, not a new axis: the two axes, the gates, and the geometry foundation
are unchanged. The skill stays **contract, not code** — it grades the descriptor, it does not emit
the element.

## The four channels (and which is primary)

A custom element's authored surface is four coupled channels:

1. **Attributes** — the HTML surface. *Typed* (`string | number | boolean | enum | json`), each with a
   **reflection direction** (does a property change write back to the attribute?) and a default. An
   `enum` attribute has a **closed value set**.
2. **Properties** — the JS surface. Some are **declared** (backed by the prop system); some are
   **hand-written accessors** (`value` with sanitize / caret / dirty-state guards). The
   attribute ↔ property ↔ reflection relationship *is* the contract — and it carries a real,
   repeatable bug (below).
3. **Events** — also API. Must be the **semantic** set (`change` / `input` / `open` / `close` /
   `select` / …), never implementation names (`onClick`, `handleFoo`).
4. **Form value (FACE)** — for a value-bearing control, the value channel is the **primary** API:
   dirty-value semantics, the `value` property typically **non-reflecting**, and a `setValidity`
   story (see `family-controls.md`, `platform-baseline.md`).

> **Decision rule.** For a value-bearing control the **form-value channel is primary** — grade it
> first. For everything else, attributes are the surface a consumer reaches for, so grade their
> types and reflection before the prop list.

## The typed-attribute table

| Field | Rule |
|---|---|
| `type` | one of `string · number · boolean · enum · json` |
| `values` | **required when `type:"enum"`** — an enum is a closed set; an enum with no declared values is a gate failure |
| `reflect` | the direction property→attribute. Default **off**. Reflect presentational/queryable state (`size`, `variant`, `open`); **do not reflect** the dirty `value` of a form control |
| default | the value when the attribute is absent |

- **Naming:** attributes are **kebab-case** on the HTML surface (`max-length`), properties are
  **camelCase** on the JS surface (`maxLength`). One concept, two spellings — keep them paired.
- **`boolean` attributes** are presence-based (`disabled`, not `disabled="false"`).

## Events are API — semantic, not implementation

An event name is part of the public contract; renaming it is a breaking change. Emit the **semantic**
set — `change` (committed value), `input` (in-progress), `open`/`close`, `select`, `toggle`,
`submit`, `invalid` — or a namespaced semantic event (`page-change`). An implementation-named event
(`onItemClick`, `handleUpdate`) leaks the internals and can't be relied on. *(Cross-links
`api-policy.md` A5 naming.)*

## The manual-accessor / lazy-upgrade hazard (the load-bearing failure A3 misses)

The defect that makes a clean-looking API review pass a broken component:

- **Symptom** — the component renders **empty or stale**, but **only under dynamic subtree
  insertion** (a list re-render, a portal, a framework patch). Static server HTML is fine, because
  the parser upgrades children-first and hides it.
- **Cause** — a template `.prop=` binding commits the value on a *cloned* element **before** the
  custom element upgrades. The value lands as a **shadowing own data property**, and when the class
  accessor is finally installed at upgrade it sits *behind* that own property — so the accessor never
  sees the value.
- **Who's affected** — only **hand-written** (`manual`) accessors. Declared props are handled by the
  prop system; manual accessors are the gap.
- **The rule (corrective).** Every hand-written property accessor must be listed `manual: true` on
  the contract card, and the component must **re-apply each manual accessor at connect** — the
  `upgradeProperty(...names)` pattern (delete the own property, then re-set it through the accessor).
  The card asserts this with a single marker `upgrades_manual_props: true`.

This is a **designed-right / built-wrong** defect in API form: the contract reads fine, but the
component is broken in the one case a test rarely covers. So **A3 cannot score 5 while a `manual:true`
property has no upgrade story.**

## What the linter checks (`scripts/component-contract-check.py`)

The mechanizable subset of the above (the judgment stays in A3):

- **FAIL** — an `attributes` entry with `type:"enum"` and no `values[]` (a closed set with no members).
- **WARN** — a `properties[]` entry with `manual:true` while the card lacks `upgrades_manual_props:true`
  (the lazy-upgrade hazard, unaddressed).
- **WARN** — an `events[]` name outside the semantic set (an implementation-named event).
- **WARN** — a form-associated control that **reflects** its `value` attribute (the dirty-value smell).

The `attributes` / `properties` / `events` / `upgrades_manual_props` fields are **additive**: a
contract card that carries only the flat `props` / `boolean_props` still lints clean.

## Rulings — taste-gate answers recorded on the card (added 2026-07-16)

A contract card MAY carry `rulings: [{fork, choice, date}]` — the durable record of any
taste-gate answer (SKILL.md step 4's gate; canon: layout-decompose's
`references/taste-elicitation.md`). Checkers tolerate the key; sessions consult it before
asking — a recorded fork is never re-asked.
