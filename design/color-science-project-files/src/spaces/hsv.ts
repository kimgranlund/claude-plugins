// HSV ↔ XYZ_D65 (via encoded sRGB)
//
// HSV is a cylindrical reparameterization of encoded sRGB, related to HSL but with
// a different cone shape. Not perceptual. For perceptual cylindrical color use OKLCH
// or OKHSV (Ottosson).
//
// Storage: [hue_degrees, saturation_0_1, value_0_1]
// Pipeline: HSV → encoded sRGB → linear sRGB → XYZ_D65 (and inverse).

import type { HSV, EncodedSRGB, XYZ_D65, TestVector } from '../types.js';
import { encodedSRGB, xyz, wrapHueDeg, NONLINEAR_TOLERANCE } from '../types.js';
import * as srgbTransfer from '../transfer/srgb.js';
import * as srgbSpace from './srgb.js';

export function toEncodedSRGB(hsv: HSV): EncodedSRGB {
  const [hDeg, s, v] = hsv;
  const h = wrapHueDeg(hDeg);
  const c = v * s;
  const hp = h / 60;
  const x = c * (1 - Math.abs((hp % 2) - 1));
  let r1 = 0, g1 = 0, b1 = 0;
  if (hp < 1)      { r1 = c; g1 = x; b1 = 0; }
  else if (hp < 2) { r1 = x; g1 = c; b1 = 0; }
  else if (hp < 3) { r1 = 0; g1 = c; b1 = x; }
  else if (hp < 4) { r1 = 0; g1 = x; b1 = c; }
  else if (hp < 5) { r1 = x; g1 = 0; b1 = c; }
  else             { r1 = c; g1 = 0; b1 = x; }
  const m = v - c;
  return encodedSRGB(r1 + m, g1 + m, b1 + m);
}

export function fromEncodedSRGB(rgb: EncodedSRGB): HSV {
  const [r, g, b] = rgb;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const d = max - min;
  const v = max;
  const s = max === 0 ? 0 : d / max;

  let h: number;
  if (d === 0) {
    h = 0;
  } else if (max === r) {
    h = 60 * (((g - b) / d) % 6);
  } else if (max === g) {
    h = 60 * (((b - r) / d) + 2);
  } else {
    h = 60 * (((r - g) / d) + 4);
  }
  if (h < 0) h += 360;

  return [h, s, v] as unknown as HSV;
}

export function toXYZ(hsv: HSV): XYZ_D65 {
  return srgbSpace.toXYZ(srgbTransfer.decode(toEncodedSRGB(hsv)));
}

export function fromXYZ(c: XYZ_D65): HSV {
  return fromEncodedSRGB(srgbTransfer.encode(srgbSpace.fromXYZ(c)));
}

export const testVectors: ReadonlyArray<TestVector<XYZ_D65, HSV>> = [
  // Note: achromatic round-trip fails because hue is indeterminate at S=0.
  // Only chromatic test vectors below.
  {
    input: xyz(0.4123907993, 0.2126390059, 0.0193308187), // pure sRGB red
    output: [0, 1, 1] as unknown as HSV,
    tolerance: 1e-3,
    source: 'Pure sRGB red → HSV (0°, 100%, 100%)',
  },
];
