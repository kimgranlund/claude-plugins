// Jzazbz ↔ XYZ_D65 — HDR uniform color space (Safdar et al. 2017).
//
// Designed for HDR content (up to 10,000 nits absolute luminance). The PQ-like
// nonlinearity gives perceptual uniformity across the full HDR luminance range,
// fixing the limitation of OKLab and CIELAB (calibrated for SDR luminance).
//
// Pipeline:
//   XYZ → X'Y'Z' (pre-adaptation) → LMS → PQ-like nonlinearity → opponent (Jz, az, bz)
//
// Use cases: HDR display work, cross-luminance color difference, scientific
// HDR visualization. For SDR UI work, OKLab is the right choice.
//
// Primary source: Safdar, Cui, Kim, Luo (2017), "Perceptually uniform color
// space for image signals including high dynamic range and wide gamut,"
// Optics Express 25(13), 15131-15151.

import type { Jzazbz, XYZ_D65, Matrix3x3 } from '../types.js';
import { mulMat3Vec3, xyz } from '../types.js';

// ─── Pre-adaptation constants ─────────────────────────────────────────────────

const B = 1.15;
const G = 0.66;

// ─── PQ-like nonlinearity constants ───────────────────────────────────────────

const N = 2610 / 16384;          // m1
const M = 1.7 * 2523 / 32;       // m2 (note: 1.7 prefactor differs from PQ)
const C1 = 3424 / 4096;
const C2 = 2413 / 128;
const C3 = 2392 / 128;
const D_J = -0.56;               // J offset adjustment
const D0 = 1.6295499532821566e-11; // black-point offset

// ─── Matrices ─────────────────────────────────────────────────────────────────

/** XYZ → LMS (pre-adaptation) */
const M1: Matrix3x3 = [
  [ 0.41478972,  0.579999,    0.014648],
  [-0.20151,     1.120649,    0.0531008],
  [-0.0166008,   0.2648,      0.6684799],
];

/** LMS → Jzazbz cartesian. */
const M2: Matrix3x3 = [
  [0.5,        0.5,         0.0],
  [3.524000,  -4.066708,    0.542708],
  [0.199076,   1.096799,   -1.295875],
];

const M1_INV: Matrix3x3 = [
  [ 1.9242264358, -1.0047923126,  0.0376514040],
  [ 0.3503167621,  0.7264811939, -0.0653844229],
  [-0.0909828110, -0.3127282905,  1.5227665613],
];

const M2_INV: Matrix3x3 = [
  [1.0,  0.1386050432,  0.0580473162],
  [1.0, -0.1386050432, -0.0580473162],
  [1.0, -0.0960192421, -0.8118918960],
];

// ─── PQ-like forward / inverse ────────────────────────────────────────────────

function pqLike(x: number): number {
  const xp = Math.pow(Math.max(x, 0) / 10000, N);
  return Math.pow((C1 + C2 * xp) / (1 + C3 * xp), M);
}

function pqLikeInverse(y: number): number {
  const yp = Math.pow(Math.max(y, 0), 1 / M);
  const num = C1 - yp;
  const den = C3 * yp - C2;
  return 10000 * Math.pow(num / den, 1 / N);
}

// ─── Forward: XYZ_D65 → Jzazbz ────────────────────────────────────────────────
//
// Note: input XYZ is in our normalized [0, 1] scale. The paper uses 0-10000
// absolute luminance. We multiply by 10000 internally for the PQ-like step.

export function fromXYZ(c: XYZ_D65): Jzazbz {
  // Scale to 0-10000 nits for PQ-like nonlinearity.
  const X = c[0] * 10000;
  const Y = c[1] * 10000;
  const Z = c[2] * 10000;

  // Pre-adaptation.
  const Xp = B * X - (B - 1) * Z;
  const Yp = G * Y - (G - 1) * X;

  // XYZ' → LMS.
  const lms = mulMat3Vec3(M1, [Xp, Yp, Z] as const);

  // PQ-like nonlinearity per component.
  const lmsP = [pqLike(lms[0]), pqLike(lms[1]), pqLike(lms[2])] as const;

  // LMS' → Iz, az, bz.
  const [Iz, az, bz] = mulMat3Vec3(M2, lmsP);

  // Jz from Iz.
  const Jz = ((1 + D_J) * Iz) / (1 + D_J * Iz) - D0;

  return [Jz, az, bz] as unknown as Jzazbz;
}

// ─── Inverse: Jzazbz → XYZ_D65 ────────────────────────────────────────────────

export function toXYZ(c: Jzazbz): XYZ_D65 {
  const [Jz, az, bz] = c;

  // Jz → Iz.
  const JzPlusD0 = Jz + D0;
  const Iz = JzPlusD0 / (1 + D_J - D_J * JzPlusD0);

  // (Iz, az, bz) → LMS'.
  const lmsP = mulMat3Vec3(M2_INV, [Iz, az, bz] as const);

  // Inverse PQ-like.
  const lms = [pqLikeInverse(lmsP[0]), pqLikeInverse(lmsP[1]), pqLikeInverse(lmsP[2])] as const;

  // LMS → XYZ'.
  const [Xp, Yp, Z] = mulMat3Vec3(M1_INV, lms);

  // Inverse pre-adaptation.
  const X = (Xp + (B - 1) * Z) / B;
  const Y = (Yp + (G - 1) * X) / G;

  // Scale back to [0, 1] convention.
  return xyz(X / 10000, Y / 10000, Z / 10000);
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { TestVector } from '../types.js';

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, Jzazbz>> = [
  {
    input: xyz(0, 0, 0),
    output: [0 - D0, 0, 0] as unknown as Jzazbz,
    tolerance: 1e-3,
    source: 'Black point — Jz = -D0 ≈ 0, az = bz = 0',
  },
];
