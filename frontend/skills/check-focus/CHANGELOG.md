# Changelog

## 2026-07-03 — excellence-campaign batch 1 fixes
Calibration deep-review fixes against `skills-audit/references/standard-of-excellence.md` v1 (ledger: `skills-audit/campaign/batch-1/focus-verify.findings.jsonl`):
- **A3 (template-escalated)** the 3:1 ring-contrast floor was mis-attributed to SC 2.4.11 (Focus Not Obscured); corrected to **SC 1.4.11** (Non-text Contrast) in SKILL.md, `scripts/focus-check.py` (docstring + RING_LOW_CONTRAST message), and `focus-ring/recipes.json` — whose header also stops claiming a recipe can "satisfy" 2.4.11 (a layout property), and whose `outline: none` refused-pattern now cites SC 2.4.7. Family sweep (i18n-/perf-/safety-/color-verify): color-verify's lone SC cite (1.4.11, line 73) verified correct; the others carry no SC citations — no inherited defects.
- **A3** "offset ≈ half the element radius" gloss replaced by the `offsets/per-surface.json` truth (2px none/sm/md · 3px lg · 4px xl); focus-check docstring's `bin/` and "focus-verifier" corrected to `scripts/` and focus-verify; Invariants section now names `targets/minimums.json` + `focus-ring/recipes.json` as canon (the table is the summary).
- **N2** description leads with "Verify … and prescribe the compliant values"; step 4's per-role tokens reframed as the verdict's prescribed-values payload, not a generation product.
- **N3** breadth-under-one-stem citation added (one `*.focus.json` card carries ring + target + keys; keep-as-is chosen per the standard's N3).
- **M2/S2** triggers added ("modal/dialog focus trap and restore", "Escape and arrow keys per role", "the focus ring is invisible in dark mode") + owned vocabulary "which keys a menu / tabs / listbox answers (APG)" counterbalancing the fence-repelled positive; component-author fence unchanged. Routing corpus of record checked in (`scripts/routing-corpus.json`, 12 pos / 12 neg) — F1 0.870, every miss/grab dispositioned.
- **A4** declared narrowing documented: the card models only `inline_text`/`spacing_ok` of SC 2.5.8's exceptions — `essential` and UA-default control are judgment-tier.
- **S5** Material & routing gains the maker row: keyboard-affordance defects route to component-author (or the repo's component seat).
- **L** file closes on the done/NOT-done predicate (necessary-not-sufficient echoed).

## 2026-07-02 — shakedown fixes
focus-check gains `modals[]` (per-overlay trap/restore, legacy `modal{}` kept), `targets[]` (`TARGET_TOO_SMALL` gate with SC 2.5.8 exceptions) and `ring{}` (`RING_TOO_THIN` / `RING_LOW_CONTRAST` gates) with locked fixtures; SKILL card + gate table synced, judgment-tier card boundary stated.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `reasoning-about-focus-and-hit-targets` to `focus-verifier` per the `ui-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## 0.1.1 - 2026-05-06

- Expanded `skill.json` with typed-function fields: `domain`, `interface`, `invariants`, `composition`, and, where applicable, `adapters`.
- Added `$schema` declaration to `skill.json`.
- Inserted `## Typed Interface` section into `SKILL.md` documenting domain contract, input/output types, invariants, and downstream routing.
- Tagged as `typed-pipeline` consumer.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.
