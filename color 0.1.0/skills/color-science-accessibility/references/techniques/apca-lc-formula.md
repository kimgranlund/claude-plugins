# APCA Lightness Contrast — Math

APCA — the Accessible Perceptual Contrast Algorithm — is the modern replacement
for WCAG 2.x contrast. **Polarity-sensitive**, spatial-frequency aware,
calibrated against real readability research.

This document covers the math. For positioning (APCA as design standard,
WCAG 2.2 as legal floor), see [SKILL.md](../../SKILL.md) and
[`apca-myndex-contrast.md`](./apca-myndex-contrast.md).

---

## TL;DR

- Output: $L^c$ ("lightness contrast") in roughly $[-108, +106]$.
  - Positive = dark text on light background (BoW).
  - Negative = light text on dark background (WoB).
  - Magnitude = perceived readability.
- **Polarity-sensitive**: white-on-black ≠ black-on-white (different magnitudes).
- Uses a **simplified 2.4 power gamma** (not sRGB's piecewise transfer) — intentional.
- Standard thresholds: $|L^c| \ge 60$ minimum body text, $\ge 75$ for fluent
  reading, $\ge 90$ for sustained reading.

---

## Natural-language description

WCAG 2.x contrast has documented problems:

1. **Polarity-blind**: $(L_1 + 0.05) / (L_2 + 0.05)$ is symmetric. But the eye sees
   white-on-black and black-on-white differently — dark backgrounds need more
   contrast to read the same text legibly.
2. **Spatial-frequency-blind**: the same numbers apply to 18pt thin text and 36pt
   bold text, but the eye needs very different contrast for those cases.
3. **Mid-range distortion**: passes pairs that look poor (e.g., dark gray on
   medium gray); rejects pairs that look fine.

APCA fixes these by:

- Using **lightness contrast** ($L^c$) rather than luminance ratio. Lightness is
  the perceived brightness; luminance is the physical light.
- Including **polarity-aware exponents**: different power values for the
  background and text depending on whether the text is darker or lighter.
- Pairing $L^c$ values with a **font-size × weight lookup table** so a 12pt
  light-weight font needs more contrast than 36pt bold.

The 2.4 power gamma is a deliberate simplification — APCA is calibrated against
readability experiments, and the simplified gamma matches those calibrations
better than the strict sRGB transfer.

---

## Formulas

All operations use APCA's simplified Y. Constants below are from APCA-W3
v0.1.9 (the W3C-archived APCA Bronze Simple Mode reference).

### Step 1: simplified Y from encoded sRGB

$$
Y = 0.2126729 \cdot R^{2.4} + 0.7151522 \cdot G^{2.4} + 0.0721750 \cdot B^{2.4}
$$

where $R, G, B$ are encoded sRGB in $[0, 1]$ (or $[0, 255]$ divided by 255).

### Step 2: near-black soft clamp

For very dark values, apply a soft clamp to model display flare:

$$
Y \leftarrow Y + (0.022 - Y)^{1.414} \quad \text{if } Y < 0.022
$$

### Step 3: bail-out checks

- If $|Y_\text{bg} - Y_\text{txt}| < 0.0005$, return $L^c = 0$ (too close to measure).

### Step 4a: dark text on light background (BoW)

$$
C = 1.14 \left( Y_\text{bg}^{0.56} - Y_\text{txt}^{0.57} \right)
$$

- If $C < 0.1$, return $L^c = 0$ (low-contrast clip).
- If $C < 0.027$, apply soft scaling:

$$
SAPC = C - C \cdot \frac{32.8 \cdot (0.027 - C)}{0.027}
$$

- Otherwise: $SAPC = C - 0.027$.

### Step 4b: light text on dark background (WoB)

$$
C = 1.14 \left( Y_\text{bg}^{0.65} - Y_\text{txt}^{0.62} \right)
$$

(Note the **different exponents** — that's the polarity-sensitive part.)

- If $C > -0.1$, return $L^c = 0$.
- If $C > -0.027$, apply soft scaling (mirror of BoW).
- Otherwise: $SAPC = C + 0.027$.

### Step 5: final output

$$
L^c = SAPC \cdot 100
$$

---

## Readability tiers (Bronze Simple Mode)

Approximate guidance — full table considers font size and weight:

| $|L^c|$ | Tier | Use |
|---|---|---|
| **90+** | Optimal | Sustained body reading |
| **75–89** | Fluent body | Body text, recommended baseline |
| **60–74** | Body minimum | Minimum for readable body text |
| **45–59** | Heading / large body | Headings (≥24pt) or large body (≥18pt bold) |
| **30–44** | Large heading | Headings ≥36pt |
| **15–29** | Non-text only | Icons, decorative elements |
| **<15** | Insufficient | Not usable for readable content |

For full font-size × weight tables, see the
[APCA-W3 lookup tables](https://github.com/Myndex/SAPC-APCA).

---

## Implementation

Canonical TypeScript: [`src/metrics/apca.ts`](../../../../color-science-project-files/src/metrics/apca.ts).

Exports:
- `apcaY(rgb: EncodedSRGB): number` — APCA's simplified Y (gamma 2.4 with soft clamp)
- `apcaContrast(text: EncodedSRGB, bg: EncodedSRGB): number` — main API, returns $L^c$
- `readabilityTier(lc: number): ApcaTier` — tier label per Bronze Simple Mode

```ts
export function apcaContrast(text: EncodedSRGB, bg: EncodedSRGB): number {
  const txtY = apcaY(text);
  const bgY = apcaY(bg);
  if (Math.abs(bgY - txtY) < DELTA_Y_MIN) return 0;

  if (bgY > txtY) {
    const C = SCALE_BOW * (Math.pow(bgY, NORM_BG) - Math.pow(txtY, NORM_TXT));
    /* ... soft clip + offset ... */
  } else {
    const C = SCALE_WOB * (Math.pow(bgY, REV_BG) - Math.pow(txtY, REV_TXT));
    /* ... soft clip + offset ... */
  }
}
```

Test vectors include pure black-on-white ($L^c \approx 106$) and pure
white-on-black ($L^c \approx -107.88$) cross-checked against APCA-W3.

---

## Edge cases

- **Out-of-range input**: APCA expects encoded sRGB in $[0, 1]$. Values outside
  this range are accepted but produce undefined behavior.
- **Floating-point near-zero**: the $\delta Y \ge 0.0005$ early-out prevents
  spurious tiny $L^c$ values from float noise.
- **Polarity swap**: `apcaContrast(text, bg)` is NOT the same as
  `apcaContrast(bg, text)` — that's the whole point. Order matters.
- **Non-sRGB content**: APCA is defined for sRGB. Wide-gamut content (P3,
  Rec.2020) must be gamut-mapped to sRGB first. (A future APCA-P3 may exist
  but isn't standardized as of 2026.)

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/metrics/apca.ts` — APCA-W3 v0.1.9 constants + readability tiers. |
| **apca-w3** (Myndex) | <https://github.com/Myndex/apca-w3> — reference MIT-licensed implementation. |
| **Color.js** | `Color.contrast(a, b, "APCA")` — uses Myndex's algorithm. |
| **Culori** | No direct APCA support as of 2026; can compose via `displayable` + manual implementation. |

---

## Primary sources

- **APCA-W3** (Myndex Research) — <https://github.com/Myndex/apca-w3> —
  MIT-licensed reference implementation, v0.1.9 constants used here.
- **SAPC-APCA** (Myndex) — <https://github.com/Myndex/SAPC-APCA> — the full
  research toolkit including the font-size × weight lookup tables.
- **APCAcontrast.com** — interactive calculator.
- **WCAG 2.2** — <https://www.w3.org/TR/WCAG22/> — current legal floor; APCA is
  positioned as the modern design standard above this floor (per
  [SKILL.md](../../SKILL.md)).
