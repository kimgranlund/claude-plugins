# Reduced motion — the accessibility policy layer

Researched 2026-07-09 from primary sources (w3.org/WAI, MDN, developer.apple.com, web.dev,
vestibular.org, valhead.com). The doctrine in one line: **reduce, don't remove** — replace
triggering motion with safe equivalents; never strip meaning-carrying feedback.

## The WCAG floor (levels matter)

| SC | Level | Normative core |
|---|---|---|
| **2.2.2 Pause, Stop, Hide** | **A** | Moving/blinking/scrolling content that starts automatically, lasts **>5 s**, and sits parallel to other content needs a pause/stop/hide mechanism (unless essential). **Auto-updating** content (tickers, feeds) gets NO 5-second grace — it always needs pause/stop/hide or a frequency control. |
| **2.3.1 Three Flashes** | **A** | Nothing flashes more than three times per second (or stays under the flash/red-flash thresholds) — seizure risk, distinct from vestibular concerns. |
| **2.3.3 Animation from Interactions** | **AAA** | Interaction-triggered motion can be disabled unless essential. `prefers-reduced-motion` is the named sufficient technique. |

So: pause controls and flash limits are the *legal floor* (A); honoring reduced-motion on
interaction animation is the *quality bar* (AAA) — this estate treats it as required anyway.
(w3.org/WAI/WCAG22/Understanding/… — accessed 2026-07-09.)

## `prefers-reduced-motion`

`@media (prefers-reduced-motion: reduce)` — Baseline since January 2020 (MDN). It maps to real OS
switches: macOS/iOS *Reduce Motion*, Windows *Show animations* (off), Android 9+ *Remove
Animations*. It means "this user gets vestibular-safe motion", **not** "this user wants a static
page" — functional feedback stays. CSS alone misses JS-driven animation: gate those on
`matchMedia('(prefers-reduced-motion: reduce)')` (and in SwiftUI, `accessibilityReduceMotion`).

## Vestibular trigger taxonomy (what to substitute away)

Highest-risk first (vestibular.org, web.dev, a11yproject.com): **parallax** (fore/background rate
differential) · **background/autoplay video** (88–94% symptom-trigger rates documented for
high-complexity clips in vestibular-migraine users — vestibular.org) · **zoom/scale transitions** ·
**spinning/rotation** · **multi-directional or peripheral movement** · **rapid camera/perspective
changes** · **slide-everything screen transitions**. Consequences are physical: vertigo, nausea,
migraine, hours of recovery. Prevalence caveat, cited both ways: NHANES found balance dysfunction
in ~35% of US adults 40+ (~69M people, via vestibular.org); the 2024 AVOCADO study's rigorous
weighting puts vestibular hypofunction nearer 3%. Cite the range, not one number.

## The substitution table (reduce, not remove)

Doctrine authored by Val Head (valhead.com/2017/06/23/reduced-motion-query, "Reduced Motion In The
Wild" 2020) and web.dev/articles/prefers-reduced-motion; Apple's HIG states it verbatim for apps
("provide a new animation that avoids motion, such as a dissolve, highlight fade, or color shift"):

| Full motion | Reduced-motion substitute |
|---|---|
| Zoom/scale transition | crossfade/dissolve |
| Slide/movement | opacity fade |
| Parallax | remove; static background |
| Animated reveal | instant or fade-only |
| Attention motion (shake, bounce) | color shift / highlight fade |
| Autoplay media | static first frame + explicit play |
| Functional feedback (press, state change) | **keep** — shorten/simplify, never delete |

## Apple as the reference implementation

With Reduce Motion on, iOS/macOS swap app-switch zooms for dissolves, disable parallax and
depth-of-field effects, and simplify dock/icon animations — i.e., the platform itself performs the
substitution table above (support.apple.com/en-us/111781). A product that deletes all animation
under reduced-motion has misread the setting; match Apple's behavior instead.

## Policy this corpus recommends

1. Every animation is classified **functional** (communicates state — keep, simplified) or
   **decorative** (delete under `reduce`).
2. The reduced variant is *designed*, not a side effect: crossfade timings still follow
   `durations.md`.
3. Autoplaying/looping anything >5 s ships a pause affordance regardless of the media query
   (that's Level A, not a preference).
