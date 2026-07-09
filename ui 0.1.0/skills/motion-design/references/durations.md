# Durations — how long UI motion should run

Researched 2026-07-09 from primary sources (nngroup.com, m1/m3.material.io, carbondesignsystem.com,
developer.apple.com, web.dev). Every value below is cited; the two things nobody publishes are
flagged at the end.

## The perceptual floor: Nielsen's three limits

- **0.1 s (100 ms)** — the limit for feeling that the system responds *instantly*; feedback within
  it reads as direct manipulation.
- **1 s** — the limit for an uninterrupted flow of thought.
- **10 s** — the limit for keeping attention on the dialogue at all.

Simple feedback (checkbox, toggle) ≈ 100 ms; the general UI sweet spot is **100–500 ms**; past
500 ms an animation starts to read as a drag. (nngroup.com/articles/response-times-3-important-limits,
/animation-duration — accessed 2026-07-09.)

## Published duration ladders

| System | Values | Source (2026-07-09) |
|---|---|---|
| Material 1 (mobile baseline) | standard 300 ms · large/complex 375 ms · enter 225 ms · exit 195 ms · >400 ms "too slow" | m1.material.io/motion/duration-easing |
| Material 1 (platform scaling) | desktop 150–200 ms · tablet +30% · wearable −30% | same |
| IBM Carbon (six duration tokens) | `$duration-fast-01/02` 70/110 ms · `$duration-moderate-01/02` 150/240 ms · `$duration-slow-01/02` 400/700 ms, scaled up dynamically with distance/size | carbon-design-system/carbon `packages/motion/index.scss` (verified in source 2026-07-09) |
| Industry consensus (web.dev + NN/g) | simple feedback ~100 ms · modal/major transition 200–300 ms · ease-out 200–500 ms · bounce/elastic 800–1200 ms | web.dev/articles/the-basics-of-easing |

## Duration is being replaced by physics at the top of the market

Apple parameterizes motion as **spring duration (seconds) + bounce**, not target milliseconds —
perceptual duration falls out of the physics (`stiffness = (2π ÷ duration)²`;
`CASpringAnimation.settlingDuration` computes when motion is imperceptible). Material 3 likewise
moved to spring tokens (stiffness/damping/velocity) and publishes **no fixed-duration ladder** for
its current spring scheme. Consequence: treat a millisecond ladder as the *web/CSS realization*,
and springs as the *model* — see `easing.md`. (developer.apple.com WWDC23 session 10158;
m3.material.io/styles/motion/overview/how-it-works — accessed 2026-07-09.)

## Enter/exit asymmetry

Exits run faster than entrances — the user is done with the thing and waiting for what's next.
Codified examples (web.dev/articles/asymmetric-animation-timing, m1.material.io):

- Navigation drawer: open 250 ms, close 200 ms. Card: expand 300 ms, collapse 250 ms.
  Modal: appear 300 ms, dismiss 200–250 ms.
- Direction of asymmetry flips with the initiator: **user-initiated** UI answers fast (enter
  ~100 ms) and departs gently (~300 ms); **system-initiated** UI (an error modal) enters slowly
  enough to be noticed (~300 ms) and gets out of the way fast.

## Scaling rules

- Duration scales **up with distance traveled and size changed** (Carbon: "the larger the change
  in distance or size, the longer the animation takes"; Carbon uses a non-linear scale and ships a
  Motion Generator tool). Material 1's 400 ms ceiling implies the same.
- Smaller elements animate faster; larger elements longer (also Fluent 2, fluent2.microsoft.design/motion).

## Honest gaps (do not invent these)

- **No published formula** maps distance→duration (Carbon's generator model is not public). Give a
  ladder plus the scaling *principle*, never a derived equation.
- **No universal enter:exit ratio** exists — published examples cluster around exits 15–35% faster,
  but no system codifies a constant.
