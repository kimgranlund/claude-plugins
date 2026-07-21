// <token-ramp hue="264" curve="tailwind" chroma="auto"></token-ramp>
//
// Generate an 11-stop OKLCh color ramp at a fixed hue, with the chroma at each
// stop bounded by `peakC(L, h)` to keep every step in sRGB gamut.
//
// Attributes:
//   hue     — float in [0, 360]
//   curve   — "tailwind" (default), "linear", "smoothstep", "gamma-1.5"
//   chroma  — "auto" (default; peakC at each L) or a fixed float (e.g. "0.12")
//   target  — "srgb" (default) | "p3" | "rec2020" — gamut for the peakC clamp

import { toHex, toCssOklch, fmt } from '../utils.js';
import * as oklchSpace from '../../dist/spaces/oklch.js';
import * as oklabSpace from '../../dist/spaces/oklab.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import {
  peakC,
  M_XYZ_TO_SRGB,
  M_XYZ_TO_P3,
  M_XYZ_TO_REC2020,
} from '../../dist/gamut/oklch-peak.js';
import {
  TAILWIND_V4_L_STOPS,
  linearRamp,
  smoothstepRamp,
  gammaRamp,
} from '../../dist/interpolation/lightness-curves.js';

const STEP_LABELS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];

const GAMUT_MATRIX = {
  srgb: M_XYZ_TO_SRGB,
  p3: M_XYZ_TO_P3,
  rec2020: M_XYZ_TO_REC2020,
};

function oklchToHex(L, C, hDeg) {
  const lab = oklchSpace.toOKLab([L, C, hDeg]);
  const xyz = oklabSpace.toXYZ(lab);
  const lin = srgbSpace.fromXYZ(xyz);
  const clamped = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  return toHex(srgbTransfer.encode(clamped));
}

class TokenRamp extends HTMLElement {
  static get observedAttributes() { return ['hue', 'curve', 'chroma', 'target']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() {
    if (this._root) this.render();
  }

  _mount() {
    this.innerHTML = `<div class="ramp-host"></div>`;
    this._root = this.querySelector('.ramp-host');
  }

  render() {
    const hue = parseFloat(this.getAttribute('hue') ?? '264');
    const curve = this.getAttribute('curve') || 'tailwind';
    const chromaAttr = this.getAttribute('chroma') || 'auto';
    const target = this.getAttribute('target') || 'srgb';
    const matrix = GAMUT_MATRIX[target] || M_XYZ_TO_SRGB;

    // Compute L stops based on the chosen curve.
    let lStops;
    if (curve === 'tailwind') {
      lStops = TAILWIND_V4_L_STOPS.slice();
    } else if (curve === 'linear') {
      lStops = STEP_LABELS.map((_, i) => linearRamp(1 - i / (STEP_LABELS.length - 1), 0.13, 0.985));
    } else if (curve === 'smoothstep') {
      lStops = STEP_LABELS.map((_, i) => smoothstepRamp(1 - i / (STEP_LABELS.length - 1), 0.13, 0.985));
    } else if (curve.startsWith('gamma-')) {
      const g = parseFloat(curve.slice(6)) || 1.5;
      lStops = STEP_LABELS.map((_, i) => gammaRamp(1 - i / (STEP_LABELS.length - 1), g, 0.13, 0.985));
    } else {
      lStops = TAILWIND_V4_L_STOPS.slice();
    }

    // For each (L, hue), compute peak chroma OR use the fixed chroma.
    const rows = lStops.map((L, i) => {
      let C;
      if (chromaAttr === 'auto') {
        C = peakC(L, hue, matrix, 28, 0.4);
      } else {
        const fixed = parseFloat(chromaAttr) || 0;
        C = Math.min(fixed, peakC(L, hue, matrix, 24, 0.4));
      }
      const hex = oklchToHex(L, C, hue);
      const css = toCssOklch([L, C, hue]);
      return { step: STEP_LABELS[i], L, C, hex, css };
    });

    this._root.innerHTML = rows.map(r => `
      <div class="ramp-row" style="background:${r.hex};color:${r.L > 0.5 ? '#111' : '#fafafa'}">
        <div class="ramp-step">${r.step}</div>
        <div class="ramp-meta">
          <div class="ramp-hex">${r.hex}</div>
          <div class="ramp-css">${r.css}</div>
        </div>
        <div class="ramp-lc">L=${fmt(r.L, 3)} C=${fmt(r.C, 3)}</div>
      </div>
    `).join('');
  }
}

customElements.define('token-ramp', TokenRamp);
