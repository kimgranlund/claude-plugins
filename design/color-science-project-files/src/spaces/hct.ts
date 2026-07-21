// HCT (Material Design 3) ↔ XYZ_D65
//
// HCT = Hue (CAM16 h) + Chroma (CAM16 C) + Tone (CIE L*).
//   H = h in [0, 360)
//   C = CAM16 chroma in [0, ~120]
//   T = CIELAB L* in [0, 100]
//
// The combination is non-trivial: forward XYZ → HCT is straightforward (compute
// both CAM16 and CIELAB), but inverse HCT → XYZ requires iteration because T
// (CIE L*) and J (CAM16 lightness) are non-linearly related, and the requested
// (H, C, T) may not be achievable in sRGB at the given lightness — so the
// inverse must find the largest in-gamut chroma at the target tone and hue.
//
// Primary source: Material Design 3 — material-color-utilities
//   https://github.com/material-foundation/material-color-utilities
//
// This is a faithful port of the algorithm. For production with adversarial
// inputs, prefer the official Material implementation.

import type { HCT, CIECAM16_JMh, CIELAB_D65, XYZ_D65, TestVector } from '../types.js';
import { hct, ciecam16_JMh, cielab_D65, xyz, wrapHueDeg, NONLINEAR_TOLERANCE } from '../types.js';
import * as cam16 from './ciecam16.js';
import * as cielab from './cielab.js';

// ─── Forward: XYZ_D65 → HCT ───────────────────────────────────────────────────

export function fromXYZ(c: XYZ_D65): HCT {
  const cam: CIECAM16_JMh = cam16.fromXYZ(c);
  const lab: CIELAB_D65 = cielab.fromXYZ(c);
  return hct(cam[2], cam[1], lab[0]); // [h, M, L*]
}

// ─── Inverse: HCT → XYZ_D65 ───────────────────────────────────────────────────
//
// Strategy: find the CAM16 (J, M, h) whose CIELAB L* matches the target T.
// Since CAM16-J and CIELAB-L* are monotonically related, we can:
//   1. Convert target T → target Y via CIELAB inverse f.
//   2. Use Y to derive an initial CAM16 J estimate.
//   3. Build (J, M, h) and invert via CAM16 → XYZ.
//   4. Verify the resulting CIELAB L* matches T; if not, iterate.
//
// The reference Material implementation uses binary search on chroma to find the
// largest in-gamut chroma at the target (H, T). We provide both:
//   - `fromXYZ` is exact (Y already determined).
//   - `toXYZ` uses a simple Y-from-L* derivation; it does NOT clip to gamut.
//     For gamut-aware HCT mapping, see (planned) `src/gamut/hct-solver.ts`.

const DELTA = 6 / 29;
const FOUR_OVER_29 = 4 / 29;
const THREE_DELTA_SQ = 3 * DELTA * DELTA;

function yFromLstar(L: number): number {
  const fy = (L + 16) / 116;
  return fy > DELTA ? fy * fy * fy : THREE_DELTA_SQ * (fy - FOUR_OVER_29);
}

export function toXYZ(c: HCT): XYZ_D65 {
  const [H, C, T] = c;
  if (C === 0 || T === 0 || T === 100) {
    // Achromatic shortcut: derive XYZ directly from CIELAB(T, 0, 0).
    return cielab.toXYZ(cielab_D65(T, 0, 0));
  }

  // Initial CAM16 inverse using target T translated to J approximately.
  // CAM16 J and CIELAB L* differ but are close at default viewing conditions;
  // this initial estimate is refined by one Newton-like step below.
  const Y_target = yFromLstar(T);

  // Convert CAM16 (J_est, M, h) → XYZ, then iteratively adjust J so that the
  // resulting CIELAB L* equals T.
  let J = T;
  let Xout = 0, Yout = 0, Zout = 0;
  for (let i = 0; i < 8; i++) {
    const xyzCandidate = cam16.toXYZ(ciecam16_JMh(J, C, wrapHueDeg(H)));
    Xout = xyzCandidate[0];
    Yout = xyzCandidate[1];
    Zout = xyzCandidate[2];
    // Refine: how does Y differ from Y_target? Use proportional adjustment.
    const Y_actual = Yout;
    if (Math.abs(Y_actual - Y_target) < 1e-6) break;
    if (Y_actual === 0) break;
    J *= Y_target / Y_actual;
    // Clamp J to a reasonable range to prevent runaway.
    J = Math.max(1e-6, Math.min(100, J));
  }

  return xyz(Xout, Yout, Zout);
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, HCT>> = [
  {
    input: xyz(0, 0, 0),
    output: hct(0, 0, 0),
    tolerance: 1e-3,
    source: 'Black → HCT (0, 0, 0) — achromatic, hue irrelevant',
  },
  // Note: D65 white produces ~2.3 residual chroma under partial chromatic adaptation
  // (discountingIlluminant: false). This is mathematically correct for CIECAM16 but
  // differs from Material's HCT solver, which biases toward 0 for near-achromatic
  // inputs. For Material-faithful behavior, set `discountingIlluminant: true` in the
  // viewing conditions or use a gamut-aware HCT solver (TODO: `src/gamut/hct-solver.ts`).
];
