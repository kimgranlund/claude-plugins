# Worked run — SWEEP: routing_eval threshold across the corpus estate (2026-07-04)

The `researcher` seat's first live dispatch — preserved verbatim as the genre's dated, real-session
worked example AND as the reference journal fixture (what a run's journal must look like for the
R1/R3/R7 gates to be line-checkable; see rubric.md's journal shape-check note).

**Dispatch (sealed):** system = the `threshold=0.34` module default in skill-author's
`routing_eval.py`; scorer = macro-F1 + sub-0.70 tripwire count over all 55 checked-in corpus pairs;
method = SWEEP (mandated); measure-only, winner not applied. **Result:** 0.34 is the joint optimum
(macro-F1 0.8699, tied 0.34–0.36; delta +0.0000), the estate is peaked not flat, and the sweep
surfaced one real defect no threshold rescues (orchestration-reviewer, F1 ≤ 0.57 at every t —
filed to its owner). **Consumer-as-critic grade (the dispatching seat):** R1/R3/R7 pass — each
verified from the journal below, not the self-score; measure-only verified against git status.

---

# SWEEP round journal — routing_eval threshold over the checked-in corpus estate

Method: SWEEP (single numeric parameter). Date: 2026-07-04.
Scorer (fixed BEFORE the loop, per dispatch): for threshold t, run
`routing_eval.evaluate(desc, corpus, threshold=t)` over EVERY corpus pair →
macro-avg F1 (primary), count of pairs with F1<0.70 (secondary tripwire),
macro-avg precision + recall (diagnostic). 55 pairs (40 skill, 15 agent).

MEASURE-ONLY: routing_eval.py, corpora, descriptions all read-only. Winner NOT applied.

## Phase -1 — grounding (web)
Threshold tuning to maximize F1 is standard; the default is rarely optimal.
Lower t → higher recall / lower precision; higher t → the inverse. Theory: 0.5 is the
upper bound on the F1-optimal threshold. → swept 0.10–0.60 (brackets that bound). Sources
in report.

## Phase 0 — baseline
Estate loaded: 55/55 pairs, 0 skipped. Descriptions extracted via PyYAML (handles both
folded `>`/`>-` blocks — 34 skills + 15 agents — and inline single-line `description:` —
6 skills). Every pair's extraction path logged in results.json.
Baseline t=0.34 (hand-picked default): macro-F1 = 0.8699, trip = 1, P = 0.874, R = 0.881.

## Phase 1 — the sweep (one variable: threshold; every point restored to the same
## baseline estate; grid computed independently per t — no accumulation)

Coarse pass, 0.05 steps 0.10→0.60:
  t     macroF1  trip  P      R
  0.10  0.7965   6     0.675  0.990
  0.15  0.7915   8     0.681  0.965
  0.20  0.7987   7     0.697  0.954
  0.25  0.8151   5     0.734  0.935
  0.30  0.8468   4     0.810  0.909
  0.35  0.8699   1     0.874  0.881   ← coarse peak
  0.40  0.8532   4     0.871  0.855
  0.45  0.8019   11    0.874  0.764
  0.50  0.7991   12    0.873  0.760
  0.55  0.7458   16    0.931  0.641
  0.60  0.7191   23    0.934  0.604

Coarse peak = 0.35 → fine pass, 0.01 steps 0.30→0.40:
  0.30 0.8468 | 0.31 0.8459 | 0.32 0.8459 | 0.33 0.8459 |
  0.34 0.8699(trip1) | 0.35 0.8699(trip1) | 0.36 0.8699(trip1) |
  0.37 0.8686(trip2) | 0.38 0.8532 | 0.39 0.8532 | 0.40 0.8532

Peak is a discrete plateau [0.34, 0.36] (F1=0.8699, trip=1) — identical across those three
points. Discrete steps because the overlap score is hits/n over small token counts, so F1
only moves as t crosses a specific rational score value. Sharp step up at 0.33→0.34
(+0.024, trip 4→1) and down at 0.37→0.38 (−0.015, trip 2→4).

## Phase 1 — stop
Predicate: SPACE EXHAUSTED (full coarse grid + one fine pass over the peak region, both
shoulders of the plateau captured). Best macro-F1 = 0.8699 at t∈{0.34, 0.35, 0.36};
baseline 0.34 is the joint optimum → delta = +0.0000. No further grid warranted (dispatch:
grid + one fine pass only).

## Findings recorded
- 0.34 is jointly optimal on BOTH the primary (macro-F1) and secondary (trip=1) scorers.
- Sensitivity: PEAKED, not flat. Full-range macro-F1 spread 0.719→0.870 = 0.151. R falls
  monotonically 0.99→0.60 as t rises; P rises 0.675→0.934; F1 peaks mid-range. Narrow
  optimal plateau (width 0.02–0.03); meaningful degradation outside [0.30, 0.40].
- Per-pair optima are BIMODAL: a recall-driven cluster wants t=0.10 (vision-memo-forge,
  prd-author, check-translations, check-safety, check-focus, research-methods, token-builder —
  mostly paraphrase positives the lexical proxy can't see, a measurement artifact the module
  docstring flags), and a precision-driven cluster wants t≥0.35 (system-builder, color-theory-facts,
  spec-author, code-reviewer, component-checker@0.55). 0.34 is the balance point between them
  — exactly why a single global knob peaks in the middle.
- Outlier (below tripwire at 0.34): orchestration-reviewer (agent), F1=0.545. Its own curve
  caps at 0.57 at EVERY threshold — no knob value rescues it. This is a description/corpus
  quality defect, NOT a threshold issue → route to the agent's owner.
- Outlier (wants higher t): component-checker (agent), individual optimum t=0.55, but not
  below tripwire at 0.34 — mild precision preference, no action.
