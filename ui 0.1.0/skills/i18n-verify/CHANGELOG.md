# Changelog

## 2026-07-03 — excellence-campaign batch-3 fixes (G2)
`locales/expansion-factors.json` re-grounded and made the named canon (v2): expansion is regime-split per locale — `shortString` (≤ ~10 en chars: +100–200%, de/it ×3.0/×2.8-grounded) vs `runningText` (> ~70 chars: +30–50% European incl. Russian; CJK contracts ~×0.7) — cited in-file to W3C "Text size in translation" (Ishida) and the IBM i Globalization additional-space table; SKILL invariants row and i18n-check's NO_EXPANSION_ROOM advisory re-derived from it (one canon, two consumers); the advisory now names its regime via the new `string_regime` card key (surface → top-level → runningText default), selftest-locked. Smalls: checker usage lines bin/→scripts/; "progress direction" re-scoped out of the always-mirror list (logical-axis CSS per `icon-policies.json`); `LOCALE_POSTURE_DECLARED` named in the gate table. Description gains verbatim i18n / line-height per script / hardcoded-untranslated / Arabic / CJK / German-expansion triggers + the typography-lettering reciprocal fence (routing F1 0.737→0.857, precision 1.000; corpus of record at `scripts/routing-corpus.json`). Card section states the never-carries (judgment-tier) clause; Material & routing gains fix-owner rows ([[component-author]] surfaces, [[spec-author]]/[[prd-author]] posture); Done/NOT-done predicate closes the file.

## 2026-07-02 — shakedown fixes
i18n-check gains `i18n_layer: false` posture collapse (per-surface gates → one `LOCALE_POSTURE_UNDECLARED` gate; `declared_posture` softens it to a single advisory) and `dir` inheritance parity with `lang` (missing `dir` gated only under `rtl_in_scope: true` or `user_content: true`) with locked fixtures; SKILL card + gate table synced to the invariants table.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `reasoning-about-internationalization` to `i18n-verifier` per the `ui-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## 0.1.1 - 2026-05-06

- Expanded `skill.json` with typed-function fields: `domain`, `interface`, `invariants`, `composition`, and, where applicable, `adapters`.
- Added `$schema` declaration to `skill.json`.
- Inserted `## Typed Interface` section into `SKILL.md` documenting domain contract, input/output types, invariants, and downstream routing.
- Tagged as `typed-pipeline` consumer.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-02 — net-new re-author (family template)
Rebuilt 213→93 lines on the focus-verify template: kept the i18n card + i18n-check gate table, the per-script numbers (line-height bands, min body sizes, expansion budgets), logical-axis/dir-lang/bidi/Intl rules, icon-mirroring policy, all data-dir pointers, and the [[typography-lettering]]/[[ui-audit]] edges; killed Invocation/Ingestion/Decomposition ceremony, When-to-use/NOT sections, Rate-limiting factor, First-principles prose, the 9-step narrative procedure, LocaleSchema listing, and Typed Interface.
