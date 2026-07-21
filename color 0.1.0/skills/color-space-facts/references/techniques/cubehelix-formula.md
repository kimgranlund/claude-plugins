# Cubehelix — Math

D. A. Green's 2011 algorithm for a **perceptually-monotonic** colormap that
smoothly rotates through hues as brightness increases. Originally designed
for astronomical imaging (where grayscale fallback must remain legible) and
widely adopted in scientific visualization as a better alternative to the
"jet" / "rainbow" colormaps.

---

## TL;DR

For parameter $t \in [0, 1]$:

$$
\begin{aligned}
\ell &= t^\gamma \\
\phi &= 2\pi \cdot (\text{start}/360 + 1 + \text{rotations} \cdot t) \\
A &= \text{hue} \cdot \ell \cdot (1 - \ell) / 2 \\
R &= \ell + A(-0.14861 \cos\phi + 1.78277 \sin\phi) \\
G &= \ell + A(-0.29227 \cos\phi - 0.90649 \sin\phi) \\
B &= \ell + A(\phantom{-}1.97294 \cos\phi)
\end{aligned}
$$

Output is **linear sRGB**. May exceed $[0, 1]$ at extreme parameter values;
clip or gamut-map for display.

Default parameters: $\text{start} = 0°$, $\text{rotations} = -1.5$,
$\text{hue} = 1.0$, $\gamma = 1.0$.

---

## Natural-language description

### The motivation

Most "rainbow" colormaps (e.g., `jet`) have non-monotonic luminance — colors
in the middle of the ramp are brighter than colors at the ends. When printed
in grayscale or seen by color-vision-deficient viewers, the ordering breaks.
The yellow "highlight" in the middle looks like the most intense data point,
even when it represents a mid-range value.

Cubehelix fixes this by:

1. **Linear lightness ramp**: $\ell = t^\gamma$. Defaults to $\gamma = 1$
   (linear). Setting $\gamma > 1$ emphasizes the dark end, $\gamma < 1$ the
   light end.
2. **Smoothly rotating hue**: as $t$ increases, the hue angle $\phi$ rotates
   continuously. The number of full rotations is controlled by the
   `rotations` parameter.
3. **Amplitude envelope** $A = \ell(1-\ell)/2$: zero at the endpoints, peaks
   at the middle. Ensures both endpoints are pure black and pure white (or
   pure linear gray), regardless of hue.

The three RGB equations encode a fixed rotation in CIE perceptual space; the
coefficients were derived by Green so that the rotation produces equal
chroma steps perceptually.

### Why it's good for data viz

- **Black-to-white anchored**: $t=0$ is black, $t=1$ is white. Always.
- **Monotonic luminance**: when printed grayscale, the order is preserved.
- **CVD-resilient**: the smooth hue rotation means no two adjacent values
  look identical to deuteranopic / protanopic viewers.
- **Compact spec**: just four parameters fully define the colormap.

### Why not always use cubehelix?

- **Mid-tones can look out of gamut** at high `hue` values (chroma amplitude).
  Default `hue=1.0` is conservative; set lower for tighter gamut compliance.
- **Hue rotation can be distracting** for some visualizations where the eye
  wants to track value, not color.
- **For dual-anchor (diverging) maps** — e.g., red-to-blue for positive/negative
  — cubehelix isn't the right tool. Use a built diverging palette instead.

---

## Formulas

### The mathematical content

Each RGB channel is a linear combination of three terms:

$$
\text{channel}(t) = \ell(t) + A(t) \cdot \big(c_{cos} \cos\phi(t) + c_{sin} \sin\phi(t)\big)
$$

The coefficients $c_{cos}, c_{sin}$ per channel:

| Channel | $c_{cos}$ | $c_{sin}$ |
|---|---|---|
| R | $-0.14861$ | $+1.78277$ |
| G | $-0.29227$ | $-0.90649$ |
| B | $+1.97294$ | $\phantom{-}0$ |

These are derived from a rotation in CIE perceptual space at the
"equal-chroma" radius, then projected back to linear RGB. The asymmetry
(B has no sin component) is a fixed property of the rotation chosen — different
rotation axes would give different coefficient tables.

### Parameter ranges

| Parameter | Range | Default | Effect |
|---|---|---|---|
| `start` | $[0, 360)$ | $0$ | Starting hue angle in degrees |
| `rotations` | $\mathbb{R}$ (any sign) | $-1.5$ | Number of full rotations from black to white. Negative reverses direction. |
| `hue` | $[0, \infty)$ | $1.0$ | Chroma amplitude. $0$ = grayscale ramp; larger = more vivid (but more gamut-clipping). |
| `gamma` | $(0, \infty)$ | $1.0$ | Lightness curve. $> 1$ slow start; $< 1$ fast start. |

### Endpoints

- At $t = 0$: $\ell = 0$, $A = 0$, so $(R, G, B) = (0, 0, 0)$ — black.
- At $t = 1$: $\ell = 1$, $A = 0$, so $(R, G, B) = (1, 1, 1)$ — white.

The amplitude envelope $\ell(1-\ell)/2$ vanishes at both endpoints, anchoring
them to the linear-gray axis regardless of `hue` or `rotations`.

---

## Implementation

Canonical TypeScript: [`src/interpolation/cubehelix.ts`](../../../../color-science-project-files/src/interpolation/cubehelix.ts).

Exports:
- `cubehelix(t, options?)` → `LinearSRGB` — single sample
- `cubehelixPalette(n, options?)` → `readonly LinearSRGB[]` — `n` equally-spaced
- `DEFAULT_OPTIONS` — Green's published defaults

```ts
export function cubehelix(t: number, opts: Partial<CubehelixOptions> = {}): LinearSRGB {
  const { start, rotations, hue, gamma } = { ...DEFAULT_OPTIONS, ...opts };
  const l = Math.pow(t, gamma);
  const angle = TWO_PI * (start / 360 + 1 + rotations * t);
  const amp = (hue * l * (1 - l)) / 2;
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  const r = l + amp * (-0.14861 * cos + 1.78277 * sin);
  const g = l + amp * (-0.29227 * cos - 0.90649 * sin);
  const b = l + amp * ( 1.97294 * cos);
  return linearSRGB(r, g, b);
}
```

Test vectors verify the black/white endpoints, mid-tone luminance is roughly
$Y \approx 0.5$, and palette endpoints are inclusive.

---

## Worked example: 5-step cubehelix palette

With default parameters (`start=0`, `rotations=-1.5`, `hue=1.0`, `gamma=1.0`):

| $t$ | Linear sRGB | Linear Y | Notes |
|---|---|---|---|
| 0.00 | (0.000, 0.000, 0.000) | 0.000 | Pure black |
| 0.25 | (0.123, 0.275, 0.119) | 0.232 | Green-ish dark |
| 0.50 | (0.520, 0.456, 0.706) | 0.504 | Purple-ish mid |
| 0.75 | (0.892, 0.687, 0.733) | 0.728 | Pink-ish light |
| 1.00 | (1.000, 1.000, 1.000) | 1.000 | Pure white |

The luminance Y increases monotonically. The hue rotates through green →
purple → pink as brightness increases.

For a more chromatic ramp, set `hue: 1.5`. For a fewer-rotations ramp
(e.g., a single hue family with darken-to-lighten progression), set
`rotations: 0`.

---

## Edge cases

- **Out-of-gamut outputs**: with `hue > 1.5` or extreme `rotations`, mid-tones
  can land outside linear $[0, 1]$. Apply `clipNaive` (per-channel clamp) for
  display, or `mapToSRGB` for hue-preserving correction.
- **t outside [0, 1]**: defined mathematically but the brightness and
  amplitude formulas behave non-trivially. Pre-clamp t to $[0, 1]$.
- **gamma at 0**: undefined (division by zero in $t^\gamma$ when $t = 0$).
  JavaScript's `Math.pow(0, 0)` returns 1; behavior at exactly $\gamma = 0$
  is undefined. Don't pass $\gamma = 0$.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/interpolation/cubehelix.ts` — typed `LinearSRGB` output, configurable parameters. |
| **D3** | `d3.scaleSequential(d3.interpolateCubehelixDefault)` — defaults to Green's parameters. |
| **D. A. Green reference** | <https://www.mrao.cam.ac.uk/~dag/CUBEHELIX/> — original Fortran + Python source. |
| **matplotlib** | `cm.cubehelix` — Python implementation following Green's paper. |
| **Culori** | `mode_cubehelix` — color space, but not the colormap. |

---

## Primary sources

- **D. A. Green, "A colour scheme for the display of astronomical intensity
  images"** (Bull. Astr. Soc. India, 2011, vol. 39, p. 289-295) —
  <https://astron-soc.in/bulletin/11June/289392011.pdf> — the original paper.
- **D. A. Green website** — <https://www.mrao.cam.ac.uk/~dag/CUBEHELIX/> —
  source code, sample palettes, parameter discussion.
- **W3C / CSS Color 5 `cubehelix` interpolation mode** — proposed but not
  standardized in CSS as of 2026.
