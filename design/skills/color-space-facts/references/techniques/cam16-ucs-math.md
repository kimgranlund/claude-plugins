# CAM16-UCS — Math

The **Uniform Colour Space** companion to CIECAM16. Transforms CAM16's
$(J, M, h)$ — which are perceptually meaningful but **not Euclidean** —
into Cartesian $(J', a', b')$ where Euclidean distance approximates
perceptual difference. The CIE TC 8-11-recommended uniform colour space.

**Use for**: $\Delta E_{\text{CAM16}}$ color-difference metric, palette
generation in CAM16's perceptual space, cross-illuminant uniform comparisons.

---

## TL;DR

$$
\begin{aligned}
J' &= \frac{(1 + 100 c_1) J}{1 + c_1 J} \\
M' &= \frac{1}{c_2} \ln(1 + c_2 M) \\
a' &= M' \cos h \\
b' &= M' \sin h
\end{aligned}
$$

with $c_1 = 0.007$, $c_2 = 0.0228$ (Li et al. 2017).

$\Delta E_{\text{CAM16}}(\mathbf{p}, \mathbf{q}) = \sqrt{(J'_p - J'_q)^2 + (a'_p - a'_q)^2 + (b'_p - b'_q)^2}$.

**Inverse**:

$$
J = \frac{J'}{1 + c_1 (100 - J')}, \quad
M = \frac{e^{c_2 M'} - 1}{c_2}, \quad
h = \text{atan2}(b', a')
$$

---

## Natural-language description

### The uniformity problem

CIECAM16's $(J, M, h)$ are perceptually meaningful but they're not
**equidistant** — i.e., equal Euclidean steps in $(J, M, h)$ space do not
correspond to equal perceived color differences. Two issues:

1. **$J$ scaling is nonlinear in perception**: a $J$ step from 50 to 60
   doesn't look the same as from 90 to 100.
2. **$(M, h)$ is polar**: Euclidean distance in $(M, h)$ doesn't even make
   sense (mixing colorfulness with angle).

CAM16-UCS rescales $J$ via a hyperbolic curve, log-compresses $M$, and
converts the polar $(M, h)$ to Cartesian $(a', b')$. The result $(J', a', b')$
has approximately uniform perceptual spacing — Euclidean distance gives a
reliable color-difference metric.

### Why $c_1 = 0.007$ and $c_2 = 0.0228$

These constants were derived by Li et al. (2017) by fitting the CAM16
output to experimental color-difference datasets (the same data that
informed CIEDE2000). The fit produces $\Delta E_{\text{CAM16}}$ values
that correlate well with perceived differences in psychophysical tests.

### Compared to ΔE2000 and ΔE_ok

| Metric | Space | When optimal |
|---|---|---|
| **ΔE_ok** | OKLab | Modern UI design tokens, palettes |
| **ΔE2000** | CIELAB + corrections | Print, textile, ICC pipelines |
| **ΔE_CAM16** | CAM16-UCS | Cross-viewing-condition work; specifies VC explicitly |

For UI work that lives at D65 on a display, ΔE_ok is the cheaper and equally
accurate choice. ΔE_CAM16 matters when viewing conditions are an explicit
input (cross-illuminant rendering, soft-proofing).

---

## Formulas

### Forward: $(J, M, h)$ → $(J', a', b')$

$$
J' = \frac{(1 + 100 c_1) J}{1 + c_1 J}
$$

This is a hyperbolic rescaling. At $J = 0$, $J' = 0$; at $J = 100$, $J' = 100$.
In between, the curve is slightly compressed near both ends, expanded in the
middle.

$$
M' = \frac{1}{c_2} \ln(1 + c_2 M)
$$

Log-compression of colorfulness. For small $M$ (low chroma), $M' \approx M$.
For large $M$, $M'$ grows much slower — matching the diminishing-returns
character of perceived colorfulness.

$$
a' = M' \cos h, \quad b' = M' \sin h
$$

Standard polar-to-Cartesian (with $h$ in radians).

### Inverse: $(J', a', b')$ → $(J, M, h)$

$$
J = \frac{J'}{1 + c_1 (100 - J')}
$$

Invert the hyperbolic rescaling. Same fixed points $0 \leftrightarrow 0$,
$100 \leftrightarrow 100$.

$$
M' = \sqrt{(a')^2 + (b')^2}, \quad M = \frac{e^{c_2 M'} - 1}{c_2}
$$

Cartesian → polar gives $M'$, then invert the log compression to get $M$.

$$
h = \text{atan2}(b', a') \quad (\text{degrees in } [0, 360))
$$

### ΔE_CAM16

$$
\Delta E_{\text{CAM16}}(p, q) = \sqrt{(J'_p - J'_q)^2 + (a'_p - a'_q)^2 + (b'_p - b'_q)^2}
$$

Euclidean in $(J', a', b')$. Same form as ΔE76 in CIELAB or ΔE_ok in OKLab,
but operating in the uniformity-adjusted CAM16 space.

---

## Implementation

Canonical TypeScript: [`src/spaces/cam16-ucs.ts`](../../../../color-science-project-files/src/spaces/cam16-ucs.ts).

Exports:
- `fromJMh(jmh: CIECAM16_JMh): CAM16_UCS` — direct from JMh
- `toJMh(ucs: CAM16_UCS): CIECAM16_JMh` — inverse
- `fromXYZ(xyz)`, `toXYZ(ucs)` — hub conversion through CIECAM16
- `deltaECAM16(a, b): number` — Euclidean distance in UCS

```ts
const C1 = 0.007;
const C2 = 0.0228;

export function fromJMh(jmh: CIECAM16_JMh): CAM16_UCS {
  const [J, M, hDeg] = jmh;
  const Jp = ((1 + 100 * C1) * J) / (1 + C1 * J);
  const Mp = (1 / C2) * Math.log(1 + C2 * M);
  const hRad = wrapHueDeg(hDeg) * DEG_TO_RAD;
  return [Jp, Mp * Math.cos(hRad), Mp * Math.sin(hRad)] as unknown as CAM16_UCS;
}

export function deltaECAM16(a: CAM16_UCS, b: CAM16_UCS): number {
  const dJ = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return Math.sqrt(dJ * dJ + dA * dA + dB * dB);
}
```

Test vectors verify the black-point round-trip (J=M=0 → J'=a'=b'=0).

---

## CAM16-LCD and CAM16-SCD variants

The CAM16 family includes three uniform spaces beyond CAM16-UCS:

| Variant | $c_1$ | $c_2$ | Use |
|---|---|---|---|
| **CAM16-UCS** | 0.007 | 0.0228 | General uniformity (default; this skill) |
| **CAM16-LCD** | 0.0067 | 0.0363 | Large-difference judgment |
| **CAM16-SCD** | 0.0078 | 0.0233 | Small-difference judgment |

For palette work and general design, CAM16-UCS is the right default. The LCD
and SCD variants are calibrated for specific psychophysical tasks (rating
large or small differences); rarely needed for design.

---

## Edge cases

- **Black point**: $J = M = 0 \to J' = 0, M' = 0 \to a' = b' = 0$.
- **Hue indeterminacy at $M = 0$**: $h$ is undefined; $\text{atan2}(0, 0) = 0$.
  Round-trip works but the hue value is meaningless.
- **Very high $M$**: $M'$ saturates due to log compression. The inverse
  recovers via the exponential.
- **Mixing viewing conditions**: $\Delta E_{\text{CAM16}}$ is meaningful only
  when both colors are computed under the same VC. The metric loses calibration
  otherwise.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/cam16-ucs.ts` — branded types, ΔE_CAM16 metric. |
| **Material color-utilities** | Has CAM16 conversions but not the UCS form as a first-class space. |
| **Culori** | `mode_cam16_jch` for CAM16 polar; UCS variant via composition. |
| **Color.js** | Limited CAM16-UCS support; cross-checks against the spec. |
| **Reference Python** | Mark Fairchild's CIECAM16 / CAM16-UCS reference at <https://www.rit.edu/cos/colorscience/rc_useful_data.php>. |

---

## Primary sources

- **Li, Li, Wang, Cui, Luo, Melgosa, Brill, Pointer (2017)** — "Comprehensive
  color solutions: CAM16, CAT16, and CAM16-UCS," *Color Research & Application*
  42(6), 703–718. The defining paper for CAM16-UCS and its constants.
- **CIE 248:2022** — *CIE 2016 Colour Appearance Model for Colour Management
  Systems: CIECAM16*. Normative reference for CIECAM16; CAM16-UCS appears in
  Annex A.
- **CIE TC 8-11** — recommends CAM16-UCS as the official Uniform Colour Space
  for colour management.
- **Companion**: [`ciecam16-forward-inverse.md`](./ciecam16-forward-inverse.md) —
  the CIECAM16 step that feeds CAM16-UCS.
- **Companion**: [`delta-e-formulas.md`](./delta-e-formulas.md) — comparison
  with ΔE76, ΔE94, ΔE2000, ΔE_ok.
