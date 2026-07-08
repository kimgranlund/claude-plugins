# Color Difference (ΔE) — Math

ΔE ("Delta E") is the scalar distance between two colors in a perceptual space.
**Five formulas worth knowing**, each calibrated for a different use case. Pick
based on your task — using the wrong ΔE silently produces bad results.

---

## TL;DR

| Formula | Year | Space | When to use |
|---|---|---|---|
| **ΔE_ok** | 2020 | OKLab | **Modern default** — design tokens, palette work, gradients |
| **ΔE2000** | 2001 | CIELAB | Gold standard for color science, print, textile |
| **ΔE94** | 1994 | CIELAB | Legacy graphic-arts; mostly superseded by ΔE2000 |
| **ΔE76** | 1976 | CIELAB | Obsolete but ubiquitous (Euclidean Lab) |
| **HyAB** | 2020 | CIELAB | Robust for very large color differences |

JND (just noticeable difference) approximations:
- ΔE76 ≈ 2.3
- ΔE2000 ≈ 1.0
- ΔE_ok ≈ 0.02

---

## Natural-language description

Why does ΔE need five variants? Because **perceptual uniformity is hard.**
CIELAB (1976) was designed to be uniform — equal Euclidean distances → equal
perceived differences. It mostly is, but not perfectly: differences in the
blue-purple region appear larger than equivalent distances elsewhere, chroma
weights vary with lightness, etc.

Each successive ΔE formula patches the same underlying space (CIELAB) with
correction terms. ΔE94 added simple lightness-weighted scaling. ΔE2000 added
rotational corrections for the blue-purple problem and chroma-dependent
weights. The math grew accordingly.

OKLab (2020) takes the opposite approach: **fix the space, not the metric.**
OKLab's coordinates are perceptually uniform enough that plain Euclidean
distance (ΔE_ok) is competitive with ΔE2000 for most tasks — and it's an order
of magnitude faster to compute.

**Recommendation for new work**: ΔE_ok. For interop with established
pipelines: ΔE2000. Avoid ΔE76 unless you specifically need to match legacy
behavior.

---

## Formulas

### ΔE76 (CIE 1976) — Euclidean in CIELAB

$$
\Delta E_{76} = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}
$$

### ΔE94 (CIE 1994) — weighted CIELAB

Constants for graphic-arts ($k_L = 1$, $K_1 = 0.045$, $K_2 = 0.015$):

$$
\begin{aligned}
C_i^* &= \sqrt{(a_i^*)^2 + (b_i^*)^2} \\
\Delta C^* &= C_1^* - C_2^* \\
\Delta H^* &= \sqrt{(\Delta a^*)^2 + (\Delta b^*)^2 - (\Delta C^*)^2} \\
S_L &= 1, \quad S_C = 1 + K_1 C_1^*, \quad S_H = 1 + K_2 C_1^* \\
\Delta E_{94} &= \sqrt{\left(\tfrac{\Delta L^*}{k_L S_L}\right)^2
                       + \left(\tfrac{\Delta C^*}{S_C}\right)^2
                       + \left(\tfrac{\Delta H^*}{S_H}\right)^2}
\end{aligned}
$$

For textiles: $k_L = 2$, $K_1 = 0.048$, $K_2 = 0.014$.

### ΔE2000 (CIE 2001) — gold standard

The full formula has 19 sub-steps; see [Sharma/Wu/Dalal 2005](#primary-sources)
for the canonical derivation. Key ingredients:

1. **Chroma rotation $G$**: corrects the "neutral colors look chromatic in CIELAB" bias.

$$
\bar{C} = \tfrac{1}{2}(C_1^* + C_2^*), \qquad
G = \tfrac{1}{2}\left(1 - \sqrt{\tfrac{\bar{C}^7}{\bar{C}^7 + 25^7}}\right)
$$

2. **Rotated $a'$**: $a'_i = (1 + G) \cdot a_i^*$, with $C'_i$ and $h'_i$ recomputed from $(a'_i, b_i^*)$.

3. **Differences**: $\Delta L' = L_2 - L_1$, $\Delta C' = C'_2 - C'_1$,
   $\Delta H' = 2 \sqrt{C'_1 C'_2} \sin(\Delta h' / 2)$.

4. **Lightness weighting**:

$$
S_L = 1 + \frac{0.015 (\bar{L} - 50)^2}{\sqrt{20 + (\bar{L} - 50)^2}}, \quad
S_C = 1 + 0.045 \bar{C'}, \quad
S_H = 1 + 0.015 \bar{C'} T
$$

5. **Hue weighting** $T$ (cosine combination) and **rotation term** $R_T$ (corrects blue-purple).

6. **Final**:

$$
\Delta E_{00} = \sqrt{
  \left(\tfrac{\Delta L'}{k_L S_L}\right)^2 +
  \left(\tfrac{\Delta C'}{k_C S_C}\right)^2 +
  \left(\tfrac{\Delta H'}{k_H S_H}\right)^2 +
  R_T \cdot \tfrac{\Delta C'}{k_C S_C} \cdot \tfrac{\Delta H'}{k_H S_H}
}
$$

### ΔE_ok (Ottosson 2020) — Euclidean in OKLab

$$
\Delta E_{ok} = \sqrt{(\Delta L)^2 + (\Delta a)^2 + (\Delta b)^2}
$$

Same form as ΔE76, but in OKLab (perceptually uniform) instead of CIELAB.

### HyAB (Abasi et al. 2020) — Hybrid for large differences

$$
\text{HyAB} = \sqrt{(\Delta L^*)^2} + |\Delta a^*| + |\Delta b^*|
$$

Euclidean in $L^*$ + city-block in $(a^*, b^*)$. More robust than ΔE76 for
large color differences where the Euclidean assumption breaks down.

---

## Implementation

Canonical TypeScript: [`src/metrics/deltaE.ts`](../../../../color-science-project-files/src/metrics/deltaE.ts).

Exports `deltaE76`, `deltaE94(a, b, textiles?)`, `deltaE2000(a, b, kL?, kC?, kH?)`,
`deltaEOK`, and `hyAB`. Each takes branded `CIELAB_D65` (or `OKLab` for ΔE_ok).

```ts
export function deltaEOK(a: OKLab, b: OKLab): number {
  const dL = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return Math.sqrt(dL * dL + dA * dA + dB * dB);
}
```

ΔE2000 is the longest at ~70 lines; the implementation follows Sharma's
published pseudocode exactly. Test vectors include pairs 1 and 2 from
Sharma/Wu/Dalal 2005 Table 1 (the canonical numerical-correctness check).

---

## Edge cases

- **Hue at chroma=0**: ΔE2000 has special-case branches for when $C_1' = 0$ or
  $C_2' = 0$ (hue is undefined for grayscale). The implementation handles these
  explicitly; without the branches you get `NaN` from `atan2(0, 0)` ambiguity.
- **Lab D50 vs D65 mismatch**: ΔE76/94/2000 are typically computed in CIELAB,
  but CIELAB exists in both D50 and D65 variants. Mixing them produces wrong
  answers. This skill's modules use `CIELAB_D65`.
- **OKLab range mismatch**: OKLab's $L$ axis is roughly $[0, 1]$ while
  CIELAB's $L^*$ axis is $[0, 100]$. ΔE_ok values are correspondingly ~100×
  smaller than equivalent ΔE_76 values.
- **Negative components**: out-of-gamut colors can have negative $a^*$ or
  negative OKLab components. All five formulas handle this correctly (only
  squares and absolute values are used).

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/metrics/deltaE.ts` — all five, branded-typed, with Sharma test vectors. |
| **Culori** | `differenceCie76`, `differenceCie94`, `differenceCiede2000`, `differenceEuclidean`. |
| **Color.js** | `Color.deltaE(a, b, method)` where method is `'76'`, `'94'`, `'2000'`, `'OK'`, `'CMC'`, etc. |
| **chroma.js** | `chroma.deltaE(a, b)` (CIE2000). |
| **delta-e** (npm) | Lightweight ΔE2000 + others. |

---

## Primary sources

- **CIE 015:2018** — Colorimetry, 4th edition. CIELAB and original ΔE definition.
- **CIE 116:1995** — CIE94 color-difference formula.
- **CIE 142:2001** — CIEDE2000 color-difference formula.
- **Sharma, Wu, Dalal, "The CIEDE2000 Color-Difference Formula" (2005)** —
  reference implementation and numerical test data:
  <http://www2.ece.rochester.edu/~gsharma/ciede2000/>
- **Björn Ottosson 2020** — OKLab (and ΔE_ok by extension):
  <https://bottosson.github.io/posts/oklab/>
- **Abasi, Amani Tehran, Fairchild "Distance metrics for very large color differences" (2020)** —
  HyAB definition.
