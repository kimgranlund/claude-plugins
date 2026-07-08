// K-means color quantization in OKLab.
//
// Given a set of input colors, find K representative colors that minimize
// the total perceptual distance (ΔE_ok) between each input and its nearest
// cluster center. The output K colors form a palette that approximates the
// input distribution.
//
// Use cases:
//   - Extract a brand palette from a logo image
//   - Reduce a photo to N colors for stylization or printing
//   - Cluster CSS token candidates to find semantic groups
//
// Why OKLab: clustering needs a perceptually-uniform space so that
// "nearest centroid" matches "looks closest." Euclidean distance in
// OKLab ≈ ΔE_ok, which is well-calibrated for perceptual difference.
//
// Primary source: Lloyd 1957 (original k-means); k-means++ initialization
// from Arthur & Vassilvitskii (2007).

import type { OKLab, XYZ_D65 } from '../types.js';
import { oklab } from '../types.js';
import * as oklabSpace from '../spaces/oklab.js';

// ─── Core k-means in OKLab ────────────────────────────────────────────────────

function distSquared(a: OKLab, b: OKLab): number {
  const dL = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return dL * dL + dA * dA + dB * dB;
}

function nearestCentroidIndex(point: OKLab, centroids: ReadonlyArray<OKLab>): number {
  let bestIdx = 0;
  let bestDist = distSquared(point, centroids[0]);
  for (let i = 1; i < centroids.length; i++) {
    const d = distSquared(point, centroids[i]);
    if (d < bestDist) {
      bestDist = d;
      bestIdx = i;
    }
  }
  return bestIdx;
}

// ─── k-means++ initialization (better convergence than random) ────────────────

function pickInitial(points: ReadonlyArray<OKLab>, k: number, seed: number = 0): OKLab[] {
  // Deterministic LCG for reproducibility
  let state = seed >>> 0;
  const rand = () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 0x100000000;
  };

  const centroids: OKLab[] = [];
  // First centroid: random point
  centroids.push(points[Math.floor(rand() * points.length)]);

  while (centroids.length < k) {
    // Compute squared distance from each point to nearest existing centroid.
    const dists: number[] = points.map(p => {
      let min = Infinity;
      for (const c of centroids) {
        const d = distSquared(p, c);
        if (d < min) min = d;
      }
      return min;
    });
    // Weighted random selection biased toward distant points.
    const total = dists.reduce((s, d) => s + d, 0);
    const target = rand() * total;
    let cum = 0;
    for (let i = 0; i < dists.length; i++) {
      cum += dists[i];
      if (cum >= target) {
        centroids.push(points[i]);
        break;
      }
    }
  }
  return centroids;
}

// ─── Main quantization API ────────────────────────────────────────────────────

export type QuantizeOptions = Readonly<{
  /** Number of palette colors to extract. */
  k: number;
  /** Maximum iterations (default 50). */
  maxIterations?: number;
  /** Convergence tolerance — stop when centroid movement falls below this. */
  tolerance?: number;
  /** Seed for k-means++ initialization (default 0; deterministic). */
  seed?: number;
}>;

export type QuantizeResult = Readonly<{
  /** The K cluster centroids in OKLab — the extracted palette. */
  palette: ReadonlyArray<OKLab>;
  /** Index of the nearest palette color for each input point. */
  assignments: ReadonlyArray<number>;
  /** Final total squared-distance error. */
  error: number;
  /** Number of iterations executed. */
  iterations: number;
}>;

/**
 * Run k-means quantization on a set of OKLab points.
 * Use `quantizeFromXYZ` for XYZ inputs or compose with other space modules.
 */
export function quantize(
  points: ReadonlyArray<OKLab>,
  opts: QuantizeOptions
): QuantizeResult {
  const { k, maxIterations = 50, tolerance = 1e-6, seed = 0 } = opts;
  if (points.length < k) {
    throw new Error(`Cannot quantize ${points.length} points to ${k} clusters`);
  }

  let centroids = pickInitial(points, k, seed);
  let assignments = points.map(p => nearestCentroidIndex(p, centroids));
  let iterations = 0;

  for (; iterations < maxIterations; iterations++) {
    // Update centroids: mean of assigned points.
    const sums: [number, number, number][] = centroids.map(() => [0, 0, 0]);
    const counts: number[] = new Array(k).fill(0);
    for (let p = 0; p < points.length; p++) {
      const idx = assignments[p];
      sums[idx][0] += points[p][0];
      sums[idx][1] += points[p][1];
      sums[idx][2] += points[p][2];
      counts[idx]++;
    }
    const newCentroids: OKLab[] = sums.map((s, i) => {
      const c = counts[i] || 1;
      return oklab(s[0] / c, s[1] / c, s[2] / c);
    });

    // Compute movement.
    let maxMovement = 0;
    for (let i = 0; i < k; i++) {
      const d = Math.sqrt(distSquared(centroids[i], newCentroids[i]));
      if (d > maxMovement) maxMovement = d;
    }
    centroids = newCentroids;

    // Re-assign.
    const newAssignments = points.map(p => nearestCentroidIndex(p, centroids));
    assignments = newAssignments;

    if (maxMovement < tolerance) break;
  }

  // Final error.
  let error = 0;
  for (let p = 0; p < points.length; p++) {
    error += distSquared(points[p], centroids[assignments[p]]);
  }

  return { palette: centroids, assignments, error, iterations };
}

/** Convert XYZ points to OKLab, run k-means, return palette in OKLab. */
export function quantizeFromXYZ(
  xyzPoints: ReadonlyArray<XYZ_D65>,
  opts: QuantizeOptions
): QuantizeResult {
  const oklabPoints = xyzPoints.map(p => oklabSpace.fromXYZ(p));
  return quantize(oklabPoints, opts);
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'k-means: 2 well-separated clusters → 2 centroids near input modes',
    fn: () => {
      const points: OKLab[] = [];
      for (let i = 0; i < 10; i++) {
        points.push(oklab(0.2 + i * 0.001, 0.05, 0.05));  // dark cluster
        points.push(oklab(0.8 + i * 0.001, -0.05, -0.05)); // light cluster
      }
      const { palette } = quantize(points, { k: 2, seed: 42 });
      // Should find one centroid near each cluster
      const Ls = palette.map(p => p[0]).sort((a, b) => a - b);
      const darkOK = Math.abs(Ls[0] - 0.205) < 0.01;
      const lightOK = Math.abs(Ls[1] - 0.805) < 0.01;
      return darkOK && lightOK ? 0 : 1;
    },
    expected: 0,
    tolerance: 0,
    source: 'k-means must recover two well-separated input clusters',
  },
  {
    name: 'k-means: deterministic with same seed',
    fn: () => {
      const points: OKLab[] = [];
      for (let i = 0; i < 20; i++) {
        points.push(oklab(Math.sin(i) * 0.5 + 0.5, Math.cos(i) * 0.2, Math.sin(i * 2) * 0.2));
      }
      const r1 = quantize(points, { k: 3, seed: 42 });
      const r2 = quantize(points, { k: 3, seed: 42 });
      // Compare palette L values
      const diff = r1.palette.reduce((acc, c, i) => acc + Math.abs(c[0] - r2.palette[i][0]), 0);
      return diff;
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Same seed must produce identical results',
  },
];
