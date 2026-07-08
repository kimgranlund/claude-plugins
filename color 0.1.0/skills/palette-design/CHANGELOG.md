# Changelog

## 2026-07-03 — excellence campaign batch-2 (group F5): one canon, mechanized
- **`ramps/` crowned THE canon** for grids/curves; SKILL.md's numbers re-derived from it.
  Reconciled: scale is 13 steps `0, 50, 100..900, 950, 1000` (body said "default 11" while
  enumerating 12; the role defaults require neutral-950) · L-anchor row split per family from the
  JSONs (old mixed row claimed 1000 → 0.12 vs canon 0.080/0.100) · extreme-C caps 0.04/0.03 from
  `extremeFloors` (body claimed 0.02) · evenness aligned to color-verify's per-label-unit form
  (ΔL ÷ Δlabel, gap-to-gap ≤ 1.5; false "≤ 20%" design-margin claim dropped) · neutral 0.02
  ceiling now stated as design margin under color-verify's 0.06 tinted gate.
- **Canon fixes in the JSONs**: neutral-curve note 11→13-step; its evenness invariant re-stated
  per-label-unit (end-gap exclusion removed — normalization makes 50-unit gaps commensurate);
  chromaDistribution prose → machine-readable `chromaBell` (L_peak 0.5, k 12, in-gamut rationale);
  accent-curve 950 anchor 0.180 → 0.185 (old value broke evenness: ratio 1.556 > 1.5);
  `extremeFloors` machine-readable; `gamutPolicy.forbidden` now bans L **and H** shifts (C-only).
- **`scripts/ramp_build.py` shipped** (stdlib-only, selftest-locked): skeleton → chroma bell
  (anchor C reproduced exactly) → C-only gamut walk (0.005 steps; same CSS Color 4 matrices as
  color-verify's contrast-check.py) → invariant report with `DecompositionGap` exit 1. Selftest:
  neutral canon build (monotone, evenness ≤ 1.5, in gamut, zero rescue) + negative control (an
  out-of-gamut anchor must show reduced C, byte-identical L/H) + broken-curve detector fixtures.
  Judgment stays with the model: anchor negotiation, hue-drift trades, role mapping.
- **Routing**: phantom "the brand corpus" route (description + routing row) repointed to
  color-theory; description gained intent-hue choosing + 13-step scale; corpus checked in at
  `scripts/routing-corpus.json` (routing_eval F1 1.000, all misses/grabs dispositioned).
- **Species organs**: Update line (re-derive from color-verify invariants + ramps/, never patch
  prose), single role-NEVER, detection catalog de-imperativized, done/NOT-done close,
  `UISchema.primitive.color.scale` shape defined inline.
- Ledger: `skills-audit/campaign/batch-2/palette-design.findings.jsonl` (13 findings, all fixed).

## 2026-07-02 — extracted from color-verify
- Net-new generator skill created by the charter split of `color-verify`: ramp construction
  (the legacy Steps 1–6), semantic role mapping, dark-scheme derivation, and UISchema/BrandSchema
  ingestion with elicit-if-absent fallback now live here.
- `ramps/` data dir (neutral-curve, accent-curve, intent-hues) moved here from `color-verify/`.
- Contract: every emitted ramp/mapping runs `color-verify` before finalize (design → verify).
