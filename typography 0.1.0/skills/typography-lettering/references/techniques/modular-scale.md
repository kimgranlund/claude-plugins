---
date: 2026-04-17
coverage: medium
peers:
  - ./measure.md
  - ./vertical-rhythm.md
  - ../metrics/metrics-glossary.md
  - ../metrics/units.md
primary_sources:
  - https://alistapart.com/article/more-meaningful-typography/
  - https://www.modularscale.com/
  - https://type-scale.com/
  - https://utopia.fyi/type/calculator/
  - https://utopia.fyi/blog/designing-with-fluid-type-scales/
  - https://tailwindcss.com/docs/font-size
  - https://en.wikipedia.org/wiki/Golden_ratio
  - https://en.wikipedia.org/wiki/Modulor
  - https://en.wikipedia.org/wiki/Just_intonation
---

# Modular Scale

A modular scale is a hierarchy of type sizes derived by repeatedly multiplying (or dividing) an anchor size by a single ratio. Given an anchor of `1rem` and a ratio of `1.25`, the scale runs `…0.64, 0.8, 1, 1.25, 1.5625, 1.953, 2.441…` and each step maps to a semantic role (`caption`, `body`, `lead`, `h4`, `h3`, `h2`, `h1`, `display`). The scale is a discipline: instead of picking arbitrary sizes per surface, you pick a shape and reuse it.

**Scope.** This file covers what a modular scale is, why ratios produce coherence, which ratios are conventional and where their names come from, and when each is the right call. It also covers fluid type and role assignment. It does **not** end in a token sheet. No type-scale generator is installed — that is a handled dead-end, not a hidden peer: compute the scale (sizes, roles, `clamp()` coefficients) inline from this file's formulas. Realizing the result as a project token layer — role-named ladders wired into custom properties — is the `token-builder` agent's seat.

---

## What It Is

Formally: `size(n) = anchor × ratio^n`, for integer `n` around zero. The anchor is almost always body text at `1rem` (which is `16px` by default, though user-agent settings can change this). Steps above the anchor are larger; steps below are smaller.

A few properties follow from the formula and are the reason the practice exists.

**Geometric progression means constant visual pace.** Each step is the same multiplicative factor larger than the last, so the perceived jump between `h3` and `h2` feels like the jump between `h2` and `h1`. Perception of size difference is closer to ratio than to delta, which is why `12 → 14` reads as a real jump but `60 → 62` reads as nothing. Arithmetic scales (`12, 14, 16, 18, 20, 24`) accelerate at the small end and stall at the large end.

**One decision produces many sizes.** Choosing a ratio and an anchor fixes eight or ten sizes. You can still override any individual size, but the default shape is coherent by construction, and overrides are visibly exceptional against the grid.

**Roles, not just numbers.** The useful output isn't `1.25rem` — it's a map from semantic role to step. The ratio is a compositional choice (how much hierarchy do you want?), and role assignment is an editorial choice (which rung is `h2`?). Both decisions are portable; the `px` values at any given anchor are not.

---

## Ratio Catalog

| Ratio   | Musical name          | Character                                | When it wins                                                                    |
|---------|------------------------|------------------------------------------|----------------------------------------------------------------------------------|
| 1.067   | Minor second           | Imperceptible progression                | Almost never — sizes collapse into each other                                    |
| 1.125   | Major second           | Gentle, near-monotone                    | Dense data UI where hierarchy is mostly color/weight, not size                   |
| 1.200   | Minor third            | Subtle but visible                       | Admin panels, email clients, heavy-chrome dashboards                             |
| 1.250   | Major third            | Balanced, generic                        | Default for most product UI; Tailwind's default `text-*` ratio is near this      |
| 1.333   | Perfect fourth         | Confident, editorial-leaning             | Marketing sites, prose-forward landing pages, blog templates                     |
| 1.414   | Augmented fourth (√2)  | Paper-proportional                       | Editorial layouts; matches ISO paper ratio and document-like surfaces            |
| 1.500   | Perfect fifth          | Expressive, punchy                       | Promotional or campaign surfaces; headlines want to shout                        |
| 1.618   | Golden ratio (phi)     | Print-traditional, dramatic              | Editorial hero pages; brand-forward marketing                                    |
| 1.667   | Major sixth            | Poster-adjacent                          | Display-heavy marketing hero blocks                                              |
| 1.778   | Minor seventh          | Very dramatic                            | Single-page poster compositions                                                  |
| 1.875   | Major seventh          | Extreme                                  | One-off display work; rarely used in systems                                     |
| 2.000   | Octave                 | Doubling                                 | Pure display pieces; pairs with a second ratio for the body range                |

The table's "when it wins" column is a starting point, not a rule. A dense terminal UI can use `1.333` if it only uses two sizes and otherwise leans on color. An editorial layout can use `1.125` if the editorial drama lives in weight and leading instead of size. Pick the ratio that makes the *hierarchy you already know you want* fall out naturally, then tune.

**Starter default.** For a general-purpose product UI that mixes prose and chrome, `1.25` (major third) is the right first guess. It produces visible-but-not-dramatic jumps, it plays well with a `1rem` anchor and an 8-point spacing grid, and it leaves room to push one heading harder with a custom display size without breaking the rest. Tailwind's shipped scale is close to `1.2` between most adjacent sizes and is a reasonable sanity-check.

---

## Musical vs Geometric — Naming Honesty

The "major third / perfect fourth / golden ratio" names are marketing; the math is geometric progression.

**Where the names came from.** Tim Brown's 2007 A List Apart article *More Meaningful Typography* introduced "modular scale" as a web-design term and mapped several candidate ratios to just-intonation musical intervals. The argument was that ratios that humans find consonant in sound might also be the ones humans find harmonious in sight. It is a genuinely pretty argument and it helped the idea go viral. But it is also an analogy, not a proof — there is no established perceptual literature showing that `1.5` looks better on a page because a `3:2` frequency ratio sounds consonant to an ear.

**Where phi came from.** The golden ratio (`1.618…`) arrives in typography through a different door: Renaissance page-proportion tradition, Le Corbusier's *Modulor* (1948), mid-century graphic design pedagogy, and the broader art-theoretic mystique around phi. It has never needed a musical label; it has always been sold as a geometric / aesthetic constant.

**What actually matters.** You are picking a multiplicative factor. The factor determines visual pace. Pace should serve hierarchy. If `1.333` produces the hierarchy you want, use `1.333` and don't worry about whether a perfect fourth is more "consonant" than a tritone. The musical vocabulary is useful as shorthand — saying "minor third" is faster than saying "`1.2`" — but it is not evidence.

When specifying a system, name the ratio by number first and the musical label second, or drop the musical label entirely. Readers outside the original 2007 lineage will thank you.

---

## Compound Scales

Tim Brown's later writing popularized *compound* modular scales — two ratios interleaved to produce more steps without picking a huge jump. A classic example uses `1.125` and `1.333` on the same anchor, producing a denser scale than either alone.

This was most useful when CSS had no fluid-type primitive and designers needed more granularity at the small end while still having drama at the large end. It is **less common today.** The modern answer is to pick one ratio and use `clamp()` to smooth the responsiveness, not to interleave two ratios.

If you do want a compound scale, the math is: generate both sequences from the same anchor, merge, sort, deduplicate. The risk is that the interleaved sizes sit close enough together that readers can't see the difference, which defeats the purpose. If two adjacent steps are less than ~6% apart, delete one.

---

## Fluid Type (2020+ Canonical Recipe)

A modular scale fixes the *ratio* between sizes at a given viewport. What about *across* viewports? A `2.5rem` h1 that looks right on a 1440px laptop is aggressive on a 375px phone and timid on a 2560px monitor.

The canonical answer since ~2020 is CSS `clamp()` with a viewport-unit middle term.

**Basic shape:**

```css
font-size: clamp(<min>, <preferred>, <max>);
```

- `<min>` is the smallest acceptable size (usually the mobile size).
- `<max>` is the largest acceptable size (usually the desktop size).
- `<preferred>` is a fluid expression using `vw`, `svi`, `lvi`, `dvi`, or `cqi` that scales with viewport or container.

**Example — single step (display heading):**

```css
--size-h1: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);
```

At 0vw the fluid term is `1.5rem`, below the min → clamps to `2rem`. At ~80vw the fluid term crosses `3.5rem` → clamps to max. In between it interpolates linearly.

**Utopia.fyi's two-viewport formula.** The Utopia approach (Trys Mudford + James Gilyead) formalizes the recipe: pick a min viewport (e.g. 320px) and a max viewport (e.g. 1240px); pick a min size at min viewport and a max size at max viewport; compute the `clamp()` that interpolates between them linearly. The slope is `(maxSize − minSize) / (maxViewport − minViewport)` in viewport units. Their calculator at `utopia.fyi/type/calculator/` emits whole type scales in this form. For any production system using fluid type, use Utopia's formula rather than hand-tuning each clamp.

**Why pure `vw` fails.** If you set `font-size: 2vw`, the text shrinks unboundedly on small viewports (unreadable at 320px) and grows unboundedly on giant ones (absurd at 4K). It also refuses to respect user font-size preferences, which is an accessibility failure.

**Why pure percentage fails.** Percentage resolves against the parent's computed font-size, not the viewport. It lets you scale a subtree relative to its parent but gives no viewport-awareness.

**Viewport units — pick the right one.** On modern iOS and Android the "viewport" has several definitions because of retractable browser chrome:

- `vw` / `vh` — large viewport (chrome retracted). Legacy default. Jumps when chrome toggles.
- `svw` / `svh` / `svi` — small viewport (chrome extended). Conservative; never overflows.
- `lvw` / `lvh` / `lvi` — large viewport (chrome retracted). Explicit name for what `vw` used to mean.
- `dvw` / `dvh` / `dvi` — dynamic viewport. Changes live as chrome toggles. Avoid for `font-size` (can cause layout thrash); fine for layout height.
- `cqi` / `cqb` — container-query inline / block. Scales with the *container*, not the viewport. Preferred when type should respond to its layout container (cards on a dashboard) rather than the browser window.

For fluid type, prefer `vi` over `vw` (inline vs. horizontal — respects writing mode) and prefer `cqi` when the component has a defined container. Use `svi` if you want to be conservative about mobile chrome.

**Copy-pasteable fluid clamp snippets.**

```css
/* Small step — body to lead. Subtle growth. */
--size-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);

/* Medium step — h3 / h2. Visible responsiveness. */
--size-h2: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);

/* Large step — h1 / display. Drama at the top. */
--size-h1: clamp(2.25rem, 1.5rem + 3.5vw, 4rem);

/* Container-aware — scales with the card, not the window. */
--size-card-title: clamp(1rem, 0.9rem + 1cqi, 1.5rem);
```

Compute these with Utopia (or equivalent) rather than eyeballing the middle term. The fluid coefficient has to produce a size that sits neatly between min and max at your target viewport, and the arithmetic is fiddly.

---

## Role Assignments

A modular scale gives you steps. Roles give those steps meaning. A typical 8-step mapping:

| Step (relative to anchor) | Role                    | Notes                                             |
|---------------------------|--------------------------|---------------------------------------------------|
| −2                        | `caption` / `micro`      | Legal, timestamps, metadata                       |
| −1                        | `small`                  | Secondary UI labels, dense data                   |
|  0                        | `body`                   | Anchor. Default reading size.                     |
| +1                        | `lead`                   | Intro paragraphs, larger body                     |
| +2                        | `h4`                     | Smallest heading                                  |
| +3                        | `h3`                     | Subsection                                        |
| +4                        | `h2`                     | Section                                           |
| +5                        | `h1`                     | Page title                                        |
| +6 (optional)             | `h1-display` / `hero`    | Marketing hero headlines                          |
| +7 (optional)             | `h1-mega` / `poster`     | Display-only; rarely in product surfaces          |

**Skipping steps intentionally.** A common move is to skip every other step for headings — use `+2, +4, +6` for `h4, h2, h1` and leave `+1, +3, +5` for body sizes and opticals. This produces more visible hierarchy with the same ratio and is the reason a `1.25` scale still feels punchy.

**When the design asks for more sizes than the scale provides.** First, audit: are the extra sizes actually semantically different, or did the designer just nudge for optical reasons? If optical (a 17px label that "felt better" than 16px), treat as an optical override, not a new step. If semantic (there really are two different kinds of section heading), either widen the scale by going to a denser ratio (`1.25` → `1.2`), or introduce a secondary ratio (compound scale) for the body range only. Avoid adding ad-hoc off-scale sizes, each of which is a future inconsistency.

**Display and hero steps.** Marketing surfaces often want one or two sizes beyond the standard scale. These are fine as named outliers — `display-1`, `display-2`, `hero` — rather than extending the main scale with more steps that the rest of the product will never use.

---

## When Modular Scale Doesn't Apply

Not every surface benefits from a modular scale. A few cases where the tool is the wrong one:

**Data-heavy interfaces.** In a spreadsheet, trading terminal, or analytics dashboard, size is not the primary hierarchy signal. Color, weight, alignment, and spacing do the work, and everything sits within a narrow band (12px–16px). A modular scale is over-engineering for two sizes. Just pick the two sizes.

**Illustrated / editorial layouts.** A long-form editorial piece where each spread has its own headline treatment is not a system; it is a sequence of custom layouts. Trying to force a modular scale on it either flattens the work or creates a fifty-step scale that no one uses twice. Let editorial design be editorial.

**Logo-pinned compositions.** When the brand wordmark pins a specific size on the page (e.g., the logo is exactly `72px` and the hero headline must match), the scale should not try to accommodate the logo. Treat the logo as an external constraint; align other type to the scale; let the logo sit where it sits.

**Single-size components.** A navbar with one font size does not need a scale. It needs one size.

---

## Ratios That Are Almost Never Right

- **Below `1.1`.** Sizes collapse visually. `1.05` between adjacent steps is invisible at 16px (16 → 16.8 → 17.64); readers cannot tell these apart. Use when you need a faint indication of hierarchy and have exhausted color/weight, which is almost never.
- **Above `2.0`.** Doubles or more between adjacent steps are poster scale. Fine for a one-page hero. Catastrophic for a system that needs `caption` through `h1` on the same scale — you either start absurdly small or end absurdly large.
- **Irrational ratios with no tradition.** `1.337` or `1.559` pulled from nowhere. If you want math mysticism, use phi or √2, both of which have a documented lineage and are as arbitrary as any other pick but have the advantage of not being arbitrary-looking. Better: pick a named ratio, then tune if the audit demands it.

---

## Anti-patterns

**Per-surface scale drift.** "The marketing page uses `1.333`, the app uses `1.2`, the docs site uses `1.25`." Each was picked locally by a different designer. Readers crossing surfaces feel the seams even if they can't name them. Unify the ratio at the system level; let surfaces diverge in anchor, weight, or leading instead.

**Hardcoded `px` values alongside a scale.** Tokens expose the scale; components reach past the tokens into `font-size: 17px;` because a designer nudged. Each nudge is invisible in isolation and corrosive over a year. Either the nudge belongs in the scale (widen the ratio or add a step) or it doesn't belong at all.

**Naming tokens by size, not role.** `--text-18`, `--text-24`, `--text-32` tie the token name to today's anchor. Move the anchor (accessibility, density mode, theme) and every name lies. Name by role (`--text-h2`, `--text-body`, `--text-caption`). The ratio is a derivation detail, not a naming convention.

**Treating musical names as prescriptive.** "We use a perfect fifth because it's the most harmonic." The ratio's name is not evidence; the hierarchy it produces is. If a perfect fifth gives you the drama you want, great. If it gives you too much drama, a minor third is not less pretty — it's less dramatic. Pick on visual pace, not nomenclature.

**Fluid type without min/max.** `font-size: 2vw` with no `clamp()`. Unreadable on small screens, absurd on large ones, and hostile to user font-size settings. Always clamp.

**Fluid type computed by eye.** Hand-tuning the coefficient inside `clamp()` until it "looks right" at your laptop's viewport. It will be wrong at every other viewport. Use Utopia's formula or equivalent — the math is short and mechanical.

**Letting the scale generate tokens ad-hoc.** This is the scope-boundary anti-pattern. A modular scale is a design choice; a token sheet is an engineering artifact. Computing the sizes is inline work — this file's formula is all the machinery there is — but don't scatter `--h1: 2.441rem` into component CSS because you computed it once. Hand the computed scale (ratio, anchor, role map, fluid recipe) to the `token-builder` agent to realize as the project's role-named token ladder, wired where every consumer reads it.

---

## Cross-references

- **`token-builder` agent** — owns the project token layer. Computation stays here (derive the scale inline from this file — no generator skill is installed); route only the token-layer realization — the computed scale landed as role-named custom properties — to that seat.
- **`./measure.md`** — ratio interacts with measure: bigger body text on a fixed container reduces characters per line, which affects the `body` step choice.
- **`./vertical-rhythm.md`** — each step should land on (or relate to) the baseline grid. Ratio choice constrains which leading values produce clean rhythm.
- **`../metrics/units.md`** — `rem` vs `em` vs `px` vs viewport units: what each resolves against and when to use which.
- **`../metrics/metrics-glossary.md`** — UPM, x-height, cap-height, leading; the physical quantities the scale is ultimately expressed in.

---

## Sources

- Tim Brown, *More Meaningful Typography*, A List Apart (2007) — the original article introducing modular scale as a web-design term and its musical-interval vocabulary.
- Tim Brown, *Combining Typefaces* — extended treatment of pairing and scale.
- `modularscale.com` — Brown's calculator; useful for quick exploration of ratio + anchor combinations.
- `type-scale.com` — alternate calculator; exposes a slightly different UI and ratio set.
- Utopia.fyi (Trys Mudford and James Gilyead), *Designing with Fluid Type Scales* — canonical modern treatment of `clamp()`-based fluid type.
- Robert Bringhurst, *The Elements of Typographic Style* — on scale and proportion; the book-traditional case.
- Le Corbusier, *Le Modulor* (1948) — phi-based proportional system; historical context for the golden-ratio thread.
- Tailwind CSS default font-size scale — a contemporary shipped scale at roughly `1.2` ratio; useful sanity check.
- MDN, `clamp()` and viewport-units documentation — authoritative reference for the CSS primitives.
