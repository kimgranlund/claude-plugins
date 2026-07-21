# Changelog

## 2026-07-03 — excellence-campaign batch 3 fixes
- `verification/contrast-pairs.json`: deleted the phantom `AAA uiComponent: 4.5` target (no such WCAG tier — SC 1.4.6 is text-only; SKILL.md and the checker already said so); `note` + `escalation` rewritten in verifier voice (the escalation is the prescription the `DecompositionGap` carries; palette-design executes it — the file no longer speaks as the pre-split generator).
- Canon named on both sides: the invariant table's ramp-geometry rows now cite [[palette-design]]'s `ramps/` + `ramp_build.py` as the canon (this table is the gate's view); `scripts/contrast-check.py`'s docstring declares SKILL.md's card section canonical for the card interface.
- Mechanism section states the A4 exception (the checker sees PAIRS, not ramps — ramp-geometry gates run mechanically in palette-design's `ramp_build.py`, re-judged here in step 3) and the coverage boundary (only pairs shown are verified; coverage vs `contrast-pairs.json` is skipped-not-passed).
- Description: "WCAG AA/AAA" tokens, "alpha/translucent colors composited over a backdrop", unhyphenated "hue stability, perceptual evenness" (hyphenated forms kept), color-science fence extended to "color-space math or converting between color spaces".
- Done/NOT-done predicate closes the file; M2 routing corpus of record checked in at `scripts/routing-corpus.json`.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `reasoning-about-color` to `color-verifier` per the `ui-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## 0.1.1 - 2026-05-06

- Expanded `skill.json` with typed-function fields: `domain`, `interface`, `invariants`, `composition`, and, where applicable, `adapters`.
- Added `$schema` declaration to `skill.json`.
- Inserted `## Typed Interface` section into `SKILL.md` documenting domain contract, input/output types, invariants, and downstream routing.
- Tagged as `typed-pipeline` consumer.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-02 — net-new re-author: split to pure verifier; generation extracted to palette-design
SKILL.md rewritten on the focus-verify template as a pure verifier (card → gate → judgment sweep → ColorProof). Ramp construction, semantic role mapping, and dark-scheme derivation (legacy Steps 1–6/8) moved to the new `palette-design` skill, along with the `ramps/` data dir. `verification/` and `scripts/contrast-check.py` stay here.

## 2026-07-02 — shakedown fixes: oklch/light-dark/alpha-compositing, full JSON table, invariant corrections, focus-ring handoff
- `scripts/contrast-check.py`: `oklch(L C H [/ A])` parsing (standard OKLab→linear-sRGB matrices; gamut clamp + `OKLCH_OUT_OF_GAMUT` advisory); `light-dark(X, Y)` resolved by card `meta.scheme` — no scheme is a per-pair ERROR, never a first-leg pick; alpha accepted in `rgba()`/`#rrggbbaa`/`oklch(/A)` with per-pair `"over"` source-over compositing (gamma-encoded sRGB, as browsers) — alpha fg with no `over` is a per-pair ERROR, translucent `bg`/`over` likewise; `--json` now emits the full per-pair table (every pair: name/fg/bg/ratio/target/pass + fgToken/bgToken/meta pass-through); card `meta {theme, scheme, contrast}` + per-pair `fgToken`/`bgToken` provenance. New selftest fixtures: oklch known values (white/black, sRGB-red roundtrip, the documented `oklch(0.558 0.135 255)` ≈ 4.70-vs-white token), out-of-gamut clamp, light-dark leg selection, the composited-outline inversion (passes opaque, fails composited).
- `verification/contrast-pairs.json`: added the `intent-as-text-ink` class typed `normalText` 4.5 (the shakedown's live miss — danger bound as text ink, typed only `uiComponent` 3.0); removed the three `--focus-ring` pairs — focus-ring contrast is [[focus-verify]]'s per both skills' NOT clauses, handoff noted in the file; added the per-repo role→pair `mapping` note.
- `SKILL.md`: card section documents `meta`/`scheme`/`over`/provenance + the `*.surface.json`/`*.contrast.json` dir-globs (example filename aligned); invariants table corrected (per-label-unit ΔL evenness ≤ 1.5, hue drift gated at C ≥ 0.02, declared true-grey ≤ 0.02 / tinted ≤ 0.06 neutral tiers, declared monotonic direction); focus-ring ownership named in Material & routing.
