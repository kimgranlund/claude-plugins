// HLG (Hybrid Log-Gamma) — BT.2100 / ARIB STD-B67
//
// Relative HDR transfer. Compatible with SDR displays via its log-gamma upper
// segment that mimics conventional gamma curves.
//
// Primary source: ITU-R BT.2100-2 (2018), ARIB STD-B67 (2015)

import { NONLINEAR_TOLERANCE } from '../types.js';
import type { TestVector } from '../types.js';

const A = 0.17883277;
const B = 0.28466892;          // 1 - 4a
const C = 0.55991073;          // 0.5 - a*ln(4a)

/** Scene linear [0, 1] → display-encoded [0, 1]. */
export function encodeComponent(linear: number): number {
  const L = Math.max(0, linear);
  if (L <= 1 / 12) return Math.sqrt(3 * L);
  return A * Math.log(12 * L - B) + C;
}

/** Display-encoded [0, 1] → scene linear [0, 1]. */
export function decodeComponent(encoded: number): number {
  const V = Math.max(0, encoded);
  if (V <= 0.5) return (V * V) / 3;
  return (Math.exp((V - C) / A) + B) / 12;
}

export function encode(linear: readonly [number, number, number]): [number, number, number] {
  return [encodeComponent(linear[0]), encodeComponent(linear[1]), encodeComponent(linear[2])];
}

export function decode(encoded: readonly [number, number, number]): [number, number, number] {
  return [decodeComponent(encoded[0]), decodeComponent(encoded[1]), decodeComponent(encoded[2])];
}

export const testVectors: ReadonlyArray<TestVector<readonly [number, number, number], readonly [number, number, number]>> = [
  {
    input: [0, 0, 0],
    output: [0, 0, 0],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'BT.2100 HLG — black point',
  },
  {
    input: [1 / 12, 1 / 12, 1 / 12],
    output: [0.5, 0.5, 0.5],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'BT.2100 HLG — piecewise boundary at 1/12 linear → 0.5 encoded',
  },
  {
    input: [1, 1, 1],
    output: [1, 1, 1],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'BT.2100 HLG — reference white',
  },
];
