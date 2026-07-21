# Dithering Algorithms — Math

Map a continuous-tone source to a limited palette while preserving
**average perceived color** through controlled noise. The classic problem
of 8-bit display, low-bit retro art, halftone printing, and any output
constrained to fewer colors than the source.

---

## TL;DR

**Floyd-Steinberg** is the default error-diffusion algorithm. For each
pixel:
1. Find nearest palette color, output it.
2. Compute quantization error.
3. Distribute error to right + below neighbors with weights
   $(7/16, 3/16, 5/16, 1/16)$.

Operate in **OKLab** so error is perceptually meaningful.

Alternatives: **Bayer / ordered dithering** (deterministic threshold
matrix, no error propagation), **blue noise** (precomputed noise patterns
with even spectral distribution).

---

## Natural-language description

### The problem

Quantizing each pixel to the nearest palette color produces banding,
posterization, and visible color shifts in gradients. Dithering trades
spatial noise for tonal accuracy: each output pixel is wrong (it's a
palette member, not the true color), but **regions of pixels average to
the right color**.

### Error diffusion (Floyd-Steinberg)

For each pixel in raster (left-to-right, top-to-bottom) order:
1. Find the nearest palette color and output it.
2. Compute the error = (true color − palette color).
3. Diffuse that error into the input buffer for not-yet-processed neighbors.

By the time you reach a pixel, it has accumulated errors from previous
pixels — biasing its choice toward correcting their quantization.

The standard Floyd-Steinberg distribution:

```
                  *   7/16
          3/16  5/16  1/16
```

(Where `*` is the just-processed pixel.) These weights sum to 1.

### Ordered (Bayer) dithering

Add a deterministic threshold matrix to the input before quantizing. The
matrix is sized $2^n \times 2^n$ and contains a recursive pattern. The
result has a characteristic crosshatch / dotted texture but is
parallelizable (each pixel decided independently).

The Bayer matrix has minimal worst-case threshold deviation but
visible regular patterns.

### Blue noise

Pre-computed noise textures with **spectral distribution biased to high
frequencies** (no low-frequency clumps). Adds error like ordered dithering
but the spatial noise pattern is closer to white noise (no visible regular
grids).

Tradeoff: needs pre-computed noise textures; can't be derived from a
formula. But result quality is excellent.

---

## Formulas

### Floyd-Steinberg error diffusion

Let $S(x, y)$ be the source, $P$ a palette function returning the nearest
palette color, and $D(x, y)$ the diffusion buffer (initially $D = S$):

```
for each (x, y) in raster order:
    out(x, y) = P(D(x, y))                    // nearest palette
    err = D(x, y) − out(x, y)                  // quantization error
    D(x+1, y)   += err · 7/16
    D(x-1, y+1) += err · 3/16
    D(x, y+1)   += err · 5/16
    D(x+1, y+1) += err · 1/16
```

The error is a 3-component value (OKLab L, a, b) diffused per channel.

### Bayer 4×4 threshold matrix

$$
M_{\text{Bayer4}} = \frac{1}{16}
\begin{bmatrix}
0  & 8  & 2  & 10 \\
12 & 4  & 14 & 6 \\
3  & 11 & 1  & 9 \\
15 & 7  & 13 & 5
\end{bmatrix}
$$

Add $M_{\text{Bayer4}}(x \bmod 4, y \bmod 4) - 0.5$ to each pixel's
lightness before quantizing.

### Floyd-Steinberg variants

- **Stucki**: distributes over a larger neighborhood (8/42, 4/42, 2/42).
- **Sierra**: similar 5×3 distribution.
- **Atkinson** (used on early Mac displays): only diffuses 75% of error,
  produces lighter output.

---

## Implementation

Canonical TypeScript: [`src/dithering/floyd-steinberg.ts`](../../../../color-science-project-files/src/dithering/floyd-steinberg.ts).

Exports `ditherFloydSteinberg(source, palette)` which takes an `OkLabImage`
(2D array of `OKLab` values) and an `OKLab[]` palette, returns:
- `indices[y][x]`: which palette color each pixel was mapped to
- `dithered[y][x]`: the actual OKLab color at each pixel (for direct
  display or further processing)

```ts
export function ditherFloydSteinberg(
  source: OkLabImage,
  palette: ReadonlyArray<OKLab>
): { indices: number[][]; dithered: OKLab[][] } {
  const buf = source.map(row => row.map(c => oklab(c[0], c[1], c[2])));
  // ... iterate, distribute error ...
}
```

Test vectors verify:
- Single-color palette maps every pixel to that color.
- Error preservation: average dithered value ≈ average source value (the
  whole point of dithering).

---

## Typical workflow

```ts
import * as kmeans from '../quantize/kmeans.js';
import { ditherFloydSteinberg } from '../dithering/floyd-steinberg.js';

// 1. Quantize: find an N-color palette via k-means
const { palette } = kmeans.quantize(sourceOklabPixels, { k: 16 });

// 2. Dither: map every pixel to a palette index with error diffusion
const { indices, dithered } = ditherFloydSteinberg(sourceImage, palette);

// 3. indices[y][x] gives the palette index for each pixel
//    dithered[y][x] gives the OKLab color at that pixel
```

This is the standard quantize + dither pipeline used by GIF encoders, 8-bit
retro game asset tools, and any "give me a stylized N-color rendering"
feature.

---

## Edge cases

- **Source out of palette range**: error grows unbounded near the
  boundary. Clamp inputs.
- **Single-channel error vs full OKLab**: this implementation diffuses
  errors in all three OKLab components. Some game-asset tools diffuse
  only L (luminance), keeping chroma unchanged.
- **Bayer regular pattern**: visible at sharp viewing angles. Use blue
  noise for higher quality at the cost of pre-computation.
- **Raster order bias**: Floyd-Steinberg's standard left-to-right /
  top-to-bottom order creates a faint diagonal grain. Serpentine scan
  (alternate left-to-right and right-to-left) reduces this.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/dithering/floyd-steinberg.ts` — OKLab error diffusion. |
| **canvas-quantize-2** | Floyd-Steinberg + median-cut in browser. |
| **ImageMagick** | `-dither FloydSteinberg`, `-dither Riemersma`, etc. |
| **GIMP** | Floyd-Steinberg standard or normal/positioned dither modes. |

---

## Primary sources

- **Floyd, R.W. & Steinberg, L. (1976)** — "An adaptive algorithm for
  spatial grayscale," *Proc. SID* 17(2), 75-77.
- **Bayer, B. E. (1973)** — "An optimum method for two-level rendition
  of continuous-tone pictures," *IEEE ICC '73*.
- **Ulichney, R. (1987)** — *Digital Halftoning*, MIT Press.
- **Companion**: [`color-quantization-math.md`](./color-quantization-math.md) —
  generates the palette that dithering then maps onto.
