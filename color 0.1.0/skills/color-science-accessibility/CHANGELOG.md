# Changelog — color-science-accessibility

## [1.0.0] — 2026-07-06 — Extraction from color-science

### Added

- Pack minted by splitting the 159-reference `color-science` pack into four sibling packs; this
  pack takes the contrast-standards & color-vision-deficiency corpus ("what makes color usable");
  prior history lives in `color-science-project-files/CHANGELOG.md` (the renamed, now-non-skill
  archive that keeps `src/`, `examples/`, and the full repo history).
- 8 reference files moved (subdir structure preserved): 3 `contemporary/`
  (accessible-color-combinations-count, cvd-simulation-canonical, opponent-process-color-blindness)
  and 5 `techniques/` (apca-lc-formula, apca-myndex-contrast, wcag-2-2-current-legal-floor,
  relative-luminance-derivation, cvd-simulation-algorithms).
- Net-new `SKILL.md` entry surface (identity → consult table → worked APCA-vs-WCAG consult →
  standing defaults → boundaries), `references/INDEX.md` (3 axes: contrast standards, CVD,
  low-vision-as-a-lens; one intentional cross-pack citation to `color-science-spaces`'s CSS Color
  2026 snapshot for WCAG 3 status), `scripts/routing-corpus.json` (14 positives across four
  phrasing classes, 13 negatives drawn adversarially from color-verify, focus-verify, the other
  three color-science-* packs, palette-design, and color-theory), and an `evals/` slice (the
  calm-vs-triadic boundary trigger + the 18 generic negatives + task prompt 5).
- Three moved math files' Implementation sections repointed from `src/…` to
  `../../../color-science-project-files/src/…` (apca-lc-formula, relative-luminance-derivation,
  cvd-simulation-algorithms) — the src/ ↔ math-reference co-versioning contract
  (`color-science-project-files/ARCHITECTURE.md` Decision 8) survives the move unchanged.
