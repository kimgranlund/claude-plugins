// Site shell — sets up navigation and global behavior.

import { el } from './utils.js';

// Grouped demo catalog. Each item's `href` is written as if from a root;
// resolveHref() rewrites it to be relative to the current page.
const DEMO_GROUPS = [
  {
    label: 'Core color science',
    items: [
      { href: '/examples/pages/picker.html',        label: 'OKLCh picker' },
      { href: '/examples/pages/okhsl.html',         label: 'OKHSL picker' },
      { href: '/examples/pages/gradient.html',      label: 'Gradient comparison' },
      { href: '/examples/pages/blendwhite.html',    label: 'Blend through white' },
      { href: '/examples/pages/transfer.html',      label: 'Transfer curves' },
      { href: '/examples/pages/chromaticity.html',  label: 'CIE xy chromaticity' },
      { href: '/examples/pages/illuminants.html',   label: 'Spectral illuminants' },
      { href: '/examples/pages/wavelength.html',    label: 'Wavelength → color' },
      { href: '/examples/pages/cmf.html',           label: 'Cone fundamentals' },
    ],
  },
  {
    label: 'Gamut & mapping',
    items: [
      { href: '/examples/pages/gamut.html',         label: 'Gamut envelope' },
      { href: '/examples/pages/mapping.html',       label: 'Gamut mapping playground' },
      { href: '/examples/pages/wheel.html',         label: 'Perceptual hue wheel' },
      { href: '/examples/pages/ramp.html',          label: 'Token ramp generator' },
      { href: '/examples/pages/tonemap.html',       label: 'HDR tone mapping' },
      { href: '/examples/pages/kelvin.html',        label: 'Color temperature (Kelvin)' },
    ],
  },
  {
    label: 'Accessibility & perception',
    items: [
      { href: '/examples/pages/contrast.html',      label: 'Contrast (WCAG + APCA)' },
      { href: '/examples/pages/cvd.html',           label: 'Color-blindness simulator' },
      { href: '/examples/pages/cvdsafe.html',       label: 'CVD-safe palette' },
      { href: '/examples/pages/deltae.html',        label: 'ΔE metric comparator' },
      { href: '/examples/pages/harmony.html',       label: 'Color harmony generator' },
      { href: '/examples/pages/ciecam16.html',      label: 'CIECAM16 viewing conditions' },
      { href: '/examples/pages/adapt.html',         label: 'Chromatic adaptation' },
    ],
  },
  {
    label: 'Image analysis',
    items: [
      { href: '/examples/pages/palette.html',       label: 'Palette extraction' },
      { href: '/examples/pages/imagestats.html',    label: 'Image color analysis' },
      { href: '/examples/pages/dither.html',        label: 'Floyd-Steinberg dithering' },
    ],
  },
  {
    label: 'Tokens, schemes & CSS',
    items: [
      { href: '/examples/pages/tonal.html',         label: 'Material 3 tonal palette' },
      { href: '/examples/pages/csscolor5.html',     label: 'CSS Color 5/6 playground' },
      { href: '/examples/pages/procedural.html',    label: 'Procedural palettes' },
      { href: '/examples/pages/pigment.html',       label: 'Kubelka-Munk paint mixer' },
      { href: '/examples/pages/namer.html',         label: 'Color namer' },
    ],
  },
  {
    label: 'Foundations & illusions',
    items: [
      { href: '/examples/pages/macadam.html',       label: 'MacAdam ellipses' },
      { href: '/examples/pages/illusions.html',     label: 'Color illusions' },
      { href: '/examples/pages/volume.html',        label: 'Color volume comparison' },
      { href: '/examples/pages/cube3d.html',        label: '3D sRGB cube in OKLab' },
      { href: '/examples/pages/match.html',         label: 'Color matching game' },
      { href: '/examples/pages/apcatable.html',     label: 'APCA reading table' },
      { href: '/examples/pages/multidither.html',   label: 'Multi-dither comparison' },
      { href: '/examples/pages/scatter.html',       label: 'Image chromaticity scatter' },
    ],
  },
  {
    label: 'Josef Albers',
    items: [
      { href: '/examples/pages/albers-who.html',          label: '01 · Who was Josef Albers?' },
      { href: '/examples/pages/albers-relational.html',   label: '02 · Color is relational' },
      { href: '/examples/pages/albers-book.html',         label: '03 · The book as a learning system' },
      { href: '/examples/pages/albers-deception.html',    label: '04 · Color deception' },
      { href: '/examples/pages/albers-simultaneous.html', label: '05 · Simultaneous contrast' },
      { href: '/examples/pages/albers-one-as-two.html',   label: '06 · One color appearing as two' },
      { href: '/examples/pages/albers-two-as-one.html',   label: '07 · Two colors appearing as one' },
      { href: '/examples/pages/albers-homage.html',       label: '08 · Homage to the Square system' },
      { href: '/examples/pages/albers-square.html',       label: '09 · Why the square?' },
      { href: '/examples/pages/albers-proportion.html',   label: '10 · Proportion, area, weight' },
      { href: '/examples/pages/albers-warm-cool.html',    label: '11 · Temperature is contextual' },
      { href: '/examples/pages/albers-transparency.html', label: '12 · Transparency illusions' },
      { href: '/examples/pages/albers-afterimage.html',   label: '13 · Afterimage & optical memory' },
      { href: '/examples/pages/albers-vs-science.html',   label: '14 · Albers vs. scientific models' },
      { href: '/examples/pages/albers-digital.html',      label: '15 · Albers for digital design' },
      { href: '/examples/pages/albers-lab.html',          label: '16 · Color lab' },
    ],
  },
];

// Resolve nav hrefs relative to where the current page lives.
function resolveHref(rawHref) {
  const path = window.location.pathname;
  const inPages = path.includes('/examples/pages/');
  const inExamplesRoot = path.endsWith('/examples/index.html') || path.endsWith('/examples/');

  if (inPages) {
    if (rawHref === '/examples/index.html') return '../index.html';
    if (rawHref.startsWith('/examples/pages/')) return './' + rawHref.slice('/examples/pages/'.length);
  }
  if (inExamplesRoot) {
    if (rawHref === '/examples/index.html') return './index.html';
    if (rawHref.startsWith('/examples/pages/')) return './pages/' + rawHref.slice('/examples/pages/'.length);
  }
  return rawHref;
}

function currentFilename() {
  return window.location.pathname.split('/').pop() || 'index.html';
}

function mountSkipLink() {
  // First focusable element on every page — keyboard users hit Tab and get a
  // visible "skip to content" link that jumps past the header nav.
  const main = document.querySelector('.app-main');
  if (!main || document.querySelector('.skip-link')) return;
  if (!main.id) main.id = 'main';
  const link = el('a', { class: 'skip-link', href: '#main' }, 'skip to content');
  document.body.insertBefore(link, document.body.firstChild);
}

function mountHeader() {
  const header = document.querySelector('.app-header');
  if (!header || header.dataset.mounted) return;
  header.dataset.mounted = '1';

  const brandHref = resolveHref('/examples/index.html');
  const here = currentFilename();

  // Build the select with optgroup'd options.
  const select = el('select', { class: 'app-nav-select', 'aria-label': 'Jump to demo' });
  // Placeholder option (only shown when none of the page options match).
  const placeholder = el('option', { value: '', disabled: 'true' }, 'Jump to demo…');
  select.append(placeholder);

  let matchedCurrent = false;
  for (const group of DEMO_GROUPS) {
    const og = el('optgroup', { label: group.label });
    for (const item of group.items) {
      const resolved = resolveHref(item.href);
      const opt = el('option', { value: resolved }, item.label);
      if (resolved.split('/').pop() === here) {
        opt.setAttribute('selected', 'true');
        matchedCurrent = true;
      }
      og.append(opt);
    }
    select.append(og);
  }
  if (!matchedCurrent) placeholder.setAttribute('selected', 'true');

  select.addEventListener('change', () => {
    if (select.value) window.location.href = select.value;
  });

  // "Home" anchor stays separate so users always have a way back without
  // touching the select.
  const isHome = here === 'index.html' || here === '';
  const homeLink = el('a', {
    href: brandHref,
    class: 'app-nav-home',
    'aria-current': isHome ? 'page' : null,
  }, 'Home');

  header.innerHTML = '';
  header.append(
    el('a', { class: 'app-header__brand', href: brandHref },
      el('span', { class: 'app-header__brand-dot' }),
      'ref-color ',
      el('small', {}, 'examples'),
    ),
    el('nav', { class: 'app-nav' }, homeLink, select),
  );
}

function mountFooter() {
  const footer = document.querySelector('.app-footer');
  if (!footer || footer.dataset.mounted) return;
  footer.dataset.mounted = '1';
  footer.innerHTML = '';
  footer.append(
    el('p', {},
      'Static demos dogfooding ',
      el('code', {}, 'ref-color'),
      '. Color math: ',
      el('a', { href: 'https://bottosson.github.io/posts/oklab/', target: '_blank', rel: 'noreferrer' }, 'Ottosson 2020'),
      ', ',
      el('a', { href: 'https://www.myndex.com/APCA/', target: '_blank', rel: 'noreferrer' }, 'APCA'),
      ', ',
      el('a', { href: 'https://www.w3.org/TR/css-color-4/', target: '_blank', rel: 'noreferrer' }, 'CSS Color 4'),
      '. No frameworks, no build step at runtime — just compiled TS modules. ',
      el('span', { style: { opacity: '0.7' } },
        'Tip: press ',
        el('kbd', {}, '['),
        ' / ',
        el('kbd', {}, ']'),
        ' to navigate demos.'
      )
    )
  );
}

// Keyboard navigation: `[` = previous demo, `]` = next demo. Wraps at the
// ends, crosses section boundaries within DEMO_GROUPS order. Skipped when the
// user is typing in a form field so hex/number inputs don't get hijacked.
function installKeyNav() {
  const flat = [];
  for (const group of DEMO_GROUPS) for (const item of group.items) flat.push(item.href);

  function isTyping(target) {
    if (!target) return false;
    const tag = target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true;
    if (target.isContentEditable) return true;
    return false;
  }

  document.addEventListener('keydown', (e) => {
    if (e.key !== '[' && e.key !== ']') return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (isTyping(e.target)) return;

    const here = currentFilename();
    let idx = flat.findIndex(h => h.split('/').pop() === here);

    let target;
    if (idx === -1) {
      // Not in the list (e.g. on index.html). Go to first or last demo.
      target = e.key === ']' ? flat[0] : flat[flat.length - 1];
    } else {
      const n = flat.length;
      const next = e.key === ']' ? (idx + 1) % n : (idx - 1 + n) % n;
      target = flat[next];
    }
    window.location.href = resolveHref(target);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => { mountSkipLink(); mountHeader(); mountFooter(); installKeyNav(); });
} else {
  mountSkipLink();
  mountHeader();
  mountFooter();
  installKeyNav();
}
