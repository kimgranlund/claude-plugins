// ACES filmic tone mapping — the cinema/games industry standard.
//
// The full ACES (Academy Color Encoding System) pipeline is complex: input
// transforms, scene-referred LMT (Look Modification Transform), and output
// device transforms. For real-time / shader use, Krzysztof Narkowicz's
// simplified ACES fit is universal:
//
//   y = (x · (a · x + b)) / (x · (c · x + d) + e)
//
// with constants (a=2.51, b=0.03, c=2.43, d=0.59, e=0.14).
//
// This skill implements the Narkowicz fit as `applyACES`. For full-pipeline
// ACES (with input transforms, RRT, ODT), use the Academy's official C++
// reference or OpenColorIO.
//
// Primary source: Narkowicz, "ACES Filmic Tone Mapping Curve" (2015)
//   https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/
// ACES official: https://github.com/ampas/aces-dev

import type { LinearSRGB } from '../types.js';
import { linearSRGB } from '../types.js';

// ─── ACES Narkowicz coefficients ──────────────────────────────────────────────

const A = 2.51;
const B = 0.03;
const C = 2.43;
const D = 0.59;
const E = 0.14;

// ─── Scalar operator ──────────────────────────────────────────────────────────

/**
 * ACES filmic tone map (Narkowicz fit). Scalar.
 *
 *   y = (x · (A · x + B)) / (x · (C · x + D) + E)
 *
 * Maps [0, ∞) → [0, ~0.999]. Smoother than Reinhard with a characteristic
 * filmic toe (slight desaturation in shadows) and stronger highlight rolloff.
 */
export function acesNarkowicz(x: number): number {
  return (x * (A * x + B)) / (x * (C * x + D) + E);
}

// ─── Per-channel application ──────────────────────────────────────────────────

/** Apply ACES filmic per channel. */
export function applyACES(rgb: LinearSRGB): LinearSRGB {
  return linearSRGB(
    acesNarkowicz(rgb[0]),
    acesNarkowicz(rgb[1]),
    acesNarkowicz(rgb[2])
  );
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'acesNarkowicz(0) ≈ 0',
    fn: () => acesNarkowicz(0),
    expected: 0,
    tolerance: 1e-12,
    source: 'Black point: numerator is 0, output is 0',
  },
  {
    name: 'acesNarkowicz(1) is ~0.8',
    fn: () => acesNarkowicz(1),
    expected: 0.80,
    tolerance: 0.02,
    source: 'ACES at SDR white (input=1) maps to ~0.8 — characteristic filmic value',
  },
  {
    name: 'acesNarkowicz(100) approaches asymptote 1.033',
    fn: () => acesNarkowicz(100),
    expected: 1.033,
    tolerance: 0.005,
    source: 'Narkowicz fit asymptotes to a/c = 2.51/2.43 ≈ 1.033 (small overshoot; clip post-hoc for display)',
  },
  {
    name: 'acesNarkowicz is monotonic over [0, 10]',
    fn: () => {
      for (let i = 0; i < 100; i++) {
        const x1 = i * 0.1;
        const x2 = (i + 1) * 0.1;
        if (acesNarkowicz(x2) <= acesNarkowicz(x1)) return 1;
      }
      return 0;
    },
    expected: 0,
    tolerance: 0,
    source: 'Tone mapping must be monotonic over its operating range',
  },
];
