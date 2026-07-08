// <cvd-simulator type="deuteranopia" severity="1.0"></cvd-simulator>
//
// Image filter that applies a Machado 2009 CVD matrix to an uploaded image.
// The matrix is built in linear sRGB then applied per-pixel. Render is split
// across canvas frames if needed (large images).
//
// API:
//   .setImage(htmlImage) — set source image; component re-renders.
//   Attributes:
//     type      — one of "protanopia" | "deuteranopia" | "tritanopia"
//     severity  — float in [0, 1]
//     mode      — "split" (default) shows original | simulated; "single" shows only simulated.

import { setupCanvas } from '../utils.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { simulationMatrix } from '../../dist/cvd/machado-2009.js';
import { mulMat3Vec3 } from '../../dist/types.js';

class CVDSimulator extends HTMLElement {
  static get observedAttributes() { return ['type', 'severity', 'mode']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() {
    if (this._canvas && this._sourceData) this.render();
  }

  _mount() {
    this.innerHTML = `
      <div class="cvd-host">
        <canvas></canvas>
        <p class="cvd-empty" style="color:var(--text-muted);font-size:var(--text-sm);">Drop or pick an image to see the simulation.</p>
      </div>`;
    this._canvas = this.querySelector('canvas');
    this._empty = this.querySelector('.cvd-empty');
  }

  setImage(image) {
    const work = document.createElement('canvas');
    work.width = image.naturalWidth || image.width;
    work.height = image.naturalHeight || image.height;
    const ctx = work.getContext('2d');
    ctx.drawImage(image, 0, 0);
    this._sourceData = ctx.getImageData(0, 0, work.width, work.height);
    this._sourceWidth = work.width;
    this._sourceHeight = work.height;
    if (this._empty) this._empty.style.display = 'none';
    this.render();
  }

  render() {
    if (!this._canvas || !this._sourceData) return;
    const type = (this.getAttribute('type') || 'deuteranopia');
    const severity = parseFloat(this.getAttribute('severity') ?? '1') || 0;
    const mode = (this.getAttribute('mode') || 'split');

    const srcW = this._sourceWidth, srcH = this._sourceHeight;
    const M = simulationMatrix(type, severity);

    // Build simulated image data (modify a fresh copy of source).
    const simData = new ImageData(srcW, srcH);
    const src = this._sourceData.data;
    const dst = simData.data;
    for (let i = 0; i < src.length; i += 4) {
      // encoded sRGB → linear sRGB → CVD matrix → encoded sRGB
      const r = src[i] / 255, g = src[i + 1] / 255, b = src[i + 2] / 255;
      const lin = srgbTransfer.decode([r, g, b]);
      const sim = mulMat3Vec3(M, lin);
      const cs = [
        Math.max(0, Math.min(1, sim[0])),
        Math.max(0, Math.min(1, sim[1])),
        Math.max(0, Math.min(1, sim[2])),
      ];
      const enc = srgbTransfer.encode(cs);
      dst[i]     = Math.round(enc[0] * 255);
      dst[i + 1] = Math.round(enc[1] * 255);
      dst[i + 2] = Math.round(enc[2] * 255);
      dst[i + 3] = src[i + 3];
    }

    // Lay out canvas. Split mode: original | simulated. Single: simulated only.
    const targetW = Math.min(900, this.offsetWidth || 900);
    const aspect = srcH / srcW;
    let canvW, canvH, drawW;
    if (mode === 'split') {
      drawW = targetW / 2;
      canvW = targetW;
      canvH = drawW * aspect;
    } else {
      drawW = targetW;
      canvW = targetW;
      canvH = targetW * aspect;
    }
    const { ctx, w, h } = setupCanvas(this._canvas, canvW, canvH);

    // Draw via off-screen canvases (lets us scale the imageData correctly).
    const origCv = document.createElement('canvas');
    origCv.width = srcW; origCv.height = srcH;
    origCv.getContext('2d').putImageData(this._sourceData, 0, 0);

    const simCv = document.createElement('canvas');
    simCv.width = srcW; simCv.height = srcH;
    simCv.getContext('2d').putImageData(simData, 0, 0);

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    if (mode === 'split') {
      ctx.drawImage(origCv, 0, 0, drawW, h);
      ctx.drawImage(simCv,  drawW, 0, drawW, h);
      // Divider + labels
      ctx.strokeStyle = 'rgba(255,255,255,0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(drawW, 0); ctx.lineTo(drawW, h); ctx.stroke();
      ctx.fillStyle = 'rgba(0,0,0,0.6)';
      ctx.fillRect(4, 4, 78, 18);
      ctx.fillRect(drawW + 4, 4, 130, 18);
      ctx.fillStyle = '#fff';
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('original', 8, 17);
      ctx.fillText(`${type} ${Math.round(severity * 100)}%`, drawW + 8, 17);
    } else {
      ctx.drawImage(simCv, 0, 0, w, h);
    }
  }
}

customElements.define('cvd-simulator', CVDSimulator);
