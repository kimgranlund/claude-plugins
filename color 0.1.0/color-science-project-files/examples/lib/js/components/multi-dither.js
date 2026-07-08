// <multi-dither k="8"></multi-dither>
//
// Apply four dithering algorithms to the same image with the same palette,
// side-by-side: Floyd-Steinberg, Atkinson, Bayer 4×4 (ordered), Jarvis-
// Judice-Ninke. Quantization is in OKLab.
//
// API: .setImage(htmlImage)

import { setupCanvas } from '../utils.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { quantize } from '../../dist/quantize/kmeans.js';

function nearestIdx(point, palette) {
  let best = 0, bestDist = Infinity;
  for (let i = 0; i < palette.length; i++) {
    const dL = point[0] - palette[i][0];
    const dA = point[1] - palette[i][1];
    const dB = point[2] - palette[i][2];
    const d = dL*dL + dA*dA + dB*dB;
    if (d < bestDist) { bestDist = d; best = i; }
  }
  return best;
}

function ditherFS(source, palette) {
  const H = source.length, W = source[0].length;
  const buf = source.map(row => row.map(c => [c[0], c[1], c[2]]));
  const indices = [];
  for (let y = 0; y < H; y++) {
    const row = [];
    for (let x = 0; x < W; x++) {
      const idx = nearestIdx(buf[y][x], palette);
      row.push(idx);
      const errL = buf[y][x][0] - palette[idx][0];
      const errA = buf[y][x][1] - palette[idx][1];
      const errB = buf[y][x][2] - palette[idx][2];
      const diff = (yy, xx, weight) => {
        if (yy < 0 || yy >= H || xx < 0 || xx >= W) return;
        buf[yy][xx] = [buf[yy][xx][0] + errL * weight,
                       buf[yy][xx][1] + errA * weight,
                       buf[yy][xx][2] + errB * weight];
      };
      diff(y, x + 1,     7 / 16);
      diff(y + 1, x - 1, 3 / 16);
      diff(y + 1, x,     5 / 16);
      diff(y + 1, x + 1, 1 / 16);
    }
    indices.push(row);
  }
  return indices;
}

function ditherAtkinson(source, palette) {
  // Atkinson: 1/8 of error to each of 6 neighbors (only 6/8 of the error
  // is propagated — Atkinson's "lossy" diffusion).
  const H = source.length, W = source[0].length;
  const buf = source.map(row => row.map(c => [c[0], c[1], c[2]]));
  const indices = [];
  for (let y = 0; y < H; y++) {
    const row = [];
    for (let x = 0; x < W; x++) {
      const idx = nearestIdx(buf[y][x], palette);
      row.push(idx);
      const errL = (buf[y][x][0] - palette[idx][0]) / 8;
      const errA = (buf[y][x][1] - palette[idx][1]) / 8;
      const errB = (buf[y][x][2] - palette[idx][2]) / 8;
      const diff = (yy, xx) => {
        if (yy < 0 || yy >= H || xx < 0 || xx >= W) return;
        buf[yy][xx] = [buf[yy][xx][0] + errL,
                       buf[yy][xx][1] + errA,
                       buf[yy][xx][2] + errB];
      };
      diff(y, x + 1); diff(y, x + 2);
      diff(y + 1, x - 1); diff(y + 1, x); diff(y + 1, x + 1);
      diff(y + 2, x);
    }
    indices.push(row);
  }
  return indices;
}

function ditherJarvis(source, palette) {
  // Jarvis-Judice-Ninke: spreads error over 12 neighbors with weights /48.
  // Kernel:        *  7  5
  //         3 5 7 5 3
  //         1 3 5 3 1
  const H = source.length, W = source[0].length;
  const buf = source.map(row => row.map(c => [c[0], c[1], c[2]]));
  const indices = [];
  const W_TABLE = [
    [0, 1, 7], [0, 2, 5],
    [1, -2, 3], [1, -1, 5], [1, 0, 7], [1, 1, 5], [1, 2, 3],
    [2, -2, 1], [2, -1, 3], [2, 0, 5], [2, 1, 3], [2, 2, 1],
  ];
  for (let y = 0; y < H; y++) {
    const row = [];
    for (let x = 0; x < W; x++) {
      const idx = nearestIdx(buf[y][x], palette);
      row.push(idx);
      const errL = buf[y][x][0] - palette[idx][0];
      const errA = buf[y][x][1] - palette[idx][1];
      const errB = buf[y][x][2] - palette[idx][2];
      for (const [dy, dx, wgt] of W_TABLE) {
        const yy = y + dy, xx = x + dx;
        if (yy < 0 || yy >= H || xx < 0 || xx >= W) continue;
        const f = wgt / 48;
        buf[yy][xx] = [buf[yy][xx][0] + errL * f,
                       buf[yy][xx][1] + errA * f,
                       buf[yy][xx][2] + errB * f];
      }
    }
    indices.push(row);
  }
  return indices;
}

const BAYER_4 = [
  [ 0,  8,  2, 10],
  [12,  4, 14,  6],
  [ 3, 11,  1,  9],
  [15,  7, 13,  5],
];

function ditherBayer(source, palette) {
  // Ordered (Bayer) dithering: add a 16-level pattern matrix to each pixel
  // before nearest-palette assignment. The threshold matrix is normalized to
  // [-0.5/16, +0.5/16] of OKLab-space units; we tune the scale empirically.
  const H = source.length, W = source[0].length;
  const indices = [];
  const SCALE = 0.06; // empirically tuned for OKLab range
  for (let y = 0; y < H; y++) {
    const row = [];
    for (let x = 0; x < W; x++) {
      const m = BAYER_4[y % 4][x % 4];
      const off = (m / 16 - 0.5) * SCALE;
      const p = [source[y][x][0] + off, source[y][x][1] + off * 0.3, source[y][x][2] + off * 0.3];
      row.push(nearestIdx(p, palette));
    }
    indices.push(row);
  }
  return indices;
}

const ALGOS = [
  { id: 'fs',       name: 'Floyd-Steinberg',     fn: ditherFS },
  { id: 'atkinson', name: 'Atkinson',            fn: ditherAtkinson },
  { id: 'jarvis',   name: 'Jarvis-Judice-Ninke', fn: ditherJarvis },
  { id: 'bayer',    name: 'Bayer 4×4 ordered',   fn: ditherBayer },
];

function oklabToHexBytes(lab) {
  const xyz = oklab.toXYZ(lab);
  const lin = srgb.fromXYZ(xyz);
  const cs = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(cs);
  return [Math.round(enc[0] * 255), Math.round(enc[1] * 255), Math.round(enc[2] * 255)];
}

class MultiDither extends HTMLElement {
  static get observedAttributes() { return ['k']; }

  connectedCallback() {
    this._mount();
  }

  attributeChangedCallback() {
    if (this._source) this.run();
  }

  _mount() {
    this.innerHTML = `<div class="md-host">
      <div class="md-grid">${ALGOS.map(a => `
        <div class="md-cell">
          <h4>${a.name}</h4>
          <canvas data-algo="${a.id}" class="md-canvas"></canvas>
        </div>
      `).join('')}</div>
      <p class="md-status" style="color:var(--text-muted);font-size:var(--text-sm);">Drop an image to start.</p>
    </div>`;
    this._status = this.querySelector('.md-status');
  }

  setImage(image) {
    if (!this._status) this._mount();
    const scale = Math.min(1, 280 / Math.max(image.naturalWidth, image.naturalHeight));
    const W = Math.round(image.naturalWidth * scale);
    const H = Math.round(image.naturalHeight * scale);
    const tmp = document.createElement('canvas');
    tmp.width = W; tmp.height = H;
    tmp.getContext('2d').drawImage(image, 0, 0, W, H);
    this._source = tmp.getContext('2d').getImageData(0, 0, W, H);
    this._sw = W; this._sh = H;
    this.run();
  }

  run() {
    if (!this._source) return;
    const k = Math.max(2, Math.min(16, parseInt(this.getAttribute('k') || '8', 10)));
    this._status.textContent = 'Dithering…';
    requestAnimationFrame(() => {
      const t = performance.now();
      const W = this._sw, H = this._sh;
      const data = this._source.data;
      const grid = [];
      const pixels = [];
      for (let y = 0; y < H; y++) {
        const row = [];
        for (let x = 0; x < W; x++) {
          const i = (y * W + x) * 4;
          const r = data[i] / 255, g = data[i+1] / 255, b = data[i+2] / 255;
          const lin = srgbTransfer.decode([r, g, b]);
          const xyz = srgb.toXYZ(lin);
          const lab = oklab.fromXYZ(xyz);
          row.push(lab);
          pixels.push(lab);
        }
        grid.push(row);
      }
      const { palette } = quantize(pixels, { k, seed: 42 });
      const paletteBytes = palette.map(oklabToHexBytes);

      for (const algo of ALGOS) {
        const indices = algo.fn(grid, palette);
        const canv = this.querySelector('canvas[data-algo="' + algo.id + '"]');
        const wCss = Math.min(this.offsetWidth || 360, 380);
        const hCss = Math.round(wCss * H / W);
        const { ctx, w, h } = setupCanvas(canv, wCss, hCss);
        const tmpC = document.createElement('canvas');
        tmpC.width = W; tmpC.height = H;
        const imgData = tmpC.getContext('2d').createImageData(W, H);
        for (let y = 0; y < H; y++) {
          for (let x = 0; x < W; x++) {
            const idx = indices[y][x];
            const rgb = paletteBytes[idx];
            const i = (y * W + x) * 4;
            imgData.data[i]     = rgb[0];
            imgData.data[i + 1] = rgb[1];
            imgData.data[i + 2] = rgb[2];
            imgData.data[i + 3] = 255;
          }
        }
        tmpC.getContext('2d').putImageData(imgData, 0, 0);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(tmpC, 0, 0, w, h);
      }
      const elapsed = (performance.now() - t).toFixed(0);
      this._status.textContent = `${k} colors, ${W}×${H} samples — 4 algorithms in ${elapsed}ms`;
    });
  }
}

customElements.define('multi-dither', MultiDither);
