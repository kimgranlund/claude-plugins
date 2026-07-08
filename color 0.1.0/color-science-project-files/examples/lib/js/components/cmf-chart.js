// <cmf-chart wavelength="555"></cmf-chart>
//
// Plot the CIE 1931 2° color-matching functions x̄(λ), ȳ(λ), z̄(λ) plus the
// Ottosson LMS cone-fundamental approximation. A movable wavelength indicator
// shows the cone-response signals + the resulting CIE chromaticity.

import { setupCanvas, fmt } from '../utils.js';
import { CMF_1931, X_BAR_1931, Y_BAR_1931, Z_BAR_1931 } from '../../dist/spectral/cmf.js';
import { WAVELENGTHS_NM } from '../../dist/spectral/illuminants.js';
import { M_XYZ_TO_LMS } from '../../dist/spaces/lms.js';
import { mulMat3Vec3 } from '../../dist/types.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

// Pre-compute LMS curves by transforming XYZ CMFs through M_XYZ_TO_LMS.
const LMS_CURVES = (() => {
  const Lc = [], Mc = [], Sc = [];
  for (let i = 0; i < 36; i++) {
    const xyz = [X_BAR_1931[i], Y_BAR_1931[i], Z_BAR_1931[i]];
    const lms = mulMat3Vec3(M_XYZ_TO_LMS, xyz);
    Lc.push(lms[0]); Mc.push(lms[1]); Sc.push(lms[2]);
  }
  return { L: Lc, M: Mc, S: Sc };
})();

function spectralColorHex(nm) {
  // Index nearest 10nm wavelength.
  const idx = Math.max(0, Math.min(35, Math.round((nm - 380) / 10)));
  // Use the CMF row scaled to a visible color.
  const xyz = CMF_1931[idx];
  const lin = srgb.fromXYZ(xyz);
  // Normalize for visibility.
  const m = Math.max(lin[0], lin[1], lin[2], 1e-6);
  const norm = [lin[0] / m, lin[1] / m, lin[2] / m];
  const cs = [
    Math.max(0, Math.min(1, norm[0])),
    Math.max(0, Math.min(1, norm[1])),
    Math.max(0, Math.min(1, norm[2])),
  ];
  const enc = srgbTransfer.encode(cs);
  return '#' + [enc[0], enc[1], enc[2]]
    .map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join('');
}

class CMFChart extends HTMLElement {
  static get observedAttributes() { return ['wavelength', 'show-lms']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _mount() {
    this.innerHTML = `<div class="cmf-host">
      <canvas class="cmf-canvas"></canvas>
      <div class="cmf-readout"></div>
    </div>`;
    this._canvas = this.querySelector('.cmf-canvas');
    this._readout = this.querySelector('.cmf-readout');
  }

  render() {
    const wavelength = Math.max(380, Math.min(730, parseFloat(this.getAttribute('wavelength') ?? '555')));
    const showLms = this.getAttribute('show-lms') !== 'false';

    const wCss = Math.min(this.offsetWidth || 720, 720);
    const hCss = 320;
    const { ctx, w, h } = setupCanvas(this._canvas, wCss, hCss);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);

    const padL = 40, padR = 12, padT = 16, padB = 32;
    const cw = w - padL - padR;
    const ch = h - padT - padB;

    // Y range: 0 to ~2.0 (z-bar can be > 1.8 near 440nm).
    const yMax = 2.0;
    const X_OF = nm => padL + ((nm - 380) / (730 - 380)) * cw;
    const Y_OF = v => padT + ch - (v / yMax) * ch;

    // Wavelength gradient strip below the chart (spectral colors).
    for (let nm = 380; nm <= 730; nm += 2) {
      const hex = spectralColorHex(nm);
      ctx.fillStyle = hex;
      const x = X_OF(nm);
      const xn = X_OF(nm + 2);
      ctx.fillRect(x, padT + ch + 4, xn - x + 1, 14);
    }
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '10px ui-monospace, monospace';
    [400, 450, 500, 550, 600, 650, 700].forEach(nm => {
      const x = X_OF(nm);
      ctx.fillText(nm + 'nm', x - 14, padT + ch + 30);
      ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, padT); ctx.lineTo(x, padT + ch); ctx.stroke();
    });
    [0, 0.5, 1.0, 1.5, 2.0].forEach(v => {
      const y = Y_OF(v);
      ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(padL + cw, y); ctx.stroke();
      ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
      ctx.fillText(v.toFixed(1), 4, y + 4);
    });

    function plot(arr, color, lw) {
      ctx.beginPath();
      WAVELENGTHS_NM.forEach((nm, i) => {
        const x = X_OF(nm);
        const y = Y_OF(arr[i]);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.strokeStyle = color;
      ctx.lineWidth = lw || 2;
      ctx.stroke();
    }

    if (showLms) {
      plot(LMS_CURVES.L, 'oklch(0.55 0.22 29)',  2);
      plot(LMS_CURVES.M, 'oklch(0.62 0.18 142)', 2);
      plot(LMS_CURVES.S, 'oklch(0.55 0.22 264)', 2);
    }
    plot(X_BAR_1931, 'oklch(0.55 0.22 29)',  showLms ? 1 : 2.5);
    plot(Y_BAR_1931, 'oklch(0.62 0.18 142)', showLms ? 1 : 2.5);
    plot(Z_BAR_1931, 'oklch(0.55 0.22 264)', showLms ? 1 : 2.5);

    // Current-wavelength indicator.
    const cx = X_OF(wavelength);
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--text').trim() || '#000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, padT); ctx.lineTo(cx, padT + ch);
    ctx.stroke();

    // Readout.
    const idx = Math.max(0, Math.min(35, Math.round((wavelength - 380) / 10)));
    const xb = X_BAR_1931[idx], yb = Y_BAR_1931[idx], zb = Z_BAR_1931[idx];
    const sum = xb + yb + zb || 1e-9;
    const cx_chroma = xb / sum, cy_chroma = yb / sum;
    const Lr = LMS_CURVES.L[idx], Mr = LMS_CURVES.M[idx], Sr = LMS_CURVES.S[idx];
    const hex = spectralColorHex(wavelength);
    this._readout.innerHTML =
      '<div class="cmf-r-row"><div>λ = <strong>' + wavelength.toFixed(0) + ' nm</strong></div>'
      + '<div class="cmf-swatch" style="background:' + hex + '"></div></div>'
      + '<div class="cmf-r-grid">'
        + '<div><span class="cmf-tag" style="background:oklch(0.55 0.22 29)">x̄</span> ' + fmt(xb, 4) + '</div>'
        + '<div><span class="cmf-tag" style="background:oklch(0.62 0.18 142)">ȳ</span> ' + fmt(yb, 4) + '</div>'
        + '<div><span class="cmf-tag" style="background:oklch(0.55 0.22 264)">z̄</span> ' + fmt(zb, 4) + '</div>'
        + '<div><span class="cmf-tag" style="background:oklch(0.55 0.18 29)">L</span> ' + fmt(Lr, 4) + '</div>'
        + '<div><span class="cmf-tag" style="background:oklch(0.62 0.14 142)">M</span> ' + fmt(Mr, 4) + '</div>'
        + '<div><span class="cmf-tag" style="background:oklch(0.55 0.18 264)">S</span> ' + fmt(Sr, 4) + '</div>'
      + '</div>'
      + '<div>chromaticity x = <strong>' + fmt(cx_chroma, 4) + '</strong>, y = <strong>' + fmt(cy_chroma, 4) + '</strong></div>';
  }
}

customElements.define('cmf-chart', CMFChart);
