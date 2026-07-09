---
name: ui-patterns
description: >-
  Answers questions about common UI patterns — how software UIs are structured at macro (shells, templates)
  and micro (modules) level. Use when naming, choosing, or explaining a pattern: "what pattern is this",
  "name this screen type", "how should a data table / form / wizard behave", "what's the common layout for
  settings / search / a feed", "what modules does a dashboard / settings / landing page need", "what states does a screen need", "empty state best practice", "when is a modal wrong". Covers page templates (master-detail, canvas+inspector, wizard,
  feed, settings, board, chat), the module catalog (tables, forms, nav, pickers, toolbars, overlays,
  search, media, viz, maps, marketing), and screen-state grammar
  (ideal/empty/loading/partial/error). ANSWERS and names patterns — it does not apply or build them:
  applying to a layout is layout-decompose, building a module is component-author, the
  whole-product sweep is ui-audit. NOT for what a whole product genre conventionally includes
  (ui-genres).
user-invocable: false
disable-model-invocation: false
---

# ui-patterns — the pattern world model

Names and explains the recurring shapes of software UIs so design and review can reason from
vocabulary instead of taste. Two altitudes, one state grammar — each in its own reference:

| Ask | Load |
|---|---|
| Page/screen shape — "what template fits this job?", "name this screen type" | `references/macro-patterns.md` |
| Shell archetypes — the four ASCII wireframes (productivity-shell, saas-dashboard, marketing-site, mobile-app) | `references/archetype-*.md` (applied by [[layout-decompose]]) |
| Module behavior — "how should this table/form/picker/carousel/map work?" | `references/micro-patterns.md` |
| Screen states — empty/loading/partial/error, progressive disclosure | `references/state-patterns.md` |
| Provenance — where a pattern claim comes from | `references/sources.md` |

## Consult procedure

1. Classify the ask: template (macro) · module (micro) · state. Load only the matching reference —
   Grep for the pattern name, Read that section; the files are catalogs, not linear reads.
2. Answer with the pattern's **name, anatomy, when-it-fits, and its named failure mode** — a pattern
   recommendation without the failure mode it invites is half an answer. Worked shape:
   > *"Should settings be tabs or a sidebar?"* → macro ask → **settings** template: category nav
   > (sidebar past ~6 categories, tabs below), one save model product-wide; the failure to design
   > against is mixed save models — name it in the answer.
3. Route output work at the boundary: apply the template to a real screen → [[layout-decompose]]
   (which applies this pack's four archetype wireframes — owned here in `references/` — to concrete
   screens); build the module →
   [[component-author]]; check a whole product's conformance → [[ui-audit]]; the interaction
   invariants a module must clear → the verifier family ([[focus-verify]], [[perf-verify]],
   [[safety-verify]], [[i18n-verify]]).

## Boundaries

- **This skill answers; it does not generate.** No wireframes, no CSS, no component code — name the
  pattern, hand the making to the builder skills above.
- A pattern is a *default with a rationale*, not a rule: when a product deviates, judge the
  deviation against the failure mode the pattern exists to prevent — deviation with a reason is
  design, deviation without one is drift.
- Genre conventions (which patterns a product *category* expects) are owned by [[ui-genres]] —
  this pack says what a canonical table *is*; that one says whether THIS kind of product needs it.

## Extending this pack

A missing axis, a stale reference, or "add X to this pack" is authoring work — route to
[[knowledge-author]] (axis decomposition, grounded research waves, index discipline); never bolt
an uncited file onto the corpus inline.
