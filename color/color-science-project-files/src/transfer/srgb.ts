// sRGB transfer function — IEC 61966-2-1
//
// The sRGB transfer is piecewise: a small linear segment near zero, then a
// power curve. The piecewise definition prevents the infinite slope at zero
// that a pure power curve would have.
//
// This same transfer function is used by Display P3 (SMPTE EG 432-1).
//
// Primary source: IEC 61966-2-1:1999 Annex E
// W3C spec: https://www.w3.org/TR/css-color-4/#valdef-color-srgb

import type { LinearSRGB, EncodedSRGB, TestVector } from '../types.js';
import { linearSRGB, encodedSRGB, NONLINEAR_TOLERANCE } from '../types.js';

// ─── Scalar transfer ──────────────────────────────────────────────────────────

/** Linear → encoded (display) scalar component. Sign-preserving for out-of-range values. */
export function encodeComponent(linear: number): number {
  const abs = Math.abs(linear);
  const sign = Math.sign(linear);
  if (abs <= 0.0031308) return sign * 12.92 * abs;
  return sign * (1.055 * Math.pow(abs, 1 / 2.4) - 0.055);
}

/** Encoded → linear scalar component. Sign-preserving for negative values. */
export function decodeComponent(encoded: number): number {
  const abs = Math.abs(encoded);
  const sign = Math.sign(encoded);
  if (abs <= 0.04045) return sign * abs / 12.92;
  return sign * Math.pow((abs + 0.055) / 1.055, 2.4);
}

// ─── Tuple transfer ───────────────────────────────────────────────────────────

export function encode(linear: LinearSRGB): EncodedSRGB {
  return encodedSRGB(
    encodeComponent(linear[0]),
    encodeComponent(linear[1]),
    encodeComponent(linear[2])
  );
}

export function decode(encoded: EncodedSRGB): LinearSRGB {
  return linearSRGB(
    decodeComponent(encoded[0]),
    decodeComponent(encoded[1]),
    decodeComponent(encoded[2])
  );
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

export const testVectors: ReadonlyArray<TestVector<LinearSRGB, EncodedSRGB>> = [
  {
    input: linearSRGB(0, 0, 0),
    output: encodedSRGB(0, 0, 0),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'IEC 61966-2-1 — black point',
  },
  {
    input: linearSRGB(1, 1, 1),
    output: encodedSRGB(1, 1, 1),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'IEC 61966-2-1 — white point (1.055 * 1^(1/2.4) - 0.055 = 1)',
  },
  {
    input: linearSRGB(0.5, 0.5, 0.5),
    output: encodedSRGB(0.7353569830524495, 0.7353569830524495, 0.7353569830524495),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'Linear 0.5 → encoded ~0.735 (canonical 50% linear gray)',
  },
  {
    input: linearSRGB(0.0031308, 0.0031308, 0.0031308),
    output: encodedSRGB(0.04045, 0.04045, 0.04045),
    tolerance: NONLINEAR_TOLERANCE,
    source: 'IEC 61966-2-1 — piecewise boundary (12.92 × 0.0031308 = 0.04045)',
  },
];
