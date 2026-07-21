// <chip-composer
//   chip-a="#888" ground-a="#1a1a1a"
//   chip-b="#888" ground-b="#eeeeee"
//   label-a="dark surround" label-b="light surround"
//   reveal="false"></chip-composer>
//
// Workhorse for Albers' one-color-on-two-grounds exercises. Renders two
// half-stages side-by-side, each with a chip centered on a colored ground.
// Toggling `reveal="true"` shows the two chips stripped of context for
// comparison.

class ChipComposer extends HTMLElement {
  static get observedAttributes() {
    return ['chip-a', 'chip-b', 'ground-a', 'ground-b', 'label-a', 'label-b', 'reveal'];
  }

  connectedCallback() { this._mount(); this.render(); }
  attributeChangedCallback() { if (this._halvesEl) this.render(); }

  _mount() {
    this.innerHTML = `
      <div class="cc-host">
        <div class="cc-halves"></div>
        <div class="cc-reveal" hidden>
          <div class="cc-reveal-label">stripped of context:</div>
          <div class="cc-reveal-row">
            <div class="cc-reveal-chip cc-reveal-a"></div>
            <div class="cc-reveal-chip cc-reveal-b"></div>
          </div>
          <div class="cc-reveal-hex"></div>
        </div>
      </div>`;
    this._halvesEl = this.querySelector('.cc-halves');
    this._revealEl = this.querySelector('.cc-reveal');
    this._revealA  = this.querySelector('.cc-reveal-a');
    this._revealB  = this.querySelector('.cc-reveal-b');
    this._revealH  = this.querySelector('.cc-reveal-hex');
  }

  render() {
    const chipA   = this.getAttribute('chip-a')   || '#888888';
    const chipB   = this.getAttribute('chip-b')   || '#888888';
    const groundA = this.getAttribute('ground-a') || '#1a1a1a';
    const groundB = this.getAttribute('ground-b') || '#eeeeee';
    const labelA  = this.getAttribute('label-a')  || '';
    const labelB  = this.getAttribute('label-b')  || '';
    const reveal  = this.getAttribute('reveal') === 'true';

    this._halvesEl.innerHTML = `
      <div class="cc-half" style="background:${groundA}">
        <div class="cc-chip" style="background:${chipA}"></div>
        ${labelA ? `<div class="cc-label">${labelA}</div>` : ''}
      </div>
      <div class="cc-half" style="background:${groundB}">
        <div class="cc-chip" style="background:${chipB}"></div>
        ${labelB ? `<div class="cc-label">${labelB}</div>` : ''}
      </div>`;

    this._revealA.style.background = chipA;
    this._revealB.style.background = chipB;
    const same = chipA.toLowerCase() === chipB.toLowerCase();
    this._revealH.innerHTML = same
      ? `Both chips: <strong>${chipA}</strong> — physically identical.`
      : `Left: <strong>${chipA}</strong> · Right: <strong>${chipB}</strong>`;
    this._revealEl.hidden = !reveal;
  }
}

customElements.define('chip-composer', ChipComposer);
