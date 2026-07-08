// Linear sRGB ↔ XYZ_D65
//
// Matrix values from IEC 61966-2-1:1999 (Annex E) and the W3C CSS Color 4
// derivation. Primaries: BT.709 chromaticities at D65 white point.
//
// IMPORTANT: this module handles LINEAR sRGB only. Gamma encoding/decoding
// (the piecewise transfer with the 1.055 power curve) lives in
// `src/transfer/srgb.ts`. The encoded → linear → XYZ path is:
//   import * as srgbTransfer from '../transfer/srgb.js';
//   import * as srgbSpace from '../spaces/srgb.js';
//   const xyzColor = srgbSpace.toXYZ(srgbTransfer.decode(encoded));

import type { LinearSRGB, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, linearSRGB, xyz, LINEAR_TOLERANCE } from '../types.js';

/** XYZ_D65 → Linear sRGB. IEC 61966-2-1 derived. */
export const M_XYZ_TO_SRGB: Matrix3x3 = [
  [ 3.2409699419, -1.5373831776, -0.4986107603],
  [-0.9692436363,  1.8759675015,  0.0415550574],
  [ 0.0556300797, -0.2039769589,  1.0569715142],
];

/** Linear sRGB → XYZ_D65. */
export const M_SRGB_TO_XYZ: Matrix3x3 = [
  [0.4123907993, 0.3575843394, 0.1804807884],
  [0.2126390059, 0.7151686788, 0.0721923154],
  [0.0193308187, 0.1191947798, 0.9505321522],
];

export function toXYZ(c: LinearSRGB): XYZ_D65 {
  const [X, Y, Z] = mulMat3Vec3(M_SRGB_TO_XYZ, c);
  return xyz(X, Y, Z);
}

export function fromXYZ(c: XYZ_D65): LinearSRGB {
  const [R, G, B] = mulMat3Vec3(M_XYZ_TO_SRGB, c);
  return linearSRGB(R, G, B);
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, LinearSRGB>> = [
  {
    input: xyz(0, 0, 0),
    output: linearSRGB(0, 0, 0),
    tolerance: LINEAR_TOLERANCE,
    source: 'Trivial — black point',
  },
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: linearSRGB(1, 1, 1),
    tolerance: 1e-6,
    source: 'IEC 61966-2-1 — D65 white → linear sRGB (1, 1, 1)',
  },
  {
    input: xyz(0.4123907993, 0.2126390059, 0.0193308187),
    output: linearSRGB(1, 0, 0),
    tolerance: 1e-6,
    source: 'IEC 61966-2-1 — pure red column of M_SRGB_TO_XYZ',
  },
  {
    input: xyz(0.3575843394, 0.7151686788, 0.1191947798),
    output: linearSRGB(0, 1, 0),
    tolerance: 1e-6,
    source: 'IEC 61966-2-1 — pure green column of M_SRGB_TO_XYZ',
  },
  {
    input: xyz(0.1804807884, 0.0721923154, 0.9505321522),
    output: linearSRGB(0, 0, 1),
    tolerance: 1e-6,
    source: 'IEC 61966-2-1 — pure blue column of M_SRGB_TO_XYZ',
  },
];
