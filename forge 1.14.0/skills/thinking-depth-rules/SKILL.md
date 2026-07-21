---
name: thinking-depth-rules
description: >-
  The n-order reasoning spectrum, operationalized for decision and refactor work: which order a
  decision actually demands, the question each order asks, when to escalate, and the rent rule
  that keeps higher-order claims honest. Use when a verdict feels like tidying rather than
  improvement, when the same finding class recurs despite fixes, when tests conflict, when asked to
  "push the reasoning further", "question the rules themselves", "apply higher-order reasoning",
  "check whether we're at a local maximum", or "how do I know if this improvement claim is real
  or just relabeling" — and when any skill's output would merely reorganize what exists. NOT the
  wording layer (prompt-wording-rules); NOT a structural breakdown (break-down-problem); NOT
  extracting what's being asked (find-the-ask); NOT running a measured experiment against a
  scorer to find out empirically (docs' research-methods) — this governs the judgment call of
  what order of claim is being made, not the measurement itself.
disable-model-invocation: false
user-invocable: false
---

# Reasoning Orders

A spectrum for matching reasoning depth to the decision at hand — and for refusing both failure
modes: under-reasoning (organizing when transformation was available) and over-reasoning (paradigm
theater where a rename suffices). Provenance: the spectrum is the user's framework [imported
2026-07-07]; the escalation triggers, instantiations, and rent rule are this project's practice,
each anchored to a dated worked case from harness's own build.

## The spectrum

| Order | Core question | Architectural level | Forge-scale instantiation (worked case) |
|---|---|---|---|
| 1st | What does the data say? | Tool execution | Run the lint; read the graph; count the files. (`skill_lint.py`, `surface_map.py map`) |
| 2nd | How well did I analyze it? | Reflection / self-check | The validator validates itself: every script's `selftest`, the gate refusing its own bad ship, generator ≠ critic audits. (G4; the fixture that had to *actually* cross a preload edge) |
| 3rd | How will the other player react to my act? | Multi-agent / game theory | Model the router and the consumer: blind `/check-routing` judges choosing from the menu; fence closure anticipating sibling theft; a description written for how it will be *read*, not what it says. (stolen/leaked shapes) |
| 4th | How will the ecosystem react to those reactions? | Network / ecosystem simulation | The shared 1% listing budget; trust re-decisions on every update; stutter and namespace competition across *all* installed plugins; partition by install/update behavior, not folder resemblance. (G8; the lifecycle ledger) |
| 5th | Are the system's rules themselves wrong or limited? | Ontological / paradigm evolution | Falsify the given laws and amend the corpus: the §6.6 library-only state disproved and re-modeled; mention-vs-use discovered as a rule *about* rules; asking "is the plugin even the right unit?" before partitioning plugins. |

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
`break-down-problem`. What's actually being asked → `find-the-ask`. Whether decisions earned their
verdicts → the decision skills' own tests; this skill governs how high those tests must reach.
