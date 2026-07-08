// <transfer-curve curves="srgb,rec2020,pq"></transfer-curve>
//
// Plot one or more transfer functions on a 1×1 canvas. Linear input on X,
// encoded output on Y. Demonstrates how different gamma curves differ.

import { setupCanvas } from '../utils.js';
import * as srgb from '../../dist/transfer/srgb.js';
import * as rec2020 from '../../dist/transfer/rec2020.js';
import * as pq from '../../dist/transfer/pq.js';
import * as hlg from '../../dist/transfer/hlg.js';
import * as adobeRgb from '../../dist/transfer/adobe-rgb.js';
import * as prophoto from '../../dist/transfer/prophoto.js';

const CURVES = {
  srgb:     { encode: srgb.encodeComponent,     color: 'oklch(0.55 0.18 264)', label: 'sRGB / Display P3' },
  rec2020:  { encode: rec2020.encodeComponent,  color: 'oklch(0.62 0.18 150)', label: 'Rec.2020 / Rec.709' },
  pq:       { encode: pq.encodeComponent,       color: 'oklch(0.70 0.18  50)', label: 'PQ (HDR)' },
  hlg:      { encode: hlg.encodeComponent,      color: 'oklch(0.57 0.22  29)', label: 'HLG (HDR)' },
  adobergb: { encode: adobeRgb.encodeComponent, color: 'oklch(0.55 0.18 300)', label: 'Adobe RGB γ=2.2' },
  prophoto: { encode: prophoto.encodeComponent, color: 'oklch(0.55 0.18 200)', label: 'ProPhoto γ=1.8' },
};

class TransferCurve extends HTMLElement {
  static get observedAttributes() { return ['curves']; }

  connectedCallback() {
    this._build();
    this.render();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _build() {
    this.innerHTML = `<canvas></canvas><div class="legend" style="margin-top:var(--s-3);display:flex;gap:var(--s-3);flex-wrap:wrap;font-family:var(--font-mono);font-size:var(--text-xs);"></div>`;
    this._canvas = this.querySelector('canvas');
    this._legend = this.querySelector('.legend');
  }

  render() {
    const curvesList = (this.getAttribute('curves') || 'srgb,rec2020')
      .split(',').map(s => s.trim().toLowerCase()).filter(s => CURVES[s]);

    const size = Math.min(this.offsetWidth || 400, 500);
    const { ctx, w, h } = setupCanvas(this._canvas, size, size);

    // Background + axes
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card') || '#fff';
    ctx.fillRect(0, 0, w, h);

    // Grid
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--border') || '#eee';
    ctx.lineWidth = 1;
    for (let i = 1; i < 10; i++) {
      const p = (i / 10) * w;
      ctx.beginPath();
      ctx.moveTo(p, 0); ctx.lineTo(p, h); ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, p); ctx.lineTo(w, p); ctx.stroke();
    }

    // Identity reference
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-faint') || '#888';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, h); ctx.lineTo(w, 0); ctx.stroke();
    ctx.setLineDash([]);

    // Curves
    for (const key of curvesList) {
      const { encode, color } = CURVES[key];
      ctx.strokeStyle = color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      const samples = w;
      for (let i = 0; i <= samples; i++) {
        const x = i / samples;
        const y = encode(x);
        const px = x * w;
        const py = (1 - Math.max(0, Math.min(1, y))) * h;
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
    }

    // Axis labels
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted') || '#888';
    ctx.font = '11px ui-monospace, monospace';
    ctx.fillText('linear', 4, h - 4);
    ctx.fillText('encoded', 4, 12);

    // Legend
    this._legend.innerHTML = curvesList.map(k => {
      const { color, label } = CURVES[k];
      return `<span style="display:flex;align-items:center;gap:4px;">
        <span style="display:inline-block;width:14px;height:3px;background:${color};border-radius:2px;"></span>
        ${label}
      </span>`;
    }).join('');
  }
}

customElements.define('transfer-curve', TransferCurve);
