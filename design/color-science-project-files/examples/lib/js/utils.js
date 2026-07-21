// Small DOM and formatting helpers shared across pages and components.

/** Format a number to N decimal places. */
export const fmt = (x, n = 3) => {
  if (!Number.isFinite(x)) return 'NaN';
  return Number(x).toFixed(n);
};

/** Format a 3-tuple. */
export const fmtTuple = (t, n = 3) =>
  '[' + Array.from(t).map(v => fmt(v, n)).join(', ') + ']';

/** Clamp to [min, max]. */
export const clamp = (x, min, max) => Math.max(min, Math.min(max, x));

/** Linear RGB component (0-1) → hex byte (00-FF). */
export const toHexByte = (x) => {
  const v = Math.round(clamp(x, 0, 1) * 255);
  return v.toString(16).padStart(2, '0');
};

/** Encoded sRGB tuple → '#rrggbb'. */
export const toHex = (encoded) =>
  '#' + toHexByte(encoded[0]) + toHexByte(encoded[1]) + toHexByte(encoded[2]);

/** Parse '#rrggbb' (or '#rgb') → encoded sRGB tuple [0, 1]. */
export const fromHex = (hex) => {
  hex = hex.trim().replace(/^#/, '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  if (hex.length !== 6) return [0, 0, 0];
  return [
    parseInt(hex.substr(0, 2), 16) / 255,
    parseInt(hex.substr(2, 2), 16) / 255,
    parseInt(hex.substr(4, 2), 16) / 255,
  ];
};

/** Encoded sRGB tuple → CSS `rgb()` string. */
export const toCssRgb = (encoded) =>
  `rgb(${Math.round(encoded[0] * 255)} ${Math.round(encoded[1] * 255)} ${Math.round(encoded[2] * 255)})`;

/** OKLCh tuple → CSS `oklch()` string. */
export const toCssOklch = (oklch) =>
  `oklch(${fmt(oklch[0], 4)} ${fmt(oklch[1], 4)} ${fmt(oklch[2], 2)})`;

/** OKLab tuple → CSS `oklab()` string. */
export const toCssOklab = (oklab) =>
  `oklab(${fmt(oklab[0], 4)} ${fmt(oklab[1], 4)} ${fmt(oklab[2], 4)})`;

/** Make a DOM element shorthand. */
export const el = (tag, attrs = {}, ...children) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') e.className = v;
    else if (k === 'style' && typeof v === 'object') Object.assign(e.style, v);
    else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v !== undefined && v !== null) e.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null) continue;
    e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
  }
  return e;
};

/** Throttle a function call to once per animation frame. */
export const raf = (fn) => {
  let pending = false;
  let lastArgs;
  return (...args) => {
    lastArgs = args;
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => {
      pending = false;
      fn(...lastArgs);
    });
  };
};

/** Copy text to clipboard with fallback. */
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
};

/** Get a device-pixel-ratio-aware canvas context. */
export const setupCanvas = (canvas, w, h) => {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  return { ctx, w, h };
};

/** Wire a drag-and-drop file handler onto `target`. Calls `handler(file)` on
 *  drop. Adds/removes the `drop-active` class for CSS-driven affordance. */
export const wireFileDrop = (target, handler) => {
  if (!target) return;
  const setActive = (a) => target.classList.toggle('drop-active', a);
  target.addEventListener('dragover', (e) => { e.preventDefault(); setActive(true); });
  target.addEventListener('dragenter', (e) => { e.preventDefault(); setActive(true); });
  target.addEventListener('dragleave', () => setActive(false));
  target.addEventListener('dragend', () => setActive(false));
  target.addEventListener('drop', (e) => {
    e.preventDefault();
    setActive(false);
    const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (file) handler(file);
  });
};
