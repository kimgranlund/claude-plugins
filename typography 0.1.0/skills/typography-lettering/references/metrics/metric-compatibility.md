---
date: 2026-04-18
coverage: medium
peers:
  - ./anatomy.md
  - ./metrics-glossary.md
  - ./units.md
  - ../contemporary/metric-overrides.md
  - ../techniques/fallback-stacks.md
primary_sources:
  - https://seek-oss.github.io/capsize/
  - https://github.com/seek-oss/capsize
  - https://wakamaifondue.com/
  - https://fontdrop.info/
  - https://samsa-family.github.io/samsa/
  - https://github.com/fonttools/fonttools
  - https://github.com/unjs/fontaine
  - https://modernfontstacks.com/
  - https://web.dev/articles/preload-optional-fonts
  - https://simonhearne.com/2021/layout-shifts-webfonts/
  - https://web.dev/blog/font-metric-overrides
  - https://calendar.perfplanet.com/2020/a-font-loading-strategy-to-prevent-fout-and-flash-of-invisible-text/
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2
  - https://developer.chrome.com/blog/framework-tools-font-fallback
  - https://github.com/w3c/IFT
---

# Metric compatibility — metrics reference

Two fonts are **metric-compatible** when their key vertical and horizontal
metrics — x-height, cap-height, ascender, descender, advance-width averages,
baseline position — are close enough that substituting one for the other
causes no visible density change and no layout shift. The practical goal is
a fallback font the user never notices is a fallback.

This file covers the **how-to-know**: what to measure, which tools to use,
what "close enough" means per script, and how to verify. For the mechanism
(`@font-face` descriptors), see `../contemporary/metric-overrides.md`. For a
catalog of production-ready pairings, see `../techniques/fallback-stacks.md`.
For the binary-table source of truth behind every quantity below, see
`./metrics-glossary.md`.

---

## Why Metric Compatibility Matters

When the browser resolves `font-family: "Inter", sans-serif;` the UA paints
immediately with its resolved `sans-serif` — Arial on Windows, Helvetica /
SF Pro on macOS, Roboto on Android, Liberation Sans on most Linux. Under
`font-display: swap` (or the default `auto`/`block`), when Inter arrives the
browser re-lays-out with Inter's metrics. Every line below the first moves.
That motion is **Cumulative Layout Shift (CLS)** — a Core Web Vital with a
"good" budget of < 0.1 per page.

The mismatch is rarely about shape. It is about the vertical line-box and
horizontal advance. Inter vs Arial normalized to em:

| Font  | Ascent | Descent | Line-gap | x-height | UPM  |
| ----- | -----: | ------: | -------: | -------: | ---: |
| Inter | 0.968  | 0.242   | 0.000    | 0.546    | 1000 |
| Arial | 0.905  | 0.212   | 0.033    | 0.519    | 2048 |

A 16px line of Inter reserves 19.36px; the same line in Arial reserves
18.40px. Over a 40-line article, that is ~38px of vertical drift on swap.
Simon Hearne (2021) measured real pages shifting CLS from 0.18 → 0.005
after fallback-metric tuning — a 35× improvement with no glyph change.
Barry Pollard (Smashing, 2022) reports similar production deltas.

Metric compatibility is therefore upstream of three concerns:

1. **Core Web Vitals CLS budget** — mismatched metrics are the leading
   font-related cause of layout shift.
2. **Reading experience** — line heights and x-heights that change mid-read
   are perceived as "flickering" even when the shift is subliminal.
3. **Design proportions** — vertical rhythm, icon-text alignment, and grid
   snapping all assume a stable line-box height.

---

## The Metrics That Actually Matter

Ordered by impact on perceived compatibility, not by spec prominence. Every
field below is sourced from `OS/2` or `head`; see `./metrics-glossary.md`
for table locations.

### x-height (most impactful)

The single most important metric for density and perceived size at body
copy. A primary with x-height 0.546 em against a fallback at 0.519 em looks
~5% smaller during FOUT — lines feel less "heavy", counters look more open.
Because most lowercase mass sits at or below the x-line, this drives the
page's optical weight. The Capsize formula uses the x-height *ratio* as the
primary `size-adjust` driver. Comes from `OS/2.sxHeight` (OS/2 v2+); when
absent, tools measure the bounding box of `x` (U+0078).

### Cap-height

Second-order impact. Matters for all-caps runs, headings, and icon
alignment. Comes from `OS/2.sCapHeight` (OS/2 v2+); fallback to measuring
`H` when absent. Capsize's production formula blends x-height and cap-height
so caps and lowercase both align at the same `font-size` — hence the
typical ~2% correction over the pure x-height ratio (Inter→Arial: 105.2%
x-height-only vs 107.12% cap-corrected).

### Ascender / Descender (line-box budget)

These set the *vertical box* the line occupies. Mismatched ascent/descent
is what actually produces CLS — the text appears to leap when the browser
re-reserves vertical space on swap. Read from `OS/2.sTypoAscender`,
`OS/2.sTypoDescender` (negative in file; use absolute), and `hhea.ascender`/
`hhea.descender`. Modern fonts with `USE_TYPO_METRICS=1` unify these; legacy
fonts don't. See `./metrics-glossary.md#the-metric-wars`.

### Advance-width averages

Horizontal impact. Drives where lines wrap. A fallback with wider advances
produces shorter lines — last words wrap differently — so prose reflows
horizontally on swap. `size-adjust` scales every advance uniformly, which
approximates but doesn't per-glyph-match horizontal fit. Monospaces are
immune (all advances fixed). Proportional fonts with > 8% horizontal
divergence (e.g., Poppins vs Arial) still show subtle horizontal CLS even
with perfect vertical tuning. No `advance-override` descriptor exists — it
was dropped from CSS Fonts 4 in 2020.

### Line-gap

Usually 0 in modern variable web fonts (Inter, Roboto, Geist, SF Pro)
because they pack the leading into ascent+descent. Arial is 3.3%, Times New
Roman 4.2%. Missing `line-gap-override: 0%` on the fallback causes
double-leading during FOUT. See `../contemporary/metric-overrides.md#pitfalls`.

### Units per em (UPM)

Not a compatibility axis itself — it is the denominator that makes all
other metrics comparable. 1000 is typical for CFF/PostScript (Adobe, most
Google Fonts); 2048 is typical for TrueType (Microsoft legacy, Arial,
Georgia, Times). Comparing raw unit values across fonts without
normalizing by UPM is a common beginner error; always divide by UPM first.
See `./metrics-glossary.md#upm-units-per-em`.

---

## How to Measure

### Capsize + `@capsizecss/metrics` — the reference

Capsize (Michael Taranto, Seek, 2020; current v5, 2026) is the canonical
algorithm and ships pre-extracted metrics for most Google Fonts and common
system fonts via `@capsizecss/metrics`. `createFontStack()` emits the
`@font-face` CSS directly. Reads `OS/2.sTypoAscender`, `sTypoDescender`,
`sTypoLineGap`, `sxHeight`, `sCapHeight`, and `head.unitsPerEm`, with
bounding-box fallback for `sxHeight` / `sCapHeight` when the OS/2 v2 fields
are absent.

### Wakamai Fondue — pedagogical web inspector

`wakamaifondue.com` (Roel Nieskens). Drop a font file (`.ttf`, `.otf`,
`.woff2`), see every `OS/2` and `hhea` metric, every OpenType feature, every
variable-font axis. Good for explaining the metric wars to stakeholders.
Does not emit CSS overrides.

### FontDrop — binary inspection

`fontdrop.info` (Viktor Nübel). Drag-and-drop, browser-side parsing. Shows
all metric tables, the `fsSelection` bits (including `USE_TYPO_METRICS`
bit 7), and `MVAR` deltas if present. Tab labelled "Metrics" exposes the
exact integers to feed Capsize.

### Samsa — variable-font aware

`samsa-family.github.io/samsa` (Laurence Penney). Handles variable fonts
correctly — lets you inspect metrics at specific axis positions, which
matters for fonts with `opsz` (x-height shifts) or `wdth` (advances shift).
Essential when measuring a variable-font primary for an override intended
to live against the user's most-common axis position, not the default.

### FontTools / TTX — command-line, scriptable

`pip install fonttools`, then `ttx -t OS/2 -t hhea -t head Font.ttf` dumps
XML. Scriptable via `from fontTools.ttLib import TTFont`. The batch tool
when you own a licensed library not in Capsize's registry. Google Fonts
uses `fontbakery` (built on fonttools) to audit vertical metrics during
ingestion.

### Fontaine — auto-generates at build time

`unjs/fontaine` (2026). Vite / Nuxt / PostCSS plugin that scans `@font-face`
rules, looks up metrics in `@capsizecss/metrics`, and injects fallback
aliases. Zero hand-computation. Handles the common case; falls back to
error if the primary is not in the registry.

### fontpie — CLI override generation

`fontpie Font.ttf --fallback Arial` prints a ready-to-paste `@font-face`.
Useful for licensed fonts where you have the binary but no build
integration. Uses the Capsize formula internally.

### Next.js `next/font`

`next/font/google('Inter')` / `next/font/local(…)` emits primary + tuned
fallback automatically at build. The fallback values are the Capsize
outputs (Next.js imports `@capsizecss/metrics`). For any project already on
Next.js, this is the path of least resistance.

### Tool selection — 2026-04

| Tool | Input | Output | When to reach |
| ---- | ----- | ------ | ------------- |
| **Capsize** (lib) | Metrics object or font file | Computed CSS | You control build; need precise values |
| **`@capsizecss/metrics`** | Font name string | Pre-extracted metrics | Font is in the registry (most Google Fonts) |
| **Wakamai Fondue** | Drag-and-drop | HTML inspection | Teaching, auditing; no CSS |
| **FontDrop** | Drag-and-drop | HTML inspection | Quick metric reads, `fsSelection` checks |
| **Samsa** | Font file | Variable-font inspection | Measuring at specific axis positions |
| **TTX / fontTools** | Font file | XML dump, Python API | Scripted audits, licensed libraries |
| **Fontaine** | Your `@font-face` CSS | Rewrites with fallback aliases | Vite / Nuxt / Vue projects |
| **fontpie** | Font file path | CSS string | CLI in any toolchain |
| **Next.js `next/font`** | Import call | Primary + tuned fallback | Next.js projects |
| **Modernfontstacks.com** (Dan Klammer) | Genre pick | OS-native stacks grouped by feel | No web font at all; pure system |

Prefer tools over hand-computation. Hand-compute only when the primary is a
licensed face whose metrics are outside every registry.

---

## The Override Recipe (Summary — Full Derivation in `../contemporary/metric-overrides.md`)

Given primary `P` and fallback `F`, both normalized to em (each raw metric
divided by its font's UPM):

```
size-adjust       = P.xHeight_em / F.xHeight_em         (face-level; fixes CLS)
ascent-override   = P.ascent_em  / size-adjust
descent-override  = P.descent_em / size-adjust
line-gap-override = P.lineGap_em / size-adjust
```

All four outputs multiply by 100 to become the `%` the descriptor expects.
Apply within the `@font-face` rule of the **fallback** (not the primary).
Why divide by `size-adjust`: the three override percentages are taken
against the *post-size-adjust* em, so dividing compensates for the scale.

See `../contemporary/metric-overrides.md#computing-values` for the full
four-step derivation including the optional cap-height refinement.

---

## Common Pairings — Compute, Don't Copy

The full table lives in `../techniques/fallback-stacks.md`. What this file
emphasizes is **how to verify**: measurements drift across font versions
(Inter 3.x vs 4.x have different x-heights; Google Fonts re-normalized in
2023), across extraction tools (FontDrop vs Capsize's stored metrics can
differ by ~0.1% due to glyph-bounding-box vs table-field resolution), and
across system-font updates (Arial on Windows 11 23H2 differs from Arial on
Windows 10 LTSC 2019).

Canonical pairings worth knowing as a compatibility benchmark (see
`../techniques/fallback-stacks.md` for the tuned override CSS):

- **Inter → Arial** — geometric sans → neo-grotesque; ~7% size-adjust.
  Close enough that even without overrides the mismatch is small.
- **Geist → system-ui sans** — Vercel's Geist has near-identical metrics
  to Arial and SF Pro (designed that way); ~0% size-adjust.
- **Roboto → Arial** — Roboto's x-height (0.528) is close to Arial's
  (0.519); ~2% size-adjust.
- **Source Sans → Helvetica / Arial** — humanist sans; larger descent
  override (~30%) than geometric sans.
- **Helvetica Neue → Arial** — Arial was commissioned by Monotype (1982)
  as a metric-compatible Helvetica clone; identical advance widths, near-
  identical ascent/descent. Overrides stay under 2% off 100%.
- **Georgia → Times New Roman** — Georgia was designed by Matthew Carter
  for screen; larger x-height (0.481) than Times (0.447); 10–15% size-adjust
  when using Times as Georgia's fallback (rare; Georgia has been a system
  default on macOS and Windows for 25+ years).
- **Merriweather → Georgia** — book serif to screen serif; Merriweather
  ships an unusual 25% line-gap for diacritic headroom. Replicate it in the
  fallback or lines collapse visibly.
- **Playfair Display → Georgia** — display serif with tall caps; overrides
  push `ascent-override` above 100% because Playfair's caps tower over
  Georgia's shorter ascenders.
- **IBM Plex Sans → system-ui** — Plex targets metric parity with SF Pro
  and Segoe; overrides near 100%.
- **IBM Plex Mono → ui-monospace → Menlo / Consolas / monospace** — all
  monospaces share advance widths, so horizontal CLS is zero; only vertical
  box needs tuning. `size-adjust` typically 105–110% because Plex Mono's
  x-height is smaller than Menlo's.
- **Lato → system-ui** — close to Segoe UI; mid-range humanist.

For every one of these, verify against your current font version, because
Google Fonts' 2023 normalization pass shifted several families' metrics by
up to 2%. The values in `fallback-stacks.md` are dated 2026-04 and pinned
to Capsize's registry at that date.

---

## Script-Specific Considerations

The x-height-centric approach above is a Latin convention. Other scripts
require different compatibility axes. See also the per-script files in
`../scripts/`.

### Latin

The approach above works cleanly. x-height + cap-height cover ~95% of the
perceived-density problem; advance widths cover most of the remainder.

### CJK (Chinese / Japanese / Korean)

CJK fonts often have no "x-height" in the Latin sense — every glyph fills
the em-box. Compatibility is measured via:

- **Ideographic-box alignment** — the square the glyph is designed to
  occupy. Hiragino Sans, Noto Sans CJK, and Yu Gothic all target the em-box
  closely; PingFang is slightly tighter.
- **Punctuation width** — full-width (ASCII punctuation rendered at 1 em)
  vs half-width vs proportional. Mismatches here cause visible gaps around
  periods and commas.
- **Baseline offset** — many CJK fonts have asymmetric ascent/descent
  relative to Latin expectations.

CJK fonts are typically 15–30 MB per weight for full subsets. The fallback
is often visually acceptable as a persistent choice, not a placeholder —
see `../techniques/fallback-stacks.md#cjk`.

### Arabic

Arabic's baseline sits mid-letter, not bottom-aligned. Ascender /
descender don't map to x-height / cap-height conventions. Compatibility
requires:

- **Baseline-offset matching** — where the baseline sits within the em-box.
- **Connecting-stroke position** — the horizontal line glyphs connect along.
- **Contextual-form metrics** — isolated, initial, medial, final. A font
  with different isolated-vs-medial heights will swap badly even if its
  overall ascent matches.

`size-adjust` can correct gross mass mismatches; finer baseline alignment
needs per-script tuning. See `../scripts/arabic.md`.

### Devanagari

**Shirorekha** (headline) must align across fonts — otherwise the top rule
appears to jump. Acts as a pseudo-cap-height constraint unique to Devanagari.
Conjuncts and vowel signs (matras) extend above and below the shirorekha;
ascender/descender budgets are larger than Latin. Noto Sans Devanagari,
Mukti, and Yatra One all target similar shirorekha heights for this reason.
See `../scripts/devanagari.md`.

### Hebrew

Unicameral — no uppercase/lowercase distinction, so "x-height" equivalent
is the height of all consonants. Otherwise similar Latin mechanics apply to
ascent/descent. Nikud (vowel points) and cantillation marks stack above and
below and demand extra line-height — even when not rendered, the font's
line-box budgets for them. Heebo, Rubik, and IBM Plex Hebrew are authored
for metric compatibility with their Latin siblings; use `size-adjust` to
tune for bilingual Hebrew+Latin layouts. See `../scripts/hebrew.md`.

### Greek and Cyrillic

Broadly Latin-like mechanics. Cyrillic is sometimes drawn slightly darker
than Latin at the same weight — not a metric issue but a color/density one.
Greek italic cuts redraw α, γ, ζ, κ, λ — visual not metric.

---

## Variable Fonts and Metric Compatibility

Variable-font metrics can drift across axis positions:

- **`opsz`** — x-height and cap-height tend to grow at small optical sizes
  (text cuts) and shrink at display cuts. Roboto Flex's x-height shifts
  from ~0.53 at opsz=8 to ~0.49 at opsz=144. Compute overrides against the
  axis position your users see most (usually the opsz=16 body position, not
  the axis default).
- **`wdth`** — Width shifts advance widths dramatically. A `wdth: 75`
  condensed variant may be 20% narrower than the default; it is not
  metric-compatible with its own regular width.
- **`wght`** — Slight x-height compensation in most families (heavier
  weights add optical weight at the x-line); usually within tolerance.

No CSS override descriptor is per-axis as of 2026-04. One set of values
applies regardless of `font-variation-settings`. The practical rule: compute
against the **most-used instance** (typically body weight, default width,
opsz ≈ 16) and accept drift at extremes. `MVAR` stores per-instance metric
deltas for tools to read; see `./metrics-glossary.md#mvar-metric-deltas`.

For the variable-font axis reference, see `../contemporary/variable-fonts.md`.

---

## Testing and Verification

### Side-by-side render

Open the page in a browser, force the fallback via DevTools' "Network
throttling: offline" or `Content-Security-Policy: font-src 'none'`, and
compare visually against the loaded-primary render. Lines of text should
sit at the same Y-coordinates. Any > 2px shift indicates override drift.

### CLS measurement

Three instrumentation paths:

1. **Web Vitals library.** `npm i web-vitals` + `import { onCLS } from
   'web-vitals'; onCLS(console.log);` — reports real-time CLS contributions.
2. **PerformanceObserver.** `new PerformanceObserver(list => …).observe({
   type: 'layout-shift', buffered: true })` — native API, no deps.
3. **Lighthouse CI.** Flags any `@font-face` without overrides; also
   surfaces the CLS score per run.

A good stack keeps per-swap CLS < 0.02; page-level Core Web Vitals "good"
is < 0.1.

### Forced-fallback testing in production CSS

```css
/* Test mode: pretend the primary never loaded */
@supports not (font-variation-settings: "opsz" 16) {
  /* Use this when you want to visually A/B the fallback; remove before ship. */
  :root { font-family: system-ui, sans-serif; }
}
```

Or use `document.fonts.ready` in JS to time the swap explicitly:

```js
document.fonts.ready.then(() => {
  // Primary loaded; measure or log.
});
```

### Visual regression

Percy, Chromatic, Argos CI, or Playwright's `toHaveScreenshot()` — snapshot
the page with fonts blocked and with fonts loaded. Expect byte-identical
block-level layout below the first fold. Any difference above the noise
floor indicates override drift.

### Katie Hempenius — "Preload fonts" (web.dev, 2020, revalidated 2024)

Recommends combining `<link rel="preload" as="font" crossorigin>` for the
primary with metric-tuned fallback aliases — preload cuts the FOUT window,
overrides cure any shift during it.

### Malte Ubl — CLS measurement (AMP team, 2020)

Canonical explanation of the `layout-shift` entry type, the impact score
formula (`impact fraction × distance fraction`), and how font-swap shifts
are scored. Worth reading before debugging CLS complaints.

---

## When Metric Compatibility Fails

### Different script

Latin primary, CJK fallback. No x-height compatibility possible; the
fallback's density and proportions are fundamentally different. Options:
ship a per-script fallback (`unicode-range`-scoped `@font-face` per script),
use `font-display: block` to hide text during the FOUT window (accept
blank-text flash instead of wrong-script flash), or use `font-display:
optional` to skip the primary on slow connections.

### Drastically different design

Serif → sans, condensed → wide, display → text. Overrides can close the CLS
gap (vertical box matches), but the visual difference is irreducible. Accept
the reflow, preload aggressively, or ship with `font-display: block` so
users never see the mismatched face.

### Licensed primary without registry metrics

Extract metrics yourself via FontDrop, Samsa, or TTX and feed Capsize
manually. `fontpie` or the `@capsizecss/core` API accept ad-hoc metric
objects.

---

## Anti-Patterns

- **Copying `size-adjust` values from the internet without verification.**
  Numbers vary by tool (bounding-box measurement vs OS/2 field read), by
  font version (Inter 3 vs Inter 4; Roboto pre- vs post-2020 re-cut), and
  by system-font variant (Arial on Windows 11 vs macOS bundled Arial).
  Re-measure when you change any input.
- **Overriding metrics on the primary instead of the fallback.** Reverses
  the relationship. The primary is the reference; `size-adjust: 107%` on
  Inter's own `@font-face` makes every heading 7% too large.
- **Mixing `size-adjust` with `font-size-adjust` without understanding
  them.** `size-adjust` is face-level, cures CLS, and lives in `@font-face`.
  `font-size-adjust` is per-element, does not cure CLS, and lives in the
  cascade. They are complementary — use both for belt-and-braces. See
  `./metrics-glossary.md` and `./units.md`.
- **Assuming `system-ui` is metric-compatible across OSes.** It is not. SF
  Pro vs Segoe UI Variable vs Roboto Flex vs Cantarell / Adwaita Sans
  differ substantially in x-height (0.49 to 0.54 em range) and advance
  widths. `system-ui` for brand body text is a trap; use it for OS-chrome
  UI only. See `../techniques/fallback-stacks.md#system-ui-reference`.
- **Ignoring `USE_TYPO_METRICS` mismatch between primary and fallback.**
  Modern Google Fonts all have the flag set; locally-installed legacy Arial
  on Windows 7 does not. Modern browsers mostly paper over this by reading
  `sTypo*` regardless of the flag, but legacy engines differ. For robust
  legacy support, also override the primary's ascent/descent via its own
  `@font-face`.
- **Computing overrides at the variable font's default instance when users
  see a different instance.** Compute against the opsz / wght / wdth your
  users actually get. `MVAR` stores per-instance deltas — Samsa reads them
  correctly.

---

## Emerging: Incremental Font Transfer (IFT)

IFT (W3C Font Working Group; Chrome behind a flag as of 2026-04, not
Baseline) ships only the glyphs a page actually uses in the order they
render. Once Baseline, the fallback-stack problem shrinks for many use
cases: if the primary's first-needed-glyphs arrive within the same RTT as
the fallback's first paint, the swap becomes invisible — no FOUT, no CLS,
no need for metric overrides.

As of 2026-04:

- **Chrome** — behind `--enable-blink-features=IncrementalFontTransfer`.
  Server support via `chrome.fonts.googleapis.com` for select Google Fonts.
- **Firefox** — tracking, no ship date.
- **Safari** — no public commitment.
- **Spec** — `github.com/w3c/IFT` (draft, 2025-2026).

IFT does not replace fallback stacks for first-paint (the first render
still needs *some* face) and does not help offline-first apps. Metric
compatibility remains essential for: slow connections, offline installs,
script mismatches, and design-time rendering (static-site generators,
PDF export, email).

---

## Cross-References

- **`./metrics-glossary.md`** — canonical definitions of every metric
  named here; `OS/2` / `hhea` / `head` table field reference; the metric
  wars (`hhea` vs `OS/2.sTypo*` vs `OS/2.usWin*`) and `USE_TYPO_METRICS`.
- **`./anatomy.md`** — named letterform parts (ascender, descender,
  x-line, baseline) for the measurement vocabulary.
- **`./units.md`** — CSS unit derivations (`em`, `ex`, `ch`, `cap`, `ic`,
  `lh`) and their mapping to font metrics.
- **`../contemporary/metric-overrides.md`** — the four `@font-face`
  descriptors, full algorithm derivation, `font-size-adjust` interaction,
  browser support, pitfalls.
- **`../techniques/fallback-stacks.md`** — production-ready pairings per
  genre with pre-computed overrides.
- **`../contemporary/variable-fonts.md`** — variable-font axis mechanics.
- **`../scripts/arabic.md`**, **`../scripts/cjk-han.md`**,
  **`../scripts/devanagari.md`**, **`../scripts/hebrew.md`** — per-script
  metric conventions.

---

## Sources

- **[Capsize (v5, 2026)](https://github.com/seek-oss/capsize)** — Michael
  Taranto, Seek. Reference implementation of x-height + cap-height formula.
- **[Seek Blog — "Capsize: Flipping how we define typography in CSS"](https://seek-oss.github.io/capsize/)** (Taranto, 2020, revalidated 2024).
- **[`@capsizecss/metrics` (2026)](https://www.npmjs.com/package/@capsizecss/metrics)** — pre-extracted metrics registry for ~1000 Google Fonts and common system fonts.
- **[Fontaine (unjs/fontaine, 2026)](https://github.com/unjs/fontaine)** — PostCSS / Vite / Nuxt plugin for auto-generated fallback aliases.
- **[Wakamai Fondue](https://wakamaifondue.com/)** — Roel Nieskens. Web-based font inspection tool.
- **[FontDrop](https://fontdrop.info/)** — Viktor Nübel. Browser-side font binary inspection.
- **[Samsa](https://samsa-family.github.io/samsa/)** — Laurence Penney. Variable-font-aware inspector.
- **[fontTools / TTX](https://github.com/fonttools/fonttools)** (2026). Python library for font table read/write.
- **[Modernfontstacks.com](https://modernfontstacks.com/)** — Dan Klammer (2024). Curated system-font stacks grouped by design feel.
- **[Simon Hearne — "How to avoid layout shifts caused by web fonts"](https://simonhearne.com/2021/layout-shifts-webfonts/)** (2021). Diagnostic methodology and CLS measurement.
- **[Katie Hempenius — "Preload optional fonts" (web.dev)](https://web.dev/articles/preload-optional-fonts)** (2020, revalidated 2024). Preload + fallback interaction.
- **[Bramus Van Damme — "Improved font fallbacks" (web.dev)](https://web.dev/blog/font-metric-overrides)** (2021, revalidated 2024). Canonical developer walkthrough.
- **[Malte Ubl — "A font-loading strategy to prevent FOUT and FOIT" (perfplanet)](https://calendar.perfplanet.com/2020/a-font-loading-strategy-to-prevent-fout-and-flash-of-invisible-text/)** (2020). CLS measurement under different font-display strategies.
- **[Barry Pollard — "Reducing Layout Shift" (Smashing)](https://www.smashingmagazine.com/2022/05/reducing-layout-shift-font-fallbacks/)** (2022). Production case studies with before/after CLS numbers.
- **[Chrome Developers — "Framework tools for font fallbacks"](https://developer.chrome.com/blog/framework-tools-font-fallback)** (2023).
- **[Kilian Valkhof — font-loading strategies](https://kilianvalkhof.com/2017/design/the-problem-with-font-display-swap/)** (2017, still cited 2026). `font-display` semantics primer.
- **[Microsoft OpenType `OS/2` table](https://learn.microsoft.com/en-us/typography/opentype/spec/os2)** (accessed 2026-04-17). Source of truth for `sTypoAscender`, `sxHeight`, `sCapHeight`, `fsSelection`.
- **[W3C IFT draft](https://github.com/w3c/IFT)** (2025-2026). Incremental Font Transfer spec.
- **Google Fonts metric normalization** — `github.com/googlefonts/gf-docs/tree/main/Spec` (2018-ongoing). Policy for `USE_TYPO_METRICS` on hosted fonts.
- **Typographica** — `typographica.org` reviews frequently annotate metrics and design intent; useful secondary source for font-release context.
