# CIECAM16 Forward / Inverse — Math

The CIE Color Appearance Model 16 (2022). Predicts how a color **appears** under
specified viewing conditions — accounting for surrounding luminance, adapting
field, background brightness, and chromatic adaptation. Output is a perceptual
triple $(J, M, h)$: lightness, colorfulness, hue.

**Use when**: you need cross-viewing-condition color matching, perceptual
ΔE under specific lighting, or as the foundation for Material HCT and CAM16-UCS.

**Don't use when**: OKLab/OKLCh suffices. CAM16 is heavier and assumes a
specific viewing setup; OKLab is "good enough" for most UI work and faster.

---

## TL;DR

CIECAM16 has **two phases**:

1. **Viewing condition setup** (precomputed once): from white point, adapting
   luminance, background L*, surround mode, compute scalars $D, F_L, n, N_{bb},
   N_{cb}, A_w, z, c$.
2. **Color transform**: XYZ → CAT16 RGB → adapted RGB → post-adaptation cone
   response → opponent (a, b) → J, M, h.

The reverse direction is symmetric: J, M, h → opponent → unadapted cone
response → adapted RGB → XYZ.

For Material HCT compatibility, use the convention **without** the +0.1 offset
on the post-adaptation cone response (CIE 248 specifies +0.1; Material omits it
so J=0 at black).

---

## Natural-language description

### The viewing condition problem

A piece of paper looks white under both:
- D65 daylight (~6500 K)
- A tungsten lamp (~2856 K)

Even though the spectral content reflected from the paper is radically different
in each case. The human visual system **adapts** to the illuminant, "discounting"
its color so the paper is perceived as white. This is **chromatic adaptation**.

CIELAB and OKLab assume a fixed adaptation (D65 = white). They give correct
results for D65 displays. But for cross-illuminant work — comparing a paint
chip under store lighting to the same chip under daylight, or rendering an
image for variable display conditions — you need an explicit appearance model
that takes viewing conditions as input.

CIECAM16 (and predecessor CIECAM02) does this.

### Structure

CAM16's forward path:

1. **Adapt XYZ to the reference white** via CAT16 chromatic adaptation matrix.
2. **Apply non-linear post-adaptation cone response** — the function that
   compresses high luminances and expands low luminances (analogous to OKLab's
   cube root, but more elaborate).
3. **Compute opponent signals** $(a, b)$ from the adapted cones.
4. **Derive perceptual quantities**: lightness J, colorfulness M, hue h,
   chroma C, saturation s, etc.

The inverse path undoes each step.

### Viewing condition scalars (precomputed once)

Given:
- $W$: reference white XYZ (at the viewing illuminant)
- $L_A$: adapting field luminance in $\text{cd}/\text{m}^2$
- $Y_b$: background luminance (from CIELAB L* of the background)
- Surround: dark (0), dim (1), average (2)
- Discounting illuminant: boolean

Computed:
- $D$: degree of chromatic adaptation (0 to 1; 1 = full discount)
- $F_L$: luminance adaptation factor
- $n = Y_b / Y_w$: background-to-white ratio
- $N_{bb}, N_{cb}$: chromatic induction factors
- $A_w$: achromatic response of the reference white
- $z = 1.48 + \sqrt{n}$: brightness exponent base
- $c$: surround-dependent exponent (0.525 dark, 0.59 dim, 0.69 average)
- $N_c$: chromatic surround factor (matches $c$)

**Default viewing conditions** (Material HCT defaults, sRGB display):
$W = (95.046, 100, 108.906)$ at D65, $L_A = (200/\pi) \cdot Y(L^*\!=\!50) / 100 \approx 11.7$ cd/m², $Y_b$ from $L^*=50$ ≈ 18.4, average surround, no illuminant discounting.

---

## Formulas

### CAT16 matrix (chromatic adaptation transform)

$$
M_{\text{CAT16}} =
\begin{bmatrix}
\phantom{-}0.401288 & \phantom{-}0.650173 & -0.051461 \\
-0.250268 & \phantom{-}1.204414 & \phantom{-}0.045854 \\
-0.002079 & \phantom{-}0.048952 & \phantom{-}0.953127
\end{bmatrix}
$$

### Degree of adaptation $D$

$$
D = F \cdot \left(1 - \frac{1}{3.6} e^{-(L_A + 42)/92}\right)
$$

Clamped to $[0, 1]$. $F$ is surround-dependent: $0.8$ dark, $0.9$ dim, $1.0$ average. If `discountingIlluminant: true`, set $D = 1$.

### Luminance adaptation factor $F_L$

$$
k = \frac{1}{5 L_A + 1}, \quad
F_L = k^4 L_A + 0.1 (1 - k^4)^2 \cdot (5 L_A)^{1/3}
$$

### Post-adaptation cone response

For a cone response $\rho_{adapted}$, the adapted signal is:

$$
\rho' = \frac{\text{sign}(\rho) \cdot 400 \cdot \big((F_L |\rho|) / 100\big)^{0.42}}{\big((F_L |\rho|) / 100\big)^{0.42} + 27.13}
$$

**Note: the CIE 248 standard adds $+0.1$ to this result.** This skill (and
Material HCT) omit the $+0.1$ so the response is zero at zero. See the
implementation notes below.

### Achromatic response and lightness

$$
A = (2 \rho_L' + \rho_M' + 0.05 \rho_S') \cdot N_{bb}, \quad
J = 100 \cdot \left(\frac{A}{A_w}\right)^{c \cdot z}
$$

### Opponent signals

$$
a = \rho_L' - \frac{12 \rho_M'}{11} + \frac{\rho_S'}{11}, \quad
b = \frac{\rho_L' + \rho_M' - 2 \rho_S'}{9}
$$

### Hue and chroma

$$
h = \text{atan2}(b, a), \quad
C = \alpha \sqrt{J / 100}, \quad
M = C \cdot F_L^{1/4}
$$

where $\alpha$ is a complex function of $a, b$, eccentricity, and viewing
condition scalars. See `src/spaces/ciecam16.ts` for the implementation; the
detailed formula has ~10 sub-terms and is best read in code.

### Inverse direction

The inverse is essentially the forward with each step reversed:

1. From $(J, M, h)$, compute $\alpha$, then opponent $a, b$, then achromatic $A$.
2. Solve for adapted cone responses $\rho'_L, \rho'_M, \rho'_S$.
3. Invert the post-adaptation cone response (closed-form inverse exists).
4. Divide by $\rho_D$ to get unadapted cone responses.
5. Apply $M_{\text{CAT16}}^{-1}$ to get XYZ.

---

## Implementation

Canonical TypeScript: [`src/spaces/ciecam16.ts`](../../../../color-science-project-files/src/spaces/ciecam16.ts).

Exports:
- `fromXYZ(xyz, precomputedVC?)` → `CIECAM16_JMh`
- `toXYZ(jmh, precomputedVC?)` → `XYZ_D65`
- `DEFAULT_VC` — Material HCT viewing conditions
- `ViewingConditions`, `PrecomputedVC` — type definitions

```ts
function adaptResponse(component: number, fl: number): number {
  const sign = Math.sign(component);
  const abs = Math.abs(component);
  const x = Math.pow((fl * abs) / 100, 0.42);
  return (sign * 400 * x) / (x + 27.13);
  // NOTE: CIE 248 includes a +0.1 offset; Material color-utilities omits it
  // so J=0 at black. This implementation follows Material's convention.
}
```

The full forward/inverse is ~200 lines of TypeScript. Test vector: black point
→ J=0, M=0 (the convention-defining property).

### Viewing condition precomputation

For performance, viewing conditions are precomputed once and reused:

```ts
const pre = precompute(myVC);  // computes D, F_L, n, N_{bb}, N_{cb}, A_w, etc.
const jmh1 = fromXYZ(xyz1, pre);
const jmh2 = fromXYZ(xyz2, pre);
// ... all use the same pre
```

The default precomputation uses `DEFAULT_VC` (Material HCT defaults).

---

## Edge cases

- **Black point ($Y = 0$)**: with the Material convention (no +0.1 offset), J=0
  exactly. With the CIE convention, J ≈ 0.236.
- **White point ($XYZ = W$) with `discountingIlluminant: false`**: produces
  residual chroma ~2-3. Property of partial chromatic adaptation, not a bug.
  Set `discountingIlluminant: true` to suppress.
- **Out-of-gamut input**: CAM16 doesn't clip; produces a value that may not be
  reproducible in any RGB gamut. Use gamut mapping (or HCT's iterative inverse)
  to find an in-gamut representative.
- **Achromatic hue indeterminacy**: when $M = 0$, $h$ is undefined; `atan2(0, 0)`
  returns 0. Round-trip works but hue is meaningless.
- **Custom viewing conditions**: any consistent `ViewingConditions` works,
  but cross-illuminant comparison requires both sides to share the same VC.
  Mixing VCs silently is a common bug.

---

## Comparison with OKLab and CIELAB

| Aspect | CIELAB | OKLab | CIECAM16 |
|---|---|---|---|
| **Viewing conditions** | Fixed D50 or D65 | Fixed D65 | Configurable |
| **Computational cost** | Low | Low | High (~10× OKLab) |
| **Perceptual uniformity** | OK (mid-tones), poor (blue) | Good | Best |
| **Use case** | ICC interop, ΔE2000 | UI design tokens, gradients | Cross-illuminant, appearance |

For UI work that lives entirely on sRGB/P3 displays at typical office
lighting, **OKLab is the right default**. CIECAM16 is for cases where
viewing conditions are explicit inputs.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/ciecam16.ts` — Material HCT convention, branded types. |
| **Material color-utilities** | <https://github.com/material-foundation/material-color-utilities> — reference for HCT compatibility. |
| **Culori** | `mode_cam16_jch` and related modes. |
| **Color.js** | `ColorSpace.get('cam16-jmh')`. |

---

## Primary sources

- **CIE 248:2022** — *CIE 2016 Colour Appearance Model for Colour Management
  Systems: CIECAM16*. Normative reference.
- **Li, Li, Wang, Cui, Luo, Melgosa, Brill, Pointer (2017)** — "Comprehensive
  color solutions: CAM16, CAT16, and CAM16-UCS," *Color Research & Application*
  42(6), 703–718. The companion paper bridging CIECAM16 ↔ CAM16-UCS.
- **Material Design 3 color utilities** —
  <https://github.com/material-foundation/material-color-utilities> —
  practical reference implementation in multiple languages.
- **Companion**: [`material-hct-math.md`](./material-hct-math.md) — HCT
  built on CIECAM16's hue and chroma.
- **Companion**: [`cam16-ucs-math.md`](./cam16-ucs-math.md) — the uniform
  Cartesian companion to CIECAM16's JMh.
- **Companion**: [`chromatic-adaptation-matrices.md`](./chromatic-adaptation-matrices.md) —
  CAT16 matrix used by the adaptation step.
