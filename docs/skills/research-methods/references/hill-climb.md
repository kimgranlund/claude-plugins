# Hill Climb — greedy local optimization

Explore the neighborhood of the current solution: try **every** single-step change, score each,
move to the best, repeat until no neighbor improves. Where autoresearch fixes the *weakest* dimension
one change at a time, hill-climb tries *all* candidate moves each round and takes the winner. Answers:
*"what's the best of these alternatives?"*

## When to use
- Several viable alternatives exist and you want the empirically best, not the first plausible one.
- The move set is discrete and enumerable (refactors, rule swaps, flag toggles, layout options).
- Not this method when: you already know the weak spot and want one targeted fix → **autoresearch**;
  the knob is a numeric range → **sweep**; you want to know what to *remove* → **ablation**.

## Input
The dispatch names what to optimize — a file, a config, a design, or a parameter space with discrete
alternatives — and the scorer. (Sealed dispatch: the caller enumerates the target; no "most recent"
fallback.)

## Configuration
- `MAX_ROUNDS` 100 · `PLATEAU_LIMIT` 3 (stop after N rounds with no improvement) ·
  `NEIGHBORHOOD_SIZE` 5 (alternatives tried per round) — defaults; the dispatch may override any.

## Phase −1 · Research (mandatory)
Web-search to *widen the neighborhood* — you can only propose moves you know about: (1) what
approaches exist for this problem and their trade-offs; (2) what established guidelines recommend;
(3) the state of the art and what makes it good. Compile a **moves catalog**; it is the neighborhood
generator for Phase 1. A hill-climb is only as good as its move vocabulary.

## Phase 0 · Baseline
1. Identify the artifact and scorer (as autoresearch); run the baseline score.
2. **Enumerate the move space** — the possible single-step changes (swap an algorithm, add/remove/
   strengthen a rule, toggle a flag, rearrange a structure).

## Phase 1 · Loop
For each round (1 → `MAX_ROUNDS`):
1. **Generate the neighborhood** — `NEIGHBORHOOD_SIZE` independent single-step changes (each stands
   alone, none building on another).
2. **Try each neighbor** — apply, score, record, **revert**. Every neighbor is measured against the
   *same* current base.
3. **Pick the best.** If no neighbor beats the current score → **plateau** (increment the counter).
4. **Apply the winner** permanently — only the winner, never the runner-up, never a combination.
5. **Check exit** — plateau counter ≥ `PLATEAU_LIMIT` → stop (local optimum); target reached → stop;
   `MAX_ROUNDS` → stop.

Per round: `Round n: tried <c> · best "<move>" → <score> (+Δ) · others <…> · applied|plateau p/limit`.

## Phase 2 · Report
```
Hill Climb · <artifact> · scorer: <how>
Baseline <b> → Final <f> (+Δ)  ·  rounds <n> (<total> neighbors tried)
Path:  R1 <move> (+Δ)  ·  R2 <move> (+Δ)  ·  R3 plateau (local optimum)
Stopped: <local optimum | target | budget>
Recommendation: <apply the path | chain into adversarial to stress the optimum | restart to escape>
```

## Rules
- Try multiple alternatives per round — this is what separates it from autoresearch.
- Always revert between neighbors — each is scored against the same base. · Apply only the winner.
- Track the rejected neighbors — they inform later rounds. · Stop at the plateau — 3 fruitless rounds
  is a local optimum, not a reason to keep grinding. · Consider a larger random restart to escape one.
- **Web-search on plateaus** — when every neighbor ties or you're out of moves, research novel
  approaches; external knowledge generates neighbors you wouldn't have. Search before restarting blind.

## Rubric — hill-climb conducted well
Inherits **R1 · R3 · R7** from `references/rubric.md`. Additive method checks:
- **Neighborhood breadth** — 1: one move tried (that's autoresearch) · 3: a couple · 5: a genuine
  informed neighborhood each round, drawn from the moves catalog.
- **Revert-between-neighbors** — 1: neighbors stack on each other; scores incomparable · 5: every
  neighbor scored against the identical base, reverted before the next.
- **Winner-only application** — 1: a blend of the top-2 applied · 5: exactly the single best move
  committed each round.

**Gate:** R1 · R3 · R7 ≥ 3, **and** neighbors are reverted between trials (else the scores aren't
comparable and the "winner" is an artifact of order).
