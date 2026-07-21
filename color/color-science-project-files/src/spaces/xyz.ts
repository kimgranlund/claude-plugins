// XYZ_D65 — identity module
//
// XYZ_D65 is the source of truth in this system. Every other space module
// converts to/from XYZ_D65. This module exists so that XYZ itself satisfies
// the `SpaceModule<T>` contract (toXYZ + fromXYZ) — both functions are the
// identity. This makes XYZ a uniform participant in the registry / convert.ts.

import type { XYZ_D65, TestVector } from '../types.js';
import { xyz, LINEAR_TOLERANCE } from '../types.js';

export function toXYZ(c: XYZ_D65): XYZ_D65 {
  return c;
}

export function fromXYZ(c: XYZ_D65): XYZ_D65 {
  return c;
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, XYZ_D65>> = [
  {
    input: xyz(0.95047, 1.0, 1.08883),
    output: xyz(0.95047, 1.0, 1.08883),
    tolerance: LINEAR_TOLERANCE,
    source: 'D65 white point — identity check',
  },
];
