# Changelog — color-theory

## [1.0.2] — 2026-07-06 — Repathed for the color-science-* split

### Changed

- **INDEX §Cited-from** repathed: the 5 straddle-file links (Albers, Goethe edge colors, opponent
  process, Koenderink warm/cool, green-warm-or-cool) now point at their new homes — the plain
  `color-science` handle disappeared in this refactor, replaced by `color-science-perception`,
  `color-science-spaces`, and `color-science-accessibility` respectively (D6 straddle rule
  unchanged, only the target paths moved).
- **SKILL.md**: the NOT-clause, sibling-identity line, straddle index row, contrast/numbers exits,
  and mechanism boundary all repointed from the single `[[color-science]]` handle to the four
  named packs, by meaning (see color-science-extraction-rewire.md for the full map).
- **routing-corpus.json**: `siblings_in_repo`/negative attributions re-aimed from `color-science`
  to the real competitors — `color-science-perception`, `color-science-spaces`,
  `color-science-accessibility`.

## [1.0.1] — 2026-07-03 — Deep-review fixes: PDF truth, count canon, routing corpus

### Fixed

- **INDEX §Source PDFs told the truth-shape wrong**: it claimed 7 PDFs "gitignored on disk" —
  none exist anywhere in the pack. Section reworded to "not shipped with this pack; canonical at
  the cited URLs / archive.org" and every dangling PDF link delinked: the 7 section rows plus the
  per-file "Local PDF" pointers (schloss-palmer, gencolor, designing-programmes, pleasing-colour,
  two-color-combinations, what-happened-to-indigo, oldest-color-wheel-with-magenta,
  ostwald-color-wheel, gerritsen header).
- **Every INDEX row now carries a real source link**: GenColor row → DOI + arXiv (was "(PDF
  gitignored; see paper)"); pleasing-colour row → "original (unpublished local report; the
  reference file is the canonical record)" (was a bare "local PDF").
- **Count canon named**: `references/INDEX.md` owns the file count (28); SKILL.md and this log
  cite it rather than restating independently.

### Changed

- **Routing corpus checked in** at `scripts/routing-corpus.json` (12 positives across four
  phrasing classes / 13 negatives drawn from color-science, palette-design, color-verify,
  ui-patterns, knowledge-author).
- **Description**: "dominant/accent" token pair added (both review misses hit that hole);
  "Itten's seven contrasts" and "vibe" added to the positive vocabulary to counterbalance the
  contrast/APCA/WCAG fence — the fence itself untouched.
- **SKILL.md**: deviation doctrine declared (corrections are defaults-with-rationale — when the
  folk rule remains right for the job, say so and cite why); Boundaries moved to close the file.

## [1.0.0] — 2026-07-02 — Extraction from color-science

### Added

- Pack minted by splitting the 190-reference `color-science` pack along the judgment boundary:
  **color-science** keeps perception/math/standards ("what is perceptually true");
  **color-theory** takes aesthetics/meaning/history ("what reads as intended").
- 28 reference files moved (`mv`, subdir structure preserved): 12 `historical/` (color wheels and
  theorists — Ostwald, Moses Harris, Lewis, Sawyer, Cheskin, Itten critique; colorists Reilly,
  Bardwell, Parkinson), 5 `contemporary/` (Gerstner's Designing Programmes, Schloss & Palmer,
  GenColor color-concept association, Gerritsen wheel, palette-sorting report), 11 `techniques/`
  (harmony corpus — Divers character-first, Farges, Duru, pro-color-harmonies; Aladdin color
  analysis, Drawing Codex proportion, Pixel Parmesan, Mulvenna, Procreate wheel critique, The
  Futur playlist).
- Net-new `SKILL.md` entry surface (identity → consult table → worked consult → boundaries) and
  `references/INDEX.md` organized by ask-axis (harmony · wheel/history · programmes · meaning).
- Straddle files (perceptual mechanism + aesthetic consequence) stay in color-science and are
  cited from this pack's INDEX, never duplicated: Albers' Interaction of Color (simultaneous
  contrast), Goethe edge colors, opponent process, the warm/cool spectral files.
- Cross-references wired: [[color-science]] ↔ [[color-theory]] mutual boundary edges;
  [[color-verify]] and [[palette-design]] descriptions now route harmony/meaning here.
