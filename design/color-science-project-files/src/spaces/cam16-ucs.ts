// CAM16-UCS ↔ XYZ_D65 — the Uniform Colour Space companion to CIECAM16.
//
// CAM16 outputs J (lightness), M (colorfulness), h (hue) — perceptually meaningful
// but NOT a Euclidean space. CAM16-UCS transforms (J, M, h) into Cartesian (J', a', b')
// where Euclidean distance approximates perceptual difference (ΔE_CAM16).
//
// Use CAM16-UCS for:
//   - Color difference metrics under specified viewing conditions
//   - Palette generation where uniformity in CAM16's perceptual space matters
//   - Cross-illuminant comparisons (CAM16-UCS accounts for viewing conditions)
//
// Algorithm:
//   J' = (1 + 100·c1) · J / (1 + c1 · J)
//   M' = (1/c2) · ln(1 + c2 · M)
//   a' = M' · cos(h)
//   b' = M' · sin(h)
//
//   Inverse:
//   J = J' / (1 + c1 · (100 - J'))
//   M = (exp(c2 · M') - 1) / c2
//   h = atan2(b', a')
//
// Constants per Li et al. (2017):
//   c1 = 0.007, c2 = 0.0228
//
// Primary source: Li, Li, Wang, Cui, Luo, Melgosa, Brill, Pointer (2017),
//   "Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,"
//   Color Research & Application, 42(6), 703–718.

import type { CAM16_UCS, CIECAM16_JMh, XYZ_D65 } from '../types.js';
import { wrapHueDeg } from '../types.js';
import * as cam16 from './ciecam16.js';

const C1 = 0.007;
const C2 = 0.0228;
const DEG_TO_RAD = Math.PI / 180;
const RAD_TO_DEG = 180 / Math.PI;

// ─── CIECAM16 (JMh) ↔ CAM16-UCS (J'a'b') ──────────────────────────────────────

/** Convert CIECAM16 (J, M, h_deg) to CAM16-UCS (J', a', b'). */
export function fromJMh(jmh: CIECAM16_JMh): CAM16_UCS {
  const [J, M, hDeg] = jmh;
  const Jp = ((1 + 100 * C1) * J) / (1 + C1 * J);
  const Mp = (1 / C2) * Math.log(1 + C2 * M);
  const hRad = wrapHueDeg(hDeg) * DEG_TO_RAD;
  return [Jp, Mp * Math.cos(hRad), Mp * Math.sin(hRad)] as unknown as CAM16_UCS;
}

/** Convert CAM16-UCS (J', a', b') back to CIECAM16 (J, M, h_deg). */
export function toJMh(ucs: CAM16_UCS): CIECAM16_JMh {
  const [Jp, ap, bp] = ucs;
  const J = Jp / (1 + C1 * (100 - Jp));
  const Mp = Math.sqrt(ap * ap + bp * bp);
  const M = (Math.exp(C2 * Mp) - 1) / C2;
  let hDeg = Math.atan2(bp, ap) * RAD_TO_DEG;
  if (hDeg < 0) hDeg += 360;
  return [J, M, hDeg] as unknown as CIECAM16_JMh;
}

// ─── Hub conversion through XYZ_D65 ───────────────────────────────────────────

export function fromXYZ(c: XYZ_D65): CAM16_UCS {
  return fromJMh(cam16.fromXYZ(c));
}

export function toXYZ(c: CAM16_UCS): XYZ_D65 {
  return cam16.toXYZ(toJMh(c));
}

// ─── ΔE_CAM16 (Euclidean in CAM16-UCS) ────────────────────────────────────────

/**
 * ΔE in CAM16-UCS. Euclidean distance between two CAM16-UCS points.
 * Perceptually calibrated under the same viewing conditions as the input CAM16
 * computation.
 */
export function deltaECAM16(a: CAM16_UCS, b: CAM16_UCS): number {
  const dJ = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return Math.sqrt(dJ * dJ + dA * dA + dB * dB);
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

import type { TestVector } from '../types.js';
import { xyz } from '../types.js';

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, CAM16_UCS>> = [
  {
    input: xyz(0, 0, 0),
    output: [0, 0, 0] as unknown as CAM16_UCS,
    tolerance: 1e-3,
    source: 'Black point under default viewing conditions',
  },
];
