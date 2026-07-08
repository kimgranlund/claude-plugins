// CIE color matching functions.
//
// The three functions that, when integrated against a Spectral Power
// Distribution (SPD), produce CIE XYZ. They encode the human visual
// response of the standard 2° observer (CIE 1931).
//
// Values at 380-730nm in 10nm steps. Source: CIE 1931 (re-tabulated for
// 10nm intervals from the original 5nm data).

// ─── CIE 1931 2° observer ─────────────────────────────────────────────────────

/** $\bar{x}(\lambda)$ at 380-730nm, 10nm steps. */
export const X_BAR_1931: readonly number[] = [
  0.001368, 0.004243, 0.014310, 0.043510, 0.134380, 0.283900, 0.348280, 0.336200,
  0.290800, 0.195360, 0.095640, 0.032010, 0.004900, 0.009300, 0.063270, 0.165500,
  0.290400, 0.433450, 0.594500, 0.762100, 0.916300, 1.026300, 1.062200, 1.002600,
  0.854450, 0.642400, 0.447900, 0.283500, 0.164900, 0.087400, 0.046770, 0.022700,
  0.011359, 0.005790, 0.002899, 0.001440,
];

/** $\bar{y}(\lambda)$ at 380-730nm, 10nm steps. */
export const Y_BAR_1931: readonly number[] = [
  0.000039, 0.000120, 0.000396, 0.001210, 0.004000, 0.011600, 0.023000, 0.038000,
  0.060000, 0.090980, 0.139020, 0.208020, 0.323000, 0.503000, 0.710000, 0.862000,
  0.954000, 0.994950, 0.995000, 0.952000, 0.870000, 0.757000, 0.631000, 0.503000,
  0.381000, 0.265000, 0.175000, 0.107000, 0.061000, 0.032000, 0.017000, 0.008210,
  0.004102, 0.002091, 0.001047, 0.000520,
];

/** $\bar{z}(\lambda)$ at 380-730nm, 10nm steps. */
export const Z_BAR_1931: readonly number[] = [
  0.006450, 0.020050, 0.067850, 0.207400, 0.645600, 1.385600, 1.747060, 1.772110,
  1.669200, 1.287640, 0.812950, 0.465180, 0.272000, 0.158200, 0.078250, 0.042160,
  0.020300, 0.008750, 0.003900, 0.002100, 0.001650, 0.001100, 0.000800, 0.000340,
  0.000190, 0.000050, 0.000020, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
  0.000000, 0.000000, 0.000000, 0.000000,
];

/** All three CMFs packed as 36 × 3 array (one row per wavelength). */
export const CMF_1931: ReadonlyArray<readonly [number, number, number]> = (() => {
  const out: Array<readonly [number, number, number]> = [];
  for (let i = 0; i < 36; i++) {
    out.push([X_BAR_1931[i], Y_BAR_1931[i], Z_BAR_1931[i]]);
  }
  return out;
})();
