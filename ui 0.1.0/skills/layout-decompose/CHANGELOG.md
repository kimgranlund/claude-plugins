# Changelog — layout-decompose (formerly layout-decomposer)

Format: [Keep a Changelog](https://keepachangelog.com/). Versioning: [SemVer](https://semver.org/).

## 0.2.0 — beta

Promoted to beta as part of the marketplace **v0.2.0** milestone (see the root CHANGELOG). This cycle the skill gained a checked-in, sibling-collision-tested routing-eval corpus, an adversarial-review hardening pass (fixes locked as selftest fixtures), and a worked `examples/walkthrough.md` (a red→green bin proof).

## [0.1.0] — 2026-06-15

Initial cut. The two-axis UI-decomposition technique extracted from the dev-factory cockpit + design-rubric work.

### Added
- **The two-axis method** (`references/decomposition-method.md`) — OUTSIDE-IN (macro→micro: frame → regions →
  groups → atoms) × INSIDE-OUT (core→whole: actions → bindings → feedback → coherence), the gated rubric
  (A1·A2·B1·B2 `[gate]`, the rest `[review]`), the "pretty-but-dead vs functional-but-unreadable" framing, and the
  DECOMPOSE / DESIGN / GRADE workflows.
- **Four archetype references with ASCII wireframes** — `productivity-shell` (the cockpit we built),
  `saas-dashboard` (clamshell · sidebar/section-nav · breadcrumbs · page-header · table/data/settings content ·
  modal/drawer/snackbar), `marketing-site` (homepage section stack + feature/about/pricing/lead-gen/blog
  templates), `mobile-app` (tabbed view stack · sheets · modality · FAB · workflows). Each carries a named-pattern
  vocabulary + per-archetype outside-in / inside-out notes.
- `SKILL.md` table-of-contents with Quick Start, the archetype-selection table, §SelfAudit (structure-not-skin;
  artifact-as-data; gates-before-reviews; two-scores-never-one), and a Verify Target.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-03 — excellence-campaign batch 1 fixes

**Corrects the record on 0.2.0:** the checked-in routing-eval corpus and the selftest fixtures that
entry claims were **dropped in the 2026-07-01 plugin port** — neither survived into this tree. The
routing corpus is now restored (rebuilt, sibling-collision-tested) at `scripts/routing-corpus.json`;
the selftest fixtures remain absent. The 0.2.0 entry stands unedited as history; this entry corrects it.

Also in this batch:
- Description: two up-fences added (whole-product sweep → ui-audit; abstract pattern naming → ui-patterns)
  and two symptom-family triggers ("the screen looks clean but nothing on it does anything", "every action
  works but it's all one giant stacked column").
- Defect-quadrant enum unified: the method file's "REBUILD" cell renamed to **broken**, SKILL.md's canon.
- Shippable floor stated once: canon is `references/decomposition-method.md` §Scoring; SKILL.md and the
  quadrant now point there.
- §SelfAudit argues the no-checker exception: screenshots/prose resist mechanization by construction;
  live-DOM A1-frame facts route to ui-audit's browser probe.
