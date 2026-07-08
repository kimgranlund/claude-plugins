// <tonal-palette source="#3b82f6"></tonal-palette>
//
// Material Design 3 tonal-palette generator. Given a source color, produce
// 5 tonal palettes (primary / secondary / tertiary / neutral / neutral-variant)
// at 11 tones each (0, 10, 20, ..., 100). Tone is CIELAB L*.
//
// Algorithm (faithful to material-color-utilities):
//   1. source → HCT (H, C, T)
//   2. primary:          (H, C, T_i)     for each tone i
//   3. secondary:        (H, C * 0.33, T_i)
//   4. tertiary:         (H + 60°, C * 0.5, T_i)
//   5. neutral:          (H, 4, T_i)     low chroma
//   6. neutral variant:  (H, 8, T_i)
//
// For each (H, C, T_i), reduce C if needed to fit in sRGB (binary search).

import { toHex, fmt } from '../utils.js';
import * as hct from '../../dist/spaces/hct.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

const TONES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100];

function hctToHexInGamut(H, C, T) {
  // Binary search on chroma to find max in-gamut C ≤ requested C.
  let lo = 0, hi = C;
  const inGamut = (c) => {
    const xyz = hct.toXYZ([H, c, T]);
    const lin = srgb.fromXYZ(xyz);
    return lin[0] >= -0.005 && lin[0] <= 1.005
        && lin[1] >= -0.005 && lin[1] <= 1.005
        && lin[2] >= -0.005 && lin[2] <= 1.005;
  };
  if (inGamut(C)) {
    lo = C;
  } else {
    for (let i = 0; i < 18; i++) {
      const m = (lo + hi) / 2;
      if (inGamut(m)) lo = m; else hi = m;
    }
  }
  const xyz = hct.toXYZ([H, lo, T]);
  const lin = srgb.fromXYZ(xyz);
  const clamped = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  return toHex(srgbTransfer.encode(clamped));
}

function hexToHCT(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const lin = srgbTransfer.decode([r, g, b]);
  const xyz = srgb.toXYZ(lin);
  return hct.fromXYZ(xyz);
}

class TonalPalette extends HTMLElement {
  static get observedAttributes() { return ['source']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="tonal-host"></div>`;
    this._root = this.querySelector('.tonal-host');
  }

  render() {
    const source = this.getAttribute('source') || '#3b82f6';
    if (!/^#[0-9a-fA-F]{6}$/.test(source)) return;
    const [H, C, T] = hexToHCT(source);

    const palettes = [
      { name: 'Primary',          H, C },
      { name: 'Secondary',        H, C: Math.max(8, C * 0.33) },
      { name: 'Tertiary',         H: (H + 60) % 360, C: Math.max(8, C * 0.5) },
      { name: 'Neutral',          H, C: 4 },
      { name: 'Neutral variant',  H, C: 8 },
    ];

    let html = '<table class="tonal-table"><thead><tr><th></th>';
    for (const t of TONES) html += '<th>' + t + '</th>';
    html += '</tr></thead><tbody>';
    for (const p of palettes) {
      html += '<tr><th>' + p.name + '</th>';
      for (const t of TONES) {
        const hex = hctToHexInGamut(p.H, p.C, t);
        const textColor = t >= 50 ? '#111' : '#fff';
        html += '<td style="background:' + hex + ';color:' + textColor + '"><span>' + hex + '</span></td>';
      }
      html += '</tr>';
    }
    html += '</tbody></table>';

    html += '<div class="tonal-source">';
    html += '<strong>Source</strong> ' + source + ' → HCT(';
    html += 'H=' + fmt(H, 1) + ', C=' + fmt(C, 2) + ', T=' + fmt(T, 2) + ')';
    html += '</div>';

    this._root.innerHTML = html;
  }
}

customElements.define('tonal-palette', TonalPalette);
