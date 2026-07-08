# Craft — the doctrine, voice, and failure modes of the vision-memo genre

The `SKILL.md` carries the method; this carries the *why* behind it — the six principles the genre
rests on, the voice that distinguishes it, the anti-patterns that kill it, and a worked example.

## The six principles

1. **A vision memo is an argument, not a description.** A spec describes what should exist; a PRD
   describes what to build; a vision memo argues for a *way of thinking*. New facts + same mental model
   = failure. Same facts + changed mental model = success. Every memo has a thesis the reader doesn't
   yet hold, and everything serves it.
2. **Reduction precedes construction.** Before proposing anything, reduce the problem to its irreducible
   atoms — what is this, stripped of tooling, convention, and inherited practice? The reduction earns
   the reader's trust to accept what follows; skip it and you're asserting. A good reduction is concrete
   and immediately constrains what solutions are possible ("software is encoded intent"; "a factory is a
   closed-loop transformation system that measures and corrects"), never an abstract platitude.
3. **The best memos reframe, not just propose.** The highest-leverage moment is when the reader realizes
   they've been asking the wrong question. "We don't document enough" → "documentation has no contract."
   "How do we make LLMs reliable" → "how do we constrain the distribution of outputs." Not every memo
   needs one — force a reframe where no genuine misdiagnosis exists and you get a straw-man opening.
4. **Physics beats metaphor.** Treat physical and mathematical constraints as literal, not figurative.
   "Types are the physics of this problem" is a claim about error-propagation math, not a flourish. The
   test: **can you compute with the framing?** If "composability under compounding uncertainty" yields
   the 0.9ⁿ calculation showing why multi-agent pipelines fail, it's physics; if it's just evocative,
   cut it or replace it.
5. **Opinionated beats balanced.** A vision memo takes positions. It does not neutrally "explore
   tradeoffs"; when it names alternatives, it's to explain why they're wrong; when it names principles,
   they're non-negotiable. This is the opposite of most technical writing's trained balance — and a
   balanced vision memo is a failed one, because if every option is equally valid there's no vision,
   only survey.
6. **Every paragraph earns its place.** Dense, not wordy. If a paragraph could be cut without weakening
   the case — or could appear in any memo on any topic — cut it. Density is the genre's signature: a lot
   of thinking per page.

## Voice and style

- **Opinionated, not hedged.** "Types don't just validate output. They make LLM output *better*." — not
  "Types can, in some cases, help with output quality."
- **Physics-literal, not metaphorical.** "This is multiplicative error propagation — the fundamental
  scaling limit of untyped agent systems." — not "Errors can compound, which is problematic."
- **Declarative, not survey-style.** "The factory is the asset. The product is an artifact." — not
  "There are different perspectives on what constitutes the asset."
- **Short closers for impact.** End major sections with one or two compressed sentences, italicised or
  blockquoted when they carry the section's weight:
  > Types at the documentation layer. Types at the pipeline layer. Types at the verification layer.
  > The same principle, at every boundary where imprecision can propagate.
- **Tables for distillation.** A table at a section boundary is the argument re-expressed in its most
  compressed form, not decoration:

  | Principle | Implication |
  |---|---|
  | Software is encoded intent | The factory's input is structured intent, not prompts |
  | A factory is a closed loop | Verification and feedback are structural, not afterthoughts |

- **Confidence without arrogance.** Sound like someone who has thought about this harder than the reader
  and makes the case with reasoning — the authority comes from the reduction and the physics, not the
  tone.

## Anti-patterns

| Anti-pattern | Why it fails | Correct move |
|---|---|---|
| A survey of positions | Reader gets information, not changed thinking | Take a stake; argue one thesis (V1) |
| 10+ "principles" | Dilutes every principle; none land | 3–7 opinionated primitives, each justified (V4) |
| Metaphor without mechanics | "Like a factory" with no closed-loop math | Use physics literally or cut it (V7) |
| Skipping the reduction | Reader hasn't earned the conclusion | Strip to atoms first (V2) |
| Balanced, hedged voice | The genre rewards stakes, not neutrality | Opinionated throughout (V6) |
| Missing the elevation | Memo feels tactical, not strategic | End by lifting topic → meta-point (V5) |
| A reframe that isn't there | Straw-man opening | Skip the reframe stage; make the argument (V3) |
| Manifesto scope for a simple reframe | Bloated, over-structured | Pick the archetype for the argument size (V9) |
| Filler paragraphs | Dilutes density — the genre's signature | Cut anything that doesn't advance the argument (V8) |

## Worked example (condensed)

**Prompt:** "Help me write a vision memo about why our ML platform should standardize on a feature store
before we scale."

- **Thesis:** "The feature store is the coordination mechanism between model development and production
  ML; without it, every team redevelops the same pipelines and data contracts drift." (Written down
  *before* drafting.)
- **Reduction:** An ML platform transforms data into predictions; the irreducible atom is the *feature*
  — the transformed data point models consume. Models, pipelines, serving are composition around
  features.
- **Reframe:** Misdiagnosis — "we have a tooling problem, we need better pipeline frameworks." Actual —
  "we have a coordination problem: features have no canonical form." The reframe: feature stores aren't
  infrastructure, they're **contracts**.
- **Primitives (4–5):** features are the unit of composition · without a canonical definition, contracts
  drift across teams · drift is undetectable until models degrade in production · a feature store makes
  contracts first-class and versionable · the cost of introducing one grows super-linearly with team
  count.
- **Arc (Case-For):** the problem (drift as a silent tax) → reduction (features as the ML primitive) →
  reframe (stores as contracts) → what changes (by role) → scaling argument (why "later" becomes
  "never") → deeper point (contracts as any platform's coordination mechanism).
- **Draft & cut:** write in voice; cut every non-advancing paragraph; add one distillation table; close
  by elevating from "feature stores" to "platform contracts."

## When NOT to write a vision memo

Back off (and route elsewhere) when the user actually wants: a **spec or PRD** (spec-author /
prd-author — those describe what to build); **marketing copy** (different voice and purpose); **academic
writing** (hedged and peer-reviewable, the opposite genre); a **status update / meeting notes / report**
(describes what happened); a **tutorial** (teaches, doesn't argue); a **neutral analysis** ("pros and
cons" — this genre will be too opinionated); or a **one-paragraph deliverable** (a memo is 1500–4000
words — overkill for a single page).
