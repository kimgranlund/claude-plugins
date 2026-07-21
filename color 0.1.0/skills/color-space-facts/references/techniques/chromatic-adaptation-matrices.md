# Chromatic Adaptation Matrices — Math

Chromatic adaptation models how the human visual system "discounts" the
illuminant — why a white piece of paper looks white under daylight (D65) and
under tungsten (A) even though the spectral content is wildly different. The
math: scale color-opponent responses to match the destination illuminant.

**Bradford** is the standard for ICC profile work and CSS Color 4.
**CAT16** is the standard for CIECAM16 (used by Material HCT). They differ
slightly in their response matrices but follow identical structure.

---

## TL;DR

Adapt $\text{XYZ}_{src}$ at source white $W_s$ to $\text{XYZ}_{dst}$ at
destination white $W_d$:

1. Transform XYZ to cone-response space: $\rho = M \cdot \text{XYZ}$.
2. Compute per-channel scale factors: $D_i = \rho_d[i] / \rho_s[i]$ where
   $\rho_d = M \cdot W_d$ and $\rho_s = M \cdot W_s$.
3. Apply diagonal scaling: $\rho' = \text{diag}(\vec{D}) \cdot \rho$.
4. Transform back to XYZ: $\text{XYZ}_{dst} = M^{-1} \cdot \rho'$.

Combined into a single matrix:

$$
M_{\text{adapt}} = M^{-1} \cdot \text{diag}(\rho_d / \rho_s) \cdot M
$$

Apply this matrix to source XYZ for the adapted XYZ. **Pre-compute and cache**
when adapting many colors between the same illuminants.

---

## Natural-language description

Why chromatic adaptation matters:

- **ICC profile work**: ICC's Profile Connection Space (PCS) is at D50. Modern
  displays are at D65. Converting an ICC-tagged image to display-ready sRGB
  requires D50 → D65 adaptation.
- **CIELAB across white points**: CIELAB-D50 (traditional) and CIELAB-D65 (modern
  display) differ by Bradford adaptation. Mixing them silently gives ~5% color
  errors.
- **Multi-illuminant rendering**: rendering a scene under one illuminant and
  displaying under another (white-balance correction) is adaptation.

The Bradford CAT was derived by Lam (1985) by optimizing fit to perceptual
data on chromatic adaptation. CAT02 (CIECAM02) and CAT16 (CIECAM16) were
later refinements. Bradford remains the most widely adopted because it's the
ICC standard.

**Why diagonal scaling works**: the von Kries hypothesis — the visual system
adapts each cone class independently. If true, adaptation is mathematically
just scaling each cone response. The "cone response matrix" $M$ is a learned
approximation to the actual cone fundamentals, optimized for adaptation fit
rather than physiological accuracy.

---

## Formulas

### Bradford matrix

$$
M_{\text{Bradford}} =
\begin{bmatrix}
\phantom{-}0.8951 & \phantom{-}0.2664 & -0.1614 \\
-0.7502 & \phantom{-}1.7135 & \phantom{-}0.0367 \\
\phantom{-}0.0389 & -0.0685 & \phantom{-}1.0296
\end{bmatrix}
$$

$$
M_{\text{Bradford}}^{-1} =
\begin{bmatrix}
\phantom{-}0.9869929 & -0.1470543 & \phantom{-}0.1599627 \\
\phantom{-}0.4323053 & \phantom{-}0.5183603 & \phantom{-}0.0492912 \\
-0.0085287 & \phantom{-}0.0400428 & \phantom{-}0.9684867
\end{bmatrix}
$$

### CAT16 matrix (CIECAM16)

$$
M_{\text{CAT16}} =
\begin{bmatrix}
\phantom{-}0.401288 & \phantom{-}0.650173 & -0.051461 \\
-0.250268 & \phantom{-}1.204414 & \phantom{-}0.045854 \\
-0.002079 & \phantom{-}0.048952 & \phantom{-}0.953127
\end{bmatrix}
$$

(Used by [`src/spaces/ciecam16.ts`](../../../../color-science-project-files/src/spaces/ciecam16.ts).)

### Adaptation procedure

Given source white $W_s$, destination white $W_d$, and source color
$\text{XYZ}_s$:

$$
\begin{aligned}
\rho_s &= M \cdot W_s \\
\rho_d &= M \cdot W_d \\
\rho &= M \cdot \text{XYZ}_s \\
\rho' &= \begin{bmatrix} \rho[0] \cdot \rho_d[0] / \rho_s[0] \\
                          \rho[1] \cdot \rho_d[1] / \rho_s[1] \\
                          \rho[2] \cdot \rho_d[2] / \rho_s[2] \end{bmatrix} \\
\text{XYZ}_{dst} &= M^{-1} \cdot \rho'
\end{aligned}
$$

Equivalently, pre-compute the adaptation matrix:

$$
M_{\text{adapt}} = M^{-1} \cdot
\begin{bmatrix}
\rho_d[0] / \rho_s[0] & 0 & 0 \\
0 & \rho_d[1] / \rho_s[1] & 0 \\
0 & 0 & \rho_d[2] / \rho_s[2]
\end{bmatrix} \cdot M
$$

Then $\text{XYZ}_{dst} = M_{\text{adapt}} \cdot \text{XYZ}_s$.

### Standard illuminant white points (XYZ, Y=1)

| Illuminant | $X_n$ | $Y_n$ | $Z_n$ |
|---|---|---|---|
| **D65** | 0.95046 | 1.0 | 1.08906 |
| **D50** | 0.96430 | 1.0 | 0.82510 |
| **D55** | 0.95682 | 1.0 | 0.92149 |
| **A**   | 1.09850 | 1.0 | 0.35585 |
| **F2**  | 0.99186 | 1.0 | 0.67393 |

---

## Implementation

Canonical TypeScript: [`src/adaptation/bradford.ts`](../../../../color-science-project-files/src/adaptation/bradford.ts).

Exports:
- `M_BRADFORD`, `M_BRADFORD_INV` — the matrices
- `D65`, `D50`, `A`, `F2` — pre-computed illuminant XYZ values
- `bradfordMatrix(srcWhite, dstWhite)` — generic adaptation matrix builder
- `adapt(srcXYZ, srcWhite, dstWhite)` — single-color adaptation
- `d50ToD65(...)`, `d65ToD50(...)` — convenience for the common ICC case
- `M_D50_TO_D65`, `M_D65_TO_D50` — pre-computed matrices

```ts
export function bradfordMatrix(srcWhite, dstWhite): Matrix3x3 {
  const rgbSrc = mulMat3Vec3(M_BRADFORD, srcWhite);
  const rgbDst = mulMat3Vec3(M_BRADFORD, dstWhite);
  const D: Matrix3x3 = [
    [rgbDst[0] / rgbSrc[0], 0, 0],
    [0, rgbDst[1] / rgbSrc[1], 0],
    [0, 0, rgbDst[2] / rgbSrc[2]],
  ];
  return mulMat3Mat3(M_BRADFORD_INV, mulMat3Mat3(D, M_BRADFORD));
}
```

Test vectors verify identity (D65 → D65), round-trip (D65 → D50 → D65),
and white-point mapping (D65 white must map to D50 white).

CAT16 is currently embedded in `src/spaces/ciecam16.ts`. A future
`src/adaptation/cat16.ts` would extract it for general-purpose use.

---

## Edge cases

- **Precision**: published Bradford matrices are 7 digits; their inverse
  accumulates ~$10^{-7}$ error. Round-trip tolerance is $10^{-6}$ — strict
  enough to catch bugs, loose enough to accept published precision.
- **Near-black input**: $\rho$ components can be very small for dark colors;
  the diagonal scaling is still well-defined since $\rho_s$ at the white
  point is bounded away from zero.
- **Same source and destination white**: the adaptation matrix collapses to
  the identity (modulo floating-point precision). The implementation handles
  this correctly without a special case.
- **Black point compensation**: Bradford CAT does NOT compensate for the
  black point. Some ICC workflows apply a separate black-point compensation
  step; see the ICC v4 spec for details.

---

## Comparison: Bradford vs. CAT02 vs. CAT16

| | Bradford (1985) | CAT02 (2002) | CAT16 (2016) |
|---|---|---|---|
| **Used by** | ICC, CSS Color 4 | CIECAM02 | CIECAM16, Material HCT |
| **Status** | De-facto standard | Largely superseded | CIE-current |
| **Adoption** | Universal | Niche | Growing |
| **Performance fit** | Good | Slightly better | Best |

For new code without specific compatibility constraints: **use Bradford** for
generic chromatic adaptation, **use CAT16** when working with CIECAM16 or HCT.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/adaptation/bradford.ts` — Bradford with D50/D65/A/F2 illuminants. |
| **Culori** | `convertOklabToXyz50`, `convertOklabToXyz65`, etc. — implicit adaptation. |
| **Color.js** | `Color.adaptWhite(...)` with method selection. |
| **icc.js** | ICC profile work, handles black-point compensation. |

---

## Primary sources

- **Lam, K. M. (1985)** — *Metamerism and Colour Constancy* (PhD thesis,
  University of Bradford). Original Bradford CAT derivation.
- **CIE 159:2004** — A colour appearance model for colour management systems:
  CIECAM02 (and CAT02).
- **CIE 248:2022** — CIE CAM16 (CAT16).
- **ICC.1:2010-12** — Image technology colour management — Architecture, profile
  format, and data structure. ICC's Profile Connection Space at D50.
- **Bruce Lindbloom** — <http://brucelindbloom.com/Eqn_ChromAdapt.html> —
  practical implementation reference with all standard CAT matrices.
- **W3C CSS Color 4** — <https://www.w3.org/TR/css-color-4/#color-conversion> —
  web-normative Bradford reference.
