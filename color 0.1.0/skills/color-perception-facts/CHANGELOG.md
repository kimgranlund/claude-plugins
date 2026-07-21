# Changelog — color-science-perception

## [1.0.0] — 2026-07-06 — Extraction from color-science

### Added

- Pack minted by splitting the `color-science` corpus into four sibling packs
  (`color-science-spaces`, `color-science-perception`, `color-science-accessibility`,
  `color-science-materials`); this pack takes vision and color-appearance science — what the eye
  and brain do with light, independent of any particular color space's math. Prior history lives in
  `color-science-project-files/CHANGELOG.md`.
- 49 reference files moved (subdir structure preserved): 1 `historical/` (Albers — Interaction of
  Color), 47 `contemporary/` (25 root files — terminology, vision mechanics, appearance science,
  Briggs lectures, philosophy/education — plus the two whole-site scrapes: `huevaluechroma/`, 14
  files, and `colorandcontrast/`, 8 files), 1 `techniques/` (MacAdam Ellipses — Math, the math
  companion to `contemporary/macadam-ellipses-jnd.md`).
- Net-new `SKILL.md` entry surface (identity → consult index → load discipline → worked consult →
  standing distinctions → straddle rule → boundaries → knowledge-author footer) and
  `references/INDEX.md` organized by ask-axis (terminology & dimensions · vision mechanics ·
  appearance science · textbook layer).
- Straddle files (perceptual mechanism cited under an aesthetic claim) stay here and are cited from
  `color-theory`'s INDEX, never duplicated: Albers' Interaction of Color (simultaneous contrast),
  the Koenderink warm/cool series, and Is Green Warm or Cool — three of the family's five straddle
  files; the other two, opponent-process-color-blindness (CVD-safe pairs) and
  goethe-edge-colors-design-hack (gradient math), live in `color-science-accessibility` and
  `color-science-spaces` respectively; this pack's scrapes cover opponent process as vision science.
- `scripts/routing-corpus.json` re-derived for this pack's charter: 14 positives across four
  phrasing classes (imperative/diagnostic/symptom/indirect), 13 negatives drawn adversarially from
  `color-science-spaces`, `color-science-accessibility`, `color-science-materials`, `color-theory`,
  and `color-verify`.
- `evals/` slice split from `color-science-project-files/evals/`: trigger positives #5 (HSL
  saturation ≠ vivid), #9 (perceptual terminology), #28 (JPEG 4:2:0 subsampling) plus the 18 generic
  negatives; task prompts 7 (perceptual terminology) and 8 (image compression and vision).
- Two internal cross-references in `techniques/macadam-ellipses-math.md` (to `oklab-xyz-math.md` and
  `delta-e-formulas.md`, both companions that moved to `color-science-spaces`) repointed to their
  new cross-pack location rather than left dangling.

### Notes

- R4 (THIRD_PARTY_NOTICES check): `color-science-project-files/THIRD_PARTY_NOTICES.md` carries only
  a repository-wide generic notice and names no scrape specifically — no pack-specific notice rows
  were carried into this pack's INDEX; see INDEX.md's "Third-party notices" section for the
  disposition.
