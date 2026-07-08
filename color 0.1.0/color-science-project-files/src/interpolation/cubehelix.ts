// Cubehelix — D. A. Green's perceptually-monotonic brightness ramp with
// smoothly rotating hue.
//
// Originally designed for astronomical visualization (intensity-grayscale
// fallback), cubehelix produces an excellent perceptual ramp from black to
// white where the brightness progresses uniformly while the hue smoothly
// cycles through chromatic regions.
//
// Use cases:
//   - Scientific colormaps (better than the dreaded "rainbow" / "jet")
//   - Single-color ramp generators
//   - Fallback ramps when you need monotonic luminance with character
//
// Primary source: D. A. Green, "A colour scheme for the display of
//   astronomical intensity images" (2011)
//   https://astron-soc.in/bulletin/11June/289392011.pdf

import type { LinearSRGB } from '../types.js';
import { linearSRGB } from '../types.js';

const TWO_PI = Math.PI * 2;
const DEG_TO_RAD = Math.PI / 180;

export type CubehelixOptions = Readonly<{
  /** Starting hue in degrees [0, 360). Default 0 (red). */
  start: number;
  /** Number of full 360° rotations as t goes from 0 to 1. Default -1.5 (D. A. Green). */
  rotations: number;
  /** Hue intensity (chroma amplitude). Default 1.0. */
  hue: number;
  /** Brightness curve exponent. Default 1.0 (linear lightness). Set >1 for slower start. */
  gamma: number;
}>;

export const DEFAULT_OPTIONS: CubehelixOptions = {
  start: 0,
  rotations: -1.5,
  hue: 1.0,
  gamma: 1.0,
};

/**
 * Cubehelix value at parameter t ∈ [0, 1] → linear sRGB.
 *
 * Green's formula:
 *   l = t^gamma
 *   angle = 2π · (start/360 + 1 + rotations · t)
 *   amp = hue · l · (1 − l) / 2
 *   R = l + amp · (−0.14861 cos(angle) + 1.78277 sin(angle))
 *   G = l + amp · (−0.29227 cos(angle) − 0.90649 sin(angle))
 *   B = l + amp · ( 1.97294 cos(angle))
 *
 * Output is NOT clipped — out-of-gamut values are returned as-is.
 * For display, run through `mapToSRGB` or `clipNaive`.
 */
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

/** Generate `n` cubehelix colors equally spaced in t ∈ [0, 1] (inclusive). */
export function cubehelixPalette(
  n: number,
  opts: Partial<CubehelixOptions> = {}
): readonly LinearSRGB[] {
  if (n <= 1) return [cubehelix(0, opts)];
  const out: LinearSRGB[] = [];
  for (let i = 0; i < n; i++) {
    out.push(cubehelix(i / (n - 1), opts));
  }
  return out;
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'cubehelix at t=0 is black',
    fn: () => Math.hypot(...cubehelix(0)),
    expected: 0,
    tolerance: 1e-12,
    source: 'Green 2011 — t=0 is the black anchor (l=0 → R=G=B=0)',
  },
  {
    name: 'cubehelix at t=1 is white',
    fn: () => {
      const c = cubehelix(1);
      return Math.hypot(c[0] - 1, c[1] - 1, c[2] - 1);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Green 2011 — t=1 is the white anchor (l=1, amp=0 → R=G=B=1)',
  },
  {
    name: 'cubehelix at t=0.5 has reasonable mid-tone luminance',
    fn: () => {
      const c = cubehelix(0.5);
      // Y from linear sRGB
      const Y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
      // Luminance at mid-t should be roughly 0.5 (cubehelix is designed for this)
      return Y;
    },
    expected: 0.5,
    tolerance: 0.1,
    source: 'Cubehelix is designed for monotonic Y; mid-t should give Y ~0.5',
  },
  {
    name: 'cubehelix palette of 5 starts at black',
    fn: () => Math.hypot(...cubehelixPalette(5)[0]),
    expected: 0,
    tolerance: 1e-12,
    source: 'Palette inclusive of endpoints',
  },
  {
    name: 'cubehelix palette of 5 ends at white',
    fn: () => {
      const last = cubehelixPalette(5)[4];
      return Math.hypot(last[0] - 1, last[1] - 1, last[2] - 1);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Palette inclusive of endpoints',
  },
];
