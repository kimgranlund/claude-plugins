# Color Vision Deficiency Simulation — Math

The three published algorithms for simulating how colors appear to viewers
with **dichromatic** color vision deficiencies (no L-cones / no M-cones /
no S-cones). All three are physiologically grounded; they differ in
mathematical structure and computational cost.

For accessibility tooling, design review, and palette validation, **Machado
2009 is the modern default** — it's what Chrome DevTools uses.

---

## TL;DR

| Algorithm | Year | Structure | When to use |
|---|---|---|---|
| **Brettel** | 1997 | LMS confusion-line plane projection | Highest accuracy; foundational reference |
| **Viénot-Mollon-Brettel** | 1999 | Single 3×3 matrix (simplified Brettel) | Legacy systems; fast but less accurate |
| **Machado-Oliveira-Fernandes** | 2009 | Severity-parameterized 3×3 matrix | **Modern default** — what Chrome DevTools uses |

CVD types simulated by all three:
- **Protanopia** — no L-cones (~1% of males)
- **Deuteranopia** — no M-cones (~1% of males)
- **Tritanopia** — no S-cones (rare)

Anomalous trichromacies (protanomaly, deuteranomaly, tritanomaly) have
shifted cone sensitivities and are typically simulated by interpolating
between the identity (severity=0) and the dichromat matrix (severity=1).

---

## Natural-language description

### The biology

Normal human color vision is **trichromatic**: three cone classes (L = long,
M = medium, S = short wavelength) provide three independent signals to the
brain. A dichromat is missing one cone class — they see in 2D color rather
than 3D.

Each cone class has a characteristic spectral sensitivity curve. CVD
simulation maps the input color through the dichromat's reduced color
space and back, producing an image that approximates what the dichromat
sees.

### Brettel 1997 — the foundational algorithm

Brettel, Viénot, and Mollon (1997) published the first rigorous CVD
simulation. The algorithm:

1. Convert input RGB → linear RGB → CIE XYZ → LMS (Smith-Pokorny cone
   fundamentals).
2. For each dichromat type, identify the **two half-planes** in LMS space
   that contain the perceived colors. The boundary is the line through
   equal-energy white (LMS where L = M = S).
3. **Project** the input LMS onto one of these planes (chosen by which
   side of the boundary the input falls on).
4. Convert back: LMS → XYZ → linear RGB → RGB.

The planes are defined by three "anchor" colors per deficiency type —
known wavelengths where the dichromat's perception is unambiguous (e.g.,
475 nm for the cool side of protanopia/deuteranopia).

Pros: accurate, physiologically defensible.
Cons: requires plane-selection logic per pixel, plus the LMS round-trip.

### Viénot 1999 — the simplified version

Two years later, Viénot, Brettel, and Mollon (1999) showed that **a single
3×3 matrix per dichromat type** captures most of the visual effect with
much simpler math. The matrix combines:

- RGB → LMS conversion
- Confusion-line collapse
- LMS → RGB inverse

into one linear transform. Less accurate than the full Brettel algorithm
(particularly for the protanopia/deuteranopia split-plane case) but fast
and good enough for screen-rendering purposes.

### Machado 2009 — the modern default

Machado, Oliveira, and Fernandes (2009) refined Viénot's approach with:

- **Severity parameter**: instead of binary "deficient" or "normal," produce
  a continuous spectrum from 0 (identity) to 1 (full deficiency).
- **Updated cone fundamentals**: based on Stockman-Sharpe 2-degree cone
  responses, more accurate than Smith-Pokorny.
- **Published table of 33 matrices**: 3 deficiency types × 11 severities
  (0.0, 0.1, ..., 1.0). The matrix at intermediate severities is NOT a
  linear interpolation of the endpoints — the paper publishes each
  intermediate matrix explicitly.

Chrome DevTools' "Emulate vision deficiencies" feature uses Machado's
severity-1.0 matrices. Most CVD-simulation libraries default to these.

---

## Formulas

### Machado 2009 — Protanopia (severity 1.0)

$$
M_{\text{protanopia}} =
\begin{bmatrix}
\phantom{-}0.152286 & \phantom{-}1.052583 & -0.204868 \\
\phantom{-}0.114503 & \phantom{-}0.786281 & \phantom{-}0.099216 \\
-0.003882 & -0.048116 & \phantom{-}1.051998
\end{bmatrix}
$$

### Machado 2009 — Deuteranopia (severity 1.0)

$$
M_{\text{deuteranopia}} =
\begin{bmatrix}
\phantom{-}0.367322 & \phantom{-}0.860646 & -0.227968 \\
\phantom{-}0.280085 & \phantom{-}0.672501 & \phantom{-}0.047413 \\
-0.011820 & \phantom{-}0.042940 & \phantom{-}0.968881
\end{bmatrix}
$$

### Machado 2009 — Tritanopia (severity 1.0)

$$
M_{\text{tritanopia}} =
\begin{bmatrix}
\phantom{-}1.255528 & -0.076749 & -0.178779 \\
-0.078411 & \phantom{-}0.930809 & \phantom{-}0.147602 \\
\phantom{-}0.004733 & \phantom{-}0.691367 & \phantom{-}0.303900
\end{bmatrix}
$$

### Application

For a linear sRGB input $(R, G, B)$ and deficiency type $T$:

$$
\begin{bmatrix} R' \\ G' \\ B' \end{bmatrix} = M_T \begin{bmatrix} R \\ G \\ B \end{bmatrix}
$$

### Severity parameter (linear approximation)

For severity $s \in [0, 1]$:

$$
M_{T, s} = (1 - s) \cdot I + s \cdot M_T
$$

where $I$ is the identity matrix. **Note**: this is an approximation. The
Machado paper publishes the exact matrix at $s = 0.1, 0.2, \ldots, 1.0$;
the matrices change non-linearly with $s$. For strict-precision intermediate
severities, look up the published table.

### Viénot 1999 matrices (alternative, kept for compatibility)

Operating on linear sRGB directly:

$$
M_{\text{prot,V99}} =
\begin{bmatrix}
0.11238 & 0.88762 & 0 \\
0.11238 & 0.88762 & 0 \\
0 & 0 & 1
\end{bmatrix}, \quad
M_{\text{deut,V99}} =
\begin{bmatrix}
0.29275 & 0.70725 & 0 \\
0.29275 & 0.70725 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

Viénot's matrices are simpler (mathematically rank-2) but less accurate.
Use them for legacy compatibility or low-fidelity preview; prefer Machado
2009 for any modern work.

---

## Implementation

Canonical TypeScript: [`src/cvd/machado-2009.ts`](../../../../color-science-project-files/src/cvd/machado-2009.ts).

Exports:
- `M_PROTANOPIA`, `M_DEUTERANOPIA`, `M_TRITANOPIA` — the three matrices
- `simulationMatrix(type, severity?)` — build matrix for type + severity
- `simulate(rgb, type, severity?)` — apply to a single linear sRGB color
- `simulateProtanopia`, `simulateDeuteranopia`, `simulateTritanopia` — wrappers

```ts
export function simulate(
  rgb: LinearSRGB,
  type: CVDType,
  severity: number = 1.0
): LinearSRGB {
  const M = simulationMatrix(type, severity);
  const [r, g, b] = mulMat3Vec3(M, rgb);
  return linearSRGB(r, g, b);
}
```

Test vectors verify identity at severity=0, achromatic preservation,
white preservation (rows sum to ~1), and the published `simulate(red,
protanopia, 1.0)` value.

### Pipeline: encoded sRGB → CVD-simulated encoded sRGB

```ts
import * as srgbTransfer from '../transfer/srgb.js';
import * as machado from '../cvd/machado-2009.js';

const inputEncoded = encodedSRGB(0.8, 0.2, 0.1);
const inputLinear = srgbTransfer.decode(inputEncoded);
const simulatedLinear = machado.simulateProtanopia(inputLinear);
const simulatedEncoded = srgbTransfer.encode(simulatedLinear);
```

**Always decode gamma first.** Applying CVD matrices to gamma-encoded
values produces wrong results (the matrices assume linear-light input).

---

## Edge cases

- **Out-of-gamut input**: CVD matrices can map in-gamut colors to slightly
  out-of-gamut outputs. Apply `clipNaive` or `mapToSRGB` for display.
- **Severity ≥ 1**: clamped to 1 (full deficiency).
- **Severity ≤ 0**: clamped to 0 (identity).
- **Anomalous trichromacies**: Machado's paper distinguishes between
  dichromacy (no cone class) and anomalous trichromacy (shifted cones).
  This implementation models dichromacy (severity 1.0); anomalous
  trichromacy is approximated by severity < 1.0 — useful for "what
  would a mild deuteranomalic viewer see?" simulations.
- **Severity discontinuity**: the published Machado matrices don't change
  smoothly at intermediate severities. Linear interpolation between
  identity and full produces a defensible but not exact approximation.

---

## Recommended usage for design accessibility review

From the existing positioning doc
([`cvd-simulation-canonical.md`](../contemporary/cvd-simulation-canonical.md)):

1. **Default to deuteranopia** for first-pass review — it's the most common
   deficiency.
2. **Use severity 0.6, not 1.0** for the most common real-world case —
   most CVD viewers have anomalous trichromacy (mild-to-moderate severity),
   not full dichromacy.
3. **Always pair color with non-color cues** — text, shape, position. CVD
   simulation is for catching color-only signals that fail; the fix is
   never "pick different colors" alone.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/cvd/machado-2009.ts` — Machado 2009 with severity parameter. |
| **Chrome DevTools** | "Emulate vision deficiencies" uses Machado severity 1.0. |
| **Culori** | `filterDeficiencyProt`, `filterDeficiencyDeuter`, `filterDeficiencyTrit` (Brettel-based). |
| **color-blind** (npm) | Brettel 1997 implementation. |
| **Color Blindness Simulator** | <https://www.color-blindness.com/coblis-color-blindness-simulator/> — interactive tool using Brettel. |

---

## Primary sources

- **Machado, Oliveira, Fernandes (2009)** — "A Physiologically-based Model
  for Simulation of Color Vision Deficiency," *IEEE TVCG* 15(6), 1291-1298.
  Modern reference; full 33-matrix table.
- **Viénot, Brettel, Mollon (1999)** — "Digital video colourmaps for
  checking the legibility of displays by dichromats," *Color Research &
  Application* 24(4), 243-252.
- **Brettel, Viénot, Mollon (1997)** — "Computerized simulation of color
  appearance for dichromats," *Journal of the Optical Society of America A*
  14(10), 2647-2655.
- **Companion**: [`cvd-simulation-canonical.md`](../contemporary/cvd-simulation-canonical.md) —
  existing overview / positioning doc with usage recommendations.
- **Companion**: [`apca-lc-formula.md`](./apca-lc-formula.md) — APCA
  contrast doesn't model CVD directly, but APCA + CVD simulation together
  catch most accessibility failures.
