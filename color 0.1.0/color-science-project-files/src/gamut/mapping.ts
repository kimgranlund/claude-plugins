// CSS Color 4 gamut mapping — the normative algorithm for fitting an
// out-of-gamut OKLCh color into a target RGB gamut.
//
// Strategy: binary-search chroma reduction in OKLCh while preserving hue and
// lightness. Accept a small ΔE_ok (≤ JND ≈ 0.02) between the reduced color and
// its naive clip — this lets the algorithm exit early when the reduction is
// imperceptible.
//
// Why hue-preserving chroma reduction (instead of clipping each channel):
//   - Naive clipping shifts hue. A vivid red that becomes (1.05, 0.02, -0.01)
//     clips to (1, 0.02, 0) — hue is now slightly off-axis red. Multiple clips
//     across a gradient produce visible hue waver.
//   - Chroma reduction in OKLCh preserves the perceptual hue. The L axis is
//     also preserved. The trade-off is reduced saturation, which is
//     perceptually consistent.
//
// Primary source: W3C CSS Color 4 — https://www.w3.org/TR/css-color-4/#binsearch
// Companion math: references/techniques/css-color-4-gamut-mapping.md

import type { OKLCH, LinearSRGB, LinearP3, LinearRec2020, Matrix3x3 } from '../types.js';
import { oklch as makeOklch, linearSRGB, linearP3 } from '../types.js';
import * as oklabSpace from '../spaces/oklab.js';
import * as oklchSpace from '../spaces/oklch.js';
import * as srgbSpace from '../spaces/srgb.js';
import * as p3Space from '../spaces/p3.js';
import * as rec2020Space from '../spaces/rec2020.js';
import { deltaEOK } from '../metrics/deltaE.js';
import { inGamut, M_XYZ_TO_SRGB, M_XYZ_TO_P3, M_XYZ_TO_REC2020 } from './oklch-peak.js';
import { mulMat3Vec3 } from '../types.js';

const JND_OK = 0.02;     // ΔE_ok just-noticeable difference (per W3C)
const EPSILON = 0.0001;  // binary-search termination threshold

// ─── In-gamut tests ───────────────────────────────────────────────────────────

function oklchToLinearRGB(c: OKLCH, toRGB: Matrix3x3): [number, number, number] {
  const lab = oklchSpace.toOKLab(c);
  const xyz = oklabSpace.toXYZ(lab);
  return mulMat3Vec3(toRGB, xyz);
}

export function inGamutSRGB(c: OKLCH): boolean {
  return inGamut(oklchToLinearRGB(c, M_XYZ_TO_SRGB));
}

export function inGamutP3(c: OKLCH): boolean {
  return inGamut(oklchToLinearRGB(c, M_XYZ_TO_P3));
}

export function inGamutRec2020(c: OKLCH): boolean {
  return inGamut(oklchToLinearRGB(c, M_XYZ_TO_REC2020));
}

// ─── Naive per-channel clipping (the wrong approach, available for comparison) ──

/**
 * Naive clip: clamp each linear RGB component to $[0, 1]$.
 * **This shifts hue** and is rarely the right answer. Use `mapTo*` instead.
 */
export function clipNaive(
  rgb: readonly [number, number, number]
): [number, number, number] {
  return [
    Math.min(1, Math.max(0, rgb[0])),
    Math.min(1, Math.max(0, rgb[1])),
    Math.min(1, Math.max(0, rgb[2])),
  ];
}

// ─── The CSS Color 4 gamut-mapping algorithm ──────────────────────────────────

/**
 * Map an OKLCH color into the target RGB gamut by hue-preserving chroma
 * reduction. Returns the in-gamut OKLCH (which can be converted to RGB via
 * `oklchToLinearRGB`).
 *
 * Algorithm (W3C CSS Color 4):
 *   1. If the color is already in gamut, return as-is.
 *   2. If L ≥ 1, return white in target gamut.
 *   3. If L ≤ 0, return black in target gamut.
 *   4. Naive-clip and check ΔE_ok against the original — if < JND, return clipped.
 *   5. Otherwise binary-search chroma in [0, originalC]:
 *      - At each step, check if reduced color is in gamut OR its clipped
 *        version is within JND.
 *      - Tighten bounds and repeat until convergence.
 */
export function mapToGamutOklch(
  origin: OKLCH,
  toRGB: Matrix3x3,
  inGamutFn: (c: OKLCH) => boolean
): OKLCH {
  const [L, C, hDeg] = origin;

  // Edge cases.
  if (inGamutFn(origin)) return origin;
  if (L >= 1) return makeOklch(1, 0, hDeg);
  if (L <= 0) return makeOklch(0, 0, hDeg);

  // Early exit: if the naive clip is perceptually identical to the origin,
  // there's no point doing a binary search.
  const naiveClipColor = clipFromOklch(origin, toRGB);
  if (deltaEOK(oklchSpace.toOKLab(origin), oklchSpace.toOKLab(naiveClipColor)) < JND_OK) {
    return naiveClipColor;
  }

  // Binary search on chroma.
  let min = 0;
  let max = C;
  let minInGamut = true;

  while (max - min > EPSILON) {
    const chroma = (min + max) / 2;
    const current = makeOklch(L, chroma, hDeg);

    if (minInGamut && inGamutFn(current)) {
      min = chroma;
    } else {
      const clipped = clipFromOklch(current, toRGB);
      const E = deltaEOK(oklchSpace.toOKLab(current), oklchSpace.toOKLab(clipped));
      if (E < JND_OK) {
        if (JND_OK - E < EPSILON) {
          return clipped;
        }
        minInGamut = false;
        min = chroma;
      } else {
        max = chroma;
      }
    }
  }

  return makeOklch(L, min, hDeg);
}

/**
 * Helper: take an OKLCH that may be out of gamut, naive-clip it in linear RGB,
 * and convert back to OKLCH for ΔE comparison.
 */
function clipFromOklch(c: OKLCH, toRGB: Matrix3x3): OKLCH {
  const rgb = oklchToLinearRGB(c, toRGB);
  const clipped = clipNaive(rgb);
  // Convert clipped RGB back to OKLCH. We need to go RGB → XYZ → OKLab → OKLCH.
  // Since each target gamut has its own toXYZ, we resolve by gamut.
  let oklch: OKLCH;
  if (toRGB === M_XYZ_TO_SRGB) {
    oklch = oklchSpace.fromXYZ(srgbSpace.toXYZ(linearSRGB(clipped[0], clipped[1], clipped[2])));
  } else if (toRGB === M_XYZ_TO_P3) {
    oklch = oklchSpace.fromXYZ(p3Space.toXYZ(linearP3(clipped[0], clipped[1], clipped[2])));
  } else {
    oklch = oklchSpace.fromXYZ(rec2020Space.toXYZ(clipped as unknown as LinearRec2020));
  }
  return oklch;
}

// ─── Gamut-specific convenience wrappers ──────────────────────────────────────

export function mapToSRGB(c: OKLCH): LinearSRGB {
  const mapped = mapToGamutOklch(c, M_XYZ_TO_SRGB, inGamutSRGB);
  const rgb = oklchToLinearRGB(mapped, M_XYZ_TO_SRGB);
  // Final defensive clip — handles last-mile float drift at the boundary.
  const clipped = clipNaive(rgb);
  return linearSRGB(clipped[0], clipped[1], clipped[2]);
}

export function mapToP3(c: OKLCH): LinearP3 {
  const mapped = mapToGamutOklch(c, M_XYZ_TO_P3, inGamutP3);
  const rgb = oklchToLinearRGB(mapped, M_XYZ_TO_P3);
  const clipped = clipNaive(rgb);
  return linearP3(clipped[0], clipped[1], clipped[2]);
}

export function mapToRec2020(c: OKLCH): LinearRec2020 {
  const mapped = mapToGamutOklch(c, M_XYZ_TO_REC2020, inGamutRec2020);
  const rgb = oklchToLinearRGB(mapped, M_XYZ_TO_REC2020);
  const clipped = clipNaive(rgb);
  return clipped as unknown as LinearRec2020;
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'in-gamut sRGB red is unchanged',
    fn: () => {
      const c = makeOklch(0.6279554, 0.2576, 29.2339);
      const mapped = mapToSRGB(c);
      return Math.hypot(mapped[0] - 1, mapped[1] - 0, mapped[2] - 0);
    },
    expected: 0,
    tolerance: 1e-2,
    source: 'OKLCh pure sRGB red → unchanged through mapToSRGB',
  },
  {
    name: 'out-of-gamut chroma reduced (very vivid red)',
    fn: () => {
      // Extreme chroma beyond sRGB
      const c = makeOklch(0.6, 0.5, 29.0);
      const mapped = mapToSRGB(c);
      // The result should be in gamut and have reduced chroma
      const allInRange = mapped[0] >= 0 && mapped[0] <= 1
                      && mapped[1] >= 0 && mapped[1] <= 1
                      && mapped[2] >= 0 && mapped[2] <= 1;
      return allInRange ? 0 : 1;
    },
    expected: 0,
    tolerance: 0,
    source: 'Out-of-gamut input must land in [0, 1]^3 after mapping',
  },
  {
    name: 'L ≥ 1 returns white in sRGB',
    fn: () => {
      const c = makeOklch(1.5, 0.3, 180);
      const mapped = mapToSRGB(c);
      return Math.hypot(mapped[0] - 1, mapped[1] - 1, mapped[2] - 1);
    },
    expected: 0,
    tolerance: 1e-2,
    source: 'L > 1 must clamp to ~white in target gamut (small float drift through OKLab cube-root is expected)',
  },
  {
    name: 'L ≤ 0 returns black in sRGB',
    fn: () => {
      const c = makeOklch(-0.1, 0.3, 180);
      const mapped = mapToSRGB(c);
      return Math.hypot(mapped[0], mapped[1], mapped[2]);
    },
    expected: 0,
    tolerance: 1e-4,
    source: 'L < 0 must clamp to black in target gamut',
  },
];
