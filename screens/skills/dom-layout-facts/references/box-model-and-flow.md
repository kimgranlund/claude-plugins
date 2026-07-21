# Box model and normal flow

Researched 2026-07-15 from MDN (developer.mozilla.org) as primary source, cross-checked against
the CSS Working Group specs (w3.org/TR/css-box-3, w3.org/TR/css-display-3) where MDN's own
phrasing is informal.

## The box model — four areas, one sizing switch

Every element generates a box built of four concentric areas, outside to in: **margin** (invisible
spacing outside the border, never paints) → **border** → **padding** → **content**.
`box-sizing` decides which of those areas an explicit `width`/`height` measures:

- **`content-box`** (the CSS default) — `width`/`height` set the CONTENT area only; padding and
  border add ON TOP, so an element's rendered footprint is always larger than the declared
  width/height. (MDN, `box-sizing` — accessed 2026-07-15.)
- **`border-box`** — `width`/`height` set the outer edge of the BORDER; padding and border are
  carved out of that budget instead of adding to it. This is why most CSS resets apply
  `box-sizing: border-box` globally: it makes `width: 100%` plus padding behave predictably
  instead of overflowing its container. (MDN, `box-sizing` — accessed 2026-07-15.)

Margin never participates in either box-sizing mode — it always sits outside the border and is
never part of an element's own measured size.

## Margin collapsing — when two margins become one

Adjoining vertical margins between block-level boxes in normal flow **collapse into a single
margin** equal to the larger of the two (not their sum) — this is normal-flow behavior, not a bug.
Collapsing happens between: **adjacent siblings** (one element's bottom margin touching the next
element's top margin), a **parent and its first/last child** (when nothing separates them), and an
**empty block's own top and bottom margin** (collapsing into itself). (MDN, "Mastering margin
collapsing" — accessed 2026-07-15.)

**What prevents collapsing** (any one of these breaks the adjoining-margin condition):
- Padding or border on the parent, between the parent's edge and the child's margin.
- The parent establishing a new **Block Formatting Context** (see `formatting-contexts.md`) —
  collapsing never crosses a BFC boundary.
- `overflow` other than `visible` on the parent.
- The elements being in different formatting contexts (e.g. one is a flex/grid item — flex and
  grid containers do NOT collapse margins with their children at all, by spec).

**The failure this explains:** unexpected extra whitespace at the top of a container — the
container's supposedly-zero top margin is actually the CHILD's top margin collapsing straight
through the parent's own top edge, because nothing (no padding, no border, no BFC) stopped it.

## Normal flow: block, inline, and how `display` changes participation

In normal flow, **block-level boxes** stack vertically, each taking the full available inline
width by default and starting a new "line" regardless of content width. **Inline-level boxes** flow
horizontally within a line, wrap at the inline axis's edge, and do not accept `width`/`height` (an
inline box's dimensions come from its content) unless changed to `inline-block`, which flows
inline but accepts explicit sizing and padding/margin on all four sides (a plain inline box's
vertical margin/padding affects rendering but not surrounding layout — the classic "why doesn't
this padding push other lines away" surprise). `display: none` removes a box from flow (and the
accessibility tree) entirely; `visibility: hidden` hides it but the box still occupies its space in
flow. (MDN, "Normal flow", `display` — accessed 2026-07-15.)
