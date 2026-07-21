# Changelog — component-author (formerly component-decomposer)

Format: [Keep a Changelog](https://keepachangelog.com/). Versioning: [SemVer](https://semver.org/).

## [0.2.0] — 2026-07-03

Excellence-campaign batch-3 fix wave — the un-run Update made visible, then run. Ledger:
`skills-audit/campaign/batch-3/component-author.findings.jsonl`.

### Changed
- **references/ re-derive sweep (A3)** — 13× `bin/*.py` → `scripts/*.py`; `component-decomposer` →
  component-author (self-naming); `layout-decomposer` → layout-decompose (references + the three
  checker docstrings and composition-check's up-handoff message); the dead `mermaid-decomposer`
  mention dropped; the phantom "`component-rubric.md` lives inline in this file" fixed to say what
  is true — the leveled walk IS the rubric; geometry-law canon ownership declared in
  `references/geometry-system.md` (general components: THIS file is canon; agent-ui's `geometry.md`
  is that repo's realization). All three checker selftests green after the sweep.
- **SKILL.md Update organ (S1)** — new "Update — re-derive, never patch" section naming the drift
  axes (corpus renames, Baseline movement — `platform-baseline.md` is dated and WILL drift, checker
  docstrings as gate canon); the leveled walk (`references/decomposition-method.md`) named as the
  bound rubric in the references table and the reviewer handoff.
- **Build handoff repointed (S5)** — the phantom `ui-build-components` peer
  (decomposition-method.md, family-controls.md) → the repo's component seat (agent-ui:
  `component-builder`) or the host/`system-builder` agent; the `component-reviewer` handoff now
  binds the rubric it scores against.
- **Description (M2/S2)** — added the geometry symptom ("my icon-only button isn't square — what
  padding"), the renders-empty symptom ("my custom element renders empty after a re-render"), and
  the ramp vocabulary (icon/caret sizes, XS–2XL size ramp); back-fences added toward ui-patterns,
  system-decompose, and palette-design; the layout fence now names layout-decompose. D1 trigger at
  char 89. routing_eval: F1 0.800 → 1.000 on the checked-in corpus.
- **Definition of done (L)** — closing NOT-done predicate added (skipped checker, surviving native
  form element, eyeballed geometry, self-blessed build).

### Added
- **`scripts/routing-corpus.json`** — the M2 test of record (12 positives / 10 negatives drawn from
  the graph neighbors' trigger vocabulary).

## [0.1.0] — 2026-06

Initial cut (predates this changelog; ported from the component-decomposer lineage). The
contract-first, geometry-checked authoring method: COMPOSE × REALIZE leveled walk with gated
joints, the `(height − glyph)/2` law + XS–2XL ramp (`geometry-check.py`), attributes-as-API
contract cards (`component-contract-check.py`), tier/seam composition cards
(`composition-check.py`), and the family/API/platform reference set.
