// OKLab ↔ XYZ_D65
//
// OKLab is a perceptually uniform color space by Björn Ottosson (2020).
// It fixes CIELAB's blue-purple curvature and provides better uniformity
// for lightness, chroma, and hue manipulation.
//
// Algorithm:
//   XYZ_D65 → LMS (linear cone response, via M1)
//   LMS → LMS' (cube root)
//   LMS' → OKLab (via M2)
//
// Inverse:
//   OKLab → LMS' (via M2_INV)
//   LMS' → LMS (cube)
//   LMS → XYZ_D65 (via M1_INV)
//
// Primary source: Björn Ottosson, "A perceptual color space for image processing"
// https://bottosson.github.io/posts/oklab/
//
// See also: references/techniques/oklab-xyz-math.md

import type { XYZ_D65, OKLab, Matrix3x3, TestVector } from '../types.js';
import {
  mulMat3Vec3,
  cbrt,
  oklab,
  xyz,
  NONLINEAR_TOLERANCE,
} from '../types.js';

// ─── Ottosson matrices ────────────────────────────────────────────────────────

/** M1: XYZ_D65 → linear LMS. From Ottosson 2020. */
const M1: Matrix3x3 = [
  [ 0.8189330101,  0.3618667424, -0.1288597137],
  [ 0.0329845436,  0.9293118715,  0.0361456387],
  [ 0.0482003018,  0.2643662691,  0.6338517070],
];

/** M1 inverse: linear LMS → XYZ_D65. */
const M1_INV: Matrix3x3 = [
  [ 1.2270138511, -0.5577999807,  0.2812561490],
  [-0.0405801784,  1.1122568696, -0.0716766787],
  [-0.0763812845, -0.4214819784,  1.5861632204],
];

/** M2: LMS' (cube root of LMS) → OKLab. */
const M2: Matrix3x3 = [
  [ 0.2104542553,  0.7936177850, -0.0040720468],
  [ 1.9779984951, -2.4285922050,  0.4505937099],
  [ 0.0259040371,  0.7827717662, -0.8086757660],
];

/** M2 inverse: OKLab → LMS'. Note: first column is all 1s (defining OKLab property). */
const M2_INV: Matrix3x3 = [
  [1.0000000000,  0.3963377774,  0.2158037573],
  [1.0000000000, -0.1055613458, -0.0638541728],
  [1.0000000000, -0.0894841775, -1.2914855480],
];

// ─── Forward: XYZ_D65 → OKLab ─────────────────────────────────────────────────

export function fromXYZ(c: XYZ_D65): OKLab {
  const lms = mulMat3Vec3(M1, c);
  const lmsPrime: [number, number, number] = [
    cbrt(lms[0]),
    cbrt(lms[1]),
    cbrt(lms[2]),
  ];
  const [L, a, b] = mulMat3Vec3(M2, lmsPrime);
  return oklab(L, a, b);
}

// ─── Inverse: OKLab → XYZ_D65 ─────────────────────────────────────────────────

export function toXYZ(c: OKLab): XYZ_D65 {
  const lmsPrime = mulMat3Vec3(M2_INV, c);
  const lms: [number, number, number] = [
    lmsPrime[0] ** 3,
    lmsPrime[1] ** 3,
    lmsPrime[2] ** 3,
  ];
  const [X, Y, Z] = mulMat3Vec3(M1_INV, lms);
  return xyz(X, Y, Z);
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

/**
 * Test vectors from Ottosson 2020 ("Reference values").
 * Round-trip identity should hold within NONLINEAR_TOLERANCE (1e-4) due to the
 * cube-root nonlinearity.
 */
export const testVectors: ReadonlyArray<TestVector<XYZ_D65, OKLab>> = [
  {
    input: xyz(0.950, 1.000, 1.089),
    output: oklab(1.000, 0.000, 0.000),
    tolerance: 1e-3,
    source: 'Ottosson 2020 — D65 white point',
    note: 'D65 white (Y=1) → OKLab L=1, a=0, b=0',
  },
  {
    input: xyz(1.000, 0.000, 0.000),
    output: oklab(0.44999, 1.23553, -0.01903),
    tolerance: 1e-3,
    source: 'Ottosson 2020 — pure X stimulus',
    note: 'Pure X → strong red-green axis, near-zero blue-yellow',
  },
  {
    input: xyz(0.000, 1.000, 0.000),
    output: oklab(0.92187, -0.67137, 0.26330),
    tolerance: 1e-3,
    source: 'Ottosson 2020 — pure Y stimulus',
    note: 'Pure Y → negative a (green direction), positive b (yellow direction)',
  },
  {
    input: xyz(0.000, 0.000, 1.000),
    output: oklab(0.15265, -1.41481, -0.44850),
    tolerance: 1e-3,
    source: 'Ottosson 2020 — pure Z stimulus',
    note: 'Pure Z → low L, deep blue direction',
  },
];

// ─── Bidirectionality contract: this module is complete iff ───────────────────
//
//   1. `fromXYZ` and `toXYZ` are both exported.                                 ✓
//   2. For every testVector, `fromXYZ(input)` matches `output` within tolerance.
//   3. For every testVector, `toXYZ(fromXYZ(input))` matches `input` within tolerance.
//   4. For every testVector, `fromXYZ(toXYZ(output))` matches `output` within tolerance.
//
// Verification lives in `src/test/roundtrip.ts`.
