// CIELCH at D65 — polar form of CIELAB.
//
// [L*, C*, h_degrees] where C* = sqrt(a*² + b*²) and h = atan2(b*, a*).
// Bidirectional with CIELAB via standard polar/cartesian conversion.
//
// Hub conversion goes through CIELAB → XYZ_D65.

import type { CIELCH_D65, CIELAB_D65, XYZ_D65, TestVector } from '../types.js';
import { cielch_D65, cielab_D65, xyz, wrapHueDeg, NONLINEAR_TOLERANCE } from '../types.js';
import * as cielabSpace from './cielab.js';

const DEG_TO_RAD = Math.PI / 180;
const RAD_TO_DEG = 180 / Math.PI;

/** CIELAB → CIELCH (polar form). */
export function fromCIELAB(lab: CIELAB_D65): CIELCH_D65 {
  const [L, a, b] = lab;
  const C = Math.sqrt(a * a + b * b);
  let h = Math.atan2(b, a) * RAD_TO_DEG;
  if (h < 0) h += 360;
  return cielch_D65(L, C, h);
}

/** CIELCH → CIELAB (cartesian form). */
export function toCIELAB(lch: CIELCH_D65): CIELAB_D65 {
  const [L, C, hDeg] = lch;
  const h = wrapHueDeg(hDeg) * DEG_TO_RAD;
  return cielab_D65(L, C * Math.cos(h), C * Math.sin(h));
}

export function fromXYZ(c: XYZ_D65): CIELCH_D65 {
  return fromCIELAB(cielabSpace.fromXYZ(c));
}

export function toXYZ(c: CIELCH_D65): XYZ_D65 {
  return cielabSpace.toXYZ(toCIELAB(c));
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, CIELCH_D65>> = [
  {
    input: xyz(0, 0, 0),
    output: cielch_D65(0, 0, 0),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'Black point — L=C=0, hue undefined (returned as 0)',
  },
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: cielch_D65(100, 0, 0),
    tolerance: 1e-6,
    source: 'D65 white → L*=100, C*=0',
  },
];
