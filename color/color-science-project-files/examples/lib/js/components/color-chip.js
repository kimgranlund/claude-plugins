// <color-chip color="oklch(0.55 0.18 264)" label="Brand 500"></color-chip>
//
// Renders a small swatch with optional label. Color can be any CSS color string.

class ColorChip extends HTMLElement {
  static get observedAttributes() { return ['color', 'label']; }

  connectedCallback() { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    const color = this.getAttribute('color') || 'transparent';
    const label = this.getAttribute('label') || '';
    this.innerHTML = `
      <div class="chip-swatch" style="background: ${color};"></div>
      ${label ? `<div class="chip-label">${label}</div>` : ''}
    `;
  }
}

customElements.define('color-chip', ColorChip);
