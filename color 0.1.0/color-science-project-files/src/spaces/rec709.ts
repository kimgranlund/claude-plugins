// Linear Rec.709 ↔ XYZ_D65
//
// ITU-R BT.709 primaries (BT.709-6, 2015). **Identical primaries to sRGB**;
// matrices are the same. The distinction matters only at the encode/decode
// step:
//   - sRGB uses IEC 61966-2-1 piecewise transfer
//   - Rec.709 uses BT.709 OETF (≈ Rec.2020 OETF)
//
// Most software treats Rec.709 and sRGB as interchangeable for matrix work.
// This module exists so Rec.709 can participate in the typed registry.

import type { LinearRec709, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, xyz, LINEAR_TOLERANCE } from '../types.js';

// Same matrices as sRGB (shared BT.709 primaries + D65 white point).
export const M_XYZ_TO_REC709: Matrix3x3 = [
  [ 3.2409699419, -1.5373831776, -0.4986107603],
  [-0.9692436363,  1.8759675015,  0.0415550574],
  [ 0.0556300797, -0.2039769589,  1.0569715142],
];

export const M_REC709_TO_XYZ: Matrix3x3 = [
  [0.4123907993, 0.3575843394, 0.1804807884],
  [0.2126390059, 0.7151686788, 0.0721923154],
  [0.0193308187, 0.1191947798, 0.9505321522],
];

export function toXYZ(c: LinearRec709): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_REC709_TO_XYZ, c);
  return xyz(X, Y, Z);
}

export function fromXYZ(c: XYZ_D65): LinearRec709 {
  const [R, G, B] = mulMat3Vec3(M_XYZ_TO_REC709, c);
  return [R, G, B] as unknown as LinearRec709;
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, LinearRec709>> = [
  {
    input: xyz(0, 0, 0),
    output: [0, 0, 0] as unknown as LinearRec709,
    tolerance: LINEAR_TOLERANCE,
    source: 'Trivial — black point',
  },
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: [1, 1, 1] as unknown as LinearRec709,
    tolerance: 1e-6,
    source: 'BT.709 (same primaries as sRGB) — D65 white → (1, 1, 1)',
  },
];
