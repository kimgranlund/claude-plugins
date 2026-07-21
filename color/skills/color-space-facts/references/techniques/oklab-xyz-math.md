# OKLab ↔ XYZ — Math

OKLab is Björn Ottosson's 2020 perceptually-uniform color space. **It corrects
CIELAB's known issues** — particularly the blue-purple hue curvature — and is
the modern default for perceptual color manipulation.

For UI design tokens, gradient interpolation, and palette generation, OKLab (or
its polar form OKLCH) is the right starting point.

---

## TL;DR

OKLab transforms XYZ to a perceptually-uniform $(L, a, b)$ representation via
two matrices and a **cube-root nonlinearity** on intermediate LMS (cone-like)
response:

$$
\text{XYZ} \xrightarrow{M_1} \text{LMS} \xrightarrow{(\cdot)^{1/3}} \text{LMS}' \xrightarrow{M_2} \text{OKLab}
$$

- $L$: perceived lightness, roughly $[0, 1]$ (close to perceptually linear).
- $a$: red-green axis (positive = red).
- $b$: yellow-blue axis (positive = yellow).
- Polar form **OKLCH** uses $(L, C, h_\text{deg})$ where $C = \sqrt{a^2 + b^2}$
  and $h = \text{atan2}(b, a)$.

---

## Natural-language description

CIELAB was the 1976 perceptually-uniform standard. Two known issues prompted
OKLab's design:

1. **Blue-purple hue curvature**: in CIELAB, the blue-violet hue line bends
  noticeably as lightness changes. A uniform-hue gradient produces visibly
  hue-shifting colors.
2. **Inconsistent chroma**: equal-magnitude chroma steps don't look equal
  across hues, particularly at high chroma.

Ottosson's approach:

1. Start from XYZ.
2. Map to **LMS** (long, medium, short cone responses) via a learned matrix.
   The matrix is optimized for perceptual uniformity rather than physiological
   accuracy.
3. Apply cube-root nonlinearity (analogous to CIELAB's $f(t)$, but applied to
   LMS directly).
4. Map to opponent-color $(L, a, b)$ via a second learned matrix.

The two matrices $M_1$ and $M_2$ were derived by fitting against perceptual
datasets. The full derivation is in Ottosson's 2020 article (cited below).

**Why use OKLab over CIELAB:**

- Perceptually uniform hue across the lightness range (no blue-purple shift).
- Better suited for gradients (no mid-gradient darkening or hue drift).
- Compatible with modern displays (D65 white point built in).
- Native to CSS Color 4 (`oklab()`, `oklch()`).

**Why CIELAB still matters:**

- ICC profile interoperability.
- 40+ years of literature and tooling.
- $\Delta E_{2000}$ contrast metric is well-calibrated in CIELAB space.

---

## Formulas

### Step 1: XYZ-D65 → LMS (linear cone response)

$$
\begin{bmatrix} L_\ell \\ M_\ell \\ S_\ell \end{bmatrix}
= M_1
\begin{bmatrix} X \\ Y \\ Z \end{bmatrix}
$$

$$
M_1 =
\begin{bmatrix}
0.8189330101 & 0.3618667424 & -0.1288597137 \\
0.0329845436 & 0.9293118715 & \phantom{-}0.0361456387 \\
0.0482003018 & 0.2643662691 & \phantom{-}0.6338517070
\end{bmatrix}
$$

### Step 2: LMS → LMS' (cube root)

Sign-preserving cube root applied component-wise:

$$
L' = \sqrt[3]{L_\ell}, \quad M' = \sqrt[3]{M_\ell}, \quad S' = \sqrt[3]{S_\ell}
$$

### Step 3: LMS' → OKLab

$$
\begin{bmatrix} L \\ a \\ b \end{bmatrix}
= M_2
\begin{bmatrix} L' \\ M' \\ S' \end{bmatrix}
$$

$$
M_2 =
\begin{bmatrix}
0.2104542553 & \phantom{-}0.7936177850 & -0.0040720468 \\
1.9779984951 & -2.4285922050 & \phantom{-}0.4505937099 \\
0.0259040371 & \phantom{-}0.7827717662 & -0.8086757660
\end{bmatrix}
$$

**Note**: the first column of $M_2$'s inverse is all 1s (a defining structural
property — it ensures $L$ is a pure lightness component decoupled from $a, b$).

### Inverse: OKLab → XYZ-D65

$$
\begin{aligned}
\begin{bmatrix} L' \\ M' \\ S' \end{bmatrix} &= M_2^{-1} \begin{bmatrix} L \\ a \\ b \end{bmatrix} \\
\begin{bmatrix} L_\ell \\ M_\ell \\ S_\ell \end{bmatrix} &= \begin{bmatrix} (L')^3 \\ (M')^3 \\ (S')^3 \end{bmatrix} \\
\begin{bmatrix} X \\ Y \\ Z \end{bmatrix} &= M_1^{-1} \begin{bmatrix} L_\ell \\ M_\ell \\ S_\ell \end{bmatrix}
\end{aligned}
$$

$$
M_1^{-1} =
\begin{bmatrix}
\phantom{-}1.2270138511 & -0.5577999807 & \phantom{-}0.2812561490 \\
-0.0405801784 & \phantom{-}1.1122568696 & -0.0716766787 \\
-0.0763812845 & -0.4214819784 & \phantom{-}1.5861632204
\end{bmatrix}
$$

$$
M_2^{-1} =
\begin{bmatrix}
1.0000000000 & \phantom{-}0.3963377774 & \phantom{-}0.2158037573 \\
1.0000000000 & -0.1055613458 & -0.0638541728 \\
1.0000000000 & -0.0894841775 & -1.2914855480
\end{bmatrix}
$$

### Polar form (OKLCH)

$$
C = \sqrt{a^2 + b^2}, \qquad h = \text{atan2}(b, a) \cdot \frac{180}{\pi}
$$

Normalize $h$ to $[0, 360)$ by adding $360$ if negative.

---

## Implementation

Canonical TypeScript:

- [`src/spaces/oklab.ts`](../../../../color-science-project-files/src/spaces/oklab.ts) — OKLab ↔ XYZ-D65
- [`src/spaces/oklch.ts`](../../../../color-science-project-files/src/spaces/oklch.ts) — OKLCH ↔ XYZ-D65 (polar)
- [`src/gamut/oklch-peak.ts`](../../../../color-science-project-files/src/gamut/oklch-peak.ts) — Peak L(C, h) and C(L, h) for sRGB / P3 / Rec.2020

```ts
const cbrt = (x: number) => Math.sign(x) * Math.pow(Math.abs(x), 1 / 3);

export function fromXYZ(c: XYZ_D65): OKLab {
  const lms = mulMat3Vec3(M1, c);
  const lmsPrime: [number, number, number] = [cbrt(lms[0]), cbrt(lms[1]), cbrt(lms[2])];
  const [L, a, b] = mulMat3Vec3(M2, lmsPrime);
  return oklab(L, a, b);
}

export function toXYZ(c: OKLab): XYZ_D65 {
  const lmsPrime = mulMat3Vec3(M2_INV, c);
  const lms: [number, number, number] = [lmsPrime[0] ** 3, lmsPrime[1] ** 3, lmsPrime[2] ** 3];
  const [X, Y, Z] = mulMat3Vec3(M1_INV, lms);
  return xyz(X, Y, Z);
}
```

**Sign-preserving cube root** is essential: out-of-gamut OKLab inputs (e.g.,
high-chroma colors that don't fit in sRGB) produce negative LMS values, and
JavaScript's `Math.pow` of a negative base to a fractional exponent returns
`NaN`. The sign-preserving form keeps the math defined everywhere.

---

## Edge cases

- **Out-of-gamut**: OKLab can represent colors outside any specific RGB gamut.
  `toXYZ(oklab(0.5, 0.5, 0))` returns valid XYZ; converting to linear sRGB may
  give negative or >1 components. Gamut handling (clipping or mapping) is
  separate from the OKLab math. See
  [`oklch-gamut-peak-math.md`](./oklch-gamut-peak-math.md) and
  `src/gamut/oklch-peak.ts`.
- **Hue indeterminacy at C=0**: OKLCH round-trip at the achromatic axis
  produces arbitrary hue values from float noise. Mathematically correct.
- **Numerical precision**: round-trip identity holds to $\sim 10^{-4}$ due to
  the cube-root nonlinearity. Linear matrix transforms achieve $\sim 10^{-9}$.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/oklab.ts` + `src/spaces/oklch.ts` — branded, sign-preserving. |
| **Culori** | `mode_oklab`, `mode_oklch`. Robust default. |
| **Color.js** | `ColorSpace.get('oklab')`, `ColorSpace.get('oklch')`. |
| **@texel/color** | Minimal, fast OKLab implementation. Use for real-time pickers. |
| **Ottosson reference C** | <https://bottosson.github.io/posts/oklab/> — canonical 100-line implementation. |

---

## Primary sources

- **Björn Ottosson, "A perceptual color space for image processing" (2020)** —
  the OKLab paper. $M_1$ and $M_2$ matrices defined here.
  <https://bottosson.github.io/posts/oklab/>
- **Björn Ottosson, "How software gets color wrong" (2021)** — context on
  why OKLab matters for design work.
  <https://bottosson.github.io/posts/colorwrong/>
- **W3C CSS Color 4** — web-normative definition:
  <https://www.w3.org/TR/css-color-4/#ok-lab>
