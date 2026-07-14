# Block Formatting Contexts and containing blocks

Researched 2026-07-15 from MDN + w3.org/TR/css-display-3 (BFC), w3.org/TR/css-position-3
(containing block resolution).

## What a Block Formatting Context (BFC) actually does

A BFC is a region of the page that lays out its contents independently of the rest of the page.
Establishing one has three concrete, checkable effects:

1. **It contains floats.** A parent with a BFC will size to enclose its floated children instead
   of collapsing to zero height around them (the classic "clearfix" problem — before `clear` or a
   BFC trigger, a container with only floated children reports zero height because floats are
   removed from normal flow).
2. **It stops margin collapse from crossing its boundary.** A child's margin can no longer collapse
   through a BFC-establishing parent's edge (see `box-model-and-flow.md`).
3. **It does not overlap floats from outside itself.** A BFC's box will not run under an
   already-floated element beside it — instead its content area shrinks to avoid the float, which
   is how a classic two-column "sidebar float + BFC main content" layout worked before flexbox/grid.

**What triggers a new BFC** (any ONE is sufficient): `overflow` set to anything other than
`visible` (including `hidden`, `auto`, `scroll`) on the block itself; `float` other than `none`;
`position: absolute` or `fixed`; `display: flow-root` (the modern, side-effect-free way to
establish a BFC on purpose — MDN explicitly recommends it over `overflow: hidden` when the ONLY
goal is a new BFC, since `overflow: hidden` also clips overflowing content as an unwanted side
effect); `display: inline-block`, `table-cell`, `table-caption`, `flex`, `grid`, or their inline
equivalents; `contain: layout` (or `content`/`paint`/`strict`, which imply `layout`). (MDN, "Block
formatting context" — accessed 2026-07-15.)

**The failure this explains:** reaching for `overflow: hidden` to "fix" a collapsed-height float
container is solving the BFC problem with a side effect (clipping) nobody asked for — `display:
flow-root` establishes the same BFC with none of overflow's clipping behavior.

## The containing block — what a positioned element actually positions against

Every element's size and position calculations resolve against its **containing block** — but
which box that is depends entirely on the element's own `position` value:

- **`static` or `relative`:** the containing block is the nearest **block-level ancestor's content
  box** (or the initial containing block, for a root element) — the intuitive "my parent" answer.
- **`absolute`:** the containing block is the nearest ancestor whose `position` is anything OTHER
  than `static` (relative, absolute, fixed, or sticky) — specifically that ancestor's **padding
  box**, not its content box (which is why an absolutely positioned child can end up inset
  differently than expected if the positioned ancestor has padding). If NO ancestor is positioned,
  the containing block falls all the way back to the initial containing block (the viewport, in
  the common case) — the classic "why did my `position: absolute` element jump to the top of the
  whole page" surprise, caused by forgetting `position: relative` on the intended parent.
- **`fixed`:** the containing block is the viewport itself (or the nearest ancestor with certain
  properties that create a new containing block for fixed elements, e.g. a `transform`, `filter`,
  `will-change: transform`, or `contain: paint` value — a lesser-known trap: a `transform` anywhere
  in the ancestor chain "hijacks" fixed positioning away from the viewport).
- **`sticky`:** resolves against its nearest scrolling ancestor and its own normal-flow position,
  not a single containing-block ancestor the way absolute/fixed do — a sticky element also
  requires that scrolling ancestor to actually have room to scroll AND no ancestor between it and
  the sticky element may have `overflow` clipping that removes the scroll (a very common reason
  "sticky doesn't work" in nested scroll containers).

(MDN, "Containing block", `position` — accessed 2026-07-15.)

**The failure this explains:** a percentage width/height on a descendant silently resolving against
the wrong ancestor, because the containing block was never the element the author assumed — always
trace which ancestor the position value actually resolves against before debugging the percentage
itself.
