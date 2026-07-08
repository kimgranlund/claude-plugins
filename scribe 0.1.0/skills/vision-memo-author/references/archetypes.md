# Archetypes — full section templates

Four archetypes, each a different *kind* of argument and therefore a different structure. `SKILL.md`
Step 1 selects one; this file is the section-by-section template + voice cues for the one you picked.
Rubric dimension V9 (archetype fit) scores whether the shape matches the argument's size.

---

## Archetype 1: Manifesto

**When:** a full vision for a new system, platform, or direction — the reader should leave with a
complete mental model of what's proposed, why, and how it unfolds over time. **Words:** 2500–4500.
**Exemplar:** "The Software Factory Manifesto."

```markdown
# {System Name}: {Subtitle that states the thesis}

## Part I: First Principles Decomposition
[Strip the problem to its atoms. 2–3 paragraphs, each ending on a sentence that constrains what follows.]
> {Blockquote: the reduced definition — the essence of what the system is.}
[One paragraph connecting the reduction to the design implication.]

## Part II: The N Essential Building Blocks
[Framing: "Everything else is composition of these."]
### 1. {Primitive Name}
{Define it: what it is, what it does, why it exists. End with what follows from its existence.}
### 2. {Primitive Name} … [3–7 total]

## Part III: Platform Foundation   [usually 3 layers]
### Layer 1/2/3: {Name} — {what this layer owns and why}

## Part IV: Core Principles   [4–6 non-negotiable constraints, each standing alone]
### 1. {Principle Name} — {one opinionated paragraph: what must be true and why}

## Part V: Operating Principles   [how the team works, day-to-day — shorter]
**{Principle}.** {Explanation.}

## Part VI: Path Forward — {Metaphor} → {Metaphor} → {Metaphor}   [3–4 phases, evocative names]
### Phase A: "{Name}" ({Metaphor})
*Goal: {one sentence.}*
[activities and capabilities]
**Milestone:** {concrete, verifiable signal of phase completion.}

## Part VII: The One Thing to Get Right First
[The highest-leverage decision. 2–3 paragraphs — where the conviction lands hardest.]

## Summary: {Meta-Framing}
| Principle | Implication |
|---|---|
| {Reduced claim} | {What follows} |
> {Closing aphorism. One or two short italicised sentences.}
```

**Voice cues:** open with scope or a claim-staking subtitle; use "we" sparingly — third-person abstract
("the factory does X") reads like a physics paper, not a pitch; phases should *unfold*, each implying
the next; the "One Thing" is the memo's secret — what the author would emphasise in person.

---

## Archetype 2: Reframe Essay

**When:** surgical — arguing one decision or concept should be seen differently than it commonly is. The
thesis is a lens, not a system. **Words:** 1500–2500. **Exemplar:** "Types as Physics in AI Systems."

```markdown
# {Concept} as {Reframed Lens}

## {The Current View} vs. {The Reframed View}
[Two paragraphs: how it's conventionally seen, then the reframe. Short closer stating the thesis cleanly.]
> {Italicised one-liner of the reframe — the memo's core claim.}

## The Root Problem
[Why the current view is inadequate — why the reframe is necessary, not just interesting.]

## The N {Leverage Points / Aspects / Implications}   [5–7, each self-contained]
### 1. {Aspect Name}
{Opening sentence states the claim.} {Develop with physics/mechanics/math where possible.} [concrete case]
**The leverage:** {one-paragraph summary of what this aspect buys you.}   ← the genre's signature pattern

## The Meta-Point: Why This Matters More {In Context / At Scale / Now}
[Elevation — why the reframe matters more than it first seems; often contrasts a less-constrained domain.]

## Summary: {Compressed Reframing}
| Leverage Point | What {The Thing} Does | Why It's Different {In Context} |
|---|---|---|
> {Closing — ideally three short parallel sentences, the third the twist. E.g.: "In deterministic
> systems, types catch errors. In probabilistic systems, types prevent categories of errors from being
> representable. That's a different physics."}
```

**Voice cues:** the opening contrast must be crisp — show the old view cleanly before replacing it; each
leverage point stands alone (a reader who reads one gets value); the closing is a mic drop — short,
declarative, memorable. No roadmap or phased rollout — that over-structures a reframe.

---

## Archetype 3: Case-For

**When:** the strategic/economic argument for an approach, for decision-makers who need to understand
not just what it is but why it's the right investment *now*. **Words:** 2000–3500. **Exemplar:** "The
Case for Schema-Driven Project Documentation."

```markdown
# The Case for {Approach}
## {Subtitle stating the thesis briefly}

## The Problem We've Been {Misdiagnosing / Ignoring / Undervaluing}
[The common (wrong) diagnosis and conventional response, then the pivot to what the problem actually is.]
> {Short italicised line: the reframe.}

## Why It Matters Now: The {Inflection / Shift}
[What changed that makes this urgent — a tech shift, scaling dynamic, or economic inversion. Show the
specific dynamic: what used to be tolerable but isn't.]
**{Bold summary of the shift in consequences.}**

## First Principles: What Is {X}, Actually?   [tighter than a manifesto's reduction — usually 3 truths]
**1. {Truth.}** {Explanation.}

## The {Approach} Approach   [what the reframed view produces as a solution]
### What {The Approach} Gives You
**{Benefit}.** {Why it follows from the approach.}   [4–6 benefits]

## What Changes in Practice   [concrete implications, subdivided by role]
### For {Role 1 / 2 / 3} — {how it changes their work}

## The Scaling Argument   [why it grows more valuable as the org grows — structural > process guarantees]
## The {Economic / Compounding} Argument   [ROI: cycle time / error reduction, or cost curves / leverage]

## The Transition   [pragmatic, demand-driven adoption path]
**Stage 1/2/3:** {pragmatic first step → backfill → default state}

## The Deeper Point
[Elevation — why this matters beyond the case; ties to a principle that applies more broadly.]
> {Closing — often the principle as a physical constraint or asymmetry.}
```

**Voice cues:** the misdiagnosis opening is the signature hook — make it sharp; "why now" must be
specific (if the argument held five years ago, you haven't found the real inflection); the transition
section is what distinguishes a Case-For from a pure reframe — the pragmatic path is *part of the
argument*; the Deeper Point hands the reader a principle they can apply elsewhere.

---

## Archetype 4: Synthesis

**When:** two or more competing positions exist; you analyse them to find conflicts, alignments, and a
path forward that honours what each gets right. **Words:** 1500–3000. **Exemplar:** "Architecture
Synthesis: Type-Driven vs. PKG/RL-Driven."

```markdown
# {Synthesis Topic}: {Position A} vs. {Position B}

## Context   [what the two positions are and why the comparison matters]

## Deep Alignments   [what both agree on — convergence suggests they track real principles; 3–5]
- **{Point of agreement}.** {Why both converge here.}

## Conflict {N}: {Title framing the choice}   [2–4 genuine conflicts]
**{Position A}:** {what it says.}  **{Position B}:** {what it says.}
**Why this matters:** {the implications — each position's failure mode.}
**Synthesis path:** {how the two reconcile, if they can.}

## Gaps {A} Fills for {B}  /  Gaps {B} Fills for {A}   [symmetric — what each has that the other lacks]

## Net Assessment   [the synthesis — the combination that honours what each gets right]
1. **{Recommendation}** — {reasoning.}   [3–5 numbered, describing the integrated approach]
[Closing: the biggest risk of each position, and why the synthesis mitigates it.]
```

**Voice cues:** evenhanded in the analysis, then take a position in the Net Assessment — fair until it's
time to synthesise; "why this matters" after each conflict turns an abstract tradeoff into a concrete
consequence; the synthesis must feel *earned by* the analysis, not imposed on it; end on the risk
framing.

---

## Choosing, and combining

Ask in order: proposing an entire system? → **Manifesto**. Arguing one concept should be seen
differently? → **Reframe**. Making the business/strategic case? → **Case-For**. Resolving competing
positions? → **Synthesis**. When in doubt, pick the smaller form — a reframe that lands beats a
manifesto that sprawls.

**Combining:** occasionally a manifesto contains a reframe *moment* inside it (a mini-reframe serving
the larger vision). But don't blend archetypes at the structural level — pick the dominant shape and let
sub-moves serve it.
