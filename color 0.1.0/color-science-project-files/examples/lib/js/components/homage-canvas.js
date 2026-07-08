// <homage-canvas outer="..." mid1="..." mid2="..." inner="..." squares="4"></homage-canvas>
//
// Renders Albers' Homage to the Square composition: 3 or 4 nested squares,
// centered horizontally, offset toward the bottom of the frame. Proportions
// approximate Albers' canonical 4-square format.

class HomageCanvas extends HTMLElement {
  static get observedAttributes() { return ['outer', 'mid1', 'mid2', 'inner', 'squares']; }

  connectedCallback() { this._mount(); this.render(); }
  attributeChangedCallback() { if (this._frame) this.render(); }

  _mount() {
    this.innerHTML = `<div class="hc-frame"></div>`;
    this._frame = this.querySelector('.hc-frame');
  }

  render() {
    const outer = this.getAttribute('outer') || 'oklch(0.42 0.10 264)';
    const mid1  = this.getAttribute('mid1')  || 'oklch(0.56 0.13 264)';
    const mid2  = this.getAttribute('mid2')  || 'oklch(0.72 0.13 264)';
    const inner = this.getAttribute('inner') || 'oklch(0.88 0.05 264)';
    const squares = this.getAttribute('squares') === '3' ? 3 : 4;

    // Albers proportions: width-% and top-% of the outer frame.
    // Bottom-heavy: top margin grows faster than centered would place each square.
    const layout4 = [
      { w: 100, t:  0 },
      { w:  78, t: 12 },
      { w:  56, t: 26 },
      { w:  32, t: 44 },
    ];
    const layout3 = [
      { w: 100, t:  0 },
      { w:  70, t: 16 },
      { w:  40, t: 38 },
    ];
    const layout = squares === 4 ? layout4 : layout3;
    const colors = squares === 4 ? [outer, mid1, mid2, inner] : [outer, mid1, inner];

    this._frame.innerHTML = layout.map((L, i) =>
      `<div class="hc-square" style="background:${colors[i]};width:${L.w}%;top:${L.t}%;"></div>`
    ).join('');
  }
}

customElements.define('homage-canvas', HomageCanvas);
