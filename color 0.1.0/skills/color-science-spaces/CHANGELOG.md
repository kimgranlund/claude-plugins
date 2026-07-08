# Changelog — color-science-spaces

## [1.0.0] — 2026-07-06 — Extraction from color-science

### Added

- Pack minted by splitting the 159-reference `color-science` pack into four independently-routed
  siblings (`color-science-spaces`, `color-science-perception`, `color-science-accessibility`,
  `color-science-materials`); this pack takes the computational layer — spaces & conversions,
  gamut & interpolation, HDR & tone mapping, CSS color syntax, image palettes & quantization, and
  the palette-generation/library catalog (72 files: 11 `contemporary/`, 61 `techniques/`).
- Net-new `SKILL.md` (identity → 6-axis consult index → Grep-first load discipline → worked
  consult → standing distinctions/defaults → demo/implementation pointer → boundaries → extending
  footer); `references/INDEX.md` trimmed to this pack's 72 rows, reorganized by axis, with the
  Online-Tools table filtered to pickers/palette/gamut tools per the split's routing rule.
- Every moved math file's "Implementation" section repointed from `src/…` to
  `../../../color-science-project-files/src/…`; three stale `../ARCHITECTURE.md` links repointed
  to `../../../color-science-project-files/ARCHITECTURE.md` (the file moved to the project-files
  root in the same extraction). Five cross-file citations that pointed at files which moved to
  sibling packs (ciecam02/fairchild → perception; apca-myndex-contrast → accessibility ×3;
  kubelka-munk → materials) repointed to their new pack paths.
- One cross-pack citation added (never duplicated): the colorandcontrast.com scrape's
  space-conversion chapter, which moved whole to `color-science-perception`.
- `scripts/routing-corpus.json` re-derived for this pack's own charter (20 positives across 4
  phrasing classes and the pack's 6 axes, including 2 of its canonical trigger evals — muddy
  gradients, palette sort — plus one axis-2 diagnostic positive; 21 negatives drawn adversarially
  from the live siblings: color-science-perception, color-science-accessibility,
  color-science-materials, color-theory, palette-design, color-verify).
- `evals/` slice: 2 of the pack's original trigger positives (muddy gradients, palette sort) +
  generic negatives, originally copied from `color-science-project-files/evals/trigger-evals.json`
  (since removed; in git history — `git show af81c64:skills/color-science/evals/trigger-evals.json`);
  task prompts 1 and 6, originally from that folder's `task-prompts.md` (since removed; in git
  history — `git show af81c64:skills/color-science/evals/task-prompts.md`).

### Fixed

- **2026-07-06, post skill-reviewer FIX-FIRST verdict**: the OKLCH-ramp trigger eval ("a 10-step
  OKLCH ramp for a warning color…") was mislabeled as a positive — it is a generation ask (build a
  ramp), which this answers-only pack's own description fences and which `palette-design` owns.
  Relabeled to a negative (attributed to palette-design) in both `scripts/routing-corpus.json` and
  `evals/trigger-evals.json`; replaced with a genuine axis-2 diagnostic positive ("why does my
  OKLCH ramp clip at high chroma near yellow") in both files to hold the corpus balance.
- Dangling present-tense references to `color-science-project-files/evals/` (deleted by T6 once
  every prompt/trigger had landed in a pack, per A2) corrected to note the path is historical.

Prior history (the full pre-split corpus, the TypeScript library, and the demo site) lives in
[`color-science-project-files/CHANGELOG.md`](../color-science-project-files/CHANGELOG.md).
