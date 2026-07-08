// Color difference (ΔE) — the five variants worth knowing.
//
// All ΔE values are scalar non-negative distances. ΔE = 0 means identical colors.
// "Just noticeable difference" (JND) is roughly ΔE76 ≈ 2.3, ΔE2000 ≈ 1, ΔE_ok ≈ 0.02.
//
// Choose based on your task:
//   - ΔE_ok       — modern default for design tokens, palette work (OKLab-based)
//   - ΔE2000      — gold standard for color science / print / textile
//   - ΔE94        — legacy graphic-arts default; superseded by ΔE2000
//   - ΔE76        — Euclidean in CIELAB; obsolete but ubiquitous
//   - HyAB        — perceptually motivated hybrid (Lab) — robust for large differences
//
// Primary sources:
//   - CIE 015:2018 (CIELAB and the original ΔE definition)
//   - CIE 116:1995 (CIE94)
//   - CIE 142:2001 (CIEDE2000)
//   - Sharma, Wu, Dalal "The CIEDE2000 Color-Difference Formula" (2005)
//   - Ottosson 2020 (OKLab; ΔE_ok = Euclidean in OKLab)
//   - Abasi et al. "Distance metrics for very large color differences" (2020) — HyAB

import type { CIELAB_D65, OKLab } from '../types.js';

// ─── ΔE76 — Euclidean distance in CIELAB ──────────────────────────────────────

/** ΔE*ab (CIE 1976). Simple, fast, perceptually uneven. */
export function deltaE76(a: CIELAB_D65, b: CIELAB_D65): number {
  const dL = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return Math.sqrt(dL * dL + dA * dA + dB * dB);
}

// ─── ΔE94 — weighted CIELAB difference (CIE 1994) ─────────────────────────────

/**
 * ΔE*94 with graphic-arts weights (kL=1, K1=0.045, K2=0.015).
 * `textiles` flag toggles the textile weights (kL=2, K1=0.048, K2=0.014).
 */
export function deltaE94(
  a: CIELAB_D65,
  b: CIELAB_D65,
  textiles: boolean = false
): number {
  const [L1, a1, b1] = a;
  const [L2, a2, b2] = b;
  const C1 = Math.hypot(a1, b1);
  const C2 = Math.hypot(a2, b2);
  const dC = C1 - C2;
  const dL = L1 - L2;
  const dA = a1 - a2;
  const dB = b1 - b2;
  const dH2 = Math.max(0, dA * dA + dB * dB - dC * dC);

  const kL = textiles ? 2 : 1;
  const K1 = textiles ? 0.048 : 0.045;
  const K2 = textiles ? 0.014 : 0.015;
  const sL = 1;
  const sC = 1 + K1 * C1;
  const sH = 1 + K2 * C1;

  const tL = dL / (kL * sL);
  const tC = dC / sC;
  return Math.sqrt(tL * tL + tC * tC + dH2 / (sH * sH));
}

// ─── ΔE2000 — current gold standard (CIE 2001) ────────────────────────────────

/**
 * ΔE2000 — Sharma/Wu/Dalal implementation with rotational term.
 * The most perceptually accurate ΔE in widespread use.
 */
export function deltaE2000(
  a: CIELAB_D65,
  b: CIELAB_D65,
  kL: number = 1,
  kC: number = 1,
  kH: number = 1
): number {
  const [L1, a1, b1] = a;
  const [L2, a2, b2] = b;

  const C1 = Math.hypot(a1, b1);
  const C2 = Math.hypot(a2, b2);
  const Cbar = (C1 + C2) / 2;

  const Cbar7 = Math.pow(Cbar, 7);
  const G = 0.5 * (1 - Math.sqrt(Cbar7 / (Cbar7 + Math.pow(25, 7))));

  const a1p = (1 + G) * a1;
  const a2p = (1 + G) * a2;

  const C1p = Math.hypot(a1p, b1);
  const C2p = Math.hypot(a2p, b2);

  const h1p = (() => {
    if (b1 === 0 && a1p === 0) return 0;
    const h = Math.atan2(b1, a1p) * 180 / Math.PI;
    return h < 0 ? h + 360 : h;
  })();
  const h2p = (() => {
    if (b2 === 0 && a2p === 0) return 0;
    const h = Math.atan2(b2, a2p) * 180 / Math.PI;
    return h < 0 ? h + 360 : h;
  })();

  const dLp = L2 - L1;
  const dCp = C2p - C1p;

  let dhp = 0;
  if (C1p === 0 || C2p === 0) {
    dhp = 0;
  } else {
    const diff = h2p - h1p;
    if (Math.abs(diff) <= 180) dhp = diff;
    else if (diff > 180) dhp = diff - 360;
    else dhp = diff + 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin((dhp / 2) * Math.PI / 180);

  const Lbar = (L1 + L2) / 2;
  const Cbarp = (C1p + C2p) / 2;

  let hbarp;
  if (C1p === 0 || C2p === 0) {
    hbarp = h1p + h2p;
  } else if (Math.abs(h1p - h2p) <= 180) {
    hbarp = (h1p + h2p) / 2;
  } else if (h1p + h2p < 360) {
    hbarp = (h1p + h2p + 360) / 2;
  } else {
    hbarp = (h1p + h2p - 360) / 2;
  }

  const T = 1
    - 0.17 * Math.cos((hbarp - 30) * Math.PI / 180)
    + 0.24 * Math.cos((2 * hbarp) * Math.PI / 180)
    + 0.32 * Math.cos((3 * hbarp + 6) * Math.PI / 180)
    - 0.20 * Math.cos((4 * hbarp - 63) * Math.PI / 180);

  const dTheta = 30 * Math.exp(-Math.pow((hbarp - 275) / 25, 2));
  const Rc = 2 * Math.sqrt(Math.pow(Cbarp, 7) / (Math.pow(Cbarp, 7) + Math.pow(25, 7)));
  const Sl = 1 + (0.015 * Math.pow(Lbar - 50, 2)) / Math.sqrt(20 + Math.pow(Lbar - 50, 2));
  const Sc = 1 + 0.045 * Cbarp;
  const Sh = 1 + 0.015 * Cbarp * T;
  const Rt = -Math.sin(2 * dTheta * Math.PI / 180) * Rc;

  const tL = dLp / (kL * Sl);
  const tC = dCp / (kC * Sc);
  const tH = dHp / (kH * Sh);

  return Math.sqrt(tL * tL + tC * tC + tH * tH + Rt * tC * tH);
}

// ─── ΔE_ok — Euclidean distance in OKLab ──────────────────────────────────────

/** ΔE_ok = Euclidean distance in OKLab. Modern recommended default for design work. */
export function deltaEOK(a: OKLab, b: OKLab): number {
  const dL = a[0] - b[0];
  const dA = a[1] - b[1];
  const dB = a[2] - b[2];
  return Math.sqrt(dL * dL + dA * dA + dB * dB);
}

// ─── HyAB — Hybrid angular + Lab distance ─────────────────────────────────────

/**
 * HyAB — Euclidean L + city-block (a, b).
 * Robust for large color differences where Euclidean ΔE76 fails perceptually.
 */
export function hyAB(a: CIELAB_D65, b: CIELAB_D65): number {
  const dL = a[0] - b[0];
  const dA = Math.abs(a[1] - b[1]);
  const dB = Math.abs(a[2] - b[2]);
  return Math.sqrt(dL * dL) + dA + dB;
}

// ─── Test vectors ─────────────────────────────────────────────────────────────

import { cielab_D65, oklab } from '../types.js';

export type MetricTest = {
  name: string;
  fn: () => number;
  expected: number;
  tolerance: number;
  source: string;
};

export const testCases: ReadonlyArray<MetricTest> = [
  // Identity: same color → 0
  {
    name: 'deltaE76 identity',
    fn: () => deltaE76(cielab_D65(50, 10, -20), cielab_D65(50, 10, -20)),
    expected: 0,
    tolerance: 1e-12,
    source: 'Trivial identity',
  },
  {
    name: 'deltaE2000 identity',
    fn: () => deltaE2000(cielab_D65(50, 10, -20), cielab_D65(50, 10, -20)),
    expected: 0,
    tolerance: 1e-12,
    source: 'Trivial identity',
  },
  {
    name: 'deltaEOK identity',
    fn: () => deltaEOK(oklab(0.5, 0.1, -0.05), oklab(0.5, 0.1, -0.05)),
    expected: 0,
    tolerance: 1e-12,
    source: 'Trivial identity',
  },
  // Sharma et al. (2005), Table 1 — selected CIEDE2000 test pairs:
  {
    name: 'deltaE2000 Sharma pair 1 (50,2.6772,-79.7751 vs 50,0,-82.7485)',
    fn: () => deltaE2000(
      cielab_D65(50, 2.6772, -79.7751),
      cielab_D65(50, 0.0, -82.7485)
    ),
    expected: 2.0425,
    tolerance: 5e-4,
    source: 'Sharma/Wu/Dalal 2005 Table 1 pair 1',
  },
  {
    name: 'deltaE2000 Sharma pair 2 (50,3.1571,-77.2803 vs 50,0,-82.7485)',
    fn: () => deltaE2000(
      cielab_D65(50, 3.1571, -77.2803),
      cielab_D65(50, 0.0, -82.7485)
    ),
    expected: 2.8615,
    tolerance: 5e-4,
    source: 'Sharma/Wu/Dalal 2005 Table 1 pair 2',
  },
  // deltaE76: pure perpendicular axis distance
  {
    name: 'deltaE76 axis distance (a)',
    fn: () => deltaE76(cielab_D65(50, 0, 0), cielab_D65(50, 50, 0)),
    expected: 50,
    tolerance: 1e-12,
    source: 'Trivial axis-aligned distance',
  },
  // HyAB: city-block in (a, b)
  {
    name: 'hyAB city-block (a, b)',
    fn: () => hyAB(cielab_D65(50, 0, 0), cielab_D65(50, 3, 4)),
    expected: 7,
    tolerance: 1e-12,
    source: 'Pure (a, b) city-block distance: 3 + 4 = 7',
  },
];
