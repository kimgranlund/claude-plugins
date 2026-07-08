# Ablation — contribution measurement by removal

Disable one component at a time and measure how much the score moves. Answers: *"which parts actually
pull their weight?"* — turning a vague "this feels bloated" into a per-component contribution number,
and a defensible list of what to cut.

## When to use
- A multi-component system you suspect is carrying dead weight, and you want to simplify *safely*.
- You need evidence that a part matters (or doesn't) before removing it.
- Not this method when: you want to *add* improvements → **autoresearch**; you want the best value of
  a knob → **sweep**; something regressed → **bisect**.

## Input
The dispatch names what to ablate — a system with separable components (scorer checks, pipeline stages),
a config with many flags, a prompt with many rules/sections — and the scorer. (Sealed dispatch: the
caller enumerates the target; there is no "most complex thing in context" fallback.)

## Configuration
- `MAX_ROUNDS` 100 · `BASELINE_RUNS` 3 (run the baseline N times and **average** — ablation deltas are
  only as trustworthy as the baseline's stability) — defaults; the dispatch may override any.

## Phase −1 · Research (mandatory)
Web-search the *theory of contribution* before measuring it: (1) which components of this kind of
system practitioners consider essential; (2) what evaluation frameworks exist for the domain; (3) any
prior ablation studies and what they found. **Predict** essential vs. inert before running — then
compare predictions to results in the report. Research says what *should* matter; the ablation says
what *does*.

## Phase 0 · Inventory
1. **List every removable component** — each scorer check, each rule, each stage, each flag.
2. **Run the averaged baseline** — everything enabled, `BASELINE_RUNS` times, averaged.

## Phase 1 · Single ablations
For each component (up to `MAX_ROUNDS`):
1. **Disable one** component; leave everything else untouched.
2. **Score** with the same scorer.
3. **Contribution = baseline − ablated.** Positive → it helps; ~zero → inert (removal candidate);
   negative → it *hurts* (removing it improves the score).
4. **Restore** the component before the next round — ablation is non-destructive.

Per component: `Ablate <c>: <baseline> → <ablated> (contribution <Δ>) · essential|helpful|inert|harmful`.

## Phase 2 · Interaction effects (optional)
For the top ~5 most impactful components, test pairwise removals — two parts that each help alone but
are redundant together show up only here.

## Phase 3 · Report
```
Ablation · <system> · baseline <avg> (n=<runs>)
Essential (removing hurts >5%):  <c> (+score) …
Helpful   (hurts 1–5%):          <c> (+score) …
Inert     (no effect):           <c> (0) …
Harmful   (removing helps):      <c> (−score) …
Recommendation: remove {inert + harmful}; keep {essential + helpful}; projected net +Δ
Prediction vs. result: <where research and measurement disagreed>
```

## Rules
- Disable one component per round — pairwise removals belong to Phase 2, labelled as such.
- Always restore before the next round. · Average the baseline for a stable comparison.
- Sort results by impact. · Don't just report — recommend the cut. · Two "inert" parts may be
  redundant with each other, not truly inert — check the interaction.
- **Web-search on ambiguity** — when a contribution sits near zero and you can't tell inert from
  hard-to-measure, research whether the industry considers that component load-bearing before cutting.

## Rubric — ablation conducted well
Inherits **R1 · R3 · R7** from `references/rubric.md`. Additive method checks:
- **Averaged baseline** — 1: single noisy baseline run · 3: a couple · 5: `BASELINE_RUNS`-averaged, so
  small contributions are distinguishable from noise.
- **Restore-between** — 1: removals accumulate; later deltas are polluted · 5: every component restored
  before the next ablation.
- **Actionable ranking** — 1: an unsorted dump · 5: sorted by impact with an explicit remove/keep call
  and a projected net delta.

**Gate:** R1 · R3 · R7 ≥ 3, **and** the baseline is averaged and every component is restored between
rounds (an un-restored ablation makes every subsequent contribution number a lie).
