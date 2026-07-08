// <contrast-readout text="#000" bg="#fff"></contrast-readout>
//
// Live WCAG + APCA contrast metrics for a foreground/background pair.

import { wcagContrast } from '../../dist/metrics/luminance.js';
import { apcaContrast, readabilityTier } from '../../dist/metrics/apca.js';
import { fromHex, fmt } from '../utils.js';

function wcagTier(ratio) {
  if (ratio >= 7.0) return 'AAA';
  if (ratio >= 4.5) return 'AA';
  if (ratio >= 3.0) return 'AA-large';
  return 'fail';
}

function wcagPill(ratio) {
  const t = wcagTier(ratio);
  const cls = ratio >= 4.5 ? 'pass' : ratio >= 3.0 ? 'warn' : 'fail';
  return `<span class="pill ${cls}">${t}</span>`;
}

function apcaPill(tier) {
  const goodTiers = ['optimal', 'fluent-body', 'body-minimum'];
  const cls = goodTiers.includes(tier) ? 'pass' :
    tier === 'insufficient' ? 'fail' : 'warn';
  return `<span class="pill ${cls}">${tier}</span>`;
}

class ContrastReadout extends HTMLElement {
  static get observedAttributes() { return ['text', 'bg']; }

  connectedCallback() {
    this._build();
    this.render();
  }

  attributeChangedCallback() { if (this._mounted) this.render(); }

  _build() {
    this.innerHTML = `
      <div class="preview" data-preview>
        The quick brown fox jumps.
        <div class="small">Aa Bb Cc 0123456789 — body text @ 16px / 400</div>
      </div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">WCAG 2.2 contrast</div>
          <div class="metric-value" data-wcag>—</div>
          <div class="metric-detail" data-wcag-detail>—</div>
        </div>
        <div class="metric">
          <div class="metric-label">APCA L<sup>c</sup></div>
          <div class="metric-value" data-apca>—</div>
          <div class="metric-detail" data-apca-detail>—</div>
        </div>
      </div>
    `;
    this._mounted = true;
  }

  render() {
    const textHex = this.getAttribute('text') || '#000000';
    const bgHex = this.getAttribute('bg') || '#ffffff';
    const text = fromHex(textHex);
    const bg = fromHex(bgHex);

    const wcag = wcagContrast(text, bg);
    const apca = apcaContrast(text, bg);
    const tier = readabilityTier(apca);

    const preview = this.querySelector('[data-preview]');
    preview.style.background = bgHex;
    preview.style.color = textHex;

    this.querySelector('[data-wcag]').innerHTML = `${fmt(wcag, 2)}:1`;
    this.querySelector('[data-wcag-detail]').innerHTML =
      wcagPill(wcag) + ' &nbsp; AA=4.5 · AAA=7';

    this.querySelector('[data-apca]').innerHTML = `${fmt(apca, 1)}`;
    this.querySelector('[data-apca-detail]').innerHTML =
      apcaPill(tier);
  }
}

customElements.define('contrast-readout', ContrastReadout);
