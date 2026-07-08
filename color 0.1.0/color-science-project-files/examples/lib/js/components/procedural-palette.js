// <procedural-palette algorithm="cubehelix"></procedural-palette>
//
// Procedural-palette explorer. Two modes:
//
//   1. Cubehelix (D. A. Green 2011)
//        params: start (deg), rotations, hue, gamma
//
//   2. iq cosine (Inigo Quilez)
//        params: a, b, c, d (each is a 3-vector R/G/B)
//        formula: color(t) = a + b * cos(2π · (c · t + d))
//
// API:
//   attribute `algorithm` — "cubehelix" | "iq"
//   sliders are wired by the host page; we expose JSON-encoded params via
//   `.params` setter for cubehelix, or `.iqParams` setter for iq.

import { setupCanvas, toHex } from '../utils.js';
import { cubehelix } from '../../dist/interpolation/cubehelix.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as oklch from '../../dist/spaces/oklch.js';
import { mapToSRGB } from '../../dist/gamut/mapping.js';

function clip01(v) { return Math.max(0, Math.min(1, v)); }
function clipLin(rgb) { return [clip01(rgb[0]), clip01(rgb[1]), clip01(rgb[2])]; }
function linToHex(lin) { return toHex(srgbTransfer.encode(clipLin(lin))); }

function iqColor(t, a, b, c, d) {
  // a + b * cos(2π · (c · t + d))
  return [0, 1, 2].map(i => a[i] + b[i] * Math.cos(2 * Math.PI * (c[i] * t + d[i])));
}

class ProceduralPalette extends HTMLElement {
  static get observedAttributes() { return ['algorithm', 'params']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="proc-host">
      <canvas class="proc-ramp"></canvas>
      <div class="proc-strip"></div>
      <canvas class="proc-y"></canvas>
    </div>`;
    this._root = this.querySelector('.proc-host');
    this._ramp = this.querySelector('.proc-ramp');
    this._strip = this.querySelector('.proc-strip');
    this._yChart = this.querySelector('.proc-y');
  }

  set params(p) {
    this._params = p;
    this.render();
  }
  set iqParams(p) {
    this._iqParams = p;
    this.render();
  }

  render() {
    const algo = this.getAttribute('algorithm') || 'cubehelix';
    const N_RAMP = 256;
    const N_STRIP = 9;

    function sampler(t) {
      if (algo === 'iq') {
        const p = this._iqParams || { a: [0.5,0.5,0.5], b: [0.5,0.5,0.5], c: [1,1,1], d: [0,0.33,0.67] };
        return iqColor(t, p.a, p.b, p.c, p.d);
      }
      const p = this._params || { start: 0.5, rotations: -1.5, hue: 1.0, gamma: 1.0 };
      return cubehelix(t, p);
    }
    sampler = sampler.bind(this);

    // ─── Smooth ramp ─────────────────────────────────────────────────────
    const wCss = Math.min(this.offsetWidth || 720, 720);
    const hCss = 64;
    const { ctx, w, h } = setupCanvas(this._ramp, wCss, hCss);
    const tmp = document.createElement('canvas');
    tmp.width = N_RAMP; tmp.height = 1;
    const imgData = tmp.getContext('2d').createImageData(N_RAMP, 1);
    for (let i = 0; i < N_RAMP; i++) {
      const t = i / (N_RAMP - 1);
      const lin = sampler(t);
      const enc = srgbTransfer.encode(clipLin(lin));
      imgData.data[i * 4]     = Math.round(enc[0] * 255);
      imgData.data[i * 4 + 1] = Math.round(enc[1] * 255);
      imgData.data[i * 4 + 2] = Math.round(enc[2] * 255);
      imgData.data[i * 4 + 3] = 255;
    }
    tmp.getContext('2d').putImageData(imgData, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(tmp, 0, 0, w, h);

    // ─── Discrete N-color strip ─────────────────────────────────────────
    const hexes = [];
    for (let i = 0; i < N_STRIP; i++) {
      const t = i / (N_STRIP - 1);
      hexes.push(linToHex(sampler(t)));
    }
    this._strip.innerHTML = hexes.map(hex => `
      <div class="proc-swatch" style="background:${hex}">
        <span>${hex}</span>
      </div>
    `).join('');

    // ─── Luminance plot ─────────────────────────────────────────────────
    const wY = Math.min(this.offsetWidth || 720, 720);
    const hY = 120;
    const { ctx: yctx, w: yw, h: yh } = setupCanvas(this._yChart, wY, hY);
    yctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    yctx.fillRect(0, 0, yw, yh);
    const padL = 28, padR = 8, padT = 12, padB = 20;
    const cw = yw - padL - padR;
    const ch = yh - padT - padB;
    yctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
    yctx.lineWidth = 1;
    yctx.font = '10px ui-monospace, monospace';
    yctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    [0, 0.5, 1].forEach(v => {
      const y = padT + ch - v * ch;
      yctx.beginPath();
      yctx.moveTo(padL, y); yctx.lineTo(padL + cw, y);
      yctx.stroke();
      yctx.fillText(v.toFixed(1), 4, y + 4);
    });

    // Plot relative luminance Y.
    yctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || 'oklch(0.55 0.18 264)';
    yctx.lineWidth = 2;
    yctx.beginPath();
    for (let i = 0; i < N_RAMP; i++) {
      const t = i / (N_RAMP - 1);
      const lin = clipLin(sampler(t));
      const Y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
      const x = padL + (i / (N_RAMP - 1)) * cw;
      const y = padT + ch - Y * ch;
      if (i === 0) yctx.moveTo(x, y); else yctx.lineTo(x, y);
    }
    yctx.stroke();
    yctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    yctx.fillText('relative luminance Y vs t', padL + 4, padT + 12);
  }
}

customElements.define('procedural-palette', ProceduralPalette);
