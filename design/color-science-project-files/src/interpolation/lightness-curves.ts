// Lightness ramp curves — primitives for generating lightness progressions
// used in design-token systems (Tailwind v4, Radix Themes 3, Material 3).
//
// The choice of curve dramatically changes the perceived "feel" of a palette:
//   - **Linear** progression in OKLab L feels perceptually even — best default.
//   - **Exponential** (gamma curves) emphasize either dark or light end.
//   - **Tailwind v4** uses irregular OKLab stops (50, 100, 200, ..., 950).
//   - **Radix** uses 12 semantic stops (1-12) with non-uniform spacing.
//
// Companion math: references/techniques/lightness-ramp-curves.md

// ─── Generic ramp curves ──────────────────────────────────────────────────────

/** Linear ramp: t in [0, 1] → L in [lMin, lMax]. */
export function linearRamp(t: number, lMin: number = 0, lMax: number = 1): number {
  return lMin + t * (lMax - lMin);
}

/**
 * Gamma ramp: t^gamma scaled to [lMin, lMax].
 * - gamma > 1: slow start (emphasizes light end)
 * - gamma < 1: fast start (emphasizes dark end)
 * - gamma = 1: linear
 */
export function gammaRamp(t: number, gamma: number, lMin: number = 0, lMax: number = 1): number {
  return lMin + Math.pow(t, gamma) * (lMax - lMin);
}

/**
 * Perceptual ramp: linearly interpolated in OKLab L (which is already
 * perceptually uniform). Identical to `linearRamp` since the OKLab L axis is
 * itself the perceptual lightness — but provided for naming clarity.
 */
export function perceptualRamp(t: number, lMin: number = 0, lMax: number = 1): number {
  return lMin + t * (lMax - lMin);
}

/**
 * S-curve (smoothstep) ramp: emphasizes the middle, soft endpoints.
 * Useful when the palette should have more visual differentiation in the
 * mid-tones than at the extremes.
 */
export function smoothstepRamp(t: number, lMin: number = 0, lMax: number = 1): number {
  const s = t * t * (3 - 2 * t);
  return lMin + s * (lMax - lMin);
}

// ─── Tailwind v4 OKLab stops ──────────────────────────────────────────────────

/**
 * Tailwind v4's L stops (OKLab L space). The actual values published by
 * Tailwind for the default palette across 11 stops:
 *   50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
 *
 * Note: these are L values in OKLab, NOT linear t values. They're non-uniform
 * to feel right perceptually (the eye is more sensitive to lightness changes
 * in the mid-tones).
 *
 * Source: Tailwind v4.0 default palette generation
 */
export const TAILWIND_V4_L_STOPS: readonly number[] = [
  0.985, // 50
  0.967, // 100
  0.922, // 200
  0.870, // 300
  0.708, // 400
  0.554, // 500
  0.446, // 600
  0.371, // 700
  0.269, // 800
  0.205, // 900
  0.130, // 950
];

/**
 * Get Tailwind v4 L at a step number.
 * @param step One of 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
 */
export function tailwindV4LAtStep(step: number): number {
  const stepMap: Record<number, number> = {
    50: 0, 100: 1, 200: 2, 300: 3, 400: 4, 500: 5,
    600: 6, 700: 7, 800: 8, 900: 9, 950: 10,
  };
  const idx = stepMap[step];
  if (idx === undefined) {
    throw new Error(`Tailwind v4 step must be one of 50, 100, 200, ..., 950 (got ${step})`);
  }
  return TAILWIND_V4_L_STOPS[idx];
}

// ─── Radix Themes 3 stops ─────────────────────────────────────────────────────

/**
 * Radix Themes 3 12-step L curve (light mode).
 * The 12 stops map to UI roles:
 *   1: App background     7: UI hover
 *   2: Subtle background  8: Borders
 *   3: UI                 9: Solid (brand)
 *   4: Hover              10: Solid hover
 *   5: Active             11: Low-contrast text
 *   6: Subtle border      12: High-contrast text
 *
 * Source: Radix Themes 3 documentation.
 */
export const RADIX_THEMES_3_L_STOPS_LIGHT: readonly number[] = [
  0.995, 0.988, 0.965, 0.930, 0.879, 0.821,
  0.756, 0.673, 0.564, 0.481, 0.396, 0.180,
];

/** Get Radix Themes 3 light-mode L at step 1-12. */
export function radixLightLAtStep(step: number): number {
  if (step < 1 || step > 12 || !Number.isInteger(step)) {
    throw new Error(`Radix step must be integer 1-12 (got ${step})`);
  }
  return RADIX_THEMES_3_L_STOPS_LIGHT[step - 1];
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'linearRamp(0.5) = 0.5 default',
    fn: () => linearRamp(0.5),
    expected: 0.5,
    tolerance: 1e-12,
    source: 'Trivial midpoint',
  },
  {
    name: 'linearRamp(0.5, 0.2, 0.8) = 0.5',
    fn: () => linearRamp(0.5, 0.2, 0.8),
    expected: 0.5,
    tolerance: 1e-12,
    source: 'Midpoint of [0.2, 0.8] is 0.5',
  },
  {
    name: 'gammaRamp(0.5, 2) = 0.25 (slow start)',
    fn: () => gammaRamp(0.5, 2),
    expected: 0.25,
    tolerance: 1e-12,
    source: '0.5^2 = 0.25',
  },
  {
    name: 'gammaRamp(0.5, 0.5) = sqrt(0.5)',
    fn: () => gammaRamp(0.5, 0.5),
    expected: Math.sqrt(0.5),
    tolerance: 1e-12,
    source: '0.5^0.5 = sqrt(0.5) ≈ 0.707',
  },
  {
    name: 'smoothstepRamp(0.5) = 0.5',
    fn: () => smoothstepRamp(0.5),
    expected: 0.5,
    tolerance: 1e-12,
    source: '0.5²(3 - 2·0.5) = 0.25 · 2 = 0.5; smoothstep is symmetric at midpoint',
  },
  {
    name: 'smoothstepRamp(0) = 0',
    fn: () => smoothstepRamp(0),
    expected: 0,
    tolerance: 1e-12,
    source: 'Endpoint anchor',
  },
  {
    name: 'tailwindV4LAtStep(500) = 0.554',
    fn: () => tailwindV4LAtStep(500),
    expected: 0.554,
    tolerance: 1e-9,
    source: 'Tailwind v4 step 500 (mid)',
  },
  {
    name: 'tailwindV4LAtStep(950) is darkest',
    fn: () => tailwindV4LAtStep(950),
    expected: 0.130,
    tolerance: 1e-9,
    source: 'Tailwind v4 step 950',
  },
  {
    name: 'radixLightLAtStep(1) is lightest',
    fn: () => radixLightLAtStep(1),
    expected: 0.995,
    tolerance: 1e-9,
    source: 'Radix step 1 (app background, near-white)',
  },
  {
    name: 'radixLightLAtStep(12) is darkest',
    fn: () => radixLightLAtStep(12),
    expected: 0.180,
    tolerance: 1e-9,
    source: 'Radix step 12 (high-contrast text, dark)',
  },
];
