// Machado 2009 — physiologically-based simulation of color vision deficiency.
//
// Severity-parameterized matrices acting directly on linear sRGB. The standard
// for modern CVD simulation tooling (Chrome DevTools uses these). Faster than
// Brettel 1997's full LMS-confusion-line projection while remaining
// physiologically grounded.
//
// Coverage: protanopia, deuteranopia, tritanopia at severity 1.0.
// For partial severities, linearly interpolates against identity. This is an
// approximation — Machado's paper publishes full tables at severity 0.1, 0.2,
// ..., 1.0 because the matrices change non-linearly with severity. For
// strict-precision intermediate-severity use, replace `simulate(severity < 1.0)`
// with a lookup against the full table.
//
// Primary source: Machado, Oliveira, Fernandes (2009),
//   "A Physiologically-based Model for Simulation of Color Vision Deficiency,"
//   IEEE Transactions on Visualization and Computer Graphics 15(6), 1291-1298.
//
// Companion math: references/techniques/cvd-simulation-algorithms.md

import type { LinearSRGB, Matrix3x3 } from '../types.js';
import { mulMat3Vec3, linearSRGB } from '../types.js';

// ─── Machado severity-1.0 matrices ────────────────────────────────────────────

/** Protanopia (no L-cones) at full severity. */
export const M_PROTANOPIA: Matrix3x3 = [
  [ 0.152286,  1.052583, -0.204868],
  [ 0.114503,  0.786281,  0.099216],
  [-0.003882, -0.048116,  1.051998],
];

/** Deuteranopia (no M-cones) at full severity. */
export const M_DEUTERANOPIA: Matrix3x3 = [
  [ 0.367322,  0.860646, -0.227968],
  [ 0.280085,  0.672501,  0.047413],
  [-0.011820,  0.042940,  0.968881],
];

/** Tritanopia (no S-cones) at full severity. */
export const M_TRITANOPIA: Matrix3x3 = [
  [ 1.255528, -0.076749, -0.178779],
  [-0.078411,  0.930809,  0.147602],
  [ 0.004733,  0.691367,  0.303900],
];

const IDENTITY: Matrix3x3 = [
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1],
];

// ─── Public API ───────────────────────────────────────────────────────────────

export type CVDType = 'protanopia' | 'deuteranopia' | 'tritanopia';

const TYPE_MATRIX: Readonly<Record<CVDType, Matrix3x3>> = {
  protanopia: M_PROTANOPIA,
  deuteranopia: M_DEUTERANOPIA,
  tritanopia: M_TRITANOPIA,
};

/**
 * Linearly interpolate two 3×3 matrices component-wise.
 * Note: for Machado intermediate severities, this is an approximation;
 * the full Machado table is more accurate.
 */
function lerpMatrix(a: Matrix3x3, b: Matrix3x3, t: number): Matrix3x3 {
  const r = (i: number, j: number) => a[i][j] + (b[i][j] - a[i][j]) * t;
  return [
    [r(0, 0), r(0, 1), r(0, 2)],
    [r(1, 0), r(1, 1), r(1, 2)],
    [r(2, 0), r(2, 1), r(2, 2)],
  ];
}

/**
 * Build the CVD simulation matrix for a given type and severity.
 * @param type - which CVD type to simulate
 * @param severity - in [0, 1]; 0 = no deficiency (identity), 1 = full deficiency
 */
export function simulationMatrix(type: CVDType, severity: number = 1.0): Matrix3x3 {
  const s = Math.max(0, Math.min(1, severity));
  if (s === 0) return IDENTITY;
  if (s === 1) return TYPE_MATRIX[type];
  return lerpMatrix(IDENTITY, TYPE_MATRIX[type], s);
}

/**
 * Simulate CVD on a single linear sRGB color.
 * @param rgb - input linear sRGB
 * @param type - which CVD type to simulate
 * @param severity - in [0, 1]; default 1.0 (full deficiency)
 */
export function simulate(
  rgb: LinearSRGB,
  type: CVDType,
  severity: number = 1.0
): LinearSRGB {
  const M = simulationMatrix(type, severity);
  const [r, g, b] = mulMat3Vec3(M, rgb);
  return linearSRGB(r, g, b);
}

// ─── Convenience helpers ──────────────────────────────────────────────────────

export const simulateProtanopia = (rgb: LinearSRGB, severity: number = 1.0) =>
  simulate(rgb, 'protanopia', severity);

export const simulateDeuteranopia = (rgb: LinearSRGB, severity: number = 1.0) =>
  simulate(rgb, 'deuteranopia', severity);

export const simulateTritanopia = (rgb: LinearSRGB, severity: number = 1.0) =>
  simulate(rgb, 'tritanopia', severity);

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'severity=0 returns identity (protanopia)',
    fn: () => {
      const input = linearSRGB(0.5, 0.3, 0.7);
      const out = simulate(input, 'protanopia', 0);
      return Math.hypot(out[0] - 0.5, out[1] - 0.3, out[2] - 0.7);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Severity 0 = no deficiency = identity transform',
  },
  {
    name: 'severity=0 returns identity (deuteranopia)',
    fn: () => {
      const input = linearSRGB(0.8, 0.2, 0.4);
      const out = simulate(input, 'deuteranopia', 0);
      return Math.hypot(out[0] - 0.8, out[1] - 0.2, out[2] - 0.4);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Severity 0 = no deficiency = identity transform',
  },
  {
    name: 'black is unchanged (protanopia)',
    fn: () => {
      const out = simulate(linearSRGB(0, 0, 0), 'protanopia', 1.0);
      return Math.hypot(...out);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Black has no chromatic component; CVD simulation preserves it',
  },
  {
    name: 'white is approximately unchanged (deuteranopia)',
    fn: () => {
      const out = simulate(linearSRGB(1, 1, 1), 'deuteranopia', 1.0);
      // Sum of each row of M should be ~1; white preserves
      return Math.hypot(out[0] - 1, out[1] - 1, out[2] - 1);
    },
    expected: 0,
    tolerance: 1e-3,
    source: 'CVD matrix rows sum to ~1 (preserves white)',
  },
  {
    name: 'severity=1 protanopia desaturates pure red',
    fn: () => {
      const input = linearSRGB(1, 0, 0);
      const out = simulate(input, 'protanopia', 1.0);
      // Pure red under protanopia should look much darker / more yellow
      return out[0];  // R value should drop significantly
    },
    expected: 0.152286,
    tolerance: 1e-5,
    source: 'Machado 2009 — pure red under protanopia maps to ~0.152',
  },
  {
    name: 'severity=0.5 is midpoint between identity and full',
    fn: () => {
      const input = linearSRGB(1, 0, 0);
      const full = simulate(input, 'protanopia', 1.0);
      const half = simulate(input, 'protanopia', 0.5);
      const expectedR = 0.5 * (1.0 + full[0]);
      return Math.abs(half[0] - expectedR);
    },
    expected: 0,
    tolerance: 1e-9,
    source: 'Linear interpolation: severity 0.5 = mean of identity and full',
  },
];
