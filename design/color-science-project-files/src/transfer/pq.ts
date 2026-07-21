// PQ (Perceptual Quantizer) — SMPTE ST 2084 / BT.2100
//
// Absolute HDR transfer function. Input/output normalized to [0, 1] where 1 = 10,000 nits.
//
// Primary source: SMPTE ST 2084:2014, ITU-R BT.2100-2 (2018)

import { NONLINEAR_TOLERANCE } from '../types.js';
import type { TestVector } from '../types.js';

const M1 = 2610 / 16384;          // 0.1593017578125
const M2 = (2523 / 4096) * 128;   // 78.84375
const C1 = 3424 / 4096;           // 0.8359375
const C2 = (2413 / 4096) * 32;    // 18.8515625
const C3 = (2392 / 4096) * 32;    // 18.6875

/** Linear absolute luminance [0, 1] (1 = 10,000 nits) → encoded [0, 1]. */
export function encodeComponent(linear: number): number {
  const Y = Math.max(0, linear);
  const Yp = Math.pow(Y, M1);
  return Math.pow((C1 + C2 * Yp) / (1 + C3 * Yp), M2);
}

/** Encoded [0, 1] → linear absolute luminance [0, 1] (1 = 10,000 nits). */
export function decodeComponent(encoded: number): number {
  const E = Math.max(0, encoded);
  const Ep = Math.pow(E, 1 / M2);
  const num = Math.max(0, Ep - C1);
  const den = Math.max(1e-12, C2 - C3 * Ep);
  return Math.pow(num / den, 1 / M1);
}

export function encode(linear: readonly [number, number, number]): [number, number, number] {
  return [encodeComponent(linear[0]), encodeComponent(linear[1]), encodeComponent(linear[2])];
}

export function decode(encoded: readonly [number, number, number]): [number, number, number] {
  return [decodeComponent(encoded[0]), decodeComponent(encoded[1]), decodeComponent(encoded[2])];
}

/** Convenience: encode taking luminance in nits (cd/m²). 10,000 nits = 1.0 linear. */
export const encodeNits = (nits: number) => encodeComponent(nits / 10000);

/** Convenience: decode returning luminance in nits. */
export const decodeNits = (encoded: number) => decodeComponent(encoded) * 10000;

export const testVectors: ReadonlyArray<TestVector<readonly [number, number, number], readonly [number, number, number]>> = [
  {
    input: [0, 0, 0],
    output: [0, 0, 0],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'SMPTE ST 2084 — black point',
  },
  {
    input: [1, 1, 1],
    output: [1, 1, 1],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'SMPTE ST 2084 — peak (10,000 nits)',
  },
];
