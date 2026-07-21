# Spectral → XYZ Integration — Math

The physical bridge from a Spectral Power Distribution (SPD) to CIE
tristimulus XYZ. The integral that defines colorimetry.

---

## TL;DR

$$
X = k \int_{380}^{780} E(\lambda) \bar{x}(\lambda) d\lambda, \quad
Y = k \int E(\lambda) \bar{y}(\lambda) d\lambda, \quad
Z = k \int E(\lambda) \bar{z}(\lambda) d\lambda
$$

For reflective surfaces under an illuminant:

$$
X = k \int R(\lambda) E(\lambda) \bar{x}(\lambda) d\lambda
$$

Where $\bar{x}, \bar{y}, \bar{z}$ are CIE 1931 2° color matching functions
and $k$ normalizes so $Y_\text{white} = 100$ (or 1, our convention).

Implementation uses 36 samples at 380-730nm, 10nm steps, rectangle-rule.

---

## Natural-language description

Spectral colorimetry is the **ground truth**. Every real-world color is a
spectrum: light hitting a surface, reflecting some wavelengths more than
others, then hitting your eye. The cones in your retina integrate that
spectrum against three sensitivity curves (long, medium, short wavelengths)
to produce three signals.

CIE 1931 standardized the **2° observer** color matching functions —
mathematical curves that approximate the average human retinal response.
The integral of an SPD against these CMFs gives CIE XYZ — the
device-independent representation of "what a standard observer sees."

**Why this matters in practice:**
- Reflectance spectra are the physical reality of paint, dye, ink, fabric.
- Different illuminants × same reflectance = different XYZ (metamerism).
- Spectral round-trip catches mistakes that XYZ-only pipelines hide.

---

## Formulas

### Continuous form

$$
\begin{aligned}
X &= k \int_{380}^{780} E(\lambda) \bar{x}(\lambda) \, d\lambda \\
Y &= k \int_{380}^{780} E(\lambda) \bar{y}(\lambda) \, d\lambda \\
Z &= k \int_{380}^{780} E(\lambda) \bar{z}(\lambda) \, d\lambda
\end{aligned}
$$

The normalization constant $k$ is chosen so that the reference white gives
$Y = Y_\text{white}$ (typically 100 in CIE units or 1 in our convention).

### Discrete (rectangle-rule) form

$$
X = \frac{\Delta\lambda}{k_w} \sum_{i=0}^{N-1} E_i \bar{x}_i, \quad
k_w = \Delta\lambda \sum_{i=0}^{N-1} E_{\text{white},i} \bar{y}_i
$$

with $\Delta\lambda = 10\text{nm}$, $N = 36$ samples from 380nm to 730nm.

### Reflective surface under illuminant

$$
X = k \int R(\lambda) E(\lambda) \bar{x}(\lambda) d\lambda
$$

The reflectance $R(\lambda) \in [0, 1]$ multiplies the illuminant before
integration. A perfect diffuse reflector ($R = 1$ everywhere) gives the
illuminant's chromaticity.

---

## Implementation

Canonical TypeScript:
- [`src/spectral/illuminants.ts`](../../../../color-science-project-files/src/spectral/illuminants.ts) — D65, D50, A, E standard illuminants
- [`src/spectral/cmf.ts`](../../../../color-science-project-files/src/spectral/cmf.ts) — CIE 1931 2° color matching functions
- [`src/spectral/spd.ts`](../../../../color-science-project-files/src/spectral/spd.ts) — `emissiveToXYZ`, `reflectiveToXYZ`

```ts
export function reflectiveToXYZ(
  reflectance: readonly number[],
  illuminant: SPD = D65
): XYZ_D65 {
  let X = 0, Y = 0, Z = 0, Yn = 0;
  for (let i = 0; i < 36; i++) {
    const E = illuminant[i];
    X += reflectance[i] * E * CMF_1931[i][0];
    Y += reflectance[i] * E * CMF_1931[i][1];
    Z += reflectance[i] * E * CMF_1931[i][2];
    Yn += E * CMF_1931[i][1];
  }
  return xyz(X / Yn, Y / Yn, Z / Yn);
}
```

Test vectors verify:
- D65 → Y = 1 (normalization).
- D65 chromaticity = (0.3127, 0.3290).
- Perfect diffuse reflector → Y = 1 regardless of illuminant.

---

## Standard illuminants (10nm-tabulated)

| Illuminant | Notes |
|---|---|
| **D65** | Modern display white (~6500 K) |
| **D50** | ICC Profile Connection Space, traditional CIELAB |
| **A** | Tungsten incandescent (~2856 K) |
| **F2** | Cool white fluorescent |
| **E** | Theoretical equal-energy (flat spectrum) |

Full tables in `src/spectral/illuminants.ts`. For higher-precision work
(5nm or 1nm), supplement with CIE-published data; this skill uses 10nm
as the design-typical resolution.

---

## Edge cases

- **Metamerism**: two different SPDs can produce the same XYZ. Forward
  integration is well-defined; the inverse (XYZ → SPD) is non-unique.
- **Out-of-gamut reflectance**: $R > 1$ is physically impossible (energy
  conservation). Some pipelines allow $R > 1$ for fluorescence; not handled.
- **Negative reflectance**: meaningless physically; not handled.
- **10nm vs 5nm sampling**: 10nm is accurate to ~0.1 ΔE for typical SPDs.
  For research-grade colorimetry use 5nm or 1nm.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spectral/{spd,cmf,illuminants}.ts` — 10nm tables, rectangle integration. |
| **Colour** (Python) | Full spectral toolkit by Colour Developers. |
| **Argyll CMS** | Production-grade spectral color management. |
| **Bruce Lindbloom** | <http://brucelindbloom.com/Spectra.html> — CMF and illuminant tables. |

---

## Primary sources

- **CIE 015:2018 — Colorimetry, 4th edition** — Normative.
- **CIE 011 — Standard Illuminants for Colorimetry**
- **Bruce Lindbloom** — <http://brucelindbloom.com/Eqn_Spect_to_XYZ.html>
- **Companion**: [`kubelka-munk-single-constant.md`](../../../color-material-facts/references/techniques/kubelka-munk-single-constant.md) (color-material-facts) —
  pigment mixing uses spectral arithmetic.
