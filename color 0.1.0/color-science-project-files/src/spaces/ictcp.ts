// ICtCp ↔ XYZ_D65 (BT.2100 HDR opponent encoding).
//
// Dolby's HDR-native opponent color space, standardized in ITU-R BT.2100.
// Used for HDR video encoding (PQ or HLG-encoded ICtCp). Constant-luminance
// preservation under PQ encoding makes it more efficient than Y'CbCr for HDR.
//
// Pipeline:
//   XYZ → Rec.2020 linear RGB → LMS (Rec.2020-LMS matrix) → PQ encoding → ICtCp
//
// Different from Jzazbz: ICtCp uses the **actual** SMPTE 2084 PQ (10,000 nit
// reference), while Jzazbz uses a PQ-like nonlinearity with adjusted exponents.
//
// Primary source: ITU-R BT.2100-2 (2018); Dolby Laboratories ICtCp white paper.

import type { ICtCp, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3 } from '../types.js';
import * as rec2020 from './rec2020.js';
import * as pq from '../transfer/pq.js';

// Rec.2020 → LMS (BT.2100 matrix, scaled to keep values in HDR range).
const M_REC2020_TO_LMS: Matrix3x3 = [
  [0.412218, 0.523925, 0.063857],
  [0.166745, 0.720429, 0.112826],
  [0.024311, 0.075463, 0.900226],
];

// LMS → Rec.2020 (inverse).
const M_LMS_TO_REC2020: Matrix3x3 = [
  [ 3.43661, -2.50645,  0.069848],
  [-0.79133,  1.98360, -0.192271],
  [-0.025950, -0.098913, 1.124863],
];

// PQ-encoded LMS' → (I, Ct, Cp).
const M_LMSp_TO_ICTCP: Matrix3x3 = [
  [0.500000,  0.500000,  0.000000],
  [1.613770, -3.323486,  1.709716],
  [4.378174, -4.245605, -0.132568],
];

// Inverse: (I, Ct, Cp) → PQ-encoded LMS'.
const M_ICTCP_TO_LMSp: Matrix3x3 = [
  [1.0,  0.008609,  0.111029],
  [1.0, -0.008609, -0.111029],
  [1.0,  0.560031, -0.320627],
];

export function fromXYZ(c: XYZ_D65): ICtCp {
  // XYZ → Rec.2020 linear
  const rec = rec2020.fromXYZ(c);
  // Rec.2020 → LMS
  const lms = mulMat3Vec3(M_REC2020_TO_LMS, rec);
  // Apply PQ encoding per LMS component (PQ expects values in [0, 1] = [0, 10000 nits])
  const lmsP: [number, number, number] = [
    pq.encodeComponent(Math.max(0, lms[0])),
    pq.encodeComponent(Math.max(0, lms[1])),
    pq.encodeComponent(Math.max(0, lms[2])),
  ];
  // LMS' → ICtCp
  const [I, Ct, Cp] = mulMat3Vec3(M_LMSp_TO_ICTCP, lmsP);
  return [I, Ct, Cp] as unknown as ICtCp;
}

export function toXYZ(c: ICtCp): XYZ_D65 {
  // ICtCp → LMS'
  const lmsP = mulMat3Vec3(M_ICTCP_TO_LMSp, c);
  // Inverse PQ per component
  const lms: [number, number, number] = [
    pq.decodeComponent(lmsP[0]),
    pq.decodeComponent(lmsP[1]),
    pq.decodeComponent(lmsP[2]),
  ];
  // LMS → Rec.2020 linear
  const rec = mulMat3Vec3(M_LMS_TO_REC2020, lms);
  // Rec.2020 → XYZ
  return rec2020.toXYZ(rec as unknown as Parameters<typeof rec2020.toXYZ>[0]);
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, ICtCp>> = [
  {
    input: { 0: 0, 1: 0, 2: 0, length: 3 } as unknown as XYZ_D65,
    output: [0, 0, 0] as unknown as ICtCp,
    tolerance: 1e-3,
    source: 'Black point — all zero (PQ at 0 is 0)',
  },
];
