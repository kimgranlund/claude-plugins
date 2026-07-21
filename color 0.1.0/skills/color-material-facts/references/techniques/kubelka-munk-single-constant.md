# Kubelka-Munk Single-Constant Mixing — Math

The standard physical model for paint, ink, and dye mixing. **Blue + Yellow
makes Green** in K-M (unlike additive RGB or naive averaging, which produce
muddy grays).

---

## TL;DR

Forward: $K/S = (1 - R)^2 / (2 R)$
Inverse: $R = 1 + K/S - \sqrt{(K/S)^2 + 2 (K/S)}$

Mixing is **linear in K/S space**, then convert back to reflectance:

$$
(K/S)_{\text{mix}} = \sum_i c_i \cdot (K/S)_i, \quad \sum_i c_i = 1
$$

The non-linearity of $R \leftrightarrow K/S$ is why K-M mixing produces
physically plausible results.

---

## Natural-language description

### Why RGB averaging fails

Two paint chips: pure blue and pure yellow. RGB averaging:
- Blue: $(0, 0, 1)$
- Yellow: $(1, 1, 0)$
- Midpoint: $(0.5, 0.5, 0.5)$ → **medium gray**

But real blue paint + yellow paint = green. Why?

Each paint absorbs certain wavelengths. Blue paint absorbs red and yellow,
reflects blue. Yellow paint absorbs blue and violet, reflects red, yellow,
green. When mixed, **both absorption profiles apply** — the only wavelengths
that survive are those reflected by both paints, which is green.

### The K-M model

Kubelka and Munk (1931, 1948) modeled this as a layered scattering medium:
- $K$ = absorption coefficient per wavelength
- $S$ = scattering coefficient per wavelength
- $R$ = observed reflectance

For thick, opaque layers (where back-illumination doesn't matter), the
**single-constant model** combines $K$ and $S$ into one ratio $K/S$.
**Mixing is linear in K/S space** because absorption is additive — both
pigments simultaneously absorb their respective wavelengths.

The forward $R \to K/S$ and inverse $K/S \to R$ formulas linearize the
absorption math, mix linearly, then return to reflectance space.

---

## Formulas

### Single-constant K-M

$$
\frac{K}{S} = \frac{(1 - R)^2}{2 R}
$$

This is **Kubelka's master equation** for the single-constant case.

Inverse:

$$
R = 1 + \frac{K}{S} - \sqrt{\left(\frac{K}{S}\right)^2 + 2 \cdot \frac{K}{S}}
$$

### Mixing N pigments

For pigment $i$ with concentration $c_i$ (where $\sum c_i = 1$):

$$
\left(\frac{K}{S}\right)_{\text{mix}}(\lambda) = \sum_i c_i \cdot \left(\frac{K}{S}\right)_i(\lambda)
$$

Apply this per wavelength to compute the mixed reflectance spectrum.

### Two-constant K-M (translucent / glaze)

For paints with measurable translucency, $K$ and $S$ are separate:

$$
\frac{K(\lambda)}{S(\lambda)} = \frac{\sum_i c_i K_i(\lambda)}{\sum_i c_i S_i(\lambda)}
$$

Not implemented in this skill; see Saunderson 1942 for the surface-reflection
correction that pairs with two-constant K-M.

---

## Implementation

Canonical TypeScript: [`src/pigment/kubelka-munk.ts`](../../../../color-science-project-files/src/pigment/kubelka-munk.ts).

Exports:
- `reflectanceToKS(R)` / `KSToReflectance(KS)` — scalar
- `spectrumToKS` / `KSToSpectrum` — per-wavelength array
- `mix(spectrumA, spectrumB, concentrationA)` — two-pigment mix
- `mixN(spectra, concentrations)` — N-pigment mix

```ts
export function reflectanceToKS(R: number): number {
  if (R <= 0) return 1e6;
  if (R >= 1) return 0;
  return ((1 - R) * (1 - R)) / (2 * R);
}

export function mix(
  spectrumA: readonly number[],
  spectrumB: readonly number[],
  concentrationA: number
): number[] {
  const cA = Math.max(0, Math.min(1, concentrationA));
  const ksA = spectrumToKS(spectrumA);
  const ksB = spectrumToKS(spectrumB);
  const mixed = ksA.map((ks, i) => cA * ks + (1 - cA) * ksB[i]);
  return KSToSpectrum(mixed);
}
```

Test vectors verify:
- $R = 1 \to K/S = 0$ (perfect reflector)
- $R = 0.5 \to K/S = 0.25$
- Round-trip identity
- White (R=1) + 4%-black (R=0.04) at 50:50 → R ≈ 0.074 (the classic K-M
  property: tiny black darkens enormously, far darker than RGB midpoint 0.52)

---

## Pigment → XYZ pipeline

```ts
import * as km from '../pigment/kubelka-munk.js';
import { reflectiveToXYZ } from '../spectral/spd.js';
import { D65 } from '../spectral/illuminants.js';

// 1. Define pigment reflectance spectra (36 samples, 380-730nm)
const blue = [/* 36 reflectance values */];
const yellow = [/* 36 reflectance values */];

// 2. K-M mix
const green = km.mix(blue, yellow, 0.5);

// 3. To XYZ under D65 illuminant
const xyz_green = reflectiveToXYZ(green, D65);
```

This is the right pipeline for any tool that simulates real-paint mixing
on screen.

---

## Edge cases

- **Pure white ($R = 1$)**: $K/S = 0$ exactly. Mixing pure white with
  anything preserves the other pigment's $K/S$ scaled by $(1 - c_{\text{white}})$.
- **Pure black ($R = 0$)**: $K/S \to \infty$. Practical implementations
  clamp $R$ to a small epsilon (typically 0.001-0.01) to avoid numerical
  blowup.
- **Saunderson correction**: real pigment surfaces have a top air-paint
  boundary that reflects ~4% of incident light. The Saunderson correction
  accounts for this in two-constant K-M; single-constant typically ignores it.
- **Wavelength resolution**: 10nm is sufficient for matching consumer
  paint formulations. Professional formulation tools use 5nm or 1nm and
  consider fluorescent pigments.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/pigment/kubelka-munk.ts` — single-constant, branded types. |
| **Spectral.js** | <https://github.com/rvanwijnen/spectral.js> — open-source K-M for GLSL. |
| **Mixbox** | Commercial (Scrtwpns Studio); rod-and-cone pigment model derived from K-M. |
| **Mixbox.js** | Free academic license; ~37 base pigments. |

---

## Primary sources

- **Kubelka, P. (1948)** — "New Contributions to the Optics of Intensely
  Light-Scattering Materials," *J. Optical Society of America* 38(5).
- **Saunderson, J. L. (1942)** — "Calculation of the Color of Pigmented
  Plastics," *J. Optical Society of America* 32(12).
- **Berns, R. S. (2019)** — *Billmeyer and Saltzman's Principles of Color
  Technology*, 4th ed. — canonical textbook for industrial colorimetry.
- **Companion**: [`spectral-to-xyz-integration.md`](../../../color-space-facts/references/techniques/spectral-to-xyz-integration.md) —
  converting reflectance spectra to XYZ.
- **Companion**: [`spectraljs-pigment-mixing.md`](./spectraljs-pigment-mixing.md) —
  the Spectral.js library overview (existing).
