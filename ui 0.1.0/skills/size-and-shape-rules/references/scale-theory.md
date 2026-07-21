# Scale theory — base unit, progression shape, and why every system converges

Researched 2026-07-15 from primary sources (m1/m3.material.io, tailwindcss.com + the Tailwind
Labs GitHub discussions, carbondesignsystem.com). Every value below is cited; where a claim is
observed convention rather than a stated rule, it says so.

## Why a base unit at all

A dimensional scale is a **closed set of legal values**, not a design constraint — the reason to
adopt one is the same reason a type scale exists: an unconstrained continuum forces a fresh
judgment call at every single spacing decision ("14px or 17px here?"), and that judgment call is
where visual inconsistency enters a product one component at a time. A base unit turns "how much
space" into "which step" — a smaller, faster, more consistent decision.

## Why 4 and 8 won

Both **Material Design** (8dp macro grid for layout, 4dp micro grid for component-internal /
baseline alignment) and **Apple's Human Interface Guidelines** independently converged on the same
family of steps; Tailwind's default scale is built on a **4px base unit** throughout
(`tailwindcss.com/docs/customizing-spacing`, accessed 2026-07-15 — "every 1 unit represents 4px").
The reasons cited converge on three:

1. **Clean division.** 4 and 8 both divide evenly by 2, so half-steps stay on-grid — useful the
   moment a design needs an intermediate value between two named steps.
2. **Density-independent alignment.** Retina/high-DPI displays commonly scale at 2×, 3×; a 4 or 8
   base stays a whole pixel at every common device pixel ratio, where an odd base (5, 7, 9...)
   drifts into sub-pixel values that render blurry on some densities.
3. **A validated default.** Because Material and Apple's own systems already standardized on this
   family, adopting it is choosing an already-battle-tested convention over inventing a new one —
   the same "why we didn't reinvent this" logic pack-writing-rules itself uses for citing a
   worked instance instead of re-deriving it.

(rejuvenate.digital/news/designing-rhythm-power-8pt-grid-ui-design;
m1.material.io/layout/metrics-keylines.html; m3.material.io/styles/spacing — accessed 2026-07-15.)

## The progression is NOT uniform — and that's deliberate

A **linear** progression (fixed increment every step: 4, 8, 12, 16, 20, 24…) is the naive default,
and it is wrong at scale: the *perceptual* gap between 4px and 8px is enormous (a 2× jump), while
the same fixed +4 increment between, say, 60px and 64px is imperceptible. Every scale this pack
found published in the wild instead runs **dense at the bottom, sparse at the top** — small steps
stay tight (every legal value available) while large steps skip numbers, because a fixed
increment stops giving the designer a *meaningfully different* choice once the base size is large.

Tailwind states this explicitly as a design decision, not an accident: *"Tailwind's scale is
incredibly predictable at the lower end, but skips a few numbers as it gets higher. This is a
feature, not a bug... the visual difference between 4px and 8px is huge, but the difference
between 64px and 65px the human eye won't notice. As the scale goes up, the gaps between the
available values get larger to give meaningful choices."* (tailwindcss.com/docs/customizing-spacing,
attributed discussion context — accessed 2026-07-15.) IBM Carbon's spacing tokens follow the same
sparse-at-the-top shape (carbondesignsystem.com — accessed 2026-07-15).

**The failure this prevents:** a purely linear scale either produces too many indistinguishable
large-size options (decision fatigue with no visual payoff) or, if kept short to avoid that, too
few small-size options (forcing a designer off-grid for fine adjustments). The dense-then-sparse
shape gives full resolution exactly where the eye can tell the difference and collapses resolution
exactly where it can't.

## Cross-system comparison

| System | Base unit | Shape | Source (2026-07-15) |
|---|---|---|---|
| Material Design | 8dp (layout) / 4dp (component-internal, baseline) | Two-tier grid: components snap to 4dp, layout regions to 8dp | m1.material.io/layout/metrics-keylines.html, m3.material.io/styles/spacing |
| Tailwind CSS | 4px (`0.25rem`) | Dense linear at small steps, increasingly sparse at large steps (explicit design decision) | tailwindcss.com/docs/customizing-spacing |
| IBM Carbon | 2px base, spacing tokens on an expanding scale | Named tokens (`spacing-01`…`spacing-13`), sparse at the top | carbondesignsystem.com |
| Apple HIG | 8pt-family grid (informal convention across the ecosystem, not a single published numeric ladder) | Not centrally codified as a numeric ladder the way Material's is — treat any specific Apple spacing number as [inferred] from ecosystem convention unless cited from a specific HIG page | see `sources.md`'s unverified-edges list |

## T-shirt sizing as a naming layer

Naming scale steps by size label (`xs · sm · md · lg · xl · 2xl…`) rather than by raw number is a
naming-layer choice, not a different progression — it decouples the *name* a component references
from the *numeric value* the scale currently binds it to, so the underlying numbers can be retuned
without renaming every consumer. `make-component`'s own six-step control ramp (`references/
geometry-system.md`) uses exactly this naming shape for its comfortable-control sizes.
