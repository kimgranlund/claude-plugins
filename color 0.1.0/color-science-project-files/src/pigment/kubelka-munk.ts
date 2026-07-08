// Kubelka-Munk single-constant pigment mixing.
//
// The standard model for paint / dye / ink mixing in the real world. Unlike
// RGB averaging (which produces unrealistic muddy mid-tones), K-M mixing
// produces physically plausible blends — blue + yellow really makes green.
//
// Single-constant K-M assumes opaque materials with a single absorption-to-
// scattering ratio per wavelength: K/S. Mixing is linear in K/S space:
//
//   (K/S)_mix = Σᵢ cᵢ · (K/S)ᵢ      where cᵢ are concentrations summing to 1
//
// The forward transform R → K/S is Kubelka's: $K/S = (1 - R)^2 / (2 R)$
// The inverse K/S → R is: $R = 1 + K/S - \sqrt{(K/S)^2 + 2 (K/S)}$
//
// For two-constant K-M (translucent/glaze) and Saunderson correction (surface
// reflection), see references/techniques/kubelka-munk-single-constant.md.
//
// Primary source: Kubelka, P. (1948), "New Contributions to the Optics of
// Intensely Light-Scattering Materials," J. Optical Society of America 38(5).

// ─── Reflectance ↔ K/S ────────────────────────────────────────────────────────

/** Scalar K/S from reflectance R ∈ (0, 1]. Returns 0 for R = 1, ∞ as R → 0. */
export function reflectanceToKS(R: number): number {
  if (R <= 0) return 1e6;
  if (R >= 1) return 0;
  return ((1 - R) * (1 - R)) / (2 * R);
}

/** Scalar reflectance from K/S. Always in [0, 1]. */
export function KSToReflectance(KS: number): number {
  if (KS <= 0) return 1;
  return 1 + KS - Math.sqrt(KS * KS + 2 * KS);
}

// ─── Spectrum ↔ K/S spectrum ──────────────────────────────────────────────────

/** Reflectance spectrum → K/S spectrum (per-wavelength). */
export function spectrumToKS(reflectance: readonly number[]): number[] {
  return reflectance.map(reflectanceToKS);
}

/** K/S spectrum → reflectance spectrum. */
export function KSToSpectrum(KS: readonly number[]): number[] {
  return KS.map(KSToReflectance);
}

// ─── Mixing ───────────────────────────────────────────────────────────────────

/**
 * Mix two reflectance spectra at given concentrations (single-constant K-M).
 * The result is a new reflectance spectrum.
 */
export function mix(
  spectrumA: readonly number[],
  spectrumB: readonly number[],
  concentrationA: number
): number[] {
  const cA = Math.max(0, Math.min(1, concentrationA));
  const cB = 1 - cA;
  const ksA = spectrumToKS(spectrumA);
  const ksB = spectrumToKS(spectrumB);
  const mixed = ksA.map((ks, i) => cA * ks + cB * ksB[i]);
  return KSToSpectrum(mixed);
}

/**
 * Mix N reflectance spectra at given concentrations (sum should equal 1).
 * Concentrations are normalized if they don't sum to 1.
 */
export function mixN(
  spectra: ReadonlyArray<readonly number[]>,
  concentrations: readonly number[]
): number[] {
  if (spectra.length !== concentrations.length) {
    throw new Error('spectra.length must equal concentrations.length');
  }
  const sum = concentrations.reduce((a, b) => a + b, 0);
  if (sum <= 0) throw new Error('concentrations must sum to > 0');
  const normalized = concentrations.map(c => c / sum);
  const n = spectra[0].length;
  const mixedKS = new Array(n).fill(0);
  for (let s = 0; s < spectra.length; s++) {
    const ks = spectrumToKS(spectra[s]);
    for (let i = 0; i < n; i++) {
      mixedKS[i] += normalized[s] * ks[i];
    }
  }
  return KSToSpectrum(mixedKS);
}

// ─── Test cases ───────────────────────────────────────────────────────────────

import type { MetricTest } from '../metrics/deltaE.js';

export const testCases: ReadonlyArray<MetricTest> = [
  {
    name: 'reflectanceToKS(1) = 0 (white)',
    fn: () => reflectanceToKS(1),
    expected: 0,
    tolerance: 1e-12,
    source: 'Perfect reflector has zero absorption / infinite scattering ratio = 0',
  },
  {
    name: 'reflectanceToKS(0.5) ≈ 0.25',
    fn: () => reflectanceToKS(0.5),
    expected: 0.25,
    tolerance: 1e-12,
    source: '(1-0.5)² / (2·0.5) = 0.25',
  },
  {
    name: 'KSToReflectance(0) = 1',
    fn: () => KSToReflectance(0),
    expected: 1,
    tolerance: 1e-12,
    source: 'No absorption → perfect reflector',
  },
  {
    name: 'K-M round trip: reflectance → KS → reflectance',
    fn: () => {
      const R = 0.3;
      return Math.abs(KSToReflectance(reflectanceToKS(R)) - R);
    },
    expected: 0,
    tolerance: 1e-12,
    source: 'Round-trip identity for reflectance ↔ K/S',
  },
  {
    name: 'Mixing white + 4%-black at c=0.5 produces K-M midpoint R ≈ 0.074',
    fn: () => {
      const white = new Array(36).fill(1);
      const black = new Array(36).fill(0.04);
      const mixed = mix(white, black, 0.5);
      return mixed[0];
    },
    expected: 0.074,
    tolerance: 0.005,
    source: 'K-M white+black at 50:50 → R ≈ 0.074 (RGB midpoint would be 0.52) — the key K-M property',
  },
];
