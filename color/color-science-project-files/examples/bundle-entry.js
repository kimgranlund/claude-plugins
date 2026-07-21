// Bundle entry — pulls in every math module, every component, and the
// utility helpers, then exposes them on window.RefColor for the demo pages
// to consume via classic <script> tags (no CORS issues over file://).

// ─── Math modules ─────────────────────────────────────────────────────────────

import * as oklab from './lib/dist/spaces/oklab.js';
import * as oklch from './lib/dist/spaces/oklch.js';
import * as cielab from './lib/dist/spaces/cielab.js';
import * as cielch from './lib/dist/spaces/cielch.js';
import * as srgb from './lib/dist/spaces/srgb.js';
import * as p3 from './lib/dist/spaces/p3.js';
import * as rec2020 from './lib/dist/spaces/rec2020.js';
import * as hsl from './lib/dist/spaces/hsl.js';
import * as hsv from './lib/dist/spaces/hsv.js';
import * as hct from './lib/dist/spaces/hct.js';
import * as cam16ucs from './lib/dist/spaces/cam16-ucs.js';
import * as ciecam16 from './lib/dist/spaces/ciecam16.js';
import * as jzazbz from './lib/dist/spaces/jzazbz.js';
import * as xyy from './lib/dist/spaces/xyy.js';
import * as xyz from './lib/dist/spaces/xyz.js';

import * as srgbTransfer from './lib/dist/transfer/srgb.js';
import * as rec2020Transfer from './lib/dist/transfer/rec2020.js';
import * as pqTransfer from './lib/dist/transfer/pq.js';
import * as hlgTransfer from './lib/dist/transfer/hlg.js';
import * as adobeRgbTransfer from './lib/dist/transfer/adobe-rgb.js';
import * as prophotoTransfer from './lib/dist/transfer/prophoto.js';

import * as luminance from './lib/dist/metrics/luminance.js';
import * as apca from './lib/dist/metrics/apca.js';
import * as deltaE from './lib/dist/metrics/deltaE.js';

import * as bradford from './lib/dist/adaptation/bradford.js';
import * as machado from './lib/dist/cvd/machado-2009.js';

import * as linearInterp from './lib/dist/interpolation/linear.js';
import * as cubehelix from './lib/dist/interpolation/cubehelix.js';
import * as lightnessCurves from './lib/dist/interpolation/lightness-curves.js';
import * as spline from './lib/dist/interpolation/spline.js';

import * as cuspMod from './lib/dist/gamut/cusp.js';
import * as oklchPeak from './lib/dist/gamut/oklch-peak.js';
import * as mapping from './lib/dist/gamut/mapping.js';

import * as kmeans from './lib/dist/quantize/kmeans.js';
import * as floydSteinberg from './lib/dist/dithering/floyd-steinberg.js';

import * as types from './lib/dist/types.js';
import * as convert from './lib/dist/convert.js';

// ─── Utility helpers ──────────────────────────────────────────────────────────

import * as utils from './lib/js/utils.js';

// ─── Components (side-effect imports register custom elements) ────────────────

import './lib/js/components/color-chip.js';
import './lib/js/components/gradient-strip.js';
import './lib/js/components/gamut-envelope.js';
import './lib/js/components/transfer-curve.js';
import './lib/js/components/contrast-readout.js';
import './lib/js/components/palette-display.js';
import './lib/js/components/cvd-simulator.js';
import './lib/js/components/token-ramp.js';
import './lib/js/components/chromaticity-diagram.js';
import './lib/js/components/gamut-strip.js';
import './lib/js/components/hue-wheel.js';
import './lib/js/components/image-histograms.js';
import './lib/js/components/pigment-mixer.js';
import './lib/js/components/adaptation-viewer.js';
import './lib/js/components/tonemap-strip.js';
import './lib/js/components/dither-compare.js';
import './lib/js/components/spd-chart.js';
import './lib/js/components/procedural-palette.js';
import './lib/js/components/tonal-palette.js';
import './lib/js/components/kelvin-picker.js';
import './lib/js/components/okhsl-picker.js';
import './lib/js/components/blend-through-white.js';
import './lib/js/components/cvd-safe-palette.js';
import './lib/js/components/cmf-chart.js';
import './lib/js/components/macadam-ellipses.js';
import './lib/js/components/volume-bars.js';
import './lib/js/components/color-cube-3d.js';
import './lib/js/components/multi-dither.js';
import './lib/js/components/image-scatter.js';
import './lib/js/components/chip-composer.js';
import './lib/js/components/homage-canvas.js';
import './lib/js/components/afterimage-trial.js';
import './lib/js/components/transparency-composer.js';

// ─── Shell (auto-mounts header + footer on DOMContentLoaded) ──────────────────

import './lib/js/shell.js';

// ─── Expose as global ─────────────────────────────────────────────────────────

window.RefColor = {
  // spaces
  oklab, oklch, cielab, cielch, srgb, p3, rec2020,
  hsl, hsv, hct, cam16ucs, ciecam16, jzazbz, xyy, xyz,

  // transfers
  srgbTransfer, rec2020Transfer, pqTransfer, hlgTransfer,
  adobeRgbTransfer, prophotoTransfer,

  // metrics
  luminance, apca, deltaE,

  // adaptation
  bradford,

  // cvd
  machado,

  // interpolation
  linearInterp, cubehelix, lightnessCurves, spline,

  // gamut
  cusp: cuspMod, oklchPeak, mapping,

  // image processing
  kmeans, floydSteinberg,

  // foundation
  types, convert,

  // utility helpers
  utils,
};
