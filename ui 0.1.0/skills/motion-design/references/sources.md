# Sources — provenance in trust order

Corpus researched 2026-07-09 (four parallel research waves; ledgers archived in the session
scratchpad, findings distilled here with citations inline in each reference). Re-run the wave for
an axis when its canon moves (a new HIG revision, a WCAG dot-release, an M3 motion re-spec).

## Trust order

1. **Normative standards** — w3.org/TR/css-easing-1 (keyword bezier values), w3.org/WAI WCAG 2.1/2.2
   Understanding pages (2.2.2, 2.3.1, 2.3.3, focus-not-obscured).
2. **Platform owners, primary docs** — developer.apple.com (SwiftUI Animation/Spring API pages,
   CASpringAnimation, HIG motion + spatial-layout, accessibilityReduceMotion; WWDC23 session 10158
   "Animate with springs", WWDC24 10145), m3.material.io + m2/m1.material.io archives,
   support.apple.com/111781 (Reduce Motion behavior).
3. **Browser/platform reference** — MDN (prefers-reduced-motion, linear(), cubic-bezier,
   will-change, caret-animation; Baseline dates), web.dev (animations-guide,
   compositor-only-properties, asymmetric-animation-timing, prefers-reduced-motion).
4. **Design systems with published motion specs** — carbondesignsystem.com (tokens, choreography),
   atlassian.design/foundations/motion, fluent2.microsoft.design/motion.
5. **Domain authorities** — nngroup.com (response-time limits, animation-duration), valhead.com
   (reduce-not-remove doctrine), vestibular.org + a11yproject.com (trigger taxonomy, prevalence),
   pubmed 38728561 (AVOCADO 2024 prevalence counterpoint).

## Known unverified edges (kept out of the corpus, listed so nobody re-invents them)

- SwiftUI `.smooth`/`.snappy`/`.bouncy` exact numeric defaults — semantics documented, numbers
  live in SDK headers only; the references cite semantics.
- `CASpringAnimation` property defaults (commonly quoted mass 1 / stiffness 100 / damping 10) —
  secondary sources only.
- Apple HIG Motion page's exact principle list — page resisted extraction; principles cited via
  WWDC sessions instead.
- Any distance→duration formula, any universal enter:exit ratio — no system publishes one.
- M3 spring-token numeric values — owned by `material-design-motion-tokens` (design-systems),
  which carries the current state of that table.

## House rulings — a distinct provenance class (added 2026-07-16, Issue #9)

`references/house-locks.md` carries values RULED in this workspace (one point per knob inside the corpus's cited envelope), informed by the 2026-07-15 external-skill review's type specimens (jakubkrehel/make-interfaces-feel-better@366f0f86e, emilkowalski/skills@6bf24434f). They are never platform citations and are labeled house rulings at the claim site; the cited envelope stays in the sibling files, and the reduced-motion floor is outside every override seam.
