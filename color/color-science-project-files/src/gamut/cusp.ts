// Ottosson cusp algorithm — closed-form max-chroma point of an RGB gamut at a
// fixed OKLab hue.
//
// The "cusp" is the (L, C) point of maximum chroma achievable in the target
// gamut for a given hue direction. It's the apex of the gamut's slice
// perpendicular to the hue ray in OKLab space.
//
// Why it matters:
//   - Building lightness ramps: max-chroma decreases as L moves away from the cusp.
//   - Gamut mapping: the cusp is the natural pivot for chroma reduction.
//   - Color pickers: OKHSL/OKHSV reparameterize around the cusp.
//
// Algorithm (Ottosson 2021):
//   1. Compute max saturation S_max = C/L along the hue ray. Uses a piecewise
//      polynomial approximation (branch by which RGB face is hit first), refined
//      by one Halley's-method step.
//   2. Find L_cusp by computing OKLab → linear sRGB at (1, S_max * a, S_max * b)
//      and identifying the smallest scaling that keeps the max channel at 1.
//   3. C_cusp = L_cusp * S_max.
//
// Primary source: Björn Ottosson, "Gamut clipping" (2021)
//   https://bottosson.github.io/posts/gamutclipping/
//
// Current scope: sRGB only. Other gamuts use the same structure with different
// face-selection coefficients; deferred until needed.

import type { OKLab, OKLCH, OKHSL } from '../types.js';
import { oklab, wrapHueDeg } from '../types.js';
import * as oklabSpace from '../spaces/oklab.js';
import * as srgbSpace from '../spaces/srgb.js';

const DEG_TO_RAD = Math.PI / 180;

// ─── Step 1: max saturation along a unit-norm (a, b) direction in OKLab ──────

/**
 * Maximum saturation $S = C/L$ achievable in sRGB along the hue direction `(a, b)`.
 * Requires `a*a + b*b = 1` (i.e., `(a, b)` is a unit vector).
 */
export function maxSaturationSRGB(a: number, b: number): number {
  // Piecewise polynomial coefficients — selected by which sRGB face is hit first
  // as saturation increases along the hue ray.
  let k0: number, k1: number, k2: number, k3: number, k4: number;
  let wl: number, wm: number, ws: number;

  if (-1.88170328 * a - 0.80936493 * b > 1) {
    // Red face
    k0 = 1.19086277; k1 = 1.76576728; k2 = 0.59662641; k3 = 0.75515197; k4 = 0.56771245;
    wl = 4.0767416621; wm = -3.3077115913; ws = 0.2309699292;
  } else if (1.81444104 * a - 1.19445276 * b > 1) {
    // Green face
    k0 = 0.73956515; k1 = -0.45954404; k2 = 0.08285427; k3 = 0.12541070; k4 = 0.14503204;
    wl = -1.2684380046; wm = 2.6097574011; ws = -0.3413193965;
  } else {
    // Blue face
    k0 = 1.35733652; k1 = -0.00915799; k2 = -1.15130210; k3 = -0.50559606; k4 = 0.00692167;
    wl = -0.0041960863; wm = -0.7034186147; ws = 1.7076147010;
  }

  // Polynomial approximation
  let S = k0 + k1 * a + k2 * b + k3 * a * a + k4 * a * b;

  // One step of Halley's method for refinement.
  // These are derivatives along the OKLab → linear-RGB → "channel = 0" surface.
  const k_l =  0.3963377774 * a +  0.2158037573 * b;
  const k_m = -0.1055613458 * a + -0.0638541728 * b;
  const k_s = -0.0894841775 * a + -1.2914855480 * b;

  const l_ = 1 + S * k_l;
  const m_ = 1 + S * k_m;
  const s_ = 1 + S * k_s;

  const l = l_ * l_ * l_;
  const m = m_ * m_ * m_;
  const s = s_ * s_ * s_;

  const l_dS = 3 * k_l * l_ * l_;
  const m_dS = 3 * k_m * m_ * m_;
  const s_dS = 3 * k_s * s_ * s_;

  const l_dS2 = 6 * k_l * k_l * l_;
  const m_dS2 = 6 * k_m * k_m * m_;
  const s_dS2 = 6 * k_s * k_s * s_;

  const f   = wl * l     + wm * m     + ws * s;
  const f1  = wl * l_dS  + wm * m_dS  + ws * s_dS;
  const f2  = wl * l_dS2 + wm * m_dS2 + ws * s_dS2;

  S = S - (f * f1) / (f1 * f1 - 0.5 * f * f2);
  return S;
}

// ─── Step 2: cusp (L_cusp, C_cusp) at a given hue ─────────────────────────────

/**
 * Cusp $(L_{cusp}, C_{cusp})$ in sRGB at the OKLab hue $(a, b)$ where
 * $a^2 + b^2 = 1$. The cusp is the maximum-chroma point achievable in the gamut.
 */
export function findCuspSRGB(a: number, b: number): readonly [number, number] {
  const S = maxSaturationSRGB(a, b);
  // The OKLab point (L=1, S*a, S*b) is on the saturation ray. Convert to
  // linear sRGB and find the channel that hits 1 first to determine L_cusp.
  const lab = oklab(1, S * a, S * b);
  const xyzVal = oklabSpace.toXYZ(lab);
  const rgb = srgbSpace.fromXYZ(xyzVal);
  const maxRGB = Math.max(rgb[0], rgb[1], rgb[2]);
  if (maxRGB <= 0) return [0, 0];
  const L_cusp = Math.cbrt(1 / maxRGB);
  const C_cusp = L_cusp * S;
  return [L_cusp, C_cusp];
}

/**
 * Cusp at a hue given in degrees (CSS convention). Convenience over
 * `findCuspSRGB(a, b)` for callers working in OKLCh.
 */
export function findCuspSRGBFromHueDeg(hDeg: number): readonly [number, number] {
  const h = wrapHueDeg(hDeg) * DEG_TO_RAD;
  return findCuspSRGB(Math.cos(h), Math.sin(h));
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'cusp sRGB at hue 0 (pure red direction) has L_cusp ≈ 0.628',
    fn: () => findCuspSRGBFromHueDeg(29.2339)[0], // OKLCh hue of pure sRGB red
    expected: 0.6279,
    tolerance: 1e-3,
    source: 'OKLab pure sRGB red has L = 0.6279554 — cusp at the matching hue should equal this',
  },
  {
    name: 'cusp sRGB at hue 29.23 (pure red) has C_cusp ≈ 0.2576',
    fn: () => findCuspSRGBFromHueDeg(29.2339)[1],
    expected: 0.2576,
    tolerance: 5e-3,
    source: 'OKLab pure sRGB red has C = 0.2576',
  },
  {
    name: 'cusp sRGB at hue 264 (blue direction) has L_cusp ≈ 0.496',
    fn: () => findCuspSRGBFromHueDeg(264.05)[0],
    expected: 0.496,
    tolerance: 5e-3,
    source: 'The cusp at blue hue is slightly higher L than pure-RGB blue (~0.45). Cusp is the max-chroma point, not the RGB primary point.',
  },
];
