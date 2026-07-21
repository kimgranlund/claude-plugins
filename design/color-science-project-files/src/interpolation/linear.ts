// Linear interpolation between two colors.
//
// In any color space, but **the choice of space matters** — interpolating in
// linear sRGB gives different mid-points than interpolating in OKLab, which
// gives different mid-points than interpolating in CIELAB. The canonical CSS
// Color 4 default is to interpolate "in oklab".
//
// For cylindrical spaces (OKLCh, CIELCh, HSL, HSV), the hue component is an
// angle and naive component-wise interpolation gives the wrong answer when
// the two hues wrap around the 0°/360° boundary. CSS Color 4 specifies four
// hue paths (shorter / longer / increasing / decreasing) for this.
//
// Primary sources:
//   - W3C CSS Color 4 — https://www.w3.org/TR/css-color-4/#interpolation
//   - Hue interpolation — https://www.w3.org/TR/css-color-4/#hue-interpolation
//
// Companion math: references/techniques/gradient-interpolation-math.md

import type { OKLab, OKLCH, CIELAB_D65, CIELCH_D65 } from '../types.js';
import { wrapHueDeg } from '../types.js';
import type { SpaceModule } from '../convert.js';

// ─── Hue paths ────────────────────────────────────────────────────────────────

export type HuePath = 'shorter' | 'longer' | 'increasing' | 'decreasing';

/**
 * Interpolate between two hue angles along a chosen path.
 * Returns a hue in [0, 360).
 *
 * - **shorter**: take the shorter arc (CSS default).
 * - **longer**: take the longer arc.
 * - **increasing**: always rotate counterclockwise (h₂ ≥ h₁).
 * - **decreasing**: always rotate clockwise (h₂ ≤ h₁).
 */
export function lerpHue(
  h1: number,
  h2: number,
  t: number,
  path: HuePath = 'shorter'
): number {
  h1 = wrapHueDeg(h1);
  h2 = wrapHueDeg(h2);
  const diff = h2 - h1;

  let effDiff: number;
  switch (path) {
    case 'shorter':
      if (Math.abs(diff) <= 180) effDiff = diff;
      else if (diff > 180) effDiff = diff - 360;
      else effDiff = diff + 360;
      break;
    case 'longer':
      if (Math.abs(diff) >= 180) effDiff = diff;
      else if (diff > 0) effDiff = diff - 360;
      else effDiff = diff + 360;
      break;
    case 'increasing':
      effDiff = diff < 0 ? diff + 360 : diff;
      break;
    case 'decreasing':
      effDiff = diff > 0 ? diff - 360 : diff;
      break;
  }
  return wrapHueDeg(h1 + t * effDiff);
}

// ─── Cartesian linear interpolation ───────────────────────────────────────────

/** Component-wise linear interpolation of two 3-tuples. */
export function lerpTuple(
  a: readonly [number, number, number],
  b: readonly [number, number, number],
  t: number
): [number, number, number] {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    a[2] + (b[2] - a[2]) * t,
  ];
}

// ─── OKLab interpolation ──────────────────────────────────────────────────────

/** Linear interpolation in OKLab. The CSS Color 4 default. */
export function lerpOklab(a: OKLab, b: OKLab, t: number): OKLab {
  return lerpTuple(a, b, t) as unknown as OKLab;
}

/** Linear interpolation in CIELAB. */
export function lerpCielab(a: CIELAB_D65, b: CIELAB_D65, t: number): CIELAB_D65 {
  return lerpTuple(a, b, t) as unknown as CIELAB_D65;
}

// ─── Polar (cylindrical) interpolation ────────────────────────────────────────

/** Linear interpolation in OKLCh with selectable hue path. */
export function lerpOklch(a: OKLCH, b: OKLCH, t: number, huePath: HuePath = 'shorter'): OKLCH {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    lerpHue(a[2], b[2], t, huePath),
  ] as unknown as OKLCH;
}

/** Linear interpolation in CIELCh with selectable hue path. */
export function lerpCielch(a: CIELCH_D65, b: CIELCH_D65, t: number, huePath: HuePath = 'shorter'): CIELCH_D65 {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    lerpHue(a[2], b[2], t, huePath),
  ] as unknown as CIELCH_D65;
}

// ─── Generic mix-via-space ────────────────────────────────────────────────────

/**
 * Mix two colors in the source space by interpolating "in" a target space.
 * E.g., mix two sRGB values "in oklab" → convert both to OKLab, lerp there,
 * convert back to sRGB.
 *
 * This matches the CSS Color 4 `color-mix(in oklab, color1, color2 t%)` semantics.
 */
export function mixVia<Source, Via extends readonly [number, number, number]>(
  a: Source,
  b: Source,
  t: number,
  sourceSpace: SpaceModule<Source>,
  viaSpace: SpaceModule<Via>
): Source {
  const aVia = viaSpace.fromXYZ(sourceSpace.toXYZ(a));
  const bVia = viaSpace.fromXYZ(sourceSpace.toXYZ(b));
  const mixed = lerpTuple(aVia, bVia, t) as unknown as Via;
  return sourceSpace.fromXYZ(viaSpace.toXYZ(mixed));
}

// ─── Generate intermediate stops ──────────────────────────────────────────────

/**
 * Generate `n` equally-spaced interpolated values (inclusive at both ends).
 * For n=5: returns t = 0, 0.25, 0.5, 0.75, 1.0.
 */
export function stops(n: number): readonly number[] {
  if (n <= 1) return [0];
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    out.push(i / (n - 1));
  }
  return out;
}

/** Generate `n` colors equally spaced between `a` and `b` in OKLab. */
export function rampOklab(a: OKLab, b: OKLab, n: number): readonly OKLab[] {
  return stops(n).map(t => lerpOklab(a, b, t));
}

/** Generate `n` colors equally spaced between `a` and `b` in OKLCh. */
export function rampOklch(a: OKLCH, b: OKLCH, n: number, huePath: HuePath = 'shorter'): readonly OKLCH[] {
  return stops(n).map(t => lerpOklch(a, b, t, huePath));
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'lerpHue shorter 350° → 10° at t=0.5 yields 0° (wraps)',
    fn: () => lerpHue(350, 10, 0.5, 'shorter'),
    expected: 0,
    tolerance: 1e-9,
    source: 'CSS Color 4 — shorter arc across 0° boundary is 20° total',
  },
  {
    name: 'lerpHue longer 350° → 10° at t=0.5 yields 180°',
    fn: () => lerpHue(350, 10, 0.5, 'longer'),
    expected: 180,
    tolerance: 1e-9,
    source: 'CSS Color 4 — longer arc across 0° boundary is 340° total → midpoint 180°',
  },
  {
    name: 'lerpHue increasing 350° → 10° at t=0.5 yields 0°',
    fn: () => lerpHue(350, 10, 0.5, 'increasing'),
    expected: 0,
    tolerance: 1e-9,
    source: 'CSS Color 4 — increasing 350° → 370° → 10°',
  },
  {
    name: 'lerpHue decreasing 10° → 350° at t=0.5 yields 0°',
    fn: () => lerpHue(10, 350, 0.5, 'decreasing'),
    expected: 0,
    tolerance: 1e-9,
    source: 'CSS Color 4 — decreasing 10° → -10° → 350° via 0°',
  },
  {
    name: 'lerpHue same hue returns same hue',
    fn: () => lerpHue(120, 120, 0.5, 'shorter'),
    expected: 120,
    tolerance: 1e-9,
    source: 'Identity case',
  },
  {
    name: 'lerpTuple at t=0 returns a',
    fn: () => lerpTuple([1, 2, 3], [4, 5, 6], 0)[1],
    expected: 2,
    tolerance: 1e-12,
    source: 'Endpoint at t=0',
  },
  {
    name: 'lerpTuple at t=1 returns b',
    fn: () => lerpTuple([1, 2, 3], [4, 5, 6], 1)[1],
    expected: 5,
    tolerance: 1e-12,
    source: 'Endpoint at t=1',
  },
  {
    name: 'lerpTuple midpoint averages',
    fn: () => lerpTuple([0, 0, 0], [10, 20, 30], 0.5)[2],
    expected: 15,
    tolerance: 1e-12,
    source: 'Midpoint of 0 and 30 is 15',
  },
  {
    name: 'stops(5) is uniformly spaced',
    fn: () => stops(5)[2],
    expected: 0.5,
    tolerance: 1e-12,
    source: 'stops(5) = [0, 0.25, 0.5, 0.75, 1.0]',
  },
];
