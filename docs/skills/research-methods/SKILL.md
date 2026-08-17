---
name: research-methods
description: >-
  Use for a measured investigation of a scorable system — six methods: autoresearch, hill-climb,
  ablation, sweep, bisect, adversarial. Triggers: "improve the score", "find the root cause of
  this regression", "which parts actually matter", "what's the best value for X", "tune these
  parameters", "what breaks this", "it used to work, now it doesn't". NOT lookup (web search); NOT
  artifact review (*-checker agents); NOT authoring/building (*-forge/builder); NOT for judging
  whether a recurring finding means a rule or reasoning-depth itself is wrong, absent a scorer
  and a baseline→change→remeasure loop (harness:thinking-depth-rules).
disable-model-invocation: false
user-invocable: false
---

# Research Methods — systematic investigation of a scorable system

Every method here shares one shape and one discriminator. The **shape**: fix a measure, establish a
baseline, change one thing, re-measure, keep or revert, repeat, report. The **discriminator**: the
*class of question* being asked. You are not choosing a favorite tool — the question selects the
method, and running the wrong one answers a question nobody asked. Full protocol and per-method
rubric for each live in `references/<method>.md`; the shared quality standard is `references/rubric.md`.

**One hard precondition:** if the system isn't scorable, you cannot research it. Before any method
runs, a reproducible measure of progress must exist — a test, a benchmark, a metric, or a written
checklist / LLM-judge rubric. No scorer → define one with the user *first*; do not enter a loop
against a measure you'll invent later to justify the change you already made (rubric R1).

**Species — a knowledge pack that carries an execution spine (declared hybrid).** Like
`prompt-wording-rules`, this is not a pure reference: it documents the six methods *and* carries the
runnable spine (Step 2 below) plus the investigation rubric they're judged by. It is consulted **inline
only for a single-round check**; a real bounded loop — mandatory web research, dozens of measured rounds
— is **dispatched to the `experiment-runner` agent**, which preloads this pack and runs one method in
isolation. The pack answers *which method, run how, judged by what*; the seat runs it. Each method's
protocol is grounded in prior art cited in `references/sources.md`.

## The six methods (the operable index)

| Method | Answers the question | Returns | Protocol |
|---|---|---|---|
| **Autoresearch** | "How do I improve this?" (known weak point) | a higher score + a changelog of what stuck | `references/autoresearch.md` |
| **Hill Climb** | "What's the best of these alternatives?" | the winning move from a tried neighborhood | `references/hill-climb.md` |
| **Ablation** | "Which parts actually matter?" | each component's measured contribution | `references/ablation.md` |
| **Sweep** | "What's the optimal value for X?" | the scored parameter landscape + sensitivity | `references/sweep.md` |
| **Bisect** | "What broke, and when?" | the exact change that introduced the regression | `references/bisect.md` |
| **Adversarial** | "What breaks this? Where are the edges?" | classified failure modes (+ fixes) | `references/adversarial.md` |

## Step 1 — Select the method (question class → method)

```
"used to work, now it doesn't" / a regression with a known-good prior  → BISECT
"improve this" + a known weak dimension                               → AUTORESEARCH
"improve this" + several viable alternatives, want the best of N      → HILL CLIMB
"improve this" + a numeric knob to tune                               → SWEEP
"which of these actually pull their weight" / "what can I remove"     → ABLATION
"is this robust" / "what breaks it" / "find the edge cases"           → ADVERSARIAL
```

**Disambiguation** (when a request maps to more than one):
- *Improve* + known weak point → Autoresearch · + no clear weak point → Hill Climb · + numeric knob → Sweep.
- *Why broken* + known-good prior state → Bisect · + no prior state → Adversarial (find what's fragile).
- *Simplify / what can I remove* → Ablation. · *Is it robust enough* → Adversarial.

**Confidence check.** If the match is a coin flip, present the top two candidates with a one-sentence
rationale each and let the user choose. Don't guess on a tie.

## Step 2 — The shared execution spine

Every method's `references/` file specializes these four phases; read that file before running.

- **Phase −1 · Research (mandatory).** Web-search the domain *before* touching anything — best
  practices, known failure patterns, prior art, established ranges. You optimize/attack/bisect only
  moves you know about; this phase is also where you re-enter when signal goes flat (rubric R5).
- **Phase 0 · Baseline.** Identify the artifact and the scorer; run the scorer; record the baseline
  and its breakdown. This is the number every later round is measured against.
- **Phase 1 · Loop.** The method's core iteration — one variable per round, re-measure, keep/revert
  or record, journal the round. Bounded by the method's exit predicate.
- **Phase 2 · Report.** State the finding, the evidence, and a concrete recommendation. Score the run
  against `references/rubric.md`.

## Step 3 — Chain when the result opens the next question

A finished method often hands the natural next question to another. Suggest the chain; run it only on
consent — never auto-chain.

| Completed | Natural follow-up | Because |
|---|---|---|
| Bisect | Autoresearch | root cause found → now fix and improve it |
| Ablation | Autoresearch | dead weight removed → now optimize what remains |
| Adversarial | Autoresearch | failure modes found → now harden iteratively |
| Sweep | Hill Climb | promising region found → now fine-tune within it |
| Hill Climb | Adversarial | local optimum reached → now stress-test it |
| Autoresearch | Adversarial | score optimized → now verify it's robust |

## Principles (apply across all six)

- **Measure everything.** No change is "obviously" good; score before and after.
- **One variable at a time.** Batching obscures which change caused the delta.
- **Return to a clean state.** Revert a regression, restore an ablation, start each midpoint clean.
- **Journal the path.** Every round's change, delta, and keep/revert decision is recorded (R6).
- **Ground before guessing.** When stuck — flat score, tied moves, repeated reverts — stop and
  research the specific problem before burning another round.
- **Stop on a predicate, not on patience.** Target hit, plateau, space exhausted, or stuck — each is
  a named stop. "I got bored" is not convergence (R7).

## How to run it — inline vs. dispatched

A quick, single-round check runs inline. A real investigation — a bounded loop, mandatory web
research, dozens of measured rounds — is the textbook case for **isolation**: dispatch the
**`experiment-runner`** agent, which preloads this skill, runs the loop in its own context (so the host
isn't flooded with 100 rounds of experiment noise), and returns a typed report. **Generator ≠
critic:** the experiment-runner does not certify its own run — the **dispatching seat that receives the
handoff** scores the report against `references/rubric.md` (the standing consumer-as-critic; the run's
self-score is disclosure, not a verdict). No separate reviewer seat owns investigation reports today.

## Output contract (a completed investigation)

```
Method: <name>   ·   System: <what was researched>   ·   Scorer: <how measured>
Baseline: <score> → Final: <score> (<delta>)   ·   Rounds: <n> (kept <k> / reverted <r>)
Finding: <the one-line answer to the question class>
Recommendation: <apply | remove | fix | set X=v | chain into <method>>
Artifacts: <paths, never inlined>
Rubric self-score: R1 <g> R3 <g> R7 <g> (gate) · R2/R4/R5/R6/R8 <1-5 each>
```

**Done** = the question answered against a scorer fixed before the loop, the loop stopped on a named
predicate, and the contract above filed with its R1/R3/R7 self-score. **NOT done** = a loop entered
without a scorer, more than one variable moved in a round, or a conclusion drawn from a run that never
terminated on a predicate.

## Worked example — autoresearch on this skill's own routing (2026-07-04)

A real, dated run of the pack on itself. **Question class:** "improve the score" + a known weak
dimension (recall) → **autoresearch**. **System:** this SKILL.md's `description`. **Scorer:**
the `routing_eval` aid (harness's routing tool) computing F1 over `scripts/routing-corpus.json` —
reproducible, baseline **0.750** (this pass reached **0.889**).
**Round 1** — weakest dimension: recall; hypothesis: fenced tokens (`skill`, `scoring`) repel owned
positives and two bisect triggers are absent; one change: add `skill, agent` to the scorable-system
list; re-measure. **Round 2** — add the two lexical-hole triggers (`regressed`, `it used to work`).
Kept both, reverted none. **Stopped** (predicate): the remaining recall misses are proxy artifacts
(inflection / paraphrase the lexical eval can't see), not description defects — no further attributable
change available. The journal and disposition live in `CHANGELOG.md`.

## References

| Path | Use when |
|---|---|
| `references/autoresearch.md` · `hill-climb.md` · `ablation.md` · `sweep.md` · `bisect.md` · `adversarial.md` | The selected method's full protocol + its per-method rubric section |
| `references/rubric.md` | Score how well the investigation was conducted (gate = R1, R3, R7) |
| `references/sources.md` | The prior art each method's protocol is grounded in (provenance) |
| `references/threshold-sweep-2026-07-04.md` | A real dispatched run end-to-end (sweep) — also the reference journal shape for the R1/R3/R7 gates |
| `scripts/journal_check.py` | Arithmetic shape-check of a run's journal (R1/R3/R7, three-valued; `selftest` proves the checks) |
| `scripts/routing-corpus.json` | The routing eval corpus for this skill's description |

## Composition

- **`experiment-runner`** runs one method in isolation and hands back the typed report above.
- **[[find-intent]]** / **[[grill-the-ask]]** sharpen a fuzzy "make it better" into a scorable
  question + a defined scorer *before* a method runs — the R1 precondition.
- **[[make-rubric]]** owns `references/rubric.md`'s shape; harness's `make-pack` owns adding or
  revising a method file (axis decomposition, grounded research, index discipline) — never bolt an
  uncited method on inline.
- Downstream of a finding, route the *fix* to its owner: a code change to **builder**, a skill
  edit to harness's **make-skill**, a design change to **planner**. This skill finds; it does not own
  the repair.
