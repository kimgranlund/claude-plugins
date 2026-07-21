# CIELAB ↔ XYZ Conversion — Math

CIELAB (CIE 1976 $L^*a^*b^*$) is the canonical perceptual color space of 20th
century color science. Defined by a cube-root nonlinearity applied to XYZ /
white-point ratios. Still widely used for $\Delta E$ color difference, ICC
profiles, and as the basis for CIELCH (polar form) and Material HCT (which uses
$L^*$ as its tone axis).

For modern UI work, **OKLab** corrects CIELAB's known issues (blue-purple
curvature) and should usually be preferred. But CIELAB remains the
interoperability standard — every color-management pipeline speaks it.

---

## TL;DR

$$
L^* = 116 \cdot f(Y/Y_n) - 16, \quad
a^* = 500 \cdot \big(f(X/X_n) - f(Y/Y_n)\big), \quad
b^* = 200 \cdot \big(f(Y/Y_n) - f(Z/Z_n)\big)
$$

where $f$ is a piecewise function with a cube-root upper branch and a linear
lower branch:

$$
f(t) =
\begin{cases}
\sqrt[3]{t} & \text{if } t > \delta^3 \\
\dfrac{t}{3 \delta^2} + \dfrac{4}{29} & \text{otherwise}
\end{cases},
\quad \delta = \tfrac{6}{29}
$$

Reference white $(X_n, Y_n, Z_n)$ depends on the chosen illuminant. **This skill
uses D65** for `CIELAB_D65`; D50 variants exist for ICC profile work.

---

## Natural-language description

CIELAB approximates perceptual uniformity in 1976-era research. Its three axes:

- **$L^*$** — perceived lightness in $[0, 100]$. $L^* = 0$ is pure black,
  $L^* = 100$ is the reference white. $L^*$ approximates the lightness an
  average observer would assign on a perceptual scale.
- **$a^*$** — red-green opponency. Positive $a^*$ is more red, negative is
  more green. Typical range $[-128, 128]$.
- **$b^*$** — yellow-blue opponency. Positive $b^*$ is more yellow, negative
  is more blue. Same range as $a^*$.

The cube-root nonlinearity approximates Stevens's psychophysical law that
perceived brightness goes roughly as luminance to the 1/3 power. The linear
segment near zero prevents the cube root's infinite slope at the origin.

**Known limitations:**
- Blue-purple hues curve as lightness changes (the well-known "blue problem").
- Chroma uniformity is good but not great; CIEDE2000 was developed to patch
  $\Delta E$ in CIELAB space.
- D50 vs D65 ambiguity in literature — always know which white point is meant.

---

## Formulas

### Constants

$$
\delta = \frac{6}{29} \approx 0.2069, \quad
3\delta^2 = \frac{108}{841} \approx 0.1284, \quad
\frac{4}{29} \approx 0.1379
$$

The piecewise boundary at $t = \delta^3 \approx 0.00886$ (in normalized
$Y/Y_n$ space) corresponds to roughly $L^* = 8$.

### D65 reference white (Yw = 1 normalization)

$$
X_n = 0.95046, \quad Y_n = 1.00000, \quad Z_n = 1.08906
$$

The W3C CSS Color 4 high-precision values used in this skill:
$X_n = 0.9504559270516716$, $Z_n = 1.0890577507598784$.

### Forward: XYZ-D65 → CIELAB-D65

$$
\begin{aligned}
f_x &= f(X/X_n) \\
f_y &= f(Y/Y_n) \\
f_z &= f(Z/Z_n) \\
L^* &= 116 f_y - 16 \\
a^* &= 500 (f_x - f_y) \\
b^* &= 200 (f_y - f_z)
\end{aligned}
$$

### Inverse: CIELAB-D65 → XYZ-D65

Let $f^{-1}$ be:

$$
f^{-1}(t) =
\begin{cases}
t^3 & \text{if } t > \delta \\
3 \delta^2 (t - \tfrac{4}{29}) & \text{otherwise}
\end{cases}
$$

Then:

$$
\begin{aligned}
f_y &= (L^* + 16) / 116 \\
f_x &= f_y + a^* / 500 \\
f_z &= f_y - b^* / 200 \\
X &= X_n \cdot f^{-1}(f_x), \quad Y = Y_n \cdot f^{-1}(f_y), \quad Z = Z_n \cdot f^{-1}(f_z)
\end{aligned}
$$

---

## Implementation

Canonical TypeScript: [`src/spaces/cielab.ts`](../../../../color-science-project-files/src/spaces/cielab.ts).

Exports `toXYZ`, `fromXYZ`, and `testVectors`. Polar form (CIELCH) lives in
[`src/spaces/cielch.ts`](../../../../color-science-project-files/src/spaces/cielch.ts) and composes via CIELAB.

```ts
const DELTA = 6 / 29;
const DELTA_CUBED = DELTA * DELTA * DELTA;
const THREE_DELTA_SQ = 3 * DELTA * DELTA;
const FOUR_OVER_29 = 4 / 29;

function f(t: number): number {
  if (t > DELTA_CUBED) return Math.cbrt(t);
  return t / THREE_DELTA_SQ + FOUR_OVER_29;
}

function fInverse(t: number): number {
  if (t > DELTA) return t * t * t;
  return THREE_DELTA_SQ * (t - FOUR_OVER_29);
}

export function fromXYZ(c: XYZ_D65): CIELAB_D65 {
  const fx = f(c[0] / Xn);
  const fy = f(c[1] / Yn);
  const fz = f(c[2] / Zn);
  return cielab_D65(116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz));
}
```

The `cbrt` used in $f(t)$ is JavaScript's `Math.cbrt`, which is sign-preserving
(important for out-of-gamut inputs that produce negative $X/X_n$ etc.).

---

## Edge cases

- **D50 vs D65**: ICC profile work traditionally uses D50; modern display work
  uses D65. Mixing them produces ~5% color errors. This module is **D65 only**.
  D50 variants (and Bradford chromatic adaptation) would live in
  `src/spaces/cielab-d50.ts` and `src/adaptation/bradford.ts` (planned).
- **Out-of-gamut inputs**: negative $X/X_n$ or $Z/Z_n$ values can occur when
  converting wide-gamut content. The linear segment of $f(t)$ handles them
  smoothly; the cube-root branch via `Math.cbrt` is sign-preserving.
- **Round-trip precision**: tested at $10^{-4}$ tolerance due to the cube-root
  nonlinearity. Linear matrix transforms achieve $10^{-9}$.
- **Piecewise boundary**: at $t = \delta^3$, both branches agree exactly:
  $\sqrt[3]{\delta^3} = \delta$, and $\delta^3 / (3\delta^2) + 4/29 = \delta/3 + 4/29 = 6/29/3 + 4/29 = 2/29 + 4/29 = 6/29 = \delta$. The transition is C0-continuous and C1-continuous (the slopes match).

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/cielab.ts` — D65, branded, sign-preserving cube root. |
| **Culori** | `mode_lab65` and `mode_lab50` (D50 variant). |
| **Color.js** | `ColorSpace.get('lab')` (D50 default), `ColorSpace.get('lab-d65')`. |
| **Bruce Lindbloom** | <http://www.brucelindbloom.com/Eqn_XYZ_to_Lab.html> — formula reference and online calculator. |

---

## Primary sources

- **CIE 015:2018 — Colorimetry, 4th edition** — normative reference for CIELAB
  including the $f(t)$ definition and recommended illuminants.
- **W3C CSS Color 4** — web-normative D65 CIELAB:
  <https://www.w3.org/TR/css-color-4/#lab-colors>
- **CIE Publication 015:2004** (older) — established the D50/D65 ambiguity that
  the 2018 revision largely clarified.
- **Bruce Lindbloom** — practical implementation guidance and Bradford CAT
  matrices for D50/D65 interconversion.
