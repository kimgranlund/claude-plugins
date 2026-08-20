# Live-lane measurement — first pass (#759)

**Verdict: 🟢 the lane holds — no defect signal, size bound respected; the turnaround multiple
is real but not measurable from PR timestamps, and this single-day window is too hot for the
follow-up-fix proxy to mean anything. Re-measure over a ≥14-day window before treating these
rates as steady-state.**

Instrument: `authorkit:spend-audit` cohort_report.py (`--since 2026-08-19 --label live-lane`),
shipped for exactly this in #763/PR #767. Trigger: ≥12 merged `live-lane` PRs (13 at run time)
vs 45 unlabeled same-window.

| metric | lane (n=13) | full flow (n=45) | reading |
|---|---|---|---|
| open→merge avg | 6.7 min | 6.7 min | **uninformative for the lane claim** — both cohorts open PRs already green-ready; the lane's savings happen BEFORE PR-open (prompt→push). Hand-measured earlier: ~20 min lane vs ~45 min full flow prompt→merge (#755 vs #751) |
| additions / deletions avg | 71 / 46 | 225 / 22 | lane changes are genuinely small (the tripwire bound holds); high deletions = the diet waves |
| checker-verdict-in-body | 62% | 56% | the lane does not skip critics |
| revert mentions | 3 flagged | 2 flagged | **all 3 lane flags manually verified as false positives** — body text describing regressions *healed pre-merge* (#787, #783) or the measurement design itself (#756). True lane reverts: **0** |
| 48h follow-up-fix (file overlap) | 46% | 93% | churn proxy, not defects — a single hyperactive day where waves touch the same plugins repeatedly inflates both; meaningless until the window spans quiet days |

## Ruling implications

1. No finding against fleet-rules §7 — the lane's revert rate is zero, its checker rate matches
   the full flow, and its size bound is visible in the data.
2. The open→merge proxy can never validate the lane's speed claim; a future pass needs
   prompt→push (first-commit→merge) or spend-ledger rows.
3. Re-measure at ≥14 days of mixed activity; if the follow-up-fix gap persists on a quiet
   window, THAT is the number to investigate.

Provenance: 2026-08-19 overhaul session, plugins-marshal; raw JSON in the session scratchpad.
Closes #759's first-pass obligation; the 14-day re-run is the recorded follow-up.
