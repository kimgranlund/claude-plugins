#!/usr/bin/env node
/**
 * ui-probe.mjs — the ui-audit "measured, not computed" probe.
 *
 * Step 4 (invariant pass) of the audit builds each verifier's card. Hand-building them from source is COMPUTED —
 * an inference about what the browser will do. This probe drives the RUNNING app (Chromium via
 * playwright) and emits the cards from RENDERED truth: resolved colors, real focus deltas, real
 * paint timings, the actual lang/dir the document carries. Probed cards supersede hand-built
 * ones; whatever the probe can't reach stays hand-built and is reported as computed-not-measured.
 *
 *   node ui-probe.mjs <baseURL> --inventory inventory.json [--out cards/]
 *                     [--scheme light|dark|both] [--screens id,id] [--storage-state path.json]
 *   node ui-probe.mjs selftest [--no-browser]
 *
 * Dependency: playwright, resolved from the CWD's node_modules FIRST (the probe usually runs from
 * the target repo, whose install carries the browsers), then from this script's tree. Unavailable
 * playwright (or an unlaunchable chromium) exits 2 — distinct from probe failures — with exact
 * install guidance. Never a fake pass.
 *
 * Authenticating for gated routes: this probe opens a fresh, unauthenticated browser context per
 * screen. A route behind a session/auth guard will redirect — the probe DETECTS that (final URL
 * != requested URL) and skips the screen with the redirect named, rather than silently capturing
 * the login page under the wrong screen id. To probe gated routes for real, pass
 * `--storage-state <path>` (a Playwright storage-state JSON — cookies/localStorage from a prior
 * authenticated session, e.g. via `context.storageState({ path })` after a manual/scripted login);
 * it is threaded into every screen's browser context. Optional — detection works with or without it.
 *
 * Per screen (navigate baseURL+route, network idle + bounded DOM-quiescence settle + double-rAF),
 * per scheme (prefers-color-scheme emulated; "both" runs twice):
 *
 *   <screen>.<scheme>.surface.json — check-colors card. Walks visible text nodes; per node the
 *     resolved color and the EFFECTIVE background (first non-transparent ancestor
 *     background-color, alpha composited down the chain, white canvas fallback). fg alpha is
 *     composited over that background, so every emitted pair is opaque rgb() — no "over" needed.
 *     Colors are parsed from rgb()/rgba()/#hex/color(srgb ...)/oklch()/oklab() (the CSS Color 4
 *     syntaxes real Chromium computed-style serialization actually emits for custom-property-
 *     sourced colors); an unparsed pair is dropped and counted in meta, never silently guessed.
 *     kind: largeText iff >= 24px, or >= 18.66px at weight >= 700 (WCAG large-text rule); else
 *     normalText (size:"large"/"normal" mirrors it for the checker's floors). Pairs deduped by
 *     (fg, bg, kind) with a count; capped at 80/screen with the overflow counted in meta.
 *
 *   <screen>.focus.json — focus-verify card. Tabbable candidates (interactive selectors +
 *     [tabindex]) -> elements[] {id, tabindex, focusable, visible_focus}. `focusable` is a cheap
 *     existence check (programmatic .focus()/.blur() — can the element take focus at all).
 *     `visible_focus` is MEASURED via REAL keyboard navigation: after enumerating candidates, the
 *     probe drives `page.keyboard.press('Tab')` from a blurred start and reads document.activeElement
 *     at each stop, diffing its computed outline/box-shadow/border/background against its resting
 *     (unfocused) snapshot. This is deliberate, not incidental: Chromium's actual :focus-visible
 *     heuristic keys off input modality, and a scripted `el.focus()` call is NOT reliably treated as
 *     keyboard-equivalent — only genuine keyboard-dispatched focus reliably matches :focus-visible.
 *     (An earlier version of this probe used programmatic focus for this measurement and produced
 *     mass false NO_VISIBLE_FOCUS positives on any component styled via :focus-visible — confirmed
 *     against a real app; see CHANGELOG.) Tab order may not reach every candidate (skip links,
 *     custom tabindex) within a bounded walk (2x the enumerated count, floored at 6): an element
 *     never reached omits `visible_focus` entirely (UNMEASURED-for-this-element) rather than
 *     guessing — the checker treats an absent key as unmeasured, never as a pass. dom_order from
 *     document order. targets[] from getBoundingClientRect (+ inline_text for inline <a>).
 *     ring{} from the first REAL-Tab-focused element painting an outline: width_px + contrast of
 *     the outline color vs that element's effective background, computed per scheme pass
 *     (contrast_light / contrast_dark). Only CSS `outline`-based rings are detected — a ring
 *     implemented via `box-shadow` (a common, spec-encouraged technique) is not recognized and
 *     ring{} is simply absent; a filed, known gap, not silently wrong. modals[]: visible
 *     dialog[open] / [role=dialog] -> {id, open:true}; trap/restore are NOT measurable statically,
 *     so they are OMITTED — the checker reports them, never a silent guess.
 *
 *   <screen>.budget.json — perf-verify card. LCP + CLS from buffered PerformanceObservers during
 *     the load window; bundle_kb = js+css transferSize (split noted under resources{}); requests
 *     + nav timing recorded. inp_ms / tbt_ms are interaction metrics a load probe cannot measure:
 *     OMITTED, and the checker reports them as skipped/UNMEASURED. CAVEAT: if the target is a dev
 *     server (`npm run dev`), bundle_kb reflects its unbundled/unminified/HMR-served module graph —
 *     not comparable to a production build's budget. Probe a production build (`vite build && vite
 *     preview` or equivalent) when bundle_kb needs to mean something.
 *
 *   <screen>.i18n.json — i18n-verify card. has_lang / has_dir true iff the document carries the
 *     attribute on self-or-ancestor of <body>. hardcoded_strings stays [] — a STATIC concern
 *     (inventory-scan territory), noted on the card, not guessed by the probe.
 *
 *   cards/probe-manifest.json — {baseURL, when, schemes, probed, skipped[{id, reason}]}.
 *
 * selftest: starts a node:http server on an ephemeral port serving an embedded fixture with KNOWN
 * defects (16x16 icon button, rgb(119,119,119)-on-white text, an outline:none no-delta button,
 * tabindex=3, an open <dialog>, a :focus-visible-only ring, a setTimeout-delayed content swap, a
 * redirecting route), probes it headless, asserts the cards carry those facts, then pipes the
 * cards through the REAL checkers (check-colors/focus-verify, resolved as sibling skills) and
 * asserts CONTRAST_FAIL_AA, TARGET_TOO_SMALL, NO_VISIBLE_FOCUS, POSITIVE_TABINDEX fire.
 * `--no-browser` runs only the pure-function unit checks (contrast math, color parsing —
 * including oklch()/oklab() — compositing, joinURL, routeMismatch, card assembly). No playwright
 * => SKIP printed with guidance, exit 2 — never a fake pass.
 */
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync, rmSync, existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import http from 'node:http';
import os from 'node:os';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const INSTALL_GUIDANCE =
  'ui-probe needs playwright + chromium. From the target repo (preferred — its install works):\n' +
  '  npm i -D playwright && npx playwright install chromium\n' +
  'or run this probe with the target repo as CWD so its node_modules resolves.';

// ---------------------------------------------------------------------------------------------
// Pure functions — no DOM, no browser. These are the unit-tested core (`selftest --no-browser`).
// ---------------------------------------------------------------------------------------------

// --- OKLab -> sRGB conversion chain ------------------------------------------------------------
// Modern Chromium serializes computed-style colors sourced from CSS custom properties in
// oklch()/oklab() syntax (CSS Color 4), not always rgb() — confirmed against a real design system
// (adia-pay/@adia-ai/web-components). Matrices ported verbatim (not re-derived) from this corpus's
// own color-space-facts knowledge pack:
//   - OKLab<->XYZ_D65 (M2^-1, M1^-1): Björn Ottosson, "A perceptual color space for image
//     processing" (2020) — ~/.claude/skills/color-space-facts/references/techniques/oklab-xyz-math.md
//   - XYZ_D65->linear sRGB (M_XYZ_TO_SRGB) + the gamma transfer curve: IEC 61966-2-1 —
//     ~/.claude/skills/color-science-project-files/src/spaces/srgb.ts + src/transfer/srgb.ts
// Chain: OKLab -> (M2^-1) -> LMS' -> (cube) -> LMS -> (M1^-1) -> XYZ_D65 -> (M_XYZ_TO_SRGB) ->
// linear sRGB -> (gamma encode) -> [0,255]. Clamping to [0,255] is a gamut safety net (Chromium's
// own computed-style output is generally already in-gamut for what it renders), not the primary path.
const OKLAB_TO_LMS_PRIME = [ // M2^-1
  [1, 0.3963377774, 0.2158037573],
  [1, -0.1055613458, -0.0638541728],
  [1, -0.0894841775, -1.2914855480],
];
const LMS_TO_XYZ_D65 = [ // M1^-1
  [1.2270138511, -0.5577999807, 0.2812561490],
  [-0.0405801784, 1.1122568696, -0.0716766787],
  [-0.0763812845, -0.4214819784, 1.5861632204],
];
const XYZ_D65_TO_LINEAR_SRGB = [ // M_XYZ_TO_SRGB, IEC 61966-2-1
  [3.2409699419, -1.5373831776, -0.4986107603],
  [-0.9692436363, 1.8759675015, 0.0415550574],
  [0.0556300797, -0.2039769589, 1.0569715142],
];

function mulMat3Vec3(m, v) {
  return [
    m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
    m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
    m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
  ];
}

/** Linear -> gamma-encoded sRGB scalar (IEC 61966-2-1 piecewise transfer). */
function srgbGammaEncode(linear) {
  const abs = Math.abs(linear);
  const sign = Math.sign(linear);
  const enc = abs <= 0.0031308 ? 12.92 * abs : 1.055 * Math.pow(abs, 1 / 2.4) - 0.055;
  return sign * enc;
}

/** OKLab (L in [0,1], a/b unbounded) -> {r,g,b} in [0,255], clamped (out-of-gamut safety net). */
export function oklabToSrgb255(L, a, b) {
  const lmsPrime = mulMat3Vec3(OKLAB_TO_LMS_PRIME, [L, a, b]);
  const lms = lmsPrime.map((c) => c * c * c); // LMS' -> LMS: cube (inverse of OKLab's cube-root step)
  const xyz = mulMat3Vec3(LMS_TO_XYZ_D65, lms);
  const linearRgb = mulMat3Vec3(XYZ_D65_TO_LINEAR_SRGB, xyz);
  const to255 = (linear) => Math.min(255, Math.max(0, Math.round(srgbGammaEncode(linear) * 255)));
  return { r: to255(linearRgb[0]), g: to255(linearRgb[1]), b: to255(linearRgb[2]) };
}

/** A CSS Color 4 number|percentage|'none' component -> a plain number. `pctScale` is what 100%
 *  means (1 for OKLCH/OKLab lightness and alpha, 0.4 for OKLCH chroma / OKLab a·b per spec). */
function numOrPct(tok, pctScale) {
  if (tok === undefined || tok === 'none') return 0;
  return tok.endsWith('%') ? (parseFloat(tok) / 100) * pctScale : parseFloat(tok);
}

const NUM_PCT_NONE = '(?:[\\d.]+%?|none)';

/** Parse a computed-style color string -> {r,g,b,a} or null. Handles rgb()/rgba() (what Chromium
 *  computed styles emit), #hex, color(srgb ...), oklch()/oklab() (what Chromium emits for colors
 *  sourced from CSS custom properties in a modern design system — confirmed real-world), and
 *  'transparent'. */
export function parseCssColor(str) {
  if (typeof str !== 'string') return null;
  const s = str.trim().toLowerCase();
  if (s === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
  let m = s.match(/^rgba?\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)(?:\s*,\s*([0-9.]+%?))?\s*\)$/) ||
          s.match(/^rgba?\(\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)(?:\s*\/\s*([0-9.]+%?))?\s*\)$/);
  if (m) {
    const a = m[4] === undefined ? 1
      : m[4].endsWith('%') ? parseFloat(m[4]) / 100 : parseFloat(m[4]);
    return { r: +m[1], g: +m[2], b: +m[3], a };
  }
  m = s.match(/^color\(srgb\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)(?:\s*\/\s*([0-9.]+))?\s*\)$/);
  if (m) {
    return { r: Math.round(+m[1] * 255), g: Math.round(+m[2] * 255), b: Math.round(+m[3] * 255),
             a: m[4] === undefined ? 1 : +m[4] };
  }
  m = s.match(new RegExp(`^oklch\\(\\s*(${NUM_PCT_NONE})\\s+(${NUM_PCT_NONE})\\s+(-?[\\d.]+|none)` +
                          `(?:\\s*\\/\\s*(${NUM_PCT_NONE}))?\\s*\\)$`));
  if (m) {
    const L = numOrPct(m[1], 1);
    const C = numOrPct(m[2], 0.4);
    const H = m[3] === 'none' ? 0 : parseFloat(m[3]);
    const hRad = (H * Math.PI) / 180;
    const rgb = oklabToSrgb255(L, C * Math.cos(hRad), C * Math.sin(hRad));
    return { ...rgb, a: m[4] === undefined ? 1 : numOrPct(m[4], 1) };
  }
  m = s.match(new RegExp(`^oklab\\(\\s*(${NUM_PCT_NONE})\\s+(-?[\\d.]+%?|none)\\s+(-?[\\d.]+%?|none)` +
                          `(?:\\s*\\/\\s*(${NUM_PCT_NONE}))?\\s*\\)$`));
  if (m) {
    const L = numOrPct(m[1], 1);
    const a2 = numOrPct(m[2], 0.4);
    const b2 = numOrPct(m[3], 0.4);
    const rgb = oklabToSrgb255(L, a2, b2);
    return { ...rgb, a: m[4] === undefined ? 1 : numOrPct(m[4], 1) };
  }
  m = s.match(/^#([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$/);
  if (m) {
    let h = m[1];
    if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    return { r: parseInt(h.slice(0, 2), 16), g: parseInt(h.slice(2, 4), 16),
             b: parseInt(h.slice(4, 6), 16), a: h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1 };
  }
  return null;
}

/** Source-over compositing of a translucent fg over an OPAQUE bg (gamma-encoded, as browsers). */
export function compositeOver(fg, bg) {
  const a = fg.a === undefined ? 1 : fg.a;
  return {
    r: Math.round(fg.r * a + bg.r * (1 - a)),
    g: Math.round(fg.g * a + bg.g * (1 - a)),
    b: Math.round(fg.b * a + bg.b * (1 - a)),
    a: 1,
  };
}

/** WCAG 2.x relative luminance of an opaque sRGB color. */
export function relativeLuminance({ r, g, b }) {
  const lin = (c) => {
    const cs = c / 255;
    return cs <= 0.03928 ? cs / 12.92 : ((cs + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

/** WCAG 2.x contrast ratio of two opaque sRGB colors, in [1, 21]. */
export function contrastRatio(c1, c2) {
  const l1 = relativeLuminance(c1);
  const l2 = relativeLuminance(c2);
  const [hi, lo] = l1 >= l2 ? [l1, l2] : [l2, l1];
  return (hi + 0.05) / (lo + 0.05);
}

/** Resolve an effective background from a chain of ancestor background-colors
 *  (innermost -> outermost): composite every non-transparent layer over the white canvas. */
export function resolveBgChain(chain) {
  let eff = { r: 255, g: 255, b: 255, a: 1 }; // browser canvas default
  for (let i = (chain || []).length - 1; i >= 0; i--) {
    const c = parseCssColor(chain[i]);
    if (c && c.a > 0) eff = compositeOver(c, eff);
  }
  return eff;
}

/** WCAG large-text rule: >= 24px, or >= 18.66px at weight >= 700; else normalText. */
export function classifyTextKind(fontSizePx, fontWeight) {
  const bold = (Number(fontWeight) || 400) >= 700;
  return fontSizePx >= 24 || (bold && fontSizePx >= 18.66) ? 'largeText' : 'normalText';
}

export function rgbStr({ r, g, b }) {
  return `rgb(${r}, ${g}, ${b})`;
}

const PAIR_CAP = 80;

/** Assemble a check-colors surface card from raw text-node measurements. */
export function buildSurfaceCard(screenId, scheme, raws) {
  const seen = new Map();
  let unparsed = 0;
  for (const raw of raws || []) {
    const fgP = parseCssColor(raw.color);
    if (!fgP) { unparsed++; continue; }
    const bg = resolveBgChain(raw.bgChain);
    const fg = fgP.a < 1 ? compositeOver(fgP, bg) : fgP;
    const kind = classifyTextKind(raw.fontSize, raw.fontWeight);
    const key = `${rgbStr(fg)}|${rgbStr(bg)}|${kind}`;
    const hit = seen.get(key);
    if (hit) { hit.count++; continue; }
    seen.set(key, {
      name: raw.name || '<text>',
      fg: rgbStr(fg),
      bg: rgbStr(bg),
      kind,
      size: kind === 'largeText' ? 'large' : 'normal',
      role: 'text',
      count: 1,
    });
  }
  const unique = [...seen.values()];
  const pairs = unique.slice(0, PAIR_CAP);
  return {
    meta: {
      scheme,
      probe: 'rendered',
      screen: screenId,
      pairs_total_raw: (raws || []).length,
      pairs_deduped: (raws || []).length - unparsed - unique.length,
      pairs_capped: Math.max(0, unique.length - PAIR_CAP),
      pairs_unparsed: unparsed,
    },
    pairs,
  };
}

/** Assemble a focus-verify card from a raw focus sweep (+ per-scheme ring contrasts). */
export function buildFocusCard(screenId, raw, ringContrasts) {
  const card = {
    id: screenId,
    elements: raw.elements || [],
    dom_order: raw.dom_order || [],
    targets: raw.targets || [],
    modals: raw.modals || [], // {id, open} only — trap/restore not measurable: omitted, never guessed
  };
  if (raw.ring) {
    const ring = { width_px: raw.ring.width_px };
    for (const [key, ratio] of Object.entries(ringContrasts || {})) {
      if (typeof ratio === 'number') ring[key] = Math.round(ratio * 100) / 100;
    }
    card.ring = ring;
  }
  return card;
}

/** Assemble a perf-verify budget card. inp_ms/tbt_ms are OMITTED (unmeasurable without
 *  interaction) — the checker reports them as skipped, never as a pass. */
export function buildBudgetCard(screenId, perf) {
  const metrics = {};
  if (typeof perf.lcp_ms === 'number') metrics.lcp_ms = perf.lcp_ms;
  if (typeof perf.cls === 'number') metrics.cls = perf.cls;
  const bundle = (perf.js_kb || 0) + (perf.css_kb || 0);
  metrics.bundle_kb = Math.round(bundle * 10) / 10;
  if (typeof perf.requests === 'number') metrics.requests = perf.requests;
  return {
    page: screenId,
    metrics,
    resources: { js_kb: perf.js_kb, css_kb: perf.css_kb, other_kb: perf.other_kb, doc_kb: perf.doc_kb },
    timing: { ttfb_ms: perf.ttfb_ms, dcl_ms: perf.dcl_ms, load_ms: perf.load_ms },
    note: 'probed load window — inp_ms/tbt_ms need interaction and are omitted (UNMEASURED)',
  };
}

/** Assemble an i18n-verify card. hardcoded_strings is a static concern — [] with a note. */
export function buildI18nCard(screenId, i18n) {
  return {
    surfaces: [{
      id: screenId,
      has_lang: !!i18n.has_lang,
      has_dir: !!i18n.has_dir,
      hardcoded_strings: [],
    }],
    probe: 'rendered',
    note: 'hardcoded_strings/posture/rtl scope are static concerns — inventory-scan + repo review, not probed',
  };
}

// ---------------------------------------------------------------------------------------------
// Playwright resolution — CWD's node_modules first (the target repo), then this script's tree.
// ---------------------------------------------------------------------------------------------

async function loadPlaywright() {
  const candidates = [];
  for (const base of [path.join(process.cwd(), 'noop.js'), import.meta.url]) {
    try { candidates.push({ spec: createRequire(base).resolve('playwright'), from: base }); }
    catch { /* not resolvable from here */ }
  }
  candidates.push({ spec: 'playwright', from: 'bare import' });
  for (const c of candidates) {
    try {
      const href = c.spec.startsWith('/') ? pathToFileURL(c.spec).href : c.spec;
      const mod = await import(href);
      const pw = mod.chromium ? mod : mod.default;
      if (pw && pw.chromium) return { pw, resolvedFrom: c.spec };
    } catch { /* try the next candidate */ }
  }
  return null;
}

// ---------------------------------------------------------------------------------------------
// In-page collectors (serialized into the page by playwright's evaluate)
// ---------------------------------------------------------------------------------------------

const PERF_INIT = () => {
  window.__probe = { lcp: null, cls: 0 };
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) window.__probe.lcp = e.startTime;
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch { /* entry type unsupported */ }
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) window.__probe.cls += e.value;
    }).observe({ type: 'layout-shift', buffered: true });
  } catch { /* entry type unsupported */ }
};

const COLLECT_TEXT = () => {
  const out = [];
  const isVisible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const selPath = (el) => {
    const parts = [];
    let n = el;
    for (let d = 0; n && n.nodeType === 1 && d < 3; d++) {
      let s = n.tagName.toLowerCase();
      if (n.id) { parts.unshift(s + '#' + n.id); break; }
      const cls = (n.getAttribute('class') || '').trim().split(/\s+/)[0];
      if (cls) s += '.' + cls;
      parts.unshift(s);
      n = n.parentElement;
    }
    return parts.join(' > ');
  };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  let visited = 0;
  while ((node = walker.nextNode()) && visited < 5000) {
    if (!node.textContent.trim()) continue;
    const el = node.parentElement;
    if (!el || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(el.tagName)) continue;
    if (!isVisible(el)) continue;
    visited++;
    const cs = getComputedStyle(el);
    const chain = [];
    for (let a = el; a; a = a.parentElement) chain.push(getComputedStyle(a).backgroundColor);
    out.push({
      name: selPath(el),
      color: cs.color,
      bgChain: chain,
      fontSize: parseFloat(cs.fontSize),
      fontWeight: parseFloat(cs.fontWeight) || 400,
    });
  }
  return out;
};

// --- Focus enumeration + REAL keyboard-driven ring/visible-focus measurement -------------------
// Split in two on purpose (Bug 5 fix). Programmatic `el.focus()` is fine for an EXISTENCE check
// (can this element take focus at all — `focusable`) but is NOT reliable for Chromium's actual
// :focus-visible matching, which keys off input MODALITY, not merely "is something focused". Ring
// and visible_focus measurement is driven for real via `page.keyboard.press('Tab')` in
// `driveKeyboardFocus` (probeScreen, below) — COLLECT_FOCUS_SETUP only enumerates candidates + a
// resting (unfocused) style snapshot to diff against.
const COLLECT_FOCUS_SETUP = () => {
  const SEL = 'a[href], button, input, select, textarea, summary, audio[controls], ' +
              'video[controls], [contenteditable="true"], [tabindex]';
  const isVisible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const idOf = (el, i) =>
    el.getAttribute('data-testid') || (el.id ? '#' + el.id : el.tagName.toLowerCase() + '[' + i + ']');
  const snap = (el) => {
    const cs = getComputedStyle(el);
    return [cs.outlineWidth, cs.outlineStyle, cs.outlineColor, cs.boxShadow,
            cs.borderTopColor, cs.borderRightColor, cs.borderBottomColor, cs.borderLeftColor,
            cs.backgroundColor].join('|');
  };
  const all = [...document.querySelectorAll(SEL)].filter(isVisible).filter((el) => !el.disabled);
  // Live element refs, indexed — the real-keyboard driver loop (Playwright-side, between
  // page.keyboard.press('Tab') calls) matches document.activeElement back to a candidate by
  // identity via this array, so the id-computation logic (idOf) lives in exactly one place.
  window.__focusEls = [];
  const elements = [];
  const targets = [];
  const dom_order = [];
  all.forEach((el, i) => {
    const id = idOf(el, i);
    const tiAttr = el.getAttribute('tabindex');
    const tabindex = tiAttr !== null && /^-?\d+$/.test(tiAttr.trim()) ? parseInt(tiAttr, 10) : 0;
    const restSnapshot = snap(el); // resting (unfocused) style — the later real-Tab diff baseline
    el.focus({ preventScroll: true }); // existence check ONLY — never used to measure visible_focus
    const focusable = document.activeElement === el;
    el.blur();
    window.__focusEls.push(el);
    elements.push({ id, tabindex, focusable, restSnapshot });
    dom_order.push(id);
    const r = el.getBoundingClientRect();
    targets.push({
      id,
      w: Math.round(r.width),
      h: Math.round(r.height),
      inline_text: el.tagName === 'A' && getComputedStyle(el).display === 'inline',
    });
  });
  const seen = new Set();
  const modals = [...document.querySelectorAll('dialog[open], [role="dialog"]')]
    .filter((el) => isVisible(el) && !seen.has(el) && seen.add(el))
    .map((el, i) => ({
      id: el.getAttribute('data-testid') || (el.id ? '#' + el.id : 'dialog[' + i + ']'),
      open: true,
    }));
  return { elements, dom_order, targets, modals };
};

/** Read after a real `page.keyboard.press('Tab')` — matches document.activeElement back to a
 *  COLLECT_FOCUS_SETUP candidate via window.__focusEls, and captures the focused-state style
 *  snapshot + any outline ring, driven by REAL keyboard navigation (the only reliable way to
 *  trigger Chromium's actual :focus-visible matching — see the top docstring and CHANGELOG). */
const READ_ACTIVE_ELEMENT = () => {
  const el = document.activeElement;
  const idx = el && window.__focusEls ? window.__focusEls.indexOf(el) : -1;
  if (idx < 0) return { idx: -1 };
  const cs = getComputedStyle(el);
  const snapshot = [cs.outlineWidth, cs.outlineStyle, cs.outlineColor, cs.boxShadow,
                    cs.borderTopColor, cs.borderRightColor, cs.borderBottomColor, cs.borderLeftColor,
                    cs.backgroundColor].join('|');
  let ring = null;
  if (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) {
    const chain = [];
    for (let a = el; a; a = a.parentElement) chain.push(getComputedStyle(a).backgroundColor);
    ring = { width_px: parseFloat(cs.outlineWidth), color: cs.outlineColor, bgChain: chain };
  }
  return { idx, snapshot, ring };
};

const COLLECT_PERF = () => {
  const nav = performance.getEntriesByType('navigation')[0];
  const res = performance.getEntriesByType('resource');
  let js = 0, css = 0, other = 0;
  for (const r of res) {
    const kb = (r.transferSize || 0) / 1024;
    if (r.initiatorType === 'script' || /\.[mc]?js(\?|$)/.test(r.name)) js += kb;
    else if (/\.css(\?|$)/.test(r.name)) css += kb;
    else other += kb;
  }
  const round1 = (n) => Math.round(n * 10) / 10;
  const p = window.__probe || {};
  return {
    lcp_ms: typeof p.lcp === 'number' ? Math.round(p.lcp) : null,
    cls: typeof p.cls === 'number' ? Math.round(p.cls * 1000) / 1000 : null,
    js_kb: round1(js),
    css_kb: round1(css),
    other_kb: round1(other),
    doc_kb: nav ? round1((nav.transferSize || 0) / 1024) : 0,
    requests: res.length + (nav ? 1 : 0),
    ttfb_ms: nav ? Math.round(nav.responseStart) : null,
    dcl_ms: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
    load_ms: nav ? Math.round(nav.loadEventEnd) : null,
  };
};

const COLLECT_I18N = () => ({
  has_lang: !!(document.body && document.body.closest('[lang]')),
  has_dir: !!(document.body && document.body.closest('[dir]')),
});

// ---------------------------------------------------------------------------------------------
// The probe
// ---------------------------------------------------------------------------------------------

// Settle-strategy constants (Bug 3 fix). `networkidle` + a bare double-rAF waits for network
// quiet + one paint tick — it does NOT wait out setTimeout-scheduled DOM updates (a common
// loading-skeleton -> real-content pattern with no further network activity to make "networkidle"
// meaningful). Confirmed against a real app: a loading-skeleton state (2 real text pairs) was
// captured instead of settled content (72 real text pairs) until the wait was manually extended.
// SETTLE_QUIET_MS: how long the DOM must go without a mutation to be considered settled.
// SETTLE_MAX_CAP_MS: a hard ceiling so a genuinely-never-settling page (a live clock, a running
// animation) can't hang the probe — hitting the cap is an honest, bounded limitation ("captured
// pre-settle"), not a silent one; a page whose real content lands PAST the cap will be captured
// before it's ready.
const SETTLE_QUIET_MS = 200;
const SETTLE_MAX_CAP_MS = 4000;

/** In-page collector: resolves once the DOM has gone SETTLE_QUIET_MS without a mutation, or after
 *  SETTLE_MAX_CAP_MS regardless (never hangs the probe). Run BEFORE the double-rAF paint-settle
 *  step (mutations settling doesn't guarantee a paint has happened yet — belt and suspenders). */
const WAIT_FOR_DOM_QUIESCENCE = ({ quietMs, maxMs }) => new Promise((resolve) => {
  let quietTimer;
  const finish = () => { observer.disconnect(); clearTimeout(quietTimer); clearTimeout(capTimer); resolve(); };
  const observer = new MutationObserver(() => {
    clearTimeout(quietTimer);
    quietTimer = setTimeout(finish, quietMs);
  });
  observer.observe(document.documentElement,
    { childList: true, subtree: true, attributes: true, characterData: true });
  quietTimer = setTimeout(finish, quietMs); // no mutation ever fires -> settle after one quiet window
  const capTimer = setTimeout(finish, maxMs); // never hang past the cap
});

/** Join a route onto a baseURL. Fragment-only ('#/x') and query(+fragment)-only ('?a=1#/x')
 *  routes never touch base's path — `new URL()` resolves these correctly regardless of whether
 *  base carries a trailing slash (this is how the URL spec defines a relative reference that is
 *  only a fragment or a query); this also FIXES the historical hash-route branch, which used to
 *  force a trailing slash onto base before string-concatenating, breaking a FILE-style base (e.g.
 *  '.../prototype-002.html' -> '.../prototype-002.html/#/x' — a dev server's SPA fallback then
 *  silently 200s that as the WRONG page; confirmed against a real multi-page Vite app, captured
 *  the wrong page for all 24 screen/scheme combinations with "0 skipped"). An absolute-path route
 *  ('/x') also ignores base's path entirely, so `new URL()` is already correct there too. A bare
 *  relative route ('x' / 'x.html') is the remaining case: `new URL(route, base)` treats a base
 *  with no trailing slash as a FILE and REPLACES its last path segment instead of appending under
 *  it — normalize a directory-style base to carry a trailing slash first. */
export function joinURL(base, route) {
  if (!route) return base;
  if (route.startsWith('#') || route.startsWith('?') || route.startsWith('/')) {
    return new URL(route, base).href;
  }
  const normalizedBase = base.endsWith('/') ? base : base + '/';
  return new URL(route, normalizedBase).href;
}

/** Did navigation land somewhere other than requested? Compares path (a server-side redirect / a
 *  dev-server SPA fallback) AND hash (a client-side router's auth guard bouncing #/pay -> #/login
 *  — the confirmed real-world case: a fresh unauthenticated context got redirected to the login
 *  screen and the probe captured + labeled it as the gated screen, silently, 0 skipped). Hash is
 *  only compared when the expected route specified one, so a plain path-based app never
 *  false-positives on some unrelated default hash. */
export function routeMismatch(expectedURL, actualURL) {
  try {
    const exp = new URL(expectedURL);
    const act = new URL(actualURL);
    if (exp.pathname !== act.pathname) {
      return { mismatched: true, reason: `path: expected '${exp.pathname}', landed on '${act.pathname}'` };
    }
    if (exp.hash && exp.hash !== act.hash) {
      return { mismatched: true, reason: `hash: expected '${exp.hash}', landed on '${act.hash}'` };
    }
    return { mismatched: false };
  } catch {
    return { mismatched: expectedURL !== actualURL, reason: 'unparseable URL(s) — falling back to a string compare' };
  }
}

async function probeScreen(pw, browser, baseURL, screen, scheme, storageStatePath) {
  const context = await browser.newContext({
    colorScheme: scheme,
    viewport: { width: 1280, height: 800 },
    reducedMotion: 'reduce',
    ...(storageStatePath ? { storageState: storageStatePath } : {}),
  });
  try {
    await context.addInitScript(PERF_INIT);
    const page = await context.newPage();
    const expectedURL = joinURL(baseURL, screen.route);
    await page.goto(expectedURL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.evaluate(WAIT_FOR_DOM_QUIESCENCE, { quietMs: SETTLE_QUIET_MS, maxMs: SETTLE_MAX_CAP_MS });
    await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));

    // Bug 4 (auth-gated routes): detect a redirect AFTER settling (a client-side auth guard's
    // hash-bounce can happen post-load) and skip honestly rather than silently capturing +
    // labeling the wrong screen (e.g. login) under this screen's id.
    const actualURL = page.url();
    const mismatch = routeMismatch(expectedURL, actualURL);
    if (mismatch.mismatched) {
      throw new Error(`redirected — expected ${expectedURL}, landed on ${actualURL} (${mismatch.reason}) ` +
                       `— likely auth-gated; capture skipped, hand-build its cards and mark them ` +
                       `computed-not-measured, or pass --storage-state to authenticate`);
    }

    const textRaws = await page.evaluate(COLLECT_TEXT);
    const setup = await page.evaluate(COLLECT_FOCUS_SETUP);
    const focusRaw = await driveKeyboardFocus(page, setup);
    const perfRaw = await page.evaluate(COLLECT_PERF);
    const i18nRaw = await page.evaluate(COLLECT_I18N);
    return { textRaws, focusRaw, perfRaw, i18nRaw };
  } finally {
    await context.close();
  }
}

/** Drive REAL `page.keyboard.press('Tab')` navigation to measure visible_focus/ring — the only
 *  reliable way to trigger Chromium's actual :focus-visible matching (see top docstring). Bounded
 *  at 2x the enumerated candidate count (floored at 6, for slack — skip links / custom tabindex
 *  can make the walk non-monotonic): a candidate never reached within the bound OMITS
 *  `visible_focus` entirely (UNMEASURED-for-this-element), never a guessed value. */
async function driveKeyboardFocus(page, setup) {
  const candidates = setup.elements;
  await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); });
  const maxPresses = Math.max(candidates.length * 2, 6);
  const visited = new Set();
  let ring = null;
  for (let i = 0; i < maxPresses && visited.size < candidates.length; i++) {
    await page.keyboard.press('Tab');
    const read = await page.evaluate(READ_ACTIVE_ELEMENT);
    if (read.idx < 0 || visited.has(read.idx)) continue;
    visited.add(read.idx);
    const cand = candidates[read.idx];
    cand.visible_focus = read.snapshot !== cand.restSnapshot;
    if (cand.visible_focus && !ring && read.ring) {
      ring = { ...read.ring, from: cand.id };
    }
  }
  const elements = candidates.map(({ id, tabindex, focusable, visible_focus }) =>
    visible_focus === undefined ? { id, tabindex, focusable } : { id, tabindex, focusable, visible_focus });
  return { elements, dom_order: setup.dom_order, targets: setup.targets, modals: setup.modals, ring };
}

async function runProbe(baseURL, invPath, outDir, schemeArg, screenFilter, storageStatePath) {
  const loaded = await loadPlaywright();
  if (!loaded) {
    console.error('ui-probe: playwright not resolvable from CWD or the script tree.');
    console.error(INSTALL_GUIDANCE);
    return 2;
  }
  const inv = JSON.parse(readFileSync(invPath, 'utf-8'));
  let screens = Array.isArray(inv.screens) ? inv.screens : [];
  if (screenFilter) {
    const want = new Set(screenFilter.split(',').map((s) => s.trim()).filter(Boolean));
    screens = screens.filter((s) => want.has(s.id));
  }
  const schemes = schemeArg === 'both' ? ['light', 'dark'] : [schemeArg];
  mkdirSync(outDir, { recursive: true });

  let browser;
  try {
    browser = await loaded.pw.chromium.launch();
  } catch (e) {
    console.error(`ui-probe: chromium failed to launch (${e.message ? e.message.split('\n')[0] : e}).`);
    console.error(INSTALL_GUIDANCE);
    return 2;
  }

  const probed = [];
  const skipped = [];
  try {
    for (const screen of screens) {
      if (!screen || !screen.id) continue;
      if (!screen.route) {
        skipped.push({ id: screen.id, reason: 'no route in inventory — hand-build its cards and report them as computed-not-measured' });
        continue;
      }
      const bySchemes = {};
      let failed = null;
      for (const scheme of schemes) {
        try {
          bySchemes[scheme] = await probeScreen(loaded.pw, browser, baseURL, screen, scheme, storageStatePath);
        } catch (e) {
          failed = `probe failed (${scheme}): ${e.message ? e.message.split('\n')[0] : e}`;
          break;
        }
      }
      if (failed) {
        skipped.push({ id: screen.id, reason: failed });
        continue;
      }
      const first = bySchemes[schemes[0]];
      for (const scheme of schemes) {
        writeCard(outDir, `${screen.id}.${scheme}.surface.json`,
          buildSurfaceCard(screen.id, scheme, bySchemes[scheme].textRaws));
      }
      const ringContrasts = {};
      for (const scheme of schemes) {
        const ring = bySchemes[scheme].focusRaw.ring;
        if (ring) {
          const c = parseCssColor(ring.color);
          if (c) {
            const bg = resolveBgChain(ring.bgChain);
            const fg = c.a < 1 ? compositeOver(c, bg) : c;
            ringContrasts[`contrast_${scheme}`] = contrastRatio(fg, bg);
          }
        }
      }
      writeCard(outDir, `${screen.id}.focus.json`,
        buildFocusCard(screen.id, first.focusRaw, ringContrasts));
      writeCard(outDir, `${screen.id}.budget.json`, buildBudgetCard(screen.id, first.perfRaw));
      writeCard(outDir, `${screen.id}.i18n.json`, buildI18nCard(screen.id, first.i18nRaw));
      probed.push(screen.id);
    }
  } finally {
    await browser.close();
  }

  writeCard(outDir, 'probe-manifest.json', {
    baseURL,
    when: new Date().toISOString(),
    schemes,
    playwright: { resolvedFrom: loaded.resolvedFrom },
    probed,
    skipped,
  });
  console.log(`ui-probe: ${probed.length} screen(s) probed (${schemes.join('+')}), ` +
              `${skipped.length} skipped -> ${outDir}/  (see probe-manifest.json)`);
  for (const s of skipped) console.log(`  - SKIP ${s.id}: ${s.reason}`);
  return probed.length > 0 || screens.length === 0 ? 0 : 1;
}

function writeCard(dir, name, obj) {
  writeFileSync(path.join(dir, name), JSON.stringify(obj, null, 2) + '\n');
}

// ---------------------------------------------------------------------------------------------
// selftest
// ---------------------------------------------------------------------------------------------

const FIXTURE_HTML = `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>ui-probe fixture</title>
<style>
  body { margin: 16px; font-family: sans-serif; background: #ffffff; color: #111111; }
  #muted { color: rgb(119, 119, 119); font-size: 16px; font-weight: 400; }
  #icon-btn { width: 16px; height: 16px; padding: 0; border: 0; box-sizing: border-box;
              background: #1a56db; }
  #ghost-btn { outline: none; width: 64px; height: 32px; border: 1px solid #767676;
               background: #ffffff; color: #111111; }
  #ghost-btn:focus, #ghost-btn:focus-visible { outline: none; }
  #ring-btn { width: 120px; height: 32px; background: #ffffff; border: 1px solid #111111; }
  #ring-btn:focus, #ring-btn:focus-visible { outline: 2px solid #1a56db; }
  #jump:focus, #jump:focus-visible, #icon-btn:focus, #icon-btn:focus-visible,
  #close-btn:focus, #close-btn:focus-visible {
    outline: none; box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.9);
  }
  /* :focus-visible ONLY — no :focus rule at all, base state outline:none. Only a REAL
     keyboard-driven focus can produce a visible delta here; a scripted el.focus() cannot
     (Chromium's :focus-visible heuristic keys off input modality, not "is something focused"). */
  #modern-btn { outline: none; width: 120px; height: 32px; background: #ffffff;
                border: 1px solid #111111; }
  #modern-btn:focus-visible { outline: 2px solid #1a56db; }
</style></head>
<body>
  <h1>Probe fixture</h1>
  <p id="muted">low-contrast muted text</p>
  <p>healthy body text</p>
  <p><a id="jump" href="#main" tabindex="3">positive-tabindex link</a></p>
  <button id="ring-btn">ring me</button>
  <button id="ghost-btn">no ring</button>
  <button id="modern-btn">modern ring</button>
  <button id="icon-btn" aria-label="tiny icon"></button>
  <dialog id="prefs" open>settings <button id="close-btn">close</button></dialog>
  <div id="async-content">loading…</div>
  <script>
    setTimeout(function () {
      document.getElementById('async-content').textContent = 'settled content, no more loading';
    }, 400);
  </script>
</body></html>`;

function approx(actual, expected, tol) {
  return typeof actual === 'number' && Math.abs(actual - expected) <= tol;
}

function unitChecks() {
  const errs = [];
  const ok = (cond, msg) => { if (!cond) errs.push(msg); };

  // contrast math against known values
  ok(approx(contrastRatio({ r: 119, g: 119, b: 119 }, { r: 255, g: 255, b: 255 }), 4.48, 0.01),
     '#777 vs #fff must be ~4.48');
  ok(approx(contrastRatio({ r: 0, g: 0, b: 0 }, { r: 255, g: 255, b: 255 }), 21, 0.01),
     'black vs white must be 21');
  ok(approx(contrastRatio({ r: 255, g: 255, b: 255 }, { r: 119, g: 119, b: 119 }),
            contrastRatio({ r: 119, g: 119, b: 119 }, { r: 255, g: 255, b: 255 }), 1e-9),
     'contrast must be symmetric');

  // color parsing
  ok(JSON.stringify(parseCssColor('rgb(119, 119, 119)')) === JSON.stringify({ r: 119, g: 119, b: 119, a: 1 }),
     'rgb() parse wrong');
  ok(parseCssColor('rgba(0, 0, 0, 0.5)').a === 0.5, 'rgba() alpha parse wrong');
  ok(parseCssColor('rgba(0, 0, 0, 0)').a === 0, 'rgba() zero alpha parse wrong');
  ok(parseCssColor('transparent').a === 0, "'transparent' must parse as alpha 0");
  ok(JSON.stringify(parseCssColor('#1a56db')) === JSON.stringify({ r: 26, g: 86, b: 219, a: 1 }),
     '#hex parse wrong');
  ok(parseCssColor('color(srgb 1 0 0)').r === 255, 'color(srgb) parse wrong');
  ok(parseCssColor('weird(1,2,3)') === null, 'unknown color must parse to null');

  // oklch()/oklab() parsing (Bug 2) — Chromium serializes custom-property-sourced computed
  // colors this way for a modern design system; an unparsed color used to be silently DROPPED,
  // and enough drops emptied a surface card entirely, which contrast-check.py then reported as a
  // trivial false PASS on empty data (UNMEASURED laundered into PASS). Expected values: pure
  // white/black are exact by construction; the oklch(0.627955 0.257683 29.2338) triple is
  // Ottosson's own published sRGB-red round-trip (bottosson.github.io/posts/oklab — the oklch
  // converter's worked example), independently re-derived here via matrices ported from the
  // color-science library (now color-science-project-files; see the oklabToSrgb255 comment
  // above) and cross-checked against them.
  ok(JSON.stringify(parseCssColor('oklch(1 0 0)')) === JSON.stringify({ r: 255, g: 255, b: 255, a: 1 }),
     'oklch(1 0 0) must be pure white — got ' + JSON.stringify(parseCssColor('oklch(1 0 0)')));
  ok(JSON.stringify(parseCssColor('oklch(0 0 0)')) === JSON.stringify({ r: 0, g: 0, b: 0, a: 1 }),
     'oklch(0 0 0) must be pure black — got ' + JSON.stringify(parseCssColor('oklch(0 0 0)')));
  const oklchRed = parseCssColor('oklch(0.627955 0.257683 29.2338)');
  ok(oklchRed && oklchRed.r === 255 && oklchRed.g === 0 && oklchRed.b === 0,
     `oklch red round-trip must be rgb(255,0,0) — got ${JSON.stringify(oklchRed)}`);
  const oklchPct = parseCssColor('oklch(70% 0.1 240)');
  ok(oklchPct && typeof oklchPct.r === 'number', `oklch() percentage L must parse — got ${JSON.stringify(oklchPct)}`);
  const oklchAlpha = parseCssColor('oklch(0.6 0.15 250 / 0.5)');
  ok(oklchAlpha && oklchAlpha.a === 0.5, `oklch() alpha must parse — got ${JSON.stringify(oklchAlpha)}`);
  const oklabWhite = parseCssColor('oklab(1 0 0)');
  ok(oklabWhite && oklabWhite.r === 255 && oklabWhite.g === 255 && oklabWhite.b === 255,
     `oklab(1 0 0) must be pure white — got ${JSON.stringify(oklabWhite)}`);
  ok(parseCssColor('oklch(nonsense)') === null, 'malformed oklch() must parse to null, never guessed');

  // joinURL (Bug 1) — a directory-style base with no trailing slash used to have its last path
  // segment REPLACED by a bare relative route (new URL() treats such a base as a FILE); the
  // hash-route branch separately used to force a trailing slash onto ANY base before
  // string-concatenating, which broke a FILE-style base by inserting a spurious '/' after the
  // filename — confirmed real-world: a Vite dev server's SPA fallback then silently 200'd that
  // malformed URL as the WRONG page (the chooser/landing screen) for every screen/scheme capture.
  ok(joinURL('http://x/sub', 'pay') === 'http://x/sub/pay',
     'a bare relative route onto a no-trailing-slash base must APPEND, not replace the last segment');
  ok(joinURL('http://x/sub/', 'pay') === 'http://x/sub/pay',
     'a bare relative route onto an already-trailing-slash base must be unchanged');
  ok(joinURL('http://x/sub', '/pay') === 'http://x/pay',
     "an absolute-path route must ignore base's path entirely");
  ok(joinURL('http://x/sub/', '#/y') === 'http://x/sub/#/y',
     'a hash route onto a trailing-slash base must be unchanged');
  ok(joinURL('http://localhost:5173/prototype-002.html', '#/statement') ===
     'http://localhost:5173/prototype-002.html#/statement',
     'a hash route onto a FILE-style base must NOT insert a spurious "/" — the confirmed ' +
     'real-world adia-pay failure (Vite\'s SPA fallback then 200s the wrong page)');
  ok(joinURL('http://localhost:5173/prototype-002.html', '?probe=1#/pay') ===
     'http://localhost:5173/prototype-002.html?probe=1#/pay',
     'a query+hash route onto a FILE-style base must preserve the file path');

  // routeMismatch (Bug 4 detection primitive) — the redirect/auth-gate detector.
  ok(routeMismatch('http://x/a', 'http://x/a').mismatched === false, 'identical URLs must not mismatch');
  ok(routeMismatch('http://x/pay', 'http://x/login').mismatched === true,
     'a differing path (server-side redirect / SPA fallback) must mismatch');
  ok(routeMismatch('http://x/app.html#/pay', 'http://x/app.html#/login').mismatched === true,
     'a differing hash on the SAME path (client-side auth-guard bounce) must mismatch');
  ok(routeMismatch('http://x/app.html', 'http://x/app.html#/whatever').mismatched === false,
     'a route with no hash expectation must not false-positive on a landed hash');

  // compositing
  const comp = compositeOver({ r: 0, g: 0, b: 0, a: 0x59 / 255 }, { r: 255, g: 255, b: 255 });
  ok(comp.r === 166 && comp.g === 166 && comp.b === 166, 'source-over compositing math wrong');
  const eff = resolveBgChain(['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0.5)', 'rgb(255, 255, 255)']);
  ok(eff.r === 128 && eff.g === 128 && eff.b === 128, 'bg-chain alpha compositing wrong');
  ok(resolveBgChain(['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)']).r === 255,
     'all-transparent chain must fall back to the white canvas');

  // WCAG large-text classification boundaries
  ok(classifyTextKind(16, 400) === 'normalText', '16px/400 must be normalText');
  ok(classifyTextKind(23.9, 400) === 'normalText', '23.9px/400 must be normalText');
  ok(classifyTextKind(24, 400) === 'largeText', '24px/400 must be largeText');
  ok(classifyTextKind(18.66, 700) === 'largeText', '18.66px/700 must be largeText');
  ok(classifyTextKind(18.5, 700) === 'normalText', '18.5px/700 must be normalText');
  ok(classifyTextKind(19, 400) === 'normalText', '19px/400 must be normalText');

  // surface-card assembly: dedupe + cap + schema + alpha compositing of the fg
  const raw = (over = {}) => ({ name: 'p', color: 'rgb(119, 119, 119)',
    bgChain: ['rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)'], fontSize: 16, fontWeight: 400, ...over });
  const dup = buildSurfaceCard('s', 'light', [raw(), raw(), raw({ color: 'rgb(0, 0, 0)' })]);
  ok(dup.pairs.length === 2 && dup.pairs[0].count === 2 && dup.meta.pairs_deduped === 1,
     'surface card dedupe/count wrong');
  ok(dup.pairs[0].fg === 'rgb(119, 119, 119)' && dup.pairs[0].bg === 'rgb(255, 255, 255)' &&
     dup.pairs[0].kind === 'normalText' && dup.pairs[0].size === 'normal' && dup.pairs[0].role === 'text',
     'surface card pair schema wrong');
  ok(dup.meta.scheme === 'light' && dup.meta.probe === 'rendered', 'surface card meta wrong');
  const alpha = buildSurfaceCard('s', 'light',
    [raw({ color: 'rgba(0, 0, 0, 0.35)' })]);
  ok(alpha.pairs[0].fg === 'rgb(166, 166, 166)',
     'translucent fg must be composited over the effective bg (opaque rgb, no "over")');
  const many = buildSurfaceCard('s', 'light',
    Array.from({ length: 100 }, (_, i) => raw({ color: `rgb(${i}, 0, 0)` })));
  ok(many.pairs.length === 80 && many.meta.pairs_capped === 20, 'surface card cap-at-80 wrong');

  // focus-card assembly: ring contrast per scheme; no ring => no ring key
  const fRaw = { elements: [{ id: '#a', tabindex: 0, focusable: true, visible_focus: true }],
    dom_order: ['#a'], targets: [{ id: '#a', w: 44, h: 44, inline_text: false }],
    modals: [{ id: '#m', open: true }],
    ring: { width_px: 2, color: 'rgb(26, 86, 219)', bgChain: ['rgb(255, 255, 255)'] } };
  const fc = buildFocusCard('s', fRaw, { contrast_light: 6.178, contrast_dark: 4.2 });
  ok(fc.ring && fc.ring.width_px === 2 && fc.ring.contrast_light === 6.18 && fc.ring.contrast_dark === 4.2,
     'focus card ring assembly wrong');
  ok(fc.modals[0].open === true && !('trap' in fc.modals[0]) && !('restore_focus' in fc.modals[0]),
     'modal trap/restore must be omitted (not guessed)');
  const noRing = buildFocusCard('s', { ...fRaw, ring: null }, {});
  ok(!('ring' in noRing), 'absent ring must omit the ring key (checker skips-and-reports)');

  // budget-card assembly: omitted inp/tbt, bundle from js+css
  const bc = buildBudgetCard('s', { lcp_ms: 1200, cls: 0.02, js_kb: 100.24, css_kb: 20, other_kb: 5,
    doc_kb: 3, requests: 7, ttfb_ms: 40, dcl_ms: 300, load_ms: 500 });
  ok(bc.metrics.lcp_ms === 1200 && bc.metrics.cls === 0.02 && bc.metrics.bundle_kb === 120.2 &&
     bc.metrics.requests === 7, 'budget card metrics wrong');
  ok(!('inp_ms' in bc.metrics) && !('tbt_ms' in bc.metrics),
     'inp/tbt must be omitted, not invented');
  const bcNull = buildBudgetCard('s', { lcp_ms: null, cls: 0, js_kb: 0, css_kb: 0 });
  ok(!('lcp_ms' in bcNull.metrics), 'an unmeasured lcp must be omitted, never null');

  // i18n-card assembly
  const ic = buildI18nCard('s', { has_lang: true, has_dir: false });
  ok(ic.surfaces[0].has_lang === true && ic.surfaces[0].has_dir === false &&
     Array.isArray(ic.surfaces[0].hardcoded_strings) && ic.surfaces[0].hardcoded_strings.length === 0,
     'i18n card shape wrong');

  return errs;
}

async function selftest(noBrowser) {
  const errs = unitChecks();
  if (errs.length) {
    console.error(`ui-probe selftest: FAIL (${errs.length} unit check(s))`);
    for (const e of errs) console.error(`  - ${e}`);
    return 1;
  }
  if (noBrowser) {
    console.log('ui-probe selftest: OK (unit checks only — --no-browser: contrast math, color ' +
                'parsing incl. oklch()/oklab(), joinURL, routeMismatch, compositing, text-kind ' +
                'boundaries, card assembly). Browser leg NOT run.');
    return 0;
  }

  const loaded = await loadPlaywright();
  if (!loaded) {
    console.error('ui-probe selftest: SKIP — playwright not resolvable from CWD or the script tree.');
    console.error(INSTALL_GUIDANCE);
    return 2;
  }
  let browser;
  try {
    browser = await loaded.pw.chromium.launch();
  } catch (e) {
    console.error(`ui-probe selftest: SKIP — chromium failed to launch (${e.message ? e.message.split('\n')[0] : e}).`);
    console.error(INSTALL_GUIDANCE);
    return 2;
  }

  const server = http.createServer((req, res) => {
    // Bug 4 fixture: a route that always redirects, standing in for an auth-guarded screen — a
    // real client-side bounce (auth checked, then navigate to #/login) or a server-side one both
    // land the probe somewhere other than requested; a plain HTTP redirect is the simplest
    // deterministic stand-in for the "landed elsewhere" case routeMismatch must catch.
    if (req.url.startsWith('/gated')) {
      res.writeHead(302, { location: '/' });
      res.end();
      return;
    }
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(FIXTURE_HTML);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const baseURL = `http://127.0.0.1:${server.address().port}/`;
  const outDir = mkdtempSync(path.join(os.tmpdir(), 'ui-probe-selftest-'));

  try {
    const result = await probeScreen(loaded.pw, browser, baseURL, { id: 'fixture', route: '/' }, 'light');
    const surface = buildSurfaceCard('fixture', 'light', result.textRaws);
    const ringContrasts = {};
    if (result.focusRaw.ring) {
      const c = parseCssColor(result.focusRaw.ring.color);
      const bg = resolveBgChain(result.focusRaw.ring.bgChain);
      if (c) ringContrasts.contrast_light = contrastRatio(c.a < 1 ? compositeOver(c, bg) : c, bg);
    }
    const focus = buildFocusCard('fixture', result.focusRaw, ringContrasts);
    const budget = buildBudgetCard('fixture', result.perfRaw);
    const i18n = buildI18nCard('fixture', result.i18nRaw);
    writeCard(outDir, 'fixture.light.surface.json', surface);
    writeCard(outDir, 'fixture.focus.json', focus);
    writeCard(outDir, 'fixture.budget.json', budget);
    writeCard(outDir, 'fixture.i18n.json', i18n);

    const ok = (cond, msg) => { if (!cond) errs.push(msg); };

    // --- the cards carry the fixture's known defects, measured -----------------------------
    ok(surface.pairs.some((p) => p.fg === 'rgb(119, 119, 119)' && p.bg === 'rgb(255, 255, 255)' &&
       p.kind === 'normalText'),
       'surface card missing the rgb(119,119,119)-on-white normalText pair');
    const el = (id) => focus.elements.find((e) => e.id === id);
    ok(el('#jump') && el('#jump').tabindex === 3, 'focus card missing tabindex=3 on #jump');
    ok(el('#ghost-btn') && el('#ghost-btn').focusable === true && el('#ghost-btn').visible_focus === false,
       '#ghost-btn (outline:none in every modality — the reverse control) must measure ' +
       'visible_focus:false; a method that makes everything true would wrongly pass this too');
    ok(el('#ring-btn') && el('#ring-btn').visible_focus === true,
       '#ring-btn (2px outline on :focus AND :focus-visible) must measure visible_focus:true');
    // Bug 5, the headline fixture: #modern-btn is styled ONLY via :focus-visible (no :focus rule,
    // outline:none base) — a scripted el.focus() (the old methodology) cannot trigger real
    // :focus-visible matching in Chromium, so the old code measured this as visible_focus:false
    // on a fully-compliant, deliberately-modern component — a mass false positive confirmed
    // against a real app (~60 false NO_VISIBLE_FOCUS findings). Only REAL page.keyboard.press
    // ('Tab') navigation (this file's new methodology) can produce true here.
    ok(el('#modern-btn') && el('#modern-btn').visible_focus === true,
       `#modern-btn (:focus-visible-only ring) must measure visible_focus:true via real keyboard ` +
       `Tab navigation — got ${JSON.stringify(el('#modern-btn'))} (a false 'false' here IS the ` +
       `regression this fixture exists to catch)`);
    const tgt = focus.targets.find((t) => t.id === '#icon-btn');
    ok(tgt && tgt.w === 16 && tgt.h === 16, '#icon-btn must measure 16x16');
    ok(focus.modals.some((m) => m.id === '#prefs' && m.open === true),
       'open <dialog id=prefs> not captured in modals[]');
    ok(focus.ring && focus.ring.width_px === 2 && approx(focus.ring.contrast_light, 6.18, 0.3),
       `ring must be 2px at ~6.18:1 vs white, got ${JSON.stringify(focus.ring)}`);
    ok(typeof budget.metrics.lcp_ms === 'number' && budget.metrics.lcp_ms >= 0,
       'budget card must carry a measured lcp_ms');
    ok(typeof budget.metrics.cls === 'number', 'budget card must carry a measured cls');
    ok(!('inp_ms' in budget.metrics) && !('tbt_ms' in budget.metrics),
       'inp/tbt must stay omitted (UNMEASURED)');
    ok(i18n.surfaces[0].has_lang === true, 'html[lang=en] must measure has_lang:true');
    ok(i18n.surfaces[0].has_dir === false, 'no dir anywhere must measure has_dir:false');

    // --- Bug 3: settle strategy must wait out setTimeout-scheduled DOM updates -------------
    // #async-content shows a "loading…" placeholder at load, replaced by real content via
    // setTimeout(400ms). A bare double-rAF (the old strategy) resolves within ~2 paint ticks
    // (single-digit ms in a headless browser) — nowhere near 400ms — so it would have captured
    // the placeholder. Prove the NEW settle actually waited past that naive baseline (elapsed
    // time, not just a specific outcome) AND landed on the real content, via a second direct
    // probe reusing the same fixture + settle path.
    {
      const context2 = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page2 = await context2.newPage();
      const t0 = Date.now();
      await page2.goto(baseURL, { waitUntil: 'networkidle', timeout: 30000 });
      await page2.evaluate(WAIT_FOR_DOM_QUIESCENCE, { quietMs: SETTLE_QUIET_MS, maxMs: SETTLE_MAX_CAP_MS });
      await page2.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
      const elapsedMs = Date.now() - t0;
      const asyncText = await page2.evaluate(() =>
        document.getElementById('async-content') && document.getElementById('async-content').textContent);
      await context2.close();
      ok(asyncText === 'settled content, no more loading',
         `settle must capture the REAL setTimeout-injected content, not the loading placeholder ` +
         `— got ${JSON.stringify(asyncText)}`);
      ok(elapsedMs > 300,
         `settle must take measurably longer than a bare double-rAF (a few ms) to clear the ` +
         `400ms setTimeout + ${SETTLE_QUIET_MS}ms quiet window — only took ${elapsedMs}ms, ` +
         `suggesting the mutation-quiescence wait did not actually run`);
    }

    // --- Bug 4: a redirected route must be detected and SKIPPED, never silently captured ---
    // /gated always 302s to '/' (standing in for an auth-guard bounce). probeScreen must throw
    // (routeMismatch fires) rather than return a card labeled under the requested screen id.
    {
      let redirectReason = null;
      try {
        await probeScreen(loaded.pw, browser, baseURL, { id: 'gated', route: 'gated' }, 'light');
      } catch (e) {
        redirectReason = e.message;
      }
      ok(redirectReason !== null,
         'a redirected route must throw so runProbe reports a SKIP — a captured card under the ' +
         'wrong screen id is the exact silent-mislabeling failure this fixture exists to catch');
      ok(redirectReason && /redirected/i.test(redirectReason) && redirectReason.includes(joinURL(baseURL, 'gated')),
         `redirect-skip reason must name both the expected and actual URL — got ${JSON.stringify(redirectReason)}`);
    }

    // --- pipe the generated cards through the REAL checkers --------------------------------
    const skillsDir = path.resolve(SCRIPT_DIR, '..', '..');
    const checkers = [
      { py: path.join(skillsDir, 'check-colors', 'scripts', 'contrast-check.py'),
        card: path.join(outDir, 'fixture.light.surface.json'), gates: ['CONTRAST_FAIL_AA'] },
      { py: path.join(skillsDir, 'focus-verify', 'scripts', 'focus-check.py'),
        card: path.join(outDir, 'fixture.focus.json'),
        gates: ['TARGET_TOO_SMALL', 'NO_VISIBLE_FOCUS', 'POSITIVE_TABINDEX'] },
    ];
    for (const { py, card, gates } of checkers) {
      if (!existsSync(py)) {
        console.log(`  · checker leg SKIPPED (not found: ${py}) — card-fact assertions still ran`);
        continue;
      }
      const run = spawnSync('python3', [py, card], { encoding: 'utf-8' });
      const output = (run.stdout || '') + (run.stderr || '');
      ok(run.status === 1, `${path.basename(py)} must FAIL (exit 1) on the defect card, got ${run.status}`);
      for (const gate of gates) {
        ok(output.includes(gate), `${path.basename(py)} must fire ${gate}; output was:\n${output}`);
      }
    }
  } catch (e) {
    errs.push(`browser leg crashed: ${e.stack || e}`);
  } finally {
    await browser.close();
    server.close();
  }

  if (errs.length) {
    console.error(`ui-probe selftest: FAIL (${errs.length})`);
    for (const e of errs) console.error(`  - ${e}`);
    console.error(`  cards left for inspection in ${outDir}`);
    return 1;
  }
  rmSync(outDir, { recursive: true, force: true });
  console.log('ui-probe selftest: OK — units + browser leg (fixture probed headless; cards carry ' +
              'the planted defects, including real-keyboard :focus-visible-only ring detection and ' +
              'a setTimeout-settled async pair; a redirected route SKIPPED, never mislabeled; real ' +
              'checkers fired CONTRAST_FAIL_AA / TARGET_TOO_SMALL / NO_VISIBLE_FOCUS / ' +
              `POSITIVE_TABINDEX). playwright: ${loaded.resolvedFrom}`);
  return 0;
}

// ---------------------------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------------------------

async function main(argv) {
  if (argv[0] === 'selftest') {
    return selftest(argv.includes('--no-browser'));
  }
  let baseURL = null;
  let invPath = null;
  let outDir = 'cards';
  let scheme = 'light';
  let screenFilter = null;
  let storageStatePath = null;
  const args = [...argv];
  while (args.length) {
    const a = args.shift();
    if (a === '--inventory') invPath = args.shift();
    else if (a === '--out') outDir = args.shift();
    else if (a === '--scheme') scheme = args.shift();
    else if (a === '--screens') screenFilter = args.shift();
    else if (a === '--storage-state') storageStatePath = args.shift();
    else if (!baseURL) baseURL = a;
    else { console.error(`unexpected argument ${a}`); return 2; }
  }
  if (!baseURL || !invPath) {
    console.error('usage: node ui-probe.mjs <baseURL> --inventory inventory.json [--out cards/] ' +
                  '[--scheme light|dark|both] [--screens id,id] [--storage-state path.json] | ' +
                  'selftest [--no-browser]');
    return 2;
  }
  if (!['light', 'dark', 'both'].includes(scheme)) {
    console.error(`--scheme must be light|dark|both, got ${scheme}`);
    return 2;
  }
  return runProbe(baseURL, invPath, outDir, scheme, screenFilter, storageStatePath);
}

// Guard the CLI entrypoint so importing this module (to reuse its exported pure functions/card
// builders — e.g. a supplementary tool composing buildFocusCard/buildBudgetCard/buildI18nCard)
// never re-executes main() against the IMPORTER's argv or launches a browser as a side effect.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
}
