// OKHSV ↔ XYZ_D65 (Ottosson's perceptual HSV with cusp shaping).
//
// Companion to OKHSL (`src/spaces/okhsl.ts`). Where OKHSL uses Lightness
// (mid-tone L axis), OKHSV uses Value (the max-channel direction in OKLab).
//
// Storage: [hue_degrees, saturation_0_1, value_0_1]
//
// Primary source: Björn Ottosson, "Two new color spaces for color picking"
// (2021): https://bottosson.github.io/posts/colorpicker/
//
// This is a pragmatic implementation following the same cusp-finding pattern
// as `okhsl.ts`. Tolerance is loose at the extremes; cross-check against
// Ottosson's reference JS for strict-precision needs.

import type { OKHSV, OKLab, XYZ_D65 } from '../types.js';
import { oklab, okhsv, wrapHueDeg } from '../types.js';
import * as oklabSpace from './oklab.js';
import { findCuspSRGB } from '../gamut/cusp.js';

const DEG_TO_RAD = Math.PI / 180;
const RAD_TO_DEG = 180 / Math.PI;

// ─── OKHSV → OKLab ────────────────────────────────────────────────────────────

export function toOKLab(hsv: OKHSV): OKLab {
  const [hDeg, s, v] = hsv;
  if (v <= 0 || s <= 0) {
    // Achromatic; just use v as approximate L.
    return oklab(v, 0, 0);
  }
  const h = wrapHueDeg(hDeg) * DEG_TO_RAD;
  const a_ = Math.cos(h);
  const b_ = Math.sin(h);
  const [L_cusp, C_cusp] = findCuspSRGB(a_, b_);

  // For OKHSV: V corresponds to the max-channel direction in OKLab.
  // L = v * L_cusp_normalized; C = s * v * C_cusp (approximate)
  const L = v;
  const C = s * v * (C_cusp / Math.max(L_cusp, 1e-9));

  return oklab(L, C * a_, C * b_);
}

// ─── OKLab → OKHSV ────────────────────────────────────────────────────────────

export function fromOKLab(lab: OKLab): OKHSV {
  const [L, a, b] = lab;
  const C = Math.sqrt(a * a + b * b);
  if (L <= 0) return okhsv(0, 0, 0);
  if (C <= 0) return okhsv(0, 0, L);

  const a_ = a / C;
  const b_ = b / C;
  const [L_cusp, C_cusp] = findCuspSRGB(a_, b_);

  const v = L;
  const C_at_v = v * (C_cusp / Math.max(L_cusp, 1e-9));
  const s = Math.max(0, Math.min(1, C / Math.max(C_at_v, 1e-9)));

  let hDeg = Math.atan2(b, a) * RAD_TO_DEG;
  if (hDeg < 0) hDeg += 360;

  return okhsv(hDeg, s, v);
}

// ─── Hub conversion ───────────────────────────────────────────────────────────

export function toXYZ(c: OKHSV): XYZ_D65 {
  return oklabSpace.toXYZ(toOKLab(c));
}

export function fromXYZ(c: XYZ_D65): OKHSV {
  return fromOKLab(oklabSpace.fromXYZ(c));
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

import type { TestVector } from '../types.js';
import { xyz } from '../types.js';

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, OKHSV>> = [
  {
    input: xyz(0, 0, 0),
    output: okhsv(0, 0, 0),
    tolerance: 1e-2,
    source: 'Black → OKHSV (0, 0, 0)',
  },
];
