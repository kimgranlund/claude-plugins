// <volume-bars></volume-bars>
//
// Monte Carlo estimation of color-gamut volumes in OKLab perceptual units.
// Sample uniformly in an OKLab bounding box [0,1] × [-0.5, 0.5] × [-0.5, 0.5],
// for each sample test inclusion in each gamut's linear-RGB cube. Volume =
// (samples-in-gamut / total) × box-volume.
//
// Output: a bar chart normalized so sRGB = 1.0. Larger bars = wider gamut in
// perceptual units (not just chromaticity area).

import { setupCanvas, fmt } from '../utils.js';
import * as oklab from '../../dist/spaces/oklab.js';
import {
  M_XYZ_TO_SRGB,
  M_XYZ_TO_P3,
  M_XYZ_TO_REC2020,
  inGamut,
} from '../../dist/gamut/oklch-peak.js';
import { mulMat3Vec3 } from '../../dist/types.js';

// Adobe RGB (1998) D65 XYZ → linear RGB matrix.
const M_XYZ_TO_ADOBE_RGB = [
  [ 2.0413690, -0.5649464, -0.3446944],
  [-0.9692660,  1.8760108,  0.0415560],
  [ 0.0134474, -0.1183897,  1.0154096],
];

// ProPhoto D50; treated approximately here (no Bradford applied — Monte Carlo
// volume estimate is intended for relative comparison, not absolute accuracy).
const M_XYZ_TO_PROPHOTO_D65 = [
  [ 1.3460000, -0.2556000, -0.0511000],
  [-0.5446000,  1.5082000,  0.0205000],
  [ 0.0000000,  0.0000000,  1.2117000],
];

const GAMUTS = [
  { name: 'Rec.709',    matrix: M_XYZ_TO_SRGB,       color: 'oklch(0.55 0.18 264)' },
  { name: 'sRGB',       matrix: M_XYZ_TO_SRGB,       color: 'oklch(0.55 0.18 264)' },
  { name: 'Display P3', matrix: M_XYZ_TO_P3,         color: 'oklch(0.62 0.18 150)' },
  { name: 'Adobe RGB',  matrix: M_XYZ_TO_ADOBE_RGB,  color: 'oklch(0.55 0.18 300)' },
  { name: 'Rec.2020',   matrix: M_XYZ_TO_REC2020,    color: 'oklch(0.70 0.18  50)' },
  { name: 'ProPhoto',   matrix: M_XYZ_TO_PROPHOTO_D65, color: 'oklch(0.62 0.18 200)' },
];

const SAMPLES = 30000;

function measureVolumes() {
  // Sample uniformly in OKLab box.
  const Lmin = 0, Lmax = 1;
  const aRange = 0.45, bRange = 0.45;
  const boxVolume = (Lmax - Lmin) * (aRange * 2) * (bRange * 2);
  const counts = GAMUTS.map(() => 0);
  let xorshift = 0xC0FFEE;
  function rand() {
    xorshift ^= xorshift << 13;
    xorshift ^= xorshift >>> 17;
    xorshift ^= xorshift << 5;
    return (xorshift >>> 0) / 0xFFFFFFFF;
  }
  for (let i = 0; i < SAMPLES; i++) {
    const L = Lmin + rand() * (Lmax - Lmin);
    const a = -aRange + rand() * (aRange * 2);
    const b = -bRange + rand() * (bRange * 2);
    const xyz = oklab.toXYZ([L, a, b]);
    for (let g = 0; g < GAMUTS.length; g++) {
      if (inGamut(mulMat3Vec3(GAMUTS[g].matrix, xyz))) counts[g]++;
    }
  }
  return counts.map((c, g) => ({
    name: GAMUTS[g].name,
    color: GAMUTS[g].color,
    volume: (c / SAMPLES) * boxVolume,
  }));
}

class VolumeBars extends HTMLElement {
  connectedCallback() {
    this._mount();
    this.render();
  }

  _mount() {
    this.innerHTML = `<div class="vol-host">
      <p class="vol-status" style="color:var(--text-muted);font-size:var(--text-sm);">Measuring volumes by Monte Carlo (${SAMPLES.toLocaleString()} samples)…</p>
      <canvas class="vol-canvas"></canvas>
      <table class="vol-table"></table>
    </div>`;
    this._canvas = this.querySelector('.vol-canvas');
    this._table = this.querySelector('.vol-table');
    this._status = this.querySelector('.vol-status');
  }

  render() {
    requestAnimationFrame(() => {
      const t = performance.now();
      const measured = measureVolumes();
      const sRGB = measured.find(m => m.name === 'sRGB').volume;
      const elapsed = (performance.now() - t).toFixed(0);

      const wCss = Math.min(this.offsetWidth || 700, 760);
      const hCss = 320;
      const { ctx, w, h } = setupCanvas(this._canvas, wCss, hCss);
      ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
      ctx.fillRect(0, 0, w, h);

      const padL = 110, padR = 60, padT = 16, padB = 16;
      const cw = w - padL - padR;
      const ch = h - padT - padB;
      const barH = ch / measured.length - 6;
      // Use the absolute max for x-axis.
      const maxV = Math.max(...measured.map(m => m.volume));
      ctx.font = '12px ui-monospace, monospace';

      measured.forEach((m, i) => {
        const y = padT + i * (barH + 6);
        const ratio = m.volume / sRGB;
        const widthPx = (m.volume / maxV) * cw;
        ctx.fillStyle = m.color;
        ctx.fillRect(padL, y, widthPx, barH);
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#666';
        ctx.textAlign = 'right';
        ctx.fillText(m.name, padL - 8, y + barH / 2 + 4);
        ctx.textAlign = 'left';
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text').trim() || '#111';
        ctx.fillText(ratio.toFixed(2) + '×', padL + widthPx + 8, y + barH / 2 + 4);
      });

      // Table
      let html = '<thead><tr><th>Gamut</th><th>Volume (OKLab units)</th><th>vs sRGB</th></tr></thead><tbody>';
      for (const m of measured) {
        html += '<tr>' +
          '<td><span class="vol-dot" style="background:' + m.color + '"></span> <strong>' + m.name + '</strong></td>' +
          '<td>' + fmt(m.volume, 4) + '</td>' +
          '<td>' + fmt(m.volume / sRGB, 2) + '×</td>' +
          '</tr>';
      }
      html += '</tbody>';
      this._table.innerHTML = html;
      this._status.textContent = `Monte Carlo with ${SAMPLES.toLocaleString()} OKLab samples — ${elapsed}ms`;
    });
  }
}

customElements.define('volume-bars', VolumeBars);
