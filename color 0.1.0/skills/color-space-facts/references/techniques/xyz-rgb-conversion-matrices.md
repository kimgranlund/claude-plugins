# XYZ ↔ RGB Conversion Matrices — Math

The 3×3 matrices that map between CIE XYZ (D65) and each gamut-specific linear
RGB space. **Every conversion in this skill goes through XYZ-D65 as the source
of truth** ([ARCHITECTURE.md](../../../../color-science-project-files/ARCHITECTURE.md)), so these matrices are
foundational — every wide-gamut conversion, every chromatic adaptation, every
appearance-model forward pass starts here.

---

## TL;DR

A linear RGB space is defined by:
1. **Three primary chromaticities** $(x_r, y_r), (x_g, y_g), (x_b, y_b)$ — the
   colors of pure red / green / blue at maximum intensity.
2. **A white point** $(x_w, y_w)$ — the color that results when all three
   channels equal 1.

From those five chromaticities, the XYZ → RGB matrix is derived analytically.
The inverse RGB → XYZ matrix is the matrix inverse.

For modern displays the three standard gamuts are:

| Gamut | Primaries | White | Use |
|---|---|---|---|
| **sRGB** | BT.709 | D65 | Web default; ~35% of visible gamut |
| **Display P3** | DCI-P3 | D65 | Apple ecosystem; ~45% of visible gamut |
| **Rec.2020** | BT.2020 | D65 | HDR / UHD-TV; ~75% of visible gamut |

All four matrices below are at the **D65 white point** (Yw = 1) using the
W3C CSS Color 4 normative high-precision values.

---

## Natural-language description

The chromaticity-to-matrix derivation:

1. **Compute XYZ for each primary**: given chromaticity $(x_p, y_p)$ and $Y_p = 1$,
   $X_p = x_p / y_p$, $Z_p = (1 - x_p - y_p) / y_p$. Yields a 3×3 matrix $M_p$
   of primary XYZ values.
2. **Find the white-point scale factors**: solve $M_p \cdot \vec{S} = W$ where
   $W$ is the white point's XYZ. The $S_i$ values balance the primaries so
   $(1, 1, 1)$ RGB maps to the white point.
3. **The forward matrix** is $M = M_p \cdot \text{diag}(\vec{S})$.
4. **The inverse matrix** is $M^{-1}$.

This is mechanical once the chromaticities are fixed. The matrices below are
the result of this derivation for the three standard gamuts.

**Why D65 for all of them.** sRGB, Display P3, Rec.2020, and Rec.709 all specify
D65 as their reference white. ICC profiles often use D50 (the Profile Connection
Space); chromatic adaptation via [Bradford or CAT16](./chromatic-adaptation-matrices.md) bridges
D50 ↔ D65.

---

## Formulas

### sRGB ↔ XYZ-D65 (BT.709 primaries, IEC 61966-2-1)

$$
M_{\text{XYZ}\to\text{sRGB}} =
\begin{bmatrix}
\phantom{-}3.2409699419 & -1.5373831776 & -0.4986107603 \\
-0.9692436363 & \phantom{-}1.8759675015 & \phantom{-}0.0415550574 \\
\phantom{-}0.0556300797 & -0.2039769589 & \phantom{-}1.0569715142
\end{bmatrix}
$$

$$
M_{\text{sRGB}\to\text{XYZ}} =
\begin{bmatrix}
0.4123907993 & 0.3575843394 & 0.1804807884 \\
0.2126390059 & 0.7151686788 & 0.0721923154 \\
0.0193308187 & 0.1191947798 & 0.9505321522
\end{bmatrix}
$$

The middle row of $M_{\text{sRGB}\to\text{XYZ}}$ is the **luminance weights**
$(0.2126, 0.7152, 0.0722)$ — used directly for relative luminance Y.

### Display P3 ↔ XYZ-D65 (DCI-P3 primaries, D65 white, SMPTE EG 432-1)

$$
M_{\text{XYZ}\to\text{P3}} =
\begin{bmatrix}
\phantom{-}2.4934969119 & -0.9313836179 & -0.4027107845 \\
-0.8294889696 & \phantom{-}1.7626640603 & \phantom{-}0.0236246858 \\
\phantom{-}0.0358458302 & -0.0761723893 & \phantom{-}0.9568845240
\end{bmatrix}
$$

$$
M_{\text{P3}\to\text{XYZ}} =
\begin{bmatrix}
0.4865709486 & 0.2656676932 & 0.1982172852 \\
0.2289745641 & 0.6917385241 & 0.0792869117 \\
0.0000000000 & 0.0451133819 & 1.0439443689
\end{bmatrix}
$$

The bottom-left zero is exact: DCI-P3 red has $z = 0$ chromaticity, so its
contribution to the Z channel is exactly zero.

### Rec.2020 ↔ XYZ-D65 (BT.2020)

$$
M_{\text{XYZ}\to\text{Rec.2020}} =
\begin{bmatrix}
\phantom{-}1.7166511880 & -0.3556707838 & -0.2533662814 \\
-0.6666843518 & \phantom{-}1.6164812366 & \phantom{-}0.0157685458 \\
\phantom{-}0.0176398574 & -0.0427706133 & \phantom{-}0.9421031212
\end{bmatrix}
$$

$$
M_{\text{Rec.2020}\to\text{XYZ}} =
\begin{bmatrix}
0.6369580483 & 0.1446169036 & 0.1688809752 \\
0.2627002120 & 0.6779980715 & 0.0593017165 \\
0.0000000000 & 0.0280726930 & 1.0609850577
\end{bmatrix}
$$

Same as P3: red primary has $z = 0$.

---

## Implementation

Canonical TypeScript per gamut:

- [`src/spaces/srgb.ts`](../../../../color-science-project-files/src/spaces/srgb.ts) — Linear sRGB ↔ XYZ_D65
- [`src/spaces/p3.ts`](../../../../color-science-project-files/src/spaces/p3.ts) — Linear Display P3 ↔ XYZ_D65
- [`src/spaces/rec2020.ts`](../../../../color-science-project-files/src/spaces/rec2020.ts) — Linear Rec.2020 ↔ XYZ_D65
- [`src/spaces/xyz.ts`](../../../../color-science-project-files/src/spaces/xyz.ts) — XYZ identity (registry uniformity)

Each module exports `toXYZ`, `fromXYZ`, the forward + inverse matrix as
`Matrix3x3` constants, and `testVectors`. All matrix multiplications use
`mulMat3Vec3` from `src/types.ts`.

```ts
// src/spaces/srgb.ts
export const M_SRGB_TO_XYZ: Matrix3x3 = [
  [0.4123907993, 0.3575843394, 0.1804807884],
  [0.2126390059, 0.7151686788, 0.0721923154],
  [0.0193308187, 0.1191947798, 0.9505321522],
];

export function toXYZ(c: LinearSRGB): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_SRGB_TO_XYZ, c);
  return xyz(X, Y, Z);
}
```

**These modules handle LINEAR RGB only.** Gamma encoding lives in
[`src/transfer/`](../../../../color-science-project-files/src/transfer/). The full pipeline from encoded sRGB to
XYZ is `srgb.toXYZ(srgbTransfer.decode(encoded))`.

---

## Edge cases

- **Wide-gamut content in narrow-gamut encoding**: P3 → sRGB conversion produces
  linear RGB values outside $[0, 1]$ for colors that don't fit. The matrix math
  is correct; the calling code decides whether to clip, map, or accept.
- **D50 vs D65 confusion**: ICC profiles often use D50. Mixing D50-based
  matrices (CIELAB original definition) with D65-based matrices (display
  ecosystem) produces ~5% color errors. Always know which white point your
  matrix is defined at.
- **Source precision**: some references publish matrices with 4-6 decimal
  digits. The 10-digit values above (from W3C CSS Color 4) round-trip to
  better than $10^{-9}$. Lower-precision matrices accumulate ~$10^{-4}$ error
  per round trip.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/{srgb,p3,rec2020}.ts` — branded types, exact W3C matrices. |
| **Culori** | `mode_xyz65`, `mode_xyz50` and `mode_p3`, `mode_rec2020` registered globally. |
| **Color.js** | `ColorSpace.get('xyz-d65')`, `ColorSpace.get('display-p3')`, etc. |
| **Bruce Lindbloom** | <http://www.brucelindbloom.com/Eqn_RGB_XYZ_Matrix.html> — derivation calculator and matrix tables for every common gamut. |

---

## Primary sources

- **IEC 61966-2-1:1999** — sRGB primaries + transfer.
- **ITU-R BT.709-6** (2015) — Rec.709 (same primaries as sRGB).
- **SMPTE EG 432-1** (2010) — DCI-P3 primaries; Display P3 = DCI-P3 with D65 + sRGB transfer.
- **ITU-R BT.2020-2** (2015) — Rec.2020 primaries.
- **W3C CSS Color 4** — Web normative high-precision matrices: <https://www.w3.org/TR/css-color-4/#color-conversion-code>
