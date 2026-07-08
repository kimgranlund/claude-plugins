// <spd-chart show="D65,A,D50,F2"></spd-chart>
//
// Plot the spectral power distributions of standard illuminants on the same
// chart (380-730 nm × intensity), with a sample-color grid below showing how
// a fixed set of reflectance spectra render under each illuminant.

import { setupCanvas } from '../utils.js';
import { D65, D50, A, F2, E, WAVELENGTHS_NM } from '../../dist/spectral/illuminants.js';
import { reflectiveToXYZ } from '../../dist/spectral/spd.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { bradfordMatrix, D65 as D65xyz } from '../../dist/adaptation/bradford.js';
import { mulMat3Vec3 } from '../../dist/types.js';

const ILLUMINANTS = {
  D65: { name: 'D65 ~6500K',     spd: D65, color: 'oklch(0.554 0.180 264)', wpXYZ: [0.95046, 1.0, 1.08906] },
  D50: { name: 'D50 ~5000K',     spd: D50, color: 'oklch(0.620 0.180 60)',  wpXYZ: [0.96430, 1.0, 0.82510] },
  A:   { name: 'A 2856K (tungsten)', spd: A, color: 'oklch(0.700 0.180 50)',  wpXYZ: [1.0985, 1.0, 0.35585] },
  F2:  { name: 'F2 cool white',  spd: F2, color: 'oklch(0.620 0.180 150)', wpXYZ: [0.99186, 1.0, 0.67393] },
  E:   { name: 'E equal energy', spd: E,  color: 'oklch(0.600 0.020 264)', wpXYZ: [1.0, 1.0, 1.0] },
};

// Sample reflectance spectra — simulated, but illustrative.
function gauss(center, width, height) {
  return WAVELENGTHS_NM.map(nm => {
    const t = (nm - center) / width;
    return Math.max(0.04, Math.min(1, height * Math.exp(-t * t)));
  });
}
function sigmoid(edge, width, lo, hi) {
  return WAVELENGTHS_NM.map(nm => {
    const t = (nm - edge) / width;
    return Math.max(0.04, Math.min(1, lo + (hi - lo) / (1 + Math.exp(-t))));
  });
}

const SAMPLES = [
  { name: 'white',  spectrum: new Array(36).fill(0.85) },
  { name: 'red',    spectrum: sigmoid(595, 15, 0.05, 0.78) },
  { name: 'green',  spectrum: gauss(520, 35, 0.55) },
  { name: 'blue',   spectrum: gauss(450, 50, 0.55) },
  { name: 'orange', spectrum: sigmoid(550, 18, 0.05, 0.72) },
  { name: 'magenta',spectrum: WAVELENGTHS_NM.map(nm => {
      const t1 = (nm - 430) / 40;
      const t2 = (nm - 660) / 40;
      return Math.max(0.04, Math.min(1, 0.6 * (Math.exp(-(t1 * t1)) + Math.exp(-(t2 * t2)))));
    }) },
  { name: 'skin',   spectrum: sigmoid(540, 30, 0.20, 0.55) },
  { name: 'gray',   spectrum: new Array(36).fill(0.18) },
];

function spectrumToHex(spectrum, illuminant) {
  const sceneXyz = reflectiveToXYZ(spectrum, illuminant.spd);
  // Adapt to D65 for display (the user's screen IS sRGB which is D65),
  // simulating "if my eyes are adapted to D65 but the light source is X".
  const adaptM = bradfordMatrix(illuminant.wpXYZ, D65xyz);
  const adaptedXyz = mulMat3Vec3(adaptM, sceneXyz);
  // Actually for the "see under different illuminants" demo, we want the
  // OPPOSITE — assume eyes adapt to the new illuminant. Simulated as: use
  // the scene XYZ directly (no chromatic adaptation), which makes whites
  // look colored when the illuminant is colored.
  const lin = srgb.fromXYZ(sceneXyz);
  const cs = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(cs);
  return '#' + [enc[0], enc[1], enc[2]]
    .map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join('');
}

class SPDChart extends HTMLElement {
  static get observedAttributes() { return ['show']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="spd-host">
      <canvas class="spd-chart-canvas"></canvas>
      <div class="spd-samples"></div>
    </div>`;
    this._root = this.querySelector('.spd-host');
    this._chart = this.querySelector('.spd-chart-canvas');
    this._samples = this.querySelector('.spd-samples');
  }

  render() {
    const showAttr = this.getAttribute('show') || 'D65,A,D50,F2';
    const showList = showAttr.split(',').map(s => s.trim()).filter(k => ILLUMINANTS[k]);
    this._renderChart(showList);
    this._renderSamples(showList);
  }

  _renderChart(showList) {
    const wCss = Math.min(this.offsetWidth || 760, 760);
    const hCss = 280;
    const { ctx, w, h } = setupCanvas(this._chart, wCss, hCss);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);
    const padL = 36, padR = 8, padT = 16, padB = 28;
    const cw = w - padL - padR;
    const ch = h - padT - padB;

    // Find max for y-axis scaling.
    let maxY = 0;
    for (const key of showList) maxY = Math.max(maxY, ...ILLUMINANTS[key].spd);
    maxY = Math.ceil(maxY / 25) * 25;

    // Grid
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
    ctx.lineWidth = 1;
    ctx.font = '10px ui-monospace, monospace';
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    [400, 500, 600, 700].forEach(nm => {
      const x = padL + ((nm - 380) / (730 - 380)) * cw;
      ctx.beginPath();
      ctx.moveTo(x, padT); ctx.lineTo(x, padT + ch);
      ctx.stroke();
      ctx.fillText(String(nm), x - 10, padT + ch + 18);
    });
    for (let v = 0; v <= maxY; v += maxY / 4) {
      const y = padT + ch - (v / maxY) * ch;
      ctx.beginPath();
      ctx.moveTo(padL, y); ctx.lineTo(padL + cw, y);
      ctx.stroke();
      ctx.fillText(v.toFixed(0), 4, y + 4);
    }

    // Plot each SPD.
    for (const key of showList) {
      const { spd, color } = ILLUMINANTS[key];
      ctx.beginPath();
      WAVELENGTHS_NM.forEach((nm, i) => {
        const x = padL + ((nm - 380) / (730 - 380)) * cw;
        const y = padT + ch - (spd[i] / maxY) * ch;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Legend
    ctx.font = '11px ui-monospace, monospace';
    let lx = padL + 8;
    for (const key of showList) {
      const { name, color } = ILLUMINANTS[key];
      ctx.fillStyle = color;
      ctx.fillRect(lx, padT + 4, 12, 8);
      ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text').trim() || '#111';
      ctx.fillText(name, lx + 16, padT + 12);
      lx += ctx.measureText(name).width + 36;
    }
  }

  _renderSamples(showList) {
    let html = '<table class="spd-table"><thead><tr><th></th>';
    for (const key of showList) {
      html += '<th>' + ILLUMINANTS[key].name + '</th>';
    }
    html += '</tr></thead><tbody>';
    for (const sample of SAMPLES) {
      html += '<tr><th>' + sample.name + '</th>';
      for (const key of showList) {
        const hex = spectrumToHex(sample.spectrum, ILLUMINANTS[key]);
        html += '<td><div class="spd-swatch" style="background:' + hex + '"></div></td>';
      }
      html += '</tr>';
    }
    html += '</tbody></table>';
    this._samples.innerHTML = html;
  }
}

customElements.define('spd-chart', SPDChart);
