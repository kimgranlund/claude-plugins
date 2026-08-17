---
name: thinking-depth-rules
description: >-
  The n-order reasoning spectrum for matching judgment depth to a decision, and for naming when a
  rule itself — not just the latest attempt — is wrong. Use for "push the reasoning further",
  "question the rules themselves", "the same finding keeps recurring despite fixes", "are we at a
  local maximum", or "is this improvement real or just relabeling". NOT the wording layer
  (prompt-wording-rules); NOT a structural breakdown (break-down-problem); NOT extracting the ask
  (find-intent); NOT a scored baseline→change→remeasure loop (docs:research-methods) — this skill
  judges whether a rule deserves scrutiny, it never runs the loop that scores a change.
disable-model-invocation: false
user-invocable: false
---

# Reasoning Orders

A spectrum for matching reasoning depth to the decision at hand — and for refusing both failure
modes: under-reasoning (organizing when transformation was available) and over-reasoning (paradigm
theater where a rename suffices). Provenance: the spectrum is the user's framework [imported
2026-07-07]; the escalation triggers, worked examples, and rent rule are this project's practice,
distilled from harness's own build.

## The spectrum

| Order | Core question | Architectural level | Worked example |
|---|---|---|---|
| 1st | What does the data say? | Tool execution | Run the lint; read the graph; count the files. |
| 2nd | How well did I analyze it? | Reflection / self-check | The validator validates itself: a script's `selftest`, a gate refusing its own bad ship, generator ≠ critic audits. |
| 3rd | How will the other player react to my act? | Multi-agent / game theory | Model the router and the consumer: a blind routing judge choosing from the menu; fence closure anticipating sibling theft; a description written for how it will be *read*, not what it says. |
| 4th | How will the ecosystem react to those reactions? | Network / ecosystem simulation | A shared listing budget; trust re-decisions on every update; namespace competition across *all* installed plugins; partition by install/update behavior, not folder resemblance. |
| 5th | Are the system's rules themselves wrong or limited? | Ontological / paradigm evolution | Falsify a given law and amend the corpus: a documented invariant disproved and re-modeled; a rule discovered to be *about* rules; asking "is this even the right unit?" before restructuring. |

## Escalation protocol

Default to the **lowest order that changes the decision** — orders are not virtue tiers, and most
work is correctly 1st/2nd order. Escalate one level when, and only when, a trigger fires:

- **→ 3rd** when the artifact's success depends on another agent's choice: any description, fence,
  dispatch prompt, or partition whose consumer is a router, a judge, or a rival sibling.
- **→ 4th** when there is more than one consumer and they interact: shared budgets, marketplaces,
  version streams, trust cadences — anywhere a locally-optimal choice can be globally corrosive.
- **→ 5th** when the *same class* of finding recurs despite fixes (three-strikes is a 5th-order
  alarm: the rules need a rule), when the four tests of a decision skill conflict rather than
  converge, when every candidate answer feels like relabeling — or when the honest reading of the
  evidence contradicts a given "law" (then falsify it in place, dated, per pack-writing-rules'
  amendment rule).

And **de-escalate on completion**: a 5th-order insight is finished only when it lands back at 1st
order — a changed rule, a new check, an amended corpus line. Insight that never re-enters the
machinery is commentary.

## The rent rule

Every claim above 2nd order pays rent in the currency of the order below it:

- A 3rd-order claim ("the router will steal this") names the eval case that will prove it.
- A 4th-order claim ("this partition decouples update churn") states the number: installs avoided,
  updates decoupled, budget freed.
- A 5th-order claim ("the rule itself is wrong") produces a falsifiable check, an amended standard,
  or a measured delta — "orders of magnitude better" is quantified or it is discarded. The model
  case: "library-only doesn't exist" paid rent as a dead-state table row, two rewritten routing
  steps, and a lint-enforceable invariant — not as a manifesto.

## Anti-patterns

| Anti-pattern | Signature | Correction |
|---|---|---|
| Order cosplay | Ordinary analysis wearing a "5th-order" label | Ask which *rule* changed; none → it was 1st/2nd order, fine, say so |
| Paradigm inflation | Re-founding the ontology when a rename suffices | The lowest-order fix that fully resolves the finding wins |
| Unfalsifiable uplift | "Dramatically better" with no measure | Rent rule; no number, no claim |
| Escalation as avoidance | Philosophizing about the system instead of running its checks | 1st order first, always; the data may dissolve the question |
| Tidying as transformation | A "refactor" that reproduces the input's structure with new labels | If the output graph is isomorphic to the input's, no reasoning above 1st order occurred — name that honestly |

## Routing

Language of the artifact → `prompt-wording-rules`. Structure of the problem →
`break-down-problem`. What's actually being asked → `find-intent`. Whether decisions earned their
verdicts → the decision skills' own tests; this skill governs how high those tests must reach.

**Boundary vs. `docs:research-methods`.** Both surface on "why did this recur", "is this actually
better", "are we stuck". The discriminator is whether a scorer runs: research-methods fixes a
measure and loops baseline→change→remeasure→keep-or-revert against it — a regression, a tuning
knob, a stress test. This skill has no scorer and never measures a delta; it judges whether a
*rule or model* deserves scrutiny at all — the recurrence itself as 5th-order evidence, tidying
mistaken for transformation, escalation as a decision (not an experiment) about how far to push
reasoning. A research-methods loop can conclude "the rule is wrong" as a finding; this skill is
what decided the loop was worth escalating to in the first place.
