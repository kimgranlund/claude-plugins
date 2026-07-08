// HSL ↔ XYZ_D65 (via encoded sRGB)
//
// HSL is a cylindrical reparameterization of encoded (gamma-encoded) sRGB.
// It is NOT perceptual. For perceptual cylindrical color, use OKLCH.
//
// Storage: [hue_degrees, saturation_0_1, lightness_0_1]
// CSS convention: hue in degrees, sat/lightness as fractions (CSS uses %).
//
// Pipeline: HSL → encoded sRGB → linear sRGB → XYZ_D65 (and inverse).

import type { HSL, EncodedSRGB, XYZ_D65, TestVector } from '../types.js';
import { encodedSRGB, xyz, wrapHueDeg, NONLINEAR_TOLERANCE } from '../types.js';
import * as srgbTransfer from '../transfer/srgb.js';
import * as srgbSpace from './srgb.js';

// ─── HSL ↔ encoded sRGB ───────────────────────────────────────────────────────

export function toEncodedSRGB(hsl: HSL): EncodedSRGB {
  const [hDeg, s, l] = hsl;
  const h = wrapHueDeg(hDeg);
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const hp = h / 60;
  const x = c * (1 - Math.abs((hp % 2) - 1));
  let r1 = 0, g1 = 0, b1 = 0;
  if (hp < 1)      { r1 = c; g1 = x; b1 = 0; }
  else if (hp < 2) { r1 = x; g1 = c; b1 = 0; }
  else if (hp < 3) { r1 = 0; g1 = c; b1 = x; }
  else if (hp < 4) { r1 = 0; g1 = x; b1 = c; }
  else if (hp < 5) { r1 = x; g1 = 0; b1 = c; }
  else             { r1 = c; g1 = 0; b1 = x; }
  const m = l - c / 2;
  return encodedSRGB(r1 + m, g1 + m, b1 + m);
}

export function fromEncodedSRGB(rgb: EncodedSRGB): HSL {
  const [r, g, b] = rgb;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const d = max - min;
  const l = (max + min) / 2;

  let h: number;
  let s: number;

  if (d === 0) {
    h = 0;
    s = 0;
  } else {
    s = d / (1 - Math.abs(2 * l - 1));
    if (max === r)      h = 60 * (((g - b) / d) % 6);
    else if (max === g) h = 60 * (((b - r) / d) + 2);
    else                h = 60 * (((r - g) / d) + 4);
    if (h < 0) h += 360;
  }

  return [h, s, l] as unknown as HSL;
}

// ─── HSL ↔ XYZ_D65 (composition) ──────────────────────────────────────────────

export function toXYZ(hsl: HSL): XYZ_D65 {
  const encoded = toEncodedSRGB(hsl);
  const linear = srgbTransfer.decode(encoded);
  return srgbSpace.toXYZ(linear);
}

export function fromXYZ(c: XYZ_D65): HSL {
  const linear = srgbSpace.fromXYZ(c);
  const encoded = srgbTransfer.encode(linear);
  return fromEncodedSRGB(encoded);
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, HSL>> = [
  // Note: achromatic round-trip fails because hue is indeterminate at S=0.
  // Only chromatic test vectors where (h, s, l) are all well-defined.
  {
    input: xyz(0.4123907993, 0.2126390059, 0.0193308187), // pure sRGB red
    output: [0, 1, 0.5] as unknown as HSL,
    tolerance: 1e-3,
    source: 'Pure sRGB red → HSL (0°, 100%, 50%)',
  },
];
