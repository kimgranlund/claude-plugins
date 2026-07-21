// SPD ↔ XYZ via CMF integration.
//
// The physical bridge between spectral and tristimulus color. Given a
// Spectral Power Distribution (SPD) of an illuminant and a surface
// reflectance spectrum (also an SPD shape), integrate against the CIE 1931
// 2° color matching functions to obtain XYZ.
//
// The inverse (XYZ → SPD) is the *spectral upsampling* problem and is
// fundamentally non-unique (many spectra produce the same XYZ — metamers).
// This module handles only the forward direction.
//
// Primary source: CIE 015:2018, formulas in Section 7.

import type { SPD, XYZ_D65 } from '../types.js';
import { xyz } from '../types.js';
import { CMF_1931 } from './cmf.js';
import { D65 } from './illuminants.js';

// ─── Tristimulus from SPD via CMF integration ─────────────────────────────────

/**
 * Compute XYZ from an emissive SPD (light source).
 * $X = k \int E(\lambda) \bar{x}(\lambda) d\lambda$ (and similarly for Y, Z),
 * where $k$ normalizes so $Y = 100$ for the reference white.
 *
 * 10nm rectangle-rule integration over 380-730nm. Returns XYZ normalized so
 * D65 white = Y=1 (matches the rest of this skill's XYZ_D65 convention).
 */
export function emissiveToXYZ(spd: SPD): XYZ_D65 {
  let X = 0, Y = 0, Z = 0;
  for (let i = 0; i < 36; i++) {
    X += spd[i] * CMF_1931[i][0];
    Y += spd[i] * CMF_1931[i][1];
    Z += spd[i] * CMF_1931[i][2];
  }
  // 10nm step; the constant cancels when we normalize.
  // Normalize so D65 → Y = 1.
  return xyz(X / D65_Y, Y / D65_Y, Z / D65_Y);
}

/**
 * Compute XYZ from a reflectance spectrum under an illuminant.
 *
 * $X = k \int R(\lambda) E(\lambda) \bar{x}(\lambda) d\lambda$
 *
 * Normalized so a perfect diffuse reflector (R=1 everywhere) under the same
 * illuminant gives Y = 1.
 */
export function reflectiveToXYZ(
  reflectance: readonly number[],
  illuminant: SPD = D65
): XYZ_D65 {
  let X = 0, Y = 0, Z = 0;
  let Yn = 0;
  for (let i = 0; i < 36; i++) {
    const E = illuminant[i];
    X += reflectance[i] * E * CMF_1931[i][0];
    Y += reflectance[i] * E * CMF_1931[i][1];
    Z += reflectance[i] * E * CMF_1931[i][2];
    Yn += E * CMF_1931[i][1];
  }
  return xyz(X / Yn, Y / Yn, Z / Yn);
}

// ─── Pre-computed: D65's Y for normalization ──────────────────────────────────

const D65_Y = (() => {
  let Y = 0;
  for (let i = 0; i < 36; i++) Y += D65[i] * CMF_1931[i][1];
  return Y;
})();

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'D65 SPD → XYZ has Y ≈ 1',
    fn: () => Math.abs(emissiveToXYZ(D65)[1] - 1),
    expected: 0,
    tolerance: 1e-12,
    source: 'D65 white normalizes to Y = 1 by construction',
  },
  {
    name: 'D65 SPD → XYZ x chromaticity ≈ 0.3127',
    fn: () => {
      const [X, Y, Z] = emissiveToXYZ(D65);
      const x = X / (X + Y + Z);
      return Math.abs(x - 0.3127);
    },
    expected: 0,
    tolerance: 1e-3,
    source: 'D65 chromaticity is x ≈ 0.3127, y ≈ 0.3290',
  },
  {
    name: 'D65 SPD → XYZ y chromaticity ≈ 0.3290',
    fn: () => {
      const [X, Y, Z] = emissiveToXYZ(D65);
      const y = Y / (X + Y + Z);
      return Math.abs(y - 0.3290);
    },
    expected: 0,
    tolerance: 1e-3,
    source: 'D65 chromaticity is x ≈ 0.3127, y ≈ 0.3290',
  },
  {
    name: 'Perfect diffuse reflector under D65 → Y = 1',
    fn: () => {
      const flat = new Array(36).fill(1);
      return Math.abs(reflectiveToXYZ(flat, D65)[1] - 1);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Perfect diffuse reflector (R=1 everywhere) under any illuminant gives Y = 1',
  },
];
