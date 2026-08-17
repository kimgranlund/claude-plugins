# Assembling the per-turn trace, and diagnosing a failure in ONE format for two audiences

> Axis: for a deployed chat product's own producer/turn loop (distinct from this pack's other
> files, which are about THIS harness's own hook-based observability), who assembles the trace
> and what a failure message must name. Grounded in a worked instance: `@agent-ui/a2ui`'s
> `produce.ts`/`meta-line.ts`.

## The driver assembles the trace; the model never authors its own

**Claim — `TurnTrace` (retrieval query, exemplar ids, retry rounds, healed-line count, failure
codes, model) is runtime-assembled and attached by the loop itself; a model-authored `trace`
field is ignored if one is ever present.** Observability facts and model output are different
PROVENANCE classes riding one wire — conflating them would let a model narrate its own trace,
which defeats the entire point of an independently-assembled audit trail. ·
`meta-line.ts:41-60,143-157` (ADR-0088 §2) · 2026-08-17 · [verified]

## Say WHICH member and WHERE, in one format for both audiences

**Claim — a halt naming only the failure code ("IDGRAPH") was undiagnosable live without
re-instrumenting; each failure now renders `CODE at path`, the SAME wording fed back to both the
operator's logs and the model's own retry prompt — one format, two audiences, so the two surfaces
can never disagree about what went wrong.** · `produce.ts:294-314` (GH #307) · 2026-08-17 ·
[verified][incident]

## What this file does NOT cover

This harness's OWN hook-based tracing mechanism (PreToolUse/PostToolUse, this repo's dev-time
observability) — a distinct concern grounded in a different system entirely: this pack's own
`logging-and-tracing.md`. Keeping a repair-rate METRIC from saturating on mechanical noise, and
decoupling progress delivery from a provider's own yield cadence:
`metric-integrity-and-progress-delivery.md`.
