// Relative luminance (CIE Y) and WCAG 2.x contrast.
//
// Relative luminance Y is just the Y component of XYZ_D65. This module provides
// convenience wrappers for the common cases (encoded sRGB input, WCAG contrast).
//
// Primary sources:
//   - CIE 015:2018 (relative luminance definition)
//   - WCAG 2.1/2.2 (contrast ratio definition): https://www.w3.org/TR/WCAG22/#contrast-minimum
//   - IEC 61966-2-1 (sRGB transfer)
//
// For modern UX work, prefer APCA over WCAG. See `apca-myndex-contrast.md` and
// (planned) `src/metrics/apca.ts`.

import type { EncodedSRGB, LinearSRGB, XYZ_D65 } from '../types.js';
import * as srgbTransfer from '../transfer/srgb.js';
import * as srgbSpace from '../spaces/srgb.js';

/** Relative luminance Y from XYZ_D65. Trivially the Y component. */
export function fromXYZ(c: XYZ_D65): number {
  return c[1];
}

/** Relative luminance Y from linear sRGB via the standard coefficients. */
export function fromLinearSRGB(c: LinearSRGB): number {
  return 0.2126390059 * c[0] + 0.7151686788 * c[1] + 0.0721923154 * c[2];
}

/** WCAG-style relative luminance from encoded (gamma-encoded) sRGB. */
export function fromEncodedSRGB(c: EncodedSRGB): number {
  return fromLinearSRGB(srgbTransfer.decode(c));
}

/**
 * WCAG 2.x contrast ratio between two encoded sRGB colors.
 * Returns a value in [1, 21].
 *
 * Thresholds (per WCAG 2.1/2.2):
 *   - 3.0:1 — Large text (≥18pt regular or 14pt bold), AA
 *   - 4.5:1 — Normal text, AA
 *   - 7.0:1 — Normal text, AAA
 */
export function wcagContrast(a: EncodedSRGB, b: EncodedSRGB): number {
  const La = fromEncodedSRGB(a);
  const Lb = fromEncodedSRGB(b);
  const lighter = Math.max(La, Lb);
  const darker = Math.min(La, Lb);
  return (lighter + 0.05) / (darker + 0.05);
}

/** True iff the pair clears WCAG AA for normal text (≥4.5:1). */
export const passesAA = (a: EncodedSRGB, b: EncodedSRGB) =>
  wcagContrast(a, b) >= 4.5;

/** True iff the pair clears WCAG AA for large text (≥3.0:1). */
export const passesAALarge = (a: EncodedSRGB, b: EncodedSRGB) =>
  wcagContrast(a, b) >= 3.0;

/** True iff the pair clears WCAG AAA for normal text (≥7.0:1). */
export const passesAAA = (a: EncodedSRGB, b: EncodedSRGB) =>
  wcagContrast(a, b) >= 7.0;

// ─── Test cases ───────────────────────────────────────────────────────────────

import { xyz, encodedSRGB, linearSRGB } from '../types.js';
import type { MetricTest } from './deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'luminance.fromXYZ extracts Y component',
    fn: () => fromXYZ(xyz(0.5, 0.7, 0.3)),
    expected: 0.7,
    tolerance: 1e-12,
    source: 'Y is the second component of XYZ_D65 by definition',
  },
  {
    name: 'linear sRGB white has Y = 1',
    fn: () => fromLinearSRGB(linearSRGB(1, 1, 1)),
    expected: 1.0,
    tolerance: 1e-6,
    source: 'BT.709 luminance coefficients sum to 1',
  },
  {
    name: 'linear sRGB black has Y = 0',
    fn: () => fromLinearSRGB(linearSRGB(0, 0, 0)),
    expected: 0,
    tolerance: 1e-12,
    source: 'Zero light → zero luminance',
  },
  {
    name: 'WCAG contrast pure white on pure black = 21',
    fn: () => wcagContrast(encodedSRGB(1, 1, 1), encodedSRGB(0, 0, 0)),
    expected: 21,
    tolerance: 1e-4,
    source: 'WCAG max contrast: (1 + 0.05) / (0 + 0.05) = 21',
  },
  {
    name: 'WCAG contrast same color = 1',
    fn: () => wcagContrast(encodedSRGB(0.5, 0.5, 0.5), encodedSRGB(0.5, 0.5, 0.5)),
    expected: 1,
    tolerance: 1e-12,
    source: 'WCAG min contrast: identity is 1',
  },
  {
    name: 'WCAG contrast is symmetric',
    fn: () => {
      const a = encodedSRGB(0.2, 0.3, 0.4);
      const b = encodedSRGB(0.8, 0.7, 0.6);
      return Math.abs(wcagContrast(a, b) - wcagContrast(b, a));
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'WCAG contrast is order-independent',
  },
];
