# Jzazbz & ICtCp — HDR Uniform Color Spaces — Math

Two HDR-capable perceptually uniform color spaces. Designed for HDR
content where SDR-calibrated spaces (CIELAB, OKLab) fail at the high
luminance end. Use when working with HDR pipelines (10,000 nits), HDR
display calibration, or any HDR perceptual difference metric.

---

## TL;DR

| Space | Year | Use |
|---|---|---|
| **Jzazbz** | Safdar et al. 2017 | HDR uniform $(J_z, a_z, b_z)$ analogous to OKLab/CIELAB |
| **ICtCp** | Dolby 2014 / BT.2100 | HDR opponent encoding with constant-luminance preservation |

Both apply PQ-like nonlinearity to LMS-derived cone responses. Jzazbz is
more uniform; ICtCp is more efficient for video encoding.

---

## Natural-language description

### The HDR problem

OKLab's cube root and CIELAB's $L^*$ formula are calibrated for the SDR
luminance range (0–100 cd/m²). At higher luminances (HDR displays go to
1000+ cd/m², HDR mastering targets 10,000 nits), these spaces become
non-uniform — the cube root flattens out the perceptual variation at
high brightness.

The fix: use a transfer function calibrated across the full HDR range.
Safdar's Jzazbz uses a PQ-like (Perceptual Quantizer) function adapted
from the SMPTE ST 2084 HDR transfer. ICtCp uses the actual PQ.

### Jzazbz structure

Pipeline:
1. **Pre-adaptation**: subtract a fraction of Z from X and X from Y
   (corrects blue-yellow bias).
2. **XYZ → LMS** via a matrix (similar in spirit to OKLab's M1).
3. **PQ-like nonlinearity** per LMS component.
4. **LMS → (Iz, az, bz)** via opponent matrix.
5. **Iz → Jz** via a final hyperbolic transform.

The result is approximately uniform from 0 to 10,000 nits.

### ICtCp structure

Pipeline:
1. **Rec.2020 → LMS** (different LMS matrix than Jzazbz).
2. **PQ nonlinearity** per LMS component (the actual SMPTE 2084 PQ).
3. **LMS → (I, Ct, Cp)** via opponent matrix.

The "I" component is luminance, Ct/Cp are blue-yellow / red-green opponent
signals. Used in BT.2100 HDR video encoding.

---

## Formulas

### Jzazbz forward

Constants: $b = 1.15$, $g = 0.66$, $d = -0.56$, $d_0 = 1.6295 \times 10^{-11}$.

PQ-like with adjusted exponents: $n = 2610/16384$, $m = 1.7 \cdot 2523/32$,
$c_1 = 3424/4096$, $c_2 = 2413/128$, $c_3 = 2392/128$.

$$
\begin{aligned}
X' &= b \cdot X - (b - 1) \cdot Z \\
Y' &= g \cdot Y - (g - 1) \cdot X \\
\text{LMS} &= M_1 \cdot (X', Y', Z) \\
\text{LMS}' &= \left(\frac{c_1 + c_2 (\text{LMS}/10000)^n}{1 + c_3 (\text{LMS}/10000)^n}\right)^m \\
(I_z, a_z, b_z) &= M_2 \cdot \text{LMS}' \\
J_z &= \frac{(1 + d) I_z}{1 + d I_z} - d_0
\end{aligned}
$$

Matrices $M_1$ and $M_2$: see implementation in `src/spaces/jzazbz.ts`.

### ICtCp forward (BT.2100)

Different LMS matrix and the actual SMPTE ST 2084 PQ:

$$
\begin{aligned}
\text{LMS} &= M_{\text{Rec.2020}\to\text{LMS}} \cdot \text{RGB}_{\text{linear}} \\
\text{LMS}' &= \text{PQ}(\text{LMS}) \\
(I, C_t, C_p) &= M_{\text{LMS}'\to\text{ICtCp}} \cdot \text{LMS}'
\end{aligned}
$$

Where PQ is the standard BT.2100 PQ from
[`gamma-transfer-functions.md`](./gamma-transfer-functions.md). ICtCp is
not implemented in this skill yet — composes from existing PQ + matrix work.

---

## Implementation

Canonical TypeScript: [`src/spaces/jzazbz.ts`](../../../../color-science-project-files/src/spaces/jzazbz.ts).

Exports `fromXYZ(xyz)` / `toXYZ(jzazbz)`. Note: input XYZ is in the
normalized [0, 1] convention used throughout this skill; the Jzazbz
algorithm internally scales to the 0–10,000 nit range for the PQ-like
step, then scales back.

```ts
export function fromXYZ(c: XYZ_D65): Jzazbz {
  const X = c[0] * 10000, Y = c[1] * 10000, Z = c[2] * 10000;
  const Xp = B * X - (B - 1) * Z;
  const Yp = G * Y - (G - 1) * X;
  const lms = mulMat3Vec3(M1, [Xp, Yp, Z]);
  const lmsP = [pqLike(lms[0]), pqLike(lms[1]), pqLike(lms[2])];
  const [Iz, az, bz] = mulMat3Vec3(M2, lmsP);
  const Jz = ((1 + D_J) * Iz) / (1 + D_J * Iz) - D0;
  return [Jz, az, bz] as Jzazbz;
}
```

Test vector: black point → $(J_z = -d_0, a_z = 0, b_z = 0)$. The small
$-d_0$ ($\sim 10^{-11}$) is intentional — it adjusts the black point
slightly for numerical stability of the inverse.

### ICtCp implementation (deferred)

Not implemented as a separate space module. Composable from existing
parts:
1. Rec.2020 linear input via `src/spaces/rec2020.ts`
2. PQ encoding via `src/transfer/pq.ts`
3. ICtCp opponent matrix (would be ~20 lines)

If concrete need arises, add `src/spaces/ictcp.ts` following the Jzazbz
pattern.

---

## When to use which

| Use case | Recommended |
|---|---|
| HDR uniform color picker | Jzazbz |
| HDR ΔE metric | Jzazbz (use Euclidean) |
| HDR video encoding | ICtCp (BT.2100 standard) |
| SDR UI work | OKLab (lighter, simpler, calibrated for SDR) |
| Tone mapping pipeline | Both — Jzazbz for perceptual analysis, ICtCp for storage |

For typical UI / design-token work that stays in SDR (sRGB / P3 at
display white): use OKLab. Reach for Jzazbz when you have HDR content.

---

## Edge cases

- **Black point**: $J_z = -d_0 \approx -1.6 \times 10^{-11}$, not exactly 0.
  Test tolerance must accommodate this.
- **Near-zero LMS**: the PQ-like nonlinearity diverges as LMS → 0 from
  the negative side. Clamp inputs to $\geq 0$.
- **Out-of-range**: Jzazbz is defined for any positive XYZ. Wide-gamut
  content (P3, Rec.2020) is supported; gamut handling is separate.
- **Round-trip precision**: limited to ~$10^{-3}$ due to the PQ-like
  cube-rooting + transcendentals. Higher precision requires careful
  implementation of the inverse PQ-like.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/jzazbz.ts` — branded types, hub conversion. |
| **Culori** | `mode_jab` (Jzazbz) and partial ICtCp. |
| **Color.js** | `ColorSpace.get('jzazbz')` and `'ictcp'`. |
| **HDRTools** | C++ reference for BT.2100 / ICtCp. |

---

## Primary sources

- **Safdar, Cui, Kim, Luo (2017)** — "Perceptually uniform color space
  for image signals including high dynamic range and wide gamut,"
  *Optics Express* 25(13), 15131-15151. Jzazbz definition.
- **ITU-R BT.2100** (2018) — HDR-TV reference; ICtCp normative.
- **SMPTE ST 2084:2014** — Perceptual Quantizer (PQ) electro-optical
  transfer function.
- **Companion**: [`gamma-transfer-functions.md`](./gamma-transfer-functions.md) —
  PQ transfer used by both spaces.
- **Companion**: [`tone-mapping-operators.md`](./tone-mapping-operators.md) —
  the HDR → SDR pipeline.
