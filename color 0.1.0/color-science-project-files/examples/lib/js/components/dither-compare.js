// <dither-compare k="8"></dither-compare>
//
// Quantize an image to a k-color palette via k-means in OKLab, then show three
// views: the palette, the nearest-neighbor quantization (no dithering), and
// the same palette with Floyd-Steinberg error diffusion.
//
// API:
//   .setImage(htmlImage)
//
// Attribute:
//   k — palette size (default 8)

import { setupCanvas, toHex } from '../utils.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { quantize } from '../../dist/quantize/kmeans.js';
import { ditherFloydSteinberg } from '../../dist/dithering/floyd-steinberg.js';

function oklabToHexBytes(lab) {
  const xyz = oklab.toXYZ(lab);
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

class DitherCompare extends HTMLElement {
  static get observedAttributes() { return ['k']; }

  connectedCallback() {
    this._mount();
  }

  attributeChangedCallback() {
    if (this._source) this.run();
  }

  _mount() {
    this.innerHTML = `<div class="dither-host">
      <div class="dither-grid">
        <div class="dither-cell">
          <h4>Palette (${this.getAttribute('k') || 8} colors)</h4>
          <div class="dither-palette" id="dp-palette"></div>
        </div>
        <div class="dither-cell">
          <h4>Nearest-neighbor (no dither)</h4>
          <canvas class="dither-canvas" id="dp-nn"></canvas>
        </div>
        <div class="dither-cell">
          <h4>Floyd-Steinberg (error-diffused)</h4>
          <canvas class="dither-canvas" id="dp-fs"></canvas>
        </div>
      </div>
      <p class="dither-status" style="color:var(--text-muted);font-size:var(--text-sm);">Drop an image to begin.</p>
    </div>`;
    this._paletteEl = this.querySelector('#dp-palette');
    this._nnCanvas = this.querySelector('#dp-nn');
    this._fsCanvas = this.querySelector('#dp-fs');
    this._status = this.querySelector('.dither-status');
  }

  setImage(image) {
    if (!this._paletteEl) this._mount();
    // Aggressively downsample so dithering completes in <2s for typical photos.
    const scale = Math.min(1, 320 / Math.max(image.naturalWidth, image.naturalHeight));
    const W = Math.round(image.naturalWidth * scale);
    const H = Math.round(image.naturalHeight * scale);
    const work = document.createElement('canvas');
    work.width = W; work.height = H;
    work.getContext('2d').drawImage(image, 0, 0, W, H);
    this._source = work.getContext('2d').getImageData(0, 0, W, H);
    this._sourceWidth = W;
    this._sourceHeight = H;
    this.run();
  }

  run() {
    if (!this._source) return;
    const k = Math.max(2, Math.min(32, parseInt(this.getAttribute('k') || '8', 10)));
    const W = this._sourceWidth, H = this._sourceHeight;
    const data = this._source.data;
    this._status.textContent = 'Quantizing…';

    // Defer so the status updates before the heavy work.
    requestAnimationFrame(() => {
      const t = performance.now();
      // Convert pixels to OKLab.
      const pixels = [];
      const grid = [];
      for (let y = 0; y < H; y++) {
        const row = [];
        for (let x = 0; x < W; x++) {
          const i = (y * W + x) * 4;
          const r = data[i] / 255, g = data[i+1] / 255, b = data[i+2] / 255;
          const lin = srgbTransfer.decode([r, g, b]);
          const xyz = srgb.toXYZ(lin);
          const lab = oklab.fromXYZ(xyz);
          pixels.push(lab);
          row.push(lab);
        }
        grid.push(row);
      }

      // K-means palette.
      const { palette } = quantize(pixels, { k, seed: 42 });
      this._renderPalette(palette);

      // Nearest-neighbor (no dither) — equivalent to mapping each pixel to
      // its closest palette member.
      this._renderQuantized(grid, palette, this._nnCanvas, /* dither */ false);
      // Floyd-Steinberg.
      this._renderQuantized(grid, palette, this._fsCanvas, /* dither */ true);

      const elapsed = (performance.now() - t).toFixed(0);
      this._status.textContent = `${k} colors, ${W}×${H} samples — ${elapsed}ms total`;
    });
  }

  _renderPalette(palette) {
    const k = this.getAttribute('k') || 8;
    const swatches = palette.map(lab => {
      const rgb = oklabToHexBytes(lab);
      const hex = '#' + rgb.map(v => v.toString(16).padStart(2, '0')).join('');
      return `<div class="dither-swatch" style="background:${hex}" title="${hex}"></div>`;
    }).join('');
    this._paletteEl.innerHTML = swatches;
    this.querySelector('#dp-palette').previousElementSibling.textContent = `Palette (${palette.length} colors)`;
  }

  _renderQuantized(grid, palette, canvas, useDither) {
    const H = grid.length, W = grid[0].length;
    const wCss = Math.min(this.offsetWidth || 400, 480);
    const hCss = Math.round(wCss * H / W);
    const { ctx, w, h } = setupCanvas(canvas, wCss, hCss);

    let outIndices;
    if (useDither) {
      const { indices } = ditherFloydSteinberg(grid, palette);
      outIndices = indices;
    } else {
      outIndices = grid.map(row => row.map(c => {
        // Nearest palette
        let best = 0, bestDist = Infinity;
        for (let i = 0; i < palette.length; i++) {
          const dL = c[0] - palette[i][0];
          const dA = c[1] - palette[i][1];
          const dB = c[2] - palette[i][2];
          const d = dL*dL + dA*dA + dB*dB;
          if (d < bestDist) { bestDist = d; best = i; }
        }
        return best;
      }));
    }

    // Build a temp canvas at W × H, fill with palette bytes, drawImage-upscale.
    const tmp = document.createElement('canvas');
    tmp.width = W; tmp.height = H;
    const imgData = tmp.getContext('2d').createImageData(W, H);
    const data = imgData.data;
    const paletteBytes = palette.map(oklabToHexBytes);
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const idx = outIndices[y][x];
        const rgb = paletteBytes[idx];
        const i = (y * W + x) * 4;
        data[i]     = rgb[0];
        data[i + 1] = rgb[1];
        data[i + 2] = rgb[2];
        data[i + 3] = 255;
      }
    }
    tmp.getContext('2d').putImageData(imgData, 0, 0);
    ctx.imageSmoothingEnabled = false; // preserve pixel-level dither pattern
    ctx.drawImage(tmp, 0, 0, w, h);
  }
}

customElements.define('dither-compare', DitherCompare);
