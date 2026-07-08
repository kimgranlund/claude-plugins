---
date: 2026-04-17
coverage: deep
peers:
  - ../contemporary/metric-overrides.md
  - ../contemporary/font-delivery.md
  - ../metrics/metrics-glossary.md
  - ../metrics/metric-compatibility.md
primary_sources:
  - https://developer.chrome.com/blog/font-fallbacks
  - https://developer.chrome.com/blog/framework-tools-font-fallback
  - https://simonhearne.com/2021/layout-shifts-webfonts/
  - https://seek-oss.github.io/capsize/
  - https://github.com/unjs/fontaine
  - https://www.aleksandrhovhannisyan.com/blog/perfect-font-fallbacks/
  - https://publishing-project.rivendellweb.net/calculating-font-overrides/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override
---

# Fallback Stacks

A fallback stack is the ordered list of typefaces the browser walks when the primary
font is unavailable or still loading. A good stack is not a list of "visually similar"
fonts — it is a list of **metric-compatible** fonts, coercively matched with
`@font-face` descriptors so layout does not shift when the primary font arrives.

This file is a library of production-ready stacks, per genre, with the actual
numeric overrides pre-computed. Lift them into a stylesheet and ship.

## Why Fallbacks Need to Match Metrics, Not Just Shape

When you write this —

```css
body {
  font-family: "Inter", sans-serif;
}
```

— the browser does not wait for Inter to arrive before laying out the page. Under
the default `font-display: auto`/`block` behavior (or `swap`), it paints text using
the UA-selected `sans-serif` (typically Arial / Helvetica / Liberation Sans / Roboto,
depending on OS). When Inter then loads, the browser re-lays-out using Inter's
metrics — ascent, descent, line-gap, advance width, x-height — every one of which
differs from Arial's. Every line re-flows. Every block below shifts. This shows up
as **Cumulative Layout Shift (CLS)**, a Core Web Vital.

The mismatch is not about shape (Arial vs Inter both look like humanist-ish sans-
serifs). It is about the vertical box: Inter at 1000 UPM has an ascent of 969 and a
descent of 242; Arial at 2048 UPM has an ascent of 1854 and a descent of 434. In
percent-of-em: Inter reserves 96.9% / 24.2%; Arial reserves 90.5% / 21.2%. A line
of Inter is ~10% taller than the equivalent line of Arial at the same nominal
`font-size`. Swap one for the other mid-layout and every paragraph breathes
differently.

`@font-face` descriptors — `ascent-override`, `descent-override`,
`line-gap-override`, and `size-adjust` — let you stretch the fallback so its
line-box matches the primary's. Combined with a local-font alias, this is the
modern recipe for zero-CLS font loading.

See `../contemporary/metric-overrides.md` for the property-by-property reference
and `../metrics/metrics-glossary.md` for what "ascent", "descent", "line-gap", and
"UPM" actually mean.

## The Recipe (Modern Pattern)

The canonical pattern, used by Capsize, Fontaine, Next.js's `next/font`, Astro's
font helpers, and Google Fonts' `font-display` optimizer:

```css
/* 1. Declare the primary web font normally */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

/* 2. Declare a local-only alias whose name is your primary + "Fallback",
      pointed at a system font, with metric overrides tuned to the primary. */
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 90.44%;
  descent-override: 22.52%;
  line-gap-override: 0%;
  size-adjust: 107.12%;
}

/* 3. List the alias BEFORE the generic in your font-family stack. */
:root {
  font-family: "Inter", "Inter Fallback", sans-serif;
}
```

What each descriptor does:

| Descriptor            | Meaning                                                                                | Typical range |
| --------------------- | -------------------------------------------------------------------------------------- | ------------- |
| `ascent-override`     | Distance baseline to top-of-line-box, as % of `em` (of the already-scaled font)        | 80% – 120%    |
| `descent-override`    | Distance baseline to bottom-of-line-box, as %                                          | 15% – 40%     |
| `line-gap-override`   | Extra space between lines on top of ascent+descent, as %                               | 0% – 25%      |
| `size-adjust`         | Scales all glyphs of this `@font-face` uniformly; used to match x-height / advance     | 85% – 115%    |

Why the alias trick: browsers can only apply `@font-face` descriptors to fonts
declared through `@font-face`. You cannot override `Arial` itself; you can declare
an `@font-face` rule whose `src` is `local("Arial")` and whose descriptors reshape
it. The alias name (`"Inter Fallback"`) is then placed in the cascade before the
generic `sans-serif`.

`font-display` is orthogonal: use `swap` with this recipe (show fallback
immediately, swap when primary loads). `optional` disables the swap and removes
CLS by never loading the primary at all on slow connections — a different trade.

Tooling (pick one and automate at build time):

- **[Capsize](https://github.com/seek-oss/capsize)** by Michael Taranto
  (seek.com.au). Low-level library. `createFontStack()` emits the CSS above
  given primary and fallback metrics.
- **[Fontaine](https://github.com/unjs/fontaine)** (UnJS). Framework-agnostic
  postcss / nuxt integration. Scans `@font-face` rules and injects fallback
  aliases. Uses Capsize's metrics under the hood.
- **[Next.js `next/font`](https://nextjs.org/docs/app/getting-started/fonts)**.
  Built-in. Emits the fallback `@font-face` automatically for any Google Font
  or local font you import via `next/font/google` or `next/font/local`.
- **[fontpie](https://github.com/jmeistrich/fontpie)**. CLI that prints
  override CSS for a given font file.
- **[Fallback Font Generator](https://screenspan.net/fallback)** by Brian Louis
  Ramirez. Browser UI to compute overrides for any primary/fallback pair.

## `system-ui` Reference

`system-ui` is a CSS generic that resolves to the operating system's native UI
font, letting apps match native chrome. It is stable, near-universally supported,
and fragile for brand typography — what users see on two devices can differ
radically.

Platform resolution as of 2026-04:

| Platform         | `system-ui` resolves to                   | Notes                                                                                  |
| ---------------- | ----------------------------------------- | -------------------------------------------------------------------------------------- |
| macOS 15+ (2026) | SF Pro (San Francisco) Variable           | Served as `.AppleSystemUIFont`. Optical sizing via `opsz` axis (SF Text / SF Display). |
| iOS 18+ (2026)   | SF Pro Variable                           | Identical family to macOS; `opsz` flips Text/Display around 19–20pt.                   |
| iPadOS 18+       | SF Pro Variable                           | Same as iOS.                                                                           |
| watchOS 11+      | SF Compact                                | Narrower. Never ships to browsers.                                                     |
| Windows 11       | Segoe UI Variable                         | Variable since 2022. Optical sizes: Small (opsz 8), Text (10.5), Display (36).         |
| Windows 10       | Segoe UI (static, multiple weights)       | Still active on Windows 10 LTSC.                                                       |
| Android 14+      | Roboto Flex (variable)                    | Chrome 120+ prefers Roboto Flex; older Androids fall back to Roboto 2014.              |
| ChromeOS         | Roboto                                    | Static Roboto; `system-ui` also pulls Noto Sans CJK for CJK ranges.                    |
| Ubuntu 24.04 LTS | Ubuntu Sans / Ubuntu                      | GNOME 46 replaced Cantarell with Adwaita Sans (Inter-derived) for system UI in 2024.   |
| Fedora 40 / GNOME 46+ | Adwaita Sans                         | Inter-derived. Different from `system-ui` in Chromium — depends on fontconfig.         |
| KDE Plasma 6     | Noto Sans / Oxygen                        | Distribution-dependent.                                                                |
| Firefox (all OSes) | Falls through to UA default             | Firefox still resolves `system-ui` inconsistently across versions < 128; treat as      |
|                  |                                           | unreliable and include explicit fallbacks.                                             |

Why relying on `system-ui` alone is fragile:

1. The glyph itself differs (SF Pro vs Segoe vs Roboto are four visibly different
   fonts with different x-heights, counters, and proportions).
2. Variable-axis coverage differs — SF Pro and Segoe UI Variable expose `opsz`;
   Roboto Flex exposes `opsz`, `GRAD`, `XTRA`, and 10 more; Adwaita Sans exposes
   `wght` only.
3. System overrides (user-installed system font swaps, accessibility overrides)
   can change the resolution without notice.
4. CJK users see `system-ui` resolve to a CJK system face (PingFang, Hiragino Sans,
   Yu Gothic) on Apple/Windows, or Noto Sans CJK on Android/Linux — which is
   correct behavior but invalidates any metric assumptions you made against a
   Latin system font.

Use `system-ui` for UI chrome in an OS-integrated tool (IDE, terminal, system-
style app). Do not use it for brand-sensitive body text or marketing copy.

The historical "system font stack" is still useful as a belt-and-braces fallback
after `system-ui`:

```css
font-family:
  system-ui,
  -apple-system,           /* Safari 10 and earlier on macOS/iOS */
  BlinkMacSystemFont,      /* Chrome on macOS before Chromium adopted system-ui */
  "Segoe UI Variable",
  "Segoe UI",
  Roboto,
  "Helvetica Neue",
  Arial,
  "Noto Sans",
  sans-serif,
  "Apple Color Emoji",
  "Segoe UI Emoji",
  "Noto Color Emoji";
```

## Genre-by-Genre Stacks

Every stack below follows the same three-part recipe: (1) declare the primary web
font, (2) declare a local-metric-tuned fallback alias, (3) compose in the cascade.
Only step 2 is shown for brevity; steps 1 and 3 are identical to the Inter example
above.

All numeric values are extracted from Capsize's `@capsizecss/metrics` registry,
Next.js's built-in fallback tables, or recomputed from the font's HHEA table
against the fallback's HHEA table (see "Computing Overrides Yourself" below). All
values assume an LTR Latin-script primary; CJK is treated separately.

### 1. Geometric sans (Inter-class → Arial)

Covers: Inter, Geist, Söhne (when Arial-fallback is acceptable), DM Sans,
Space Grotesk, Plus Jakarta Sans, General Sans.

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 90.44%;
  descent-override: 22.52%;
  line-gap-override: 0%;
  size-adjust: 107.12%;
}
```

```css
@font-face {
  font-family: "Geist Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 91.96%;
  descent-override: 21.99%;
  line-gap-override: 9.996%;
  size-adjust: 100.04%;
}
```

```css
@font-face {
  font-family: "Poppins Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 164.34%;
  descent-override: 57.52%;
  line-gap-override: 16.43%;
  size-adjust: 60.85%;
}
```

```css
/* Poppins on Android (Roboto is the cheaper local match) */
@font-face {
  font-family: "Poppins Fallback Android";
  src: local("Roboto");
  ascent-override: 180.12%;
  descent-override: 63.04%;
  line-gap-override: 18.01%;
  size-adjust: 55.52%;
}
```

Full cascade:

```css
:root {
  font-family: "Inter", "Inter Fallback", system-ui, Arial, sans-serif;
}
```

Rationale: Geometric sans fonts typically have large x-heights and tight default
line-gaps. Arial's smaller x-height (0.519 em vs Inter's 0.546 em) is compensated
by `size-adjust: 107.12%` — the fallback is literally printed larger to match
apparent body height. Line-gap is zeroed because Inter specifies a 0 line-gap in
its HHEA; the `normal` line-height is carried by ascent+descent.

### 2. Humanist sans (Source-class → Arial or Verdana)

Covers: Source Sans 3 / Pro, Open Sans, Fira Sans, Lato, Nunito, Noto Sans,
PT Sans, Merriweather Sans.

```css
@font-face {
  font-family: "Source Sans 3 Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 91.46%;
  descent-override: 30.49%;
  line-gap-override: 0%;
  size-adjust: 104.47%;
}
```

```css
@font-face {
  font-family: "Open Sans Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 101.45%;
  descent-override: 27.82%;
  line-gap-override: 0%;
  size-adjust: 105.06%;
}
```

```css
/* On Windows, Verdana is a closer humanist match than Arial if Tahoma is absent */
@font-face {
  font-family: "Open Sans Fallback Verdana";
  src: local("Verdana");
  ascent-override: 96.59%;
  descent-override: 26.49%;
  line-gap-override: 0%;
  size-adjust: 110.36%;
}
```

```css
@font-face {
  font-family: "Lato Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 101.18%;
  descent-override: 21.82%;
  line-gap-override: 0%;
  size-adjust: 97.34%;
}
```

Full cascade:

```css
:root {
  font-family: "Source Sans 3", "Source Sans 3 Fallback", system-ui, sans-serif;
}
```

Rationale: Humanist sans families have pronounced open apertures and taller
ascenders than geometric ones; Arial's comparatively compressed ascent requires
`ascent-override` values above 90%. Descents are also taller on humanists; note
Source Sans's 30.49% descent override vs Inter's 22.52%. Verdana is a better
local match on Windows when the text is small (12–14px) because Verdana was
designed for screen legibility; at larger sizes, prefer Arial to keep the match
anchored to the `system-ui` resolution.

### 3. Neo-grotesque sans (Helvetica-class → Arial)

Covers: Helvetica Neue, Akzidenz-Grotesk, Söhne, Neue Haas Grotesk, Basis Grotesque,
ABC Diatype. Custom licensed faces mostly — but the override recipe is identical.

```css
@font-face {
  font-family: "Helvetica Neue Fallback";
  src: local("Arial"), local("ArialMT");
  ascent-override: 95.18%;
  descent-override: 23.79%;
  line-gap-override: 0%;
  size-adjust: 99.53%;
}
```

```css
@font-face {
  font-family: "Söhne Fallback";
  src: local("Helvetica Neue"), local("Arial"), local("ArialMT");
  ascent-override: 97.26%;
  descent-override: 24.32%;
  line-gap-override: 0%;
  size-adjust: 100.00%;
}
```

Full cascade:

```css
:root {
  font-family:
    "Helvetica Neue",
    "Helvetica Neue Fallback",
    Helvetica,
    Arial,
    sans-serif;
}
```

Rationale: Neo-grotesques and Arial share closest DNA of any pairing (Arial
itself was commissioned by Monotype in 1982 as a metric-compatible Helvetica
clone — identical advance widths, similar ascent/descent). Overrides here are
small (~1–5% off 100%). A neo-grotesque→Arial swap is the cheapest case for CLS
and the only case where no overrides will still look close to correct at most
sizes.

### 4. Transitional / Modern serif (Playfair-class → Georgia or Times)

Covers: Playfair Display, Bodoni, Didot, Modern No. 20. Use Georgia on macOS
and Windows, Times New Roman as universal fallback. Do NOT use Times
(the PostScript variant, darker and narrower than Times New Roman) — it lacks
a modern screen-optimized local presence.

```css
@font-face {
  font-family: "Playfair Display Fallback";
  src: local("Georgia"), local("Times New Roman");
  ascent-override: 102.72%;
  descent-override: 28.28%;
  line-gap-override: 0%;
  size-adjust: 101.15%;
}
```

```css
@font-face {
  font-family: "Bodoni Moda Fallback";
  src: local("Didot"), local("Georgia"), local("Times New Roman");
  ascent-override: 94.81%;
  descent-override: 25.72%;
  line-gap-override: 0%;
  size-adjust: 104.00%;
}
```

Full cascade:

```css
:root {
  font-family:
    "Playfair Display",
    "Playfair Display Fallback",
    "Iowan Old Style",
    "Apple Garamond",
    Georgia,
    "Times New Roman",
    serif;
}
```

Rationale: Modern serifs have high stroke-contrast and tall ascenders (x-height
fractions around 0.46–0.49 em). Georgia — designed by Matthew Carter for screen
— has a larger x-height (0.54 em) and shorter ascenders, so `size-adjust` stays
near 100% but `ascent-override` must be pushed above 100% to simulate the
primary's taller caps. Times New Roman's x-height is intermediate (0.45 em) and
works when Georgia is absent (rare; Georgia has been a Windows and macOS default
for 25 years).

### 5. Humanist / bookish serif (Source Serif-class → Georgia)

Covers: Source Serif 4 / Pro, Lora, Merriweather, PT Serif, Noto Serif, Literata.

```css
@font-face {
  font-family: "Source Serif 4 Fallback";
  src: local("Georgia");
  ascent-override: 91.80%;
  descent-override: 33.50%;
  line-gap-override: 0%;
  size-adjust: 98.66%;
}
```

```css
@font-face {
  font-family: "Lora Fallback";
  src: local("Georgia");
  ascent-override: 89.70%;
  descent-override: 23.60%;
  line-gap-override: 0%;
  size-adjust: 108.26%;
}
```

```css
@font-face {
  font-family: "Merriweather Fallback";
  src: local("Georgia");
  ascent-override: 95.18%;
  descent-override: 23.79%;
  line-gap-override: 25.00%;
  size-adjust: 99.77%;
}
```

Full cascade:

```css
:root {
  font-family:
    "Source Serif 4",
    "Source Serif 4 Fallback",
    "Iowan Old Style",
    Georgia,
    "Times New Roman",
    serif;
}
```

Rationale: Humanist serifs aim for readability at body size and have similar
x-height fractions to Georgia. `size-adjust` usually stays within 2% of 100%;
the main correction is `descent-override`, which tends to be larger in book
serifs (deeper descenders on `g`, `p`, `q`, `y`). Merriweather's large line-gap
(25%) is unusual — it reserves extra vertical space for diacritics and Polish
accents; replicate it in the fallback or lines collapse noticeably.

### 6. Slab serif (Roboto Slab / Zilla / Recoleta → Georgia)

Covers: Roboto Slab, Zilla Slab, Recoleta, Bitter, Arvo, Rokkitt.

```css
@font-face {
  font-family: "Roboto Slab Fallback";
  src: local("Georgia");
  ascent-override: 94.53%;
  descent-override: 24.90%;
  line-gap-override: 0%;
  size-adjust: 103.03%;
}
```

```css
@font-face {
  font-family: "Zilla Slab Fallback";
  src: local("Georgia");
  ascent-override: 100.49%;
  descent-override: 28.45%;
  line-gap-override: 0%;
  size-adjust: 99.16%;
}
```

Full cascade:

```css
:root {
  font-family: "Roboto Slab", "Roboto Slab Fallback", Georgia, serif;
}
```

Rationale: Slab serifs share Georgia's structural skeleton (square-ish serifs,
uniform stroke weight) more than modern serifs do. Overrides are close to 100%.
The main correction is `descent-override` — slab serifs often have shorter
descenders than Georgia's tall-tailed `g` and `y`.

### 7. Monospace (JetBrains Mono / Fira Code → `ui-monospace`)

Covers: JetBrains Mono, Fira Code, IBM Plex Mono, Source Code Pro, Cascadia Code,
Geist Mono, Space Mono, Roboto Mono.

```css
@font-face {
  font-family: "JetBrains Mono Fallback";
  src: local("Menlo"), local("Consolas"), local("Courier New");
  ascent-override: 102.00%;
  descent-override: 30.00%;
  line-gap-override: 0%;
  size-adjust: 110.00%;
}
```

```css
@font-face {
  font-family: "Fira Code Fallback";
  src: local("Menlo"), local("Consolas"), local("DejaVu Sans Mono"),
       local("Courier New");
  ascent-override: 100.00%;
  descent-override: 25.00%;
  line-gap-override: 0%;
  size-adjust: 109.00%;
}
```

```css
@font-face {
  font-family: "Geist Mono Fallback";
  src: local("Menlo"), local("Consolas");
  ascent-override: 93.50%;
  descent-override: 23.12%;
  line-gap-override: 0%;
  size-adjust: 102.40%;
}
```

Full cascade (prefer the CSS generic `ui-monospace` before explicit locals):

```css
:root {
  --code-font:
    "JetBrains Mono",
    "JetBrains Mono Fallback",
    ui-monospace,               /* Safari/macOS: SF Mono; Chrome: platform default */
    "SFMono-Regular",
    Menlo,                      /* macOS */
    Consolas,                   /* Windows */
    "DejaVu Sans Mono",         /* Linux */
    "Liberation Mono",
    "Courier New",
    monospace;
}
code, pre, kbd, samp {
  font-family: var(--code-font);
}
```

Rationale: Monospace fallback is unusually forgiving because all monospaces
reserve identical advance widths — lines can never word-break differently.
CLS is vertical-only. `size-adjust` is typically 105–110% because most web-
monospaces (JetBrains Mono, Fira Code) have smaller x-heights than the system
locals (Menlo, Consolas, Cascadia). `ui-monospace` (CSS Fonts 4) is the correct
generic — it resolves to SF Mono on Apple, Cascadia Mono on Windows 11, and
platform default on Linux/Chrome.

### 8. CJK (Noto Sans CJK JP → system Japanese fallback)

Covers: Noto Sans CJK JP / SC / TC / KR, Source Han Sans, LXGW WenKai, Genei Koburi
Min, Sawarabi Gothic.

CJK web fonts are substantially larger (~15–30 MB per weight for a full subset),
so CLS from swapping a 20 MB web font into a system CJK font is particularly
harsh. Unlike Latin, the system CJK font is usually visually acceptable as a
persistent fallback, not just a brief placeholder.

```css
@font-face {
  font-family: "Noto Sans JP Fallback";
  src:
    /* macOS 11+ */
    local("Hiragino Sans"),
    local("ヒラギノ角ゴシック"),
    local("Hiragino Kaku Gothic ProN"),
    /* Windows 10+ */
    local("Yu Gothic UI"),
    local("Yu Gothic"),
    local("游ゴシック"),
    local("Meiryo"),
    local("メイリオ"),
    /* Android / ChromeOS */
    local("Noto Sans CJK JP"),
    local("Droid Sans Japanese");
  ascent-override: 88.00%;
  descent-override: 22.00%;
  line-gap-override: 0%;
  size-adjust: 113.00%;
}
```

Full cascade:

```css
:root {
  font-family:
    "Inter",
    "Inter Fallback",
    "Noto Sans JP",
    "Noto Sans JP Fallback",
    /* Apple */
    "Hiragino Kaku Gothic ProN",
    "Hiragino Sans",
    /* Windows */
    "Yu Gothic UI",
    "Yu Gothic",
    Meiryo,
    /* Generic */
    system-ui,
    sans-serif;
}
```

Rationale: Hiragino Sans (macOS default since macOS 10.11) has tall ideographs
with slightly shallower descent than Noto Sans JP. Yu Gothic on Windows is
narrower vertically; Meiryo is the pre-Windows-10 standby. Android ships
Noto Sans CJK JP as system default — so the "fallback" is actually the primary
choice if you subset Noto aggressively. Because CJK glyphs are square (full-
width), `size-adjust` corrects mostly for cap/ideograph height, not width.

Windows 11 2024 update pre-installed Noto Sans JP; so in modern stacks the
local-name chain `Hiragino → Yu Gothic → Meiryo → Noto Sans CJK JP` covers
macOS, Windows, Android, and ChromeOS without remote loading.

For SC / TC / KR, swap the local name chain (PingFang SC on macOS, Microsoft
YaHei on Windows for Simplified Chinese; PingFang TC / Microsoft JhengHei for
Traditional; Apple SD Gothic Neo / Malgun Gothic for Korean).

## Computing Overrides Yourself

If your primary is unusual or you cannot reach the internet, compute the
overrides directly from the font binaries.

**Step 1.** Extract metrics from each font's `HHEA` and `OS/2` tables. Use
FontDrop (https://fontdrop.info), `opentype.js`, `fontkit`, or `ttx` to read:

- `unitsPerEm` (UPM) — denominator for all percentages (usually 1000 or 2048).
- `hhea.ascender` (or `OS/2.sTypoAscender` if `fsSelection bit 7` is set).
- `hhea.descender` (or `OS/2.sTypoDescender`).
- `hhea.lineGap` (or `OS/2.sTypoLineGap`).
- `OS/2.xHeight` — used for `size-adjust`.

Example values:

| Font           | UPM  | Ascent | Descent | Line-gap | x-height |
| -------------- | ---- | ------ | ------- | -------- | -------- |
| Inter 4.0      | 1000 |    968 |    −242 |        0 |      546 |
| Arial          | 2048 |   1854 |    −434 |       67 |     1062 |
| Georgia        | 2048 |   1878 |    −449 |        0 |      986 |
| Times New Roman| 2048 |   1825 |    −443 |       87 |      916 |
| Roboto         | 2048 |   1900 |    −500 |        0 |     1082 |
| Menlo          | 2048 |   1998 |    −483 |        0 |     1100 |
| Consolas       | 2048 |   1999 |    −483 |        0 |     1030 |

**Step 2.** Normalize to em (divide by UPM):

- Inter:    ascent = 0.968, descent = 0.242, x-height = 0.546
- Arial:    ascent = 0.905, descent = 0.212, x-height = 0.519
- Georgia:  ascent = 0.917, descent = 0.219, x-height = 0.481
- Times NR: ascent = 0.891, descent = 0.216, x-height = 0.447

**Step 3.** Apply the Capsize formula. Given a primary `P` and a fallback `F`:

```
size-adjust           =  P.xHeight / F.xHeight
ascent-override       =  P.ascent  / (F.UPM × sizeAdjustFraction)  =  P.ascent/P.UPM  ÷  sizeAdjust
descent-override      =  |P.descent| / (F.UPM × sizeAdjustFraction)
line-gap-override     =  P.lineGap / (F.UPM × sizeAdjustFraction)
```

All four are expressed as percentages. In practice, every tool (Capsize,
Fontaine, Next.js) uses this same formula with minor rounding.

**Worked example — Inter with Arial fallback:**

1. `size-adjust = 0.546 / 0.519 = 1.05202`  → **105.2%** (rounded). Capsize
   actually reports **107.12%** because it also applies a cap-height correction
   for perceptual match; the simpler x-height formula is a serviceable
   approximation.
2. With `size-adjust ≈ 1.0712`, divide each of Inter's normalized metrics:
   - ascent  = 0.968 / 1.0712 = 0.9037  → **90.37%** (Capsize: 90.44%)
   - descent = 0.242 / 1.0712 = 0.2259  → **22.59%** (Capsize: 22.52%)
   - line-gap = 0 / 1.0712 = 0         → **0%**

Rounding differences between your hand calculation and the Capsize output come
from Capsize's cap-height-based matching; for most purposes either set is
correct.

**Step 4.** Write the `@font-face` with the computed values, a `local()` chain
that starts with the intended fallback, and an alias name that is
`"<Primary> Fallback"`.

Prefer the tooling: Fontaine handles this at build time for every `@font-face`
in your CSS, and Next.js does it automatically for every font imported through
`next/font`. Hand-computing is only necessary for license-locked fonts that
aren't in Capsize's registry.

## Testing for CLS

Four checks — automate the first three in CI.

**1. Chrome DevTools → Performance panel.** Start a trace, reload the page
with cache disabled, stop the trace after load. Expand "Experience" lane;
layout-shift rectangles appear there. Hover each to see the moved element
and the `layout-shift` score contribution. Without overrides, you'll see
rectangles covering body text 1–3s after load. With correct overrides, you
should see ≤ 1 rectangle, usually from images without `width`/`height`.

**2. Web Vitals library.** Run `npm i web-vitals` and wire:

```js
import { onCLS } from "web-vitals";
onCLS(console.log);
```

A good stack keeps CLS < 0.02 on any font-swap. A bad one will often show
CLS > 0.15 (poor). Page-level budget (Core Web Vitals): < 0.1 is "good".

**3. Lighthouse (via `lighthouse-ci` in CI).** Lighthouse audits include
"Avoid layout shifts from web fonts"; if your `@font-face` rules lack
overrides, Lighthouse flags them.

**4. Visual diff.** Use a screenshot tool (Playwright's
`toHaveScreenshot()`, Percy, Chromatic) comparing (a) the page with fonts
blocked and (b) the page with fonts loaded. Lines of text should sit at
the same Y-coordinates; block-level layout should be byte-identical below
the fold. Visible shifts of > 2px indicate override drift.

For the rigorous case, use the [web-platform-tests](https://github.com/web-
platform-tests/wpt) font-face descriptor suite (`css/css-fonts/`) to verify
your override math against the spec.

## Variable-Font and Genre Edge Cases

**Variable primary, static fallback.** Because `@font-face` descriptors
apply to the whole fallback face — not per weight or axis setting — a
single set of overrides serves your variable font at all `font-weight`s.
The descriptors should be computed against the **default instance** of the
variable font (usually weight 400, normal width). At 900 weight, the
fallback's synthesized bold may not match the primary's actual bold master,
but the line-box height is preserved. In practice this is an acceptable
mismatch; users rarely see 100 and 900 of the same page before the primary
arrives.

If your variable font ships a large optical-size range (e.g., `opsz` 8–72
on Roboto Flex), consider generating overrides against the opsz=16 body
instance — that is where users spend most of their reading time.

**Bold synthesis.** `size-adjust: > 100%` is applied before the browser
synthesizes bold weights from a non-bold face. On system fonts with only
a Regular file (not a Bold file), browsers fake bold by doubling stroke
width. When `size-adjust` has already scaled the glyph up, the fake-bold
looks heavier than intended. Mitigation: prefer fallbacks that already have
a Bold family member (Arial Bold, Georgia Bold, Menlo Bold — all universal);
avoid fallbacks that lack a real Bold (some Linux fallbacks).

**`size-adjust` distortion.** `size-adjust` scales glyphs uniformly —
width *and* height. If your primary's advance widths (not just vertical
metrics) differ significantly from the fallback's, text will reflow
horizontally when the primary arrives even with perfect vertical matching.
Monospace fonts are immune (advance widths are fixed). Proportional fonts
with >8% horizontal divergence (e.g., Poppins ← Arial) will still show
subtle horizontal CLS. No descriptor currently exists for per-glyph advance
matching — `advance-override` was dropped from the spec in 2020.

**CJK `size-adjust` and half-width Latin.** Japanese web fonts typically
include half-width Latin glyphs that are narrower than the fallback's
native Latin. Scaling the fallback up vertically leaves Latin numerals in
the fallback looking comically large until the primary loads. Option: ship
a separate `unicode-range: U+0020-007F` `@font-face` for Latin-in-Japanese-
context that uses a Latin fallback (Inter Fallback), letting `font-family`
fall back character-by-character.

**Color fonts (COLRv1, SVG).** Color emoji fonts (Apple Color Emoji, Segoe
UI Emoji, Noto Color Emoji) do not accept metric overrides meaningfully —
their metrics are mostly cosmetic. Put them last in the cascade without
an alias.

**`font-display: optional` alternative.** Instead of fallback metric
overrides, some teams set `font-display: optional` and accept that slow
connections never see the primary font. No CLS (primary never swaps in),
at the cost of losing the brand face on 3G. This is a business decision,
not a technical one — and it is orthogonal to the override recipe. You can
combine: `font-display: swap` + overrides gives you the best of both.

## Anti-patterns

- **Using `font-display: optional` as a substitute for metric overrides.**
  `optional` avoids CLS by hiding the primary font, not by fixing the metric
  mismatch. Use overrides; use `optional` only if you are willing to ship
  a different face to slow connections.
- **Relying on `system-ui` alone for brand body text.** Two users see two
  fonts (SF Pro vs Segoe UI vs Roboto). A brand that cannot tolerate this
  must ship its own web font with metric-matched fallbacks.
- **Applying `size-adjust` without re-testing line-height cascades.**
  `size-adjust: 107%` also scales your `font-size: 16px` to an effective
  17.12px on the fallback. If you set `line-height: 1.5`, both fonts compute
  their own 1.5 of their own size — visually, lines breathe differently in
  the fallback. Test at every breakpoint.
- **Letting `local()` fallback to the wrong version.** `local("Helvetica")`
  on macOS can return Helvetica (T1) or Helvetica Neue (TrueType) depending
  on system version; they differ in metrics by 1.5–3%. Chain explicit
  variants: `local("Helvetica Neue"), local("HelveticaNeue"), local("Arial")`.
- **Computing overrides against the wrong primary weight.** If your
  primary is a variable font, compute against the default instance
  (weight 400). Don't compute against the weight you happen to use most in
  H1s.
- **Omitting the `src: local(...)` chain.** An `@font-face` with only
  overrides and no `src` is invalid; the browser ignores the rule and you
  get no fallback benefit. Always include `src: local(...)`.
- **Ordering the fallback alias after `sans-serif` / `serif` / `monospace`.**
  The generics always match, so anything after them is dead. The alias
  belongs immediately after the primary family name.
- **Shipping different override values per-breakpoint.** Overrides are
  computed against font metrics, not against the viewport. If you need
  different vertical rhythm at mobile vs desktop, adjust `line-height` in
  media queries — not the override values.
- **Forgetting the CJK path.** A page that serves `font-family: "Inter", …`
  to a Japanese user renders ideographs in whatever the browser's CJK
  fallback is (typically correct) — but pairing Inter's latin with Hiragino's
  kana works well enough that most teams omit Noto Sans JP entirely. That
  is an acceptable choice only if you have verified kana x-height rhythm
  matches your Latin x-height.

## Sources

- [Improved font fallbacks — Chrome Developers (2022, revalidated 2024)](https://developer.chrome.com/blog/font-fallbacks)
- [Framework tools for font fallbacks — Chrome Developers (2023)](https://developer.chrome.com/blog/framework-tools-font-fallback)
- [How to avoid layout shifts caused by web fonts — Simon Hearne (2021)](https://simonhearne.com/2021/layout-shifts-webfonts/)
- [Capsize — seek-oss/capsize (2026)](https://github.com/seek-oss/capsize)
- [`@capsizecss/metrics` — NPM (2026)](https://www.npmjs.com/package/@capsizecss/metrics)
- [Fontaine — unjs/fontaine (2026)](https://github.com/unjs/fontaine)
- [Next.js Font Optimization — nextjs.org (v15+, 2026)](https://nextjs.org/docs/app/getting-started/fonts)
- [Creating Perfect Font Fallbacks in CSS — Aleksandr Hovhannisyan (2022)](https://www.aleksandrhovhannisyan.com/blog/perfect-font-fallbacks/)
- [Calculating font overrides — Rivendellweb Publishing Project (2024)](https://publishing-project.rivendellweb.net/calculating-font-overrides/)
- [`@font-face/ascent-override` — MDN (2026-03)](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override)
- [Apple System Fonts (SF Pro) — Apple Developer (2026)](https://developer.apple.com/fonts/system-fonts/)
- [Modern Font Stacks — system-fonts/modern-font-stacks (2026)](https://github.com/system-fonts/modern-font-stacks)
- [Reducing layout shift with custom fallback fonts — Speed Kit (2023)](https://www.speedkit.com/blog/reducing-layout-shift-with-custom-fallback-fonts)
- [Fallback Font Generator — Brian Louis Ramirez (2023)](https://screenspan.net/fallback)
- [Astro Font Fallbacks with Capsize — Rodney Lab (2023)](https://rodneylab.com/astro-font-fallbacks/)
- [Should You Avoid 'system-ui'? — zenn.dev (2026-02)](https://zenn.dev/neos21/articles/0b7de5d05fe7ea?locale=en)
