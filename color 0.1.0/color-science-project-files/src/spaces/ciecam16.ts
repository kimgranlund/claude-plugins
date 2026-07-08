// CIECAM16 (JMh form) ↔ XYZ_D65
//
// CIECAM16 is a color appearance model that predicts how colors appear under
// specific viewing conditions. Output is (J, M, h):
//   J = lightness    [0, 100]
//   M = colorfulness [0, ~100]
//   h = hue          [0, 360)
//
// This module bakes in the "default display viewing conditions" used by
// Material Design 3 HCT (D65 white, average surround, La≈64, Yb=20).
// For non-default viewing conditions, see the `ViewingConditions` struct.
//
// Primary sources:
//   - CIE 248:2022 (CIECAM16)
//   - Material Color Utilities reference implementation:
//     https://github.com/material-foundation/material-color-utilities

import type { CIECAM16_JMh, XYZ_D65, Matrix3x3, TestVector } from '../types.js';
import { mulMat3Vec3, ciecam16_JMh, xyz, wrapHueDeg, NONLINEAR_TOLERANCE } from '../types.js';

// ─── CAT16 matrix (chromatic adaptation transform) ────────────────────────────

const M_CAT16: Matrix3x3 = [
  [ 0.401288,  0.650173, -0.051461],
  [-0.250268,  1.204414,  0.045854],
  [-0.002079,  0.048952,  0.953127],
];

const M_CAT16_INV: Matrix3x3 = [
  [ 1.86206786, -1.01125463,  0.14918677],
  [ 0.38752654,  0.62144744, -0.00897398],
  [-0.01584150, -0.03412294,  1.04996444],
];

// ─── Viewing conditions ───────────────────────────────────────────────────────

export type ViewingConditions = Readonly<{
  whitePointXYZ: readonly [number, number, number];  // 0-100 scale
  adaptingLuminance: number;                         // La (cd/m²)
  backgroundLstar: number;                           // L* of the background [0, 100]
  surround: number;                                  // 0=dark, 1=dim, 2=average
  discountingIlluminant: boolean;
}>;

export type PrecomputedVC = Readonly<{
  vc: ViewingConditions;
  n: number;
  aw: number;
  nbb: number;
  ncb: number;
  c: number;
  nc: number;
  rgbD: readonly [number, number, number];
  fl: number;
  flRoot: number;
  z: number;
}>;

// Y at L*=50 ≈ 18.418 (CIELAB inverse). Material uses this for default La.
const Y_AT_LSTAR_50 = 18.41835828999998;

/** Defaults match Material Design 3 HCT defaults (D65 sRGB display).
 *
 *  IMPORTANT: the white point uses the W3C CSS Color 4 high-precision D65 values,
 *  scaled to Yw=100. This matches the D65 used by `src/types.ts:xyz(...)` and
 *  every other module in this skill. Using ASTM-rounded (95.047, 100, 108.883)
 *  would produce ~2.3 residual chroma at the white point. */
export const DEFAULT_VC: ViewingConditions = {
  whitePointXYZ: [95.04559270516716, 100.0, 108.90577507598784],
  adaptingLuminance: (200.0 / Math.PI) * Y_AT_LSTAR_50 / 100.0,
  backgroundLstar: 50.0,
  surround: 2,
  discountingIlluminant: false,
};

function precompute(vc: ViewingConditions): PrecomputedVC {
  const [Xw, Yw, Zw] = vc.whitePointXYZ;

  const rgbW = mulMat3Vec3(M_CAT16, [Xw, Yw, Zw] as const);

  const f = vc.surround === 0 ? 0.8 : vc.surround === 1 ? 0.9 : 1.0;
  const c = vc.surround === 0 ? 0.525 : vc.surround === 1 ? 0.59 : 0.69;
  const nc = c === 0.525 ? 0.8 : c === 0.59 ? 0.9 : 1.0;

  const dRaw = f * (1 - (1 / 3.6) * Math.exp((-vc.adaptingLuminance - 42) / 92));
  const d = vc.discountingIlluminant ? 1 : Math.max(0, Math.min(1, dRaw));

  const rgbD: [number, number, number] = [
    d * (100.0 / rgbW[0]) + 1 - d,
    d * (100.0 / rgbW[1]) + 1 - d,
    d * (100.0 / rgbW[2]) + 1 - d,
  ];

  const k = 1 / (5 * vc.adaptingLuminance + 1);
  const k4 = k * k * k * k;
  const k4_1 = 1 - k4;
  const fl = k4 * vc.adaptingLuminance +
             0.1 * k4_1 * k4_1 * Math.cbrt(5 * vc.adaptingLuminance);
  const flRoot = Math.pow(fl, 0.25);

  // Yb derived from backgroundLstar via CIELAB inverse transform.
  const yFromLstar = (L: number): number => {
    const fy = (L + 16) / 116;
    const delta = 6 / 29;
    return fy > delta ? fy ** 3 * 100 : (3 * delta * delta) * (fy - 4 / 29) * 100;
  };
  const yb = yFromLstar(vc.backgroundLstar);
  const n = yb / Yw;

  const nbb = 0.725 * Math.pow(1 / n, 0.2);
  const ncb = nbb;

  // Adapted white response.
  const rgbAW: [number, number, number] = [
    rgbD[0] * rgbW[0],
    rgbD[1] * rgbW[1],
    rgbD[2] * rgbW[2],
  ];
  const rgbAfW: [number, number, number] = [
    adaptResponse(rgbAW[0], fl),
    adaptResponse(rgbAW[1], fl),
    adaptResponse(rgbAW[2], fl),
  ];
  const aw = (2 * rgbAfW[0] + rgbAfW[1] + 0.05 * rgbAfW[2]) * nbb;

  const z = 1.48 + Math.sqrt(n);

  return { vc, n, aw, nbb, ncb, c, nc, rgbD, fl, flRoot, z };
}

// Post-adaptation cone response. Matches Material color-utilities convention
// (no +0.1 offset). The CIE 248:2022 formula adds +0.1; Material omits it so
// that J=0 at black. We follow Material's convention for HCT compatibility.
function adaptResponse(component: number, fl: number): number {
  const sign = Math.sign(component);
  const abs = Math.abs(component);
  const x = Math.pow((fl * abs) / 100, 0.42);
  return (sign * 400 * x) / (x + 27.13);
}

function unadaptResponse(value: number, fl: number): number {
  const sign = Math.sign(value);
  const abs = Math.abs(value);
  const denom = Math.max(0, 400 - abs);
  if (denom === 0) return 0;
  return sign * (100 / fl) * Math.pow((27.13 * abs) / denom, 1 / 0.42);
}

// ─── Forward: XYZ_D65 → CIECAM16 ──────────────────────────────────────────────

export function fromXYZ(c: XYZ_D65, pre: PrecomputedVC = precompute(DEFAULT_VC)): CIECAM16_JMh {
  // CIECAM16 works in 0-100 luminance scale (XYZ_D65 in our system is 0-1 normalized).
  const X100 = c[0] * 100, Y100 = c[1] * 100, Z100 = c[2] * 100;
  const rgb = mulMat3Vec3(M_CAT16, [X100, Y100, Z100] as const);
  const rgbAdapted: [number, number, number] = [
    pre.rgbD[0] * rgb[0],
    pre.rgbD[1] * rgb[1],
    pre.rgbD[2] * rgb[2],
  ];
  const rgbAf: [number, number, number] = [
    adaptResponse(rgbAdapted[0], pre.fl),
    adaptResponse(rgbAdapted[1], pre.fl),
    adaptResponse(rgbAdapted[2], pre.fl),
  ];

  const a = rgbAf[0] - (12 * rgbAf[1]) / 11 + rgbAf[2] / 11;
  const b = (rgbAf[0] + rgbAf[1] - 2 * rgbAf[2]) / 9;

  let hRad = Math.atan2(b, a);
  let hDeg = hRad * (180 / Math.PI);
  if (hDeg < 0) hDeg += 360;

  const eccentricity = 0.25 * (Math.cos(hRad + 2) + 3.8);

  const achromaticResponse = (2 * rgbAf[0] + rgbAf[1] + 0.05 * rgbAf[2]) * pre.nbb;

  const Jbase = Math.max(0, achromaticResponse / pre.aw);
  const J = 100 * Math.pow(Jbase, pre.c * pre.z);

  const t = (50000 / 13 * pre.nc * pre.ncb * eccentricity * Math.sqrt(a * a + b * b)) /
            (rgbAf[0] + rgbAf[1] + 21 * rgbAf[2] / 20);
  const alpha = Math.pow(t, 0.9) * Math.pow(1.64 - Math.pow(0.29, pre.n), 0.73);
  const C = alpha * Math.sqrt(J / 100);
  const M = C * pre.flRoot;

  return ciecam16_JMh(J, M, hDeg);
}

// ─── Inverse: CIECAM16 → XYZ_D65 ──────────────────────────────────────────────

export function toXYZ(jmh: CIECAM16_JMh, pre: PrecomputedVC = precompute(DEFAULT_VC)): XYZ_D65 {
  const [J, M, hDeg] = jmh;
  const h = wrapHueDeg(hDeg);
  const hRad = h * (Math.PI / 180);

  const alpha = M / pre.flRoot / Math.sqrt(Math.max(J, 1e-12) / 100);
  const t = Math.pow(alpha / Math.pow(1.64 - Math.pow(0.29, pre.n), 0.73), 1 / 0.9);

  const eccentricity = 0.25 * (Math.cos(hRad + 2) + 3.8);
  const A = pre.aw * Math.pow(J / 100, 1 / (pre.c * pre.z));

  const p1 = (50000 / 13) * pre.nc * pre.ncb * eccentricity;
  const p2 = A / pre.nbb;

  const hSin = Math.sin(hRad);
  const hCos = Math.cos(hRad);

  const gamma = (23 * (p2 + 0.305) * t) /
                (23 * p1 + 11 * t * hCos + 108 * t * hSin);
  const a = gamma * hCos;
  const b = gamma * hSin;

  const rA = (460 * p2 + 451 * a + 288 * b) / 1403;
  const gA = (460 * p2 - 891 * a - 261 * b) / 1403;
  const bA = (460 * p2 - 220 * a - 6300 * b) / 1403;

  const rC = unadaptResponse(rA, pre.fl);
  const gC = unadaptResponse(gA, pre.fl);
  const bC = unadaptResponse(bA, pre.fl);

  const rUnadapted = rC / pre.rgbD[0];
  const gUnadapted = gC / pre.rgbD[1];
  const bUnadapted = bC / pre.rgbD[2];

  const [X100, Y100, Z100] = mulMat3Vec3(
    M_CAT16_INV,
    [rUnadapted, gUnadapted, bUnadapted] as const
  );

  return xyz(X100 / 100, Y100 / 100, Z100 / 100);
}

// ─── Test vectors ─────────────────────────────────────────────────────────────
//
// Note: CIECAM16 round-trip is somewhat tolerant (~1e-2) due to accumulated
// nonlinearity. For strict numerical verification, cross-check against Material's
// reference implementation.

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, CIECAM16_JMh>> = [
  {
    input: xyz(0, 0, 0),
    output: ciecam16_JMh(0, 0, 0),
    tolerance: 1e-3,
    source: 'Black point — J=M=0, hue indeterminate (atan2(0,0)=0)',
  },
];
