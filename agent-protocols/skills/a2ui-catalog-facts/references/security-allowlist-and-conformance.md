# Security allowlist & conformance validation

How the catalog acts as a render-time security boundary, and how a payload is validated against it.
Sourced from `catalog/conformance.ts` + `renderer/widget.ts`; normative in catalog SPEC-R9 (security
allowlist), SPEC-R7 (conformance), SPEC-N3 (validator parity). All paths relative to
`packages/agent-ui/a2ui/src/`.

## The catalog IS the security allowlist

SPEC-R9: only components present in the bound catalog MAY render; the renderer MUST validate
agent-supplied properties against the component's typed schema. Enforcement is two-layered:

1. **Resolution layer** — an unknown type resolves to no factory, so the renderer emits `CATALOG` +
   renders a placeholder, never the agent's node (`renderer/widget.ts:108-120`; SPEC-R9 AC1). A type
   absent from the catalog cannot appear in a rendered surface at all (ADR-0087 Context — "the
   agent-emittable surface").
2. **Conformance layer** — `validateCatalogConformance(component, catalog)` (`conformance.ts:17-32`)
   verdicts the node's properties. This is the anti-injection spine: an agent cannot smuggle an
   arbitrary attribute onto a control, because an undeclared property is a `CATALOG` failure.

## `validateCatalogConformance` — three failure kinds, one code

Returns `Failure[]` (`[]` = conformant). Every failure carries `code: 'CATALOG'`
(`conformance.ts:17-32`):

- **Unknown type** — `catalog.components[component.component]` is absent ⇒ one `CATALOG` at the
  node's `id` (`conformance.ts:18-19`).
- **Unknown property** — a present property with no `PropDef` ⇒ `CATALOG` at `id.prop`
  (`conformance.ts:25-27`).
- **Type mismatch** — a property whose value fails its schema type ⇒ `CATALOG` at `id.prop`
  (`conformance.ts:29`).

Worked example (from the shipped tests, `default/index.test.ts:252-261`): a `Modal` with
`open: 'yes'` fails (`open` is declared boolean → type mismatch); a `Modal` with `bogus: 1` fails
(undeclared property). Both are `CATALOG` — the renderer's not-rendered verdict.

- **Caveat — PRESENT-props only:** conformance verdicts the properties a node CARRIES, not
  required-presence (`default/index.test.ts:253-255`). A missing required prop is NOT a conformance
  failure here by default; presence/validity of required fields is a renderer-side `checks` /
  control-validity concern, not catalog conformance. **Amended 2026-10-03:** two OPT-IN PropDef
  presence rules now exist, see "Opt-in presence and action-prop narrowing" below.

## `RESERVED` structural keys are never properties

`RESERVED = {id, component, child, children, checks}` (`conformance.ts:14`) are the adjacency-model
keys owned by the tree, skipped by conformance. Critically, `checks` is RESERVED: any node may carry
a component-level `checks` array without an unknown-property failure — it is a renderer-layer
construct (ADR-0029), never a bindable catalog prop (SPEC-R4; see `references/component-definition-contract.md`).

## Bindings: accepted only on `bindable` props

A value conforms if it is a literal matching `pd.type`, OR — when `pd.bindable` — a `{path}` data
reference or `{call}` function-call binding (`conformance.ts:44-52`). Both binding arms occupy the
same "deferred resolution" position and are evaluated at render (LLD-C5/LLD-C10); static type
checking of a `{call}` result is out of scope for the static validator (`conformance.ts:37-42`). A
`{path}` on a NON-bindable prop falls through to `matchesSchemaType` and fails (an object isn't a
string) — so bindability is itself part of the security surface.

## Type checking is primitive-only, and deliberately does NOT over-reject

`matchesSchemaType` checks only the JSON-Schema `type` keyword against the JS runtime type
(`conformance.ts:55-82`): `string`/`number`/`integer`/`boolean`/`object`/`array`/`null`. Unknown
schema keywords return `true` — "do not over-reject" (`conformance.ts:79-81`).

- **Known-tolerant caveat — FALSIFIED by ADR-0098 (correction dated 2026-08-19):** this bullet's
  original 2026-07-07 claim ("an out-of-enum `type` literal PASSES the static validator … Enum
  membership is NOT enforced by conformance … Do not tell a user conformance rejects a bad enum
  value") described the pre-ADR-0098 validator and is no longer true. **[verified]** against
  `conformance.ts` fetched from `kimgranlund/agent-ui` origin/main 2026-08-19: `matchesSchemaType`
  now checks JSON-Schema `enum` membership FIRST — strict `===`, case-sensitive, no coercion,
  evaluated before the `type` dispatch as a narrower constraint layered on top of it
  (the enum branch of `matchesSchemaType`, cite by symbol; it sat at `conformance.ts:151-156` on 2026-10-03); an out-of-enum literal fails `CATALOG`. Scope limits that DO still
  hold: only primitive-member equality is evaluated (deep-equality object members are outside the
  declared minimal subset — no shipped catalog uses them), and a bindable prop's `{path}`/`{call}`
  arms still defer to render time as above. The renderer's `applies` gate remains as
  defense-in-depth at apply-time.

## Opt-in presence and action-prop narrowing (2026-10-03)

Three PropDef flags tighten conformance past type/enum, each OFF unless a catalog row opts in:

- **`required`** (key presence) and **`requires`** (cross-prop presence: this prop needs that one)
  report at the MISSING key's path. A `{path}` or `{call}` binding satisfies presence; values are
  never checked, only that the key is there. **Failure mode:** expecting `required` to reject an
  empty string or a bad value; it does not, presence only.
- **`rejectFunctionCall`** narrows an action prop: an object value with an own `functionCall` key
  fails `CATALOG` (the client-side-execution Action arm is not accepted on that prop). Only that one
  key, and only when the PropDef opts in; there is no general object-shape descent. The
  `FUNCTION` code stays render-time-only: this rejection emits `CATALOG`, not `FUNCTION`.
  **Failure mode:** assuming conformance now validates action object shapes in general.

[verified] agent-ui `catalog/conformance.ts` (required/requires loops, `rejectFunctionCall` branch),
GH #1189, ADR-0226, ADR-0169 E7 row, GH #429 (closed 2026-08-05); 2026-10-03.

## Validator parity — ONE implementation, two callers

The catalog-conformance code path is shared: the renderer's `validate.ts` (LLD-C11) composes it, and
so does corpus admission (SPEC-N3 / corpus SPEC-N1) — one implementation, identical verdict
(`conformance.ts:1-6`). This is why a catalog-row change ripples to corpus admission automatically:
the same `validateCatalogConformance` gates both. When you change what a row accepts, you change what
the corpus admits — there is no second validator to keep in sync.
