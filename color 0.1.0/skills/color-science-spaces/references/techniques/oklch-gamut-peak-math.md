# OKLCH Gamut Boundary: Peak Lightness and Peak Chroma Math

The mathematical derivation for the boundary of a target RGB gamut (sRGB, Display P3,
Rec.2020) expressed in OKLCH coordinates, and the two practical algorithms a design
system needs: **peak L at fixed (C, h)** and **peak C at fixed (L, h)**.

---

## TL;DR

- There is **no closed-form** $L_{\text{peak}}(C)$ in OKLCH unless you also fix hue, or
  define "peak" as "maximum across all hues."
- Reason: the gamut boundary is the unit RGB cube, which becomes a non-convex,
  non-circular shape after the nonlinear `OKLab → LMS' → LMS → XYZ → linear-RGB`
  transform.
- For fixed $(C, h)$, each linear-RGB channel is a **cubic polynomial in $L$**. The
  envelope is solved channel-by-channel against $[0, 1]$.
- Production code: **binary search** (32 iterations, robust) or **analytic cubic root
  solving** (faster, more delicate). For design systems, use binary search.

---

## The OKLCH → linear-RGB pipeline

Five steps, one nonlinearity:

$$
(L, C, h) \xrightarrow{\text{polar}\to\text{cartesian}}
(L, a, b) \xrightarrow{M_2^{-1}}
\text{LMS}' \xrightarrow{(\cdot)^3}
\text{LMS} \xrightarrow{M_1^{-1}}
\text{XYZ}_{D65} \xrightarrow{M_{\text{XYZ}\to G}}
\text{lin-RGB}_G
$$

The cubing step is the only nonlinearity. Everything else is a linear matrix product.

### Step 1: OKLCH → OKLab

$$
\begin{aligned}
a &= C \cos h \\
b &= C \sin h
\end{aligned}
$$

### Step 2: OKLab → LMS′ (Ottosson's $M_2^{-1}$)

LMS′ is the cube-root-compressed LMS space. OKLab places $L = L'_M$ projected onto
the achromatic axis, with $(a, b)$ encoding red-green and blue-yellow opponency.

$$
\text{LMS}' = M_2^{-1}
\begin{bmatrix} L \\ a \\ b \end{bmatrix},
\quad
M_2^{-1} =
\begin{bmatrix}
1.0000000000 & \phantom{-}0.3963377774 & \phantom{-}0.2158037573 \\
1.0000000000 & -0.1055613458 & -0.0638541728 \\
1.0000000000 & -0.0894841775 & -1.2914855480
\end{bmatrix}
$$

### Step 3: LMS′ → LMS (component-wise cubing)

$$
\text{LMS} = \text{LMS}'^{\circ 3} =
\begin{bmatrix} (l')^3 \\ (m')^3 \\ (s')^3 \end{bmatrix}
$$

This is the cubic that breaks any hope of a closed-form gamut boundary.

### Step 4: LMS → XYZ (D65) — Ottosson's $M_1^{-1}$

$$
M_1^{-1} =
\begin{bmatrix}
\phantom{-}1.2270138511 & -0.5577999807 & \phantom{-}0.2812561490 \\
-0.0405801784 & \phantom{-}1.1122568696 & -0.0716766787 \\
-0.0763812845 & -0.4214819784 & \phantom{-}1.5861632204
\end{bmatrix}
$$

### Step 5: XYZ → linear RGB (gamut-specific)

**sRGB (D65):**

$$
M_{\text{XYZ}\to\text{sRGB}} =
\begin{bmatrix}
\phantom{-}3.24096994 & -1.53738318 & -0.49861076 \\
-0.96924364 & \phantom{-}1.87596750 & \phantom{-}0.04155506 \\
\phantom{-}0.05563008 & -0.20397696 & \phantom{-}1.05697151
\end{bmatrix}
$$

**Display P3 (D65):**

$$
M_{\text{XYZ}\to\text{P3}} =
\begin{bmatrix}
\phantom{-}2.49349691 & -0.93138362 & -0.40271078 \\
-0.82948897 & \phantom{-}1.76266406 & \phantom{-}0.02362469 \\
\phantom{-}0.03584583 & -0.07617239 & \phantom{-}0.95688452
\end{bmatrix}
$$

**Rec.2020 (D65):**

$$
M_{\text{XYZ}\to\text{rec2020}} =
\begin{bmatrix}
\phantom{-}1.71665119 & -0.35567078 & -0.25336628 \\
-0.66668435 & \phantom{-}1.61648124 & \phantom{-}0.01576855 \\
\phantom{-}0.01763986 & -0.04277061 & \phantom{-}0.94210312
\end{bmatrix}
$$

---

## Gamut membership condition

For a target gamut $G$:

$$
\mathbf{rgb}_G(L, C, h) = M_{\text{XYZ}\to G} \, M_1^{-1}
\left(M_2^{-1}
\begin{bmatrix} L \\ C\cos h \\ C\sin h \end{bmatrix}
\right)^{\!\circ 3}
$$

A color is in-gamut iff every linear-RGB channel lies in $[0, 1]$:

$$
0 \le \mathbf{rgb}_G(L, C, h)_k \le 1 \quad \forall k \in \{R, G, B\}
$$

> **Gamma encoding aside.** Gamut membership is tested on the **linear** RGB output.
> Display gamma encoding (sRGB transfer, P3 transfer) is applied afterward to produce
> the storable color. Test in linear space; transfer for display.

---

## Why each channel is a cubic in $L$

Fix $(C, h)$. Then $a = C \cos h$ and $b = C \sin h$ are constants. Define:

$$
\begin{bmatrix} l' \\ m' \\ s' \end{bmatrix} = M_2^{-1}
\begin{bmatrix} L \\ a \\ b \end{bmatrix} =
\begin{bmatrix} L + \alpha_1 \\ L + \alpha_2 \\ L + \alpha_3 \end{bmatrix}
$$

(because the first column of $M_2^{-1}$ is all 1s — a defining property of OKLab).
The $\alpha_i$ depend only on $(a, b)$, i.e., on $(C, h)$.

After cubing: LMS components are $(L + \alpha_i)^3$ — cubic in $L$.

After applying $M_1^{-1}$ and $M_{\text{XYZ}\to G}$ (both linear), each linear-RGB
channel is a **linear combination of three cubics in $L$**, which is itself a cubic
in $L$:

$$
R_G(L) = c_3 L^3 + c_2 L^2 + c_1 L + c_0
$$

The coefficients $c_0, c_1, c_2, c_3$ are polynomials in $(a, b)$ and depend on the
gamut matrix $M_{\text{XYZ}\to G}$.

**Implication.** The gamut envelope in $L$ for fixed $(C, h)$ is determined by six
cubic root-finding problems:
$R_G = 0$, $R_G = 1$, $G_G = 0$, $G_G = 1$, $B_G = 0$, $B_G = 1$.

---

## Algorithm 1: $L_{\text{peak}}(C, h)$ — peak lightness at fixed chroma and hue

The largest $L \in [0, 1]$ such that all three linear-RGB channels remain in $[0, 1]$.

### Binary search (recommended for production)

Robust, branch-free, converges in ~32 iterations to floating-point precision:

```js
function peakL(C, h, toLinearRGB, iterations = 32) {
  let lo = 0, hi = 1;
  for (let i = 0; i < iterations; i++) {
    const mid = (lo + hi) / 2;
    const [r, g, b] = toLinearRGB(mid, C, h);
    const inGamut =
      r >= 0 && r <= 1 &&
      g >= 0 && g <= 1 &&
      b >= 0 && b <= 1;
    if (inGamut) lo = mid;
    else hi = mid;
  }
  return lo;
}
```

This assumes the in-gamut set is **convex along the L axis at fixed (C, h)** — which
holds for sRGB, Display P3, and Rec.2020 because the cube is convex and the
OKLCH→linear-RGB map is monotonic in $L$ at fixed $(C, h)$.

### Analytic (faster, more delicate)

For each of the six boundary conditions ($R_G = 0, R_G = 1, ...$), solve the cubic
$c_3 L^3 + c_2 L^2 + c_1 L + c_0 = \text{boundary}$ via Cardano's formula or the
trigonometric method, keep real roots in $[0, 1]$, then take the minimum upper
boundary across all six channel-constraint cubics.

Faster (~6 cubic solves vs. 32 iterations), but precision near the cube edges is
fragile. Use only if you've profiled binary search as a bottleneck.

---

## Algorithm 2: $C_{\text{peak}}(L, h)$ — peak chroma at fixed lightness and hue

**More useful than $L_{\text{peak}}$ for design tokens**, because token systems
typically fix lightness (per step in a ramp) and want the maximum achievable chroma
at each hue.

Same structure — binary search on $C$:

```js
function peakC(L, h, toLinearRGB, iterations = 32, cMax = 0.4) {
  let lo = 0, hi = cMax;
  for (let i = 0; i < iterations; i++) {
    const mid = (lo + hi) / 2;
    const [r, g, b] = toLinearRGB(L, mid, h);
    const inGamut =
      r >= 0 && r <= 1 &&
      g >= 0 && g <= 1 &&
      b >= 0 && b <= 1;
    if (inGamut) lo = mid;
    else hi = mid;
  }
  return lo;
}
```

Set `cMax` larger than the gamut envelope (0.4 covers sRGB and P3; use 0.5 for
Rec.2020). The binary search converges to the actual gamut boundary regardless.

Ottosson has a published analytic algorithm for the **cusp point** $(L_\text{cusp},
C_\text{cusp})$ at a given hue — the maximum-chroma point of the gamut slice. From
the cusp, you can compute $C_\text{peak}(L, h)$ in closed form per hue. See his
"Gamut clipping" article (link in Primary Sources).

---

## Algorithm 3: Peak across all hues

$$
L_{\text{peak}}(C) = \max_{h \in [0, 2\pi)} L_{\text{peak}}(C, h)
$$

No closed form. Numerical:

```js
function peakLOverHue(C, toLinearRGB, hueSteps = 720) {
  let best = 0;
  let bestHue = 0;
  for (let i = 0; i < hueSteps; i++) {
    const h = (i / hueSteps) * Math.PI * 2;
    const L = peakL(C, h, toLinearRGB);
    if (L > best) {
      best = L;
      bestHue = h;
    }
  }
  return { L: best, h: bestHue };
}
```

720 hue steps (0.5° resolution) is enough for visual purposes. Use 3600 (0.1°) for
publication-quality envelope plots.

> **Design-system caveat.** $L_{\text{peak}}(C)$ across all hues is rarely the right
> primitive for a token system, because color families preserve hue. Use
> $L_{\text{peak}}(C, h)$ per family. The all-hue version is for envelope analysis
> (e.g., "what's the maximum chroma the gamut supports anywhere?").

---

## Implementation

Canonical TypeScript: [`src/gamut/oklch-peak.ts`](../../../../color-science-project-files/src/gamut/oklch-peak.ts).
Exports `peakL(C, h, toRGB)`, `peakC(L, h, toRGB)`, `peakLOverHue(C, toRGB)`, and
gamut-specific convenience wrappers (`peakL_sRGB`, `peakC_P3`, `peakL_Rec2020`,
etc.). All three XYZ → linear-RGB matrices are exported from the same module.

Composes with `src/spaces/oklab.ts` for the OKLCH → OKLab → XYZ leg of the
pipeline. See [`ARCHITECTURE.md`](../../../../color-science-project-files/ARCHITECTURE.md) for the
bidirectionality contract every space module satisfies.

## Production implementations

| Library | Notes |
|---|---|
| **This skill** | `src/gamut/oklch-peak.ts` — branded-typed, bidirectional, test-vector-verified. |
| **Culori** | `oklch` ↔ `rgb`/`p3`/`rec2020` with `inGamut`/`clampGamut`. Robust, well-tested. |
| **@texel/color** | 5–125× faster than Color.js. Minimal API. Use for real-time pickers. |
| **Color.js** (W3C) | Reference implementation of CSS Color 4. Slow but spec-correct. |
| **Ottosson's reference C** | https://bottosson.github.io/posts/gamutclipping/ — includes the cusp-based fast path. |

---

## Edge cases and numerical notes

- **Achromatic ($C = 0$):** every $L \in [0, 1]$ is in-gamut. $L_\text{peak}(0, h) = 1$.
- **Beyond gamut envelope:** if $C$ is larger than the maximum chroma at any hue (e.g.,
  $C = 0.5$ in sRGB), the binary search returns `lo = 0` because no $L > 0$ is
  in-gamut. Handle as "out of gamut at every $L$."
- **Floating-point cube precision:** the cubing step at very small $|l'|$ (near the
  black point) can lose precision. Most implementations accept this — sub-perceptual
  error at $L \approx 0$.
- **Hue wrapping:** ensure $h$ is normalized to $[0, 2\pi)$ before computing trig.
  OKLCH hues outside this range are valid but $\cos$/$\sin$ identities still hold.

---

## Primary sources

- **Björn Ottosson, "A perceptual color space for image processing" (2020)** —
  the original OKLab paper. $M_1$ and $M_2$ matrices defined here.
  <https://bottosson.github.io/posts/oklab/>

- **Björn Ottosson, "Gamut clipping" (2021)** — the cusp algorithm and fast gamut
  mapping. Includes reference C code for $C_\text{peak}(L, h)$.
  <https://bottosson.github.io/posts/gamutclipping/>

- **W3C CSS Color Module Level 4** — normative definition of OKLab/OKLCH in CSS.
  <https://www.w3.org/TR/css-color-4/#ok-lab>

- **IEC 61966-2-1** — sRGB primaries and transfer function (referenced via the
  XYZ→sRGB matrix above).

- **SMPTE EG 432-1 / SMPTE RP 431-2** — DCI-P3 primaries; Display P3 = DCI-P3 with
  D65 and sRGB transfer.

- **ITU-R BT.2020** — Rec.2020 primaries.

- **Bruce Lindbloom — Color math reference** — all XYZ↔RGB matrices for major
  working spaces (cross-reference). See `brucelindbloom-color-math.md`.

---

## When to reach for this file

- Building a token ramp from a brand anchor: use `peakC(L, h, ...)` per step.
- Verifying a palette stays in-gamut across themes: test `inGamut` at every
  (theme × scheme × contrast) combination.
- Implementing a gamut-aware color picker: combine `peakC` (chroma slider clamp)
  with `peakL` (lightness slider clamp) at the user's current hue.
- Sanity-checking a third-party OKLCH→RGB implementation: the matrices and the
  cubic-in-$L$ property are the easiest things to misimplement.
