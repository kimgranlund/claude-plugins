// Linear Rec.2020 ↔ XYZ_D65
//
// ITU-R BT.2020 primaries at D65 white point. Wider than sRGB and P3.
// Matrices from W3C CSS Color 4.

import type { LinearRec2020, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, xyz, LINEAR_TOLERANCE } from '../types.js';

/** XYZ_D65 → Linear Rec.2020. */
export const M_XYZ_TO_REC2020: Matrix3x3 = [
  [ 1.7166511880, -0.3556707838, -0.2533662814],
  [-0.6666843518,  1.6164812366,  0.0157685458],
  [ 0.0176398574, -0.0427706133,  0.9421031212],
];

/** Linear Rec.2020 → XYZ_D65. */
export const M_REC2020_TO_XYZ: Matrix3x3 = [
  [0.6369580483, 0.1446169036, 0.1688809752],
  [0.2627002120, 0.6779980715, 0.0593017165],
  [0.0000000000, 0.0280726930, 1.0609850577],
];

export function toXYZ(c: LinearRec2020): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_REC2020_TO_XYZ, c);
  return xyz(X, Y, Z);
}

export function fromXYZ(c: XYZ_D65): LinearRec2020 {
  const [R, G, B] = mulMat3Vec3(M_XYZ_TO_REC2020, c);
  return [R, G, B] as unknown as LinearRec2020;
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, LinearRec2020>> = [
  {
    input: xyz(0, 0, 0),
    output: [0, 0, 0] as unknown as LinearRec2020,
    tolerance: LINEAR_TOLERANCE,
    source: 'Trivial — black point',
  },
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: [1, 1, 1] as unknown as LinearRec2020,
    tolerance: 1e-6,
    source: 'W3C CSS Color 4 — D65 white → linear Rec.2020 (1, 1, 1)',
  },
];
