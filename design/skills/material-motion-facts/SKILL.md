---
name: material-motion-facts
description: >
  Use when ANIMATING any UI whose motion tokens use the Material `--md-sys-motion-*` naming, or
  when the M3 motion token table is the question ("what md.sys.motion easing/duration token for
  this dialog", "which spring token — fast or slow, spatial or effects", "emphasized or standard
  easing here", "what duration tier for this transition"). Carries the verified table — 10 easing
  cubic-beziers, the 16-step duration ladder (50–1000ms), the M3 Expressive spring tokens
  (spatial/effects × fast/default/slow + stiffness/damping) — the pairing laws (entrances
  decelerate, exits accelerate; speed by scope), the platform-drift map (material-web has NO
  spring tokens). Never hardcode a ms value or bezier in a Material project. NOT for
  platform-agnostic motion science — how long an animation should be in general, Apple springs,
  choreography, reduced-motion policy (motion-rules, screens plugin); NOT for color/geometry/type
  (the material-design-* siblings); NOT for DESIGNING a motion system.
disable-model-invocation: false
user-invocable: false
---

# Material Design motion tokens (M3, spec-founded)

Motion in a Material project is never a number you type — it's a **token you pick by role and
scope**. This pack is the consumption guide for the `md.sys.motion.*` layer: the easing set, the
duration ladder, and the M3 Expressive spring tokens.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file whose `:root` defines `--md-sys-motion-*` custom properties
   (or the platform equivalent: `motionEasing*`/`MotionScheme` on Android, M3 theme slots in
   Flutter). **A nonoun kit?** Its motion export is NOT a CSS file — it is the `motion` block in
   the design-system `tokens.json` (`motion.easing` · `motion.duration` · `motion.animatable`)
   plus the `## Motion` rulebook in `DESIGN.md`. Bind to that; it is a **subset** of the table
   below (see the amendment in `references/tokens.md`). **No export at all?** Bind to the **M3
   spec defaults** carried verbatim in [`references/tokens.md`](references/tokens.md), and say
   you did.
   > _Amended 2026-07-09 (same day): this step previously read "no nonoun motion export exists
   > yet." One landed hours later (the nonoun color-tokens repo, PR #243). The original claim was true when
   > written and is preserved here for audit._
2. **Let the export decide the system.** Spring tokens present → M3 Expressive springs; absent
   (every material-web project — it implements duration+easing only) → duration+easing; no export
   at all → springs, the M3 recommendation for new work. Never mix the two per-animation.
3. **Pick by role, not taste.** Easing: entrances `*.decelerate`, exits `*.accelerate`,
   `emphasized` family only for hero moments. Duration: tier by scope (small=short …
   full-screen=long). Springs: `{fast|default|slow}` by scope × `{spatial|effects}` by property —
   effects springs never overshoot, so color/opacity never bounces.

## The laws (violating any is a defect)

1. **Tokens, not values.** No `transition: 300ms ease` in a Material project — that's
   `var(--md-sys-motion-duration-medium2) var(--md-sys-motion-easing-standard)`.
2. **Entrances decelerate; exits accelerate.**
3. **Emphasized is scarce.** Everywhere-emphasized is standard with extra cost.
4. **Springs don't cross the property line.** Spatial tokens for position/size/rotation; effects
   tokens for color/opacity. A bouncing opacity change is a spec violation, not a style.
5. **Web has no spring tokens.** Expressive motion on web is realized by sampling the published
   stiffness/damping into `linear()`/WAAPI — see `references/applying.md`.

## Surface map

| Question | Reference |
|---|---|
| Token names + exact values (beziers, ms ladder, spring physics), platform drift, unverified edges | [`references/tokens.md`](references/tokens.md) |
| Which token for which use case, transition-pattern recipes, web realization, reduced-motion hook | [`references/applying.md`](references/applying.md) |

## Verify before you ship

Done when no UI source carries a raw ms value, `cubic-bezier()`, or `ease*` keyword on a
`transition`/`animation` property outside the bound token file (grep for them), and every
animation sits on the project's one system — springs XOR duration+easing.

## Boundaries

- Platform-agnostic motion questions — how long *should* something take, why springs, stagger,
  what never animates, `prefers-reduced-motion` policy — belong to `motion-rules` (screens plugin,
  where installed); this pack owns only the Material realization.
- Color/sizing/type tokens: the three sibling packs. Designing a new motion system: not this pack.

_Provenance: authored 2026-07-09 against the published M3 spec (the material-foundation token
repo's `css/motion.css`, MDC-Android Motion.md, m3.material.io — all accessed 2026-07-09), NOT
against a nonoun export: none existed at authoring time._

_Amended 2026-07-09 (same day, by the kit maintainer): a nonoun motion export now exists
(the nonoun color-tokens repo's PR #243, `src/engine/motion.mjs` → the `tokens.json` `motion` block + the
`DESIGN.md` `## Motion` section). Bind step 1 and `references/tokens.md` are re-synced against it.
Its drift gate is the export repo's own suite (`test/engine/exports.mjs` asserts every easing is a
`cubic-bezier()`, the 16-step ladder is strictly ascending, `short2` is the 100ms instant floor,
and `animatable` is exactly `transform`+`opacity`) — that is the checker the definition of done
called for; this pack does not ship a duplicate._
