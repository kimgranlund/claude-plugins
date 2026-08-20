---
name: make-brand-stack
description: >-
  Produces the one-page reading of a brand — six load-bearing tiers (Root, Position, Point of
  View, Expression, Product, Stewardship), each condensed to a thesis sentence plus a short
  elaboration from a corpus layer. Editor posture: condense ruthlessly, cite the corpus, never
  invent. Use when the user wants a one-pager, an executive summary, or a condensed reading of a
  brand — "give me the brand stack", "one-page summary of this brand", "condense this brand
  corpus", "executive summary of the brand". NOT the full corpus export (save-brand-corpus) and
  NOT open-ended strategy work (make-brand).
disable-model-invocation: false
user-invocable: true
argument-hint: "[corpus-dir — default ./brand-corpus]"
---

# make-brand-stack

Produces the Brand Stack: a one-page reading of a brand — six load-bearing tiers, each condensed
from a corpus layer. Distinct from `seed-brand` (which exports the *whole* corpus as a
distributable). Posture is editor: condense ruthlessly to one sheet, cite the corpus, never
invent.

Corpus directory: `$ARGUMENTS` (default `./brand-corpus`, the same default `save-brand-corpus` and
`seed-brand` use).

## Procedure

1. **Inventory first.** Invoke the `brand-corpus` skill (and the corpus MCP if `corpus_dir` is
   configured) to read the real layers (`01-foundation` … `08-evaluation`) — work from what's on
   disk, not memory.
2. **Build the Stack**, following
   `${CLAUDE_PLUGIN_ROOT}/skills/brand-methodology-rules/references/brand-stack.md` — the six
   tiers, the tier↦layer map, and each tier's guards-against filter. For each tier, extract one
   thesis sentence plus a ≤50-word elaboration from its source layer(s); don't restate the whole
   layer.
3. **Render** into `${CLAUDE_PLUGIN_ROOT}/templates/brand-stack-one-pager.md`. Monochrome,
   text-only, one sheet. Any polish (colour, logo, PDF) happens downstream in a publishing tool,
   never in the template.
4. **Show maturity honestly.** A tier whose layer the corpus hasn't reached → render
   `— not yet defined (layer NN missing)` and name what's missing. A Stack with the strategy tiers
   filled and the rest blank is a stage-2 brand honestly shown, not a failure.

## Failure branches

- A tier can only be written by asserting rather than citing the corpus → that's an undone layer,
  not a rendering problem: say so, point at `make-brand` to fix the corpus, then re-render — never
  fill the tier from a wish.

## Done / NOT done

Done when all six tiers are either filled from cited corpus content or honestly marked missing,
and the sheet stays to one page. NOT done if a tier was filled with asserted, uncited prose.
