// <chromaticity-diagram show="srgb,p3,rec2020"></chromaticity-diagram>
//
// CIE 1931 xy chromaticity diagram. Renders:
//   - Spectral locus (horseshoe) sampled at 5nm steps from 380-700nm.
//   - Selected gamut triangles (sRGB, P3, Rec.2020, Adobe RGB, ProPhoto).
//   - White points (D50, D55, D65, A).
//   - Interior fill = sRGB-mapped color at each (x, y) for an illustrative
//     "what colors live here" effect.
//   - Click to pick → emits `pick` event with detail { x, y, Y, xyz }.

import { setupCanvas } from '../utils.js';
import * as xyySpace from '../../dist/spaces/xyy.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

// CIE 1931 2° standard observer locus, x-y values at 5nm steps from 380 to 700 nm
// (subsampled from CIE 015:2018). Enough for visually smooth horseshoe.
const SPECTRAL_LOCUS = [
  [380, 0.1741, 0.0050], [385, 0.1740, 0.0050], [390, 0.1738, 0.0049],
  [395, 0.1736, 0.0049], [400, 0.1733, 0.0048], [405, 0.1730, 0.0048],
  [410, 0.1726, 0.0048], [415, 0.1721, 0.0048], [420, 0.1714, 0.0051],
  [425, 0.1703, 0.0058], [430, 0.1689, 0.0069], [435, 0.1669, 0.0086],
  [440, 0.1644, 0.0109], [445, 0.1611, 0.0138], [450, 0.1566, 0.0177],
  [455, 0.1510, 0.0227], [460, 0.1440, 0.0297], [465, 0.1355, 0.0399],
  [470, 0.1241, 0.0578], [475, 0.1096, 0.0868], [480, 0.0913, 0.1327],
  [485, 0.0687, 0.2007], [490, 0.0454, 0.2950], [495, 0.0235, 0.4127],
  [500, 0.0082, 0.5384], [505, 0.0039, 0.6548], [510, 0.0139, 0.7502],
  [515, 0.0389, 0.8120], [520, 0.0743, 0.8338], [525, 0.1142, 0.8262],
  [530, 0.1547, 0.8059], [535, 0.1929, 0.7816], [540, 0.2296, 0.7543],
  [545, 0.2658, 0.7243], [550, 0.3016, 0.6923], [555, 0.3373, 0.6589],
  [560, 0.3731, 0.6245], [565, 0.4087, 0.5896], [570, 0.4441, 0.5547],
  [575, 0.4788, 0.5202], [580, 0.5125, 0.4866], [585, 0.5448, 0.4544],
  [590, 0.5752, 0.4242], [595, 0.6029, 0.3965], [600, 0.6270, 0.3725],
  [605, 0.6482, 0.3514], [610, 0.6658, 0.3340], [615, 0.6801, 0.3197],
  [620, 0.6915, 0.3083], [625, 0.7006, 0.2993], [630, 0.7079, 0.2920],
  [635, 0.7140, 0.2859], [640, 0.7190, 0.2809], [645, 0.7230, 0.2770],
  [650, 0.7260, 0.2740], [655, 0.7283, 0.2717], [660, 0.7300, 0.2700],
  [665, 0.7311, 0.2689], [670, 0.7320, 0.2680], [675, 0.7327, 0.2673],
  [680, 0.7334, 0.2666], [685, 0.7340, 0.2660], [690, 0.7344, 0.2656],
  [695, 0.7346, 0.2654], [700, 0.7347, 0.2653],
];

const GAMUTS = {
  srgb:    { name: 'sRGB',       color: 'oklch(0.554 0.180 264)', tri: [[0.6400, 0.3300], [0.3000, 0.6000], [0.1500, 0.0600]] },
  p3:      { name: 'Display P3', color: 'oklch(0.620 0.180 150)', tri: [[0.6800, 0.3200], [0.2650, 0.6900], [0.1500, 0.0600]] },
  rec2020: { name: 'Rec.2020',   color: 'oklch(0.700 0.180  50)', tri: [[0.7080, 0.2920], [0.1700, 0.7970], [0.1310, 0.0460]] },
  adobergb:{ name: 'Adobe RGB',  color: 'oklch(0.554 0.180 300)', tri: [[0.6400, 0.3300], [0.2100, 0.7100], [0.1500, 0.0600]] },
  prophoto:{ name: 'ProPhoto',   color: 'oklch(0.620 0.180 200)', tri: [[0.7347, 0.2653], [0.1596, 0.8404], [0.0366, 0.0001]] },
};

const WHITE_POINTS = [
  { name: 'D65', x: 0.31272, y: 0.32903 },
  { name: 'D50', x: 0.34567, y: 0.35850 },
  { name: 'D55', x: 0.33242, y: 0.34743 },
  { name: 'A',   x: 0.44757, y: 0.40745 },
];

const X_RANGE = [0, 0.8];
const Y_RANGE = [0, 0.9];

function xToPx(x, w) { return ((x - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])) * w; }
function yToPx(y, h) { return h - ((y - Y_RANGE[0]) / (Y_RANGE[1] - Y_RANGE[0])) * h; }

function pointInTriangle(px, py, tri) {
  const [a, b, c] = tri;
  const d1 = (px - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (py - b[1]);
  const d2 = (px - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (py - c[1]);
  const d3 = (px - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (py - a[1]);
  const hasNeg = (d1 < 0) || (d2 < 0) || (d3 < 0);
  const hasPos = (d1 > 0) || (d2 > 0) || (d3 > 0);
  return !(hasNeg && hasPos);
}

class ChromaticityDiagram extends HTMLElement {
  static get observedAttributes() { return ['show', 'pick']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _mount() {
    this.innerHTML = `<canvas tabindex="0" role="application" aria-label="CIE xy chromaticity diagram — click, drag, or use arrow keys to pick a chromaticity"></canvas>`;
    this._canvas = this.querySelector('canvas');
    this._canvas.addEventListener('keydown', e => this._handleKey(e));
    // Pointer drag — click is a degenerate case. Pointer capture keeps the
    // pick streaming even if the cursor leaves the canvas mid-drag.
    this._dragging = false;
    this._canvas.addEventListener('pointerdown', e => {
      e.preventDefault();
      this._dragging = true;
      try { this._canvas.setPointerCapture(e.pointerId); } catch {}
      this._handlePoint(e);
    });
    this._canvas.addEventListener('pointermove', e => {
      if (this._dragging) this._handlePoint(e);
    });
    const endDrag = e => {
      this._dragging = false;
      try { this._canvas.releasePointerCapture(e.pointerId); } catch {}
    };
    this._canvas.addEventListener('pointerup', endDrag);
    this._canvas.addEventListener('pointercancel', endDrag);
  }

  _handlePoint(e) {
    const rect = this._canvas.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width;
    const py = 1 - (e.clientY - rect.top) / rect.height;
    const x = X_RANGE[0] + px * (X_RANGE[1] - X_RANGE[0]);
    const y = Y_RANGE[0] + py * (Y_RANGE[1] - Y_RANGE[0]);
    if (x <= 0 || y <= 0 || (1 - x - y) <= -0.05) return;
    const xyz = xyySpace.toXYZ([x, y, 1]);
    this.dispatchEvent(new CustomEvent('pick', {
      detail: { x, y, Y: 1, xyz },
    }));
  }

  _handleKey(e) {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;
    e.preventDefault();
    const pickAttr = this.getAttribute('pick') || '0.3127,0.3290'; // D65
    const parts = pickAttr.split(',').map(Number);
    let x = parts[0], y = parts[1];
    const step = e.shiftKey ? 0.05 : 0.005;
    if (e.key === 'ArrowLeft')  x = Math.max(X_RANGE[0], x - step);
    if (e.key === 'ArrowRight') x = Math.min(X_RANGE[1], x + step);
    if (e.key === 'ArrowUp')    y = Math.min(Y_RANGE[1], y + step);
    if (e.key === 'ArrowDown')  y = Math.max(Y_RANGE[0], y - step);
    if (x <= 0 || y <= 0 || (1 - x - y) <= -0.05) return;
    const xyz = xyySpace.toXYZ([x, y, 1]);
    this.dispatchEvent(new CustomEvent('pick', {
      detail: { x, y, Y: 1, xyz },
    }));
  }

  render() {
    if (!this._canvas) return;
    const w0 = Math.min(this.offsetWidth || 640, 760);
    const h0 = Math.round(w0 * (Y_RANGE[1] / X_RANGE[1])); // preserve aspect
    const { ctx, w, h } = setupCanvas(this._canvas, w0, h0);
    const showAttr = this.getAttribute('show') || 'srgb,p3,rec2020';
    const showList = showAttr.split(',').map(s => s.trim()).filter(k => GAMUTS[k]);

    // ─── Background gradient inside the locus ──────────────────────────────
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-elevated').trim() || '#222';
    ctx.fillRect(0, 0, w, h);

    // Sample at 1× DPR (matching the canvas buffer) for crisp output without
    // supersampling cost. Capped at 800 for perf on huge displays.
    const dpr = window.devicePixelRatio || 1;
    const RES = Math.min(Math.round(w * dpr), 800);
    const tmp = document.createElement('canvas');
    tmp.width = RES; tmp.height = RES;
    const tmpCtx = tmp.getContext('2d');
    const imgData = tmpCtx.createImageData(RES, RES);
    const data = imgData.data;

    // Build a polygon of the locus + closing purple line for inside-test
    const locusPolyXY = SPECTRAL_LOCUS.map(p => [p[1], p[2]]);

    for (let py = 0; py < RES; py++) {
      for (let px = 0; px < RES; px++) {
        const x = X_RANGE[0] + (px / RES) * (X_RANGE[1] - X_RANGE[0]);
        const y = Y_RANGE[1] - (py / RES) * (Y_RANGE[1] - Y_RANGE[0]);
        // Inside-the-locus test (point-in-polygon)
        if (!pointInPolygon(x, y, locusPolyXY)) {
          data[(py * RES + px) * 4 + 3] = 0;
          continue;
        }
        // xyY → XYZ → sRGB linear → clip → encoded
        const Y = 0.5;
        const xyz = xyySpace.toXYZ([x, y, Y]);
        const lin = srgbSpace.fromXYZ(xyz);
        const cs = [
          Math.max(0, Math.min(1, lin[0])),
          Math.max(0, Math.min(1, lin[1])),
          Math.max(0, Math.min(1, lin[2])),
        ];
        const enc = srgbTransfer.encode(cs);
        const i = (py * RES + px) * 4;
        data[i]     = Math.round(enc[0] * 255);
        data[i + 1] = Math.round(enc[1] * 255);
        data[i + 2] = Math.round(enc[2] * 255);
        data[i + 3] = 255;
      }
    }
    tmpCtx.putImageData(imgData, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(tmp, 0, 0, w, h);

    // ─── Spectral locus outline ────────────────────────────────────────────
    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    SPECTRAL_LOCUS.forEach(([_nm, x, y], i) => {
      const px = xToPx(x, w);
      const py = yToPx(y, h);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    });
    // Close with the line of purples
    ctx.closePath();
    ctx.stroke();

    // ─── Gamut triangles ───────────────────────────────────────────────────
    for (const key of showList) {
      const { tri, color, name } = GAMUTS[key];
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      tri.forEach(([x, y], i) => {
        const px = xToPx(x, w);
        const py = yToPx(y, h);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      });
      ctx.closePath();
      ctx.stroke();
      // Label at first vertex
      ctx.fillStyle = color;
      ctx.font = '11px ui-monospace, monospace';
      const lx = xToPx(tri[0][0], w);
      const ly = yToPx(tri[0][1], h);
      ctx.fillText(name, lx + 6, ly - 4);
    }

    // ─── White points ──────────────────────────────────────────────────────
    for (const wp of WHITE_POINTS) {
      const px = xToPx(wp.x, w);
      const py = yToPx(wp.y, h);
      ctx.beginPath();
      ctx.arc(px, py, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = '#fff';
      ctx.fill();
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = '#fff';
      ctx.font = '10px ui-monospace, monospace';
      ctx.fillText(wp.name, px + 6, py + 4);
    }

    // ─── Wavelength tick labels (sparse) ───────────────────────────────────
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    ctx.font = '9px ui-monospace, monospace';
    const WL_TICKS = [400, 470, 480, 490, 500, 520, 540, 560, 580, 600, 620, 700];
    for (const nm of WL_TICKS) {
      const sp = SPECTRAL_LOCUS.find(p => p[0] === nm);
      if (!sp) continue;
      const px = xToPx(sp[1], w);
      const py = yToPx(sp[2], h);
      ctx.fillText(String(nm), px + 4, py - 2);
    }

    // ─── Axes labels ───────────────────────────────────────────────────────
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#999';
    ctx.font = '11px ui-monospace, monospace';
    ctx.fillText('x', w - 12, h - 6);
    ctx.fillText('y', 6, 14);

    // ─── Pick marker ──────────────────────────────────────────────────────
    const pick = this.getAttribute('pick');
    if (pick) {
      const parts = pick.split(',').map(Number);
      const px = xToPx(parts[0], w);
      const py = yToPx(parts[1], h);
      ctx.beginPath();
      ctx.arc(px, py, 7, 0, Math.PI * 2);
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }
}

function pointInPolygon(x, y, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1];
    const xj = poly[j][0], yj = poly[j][1];
    const intersect = ((yi > y) !== (yj > y))
      && (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}

customElements.define('chromaticity-diagram', ChromaticityDiagram);
