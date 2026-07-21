# Tone Mapping Operators — Math

How to compress HDR (high dynamic range) scene-linear values into SDR
displayable values. Required whenever:

- A renderer outputs scene-linear values that exceed display white
  (e.g., a sun, a specular highlight, a bright window)
- A wide-gamut content needs to be displayed on a narrower display
- An HDR pipeline (PQ/HLG-encoded) needs an SDR fallback

Three operators are universal: **Reinhard** (simplest), **ACES filmic**
(industry standard), and **Uncharted 2** (popular game-industry tweak).

---

## TL;DR

| Operator | Formula | When to use |
|---|---|---|
| **Reinhard simple** | $y = x / (1 + x)$ | Quick monotonic compress; never reaches 1 |
| **Reinhard extended** | $y = x(1 + x/W^2) / (1 + x)$ | Map a chosen "white point" $W$ exactly to 1 |
| **Reinhard luminance-preserving** | Compress $Y$ only; scale RGB by gain | Hue preservation at cost of chroma fidelity |
| **ACES filmic (Narkowicz)** | $y = \frac{x(2.51x + 0.03)}{x(2.43x + 0.59) + 0.14}$ | **Modern default for cinema, games, UI** |
| **Uncharted 2** | A 6-parameter rational fit | Game-engine tradition; tunable |

ACES is the modern default. Reinhard remains useful for quick prototyping
and when you need provable mathematical properties.

---

## Natural-language description

### The problem

A render gives you scene-linear values that can exceed 1.0. The sun in an
outdoor scene might have luminance ~5000 cd/m² (peak SDR display ≈ 100 cd/m²,
so ~50× over display white). A specular highlight off a wet surface might be
10–20× display white. Naively clipping to [0, 1] destroys all detail above
display white — clouds disappear, highlights become flat white blobs.

A tone mapping operator (TMO) is a monotonic function $f : [0, \infty) \to
[0, 1)$ (approximately) that:

- Preserves shadow and mid-tone detail (linear in the low range).
- Smoothly compresses highlights (asymptotic to 1.0).
- Produces no banding, no over-/undershooting.

### How operators differ

**Reinhard** (2002): the simplest viable TMO. Just $y = x / (1 + x)$. Always
monotonic; smooth; physically motivated by photographic response. Limitation:
asymptotes to 1.0 but never reaches it — bright scenes look slightly
washed out unless extended with a white-point parameter.

**Reinhard extended**: adds a tunable $W$ (white point) so $f(W) = 1$ exactly.
$W = 4$ typical for 4× SDR overhead.

**ACES filmic** (2014, simplified by Narkowicz 2015): the industry standard.
Approximates the full ACES output transform with a 5-parameter rational
function. Has a characteristic "filmic toe" (slight shadow desaturation that
matches photographic film) and a strong highlight roll-off.

**Uncharted 2** (Hable 2010): 6-parameter rational fit popularized by
Naughty Dog. More tunable than ACES, but tuning is a black art.

### Per-channel vs luminance-preserving

A naive TMO applies $f(x)$ per channel: $R' = f(R)$, $G' = f(G)$, $B' = f(B)$.
This compresses each channel independently, which **desaturates highlights** —
a saturated red highlight gets the R channel compressed (lots of R) while G
and B barely change, so the result is less saturated than the input.

A luminance-preserving TMO computes $Y$ from the input, tone-maps $Y$, then
scales R, G, B by the gain $Y_{out} / Y_{in}$. Preserves hue, but the
chromatic information at extreme brightnesses can exceed display gamut —
needs post-hoc gamut handling.

Per-channel is the default in most production pipelines; the desaturation
is often considered desirable (a "filmic" look).

---

## Formulas

### Reinhard simple (2002)

$$
y = \frac{x}{1 + x}
$$

Maps $[0, \infty) \to [0, 1)$. At $x = 0$: $y = 0$. At $x = 1$: $y = 0.5$. At
$x = 9$: $y = 0.9$. Never reaches $1$.

### Reinhard extended

$$
y = \frac{x \cdot (1 + x/W^2)}{1 + x}
$$

Maps $[0, W] \to [0, 1]$. At $x = W$: $y = 1$ exactly. At $x > W$: $y > 1$
(careful — values above 1 are out of display range; clip post-hoc).

Typical $W = 4$ for moderate overhead. For aggressive highlight preservation
use $W = 8$ or higher.

### Reinhard luminance-preserving

Given input RGB and computed $Y_{in} = \text{luminance}(RGB)$:

$$
Y_{out} = f_{\text{Reinhard}}(Y_{in}), \quad
RGB_{out} = RGB_{in} \cdot \frac{Y_{out}}{Y_{in}}
$$

Preserves hue (chromaticity). May produce $RGB_{out}$ values above 1 in some
channels — apply gamut mapping or clipping afterward.

### ACES filmic (Narkowicz fit)

$$
y = \frac{x \cdot (a \cdot x + b)}{x \cdot (c \cdot x + d) + e}
$$

with constants $a = 2.51$, $b = 0.03$, $c = 2.43$, $d = 0.59$, $e = 0.14$.

Properties:
- At $x = 0$: $y = 0$.
- At $x = 1$ (SDR white): $y \approx 0.80$ — the filmic mid-tone compression.
- As $x \to \infty$: $y \to a/c = 2.51/2.43 \approx 1.033$ (slight overshoot
  above 1; clip for display).

Per-channel application desaturates highlights — a deliberate design choice
matching photographic film.

### Uncharted 2 (Hable)

Hable's 6-parameter form:

$$
y = \frac{x \cdot (A \cdot x + C \cdot B) + D \cdot E}{x \cdot (A \cdot x + B) + D \cdot F} - \frac{E}{F}
$$

with default $A = 0.15$, $B = 0.50$, $C = 0.10$, $D = 0.20$, $E = 0.02$, $F = 0.30$.

A "white point" parameter is then applied: divide by Hable($W$). Often $W = 11.2$.

Not implemented in this skill but documented for reference.

---

## Implementation

Canonical TypeScript:
- [`src/tonemap/reinhard.ts`](../../../../color-science-project-files/src/tonemap/reinhard.ts) — simple, extended,
  luminance-preserving variants
- [`src/tonemap/aces.ts`](../../../../color-science-project-files/src/tonemap/aces.ts) — Narkowicz ACES fit

```ts
// Simple Reinhard
export function reinhardSimple(x: number): number {
  return x / (1 + x);
}

// Extended Reinhard with white point W
export function reinhardExtended(x: number, whitePoint = 4.0): number {
  const W2 = whitePoint * whitePoint;
  return (x * (1 + x / W2)) / (1 + x);
}

// ACES filmic (Narkowicz)
const A = 2.51, B = 0.03, C = 2.43, D = 0.59, E = 0.14;
export function acesNarkowicz(x: number): number {
  return (x * (A * x + B)) / (x * (C * x + D) + E);
}
```

Each module exports the scalar operator plus `applyXxx(rgb)` per-channel
wrappers and `applyLuminancePreserving(rgb, whitePoint?)` where applicable.

Test vectors verify the endpoint behavior and the published mid-point values
(Reinhard simple at $x = 1$ gives 0.5; ACES at $x = 1$ gives ~0.8).

---

## Pipeline: HDR scene-linear → display-ready encoded sRGB

```ts
import * as aces from '../tonemap/aces.js';
import * as srgbTransfer from '../transfer/srgb.js';
import * as gamutMap from '../gamut/mapping.js';

// 1. Scene-linear HDR input (values can exceed 1)
const hdrLinear = linearSRGB(2.5, 1.8, 0.4);  // bright highlight

// 2. Tone map HDR → SDR-linear
const sdrLinear = aces.applyACES(hdrLinear);

// 3. Defensive gamut clip (ACES Narkowicz can slightly overshoot 1)
const clipped = gamutMap.clipNaive(sdrLinear);

// 4. Gamma encode for display
const encoded = srgbTransfer.encode(linearSRGB(clipped[0], clipped[1], clipped[2]));
```

For HDR display output (PQ or HLG encoding), use [`pq.ts`](../../../../color-science-project-files/src/transfer/pq.ts)
or [`hlg.ts`](../../../../color-science-project-files/src/transfer/hlg.ts) instead of sRGB encoding in step 4.

---

## Edge cases

- **Negative input**: defined mathematically for some operators (Reinhard
  simple gives negative output for negative input; ACES does too with
  sensible behavior). For safety, clamp input to $\ge 0$.
- **Highlight overshoot**: ACES Narkowicz asymptotes to ~1.033, not 1.0.
  Apply `clipNaive` post-tone-map for display.
- **White point sensitivity**: extended Reinhard's behavior is very sensitive
  to $W$. $W = 1$ degenerates to simple Reinhard plus a linear term;
  $W \to \infty$ approaches the identity for low $x$.
- **Per-channel desaturation**: applying any per-channel operator to highly
  saturated highlights produces noticeable desaturation. Some pipelines
  blend per-channel and luminance-preserving for a controlled amount of
  saturation loss.
- **Gamut clipping after tone mapping**: tone mapping does not address
  gamut. A wide-gamut HDR scene in Rec.2020 needs both tone mapping AND
  gamut mapping to fit in sRGB.

---

## Comparison: Reinhard vs ACES at common inputs

| Input | Reinhard simple | Reinhard ext (W=4) | ACES Narkowicz |
|---|---|---|---|
| 0.0 | 0.000 | 0.000 | 0.000 |
| 0.18 (mid-gray) | 0.153 | 0.182 | 0.087 |
| 0.5 | 0.333 | 0.375 | 0.302 |
| 1.0 (SDR white) | 0.500 | 0.563 | 0.795 |
| 2.0 | 0.667 | 0.750 | 0.938 |
| 4.0 (extended W) | 0.800 | 1.000 | 0.991 |
| 100 | 0.990 | 13.366 (!) | 1.033 |

Note Reinhard extended **does not clamp at W** — for $x > W$ it produces
$y > 1$, which must be clipped for display. ACES has built-in soft
saturation near 1.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/tonemap/{reinhard,aces}.ts` — scalar + per-channel + luminance-preserving variants. |
| **Three.js** | `THREE.ACESFilmicToneMapping`, `THREE.ReinhardToneMapping` shader uniforms. |
| **Unity** | Built-in tone mappers; `ACES` is the default for HDR pipelines. |
| **Filament** | Reference real-time renderer with multiple TMOs. |
| **OpenColorIO** | Full ACES pipeline (input transforms + RRT + ODT), not just the Narkowicz fit. |

---

## Primary sources

- **Reinhard, Stark, Shirley, Ferwerda (2002)** — "Photographic Tone
  Reproduction for Digital Images," *ACM TOG* 21(3), 267-276. The original
  Reinhard paper.
- **Narkowicz (2015)** — "ACES Filmic Tone Mapping Curve," blog post:
  <https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/> —
  the universal Narkowicz fit used in this skill.
- **Hable (2010)** — "Filmic Tonemapping Operators," blog post:
  <http://filmicworlds.com/blog/filmic-tonemapping-operators/> — the
  Uncharted 2 operator.
- **ACES official** — <https://github.com/ampas/aces-dev> — the full
  Academy ACES reference (RRT, ODTs, IDTs).
- **Companion**: [`gamma-transfer-functions.md`](./gamma-transfer-functions.md) —
  PQ and HLG transfers used for HDR display output.
- **Companion**: [`css-color-4-gamut-mapping.md`](./css-color-4-gamut-mapping.md) —
  post-tone-map gamut handling.
