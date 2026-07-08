# White Point Conversion — Math

The chromaticity coordinates of standard illuminants, and how to convert
XYZ values from one illuminant to another. **Required whenever ICC
profile work (D50) meets display work (D65)**.

---

## TL;DR

| Illuminant | $(x_w, y_w)$ | $(X_w, Y_w, Z_w)$ normalized | Where used |
|---|---|---|---|
| **D65** | (0.31272, 0.32903) | (0.95046, 1.0, 1.08906) | sRGB, P3, Rec.709/2020 displays |
| **D50** | (0.34567, 0.35850) | (0.96430, 1.0, 0.82510) | ICC Profile Connection Space |
| **D55** | (0.33242, 0.34743) | (0.95682, 1.0, 0.92149) | Photography (deprecated for new work) |
| **D75** | (0.29902, 0.31485) | (0.94972, 1.0, 1.22638) | Northern sky daylight |
| **A** | (0.44757, 0.40745) | (1.09850, 1.0, 0.35585) | Tungsten incandescent (2856 K) |
| **F2** | (0.37207, 0.37512) | (0.99186, 1.0, 0.67393) | Cool-white fluorescent |

Convert between illuminants via **Bradford CAT** (already implemented in
[`src/adaptation/bradford.ts`](../../../../color-science-project-files/src/adaptation/bradford.ts)).

---

## Natural-language description

### What is a "white point"

The white point of a color system defines what color "white" is. It's a
specific XYZ value (or chromaticity) chosen by the standards body that
defined the system. Different bodies chose different whites:

- **ICC PCS**: D50 (CIE 1931 daylight at 5000 K). Historical choice for
  print workflows.
- **sRGB, P3, Rec.2020**: D65 (CIE 1931 daylight at 6504 K). Modern display
  standard.
- **Pre-1976 photography**: D55 or D65 depending on era.
- **Tungsten lighting**: Illuminant A (2856 K). Used in indoor incandescent
  conditions.

A color appears "white" when its reflected/emitted XYZ matches the white
point's XYZ. Under D50 lighting, a perfect diffuse reflector has XYZ
equal to D50's (X, Y, Z). Same reflector under D65 has D65's (X, Y, Z).

### Why conversion matters

If you have an XYZ value computed under D50 (e.g., from an ICC profile)
and want to render it on a D65 display, you must **chromatically adapt**
the XYZ. Without adaptation, you'd render a color "as if" the D50 white
were D65 — producing a noticeable color shift (~5-10% error).

The Bradford transform (and its CAT16 successor) provides the matrix
math. See [`chromatic-adaptation-matrices.md`](./chromatic-adaptation-matrices.md)
for the algorithm.

---

## Common conversions

### D65 ↔ D50 (Bradford)

The most common conversion (ICC ↔ display). Pre-computed Bradford matrices
in [`src/adaptation/bradford.ts`](../../../../color-science-project-files/src/adaptation/bradford.ts):

```ts
import { d50ToD65, d65ToD50 } from '../adaptation/bradford.js';

const xyz_D65 = d50ToD65(xyz_D50);  // ICC PCS → display
const xyz_D50 = d65ToD50(xyz_D65);  // display → ICC PCS
```

The matrices (from Bradford CAT applied to the D50 and D65 white points)
are pre-computed at module load time and cached.

### D65 ↔ A (tungsten)

Less common in computer graphics, but needed for cross-illuminant
photography work. Same Bradford machinery:

```ts
import { adapt, D65, A } from '../adaptation/bradford.js';

const xyz_under_A = adapt(xyz_under_D65, D65, A);
```

### Custom white points

For colorimetry calibration: derive your own white point from measured
chromaticity and pass it as the `srcWhite` / `dstWhite` argument.

---

## Correlated Color Temperature (CCT)

Each Planckian illuminant has a color temperature (the temperature of a
black-body radiator that emits the same chromaticity). For daylight
approximations, CIE's "D series" gives:

- D50 ≈ 5000 K (warmer)
- D55 ≈ 5500 K
- D65 ≈ 6504 K (canonical)
- D75 ≈ 7500 K (cooler)

For a given CCT $T$ (in Kelvin), Robertson's 1968 approximation gives the
chromaticity coordinates:

$$
\begin{aligned}
x &= \tfrac{-4.6070 \times 10^9}{T^3} + \tfrac{2.9678 \times 10^6}{T^2} + \tfrac{0.09911 \times 10^3}{T} + 0.244063 \quad (T \in [4000, 7000]) \\
y &= -3.000 x^2 + 2.870 x - 0.275
\end{aligned}
$$

These are useful for white-balance correction in raw photo workflows. Not
implemented in this skill — composes from existing parts if needed.

---

## Implementation

Canonical TypeScript: [`src/adaptation/bradford.ts`](../../../../color-science-project-files/src/adaptation/bradford.ts)
already exports:

- `D65`, `D50`, `D55`, `D75`, `A`, `F2` constants (XYZ at Y=1)
- `bradfordMatrix(srcWhite, dstWhite)` — generic adaptation matrix
- `adapt(srcXYZ, srcWhite, dstWhite)` — single-color adaptation
- `M_D50_TO_D65`, `M_D65_TO_D50` — pre-computed common matrices
- `d50ToD65`, `d65ToD50` — typed convenience wrappers

```ts
// Usage:
import { D65, D50, adapt } from '../adaptation/bradford.js';

const xyz_d50 = [0.5, 0.5, 0.5];          // some XYZ at D50
const xyz_d65 = adapt(xyz_d50, D50, D65); // shift to D65
```

For a typed D50 / D65 type system (e.g., `CIELAB_D50` vs `CIELAB_D65`),
this skill currently only implements the D65 variants. D50 variants would
follow the pattern: define a brand, write the space module that takes the
appropriate reference white in its constants.

---

## Workflow: ICC-tagged image → sRGB display

```
1. Read ICC profile: get the profile's working space white point (often D50).
2. Decode pixel: ICC RGB → linear ICC RGB → XYZ_D50 (using profile matrices).
3. Bradford adapt: XYZ_D50 → XYZ_D65.
4. Encode for display: XYZ_D65 → linear sRGB → encoded sRGB.
```

Step 3 is the chromatic adaptation. Without it, neutrals would appear
slightly yellow (D50 has more yellow component than D65).

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/adaptation/bradford.ts` — Bradford CAT with D65, D50, D55, D75, A, F2. |
| **ICC v4 profile spec** | Defines D50 as PCS; all profile workflows ultimately ground here. |
| **LittleCMS** (`lcms2`) | Production ICC color management with full CAT support. |
| **Color.js** | `Color.to('lab-d50')`, `Color.to('lab-d65')` etc. |
| **Bruce Lindbloom** | <http://brucelindbloom.com/Eqn_ChromAdapt.html> — practical reference. |

---

## Primary sources

- **CIE 015:2018** — Section 6.4 defines standard illuminants D50, D55,
  D65, D75 and Illuminant A.
- **CIE TC 1-48** — colorimetry standardization committee.
- **ICC.1:2010-12** — Image technology colour management; defines D50 as
  Profile Connection Space.
- **Robertson, A. R. (1968)** — CCT-to-chromaticity approximation,
  *Journal of the Optical Society of America* 58(11), 1528-1535.
- **Companion**: [`chromatic-adaptation-matrices.md`](./chromatic-adaptation-matrices.md) —
  the Bradford and CAT16 algorithms used for conversion.
- **Companion**: [`cielab-xyz-conversion.md`](./cielab-xyz-conversion.md) —
  the CIELAB D65 implementation; D50 variants follow the same pattern.
