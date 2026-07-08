// CIELAB at D65 ↔ XYZ_D65
//
// L* ∈ [0, 100], a* and b* roughly ∈ [-128, 128]. Cube-root nonlinearity at f(t).
//
// IMPORTANT: traditional CIELAB uses a D50 reference white. This module uses D65
// to match the modern display ecosystem. D50 variants live in src/spaces/cielab-d50.ts
// (to be written) and conversion goes through `src/adaptation/bradford.ts`.
//
// Primary source: CIE 015:2018 (Colorimetry, 4th edition)

import type { CIELAB_D65, XYZ_D65, TestVector } from '../types.js';
import { cielab_D65, xyz, NONLINEAR_TOLERANCE } from '../types.js';

// D65 reference white in XYZ (normalized so Yn = 1).
const Xn = 0.9504559270516716;
const Yn = 1.0;
const Zn = 1.0890577507598784;

// CIELAB f(t) parameters (CIE 015 / 2-degree observer).
const DELTA = 6 / 29;
const DELTA_CUBED = DELTA * DELTA * DELTA;            // ≈ 0.008856
const THREE_DELTA_SQ = 3 * DELTA * DELTA;             // ≈ 0.128419
const FOUR_OVER_29 = 4 / 29;                          // ≈ 0.137931

function f(t: number): number {
  if (t > DELTA_CUBED) return Math.cbrt(t);
  return t / THREE_DELTA_SQ + FOUR_OVER_29;
}

function fInverse(t: number): number {
  if (t > DELTA) return t * t * t;
  return THREE_DELTA_SQ * (t - FOUR_OVER_29);
}

export function fromXYZ(c: XYZ_D65): CIELAB_D65 {
  const fx = f(c[0] / Xn);
  const fy = f(c[1] / Yn);
  const fz = f(c[2] / Zn);
  return cielab_D65(
    116 * fy - 16,
    500 * (fx - fy),
    200 * (fy - fz)
  );
}

export function toXYZ(c: CIELAB_D65): XYZ_D65 {
  const fy = (c[0] + 16) / 116;
  const fx = fy + c[1] / 500;
  const fz = fy - c[2] / 200;
  return xyz(Xn * fInverse(fx), Yn * fInverse(fy), Zn * fInverse(fz));
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, CIELAB_D65>> = [
  {
    input: xyz(0, 0, 0),
    output: cielab_D65(0, 0, 0),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'CIE 015 — black point → L*a*b* (0, 0, 0)',
  },
  {
    input: xyz(Xn, Yn, Zn),
    output: cielab_D65(100, 0, 0),
    tolerance: 1e-6,
    source: 'CIE 015 — D65 white → L*=100, a*=b*=0',
  },
  {
    input: xyz(Xn * 0.5, Yn * 0.5, Zn * 0.5),
    output: cielab_D65(76.06926101, 0, 0),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'CIE 015 — 50% gray (Y=0.5) → L* ≈ 76.07',
  },
];
