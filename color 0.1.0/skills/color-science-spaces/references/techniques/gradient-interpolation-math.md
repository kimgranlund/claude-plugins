# Gradient Interpolation & Hue Paths — Math

How to interpolate between two colors. The choice of **space** determines the
gradient's appearance — interpolating "in linear sRGB" produces different
mid-points than "in OKLab" than "in OKLCh." For cylindrical spaces, the choice
of **hue path** matters too.

This is foundational for design tokens (lightness ramps), data visualization
(continuous colormaps), and UI gradients.

---

## TL;DR

- **Default to OKLab.** Linear interpolation in OKLab is perceptually uniform
  and matches the CSS Color 4 default. Produces gradients without
  mid-gradient darkening or hue drift.
- **Avoid linear-sRGB interpolation** for visible gradients — even though it
  is mathematically "correct" for light addition, it produces perceptually
  uneven mid-points.
- **Avoid gamma-encoded sRGB interpolation** — produces mid-gradient darkening
  (the classic "muddy" gradient).
- **For cylindrical spaces** (OKLCh, CIELCh, HSL, HSV), pick a hue path:
  `shorter` (CSS default), `longer`, `increasing`, or `decreasing`.

---

## Natural-language description

### Why the space matters

Suppose you want to interpolate between **red** and **green** at $t = 0.5$:

| Space | Mid-point appearance |
|---|---|
| **Gamma-encoded sRGB** | Muddy dark olive — both channels at ~0.5 encoded means ~0.21 linear, perceptually dark. |
| **Linear sRGB** | Equal-energy mid-tone, but perceptually too bright; not where the eye expects "midway between red and green." |
| **CIELAB** | Better, but the blue-purple curvature can cause hue drift in other gradients. |
| **OKLab** | Perceptually uniform mid-point with no hue drift. |
| **OKLCh** | Same as OKLab, but with explicit hue path control for cylindrical wraparound. |

The "mid-gradient darkening" effect happens because the gamma function is
non-linear. Encoded values in [0, 1] compress dark intensities — averaging
two encoded values produces a value darker than the perceptual mid-point.
Interpolating in **linear** space avoids this, but produces a different
perceptual problem: the eye expects perceptual uniformity, not photon
uniformity.

OKLab's nonlinearity (cube root on LMS) is calibrated against perception
data. Linear interpolation in OKLab approximates linear interpolation in
*perception* — exactly what's wanted for visible gradients.

### Why hue paths matter

In OKLCh / CIELCh / HSL / HSV, hue is an angle in $[0, 360)$. Two angles
$h_1 = 350°$ and $h_2 = 10°$ are perceptually 20° apart (across the
red-magenta boundary), not 340° apart. Naive component-wise interpolation
walks the **wrong way**.

CSS Color 4 defines four hue paths:

- **shorter** (default): take the shorter arc. 350° → 10° goes through 0°.
- **longer**: take the longer arc. 350° → 10° goes through 180°.
- **increasing**: always rotate counterclockwise. 350° → 370° → 10°.
- **decreasing**: always rotate clockwise. 10° → -10° → 350° via 0°.

Most generative palette work wants `shorter`. `increasing` / `decreasing` are
useful for explicit rainbow ramps where you want a known number of full
rotations.

---

## Formulas

### Linear interpolation in any space

For a 3-tuple color $(c_0, c_1, c_2)$:

$$
\text{lerp}(\mathbf{a}, \mathbf{b}, t) =
\begin{bmatrix}
a_0 + t(b_0 - a_0) \\
a_1 + t(b_1 - a_1) \\
a_2 + t(b_2 - a_2)
\end{bmatrix}
$$

For cylindrical spaces (one component is hue), use the appropriate hue path
for that component instead of straight subtraction.

### Hue paths (CSS Color 4)

Let $\Delta = h_2 - h_1$ (signed difference). Define $\Delta_{\text{eff}}$
per path:

**Shorter**:

$$
\Delta_{\text{eff}} =
\begin{cases}
\Delta & \text{if } |\Delta| \le 180 \\
\Delta - 360 & \text{if } \Delta > 180 \\
\Delta + 360 & \text{if } \Delta < -180
\end{cases}
$$

**Longer**:

$$
\Delta_{\text{eff}} =
\begin{cases}
\Delta & \text{if } |\Delta| \ge 180 \\
\Delta - 360 & \text{if } 0 < \Delta < 180 \\
\Delta + 360 & \text{if } -180 < \Delta < 0
\end{cases}
$$

**Increasing**:

$$
\Delta_{\text{eff}} =
\begin{cases}
\Delta & \text{if } \Delta \ge 0 \\
\Delta + 360 & \text{if } \Delta < 0
\end{cases}
$$

**Decreasing**:

$$
\Delta_{\text{eff}} =
\begin{cases}
\Delta & \text{if } \Delta \le 0 \\
\Delta - 360 & \text{if } \Delta > 0
\end{cases}
$$

Then $h(t) = (h_1 + t \cdot \Delta_{\text{eff}}) \mod 360$.

### Mix via a target space

To "mix two sRGB colors in OKLab" (CSS Color 4 `color-mix(in oklab, ...)`):

$$
\text{mixVia}(a, b, t) = \text{srgb.fromXYZ}(\text{oklab.toXYZ}(\text{lerp}(\text{oklab}(a), \text{oklab}(b), t)))
$$

This produces an sRGB output whose mid-point reflects perceptual averaging
rather than channel averaging.

---

## Implementation

Canonical TypeScript: [`src/interpolation/linear.ts`](../../../../color-science-project-files/src/interpolation/linear.ts).

Exports:
- `lerpTuple(a, b, t)` — cartesian interpolation of 3-tuples
- `lerpOklab(a, b, t)`, `lerpCielab(a, b, t)` — typed wrappers
- `lerpHue(h1, h2, t, path)` — single-component hue interpolation
- `lerpOklch(a, b, t, huePath?)`, `lerpCielch(a, b, t, huePath?)` — cylindrical
- `mixVia(a, b, t, sourceSpace, viaSpace)` — CSS color-mix style
- `stops(n)`, `rampOklab(a, b, n)`, `rampOklch(a, b, n, huePath?)` — palette helpers

```ts
export function lerpHue(h1: number, h2: number, t: number, path: HuePath = 'shorter'): number {
  h1 = wrapHueDeg(h1);
  h2 = wrapHueDeg(h2);
  const diff = h2 - h1;
  let effDiff: number;
  switch (path) {
    case 'shorter':
      if (Math.abs(diff) <= 180) effDiff = diff;
      else if (diff > 180) effDiff = diff - 360;
      else effDiff = diff + 360;
      break;
    // ... other paths ...
  }
  return wrapHueDeg(h1 + t * effDiff);
}
```

Test vectors verify all four hue paths at the 350° / 10° boundary case (where
each path produces a different mid-point).

---

## Edge cases

- **Same hue**: any path returns the same hue (no rotation).
- **Hue exactly 180° apart**: `shorter` and `longer` are ambiguous — convention
  is `shorter` rotates in the positive direction.
- **t outside [0, 1]**: extrapolation. Mathematically defined but produces
  out-of-gamut results. Callers should clamp `t` first if extrapolation isn't
  desired.
- **NaN inputs**: not handled — pre-validate inputs.
- **Non-finite hue (Infinity)**: not handled — pre-validate.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/interpolation/linear.ts` — branded-typed, hue-path-aware. |
| **Culori** | `interpolate(colors, mode, options)` — supports all four hue paths. |
| **Color.js** | `Color.steps(a, b, options)` — CSS Color 4 reference implementation. |
| **CSS `color-mix()`** | Browsers implement this algorithm natively. |
| **chroma.js** | `chroma.mix(a, b, t, mode)` — limited hue path support. |

---

## Primary sources

- **W3C CSS Color Module Level 4** — <https://www.w3.org/TR/css-color-4/#interpolation> —
  normative algorithm for `color-mix()` and interpolation.
- **W3C CSS Color 4 — Hue interpolation** — <https://www.w3.org/TR/css-color-4/#hue-interpolation> —
  normative definition of the four hue paths.
- **Björn Ottosson 2020** — <https://bottosson.github.io/posts/oklab/> — why
  OKLab is the right default interpolation space for gradients.
- **Companion**: [`oklab-xyz-math.md`](./oklab-xyz-math.md) — OKLab definition.
- **Companion**: [`cylindrical-rgb-conversions.md`](./cylindrical-rgb-conversions.md) —
  the cylindrical-space context for hue paths.
