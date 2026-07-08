# Sweep — parameter-space exploration

Systematically vary one or more parameters across a range, scoring each point, to map the landscape:
where the optimum is, and how sensitive the score is to each knob. Answers: *"what's the best value
for X — and does X even matter?"*

## When to use
- One or more tunable numeric/ordinal knobs with a range, and you want the optimum *and* the
  sensitivity, not just a lucky value.
- Not this method when: the alternatives are discrete and unordered → **hill-climb**; you want to
  *remove* parts → **ablation**; you're chasing a regression → **bisect**.

## Input
The dispatch names the parameter(s) + range — one ("timeout 100–5000ms"), several ("batch 8–64 and lr
0.001–0.1"), or a single knob ("retry count 1–10") — and the scorer. (Sealed dispatch: the caller
enumerates the knobs; there is no "most recently edited config" fallback.)

## Configuration
- `MAX_ROUNDS` 100 · `GRID_RESOLUTION` 5 (steps per dimension) · `TOP_K` 3 (configs reported) —
  defaults; the dispatch may override any. Grid > `MAX_ROUNDS` → sample (Latin-hypercube or random).

## Phase −1 · Research (mandatory)
Web-search the *established ranges* before defining the grid — don't sweep blind: (1) what standards,
specs, or RFCs recommend for these values; (2) studies/benchmarks on their effect and the ranges they
tested; (3) the defaults popular frameworks ship. Use this to **narrow the bounds** — sweeping 1–10000
when research says 10–100 covers 95% of useful values wastes the whole budget on noise.

## Phase 0 · Define the parameter space
1. **List each parameter** — name, range, step (or discrete set), unit/type.
2. **Grid size** = product of steps; if it exceeds `MAX_ROUNDS`, switch to sampling.
3. **Run the baseline** at the current values.

## Phase 1 · Single-parameter sweeps
For each parameter independently (hold the others at baseline):
1. Set the parameter to each value in its range → score → record `(value, score)` → restore.
2. **Report the curve** and its shape:
   ```
   <param> (range <min>–<max>):
     <v1>  ████████████░░░░  <s1>
     <v2>  ████████████████  <s2>  ← best
     <v3>  ██████████░░░░░░  <s3>
   optimal <v> · sensitivity low|medium|high
   ```

## Phase 2 · Multi-parameter grid (if 2+ parameters)
Cross the top ~3 values of each parameter to catch interactions the single sweeps miss:
```
            b=X   b=Y   b=Z
   a=X       82    88    85
   a=Y       85    94    91   ← sweet spot
   a=Z       83    90    88
```

## Phase 3 · Report
```
Sweep · <system> · baseline <s> at <values>
Best <s> at <values> (+Δ)
Top <K>:  1. <values> → <s>   2. …   3. …
Sensitivity:  <p1> HIGH (±range → ±score)  ·  <p2> LOW (flat)
Recommendation: set <param>=<value>  ·  offer to apply the optimum
```

## Rules
- One parameter at a time first — understand individual effects before crossing them.
- Always restore to baseline between points — no accumulation. · Sample if the grid exceeds the budget.
- Report sensitivity — a flat parameter is as important a finding as a peaked one. · Visualize the
  curves. · Offer to apply the winner.
- **Web-search on surprises** — a non-monotonic curve or a counter-intuitive optimum: research *why*
  before trusting it. Knowing why a value is optimal is worth as much as the value.

## Rubric — sweep conducted well
Inherits **R1 · R3 · R7** from `references/rubric.md`. Additive method checks:
- **One-parameter-first** — 1: all knobs moved together from the start · 5: single sweeps first,
  interactions only after, labelled as the grid phase.
- **Restore-to-baseline** — 1: points accumulate; the landscape is smeared · 5: every point measured
  from the same baseline.
- **Sensitivity reported** — 1: only the best value given · 5: each parameter's sensitivity stated, so
  the reader knows which knobs matter and which are flat.

**Gate:** R1 · R3 · R7 ≥ 3, **and** single-parameter sweeps precede any grid and every point restores
to baseline (else "best value" is contaminated by whatever the previous point left set).
