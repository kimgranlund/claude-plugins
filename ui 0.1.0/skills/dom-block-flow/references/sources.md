# Sources — provenance in trust order

Corpus researched 2026-07-15 (one wave, four axes: box-model/flow, formatting-contexts/containing
blocks, stacking contexts, flex/grid mechanics). Re-run the wave for an axis when its canon moves
(a CSS Working Group spec advances stage, `contain`/`content-visibility` semantics shift, a new
`repeat()` keyword ships).

## Verification pass — 2026-07-15 (Issue #5)

The authoring wave's research agent never delivered its findings ledger, so an independent
citation-verification pass ran the same week: **71 claims checked against live
developer.mozilla.org and w3.org/TR pages — 70 CONFIRMED, 0 DIVERGED, 0 pages moved,
1 UNDETERMINED**. The full per-claim ledger (claim · verdict · live-page wording · URL · access
date 2026-07-15) is recorded in the repo's Issue #5 (git-native Findings).

The one UNDETERMINED claim, disclosed: box-model-and-flow.md's statement that a plain inline
box's vertical margin/padding "affects rendering but not surrounding layout." MDN confirms the
layout half (inline boxes ignore top/bottom margins) but no single MDN line states the
paints-without-affecting-line-height half; that half rests on CSS 2.1 inline-formatting
mechanics (line-box height is computed from line-height/vertical-align, not from inline padding,
which is why vertically-padded inline links visibly overlap adjacent lines). Kept, with this
note as its citation class — spec-mechanics-grounded, not page-quotable.

## Trust order

1. **Normative specs** — w3.org/TR/css-box-3 (box model), w3.org/TR/css-display-3 (BFC,
   `flow-root`), w3.org/TR/css-position-3 (containing block, z-index, stacking), w3.org/TR/
   css-flexbox-1, w3.org/TR/css-grid-1.
2. **Browser/platform reference** — developer.mozilla.org (MDN): "Box model", "Mastering margin
   collapsing", "Normal flow", "Block formatting context", "Containing block", "The stacking
   context", "z-index", "Basic concepts of flexbox", "Controlling ratios of flex items along the
   main axis", "Basic concepts of grid layout", "Subgrid", `repeat()`. MDN is treated as
   authoritative for phrasing and worked examples; the spec is the tie-breaker when MDN's own
   wording is ambiguous.

## Known unverified edges (kept out of the corpus, listed so nobody re-invents them)

- **Browser-specific rendering quirks.** This pack states spec/MDN-documented behavior, not
  per-browser bugs or historical quirks-mode differences — a "why does this only break in
  browser X" question is out of scope unless the divergence is itself spec-documented (e.g. an
  explicitly noted Baseline/interop gap).
- **`content-visibility` and `contain-intrinsic-size`'s interaction with formatting contexts** —
  genuinely relevant to modern layout performance but not covered in this wave; flagged as the
  next axis candidate if a real ask surfaces it.
- **Exact per-browser flex/grid algorithm edge cases** (e.g. the precise order of operations when
  `flex-basis: auto` interacts with `aspect-ratio`) — the spec's own algorithm is cited at the
  conceptual level this pack teaches; implementation-level edge cases are out of scope.
