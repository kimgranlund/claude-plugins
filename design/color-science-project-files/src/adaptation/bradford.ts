// Bradford chromatic adaptation — the workhorse for D50 ↔ D65 conversion.
//
// Chromatic adaptation models how the human visual system "discounts" the
// illuminant, so a white piece of paper looks white under both daylight (D65)
// and incandescent (A) light. The Bradford transform is the standard for ICC
// profile work and CSS Color 4.
//
// Algorithm:
//   1. Transform source XYZ to "Bradford cone response" via M_BR.
//   2. Multiply by per-channel scale factors (ratio of source-white to dest-white in Bradford space).
//   3. Inverse-transform back to XYZ at the destination white point.
//
// Primary sources:
//   - Lam, K. M. (1985) — Original Bradford CAT (PhD thesis).
//   - CIE 159:2004 — Codified Bradford as the recommended general CAT.
//   - Bruce Lindbloom — http://brucelindbloom.com/Eqn_ChromAdapt.html

import type { XYZ_D65, Matrix3x3 } from '../types.js';
import { mulMat3Vec3, mulMat3Mat3, xyz } from '../types.js';

// ─── The Bradford response matrix ─────────────────────────────────────────────

/** M_BR: XYZ → Bradford cone response. */
export const M_BRADFORD: Matrix3x3 = [
  [ 0.8951000,  0.2664000, -0.1614000],
  [-0.7502000,  1.7135000,  0.0367000],
  [ 0.0389000, -0.0685000,  1.0296000],
];

/** M_BR^-1: Bradford cone response → XYZ. */
export const M_BRADFORD_INV: Matrix3x3 = [
  [ 0.9869929, -0.1470543,  0.1599627],
  [ 0.4323053,  0.5183603,  0.0492912],
  [-0.0085287,  0.0400428,  0.9684867],
];

// ─── Standard illuminant white points (XYZ normalized to Y=1) ─────────────────

/** D65 — modern display standard (sRGB, P3, Rec.709/2020). */
export const D65: readonly [number, number, number] = [0.9504559270516716, 1.0, 1.0890577507598784];

/** D50 — ICC Profile Connection Space (ICC.1:2010, Annex D). */
export const D50: readonly [number, number, number] = [0.9642956764295677, 1.0, 0.8251046025104603];

/** A — incandescent tungsten (~2856 K). */
export const A: readonly [number, number, number] = [1.0985, 1.0, 0.35585];

/** F2 — cool white fluorescent. */
export const F2: readonly [number, number, number] = [0.99186, 1.0, 0.67393];

// ─── Generic Bradford adaptation ──────────────────────────────────────────────

/**
 * Compute the 3x3 Bradford adaptation matrix from `srcWhite` to `dstWhite`.
 *
 * Apply it via `mulMat3Vec3(M, srcXYZ)` to adapt an XYZ value.
 * Pre-compute and cache this matrix when adapting many colors between the same
 * pair of illuminants.
 */
export function bradfordMatrix(
  srcWhite: readonly [number, number, number],
  dstWhite: readonly [number, number, number]
): Matrix3x3 {
  const rgbSrc = mulMat3Vec3(M_BRADFORD, srcWhite);
  const rgbDst = mulMat3Vec3(M_BRADFORD, dstWhite);

  // Diagonal scale matrix
  const D: Matrix3x3 = [
    [rgbDst[0] / rgbSrc[0], 0, 0],
    [0, rgbDst[1] / rgbSrc[1], 0],
    [0, 0, rgbDst[2] / rgbSrc[2]],
  ];

  // M_BR^-1 * D * M_BR
  return mulMat3Mat3(M_BRADFORD_INV, mulMat3Mat3(D, M_BRADFORD));
}

/**
 * Adapt a single XYZ value from `srcWhite` to `dstWhite` via Bradford CAT.
 * For batch adaptation, pre-compute the matrix via `bradfordMatrix()`.
 */
export function adapt(
  srcXYZ: readonly [number, number, number],
  srcWhite: readonly [number, number, number],
  dstWhite: readonly [number, number, number]
): [number, number, number] {
  const M = bradfordMatrix(srcWhite, dstWhite);
  return mulMat3Vec3(M, srcXYZ);
}

// ─── Convenience: D50 ↔ D65 ───────────────────────────────────────────────────

/** Pre-computed D50 → D65 Bradford matrix. */
export const M_D50_TO_D65: Matrix3x3 = bradfordMatrix(D50, D65);

/** Pre-computed D65 → D50 Bradford matrix. */
export const M_D65_TO_D50: Matrix3x3 = bradfordMatrix(D65, D50);

/** Adapt XYZ from D50 to D65. */
export function d50ToD65(xyzD50: readonly [number, number, number]): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_D50_TO_D65, xyzD50);
  return xyz(X, Y, Z);
}

/** Adapt XYZ from D65 to D50. */
export function d65ToD50(xyzD65: XYZ_D65): [number, number, number] {
  return mulMat3Vec3(M_D65_TO_D50, xyzD65);
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

// Note: published Bradford matrices are 7-digit; the inverse accumulates ~1e-7
// precision drift. Tolerance is 1e-6 across all tests to accommodate this.
export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'bradford D65 → D65 = identity Y',
    fn: () => {
      const adapted = adapt(D65, D65, D65);
      return Math.abs(adapted[1] - 1.0);
    },
    expected: 0,
    tolerance: 1e-6,
    source: 'Self-adaptation should be identity (within published-matrix precision)',
  },
  {
    name: 'bradford D50 ↔ D65 round-trip Y',
    fn: () => {
      const round = adapt(adapt(D65, D65, D50), D50, D65);
      return Math.abs(round[1] - 1.0);
    },
    expected: 0,
    tolerance: 1e-6,
    source: 'Round-trip should restore Y=1 within published-matrix precision',
  },
  {
    name: 'bradford D65 → D50 maps D65 white to D50 white',
    fn: () => {
      const adapted = adapt(D65, D65, D50);
      return Math.hypot(adapted[0] - D50[0], adapted[1] - D50[1], adapted[2] - D50[2]);
    },
    expected: 0,
    tolerance: 1e-6,
    source: 'White points must map to white points',
  },
];
