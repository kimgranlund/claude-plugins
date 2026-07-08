// Rec.2020 (BT.2020) OETF — also used by Rec.709 (BT.709) with the same formula.
//
// Piecewise: linear segment near zero, power 0.45 curve above.
//
// Primary source: ITU-R BT.2020-2 (2015), ITU-R BT.709-6 (2015)
// W3C: https://www.w3.org/TR/css-color-4/#valdef-color-rec2020

import type { LinearRec2020, EncodedRec2020, TestVector } from '../types.js';
import { NONLINEAR_TOLERANCE } from '../types.js';

const ALPHA = 1.09929682680944;
const BETA = 0.018053968510807;

export function encodeComponent(linear: number): number {
  const abs = Math.abs(linear);
  const sign = Math.sign(linear);
  if (abs < BETA) return sign * 4.5 * abs;
  return sign * (ALPHA * Math.pow(abs, 0.45) - (ALPHA - 1));
}

export function decodeComponent(encoded: number): number {
  const abs = Math.abs(encoded);
  const sign = Math.sign(encoded);
  if (abs < BETA * 4.5) return sign * abs / 4.5;
  return sign * Math.pow((abs + (ALPHA - 1)) / ALPHA, 1 / 0.45);
}

export function encode(linear: LinearRec2020): EncodedRec2020 {
  return [
    encodeComponent(linear[0]),
    encodeComponent(linear[1]),
    encodeComponent(linear[2]),
  ] as unknown as EncodedRec2020;
}

export function decode(encoded: EncodedRec2020): LinearRec2020 {
  return [
    decodeComponent(encoded[0]),
    decodeComponent(encoded[1]),
    decodeComponent(encoded[2]),
  ] as unknown as LinearRec2020;
}

export const testVectors: ReadonlyArray<TestVector<LinearRec2020, EncodedRec2020>> = [
  {
    input: [0, 0, 0] as unknown as LinearRec2020,
    output: [0, 0, 0] as unknown as EncodedRec2020,
    tolerance: NONLINEAR_TOLERANCE,
    source: 'BT.2020 — black point',
  },
  {
    input: [1, 1, 1] as unknown as LinearRec2020,
    output: [1, 1, 1] as unknown as EncodedRec2020,
    tolerance: NONLINEAR_TOLERANCE,
    source: 'BT.2020 — white point',
  },
];
