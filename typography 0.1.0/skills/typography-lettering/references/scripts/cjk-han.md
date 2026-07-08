---
date: 2026-04-17
coverage: medium
peers:
  - ../scripts/japanese.md
  - ../scripts/hangul.md
  - ../contemporary/css-text-properties.md
  - ../contemporary/font-delivery.md
  - ../contemporary/opentype-features.md
  - ../contemporary/variable-fonts.md
primary_sources:
  - https://www.w3.org/TR/clreq/ (W3C Requirements for Chinese Text Layout, Group Note Draft 2026-03-26)
  - https://w3c.github.io/jlreq/?lang=en (W3C Requirements for Japanese Text Layout)
  - https://source.typekit.com/source-han-sans/ (Adobe Source Han project)
  - https://github.com/notofonts/noto-cjk (Google/Adobe Noto CJK)
  - https://developer.mozilla.org/en-US/docs/Web/CSS/writing-mode
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-orientation
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-spacing-trim
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt (OpenType feature spec, `palt`/`halt`/`hwid` etc.)
---

# CJK — Han (Hanzi / Kanji / Hanja) as a Shared Script

This file covers **the Han script itself** — the ideographic characters that Chinese, Japanese, and Korean all draw from — and the CJK typographic properties that are shared across those languages: fullwidth vs proportional handling, vertical text, line composition, font families that span regions, and delivery considerations.

Script-specific treatment lives in siblings: Japanese-only concerns (four-script mixing, ruby, tategaki specifics, wayō-konshō Latin-mixing) are in `../scripts/japanese.md`. Hangul (Korean syllable blocks) is in `../scripts/hangul.md`. For a Chinese-only file, see `../scripts/chinese.md` when it lands (currently this file carries shared Chinese context).

**Scope disclaimer — practitioner-medium.** This covers enough to ship CJK body text competently and ask the right questions; it is not a substitute for JLREQ/CLREQ when you hit a layout edge case, and it is not a type-designer's view of how to draw a Han glyph. Where JLREQ or CLREQ has an authoritative line, we cite it and point out.

---

## Han as a Shared Script

**One script, three (or four) linguistic traditions.** Chinese hanzi (漢字), Japanese kanji (漢字), and Korean hanja (한자 / 漢字) all refer to the same underlying set of ideographic characters, historically transmitted from China to Japan and Korea. Vietnamese historically used chữ Hán but has moved to Latin-based Quốc ngữ; historical Vietnamese corpora still need Han support.

Practically, this means a single Unicode character like `水` (water) is U+6C34 whether it appears in Mandarin, Cantonese, Japanese, or historical Korean text. But the *shape* of that character — the idealized reference form — differs slightly by region. So a font labelled "Han" must either pick a region or ship multiple region-specific glyph tables selected via `locl`.

**Where each tradition is alive today:**

| Tradition | Where it's used | Character count in common use |
|-----------|-----------------|-------------------------------|
| Simplified Chinese (简体字) | Mainland China (PRC), Singapore, Malaysia | ~3,500 (Tōngyòng Guīfàn Hànzì Biǎo is ~8,105 total) |
| Traditional Chinese (繁體字), Taiwan standard | Taiwan | ~4,800 common, ~13,000 total standard |
| Traditional Chinese, Hong Kong standard | Hong Kong, Macau | Similar count to Taiwan, different forms for some characters |
| Japanese Shinjitai (新字体) | Japan | Jōyō kanji list is 2,136; plus jinmeiyō for names |
| Korean Hanja | Korea (mostly historical, scholarly, legal, some newspapers) | 1,800 basic-education hanja; rare in modern prose |

Hanja today has minimal presence in day-to-day Korean (Hangul is the active script) but still appears in formal, legal, academic, and some newspaper contexts. See `../scripts/hangul.md` for the active Korean script.

---

## Script Variants: Why One Font Can't Cover All Four (Without `locl`)

Consider the character "direct / straight": same Unicode code point U+76F4 (直) across regions, but the stroke connections and the proportional balance differ. Taiwan's Traditional glyph leaves a micro-gap where PRC's Simplified closes it; Japan's Shinjitai form uses yet a slightly different construction. If a font ships only one glyph table, users in the other regions see shapes that read as *foreign* — not wrong, but subtly off, like a reader noticing a British `t` in an American text.

**Options for a font covering multiple regions:**

1. **Ship one glyph per character, pick a region.** Simplest. What most single-region commercial fonts do.
2. **Ship all regional variants with `locl` OpenType feature.** The reader's language tag (HTML `lang="ja"`, `lang="zh-Hans"`, `lang="zh-Hant"`, `lang="zh-Hant-HK"`, `lang="ko"`) drives `locl` substitution. This is what Noto CJK and Source Han do — each "family" is one design with region-switched glyph sets per character.
3. **Ship entirely separate regional subfamilies.** Cleaner delivery (smaller per-region downloads) at the cost of losing cross-region consistency in a single page. Noto CJK and Source Han both ship regional subfamilies as an *alternative* to the combined OTC files.

**Tag your content's `lang` attribute honestly.** Otherwise the user agent cannot pick the correct regional glyphs, and you get Japanese kanji rendering when you meant Simplified Chinese (or vice versa). This bites many multilingual sites.

```html
<html lang="ja">
  <article lang="zh-Hans">
    <blockquote lang="zh-Hant-HK">…</blockquote>
  </article>
</html>
```

---

## Unicode Blocks for Han

For subsetting strategies (see below), know the Han blocks by heart:

| Block | Range | Size | What lives here |
|-------|-------|------|-----------------|
| CJK Unified Ideographs | U+4E00–U+9FFF | ~20K | The core; 99% of everyday CJK text |
| CJK Unified Ideographs Extension A | U+3400–U+4DBF | ~6K | Rare historical characters |
| CJK Unified Ideographs Extension B | U+20000–U+2A6DF | ~42K | Very rare; scholarly, personal names |
| CJK Unified Ideographs Extension C | U+2A700–U+2B73F | ~4K | Rare; often historical |
| CJK Unified Ideographs Extensions D, E, F | U+2B740–U+2EBEF | ~15K | Rare; specialised historical |
| CJK Unified Ideographs Extension G | U+30000–U+3134F | ~5K | Added 2021; Unicode 13.0 |
| CJK Compatibility Ideographs | U+F900–U+FAFF | ~500 | Duplicate-to-canonical mappings |
| CJK Symbols & Punctuation | U+3000–U+303F | 64 | The "ideographic space" U+3000, reference mark 、(U+3001), full stop 。(U+3002), brackets, etc. |
| Hiragana | U+3040–U+309F | 96 | Japanese phonetic (see japanese.md) |
| Katakana | U+30A0–U+30FF | 96 | Japanese phonetic (see japanese.md) |
| Halfwidth and Fullwidth Forms | U+FF00–U+FFEF | 240 | Fullwidth Latin, halfwidth katakana |
| Hangul Syllables | U+AC00–U+D7AF | ~11K | Korean pre-composed syllables (see hangul.md) |

For most production CJK web typography, subsetting to **U+4E00–U+9FFF + U+3000–U+303F + halfwidth/fullwidth forms + the relevant phonetic blocks** covers >99% of day-to-day text.

---

## The Five Stroke Classes

Han characters decompose into five basic stroke classes. Traditional calligraphic and type-design pedagogy names them by Chinese terms; the same classes apply to Japanese kanji and Korean hanja construction.

| Class | Chinese | Japanese | Shape | Note |
|-------|---------|----------|-------|------|
| 橫 / 横 | héng | yoko / ō | horizontal | Nominally L→R; slight rise to the right in many styles |
| 豎 / 竖 | shù | tate | vertical | Top→bottom |
| 撇 | piě | hidari-barai | left-falling diagonal | Starts top-right, ends bottom-left with a lift |
| 捺 | nà | migi-barai | right-falling diagonal | Starts top-left, thickens as it falls to bottom-right |
| 折 | zhé | ore | turning / bent | A stroke that changes direction mid-course without lifting |

**Why the five-class decomposition matters for type design and multiplex (variable / multi-weight) fonts:** weight distribution is not uniform across stroke classes. A Han glyph at heavy weight (say `wght: 900`) does not simply thicken each stroke by the same amount — horizontals grow less than verticals (which grow less than diagonals), or the counters close up and legibility collapses. This is why CJK variable fonts are so much harder to build than Latin ones, and why Noto/Source Han variable releases (Noto Sans CJK variable, 2023 onward) are notable engineering feats. A CJK font is roughly **100× the character count of a Latin font** and each weight master has to be hand-tuned for stroke-class balance.

As a practitioner, you rarely reason about this directly — but you do feel it when a bolder weight of a CJK font looks "clogged" at small sizes. That is almost always an intentional weight master rather than interpolation drift, and it is almost always fixed by dropping one weight step.

---

## Fullwidth vs Proportional — The Most Important Shared CJK Concept

Han characters were designed — first on paper, then in metal type, now in digital UPM grids — to sit inside a **square em box**. Each character occupies one "full-width" slot. This creates a uniform grid that is itself a defining feature of CJK typography; see "Line-height and Measure" below.

The catch is what happens to *non-Han* characters that appear in Han-dominant text: punctuation, Latin letters, digits.

**Three modes of treatment:**

1. **Fullwidth (全角 / ｚｅｎｋａｋｕ).** The non-Han character is drawn to fit the full em box. Punctuation: 「」、。・ (quote brackets, tōten, kuten, middle dot). Fullwidth Latin and numerals: Ａ Ｂ Ｃ ０ １ ２ (occupy a full square).
2. **Proportional (プロポーショナル / pinyin *bǐlì*).** The character keeps its proportional, natural width — how Latin and Arabic numerals look in a Western font. A CJK font's proportional Latin glyphs are the font designer's opinion of how Latin should harmonize with Han strokes at body size.
3. **Halfwidth (半角 / ｈａｎｋａｋｕ).** The character is drawn to half the em box. Historical for halfwidth katakana ｶﾀｶﾅ (legacy from early computing where fullwidth kana could not be represented), and for some halfwidth punctuation in mixed-script contexts.

**CSS control via OpenType `font-feature-settings`:**

| Feature | Effect | When to use |
|---------|--------|-------------|
| `fwid` | Force full widths for all glyphs (including ASCII if the font has them) | Nearly never for body — too wide for Latin |
| `halt` | Alternate half widths (punctuation only) | Tighter punctuation in running text |
| `palt` | Proportional alternates (punctuation and often kana) | Most readable option in running text with mixed scripts |
| `hwid` | Half widths (glyph-width transform) | Forcing halfwidth where full is default |
| `pwid` | Proportional widths | Similar intent to `palt` but across broader glyph classes |
| `vpal` | Vertical analog of `palt` | Use in `writing-mode: vertical-*` contexts |

```css
.cjk-body {
  /* Proportional kana + punctuation, which is what most modern CJK UIs want */
  font-feature-settings: "palt" 1;
}
```

**An important spec interaction noted by OpenType:** if `kern` is activated for a CJK font, `palt` must also be activated when it exists; otherwise the font's kerning tables (which assume proportional metrics) produce wrong offsets (see Microsoft's OpenType feature spec for `palt`). Modern fonts additionally support an `apkn` feature for "already-proportional-kerning" but support is inconsistent; defaulting to `font-kerning: normal` + `font-feature-settings: "palt" 1` is the safe recipe.

**`text-spacing-trim` (CSS Text 4).** The modern replacement for hand-managing fullwidth punctuation at line starts and ends. Trims the half-em of whitespace that fullwidth punctuation carries at the line edge or adjacent to another punctuation glyph:

```css
.cjk-body {
  text-spacing-trim: space-all; /* or normal, trim-start, space-first */
}
```

Dated browser support (as of 2026-04): `space-all` and `normal` ship in Chromium-based browsers; Safari and Firefox are behind. The `trim-both`, `trim-all`, and `auto` values are not implemented in any browser. Ship it with `@supports` and a manual fallback (see Anti-patterns).

---

## Vertical Text (Tategaki in Japanese, 直排 / 豎排 in Chinese)

Historically, all three CJK languages were written **top to bottom, columns advancing right to left**. Modern usage has diverged:

- **Chinese (mainland / Simplified).** Almost entirely horizontal LTR since mid-20th-century. Vertical survives in calligraphy, formal signage, some newspaper mastheads, couplets.
- **Chinese (Taiwan, Hong Kong, traditional contexts).** More vertical usage than mainland: book spines, traditional signage, editorial callouts. Day-to-day digital is still horizontal.
- **Japanese.** Vertical remains the default for long-form fiction, poetry (tanka, haiku), traditional non-fiction, newspapers (often mixed), manga, tanzaku. Business documents and most web are horizontal. Vertical support is a real practitioner need, not a curiosity — see `../scripts/japanese.md`.
- **Korean.** Almost entirely horizontal LTR in modern use.

**CSS control:**

```css
.novel-body {
  writing-mode: vertical-rl;      /* top-to-bottom, right-to-left columns */
  /* or vertical-lr for left-to-right column advance (rare; some Mongolian, some stylistic Japanese) */
  text-orientation: mixed;         /* default — kanji/kana upright, Latin rotated 90° CW */
  /* text-orientation: upright;   — all characters upright; Latin becomes stacked */
  /* text-orientation: sideways;  — everything rotated, CJK too (rare, stylistic) */
}
```

**`text-orientation` choices in practice:**

- `mixed` is the default and correct for running text. Han characters and kana sit upright, Latin text and numerals rotate 90° clockwise (they read down the column).
- `upright` forces everything upright — useful for columns of single-digit numerals, Latin initials in vertical stacked form, and some stylistic cases.
- `sideways` rotates the entire run as if the text were horizontal and the box were turned — rarely correct; occasionally used for CJK running heads in otherwise horizontal layouts.

**Tate-chū-yoko (horizontal-within-vertical)** for multi-digit numerals, Roman words, and short runs that should not rotate character-by-character: `text-combine-upright: all`. Detailed in `../scripts/japanese.md`.

**Browser support (as of 2026-04).** `writing-mode: vertical-rl` and `text-orientation: mixed | upright` ship in all evergreen browsers (have since ~2018). `text-combine-upright: all` ships in all evergreen browsers (Firefox 48+ added layout support in 2016). Digit-range values like `text-combine-upright: digits 2` remain partially unimplemented; `all` with explicit `<span>` wrapping is the portable recipe.

**When is vertical text culturally appropriate?** Japanese fiction, poetry, traditional non-fiction, manga, signage, menus with a traditional register. Japanese business correspondence, technical documentation, and most web surfaces are horizontal. For Chinese, vertical is mostly stylistic / decorative / traditional-register in 2026; for Korean, vertical is almost always anachronistic outside calligraphy. If you are reaching for vertical because it "looks Asian," stop — it reads as a costume. Reach for it when the register (literary, traditional, ceremonial) warrants it.

---

## Line-height and Measure for CJK

**Line-height (行間 / háng jiān):** CJK body text typically wants more line-height than Latin. Rule-of-thumb ranges:

| Context | `line-height` (unitless) |
|---------|--------------------------|
| CJK body prose | 1.7 – 1.8 |
| CJK UI chrome (short strings) | 1.4 – 1.5 |
| Headlines, very large sizes | 1.2 – 1.4 |
| Mixed CJK + Latin body | 1.6 – 1.75 (trade-off — Latin prefers ~1.5) |

The reason CJK wants more: Han glyphs fill the em box more densely than Latin (which sits mostly in x-height territory), so adjacent lines need more visual breathing room to avoid a "wall of text" effect. JLREQ's recommended line-gap for standard Japanese body is roughly half the character em (~0.5em between lines), which matches a `line-height` near 1.75.

**Measure (一行あたりの字数 / hang length in characters):** CJK measure is traditionally counted in **fullwidth characters per line**. Ranges:

| Context | CJK CPL (fullwidth characters per line) |
|---------|-----------------------------------------|
| Comfortable body prose | 28 – 40 |
| Dense editorial column | 40 – 50 |
| UI chrome / caption | 14 – 24 |
| Vertical text column (novels) | 20 – 30 characters per column |

Note that this is *not* the same as Latin CPL (45–75). A fullwidth CJK character occupies roughly twice the visual width of a Latin lowercase letter at the same point size, so 30 CJK characters ≈ 60 Latin characters of visual width. Mixed CJK-Latin bodies end up in a compromise zone around 30–35 CJK characters, which is 55–70 Latin-equivalent width.

Use the `ic` unit (CSS Values 4) to set measure in fullwidth increments:

```css
.cjk-body {
  max-inline-size: 32ic; /* 32 fullwidth characters */
  line-height: 1.75;
}
```

Browser support for `ic` as of 2026-04: all evergreen browsers.

---

## Common CJK Font Families

The practitioner-level map. Distinguish carefully between **what ships with the OS** (free, no bundling needed) and **what you have to bundle or load over the network** (a webfont transaction, often a large one).

### Ships with the OS

**macOS / iOS (ships with system):**

| Family | Tradition | Style |
|--------|-----------|-------|
| PingFang SC / TC / HK | Chinese (Simplified, Traditional, HK) | Sans (neo-grotesque-adjacent) |
| Hiragino Kaku Gothic / Mincho | Japanese | Sans / Serif |
| Hiragino Sans | Japanese | Sans (unified weights) |
| Apple SD Gothic Neo | Korean | Sans |

**Windows (ships with system):**

| Family | Tradition | Style |
|--------|-----------|-------|
| Microsoft YaHei | Simplified Chinese | Sans |
| Microsoft JhengHei | Traditional Chinese | Sans |
| Yu Gothic | Japanese | Sans |
| Yu Mincho | Japanese | Serif |
| Meiryo | Japanese | Sans (ClearType-optimised) |
| MS Gothic / Mincho | Japanese | Legacy bitmap-era; avoid for new work |
| Malgun Gothic | Korean | Sans |

**Android (varies by vendor, but commonly):**

Noto Sans CJK SC/TC/JP/KR is the Google-shipped default. Third-party skins (Samsung, Xiaomi) often swap in a vendor-customised family.

### Pan-CJK open families (bundle-or-load)

- **Noto Sans CJK / Noto Serif CJK** (Google + Adobe; open source, SIL OFL). Published as four regional variants — `Noto Sans JP`, `Noto Sans SC`, `Noto Sans TC`, `Noto Sans KR`, plus `Noto Sans HK` for the Hong Kong Traditional standard. Same underlying design; region-specific glyph set. Noto Sans CJK Variable (wght axis, 100–900) shipped in 2023.
- **Source Han Sans / Source Han Serif** (Adobe + Google; open source, SIL OFL). Same project as Noto CJK — "思源" (sīyuán) is the Chinese name ("source of thought"), "源ノ角" (gen no kaku) is the Japanese, "본고딕" (bon godik) is the Korean. Released as the same font under two brand umbrellas. When you see `Source Han` on Adobe Fonts and `Noto CJK` on Google Fonts, they are substantively the same family. Source Han Sans Variable shipped in 2021.

### Other notable webfonts

- **M PLUS 1p / M PLUS 2** — Japanese sans, Jun Kobayashi, Apache licence. Very wide weight range (Thin 100 → Black 900). Modern, clean.
- **Klee One** — Japanese, Fontworks via Google Fonts. Simulates handwriting-adjacent school primer — useful for education, callouts, decorative.
- **BIZ UDPGothic / BIZ UDPMincho** — Japanese, Morisawa, distributed via Google Fonts. Universal Design (UD) family targeting legibility; ships with both sans and serif, proportional and fullwidth variants.
- **Shippori Mincho / Shippori Antique** — Japanese, traditional mincho via Google Fonts.
- **Sawarabi Gothic / Mincho** — Japanese, classical forms, Google Fonts (lower weight-axis range).
- **Kosugi / Kosugi Maru** — Japanese sans / rounded sans, Google Fonts.
- **ZCOOL KuaiLe / ZCOOL QingKe HuangYou / ZCOOL XiaoWei** — Chinese display fonts, Google Fonts.
- **LXGW WenKai** — Chinese / Japanese hybrid kaishū-style, open source, Pan-CJK. Popular for reading-oriented contexts.

For a deeper Japanese-specific taxonomy (Gothic vs Mincho vs Maru Gothic vs brush), see `../scripts/japanese.md`.

---

## File Size and Subsetting

**The scale problem.** A full CJK font covering all four regional variants and all weights is enormous. Approximate sizes for Noto CJK / Source Han as of 2024–2025:

| Packaging | Approximate size |
|-----------|------------------|
| Noto Sans CJK, all regions + all 7 weights (OTC) | ~120 MB |
| One regional subfamily (e.g. Noto Sans JP), all 7 weights | ~20–40 MB |
| One regional subfamily, one weight, WOFF2 | ~4–7 MB |
| Variable font, full region, WOFF2 | ~7–12 MB |
| Subsetted to Jōyō kanji + kana + ASCII, WOFF2 | ~600 KB – 1.5 MB |

**Subsetting is not optional for web delivery.** Nobody should ship a 7 MB font to block paint.

### Three subsetting strategies

**1. Static subset to a known character set.** Generate the font once, include only characters in your known corpus (Jōyō + Jinmeiyō kanji + kana + ASCII for Japanese; Tōngyòng Guīfàn for Chinese). Use `pyftsubset` or `fonttools` to produce the subset. Good when your content is authored (blog, marketing site) with a predictable character set.

**2. Chunked via `unicode-range`.** Split the font into multiple `@font-face` rules, each covering a Unicode range, each referencing a separate subset file. Browsers download only the chunks whose code points actually appear on the page. This is what Google Fonts does for CJK:

```css
@font-face {
  font-family: "Noto Sans JP";
  src: url("noto-sans-jp-basic.woff2") format("woff2");
  unicode-range: U+0000-00FF, U+2000-206F, U+25A0-25FF; /* ASCII + general punct */
}
@font-face {
  font-family: "Noto Sans JP";
  src: url("noto-sans-jp-kana.woff2") format("woff2");
  unicode-range: U+3000-309F, U+30A0-30FF; /* CJK punct + hiragana + katakana */
}
@font-face {
  font-family: "Noto Sans JP";
  src: url("noto-sans-jp-kanji-common.woff2") format("woff2");
  unicode-range: U+4E00-9FFF; /* CJK Unified Ideographs (the big one) */
}
/* …and further chunks for rarer blocks */
```

Google Fonts' CJK delivery splits the CJK Unified Ideographs block itself into ~100 chunks ranked by frequency, so pages with only common kanji download only the top few frequency chunks. See `../contemporary/font-delivery.md` for the general pattern.

**3. Dynamic subsetting at request time.** A server scans the incoming HTML, generates a font subset on-the-fly containing only the code points present, and serves it. Services: Glyphs, Monotype, Fontworks all offer this. Best compression; introduces a server dependency. Used widely in Japanese web typography since the early 2010s.

### The `unicode-range` anchor for everyday CJK

If you are hand-crafting a single subset file for the common case, this covers >95% of day-to-day CJK text:

```
U+0020-007E,          /* Basic Latin (minus controls) */
U+00A0-00FF,          /* Latin-1 Supplement */
U+2000-206F,          /* General Punctuation */
U+3000-303F,          /* CJK Symbols and Punctuation */
U+3040-309F,          /* Hiragana */
U+30A0-30FF,          /* Katakana */
U+4E00-9FFF,          /* CJK Unified Ideographs */
U+FF00-FFEF           /* Halfwidth and Fullwidth Forms */
```

For Traditional Chinese add the Extension A block (U+3400-4DBF) if your corpus includes rarer characters. For Korean add Hangul Syllables (U+AC00-D7AF).

---

## Kerning and Spacing

**CJK traditionally has no kerning.** Han characters are designed to sit in the em box with uniform inter-character spacing — the grid is the point. A professional CJK font does ship a `kern` table, but it is mostly exercised for *non-Han* glyph pairs (Latin-to-kana transitions, punctuation adjacencies, fullwidth bracket kerning with adjacent kana, etc.) and for proportional alternates via `palt`.

**Inter-character spacing (字間 / zì jiān / ji-kan).** Three ways to control it:

1. **`letter-spacing`** (same as Latin). Applies uniformly to all characters. Rarely wanted for CJK body — it breaks the grid — but used for display sizes.
2. **`font-feature-settings: "palt" 1`** for proportional kana / punctuation. The most common dial.
3. **`text-spacing`** (CSS Text 4, in progress). A higher-level property that wraps `text-spacing-trim` plus an `autospace` component for inter-script spacing. Browser support is immature as of 2026-04; use the individual `text-spacing-trim` for the shippable subset.

**Mixing CJK with Latin — the inter-script gap.** JLREQ and CLREQ both specify a quarter-em (¼-em, 1/4ic) of extra space between a CJK glyph and an adjacent Latin glyph or Arabic numeral. Good CJK fonts insert this automatically via GPOS rules when `palt` is off and the font's fullwidth metrics handle it; when you have turned on `palt`, you often need to insert the gap yourself or rely on `text-autospace` (poor browser support). Editorial CJK publishers hand-insert a U+200A (hair space) or a U+2009 (thin space) between scripts. On the web, the brittle pragmatic answer is a wrapped `<span lang="en">` and a small margin:

```css
[lang="ja"] :is(span[lang="en"], code, var, kbd) {
  margin-inline: 0.25em;
}
```

This is genuinely an imperfect area of CSS for CJK as of 2026. `text-autospace` (Chromium-only, experimental) is coming; until it ships broadly, the best-effort hack remains in common use.

---

## Accessibility Notes

- **Avoid letter-spacing CJK body.** It destroys the grid and reduces readability. Fine for display-size headlines.
- **Respect `prefers-reduced-motion`** just as in Latin — CJK isn't exempt.
- **Contrast ratios apply the same.** Han glyphs carry more ink per em, so in practice they hold contrast better than thin Latin at the same weight; a weight that feels right for Latin body may feel *heavy* for CJK body. Drop one weight step (e.g., 450 → 400).
- **Do not turn off `text-spacing-trim` or CJK-punctuation trimming in screen-reader contexts.** The trimming is purely visual; the underlying characters are unchanged and are read correctly.
- **For furigana / ruby accessibility:** see `../scripts/japanese.md`; `<ruby>` is read by screen readers as the base text in most configurations, with the ruby annotation skipped or read as a parenthetical depending on settings.

---

## Anti-patterns

- **Using a pan-CJK font without setting `lang`.** The font ships glyph variants for every region, but `locl` cannot fire without a language tag — so the reader gets whatever region the font declared as default (usually Japanese or Chinese, depending on which subfamily the browser picks). Always set `lang` on `<html>` and anywhere content switches.
- **Applying `letter-spacing` to CJK body.** Breaks the grid. If you want "looser" CJK, raise `line-height` or use a font with more open counters.
- **Setting `line-height: 1.5` for CJK body.** Too tight. Use 1.7–1.8 unless you have a specific design reason.
- **Measuring CJK body in `ch` or `em`.** Use `ic` (one fullwidth character). `ch` is the advance of `0` in the current font, which is Latin-scaled.
- **Bundling the full Noto Sans CJK or Source Han OTC.** 30+ MB fonts will not ship to production. Subset or use `unicode-range` chunking. See `../contemporary/font-delivery.md`.
- **Using `writing-mode: vertical-rl` for a site because it "looks Japanese" without considering register.** Vertical is correct for literary Japanese, manga, traditional signage, some editorial — not for UI chrome, technical docs, or marketing.
- **Forgetting to activate `palt` when `kern` is on in CJK fonts with proportional alternates.** Kerning tables assume proportional metrics; you get broken offsets otherwise. CSS: `font-feature-settings: "palt" 1` alongside `font-kerning: normal`.
- **Ignoring `text-spacing-trim` and letting fullwidth punctuation double-space at line starts and ends.** Until 2024–2025, the only fix was hand-tuning character-to-character. Ship `text-spacing-trim: space-all` with an `@supports` fallback.
- **Assuming one CJK font covers every locale.** A single-region font (e.g., Noto Sans JP) does NOT give you correct glyphs for `lang="zh-Hans"` content. Load the sibling (Noto Sans SC) or pick a multi-region family.
- **Synthetic bold (`font-synthesis: weight`) on CJK.** Han glyphs should never be synthetically bolded. The outline-outset algorithm creates clogged counters and broken stroke-class balance. Always ship a real weight master. `font-synthesis-weight: none` is defensible for CJK `@font-face` rules.
- **Fullwidth punctuation in Latin-dominant strings.** A Japanese comma 、 inside an otherwise-English sentence is almost never right; it reads as a typo. Use it only inside `<span lang="ja">` content (where it renders correctly) or in fully CJK contexts.
- **Forgetting to include CJK punctuation (U+3000-303F) in your subset.** A subset with just kanji + kana + Latin ASCII will render the Latin period . instead of the CJK 。 and the sentence will look wrong at the character level.

---

## Where to Read Further

- **JLREQ** — `https://w3c.github.io/jlreq/?lang=en`. Authoritative on Japanese layout rules including line composition, kinsoku shori, ruby, tate-chū-yoko, footnote placement, column advance.
- **CLREQ** — `https://www.w3.org/TR/clreq/` (Group Note Draft, 2026-03-26). Authoritative on Chinese layout, especially Simplified vs Traditional divergences and punctuation behaviour.
- **Ken Lunde, *CJKV Information Processing*** (2nd edition, O'Reilly). Still the reference on encoding, glyph repertoire, font technology for CJKV. Much predates modern variable fonts but the character-set chapters age well.
- **Adobe Source Han writeups** — https://blog.adobe.com/en/publish/2021/04/08/source-han-sans-goes-variable (variable font project notes). See also the Source Han GitHub READMEs.
- **Type designers to know:** Ryoko Nishizuka (Japanese type at Adobe, Source Han, Kozuka), Akira Kobayashi (Monotype, Neue Frutiger, Akko), Masahiko Kozuka (historical Adobe Japan), Nagata Toshimasa, Naoyuki Fujimoto. For Chinese: Li-fa Chu (朱志伟) at Monotype, Changzhi Liu (方正).
- **Professional Japanese foundries:** Morisawa (largest), Fontworks, Ryobi, Iwata, Type Project.
- **CJK web delivery:** see `../contemporary/font-delivery.md`.

---

## Sources

- W3C, *Requirements for Chinese Text Layout* (CLREQ), Group Note Draft 2026-03-26. https://www.w3.org/TR/clreq/
- W3C, *Requirements for Japanese Text Layout* (JLREQ). https://w3c.github.io/jlreq/?lang=en
- W3C, *Chinese Layout Gap Analysis*. https://www.w3.org/TR/clreq-gap/
- MDN Web Docs, `writing-mode`, `text-orientation`, `text-combine-upright`, `text-spacing-trim`, `ruby-position`, `ruby-align`, `line-break`. https://developer.mozilla.org/en-US/docs/Web/CSS/
- Microsoft, *OpenType Feature Specification*, feature tags `palt`, `halt`, `fwid`, `hwid`, `pwid`, `vpal`, `apkn`. https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt
- Adobe, *Source Han Sans* / *Source Han Serif* project pages. https://source.typekit.com/source-han-sans/ ; https://github.com/adobe-fonts/source-han-sans
- Adobe blog, *Source Han Sans goes variable* (2021-04-08). https://blog.adobe.com/en/publish/2021/04/08/source-han-sans-goes-variable
- Google / Adobe, *Noto CJK* project. https://github.com/notofonts/noto-cjk
- Can I Use, `text-spacing-trim`, `text-box-trim`, `text-combine-upright`, `ruby-align` browser-support tables. https://caniuse.com/
- Ken Lunde, *CJKV Information Processing*, 2nd ed., O'Reilly Media, 2009 (encoding and script chapters). ISBN 978-0-596-51447-1.
