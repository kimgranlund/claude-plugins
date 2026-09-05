# Changelog

## 2026-09-05 · initial release (frontend 2.7.0)
- New skill: the fix-loop contract (one family per iteration, evidence before fix, re-audit changed surfaces + previous findings, revert on regression, stop after two failures on one family, playbook entry per iteration). `scripts/lh-diff.mjs <before.json> <after.json>` prints regressions/improvements/unchanged and exits 1 on any regression; `--budgets budgets.json <after.json...>` gates reports against perf-sweep's cards. Selftest: identical reports clean, the two fixtures as before/after (10 regressions incl. aria-allowed-attr, valid-lang new failure, TBT drift), a flipped passing audit as the negative control, tolerance edges, budget mode. Provenance: 1taw297 (comment), 1tewaoi, 1rn63fb, 1tfjlbk.
