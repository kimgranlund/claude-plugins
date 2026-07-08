---
date: 2026-04-17
coverage: deep
peers:
  - ./css-text-properties.md
  - ./variable-fonts.md
  - ./metric-overrides.md
  - ./color-fonts.md
  - ../techniques/fallback-stacks.md
primary_sources:
  - https://www.w3.org/TR/css-fonts-4/
  - https://drafts.csswg.org/css-fonts-5/
  - https://www.w3.org/TR/IFT/
  - https://www.w3.org/Fonts/WG/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#rel%3D%22preload%22
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/fetchpriority
  - https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_web_fonts
  - https://developer.chrome.com/blog/font-fallbacks/
  - https://web.dev/articles/preload-optional-fonts
  - https://web.dev/articles/optimize-webfont-loading
  - https://web.dev/articles/font-display
  - https://web.dev/articles/reduce-webfont-size
  - https://www.zachleat.com/web/comprehensive-webfonts/
  - https://csswizardry.com/2020/05/the-fastest-google-fonts/
  - https://www.industrialempathy.com/posts/high-performance-web-font-loading/
  - https://fontsource.org/docs/introduction
  - https://fonts.bunny.net/
  - https://github.com/bramstein/fontfaceobserver
  - https://github.com/zachleat/glyphhanger
  - https://github.com/Munter/subfont
  - https://github.com/Pfeffer-Pack/pfeffer-pack-fontaine
  - https://datatracker.ietf.org/doc/html/rfc8081
  - https://www.w3.org/TR/WOFF2/
  - https://caniuse.com/woff2
  - https://caniuse.com/font-loading
  - https://caniuse.com/mdn-html_elements_link_fetchpriority
  - https://caniuse.com/mdn-css_at-rules_font-face_font-display
---

# Font Delivery

<orientation>
This file covers the *network + format + loading* surface: what container to ship, how to subset it, how to wire `@font-face`, `font-display`, `<link rel="preload">`, HTTP caching, and loading patterns (FOIT/FOUT/FOFT).

What this file does **not** cover:
- Metric overrides (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) — see `./metric-overrides.md`.
- Variable-font axis semantics (`wght`, `wdth`, `opsz`, etc.) — see `./variable-fonts.md`.
- Color-font containers (COLRv0, COLRv1, SVG-in-OpenType, sbix, CBDT/CBLC) internals — see `./color-fonts.md`.
- Fallback-stack recipes and how to reason about them — see `../techniques/fallback-stacks.md`.

All dated claims are scoped to the state of stable releases as of **April 2026**. "Baseline" uses the Web Platform DX Community Group definition.
</orientation>

---

## TL;DR — The Default Delivery Recipe (2026-04)

1. **Ship WOFF2 only.** Drop WOFF and TrueType/OpenType fallbacks; the last browser requiring them (Safari < 10, IE11) is outside every modern support matrix.
2. **Self-host** unless you have a specific reason not to. Privacy-law rulings in the EU (Germany 2022, Italy 2023) and France's CNIL guidance (2024) have made Google Fonts CDN a legal risk for EU-facing sites without proper consent flow.
3. **Subset** by `unicode-range` at minimum (Latin / Latin-ext / Vietnamese / Cyrillic / Greek). Static subsets cover ~98% of real projects; per-page subsetting is a Phase-2 optimization.
4. **`font-display: swap`** for body text. **`font-display: optional`** for anything below-the-fold. **`font-display: block`** only for icon fonts where a missing glyph is worse than invisible text (rarely the right call now that we have SVG icons).
5. **Preload one to two fonts max** — the roman and italic of the body, or the roman body and the heading — with `crossorigin` and `fetchpriority="high"` (Chrome 101+, Safari 17.2+, Firefox 119+; stable cross-browser Baseline by Q3 2024).
6. **Ship a variable font** when you use 3+ cuts of the family. A two-axis (`wght` + `ital` or `wght` + `opsz`) variable is usually 30–50% smaller than four static cuts after WOFF2 compression.
7. **Pair every `@font-face` with a metric-aligned fallback** using `size-adjust` + `ascent-override` + `descent-override`. See `./metric-overrides.md`.
8. **Long `Cache-Control`** (`max-age=31536000, immutable`) on fingerprinted URLs. Fonts change rarely; versioned filenames make this safe.

Everything below unpacks these defaults with dated caveats.

---

## Formats — What to Ship in 2026

### Container lineage

Every modern web font is a **SFNT** container (Spline Font with a standard table layout, inherited from Apple's TrueType). Inside that container, the outline table is one of:

- **`glyf` + `loca` (TrueType outlines)** — quadratic Bézier curves. Introduced in TrueType (1991). Still the dominant representation for variable fonts because `gvar` deltas attach to the TT outline format.
- **`CFF ` (PostScript Type 2 outlines, "CFF1")** — cubic Bézier curves. Part of OpenType 1.0 (1996). Typically smaller in file size for non-variable fonts because cubics express curves with fewer control points. No variable-font support.
- **`CFF2` (Compact Font Format 2)** — cubic Bézier with interpolable deltas. Introduced in OpenType 1.8 (September 2016) specifically to support variable fonts with PostScript outlines. Not supported by legacy non-variable pipelines.

SFNT → outline format is an orthogonal choice from the **wire format** below.

### Wire formats

| Format | MIME | Compression | When to use in 2026-04 | Notes |
|---|---|---|---|---|
| **WOFF2** | `font/woff2` | Brotli | **Default.** Always. | W3C Recommendation (March 2018). Universal support since Chrome 36, Firefox 39, Safari 10, Edge 14 (caniuse 2026-04: ~98.5% global). |
| **WOFF** | `font/woff` | zlib/gzip | Legacy. **Don't ship.** | Only needed for Safari 5–9 and IE9. Both are below 0.1% usage as of 2026-04. |
| **TTF/OTF** (raw SFNT) | `font/ttf`, `font/otf` | None | Local install / design tools. **Don't ship over HTTP.** | Typically ~2× the wire size of WOFF2. No reason to serve over the network. |
| **EOT** | `application/vnd.ms-fontobject` | MTX | Dead. | IE4–IE8 format. Never relevant in 2026. |
| **SVG fonts** | `image/svg+xml` | — | Dead. | Removed from SVG 2. Last shipped in iOS Safari pre-10. |

**Why WOFF beats TTF on the wire**: WOFF is a zlib-compressed SFNT with extended metadata and a brief header. WOFF2 goes further: it uses Brotli, removes redundant TT hinting tables, and applies a preprocessing transform (MicroTYPE-style glyph decomposition) that exposes more redundancy for Brotli to exploit. The result is typically 30–40% smaller than WOFF on Latin fonts, and 50%+ smaller than raw TTF.

**Why WOFF died**: by 2018 every evergreen browser supported WOFF2, and WOFF's compression advantage over raw TTF was dwarfed by WOFF2's. There is no modern browser that supports WOFF but not WOFF2. Shipping a WOFF fallback is pure ceremony.

### Color-font containers

Color glyph data rides in side-tables inside the same SFNT container:

- **COLRv0** — base + layer system, flat fills only. Chrome, Firefox, Safari all support (since ~2016–2019).
- **COLRv1** — gradients, transforms, composite modes, variable-font integration. Chrome 98+ (2022-02), Firefox 107+ (2022-11), Safari 16.4+ (2023-03).
- **SVG-in-OpenType** — full SVG per glyph. Firefox 26+, Safari 11+, Chrome never shipped (WONTFIX).
- **sbix (bitmap)** — Apple's emoji format. Safari 8+, Firefox 47+, Chrome 69+.
- **CBDT/CBLC (bitmap)** — Google's Android emoji format. Chrome 66+, Firefox 26+, Safari never shipped.

See `./color-fonts.md` for the full matrix and authoring tradeoffs.

---

## Subsetting

A subset is a new font with a reduced glyph set. Subsetting is the single highest-leverage optimization for Latin web fonts — a typical Google-Fonts–style Latin-only subset is 12–25 KB in WOFF2; the same font with full Unicode coverage is often 200+ KB.

### `unicode-range` splits (Google Fonts pattern)

The `unicode-range` descriptor on `@font-face` tells the browser: "use this file *only* to render code points in the given range." When a page contains no code points in the range, the browser **does not fetch the file**. This is the mechanism behind Google Fonts' multi-subset delivery.

```css
/* Latin (basic) */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-roman-latin.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range:
    U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6,
    U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F,
    U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215,
    U+FEFF, U+FFFD;
}

/* Latin Extended */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-roman-latin-ext.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range:
    U+0100-02AF, U+0304, U+0308, U+0329, U+1E00-1E9F,
    U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF,
    U+2113, U+2C60-2C7F, U+A720-A7FF;
}

/* Vietnamese */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-roman-vietnamese.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range:
    U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169,
    U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304,
    U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}

/* Cyrillic */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-roman-cyrillic.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range:
    U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}

/* Greek */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-roman-greek.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0370-03FF;
}
```

**Behavior**: if a page contains "Hello" (Latin basic only), only the Latin file is fetched. If someone pastes "Здравствуйте" into a comment form, the Cyrillic file is fetched on demand. The browser does **not** speculatively fetch all subsets (CSS Fonts 4 §4.5, stable behavior in Chrome/Firefox/Safari since ~2017).

**Pitfalls**:
- Some browsers (Chrome before 2019) would over-fetch if the page included any code point matching the range, even in `display: none` elements. This is fixed in all current stable releases.
- If you use an inline `<style>` to dynamically generate code points (e.g., user-generated content injected via JS), the browser re-evaluates the ranges on DOM mutation. There is no race; the browser loads the matching subset before rendering the new text.
- `unicode-range` only affects web-font fetching. It does not affect fallback rendering — if the subset doesn't cover a code point, the next `@font-face` block or the system fallback handles it.

### Per-page glyph subsetting at build

The more aggressive option: generate a subset that contains *exactly* the code points used on a given page (or across your whole site). Tools:

- **`glyphhanger`** (Zach Leatherman) — scans URLs (including JS-rendered output via Puppeteer) to collect code points, then drives `pyftsubset` (part of `fonttools`) to produce a subset. Still the canonical workflow as of 2026.
- **`subfont`** (Munter) — build-step tool that auto-subsets fonts referenced in your HTML output. Works well for SSG pipelines.
- **`fontaine`** — Nuxt/Vue-flavoured but runtime-agnostic. Also emits metric-aligned fallback `@font-face` blocks (see `./metric-overrides.md`).
- **`subset-font`** (Papandreou) — programmatic library, useful for custom pipelines.
- **`pyftsubset`** (from `fonttools`) — the underlying engine. Direct use if you want fine-grained control over which OpenType features/tables to keep.

When to reach for per-page subsetting:
- Logotype / brand mark where you only need ~20 specific glyphs.
- Marketing hero pages where headline text is fixed.
- UI labels in a single script that use < 100 code points.

When *not* to:
- Any page with user-generated content (comments, search results, internationalized input).
- Any site with CMS-authored body copy where the writer may legitimately use any glyph.
- Sites that will get re-subsetted anyway by a more predictable `unicode-range` strategy.

### Variable-font subsetting caveats

`pyftsubset` handles variable fonts, but there are edge cases:

- **`avar 2.0` (OpenType 1.9, 2022)** — if the font uses the "non-linear axis mapping with intermediate points" feature of `avar 2.0`, older subsetting tools may strip the `avar` table incorrectly. `fonttools` 4.43+ handles `avar 2.0`; upgrade if you hit rendering regressions after subsetting a recent variable font.
- **COLRv1 glyphs** — subsetting by code point does not reach into color-layer glyphs referenced from base glyphs. `pyftsubset` 4.38+ traces color dependencies correctly, but if you're on an older version you will ship broken color glyphs.
- **Layout features** — by default `pyftsubset` keeps all features. If you pass `--layout-features=*` you keep everything; `--layout-features-=liga` removes ligatures (rarely what you want). The safe default is `--layout-features='*'`.
- **STAT / fvar** — if you subset a variable font and restrict the axis range (`--instancer-pin wght=400` or partial instancing), the `STAT` table becomes invalid unless the tool regenerates it. `fonttools varLib.instancer` handles this; `pyftsubset` alone does not.

**The safe default for variable fonts**: subset by `unicode-range`, keep all axes, keep all features, don't instance. You almost never save enough by narrowing axes to justify the brittleness.

### CJK subsetting

CJK is a different problem category. A full Japanese or Chinese font covers **15,000–25,000+ glyphs** and weighs **5–15 MB in WOFF2**. Latin-style subsetting — "Japan" is not a 250-glyph Unicode range — doesn't help as much.

Strategies:

1. **Per-page subsetting is the only viable path for static content**. Scan exact code points, subset to ~500–2000 glyphs, serve 150–500 KB.
2. **CJK-aware dynamic subsetting**: Google Fonts CDN uses a clever approach for Noto Sans CJK — the font is split into ~100 `unicode-range` chunks based on frequency analysis, so common glyphs load first in a 30 KB chunk and rare glyphs load in later chunks. This works surprisingly well; typical first-paint includes the top-1500 most-frequent glyphs for Japanese.
3. **Dual-font approach**: Latin subset (50 KB) + CJK subset (200 KB) joined via a font stack. Latin renders immediately; CJK renders on paint.
4. **Incremental Font Transfer (IFT)** — see §Emerging below. IFT is the long-term fix: the server incrementally sends only the glyphs the page needs, at render time, with a range-request protocol.

The Chrome team (Jeffrey Kaufman) has published extensive CJK subsetting guidance (developer.chrome.com, 2024-03 and 2025-02 articles) showing that frequency-chunked `unicode-range` splits get ~90% of the IFT benefit with standard HTTP/2. For new projects the order is: frequency-split first, IFT later.

---

## `font-display` Descriptor

`font-display` is an `@font-face` descriptor that tells the browser how to render text while a web font is loading — and what to do if it never loads. The five values map to the three phases of font loading (**block**, **swap**, **failure**) via two timers:

```
[ block period ] → [ swap period ] → [ failure period ]
```

- **block period**: text is rendered invisibly (typically 0–3 s).
- **swap period**: fallback is used; if the web font arrives, it swaps in (typically up to ~30 s).
- **failure period**: fallback is used permanently.

| Value | Block period | Swap period | FOIT? | FOUT? | When to use |
|---|---|---|---|---|---|
| `auto` | UA default (~3 s) | UA default | Yes | Yes | Never use explicitly — the UA default is usually `block`, which is wrong. |
| `block` | up to ~3 s | infinite | Yes | Yes | Icon fonts where missing glyph is worse than invisible (but SVG icons are better). |
| `swap` | 0 (none) | infinite | No | Yes | **Body text default.** Shows fallback immediately, swaps when web font arrives. |
| `fallback` | ~100 ms | ~3 s | Brief | Brief | Compromise: tiny FOIT, tiny FOUT window, then lock. |
| `optional` | ~100 ms | 0 (none) | Brief | No | **Performance-first default.** If the font is cached or arrives in the block window, use it; otherwise never use it. No swap. |

**Interaction with preload**: `font-display: optional` + `<link rel="preload">` is a useful combination. Preload gives the font a head-start; `optional` ensures that if preload doesn't finish in the block window, the user never sees a swap-induced layout shift (CLS). On the second visit the font is cached and always renders.

**Interaction with metric overrides**: with metric-aligned fallback stacks (see `./metric-overrides.md`), a swap is visually invisible — the fallback occupies the same pixels the web font will occupy, so the swap is a "font face change" without any reflow. With metric overrides in place, `swap` becomes strictly better than `block` for body text.

**Interaction with Core Web Vitals**: `font-display: swap` without metric overrides causes CLS (the fallback and web font differ in advance width and ascent). `font-display: optional` sidesteps CLS entirely but at the cost of never showing the web font on slow first visits. The Core Web Vitals–friendly default in 2026-04 is **`swap` + metric overrides**, not `optional`.

**Browser support**: `font-display` is Baseline since 2020. Chrome 60+, Firefox 58+, Safari 11.1+, Edge 79+. All values work cross-browser.

### Decision table by role

| Use case | `font-display` | Preload? | Metric overrides? | Notes |
|---|---|---|---|---|
| Body serif / sans (above-the-fold) | `swap` | Yes | **Yes** | The modern default recipe. |
| Heading font (above-the-fold) | `swap` | Yes | Yes | Same as body. Balance is more visible on headings so overrides matter more. |
| Body font used mostly below the fold | `optional` | No | Optional | Cache-dependent render; never degrades FCP/CLS. |
| Icon font | `block` | Yes | — | Only if you cannot migrate to SVG icons. |
| Monospace for code blocks | `optional` or `swap` | No | Yes | Most users read code in second viewport scroll; cache-dependent is fine. |
| Specialty display face (headline only) | `swap` | Maybe | Yes | Preload only if the headline is in the initial viewport. |
| Low-priority decorative face | `optional` | No | Optional | Nothing catastrophic if it doesn't load. |

---

## Preload

`<link rel="preload" as="font">` tells the browser to start fetching a font earlier in the critical path than it otherwise would. Fonts are normally discovered late (after CSS parses and layout needs them), so a preload can save a full round-trip.

### Minimal syntax

```html
<link
  rel="preload"
  href="/fonts/inter-roman-latin.woff2"
  as="font"
  type="font/woff2"
  crossorigin
  fetchpriority="high"
>
```

**Required attributes**:
- `as="font"` — without this, the browser may download but won't preload to the font cache bucket.
- `type="font/woff2"` — helps browsers skip the request when the format isn't supported (irrelevant for WOFF2 in 2026, but good hygiene).
- `crossorigin` — **even for same-origin fonts**. Font requests are *always* CORS-fetched regardless of origin. Without `crossorigin`, the preload will be ignored and a duplicate request will fire from CSS discovery.
- `href` — must match the URL in `@font-face src` *exactly* (including trailing query strings). Browsers do not deduplicate near-matches.

**Optional but recommended**:
- `fetchpriority="high"` — HTML spec addition (Chrome 101+, 2022-04; Safari 17.2+, 2023-12; Firefox 119+, 2023-10). Bumps the font above other resources competing for bandwidth during initial load. Baseline 2024.

### When to preload

**Yes**:
- The single most-important body font for above-the-fold content.
- A distinct heading font if the heading is in the initial viewport and visually critical to brand.
- Variable-font body containers (single file, serves both roman and oblique via the italic axis — preloading once covers many display states).

**No**:
- Italic cut that appears only below the fold.
- Any font that loads only on interaction (hover, modal, etc.).
- More than ~2 fonts. Preloading 4+ fonts starves the HTML/CSS parse and makes FCP worse, not better (Harry Roberts has measured 200–400 ms regressions on third-world network profiles).
- Display faces used only on /about or /contact. Preload is per-page.

**Probably not**:
- Fonts you've delivered as `font-display: optional`. The whole point of `optional` is to render fallback on slow networks; preload subverts that goal unless the font is tiny.

### Preload + `font-display` interaction

| Preload | `font-display` | Behavior |
|---|---|---|
| Yes | `swap` | Fastest perceived font swap. Fallback shown until preloaded font arrives; swap may still cause CLS without metric overrides. |
| Yes | `optional` | "Try to get the font in the block window; if we miss, never use it." Good for cache-dependent rendering. |
| Yes | `block` | FOIT with an earlier cutoff. Useful only for small icon fonts. |
| No | `swap` | Standard fallback-then-swap pattern. Best default for progressively enhanced pages. |
| No | `optional` | Cache-dependent rendering; font almost never appears on first visit unless on a fast network. |

### Preload and variable fonts

A single variable-font file often replaces 4–8 static files. Preloading a variable font is more bandwidth-efficient than preloading 2 static cuts, *provided* the variable file is smaller than the sum of the cuts you'd otherwise preload. Rule of thumb: variable wins at 3+ cuts after Brotli compression.

---

## HTTP Delivery

### HTTP/2 and HTTP/3

The bad-old-days of web-font delivery assumed HTTP/1.1 with 6-connection-per-origin parallelism. That imposed a hard ceiling on the number of fonts you could fetch without head-of-line blocking. Two things changed it:

1. **HTTP/2 (2015)**: multiplexes streams over a single connection. Head-of-line blocking moved to TCP, not protocol.
2. **HTTP/3 / QUIC (RFC 9114, 2022)**: uses UDP with per-stream ordering, eliminating TCP-level head-of-line. Serial font loads from a single origin are essentially free of head-of-line penalties in 2026.

**Practical effect on font delivery**:
- Pre-2015 advice to "concatenate all fonts into a single file via base64 embedding" is obsolete. Keep fonts as separate `@font-face` requests.
- The Google Fonts `unicode-range` splits work well over HTTP/2 and HTTP/3; each subset is an independent request but they multiplex cleanly.
- For same-origin fonts, HTTP/3 gives you 5–15% FCP improvement over HTTP/2 on lossy mobile networks (Cloudflare and Fastly measurements, 2024–2025).
- The revived HTTP/2 `push` for fonts is **dead**: Chrome removed server-push support (Chrome 106, 2022-09). `<link rel="preload">` replaced it. Don't configure origin-push for fonts in 2026.

### Cache-Control

Fonts rarely change; when they do, they change names (fingerprinted URLs). The correct pattern is:

```
Cache-Control: public, max-age=31536000, immutable
```

- `public` — allows shared caches (CDNs, corporate proxies).
- `max-age=31536000` — one year, the current practical cap for long-TTL resources.
- `immutable` — tells the browser not to re-validate. Saves a 304 check. Supported in Firefox, Safari 14+, Chrome (no-op but harmless).

If your build emits `/fonts/inter-roman-latin.DEADBEEF.woff2`, this is safe. If you emit `/fonts/inter-roman-latin.woff2` without fingerprinting, drop `immutable` and use `max-age=604800` (one week).

### Service-worker caching

Fonts are ideal service-worker candidates: rarely updated, bounded in size, worth bulletproof offline coverage.

```js
// service-worker.js — fonts go in a stale-while-revalidate cache
const FONT_CACHE = "fonts-v1";

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith("/fonts/")) {
    event.respondWith(
      caches.open(FONT_CACHE).then(async (cache) => {
        const cached = await cache.match(event.request);
        const network = fetch(event.request).then((res) => {
          cache.put(event.request, res.clone());
          return res;
        });
        return cached || network;
      })
    );
  }
});
```

Common pitfall: if your service worker caches fonts *without* matching the `Access-Control-Allow-Origin` headers, the browser will refuse to use them via CORS. Use `new Request(url, { mode: 'cors' })` when prefetching, or ensure your cache hits include the full response headers.

Workbox (Google's SW library) has a font-recipe preset that handles this correctly — reach for that rather than rolling your own if you're on Workbox already.

### CDN vs self-host

There are four practical paths:

#### 1. Self-host from your own origin

**Pros**:
- Same-origin delivery; no DNS lookup, no TCP handshake, no TLS handshake beyond the one you already did for HTML/CSS.
- Full control over `Cache-Control`, CORS headers, and subsetting.
- No third-party tracking risk.
- No EU privacy exposure (see below).

**Cons**:
- You maintain the subsets and build pipeline.
- You pay for egress (usually trivial; fonts are tiny).

**Tooling**:
- **`@fontsource/*`** — npm packages of self-hostable Google Fonts, correctly subsetted with `unicode-range` splits. Current as of 2026-04. This is the default for most projects.
- **`fontsource-variable`** — variable-font versions, same subsetting strategy.
- Direct download from Google Fonts + run through `glyphhanger` / `pyftsubset` if you need a different subset shape.

#### 2. Google Fonts CDN (`fonts.googleapis.com`)

**Pros**:
- Zero setup.
- Google's CDN is fast (global POPs).
- Google pre-subsets with `unicode-range`.

**Cons**:
- **EU privacy risk** (see below).
- The CSS file is on `fonts.googleapis.com` and the font files are on `fonts.gstatic.com` — two extra DNS/TLS hops before first byte of font. The CSS hop blocks the critical path.
- No control over which subsets ship; you get Google's defaults.

#### 3. Bunny Fonts (`fonts.bunny.net`)

**Pros**:
- Drop-in Google Fonts replacement with matching URL structure.
- Hosted in EU-friendly jurisdictions with a privacy policy that complies with GDPR without consent prompts.
- Same `unicode-range` subsetting as Google.

**Cons**:
- Smaller font library than Google Fonts.
- External CDN; DNS/TLS hops same as Google.

**When to choose Bunny Fonts over self-host**: if you want the Google-Fonts DX without the privacy liability and you don't want to manage subsetting yourself.

#### 4. Adobe Fonts / Monotype / subscription foundries

**Pros**:
- Access to commercial libraries (Fraktur, Paratype, KLIM, Grilli Type, etc., depending on subscription).
- Adobe's CDN is fast and stable.
- Licensing handled by the vendor.

**Cons**:
- JavaScript-based loader (Typekit pattern) — adds a render-blocking script and delays font discovery.
- Vendor lock-in.
- Privacy footprint similar to Google Fonts, though Adobe publishes a clearer data-processing agreement.

**Modern Adobe Fonts** (2024+) supports a CSS-only embed mode that avoids the JS loader. Use that when possible.

### Privacy implications — Google Fonts and the EU

This is the decision that has flipped for most EU-facing sites between 2022 and 2026. The timeline:

- **Munich District Court, January 2022** — ruled that embedding Google Fonts without a user's consent transfers their IP address to Google, which constitutes processing of personal data under GDPR Art. 4(1), without a legal basis. Plaintiff awarded €100.
- **Italian Data Protection Authority (Garante), March 2023** — issued guidance classifying IP addresses sent to Google Fonts CDN as personal data requiring Art. 6 legal basis (typically consent).
- **CNIL (France), 2024 guidance** — Google Fonts CDN falls under "third-party data transfers" and requires prior consent unless self-hosted or proxied.
- **Schrems II implications (ongoing)** — data transfers to US-based CDNs remain contested under the EU-US Data Privacy Framework (2023); status changed again with the July 2025 ECJ ruling on adequacy decision scope.

**Practical effect for EU-facing sites in 2026-04**:
- Default to **self-host** for Google Fonts.
- If you must use a CDN, use **Bunny Fonts** (EU-friendly) or proxy Google Fonts through your own origin.
- If you use Google Fonts directly, gate the `<link>` injection behind consent management, which defeats most of the latency benefit anyway.

**US-only or global-non-EU sites**: these rulings don't apply, and Google Fonts CDN remains fast and free. But the self-host story is good enough that most new projects self-host regardless — one less third-party dependency.

---

## Loading Patterns (FOIT / FOUT / FOFT)

The three named patterns describe what a user sees while a web font is loading. Zach Leatherman's taxonomy (2016, revised multiple times; his 2020 "comprehensive" update is still canonical) covers them:

### FOIT — Flash of Invisible Text

**What it is**: text is rendered invisibly until the web font loads (or the block timeout expires, typically 3 s).

**When it happens**: `font-display: block`, or legacy browsers pre-`font-display` (IE, old Edge).

**Why it's bad**: your page looks loaded but the text is unreadable. Users perceive this as slower than plain fallback text.

**When it's acceptable**: icon fonts, where the fallback character is meaningless or wrong. (But you should migrate to SVG icons.)

### FOUT — Flash of Unstyled Text

**What it is**: fallback font renders immediately; web font swaps in when it loads.

**When it happens**: `font-display: swap`.

**Why it's the default**: users can read from T+0. The swap is visible but content is always accessible.

**Downside without metric overrides**: the swap causes CLS. With metric overrides (`size-adjust` + `ascent-override`), the fallback pre-sizes to match the web font and the swap becomes invisible in layout terms. See `./metric-overrides.md`.

### FOFT — Flash of Faux Text

**What it is**: a two-stage load. First, a lightweight subset (roman only, ASCII only) loads fast and is shown with CSS faux-bold/italic synthesis. Second, the full weighted fonts load and replace the faux-synthesized versions.

**Where it came from**: Zach Leatherman's 2015–2016 writings. The pattern was designed for a pre-variable-font world where you shipped multiple static cuts and the roman-regular cut was on the critical path while bold/italic weren't.

**Modern relevance**: **largely obsolete.** Variable fonts collapse most of the "multiple cuts" problem into a single file. If you ship a variable font with `wght` + `ital`, you have one file that covers all the cases; there's no staging to do. FOFT patterns are still occasionally useful when:
- You can't ship a variable font (licensing, legacy rendering pipeline).
- Your brand font is 4+ static cuts and you need to prioritize roman-regular aggressively.

### Pattern snippets

**Pattern A — Modern default (WOFF2, variable, metric-override fallback)**:

```html
<link
  rel="preload"
  href="/fonts/inter-variable-latin.woff2"
  as="font"
  type="font/woff2"
  crossorigin
  fetchpriority="high"
>
```

```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-variable-latin.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, /* …basic Latin… */ ;
}

/* Metric-aligned system fallback. See ./metric-overrides.md for derivation. */
@font-face {
  font-family: "Inter-Fallback";
  src: local("Arial");
  size-adjust: 107.4%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: "Inter", "Inter-Fallback", Arial, sans-serif;
}
```

**Pattern B — `font-display: optional` for aggressive CLS avoidance**:

```css
@font-face {
  font-family: "Playfair Display";
  src: url("/fonts/playfair-variable.woff2") format("woff2-variations");
  font-weight: 400 900;
  font-style: normal;
  font-display: optional;  /* Don't swap; either use cache or stay on fallback. */
}
```

**Pattern C — Font Loading API (advanced; explicit control)**:

```html
<style>
  /* Declare the font but don't reference it yet. */
  @font-face {
    font-family: "Inter";
    src: url("/fonts/inter-variable-latin.woff2") format("woff2-variations");
    font-weight: 100 900;
    font-display: swap;
  }

  /* Pre-apply a "loaded" class on <html> to opt in. */
  .fonts-loaded body {
    font-family: "Inter", system-ui, sans-serif;
  }

  body {
    font-family: system-ui, sans-serif;  /* Pre-load fallback. */
  }
</style>
<script>
  document.fonts.load('1em "Inter"').then(() => {
    document.documentElement.classList.add('fonts-loaded');
  });
</script>
```

The CSS Font Loading API (`document.fonts`) is Baseline (all engines since ~2019). It's the lowest-level, most predictable control — but it is more code than most sites need. Reach for it when you have specific requirements that `font-display` can't express (e.g., "show fallback for exactly 800 ms, then switch").

---

## Variable Fonts — Delivery Tradeoffs

(See `./variable-fonts.md` for axis semantics. Here we focus only on delivery.)

### When variable beats static

**Rule of thumb**: variable wins when you ship 3+ cuts of a family.

- 2 cuts (roman + italic, both regular weight): a two-axis variable file is often larger than two static cuts because of `gvar`/CFF2 overhead. Ship static.
- 3 cuts: break-even. Often variable wins slightly after WOFF2.
- 4+ cuts: variable usually wins 30–50% on file size.
- 8+ cuts: variable is a clear win (2–3× smaller) and also gives you the in-between weights for free.

**Benchmarks (Roboto Flex, 2024 measurement)**:
- Static Roboto Regular (wght=400): ~30 KB WOFF2.
- Static Roboto Light + Regular + Medium + Bold + Black: ~145 KB total.
- Roboto Flex variable (all `wght` + `wdth` + `slnt` + 11 custom axes): ~280 KB WOFF2.

So Roboto Flex is *larger* than 5 static cuts — but it gives you 13 axes and infinite interpolation. The decision is whether you use those axes.

**Recursive (ArrowType)** is another reference: a single variable file, ~150 KB WOFF2, covers the full range from monospace to sans + `wght` 300–1000 + `slnt` + `CRSV` + `MONO`. Shipping it as statics would be 15+ files.

### Subsetting variable fonts

Variable fonts subset cleanly by `unicode-range` with `pyftsubset`. Caveats:

- Don't narrow the axis range unless you know what you're doing. Partial instancing via `varLib.instancer` is a build step that must regenerate `STAT` and `fvar`.
- Keep `GSUB`/`GPOS` tables intact. Subsetting them breaks OpenType features (e.g., `ss01`, `tnum`).
- Keep `HVAR`/`MVAR` tables. They hold the variation deltas for advance width and layout metrics; losing them makes the variable interpolation asymmetric.

### Variable-font file sizes at a glance

| File | Size (WOFF2) | Static equivalent |
|---|---|---|
| Inter variable (`wght` + `slnt`, Latin-only subset) | ~85 KB | 4× static ≈ 80 KB |
| Inter variable (full Unicode) | ~380 KB | 4× static ≈ 400 KB |
| Roboto Flex (13 axes, Latin-only) | ~280 KB | 5× static ≈ 145 KB |
| Recursive (sans + mono, `wght`/`slnt`/`CRSV`/`MONO`) | ~150 KB | 15+ static ≈ 600 KB |
| Noto Sans CJK JP variable (`wght`) | ~8 MB | 7× static ≈ 30 MB |

---

## Emerging (as of 2026-04)

### Incremental Font Transfer (IFT)

**What it is**: a protocol where the server sends only the glyphs the client needs at render time, in range-request chunks, reusing a patching format (Brotli Shared Dictionary) across requests. The client assembles the font incrementally as more glyphs are needed.

**Status (2026-04)**: W3C Fonts WG **Working Draft**. The spec has been "almost there" for 3+ years. Active drafting at https://www.w3.org/TR/IFT/ (as of 2026-04-17). Chrome has a prototype (behind `chrome://flags/#incremental-font-transfer`, updated through 2025); Firefox and Safari have not shipped.

**Why it matters**: CJK. A 25,000-glyph font that's normally 10–15 MB could ship as a 50–200 KB initial request + on-demand patches. For Latin, IFT provides maybe 30% bandwidth savings; for CJK, it's 10–100× depending on page content.

**What to do now**: nothing. Keep using `unicode-range` splits. IFT will be a future drop-in win when it stabilizes. Reasonable bet: stable cross-browser Baseline by 2027-2028.

### `fetchpriority` for fonts

Already covered above. Shipped and stable Baseline 2024.

### Client Hints and font selection

`Sec-CH-UA`, `Sec-CH-UA-Platform`, `Sec-CH-UA-Mobile` — these allow the server to select different font subsets per client. Not widely used for fonts today (2026-04); most of the decisioning happens on the client via `@font-face` directly. The one production pattern: serving pre-fingerprinted variable vs static based on client age (assume ancient Safari → static, modern → variable). Diminishing returns now that every browser supports variable fonts.

### Compression: Brotli-over-Zstandard

Zstandard (Zstd) entered the browser with Chrome 123 (2024-03), Firefox 126 (2024-05). For font transfer specifically, Zstd is slightly worse than Brotli on WOFF2 payloads (because WOFF2 already Brotli-compresses internally). Not relevant for font delivery.

### HTTP/3 0-RTT for fonts

If your TLS 1.3 session is resumed, 0-RTT allows the font fetch to piggyback on the connection setup. This is enabled by default in Chrome, Firefox, Safari with HTTP/3. No configuration needed.

---

## Anti-patterns

### 1. Preloading every font
Preloading 4+ fonts pushes HTML/CSS parse off the critical path. The first font arrives faster; overall FCP regresses. Rule: preload at most 2.

### 2. Omitting `crossorigin` on preload
Without `crossorigin`, the preload is wasted; the browser fires a second, non-preloaded request from CSS discovery. Symptom: two network requests for the same font URL, neither benefiting from the other.

### 3. Shipping WOFF alongside WOFF2
Wastes build time and bytes. Every modern browser that fetches your WOFF2 also supports WOFF2. IE11 is dead.

### 4. Shipping TTF/OTF over HTTP
Typically 2× the size of WOFF2. No upside. Keep raw SFNT for design-tool authoring only.

### 5. `font-display: auto` (or no descriptor)
Defers to the UA default, which is `block` in most engines — meaning FOIT by accident. Always specify.

### 6. Using `@import` for Google Fonts
```css
@import url("https://fonts.googleapis.com/css2?family=Inter");
```
This blocks CSS parsing until the imported file arrives — worst case on the critical path. Use `<link rel="stylesheet">` or (better) self-host.

### 7. Static `@font-face` for a variable font you've shipped
```css
/* Wrong: ships 4 files for one variable family */
@font-face { font-family: "X"; src: url("x-regular.woff2"); font-weight: 400; }
@font-face { font-family: "X"; src: url("x-bold.woff2"); font-weight: 700; }
@font-face { font-family: "X"; src: url("x-italic.woff2"); font-style: italic; }
@font-face { font-family: "X"; src: url("x-bold-italic.woff2"); font-weight: 700; font-style: italic; }
```
If you have a variable font, declare it once with `font-weight: 100 900`:
```css
@font-face {
  font-family: "X";
  src: url("x-variable.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
}
```

### 8. Using Google Fonts CDN for EU-facing sites without consent
See §Privacy above. Expect legal complaints; expect competitor PRs about your privacy posture.

### 9. Cache-Control without fingerprinted URLs
`max-age=31536000, immutable` on a non-versioned URL means users see stale fonts for a year after you ship a new brand. Fingerprint before you long-cache.

### 10. Embedding fonts as base64 data URIs in CSS
Defeats HTTP caching (the font re-downloads on every CSS change), inflates CSS by 30%+ after base64 overhead, and blocks CSS parse. Pre-2015 HTTP/1.1 era tactic. Obsolete.

### 11. Loading fonts with JavaScript that blocks render
Typekit-style synchronous loaders, or `new FontFace()` assignments in a blocking script, defer font discovery. Use `<link rel="preload">` or `<link rel="stylesheet">` instead.

### 12. Not pairing web fonts with metric-aligned fallbacks
Results in visible CLS on every first visit. Cheap to fix (~5 lines of CSS per family) and the single best CLS optimization for font-heavy sites. See `./metric-overrides.md`.

### 13. Over-subsetting and breaking scripts
Aggressive per-page subsetting can drop combining marks or contextual forms. Common symptom: Vietnamese tones rendered as tofu despite the base vowel rendering. Test subsets against a representative sample of expected content; don't subset blindly.

### 14. Using `font-display: block` as a universal default
Cargo-culted from icon-font advice. For body text, `block` is strictly worse than `swap`. For headings, `block` prevents the reader from starting to read until the font loads — a poor UX default.

### 15. Preloading fonts that `font-display: optional` then rejects
`optional` gives the font a short window (~100 ms after paint) to be used. If preload wins the race, great. If not, the preload is wasted bandwidth. Pair preload + optional only when you know the font is small (< 30 KB WOFF2) and HTTP/3 is on.

---

## Sources

URLs with dates retrieved 2026-04-17 unless noted.

- **W3C CSS Fonts Module Level 4 (Working Draft)**: https://www.w3.org/TR/css-fonts-4/ — last updated 2024-09-24; still the basis for `@font-face`, `font-display`, `unicode-range`, `size-adjust`.
- **W3C CSS Fonts Module Level 5 (Editor's Draft)**: https://drafts.csswg.org/css-fonts-5/ — tracks IFT hooks and new descriptors; not yet stable.
- **W3C Incremental Font Transfer (Working Draft)**: https://www.w3.org/TR/IFT/ — snapshot 2024-11-07; active drafting continues 2025–2026.
- **W3C WOFF2 Recommendation**: https://www.w3.org/TR/WOFF2/ — published 2018-03-01, unchanged.
- **MDN `font-display`**: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display — retrieved 2026-04-17.
- **MDN `unicode-range`**: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range — retrieved 2026-04-17.
- **MDN `rel="preload"`**: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link — retrieved 2026-04-17.
- **MDN `fetchpriority`**: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/fetchpriority — retrieved 2026-04-17.
- **web.dev — "Optimize WebFont loading" (Addy Osmani, updated 2024)**: https://web.dev/articles/optimize-webfont-loading.
- **web.dev — "Prevent layout shifts" (Katie Hempenius, 2023)**: https://web.dev/articles/preload-optional-fonts.
- **web.dev — "font-display for the masses" (Brad Fitzpatrick)**: https://web.dev/articles/font-display.
- **web.dev — "Reduce WebFont size" (Ilya Grigorik)**: https://web.dev/articles/reduce-webfont-size.
- **Chrome for Developers — "CSS font fallbacks you can use today" (Katie Hempenius, updated 2024)**: https://developer.chrome.com/blog/font-fallbacks/.
- **Industrial Empathy — "High-performance web-font loading" (Malte Ubl, updated 2023)**: https://www.industrialempathy.com/posts/high-performance-web-font-loading/.
- **CSS Wizardry — "The Fastest Google Fonts" (Harry Roberts, 2020; reviewed 2024)**: https://csswizardry.com/2020/05/the-fastest-google-fonts/.
- **Zach Leatherman — "A Comprehensive Guide to Font Loading Strategies"** (2020 revision of the canonical FOUT/FOIT/FOFT essay): https://www.zachleat.com/web/comprehensive-webfonts/.
- **Fontsource docs**: https://fontsource.org/docs/introduction — retrieved 2026-04-17.
- **Bunny Fonts**: https://fonts.bunny.net/ — retrieved 2026-04-17.
- **caniuse — WOFF2**: https://caniuse.com/woff2 — 2026-04.
- **caniuse — `font-display`**: https://caniuse.com/mdn-css_at-rules_font-face_font-display — 2026-04.
- **caniuse — `fetchpriority`**: https://caniuse.com/mdn-html_elements_link_fetchpriority — 2026-04.
- **Munich District Court — Google Fonts ruling (Az. 3 O 17493/20)**, 2022-01-20.
- **Garante per la Protezione dei Dati Personali — guidance on Google Fonts**, 2023-03.
- **CNIL — third-party fonts guidance**, 2024.
- **Microsoft Learn — OpenType spec (CFF, CFF2, `gvar`, `HVAR`, `STAT`)**: https://learn.microsoft.com/en-us/typography/opentype/spec/ — updated 2024-05-29.
