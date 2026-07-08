// <blend-through-white color="#0066ff"></blend-through-white>
//
// Ottosson's canonical OKLab visualization: blend a source color into white
// through 5 different spaces, side by side. The encoded-sRGB and HSL strips
// show the iconic "hue shift toward purple" bug for blue→white; OKLab keeps
// the hue stable.

import { setupCanvas, toHex } from '../utils.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as cielab from '../../dist/spaces/cielab.js';
import * as hsl from '../../dist/spaces/hsl.js';

const STOPS = 64;

function hexToEnc(hex) {
  return [
    parseInt(hex.slice(1, 3), 16) / 255,
    parseInt(hex.slice(3, 5), 16) / 255,
    parseInt(hex.slice(5, 7), 16) / 255,
  ];
}

function clipLin(lin) {
  return [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
}

function encToHexBytes(enc) {
  return [Math.round(enc[0] * 255), Math.round(enc[1] * 255), Math.round(enc[2] * 255)];
}

function lerp(a, b, t) { return a + (b - a) * t; }
function lerp3(A, B, t) { return [lerp(A[0], B[0], t), lerp(A[1], B[1], t), lerp(A[2], B[2], t)]; }

const SPACES = [
  {
    id: 'encoded', label: 'Encoded sRGB',
    note: 'naively averaging hex values — the classic muddy mid-tone bug.',
    interp: (src, t) => {
      const srcEnc = hexToEnc(src);
      const whEnc = [1, 1, 1];
      return lerp3(srcEnc, whEnc, t);
    },
  },
  {
    id: 'linear', label: 'Linear sRGB',
    note: 'gamma-correct linear interpolation. Mid-tones brighten, but hue can drift.',
    interp: (src, t) => {
      const srcLin = srgbTransfer.decode(hexToEnc(src));
      const whLin = [1, 1, 1];
      const mix = lerp3(srcLin, whLin, t);
      return srgbTransfer.encode(clipLin(mix));
    },
  },
  {
    id: 'oklab', label: 'OKLab',
    note: 'perceptually uniform — equal t looks like equal steps; hue stays stable.',
    interp: (src, t) => {
      const srcXyz = srgb.toXYZ(srgbTransfer.decode(hexToEnc(src)));
      const whXyz = srgb.toXYZ([1, 1, 1]);
      const srcLab = oklab.fromXYZ(srcXyz);
      const whLab = oklab.fromXYZ(whXyz);
      const mixLab = lerp3(srcLab, whLab, t);
      const mixXyz = oklab.toXYZ(mixLab);
      const lin = srgb.fromXYZ(mixXyz);
      return srgbTransfer.encode(clipLin(lin));
    },
  },
  {
    id: 'cielab', label: 'CIELAB',
    note: 'older perceptual space — works but blues notoriously curve toward purple.',
    interp: (src, t) => {
      const srcXyz = srgb.toXYZ(srgbTransfer.decode(hexToEnc(src)));
      const whXyz = srgb.toXYZ([1, 1, 1]);
      const srcLab = cielab.fromXYZ(srcXyz);
      const whLab = cielab.fromXYZ(whXyz);
      const mixLab = lerp3(srcLab, whLab, t);
      const mixXyz = cielab.toXYZ(mixLab);
      const lin = srgb.fromXYZ(mixXyz);
      return srgbTransfer.encode(clipLin(lin));
    },
  },
  {
    id: 'hsl', label: 'HSL',
    note: 'cylindrical RGB — saturation drops to 0 mid-mix; lightness sweep is uneven.',
    interp: (src, t) => {
      const srcXyz = srgb.toXYZ(srgbTransfer.decode(hexToEnc(src)));
      const whXyz = srgb.toXYZ([1, 1, 1]);
      const srcHsl = hsl.fromXYZ(srcXyz);
      const whHsl = hsl.fromXYZ(whXyz);
      // Use hue from src (white has undefined hue); lerp s and l only.
      const mixHsl = [srcHsl[0], lerp(srcHsl[1], whHsl[1], t), lerp(srcHsl[2], whHsl[2], t)];
      const mixXyz = hsl.toXYZ(mixHsl);
      const lin = srgb.fromXYZ(mixXyz);
      return srgbTransfer.encode(clipLin(lin));
    },
  },
];

class BlendThroughWhite extends HTMLElement {
  static get observedAttributes() { return ['color']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="btw-host"></div>`;
    this._root = this.querySelector('.btw-host');
  }

  render() {
    const src = this.getAttribute('color') || '#0066ff';
    if (!/^#[0-9a-fA-F]{6}$/.test(src)) return;
    this._root.innerHTML = SPACES.map(s => `
      <div class="btw-row">
        <div class="btw-label">
          <strong>${s.label}</strong>
          <div class="btw-note">${s.note}</div>
        </div>
        <canvas class="btw-canvas" data-space="${s.id}"></canvas>
      </div>
    `).join('');

    this._root.querySelectorAll('canvas[data-space]').forEach(canv => {
      const space = SPACES.find(s => s.id === canv.dataset.space);
      const wCss = Math.min(this.offsetWidth || 600, 720) - 200;
      const hCss = 56;
      const { ctx, w, h } = setupCanvas(canv, wCss, hCss);
      const tmp = document.createElement('canvas');
      tmp.width = STOPS; tmp.height = 1;
      const imgData = tmp.getContext('2d').createImageData(STOPS, 1);
      for (let i = 0; i < STOPS; i++) {
        const t = i / (STOPS - 1);
        const enc = space.interp(src, t);
        const bytes = encToHexBytes(enc);
        imgData.data[i * 4]     = bytes[0];
        imgData.data[i * 4 + 1] = bytes[1];
        imgData.data[i * 4 + 2] = bytes[2];
        imgData.data[i * 4 + 3] = 255;
      }
      tmp.getContext('2d').putImageData(imgData, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(tmp, 0, 0, w, h);
    });
  }
}

customElements.define('blend-through-white', BlendThroughWhite);
