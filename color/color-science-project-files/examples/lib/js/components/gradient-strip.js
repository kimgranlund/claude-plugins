// <gradient-strip from="..." to="..." space="oklab" hue-path="shorter"></gradient-strip>
//
// Renders a gradient on canvas, computed by linear interpolation in the named
// color space. Demonstrates the perceptual difference between spaces.
//
// Supported spaces: 'encoded-srgb' | 'linear-srgb' | 'oklab' | 'oklch' | 'cielab'
// from / to are encoded sRGB hex strings ("#ff0080") for ergonomic input.

import { setupCanvas, fromHex, toCssRgb } from '../utils.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as oklch from '../../dist/spaces/oklch.js';
import * as cielab from '../../dist/spaces/cielab.js';
import * as linInterp from '../../dist/interpolation/linear.js';
import * as mapping from '../../dist/gamut/mapping.js';

const SPACE_LABELS = {
  'encoded-srgb': 'Encoded sRGB (muddy mid-tones)',
  'linear-srgb': 'Linear sRGB (too bright mid)',
  'cielab': 'CIELAB (blue-purple drift)',
  'oklab': 'OKLab (perceptually uniform)',
  'oklch': 'OKLCh (preserves hue path)',
};

class GradientStrip extends HTMLElement {
  static get observedAttributes() { return ['from', 'to', 'space', 'hue-path', 'samples']; }

  connectedCallback() {
    this._build();
    this.render();
  }

  attributeChangedCallback() {
    if (this._canvas) this.render();
  }

  _build() {
    const space = this.getAttribute('space') || 'oklab';
    const label = SPACE_LABELS[space] || space;
    this.innerHTML = `
      <div class="strip-label"><strong>${space}</strong><span>${label}</span></div>
      <canvas></canvas>
    `;
    this._canvas = this.querySelector('canvas');
  }

  render() {
    if (!this._canvas) return;
    const w = this.offsetWidth || 600;
    const h = 56;
    const samples = parseInt(this.getAttribute('samples') || '128', 10);
    const space = this.getAttribute('space') || 'oklab';
    const huePath = this.getAttribute('hue-path') || 'shorter';

    const fromHex_ = this.getAttribute('from') || '#000000';
    const toHex_ = this.getAttribute('to') || '#ffffff';

    const a_encoded = fromHex(fromHex_);
    const b_encoded = fromHex(toHex_);
    const a_linear = srgbTransfer.decode(a_encoded);
    const b_linear = srgbTransfer.decode(b_encoded);
    const a_xyz = srgb.toXYZ(a_linear);
    const b_xyz = srgb.toXYZ(b_linear);

    // Build the sample colors per space; each rendered back to encoded sRGB.
    const colors = [];
    for (let i = 0; i < samples; i++) {
      const t = i / (samples - 1);
      let resultEncoded;

      switch (space) {
        case 'encoded-srgb': {
          // Naive interpolation in encoded space (the "muddy" case)
          const rgb = linInterp.lerpTuple(a_encoded, b_encoded, t);
          resultEncoded = rgb;
          break;
        }
        case 'linear-srgb': {
          const rgb = linInterp.lerpTuple(a_linear, b_linear, t);
          resultEncoded = srgbTransfer.encode(rgb);
          break;
        }
        case 'cielab': {
          const a_lab = cielab.fromXYZ(a_xyz);
          const b_lab = cielab.fromXYZ(b_xyz);
          const mid = linInterp.lerpCielab(a_lab, b_lab, t);
          const xyz_mid = cielab.toXYZ(mid);
          const lin = srgb.fromXYZ(xyz_mid);
          resultEncoded = srgbTransfer.encode(lin);
          break;
        }
        case 'oklch': {
          const a_lch = oklch.fromXYZ(a_xyz);
          const b_lch = oklch.fromXYZ(b_xyz);
          const mid = linInterp.lerpOklch(a_lch, b_lch, t, huePath);
          // Gamut-map for sRGB display
          const mapped = mapping.mapToSRGB(mid);
          resultEncoded = srgbTransfer.encode(mapped);
          break;
        }
        case 'oklab':
        default: {
          const a_lab = oklab.fromXYZ(a_xyz);
          const b_lab = oklab.fromXYZ(b_xyz);
          const mid = linInterp.lerpOklab(a_lab, b_lab, t);
          const xyz_mid = oklab.toXYZ(mid);
          const lin = srgb.fromXYZ(xyz_mid);
          resultEncoded = srgbTransfer.encode(lin);
          break;
        }
      }
      colors.push(resultEncoded);
    }

    // Render bands to canvas.
    const { ctx, w: cw, h: ch } = setupCanvas(this._canvas, w, h);
    const bw = cw / samples;
    for (let i = 0; i < samples; i++) {
      ctx.fillStyle = toCssRgb(colors[i]);
      ctx.fillRect(i * bw, 0, Math.ceil(bw) + 0.5, ch);
    }
  }
}

customElements.define('gradient-strip', GradientStrip);
