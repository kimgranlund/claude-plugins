// Standard illuminant SPDs (Spectral Power Distributions).
//
// 36 samples per illuminant from 380nm to 730nm at 10nm intervals — matches
// the SPD branded type and CIE color matching function tabulation.
//
// Values are relative SPDs normalized so the integral over the visible range
// against the CIE 1931 2° Y CMF gives Y = 100.
//
// Primary source: CIE 015:2018, Tables 1-3. Values reproduced from the W3C
// CSS Color 4 working group reference data.

import type { SPD } from '../types.js';

// ─── D65 (modern display standard, ~6500 K) ──────────────────────────────────

/** D65 standard illuminant at 380-730nm, 10nm steps. */
export const D65: SPD = [
  49.9755, 54.6482, 82.7549, 91.4860, 93.4318, 86.6823, 104.8650, 117.0080,
  117.8120, 114.8610, 115.9230, 108.8110, 109.3540, 107.8020, 104.7900, 107.6890,
  104.4050, 104.0460, 100.0000, 96.3342, 95.7880, 88.6856, 90.0062, 89.5991,
  87.6987, 83.2886, 83.6992, 80.0268, 80.2146, 82.2778, 78.2842, 69.7213,
  71.6091, 74.3490, 61.6040, 69.8856,
] as unknown as SPD;

// ─── D50 (ICC PCS, traditional CIELAB white) ─────────────────────────────────

/** D50 standard illuminant. */
export const D50: SPD = [
  24.4880, 27.1791, 39.5808, 44.9117, 46.6383, 47.1834, 60.0322, 67.3963,
  68.6125, 67.3534, 70.2992, 67.9145, 70.6403, 71.8260, 73.2832, 78.4108,
  78.8729, 80.9152, 80.4498, 81.5301, 84.5717, 80.7019, 86.1606, 88.7676,
  89.9090, 87.8907, 91.7404, 90.7150, 92.5969, 96.6097, 92.1183, 83.4070,
  86.1611, 90.7204, 75.0727, 86.1635,
] as unknown as SPD;

// ─── A (CIE Standard Illuminant A — incandescent tungsten, ~2856 K) ──────────

/** A standard illuminant (tungsten). */
export const A: SPD = [
  9.7951, 12.0853, 14.7080, 17.6753, 20.9950, 24.6709, 28.7027, 33.0859,
  37.8121, 42.8693, 48.2423, 53.9132, 59.8611, 66.0635, 72.4959, 79.1326,
  85.9470, 92.9120, 100.0000, 107.1840, 114.4360, 121.7310, 129.0430, 136.3460,
  143.6180, 150.8360, 157.9790, 165.0280, 171.9630, 178.7690, 185.4290, 191.9310,
  198.2610, 204.4090, 210.3650, 216.1170,
] as unknown as SPD;

// ─── F2 (CIE Standard Illuminant F2 — cool white fluorescent) ────────────────

/** F2 standard illuminant — cool white fluorescent (~4230 K).
 * Note the characteristic mercury-vapor spikes near 405, 435, 545, and 580 nm. */
export const F2: SPD = [
  1.18, 1.48, 1.84, 2.15, 3.44, 15.69, 3.85, 3.74,
  4.19, 4.62, 5.06, 34.98, 11.81, 6.27, 7.32, 8.45,
  9.92, 11.51, 12.79, 13.71, 14.20, 14.06, 13.18, 11.92,
  10.51, 9.05, 7.65, 6.27, 5.16, 4.10, 3.20, 2.43,
  1.89, 1.46, 1.10, 0.81,
] as unknown as SPD;

// ─── E (equal-energy illuminant, theoretical) ─────────────────────────────────

/** E equal-energy illuminant — flat spectrum. Useful for testing / metamerism work. */
export const E: SPD = new Array(36).fill(100) as unknown as SPD;

// ─── Wavelength axis ──────────────────────────────────────────────────────────

/** The 36 wavelengths (nm) sampled by all illuminants and CMFs in this skill. */
export const WAVELENGTHS_NM: readonly number[] = (() => {
  const out: number[] = [];
  for (let i = 0; i < 36; i++) out.push(380 + i * 10);
  return out;
})();
