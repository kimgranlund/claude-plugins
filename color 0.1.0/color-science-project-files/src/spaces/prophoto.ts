// Linear ProPhoto RGB (ROMM RGB) ↔ XYZ_D65
//
// ProPhoto has very wide gamut — encompasses Rec.2020 and most of Pointer's
// gamut (real surface colors). White point: **D50** (not D65). Hub conversion
// bridges D50 ↔ D65 via Bradford CAT.
//
// Transfer: piecewise 1.8 gamma (see `src/transfer/prophoto.ts`).
//
// Primary source: Eastman Kodak, "Reference Output Medium Metric RGB Color
// Encoding" (ROMM RGB). Matrices from Bruce Lindbloom's reference at D50.

import type { LinearProPhoto, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, xyz, LINEAR_TOLERANCE } from '../types.js';
import { d50ToD65, d65ToD50 } from '../adaptation/bradford.js';

// Matrices at the native D50 white point.
export const M_XYZ_D50_TO_PROPHOTO: Matrix3x3 = [
  [ 1.3459433, -0.2556075, -0.0511118],
  [-0.5445989,  1.5081673,  0.0205351],
  [ 0.0000000,  0.0000000,  1.2118128],
];

export const M_PROPHOTO_TO_XYZ_D50: Matrix3x3 = [
  [0.7976749, 0.1351917, 0.0313534],
  [0.2880402, 0.7118741, 0.0000857],
  [0.0000000, 0.0000000, 0.8252100],
];

// ProPhoto is D50-native; bridge to/from the D65 hub via Bradford.
export function toXYZ(c: LinearProPhoto): XYZ_D65 {
  const xyz_d50 = mulMat3Vec3(M_PROPHOTO_TO_XYZ_D50, c);
  return d50ToD65(xyz_d50);
}

export function fromXYZ(c: XYZ_D65): LinearProPhoto {
  const xyz_d50 = d65ToD50(c);
  const [R, G, B] = mulMat3Vec3(M_XYZ_D50_TO_PROPHOTO, xyz_d50);
  return [R, G, B] as unknown as LinearProPhoto;
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, LinearProPhoto>> = [
  {
    input: xyz(0, 0, 0),
    output: [0, 0, 0] as unknown as LinearProPhoto,
    tolerance: LINEAR_TOLERANCE,
    source: 'Black point',
  },
  // ProPhoto round-trip tolerance is loose because we chain through D50↔D65
  // Bradford adaptation (which is itself 1e-6 precise due to published matrix
  // rounding).
];
