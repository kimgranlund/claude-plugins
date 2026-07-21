// <hue-wheel l="0.65" c="0.15"></hue-wheel>
//
// Three concentric rings at constant lightness, plotting hue around 360° in:
//   - OKLCh (outer ring)    — perceptually uniform
//   - HSL   (middle ring)   — RGB-cylindrical, distorts hue
//   - HCT   (inner ring)    — Material's perceptual space
//
// Same L (or L*-equivalent) per ring → makes the perceptual differences
// jump out: HSL "green" feels overly bright, HSL "blue" feels overly dark, etc.

import { setupCanvas } from '../utils.js';
import * as oklchSpace from '../../dist/spaces/oklch.js';
import * as oklabSpace from '../../dist/spaces/oklab.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import * as hslSpace from '../../dist/spaces/hsl.js';
import * as hctSpace from '../../dist/spaces/hct.js';

const RING_COUNT = 3;
const HUE_STEPS = 180;

function oklchToHex(L, C, hDeg) {
  const lab = oklchSpace.toOKLab([L, C, hDeg]);
  const xyz = oklabSpace.toXYZ(lab);
  const lin = srgbSpace.fromXYZ(xyz);
  const clamped = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(clamped);
  return [
    Math.round(enc[0] * 255),
    Math.round(enc[1] * 255),
    Math.round(enc[2] * 255),
  ];
}

function hslToHex(h, s, l) {
  // Use the HSL module: HSL → XYZ → linear sRGB → encoded.
  const xyz = hslSpace.toXYZ([h, s, l]);
  const lin = srgbSpace.fromXYZ(xyz);
  const clamped = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(clamped);
  return [
    Math.round(enc[0] * 255),
    Math.round(enc[1] * 255),
    Math.round(enc[2] * 255),
  ];
}

function hctToHex(h, c, t) {
  const xyz = hctSpace.toXYZ([h, c, t]);
  const lin = srgbSpace.fromXYZ(xyz);
  const clamped = [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
  const enc = srgbTransfer.encode(clamped);
  return [
    Math.round(enc[0] * 255),
    Math.round(enc[1] * 255),
    Math.round(enc[2] * 255),
  ];
}

class HueWheel extends HTMLElement {
  static get observedAttributes() { return ['l', 'c']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _mount() {
    this.innerHTML = `<canvas></canvas>
      <div class="wheel-legend" style="display:flex;gap:1rem;font-size:var(--text-xs);font-family:var(--font-mono);justify-content:center;margin-top:var(--s-3);color:var(--text-muted)">
        <span><span style="color:oklch(0.554 0.18 264)">●</span> OKLCh (outer)</span>
        <span><span style="color:oklch(0.620 0.18 150)">●</span> HCT (middle)</span>
        <span><span style="color:oklch(0.700 0.18 50)">●</span> HSL (inner)</span>
      </div>`;
    this._canvas = this.querySelector('canvas');
  }

  render() {
    if (!this._canvas) return;
    const L = parseFloat(this.getAttribute('l') ?? '0.65');
    const Cok = parseFloat(this.getAttribute('c') ?? '0.15');
    const size = Math.min(this.offsetWidth || 480, 560);
    const { ctx, w, h } = setupCanvas(this._canvas, size, size);
    ctx.clearRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2;
    const ringOuter = Math.min(w, h) * 0.46;
    const ringInner = ringOuter * 0.40;
    const ringThickness = (ringOuter - ringInner) / RING_COUNT;

    const tau = Math.PI * 2;
    const sliceAngle = tau / HUE_STEPS;

    // Rings: 0=outer (OKLCh), 1=middle (HCT), 2=inner (HSL)
    for (let r = 0; r < RING_COUNT; r++) {
      const rOut = ringOuter - r * ringThickness;
      const rIn = rOut - ringThickness + 1; // 1px gap

      for (let i = 0; i < HUE_STEPS; i++) {
        const hueDeg = (i / HUE_STEPS) * 360;
        let rgb;
        if (r === 0) {
          rgb = oklchToHex(L, Cok, hueDeg);
        } else if (r === 1) {
          // HCT: tone is on 0-100 scale, chroma roughly 0-150
          rgb = hctToHex(hueDeg, 50, L * 100);
        } else {
          rgb = hslToHex(hueDeg, 0.65, L);
        }
        ctx.fillStyle = `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;
        const a0 = -Math.PI / 2 + i * sliceAngle;
        const a1 = a0 + sliceAngle + 0.005; // tiny overlap to hide seams
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(a0) * rIn, cy + Math.sin(a0) * rIn);
        ctx.arc(cx, cy, rOut, a0, a1);
        ctx.lineTo(cx + Math.cos(a1) * rIn, cy + Math.sin(a1) * rIn);
        ctx.arc(cx, cy, rIn, a1, a0, true);
        ctx.closePath();
        ctx.fill();
      }
    }

    // Center label
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '12px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`L = ${L.toFixed(2)}`, cx, cy - 4);
    ctx.fillText(`C = ${Cok.toFixed(2)}`, cx, cy + 14);

    // Hue tick labels around the outer ring
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '10px ui-monospace, monospace';
    ctx.textAlign = 'center';
    for (let deg = 0; deg < 360; deg += 30) {
      const a = -Math.PI / 2 + (deg / 360) * tau;
      const lx = cx + Math.cos(a) * (ringOuter + 12);
      const ly = cy + Math.sin(a) * (ringOuter + 12) + 4;
      ctx.fillText(`${deg}°`, lx, ly);
    }
  }
}

customElements.define('hue-wheel', HueWheel);
