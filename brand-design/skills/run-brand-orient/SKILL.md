---
name: run-brand-orient
description: >-
  Gets your bearings in a brand before doing any work — inventories the corpus, reads it against
  the methodology as working / drifting / missing, and proposes next steps by pipeline stage. Use
  when the user has just been handed a brand and doesn't know what exists, or asks "where does
  this brand stand", "what's in this brand corpus", "orient me on this brand", "what should we do
  next with this brand". NOT for making new work (make-brand), scoring existing work
  (check-brand-rubric), or the one-page brand-stack summary (make-brand-stack).
disable-model-invocation: false
user-invocable: true
argument-hint: "[optional focus]"
---

# run-brand-orient

Orient mode: gets your bearings in a brand before doing any work — the right cold-start move when
handed a brand with no context yet. Posture is surveyor — map first, opine second.

Optional focus: `$ARGUMENTS`

## Procedure

1. **Inventory the corpus.** Invoke the `brand-corpus` skill (and the corpus MCP, if `corpus_dir`
   is configured) to enumerate what's actually on hand — strategy docs, positioning, the
   Foundation Canon, expression system, voice guidance, tokens, prior identity work. List what's
   found by pipeline stage (`research → strategy → expression → stewardship`). MCP not configured
   → work from whatever the user points at and say so.
2. **Read the state.** Using the `brand-methodology-rules` skill as the yardstick, assess the
   corpus on three axes:
   - **Working** — solid, grounded, load-bearing.
   - **Drifting** — exists but inconsistent, stale, or off its own stated strategy.
   - **Missing** — what a coherent brand needs that isn't here at all (no grounded positioning, no
     point of view, no voice spec).
3. **Close with next steps.** A short, structured plan — a few concrete moves in priority order,
   each pointing at the right next skill (`make-brand` to make, `check-brand-rubric` to score,
   `check-brand-council` for a hostile read). Keep it tight — the user should know exactly what to
   do next.

## Failure branches

- Corpus MCP configured but returns nothing → say so explicitly rather than reporting an empty
  brand as "nothing exists yet."
- No corpus and no user-pointed material at all → report stage 0 (per `brand-corpus`'s maturity
  scale) and point straight at `make-brand`.

## Done / NOT done

Done when the inventory is listed by pipeline stage, the three-axis read is given, and the
next-step plan names concrete skills in priority order. NOT done if the assessment asserts a
brand's state from memory instead of the actual corpus contents.
