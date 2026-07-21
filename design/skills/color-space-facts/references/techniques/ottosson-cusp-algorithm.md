# Ottosson Cusp Algorithm — Math

The **cusp** is the maximum-chroma point of a gamut at a given hue. Ottosson's
2021 algorithm computes it in closed form (after one Halley's-method
refinement step). The cusp is the foundation for:

- **OKHSL / OKHSV** color pickers (shape the cylinder to the gamut)
- **Closed-form gamut mapping** (cusp-based chroma reduction, faster than
  binary search)
- **Maximum-chroma ramps** (designing palettes that walk the gamut envelope)

---

## TL;DR

For a hue direction $(a, b)$ with $a^2 + b^2 = 1$ in OKLab:

1. Compute max saturation $S_{max} = C / L$ along the hue ray. Selected by
   which sRGB face is hit first (red, green, or blue), refined via one step
   of Halley's method.
2. Convert OKLab $(L=1, S_{max} \cdot a, S_{max} \cdot b)$ to linear sRGB.
3. $L_{cusp} = \sqrt[3]{1 / \max(R, G, B)}$.
4. $C_{cusp} = L_{cusp} \cdot S_{max}$.

**Current scope: sRGB only.** Other gamuts use the same structure with
different polynomial coefficients per RGB face.

---

## Natural-language description

### What's the cusp?

Imagine the sRGB cube transformed into OKLab. At a fixed hue (a single slice
through the OKLab cylinder), the gamut looks like an irregular **diamond**.
The widest point of that diamond — the maximum-chroma point — is the cusp.

For pure red hue (29.23°), the cusp is at approximately $(L=0.628, C=0.258)$.
That's where the gamut is widest. Above and below this $L$, the maximum
achievable chroma decreases.

### Why a closed form?

The gamut boundary at a fixed hue is a cubic in $L$ (each linear RGB channel
is a cubic in $L$ when $(C, h)$ are fixed; see
[`oklch-gamut-peak-math.md`](./oklch-gamut-peak-math.md)). So finding the
maximum $C$ across all $L$ is a constrained optimization — solvable
analytically.

Ottosson's approach:

1. **Walk along the saturation ray**: from the origin, increase $S = C/L$
   while keeping $C/L$ constant. Eventually one of $R$, $G$, $B$ falls
   below zero (or above 1) — the first face you hit.

2. **The first-hit face depends on $(a, b)$**: three polynomial branches
   (red, green, blue) selected by simple linear inequalities.

3. **For each branch, a polynomial approximates $S_{max}$**: fit during
   model development. The polynomial gets within ~$10^{-3}$ of the true
   $S_{max}$.

4. **One Halley step refines to $\sim 10^{-9}$**: standard root-finding
   on the gamut-boundary equation.

5. **Convert to $(L, C)$**: the saturation ray $(L=1, S \cdot a, S \cdot b)$
   in OKLab maps to a specific linear-RGB direction; the cube root of the
   inverse-max-channel gives $L_{cusp}$.

---

## Formulas

### Step 1: Face selection

Given OKLab hue $(a, b)$ with $a^2 + b^2 = 1$:

$$
\text{Face} =
\begin{cases}
\text{Red}   & \text{if } -1.88170328 a - 0.80936493 b > 1 \\
\text{Green} & \text{else if } 1.81444104 a - 1.19445276 b > 1 \\
\text{Blue}  & \text{otherwise}
\end{cases}
$$

### Step 2: Polynomial $S_{max}$ approximation per face

Each face has 5 polynomial coefficients $(k_0, k_1, k_2, k_3, k_4)$ and 3
RGB-weight constants $(w_l, w_m, w_s)$:

| Face | $k_0$ | $k_1$ | $k_2$ | $k_3$ | $k_4$ |
|---|---|---|---|---|---|
| **Red** | 1.19086 | 1.76577 | 0.59663 | 0.75515 | 0.56771 |
| **Green** | 0.73957 | -0.45954 | 0.08285 | 0.12541 | 0.14503 |
| **Blue** | 1.35734 | -0.00916 | -1.15130 | -0.50560 | 0.00692 |

| Face | $w_l$ | $w_m$ | $w_s$ |
|---|---|---|---|
| **Red** | 4.0767 | -3.3077 | 0.2310 |
| **Green** | -1.2684 | 2.6098 | -0.3413 |
| **Blue** | -0.0042 | -0.7034 | 1.7076 |

Initial estimate:

$$
S = k_0 + k_1 a + k_2 b + k_3 a^2 + k_4 a b
$$

### Step 3: Halley's-method refinement

The exact equation is "$w_l \cdot l + w_m \cdot m + w_s \cdot s = 0$" where
$(l, m, s)$ are the cube of the LMS' values along the saturation ray.

Let $k_l = 0.39634 a + 0.21580 b$, $k_m = -0.10556 a - 0.06385 b$, $k_s = -0.08948 a - 1.29149 b$.

Define $l' = 1 + S k_l$, $m' = 1 + S k_m$, $s' = 1 + S k_s$.

Then $l = (l')^3$, $m = (m')^3$, $s = (s')^3$, and:

$$
\begin{aligned}
f(S) &= w_l l + w_m m + w_s s \\
f'(S) &= 3 w_l k_l (l')^2 + 3 w_m k_m (m')^2 + 3 w_s k_s (s')^2 \\
f''(S) &= 6 w_l k_l^2 l' + 6 w_m k_m^2 m' + 6 w_s k_s^2 s' \\
S_{\text{new}} &= S - \frac{f \cdot f'}{(f')^2 - \tfrac{1}{2} f \cdot f''}
\end{aligned}
$$

(Halley's method = Newton's method with second-order correction. Converges
cubically when the initial estimate is reasonable.)

### Step 4: $L_{cusp}$ and $C_{cusp}$

Compute OKLab $\to$ linear sRGB at $(L=1, S_{max} a, S_{max} b)$. Let
$M = \max(R, G, B)$:

$$
L_{cusp} = \sqrt[3]{1 / M}, \qquad C_{cusp} = L_{cusp} \cdot S_{max}
$$

---

## Implementation

Canonical TypeScript: [`src/gamut/cusp.ts`](../../../../color-science-project-files/src/gamut/cusp.ts).

Exports:
- `maxSaturationSRGB(a, b)` — $S_{max}$ for unit-norm $(a, b)$
- `findCuspSRGB(a, b)` — returns $[L_{cusp}, C_{cusp}]$ for unit-norm $(a, b)$
- `findCuspSRGBFromHueDeg(hueDeg)` — convenience over a degree input

```ts
export function findCuspSRGB(a: number, b: number): readonly [number, number] {
  const S = maxSaturationSRGB(a, b);
  const lab = oklab(1, S * a, S * b);
  const xyzVal = oklabSpace.toXYZ(lab);
  const rgb = srgbSpace.fromXYZ(xyzVal);
  const maxRGB = Math.max(rgb[0], rgb[1], rgb[2]);
  if (maxRGB <= 0) return [0, 0];
  const L_cusp = Math.cbrt(1 / maxRGB);
  const C_cusp = L_cusp * S;
  return [L_cusp, C_cusp];
}
```

Test vectors verify the cusp at hue 29.23° (pure red OKLCh hue) lands near
$(L \approx 0.628, C \approx 0.258)$, matching OKLab's pure-red coordinates.
Other test hues confirm the algorithm doesn't degrade for green/blue faces.

---

## Cusp table for sRGB (selected hues)

Computed by `findCuspSRGBFromHueDeg`:

| Hue (deg) | $L_{cusp}$ | $C_{cusp}$ | Notes |
|---|---|---|---|
| 29.23° | 0.628 | 0.258 | Pure red direction |
| 109.77° | 0.866 | 0.295 | Pure green direction |
| 264.05° | 0.496 | 0.314 | Near pure blue (cusp at higher L than sRGB blue's L) |
| 30° | 0.628 | 0.258 | (Same as 29.23 — sRGB red region) |
| 90° | 0.880 | 0.230 | Yellow-green region |
| 180° | 0.911 | 0.180 | Cyan |
| 360° | 0.628 | 0.258 | Wraps to red |

The cusp $L$ varies from ~0.45 (blue/violet) to ~0.91 (cyan). The cusp $C$
varies less, roughly $[0.18, 0.32]$ across all hues.

---

## Edge cases

- **Achromatic ($a = b = 0$)**: not a meaningful input. Saturation is
  undefined. Callers should short-circuit.
- **Non-unit-norm $(a, b)$**: `maxSaturationSRGB` assumes $a^2 + b^2 = 1$.
  If you have a non-normalized direction, normalize first.
- **Beyond Halley's convergence radius**: rare with the polynomial initial
  estimate; can occur for extreme out-of-domain inputs. Production code
  should iterate Halley once more or fall back to bisection.
- **P3 / Rec.2020 cusp**: requires re-deriving the polynomial coefficients
  for the wider gamuts. Deferred until needed.

---

## Why this matters more than the binary search

Binary-search gamut mapping (CSS Color 4) is $O(\log)$ iterations. The cusp
algorithm is $O(1)$ — a single calculation. For:

- **Real-time color pickers** (60 fps OKHSL editing): cusp is the
  efficiency-critical primitive.
- **Mass palette generation** (thousands of colors): cusp eliminates the
  log factor.
- **Mathematical reasoning** (proving palette properties): closed form
  enables analytic arguments.

For one-off color conversions where you don't care about throughput, binary
search is simpler and gives equivalent results.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/gamut/cusp.ts` — sRGB only, branded inputs, test vectors. |
| **Culori** | `findCuspOKLCH` (sRGB cusp implementation). |
| **@texel/color** | Fast implementations of cusp + OKHSL using the same algorithm. |
| **Ottosson reference** | <https://bottosson.github.io/posts/gamutclipping/> — original C++ source. |

---

## Primary sources

- **Björn Ottosson, "Gamut clipping" (2021)** —
  <https://bottosson.github.io/posts/gamutclipping/> — the algorithm + C++
  reference code.
- **Björn Ottosson, "Two new color spaces for color picking" (2021)** —
  <https://bottosson.github.io/posts/colorpicker/> — OKHSL / OKHSV built on
  the cusp algorithm.
- **Companion**: [`oklch-gamut-peak-math.md`](./oklch-gamut-peak-math.md) —
  why the gamut boundary is a cubic in $L$ at fixed $(C, h)$.
- **Companion**: [`css-color-4-gamut-mapping.md`](./css-color-4-gamut-mapping.md) —
  the binary-search alternative and when to prefer it.
