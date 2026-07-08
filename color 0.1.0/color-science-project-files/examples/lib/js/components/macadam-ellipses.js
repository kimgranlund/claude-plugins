// <macadam-ellipses scale="10"></macadam-ellipses>
//
// Plot MacAdam's 25 just-noticeable-difference ellipses on the CIE 1931 xy
// chromaticity diagram. Each ellipse encloses the region where humans cannot
// distinguish the colors from the ellipse center. Ellipses are massively
// non-uniform in size — green ellipses are ~10× larger than blue ellipses —
// which is exactly why CIE xy is a poor perceptual metric and why OKLab and
// CIELAB exist.
//
// Data: David L. MacAdam (1942), "Visual sensitivities to color differences
// in daylight," J. Opt. Soc. Am. 32(5), 247-274. Values reproduced from the
// classical secondary literature; published widely.

import { setupCanvas } from '../utils.js';

// 25 MacAdam ellipses: [center_x, center_y, semi-major-a, semi-minor-b, angle-deg]
// Note: original sizes are 1× JND; the canonical visualization shows 10× for
// visibility. This component lets the caller adjust the scale factor.
const MACADAM = [
  [0.160, 0.057, 0.00085, 0.00035,  62.5],
  [0.187, 0.118, 0.00220, 0.00055,  77.0],
  [0.253, 0.125, 0.00255, 0.00080,  55.5],
  [0.150, 0.680, 0.00500, 0.00150, 105.0],
  [0.131, 0.521, 0.00460, 0.00190, 112.5],
  [0.212, 0.550, 0.00580, 0.00200, 100.0],
  [0.258, 0.450, 0.00510, 0.00200,  92.0],
  [0.152, 0.365, 0.00400, 0.00150, 110.0],
  [0.280, 0.385, 0.00380, 0.00150,  75.5],
  [0.380, 0.498, 0.00440, 0.00120,  70.0],
  [0.160, 0.200, 0.00210, 0.00095,  77.0],
  [0.228, 0.250, 0.00310, 0.00090,  86.0],
  [0.305, 0.323, 0.00230, 0.00090,  59.5],
  [0.385, 0.393, 0.00380, 0.00160,  64.5],
  [0.472, 0.399, 0.00320, 0.00140,  72.5],
  [0.527, 0.350, 0.00260, 0.00130,  74.0],
  [0.475, 0.300, 0.00290, 0.00110,  69.5],
  [0.510, 0.236, 0.00240, 0.00120,  56.5],
  [0.596, 0.283, 0.00260, 0.00130,  58.0],
  [0.344, 0.284, 0.00230, 0.00090,  60.0],
  [0.390, 0.237, 0.00250, 0.00100,  47.0],
  [0.441, 0.198, 0.00280, 0.00095,  44.5],
  [0.278, 0.223, 0.00240, 0.00055,  37.5],
  [0.300, 0.163, 0.00290, 0.00060,  20.0],
  [0.365, 0.153, 0.00360, 0.00080,  50.0],
];

const SPECTRAL_LOCUS = [
  [0.1741, 0.0050], [0.1738, 0.0049], [0.1733, 0.0048], [0.1726, 0.0048],
  [0.1714, 0.0051], [0.1689, 0.0069], [0.1644, 0.0109], [0.1566, 0.0177],
  [0.1440, 0.0297], [0.1241, 0.0578], [0.0913, 0.1327], [0.0454, 0.2950],
  [0.0082, 0.5384], [0.0139, 0.7502], [0.0743, 0.8338], [0.1547, 0.8059],
  [0.2296, 0.7543], [0.3016, 0.6923], [0.3731, 0.6245], [0.4441, 0.5547],
  [0.5125, 0.4866], [0.5752, 0.4242], [0.6270, 0.3725], [0.6658, 0.3340],
  [0.6915, 0.3083], [0.7079, 0.2920], [0.7190, 0.2809], [0.7260, 0.2740],
  [0.7300, 0.2700], [0.7320, 0.2680], [0.7334, 0.2666], [0.7344, 0.2656],
  [0.7347, 0.2653],
];

const SRGB_TRIANGLE = [[0.6400, 0.3300], [0.3000, 0.6000], [0.1500, 0.0600]];

const X_RANGE = [0, 0.8];
const Y_RANGE = [0, 0.9];

class MacadamEllipses extends HTMLElement {
  static get observedAttributes() { return ['scale']; }

  connectedCallback() {
    this._mount();
    this.render();
  }

  attributeChangedCallback() { if (this._canvas) this.render(); }

  _mount() {
    this.innerHTML = `<canvas class="macadam-canvas"></canvas>
      <div class="macadam-legend" style="color:var(--text-muted);font-size:var(--text-xs);margin-top:var(--s-2);">
        Each ellipse encloses a "just-noticeable difference" region — the colors
        inside look identical to a trained observer. Shown at <strong>10× actual
        size</strong> by default for visibility (real ellipses are tiny).
      </div>`;
    this._canvas = this.querySelector('.macadam-canvas');
  }

  render() {
    const scale = parseFloat(this.getAttribute('scale') ?? '10');
    const wCss = Math.min(this.offsetWidth || 640, 760);
    const hCss = Math.round(wCss * (Y_RANGE[1] / X_RANGE[1]));
    const { ctx, w, h } = setupCanvas(this._canvas, wCss, hCss);

    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || '#fff';
    ctx.fillRect(0, 0, w, h);
    const X = (xv) => ((xv - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])) * w;
    const Y = (yv) => h - ((yv - Y_RANGE[0]) / (Y_RANGE[1] - Y_RANGE[0])) * h;

    // Spectral locus
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    SPECTRAL_LOCUS.forEach(([x, y], i) => {
      const px = X(x), py = Y(y);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    });
    ctx.closePath();
    ctx.stroke();

    // sRGB triangle for reference
    ctx.strokeStyle = 'oklch(0.554 0.180 264)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    SRGB_TRIANGLE.forEach(([x, y], i) => {
      const px = X(x), py = Y(y);
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    });
    ctx.closePath();
    ctx.stroke();

    // Ellipses
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#0066cc';
    ctx.lineWidth = 1.5;
    ctx.fillStyle = 'oklch(0.554 0.180 264 / 0.18)';
    for (const [cx, cy, a, b, angleDeg] of MACADAM) {
      const px = X(cx), py = Y(cy);
      // Convert the ellipse from xy space to pixel space.
      // The semi-axes are in xy units; multiply by per-unit pixel scale and scale factor.
      const xPerUnit = w / (X_RANGE[1] - X_RANGE[0]);
      const yPerUnit = h / (Y_RANGE[1] - Y_RANGE[0]);
      // Approximate: use a*xPerUnit, b*yPerUnit, ignoring slight axis stretching.
      const aPx = a * scale * xPerUnit;
      const bPx = b * scale * yPerUnit;
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate((-angleDeg * Math.PI) / 180);
      ctx.beginPath();
      ctx.ellipse(0, 0, aPx, bPx, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    // Axis labels
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#888';
    ctx.font = '11px ui-monospace, monospace';
    [0.2, 0.4, 0.6].forEach(v => {
      ctx.fillText(v.toFixed(1), X(v) - 8, h - 6);
      ctx.fillText(v.toFixed(1), 4, Y(v) - 4);
    });
    ctx.fillText('x', w - 12, h - 6);
    ctx.fillText('y', 6, 14);
    ctx.fillText('sRGB gamut', X(0.34), Y(0.36));
  }
}

customElements.define('macadam-ellipses', MacadamEllipses);
