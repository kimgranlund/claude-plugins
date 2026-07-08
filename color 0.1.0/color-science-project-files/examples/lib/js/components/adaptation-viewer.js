// <adaptation-viewer src-white="D65" dst-white="A"></adaptation-viewer>
//
// Display an image as it would appear under a different illuminant via
// Bradford chromatic adaptation. Simulates: take the scene's reflected XYZ
// (assumed captured under src-white), re-render under dst-white assuming the
// viewer is adapted to src-white. The result shows "if the lighting changed
// from D65 to {A, F2, D50} but my eyes didn't adapt, what would I see?"
//
// API:
//   .setImage(htmlImage)
//
// Attributes:
//   src-white — "D65" | "D50" | "A" | "F2"
//   dst-white — same options
//   mode      — "split" | "single"

import { setupCanvas } from '../utils.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { bradfordMatrix, D65, D50, A, F2 } from '../../dist/adaptation/bradford.js';
import { mulMat3Vec3 } from '../../dist/types.js';

const WHITES = { D65, D50, A, F2 };
const LABELS = {
  D65: 'D65 (daylight ~6500K)',
  D50: 'D50 (warm daylight ~5000K)',
  A:   'A (tungsten ~2856K)',
  F2:  'F2 (cool white fluorescent)',
};

class AdaptationViewer extends HTMLElement {
  static get observedAttributes() { return ['src-white', 'dst-white', 'mode']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() {
    if (this._canvas && this._sourceData) this.render();
  }

  _mount() {
    this.innerHTML = `<div class="adapt-host">
      <canvas></canvas>
      <p class="adapt-empty" style="color:var(--text-muted);font-size:var(--text-sm);">Drop or pick an image to start.</p>
    </div>`;
    this._canvas = this.querySelector('canvas');
    this._empty = this.querySelector('.adapt-empty');
  }

  setImage(image) {
    const work = document.createElement('canvas');
    work.width = image.naturalWidth || image.width;
    work.height = image.naturalHeight || image.height;
    work.getContext('2d').drawImage(image, 0, 0);
    this._sourceData = work.getContext('2d').getImageData(0, 0, work.width, work.height);
    this._sourceWidth = work.width;
    this._sourceHeight = work.height;
    if (this._empty) this._empty.style.display = 'none';
    this.render();
  }

  render() {
    if (!this._canvas || !this._sourceData) return;
    const srcKey = this.getAttribute('src-white') || 'D65';
    const dstKey = this.getAttribute('dst-white') || 'A';
    const mode = this.getAttribute('mode') || 'split';
    const srcW = WHITES[srcKey] || D65;
    const dstW = WHITES[dstKey] || A;
    const M = bradfordMatrix(srcW, dstW);

    const sW = this._sourceWidth, sH = this._sourceHeight;
    const src = this._sourceData.data;
    const adapted = new ImageData(sW, sH);
    const dst = adapted.data;
    for (let i = 0; i < src.length; i += 4) {
      const r = src[i] / 255, g = src[i+1] / 255, b = src[i+2] / 255;
      const lin = srgbTransfer.decode([r, g, b]);
      const xyz = srgb.toXYZ(lin);
      const adaptedXyz = mulMat3Vec3(M, xyz);
      const linOut = srgb.fromXYZ(adaptedXyz);
      const cs = [
        Math.max(0, Math.min(1, linOut[0])),
        Math.max(0, Math.min(1, linOut[1])),
        Math.max(0, Math.min(1, linOut[2])),
      ];
      const enc = srgbTransfer.encode(cs);
      dst[i]     = Math.round(enc[0] * 255);
      dst[i + 1] = Math.round(enc[1] * 255);
      dst[i + 2] = Math.round(enc[2] * 255);
      dst[i + 3] = src[i + 3];
    }

    const targetW = Math.min(900, this.offsetWidth || 900);
    const aspect = sH / sW;
    let canvW, canvH, drawW;
    if (mode === 'split') {
      drawW = targetW / 2;
      canvW = targetW;
      canvH = drawW * aspect;
    } else {
      drawW = targetW;
      canvW = targetW;
      canvH = canvW * aspect;
    }
    const { ctx, w, h } = setupCanvas(this._canvas, canvW, canvH);

    const origCv = document.createElement('canvas');
    origCv.width = sW; origCv.height = sH;
    origCv.getContext('2d').putImageData(this._sourceData, 0, 0);
    const adaptCv = document.createElement('canvas');
    adaptCv.width = sW; adaptCv.height = sH;
    adaptCv.getContext('2d').putImageData(adapted, 0, 0);

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    if (mode === 'split') {
      ctx.drawImage(origCv, 0, 0, drawW, h);
      ctx.drawImage(adaptCv, drawW, 0, drawW, h);
      ctx.strokeStyle = 'rgba(255,255,255,0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(drawW, 0); ctx.lineTo(drawW, h); ctx.stroke();
      ctx.fillStyle = 'rgba(0,0,0,0.65)';
      ctx.fillRect(4, 4, 200, 20);
      ctx.fillRect(drawW + 4, 4, 240, 20);
      ctx.fillStyle = '#fff';
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('source · ' + LABELS[srcKey], 8, 19);
      ctx.fillText('adapted · ' + LABELS[dstKey], drawW + 8, 19);
    } else {
      ctx.drawImage(adaptCv, 0, 0, w, h);
    }
  }
}

customElements.define('adaptation-viewer', AdaptationViewer);
