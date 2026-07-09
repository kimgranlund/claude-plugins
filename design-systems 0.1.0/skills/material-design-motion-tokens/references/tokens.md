# The md.sys.motion token table (M3, verified 2026-07-09)

Verified verbatim against the material-foundation token repo (`css/motion.css`), MDC-Android
`docs/theming/Motion.md`, and m3.material.io — accessed 2026-07-09. Two CSS shapes exist in the
wild, so bind expecting either: the tier-named single-property form shown in this file
(`--md-sys-motion-easing-standard`, `--md-sys-motion-duration-short1` — the conventional
kebab-casing of the token names), and the published Google token export's own shape, which
value-names durations (`--md-sys-motion-duration-300`) and splits easings into per-control-point
properties (`--md-sys-motion-easing-standard-x0/y0/x1/y1`).

## Easing tokens (cubic-bezier)

| Token | Value | Use |
|---|---|---|
| `easing.linear` | (0, 0, 1, 1) | non-stylized/technical motion |
| `easing.standard` | (0.2, 0, 0, 1) | on-screen utility animation |
| `easing.standard.accelerate` | (0.3, 0, 1, 1) | exits |
| `easing.standard.decelerate` | (0, 0, 0, 1) | entrances |
| `easing.emphasized` | (0.2, 0, 0, 1) | M3-styled on-screen animation (see caveat) |
| `easing.emphasized.accelerate` | (0.3, 0, 0.8, 0.15) | M3-styled exits |
| `easing.emphasized.decelerate` | (0.05, 0.7, 0.1, 1) | M3-styled entrances |
| `easing.legacy` | (0.4, 0, 0.2, 1) | the M2 standard curve |
| `easing.legacy.accelerate` | (0.4, 0, 1, 1) | M2 exits |
| `easing.legacy.decelerate` | (0, 0, 0.2, 1) | M2 entrances |

**Emphasized caveat:** in the published token JSON and material-web, `emphasized` carries the
*same* bezier as `standard` — the emphasized *family's* distinctness lives in its accelerate/
decelerate variants. Android's emphasized interpolator has historically been a path interpolator;
verify per platform rather than assuming one curve everywhere.

## Duration tokens (ms)

| Tier | Tokens | Values |
|---|---|---|
| short | `duration.short1–4` | 50 · 100 · 150 · 200 |
| medium | `duration.medium1–4` | 250 · 300 · 350 · 400 |
| long | `duration.long1–4` | 450 · 500 · 550 · 600 |
| extra-long | `duration.extra-long1–4` | 700 · 800 · 900 · 1000 |

## Spring tokens (M3 Expressive, introduced May 2025)

`md.sys.motion.spring.{speed}.{type}` — documented as replacing duration+easing for most new
work; duration+easing remains the fallback and the only system material-web implements.

Two types by animated property: **spatial** (position/rotation/size/corners — overshoots) and
**effects** (color/opacity — never overshoots). Three speeds by scope:

| Speed | Scope | Spatial stiffness/damping | Effects stiffness/damping |
|---|---|---|---|
| fast | small components (switches, icons) | 1400 / 0.9 | 3800 / 1 |
| default | partial-screen (drawers, FABs) | 700 / 0.9 | 1600 / 1 |
| slow | full-screen transitions | 300 / 0.9 | 800 / 1 |

The values above are the single set MDC-Android publishes; per-scheme variants are unpublished
(see Unverified edges). Two preset schemes: **Expressive** (overshooting springs — hero moments,
the M3 default) and **Standard** (minimal bounce, utilitarian).
(m3.material.io/blog/m3-expressive-motion-theming; MDC-Android Motion.md.)

## Platform exposure (drift is real)

- **Android/Compose** — full: `motionEasing*Interpolator`, `motionDuration{Tier}{N}`,
  `MotionScheme` (expressive/standard) with spring tokens.
- **Web (material-web, v2.x — maintenance mode)** — easing+duration custom properties ONLY; **no
  `--md-sys-motion-spring-*` exists**. Expressive feel on web = JS springs (Web Animations API /
  a sampled CSS `linear()` curve) driven by the stiffness/damping values above.
- **Flutter** — `SpringDescription(mass, stiffness, damping)` + M3 theme slots; Expressive parity
  still rolling out (flutter/flutter#116526).

## Unverified edges (2026-07-09)

Per-device spring adaptation values (wearable/tablet), per-scheme (Expressive vs Standard) spring
value variants, the component-by-component Expressive adoption inventory, and material-web's
spring roadmap — none published; don't invent them.
