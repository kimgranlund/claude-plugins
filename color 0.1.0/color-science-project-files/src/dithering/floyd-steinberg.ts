// Floyd-Steinberg error-diffusion dithering.
//
// Given a continuous-tone source image and a fixed palette, produce a
// quantized image where the perceived color matches the source on average
// despite each pixel being constrained to a palette member.
//
// Algorithm (Floyd & Steinberg, 1976): for each pixel in raster order, find
// the nearest palette color, compute the quantization error, and diffuse the
// error to neighboring pixels with the standard 7/16, 3/16, 5/16, 1/16
// weights:
//
//                       *   7/16
//                3/16  5/16  1/16
//
// Apply in OKLab for perceptually-uniform error metric.
//
// Primary source: Floyd, R.W. & Steinberg, L. (1976), "An adaptive algorithm
// for spatial grayscale," Proc. SID 17(2), 75-77.

import type { OKLab } from '../types.js';
import { oklab } from '../types.js';

// ─── Floyd-Steinberg error diffusion ──────────────────────────────────────────

/** A 2D image of OKLab values laid out as rows of columns. */
export type OkLabImage = ReadonlyArray<ReadonlyArray<OKLab>>;

/** Mutable 2D buffer for in-place dithering work. */
type MutableOkLabImage = OKLab[][];

function nearestPaletteIndex(point: OKLab, palette: ReadonlyArray<OKLab>): number {
  let best = 0;
  let bestDist = Infinity;
  for (let i = 0; i < palette.length; i++) {
    const dL = point[0] - palette[i][0];
    const dA = point[1] - palette[i][1];
    const dB = point[2] - palette[i][2];
    const d = dL * dL + dA * dA + dB * dB;
    if (d < bestDist) {
      bestDist = d;
      best = i;
    }
  }
  return best;
}

/**
 * Apply Floyd-Steinberg dithering. Returns:
 *   - `indices`: 2D array of palette indices (same shape as input)
 *   - `dithered`: 2D array of palette OKLab values (for direct display)
 */
export function ditherFloydSteinberg(
  source: OkLabImage,
  palette: ReadonlyArray<OKLab>
): { indices: number[][]; dithered: OKLab[][] } {
  const H = source.length;
  const W = source[0].length;

  // Copy source into a mutable buffer (we accumulate errors here).
  const buf: MutableOkLabImage = source.map(row => row.map(c => oklab(c[0], c[1], c[2])));
  const indices: number[][] = [];
  const dithered: OKLab[][] = [];

  for (let y = 0; y < H; y++) {
    const idxRow: number[] = [];
    const dRow: OKLab[] = [];
    for (let x = 0; x < W; x++) {
      const current = buf[y][x];
      const idx = nearestPaletteIndex(current, palette);
      const nearest = palette[idx];
      idxRow.push(idx);
      dRow.push(nearest);

      const errL = current[0] - nearest[0];
      const errA = current[1] - nearest[1];
      const errB = current[2] - nearest[2];

      // Diffuse error to neighbors.
      const diffuse = (yy: number, xx: number, weight: number) => {
        if (yy < 0 || yy >= H || xx < 0 || xx >= W) return;
        buf[yy][xx] = oklab(
          buf[yy][xx][0] + errL * weight,
          buf[yy][xx][1] + errA * weight,
          buf[yy][xx][2] + errB * weight
        );
      };

      diffuse(y,     x + 1, 7 / 16);
      diffuse(y + 1, x - 1, 3 / 16);
      diffuse(y + 1, x,     5 / 16);
      diffuse(y + 1, x + 1, 1 / 16);
    }
    indices.push(idxRow);
    dithered.push(dRow);
  }

  return { indices, dithered };
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'Floyd-Steinberg with 1-color palette returns that color everywhere',
    fn: () => {
      const source: OkLabImage = [
        [oklab(0.5, 0.1, 0.1), oklab(0.6, 0.0, 0.2)],
        [oklab(0.3, 0.2, -0.1), oklab(0.7, -0.1, 0.0)],
      ];
      const palette = [oklab(0.5, 0, 0)];
      const { indices } = ditherFloydSteinberg(source, palette);
      // All indices must be 0
      for (const row of indices) for (const i of row) if (i !== 0) return 1;
      return 0;
    },
    expected: 0,
    tolerance: 0,
    source: 'With only one palette color, every pixel maps to index 0',
  },
  {
    name: 'Floyd-Steinberg: average error close to zero for balanced palette',
    fn: () => {
      // Source: gradient from 0 to 1 in L
      const source: OKLab[][] = [];
      for (let y = 0; y < 8; y++) {
        const row: OKLab[] = [];
        for (let x = 0; x < 8; x++) {
          const L = (y * 8 + x) / 63;
          row.push(oklab(L, 0, 0));
        }
        source.push(row);
      }
      const palette = [oklab(0, 0, 0), oklab(1, 0, 0)]; // black + white
      const { dithered } = ditherFloydSteinberg(source, palette);

      // Average dithered L should approximate average source L (0.5).
      let sumDithered = 0;
      let sumSource = 0;
      for (let y = 0; y < 8; y++) {
        for (let x = 0; x < 8; x++) {
          sumDithered += dithered[y][x][0];
          sumSource += source[y][x][0];
        }
      }
      return Math.abs(sumDithered / 64 - sumSource / 64);
    },
    expected: 0,
    tolerance: 0.05,
    source: 'Floyd-Steinberg preserves average tone via error diffusion',
  },
];
