# Spline Interpolation in Color Spaces — Math

Cubic splines smoothly pass through a sequence of anchor colors. Use for
palette construction when you have non-uniformly spaced "key colors" (e.g.,
dark anchor, mid-tone with hue shift, light anchor) and want a smooth ramp
that hits each one exactly.

Catmull-Rom is the standard choice — it interpolates control points
exactly (no overshoot), provides C1 continuity at every interior point,
and has a simple closed-form expression.

---

## TL;DR

For four control points $P_0, P_1, P_2, P_3$ and parameter $t \in [0, 1]$:

$$
P(t) = \tfrac{1}{2} \big(2 P_1 + (-P_0 + P_2) t + (2 P_0 - 5 P_1 + 4 P_2 - P_3) t^2 + (-P_0 + 3 P_1 - 3 P_2 + P_3) t^3 \big)
$$

The curve interpolates $P_1$ at $t = 0$ and $P_2$ at $t = 1$. $P_0$ and
$P_3$ provide tangent direction at the endpoints.

For N anchors, chain segments using consecutive 4-tuples
$(P_{i-1}, P_i, P_{i+1}, P_{i+2})$ with endpoints duplicated for boundary
segments.

**Use in OKLab** for perceptually smooth ramps.

---

## Natural-language description

### When linear interpolation falls short

Linear interpolation between two colors $A$ and $B$ produces a straight
line in color space — no overshoot, no curvature. Fine for two-color
gradients, but limited:

- **No control over intermediate stops**: a 3-stop palette (dark, mid,
  light) needs the mid-stop to be exactly where you want it. Linear
  segments produce a piecewise-linear ramp with visible kinks at the mid.

- **No smooth tangents**: a chained linear ramp through (dark, mid, light)
  has a sharp "elbow" at the mid — visible as a banding artifact in a
  gradient.

### Catmull-Rom solves both

- **Interpolates exactly** at every control point.
- **C1 continuous** at interior points (the tangent direction matches
  on both sides of each anchor).
- **Local control** — moving one anchor only affects the two adjacent
  segments.

The Catmull-Rom formula uses each control point's neighbors to determine
tangent direction at that point. The tangent at $P_i$ is $(P_{i+1} - P_{i-1}) / 2$ —
the average direction of the neighboring chords.

### In color space

The spline operates component-wise on a color tuple. In OKLab:
$(L_0, a_0, b_0), (L_1, a_1, b_1), \ldots$ — run Catmull-Rom on each
component independently. Result: an OKLab curve through the anchors.

OKLab is the right choice because Euclidean distance ≈ ΔE_ok, so the
spline's curvature matches perceptual smoothness.

---

## Formulas

### Catmull-Rom cubic (uniform)

Given $P_0, P_1, P_2, P_3$ and $t \in [0, 1]$:

$$
P(t) = \tfrac{1}{2} \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}
\begin{bmatrix}
0 & 2 & 0 & 0 \\
-1 & 0 & 1 & 0 \\
2 & -5 & 4 & -1 \\
-1 & 3 & -3 & 1
\end{bmatrix}
\begin{bmatrix} P_0 \\ P_1 \\ P_2 \\ P_3 \end{bmatrix}
$$

Expanded:

$$
P(t) = \tfrac{1}{2} \big[ 2 P_1 + (-P_0 + P_2) t + (2 P_0 - 5 P_1 + 4 P_2 - P_3) t^2 + (-P_0 + 3 P_1 - 3 P_2 + P_3) t^3 \big]
$$

### Chained Catmull-Rom

For $n + 1$ control points $P_0, P_1, \ldots, P_n$ at parameter values
$0, 1, \ldots, n$ (uniform spacing), the curve at parameter $u \in [0, n]$:

1. Let $i = \lfloor u \rfloor$ (clamped to $[0, n-1]$).
2. Let local $t = u - i$.
3. Use control points $P_{i-1}, P_i, P_{i+1}, P_{i+2}$ (clamped at
   endpoints).

Endpoint convention: duplicate first and last control points
($P_{-1} = P_0$, $P_{n+1} = P_n$). Produces no extrapolation beyond the
input range.

### Centripetal Catmull-Rom (variant)

For non-uniform spacing or to avoid loops near sharp turns, use
**centripetal Catmull-Rom**: parametrize by $t_i = t_{i-1} + \sqrt{\|P_i - P_{i-1}\|}$.
Not implemented in this skill (uniform is sufficient for typical palette
work).

---

## Implementation

Canonical TypeScript: [`src/interpolation/spline.ts`](../../../../color-science-project-files/src/interpolation/spline.ts).

Exports:
- `catmullRomScalar(P0, P1, P2, P3, t)` — scalar
- `catmullRomTuple(P0, P1, P2, P3, t)` — 3-tuple
- `catmullRomCurve(controls, t)` — through any number of controls, t in [0, 1]
- `catmullRomSamples(controls, n)` — n equally-spaced samples

```ts
export function catmullRomScalar(P0, P1, P2, P3, t): number {
  const t2 = t * t;
  const t3 = t2 * t;
  return 0.5 * (
    (2 * P1) +
    (-P0 + P2) * t +
    (2 * P0 - 5 * P1 + 4 * P2 - P3) * t2 +
    (-P0 + 3 * P1 - 3 * P2 + P3) * t3
  );
}

export function catmullRomCurve(controls, t): [number, number, number] {
  const n = controls.length - 1;
  const u = t * n;
  const segment = Math.min(Math.floor(u), n - 1);
  const localT = u - segment;
  const P0 = controls[Math.max(0, segment - 1)];
  const P1 = controls[segment];
  const P2 = controls[segment + 1];
  const P3 = controls[Math.min(n, segment + 2)];
  return catmullRomTuple(P0, P1, P2, P3, localT);
}
```

Test vectors verify endpoint anchoring ($P_1$ at $t=0$, $P_2$ at $t=1$),
linear case (equal-spaced controls → linear midpoint), and full-curve
anchoring at the first and last control.

---

## Typical usage: building a 9-stop palette through 3 anchors

```ts
import { catmullRomSamples } from '../interpolation/spline.js';

// Three OKLab anchor colors
const anchors = [
  [0.20, 0.05, 0.05],   // dark
  [0.55, 0.12, 0.03],   // mid with warm hue shift
  [0.90, 0.02, -0.02],  // light cool
];

// Generate 9 equally-spaced colors through the anchors
const palette = catmullRomSamples(anchors, 9);
// palette[0] === anchors[0]
// palette[4] ≈ anchors[1] (close — mid-anchor at u = n/2)
// palette[8] === anchors[2]
```

For more anchors, the spline smoothly threads through every one with C1
continuity.

---

## Comparison: linear vs spline

| | Linear (per segment) | Catmull-Rom spline |
|---|---|---|
| **Passes through anchors** | Yes | Yes |
| **Smooth at anchors** | No (sharp elbow) | Yes (C1 tangent matching) |
| **Overshoot** | Never | Never (uniform Catmull-Rom) |
| **Cost per sample** | 1 add + 1 multiply per dim | 4 adds + 7 multiplies per dim |
| **Use case** | Two-color or already-smooth controls | 3+ anchors needing smooth ramp |

---

## Edge cases

- **2 controls**: degenerates to linear interpolation (the implementation
  handles this).
- **1 control**: returns that single color regardless of $t$.
- **Very close anchors**: can produce subtle wiggles. Centripetal
  parameterization fixes this; not implemented.
- **Anchors on a straight line**: Catmull-Rom on collinear controls
  produces a straight line (the cubic degenerates).

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/interpolation/spline.ts` — uniform Catmull-Rom. |
| **D3** | `d3.interpolateRgbBasis(colors)` uses B-spline. |
| **Culori** | `interpolatorSplineBasis`, `interpolatorSplineNatural`. |
| **Color.js** | `Color.steps(colors, { space, outputSpace })` supports custom interpolators. |

---

## Primary sources

- **Catmull, E. & Rom, R. (1974)** — "A class of local interpolating
  splines," *Computer Aided Geometric Design*.
- **Yuksel, C., Schaefer, S., Keyser, J. (2011)** — "Parameterization
  and applications of Catmull-Rom curves," *Computer-Aided Design* 43.
- **Companion**: [`gradient-interpolation-math.md`](./gradient-interpolation-math.md) —
  linear interpolation primitives.
