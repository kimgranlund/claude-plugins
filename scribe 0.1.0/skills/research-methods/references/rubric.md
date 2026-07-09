# Rubric — Investigation Quality

Scores *how well a systematic investigation was conducted*, independent of which of the six methods
ran (autoresearch · ablation · bisect · adversarial · hill-climb · sweep). The method-specific gates
live in each `references/<method>.md`; this rubric is the shared spine they all inherit. Built via
`rubric-forge`. `[gate]` here = a floor that, if failed, invalidates the run regardless of the rest —
a *judgment-checked* floor read from the run's journal, not (yet) a lint-backed one, so it diverges
deliberately from the mechanically-checkable `[gate]` in the skill / linguistic-potency rubrics (see the
journal shape-check note at the foot); `[review]` = judgment with cited evidence from the run's journal.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| R1 | Scorer defined first | [gate] | A reproducible measure of progress/outcome was fixed **before** the loop began | 1: no scorer, or "improved" asserted by eye · 3: a scorer exists but is defined mid-run or only loosely reproducible · 5: an explicit, re-runnable scorer (test, benchmark, metric, or written checklist/LLM-judge rubric) with a recorded baseline, fixed before round 1 |
| R2 | Method fit | [review] | The chosen method matches the *class of question* asked (the selector) | 1: method answers a different question than the one posed · 3: defensible but a sibling method fit better · 5: the method is the one the question class selects; a chain hand-off is justified when used |
| R3 | Single-variable isolation | [gate] | One change / removal / parameter / midpoint per round — attribution stays clean | 1: multiple variables move per round; signal is unattributable · 3: mostly isolated, one or two batched rounds · 5: exactly one variable per round throughout; any planned interaction test is labelled as such |
| R4 | Clean-state discipline | [review] | Each round starts from a known base — revert-on-regression, restore-after-ablation, clean midpoint, verified fix | 1: state accumulates across rounds; a reverted change lingers · 3: mostly clean, one leaked state · 5: every round returns to a known base before the next; the winner is applied deliberately, not by drift |
| R5 | Grounding | [review] | External knowledge was gathered before guessing (Phase -1) and again when signal went flat | 1: optimized/attacked/bisected in a vacuum, no research · 3: some upfront research, none when stuck · 5: Phase -1 done and cited; web search re-entered on flat score / repeated reverts / ties, and it changed a decision |
| R6 | Journaling | [review] | Every round's change, delta, and keep/revert decision is recorded; the path is reconstructable | 1: only the final number survives · 3: partial log, some rounds undocumented · 5: a complete round-by-round journal — change, before→after, kept/reverted, rationale |
| R7 | Termination discipline | [gate] | The loop stopped on a real predicate, not exhaustion or a premature call | 1: infinite/aimless loop, or stopped at round 1 with a false conclusion · 3: stopped, but the predicate was fuzzy · 5: stopped on a named predicate — target hit N times, plateau/convergence, space exhausted, or stuck (K reverts) — and the predicate is reported |
| R8 | Reporting & recommendation | [review] | The report states the finding, the evidence, and a concrete next action — not just numbers | 1: a bare score dump, no recommendation · 3: finding stated, action vague · 5: finding + evidence + a specific recommended action (apply / remove / fix / set X=v / chain into method Y), artifacts referenced by path |

**Gate to accept an investigation: R1, R3, R7 each ≥ 3.** These three are load-bearing — an
unmeasured run (R1), a multi-variable run (R3), or a run that never terminated on a real predicate
(R7) produces a conclusion you cannot trust, however good the rest looks. R2/R4/R5/R6/R8 raise a
passing run from *ran* to *ran well*.

**Top failures to look for first:** (1) **no scorer, or a scorer invented after the fact to justify
the change already made** (R1) — the highest-cost class, because every downstream number inherits the
bias; (2) **batched changes** (R3) — two fixes in one round means neither is attributable and a
regression can't be localized; (3) **a run that stopped because the operator got bored** (R7) dressed
up as convergence — it hides an un-searched tail.

**Per-method gates are additive, not substitutes.** Each `references/<method>.md` closes with its own
gate section — method-specific checks layered *on top of* R1/R3/R7, never replacing them. Read the gate
there; this rubric deliberately does not restate the per-method list, because a restated list is a twin
that drifts out of sync — the authoritative gate for each method is that method file's own closing section.

**Journal shape-check.** R1/R3/R7 are line-checkable in a run's journal — R1: a baseline recorded
before round 1; R3: one change per round; R7: a named stop token on the final round. The bundled
checker runs them arithmetically: `python3 scripts/journal_check.py <JOURNAL.md>` (three-valued
PASS/FAIL/UNMEASURED per gate; `selftest` mode proves the checks fire; the reference journal shape is
`examples/threshold-sweep-2026-07-04.md`). It is triage for the consumer-as-critic, not the verdict —
an UNMEASURED gate means the journal's shape wasn't recognizable and must be read by eye, and the
judgment dimensions (R2/R4/R5/R6/R8) are never attempted mechanically.
