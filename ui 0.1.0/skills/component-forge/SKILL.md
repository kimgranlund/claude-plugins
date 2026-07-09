---
name: component-forge
description: >-
  Author a zero-dependency web component, or a composition of them, to the standard shape. Use when
  building or upgrading a custom element, control, or component module outside a framework: "build a
  web component / custom element", "make a checkbox / select / toolbar component", "design
  this component's API/anatomy", "add an overflow seam", "wrap a native element or
  form-associated?", "the tiers feel mis-cut", "my custom element renders empty after a re-render",
  "the icon-only button isn't square", "what icon/caret size on the ramp", "upgrade
  this jQuery dropdown" — tier, anatomy, API contract, composition, geometry, via Compose-then-Realize,
  machine-checked. NOT for ui-* controls in agent-ui / @agent-ui — "add a ui-button", "fix
  ui-select" (that repo's own build seat); NOT for app shells (layout-decompose);
  NOT for naming a UI pattern (ui-patterns); NOT for decomposing a feature/system (system-decompose);
  NOT for color ramps (palette-design); NOT for grading a component you didn't author (component-reviewer).
disable-model-invocation: false
user-invocable: true
---

# Component authoring — contract-first, geometry-checked

A component is **correct on two independent axes that walk the same hierarchy in opposite
directions**; authoring runs them as an order of operations, then reconciles at the contract:

- **Compose, whole → part** (the abstraction): tier → anatomy → API surface → composition.
- **Realize, part → whole** (the embodiment): geometry → element → platform semantics → interaction → fidelity.

A clean API can't offset off-ramp pixels and exact pixels can't hide a prop-exploded API — finish
both axes before calling it done. Route the mechanizable to `scripts/` (geometry is **arithmetic,
not judgment**); judge the rest.

## Procedure

1. **Tier + family** — place it on the **primitive → component → module** ladder and in its family
   (value-bearing control, overlay, display, container). The tier bounds the charter: a module owns a
   *seam*, not a loose pile of primitives. Families: `references/family-controls.md`,
   `references/family-overlays.md`.
2. **Anatomy** — name the parts and slots; design the anatomy to **nest** (a button is also a select
   trigger, a menu item, a modal action). Content model: host-as-grid vs a rendered cell.
3. **API surface** — attributes-as-API: attributes · properties · events · custom states, closed sets
   as literal enums, one source of truth per datum. Policy in `references/api-policy.md`; the
   card schema in `references/attributes-as-api.md`.
4. **Composition** — how it wires upward: the seam (e.g. priority + overflow, lowest-priority-first),
   slot presence, cross-component state, no self-margin. Recipes in
   `references/composition-patterns.md`. Where the module *sits* is the layout's job, not this skill's.
5. **Realize — geometry first** — five free values per size (height · icon · caret · font · spacer,
   the XS–2XL ramp); **everything else is derived** by the law *edge padding = (height − glyph) / 2*:
   asymmetric icon-vs-caret padding, the square icon-only cell, pill radius, composed insets. The law
   and ramp: `references/geometry-system.md`.
6. **Element + semantics** — autonomous custom element, signals-reactive, light DOM; role and states
   via `ElementInternals`; a value-bearing control is **FACE** (form-associated), never a wrapped
   native. Baseline features and fallbacks: `references/platform-baseline.md`.
7. **Interaction + fidelity** — APG keyboard (Enter + Space on buttons, arrows where roving), the
   native-parity budget: focus ring, `forced-colors`, mobile picker parity.
8. **Verify** (loop below) — write the contract card, run the checkers, fix, re-run.

## Validation loop (finalize only when clean)

Draft → check → fix → re-check:

1. **Geometry**: `python3 scripts/geometry-check.py <spec.json>` — derived paddings, square icon-only,
   composed insets, ramp integrity.
2. **Contract** (single component): `python3 scripts/component-contract-check.py <card.json>` — tier ·
   anatomy · API · states against the attributes-as-API schema.
3. **Composition** (module): `python3 scripts/composition-check.py <name.composition.json>` —
   tier-consistency · seam declared · overflow behavior · slot-presence grid · no self-margin.

Gate failures first; fix the component, not the check. For an adversarial grade of the finished
artifact, hand the contract card + spec JSONs to the `component-reviewer` agent (generator ≠ critic),
scored against the bound rubric — the leveled walk in `references/decomposition-method.md` (the walk
IS this skill's component rubric; there is no separate rubric file) — don't bless your own build.

## Update — re-derive, never patch

When a source this skill derives from changes, re-derive the affected references from the changed
source in the same change — never patch prose to sound current. The known drift axes: corpus
renames (sibling skill handles, `scripts/` paths), Baseline movement
(`references/platform-baseline.md` is dated June 2026 and WILL drift — re-verify its support
claims, then re-date), and checker semantics (each `scripts/*.py` docstring is the canon for what
its gate checks; the references summarize, the code wins).

## References & tools

| Path | Use when |
|---|---|
| `references/family-controls.md` / `family-overlays.md` | Classifying tier + family; family-specific invariants |
| `references/api-policy.md` + `attributes-as-api.md` | Designing the API surface; writing the contract card |
| `references/composition-patterns.md` | Wiring components into a module (seams, overflow, slots) |
| `references/geometry-system.md` | The ramp + the `(height − glyph)/2` law |
| `references/platform-baseline.md` | FACE/ElementInternals/custom-state support and fallbacks |
| `references/decomposition-method.md` | The two-axis method AND the bound rubric (the leveled walk) — the same two-plane engine as [[layout-decompose]] / [[system-decompose]] |
| `scripts/geometry-check.py` · `component-contract-check.py` · `composition-check.py` | The three mechanical gates |
| `[[system-decompose]]` | Decomposing the surrounding feature/screen before authoring the component |
| `[[rubric-forge]]` | Authoring a scoring rubric when a project needs its own component standard |

## Definition of done

- [ ] Tier + family named; anatomy nests; API card written and contract-check clean.
- [ ] Light DOM; semantics via `ElementInternals`; value-bearing ⇒ FACE; zero native form elements.
- [ ] Geometry derived from the ramp + law, geometry-check clean; icon-only square; insets compose.
- [ ] Module work: seam + overflow declared, composition-check clean.
- [ ] Keyboard per APG; focus ring + `forced-colors` + mobile parity budgeted.

**NOT done** when: a checker was skipped rather than run, a native form element survives anywhere,
geometry was eyeballed instead of derived from the ramp + law, or you blessed your own build — the
`component-reviewer` agent owns that verdict.
