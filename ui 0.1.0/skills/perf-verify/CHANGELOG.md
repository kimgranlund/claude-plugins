# Changelog

## 2026-07-03 — excellence-campaign batch 3 fixes
- `optimistic/eligibility.json`: dead `ui-sys-interaction` handle prose-ified ("reversible via a declared rollback target").
- `scripts/budget-check.py`: `RECIPE_WINDOWS` now accepts the canon's own composite tokens — `skeleton-or-spinner` (union of its legs, 300–3000ms) and `skeleton+subtle-continuous` (the skeleton window) — reconciling `thresholds/perception.json` with the gate; two card-visible judgments mechanized: `CANCEL_MISSING` (gate — progress-family recipe without `+cancel`, P95 ≥ 3s, not `cancelable:true`) and `SHAPE_MISMATCH` (advisory — skeleton-committed recipe on `outcomeShape: unknown`; `skeleton-or-spinner` exempt), with must-flag + reverse-control fixtures locked (all pre-existing fixtures stay green); docstring usage path fixed (`bin/` → `scripts/`).
- SKILL.md: p50-canon→P95-gate pivot stated in the mechanism section (the canon's upgrade rule made mechanical); the ladder windows now stated ONCE (the invariants table) — the gate table's `RECIPE_MISMATCH` row and the affordance-decision paragraph invoke it instead of restating; step-4 emit enum aligned with the checker's accepted recipe set; `SKIPPED` tier relabeled `skip` (house verdict vocabulary); `CANCEL_MISSING`/`SHAPE_MISMATCH` rows added to the gate table and the card section; Material & routing gains the maker row ([[component-author]] — recipe/reservation/streaming defects route there); Done/NOT-done predicate closes the file.
- Description: "performance budget", "Core Web Vitals (CWV)", "layout shift / jank", the surface form "cancel", and two quoted symptom phrases added; M2 routing corpus of record checked in at `scripts/routing-corpus.json`.

## 2026-07-02 — shakedown fixes
budget-check gains `operations[]` validation — `OP_UNCLASSIFIED` advisory for ops missing required fields, `RECIPE_MISMATCH` gate when a declared recipe's P95 falls outside its feedback-window (windows from the SKILL ladder: instant/none <100ms · busy <300ms · spinner 300–1000ms · skeleton 300–3000ms · progress ≥3s) — and an explicit `CWV: UNMEASURED` summary line for operations-only cards, all with locked fixtures; SKILL fallback paragraph + gate table synced (fallback no longer review-tier-only).

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `reasoning-about-perceived-performance` to `perf-verifier` per the `ui-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## 0.1.1 - 2026-05-06

- Expanded `skill.json` with typed-function fields: `domain`, `interface`, `invariants`, `composition`, and, where applicable, `adapters`.
- Added `$schema` declaration to `skill.json`.
- Inserted `## Typed Interface` section into `SKILL.md` documenting domain contract, input/output types, invariants, and downstream routing.
- Tagged as `typed-pipeline` consumer.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-02 — net-new re-author (family template)
Rebuilt 276→95 lines on the focus-verify template: kept the budget card + budget-check gate table (CWV defaults + poor lines), the feedback windows (~100ms instant, ~200ms route-loader hold, skeleton/spinner/optimistic thresholds), CLS 0.1 budget, image-dimension reservation, streaming posture, the cancellation contract, all data-dir pointers, and the [[safety-verify]]/[[ui-audit]] edges; killed Invocation/Ingestion/Decomposition ceremony, When-to-use/NOT sections, Rate-limiting factor, First-principles prose, the 9-step narrative procedure, the TS schema listings, and Typed Interface.
