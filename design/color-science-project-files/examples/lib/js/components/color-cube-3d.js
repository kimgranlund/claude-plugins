// <color-cube-3d space="oklab"></color-cube-3d>
//
// Render the sRGB unit cube as a 3D wireframe, with each vertex/edge sample
// transformed into a target perceptual space (OKLab or CIELAB). Drag to rotate.
// The cube morphs because perceptual spaces aren't linear in sRGB — the visual
// effect demonstrates the curvature.

import { setupCanvas } from '../utils.js';
import * as oklab from '../../dist/spaces/oklab.js';
import * as cielab from '../../dist/spaces/cielab.js';
import * as srgb from '../../dist/spaces/srgb.js';
import * as srgbTransfer from '../../dist/transfer/srgb.js';

const SAMPLES_PER_EDGE = 14;

// Cube vertices in sRGB byte coords.
const VERTICES = [
  [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
  [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
];
const EDGES = [
  [0, 1], [1, 2], [2, 3], [3, 0],
  [4, 5], [5, 6], [6, 7], [7, 4],
  [0, 4], [1, 5], [2, 6], [3, 7],
];

function transformPoint(encR, encG, encB, space) {
  const lin = srgbTransfer.decode([encR, encG, encB]);
  const xyz = srgb.toXYZ(lin);
  if (space === 'oklab') {
    const [L, a, b] = oklab.fromXYZ(xyz);
    // Map to a common viewing box: L is 0..1, a/b ~ -0.4..0.4. Center on origin.
    return [a * 1.6, L - 0.5, b * 1.6];
  } else if (space === 'cielab') {
    const [L, a, b] = cielab.fromXYZ(xyz);
    return [(a / 128), (L / 100) - 0.5, (b / 128)];
  } else {
    // Linear sRGB cube — for the "before" view, place corners at ±0.5
    return [encR - 0.5, encG - 0.5, encB - 0.5];
  }
}

function project(point, rotX, rotY, scale, w, h) {
  const cx = Math.cos(rotY), sx = Math.sin(rotY);
  const cy = Math.cos(rotX), sy = Math.sin(rotX);
  // Rotate around Y first, then X.
  let x = point[0], y = point[1], z = point[2];
  let x1 = x * cx + z * sx;
  let z1 = -x * sx + z * cx;
  let y1 = y * cy - z1 * sy;
  let z2 = y * sy + z1 * cy;
  // Project orthographic.
  return [
    w / 2 + x1 * scale,
    h / 2 - y1 * scale,
    z2,
  ];
}

function encodedHex(r, g, b) {
  return '#' + [r, g, b].map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join('');
}

class ColorCube3D extends HTMLElement {
  static get observedAttributes() { return ['space']; }

  connectedCallback() {
    this._rotX = 0.3;
    this._rotY = -0.5;
    this._dragging = false;
    this._mount();
    this.render();
    this._addDragHandlers();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _mount() {
    this.innerHTML = `<canvas class="cube-canvas"></canvas>
      <p class="cube-hint" style="color:var(--text-muted);font-size:var(--text-xs);margin-top:var(--s-2);">Drag the cube to rotate.</p>`;
    this._canvas = this.querySelector('.cube-canvas');
  }

  _addDragHandlers() {
    let lastX = 0, lastY = 0;
    this._canvas.addEventListener('pointerdown', (e) => {
      this._dragging = true;
      lastX = e.clientX; lastY = e.clientY;
      this._canvas.setPointerCapture(e.pointerId);
    });
    this._canvas.addEventListener('pointerup', (e) => {
      this._dragging = false;
      try { this._canvas.releasePointerCapture(e.pointerId); } catch (err) {}
    });
    this._canvas.addEventListener('pointermove', (e) => {
      if (!this._dragging) return;
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      lastX = e.clientX; lastY = e.clientY;
      this._rotY += dx * 0.01;
      this._rotX += dy * 0.01;
      this.render();
    });
  }

  render() {
    if (!this._canvas) return;
    const space = this.getAttribute('space') || 'oklab';
    const size = Math.min(this.offsetWidth || 500, 560);
    const { ctx, w, h } = setupCanvas(this._canvas, size, size);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);
    const scale = size * 0.42;

    // Sample edges.
    const allDots = []; // { proj, hex, depth }
    for (const [aIdx, bIdx] of EDGES) {
      const A = VERTICES[aIdx], B = VERTICES[bIdx];
      for (let i = 0; i <= SAMPLES_PER_EDGE; i++) {
        const t = i / SAMPLES_PER_EDGE;
        const encR = A[0] + (B[0] - A[0]) * t;
        const encG = A[1] + (B[1] - A[1]) * t;
        const encB = A[2] + (B[2] - A[2]) * t;
        const pt = transformPoint(encR, encG, encB, space);
        const proj = project(pt, this._rotX, this._rotY, scale, w, h);
        allDots.push({
          proj,
          hex: encodedHex(encR, encG, encB),
          depth: proj[2],
        });
      }
    }
    // Sort by depth (painter's algorithm).
    allDots.sort((a, b) => a.depth - b.depth);
    // Draw each as a small disc.
    for (const d of allDots) {
      ctx.fillStyle = d.hex;
      ctx.beginPath();
      ctx.arc(d.proj[0], d.proj[1], 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Axis hint.
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '11px ui-monospace, monospace';
    ctx.fillText(space === 'oklab' ? 'sRGB cube → OKLab (curved)' :
                 space === 'cielab' ? 'sRGB cube → CIELAB (curved)' :
                 'sRGB cube (linear, no transform)', 10, h - 10);
  }
}

customElements.define('color-cube-3d', ColorCube3D);
