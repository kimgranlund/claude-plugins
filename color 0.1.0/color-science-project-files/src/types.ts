// Color math system — branded types and shared primitives.
//
// Every color in this system is a [number, number, number] tuple at runtime,
// but the compiler distinguishes between color spaces via branded types.
// This catches space-mixing errors at compile time with zero runtime cost.
//
// See references/ARCHITECTURE.md for the full design rationale.

declare const __colorBrand: unique symbol;

// ─── Source of truth ──────────────────────────────────────────────────────────

/** CIE XYZ at the D65 white point. The hub through which every space converts. */
export type XYZ_D65 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'XYZ_D65';
};

// ─── Linear (un-gamma-encoded) gamut-specific RGB ─────────────────────────────

export type LinearSRGB = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearSRGB';
};
export type LinearP3 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearP3';
};
export type LinearRec2020 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearRec2020';
};
export type LinearRec709 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearRec709';
};
export type LinearAdobeRGB = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearAdobeRGB';
};
export type LinearProPhoto = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LinearProPhoto';
};

// ─── Gamma-encoded (display-ready) gamut-specific RGB ─────────────────────────

export type EncodedSRGB = readonly [number, number, number] & {
  readonly [__colorBrand]: 'EncodedSRGB';
};
export type EncodedP3 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'EncodedP3';
};
export type EncodedRec2020 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'EncodedRec2020';
};

// ─── Perceptual spaces ────────────────────────────────────────────────────────

/** OKLab: L ∈ [0, 1] roughly; a, b unbounded but typically in [-0.4, 0.4]. */
export type OKLab = readonly [number, number, number] & {
  readonly [__colorBrand]: 'OKLab';
};

/** OKLCH: [L, C, h_degrees]. CSS convention is degrees, not radians. */
export type OKLCH = readonly [number, number, number] & {
  readonly [__colorBrand]: 'OKLCH';
};

/** CIELAB at D65. (Traditional definition is D50; D65 variant matches modern displays.) */
export type CIELAB_D65 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CIELAB_D65';
};

/** CIELAB at D50 (ICC profile connection space convention). */
export type CIELAB_D50 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CIELAB_D50';
};

export type CIELCH_D65 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CIELCH_D65';
};

export type CIELCH_D50 = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CIELCH_D50';
};

// ─── Cylindrical RGB-derived (non-perceptual) ─────────────────────────────────

/** HSL: [hue_degrees, saturation_0_1, lightness_0_1]. */
export type HSL = readonly [number, number, number] & {
  readonly [__colorBrand]: 'HSL';
};
/** HSV: [hue_degrees, saturation_0_1, value_0_1]. */
export type HSV = readonly [number, number, number] & {
  readonly [__colorBrand]: 'HSV';
};

// ─── XYZ chromaticity form ────────────────────────────────────────────────────

/** xyY: [chromaticity_x, chromaticity_y, luminance_Y]. Polar form of XYZ. */
export type xyY = readonly [number, number, number] & {
  readonly [__colorBrand]: 'xyY';
};

// ─── Perceptual cylindrical (Ottosson) ────────────────────────────────────────

/** OKHSL: [hue_degrees, saturation_0_1, lightness_0_1]. Ottosson's perceptual HSL. */
export type OKHSL = readonly [number, number, number] & {
  readonly [__colorBrand]: 'OKHSL';
};
/** OKHSV: [hue_degrees, saturation_0_1, value_0_1]. Ottosson's perceptual HSV. */
export type OKHSV = readonly [number, number, number] & {
  readonly [__colorBrand]: 'OKHSV';
};

// ─── Appearance models ────────────────────────────────────────────────────────

/** CIECAM16 in JMh form: [J_lightness, M_colorfulness, h_degrees]. */
export type CIECAM16_JMh = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CIECAM16_JMh';
};

/** CAM16-UCS uniform color space: [J, a, b]. */
export type CAM16_UCS = readonly [number, number, number] & {
  readonly [__colorBrand]: 'CAM16_UCS';
};

/** Material Design HCT: [H_hue_deg, C_chroma_cam16, T_tone_Lstar]. */
export type HCT = readonly [number, number, number] & {
  readonly [__colorBrand]: 'HCT';
};

// ─── HDR spaces ───────────────────────────────────────────────────────────────

export type Jzazbz = readonly [number, number, number] & {
  readonly [__colorBrand]: 'Jzazbz';
};

export type ICtCp = readonly [number, number, number] & {
  readonly [__colorBrand]: 'ICtCp';
};

// ─── Intermediate (rarely consumed directly) ──────────────────────────────────

/** LMS — long/medium/short cone response. Intermediate space for OKLab and CIECAM. */
export type LMS = readonly [number, number, number] & {
  readonly [__colorBrand]: 'LMS';
};

// ─── Optional richer source-of-truth: Spectral SPD ────────────────────────────

/**
 * Spectral Power Distribution: 36 samples from 380nm to 730nm at 10nm intervals.
 * Used for pigment mixing, metamer construction, illuminant-correct work.
 */
export type SPD = ReadonlyArray<number> & {
  readonly [__colorBrand]: 'SPD_380_730_10nm';
};

// ─── Construction helpers (brand a tuple without runtime cost) ────────────────

export const xyz = (X: number, Y: number, Z: number) =>
  [X, Y, Z] as unknown as XYZ_D65;

export const linearSRGB = (R: number, G: number, B: number) =>
  [R, G, B] as unknown as LinearSRGB;

export const encodedSRGB = (R: number, G: number, B: number) =>
  [R, G, B] as unknown as EncodedSRGB;

export const linearP3 = (R: number, G: number, B: number) =>
  [R, G, B] as unknown as LinearP3;

export const linearRec2020 = (R: number, G: number, B: number) =>
  [R, G, B] as unknown as LinearRec2020;

export const oklab = (L: number, a: number, b: number) =>
  [L, a, b] as unknown as OKLab;

export const oklch = (L: number, C: number, h: number) =>
  [L, C, h] as unknown as OKLCH;

export const cielab_D65 = (L: number, a: number, b: number) =>
  [L, a, b] as unknown as CIELAB_D65;

export const cielch_D65 = (L: number, C: number, h: number) =>
  [L, C, h] as unknown as CIELCH_D65;

export const xyY = (x: number, y: number, Y: number) =>
  [x, y, Y] as unknown as xyY;

export const okhsl = (h: number, s: number, l: number) =>
  [h, s, l] as unknown as OKHSL;

export const okhsv = (h: number, s: number, v: number) =>
  [h, s, v] as unknown as OKHSV;

export const hct = (h: number, c: number, t: number) =>
  [h, c, t] as unknown as HCT;

export const ciecam16_JMh = (J: number, M: number, h: number) =>
  [J, M, h] as unknown as CIECAM16_JMh;

// ─── Matrix primitives ────────────────────────────────────────────────────────

export type Matrix3x3 = readonly [
  readonly [number, number, number],
  readonly [number, number, number],
  readonly [number, number, number]
];

/** Multiply a 3x3 matrix by a 3-vector. Returns a plain mutable tuple — caller brands it. */
export function mulMat3Vec3(
  m: Matrix3x3,
  v: readonly [number, number, number]
): [number, number, number] {
  return [
    m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
    m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
    m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
  ];
}

/** Multiply two 3x3 matrices. Useful for pre-composing transforms (e.g., M_XYZ→sRGB * M_adapt). */
export function mulMat3Mat3(a: Matrix3x3, b: Matrix3x3): Matrix3x3 {
  const r = (i: number, j: number) =>
    a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j];
  return [
    [r(0, 0), r(0, 1), r(0, 2)],
    [r(1, 0), r(1, 1), r(1, 2)],
    [r(2, 0), r(2, 1), r(2, 2)],
  ];
}

// ─── Test vector contract ─────────────────────────────────────────────────────

/**
 * Test vector for round-trip and primary-source verification.
 * Every module exports a `testVectors` array of these.
 */
export type TestVector<Input, Output> = {
  readonly input: Input;
  readonly output: Output;
  /** Maximum allowed L∞ distance between computed and expected output. */
  readonly tolerance: number;
  /** Primary source citation for the expected output. */
  readonly source: string;
  readonly note?: string;
};

// ─── Sign-preserving cube root (used by OKLab, CIELAB, others) ────────────────

/** Sign-preserving cube root. Required when LMS or XYZ values can be negative (out of gamut). */
export const cbrt = (x: number): number =>
  Math.sign(x) * Math.pow(Math.abs(x), 1 / 3);

// ─── Hue wrapping (used by polar spaces) ──────────────────────────────────────

/** Normalize a hue angle in degrees to [0, 360). */
export const wrapHueDeg = (h: number): number => {
  const r = h % 360;
  return r < 0 ? r + 360 : r;
};

// ─── Tolerance for round-trip checks ──────────────────────────────────────────

/** Max L∞ distance considered equal for linear (matrix-only) round-trips. */
export const LINEAR_TOLERANCE = 1e-9;

/** Max L∞ distance considered equal for nonlinear (cube root, gamma) round-trips. */
export const NONLINEAR_TOLERANCE = 1e-4;

/** L∞ distance between two tuples. */
export function lInfDistance(
  a: readonly [number, number, number],
  b: readonly [number, number, number]
): number {
  return Math.max(
    Math.abs(a[0] - b[0]),
    Math.abs(a[1] - b[1]),
    Math.abs(a[2] - b[2])
  );
}
