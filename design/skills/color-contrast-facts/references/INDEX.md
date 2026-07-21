# Color Science Accessibility References

Curated transcripts, notes, and source material for the `color-contrast-facts` pack —
contrast standards and color-vision deficiency. Extracted 2026-07-06 from the 159-file
`color-science` pack (now `color-science-project-files`, a non-skill archive); the other three
sibling packs (`color-space-facts`, `color-perception-facts`, `physical-color-facts`) took
the computational, appearance-science, and physical/naming corpora respectively.

**8 files**, organized by ask-axis below. Subdirs preserve the original taxonomy: `contemporary/`
(3 — positioning and survey pieces), `techniques/` (5 — formulas, tables, and TS-paired math).

## Contrast standards — APCA vs WCAG 2.2, luminance, thresholds, pair counts

<!-- markdownlint-disable MD060 -->

| File | Summary | Source |
| --- | --- | --- |
| [Relative Luminance & WCAG Contrast](techniques/relative-luminance-derivation.md) | Y from XYZ / linear / encoded sRGB. The $(L_1 + 0.05) / (L_2 + 0.05)$ contrast ratio formula. AA / AAA thresholds. Why APCA is better. Paired with `src/metrics/luminance.ts`. | [WCAG 2.2](https://www.w3.org/TR/WCAG22/#contrast-minimum) |
| [WCAG 2.2 — Current Legal Floor](techniques/wcag-2-2-current-legal-floor.md) | WCAG 2.2 (Recommendation since Oct 2023) is what regulations cite (EAA, Section 508, AODA) — the legal floor, not the design standard; prefer APCA for design quality. The three contrast-relevant new SCs. | [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| [APCA L^c Formula](techniques/apca-lc-formula.md) | Polarity-sensitive lightness contrast. Simplified 2.4 gamma, near-black soft clamp, BoW/WoB polarity branches, readability tiers (Bronze Simple Mode). Paired with `src/metrics/apca.ts`. | [APCA-W3](https://github.com/Myndex/apca-w3) |
| [APCA & Myndex](techniques/apca-myndex-contrast.md) | The WCAG 3 contrast algorithm. Polarity-sensitive, spatial frequency aware, font size/weight tables. apca-w3, Bridge-PCA, DeltaPhiStar, CVD simulator. "Please Stop Using Grey Text." | [GitHub](https://github.com/Myndex/SAPC-APCA) |
| [Accessible Color Pair Counts](contemporary/accessible-color-combinations-count.md) | @mrmrs\_ research-survey: a Rust brute-force run over ~281T hex pairs found that only 11.98% pass WCAG 4.5:1 (AA) and 0.08% pass APCA 90. APCA is far more restrictive than WCAG at comparable thresholds. | [@mrmrs\_](https://x.com/mrmrs_/status/2034403566040088832) |

## CVD — Brettel/Viénot/Machado, canonical defaults, confusion, safe pairs, opponent basis

| File | Summary | Source |
| --- | --- | --- |
| [CVD Simulation Algorithms](techniques/cvd-simulation-algorithms.md) | Brettel 1997, Viénot 1999, Machado 2009 (severity-parameterized). The modern default for CVD simulation; what Chrome DevTools uses. Paired with `src/cvd/machado-2009.ts`. | [Machado 2009](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html) |
| [CVD Simulation — Canonical Algorithms](contemporary/cvd-simulation-canonical.md) | Positioning of the three canonical CVD algorithms — Brettel 1997 (dichromacy projection), Viénot 1999 (simple matrix), Machado 2009 (severity-parameterized, the modern default). Recommends deuteranopia at 0.6 severity for first-pass review. | [Machado 2009](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html) |
| [Opponent Process & Color Blindness](contemporary/opponent-process-color-blindness.md) | 4 psychological primaries on 2 axes (red↔green, yellow↔blue). CVD = losing one axis. Orange↔blue is most accessible pair — works for BOTH red-green AND yellow-blue blindness. | [Color Nerd](https://www.youtube.com/watch?v=DO0kTNxEFrs) |

## Low-vision & readable color choices

No file in this pack is exclusive to this axis — it is a consult lens over the contrast-standards
files above (APCA L^c tiers and WCAG thresholds ARE the readable-color-choice guidance), read
through a low-vision lens rather than a general-legibility one. `lettering-facts`'s
low-vision reference shares this axis and cites
[APCA L^c Formula](techniques/apca-lc-formula.md) here rather than duplicating it.

<!-- markdownlint-enable MD060 -->

## Cited from color-space-facts (the one intentional cross-pack consult)

WCAG 3 is still a Working Draft; its eventual contrast algorithm is APCA-derived. Rather than
duplicate spec-status tracking in this pack, a WCAG-3-status ask routes to spaces' own
verify-current-status file:

| File (in color-space-facts) | Why this pack cites it |
| --- | --- |
| *CSS Color 2026 — Spec & Baseline Snapshot* (in `color-space-facts`) | Dated Baseline/spec-status map, incl. WCAG 3 Working Draft status — never duplicated here, always cited |

## Source-tracing rule

Every claim traces to one of the 8 files above; an answer this corpus cannot back is general
knowledge and must be flagged as such when given.
