// <transparency-composer color-a="#3366cc" color-b="#cc6633" color-c="#888888" auto-mode="none"></transparency-composer>
//
// Two overlapping rectangles A and B with an intersection region C. When C
// is the OKLab midpoint of A and B, the eye reads it as transparency. When
// C is the RGB midpoint, the eye sees opaque shapes that don't blend.

import * as oklab from '../../dist/spaces/oklab.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

function fromHex(hex) {
  hex = hex.replace('#', '');
  return [
    parseInt(hex.slice(0, 2), 16) / 255,
    parseInt(hex.slice(2, 4), 16) / 255,
    parseInt(hex.slice(4, 6), 16) / 255,
  ];
}
function toHex(enc) {
  const b = (v) => Math.round(Math.max(0, Math.min(1, v)) * 255).toString(16).padStart(2, '0');
  return '#' + b(enc[0]) + b(enc[1]) + b(enc[2]);
}

function oklabMid(aHex, bHex) {
  const aLab = oklab.fromXYZ(srgb.toXYZ(srgbTransfer.decode(fromHex(aHex))));
  const bLab = oklab.fromXYZ(srgb.toXYZ(srgbTransfer.decode(fromHex(bHex))));
  const mid = [(aLab[0]+bLab[0])/2, (aLab[1]+bLab[1])/2, (aLab[2]+bLab[2])/2];
  const lin = srgb.fromXYZ(oklab.toXYZ(mid));
  return { hex: toHex(srgbTransfer.encode([
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ])), lab: mid };
}

function rgbMid(aHex, bHex) {
  const a = fromHex(aHex), b = fromHex(bHex);
  return toHex([(a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2]);
}

function deltaE(labA, labB) {
  return Math.sqrt(
    Math.pow(labA[0]-labB[0], 2) +
    Math.pow(labA[1]-labB[1], 2) +
    Math.pow(labA[2]-labB[2], 2)
  );
}

class TransparencyComposer extends HTMLElement {
  static get observedAttributes() { return ['color-a', 'color-b', 'color-c', 'auto-mode']; }

  connectedCallback() { this._mount(); this.render(); }
  attributeChangedCallback() { if (this._stage) this.render(); }

  _mount() {
    this.innerHTML = `<div class="tc-host">
      <div class="tc-stage">
        <div class="tc-rect tc-rect-a"></div>
        <div class="tc-rect tc-rect-b"></div>
        <div class="tc-rect tc-rect-c"></div>
      </div>
      <div class="tc-readout"></div>
    </div>`;
    this._stage = this.querySelector('.tc-stage');
    this._rectA = this.querySelector('.tc-rect-a');
    this._rectB = this.querySelector('.tc-rect-b');
    this._rectC = this.querySelector('.tc-rect-c');
    this._readout = this.querySelector('.tc-readout');
  }

  render() {
    const aHex = this.getAttribute('color-a') || '#3366cc';
    const bHex = this.getAttribute('color-b') || '#cc6633';
    const cHexAttr = this.getAttribute('color-c') || '#888888';
    const auto = this.getAttribute('auto-mode') || 'none';

    const okMid  = oklabMid(aHex, bHex);
    const rgbMidHex = rgbMid(aHex, bHex);

    let actualC = cHexAttr;
    if (auto === 'oklab') actualC = okMid.hex;
    else if (auto === 'rgb') actualC = rgbMidHex;

    // ΔE_ok between actualC and the OKLab midpoint.
    const cLab = oklab.fromXYZ(srgb.toXYZ(srgbTransfer.decode(fromHex(actualC))));
    const dE = deltaE(cLab, okMid.lab);
    const transparent = dE < 0.04;

    this._rectA.style.background = aHex;
    this._rectB.style.background = bHex;
    this._rectC.style.background = actualC;

    this._readout.innerHTML = `
      <div class="tc-row">A <code>${aHex}</code> · B <code>${bHex}</code> · C <code>${actualC}</code></div>
      <div class="tc-row">OKLab midpoint: <code>${okMid.hex}</code> · RGB midpoint: <code>${rgbMidHex}</code></div>
      <div class="tc-row">ΔE<sub>ok</sub>(C, OKLab-mid) = <strong>${dE.toFixed(4)}</strong> ${transparent ? '<span class="pill pass">reads as transparent</span>' : '<span class="pill warn">reads as opaque</span>'}</div>`;
  }
}

customElements.define('transparency-composer', TransparencyComposer);
