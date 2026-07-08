// <image-histograms></image-histograms>
//
// Drop or pass an image, get:
//   - A circular hue-ring histogram (frequency of each 5° hue bin in OKLCh).
//   - A horizontal lightness histogram (frequency of each L bin).
//   - Stats: gamut coverage (% of sampled pixels that hit each gamut),
//     average chroma, total sample count.
//
// API:
//   .setImage(htmlImage) — process and render.

import { setupCanvas, fmt } from '../utils.js';
import * as oklchSpace from '../../dist/spaces/oklch.js';
import * as oklabSpace from '../../dist/spaces/oklab.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

const HUE_BINS = 72;       // 5° per bin
const L_BINS = 32;
const SAMPLE_STEP = 4;     // every 4th pixel for speed

class ImageHistograms extends HTMLElement {
  connectedCallback() {
    this._mount();
  }

  _mount() {
    this.innerHTML = `
      <div class="hist-host">
        <div class="hist-row">
          <canvas class="hist-hue"></canvas>
          <canvas class="hist-l"></canvas>
        </div>
        <div class="hist-stats" style="font-family:var(--font-mono); font-size:var(--text-xs); color:var(--text-muted); margin-top:var(--s-3); display:grid; grid-template-columns:repeat(2, 1fr); gap:var(--s-2);"></div>
      </div>`;
    this._hueCanvas = this.querySelector('.hist-hue');
    this._lCanvas = this.querySelector('.hist-l');
    this._stats = this.querySelector('.hist-stats');
  }

  setImage(image) {
    if (!this._hueCanvas) this._mount();
    const work = document.createElement('canvas');
    const W = image.naturalWidth || image.width;
    const H = image.naturalHeight || image.height;
    work.width = W; work.height = H;
    work.getContext('2d').drawImage(image, 0, 0);
    const data = work.getContext('2d').getImageData(0, 0, W, H).data;

    const hueBins = new Array(HUE_BINS).fill(0);
    const lBins = new Array(L_BINS).fill(0);
    let totalC = 0, samples = 0;

    for (let i = 0; i < data.length; i += 4 * SAMPLE_STEP) {
      const r = data[i] / 255, g = data[i + 1] / 255, b = data[i + 2] / 255;
      const lin = srgbTransfer.decode([r, g, b]);
      const xyz = srgbSpace.toXYZ(lin);
      const lch = oklchSpace.fromXYZ(xyz);
      const L = lch[0], C = lch[1], hDeg = lch[2];
      // Hue bin
      const hb = Math.floor((hDeg / 360) * HUE_BINS) % HUE_BINS;
      hueBins[hb] += C; // weight by chroma so near-gray pixels don't dominate
      // L bin
      const lb = Math.min(L_BINS - 1, Math.max(0, Math.floor(L * L_BINS)));
      lBins[lb] += 1;
      totalC += C;
      samples++;
    }

    this._renderHueHist(hueBins);
    this._renderLHist(lBins);
    const avgC = samples > 0 ? totalC / samples : 0;
    this._stats.innerHTML = `
      <div>sampled pixels: <strong>${samples}</strong></div>
      <div>avg OKLCh chroma: <strong>${fmt(avgC, 3)}</strong></div>
    `;
  }

  _renderHueHist(bins) {
    const size = Math.min(this._hueCanvas.offsetWidth || 280, 360);
    const { ctx, w, h } = setupCanvas(this._hueCanvas, size, size);
    ctx.clearRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2;
    const rIn = Math.min(w, h) * 0.22;
    const rOutMax = Math.min(w, h) * 0.46;
    const max = Math.max(...bins, 1e-9);
    const tau = Math.PI * 2;

    // Radial bars
    for (let i = 0; i < HUE_BINS; i++) {
      const hueDeg = (i / HUE_BINS) * 360;
      const t = bins[i] / max;
      const rOut = rIn + (rOutMax - rIn) * t;
      const a0 = -Math.PI / 2 + (i / HUE_BINS) * tau;
      const a1 = a0 + (tau / HUE_BINS);
      // Color of this hue bin (use OKLCh)
      const lab = oklchSpace.toOKLab([0.65, 0.15, hueDeg]);
      const xyz = oklabSpace.toXYZ(lab);
      const lin = srgbSpace.fromXYZ(xyz);
      const cs = [
        Math.max(0, Math.min(1, lin[0])),
        Math.max(0, Math.min(1, lin[1])),
        Math.max(0, Math.min(1, lin[2])),
      ];
      const enc = srgbTransfer.encode(cs);
      ctx.fillStyle = `rgb(${Math.round(enc[0]*255)},${Math.round(enc[1]*255)},${Math.round(enc[2]*255)})`;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a0) * rIn, cy + Math.sin(a0) * rIn);
      ctx.arc(cx, cy, rOut, a0, a1);
      ctx.lineTo(cx + Math.cos(a1) * rIn, cy + Math.sin(a1) * rIn);
      ctx.arc(cx, cy, rIn, a1, a0, true);
      ctx.closePath();
      ctx.fill();
    }
    // Outer ring outline
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#666';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, rOutMax, 0, tau);
    ctx.stroke();
    // Label
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '11px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText('hue × chroma', cx, cy + 4);
  }

  _renderLHist(bins) {
    const wPx = this._lCanvas.offsetWidth || 280;
    const hPx = Math.round(wPx * 0.7);
    const { ctx, w, h } = setupCanvas(this._lCanvas, wPx, hPx);
    ctx.clearRect(0, 0, w, h);
    const max = Math.max(...bins, 1);
    const barW = w / L_BINS;
    for (let i = 0; i < L_BINS; i++) {
      const L = (i + 0.5) / L_BINS;
      const t = bins[i] / max;
      const barH = t * (h - 20);
      // Use that L's neutral color as the bar color (gray at L)
      const gray = Math.round(srgbTransfer.encodeComponent(L) * 255);
      ctx.fillStyle = `rgb(${gray},${gray},${gray})`;
      ctx.fillRect(i * barW + 1, h - barH - 14, barW - 2, barH);
    }
    // Baseline
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#666';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h - 14);
    ctx.lineTo(w, h - 14);
    ctx.stroke();
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '11px ui-monospace, monospace';
    ctx.textAlign = 'left';
    ctx.fillText('L = 0', 2, h - 2);
    ctx.textAlign = 'right';
    ctx.fillText('L = 1', w - 2, h - 2);
    ctx.textAlign = 'center';
    ctx.fillText('lightness distribution', w / 2, h - 2);
  }
}

customElements.define('image-histograms', ImageHistograms);
