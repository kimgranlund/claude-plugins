// <tonemap-strip exposure="1.0" white-point="4.0"></tonemap-strip>
//
// Render five tone-mapping operators on the same synthetic HDR gradient
// (linear 0..maxStop, where maxStop > 1 = highlights to be compressed).
//
// Operators rendered top to bottom:
//   1. naive clip — anything > 1 becomes 1.0 (the "blown" result)
//   2. Reinhard simple — y = x / (1+x)
//   3. Reinhard extended (W = whitePoint)
//   4. Reinhard luminance-preserving (W = whitePoint)
//   5. ACES Narkowicz

import { setupCanvas, toHexByte } from '../utils.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { reinhardSimple, applySimple, applyExtended, applyLuminancePreserving } from '../../dist/tonemap/reinhard.js';
import { acesNarkowicz, applyACES } from '../../dist/tonemap/aces.js';

const OPS = [
  {
    id: 'clip',     label: 'naive clip',                    note: 'min(x, 1) per channel',
    apply: function (rgb) {
      return [Math.min(1, rgb[0]), Math.min(1, rgb[1]), Math.min(1, rgb[2])];
    },
  },
  {
    id: 'reinSimple', label: 'Reinhard simple',             note: 'x/(1+x); asymptotic, never reaches 1',
    apply: function (rgb) { return applySimple(rgb); },
  },
  {
    id: 'reinExt',  label: 'Reinhard extended (W=whitePt)', note: 'maps whitePoint exactly to 1.0',
    apply: function (rgb, wp) { return applyExtended(rgb, wp); },
  },
  {
    id: 'reinLum',  label: 'Reinhard luminance-preserving', note: 'compress Y only; keep RGB ratios',
    apply: function (rgb, wp) { return applyLuminancePreserving(rgb, wp); },
  },
  {
    id: 'aces',     label: 'ACES (Narkowicz fit)',          note: 'filmic toe + highlight roll-off',
    apply: function (rgb) { return applyACES(rgb); },
  },
];

class TonemapStrip extends HTMLElement {
  static get observedAttributes() { return ['exposure', 'white-point', 'max-stop']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="tonemap-host"></div>`;
    this._root = this.querySelector('.tonemap-host');
  }

  render() {
    const exposure = parseFloat(this.getAttribute('exposure') ?? '1');
    const whitePoint = parseFloat(this.getAttribute('white-point') ?? '4');
    const maxStop = parseFloat(this.getAttribute('max-stop') ?? '8');

    this._root.innerHTML = OPS.map(op => `
      <div class="tonemap-row">
        <div class="tonemap-label">
          <strong>${op.label}</strong>
          <div class="tonemap-note">${op.note}</div>
        </div>
        <canvas data-op="${op.id}" class="tonemap-canvas"></canvas>
      </div>
    `).join('');

    const canvases = this._root.querySelectorAll('canvas[data-op]');
    canvases.forEach(canv => {
      const op = OPS.find(o => o.id === canv.dataset.op);
      const wCss = Math.min(this.offsetWidth || 600, 720) - 200;
      const hCss = 48;
      const { ctx, w, h } = setupCanvas(canv, wCss, hCss);

      // Build a synthetic HDR gradient (linear, ranges 0..maxStop in lum,
      // mostly neutral so the operator's effect on the highlights is clear).
      const imgData = ctx.createImageData(Math.round(w), Math.round(h));
      const data = imgData.data;
      // We render onto a 1×W gradient then stretch vertically.
      const cols = Math.round(w);
      const rgbStrip = [];
      for (let i = 0; i < cols; i++) {
        const t = i / (cols - 1);
        const linVal = t * maxStop * exposure;
        rgbStrip.push([linVal, linVal, linVal]);
      }
      const mapped = rgbStrip.map(rgb => op.apply(rgb, whitePoint));
      for (let py = 0; py < Math.round(h); py++) {
        for (let px = 0; px < cols; px++) {
          const m = mapped[px];
          const cs = [
            Math.max(0, Math.min(1, m[0])),
            Math.max(0, Math.min(1, m[1])),
            Math.max(0, Math.min(1, m[2])),
          ];
          const enc = srgbTransfer.encode(cs);
          const i = (py * cols + px) * 4;
          data[i]     = Math.round(enc[0] * 255);
          data[i + 1] = Math.round(enc[1] * 255);
          data[i + 2] = Math.round(enc[2] * 255);
          data[i + 3] = 255;
        }
      }
      // putImageData writes raw pixels (ignores transform); we built imgData
      // at the buffer's CSS size — but the buffer was DPR-scaled by setupCanvas.
      // Use a temp canvas + drawImage to upscale correctly.
      const tmp = document.createElement('canvas');
      tmp.width = cols; tmp.height = Math.round(h);
      tmp.getContext('2d').putImageData(imgData, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(tmp, 0, 0, w, h);
    });
  }
}

customElements.define('tonemap-strip', TonemapStrip);
