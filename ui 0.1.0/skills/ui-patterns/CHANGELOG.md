# Changelog — ui-patterns

## 2026-07-07 — productivity-shell hardened from a shipped implementation

- `references/archetype-productivity-shell.md`: added a **Sectioned editor** variant (N facets of one
  document; a section switcher re-routes pane/canvas bodies over an invariant frame — distinct from
  multi-canvas/tabs), a wireframe caption bridging to it + the second (artifact-preview) `◐`, and a
  **Hardening notes** block (live-refresh vs full render + one-undo-per-drag, interaction continuity
  for focus/scroll/overlay, ephemeral-vs-persisted state, relocating collapsed-rail affordance).
- Depth deliberately kept OUT of the card: the full behavior contract (states, edges, acceptance
  criteria) lives in the design-system-agnostic **`app-shell-patterns` SPEC** (nonoun-color-tokens repo;
  reference implementation of this archetype), cross-linked from the Hardening notes. layout-decompose's
  `decomposition-method.md` unchanged — it references the card and these additions don't drift it.

## 2026-07-03 — excellence-campaign batch 4 cross-filed fixes (from the ui-genres review)

- Description: genre-altitude fence added — "NOT for what a whole product genre conventionally
  includes (ui-genres)". The trigger "what modules does a dashboard need" (product-inventory
  framing — genre territory) recast to module-behavior phrasing: "how should a dashboard's
  KPI-tile or chart module behave". Routing eval held (F1 0.769, all prior positives intact).

## 2026-07-03 — excellence-campaign batch 1 fixes

- **Archetype ownership made unambiguous** (one canon): the four shell archetypes LIVE in this
  pack's `references/archetype-*.md` and are APPLIED by layout-decompose. Fixed the three statements
  that contradicted this — `references/sources.md` (claimed they live in layout-decompose),
  `references/macro-patterns.md` §dashboard page ("layout-decompose's saas-dashboard archetype"),
  and SKILL.md's Consult-procedure routing clause.
- Each `references/archetype-*.md` now opens with a hosting note: the embedded A1–A5/B1–B5 notes
  are owned by layout-decompose's method (`references/decomposition-method.md` there); this pack
  hosts them for one-stop reading.
- Description: triggers added ("name this screen type", "what states does a screen need");
  component-author fence widened to "building or modifying the module".
- Routing corpus of record checked in at `scripts/routing-corpus.json`.
