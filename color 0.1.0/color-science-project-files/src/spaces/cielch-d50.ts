// CIELCH at D50 ↔ XYZ_D65 (polar form of CIELAB_D50).
//
// Same as `src/spaces/cielch.ts` but for the D50 variant of CIELAB.
// Used in ICC profile workflows.

import type { CIELCH_D50, CIELAB_D50, XYZ_D65, TestVector } from '../types.js';
import { wrapHueDeg } from '../types.js';
import * as cielabD50 from './cielab-d50.js';

const DEG_TO_RAD = Math.PI / 180;
const RAD_TO_DEG = 180 / Math.PI;

export function fromCIELAB(lab: CIELAB_D50): CIELCH_D50 {
  const [L, a, b] = lab;
  const C = Math.sqrt(a * a + b * b);
  let h = Math.atan2(b, a) * RAD_TO_DEG;
  if (h < 0) h += 360;
  return [L, C, h] as unknown as CIELCH_D50;
}

export function toCIELAB(lch: CIELCH_D50): CIELAB_D50 {
  const [L, C, hDeg] = lch;
  const h = wrapHueDeg(hDeg) * DEG_TO_RAD;
  return [L, C * Math.cos(h), C * Math.sin(h)] as unknown as CIELAB_D50;
}

export function fromXYZ(c: XYZ_D65): CIELCH_D50 {
  return fromCIELAB(cielabD50.fromXYZ(c));
}

export function toXYZ(c: CIELCH_D50): XYZ_D65 {
  return cielabD50.toXYZ(toCIELAB(c));
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, CIELCH_D50>> = [
  // Use a chromatic input — achromatic round-trip fails because hue is
  // mathematically indeterminate when C=0 (atan2 of float noise = arbitrary).
  {
    input: { 0: 0.4123907993, 1: 0.2126390059, 2: 0.0193308187, length: 3 } as unknown as XYZ_D65,
    // Pure sRGB red transformed through Bradford → D50 → CIELCH_D50.
    // Approximate value; tolerance loose to accommodate Bradford precision.
    output: [54.3, 106.8, 40.9] as unknown as CIELCH_D50,
    tolerance: 0.5,
    source: 'Pure sRGB red → D50 CIELCH (chromatic; hue well-defined; Bradford-adapted)',
  },
];
