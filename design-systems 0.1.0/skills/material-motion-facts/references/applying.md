# Applying motion tokens — the pairing laws

Verified against MDC-Android `docs/theming/Motion.md` and m3.material.io
transitions/applying-transitions — accessed 2026-07-09.

## Duration + easing pairing (the web/fallback system)

| Use case | Duration tier | Easing token |
|---|---|---|
| Small utility change (toggle, ripple) | short (50–200 ms) | `standard` |
| Regular on-screen animation | medium (250–400 ms) | `standard` / `standard.decelerate` |
| Large/hero transition (container transform) | long–extra-long (450–1000 ms) | `emphasized` family |
| Entrance | medium–long | `*.decelerate` |
| Exit | medium–long | `*.accelerate` |

The two invariant laws: **entrances decelerate, exits accelerate** (never the reverse), and
**emphasized is for the moments that deserve attention** — using it everywhere demotes it to
standard with extra steps.

## Spring pairing (M3 Expressive)

Choose by **scope and property**, not by curve taste:

| Animating | Token |
|---|---|
| Small component position/size | `spring.fast.spatial` |
| Partial-screen spatial change | `spring.default.spatial` |
| Full-screen spatial transition | `spring.slow.spatial` |
| Color/opacity at any scope | `spring.{speed}.effects` (never overshoots) |

The scheme (Expressive vs Standard) is a product-level choice; per-animation overrides read as
drift.

## Transition patterns as token consumers

| Pattern | Duration | Easing (fallback system) | Spring (Expressive) |
|---|---|---|---|
| Container transform | long (500–600 ms) | `emphasized` / `emphasized.decelerate` | `spring.slow.spatial` |
| Shared axis (X/Y/Z) | long (450–600 ms) | `emphasized.decelerate` in, `emphasized.accelerate` out | `spring.default–slow.spatial` |
| Fade through | medium (300–400 ms) | `standard` | `spring.default.effects` |
| Fade | short–medium (100–350 ms) | `standard.decelerate` in, `standard.accelerate` out | `spring.fast.effects` |

Pattern anatomy and when each fits (spatial-claim reasoning) is platform-agnostic knowledge —
`motion-design` (ui plugin) owns it; this file owns only the Material token realization.

## Web realization notes

- Tokens go in as custom properties: `transition: transform var(--md-sys-motion-duration-medium2)
  var(--md-sys-motion-easing-standard)`.
- No spring custom properties exist in material-web — approximate a spring token by sampling its
  stiffness/damping (values in `tokens.md`) into a CSS `linear()` stop list or a Web Animations
  API curve.
- Respect `prefers-reduced-motion` at the consumption site: swap spatial patterns to fades, keep
  effects springs (policy: `motion-design`'s reduced-motion reference, where installed).
