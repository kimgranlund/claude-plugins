// APCA — Accessible Perceptual Contrast Algorithm.
//
// Polarity-sensitive, spatial-frequency-aware contrast metric. Replaces WCAG 2.x
// contrast for modern UX work. Returns L^c in roughly [-108, +106]:
//   - Positive  = dark text on light background ("BoW")
//   - Negative  = light text on dark background ("WoB")
//   - Magnitude = perceived contrast (higher = more readable)
//
// APCA uses a SIMPLIFIED 2.4-power gamma (not sRGB's piecewise), and proprietary
// luminance weights. Both are intentional — APCA is calibrated against
// readability research, not strict colorimetry.
//
// Primary source: APCA-W3 (MIT-licensed reference)
//   https://github.com/Myndex/apca-w3
//   v0.1.9 constants used below.
//
// Note: APCA's exact constants have evolved; this implementation tracks
// APCA-W3 v0.1.9 (the version adopted by the W3C-archived APCA Bronze Simple
// Mode). For absolute parity check against apca-w3 at the same version.

import type { EncodedSRGB } from '../types.js';

// ─── APCA-W3 constants (v0.1.9) ───────────────────────────────────────────────

const MAIN_TRC = 2.4;                // simplified gamma
const SR_CO = 0.2126729;             // sRGB luminance weight, R
const SG_CO = 0.7151522;             // sRGB luminance weight, G
const SB_CO = 0.0721750;             // sRGB luminance weight, B

const NORM_BG = 0.56;                // exponent for BG in dark-text case
const NORM_TXT = 0.57;               // exponent for TXT in dark-text case
const REV_TXT = 0.62;                // exponent for TXT in light-text case
const REV_BG = 0.65;                 // exponent for BG in light-text case

const BLK_THRS = 0.022;              // near-black input clamp threshold
const BLK_CLMP = 1.414;              // near-black clamp curve exponent
const SCALE_BOW = 1.14;              // dark-text scaling
const SCALE_WOB = 1.14;              // light-text scaling
const LO_BOW_OFFSET = 0.027;         // dark-text low-contrast offset
const LO_WOB_OFFSET = 0.027;         // light-text low-contrast offset
const DELTA_Y_MIN = 0.0005;          // min Y delta to trigger contrast
const LO_CLIP = 0.1;                 // smoothing clip near zero

// ─── APCA luminance from encoded sRGB ─────────────────────────────────────────

/**
 * APCA's simplified Y from encoded sRGB. Uses pure 2.4 gamma + sRGB weights.
 * NOT the same as CIE relative luminance; do not use for non-APCA work.
 */
export function apcaY(rgb: EncodedSRGB): number {
  const r = Math.pow(rgb[0], MAIN_TRC);
  const g = Math.pow(rgb[1], MAIN_TRC);
  const b = Math.pow(rgb[2], MAIN_TRC);
  let y = SR_CO * r + SG_CO * g + SB_CO * b;

  // Near-black soft clamp
  if (y < BLK_THRS) {
    y = y + Math.pow(BLK_THRS - y, BLK_CLMP);
  }
  return y;
}

// ─── APCA contrast (L^c) ──────────────────────────────────────────────────────

/**
 * APCA contrast L^c for text on background.
 * Returns positive for dark-text-on-light, negative for light-text-on-dark.
 * Magnitude indicates perceived readability; see thresholds below.
 */
export function apcaContrast(text: EncodedSRGB, bg: EncodedSRGB): number {
  const txtY = apcaY(text);
  const bgY = apcaY(bg);

  if (Math.abs(bgY - txtY) < DELTA_Y_MIN) return 0;

  let SAPC = 0;
  if (bgY > txtY) {
    // Dark text on light background (BoW)
    const C = SCALE_BOW * (Math.pow(bgY, NORM_BG) - Math.pow(txtY, NORM_TXT));
    if (C < LO_CLIP) {
      SAPC = 0;
    } else if (C < LO_BOW_OFFSET) {
      SAPC = C - (C * 32.8 * (LO_BOW_OFFSET - C) / LO_BOW_OFFSET);
    } else {
      SAPC = C - LO_BOW_OFFSET;
    }
    return SAPC * 100;
  } else {
    // Light text on dark background (WoB)
    const C = SCALE_WOB * (Math.pow(bgY, REV_BG) - Math.pow(txtY, REV_TXT));
    if (C > -LO_CLIP) {
      SAPC = 0;
    } else if (C > -LO_WOB_OFFSET) {
      SAPC = C - (C * 32.8 * (-LO_WOB_OFFSET - C) / -LO_WOB_OFFSET);
    } else {
      SAPC = C + LO_WOB_OFFSET;
    }
    return SAPC * 100;
  }
}

// ─── Threshold tests (APCA Bronze Simple Mode) ────────────────────────────────

/** Absolute value of L^c, the way APCA tables are organized. */
export const lcMagnitude = (lc: number) => Math.abs(lc);

/**
 * Quick readability tier (APCA Bronze Simple Mode, approximate).
 * For the full font-size × weight table, see references/techniques/apca-lc-formula.md.
 */
export type ApcaTier =
  | 'non-text-only'      // |Lc| 15-29
  | 'large-heading'      // |Lc| 30-44
  | 'heading-or-large-body' // |Lc| 45-59
  | 'body-minimum'       // |Lc| 60-74
  | 'fluent-body'        // |Lc| 75-89
  | 'optimal'            // |Lc| 90+
  | 'insufficient';      // |Lc| < 15

export function readabilityTier(lc: number): ApcaTier {
  const m = Math.abs(lc);
  if (m >= 90) return 'optimal';
  if (m >= 75) return 'fluent-body';
  if (m >= 60) return 'body-minimum';
  if (m >= 45) return 'heading-or-large-body';
  if (m >= 30) return 'large-heading';
  if (m >= 15) return 'non-text-only';
  return 'insufficient';
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import { encodedSRGB } from '../types.js';
import type { MetricTest } from './deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'apca identity (same color = 0)',
    fn: () => apcaContrast(encodedSRGB(0.5, 0.5, 0.5), encodedSRGB(0.5, 0.5, 0.5)),
    expected: 0,
    tolerance: 1e-9,
    source: 'Trivial identity',
  },
  {
    name: 'apca pure black-on-white returns large positive',
    fn: () => apcaContrast(encodedSRGB(0, 0, 0), encodedSRGB(1, 1, 1)),
    expected: 106.0,
    tolerance: 0.5,
    source: 'APCA-W3 reference; pure black on white ~= 106',
  },
  {
    name: 'apca pure white-on-black returns large negative',
    fn: () => apcaContrast(encodedSRGB(1, 1, 1), encodedSRGB(0, 0, 0)),
    expected: -107.88,
    tolerance: 0.5,
    source: 'APCA-W3 reference; pure white on black ~= -107.88',
  },
];
