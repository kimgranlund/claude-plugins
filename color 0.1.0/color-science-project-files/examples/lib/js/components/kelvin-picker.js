// <kelvin-picker temp="6500"></kelvin-picker>
//
// Blackbody temperature → color via Kim/CIE chromaticity polynomial, with a
// mini xy chromaticity diagram showing the Planckian locus from 1500K to
// 25000K and the dot for the currently-selected temperature.

import { setupCanvas, toHex } from '../utils.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as xyy from '../../dist/spaces/xyy.js';

// Kim/CIE 2002 polynomial approximations for the Planckian xy chromaticity.
function plankianXY(T) {
  let x;
  if (T < 4000) {
    x = -0.2661239e9 / (T * T * T) - 0.2343589e6 / (T * T) + 0.8776956e3 / T + 0.179910;
  } else {
    x = -3.0258469e9 / (T * T * T) + 2.1070379e6 / (T * T) + 0.2226347e3 / T + 0.240390;
  }
  let y;
  if (T < 2222) {
    y = -1.1063814 * x * x * x - 1.34811020 * x * x + 2.18555832 * x - 0.20219683;
  } else if (T < 4000) {
    y = -0.9549476 * x * x * x - 1.37418593 * x * x + 2.09137015 * x - 0.16748867;
  } else {
    y = 3.0817580 * x * x * x - 5.87338670 * x * x + 3.75112997 * x - 0.37001483;
  }
  return [x, y];
}

function kelvinToHex(T) {
  const [x, y] = plankianXY(T);
  if (y === 0) return '#000000';
  const xyz = xyy.toXYZ([x, y, 1.0]);
  // Normalize so max RGB component is 1.0 (otherwise the swatch is clipped white).
  const lin = srgb.fromXYZ(xyz);
  const m = Math.max(lin[0], lin[1], lin[2], 1e-6);
  const norm = [lin[0] / m, lin[1] / m, lin[2] / m];
  const clamped = norm.map(v => Math.max(0, Math.min(1, v)));
  return toHex(srgbTransfer.encode(clamped));
}

// Standard illuminant chromaticities for reference dots.
const REFERENCE_ILLUMINANTS = [
  { name: 'A',   T: 2856,  x: 0.4476, y: 0.4074 },
  { name: 'D50', T: 5003,  x: 0.3457, y: 0.3585 },
  { name: 'D55', T: 5503,  x: 0.3324, y: 0.3474 },
  { name: 'D65', T: 6504,  x: 0.3127, y: 0.3290 },
  { name: 'D75', T: 7504,  x: 0.2990, y: 0.3149 },
];

class KelvinPicker extends HTMLElement {
  static get observedAttributes() { return ['temp']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="kelvin-host">
      <div class="kelvin-swatch"></div>
      <div class="kelvin-readout"></div>
      <canvas class="kelvin-locus"></canvas>
    </div>`;
    this._root = this.querySelector('.kelvin-host');
    this._sw = this.querySelector('.kelvin-swatch');
    this._readout = this.querySelector('.kelvin-readout');
    this._canvas = this.querySelector('.kelvin-locus');
  }

  render() {
    const T = Math.max(1500, Math.min(25000, parseFloat(this.getAttribute('temp') ?? '6500')));
    const [x, y] = plankianXY(T);
    const hex = kelvinToHex(T);
    this._sw.style.background = hex;
    this._readout.innerHTML =
      '<div><strong>' + T.toFixed(0) + ' K</strong></div>' +
      '<div>x = ' + x.toFixed(4) + '</div>' +
      '<div>y = ' + y.toFixed(4) + '</div>' +
      '<div>' + hex + '</div>';

    // ─── Mini chromaticity diagram ──────────────────────────────────────
    // Read both dimensions from the CSS layout (grid cell + aspect-ratio),
    // then size the buffer at 1× DPR for crisp output.
    const rect = this._canvas.getBoundingClientRect();
    const cssW = rect.width  > 10 ? rect.width  : 360;
    const cssH = rect.height > 10 ? rect.height : Math.round(cssW * 7 / 8);
    const dpr = window.devicePixelRatio || 1;
    this._canvas.width  = Math.round(cssW * dpr);
    this._canvas.height = Math.round(cssH * dpr);
    const ctx = this._canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = cssW, h = cssH;
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);

    // Plot bounds cover the full 1500-25000 K slider range plus margin.
    // At 1500 K the locus reaches x ≈ 0.58, at 25000 K x ≈ 0.25.
    const xMin = 0.22, xMax = 0.62;
    const yMin = 0.20, yMax = 0.50;
    const X = (xv) => ((xv - xMin) / (xMax - xMin)) * w;
    const Y = (yv) => h - ((yv - yMin) / (yMax - yMin)) * h;

    // Grid
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
    ctx.lineWidth = 1;
    ctx.font = '10px ui-monospace, monospace';
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    [0.3, 0.4, 0.5, 0.6].forEach(v => {
      const px = X(v); ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, h); ctx.stroke();
      ctx.fillText(v.toFixed(1), px + 2, h - 4);
    });
    [0.2, 0.3, 0.4, 0.5].forEach(v => {
      const py = Y(v); ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(w, py); ctx.stroke();
      ctx.fillText(v.toFixed(1), 2, py - 2);
    });

    // Planckian locus 1500K → 25000K
    ctx.beginPath();
    let first = true;
    for (let t = 1500; t <= 25000; t += t < 4000 ? 100 : 500) {
      const [px, py] = plankianXY(t);
      if (px < xMin || px > xMax || py < yMin || py > yMax) continue;
      const cx = X(px), cy = Y(py);
      if (first) { ctx.moveTo(cx, cy); first = false; } else ctx.lineTo(cx, cy);
    }
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || 'oklch(0.55 0.18 264)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Reference illuminant dots
    for (const ill of REFERENCE_ILLUMINANTS) {
      const cx = X(ill.x), cy = Y(ill.y);
      ctx.beginPath();
      ctx.arc(cx, cy, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#fff';
      ctx.fill();
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
      ctx.fillText(ill.name, cx + 5, cy - 4);
    }

    // Current temperature dot
    const cx = X(x), cy = Y(y);
    ctx.beginPath();
    ctx.arc(cx, cy, 7, 0, Math.PI * 2);
    ctx.fillStyle = hex;
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1;
    ctx.stroke();
  }
}

customElements.define('kelvin-picker', KelvinPicker);
