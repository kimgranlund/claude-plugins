// <gamut-envelope hue="29" show="srgb,p3,rec2020"></gamut-envelope>
//
// Canvas plot of the L × C envelope at a fixed OKLCh hue.
//
// Visualization strategy:
//   1. Per-pixel fill — actual OKLCh color rendered to the display (clamped to
//      sRGB since the display is sRGB). Pixels that are only inside a wider
//      gamut than sRGB are dimmed so the user can see the gamut transitions.
//   2. Stroked boundary curves on top — one per selected gamut, using each
//      gamut's representative color.
//   3. Black-bordered dot at the sRGB cusp (peak chroma at this hue).
//   4. Optional pick marker.
//
// Performance: samples at RES × RES (200 × 200 default) then drawImage-upscales
// to the actual canvas — avoids DPR/imageData mismatch and is fast.

import { setupCanvas } from '../utils.js';
import * as oklchSpace from '../../dist/spaces/oklch.js';
import * as oklabSpace from '../../dist/spaces/oklab.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';
import { findCuspSRGBFromHueDeg } from '../../dist/gamut/cusp.js';
import {
  M_XYZ_TO_SRGB,
  M_XYZ_TO_P3,
  M_XYZ_TO_REC2020,
  inGamut,
  peakC,
} from '../../dist/gamut/oklch-peak.js';
import { mulMat3Vec3 } from '../../dist/types.js';

const GAMUTS = {
  srgb:    { matrix: M_XYZ_TO_SRGB,    color: 'oklch(0.554 0.180 264)', label: 'sRGB' },
  p3:      { matrix: M_XYZ_TO_P3,      color: 'oklch(0.620 0.180 150)', label: 'Display P3' },
  rec2020: { matrix: M_XYZ_TO_REC2020, color: 'oklch(0.700 0.180  50)', label: 'Rec.2020' },
};

const C_MAX = 0.4;       // OKLCh chroma axis upper bound
const RES_CAP = 800;     // upper bound on samples-per-axis (perf cap)

function readCssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

class GamutEnvelope extends HTMLElement {
  static get observedAttributes() { return ['hue', 'show', 'pick']; }

  connectedCallback() {
    this._build();
    this.render();
  }

  attributeChangedCallback() {
    if (this._canvas) this.render();
  }

  _build() {
    const showAttr = this.getAttribute('show') || 'srgb,p3,rec2020';
    const showList = showAttr.split(',').map(s => s.trim()).filter(s => GAMUTS[s]);
    const legend = showList.map(s =>
      `<span class="legend-item">
        <span class="legend-swatch" style="background:${GAMUTS[s].color}"></span>
        ${GAMUTS[s].label}
       </span>`
    ).join('');
    this.innerHTML = `
      <canvas tabindex="0" role="application" aria-label="OKLCh gamut envelope picker — click, drag, or use arrow keys to set lightness and chroma"></canvas>
      <div class="legend">${legend}</div>
    `;
    this._canvas = this.querySelector('canvas');
    // Pointer-based drag (click is a degenerate case). Pointer capture keeps
    // updates flowing during a drag even if the cursor leaves the canvas.
    this._dragging = false;
    this._canvas.addEventListener('pointerdown', e => {
      e.preventDefault();
      this._dragging = true;
      try { this._canvas.setPointerCapture(e.pointerId); } catch {}
      this._handlePoint(e);
    });
    this._canvas.addEventListener('pointermove', e => {
      if (this._dragging) this._handlePoint(e);
    });
    const endDrag = e => {
      this._dragging = false;
      try { this._canvas.releasePointerCapture(e.pointerId); } catch {}
    };
    this._canvas.addEventListener('pointerup', endDrag);
    this._canvas.addEventListener('pointercancel', endDrag);
    this._canvas.addEventListener('keydown', e => this._handleKey(e));
  }

  _handlePoint(e) {
    const rect = this._canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = 1 - (e.clientY - rect.top) / rect.height;
    const L = Math.max(0, Math.min(1, y));
    const C = Math.max(0, Math.min(C_MAX, x * C_MAX));
    const hDeg = parseFloat(this.getAttribute('hue') || '29');
    this.dispatchEvent(new CustomEvent('pick', {
      detail: { L, C, hDeg, oklch: [L, C, hDeg] },
    }));
  }

  _handleKey(e) {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;
    e.preventDefault();
    const pickAttr = this.getAttribute('pick') || '0.5,0.1';
    const parts = pickAttr.split(',').map(Number);
    let L = parts[0], C = parts[1];
    const step = e.shiftKey ? 0.1 : 0.01;
    if (e.key === 'ArrowLeft')  C = Math.max(0,     C - C_MAX * step);
    if (e.key === 'ArrowRight') C = Math.min(C_MAX, C + C_MAX * step);
    if (e.key === 'ArrowUp')    L = Math.min(1,     L + step);
    if (e.key === 'ArrowDown')  L = Math.max(0,     L - step);
    const hDeg = parseFloat(this.getAttribute('hue') || '29');
    this.dispatchEvent(new CustomEvent('pick', {
      detail: { L, C, hDeg, oklch: [L, C, hDeg] },
    }));
  }

  render() {
    if (!this._canvas) return;
    const size = Math.min(this.offsetWidth || 500, 600);
    const { ctx, w, h } = setupCanvas(this._canvas, size, size);
    const hDeg = parseFloat(this.getAttribute('hue') || '29');
    const showList = (this.getAttribute('show') || 'srgb,p3,rec2020')
      .split(',').map(s => s.trim()).filter(s => GAMUTS[s]);

    // ─── Background ─────────────────────────────────────────────────────────
    ctx.fillStyle = readCssVar('--bg-card', '#ffffff');
    ctx.fillRect(0, 0, w, h);

    // ─── Per-pixel gamut fill on an off-screen RES × RES canvas ─────────────
    // Sample resolution matches the canvas buffer (1× DPR) for crisp output
    // without supersampling cost. Capped at RES_CAP for perf on huge displays.
    const dpr = window.devicePixelRatio || 1;
    const RES = Math.min(Math.round(w * dpr), RES_CAP);
    const tmp = document.createElement('canvas');
    tmp.width = RES;
    tmp.height = RES;
    const tmpCtx = tmp.getContext('2d');
    const imgData = tmpCtx.createImageData(RES, RES);
    const data = imgData.data;

    // Pre-compute the per-gamut "dim factor". sRGB renders at full brightness;
    // pixels only reachable in wider gamuts are dimmed so the gamut boundary
    // is visible at a glance.
    const DIM = { srgb: 1.0, p3: 0.62, rec2020: 0.38 };
    const inSrgb = showList.includes('srgb');
    const inP3 = showList.includes('p3');
    const inRec = showList.includes('rec2020');

    for (let py = 0; py < RES; py++) {
      for (let px = 0; px < RES; px++) {
        const L = 1 - py / (RES - 1);
        const C = (px / (RES - 1)) * C_MAX;

        // OKLCh → OKLab → XYZ (compute once)
        const lab = oklchSpace.toOKLab([L, C, hDeg]);
        const xyz = oklabSpace.toXYZ(lab);

        // Find the narrowest selected gamut that contains this point.
        let dim = 0;
        if (inSrgb && inGamut(mulMat3Vec3(M_XYZ_TO_SRGB, xyz))) dim = DIM.srgb;
        else if (inP3 && inGamut(mulMat3Vec3(M_XYZ_TO_P3, xyz))) dim = DIM.p3;
        else if (inRec && inGamut(mulMat3Vec3(M_XYZ_TO_REC2020, xyz))) dim = DIM.rec2020;

        const i = (py * RES + px) * 4;
        if (dim === 0) {
          // Out of all selected gamuts — transparent
          data[i + 3] = 0;
          continue;
        }

        // Render the *actual* color via sRGB (the display). Clamp out-of-sRGB
        // components — we couldn't show them correctly anyway.
        const srgbLin = mulMat3Vec3(M_XYZ_TO_SRGB, xyz);
        const r = Math.max(0, Math.min(1, srgbLin[0]));
        const g = Math.max(0, Math.min(1, srgbLin[1]));
        const b = Math.max(0, Math.min(1, srgbLin[2]));
        const enc = srgbTransfer.encode([r, g, b]);
        data[i]     = Math.round(enc[0] * 255 * dim);
        data[i + 1] = Math.round(enc[1] * 255 * dim);
        data[i + 2] = Math.round(enc[2] * 255 * dim);
        data[i + 3] = 255;
      }
    }
    tmpCtx.putImageData(imgData, 0, 0);

    // Upscale to the main canvas — drawImage *does* respect the DPR transform.
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(tmp, 0, 0, w, h);

    // ─── Gamut boundary curves ──────────────────────────────────────────────
    // For each selected gamut, plot peakC(L, h) as L sweeps 0 → 1.
    const BOUNDARY_SAMPLES = 96;
    for (const key of showList) {
      const { matrix, color } = GAMUTS[key];
      ctx.beginPath();
      const cMax = key === 'rec2020' ? 0.5 : 0.4;
      for (let i = 0; i <= BOUNDARY_SAMPLES; i++) {
        const L = i / BOUNDARY_SAMPLES;
        const Cmax = peakC(L, hDeg, matrix, 28, cMax);
        const x = (Cmax / C_MAX) * w;
        const y = (1 - L) * h;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // ─── sRGB cusp marker ──────────────────────────────────────────────────
    if (showList.includes('srgb')) {
      const cusp = findCuspSRGBFromHueDeg(hDeg);
      const cx = (cusp[1] / C_MAX) * w;
      const cy = (1 - cusp[0]) * h;
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#000';
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // ─── Axis labels ───────────────────────────────────────────────────────
    const labelColor = readCssVar('--text-muted', '#888');
    ctx.fillStyle = labelColor;
    ctx.font = '11px ui-monospace, monospace';
    ctx.fillText('L=0', 4, h - 4);
    ctx.fillText('L=1', 4, 14);
    ctx.fillText('C=0', 4, h / 2 - 4);
    ctx.fillText(`C=${C_MAX}`, w - 36, h / 2 - 4);
    ctx.fillText(`h=${hDeg.toFixed(1)}°`, w - 70, 14);

    // ─── Pick marker ───────────────────────────────────────────────────────
    const pick = this.getAttribute('pick');
    if (pick) {
      const parts = pick.split(',').map(Number);
      const pL = parts[0], pC = parts[1];
      const mx = (pC / C_MAX) * w;
      const my = (1 - pL) * h;
      ctx.beginPath();
      ctx.arc(mx, my, 7, 0, Math.PI * 2);
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }
}

customElements.define('gamut-envelope', GamutEnvelope);
