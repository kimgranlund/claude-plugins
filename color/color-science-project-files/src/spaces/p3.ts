// Linear Display P3 ↔ XYZ_D65
//
// Display P3 = DCI-P3 primaries with D65 white point + sRGB transfer function.
// Matrices from W3C CSS Color 4 (derived from SMPTE EG 432-1 with D65 adaptation).
//
// IMPORTANT: this module handles LINEAR P3 only. Use `src/transfer/srgb.ts` for
// encoding/decoding (Display P3 shares the sRGB transfer function).

import type { LinearP3, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, linearP3, xyz, LINEAR_TOLERANCE } from '../types.js';

/** XYZ_D65 → Linear Display P3. */
export const M_XYZ_TO_P3: Matrix3x3 = [
  [ 2.4934969119, -0.9313836179, -0.4027107845],
  [-0.8294889696,  1.7626640603,  0.0236246858],
  [ 0.0358458302, -0.0761723893,  0.9568845240],
];

/** Linear Display P3 → XYZ_D65. */
export const M_P3_TO_XYZ: Matrix3x3 = [
  [0.4865709486, 0.2656676932, 0.1982172852],
  [0.2289745641, 0.6917385241, 0.0792869117],
  [0.0000000000, 0.0451133819, 1.0439443689],
];

export function toXYZ(c: LinearP3): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_P3_TO_XYZ, c);
  return xyz(X, Y, Z);
}

export function fromXYZ(c: XYZ_D65): LinearP3 {
  const [R, G, B] = mulMat3Vec3(M_XYZ_TO_P3, c);
  return linearP3(R, G, B);
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, LinearP3>> = [
  {
    input: xyz(0, 0, 0),
    output: linearP3(0, 0, 0),
    tolerance: LINEAR_TOLERANCE,
    source: 'Trivial — black point',
  },
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: linearP3(1, 1, 1),
    tolerance: 1e-6,
    source: 'W3C CSS Color 4 — D65 white → linear P3 (1, 1, 1)',
  },
];
