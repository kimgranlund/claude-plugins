# Changelog

## 2026-07-03 — excellence-campaign batch-3 fixes (G2)
A3: bulk undo-toast numbers reconciled to ONE canon — `friction/recipes.json` now says ≥ 6s (12–30s for bulk-destructive) with the bulk rationale in-file (a bulk mistake is noticed while scanning the result set, not at click time), and the SKILL invariants row cites the file as the durations canon; safety-check usage lines bin/→scripts/; orphaned INV-1/INV-4/INV-5/INV-7 references stripped from checker comments/messages (content kept — the re-authored SKILL never had that numbering). A4: `matrix.json` gains a declared `default` fallback ("uncovered coordinates take the nearest higher-friction neighbor's treatment — step reversibility toward irreversible, then blast upward; never downward") + sparsity note; SKILL ladder states the rule. Description gains verbatim safety / delete-send-publish-revoke / two-person-approval triggers plus two fences — flow-decompose (cross-screen recovery/resume, reciprocating its review) and ui-audit (fenceless-grab fix surfaced by the eval); routing F1 0.727→0.800, corpus of record at `scripts/routing-corpus.json`. Card section states the never-carries (judgment-tier) clause; Material & routing gains the [[component-author]] fix-owner row; Done/NOT-done predicate closes the file; outbound one-way fences (→color-science, →component-author) filed as accepted no-risk in the batch-3 ledger.

## 2026-07-02 — shakedown fixes
blast-reversibility/matrix.json documents the two reversibility species (`user-reversible-in-app` vs `ops-reversible` — payments are ops-reversible; review-then-commit is their norm) via a `reversibilitySpecies` axis + species note; safety-check (rule is hardcoded, not matrix-read) gains the `ops_reversible: true` card field that downgrades NO_UNDO to an advisory note, with locked fixtures; SKILL card + gate table synced.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `reasoning-about-safety-and-destructive-affordances` to `safety-verifier` per the `ui-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## 0.1.1 - 2026-05-06

- Expanded `skill.json` with typed-function fields: `domain`, `interface`, `invariants`, `composition`, and, where applicable, `adapters`.
- Added `$schema` declaration to `skill.json`.
- Inserted `## Typed Interface` section into `SKILL.md` documenting domain contract, input/output types, invariants, and downstream routing.
- Tagged as `typed-pipeline` consumer.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-02 — net-new re-author (family template)
Rebuilt 270→104 lines on the focus-verify template: kept the action card + safety-check gate table, the blast×reversibility plane with its friction ladder (undo-toast → confirm → type-to-confirm → re-auth → 2-person, with coordinates), the numbers (undo ≥6s / bulk 12–30s, re-auth ≤15min), recall-window and bulk preview/dry-run rules, audit-event requirements, all data-dir pointers, and the [[focus-verify]]/[[ui-audit]] edges; killed Invocation/Ingestion/Decomposition ceremony, When-to-use/NOT sections, Rate-limiting factor, First-principles prose, the 9-step narrative procedure, the TS schema listings, and Typed Interface.
