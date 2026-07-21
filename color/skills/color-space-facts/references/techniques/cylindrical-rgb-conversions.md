# HSL & HSV ↔ RGB — Math

HSL (Hue / Saturation / Lightness) and HSV (Hue / Saturation / Value) are
**non-perceptual cylindrical reparameterizations of gamma-encoded sRGB**. They
share the hue computation but differ in their second and third axes.

Both are common in CSS, color pickers, and design tools. Both are misleading
for serious color work. **Prefer OKLCH or OKHSL for perceptual cylindrical
color.**

---

## TL;DR

- **HSL** uses lightness (the average of max and min channels) as the L axis.
- **HSV** uses value (the max channel) as the V axis.
- Both compute hue identically: from the sector of (R, G, B) sorted order.
- Both operate on **gamma-encoded** sRGB, not linear sRGB. This is the CSS
  convention.
- Neither is perceptually uniform — fully saturated yellow `hsl(60, 100%, 50%)`
  and fully saturated blue `hsl(240, 100%, 50%)` have the same L=50% but
  vastly different perceived brightness.

---

## Natural-language description

### HSL geometry

The HSL cylinder embeds the RGB cube along its grayscale diagonal. The three
black/white corners of the cube collapse to the cylinder's axis; the six
saturated corners (R, Y, G, C, B, M) form a regular hexagon at the equator.

- **Hue (H)** in $[0, 360)°$ — angle around the cylinder. Red at 0°, yellow at
  60°, green at 120°, cyan at 180°, blue at 240°, magenta at 300°.
- **Saturation (S)** in $[0, 1]$ — distance from the lightness axis. 0 is
  grayscale; 1 touches the hue hexagon's edge.
- **Lightness (L)** in $[0, 1]$ — height on the cylinder. 0 is pure black,
  1 is pure white, 0.5 is the equator (fully saturated colors live here).

### HSV geometry

Same hue, different L-axis. HSV uses the max channel directly:

- **Value (V)** in $[0, 1]$ — the brightest channel. Pure red `rgb(1,0,0)` has
  V=1, but in HSL it has L=0.5.

HSV's cylinder is "filled" at V=1 (the entire hexagon is reachable), while
HSL's "double cone" is widest at L=0.5 and shrinks to points at L=0 and L=1.

### Why neither is perceptual

The hue hexagon's geometry doesn't match perception:
- Yellow at 60° and blue at 240° are 180° apart geometrically, but they have
  very different perceived brightnesses (yellow ≫ blue at full saturation).
- Saturation distance doesn't match perceived chroma — colors at S=1 can look
  vastly different in "vividness."
- Equal-step lightness ramps look very uneven across hues.

**For modern UI/design work, use OKLCH** (perceptual polar OKLab) or **OKHSL**
(Ottosson's perceptual HSL with gamut cusp shaping).

---

## Formulas

### Common hue computation (HSL and HSV)

Given encoded sRGB $(R, G, B)$ in $[0, 1]$:

$$
M = \max(R, G, B), \quad m = \min(R, G, B), \quad d = M - m
$$

Hue depends on which channel is max:

$$
H' =
\begin{cases}
0 & \text{if } d = 0 \\
\dfrac{G - B}{d} \bmod 6 & \text{if } M = R \\
\dfrac{B - R}{d} + 2 & \text{if } M = G \\
\dfrac{R - G}{d} + 4 & \text{if } M = B
\end{cases}
\qquad H = 60° \cdot H'
$$

Normalize $H$ to $[0, 360)$ by adding $360$ if negative.

### HSL ← RGB

$$
L = \frac{M + m}{2}, \qquad
S =
\begin{cases}
0 & \text{if } d = 0 \\
\dfrac{d}{1 - |2L - 1|} & \text{otherwise}
\end{cases}
$$

### HSV ← RGB

$$
V = M, \qquad
S =
\begin{cases}
0 & \text{if } M = 0 \\
\dfrac{d}{M} & \text{otherwise}
\end{cases}
$$

### RGB ← HSL

Let $C = (1 - |2L - 1|) \cdot S$ (chroma), $H' = H / 60°$, $X = C \cdot (1 - |H' \bmod 2 - 1|)$.

$$
(R', G', B') =
\begin{cases}
(C, X, 0) & 0 \le H' < 1 \\
(X, C, 0) & 1 \le H' < 2 \\
(0, C, X) & 2 \le H' < 3 \\
(0, X, C) & 3 \le H' < 4 \\
(X, 0, C) & 4 \le H' < 5 \\
(C, 0, X) & 5 \le H' < 6
\end{cases}
$$

Then offset to the lightness:

$$
m = L - C / 2, \qquad (R, G, B) = (R' + m, G' + m, B' + m)
$$

### RGB ← HSV

Same sector logic, but with $C = V \cdot S$ and $m = V - C$.

---

## Implementation

Canonical TypeScript: [`src/spaces/hsl.ts`](../../../../color-science-project-files/src/spaces/hsl.ts),
[`src/spaces/hsv.ts`](../../../../color-science-project-files/src/spaces/hsv.ts).

Both modules compose with `src/transfer/srgb.ts` and `src/spaces/srgb.ts` to
provide `toXYZ` / `fromXYZ` through the XYZ-D65 hub:

```ts
// HSL → XYZ pipeline
export function toXYZ(hsl: HSL): XYZ_D65 {
  const encoded = toEncodedSRGB(hsl);              // cylindrical → encoded sRGB
  const linear = srgbTransfer.decode(encoded);     // gamma decode
  return srgbSpace.toXYZ(linear);                  // linear → XYZ
}
```

This three-step composition is the canonical "non-RGB-derived space → XYZ"
pattern. Any future cylindrical-or-otherwise-derived space follows the same
shape: convert to its anchor RGB, transfer if encoded, then matrix to XYZ.

---

## Edge cases

- **Achromatic round-trip**: when $S = 0$, hue is mathematically indeterminate.
  A round-trip XYZ → HSL → XYZ at the white point may return arbitrary hue
  values from float noise. This is not a bug — it's the cylindrical
  parameterization's inherent property. The achromatic test vectors in
  `src/spaces/hsl.ts` are intentionally chromatic to avoid this.
- **Negative or out-of-range input**: HSL/HSV formulas assume $(R, G, B) \in [0, 1]$.
  Out-of-range encoded sRGB (e.g., wide-gamut content represented in sRGB) will
  produce undefined behavior. Either clip first or convert via OKLCH instead.
- **CSS vs. native HSL**: CSS uses percentages for S and L (`hsl(120, 50%, 50%)`).
  These modules use the $[0, 1]$ range. Divide CSS percentages by 100.
- **Linear vs. encoded HSL**: Some applications (mostly graphics rendering)
  apply HSL to *linear* sRGB. CSS and most design tools apply it to *encoded*
  sRGB. This skill follows the CSS convention; linear-HSL is a separate
  derivative we don't implement.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/{hsl,hsv}.ts` — encoded sRGB convention, branded types. |
| **Culori** | `mode_hsl`, `mode_hsv` registered globally. |
| **Color.js** | `ColorSpace.get('hsl')`, `ColorSpace.get('hsv')`. |
| **chroma.js** | `chroma.hsl(h, s, l)` constructor. |

For perceptual cylindrical color, prefer:

- **OKHSL** (Ottosson) — `src/spaces/okhsl.ts`
- **OKLCH** (Ottosson polar OKLab) — `src/spaces/oklch.ts`
- **CIELCH** (CIELAB polar) — `src/spaces/cielch.ts`
- **HSLuv** (CIELUV-normalized) — not yet implemented in this skill

---

## Primary sources

- **A. R. Smith, "Color Gamut Transform Pairs"** (1978) — original HSV definition.
- **G. H. Joblove and D. Greenberg, "Color spaces for computer graphics"**
  (1978) — HSL definition.
- **W3C CSS Color 4** — <https://www.w3.org/TR/css-color-4/#the-hsl-notation> —
  CSS HSL specification with the modern formula.
- **Wikipedia — HSL and HSV** — <https://en.wikipedia.org/wiki/HSL_and_HSV> —
  approachable summary with diagrams.
