---
name: dom-layout-facts
description: >-
  Answers how to reason within HTML/CSS layout mechanics — box model, normal flow, block
  formatting contexts (BFC), stacking contexts, containing blocks, flex/grid algorithms — from a
  cited MDN/CSS-spec corpus. Use for "why did this margin collapse", "what triggers a new BFC",
  "why can't this z-index escape its parent", "why is this flex item overflowing despite
  flex-shrink", "auto-fill vs auto-fit", "why doesn't height: 100% work". ANSWERS the mechanism;
  does not derive a component's sizing law (make-component) or spacing-scale theory
  (size-and-shape-rules).
user-invocable: false
disable-model-invocation: false
---

# dom-layout-facts — the box-model and layout-mechanics world model

Answers why the DOM actually lays out the way it does — box model, flow, formatting contexts,
stacking, containing blocks, flex/grid algorithms — from a cited, dated corpus, so a layout bug
gets root-caused against the actual mechanism instead of patched by trial-and-error CSS.

| Ask | Load |
|---|---|
| Box model, margin collapse, block vs inline participation in normal flow | `references/box-model-and-flow.md` |
| What triggers a Block Formatting Context, what a BFC actually does, containing blocks | `references/formatting-contexts.md` |
| Stacking contexts — what creates one, why z-index can't escape its parent | `references/stacking-contexts.md` |
| Flexbox and Grid's own sizing/track algorithms and their common gotchas | `references/flex-and-grid-mechanics.md` |
| Provenance and the unverified edges | `references/sources.md` |

## Consult procedure

1. Classify the ask: box model/flow · formatting context/containing block · stacking · flex/grid
   mechanics. Load only the matching reference.
2. Answer on the contract: **claim + cited source (MDN or the CSS spec) + the failure mode the
   mechanism explains**. Worked shape:
   > *"Why didn't `height: 100%` work on this child?"* → box-model/flow ask → a percentage height
   > resolves against the containing block's own computed height, and an ancestor with no
   > explicitly-set height computes to `auto` — so the percentage has nothing to resolve against
   > and collapses. The failure this explains: reaching for `!important` or a fixed pixel height
   > instead of giving one ancestor in the chain an explicit height (MDN, `<percentage>` box
   > sizing — accessed 2026-07-15).
3. State which register the answer comes from: spec/MDN-cited vs. general convention — and say so
   when it's the latter.
4. Route derivation/build work at the boundary (below) — this pack explains mechanism, it never
   emits component code or a token file.

## Boundaries

- **This skill answers CSS/DOM mechanics; it does not derive a sizing law or build anything.** A
  control's own height→padding→radius derivation is `make-component`'s law
  (`references/geometry-system.md`); the THEORY behind why a spacing scale has the shape it does
  is `size-and-shape-rules`. This pack explains the *substrate* those systems are realized on top of —
  why a `gap` property behaves the way it does in flow, not what value to put in it.
- **Page-region placement** (where a sidebar sits, whether a frame is fixed) →
  [[break-down-layout]]; that skill's A1 "Frame" gate asks whether a fixed frame exists at all —
  this pack explains the mechanism (position/containing-block/BFC) that makes a frame behave as
  fixed or not.
- **Production component code** → [[make-component]] — this pack explains why a CSS rule behaves
  a certain way; it does not write the rule for a specific component.

## Extending this pack

Extension: governed by [[make-pack]]
