// OKLCH gamut peak math — peak lightness and peak chroma against a target gamut.
//
// There is no closed-form L_peak(C) without fixing hue, because the gamut boundary
// is the unit RGB cube, which becomes a non-convex shape after the nonlinear
// OKLab → LMS' → LMS (cube) → XYZ → linear-RGB transform. For fixed (C, h), each
// linear-RGB channel is a cubic polynomial in L, and the envelope is solved
// channel-by-channel against [0, 1].
//
// See references/techniques/oklch-gamut-peak-math.md for the full derivation.

import type {
  OKLCH,
  OKLab,
  XYZ_D65,
  LinearSRGB,
  LinearP3,
  LinearRec2020,
  Matrix3x3,
} from '../types.js';
import { mulMat3Vec3, wrapHueDeg } from '../types.js';
import * as oklabSpace from '../spaces/oklab.js';

// ─── XYZ → linear-RGB matrices for each target gamut (D65) ────────────────────

/** XYZ_D65 → Linear sRGB. IEC 61966-2-1. */
export const M_XYZ_TO_SRGB: Matrix3x3 = [
  [ 3.24096994, -1.53738318, -0.49861076],
  [-0.96924364,  1.87596750,  0.04155506],
  [ 0.05563008, -0.20397696,  1.05697151],
];

/** XYZ_D65 → Linear Display P3. SMPTE EG 432-1, D65 white. */
export const M_XYZ_TO_P3: Matrix3x3 = [
  [ 2.49349691, -0.93138362, -0.40271078],
  [-0.82948897,  1.76266406,  0.02362469],
  [ 0.03584583, -0.07617239,  0.95688452],
];

/** XYZ_D65 → Linear Rec.2020. ITU-R BT.2020. */
export const M_XYZ_TO_REC2020: Matrix3x3 = [
  [ 1.71665119, -0.35567078, -0.25336628],
  [-0.66668435,  1.61648124,  0.01576855],
  [ 0.01763986, -0.04277061,  0.94210312],
];

// ─── Gamut-specific OKLCH → linear-RGB helpers ────────────────────────────────

/** Convert OKLCH to a target-gamut linear RGB vector. */
function oklchToLinearRGB(
  oklch: OKLCH,
  toRGB: Matrix3x3
): [number, number, number] {
  const [L, C, hDeg] = oklch;
  const hRad = hDeg * Math.PI / 180;
  // OKLCH → OKLab (polar to cartesian)
  const lab = [L, C * Math.cos(hRad), C * Math.sin(hRad)] as unknown as OKLab;
  // OKLab → XYZ_D65
  const xyz = oklabSpace.toXYZ(lab);
  // XYZ → linear RGB for the target gamut
  return mulMat3Vec3(toRGB, xyz);
}

/** Test whether a linear RGB triple is in $[0, 1]^3$ (i.e. inside the unit cube). */
export function inGamut(rgb: readonly [number, number, number], epsilon: number = 0): boolean {
  return (
    rgb[0] >= -epsilon && rgb[0] <= 1 + epsilon &&
    rgb[1] >= -epsilon && rgb[1] <= 1 + epsilon &&
    rgb[2] >= -epsilon && rgb[2] <= 1 + epsilon
  );
}

// ─── Peak L at fixed (C, h) ───────────────────────────────────────────────────

/**
 * Maximum lightness L ∈ [0, 1] such that OKLCH(L, C, h) is in the target gamut.
 *
 * Algorithm: binary search. The in-gamut set is convex along L at fixed (C, h)
 * because the cube is convex and the OKLCH → linear-RGB map is monotonic in L
 * at fixed (C, h).
 *
 * @param C chroma
 * @param hDeg hue in degrees
 * @param toRGB XYZ → linear-RGB matrix for the target gamut
 * @param iterations binary search iterations (default 32 = float precision)
 */
export function peakL(
  C: number,
  hDeg: number,
  toRGB: Matrix3x3,
  iterations: number = 32
): number {
  const h = wrapHueDeg(hDeg);
  let lo = 0;
  let hi = 1;
  for (let i = 0; i < iterations; i++) {
    const mid = (lo + hi) / 2;
    const rgb = oklchToLinearRGB(
      [mid, C, h] as unknown as OKLCH,
      toRGB
    );
    if (inGamut(rgb)) lo = mid;
    else hi = mid;
  }
  return lo;
}

// ─── Peak C at fixed (L, h) — more useful for design tokens ──────────────────

/**
 * Maximum chroma C such that OKLCH(L, C, h) is in the target gamut.
 *
 * More useful than peakL for design token ramps, which typically fix lightness
 * per step and want maximum chroma at each hue.
 *
 * @param L lightness in [0, 1]
 * @param hDeg hue in degrees
 * @param toRGB XYZ → linear-RGB matrix for the target gamut
 * @param iterations binary search iterations (default 32)
 * @param cMax upper bound for search; 0.4 covers sRGB and P3, use 0.5 for Rec.2020
 */
export function peakC(
  L: number,
  hDeg: number,
  toRGB: Matrix3x3,
  iterations: number = 32,
  cMax: number = 0.4
): number {
  const h = wrapHueDeg(hDeg);
  let lo = 0;
  let hi = cMax;
  for (let i = 0; i < iterations; i++) {
    const mid = (lo + hi) / 2;
    const rgb = oklchToLinearRGB(
      [L, mid, h] as unknown as OKLCH,
      toRGB
    );
    if (inGamut(rgb)) lo = mid;
    else hi = mid;
  }
  return lo;
}

// ─── Peak L across all hues — for envelope analysis ──────────────────────────

/**
 * Maximum L_peak(C, h) across all hues at fixed chroma C.
 *
 * Returns both the peak lightness and the hue that achieves it.
 * Use for gamut envelope analysis, not for per-color-family design tokens.
 *
 * @param hueSteps number of hue samples around the circle (default 720 = 0.5° resolution)
 */
export function peakLOverHue(
  C: number,
  toRGB: Matrix3x3,
  hueSteps: number = 720
): { L: number; hDeg: number } {
  let bestL = 0;
  let bestH = 0;
  for (let i = 0; i < hueSteps; i++) {
    const h = (i / hueSteps) * 360;
    const L = peakL(C, h, toRGB);
    if (L > bestL) {
      bestL = L;
      bestH = h;
    }
  }
  return { L: bestL, hDeg: bestH };
}

// ─── Gamut-specific convenience wrappers ─────────────────────────────────────

export const peakL_sRGB = (C: number, hDeg: number) => peakL(C, hDeg, M_XYZ_TO_SRGB);
export const peakL_P3 = (C: number, hDeg: number) => peakL(C, hDeg, M_XYZ_TO_P3);
export const peakL_Rec2020 = (C: number, hDeg: number) => peakL(C, hDeg, M_XYZ_TO_REC2020);

export const peakC_sRGB = (L: number, hDeg: number) => peakC(L, hDeg, M_XYZ_TO_SRGB);
export const peakC_P3 = (L: number, hDeg: number) => peakC(L, hDeg, M_XYZ_TO_P3);
export const peakC_Rec2020 = (L: number, hDeg: number) => peakC(L, hDeg, M_XYZ_TO_REC2020, 32, 0.5);

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'peakL_sRGB(C=0, h=0) ≈ 1 (achromatic)',
    fn: () => peakL_sRGB(0, 0),
    expected: 1.0,
    tolerance: 1e-3,
    source: 'C=0 → achromatic → peak L is 1 (sRGB white) — binary search lands just below 1 due to float drift in OKLCH→RGB',
  },
  {
    name: 'peakC_sRGB(L=1, h=0) = 0 (white point)',
    fn: () => peakC_sRGB(1.0, 0),
    expected: 0.0,
    tolerance: 1e-6,
    source: 'L=1 → white point → peak C is 0',
  },
  {
    name: 'peakC_sRGB(L=0, h=0) = 0 (black point)',
    fn: () => peakC_sRGB(0.0, 0),
    expected: 0.0,
    tolerance: 1e-6,
    source: 'L=0 → black point → peak C is 0',
  },
  {
    name: 'peakL_sRGB(C=0.1, h=29) is in [0, 1]',
    fn: () => {
      const L = peakL_sRGB(0.1, 29);
      return L >= 0 && L <= 1 ? 0 : 1;
    },
    expected: 0,
    tolerance: 0,
    source: 'Peak lightness always lands in unit interval',
  },
  {
    name: 'peakC_P3 wider than peakC_sRGB at red mid-tone',
    fn: () => {
      const cSRGB = peakC_sRGB(0.5, 29);
      const cP3 = peakC_P3(0.5, 29);
      return cP3 > cSRGB ? 0 : 1;
    },
    expected: 0,
    tolerance: 0,
    source: 'P3 has wider gamut than sRGB → peak C should be larger',
  },
];
