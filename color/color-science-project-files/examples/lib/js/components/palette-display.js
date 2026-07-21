// <palette-display></palette-display>
//
// Render a palette of colors with hex labels. Set palette via `.colors` property
// (array of encoded sRGB tuples) or `colors` attribute (comma-separated hex).

import { toHex } from '../utils.js';
import { fromHex } from '../utils.js';

class PaletteDisplay extends HTMLElement {
  static get observedAttributes() { return ['colors']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  set colors(arr) {
    this._colors = arr;
    if (this._root) this.render();
  }

  get colors() { return this._colors || []; }

  _mount() {
    this.innerHTML = `<div class="palette"></div>`;
    this._root = this.querySelector('.palette');
  }

  render() {
    let cols = this._colors;
    if (!cols) {
      const attr = this.getAttribute('colors');
      if (attr) {
        cols = attr.split(',').map(s => fromHex(s.trim()));
      } else {
        cols = [];
      }
    }
    this._root.innerHTML = cols.map(c => {
      const hex = toHex(c);
      return `<div class="palette-swatch">
        <div class="color" style="background:${hex}"></div>
        <div class="meta">${hex}</div>
      </div>`;
    }).join('');
  }
}

customElements.define('palette-display', PaletteDisplay);
