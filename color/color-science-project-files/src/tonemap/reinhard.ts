// Reinhard tone mapping — the simplest physically-motivated HDR → SDR compressor.
//
// Three variants in common use:
//   1. Global (simple):       y = x / (1 + x)
//   2. Extended:              y = x · (1 + x/W²) / (1 + x)  where W = white point
//   3. Luminance-preserving:  apply to Y only, scale chroma by gain
//
// Reinhard is fast, monotonic, and produces no shadow-crushing. Its main
// weakness is that highlights compress smoothly but never reach 1.0 (the simple
// form), so a bright scene looks slightly washed out. The extended form fixes
// this by mapping a chosen "white point" W exactly to 1.0.
//
// Primary source: Reinhard, Stark, Shirley, Ferwerda (2002),
//   "Photographic Tone Reproduction for Digital Images,"
//   ACM Transactions on Graphics 21(3), 267-276.
//
// Companion math: references/techniques/tone-mapping-operators.md

import type { LinearSRGB } from '../types.js';
import { linearSRGB } from '../types.js';

// ─── Scalar operators ─────────────────────────────────────────────────────────

/**
 * Simple Reinhard: y = x / (1 + x).
 * Maps [0, ∞) → [0, 1). Never reaches 1.0; asymptotes near.
 */
export function reinhardSimple(x: number): number {
  return x / (1 + x);
}

/**
 * Extended Reinhard: maps a chosen `whitePoint` exactly to 1.0.
 * Default whitePoint = 4.0 (4× SDR white).
 *
 *   y = x · (1 + x/W²) / (1 + x)
 *
 * At x = 0 → 0. At x = W → 1. At x < W → smooth ramp.
 */
export function reinhardExtended(x: number, whitePoint: number = 4.0): number {
  const W2 = whitePoint * whitePoint;
  return (x * (1 + x / W2)) / (1 + x);
}

// ─── Per-channel application ──────────────────────────────────────────────────

/** Apply simple Reinhard per channel. */
export function applySimple(rgb: LinearSRGB): LinearSRGB {
  return linearSRGB(reinhardSimple(rgb[0]), reinhardSimple(rgb[1]), reinhardSimple(rgb[2]));
}

/** Apply extended Reinhard per channel. */
export function applyExtended(rgb: LinearSRGB, whitePoint: number = 4.0): LinearSRGB {
  return linearSRGB(
    reinhardExtended(rgb[0], whitePoint),
    reinhardExtended(rgb[1], whitePoint),
    reinhardExtended(rgb[2], whitePoint)
  );
}

// ─── Luminance-preserving variant ─────────────────────────────────────────────

const Y_WEIGHTS = [0.2126390059, 0.7151686788, 0.0721923154] as const;

/** Relative luminance from linear sRGB. */
function luminance(rgb: readonly [number, number, number]): number {
  return Y_WEIGHTS[0] * rgb[0] + Y_WEIGHTS[1] * rgb[1] + Y_WEIGHTS[2] * rgb[2];
}

/**
 * Luminance-preserving Reinhard: compress Y only, scale RGB by the Y gain.
 * Preserves hue better than per-channel Reinhard, at the cost of more saturated
 * output (chroma is not compressed alongside luminance).
 */
export function applyLuminancePreserving(
  rgb: LinearSRGB,
  whitePoint: number = 4.0
): LinearSRGB {
  const Y = luminance(rgb);
  if (Y <= 0) return rgb;
  const Y_new = reinhardExtended(Y, whitePoint);
  const gain = Y_new / Y;
  return linearSRGB(rgb[0] * gain, rgb[1] * gain, rgb[2] * gain);
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'reinhardSimple(0) = 0',
    fn: () => reinhardSimple(0),
    expected: 0,
    tolerance: 1e-12,
    source: 'Black point — no tone mapping needed',
  },
  {
    name: 'reinhardSimple(1) = 0.5',
    fn: () => reinhardSimple(1),
    expected: 0.5,
    tolerance: 1e-12,
    source: 'At input=1 (SDR white), simple Reinhard outputs 0.5',
  },
  {
    name: 'reinhardSimple asymptotes near 1',
    fn: () => reinhardSimple(1000),
    expected: 0.999,
    tolerance: 1e-3,
    source: 'Simple Reinhard → 1 as x → ∞; never reaches 1',
  },
  {
    name: 'reinhardExtended(4) = 1 (at white point)',
    fn: () => reinhardExtended(4, 4),
    expected: 1.0,
    tolerance: 1e-12,
    source: 'Extended Reinhard maps W=4 exactly to 1',
  },
  {
    name: 'reinhardExtended(0) = 0',
    fn: () => reinhardExtended(0, 4),
    expected: 0,
    tolerance: 1e-12,
    source: 'Black point preserved',
  },
  {
    name: 'reinhardExtended(2, 4) is between 0 and 1',
    fn: () => {
      const y = reinhardExtended(2, 4);
      return y > 0.5 && y < 1.0 ? 0 : 1;
    },
    expected: 0,
    tolerance: 0,
    source: 'Mid-input maps to mid-output above SDR white',
  },
];
