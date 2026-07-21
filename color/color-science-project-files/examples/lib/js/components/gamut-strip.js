// <gamut-strip oklch="0.7,0.35,29" target="srgb"></gamut-strip>
//
// Display an out-of-gamut OKLCh color rendered via four gamut-mapping strategies
// side-by-side: naive-clip, chroma-compression (CSS Color 4), MINDE / ΔE-min,
// and OKLCh-direct (cusp projection).
//
// Each strip shows the rendered swatch + the resulting OKLCh + hex.

import { toHex, toCssOklch, fmt } from '../utils.js';
import * as oklchSpace from '../../dist/spaces/oklch.js';
import * as oklabSpace from '../../dist/spaces/oklab.js';
import * as srgbSpace from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import {
  mapToGamutOklch,
  inGamutSRGB,
  clipNaive,
} from '../../dist/gamut/mapping.js';
import {
  M_XYZ_TO_SRGB,
  peakC,
} from '../../dist/gamut/oklch-peak.js';
import { findCuspSRGBFromHueDeg } from '../../dist/gamut/cusp.js';
import { mulMat3Vec3 } from '../../dist/types.js';

function oklchToLinearSRGB(c) {
  const lab = oklchSpace.toOKLab(c);
  const xyz = oklabSpace.toXYZ(lab);
  return mulMat3Vec3(M_XYZ_TO_SRGB, xyz);
}

function clampLin(lin) {
  return [
    Math.max(0, Math.min(1, lin[0])),
    Math.max(0, Math.min(1, lin[1])),
    Math.max(0, Math.min(1, lin[2])),
  ];
}

function encodedToHex(enc) {
  return toHex(enc);
}

// ─── Mapping strategies ─────────────────────────────────────────────────────

// 1. Naive per-channel clip.
function strategyClip(oklch) {
  const lin = oklchToLinearSRGB(oklch);
  const clipped = clipNaive(lin);
  const enc = srgbTransfer.encode(clipped);
  // Compute back-OKLCh of the clipped color for display
  const back = oklchSpace.fromXYZ(srgbSpace.toXYZ(clipped));
  return { hex: encodedToHex(enc), out: back };
}

// 2. CSS Color 4 chroma reduction (this is what `mapToGamutOklch` implements).
function strategyChromaReduce(oklch) {
  const mapped = mapToGamutOklch(oklch, M_XYZ_TO_SRGB, inGamutSRGB);
  const lin = oklchToLinearSRGB(mapped);
  const clipped = clipNaive(lin);
  const enc = srgbTransfer.encode(clipped);
  return { hex: encodedToHex(enc), out: mapped };
}

// 3. MINDE — minimum ΔE to a valid sRGB color. Approximated by binary-search
// chroma reduction OR L adjustment, picking whichever produces lower ΔE_ok.
// For an MVP demo, we compose the chroma-reduce result with a small lightness
// nudge toward the cusp's L, weighted by how far we had to reduce chroma.
function strategyMinde(oklch) {
  const [L, C, h] = oklch;
  const cusp = findCuspSRGBFromHueDeg(h);
  const cL = cusp[0], cC = cusp[1];
  // Reduce chroma proportionally to where the cusp lives.
  const targetC = Math.min(cC, peakC(L, h, M_XYZ_TO_SRGB, 28, 0.4));
  // Blend toward cusp L by ratio of reduction.
  const reduction = C > 0 ? (C - targetC) / C : 0;
  const blend = Math.min(0.4, Math.max(0, reduction));
  const newL = L * (1 - blend) + cL * blend;
  // Recompute valid chroma at the adjusted L.
  const finalC = peakC(newL, h, M_XYZ_TO_SRGB, 28, 0.4);
  const out = [newL, Math.min(targetC, finalC), h];
  const lin = oklchToLinearSRGB(out);
  const enc = srgbTransfer.encode(clampLin(lin));
  return { hex: encodedToHex(enc), out };
}

// 4. Cusp projection — straight line from source toward the cusp until in gamut.
function strategyCuspProject(oklch) {
  const [L, C, h] = oklch;
  const cusp = findCuspSRGBFromHueDeg(h);
  const cL = cusp[0], cC = cusp[1];
  // Param t ∈ [0, 1]: t=0 is source, t=1 is cusp.
  let lo = 0, hi = 1;
  for (let i = 0; i < 32; i++) {
    const t = (lo + hi) / 2;
    const Lt = L + (cL - L) * t;
    const Ct = C + (cC - C) * t;
    if (inGamutSRGB([Lt, Ct, h])) hi = t; else lo = t;
  }
  // Use 'hi' (just inside the gamut).
  const t = hi;
  const out = [L + (cL - L) * t, C + (cC - C) * t, h];
  const lin = oklchToLinearSRGB(out);
  const enc = srgbTransfer.encode(clampLin(lin));
  return { hex: encodedToHex(enc), out };
}

const STRATEGIES = [
  { id: 'clip',    label: 'naive clip',      note: 'clamp each linear-RGB channel — shifts hue',  fn: strategyClip },
  { id: 'css4',    label: 'CSS Color 4',     note: 'reduce chroma in OKLCh — W3C standard',       fn: strategyChromaReduce },
  { id: 'minde',   label: 'min-ΔE blend',     note: 'reduce chroma + nudge L toward cusp',         fn: strategyMinde },
  { id: 'cusp',    label: 'cusp projection', note: 'line from source toward gamut cusp',          fn: strategyCuspProject },
];

class GamutStrip extends HTMLElement {
  static get observedAttributes() { return ['oklch', 'target']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._root) this.render(); }

  _mount() {
    this.innerHTML = `<div class="gamut-strip"></div>`;
    this._root = this.querySelector('.gamut-strip');
  }

  render() {
    const attr = this.getAttribute('oklch') || '0.7,0.35,29';
    const parts = attr.split(',').map(s => parseFloat(s.trim()));
    const source = [parts[0] || 0.7, parts[1] || 0.35, parts[2] || 29];
    const sourceInGamut = inGamutSRGB(source);

    this._root.innerHTML = STRATEGIES.map(s => {
      const { hex, out } = s.fn(source);
      return `
        <div class="gamut-cell">
          <div class="gamut-swatch" style="background:${hex}"></div>
          <div class="gamut-info">
            <div class="gamut-label">${s.label}</div>
            <div class="gamut-note">${s.note}</div>
            <div class="gamut-result">
              <code>${toCssOklch(out)}</code><br>
              <code>${hex}</code>
            </div>
          </div>
        </div>
      `;
    }).join('');

    if (sourceInGamut) {
      this._root.insertAdjacentHTML('beforeend',
        `<p class="gamut-already-in"><strong>Note:</strong> this color is already in sRGB — all strategies converge.</p>`);
    }
  }
}

customElements.define('gamut-strip', GamutStrip);
