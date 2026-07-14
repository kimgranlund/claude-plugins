# Flexbox and Grid — sizing algorithms and their gotchas

Researched 2026-07-15 from MDN ("Basic concepts of flexbox", "Controlling ratios of flex items
along the main axis", "Basic concepts of grid layout") + w3.org/TR/css-flexbox-1,
w3.org/TR/css-grid-1.

## Flexbox: main axis, cross axis, and how the three flex properties compute final size

A flex container lays items along a **main axis** (set by `flex-direction`; `row` = horizontal by
default) and wraps/aligns them along the **cross axis** (the perpendicular one). Each item's final
main-axis size comes from resolving three properties together, not any one alone:

- **`flex-basis`** — the item's starting main-size, BEFORE growing or shrinking is applied (an
  explicit length, or `auto` to fall back to the item's own `width`/`height` or content size).
- **`flex-grow`** — a unitless ratio: once every item's basis is laid out, any REMAINING positive
  space in the container is distributed proportionally by each item's grow value (an item with
  `flex-grow: 2` takes twice the leftover space of one with `flex-grow: 1`; items with `0` never
  grow beyond their basis).
- **`flex-shrink`** — the same proportional idea in reverse, applied only when the combined basis
  of all items OVERFLOWS the container; items shrink proportionally by their shrink value (weighted
  by their own basis size too, per spec) until the overflow is resolved or every shrinkable item
  hits its own minimum size.

(MDN, "Controlling ratios of flex items along the main axis" — accessed 2026-07-15.)

## The `min-width: auto` gotcha — why a flex item overflows despite `flex-shrink`

Flex items have an **automatic minimum size** by default (`min-width`/`min-height: auto`), which
resolves to the item's own CONTENT'S minimum size (e.g. the longest unbreakable word, or an
image's intrinsic width) — NOT zero. This means `flex-shrink` can never shrink an item below its
own content-driven minimum, no matter how large its shrink value is: a flex item holding a long
unbreakable string or a wide image will overflow the flex container rather than shrinking to fit,
because the automatic minimum silently overrides the shrink calculation. The fix is setting an
explicit `min-width: 0` (or `min-height: 0` on the cross axis in a column flex) on the item,
which removes the content-based floor and lets `flex-shrink` actually reach small sizes. (MDN,
flex item sizing — accessed 2026-07-15; commonly documented as the single most-reported flexbox
overflow surprise.)

**The failure this explains:** "I set `flex-shrink: 1` and `overflow: hidden` but the item still
overflows the row" — the shrink value was never the limiting factor; the automatic content minimum
was, and `min-width: 0` (or an explicit smaller value) is the actual fix, not a larger shrink
number.

## Grid: explicit vs. implicit tracks, and `fr` unit distribution

**Explicit tracks** are the rows/columns named directly via `grid-template-columns`/
`-rows`; **implicit tracks** are created automatically when content is placed outside the explicit
grid (sized by `grid-auto-rows`/`grid-auto-columns`, default `auto`). The **`fr` unit** distributes
the container's remaining space (after all fixed-size and content-sized tracks are laid out)
proportionally among the tracks that use it — `1fr 2fr` splits leftover space 1:2, exactly like
`flex-grow`'s ratio model, but at the TRACK level rather than the item level. (MDN, "Basic
concepts of grid layout" — accessed 2026-07-15.)

## `auto-fill` vs. `auto-fit` in `repeat()`

Both create as many tracks of the given size as fit the container, but they diverge on what
happens with LEFTOVER empty tracks once content runs out:

- **`auto-fill`** keeps the empty tracks it created — visible gaps remain at the trailing edge if
  there isn't enough content to fill every generated track.
- **`auto-fit`** collapses those empty tracks to zero width, letting the tracks that DO have
  content stretch to fill the freed space instead of leaving a gap.

(MDN, `repeat()` — accessed 2026-07-15.) The failure this explains: a responsive card grid built
with `auto-fill` leaving a visible dead gap on a wide viewport with too little content to fill
every column — `auto-fit` is almost always the intended behavior for a content grid that should
never show trailing empty space.

## Subgrid's actual purpose

`subgrid` (on `grid-template-columns`/`-rows`) lets a nested grid item INHERIT its parent grid's
track sizing instead of defining its own independent tracks — its purpose is aligning content
across multiple sibling grid containers (e.g. several cards whose internal labels should all
align to the same column boundaries as their shared parent grid), which plain nested grids cannot
do because each nested grid otherwise sizes its own tracks independently of its siblings. (MDN,
"Subgrid" — accessed 2026-07-15.)
