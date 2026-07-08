# Relative Luminance & WCAG Contrast — Math

Relative luminance $Y$ is **the perceptual brightness component of XYZ** — the
$Y$ in $X, Y, Z$. It's the basis for WCAG 2.x contrast ratios, the lightness
axis in CIELAB, the achromatic response in CAM16, and any "how bright is this
color" calculation.

---

## TL;DR

- Relative luminance $Y$ is **just the Y component of XYZ-D65**.
- From **linear sRGB**: $Y = 0.2126 R + 0.7152 G + 0.0722 B$ (the middle row of
  $M_{\text{sRGB} \to \text{XYZ}}$).
- From **encoded sRGB**: decode via sRGB transfer first, then apply the
  coefficients above.
- **WCAG 2.x contrast** is $(L_1 + 0.05) / (L_2 + 0.05)$ where $L_1 \ge L_2$.
  Output range $[1, 21]$.
- **Use APCA for modern UX work.** WCAG 2.x is the legal floor; APCA is
  polarity-sensitive and spatial-frequency aware.

---

## Natural-language description

Two distinct concepts get conflated:

- **Relative luminance ($Y$)**: a physical/colorimetric quantity. The integral
  of an emissive spectrum against the photopic luminosity function
  $V(\lambda)$, normalized to the chosen white. Bigger $Y$ = more light.

- **Perceived lightness ($L^*$ or $J$)**: a perceptual quantity. How bright the
  color *feels*, accounting for nonlinear visual response. CIELAB defines
  $L^* = 116 \cdot f(Y/Y_n) - 16$ via a cube-root function (see
  [`cielab-xyz-conversion.md`](../../../color-science-spaces/references/techniques/cielab-xyz-conversion.md)).

WCAG contrast is defined in **luminance space, not lightness space** — which is
why it has well-known issues with darker colors and is being replaced by APCA in
modern guidance.

The **luminance coefficients** for linear sRGB $(0.2126, 0.7152, 0.0722)$ come
directly from the BT.709 primaries' $Y$ chromaticities at the D65 white point.
They are the middle row of $M_{\text{sRGB} \to \text{XYZ}}$.

---

## Formulas

### Relative luminance from XYZ-D65

Trivially:

$$
Y = c_Y
$$

where $c_Y$ is the second component of the XYZ-D65 tuple.

### Relative luminance from linear sRGB

$$
Y = 0.2126390059 \cdot R + 0.7151686788 \cdot G + 0.0721923154 \cdot B
$$

The coefficients sum to $1.0$ (white at $(1, 1, 1)$ produces $Y = 1$).

For lower-precision implementations you'll see $0.2126, 0.7152, 0.0722$ rounded
to 4 digits. The 10-digit values above match $M_{\text{sRGB} \to \text{XYZ}}$.

### Relative luminance from encoded sRGB

Decode the gamma first (see
[`gamma-transfer-functions.md`](../../../color-science-spaces/references/techniques/gamma-transfer-functions.md)), then apply
the linear formula:

$$
Y = 0.2126 \cdot \text{sRGBdecode}(R') + 0.7152 \cdot \text{sRGBdecode}(G') + 0.0722 \cdot \text{sRGBdecode}(B')
$$

This is the formula in **WCAG 2.1/2.2 Success Criterion 1.4.3 (Contrast Minimum)**.

### WCAG 2.x contrast ratio

Given two encoded sRGB colors $A$ and $B$, compute $Y_A$ and $Y_B$ via the
formula above. The contrast ratio is:

$$
\text{contrast} = \frac{L_1 + 0.05}{L_2 + 0.05}
$$

where $L_1 = \max(Y_A, Y_B)$ and $L_2 = \min(Y_A, Y_B)$.

**The $+0.05$** approximates ambient flare on a typical display. Without it the
ratio at black would be undefined (division by zero) or infinite.

**Range**: minimum 1.0 (identical colors). Maximum $(1 + 0.05) / 0.05 = 21$
(pure white on pure black).

### WCAG thresholds

| Threshold | Use case |
|---|---|
| **3.0 : 1** | Large text (≥18pt regular or ≥14pt bold) — AA |
| **4.5 : 1** | Normal text — AA |
| **7.0 : 1** | Normal text — AAA |

---

## Implementation

Canonical TypeScript: [`src/metrics/luminance.ts`](../../../../color-science-project-files/src/metrics/luminance.ts).

Exports relative-luminance helpers and WCAG contrast with AA/AAA threshold checks:

```ts
export function fromXYZ(c: XYZ_D65): number {
  return c[1];
}

export function fromLinearSRGB(c: LinearSRGB): number {
  return 0.2126390059 * c[0] + 0.7151686788 * c[1] + 0.0721923154 * c[2];
}

export function fromEncodedSRGB(c: EncodedSRGB): number {
  return fromLinearSRGB(srgbTransfer.decode(c));
}

export function wcagContrast(a: EncodedSRGB, b: EncodedSRGB): number {
  const La = fromEncodedSRGB(a);
  const Lb = fromEncodedSRGB(b);
  const lighter = Math.max(La, Lb);
  const darker = Math.min(La, Lb);
  return (lighter + 0.05) / (darker + 0.05);
}
```

---

## Why APCA is better than WCAG 2.x

WCAG 2.x has documented problems:
- **Polarity-blind**: white-on-black vs. black-on-white produce identical
  numbers, but the eye sees them differently (asymmetry between dark and light
  backgrounds).
- **Spatial-frequency-blind**: ignores font size, weight, and stroke
  geometry — but thin small text needs much more contrast than thick large text.
- **Mid-range distortion**: passes pairs that look poor; rejects pairs that
  look fine.

**APCA** (Accessible Perceptual Contrast Algorithm) fixes these by:
- Using polarity-sensitive lightness ($L^c$ formula) instead of luminance.
- Including a font-size/weight lookup table (table of minimum $L^c$ per font).
- Calibrated against real-world legibility research.

See [`apca-myndex-contrast.md`](./apca-myndex-contrast.md) (tooling reference)
and (planned) `src/metrics/apca.ts` for the $L^c$ formula and table.

**Recommendation per [SKILL.md](../../SKILL.md)**: use APCA for design
decisions; clear WCAG 2.2 for legal compliance.

---

## Edge cases

- **Encoded vs linear confusion**: applying the luminance coefficients to
  **encoded** sRGB values (without decoding first) is a common bug. Result is
  ~30% too low for darks. Always decode first.
- **Wide-gamut content in narrow encoding**: P3 / Rec.2020 colors in linear
  values can exceed $[0, 1]$. The luminance formula is still linear, so
  $Y$ can exceed 1 — this is correct for HDR but unexpected for SDR pipelines.
- **The $+0.05$ flare term**: only applies to WCAG contrast; never to raw
  luminance.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/metrics/luminance.ts` — relative Y + WCAG contrast + AA/AAA helpers. |
| **Culori** | `wcagLuminance(color)`, `wcagContrast(a, b)`. |
| **Color.js** | `color.luminance`, `Color.contrast(a, b, "WCAG21")`. |
| **apca-w3** | `APCAcontrast(text, bg)` — Myndex's reference APCA implementation. |

---

## Primary sources

- **CIE 015:2018** — Y as the photopic relative luminance.
- **IEC 61966-2-1:1999** — sRGB transfer + luminance coefficients via the
  primary chromaticities.
- **WCAG 2.1** — <https://www.w3.org/TR/WCAG21/#dfn-relative-luminance> (the
  $+0.05$ flare term defined here).
- **WCAG 2.2** — <https://www.w3.org/TR/WCAG22/#contrast-minimum> (current legal
  reference).
- **APCA-W3** — <https://github.com/Myndex/apca-w3> (Myndex's APCA reference
  implementation, MIT licensed).
