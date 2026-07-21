// <cvd-safe-palette n="5" hue="0"></cvd-safe-palette>
//
// Generate an N-color palette and report the worst-case ΔE_ok separation
// across normal vision plus the three Machado CVD simulations (protan,
// deutan, tritan). Greedy optimization tries small offsets to maximize
// the minimum pairwise ΔE under any vision condition.

import { toHex, fmt } from '../utils.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as oklch from '../../dist/spaces/oklch.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { deltaEOK } from '../../dist/metrics/deltaE.js';
import { simulationMatrix } from '../../dist/cvd/machado-2009.js';
import { mulMat3Vec3 } from '../../dist/types.js';
import { peakC, M_XYZ_TO_SRGB } from '../../dist/gamut/oklch-peak.js';

const CVDs = [
  { id: 'normal',       label: 'Normal vision' },
  { id: 'protanopia',   label: 'Protanopia'   },
  { id: 'deuteranopia', label: 'Deuteranopia' },
  { id: 'tritanopia',   label: 'Tritanopia'   },
];

function oklchToHex(L, C, h) {
  const lab = oklch.toOKLab([L, C, h]);
  const xyz = oklab.toXYZ(lab);
  const lin = srgb.fromXYZ(xyz);
  const cs = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  return toHex(srgbTransfer.encode(cs));
}

function oklchToOklab(L, C, h) {
  return oklch.toOKLab([L, C, h]);
}

function applyCVDtoOklab(lab, type) {
  if (type === 'normal') return lab;
  const xyz = oklab.toXYZ(lab);
  const lin = srgb.fromXYZ(xyz);
  const sim = mulMat3Vec3(simulationMatrix(type, 1.0), lin);
  const cs = [
    Math.max(0, Math.min(1, sim[0])),
    Math.max(0, Math.min(1, sim[1])),
    Math.max(0, Math.min(1, sim[2])),
  ];
  return oklab.fromXYZ(srgb.toXYZ(cs));
}

function paletteFromHues(hues, L) {
  return hues.map(h => {
    const C = Math.min(0.18, peakC(L, h, M_XYZ_TO_SRGB, 24, 0.4) * 0.95);
    const lab = oklchToOklab(L, C, h);
    return { h, L, C, lab, hex: oklchToHex(L, C, h) };
  });
}

function minSeparationForCVD(palette, cvdType) {
  let minD = Infinity;
  for (let i = 0; i < palette.length; i++) {
    for (let j = i + 1; j < palette.length; j++) {
      const a = applyCVDtoOklab(palette[i].lab, cvdType);
      const b = applyCVDtoOklab(palette[j].lab, cvdType);
      const d = deltaEOK(a, b);
      if (d < minD) minD = d;
    }
  }
  return minD;
}

function worstSeparation(palette) {
  return CVDs.reduce((acc, cvd) => {
    const d = minSeparationForCVD(palette, cvd.id);
    return Math.min(acc, d);
  }, Infinity);
}

function optimizePalette(n, baseHue, L) {
  // Start with evenly spaced hues.
  let hues = [];
  for (let i = 0; i < n; i++) hues.push((baseHue + (360 * i) / n) % 360);
  let best = paletteFromHues(hues, L);
  let bestScore = worstSeparation(best);
  // Coordinate-descent: try ±step on each hue.
  for (let iter = 0; iter < 18; iter++) {
    let improved = false;
    const step = 24 / (1 + iter);
    for (let i = 0; i < n; i++) {
      for (const dir of [-1, 1]) {
        const trial = hues.slice();
        trial[i] = (trial[i] + dir * step + 360) % 360;
        const cand = paletteFromHues(trial, L);
        const candScore = worstSeparation(cand);
        if (candScore > bestScore + 1e-5) {
          hues = trial; best = cand; bestScore = candScore; improved = true;
        }
      }
    }
    if (!improved) break;
  }
  return { palette: best, score: bestScore };
}

class CvdSafePalette extends HTMLElement {
  static get observedAttributes() { return ['n', 'hue', 'lightness']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="cvdp-host"></div>`;
    this._root = this.querySelector('.cvdp-host');
  }

  render() {
    const n = Math.max(2, Math.min(8, parseInt(this.getAttribute('n') ?? '5', 10)));
    const baseHue = parseFloat(this.getAttribute('hue') ?? '0');
    const L = parseFloat(this.getAttribute('lightness') ?? '0.62');

    const { palette, score } = optimizePalette(n, baseHue, L);

    let html = '<div class="cvdp-strip">';
    for (const c of palette) {
      html += '<div class="cvdp-swatch" style="background:' + c.hex + '">'
        + '<span>' + c.hex + '</span>'
        + '</div>';
    }
    html += '</div>';

    // Per-CVD min ΔE rows.
    html += '<table class="cvdp-table"><thead><tr><th>Condition</th><th>min ΔE<sub>ok</sub></th><th></th></tr></thead><tbody>';
    for (const cvd of CVDs) {
      const d = minSeparationForCVD(palette, cvd.id);
      const isWorst = Math.abs(d - score) < 1e-5;
      html += '<tr>' +
        '<td><strong>' + cvd.label + '</strong></td>' +
        '<td><strong>' + fmt(d, 3) + '</strong></td>' +
        '<td>' + (isWorst ? '<span class="pill warn">worst</span>' : '') + '</td>' +
        '</tr>';
    }
    html += '</tbody></table>';
    html += '<div class="cvdp-summary">Worst-case ΔE<sub>ok</sub> across all CVD types: <strong>' + fmt(score, 3) + '</strong></div>';

    this._root.innerHTML = html;
  }
}

customElements.define('cvd-safe-palette', CvdSafePalette);
