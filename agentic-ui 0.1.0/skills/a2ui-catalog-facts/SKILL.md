---
name: a2ui-catalog-facts
description: >-
  Answers how an A2UI catalog is designed and extended in @agent-ui/a2ui. Use for "how do I add a
  component to the catalog", "why is this control uncatalogued", "what is our coverage policy", "why did this payload fail CATALOG", "what should
  this bindable prop be named". Covers the catalog row contract (typed properties + mapsTo, the
  {prop,event} mark, child model), the factory/resolution pattern (type → ui-* widget), the naming law (a bindable prop takes the control's own prop name), two-tier
  extensibility + the callableFrom clientOnly floor, security allowlist + conformance, and
  COVERAGE POLICY (whole-fleet vs subset, drift gates, seed-and-drain). NOT for
  the wire shape a component renders (a2ui-protocol-facts); NOT for corpus exemplars
  (a2ui-training-facts); NOT for system-prompt derivation (a2ui-chat-agent-facts); NOT for
  composing a payload (a2ui-composer) or catalog/renderer/factory SOURCE (a2ui-builder); NOT for
  grading a catalog row (a2ui-reviewer). ANSWERS from the cited repo corpus; it does not build.
disable-model-invocation: false
user-invocable: false
---

# a2ui-catalog-facts — the catalog world model

Explains how the `@agent-ui/a2ui` catalog layer is designed and extended, grounded in the shipped
source (`packages/agent-ui/a2ui/src/catalog/**`) and its specs/ADRs — so a design or review question
is answered from the actual contract, not from a generic A2UI tutorial. Six axes + provenance, each
in its own reference. **7 reference files** under `references/` (full map: `references/INDEX.md`).

| Ask | Load |
|---|---|
| What one catalog row declares — properties, the `{prop,event}` value mark, child model, `checks` | `references/component-definition-contract.md` |
| How a type becomes a `ui-*` control · how the renderer resolves a type to a widget · factory shape, the `accessorFactory`/bespoke split, the type↔factory bijection | `references/factory-and-widget-resolution.md` |
| How a project catalog registers (extend vs replace) with zero package edits · the `callableFrom` security floor | `references/two-tier-extensibility.md` |
| What a bindable prop is named and why (`checked` not `value`) · one-mark-per-component · type↔tag bijection · UAX-31 identifiers | `references/naming-law.md` |
| The coverage policy · why a control is uncatalogued · CI-silent vs fleet-derived gate · seed-and-drain | `references/coverage-policy-and-drift-gates.md` |
| Why a payload failed `CATALOG` · the security allowlist · conformance · validator parity | `references/security-allowlist-and-conformance.md` |
| Where a claim comes from (provenance, trust order) | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above and load ONLY the matching reference. The files are
   lookup structures, not linear reads: **Grep the term first** (a type name, `mapsTo`, `bindable`,
   `CATALOG`, `EXCLUSION_ALLOWLIST`), then Read that section with `offset`.
2. Answer on the **answer contract**: the claim + its cited source (`file:line` or ADR/SPEC clause)
   + the failure mode or caveat the design guards against. A catalog claim without its cited source
   is a guess; a claim without its failure mode is half an answer. Worked shape:
   > *"Should `Checkbox` bind `value` or `checked`?"* → naming-law ask → **`checked`** (the bindable
   > catalog prop is named by the control's own prop, ADR-0053 fork F2 / cl.1, matching
   > `factories.ts:217-228`). **Failure mode it prevents:** `ui-checkbox` carries BOTH a `value` prop
   > (submitted string `'on'`) and a `checked` boolean, so a Basic-aligned `value:boolean` row would
   > commit `'on'` into a boolean data path — the naming is a correctness contract, not a style choice.
3. **Verify a live claim before the user acts on it.** A `file:line` is a claim about the code at
   writing (2026-07-07); line numbers drift. If the user is about to add a row or change a factory,
   re-Grep the symbol in `packages/agent-ui/a2ui/src/catalog/**` and confirm it before recommending.

## Deviation doctrine

Every default in this pack carries its rationale, so a consumer knows when deviating is legal — a
catalog decision is a *default with a reason*, not a rule:

- The naming law YIELDS Basic-catalog alignment to the seam contract (ADR-0053 cl.1) — but where a
  control has no `value`/`checked` collision, aligning with Basic's name is the better default.
- The whole-fleet coverage policy admits ONE sanctioned exception: the gate-encoded
  `EXCLUSION_ALLOWLIST` with a recorded reason + citation (SPEC-N2). "Absent" without an allowlist
  entry is drift, not a decision.
- Deviation with a stated reason (recorded in an ADR / the §5.2 Notes) is design; deviation without
  one is drift. Judge a proposed row against the failure mode the existing shape prevents.

## Boundaries — this pack ANSWERS; it routes all making

- **Building or fixing renderer / catalog / factory SOURCE** (add the `catalog.json` row + the
  `factories.ts` factory, implement the validator, wire resolution) → the **`a2ui-builder`** agent.
- **Composing an actual A2UI payload** (the message stream / node shapes an agent emits against a
  catalog) → the **`a2ui-composer`** agent.
- **Reviewing / scoring a payload, a catalog row, or a corpus record** → the **`a2ui-reviewer`**
  agent (against `.claude/docs/rubrics/a2ui-catalog.md`).
- **Sibling knowledge packs** (route by name): the wire/message shape → `a2ui-protocol-facts`; corpus
  exemplars + record format → `a2ui-training-facts`; system-prompt derivation + the live-agent
  system → `a2ui-chat-agent-facts` (a CONSUMER of this pack).

Done when the answer carries the claim + its cited source (`file:line` or ADR/SPEC clause) + the
failure mode it guards against; a claim missing its source OR its failure mode is NOT done.

## Extending this pack

A missing axis, a stale reference (a spec revision, a new ADR, a drifted `file:line`), or "add X to
this pack" is authoring work — route to **[[pack-forge]]** (axis decomposition, grounded
research waves, the INDEX discipline). Re-run the affected axis's research wave, re-date its
reference + `sources.md`, and re-verify the stated file count; never bolt an uncited file on inline.

## Corpus of record

This pack's routing corpus (the positive/negative asks that test its triggering) is checked in at
`scripts/routing-corpus.json`.
