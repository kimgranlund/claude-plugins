# Autoresearch — iterative single-change optimization

Run → score → find the weakest dimension → change **one** thing → re-run → keep if better, revert if
worse → repeat. The workhorse for *"improve this"* when you already know roughly where it's weak.
Answers: how far can a score climb, one attributable change at a time? (After Karpathy's autoresearch
pattern: the agent experiments autonomously, keeping only what measurably improves the score.)

## When to use
- There is a score to raise and at least one known weak dimension to attack.
- You want each improvement *attributable* — a changelog of exactly what helped and by how much.
- Not this method when: you have several viable alternatives and want the best of N → **hill-climb**;
  the knob is numeric and you want the whole landscape → **sweep**; nothing is improving because
  something *broke* → **bisect**.

## Input
The dispatch names what to optimize — a file path, a benchmark/test id, a prompt describing the target,
or a scorer command — and the scorer to measure it by. (Sealed dispatch: the caller enumerates the
target; there is no "most recently edited" fallback.)

## Configuration
- `MAX_ROUNDS` 100 · `TARGET_SCORE` 95 · `CONSECUTIVE_PASSES` 2 (stop after hitting target N rounds
  running) — defaults; the dispatch may override any.

## Phase −1 · Research (mandatory)
Web-search before the first edit: (1) what the domain considers quality — accepted standards and
rubrics; (2) common pitfalls and failure patterns for this kind of system; (3) how others solved the
same optimization. Compile 3–5 authoritative sources; cite one in the changelog whenever a change is
inspired by external knowledge. This grounds every round in known practice, not invention.

## Phase 0 · Baseline
1. **Identify the artifact** and **the scorer** — a test suite (pass rate), a benchmark (number), a
   custom metric (latency, size, accuracy), a written checklist (5–10 yes/no checks), or an LLM-judge
   rubric for subjective quality. Fix it now; do not redefine it mid-run.
2. **Run the scorer.** Record the baseline score, its per-dimension breakdown, and the failing checks.

## Phase 1 · Loop
For each round (1 → `MAX_ROUNDS`):
1. **Target the weakest dimension** — the lowest-scoring or first-failing check. That is this round's
   focus, and only that.
2. **Propose one change** — specific and singular. Name the exact thing changed and its expected
   effect on the weak dimension. "add empty-string validation to `parse()`", not "improve quality".
3. **Apply** it — minimal, one concept.
4. **Re-score** with the same scorer.
5. **Keep or revert** — improved or held → keep and log it; dropped → revert immediately and log the
   revert; next round tries a *different* approach, never the reverted one again.
6. **Check exit** — target held for `CONSECUTIVE_PASSES` rounds → stop (target); max possible score →
   stop (perfect); `MAX_ROUNDS` → stop (budget); **5 consecutive reverts → stop (stuck)** and report
   what was tried.

Per round, record: `Round n: prev → new (Δ) · change · kept|reverted · weakest remaining`.

## Phase 2 · Report
```
Autoresearch · <artifact> · scorer: <how>
Baseline <b> → Final <f> (<Δ>)  ·  rounds <n>  ·  kept <k> / reverted <r>
Changes that stuck:   1. <change> (+Δ)  2. …
Reverted (no help):   1. <change> (Δ)   …
Stopped: <target | perfect | budget | stuck>
Recommendation: <ship the deltas | chain into adversarial to verify robustness | …>
```

## Rules
- One change per round — never batch. · Always measure — never assume a change helped.
- Revert on any drop, before the next round. · Don't repeat a reverted approach.
- Be specific — vague changes aren't actionable. · Stop at 5 reverts — the approach is wrong, not
  under-attempted.
- **Web-search on poor signal** — flat score, tied changes, or 2+ reverts in a row: stop and research
  the specific problem before guessing again.

## Rubric — autoresearch conducted well
Inherits the shared gate **R1 (scorer fixed first) · R3 (one change/round) · R7 (stopped on a
predicate)** from `references/rubric.md`. Additive method checks:
- **Weakest-first targeting** — 1: rounds attack random dimensions · 3: mostly weakest-first · 5:
  every round names and attacks the current weakest check.
- **Revert-on-drop honored** — 1: drops kept "to see" · 3: reverted late · 5: every regression
  reverted immediately, logged, and not retried.
- **Attributable changelog** — 1: only the final number · 5: each kept change carries its own +Δ, so
  the total is decomposable.

**Gate:** R1 · R3 · R7 ≥ 3, **and** no round batches more than one change and no regression is left
standing. A "+20" with two changes in one round is an R3 failure even if the number went up.
