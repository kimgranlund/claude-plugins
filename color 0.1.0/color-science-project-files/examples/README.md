# examples/ — live demos of ref-color

Self-contained static site that dogfoods the compiled TypeScript modules.
No framework, no dev server required.

## Quick start

**Just open `index.html` in a browser.** Works directly over `file://` — no CORS
issues, no localhost setup. Everything is wired through a single classic-script
bundle (`lib/dist/refcolor.bundle.js`).

If you prefer serving, the directory also works under any static server:

```bash
cd examples
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Layout

```
examples/
├── index.html              — landing + demo cards
├── pages/                  — one HTML per demo
│   ├── picker.html         — OKLCh picker (live multi-format readout)
│   ├── gradient.html       — gradient compared in 5 color spaces
│   ├── contrast.html       — WCAG + APCA contrast metrics
│   ├── gamut.html          — interactive L×C gamut envelope
│   ├── palette.html        — image → k-means palette extraction
│   └── transfer.html       — 6 gamma transfer functions plotted
├── lib/
│   ├── css/                — global styles (dogfooded OKLCh tokens)
│   │   ├── shell.css       — site layout + inlined OKLCh design tokens
│   │   └── components.css  — custom-element styles
│   ├── js/                 — site-specific source
│   │   ├── shell.js        — nav, footer mounting
│   │   ├── utils.js        — DOM/format helpers
│   │   └── components/     — vanilla custom elements (sources)
│   │       ├── color-chip.js
│   │       ├── gradient-strip.js     (canvas)
│   │       ├── gamut-envelope.js     (canvas)
│   │       ├── transfer-curve.js     (canvas)
│   │       ├── contrast-readout.js
│   │       └── palette-display.js
│   └── dist/               — built output (committed)
│       ├── *.js            — TypeScript modules compiled to ES modules
│       └── refcolor.bundle.js  — the single classic-script bundle loaded by every page
├── bundle-entry.js         — bundler entry: imports everything, exposes window.RefColor
├── build.sh                — convenience: tsc + esbuild in one step
└── tsconfig.json           — compiler config for ../src/ → lib/dist/
```

## Why a bundle?

Browsers block ES module imports (`<script type="module">` with relative
`import` statements) when loaded over `file://` due to CORS-on-origin-null.
A classic `<script src="...">` is exempt. Bundling everything into a single
IIFE means every demo page works without a dev server.

The bundle (~113 KB, unminified) exposes a single global:

```js
window.RefColor = {
  // spaces
  oklab, oklch, cielab, cielch, srgb, p3, rec2020,
  hsl, hsv, hct, cam16ucs, ciecam16, jzazbz, xyy, xyz,
  // transfers
  srgbTransfer, rec2020Transfer, pqTransfer, hlgTransfer,
  adobeRgbTransfer, prophotoTransfer,
  // metrics
  luminance, apca, deltaE,
  // adaptation + cvd
  bradford, machado,
  // interpolation
  linearInterp, cubehelix, lightnessCurves, spline,
  // gamut
  cusp, oklchPeak, mapping,
  // image processing
  kmeans, floydSteinberg,
  // foundation
  types, convert,
  // utility helpers
  utils,
};
```

The bundle also side-effect registers all custom elements and auto-mounts the
header + footer on `DOMContentLoaded`.

## Rebuilding after source changes

```bash
cd examples
./build.sh
```

This is `npx tsc -p tsconfig.json && npx esbuild bundle-entry.js --bundle --format=iife --target=es2020 --outfile=lib/dist/refcolor.bundle.js` under the hood.

Step 1 compiles `../src/*.ts` → `lib/dist/*.js` (ES modules).
Step 2 bundles `bundle-entry.js` (which imports every dist module + every
component + utils) into the single IIFE classic script.

## Custom-element components

Six vanilla web components, each a single class extending `HTMLElement`:

| Element | Use |
|---|---|
| `<color-chip color="..." label="...">` | Small swatch with metadata |
| `<gradient-strip from="#hex" to="#hex" space="oklab">` | Canvas gradient rendered in a given space |
| `<gamut-envelope hue="29" show="srgb,p3,rec2020">` | 2D plot of gamut envelope at fixed hue |
| `<transfer-curve curves="srgb,pq">` | Plot transfer functions on a square canvas |
| `<contrast-readout text="#hex" bg="#hex">` | Live WCAG + APCA contrast metrics |
| `<palette-display>` | Grid of color swatches with hex labels |

No framework dependency — copy any component .js file into your project and
register it with `customElements.define()`.

## How the TS compiles to browser-ready JS

The source in `../src/*.ts` uses two conventions that compile to clean ESM:

1. **`.js` extensions in imports** (`from '../types.js'`). This is the ESM
   standard and what browsers expect. TypeScript preserves these in output.
2. **Branded types as zero-cost casts** (`as unknown as XYZ_D65`). Erased at
   compile time. Runtime is plain `[number, number, number]` tuples.

The compiled `lib/dist/*.js` files are valid ES2022 modules — they're
consumable directly under any modern bundler / native ESM environment.
The IIFE bundle is just a convenience for the demo pages.

## Color tokens are dogfooded

Design tokens at the top of `lib/css/shell.css` use OKLCh CSS values directly:

```css
--brand-500: oklch(0.554 0.180 264);
--brand-700: oklch(0.371 0.143 264);
```

These match the Tailwind v4 L-stop convention at hue 264°. Browsers compute
OKLCh natively (Chrome 111+, Safari 16.4+, Firefox 113+).

Dark mode auto-switches via `prefers-color-scheme`.

Tokens are inlined (not `@import`ed from a separate file) because WebKit treats
every `file://` URL as its own security origin, and chained CSS `@import`s
between two `file://` resources trip the cross-origin policy.
