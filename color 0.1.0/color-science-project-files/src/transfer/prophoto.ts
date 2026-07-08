// ProPhoto RGB (ROMM RGB) gamma — piecewise.
//
// Linear segment for very small values (slope = 16), then power 1/1.8 above.
// This compensates for ProPhoto's very wide gamut by giving more code values
// to the visible dynamic range and less to negative / out-of-gamut regions.
//
//   encoded = 16 · linear            for linear < 0.001953125
//   encoded = linear^(1/1.8)         otherwise
//
// Primary source: Eastman Kodak Company, "Reference Output Medium Metric
// RGB Color Encoding" (ROMM RGB) 2003. ANSI/I3A IT10.7666.

import type { LinearProPhoto, TestVector } from '../types.js';
import { NONLINEAR_TOLERANCE } from '../types.js';

const ET = 1 / 512; // 0.001953125 — piecewise boundary in linear space
const ET2 = 16 / 512; // 0.03125 — piecewise boundary in encoded space
const SLOPE = 16;
const GAMMA = 1.8;
const INV_GAMMA = 1 / GAMMA;

export function encodeComponent(linear: number): number {
  const abs = Math.abs(linear);
  const sign = Math.sign(linear);
  if (abs < ET) return sign * SLOPE * abs;
  return sign * Math.pow(abs, INV_GAMMA);
}

export function decodeComponent(encoded: number): number {
  const abs = Math.abs(encoded);
  const sign = Math.sign(encoded);
  if (abs < ET2) return sign * abs / SLOPE;
  return sign * Math.pow(abs, GAMMA);
}

export function encode(linear: LinearProPhoto): readonly [number, number, number] {
  return [
    encodeComponent(linear[0]),
    encodeComponent(linear[1]),
    encodeComponent(linear[2]),
  ];
}

export function decode(encoded: readonly [number, number, number]): LinearProPhoto {
  return [
    decodeComponent(encoded[0]),
    decodeComponent(encoded[1]),
    decodeComponent(encoded[2]),
  ] as unknown as LinearProPhoto;
}

export const testVectors: ReadonlyArray<TestVector<LinearProPhoto, readonly [number, number, number]>> = [
  {
    input: [0, 0, 0] as unknown as LinearProPhoto,
    output: [0, 0, 0],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'ProPhoto — black point',
  },
  {
    input: [1, 1, 1] as unknown as LinearProPhoto,
    output: [1, 1, 1],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'ProPhoto — white point (1^(1/1.8) = 1)',
  },
  {
    input: [ET, ET, ET] as unknown as LinearProPhoto,
    output: [ET2, ET2, ET2],
    tolerance: NONLINEAR_TOLERANCE,
    source: 'ProPhoto — piecewise boundary at linear=1/512',
  },
];
