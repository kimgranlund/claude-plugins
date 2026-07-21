# Gamma Transfer Functions — Math

The non-linear functions that convert linear light (radiometrically additive) to
display-encoded signal (storage / transmission). Every gamut-specific RGB space
has one. **Never mix linear and encoded values** — every blending, contrast, or
color-mixing operation must happen in linear space.

---

## TL;DR

- **sRGB and Display P3 share** a piecewise transfer: linear segment near zero,
  then $1.055 \cdot L^{1/2.4} - 0.055$.
- **Rec.2020 and Rec.709 share** a different piecewise transfer (ITU-R BT.2020):
  $4.5 L$ near zero, then $1.099 L^{0.45} - 0.099$ (slight constant variations exist).
- **PQ (BT.2100)** is an absolute HDR transfer based on Barten's contrast threshold,
  normalized so $1.0$ = $10{,}000$ nits.
- **HLG (BT.2100)** is a hybrid: $\sqrt{3L}$ near zero, log-gamma above.

All transfers in this skill are **sign-preserving** to handle out-of-range values
(e.g., wide-gamut content represented in a narrower encoding's space).

---

## Natural-language description

A transfer function maps between two domains:

- **Scene-referred / linear light**: physically additive. Doubling the value
  doubles the luminance. This is where light arithmetic happens (alpha compositing,
  blending, antialiasing, color mixing).

- **Display-referred / encoded**: perceptually distributed. Roughly uniform
  perceptual steps per code value. This is what's stored in 8-bit / 10-bit /
  12-bit files and transmitted to displays.

Display gamma exists because human vision is approximately logarithmic in
luminance. Encoding linearly wastes most code values on dark regions where the
eye is sensitive; encoding via a power function distributes resolution where the
eye needs it.

**Mixing the two destroys color math.** A mid-gradient that looks dark, a CSS
`color-mix` that produces muddy intermediates, an antialiasing operation that
makes edges look fuzzy — all symptoms of arithmetic happening in encoded
(non-linear) space.

---

## Formulas

### sRGB / Display P3 (IEC 61966-2-1)

**Linear → encoded:**

$$
V =
\begin{cases}
12.92 \cdot L & \text{if } L \le 0.0031308 \\
1.055 \cdot L^{1/2.4} - 0.055 & \text{otherwise}
\end{cases}
$$

**Encoded → linear:**

$$
L =
\begin{cases}
V / 12.92 & \text{if } V \le 0.04045 \\
\left(\dfrac{V + 0.055}{1.055}\right)^{2.4} & \text{otherwise}
\end{cases}
$$

Display P3 uses this same transfer (only the primaries differ).

### Rec.2020 / Rec.709 (ITU-R BT.2020)

Let $\alpha = 1.09929682680944$ and $\beta = 0.018053968510807$.

**Linear → encoded (OETF):**

$$
V =
\begin{cases}
4.5 \cdot L & \text{if } L < \beta \\
\alpha \cdot L^{0.45} - (\alpha - 1) & \text{otherwise}
\end{cases}
$$

**Encoded → linear (inverse OETF):**

$$
L =
\begin{cases}
V / 4.5 & \text{if } V < 4.5\beta \\
\left(\dfrac{V + \alpha - 1}{\alpha}\right)^{1/0.45} & \text{otherwise}
\end{cases}
$$

Rec.709 uses the same form with slightly different rounding ($\alpha = 1.099$,
$\beta = 0.018$) — most implementations treat them as identical.

### PQ — Perceptual Quantizer (SMPTE ST 2084)

Constants:
$$
m_1 = \frac{2610}{16384}, \quad
m_2 = \frac{2523}{4096} \cdot 128, \quad
c_1 = \frac{3424}{4096}, \quad
c_2 = \frac{2413}{4096} \cdot 32, \quad
c_3 = \frac{2392}{4096} \cdot 32
$$

**Linear → encoded** ($L \in [0, 1]$ where $1 = 10{,}000$ nits):

$$
Y' = L^{m_1}, \qquad
V = \left(\frac{c_1 + c_2 Y'}{1 + c_3 Y'}\right)^{m_2}
$$

**Encoded → linear:**

$$
E' = V^{1/m_2}, \qquad
L = \left(\frac{\max(0, E' - c_1)}{c_2 - c_3 E'}\right)^{1/m_1}
$$

### HLG — Hybrid Log-Gamma (BT.2100)

Constants:
$$
a = 0.17883277, \quad b = 0.28466892, \quad c = 0.55991073
$$

**Linear → encoded:**

$$
V =
\begin{cases}
\sqrt{3 L} & \text{if } L \le 1/12 \\
a \ln(12 L - b) + c & \text{otherwise}
\end{cases}
$$

**Encoded → linear:**

$$
L =
\begin{cases}
V^2 / 3 & \text{if } V \le 0.5 \\
\dfrac{\exp((V - c)/a) + b}{12} & \text{otherwise}
\end{cases}
$$

---

## Implementation

Canonical TypeScript implementations:

- [`src/transfer/srgb.ts`](../../../../color-science-project-files/src/transfer/srgb.ts) — sRGB / Display P3
- [`src/transfer/rec2020.ts`](../../../../color-science-project-files/src/transfer/rec2020.ts) — Rec.2020 / Rec.709
- [`src/transfer/pq.ts`](../../../../color-science-project-files/src/transfer/pq.ts) — BT.2100 PQ + `encodeNits` / `decodeNits` helpers
- [`src/transfer/hlg.ts`](../../../../color-science-project-files/src/transfer/hlg.ts) — BT.2100 HLG

All four modules export the same shape: `encodeComponent` / `decodeComponent`
(scalar) and `encode` / `decode` (tuple-branded). They follow the
[ARCHITECTURE.md](../../../../color-science-project-files/ARCHITECTURE.md) bidirectionality contract.

Each module is sign-preserving for out-of-range values:

```ts
function encodeComponent(linear: number): number {
  const abs = Math.abs(linear);
  const sign = Math.sign(linear);
  if (abs <= 0.0031308) return sign * 12.92 * abs;
  return sign * (1.055 * Math.pow(abs, 1 / 2.4) - 0.055);
}
```

This matters when handling wide-gamut content (P3, Rec.2020) represented as
out-of-range sRGB values — naive `Math.pow` of a negative number returns NaN.

---

## Edge cases

- **Negative or out-of-range input**: sign-preserving formulas handle this
  cleanly. Some implementations clamp instead — flag this when porting.
- **Piecewise boundary precision**: at the exact boundary (e.g., $L = 0.0031308$
  for sRGB), the two branches must agree. The constants in IEC 61966-2-1 are
  defined so they do, within float precision.
- **Reciprocal pairs**: `decode(encode(x))` should be the identity within
  $\sim 10^{-7}$ for inputs in $[0, 1]$. Outside that range, expect more drift.
- **PQ underflow**: at very small encoded values, $c_2 - c_3 E'$ approaches zero.
  Production code clamps the denominator.
- **HLG OOTF vs OETF**: HLG has both an opto-electronic transfer function (OETF,
  what this module implements) and an opto-optical transfer function (OOTF) that
  applies system gain. This module is OETF-only; for full HLG display pipelines
  apply the OOTF separately.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/transfer/{srgb,rec2020,pq,hlg}.ts` — branded, bidirectional, sign-preserving. |
| **Culori** | `mode_*.parse` / `mode_*.serialize` includes transfer functions per mode. |
| **Color.js** | `ColorSpace` instances have `toGamma` / `fromGamma` hooks. |
| **@texel/color** | Inline transfer functions optimized for speed (no piecewise branch). |

---

## Primary sources

- **IEC 61966-2-1:1999** Annex E — sRGB definition (transfer function + primaries).
- **ITU-R BT.2020-2** (2015) — Rec.2020 primaries and OETF.
- **ITU-R BT.709-6** (2015) — Rec.709 OETF.
- **SMPTE ST 2084:2014** — PQ Electro-Optical Transfer Function.
- **ITU-R BT.2100-2** (2018) — HDR-TV (PQ + HLG normative reference).
- **ARIB STD-B67** (2015) — HLG original specification.
- **W3C CSS Color 4** — Web normative reference: <https://www.w3.org/TR/css-color-4/>
