# Color Quantization — Math

Reduce a continuous color distribution to $K$ representative colors. The
fundamental primitive for **extracting palettes from photos**, **rendering
to limited-color outputs** (8-bit GIF, retro game consoles), and
**clustering CSS token candidates** by perceptual proximity.

---

## TL;DR

**k-means clustering in OKLab** is the modern default:

1. Initialize $K$ centroids (k-means++ for good starting points).
2. Assign each input point to its nearest centroid.
3. Update each centroid to the mean of its assigned points.
4. Repeat until centroids stop moving.

OKLab makes "nearest" perceptually meaningful (Euclidean distance there ≈
ΔE_ok). RGB k-means produces visually inferior palettes.

Alternative algorithms: octree (faster, less optimal), median-cut (fast,
classical), Wu's quantizer (optimal variance reduction).

---

## Natural-language description

### The problem

You have an image with millions of colors. You want 8 colors that "best
represent" it. What does "best" mean?

The standard objective is **total perceptual distance minimization**:

$$
\min_{\{C_1, \ldots, C_K\}} \sum_{x \in \text{input}} \min_k \|x - C_k\|^2
$$

This is the k-means objective. It's NP-hard in general but Lloyd's
algorithm (the standard iterative k-means) converges to a local optimum
quickly.

### Why OKLab matters

Distance in RGB-space doesn't match perceived difference. Two greens that
look identical might be RGB-distant; two browns that look very different
might be RGB-close. k-means in RGB minimizes the wrong objective.

OKLab is perceptually uniform — Euclidean distance there approximates
ΔE_ok. k-means in OKLab minimizes total perceived error, producing palettes
that look correct.

### Alternative algorithms

- **Octree quantization**: builds an 8-way tree of color cubes. Fast,
  deterministic. Good for low-K (≤256). Less perceptually accurate than
  k-means but ~10× faster.
- **Median cut**: recursive bisection. Heath (1980). Used by ImageMagick.
- **Wu's quantizer**: optimizes variance in CIELab. Better than median cut.

For UI/design palette extraction (K = 5-12), k-means in OKLab wins.

---

## Formulas

### k-means objective

$$
J = \sum_{i=1}^{n} \| x_i - C_{a(i)} \|^2
$$

where $a(i)$ is the index of the centroid assigned to point $x_i$.

### Lloyd's iteration

**Assignment step**: each point is assigned to its nearest centroid.

$$
a(i) = \arg\min_k \| x_i - C_k \|^2
$$

**Update step**: each centroid moves to the mean of its assigned points.

$$
C_k = \frac{1}{|S_k|} \sum_{i \in S_k} x_i, \qquad S_k = \{i \mid a(i) = k\}
$$

Iterate until $\max_k \| C_k^{\text{new}} - C_k^{\text{old}} \| < \epsilon$.

### k-means++ initialization (Arthur & Vassilvitskii 2007)

Naive random initialization can converge to poor local optima. k-means++
spreads initial centroids:

1. Pick the first centroid uniformly at random from the input.
2. For each subsequent centroid, pick a point $x$ with probability
   proportional to $\min_k \|x - C_k\|^2$ — favoring distant points.

This gives a $O(\log K)$-competitive guarantee against the optimal solution.

---

## Implementation

Canonical TypeScript: [`src/quantize/kmeans.ts`](../../../../color-science-project-files/src/quantize/kmeans.ts).

Exports:
- `quantize(points: OKLab[], opts: { k, maxIterations?, tolerance?, seed? })`
- `quantizeFromXYZ(xyz[], opts)` — convenience wrapper

```ts
export function quantize(
  points: ReadonlyArray<OKLab>,
  opts: QuantizeOptions
): QuantizeResult {
  let centroids = pickInitial(points, opts.k, opts.seed ?? 0);
  let assignments = points.map(p => nearestCentroidIndex(p, centroids));

  for (let iter = 0; iter < (opts.maxIterations ?? 50); iter++) {
    // Update step: new centroid = mean of assigned points
    const sums = centroids.map(() => [0, 0, 0]);
    const counts = new Array(opts.k).fill(0);
    for (let p = 0; p < points.length; p++) {
      const idx = assignments[p];
      sums[idx][0] += points[p][0];
      sums[idx][1] += points[p][1];
      sums[idx][2] += points[p][2];
      counts[idx]++;
    }
    const newCentroids = sums.map((s, i) => oklab(s[0]/counts[i], s[1]/counts[i], s[2]/counts[i]));

    // Convergence check
    const maxMovement = /* ... */;

    centroids = newCentroids;
    assignments = points.map(p => nearestCentroidIndex(p, centroids));
    if (maxMovement < (opts.tolerance ?? 1e-6)) break;
  }

  return { palette: centroids, assignments, error, iterations };
}
```

Deterministic via seeded LCG for reproducibility. Test vectors verify
cluster recovery on synthetic data and same-seed determinism.

---

## Typical workflow

```ts
import { quantizeFromXYZ } from '../quantize/kmeans.js';
import * as srgb from '../spaces/srgb.js';
import * as srgbTransfer from '../transfer/srgb.js';

// 1. Load image pixels (in any format) → encoded sRGB
const pixels: EncodedSRGB[] = [/* ... */];

// 2. Decode gamma and convert to XYZ (one-time per pixel)
const xyzPixels = pixels.map(p => srgb.toXYZ(srgbTransfer.decode(p)));

// 3. Quantize to K colors in OKLab
const { palette } = quantizeFromXYZ(xyzPixels, { k: 8, seed: 42 });

// 4. palette is an OKLab[] — convert back to sRGB for display
```

---

## Edge cases

- **K > unique colors**: returns one centroid per unique color plus
  duplicates. Not useful; check input cardinality.
- **All same color**: degenerate. All centroids converge to that color.
- **Empty cluster**: a centroid that gets no assignments. The
  implementation keeps it; some variants re-seed from the farthest point.
- **Local optima**: Lloyd's is greedy. k-means++ helps but doesn't
  guarantee global optimum. Run multiple seeds and pick lowest error if
  needed.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/quantize/kmeans.ts` — k-means++ in OKLab, deterministic. |
| **colorgram.py** | <https://github.com/obskyr/colorgram.py> — histogram-based; ~15ms for 340×340. |
| **node-vibrant** | Median cut, used by Material Design Color Generator. |
| **RgbQuant.js** | Octree + KD-tree; ~ImageMagick-equivalent. |

---

## Primary sources

- **Lloyd, S. (1957)** — "Least squares quantization in PCM," published 1982,
  *IEEE Trans. Info. Theory* 28(2).
- **Arthur, D. & Vassilvitskii, S. (2007)** — "k-means++: The advantages
  of careful seeding," *SODA '07*.
- **Wu, X. (1992)** — "Color quantization by dynamic programming and
  principal analysis," *ACM TOG* 11(4).
- **Heath, M. & Sherwood, M. (1980)** — median cut algorithm.
- **Companion**: [`delta-e-formulas.md`](./delta-e-formulas.md) — distance
  metric used for cluster assignment.
