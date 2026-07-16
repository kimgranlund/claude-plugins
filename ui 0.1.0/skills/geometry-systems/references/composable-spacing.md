# Composable spacing — how nested insets and density actually compose

Researched 2026-07-15. This file generalizes a principle this estate already has ONE worked,
mechanized instance of (`component-forge`'s `references/geometry-system.md` §"Composed padding —
containers & lists") — read the principle here, see it derived and checker-enforced there; this
file does not restate that derivation.

## The composition rule: same-size nesting stacks, it doesn't collapse

When a container at scale-step *S* holds a child container also at scale-step *S*, the visible gap
at their shared boundary is **inset(S) + inset(S)** — both insets render, side by side — not a
single shared inset. This is the intended look, not a bug to "fix" by deduplicating the space: it
is what lets a card, the section inside it, and a control inside that section all read as
**one coherent rhythm** built from one scale, with no per-boundary special-casing. The alternative
(collapsing to a single shared inset at every boundary) requires the layout system to know it's
looking at a boundary between two same-scale containers and suppress one side — a rule that adds a
special case at every nesting depth instead of removing one.

**The failure this prevents:** ad hoc per-boundary spacing decisions ("this gap should be a little
tighter since it's inside something else") reintroduce exactly the judgment-call inconsistency the
scale exists to remove (see `scale-theory.md` §"Why a base unit at all"). Composable spacing keeps
every boundary's math identical regardless of nesting depth — the designer never re-derives a gap,
only picks which scale-step this container sits at.

## Density is a multiplier on rhythm, never on the frame

A density knob (compact / comfortable / spacious) should scale the *gaps between things*
(the spacer/gap values) and *never* the *frame* a glyph or control centers in (the box a component
occupies). Scaling the frame breaks whatever centering law the component's own geometry depends on
— an icon centered in a square cell via `(height − glyph) / 2` (component-forge's law) stops being
centered the moment density independently rescales the height without rescaling the icon by the
same factor. The safe density knob multiplies **rhythm** — the spacing *between* elements — while
leaving each element's own internal frame alone.

## Two-band systems: not every control family shares one ramp

A single scale rarely fits every control honestly. This estate's own worked instance
(`component-forge`'s geometry system) splits into a **comfortable** band (buttons, inputs, menu
items — sized on a height-driven ramp) and a separate **compact/dense** band (tags, badges,
switches, checkboxes — sized on their own two-tier ramp, because these controls are *always*
compact regardless of the surrounding density setting, and the comfortable band's `h/2` padding
law would over-pad a keycap or a slider thumb). The general principle: when one class of control is
categorically smaller/denser than the rest of the system in every density mode, it earns its own
band rather than being forced onto the low end of the shared ramp — a shared ramp assumes every
member scales the same way with density, and a compact-only control doesn't.

## Gutters and gaps compose the same way regions do

The same additive-not-collapsing rule applies one level up, between page regions rather than
components: the gap between two adjacent grid cells or list items is the scale's `gap` value at
that region's density, applied once per boundary — consistent with how `layout-decompose` expects
a region's internal grammar to read (that skill owns *where* the regions are; this pack owns *how
much space* separates them once the region map is decided).

## What this pack does NOT prescribe

- The *specific* numeric ramp for a specific component family — that is a maker skill's job
  (`component-forge`'s law, or a bound Material export via `material-design-geometry-tokens`).
  This file states the composition RULE those systems both already follow; it does not hand out
  new numbers.
- A raw CSS mechanism for the gap itself (`gap` property vs. margin vs. `:where()` selectors) —
  the box-model/flow mechanics that realize a gap in the DOM are `dom-block-flow`'s territory.

## House lock — nested radius composition (ruled 2026-07-16, Issue #9)

House ruling (informed by the 2026-07-15 external-skill review,
jakubkrehel/make-interfaces-feel-better@366f0f86e surfaces.md, adopted because it is the
geometrically coherent rule, not because the source says so): nested rounded surfaces compose as
**always `outerRadius = innerRadius + gap`**; never equal radii on nested surfaces — an inner
card sharing its container's radius leaves a visibly thicker corner seam that reads as a mistake,
and an inner radius LARGER than the outer reads as a different component family altogether.
*Validity domain (the escape hatch, shipped with the rule): when the gap exceeds ~`24px`, the
surfaces stop reading as nested — treat them as independent surfaces, each taking its own
surface-level radius; the formula only binds while the eye parses containment. Degenerate case:
working outer-fixed, `inner = outer − gap` clamps to `0` (square inner corners) when the gap
meets or exceeds the outer radius. Derived nested radii are computed values, never per-instance
overrides of the library's radius ramp — snap to the nearest ramp step where one exists
(component-forge's one-scale-per-library rule).* Precedence: a
project ruling (DESIGN.md/token lock, minted via a taste gate) overrides; this lock fills
silence.
