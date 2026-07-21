// <okhsl-picker hue="264"></okhsl-picker>
//
// Renders side-by-side fixed-hue slices for OKHSL (Ottosson) and HSL. Each
// slice is a 2D grid of (saturation, lightness) ∈ [0,1]² at the chosen hue.
// In the OKHSL slice the lightness axis is perceptually uniform; in HSL it
// isn't. Compare the visible "brightness uniformity" along horizontal lines.

import { setupCanvas, toHex } from '../utils.js';
import * as okhsl from '../../dist/spaces/okhsl.js';
import * as hsl from '../../dist/spaces/hsl.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

const RES_CAP = 800;

function spaceSliceToRgb(spaceFn, h, s, l) {
  const xyz = spaceFn([h, s, l]);
  const lin = srgb.fromXYZ(xyz);
  const cs = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(cs);
  return [
    Math.round(enc[0] * 255),
    Math.round(enc[1] * 255),
    Math.round(enc[2] * 255),
  ];
}

function renderSlice(canvas, hueDeg, mode, label) {
  const wCss = Math.min(canvas.offsetWidth || 280, 320);
  const hCss = wCss;
  const { ctx, w, h } = setupCanvas(canvas, wCss, hCss);

  // Sample at 1× DPR (matching the canvas buffer) for crisp output.
  const dpr = window.devicePixelRatio || 1;
  const RES = Math.min(Math.round(w * dpr), RES_CAP);
  const tmp = document.createElement('canvas');
  tmp.width = RES; tmp.height = RES;
  const imgData = tmp.getContext('2d').createImageData(RES, RES);
  const data = imgData.data;

  for (let py = 0; py < RES; py++) {
    for (let px = 0; px < RES; px++) {
      const s = px / (RES - 1);
      const lVal = 1 - py / (RES - 1);
      const rgb = mode === 'okhsl'
        ? spaceSliceToRgb(okhsl.toXYZ, hueDeg, s, lVal)
        : spaceSliceToRgb(hsl.toXYZ, hueDeg, s, lVal);
      const i = (py * RES + px) * 4;
      data[i]     = rgb[0];
      data[i + 1] = rgb[1];
      data[i + 2] = rgb[2];
      data[i + 3] = 255;
    }
  }
  tmp.getContext('2d').putImageData(imgData, 0, 0);
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(tmp, 0, 0, w, h);

  // Labels
  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.font = '11px ui-monospace, monospace';
  ctx.fillText(label, 6, 14);
  ctx.fillText('s →', w - 28, h - 6);
  ctx.fillText('l ↑', 4, h - 6);
}

class OkhslPicker extends HTMLElement {
  static get observedAttributes() { return ['hue']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._okCanvas) this.render(); }

  _mount() {
    this.innerHTML = `<div class="okhsl-host">
      <div class="okhsl-grid">
        <div class="okhsl-cell">
          <h4>OKHSL (Ottosson 2021)</h4>
          <canvas class="okhsl-canvas okhsl-ok"></canvas>
        </div>
        <div class="okhsl-cell">
          <h4>HSL (CSS / RGB-cylindrical)</h4>
          <canvas class="okhsl-canvas okhsl-hsl"></canvas>
        </div>
      </div>
    </div>`;
    this._okCanvas = this.querySelector('.okhsl-ok');
    this._hslCanvas = this.querySelector('.okhsl-hsl');
  }

  render() {
    const hueDeg = parseFloat(this.getAttribute('hue') ?? '264');
    renderSlice(this._okCanvas, hueDeg, 'okhsl', 'OKHSL slice');
    renderSlice(this._hslCanvas, hueDeg, 'hsl', 'HSL slice');
  }
}

customElements.define('okhsl-picker', OkhslPicker);
