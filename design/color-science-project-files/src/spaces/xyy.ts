// xyY ↔ XYZ_D65
//
// xyY is XYZ expressed as chromaticity (x, y) + luminance (Y).
//   x = X / (X + Y + Z)
//   y = Y / (X + Y + Z)
//   z = 1 - x - y  (implicit)
//
// Inverse:
//   X = x * Y / y
//   Z = (1 - x - y) * Y / y
//
// Used for chromaticity diagrams (CIE 1931) and white-point definitions.
// D65 white point: x ≈ 0.31272, y ≈ 0.32903.

import type { xyY, XYZ_D65, TestVector } from '../types.js';
import { xyY as makeXyY, xyz, LINEAR_TOLERANCE } from '../types.js';

export function fromXYZ(c: XYZ_D65): xyY {
  const [X, Y, Z] = c;
  const sum = X + Y + Z;
  if (sum === 0) {
    // Black point: chromaticity undefined, use D65 chromaticity by convention.
    return makeXyY(0.31272, 0.32903, 0);
  }
  return makeXyY(X / sum, Y / sum, Y);
}

export function toXYZ(c: xyY): XYZ_D65 {
  const [x, y, Y] = c;
  if (y === 0) return xyz(0, 0, 0);
  const X = (x * Y) / y;
  const Z = ((1 - x - y) * Y) / y;
  return xyz(X, Y, Z);
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, xyY>> = [
  {
    input: xyz(0.9504559270516716, 1.0, 1.0890577507598784),
    output: makeXyY(0.31272661468101586, 0.32902313032606195, 1),
    tolerance: 1e-4,
    source: 'D65 white point — canonical chromaticity x≈0.3127, y≈0.3290',
  },
  {
    input: xyz(0, 0, 0),
    output: makeXyY(0.31272, 0.32903, 0),
    tolerance: 1e-3,
    source: 'Black point — chromaticity convention (D65 fallback)',
  },
];
