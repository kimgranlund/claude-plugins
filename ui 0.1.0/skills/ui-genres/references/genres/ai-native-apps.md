---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; the eval-engineering, metrics, and wrapper-vs-product strategy sections dropped, UI conventions kept. The kept conventions are practitioner-observational (the source corpus's own labeling), not settled canon
coverage: expanded
primary_sources:
  - "Practitioner consensus across the current generation of AI-native products (observational; the category is young and short on settled benchmarks — claims below are labeled accordingly)"
---

# AI-native apps

AI-native apps are products whose **core value depends on a model's capability** — the model is not a feature bolted onto a conventional app but the thing the product is built around. The defining property is that the product's quality is **probabilistic and non-deterministic** — the same input can yield different outputs, quality is a distribution rather than a guarantee, and the underlying model can change beneath you. That single fact reshapes the UI: the interface must assume the model can be wrong, slow, and expensive, and absorb all three visibly rather than pretend to determinism.

> The UI-convention frame: a conventional app's interface promises "this button does this"; an AI-native interface promises "this will probably help — here is how to check it, correct it, and escape it." The conventions below all follow from designing for a distribution of quality, not a guarantee.

## Conventions: what these apps tend to share

These are observed regularities across the current generation of AI-native products, not a settled canon.

- **Model-capability-led design.** What the product can credibly do is bounded by what the model can do _reliably enough_, so design starts from capability and works back to UX — the inverse of conventional design, which starts from the desired UX. New model capabilities open new product surface; model weaknesses (hallucination, brittleness) define the guardrails the UI must render.
- **Human-in-the-loop and graceful degradation.** Mature AI products design for the model being wrong: confidence signals, easy correction, undo, citations/sources, and fallbacks to a deterministic path. The UX assumes a distribution of quality, not a guarantee — output is presented as reviewable and editable, never as silently committed fact.
- **Cost and latency as visible product constraints.** Unlike conventional software where marginal compute is ~free, every model call has real per-token cost and real latency, and both are felt directly in the product (see below).

## Latency as a UI constraint

Model inference is slow relative to a database read; a multi-second wait that would be unacceptable in conventional UI is routine here. The genre's standard mitigations are UI conventions in their own right:

- **Streaming responses** — show output as it generates rather than after; pair with a visible stop/cancel affordance.
- **Optimistic and progressive UI** — commit the user's input immediately, render the model's work as an in-progress state, and keep the surface interactive while it runs.
- **Fast paths for easy cases** — smaller/faster models or cached answers for common queries, reserving the slow frontier call for the hard ones, so the median interaction feels responsive.

Latency frequently constrains _what the product can be_ — some otherwise-good designs are infeasible because they'd be too slow to feel responsive. Cost and latency belong in the design conversation from the start, traded against quality; "use a bigger model" spends both budget and milliseconds (emerging operational consensus).

## Pitfalls

- **Ignoring cost/latency until production.** Designing a flow that is delightful in a demo but, at scale, either too slow to use or too expensive to sustain. These are product constraints, not infra afterthoughts.
- **Presenting probabilistic output as deterministic fact.** No confidence signal, no citation, no correction path — output silently written into the user's data as if a database read. The genre's UI contract is reviewability; dropping it converts every model error into a user-facing betrayal.
- **No escape hatch.** An AI-mediated flow with no deterministic fallback (manual entry, conventional search, direct edit) dead-ends the user exactly when the model fails — the moment the fallback exists for.

## Good vs. bad (for a genre-fit dimension)

| Dimension | Good (high genre-fit) | Bad (low genre-fit) |
| --- | --- | --- |
| Output posture | Reviewable, correctable, cited; undo available | Committed as silent fact; no provenance, no undo |
| Latency | Streamed, cancellable, progress visible | Blocking spinner; UI frozen for the full inference |
| Failure path | Deterministic fallback one step away | Model failure dead-ends the flow |
| Confidence | Uncertainty signaled where quality varies | Uniform confidence regardless of reliability |

The single most diagnostic question for genre-fit: **when the model is wrong or slow — which it will be — does the interface let the user see it, fix it, and route around it without leaving the flow?**
