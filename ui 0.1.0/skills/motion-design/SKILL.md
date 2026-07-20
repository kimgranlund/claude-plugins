---
name: motion-design
description: >-
  Answers UI motion questions from a cited corpus — durations, easing and springs, choreography,
  reduced-motion policy. Use when timing or shaping animation: "how long should this
  transition/animation be", "what easing curve", "spring vs ease-in-out", "stagger these list
  items", "what transition between these screens", "this animation feels sluggish / janky / too
  bouncy", "make it snappier", "should this bounce", "what should never animate", "reduced motion
  / prefers-reduced-motion policy", "fill the Motion section of a DESIGN.md". Carries Nielsen's
  limits, the duration ladders, Apple's spring model (the house default) with the CSS
  realizations (keyword beziers, linear(), spring() status), Material's transition patterns,
  stagger values, vestibular triggers + the WCAG floor. ANSWERS only: building the animated
  component is component-forge; perceived-latency/skeleton/CWV verification is perf-verify;
  driving a live change is ui-change-verify; the md.sys.motion token table is
  material-design-motion-tokens.
user-invocable: false
disable-model-invocation: false
---

# motion-design — the motion world model

Answers how UI motion should behave — how long, on what curve, in what order, and for whom —
from a cited, dated corpus, so motion decisions reason from evidence instead of taste.

| Ask | Load |
|---|---|
| "How long?" — ladders, Nielsen limits, enter/exit asymmetry, scaling | `references/durations.md` |
| "What curve?" — Apple springs (house default), damping vocabulary, CSS beziers, `linear()` | `references/easing.md` |
| "How do these move together?" — transition patterns, stagger, z-space, interruptibility, what never animates | `references/choreography.md` |
| "Who does this hurt?" — WCAG floor, `prefers-reduced-motion`, vestibular triggers, substitutions | `references/reduced-motion.md` |
| "Just give me the value" — the ratified house point per knob (press scale, bounce, asymmetry, stagger, hover onset) + the frequency gate | `references/house-locks.md` |
| "Fill the Motion section of a DESIGN.md" — durations, easings, what never animates, reduced-motion policy | all five references, in table order — house-locks.md supplies the ratified values the section states (the section's contract is design-md-format's, design-systems plugin) |
| Provenance and the unverified edges | `references/sources.md` |

## Consult procedure

1. Classify the ask: duration · easing · choreography · accessibility. Load only the matching
   reference — Grep for the term first, Read that section; the files are catalogs, not linear reads.
2. Answer on the contract: **claim + cited source + the failure mode the default prevents**.
   Worked shape:
   > *"How long should this drawer animation be?"* → duration ask → open ~250 ms, close ~200 ms
   > (m1.material.io's codified drawer spec; exits run faster because the user is already done
   > with the drawer — web.dev asymmetric-animation-timing). The failure to design against is
   > symmetry: equal open/close reads as sluggish dismissal.
3. State which register the answer comes from: corpus-backed (cited above) · **house lock**
   (`house-locks.md` — a ruled point inside the cited envelope, overridable only by a project
   ruling) · general knowledge — and say so when it's the latter.
4. Route output work at the boundary (below).

## House default and deviation doctrine

The estate's default is **Apple-style spring motion** — critically damped or slightly under,
duration+bounce parameterized, interruptible — because velocity continuity and mid-flight
retargeting are the two properties fixed curves cannot provide (WWDC23 10158; `easing.md`).
Every default here carries its rationale, so deviation is legal when the rationale doesn't apply:
a Material-token project uses Material's own easing/spring set
(`material-design-motion-tokens`); technical motion (spinners, progress) stays `linear`.
Deviating? Name the rationale above that doesn't apply — a deviation with no named failing
rationale is drift. The specific ratified values (one point per knob, forbidden neighbors named)
and their precedence seam live in `references/house-locks.md`; the reduced-motion floor sits
outside every seam — nothing trades it away.

## Boundaries

- **This skill answers; it does not generate.** No keyframes, no component code, no token files —
  cite the value, hand the making off: build the animated component → [[component-forge]];
  verify perceived latency, skeleton-vs-spinner, CWV budgets → [[perf-verify]]; drive the change
  live → [[ui-change-verify]]; screen-state grammar (what an empty/loading state contains, not how
  it moves) → [[ui-patterns]].
- Material's `md.sys.motion.*` token table and its pairing laws → `material-design-motion-tokens`
  (design-systems plugin, where installed; otherwise cite the equivalent values from
  `easing.md`'s cross-reference row).
- Realizing motion constants as project tokens is the color plugin's `token-builder` seat (where
  installed) — this pack supplies the values and rationale it realizes.
- The WCAG *verification* of a shipped surface: focus → [[focus-verify]]; flash/seizure limits
  (2.3.1) have **no verifier seat in the estate yet** — say so in the answer rather than
  inventing a route. This pack owns the motion *policy* verifiers check against.

## Extending this pack

A missing axis, a stale reference (canon moves: HIG revisions, WCAG dot-releases, M3 re-specs),
or "add X" is authoring work — route to [[pack-forge]] (grounded research waves, one axis per
wave); never bolt an uncited file onto the corpus inline.
