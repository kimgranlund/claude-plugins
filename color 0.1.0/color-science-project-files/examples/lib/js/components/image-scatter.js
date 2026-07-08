// <image-scatter></image-scatter>
//
// Plot every (downsampled) pixel of an image as a dot on the CIE xy
// chromaticity diagram. Each dot is rendered in its actual pixel color.
// You see the "color shape" of the image — narrow palette photos cluster
// tightly; saturated photos spread out toward the spectral locus.

import { setupCanvas } from '../utils.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as xyy from '../../dist/spaces/xyy.js';

const SPECTRAL_LOCUS = [
  [0.1741, 0.0050], [0.1738, 0.0049], [0.1733, 0.0048], [0.1726, 0.0048],
  [0.1714, 0.0051], [0.1689, 0.0069], [0.1644, 0.0109], [0.1566, 0.0177],
  [0.1440, 0.0297], [0.1241, 0.0578], [0.0913, 0.1327], [0.0454, 0.2950],
  [0.0082, 0.5384], [0.0139, 0.7502], [0.0743, 0.8338], [0.1547, 0.8059],
  [0.2296, 0.7543], [0.3016, 0.6923], [0.3731, 0.6245], [0.4441, 0.5547],
  [0.5125, 0.4866], [0.5752, 0.4242], [0.6270, 0.3725], [0.6658, 0.3340],
  [0.6915, 0.3083], [0.7079, 0.2920], [0.7190, 0.2809], [0.7260, 0.2740],
  [0.7300, 0.2700], [0.7320, 0.2680], [0.7334, 0.2666], [0.7344, 0.2656],
  [0.7347, 0.2653],
];

const SRGB_TRI    = [[0.6400, 0.3300], [0.3000, 0.6000], [0.1500, 0.0600]];
const P3_TRI      = [[0.6800, 0.3200], [0.2650, 0.6900], [0.1500, 0.0600]];
const REC2020_TRI = [[0.7080, 0.2920], [0.1700, 0.7970], [0.1310, 0.0460]];

const X_RANGE = [0, 0.8];
const Y_RANGE = [0, 0.9];

class ImageScatter extends HTMLElement {
  connectedCallback() {
    this._mount();
  }

  _mount() {
    this.innerHTML = `<div class="scatter-host">
      <canvas class="scatter-canvas"></canvas>
      <div class="scatter-readout" style="color:var(--text-muted);font-size:var(--text-sm);"></div>
    </div>`;
    this._canvas = this.querySelector('.scatter-canvas');
    this._readout = this.querySelector('.scatter-readout');
  }

  setImage(image) {
    if (!this._canvas) this._mount();
    const SAMPLE_TARGET = 160; // downsample to ~160 px max dim
    const scale = Math.min(1, SAMPLE_TARGET / Math.max(image.naturalWidth, image.naturalHeight));
    const W = Math.round(image.naturalWidth * scale);
    const H = Math.round(image.naturalHeight * scale);
    const tmp = document.createElement('canvas');
    tmp.width = W; tmp.height = H;
    tmp.getContext('2d').drawImage(image, 0, 0, W, H);
    const data = tmp.getContext('2d').getImageData(0, 0, W, H).data;
    this._render(data, W, H);
  }

  _render(data, W, H) {
    const wCss = Math.min(this.offsetWidth || 640, 760);
    const hCss = Math.round(wCss * (Y_RANGE[1] / X_RANGE[1]));
    const { ctx, w, h } = setupCanvas(this._canvas, wCss, hCss);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);
    const X = (xv) => ((xv - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])) * w;
    const Y = (yv) => h - ((yv - Y_RANGE[0]) / (Y_RANGE[1] - Y_RANGE[0])) * h;

    // Spectral locus
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    SPECTRAL_LOCUS.forEach(([x, y], i) => {
      const px = X(x), py = Y(y);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    });
    ctx.closePath(); ctx.stroke();

    // Gamut triangles
    [
      { tri: REC2020_TRI, color: 'oklch(0.70 0.18 50 / 0.7)', label: 'Rec.2020' },
      { tri: P3_TRI,      color: 'oklch(0.62 0.18 150 / 0.8)', label: 'P3' },
      { tri: SRGB_TRI,    color: 'oklch(0.55 0.18 264 / 0.9)', label: 'sRGB' },
    ].forEach(({ tri, color, label }) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      tri.forEach(([x, y], i) => {
        const px = X(x), py = Y(y);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      });
      ctx.closePath(); ctx.stroke();
    });

    // Plot pixels
    let plotted = 0;
    let inSrgb = 0, inP3 = 0, inRec2020 = 0;
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i] / 255, g = data[i+1] / 255, b = data[i+2] / 255;
      const lin = srgbTransfer.decode([r, g, b]);
      const xyz = srgb.toXYZ(lin);
      const sum = xyz[0] + xyz[1] + xyz[2];
      if (sum < 1e-6) continue;
      const xc = xyz[0] / sum, yc = xyz[1] / sum;
      const px = X(xc), py = Y(yc);
      if (px < 0 || px > w || py < 0 || py > h) continue;
      const hexR = data[i], hexG = data[i+1], hexB = data[i+2];
      // Use point-in-triangle to count rough gamut membership.
      // (For the original sRGB image every pixel is in sRGB by construction;
      // the meaningful comparison is with the wider gamuts via the canvas test.)
      ctx.fillStyle = 'rgba(' + hexR + ',' + hexG + ',' + hexB + ',0.7)';
      ctx.fillRect(px - 1, py - 1, 2, 2);
      plotted++;
    }
    this._readout.innerHTML = '<strong>' + plotted + '</strong> pixels plotted on the CIE 1931 xy diagram.';
  }
}

customElements.define('image-scatter', ImageScatter);
