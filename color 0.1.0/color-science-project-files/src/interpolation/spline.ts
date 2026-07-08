// Spline interpolation in color spaces.
//
// Cubic splines smoothly pass through control points, producing C2-continuous
// curves. Use for palette construction where you want a smooth ramp through
// non-uniformly spaced anchor colors (e.g., dark → mid → light with specific
// hue shifts at each anchor).
//
// Implemented: Catmull-Rom (passes through every control point, smooth
// through interior, linear extrapolation at endpoints).
//
// Primary source: Catmull, E. & Rom, R. (1974), "A class of local
// interpolating splines," Computer Aided Geometric Design.

// ─── Catmull-Rom cubic ────────────────────────────────────────────────────────

/**
 * Catmull-Rom interpolation between P1 and P2 with P0 and P3 as tangent context.
 * For t ∈ [0, 1], the curve passes through P1 at t=0 and P2 at t=1.
 *
 * $$P(t) = 0.5 \cdot \big((2 P_1) + (-P_0 + P_2) t + (2 P_0 - 5 P_1 + 4 P_2 - P_3) t^2 + (-P_0 + 3 P_1 - 3 P_2 + P_3) t^3 \big)$$
 */
export function catmullRomScalar(
  P0: number,
  P1: number,
  P2: number,
  P3: number,
  t: number
): number {
  const t2 = t * t;
  const t3 = t2 * t;
  return 0.5 * (
    (2 * P1) +
    (-P0 + P2) * t +
    (2 * P0 - 5 * P1 + 4 * P2 - P3) * t2 +
    (-P0 + 3 * P1 - 3 * P2 + P3) * t3
  );
}

/** Catmull-Rom for a 3-component color tuple (e.g., OKLab). */
export function catmullRomTuple(
  P0: readonly [number, number, number],
  P1: readonly [number, number, number],
  P2: readonly [number, number, number],
  P3: readonly [number, number, number],
  t: number
): [number, number, number] {
  return [
    catmullRomScalar(P0[0], P1[0], P2[0], P3[0], t),
    catmullRomScalar(P0[1], P1[1], P2[1], P3[1], t),
    catmullRomScalar(P0[2], P1[2], P2[2], P3[2], t),
  ];
}

// ─── Sample a Catmull-Rom curve through an arbitrary sequence of points ──────

/**
 * Evaluate the Catmull-Rom spline through `controls` at parameter `t` ∈ [0, 1].
 * The spline passes through every control point. Endpoints are duplicated to
 * provide tangent context (no extrapolation beyond the input range).
 */
export function catmullRomCurve(
  controls: ReadonlyArray<readonly [number, number, number]>,
  t: number
): [number, number, number] {
  if (controls.length < 2) {
    throw new Error('catmullRomCurve requires at least 2 control points');
  }
  if (controls.length === 2) {
    return [
      controls[0][0] + (controls[1][0] - controls[0][0]) * t,
      controls[0][1] + (controls[1][1] - controls[0][1]) * t,
      controls[0][2] + (controls[1][2] - controls[0][2]) * t,
    ];
  }

  const n = controls.length - 1;
  // Map t ∈ [0, 1] to segment index + sub-parameter.
  const u = Math.max(0, Math.min(1, t)) * n;
  const segment = Math.min(Math.floor(u), n - 1);
  const localT = u - segment;

  // Get the four control points (duplicate at boundaries).
  const P0 = controls[Math.max(0, segment - 1)];
  const P1 = controls[segment];
  const P2 = controls[segment + 1];
  const P3 = controls[Math.min(n, segment + 2)];

  return catmullRomTuple(P0, P1, P2, P3, localT);
}

/** Sample `n` colors along the spline at equally-spaced t values. */
export function catmullRomSamples(
  controls: ReadonlyArray<readonly [number, number, number]>,
  n: number
): ReadonlyArray<[number, number, number]> {
  if (n < 2) return [catmullRomCurve(controls, 0)];
  const out: [number, number, number][] = [];
  for (let i = 0; i < n; i++) {
    out.push(catmullRomCurve(controls, i / (n - 1)));
  }
  return out;
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'Catmull-Rom passes through P1 at t=0',
    fn: () => Math.abs(catmullRomScalar(0, 1, 2, 3, 0) - 1),
    expected: 0,
    tolerance: 1e-12,
    source: 'Curve interpolates P1 exactly at t=0',
  },
  {
    name: 'Catmull-Rom passes through P2 at t=1',
    fn: () => Math.abs(catmullRomScalar(0, 1, 2, 3, 1) - 2),
    expected: 0,
    tolerance: 1e-12,
    source: 'Curve interpolates P2 exactly at t=1',
  },
  {
    name: 'Catmull-Rom on linear data is linear',
    fn: () => {
      // Equally-spaced control points → midpoint is linear midpoint
      return Math.abs(catmullRomScalar(0, 1, 2, 3, 0.5) - 1.5);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'For linearly-spaced controls, Catmull-Rom is linear',
  },
  {
    name: 'catmullRomCurve through 3 points hits first control',
    fn: () => {
      const pts: [number, number, number][] = [[0, 0, 0], [1, 2, 3], [2, 4, 6]];
      const result = catmullRomCurve(pts, 0);
      return Math.hypot(result[0], result[1], result[2]);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Endpoint anchoring',
  },
  {
    name: 'catmullRomCurve through 3 points hits last control',
    fn: () => {
      const pts: [number, number, number][] = [[0, 0, 0], [1, 2, 3], [2, 4, 6]];
      const result = catmullRomCurve(pts, 1);
      return Math.hypot(result[0] - 2, result[1] - 4, result[2] - 6);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Endpoint anchoring',
  },
];
