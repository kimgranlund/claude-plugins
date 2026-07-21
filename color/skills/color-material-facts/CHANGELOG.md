# Changelog — color-science-materials

## [1.0.0] — 2026-07-06 — Extraction from color-science

### Added

- Pack minted by splitting the 159-reference `color-science` pack into four sibling packs; this
  pack takes the physical-color & color-naming corpus ("what a pigment does, and what a color is
  called"); prior history lives in `color-science-project-files/CHANGELOG.md` (the renamed,
  now-non-skill archive that keeps `src/`, `examples/`, and the full repo history).
- 30 reference files moved (subdir structure preserved): 4 `historical/`
  (caravaggio-copper-resinate-greens, color-definitions-webster-iscc, munsell-hue-value-chroma,
  ridgway-color-standards-1912), 7 `contemporary/` (atlas-of-rare-familiar-colour,
  golden-paint-making, hunt-pointer-measuring-colour, iridescence-thin-film-interference,
  iridescent-color-math, kim-heer-color-naming-across-languages,
  pointers-gamut-real-surface-colors), and 19 `techniques/` (pigment-mixing tools and datasets —
  kubelka-munk-single-constant, spectraljs-pigment-mixing, imaginary-pigments-mixbox,
  focalpaint-impossible-pigments, color-mixing-hexaflexagon-paths,
  color-triangle-jinjer-markley, colordisk-trillium, skin-tones-color-mixing-youthforia,
  paint-mixing-lecture-ufv; reproduction — icc-profile-color-management,
  screen-to-print-colour-fidelity, pointers-gamut-math; naming — color-name-lists,
  jaffer-color-name-dictionaries, jaffer-resene-paint-colours,
  jaffer-winsor-newton-watercolours, colornerd-paint-manufacturer-swatches,
  color-description-library, digital-color-fidget).
- Net-new `SKILL.md` entry surface (identity → consult table → worked blue+yellow-paint-mixing
  consult → standing distinction "pigment mixing ≠ RGB averaging" → boundaries),
  `references/INDEX.md` (3 axes: pigment & mixing physics, reproduction & measurement, naming
  standards & datasets; two intentional cross-pack citation rows to `color-science-perception`'s
  huevaluechroma ch05/ch06 subtractive-mixing chapters, never duplicated; an Online Tools section
  carrying the naming-flavored rows split out of the old combined INDEX — color.pizza API,
  147colors, the ISCC-NBS Centroid Picker, handprint.com; the Source-PDF provenance rows for
  ISCC-NBS/Kelly & Judd/Laurie/Painting-Materials/Schweizer), `scripts/routing-corpus.json` (12
  positives across four phrasing classes spanning paint mixing, print-vs-screen/ICC, naming
  systems, and iridescence/Pointer's gamut; 12 negatives drawn adversarially from the other three
  color-science-* packs, color-theory, and palette-design — routing-eval measures
  precision 1.000 / recall 0.833 / F1 0.909; the two recall misses are hyphenated-compound
  tokenizer artifacts, read and confirmed as proxy limits, not routing gaps), and an `evals/`
  slice (trigger positives #2/#3/#6 — print-proof mismatch, bird-book naming, blue+yellow paint —
  plus the 18 generic negatives, and task prompts 2–4).
- Two moved math files' relative links repointed off the old flat `color-science` tree:
  `kubelka-munk-single-constant.md`'s Implementation section (`src/…` →
  `../../../color-science-project-files/src/…`) and its `spectral-to-xyz-integration.md`
  companion cite (now in `color-science-spaces`); `pointers-gamut-math.md`'s
  `cielab-xyz-conversion.md` and `xyz-rgb-conversion-matrices.md` companion cites (both now in
  `color-science-spaces`) — the src/ ↔ math-reference co-versioning contract
  (`color-science-project-files/ARCHITECTURE.md` Decision 8) survives the move unchanged.
