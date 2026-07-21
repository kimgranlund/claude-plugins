# ui-genres — changelog

## 2026-07-03 — excellence-campaign batch 4 fixes

- Routing corpus of record checked in at `scripts/routing-corpus.json` (10 positives / 10
  adversarial neighborhood negatives); routing eval F1 0.762 → 0.818 after the description fixes.
- Description: "habit" lexical hole closed — "habit tracker" added to the trigger quote,
  "tracking/quantified-self (habit apps, streaks)" in the genre enumeration.
- Genre count de-duplicated to one canon: `references/INDEX.md` owns the count; SKILL.md and this
  changelog cite it instead of restating an independent number.
- Harvest-provenance form verified intact (per-file `curated:` frontmatter + INDEX provenance
  block + changelog triangulation — the ratified pack provenance form); all 13 files carry their
  `curated:` line, no repair needed.

## 2026-07-02 — pack minted (ui-audit roadmap lever 4: world-model depth)
- Harvested the product-forge `product-genres` genre corpus (14 files) into `references/genres/`:
  13 genre files kept and curated, 1 dropped whole (`genre-metrics-map.md` — pure product-strategy);
  the live genre count is canonical in `references/INDEX.md`.
- Curation rule: product-strategy content dropped (every per-file metrics section, growth
  loops/PLG patterns, cold-start strategy, wrapper-vs-product and tool-vs-toy debates, metric-trap
  pitfalls and table rows); UI-convention content kept with original citations; each file's
  `curated:` frontmatter line records its cut. Load-bearing evidence folded inline where a kept
  pattern cited a dropped section (Signicat abandonment → finance; 90-9-1 → social; Google
  journey-length → travel).
- Authored net-new entry surface per [[knowledge-author]]: SKILL.md (consult table genre → file,
  consult procedure with worked example, ANSWERS-only boundaries) + `references/INDEX.md`.
