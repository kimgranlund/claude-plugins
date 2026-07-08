---
date: 2026-04-17
coverage: deep
peers:
  - ../metrics/units.md
  - ../metrics/metrics-glossary.md
  - ./variable-fonts.md
  - ./metric-overrides.md
  - ./font-delivery.md
primary_sources:
  - https://www.w3.org/TR/css-inline-3/
  - https://drafts.csswg.org/css-text-4/
  - https://drafts.csswg.org/css-text-3/
  - https://www.w3.org/TR/css-fonts-4/
  - https://drafts.csswg.org/css-fonts-5/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-trim
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-edge
  - https://developer.mozilla.org/en-US/docs/Web/CSS/initial-letter
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-spacing-trim
  - https://developer.mozilla.org/en-US/docs/Web/CSS/word-break
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hyphens
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hyphenate-character
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hyphenate-limit-chars
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis
  - https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap
  - https://developer.mozilla.org/en-US/docs/Web/CSS/letter-spacing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/word-spacing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-indent
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-east-asian
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-alternates
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-emoji
  - https://developer.chrome.com/blog/css-text-box-trim
  - https://developer.chrome.com/blog/css-i18n-features
  - https://chrome.dev/css-wrapped-2025/
  - https://caniuse.com/css-text-wrap-balance
  - https://caniuse.com/mdn-css_properties_text-wrap_pretty
  - https://caniuse.com/css-text-box-trim
  - https://caniuse.com/css-initial-letter
  - https://caniuse.com/css-hanging-punctuation
  - https://caniuse.com/mdn-css_properties_text-spacing-trim
  - https://caniuse.com/mdn-css_properties_word-break_auto-phrase
  - https://caniuse.com/mdn-css_properties_hyphenate-limit-chars
  - https://caniuse.com/mdn-css_properties_hyphenate-character
  - https://caniuse.com/font-size-adjust
  - https://caniuse.com/mdn-css_properties_font-variant-emoji
  - https://caniuse.com/mdn-css_properties_text-indent_hanging
  - https://css-tricks.com/interop-2026/
  - https://clagnut.com/blog/2445
---

# CSS Text Properties — Modern Surface

Covers the CSS text/font surface that defines line-breaking, trimming, hyphenation, spacing, typographic features, and fallback robustness, with browser support dated to **April 2026**. Out of scope: font loading, `@font-face` descriptors, subsetting, and `font-display` (see `./font-delivery.md`); metric overrides via `ascent-override` / `descent-override` / `line-gap-override` / `size-adjust` (see `./metric-overrides.md`); variable font axis mechanics (see `./variable-fonts.md`); raw metric definitions like x-height, cap-height, advance width (see `../metrics/metrics-glossary.md` and `../metrics/units.md`). All dated claims are scoped to stable releases unless marked "flagged" or "behind flag"; "Baseline" references use the Web Platform DX Community Group baseline definition.

---

## Quick Decision Table

| Property | Use when | Avoid when | Support tier (2026-04) |
|---|---|---|---|
| `text-wrap: balance` | Headings, pull quotes, cards — ≤6 lines (Chromium) / ≤10 (Firefox) | Body copy, dynamic content, long runs | Baseline 2024 (all four engines) |
| `text-wrap: pretty` | Body copy when layout quality beats perf | Long lists, tight perf budgets, Firefox-only targets | Chrome 117+/Safari 26+; Firefox **unshipped** |
| `text-wrap: stable` | `contenteditable` to prevent reflow during typing | As a quality pass — behaves like `wrap` | Chrome 130+/Safari 17.5+/Firefox 121+ |
| `text-box` / `-trim` / `-edge` | Optical alignment of text blocks, button padding, hero sections | Firefox-only targets; content mixing scripts at different sizes | Chromium 133+/Safari 18.2+; Firefox **unshipped** |
| `initial-letter` | Drop caps in long-form editorial | Interactive UI, ≤2 line designs, Firefox-only targets | WebKit/Blink partial; Firefox **none**; no full-spec implementation |
| `hanging-punctuation` | Editorial with pull quotes, justified text | Reliant on value `last` in any browser | Safari-only partial (since Safari 10); Chrome *Intent to Prototype* July 2025 |
| `text-spacing-trim` | CJK UI with full-width punctuation kerning | Non-CJK text; Firefox/Safari targets | Chrome 123+/Edge 123+; Firefox/Safari **unshipped** |
| `word-break: auto-phrase` | Japanese (and future Chinese/Korean) headings/labels | Latin text; Firefox/Safari targets | Chrome 119+; Japanese only today |
| `hyphens: auto` | Justified paragraphs with `lang` set correctly | No `lang` attribute; monospace/code | Baseline 2023 (all engines) |
| `hyphenate-character` | Language-specific hyphen character (e.g. `=` for German academic) | Where exact hyphen spec is unset by content author | Baseline 2023 (all engines) |
| `hyphenate-limit-chars` | InDesign-quality hyphenation control | Safari targets; Firefox pre-137 | Chrome 109+/Firefox 137+; Safari **unshipped** |
| `font-size-adjust` | Aligning fallback x-heights/cap-heights to web font | Without a second value (default behavior is `ex-height`) | Baseline 2024 (Firefox 118/Safari 17/Chrome 127) |
| `font-synthesis-*` | Preventing synthesized bold/italic on scripts that can't afford it (Arabic, CJK) | Suppressing accessible italics without a replacement | Shorthand Baseline Jan 2022; `-position` experimental |
| `letter-spacing` / `word-spacing` | Display sizes, uppercase tracking, small-caps | Connected scripts (Arabic, Brahmic), body text in unit-based `em` without measurement | Baseline since 2015 |
| `text-indent: each-line hanging` | Poetry, bibliographies, hanging bulleted content | Chromium-only targets pre-146 | Safari 15+/Firefox 121+/Chrome 146+ |
| `overflow-wrap: anywhere` vs `break-word` | `anywhere` when min-content should include break opportunities; `break-word` otherwise | Safari targets relying on `anywhere` for intrinsic sizing | `break-word` Baseline 2018; `anywhere` partial in Safari through 26.x |
| `word-break: break-all` vs `break-word` | `break-all` for CJK/alphanumeric arbitrary breaking; `break-word` is an alias for `overflow-wrap: break-word` | As substitute for `hyphens` | Baseline since 2015 |
| `font-variant-*` (numeric, caps, ligatures, east-asian, position, alternates) | OpenType feature activation via named switches | When font lacks the feature (silent no-op) | Baseline January 2020 |
| `font-variant-emoji` | Forcing text/emoji presentation selection | Safari targets (2026) | Chrome 131+/Firefox 141+; Safari **unshipped** |

---

## Property Reference

### `text-wrap`, `text-wrap-mode`, `text-wrap-style`

**Shorthand syntax (CSS Text 4)**
```
text-wrap        = <'text-wrap-mode'> || <'text-wrap-style'>
text-wrap-mode   = wrap | nowrap
text-wrap-style  = auto | balance | stable | pretty | avoid-orphans
```

**What it does.** `text-wrap-mode` replaces the breaking half of `white-space`; `text-wrap-style` selects a wrapping algorithm.
- `wrap` (mode): Normal breaking at soft wrap opportunities.
- `nowrap` (mode): Suppress all soft wraps; content overflows.
- `auto` (style): UA default, usually greedy-first-fit.
- `balance` (style): Solves for minimum ragged-right by minimizing line-count variance across a limited number of lines.
- `pretty` (style): Higher-quality greedy+backtrack or full-paragraph optimizer; reduces orphaned short final lines and bad widows.
- `stable` (style): Like `wrap`, but keeps already-rendered lines stable while later content changes (use case: `contenteditable`).
- `avoid-orphans` (style): CSS Text 4 draft; prevents 1-word last lines. **Not yet shipped in any engine as of 2026-04.**

**When to use each.**
- `balance` for headings and short cards ≤ ~6 lines (Chromium cap) / ~10 lines (Firefox cap) — Safari has a similar bound per spec note.
- `pretty` for body copy where visual quality matters more than layout performance.
- `stable` for live-editing surfaces (`contenteditable="true"`).
- `nowrap` for truncation patterns (paired with `overflow: hidden; text-overflow: ellipsis`).

**Browser support (2026-04).**
- `balance`: Chrome 114 (partial, 2023-05) → **Chrome 130** (full, 2024-10); Edge 130; **Safari 17.5** (2024-05); **Firefox 121** (2023-12). Baseline 2024.
- `pretty`: **Chrome 117** (2023-09); Edge 117; **Safari 26.0** (2025-09). **Firefox: unshipped as of 152** (April 2026). Firefox gracefully degrades to `wrap`.
- `stable`: **Safari 17.5** (2024-05); **Firefox 121** (2023-12); **Chrome/Edge 130** (2024-10).
- `avoid-orphans`: **no engine ships it** (2026-04).

**Gotchas.**
- `balance` is a no-op above the UA line threshold — it silently falls back to `wrap`. Tune your heading widths, don't expect `balance` to rescue ten-line runs.
- `pretty` is explicitly opt-in for its cost; avoid on extremely large paragraphs or on virtualized lists.
- `stable` is widely considered a no-op in practice for non-editable content; community consensus is that its observable behavior equals `wrap`. Don't rely on it as a quality improvement outside `contenteditable`.
- `text-wrap-mode` is the replacement for the wrap half of `white-space` — a long-running cleanup in CSS Text 4. The old `white-space: nowrap` still works.

---

### `text-box`, `text-box-trim`, `text-box-edge` (formerly `leading-trim`)

**Syntax (CSS Inline 3)**
```
text-box       = normal | <'text-box-trim'> || <'text-box-edge'>
text-box-trim  = none | trim-start | trim-end | trim-both
text-box-edge  = auto | <text-edge>
<text-edge>    = [ text | ideographic | ideographic-ink | cap | ex ]
                 [ text | ideographic | ideographic-ink | alphabetic ]?
```

Both edges can be set together: `text-box-edge: cap alphabetic` (over-edge = cap-height, under-edge = alphabetic baseline).

**What it does.** Trims the half-leading (the space above the ascender and below the descender) so block edges align to a chosen metric. Replaces the renamed `leading-trim` property (first proposed ~2020). The shorthand `text-box` combines trim side and edge:
```css
.btn { text-box: trim-both cap alphabetic; }   /* button label optically centered */
```

**When to use.**
- Button internals: after `text-box: trim-both cap alphabetic`, equal `padding-block` values look optically equal across fonts.
- Hero typography: trimming top half-leading removes the visual gap between a headline and a preceding image.
- Mixed font pairings: normalizes heights between fonts whose metrics differ.

**Browser support (2026-04).**
- **Chrome 133** (2025-02), **Edge 133** (2025-02), **Safari 18.2** (2024-12) ship the properties by default.
- Flagged earlier: Chrome 128–132, Edge 128–131, Safari 16.4–18.1 (behind "Experimental Web Platform features" / WebKit experimental flag).
- **Firefox: unshipped as of 152** (April 2026).
- Global usage ~84% (caniuse, March 2026).

**Gotchas.**
- Firefox does nothing; design must still work without trim. The property is safe to progressively enhance because it collapses to the pre-trim layout gracefully.
- `text-box-edge: auto` keeps the old (untrimmed) behavior and is the initial value.
- Percentage paddings now behave slightly differently in trimmed blocks — sizes are computed against the trimmed box, not the font's design metrics.
- Applying `text-box: trim-both` to a multi-line paragraph only trims the first and last lines, not interior leading.
- `leading-trim` is the **deprecated spelling** and never shipped. Do not author it.

---

### `initial-letter`, `initial-letter-align`

**Syntax (CSS Inline 3)**
```
initial-letter        = normal
                      | <number [1,∞]> <integer [1,∞]>?
                      | <number [1,∞]> && [ drop | raise ]?
initial-letter-align  = [ border-box? [ alphabetic | ideographic | hanging | leading ]? ]!
```

**What it does.** Sets a dropped or raised initial letter on `::first-letter` (or an inline-level first child). First number = how many lines tall; second integer or `drop|raise` keyword = sink depth.

```css
p::first-letter {
  initial-letter: 3;          /* 3-line drop cap */
  initial-letter: 3 2;        /* 3 lines tall, base at line 2 */
  initial-letter: 4 raise;    /* raised cap 4 lines tall */
}
```

**Browser support (2026-04).**
- **Safari 9+** (2015-10): partial (with and without `-webkit-` prefix).
- **Chrome 110 / Edge 110** (2023-02): partial unprefixed.
- **Opera 98**; **Samsung Internet 21**; **Chrome Android 147**, **Safari iOS 9+**: partial.
- **Firefox**: **unshipped as of 152** (April 2026).
- No browser advertises full-spec support; every implementation is listed as *partial* on caniuse.

**Gotchas.**
- "Partial" typically means: single-number form works, sink behavior varies, `::first-letter` interactions with punctuation differ between engines, and `initial-letter-align` is mostly unimplemented.
- The initial letter box is sized and positioned using font metrics — different fonts give visibly different results at the same number.
- Quotation marks before the first letter often slip outside the initial-letter box; combine with `hanging-punctuation: first` (Safari) or manual wrapping.
- Firefox renders no drop cap — plan a non-broken fallback (e.g., the first letter simply isn't enlarged).
- Use `::first-letter` plus `font-size` as a fallback when precise cap-height sink is not required.

---

### `hanging-punctuation`

**Syntax (CSS Text 4)**
```
hanging-punctuation = none | [ first || [ force-end | allow-end ] || last ]
```

**What it does.** Allows quotation marks, opening/closing brackets, stops, or commas to hang outside the block's inline edge so the visible text edge stays flush.

**Browser support (2026-04).**
- **Safari 10+** (2016-09): partial (`first`, `allow-end`, `force-end`; **`last` is not supported in any browser**).
- **Chrome/Chromium**: no support in stable (all versions 4–150). An *Intent to Prototype* was filed mid-2025, and hanging-punctuation is part of the **Interop 2026** focus areas.
- **Firefox**: no support (all versions 2–152).
- Global usage ~18% (caniuse, 2026-03) — Safari-only.

**Gotchas.**
- Safe to use as progressive enhancement: non-supporting browsers simply don't hang.
- `last` is specced but no engine implements it.
- On justified text (`text-align: justify`), `allow-end`/`force-end` change how terminal punctuation participates in justification.
- Hanging an opening quote requires the quote character to actually be present — CSS quote auto-generation via `content: open-quote` works with it.

---

### `text-spacing-trim`

**Syntax (CSS Text 4)**
```
text-spacing-trim = normal | space-all | space-first | trim-start
                  | trim-all      (* specced, unimplemented *)
                  | trim-both     (* specced, unimplemented *)
                  | auto          (* specced, unimplemented *)
```

**What it does.** Controls kerning/trimming of CJK full-width punctuation adjacent to other characters and at line edges — the equivalent of InDesign's CJK punctuation spacing.

- `normal`: UA default CJK punctuation kerning.
- `space-all`: No kerning; all CJK full-width punctuation retains full advance.
- `space-first`: Opening full-width punctuation keeps full width only at line start / after forced break.
- `trim-start`: Opening full-width punctuation is half-width at line start.

**Browser support (2026-04).**
- **Chrome 123** (2024-03), **Edge 123** (2024-03), **Opera 109** (2024-02): shipped.
- **Firefox**: unshipped as of 152.
- **Safari**: unshipped through 26.5 (Tech Preview status unclear).
- Global usage ~72% (caniuse).

**Gotchas.**
- Only meaningful for Chinese, Japanese, Korean. Applying to Latin text is a no-op.
- The four unimplemented values (`trim-all`, `trim-both`, `auto`, and additional tokens in L4) mean you cannot express full InDesign-equivalent controls today.

---

### `word-break`

**Syntax (CSS Text 3/4)**
```
word-break = normal | keep-all | break-all | break-word | auto-phrase | manual
```
(`break-word` is deprecated-aliased to `overflow-wrap: break-word`; `manual` is specced but unshipped everywhere.)

**What each value does.**
- `normal`: UA default per locale.
- `keep-all`: Forbid breaks within CJK; Latin unchanged.
- `break-all`: Allow breaks between *any* two typographic letter units (not just soft-wrap opportunities). Overrides `hyphens`.
- `break-word`: Deprecated alias; behaves like `overflow-wrap: break-word` but **with** `min-content` effects from `word-break` rather than from `overflow-wrap`.
- `auto-phrase`: Language-aware phrase breaking. Today: **Japanese only**, via the BudouX port in Chromium. Korean and Chinese planned.

**Browser support (2026-04).**
- `normal`, `keep-all`, `break-all`: Baseline since July 2015 — all engines.
- `auto-phrase`: **Chrome 119** (2023-10), **Edge 119** (2023-11), **Opera 105**, **Samsung Internet 25**. **Firefox, Safari: unshipped through 152 / 26.5.**

**Gotchas.**
- `word-break: break-all` kills hyphens even when `hyphens: auto` is set.
- `auto-phrase` today is silent-no-op for non-Japanese content; do not expect Chinese or Korean behavior from it in 2026.
- `break-word` should be written today as `overflow-wrap: break-word`; the old form exists for compatibility with Microsoft-era stylesheets.

---

### `hyphens`, `hyphenate-character`, `hyphenate-limit-chars`

**Syntax (CSS Text 3/4)**
```
hyphens               = none | manual | auto
hyphenate-character   = auto | <string>
hyphenate-limit-chars = [ auto | <integer> ]{1,3}
```

**What they do.**
- `hyphens: none` — no break, even at soft hyphen.
- `hyphens: manual` (initial) — break only at `&shy;` (U+00AD) or U+2010.
- `hyphens: auto` — algorithmic hyphenation using the UA's dictionary for the `lang` attribute.
- `hyphenate-character` — the glyph or string rendered at the break (default: locale-dependent hyphen).
- `hyphenate-limit-chars` — three integers: minimum word length, minimum chars before break, minimum chars after break. `auto` defers to the UA.

**Browser support (2026-04).**
- `hyphens`: Baseline **September 2023** (all engines).
- `hyphenate-character`: Baseline **September 2023** (all engines, ~97% global usage).
- `hyphenate-limit-chars`: **Chrome 109** (2023-01), **Edge 109**, **Firefox 137** (2025-04). **Safari: unshipped through 26.5.**

**Gotchas.**
- **`hyphens: auto` silently fails without a `lang` attribute** on the containing element (or `:root`). Always set `<html lang="en">` etc.
- The UA dictionary for a given `lang` varies by OS/browser. Same HTML can hyphenate differently on Safari macOS vs Chrome Linux.
- `hyphens: auto` is overridden by `word-break: break-all`, which suppresses the hyphen glyph.
- `hyphenate-character: "="` is used in German academic typesetting; beware breaking visually-obvious single-character words.
- `hyphenate-limit-chars: 6 3 3` is a conventional minimum; authoring `6 2 2` looks noisy in Latin.
- Safari supports `-webkit-hyphenate-character` legacy prefix but not `hyphenate-limit-chars`; for Safari's missing feature use conservative content (soft hyphens) or accept wider ragging.

---

### `font-size-adjust`

**Syntax (CSS Fonts 5)**
```
font-size-adjust = none
                 | [ ex-height | cap-height | ch-width | ic-width | ic-height ]?
                   [ from-font | <number [0,∞]> ]
```

**What it does.** When the primary font isn't loaded and a fallback is used, scales the fallback so a chosen metric matches a target aspect ratio. The one-value form defaults the metric to `ex-height`.

Aspect ratio used = metric-height ÷ font-size.

- `ex-height` — lowercase-x height over font-size.
- `cap-height` — cap height over font-size.
- `ch-width` — advance width of "0" (U+0030) over font-size.
- `ic-width` — advance width of 水 (U+6C34) over font-size (CJK).
- `ic-height` — advance height of 水 over font-size.
- `from-font` — use the primary font's own metric as the target number.

```css
body {
  font-family: "Inter", sans-serif;
  font-size-adjust: cap-height 0.72;   /* preserve cap-height aspect */
}
```

**Browser support (2026-04).**
- Firefox: long partial history (one-value form since Firefox 3); **full two-value + keyword support: Firefox 118** (2023-09).
- **Safari 17** (2023-09): full support including two-value syntax.
- **Chrome 127** (2024-07), **Edge 127**: full two-value syntax. Baseline 2024.

**Gotchas.**
- One-value form (`font-size-adjust: 0.5`) behaves as `ex-height 0.5`. Don't confuse with `cap-height 0.5`.
- Requires *both* fonts in the cascade to have the metric you're equalizing — `ic-width` is meaningless if the fallback has no CJK coverage.
- For swap-free fallback alignment, `size-adjust` / `ascent-override` in `@font-face` (see `./metric-overrides.md`) is a more precise tool because it acts at the face level. `font-size-adjust` is a paragraph-level pressure valve.
- `from-font` is the most-correct choice most of the time; `from-font` + specific metric = "preserve this ratio from the primary font."

---

### `font-synthesis`, `font-synthesis-weight`, `font-synthesis-style`, `font-synthesis-small-caps`, `font-synthesis-position`

**Syntax (CSS Fonts 4)**
```
font-synthesis             = none | [ weight || style || small-caps || position ]
font-synthesis-weight      = auto | none
font-synthesis-style       = auto | none | oblique-only
font-synthesis-small-caps  = auto | none
font-synthesis-position    = auto | none        (* experimental *)
```

**What it does.** Controls whether the UA is allowed to synthesize bold (by thickening strokes), italic (by skewing), small caps (by shrinking caps), and superscript/subscript positioning when the specified face lacks those styles.

**Browser support (2026-04).**
- Shorthand `font-synthesis`: Baseline **January 2022** (all engines). Earlier shorthand values `weight`/`style` shipped in Firefox first, ~2019.
- `font-synthesis-small-caps`: all engines shipped by 2022.
- `font-synthesis-position`: **experimental** — Chromium enabled by default since Chrome 118 (2023-09); Firefox and Safari have partial/flagged support.
- `font-synthesis-style: oblique-only`: specced L4; implementation varies — treat as experimental.

**Gotchas.**
- Synthesized bold on Arabic, Hebrew, Indic scripts is typographic malpractice — it mangles connective rules and mark placement. Use `*:lang(ar), *:lang(he) { font-synthesis: none; }` or rely on proper face weights.
- Synthesized italic on CJK tilts the glyph box and does not produce a genuine italic (CJK doesn't have italic conventions). Always `font-synthesis-style: none` in CJK contexts.
- `font-synthesis: none` disables *all four* at once. To disable only style, use the longhand.
- On variable fonts with `wght` and `ital`/`slnt` axes, `font-synthesis` only matters if no matching instance exists along the axis — typically synthesis is skipped when variable axes can produce the requested style.

---

### `letter-spacing` vs `word-spacing` vs "text-spacing"

**Syntax (CSS Text 3)**
```
letter-spacing = normal | <length-percentage>
word-spacing   = normal | <length-percentage>
```

**There is no `text-spacing` property.** The closely named properties in CSS Text 4 are `text-spacing-trim` (CJK punctuation; covered above) and the drafted but unshipped `text-spacing` shorthand (do not rely on it).

**What they do.**
- `letter-spacing`: adds to the tracking between every character. Positive = looser; negative = tighter.
- `word-spacing`: adds to the space glyph's width; widens/narrows the gap between words.
- Percentages are resolved against the advance width of the affected glyph (L3) / `font-size` in older drafts — test across engines.

**Browser support (2026-04).** Baseline since **July 2015** across all engines.

**Gotchas.**
- **Never apply `letter-spacing` to Arabic, Farsi, Urdu, Hindi, Mongolian, or other connected/shaped scripts.** It breaks connecting contextual forms. Use `*:lang(ar) { letter-spacing: normal !important; }`.
- On variable fonts with a true tracking axis (rare) or on proper opticals (`opsz`), prefer axis settings or optical-size matching to global `letter-spacing`.
- `letter-spacing: normal` permits the UA to adjust tracking during justification; any explicit length freezes tracking and can suppress justification quality.
- `letter-spacing` disables many OpenType ligatures in Blink and WebKit — use `font-variant-ligatures: no-common-ligatures` explicitly when intentional, otherwise expect fi/fl/ffi to break.
- Use `em`-based `letter-spacing`, not `px`, so tracking scales with font-size.
- `word-spacing` acts on the space glyph, so it has no effect on CJK (which doesn't use word spaces).

---

### `text-indent` — `each-line` and `hanging` keywords

**Syntax (CSS Text 3)**
```
text-indent = <length-percentage> && hanging? && each-line?
```

**What it does.**
- Base `<length-percentage>` indents the first line.
- `each-line`: indent is re-applied after every forced break (`<br>` or block boundary), not after soft wraps.
- `hanging`: inverts which lines are indented — every line *except* the first gets the indent (useful for outline numbering, bibliographies).
- Combining: `text-indent: 2em hanging each-line` → all lines except the post-break first get 2em.

**Browser support (2026-04).**
- `<length-percentage>` alone: Baseline since 2015.
- `hanging` and `each-line` keywords:
  - **Safari 15** (2021-09): shipped.
  - **Firefox 121** (2023-12): shipped.
  - **Chrome 146 / Edge 146** (2025-03): shipped.
- Global usage ~74% (caniuse). **All three engines ship as of 2026-04.**

**Gotchas.**
- `hanging` differs from negative `text-indent`: `-3%` outdents only the first line; `hanging` keeps the first line flush and indents all the rest.
- Percentages resolve against the containing block's inline size (content area only, not padding+border).
- Pre-Chrome-146 codebases sometimes simulated hanging indents with negative margin + padding-left; that technique still works as a fallback.

---

### `overflow-wrap` vs `word-break` (the four-way showdown)

**Syntax**
```
overflow-wrap = normal | break-word | anywhere
word-break    = normal | keep-all | break-all | break-word | auto-phrase | manual
```

**Decision table.**

| Goal | Best value | Why |
|---|---|---|
| Long URLs / code-ish strings break at container edge only when they'd overflow | `overflow-wrap: break-word` | Doesn't change `min-content`, layout stable |
| Same goal but want `min-content` to reflect the break | `overflow-wrap: anywhere` | Soft-wrap opportunities count in intrinsic sizing |
| CJK arbitrary break between any two characters | `word-break: break-all` | The classic CJK rule |
| Keep CJK words together, Latin normal | `word-break: keep-all` | CJK-specific |
| Japanese phrase-level breaking | `word-break: auto-phrase` | Chromium-only in 2026 |

**Browser support (2026-04).**
- `overflow-wrap: break-word`: Baseline **October 2018**.
- `overflow-wrap: anywhere`: Chromium ≥ 80; Firefox ≥ 65; **Safari: partial through 26.x** — community reports that Safari honors `anywhere` for breaking but treats it like `break-word` for intrinsic-size computation. Prefer `break-word` if you need broad min-content parity.
- `word-break: break-all` / `keep-all`: Baseline 2015.

**Gotchas.**
- `word-break: break-word` is deprecated. Use `overflow-wrap: break-word`.
- `word-break: break-all` aggressively breaks even when whitespace breaks would have sufficed; do not use as a lazy overflow fix on non-CJK content.
- `overflow-wrap: anywhere` is genuinely different from `break-word` only when the layout reads `min-content` — grids, flex with `min-width: 0`, and inline-size queries are the common surfaces where the difference bites.

---

### `font-variant` (shorthand) and the longhand family

**Shorthand syntax (CSS Fonts 4)**
```
font-variant = normal | none
             | [ <'font-variant-caps'>
                 || <'font-variant-numeric'>
                 || <'font-variant-ligatures'>
                 || <'font-variant-east-asian'>
                 || <'font-variant-position'>
                 || <'font-variant-alternates'>
                 || <'font-variant-emoji'>
               ]
```

Use the longhands in production — the shorthand is hard to read and can be clobbered by later declarations.

#### `font-variant-numeric`
```
font-variant-numeric =
  normal
  | [ ordinal || slashed-zero
      || <numeric-figure-values>         /* lining-nums | oldstyle-nums */
      || <numeric-spacing-values>        /* proportional-nums | tabular-nums */
      || <numeric-fraction-values>       /* diagonal-fractions | stacked-fractions */
    ]
```
Maps to OpenType tags: `lnum`, `onum`, `pnum`, `tnum`, `frac`, `afrc`, `ordn`, `zero`.
Baseline **January 2020** (all engines).

#### `font-variant-caps`
```
font-variant-caps = normal | small-caps | all-small-caps | petite-caps
                  | all-petite-caps | unicase | titling-caps
```
Maps to `smcp`, `c2sc`, `pcap`, `c2pc`, `unic`, `titl`. Baseline **January 2020**.

#### `font-variant-ligatures`
```
font-variant-ligatures =
  normal | none
  | [ common-ligatures | no-common-ligatures ]           /* liga, clig */
    || [ discretionary-ligatures | no-discretionary-ligatures ]  /* dlig */
    || [ historical-ligatures | no-historical-ligatures ]        /* hlig */
    || [ contextual | no-contextual ]                     /* calt */
```
Baseline **January 2020**.

#### `font-variant-east-asian`
```
font-variant-east-asian =
  normal
  | [ <east-asian-variant>     /* jis78 jis83 jis90 jis04 simplified traditional */
      || <east-asian-width>    /* full-width | proportional-width */
      || ruby ]
```
Maps to `jp78` `jp83` `jp90` `jp04` `smpl` `trad` `fwid` `pwid` `ruby`. Baseline **January 2020**.

#### `font-variant-position`
```
font-variant-position = normal | sub | super
```
Maps to `subs` / `sups`. Baseline **September 2023** (all engines).

#### `font-variant-alternates`
```
font-variant-alternates =
  normal
  | [ stylistic( <feature-value-name> )
      || historical-forms                    /* hist */
      || styleset( <feature-value-name># )   /* ssXX */
      || character-variant( <feature-value-name># ) /* cvXX */
      || swash( <feature-value-name> )       /* swsh, cswh */
      || ornaments( <feature-value-name> )   /* ornm */
      || annotation( <feature-value-name> )  /* nalt */
    ]
```
Paired with `@font-feature-values` block. Baseline **March 2023**:
- Firefox shipped the feature machinery as early as v34 (2014) but without named maps across cascades.
- **Chrome 113** (2023-05) shipped full support including the `@font-feature-values` alternate-name dictionary.
- Safari 9.1 shipped partial; full support aligns with the March 2023 baseline.

#### `font-variant-emoji`
```
font-variant-emoji = normal | text | emoji | unicode
```
- `text`: forces text-style glyphs (U+FE0E implied).
- `emoji`: forces emoji-style glyphs (U+FE0F implied).
- `unicode`: UA follows Unicode emoji presentation properties.

Support (2026-04):
- **Firefox 141** (2025-08) — earlier partial builds in Firefox 108–112 track an earlier draft.
- **Chrome 131 / Edge 131** (2024-11).
- **Safari: unshipped through 26.5.**
- Global usage ~74%.

**Gotchas across the `font-variant-*` family.**
- Silent no-op if the font lacks the feature. Detect via `font-feature-settings` in `@supports`? No — features aren't feature-detectable in CSS. Use known fonts.
- `font-variant-ligatures: none` disables all ligatures, including common ones — usually not what you want. Prefer `no-discretionary-ligatures` or `no-historical-ligatures` for targeted suppression.
- Applying `letter-spacing` in Blink/WebKit disables common ligatures as a side effect. Re-enable with `font-variant-ligatures: common-ligatures` (which may or may not override, depending on engine).
- `font-feature-settings` is the low-level escape hatch; when both are set, the high-level `font-variant-*` wins per spec. In practice, use `font-variant-*` for what it covers (it's standardized and future-proof) and `font-feature-settings` only for tags not expressible (`ss01`–`ss20`, `cv01`–`cv99`, `locl` if needed beyond `lang`).

---

## Feature Grouping Snapshots

### Trimming leading half-leading and descender space

| Property | Purpose | Support |
|---|---|---|
| `text-box-trim` / `text-box-edge` / `text-box` | Trim half-leading using font metrics | Chromium 133+, Safari 18.2+, Firefox unshipped |
| `leading-trim` (deprecated) | Old name for the above | **Never shipped, do not author** |
| `line-height: <unitless>` | Classic leading control (still essential) | Baseline forever |
| `@font-face` metric overrides (`ascent-override`, `descent-override`, `line-gap-override`) | Per-face metric normalization | See `./metric-overrides.md` |

Use `text-box-trim` for block-level optical centering. Use metric overrides for per-font metric normalization that holds across every consumer of that `@font-face`.

### Better line-breaking

| Property | Purpose | Best at |
|---|---|---|
| `text-wrap: balance` | Equalize line lengths | Headlines |
| `text-wrap: pretty` | Reduce orphans, better raggedness | Body copy |
| `text-wrap: stable` | Freeze earlier lines | `contenteditable` |
| `hyphens: auto` | Break long words | Justified body |
| `hyphenate-character` | Cosmetic hyphen glyph | Locale typography |
| `hyphenate-limit-chars` | Min word/edge chars | Editorial quality |
| `word-break: auto-phrase` | Phrase-aware break | Japanese (only, today) |
| `word-break: break-all` | Any-character break | CJK / fixed columns |
| `overflow-wrap: anywhere`/`break-word` | Prevent overflow of long strings | URLs, code |

### Drop caps and initial letters

| Property | Purpose | Support |
|---|---|---|
| `::first-letter` | Select the first letter for styling | Baseline since 2010 |
| `initial-letter` | Specify drop-cap geometry using font metrics | WebKit + Blink partial; **Firefox unshipped** |
| `initial-letter-align` | Alignment reference | No full implementation |
| `hanging-punctuation: first` | Quote mark adjacent to drop cap | Safari-only |

Safest stance: `::first-letter` with explicit `font-size` / `line-height` / `float: left`; use `initial-letter` as a progressive enhancement when you know you're targeting WebKit/Blink.

### Variant and numeric control

Group the `font-variant-*` longhands as one "OpenType switchboard":

```css
.tabular { font-variant-numeric: tabular-nums lining-nums; }
.oldstyle { font-variant-numeric: oldstyle-nums proportional-nums; }
.smallcaps { font-variant-caps: all-small-caps; font-synthesis-small-caps: none; }
.ligatures-off-for-monospace-code { font-variant-ligatures: no-common-ligatures no-discretionary-ligatures; }
```

Numeric, caps, ligatures, east-asian, position, alternates have all been Baseline since 2020–2023; prefer them over `font-feature-settings` unless you need `ss01`–`ss20`/`cv01`–`cv99`.

### Fallback robustness

| Property | Purpose |
|---|---|
| `font-size-adjust: cap-height 0.72` (or similar) | Keep cap-height aspect constant when the web font fails to load |
| `@font-face size-adjust / ascent-override / descent-override / line-gap-override` | Per-face metric normalization — **always prefer this when authoring `@font-face`** |
| `font-synthesis: none` | Suppress synthesized bold/italic for scripts that can't afford it |

For a robust fallback strategy, prefer `@font-face` metric overrides (see `./metric-overrides.md`) — they eliminate layout shift on swap. `font-size-adjust` is a paragraph-level safety net, not a replacement.

---

## Anti-patterns

1. **Using `text-wrap: balance` on body copy.**
   Why it fails: browsers cap the optimizer at ≤10 lines. Long runs silently fall back to `wrap`, producing inconsistent layouts across lengths. Use `pretty`.

2. **Using `letter-spacing` on Arabic, Hebrew, Devanagari, Mongolian.**
   Why it fails: these are connecting or shaped scripts. Tracking breaks ligatures, joiners, and contextual forms. Always exclude: `*:lang(ar), *:lang(he), *:lang(hi), *:lang(ur) { letter-spacing: normal !important; }`.

3. **Relying on `hyphens: auto` without `lang`.**
   Why it fails: UAs hyphenate only when the dictionary can be resolved via `lang` on the element or an ancestor. Missing `<html lang>` or section-level overrides yields no hyphens and no error.

4. **Authoring `leading-trim` expecting it to work.**
   Why it fails: the property was renamed to `text-box-trim` before any engine shipped it. No browser recognizes the old name.

5. **Expecting `text-wrap: stable` to improve render quality.**
   Why it fails: it behaves identically to `wrap` outside `contenteditable`. It's an editing-UX feature, not a typography feature.

6. **Using `word-break: break-all` to work around overflow.**
   Why it fails: breaks mid-word on all content, not just overflowing strings. `overflow-wrap: break-word` (or `anywhere`) is the targeted answer.

7. **Using `font-feature-settings` where `font-variant-*` applies.**
   Why it fails: `font-feature-settings` is not inheritable semantically across cascades the way the high-level variants are; if both are specified, engines honor `font-variant-*` and you'll debug a phantom override. Also: you lose cascade semantics for things like `-ligatures` and `-numeric`.

8. **Applying `font-synthesis: none` globally without providing the missing styles.**
   Why it fails: removes accessibility of italic/bold emphasis if the face stack doesn't include italic/bold cuts. Pair with explicit `@font-face` for every style you need, or keep synthesis on for Latin.

9. **Using `text-box: trim-both` with `cap alphabetic` on a multi-line paragraph and expecting uniform trim.**
   Why it fails: trim applies to the first and last lines only; interior leading is untouched.

10. **Using `initial-letter` as a design-critical feature in cross-browser production.**
    Why it fails: Firefox has no implementation (2026-04); Chromium/WebKit implementations are listed as partial. Always design a readable non-drop-cap fallback.

11. **Using `hanging-punctuation: last` anywhere.**
    Why it fails: no browser implements it, including Safari.

12. **Using `overflow-wrap: anywhere` assuming Safari intrinsic-size parity with Chrome.**
    Why it fails: Safari honors breaking but not always the min-content accounting. Use `break-word` if Safari intrinsic sizing matters.

13. **Writing `font-size-adjust: 0.5` and expecting cap-height parity.**
    Why it fails: one-value form defaults to `ex-height`. Use `font-size-adjust: cap-height 0.72` (or whatever metric you actually want).

14. **Mixing `text-spacing-trim` with non-CJK text thinking it will kern Latin punctuation.**
    Why it fails: the property is defined for CJK full-width punctuation. It silently does nothing to Latin.

---

## Sources

Retrieval date for all URLs: **2026-04-17**.

### W3C specifications
- [CSS Inline Layout Module Level 3](https://www.w3.org/TR/css-inline-3/) — `text-box-trim`, `text-box-edge`, `text-box`, `initial-letter`, `initial-letter-align`.
- [CSS Text Module Level 3 (Editor's Draft)](https://drafts.csswg.org/css-text-3/) — `hyphens`, `word-break`, `letter-spacing`, `word-spacing`, `overflow-wrap`, `text-indent`.
- [CSS Text Module Level 4 (Editor's Draft)](https://drafts.csswg.org/css-text-4/) — `text-wrap`, `text-wrap-mode`, `text-wrap-style`, `hyphenate-character`, `hyphenate-limit-chars`, `text-spacing-trim`, `word-break: auto-phrase`.
- [CSS Fonts Module Level 4](https://www.w3.org/TR/css-fonts-4/) — `font-synthesis`, `font-variant-*`, `font-size-adjust`.
- [CSS Fonts Module Level 5 (Editor's Draft)](https://drafts.csswg.org/css-fonts-5/) — two-value `font-size-adjust`, `font-synthesis-position`.

### MDN reference pages (browser compat tables)
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap-style
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-trim
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-edge
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-box
- https://developer.mozilla.org/en-US/docs/Web/CSS/initial-letter
- https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-spacing-trim
- https://developer.mozilla.org/en-US/docs/Web/CSS/word-break
- https://developer.mozilla.org/en-US/docs/Web/CSS/hyphens
- https://developer.mozilla.org/en-US/docs/Web/CSS/hyphenate-character
- https://developer.mozilla.org/en-US/docs/Web/CSS/hyphenate-limit-chars
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis
- https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap
- https://developer.mozilla.org/en-US/docs/Web/CSS/letter-spacing
- https://developer.mozilla.org/en-US/docs/Web/CSS/word-spacing
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-indent
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-east-asian
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-alternates
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position
- https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-emoji

### caniuse support tables
- https://caniuse.com/css-text-wrap-balance
- https://caniuse.com/mdn-css_properties_text-wrap_pretty
- https://caniuse.com/css-text-box-trim
- https://caniuse.com/css-initial-letter
- https://caniuse.com/css-hanging-punctuation
- https://caniuse.com/mdn-css_properties_text-spacing-trim
- https://caniuse.com/mdn-css_properties_word-break_auto-phrase
- https://caniuse.com/mdn-css_properties_hyphenate-limit-chars
- https://caniuse.com/mdn-css_properties_hyphenate-character
- https://caniuse.com/font-size-adjust
- https://caniuse.com/mdn-css_properties_font-variant-emoji
- https://caniuse.com/mdn-css_properties_text-indent_hanging
- https://caniuse.com/font-variant-alternates

### Engineering blogs
- https://developer.chrome.com/blog/css-text-box-trim — Chrome 133 ship post (2025-02).
- https://developer.chrome.com/blog/css-i18n-features — Chrome 119 word-break: auto-phrase (2023-11).
- https://chrome.dev/css-wrapped-2025/ — Chrome 2025 CSS shipping roundup.
- https://ishadeed.com/article/balancing-text-css/ — Ahmad Shadeed on text-wrap: balance.
- https://blog.stephaniestimac.com/posts/2023/1/css-initial-letter/ — Stephanie Stimac on initial-letter.
- https://css-tricks.com/leading-trim-the-future-of-digital-typesetting/ — Ethan Wang, original leading-trim proposal (now text-box-trim).
- https://clagnut.com/blog/2445 — Richard Rutter's Interop 2026 typography requests.
- https://css-tricks.com/interop-2026/ — Interop 2026 overview.
- https://adactio.com/journal/21027 — Jeremy Keith on hanging-punctuation's long partial support.
- https://adrianroselli.com/2024/02/techniques-to-break-words.html — Adrian Roselli on word-break / overflow-wrap pairings.
