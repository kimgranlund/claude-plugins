# Stacking contexts

Researched 2026-07-15 from MDN ("Stacking context", "z-index") + w3.org/TR/css-position-3 §CSS
Positioning: z-index property.

## What creates a new stacking context

A stacking context is a self-contained z-ordering unit: once an element establishes one, every
descendant's `z-index` is compared only against its OWN stacking context's siblings — it can never
be compared directly against elements outside that context. Any of the following creates a new
stacking context on an element (this list is long by spec design — treat "did this establish a
stacking context" as a real question to check, not an assumption):

- The root element (`<html>`), always.
- `position: absolute` or `relative` WITH a `z-index` other than `auto`.
- `position: fixed` or `sticky` (these create one unconditionally, with or without an explicit
  `z-index` — a common surprise, since absolute/relative need the `z-index` and fixed/sticky
  don't).
- `opacity` less than 1.
- `transform`, `filter`, `backdrop-filter`, `perspective`, or `will-change` naming any of the
  properties that themselves create a stacking context.
- `isolation: isolate` — exists SPECIFICALLY to force a new stacking context with no other visual
  side effect, when nothing else on the element already creates one.
- `mix-blend-mode` other than `normal`.
- Flex/grid items with a `z-index` other than `auto` (even though the flex/grid container's
  `position` is `static`).
- `contain: layout`, `paint`, `strict`, or `content`.

(MDN, "The stacking context" — accessed 2026-07-15.)

## Why a z-index inside one stacking context can never escape above a sibling's

Stacking contexts nest, and an element's `z-index` is only ever meaningful **relative to its own
parent stacking context** — a descendant with `z-index: 9999` painted inside a stacking context
that itself sits BELOW a sibling stacking context will still render underneath that sibling,
because the comparison never happens at the descendant's level; the browser first resolves which
of the two ANCESTOR stacking contexts wins, then paints everything inside the loser beneath
everything inside the winner, regardless of how large a z-index the loser's descendants declare.
Escaping this requires raising the z-index (or otherwise re-ordering) at the ANCESTOR stacking
context's own level, not the descendant's. (MDN, "The stacking context" — accessed 2026-07-15.)

**The failure this explains:** a modal/dropdown with an enormous `z-index` (`z-index: 999999`)
still rendering behind another part of the page — the actual fix is almost never a bigger number;
it's finding which ancestor accidentally created a losing stacking context (a `transform` on a
card wrapper is the single most common accidental culprit, since `transform` creates a stacking
context as a side effect nobody was reaching for) and either removing that trigger or moving the
modal to render outside that ancestor (a portal/teleport pattern exists specifically to route
around this).

## Stacking order within one context (painting order, not z-index alone)

Within a single stacking context, painting order (back to front) is, in order: the context-forming
element's own background/border, then negative-z-index descendants, then non-positioned in-flow
descendants (block, then floats, then inline), then `z-index: auto`/`0` positioned descendants,
then positive-z-index descendants. A negative `z-index` therefore paints BEHIND the stacking
context's own background only if that background is opaque enough to matter — it does not escape
to a lower stacking context, it only reorders within the current one. (MDN, "The stacking context"
— accessed 2026-07-15.)
