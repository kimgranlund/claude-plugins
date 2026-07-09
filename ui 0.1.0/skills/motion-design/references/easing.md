# Easing — curves, springs, and why Apple won the argument

Researched 2026-07-09 from primary sources (developer.apple.com, w3.org, MDN, m3.material.io).
This corpus's default recommendation is **spring-based motion in the Apple style** — the estate's
standing preference — with the CSS realizations that approximate it. Material's own easing/spring
token set is owned by `material-design-motion-tokens` (design-systems plugin); one cross-reference
row lives at the bottom.

## The spring model (Apple)

Springs are SwiftUI's default animation. The modern parameterization is **duration + bounce**
(perceptual, not raw physics):

- `.spring(duration:bounce:)` — bounce ∈ [−1.0, 1.0]; 0 = no bounce (critically damped),
  positive = bouncier, negative = overdamped flatness.
- Three presets, all customizable via `duration:extraBounce:`: **`.smooth`** (no bounce),
  **`.snappy`** (small bounce), **`.bouncy`** (larger bounce)
  (developer.apple.com/documentation/swiftui/animation/{smooth,snappy,bouncy}).
- ⚠ The presets' exact numeric defaults are **not stated in the web docs** (SDK headers carry
  them); cite the semantics, not invented numbers.
- Older parameterizations still in the wild: `.spring(response:dampingFraction:)` (SwiftUI),
  `CASpringAnimation` (`mass`/`stiffness`/`damping`/`initialVelocity`), and
  `UIView.animate(...usingSpringWithDamping:...)` (UIKit).
- Useful physics ↔ perception bridges Apple documents: `stiffness = (2π ÷ duration)²`;
  `settlingDuration` computes when motion becomes imperceptible.

**Why springs — the load-bearing rationale (WWDC23 "Animate with springs", session 10158):**

1. **Velocity continuity.** A bezier curve's velocity jumps discontinuously when an animation is
   interrupted or retargeted; a spring's position *and velocity* are continuous, so mid-flight
   retargeting (the common case in gesture-driven UI) stays smooth.
2. **Interruptibility.** On interruption, the spring re-aims at the new target carrying its
   current velocity — no dead stop, no restart.
3. **No fixed clock.** Motion settles when the physics settle; short moves finish sooner without
   anyone tuning per-case durations.

Damping vocabulary (developer.apple.com/documentation/swiftui/spring/dampingratio): damping ratio
0 = oscillates forever · <1 under-damped (bouncy) · 1 critically damped (fastest no-overshoot —
the "smooth" feel) · >1 over-damped (sluggish). **Critically damped or slightly under is the
default recommendation; reserve visible bounce for playful, low-frequency moments.**

## The CSS realization

W3C keyword beziers (w3.org/TR/css-easing-1, normative):

| Keyword | cubic-bezier | Character |
|---|---|---|
| `ease` | (0.25, 0.1, 0.25, 1.0) | default; accelerate then settle |
| `ease-in` | (0.42, 0, 1.0, 1.0) | for exits (accelerate away) |
| `ease-out` | (0, 0, 0.58, 1.0) | for entrances (arrive and settle) |
| `ease-in-out` | (0.42, 0, 0.58, 1.0) | symmetric S-curve |
| `linear` | identity | technical motion only (spinners, progress) |

Stock keywords read as mechanical because the curve is fixed: it cannot respond to interruption or
carry gesture velocity — precisely the two things springs solve. Prefer custom curves or spring
approximations for anything the user touches.

- **`cubic-bezier(x1,y1,x2,y2)`** — x ∈ [0,1]; **y is unbounded**, so overshoot IS expressible
  (y > 1), but the form is single-segment: it can fake one overshoot-and-settle, never a true
  damped oscillation.
- **`linear(...)`** — piecewise-linear easing; the standard way to encode a *sampled spring curve*
  in CSS. Baseline **Widely available since Dec 2023** (MDN). Generate the stop list from the
  spring's solution; this is the correct web port of an Apple-style spring.
- **`spring()`** — still only a proposal (csswg-drafts issue #280, open since 2016; WebKit
  preview implementation). Do not ship against it.

## Assignment rules (cross-system consensus)

- Entrances **decelerate** (ease-out family); exits **accelerate** (ease-in family) — Material,
  Carbon, Fluent all codify this pairing.
- One easing family per product; mixing curve personalities across surfaces reads as drift.

## Cross-reference

Material easing/spring tokens (`md.sys.motion.*` — the M2 cubic-beziers, the M3 spring scheme):
consult `material-design-motion-tokens` (design-systems plugin) where installed; historical anchor
M2 standard = cubic-bezier(0.4, 0.0, 0.2, 1).
