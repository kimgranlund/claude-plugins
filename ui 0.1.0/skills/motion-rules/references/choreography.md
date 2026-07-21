# Choreography — how elements move together, and what never moves

Researched 2026-07-09 from primary sources (m3.material.io, m2.material.io, developer.apple.com,
carbondesignsystem.com, atlassian.design, fluent2.microsoft.design, web.dev, MDN, w3.org).

## Named transition patterns (Material, current M3 set)

m3.material.io/styles/motion/transitions/transition-patterns:

- **Fade** — element fades to show/hide content behind it (overlays, dialogs).
- **Cross-fade** — outgoing and incoming fade simultaneously (peer swaps with no spatial relation).
- **Fade-through** — outgoing fades out *completely*, then incoming fades in (destination change:
  bottom-nav switches; the pattern that reads as "new place, no spatial claim").
- **Container transform** — a container and its grouped contents transform *as one unit* into the
  new layout (card → detail; the pattern that preserves object identity across screens).

Pick by spatial claim: related-and-persistent → container transform; sibling axis-move → shared
motion along one axis; unrelated destination → fade-through; layered content → fade.

## Stagger

- **20 ms per item**, whole sequence capped at **~500 ms total** — Carbon
  (carbondesignsystem.com/elements/motion/choreography) and Material 2
  (m2.material.io/design/motion/choreography.html) agree on both numbers.
- **One focal point.** One leading animation; everything else supports it. Two elements competing
  for attention is the named choreography defect (atlassian.design/foundations/motion).
- Expanding across both axes: stagger horizontal vs vertical timing so the path arcs instead of
  cutting a straight diagonal (Carbon).

## Spatial continuity and z-space

- Depth expresses hierarchy: **push** for descending into nested content, **modal/sheet** presents
  while the parent visibly *recedes* in z (Apple spatial-design guidance, WWDC23 sessions
  10072/10073; developer.apple.com/design/human-interface-guidelines/spatial-layout).
- Elements exit consistent with where they came from; a thing that entered from the right does not
  leave through the top.
- Focal elements persist and transform smoothly rather than blinking out and reappearing (M3
  transitions guidance).

## Interruptibility (the Apple bar)

Gesture-driven and navigation motion must be **retargetable mid-flight**: each gesture event
re-aims the running spring, which carries its current velocity to the new target; on release the
hand-off spring inherits the captured velocity (WWDC23 10158 "Animate with springs"; WWDC24 10145
"Enhance your UI animations and transitions"). A transition the user must *wait out* is a defect
in touch UI. This is the choreography-level argument for springs — see `easing.md`.

## What never animates

The list design-md-rules's Motion section asks for, with owners:

| Never animate | Why | Source |
|---|---|---|
| Layout properties (`top/left/width/height`) | triggers layout+paint (~37 ms render + 79 ms paint in web.dev's documented example); animated layout shift is a CLS defect | web.dev/articles/animations-guide |
| Anything but `transform`/`opacity`, by default | only compositor properties hold 60 fps (16.7 ms frame budget) off the main thread | web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count |
| Text while it's being read | blinking/moving text impedes reading; users must be able to pause | w3.org/WAI/WCAG21/Understanding/pause-stop-hide |
| Focus indicators, via reflow | showing/suppressing an outline must never shift layout | w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum |
| The text caret | OS-defined blink; `caret-color` interpolation is discrete anyway | MDN caret-animation |
| Form fields during entry | state animation mid-typing is cognitive load; value changes land instantly (convention, no normative source) | ledger, convention |
| Decorative loops without a pause control | WCAG 2.2.2's five-second rule | see `reduced-motion.md` |

`will-change: transform, opacity` is a *just-before* hint, never an always-on class — overuse
costs memory (MDN will-change).
