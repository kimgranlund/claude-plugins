# Roster & personas

## The persona contract

A **persona** is one named critic's full point of view, written as a standalone file: stance,
posture, tone, the specific things that lens catches that others miss, and its own prompt set to
run in-character against an artifact. A persona file is inlined whole into its critic dispatch —
never read off disk by the dispatched critic itself, and never summarized before it reaches the
critic. Losing any of that content between the roster and the dispatch defeats the fan-out: a
paraphrased persona is a weaker, blended voice, not the named critic's own.

A persona carries no knowledge of the machinery around it — it does not know it is one of N
critics, does not know the severity-voting mechanics, and does not know whether it is in the blind
phase or the deliberation phase unless the dispatch explicitly tells it (the two-phase model,
`two-phase-model.md`, is what adds that awareness in phase 2). The persona's OWN prompt set is the
one thing that never changes between an instance and its next; everything else — which sub-council
it sits in, which artifact it reviews — is supplied per dispatch.

## The roster

A **roster** is the full named set of personas available to one council instance. The roster is
domain configuration, not machinery: a brand council's roster is 14 named practitioners; a
different domain's council supplies its own roster entirely. Nothing in this pack fixes how many
personas a roster holds or who they are — only that a roster exists, that every member is a real
persona file (never an ad-hoc unnamed voice), and that the roster is enumerated somewhere a
dispatcher can read it (a table, a directory listing) rather than assembled from memory each time.

## Sub-councils

A **sub-council** is a named subset of the roster, grouped by the lens those personas share (a
brand instance's `strategy` / `design` / `voice` groupings). Sub-councils exist for two reasons:

1. **Scoped review.** Not every artifact needs all lenses — a positioning brief needs the strategy
   lens, not the type system critique a design sub-council would run.
2. **The blind-spot handle.** A sub-council's own synthesis can name what it structurally cannot
   see (`synthesis-shapes.md`'s blind-spot prompt) and hand off to the sub-council that can.

**`full`** is the reserved name for the union of every sub-council — every persona in the roster,
fanned out together. An instance's default sub-council (when none is named) is its own
configuration choice, stated explicitly rather than left for a dispatcher to guess.

## What a domain instance supplies vs. inherits

| Supplied by the domain instance (configuration) | Inherited from this pack (machinery) |
|---|---|
| The roster itself — who the named personas are | The persona-contract shape (inlined, not read on-disk by the critic) |
| Sub-council groupings and the default | The `full` = union convention |
| The critic-shell agent's model/tool tier | The dispatch discipline (unnamed, synchronous, same-turn concurrency) |
| Which sub-council a request maps to when unnamed | The bounded-rejection retry rule |

An instance that reinvents any right-column behavior locally, rather than citing this pack, is the
drift this generalization exists to prevent — the same reference-pack-vs-action-twin discipline
`check-brand-council` itself already proved out for its own domain packs (brand-corpus,
brand-methodology-rules, brand-rubrics): this pack states the mechanism, the action-twin runs it.
