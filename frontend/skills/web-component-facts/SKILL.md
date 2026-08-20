---
name: web-component-facts
description: >-
  Answers Web Components platform facts — light-DOM lifecycle (upgrade races, SSR shim scars,
  NOOP_INTERNALS), stamping strategies + keyed reconcile (adopt-or-stamp, logicalChildren, the
  display:contents trap), traits as a host-agnostic primitive vs. mixin-flattened-this,
  ElementInternals form association + a11y, the attributes-as-API grammar, and per-control
  testing. Use for "why didn't attributeChangedCallback replay on upgrade", "static parts vs
  tagged template vs imperative", "is a trait a mixin", "what test files does a control need".
  ANSWERS platform facts; NOT the build PROCEDURE (make-component), NOT reactivity MECHANISM
  (reactivity-facts).
user-invocable: false
disable-model-invocation: false
---

# web-component-facts — the Web Components platform world model

Answers how a zero-dependency web component actually behaves at the platform level — lifecycle
and upgrade mechanics, child-stamping strategies, the trait composition primitive, form/a11y
association, the attribute API grammar, and per-control test coverage — from a corpus grounded in
live source reads across two repos (gen-ui-kit, agent-ui) plus a dated field-report doctrine ledger
and one contrast finding (ultimate-tokens), not general custom-elements folklore.

| Ask | Load |
|---|---|
| Upgrade races, SSR shim scars, `NOOP_INTERNALS`, the base element's own lifecycle | `references/lifecycle-and-upgrade.md` |
| Which of the three stamping strategies fits; adopt-or-stamp; `logicalChildren`/`logicalSlotted`; the `display:contents` trap; keyed reconcile | `references/stamping-and-reconcile.md` |
| Is a trait a mixin; the host-agnostic factory/function shape; the mixin-flattened-`this` contrast | `references/traits-primitive.md` |
| `ElementInternals` form association, constraint validation, the host-as-control a11y pattern | `references/form-and-a11y.md` |
| The attributes-as-API grammar: yaml SoT, no-shadowing, boolean flip rule, null-over-sentinels, reflect rules, `data-*` tiers, the closed event vocabulary | `references/attributes-as-api-grammar.md` |
| The per-control test quintet, jsdom-vs-browser, architectural-boundary tests | `references/control-testing.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask against the six axes above; load only the matching reference (or
   `sources.md` for provenance). Hunting one specific claim inside a file: Grep for the term first
   rather than reading the whole file.
2. Answer on the contract: **claim + cited file:line/report + the grounding marker
   ([verified]/[incident])**. Worked shape:
   > *"Why does this custom element render an empty label after SSR?"* → upgrade-race ask →
   `lifecycle-and-upgrade.md` — the spec's own upgrade algorithm requires replaying
   `attributeChangedCallback` for every pre-existing attribute before `connectedCallback`, but
   several SSR/test DOM shims skip that replay — a real, confirmed gap [incident], not a
   hypothetical.
3. State which axis the answer draws from, and its grounding marker — never present a corpus
   citation as live-verified-today code if `sources.md`'s own disclosure (including its one
   same-day report-correction case) says otherwise.
4. Route build-procedure or reactivity-mechanism work at the boundary (below) — this pack answers
   platform facts, it never authors a component or explains a reactivity kernel.

## Boundaries

- **This skill answers Web Components PLATFORM facts and scars; it does not build a component.**
  "Build a web component", "make a checkbox/select/toolbar", "design this component's API/anatomy"
  is `make-component`'s law — that skill is the build PROCEDURE (tier, anatomy, API surface,
  geometry, taste gate); this pack is the facts/scars corpus a builder consults ALONGSIDE that
  procedure, never a substitute for it. A question naming a build verb (build/make/author/design
  this component) is `make-component`'s; a question naming a platform mechanism, scar, or
  incident (upgrade race, SSR shim, the display:contents trap, a mixin contrast) is this pack's.
- **Reactive STAMPING internals (which strategy re-renders when, keyed reconcile as a mechanism)
  are this pack's law; the reactivity KERNEL that decides WHEN a re-stamp fires belongs to
  `reactivity-facts`.** "Static parts vs tagged template vs imperative," "why did this slot miss a
  conditional child," "adopt-or-stamp" are this pack's; "why did this effect refire twice," "per-
  part reactivity vs whole-component re-render," "computed vs signal vs effect" are
  `reactivity-facts`' — a question naming a kernel primitive (signal/computed/effect/scope) is
  `reactivity-facts`'; a question naming a stamping strategy or DOM-child mechanism is this pack's.
- **UI pattern naming and the screen-state grammar** (loading/empty/error) stay
  `ui-pattern-facts`' law — unrelated territory.
- **How data gets wired into a live element** (streaming stack, bridge protocol, no-DI substitutes)
  is `data-wiring-facts`' law, unrelated to how the element's own DOM/lifecycle mechanics work.
- **Production component code, a builder-side taste decision, or a new control from scratch** →
  `make-component` — this pack explains why the platform behaves a certain way; it does not write
  the component or judge its finished anatomy (that's `component-checker`'s verdict).

## Extending this pack

Extension: governed by [[make-pack]]
