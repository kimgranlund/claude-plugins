// <pigment-mixer pigment-a="ultramarine" pigment-b="cadyellow" ratio="0.5"></pigment-mixer>
//
// Mix two pigment reflectance spectra via single-constant Kubelka-Munk,
// alongside a naive RGB mix of the same two endpoint colors. The K-M result
// is the realistic paint blend; the RGB result is the desaturated/muddy
// "additive midpoint" that pixel-averaging would give.

import { setupCanvas, toHex, fmt } from '../utils.js';
import { mix as kmMix } from '../../dist/pigment/kubelka-munk.js';
import { reflectiveToXYZ } from '../../dist/spectral/spd.js';
import { D65, WAVELENGTHS_NM } from '../../dist/spectral/illuminants.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

// Per-pigment reflectance spectra at 380-730nm, 10nm intervals (36 samples).
// These are plausible shapes for demo purposes — real measured curves from a
// pigment supplier (e.g., Golden Heavy Body) would be more accurate. They're
// hand-tuned to give the right XYZ → sRGB color appearance per pigment.
function gauss(center, width, height) {
  return WAVELENGTHS_NM.map(nm => {
    const t = (nm - center) / width;
    return Math.max(0.005, Math.min(1, height * Math.exp(-t * t)));
  });
}
function sigmoid(edge, width, low, high) {
  return WAVELENGTHS_NM.map(nm => {
    const t = (nm - edge) / width;
    return Math.max(0.005, Math.min(1, low + (high - low) / (1 + Math.exp(-t))));
  });
}
function flat(v) { return new Array(36).fill(v); }

const PIGMENTS = {
  white:     { name: 'Titanium white',    spectrum: flat(0.95) },
  black:     { name: 'Mars black',        spectrum: flat(0.04) },
  ultramarine: { name: 'Ultramarine blue', spectrum: gauss(440, 50, 0.62).map((v, i) => v + (WAVELENGTHS_NM[i] > 640 ? 0.10 : 0)) },
  cobaltblue:{ name: 'Cobalt blue',       spectrum: gauss(460, 65, 0.55) },
  cadyellow: { name: 'Cadmium yellow',    spectrum: sigmoid(520, 12, 0.04, 0.85) },
  cadred:    { name: 'Cadmium red',       spectrum: sigmoid(595, 15, 0.04, 0.78) },
  alizarin:  { name: 'Alizarin crimson',  spectrum: sigmoid(605, 18, 0.03, 0.60).map((v,i) => WAVELENGTHS_NM[i] < 460 ? Math.max(v, 0.10) : v) },
  viridian:  { name: 'Viridian green',    spectrum: gauss(520, 35, 0.55) },
  yellowochre:{ name: 'Yellow ochre',     spectrum: sigmoid(530, 22, 0.10, 0.60) },
  burntsienna:{ name: 'Burnt sienna',     spectrum: sigmoid(575, 25, 0.05, 0.50) },
};

function spectrumToHex(spectrum) {
  const xyz = reflectiveToXYZ(spectrum, D65);
  const lin = srgbSpace.fromXYZ(xyz);
  const cs = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  return toHex(srgbTransfer.encode(cs));
}

function naiveRgbMix(hexA, hexB, ratio) {
  // Linear-space midpoint between the two encoded-sRGB-rendered pigment colors.
  function fromHex(h) {
    return [
      parseInt(h.slice(1, 3), 16) / 255,
      parseInt(h.slice(3, 5), 16) / 255,
      parseInt(h.slice(5, 7), 16) / 255,
    ];
  }
  const a = fromHex(hexA), b = fromHex(hexB);
  // Decode → mix → encode
  const linA = srgbTransfer.decode(a);
  const linB = srgbTransfer.decode(b);
  const mix = [
    linA[0] * ratio + linB[0] * (1 - ratio),
    linA[1] * ratio + linB[1] * (1 - ratio),
    linA[2] * ratio + linB[2] * (1 - ratio),
  ];
  return toHex(srgbTransfer.encode(mix));
}

class PigmentMixer extends HTMLElement {
  static get observedAttributes() { return ['pigment-a', 'pigment-b', 'ratio']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="pigment-host"></div>`;
    this._root = this.querySelector('.pigment-host');
  }

  render() {
    const pa = this.getAttribute('pigment-a') || 'ultramarine';
    const pb = this.getAttribute('pigment-b') || 'cadyellow';
    const ratio = Math.max(0, Math.min(1, parseFloat(this.getAttribute('ratio') ?? '0.5')));

    const A = PIGMENTS[pa] || PIGMENTS.ultramarine;
    const B = PIGMENTS[pb] || PIGMENTS.cadyellow;

    const hexA = spectrumToHex(A.spectrum);
    const hexB = spectrumToHex(B.spectrum);

    const mixedSpectrum = kmMix(A.spectrum, B.spectrum, ratio);
    const hexKM = spectrumToHex(mixedSpectrum);
    const hexRGB = naiveRgbMix(hexA, hexB, ratio);

    this._root.innerHTML = `
      <div class="pigment-row pigment-row--inputs">
        <div class="pigment-cell">
          <div class="pigment-swatch" style="background:${hexA}"></div>
          <div class="pigment-meta"><strong>${A.name}</strong><br><span>${(ratio * 100).toFixed(0)}%</span></div>
        </div>
        <div class="pigment-cell">
          <div class="pigment-swatch" style="background:${hexB}"></div>
          <div class="pigment-meta"><strong>${B.name}</strong><br><span>${((1 - ratio) * 100).toFixed(0)}%</span></div>
        </div>
      </div>
      <div class="pigment-row pigment-row--outputs">
        <div class="pigment-cell pigment-cell--km">
          <div class="pigment-swatch" style="background:${hexKM}"></div>
          <div class="pigment-meta"><strong>Kubelka-Munk mix</strong><br><span>physical pigment blend · ${hexKM}</span></div>
        </div>
        <div class="pigment-cell pigment-cell--rgb">
          <div class="pigment-swatch" style="background:${hexRGB}"></div>
          <div class="pigment-meta"><strong>RGB midpoint</strong><br><span>naive sRGB average · ${hexRGB}</span></div>
        </div>
      </div>
    `;

    // Render the reflectance-spectrum chart inline.
    this._renderSpectrumChart(A.spectrum, B.spectrum, mixedSpectrum, hexA, hexB, hexKM);
  }

  _renderSpectrumChart(specA, specB, specMix, hexA, hexB, hexMix) {
    let chartCanvas = this._root.querySelector('.pigment-chart');
    if (!chartCanvas) {
      this._root.insertAdjacentHTML('beforeend', '<canvas class="pigment-chart"></canvas>');
      chartCanvas = this._root.querySelector('.pigment-chart');
    }
    const wCss = Math.min(this.offsetWidth || 700, 700);
    const hCss = 220;
    const { ctx, w, h } = setupCanvas(chartCanvas, wCss, hCss);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);

    // Grid: vertical at 400, 500, 600, 700 nm; horizontal at R=0, 0.5, 1.0
    const padL = 30, padR = 8, padT = 12, padB = 22;
    const cw = w - padL - padR;
    const ch = h - padT - padB;
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#ccc';
    ctx.lineWidth = 1;
    ctx.font = '10px ui-monospace, monospace';
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    [400, 500, 600, 700].forEach(nm => {
      const x = padL + ((nm - 380) / (730 - 380)) * cw;
      ctx.beginPath();
      ctx.moveTo(x, padT); ctx.lineTo(x, padT + ch);
      ctx.stroke();
      ctx.fillText(String(nm), x - 10, padT + ch + 14);
    });
    [0, 0.5, 1].forEach(r => {
      const y = padT + ch - r * ch;
      ctx.beginPath();
      ctx.moveTo(padL, y); ctx.lineTo(padL + cw, y);
      ctx.stroke();
      ctx.fillText(r.toFixed(1), 2, y + 4);
    });

    function plot(spec, color) {
      ctx.beginPath();
      WAVELENGTHS_NM.forEach((nm, i) => {
        const x = padL + ((nm - 380) / (730 - 380)) * cw;
        const y = padT + ch - spec[i] * ch;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
    plot(specA, hexA);
    plot(specB, hexB);
    plot(specMix, hexMix);

    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '10px ui-monospace, monospace';
    ctx.fillText('reflectance vs λ (nm)', padL + 4, padT + 12);
  }

  static get PIGMENTS() { return PIGMENTS; }
}

customElements.define('pigment-mixer', PigmentMixer);
