---
date: 2026-04-17
coverage: medium
peers:
  - ../scripts/cjk-han.md
  - ../contemporary/css-text-properties.md
  - ../contemporary/font-delivery.md
  - ../contemporary/variable-fonts.md
  - ../contemporary/opentype-features.md
  - ../techniques/pairing.md
primary_sources:
  - https://w3c.github.io/jlreq/?lang=en (W3C Requirements for Japanese Text Layout)
  - https://github.com/w3c/jlreq-d (JLReq-d, digital-layout-specific extensions)
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/ruby
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/ruby-position
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-combine-upright
  - https://developer.mozilla.org/en-US/docs/Web/CSS/line-break
  - https://source.typekit.com/source-han-sans/
  - https://fonts.google.com/?subset=japanese (Google Fonts Japanese subset index)
---

# Japanese Typography

This file covers **Japanese-specific** typographic concerns: the four-script mixture (kanji + hiragana + katakana + romaji), ruby annotation (furigana), tategaki (vertical writing), Japanese punctuation, the Gothic / Mincho / Maru-Gothic / brush stylistic vocabulary, font families shipped by OSes vs available on the web, and the notoriously finicky practice of mixing Japanese with Latin (wayō-konshō, 和洋混植).

For **shared CJK material** — the Han script itself, fullwidth vs proportional punctuation, `writing-mode` and `text-orientation` basics, subsetting and delivery, Noto/Source Han family structure — see `../scripts/cjk-han.md`. This file does not repeat that material; it builds on it.

**Scope disclaimer — practitioner-medium.** This covers enough to set competent Japanese body and display type for production, catch most pitfalls, and ask intelligent questions of a Japanese type designer. It is not exhaustive on JLREQ, not a substitute for a native-speaker proof, and not a design-guide for drawing kana.

---

## The Four-Script Mixture

Every Japanese text mixes **two to four** scripts. A reader encounters all four in a typical sentence of current prose.

| Script | Character count | Role | Notes |
|--------|-----------------|------|-------|
| **Kanji** (漢字) | ~2,100 in Jōyō; thousands available | Content words — nouns, verb stems, adjective stems, names. Conveys meaning densely. | Borrowed from Chinese; see `../scripts/cjk-han.md` for shared-Han mechanics. |
| **Hiragana** (ひらがな) | 46 basic + diacritics | Grammatical particles, verb endings, native words without kanji, furigana annotation. Flowing, curved forms. | Derived from cursive Chinese. Used for words the reader should parse by sound. |
| **Katakana** (カタカナ) | 46 basic + diacritics | Loanwords (especially Western — コンピュータ "computer"), foreign names, onomatopoeia, emphasis, scientific/technical terms. Angular forms. | Derived from fragments of Chinese characters. |
| **Romaji** (ローマ字) | 26 + diacritics | Latin transliteration; acronyms (TV, DVD, NASA); some proper nouns; URLs and email; branding. | Always Latin script; handling depends on whether the Japanese font supplies Latin glyphs or you pair a Latin font. |

**Example sentence with all four:**

> **東京** の **カフェ** で **Wi-Fi** を **使**って **メール** を **書**いた。
>
> tōkyō no kafe de wai-fai o tsukatte mēru o kaita
>
> ("I used Wi-Fi at a Tokyo cafe and wrote an email.")

Kanji: 東京, 使, 書. Hiragana: の, で, を, って, を, いた. Katakana: カフェ, メール. Romaji: Wi-Fi.

The way these four scripts shape together determines whether a page of Japanese looks professional, amateur, or foreign-eyed. Type designers tune kana to harmonize with kanji in stroke weight, proportion, and counter shape; Latin glyphs inside a Japanese font are an opinion of how Latin should look *next to* kanji. This is the entry point for the wayō-konshō problem below.

### Hiragana vs Katakana — the shape vocabulary

- **Hiragana** forms are **curved, flowing, based on cursive brush**. They feel soft, native, lyrical. A Japanese novel's voice is carried largely by hiragana prose with kanji for content words.
- **Katakana** forms are **angular, segmented, derived from character fragments**. They feel modern, foreign, technical, loud. A word set in katakana reads — all else equal — as either a loanword, emphasis (like italic in English), or a technical register.

A type designer's hiragana and katakana are typically drawn as a matched set per family, but they have distinct character — reading a page of kana-only text, you can feel which script is doing the work.

### Diacritics

- **Dakuten** `゛` (U+3099, combining; or U+309B standalone) — turns a voiceless kana into voiced (か → が, ka → ga).
- **Handakuten** `゜` (U+309A combining; U+309C standalone) — turns the `h`-row into `p`-row (は → ぱ, ha → pa).
- **Chōonpu** `ー` (U+30FC) — long-vowel mark. Nearly always used with katakana (コーヒー kōhī, "coffee"). Hiragana long vowels are usually written by repeating the vowel kana (おおきい, ōkii).

Font quality shows in dakuten positioning — the two dots should sit at a consistent upper-right distance from the kana base, scale with the kana's x-height-like measure, and not collide with the stroke above. Cheap fonts put dakuten at an awkward offset.

---

## Ruby (Furigana / Yomigana) — Phonetic Annotation

**Ruby** is the general term for small annotation text placed alongside a base — above for horizontal text, to the right for vertical text. In Japanese contexts it is most often called **furigana** when used to give readings of kanji. "Yomigana" is a synonym.

### HTML structure

```html
<p>
  <ruby>
    日本<rp>(</rp><rt>にほん</rt><rp>)</rp>
  </ruby>
  の
  <ruby>
    文化<rp>(</rp><rt>ぶんか</rt><rp>)</rp>
  </ruby>
</p>
```

- `<ruby>` wraps a base + annotation pair.
- `<rt>` (ruby text) holds the annotation.
- `<rp>` (ruby parenthesis) provides fallback parentheses for user agents that do not render ruby — so content still reads as "日本(にほん)" in a plaintext reader.
- `<rb>` (ruby base) is historical; the HTML spec has phased it out — the base is inferred from content before `<rt>`.

### Multi-character base with per-character annotation

For kanji compounds where each character gets its own reading (common in educational contexts):

```html
<ruby>
  日<rt>に</rt>本<rt>ほん</rt>語<rt>ご</rt>
</ruby>
```

Many user agents render per-character ruby by segmenting the base and placing each `<rt>` above its segment. Safari, Chromium, and Firefox all support this as of 2026. `ruby-align` controls how a multi-character `<rt>` aligns over a multi-character base.

### CSS surface

```css
ruby {
  ruby-position: over;       /* above the base in horizontal; right in vertical-rl */
  /* ruby-position: under;  below the base */
  /* ruby-position: alternate; alternate over/under per line */
  ruby-align: space-around;   /* space-around | space-between | start | center */
}
rt {
  font-size: 0.5em;           /* typical ~50% of base size */
  line-height: 1;             /* prevent rt from affecting base line-height */
}
```

**Ruby sizing.** JLREQ's default for Japanese ruby is **half the base size** — `rt { font-size: 0.5em; }`. This is near-universal in Japanese publishing. At display sizes, `rt` can go as small as 0.4em; in children's content or kanji-learning contexts, sometimes as large as 0.6em. Too small below ~9px actual px renders becomes unreadable; always budget `base * 0.5 ≥ 11px` for body contexts.

### Browser support (as of 2026-04)

- `<ruby>`, `<rt>`, `<rp>` — universal, have been since the late 2010s.
- `ruby-position: over | under` — universal.
- `ruby-position: alternate` — all evergreen browsers (Chromium added 2023; Safari 17+).
- `ruby-position: inter-character` — for Traditional Chinese zhuyin; mixed implementations, prefer to rely on layout-native support rather than CSS override.
- `ruby-align` — Chromium 128+, Firefox, Safari; `space-around` is the portable default.
- Line-breakable `<ruby>` — ruby now wraps across lines correctly in modern Chromium (2024+), Firefox, Safari.

### When to use ruby

- **Children's content / kanji-learning contexts.** Every kanji annotated. Default of school textbooks, manga for younger readers.
- **Unusual readings, personal names.** A name like 陽菜 can read *Hina* or *Haruna* or *Yōna* — furigana disambiguates.
- **Literary or classical texts** where an uncommon kanji reading is meant.
- **Rarely, for decorative effect** (stylised ruby, annotations that differ from literal reading — called *gikun* or "creative furigana," common in manga and pop lyrics).

Business documents, news, adult prose generally do **not** use furigana except on names and rare kanji. Over-annotation reads as condescension.

### Accessibility note

Screen readers handle ruby variably. VoiceOver (macOS/iOS) and JAWS typically read the base text and skip the `<rt>`, which is usually correct for users reading by ear. Some configurations read `<rt>` as a parenthetical. `<rp>` content is generally skipped when ruby renders natively. If your content critically depends on the annotation being spoken, test with target assistive technologies.

---

## Tategaki (Vertical Writing)

For the CSS fundamentals — `writing-mode: vertical-rl`, `text-orientation`, browser support — see `../scripts/cjk-han.md`. This section covers Japanese-specific tategaki practices that go beyond the shared CJK mechanics.

### Where vertical is default in Japanese

- **Long-form fiction and literary non-fiction.** Novels, short-story collections, literary essays are almost universally tategaki in print.
- **Poetry** (tanka 短歌, haiku 俳句, modern shi 詩).
- **Traditional signage** — shop curtains (noren), shrine boards, restaurant menus with a traditional register.
- **Manga.** Speech balloons are typically tategaki, though modern manga uses horizontal where appropriate.
- **Tanzaku** 短冊 (the vertical poem strips used at Tanabata and in calligraphy).
- **Newspapers.** Usually mixed — headlines often vertical, body and some features horizontal.

### Where horizontal is default

- Business documents, technical documentation, office correspondence.
- Almost all web UIs and apps.
- Textbooks (mostly; literary textbooks may be vertical).
- Menus in casual registers (family restaurants, fast food).
- Anything with significant Latin, numerical, or code content.

### Character-orientation behavior in vertical

In `writing-mode: vertical-rl; text-orientation: mixed`:

- **Kanji** stand upright.
- **Hiragana and katakana** stand upright.
- **Fullwidth punctuation** — 、 。 「 」 — rotates into position (Japanese fullwidth quote brackets are designed with vertical orientation in mind; they look correct either way).
- **Latin letters** rotate 90° clockwise — reader's head is tilted right to read them. Single characters stack awkwardly; multi-character Latin runs read down the column.
- **Arabic digits** rotate 90° clockwise — single digits look like fallen numerals.

### Tate-chū-yoko — horizontal-within-vertical

For short runs (2–4 digits, short Roman words) that should sit upright as a horizontal block inside the vertical flow:

```html
<p>
  昭和
  <span class="tcy">45</span>
  年生まれ
</p>
```

```css
.tcy {
  text-combine-upright: all;
}
```

This renders "45" as a horizontal two-digit block fitted into a single character's vertical slot — the standard way to set years, ages, short Western measurements, two-to-four digit numerals. Longer Latin runs (6+ characters) typically do NOT tate-chū-yoko; they either rotate with the column (`mixed` default) or the document switches context.

**Browser support.** `text-combine-upright: all` ships in all evergreen browsers (Firefox 48+, Chromium for longer, Safari). Digit-range values (`text-combine-upright: digits 2`) remain partial; use `all` with explicit `<span>` wrapping for portable code.

### The single-digit numeral case — `text-orientation: upright`

For single-digit numerals in vertical text that should stand upright (rather than rotating with `mixed`), scope `text-orientation: upright` to them:

```css
.vertical-body {
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
.vertical-body .standing-digit {
  text-orientation: upright;
}
```

Practically, `text-combine-upright: all` on single digits is usually more readable than `text-orientation: upright` because the former fits the digit into the vertical advance, while the latter leaves it as a narrow standing glyph against the surrounding kana.

### Line-breaking in vertical — `line-break`

Vertical Japanese inherits kinsoku shori (the rules forbidding certain characters from line-starts and line-ends) from the horizontal tradition; `line-break: strict | normal | loose` controls the enforcement level; see "Line Breaking" below. Tategaki bodies almost always want `strict` or `normal`.

---

## Japanese Punctuation

| Character | Unicode | Name (Japanese / translation) | Role |
|-----------|---------|-------------------------------|------|
| 、 | U+3001 | tōten (読点) / Japanese comma | Clause-separator; visually a lower-left weighted small stroke |
| 。 | U+3002 | kuten (句点) / Japanese full stop | Sentence-terminator; a small open or filled circle |
| 「 」 | U+300C, U+300D | kagi kakko / corner brackets | Primary quotation marks |
| 『 』 | U+300E, U+300F | nijū kagi / double corner brackets | Nested or title-emphasising quotation |
| （ ） | U+FF08, U+FF09 | fullwidth parentheses | Parenthetical, at full width |
| ・ | U+30FB | nakaguro / middle dot | Separator for foreign-name components (ジョン・スミス), list items, emphasis |
| ー | U+30FC | chōonpu / long-vowel mark | Katakana long vowel (a horizontal stroke at mid-height) |
| 〜 | U+301C | wave dash | "From-to" (9〜17時, "from 9 to 17 o'clock"), also stylistic |
| ！ ？ | U+FF01, U+FF1F | fullwidth exclamation / question | Used in casual / emphatic / manga registers — traditional Japanese does not use these |
| ‥ ／ … | U+2025, U+2026 | two-dot leader / horizontal ellipsis | Vertical three-dot ellipsis ︙ also exists in vertical contexts |
| 々 | U+3005 | noma / kanji iteration mark | Repeats the preceding kanji (時々, tokidoki, "sometimes") |

**Horizontal vs vertical forms.** Some Japanese punctuation has a canonically different visual form in vertical contexts — 「 」 become rotated appropriately, the ellipsis stacks vertically. OpenType's `vert` feature (or the browser's shaping with `writing-mode: vertical-*`) handles this automatically in well-made fonts.

**CJK punctuation and the line-edge trimming problem** (see `../scripts/cjk-han.md`'s section on `text-spacing-trim`): fullwidth punctuation carries half-em whitespace by design, which visually appears as awkward double-spacing at line edges and between two adjacent punctuations. `text-spacing-trim: space-all` is the modern solution; as of 2026-04, Chromium ships; Safari and Firefox are behind.

**Avoid mixing Japanese and Latin punctuation within a single clause.** A sentence like "東京 で、Wi-Fi を使った." mixes a Japanese comma with a Latin period — set the whole sentence consistently. If the content is Japanese, use 。 not `.`.

---

## Font Families for Japanese

### What ships with OSes

**macOS / iOS (installed default):**

| Family | Style | Note |
|--------|-------|------|
| Hiragino Kaku Gothic ProN | Sans | macOS default Japanese sans for UI and body. Excellent legibility. |
| Hiragino Maru Gothic ProN | Maru Gothic | Rounded-terminal sans — friendly register |
| Hiragino Mincho ProN | Serif | Traditional prose and editorial |
| Hiragino Sans | Unified sans | Newer variable-like family |
| Yu Gothic | Sans | Also included; Japanese-specific |
| Yu Mincho | Serif | Included; literary |

"ProN" suffix means "Professional N" — the newer, wider-character-set editions. Prefer ProN variants when available.

**Windows (installed default):**

| Family | Style | Note |
|--------|-------|------|
| Yu Gothic | Sans | Modern Windows default; Light, Regular, Medium, Bold, UI variants |
| Yu Mincho | Serif | Modern default serif |
| Meiryo | Sans | ClearType-optimised; widely used on Windows Vista-era → modern; better at small sizes than Yu Gothic historically |
| MS Gothic / MS PGothic | Sans (legacy) | Bitmap-era; avoid for new work; keeps appearing because of legacy software |
| MS Mincho / MS PMincho | Serif (legacy) | Same; avoid |

"P" prefix (MS PGothic) means proportional widths, not the default fullwidth.

**Android (system default varies):**

Noto Sans CJK JP is the Google stock. Vendor skins often substitute (Samsung's Samsung Sans, Xiaomi's Mitype, etc.) — do not rely on a specific system family.

**ChromeOS, Linux:**

Typically ships Noto Sans CJK JP and/or IPA Gothic/Mincho.

### Web / bundle-or-load (Google Fonts, Adobe Fonts, open foundries)

**Pan-CJK (same family, regional variants):**

- **Noto Sans JP / Noto Serif JP** — the Japanese region-specific variant of the Noto CJK family. Open source (SIL OFL). Variable font available. Available via Google Fonts with `unicode-range` chunking.
- **Source Han Sans JP / Source Han Serif JP** — Adobe's branding of the same project. Available via Adobe Fonts and GitHub. Japanese name is 源ノ角ゴシック (gen no kaku goshikku) for Sans, 源ノ明朝 (gen no minchō) for Serif.

**Japanese-focused webfonts:**

- **M PLUS 1p / M PLUS 2** — Jun Kobayashi. Open, Apache license. Very wide weight range (Thin 100 to Black 900). Modern, well-loved for UI.
- **Klee One** — Fontworks. Available on Google Fonts. Simulates a primer / handwriting-adjacent style; good for children's content, callouts, decorative.
- **BIZ UDPGothic / BIZ UDPMincho** — Morisawa UD ("Universal Design") family. On Google Fonts. Targets legibility/accessibility; both proportional ("P") and fullwidth variants.
- **Shippori Mincho / Shippori Antique** — Fontworks, traditional mincho; on Google Fonts.
- **Sawarabi Gothic / Mincho** — classical Japanese, Google Fonts, limited weight axis.
- **Kosugi / Kosugi Maru** — sans / rounded sans; Google Fonts.
- **Zen Kaku Gothic New / Zen Maru Gothic / Zen Kurenaido / Zen Old Mincho / Zen Antique** — a large family of open Japanese fonts via Google Fonts (Yoshimichi Ohira). High-quality.
- **Reggae One / Yusei Magic / RocknRoll One / DotGothic16** — display and character fonts on Google Fonts.

**Adobe Fonts (subscription):**

- **Source Han Sans / Serif JP** (also open, but available via Adobe Fonts distribution).
- **Kozuka Gothic / Kozuka Mincho** — Adobe's classic Japanese family (designer: Masahiko Kozuka).
- **Ryo Gothic / Ryo Mincho / Ryo Display / Ryo Text** — Adobe's contemporary Ryo family.
- Morisawa, Fontworks, Iwata licences also available via Adobe Fonts.

**Commercial foundries (licensed):**

- **Morisawa** — largest Japanese foundry. Shuei series, A1 series, Ryumin, Shin-Go, UD Kyokasho. Expensive but industry-standard.
- **Fontworks** — Tsukushi series, Matisse, Rodin, Klee One (open via Google Fonts).
- **Type Project** — AXIS family (one of the most widely-used contemporary Japanese sans families).
- **Iwata** — government-standard, traditional; common in public documents.

---

## Historical Type-style Distinctions — Gothic vs Mincho vs Maru vs Brush

The four main Japanese type styles parallel Latin sans / serif / rounded / script, but with their own history and conventions.

### Gothic (ゴシック)

**Sans-serif in function; no calligraphic thick/thin contrast.** The default for screen, signage, UI, and most display contexts since the postwar era.

- Clean, geometric or humanist. Modern Japanese Gothic families range from very geometric (AXIS Gothic, Hiragino Sans) to humanist (Tsukushi Gothic, UD Shin Go).
- **When to use:** UI chrome, screen body, signage, modern editorial, technical docs, marketing.
- **Canon examples:** Shin Go (Morisawa), Hiragino Sans (Screen Inc / Apple), Yu Gothic, Noto Sans CJK JP, Source Han Sans JP, M PLUS.

### Mincho (明朝)

**Serif-equivalent; high-contrast strokes with triangular serif-like features (uroko 鱗 "scales").** Traditional for print body prose.

- Derived from Ming-dynasty Chinese woodblock forms (hence "Min-chō," Ming dynasty). Thin horizontals, thick verticals, small triangular features at stroke ends.
- **When to use:** literary prose (novels, essays), traditional editorial, formal print, book design. Rarer for screen body but increasingly present as screen resolutions have increased.
- **Canon examples:** Ryumin (Morisawa, the gold-standard literary Mincho), Hiragino Mincho, Yu Mincho, Kozuka Mincho, A1 Mincho (Morisawa, with a slightly softened treatment), Shippori Mincho, Noto Serif CJK JP.

### Maru Gothic (丸ゴシック)

**Rounded-terminal sans.** Softer, friendlier register than regular Gothic.

- Every stroke end is rounded. Distinct from Gothic (sharp terminals) and Mincho (uroko).
- **When to use:** children's content, friendly consumer branding, instructional signage, casual UI, maternal/warm contexts, kawaii aesthetics.
- **Canon examples:** Hiragino Maru Gothic, Zen Maru Gothic (Google Fonts), Kosugi Maru.

### Brush / Kaishotai / Gyōshotai / Sōshotai

**Calligraphic display styles.**

- **Kaishotai** (楷書体) — regular-script calligraphy, printed-feeling.
- **Gyōshotai** (行書体) — semi-cursive, flowing.
- **Sōshotai** (草書体) — fully cursive, hard to read for non-specialists. Rarely used.
- **Kantei / Edo moji** — traditional theatre / signage styles (kabuki hand).

**When to use:** very rarely for body; display, signage for traditional register, packaging (sake, tea), ceremonial documents, certificates. Never for UI.

**Canon examples:** DF Kaisho series (DynaComware), Morisawa Kaisho series, Aoyagi Kouzan Shotai (Google Fonts — decent open option).

### Antique / Old

A minor but recognisable style: "Antique" Japanese families (Shippori Antique, Zen Antique, Zen Old Mincho) emulate pre-digital letterpress mincho with slightly uneven strokes and weathering — popular for editorial / literary design seeking a specific nostalgic register.

---

## Mixing Japanese with Latin — Wayō-konshō (和洋混植)

This is the finickiest part of Japanese web typography, and the part most Western implementers underestimate. The core problem: Latin glyphs *inside* a Japanese font, and Latin glyphs from a *separate* Latin font, rarely harmonize without tuning.

### The scale mismatch

A Japanese font designer draws Latin glyphs to harmonize with kanji at body size. To achieve visual balance with a dense kanji glyph, the Japanese-font Latin is usually drawn **taller than a dedicated Latin font's x-height would suggest**, and often with **wider proportions**. When you then set the same text in a dedicated Latin font (Inter, Source Serif, Frutiger, etc.) at the same point size, the Latin looks *smaller* or *thinner* than the surrounding kanji.

### Two strategies

**Strategy 1: Use the Japanese font's built-in Latin.** Simple, unified, what most Japanese-only sites do.

```css
.ja-body {
  font-family: "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
}
```

The font's Latin is harmonious with its kanji by design. Downsides: the Latin is rarely as refined or as feature-rich (OpenType features, italic, variable axes) as a dedicated Latin family. For branding where the Latin matters — a logo, hero heading, marketing — this is often unacceptable.

**Strategy 2: Pair a Latin font with a Japanese font.** Listed first in the `font-family` stack so it claims Latin characters before the Japanese fallback does. The browser's font-matching algorithm per glyph applies.

```css
.ja-body {
  font-family: "Inter", "Noto Sans JP", sans-serif;
}
```

This works because the browser assigns each character to the first family that covers its code point — "Inter" covers Latin but not kanji, so Latin uses Inter and kanji falls through to Noto Sans JP. But now you face the **scale mismatch** head-on: Inter's x-height at 16px will not match Noto Sans JP's visual weight. Tune with `font-size-adjust`:

```css
.ja-body {
  font-family: "Inter", "Noto Sans JP", sans-serif;
  font-size-adjust: 0.5 from-font;   /* or an explicit ratio */
}
```

`font-size-adjust` lets you specify a target x-height ratio, and the browser scales the first-loaded font to match the fallback's. For Latin + Japanese pairing, experimentally tune — 0.50 to 0.54 is the typical range for Latin sans paired with Japanese sans. Ship with `@supports (font-size-adjust: 0.5)` and a sensible fallback.

### Metric overrides

For more surgical control, `@font-face`-level metric overrides (`ascent-override`, `descent-override`, `size-adjust`) let you reshape how one family's metrics declare themselves:

```css
@font-face {
  font-family: "Inter Paired";
  src: url("/fonts/inter-var.woff2") format("woff2-variations");
  size-adjust: 108%;
  ascent-override: 92%;
  descent-override: 20%;
}
.ja-body {
  font-family: "Inter Paired", "Noto Sans JP", sans-serif;
}
```

See `../contemporary/metric-overrides.md` for the general pattern.

### Kerning and spacing between kana and Latin

JLREQ specifies a **quarter-em gap** (¼ ic) between a Japanese character and an adjacent Latin character or Arabic digit. Well-tuned Japanese fonts insert this via GPOS rules; you can hand-insert with a `<span lang="en">` wrapper plus a small inline margin (see `../scripts/cjk-han.md`'s inter-script gap recipe).

Activate `palt` for proportional kana metrics so adjacent-character spacing works correctly:

```css
.ja-body {
  font-feature-settings: "palt" 1;
  font-kerning: normal;
}
```

### Numerals — which number shape?

Japanese fonts often ship multiple numeral variants:

- **Fullwidth** ０１２ (U+FF10–FF19). Same em-box as kanji. Matches when numerals should sit in the grid (tables, dates, vertical tate-chū-yoko contexts).
- **Proportional** 012 (Latin U+0030–0039 in the Japanese font's Latin). Matches surrounding Latin body.
- **Tate-chū-yoko-ready two-digit blocks** (some fonts). Drawn to fit together as a single em.

For most Western-style body, use proportional Latin numerals. For Japanese-style tables or vertical novels, use fullwidth.

---

## Line Breaking — `line-break` and Kinsoku Shori

**Kinsoku shori** (禁則処理) is the Japanese set of line-composition rules forbidding certain characters from sitting at line starts or ends. Codified in JIS X 4051. The CSS `line-break` property controls enforcement level:

| Value | Behavior (per MDN / JIS X 4051) |
|-------|--------------------------------|
| `auto` | User agent default; broadly reasonable |
| `loose` | Least restrictive — more characters allowed at line starts/ends; typical for newspapers with tight columns |
| `normal` | Standard rules — forbids wrapping before hyphens, iteration marks, centered punctuation at line-start |
| `strict` | Most restrictive — enforces kinsoku maximally; books, literary prose |
| `anywhere` | Breaks permitted at any character (character-cluster honoured) |

```css
.ja-body { line-break: strict; }
.ja-caption { line-break: normal; }
```

### `word-break` — related but different

```css
.ja-body { word-break: normal; }
/* avoid word-break: break-all (breaks mid-word, destroys kinsoku) */
/* avoid word-break: keep-all (prevents CJK wrapping, gives horizontal overflow) */
```

Japanese wraps at character boundaries by default — this is the correct behaviour, do not interfere. `word-break: break-all` forces mid-word Latin breaks (occasionally wanted; usually wrong). `word-break: keep-all` prevents CJK from wrapping at all (almost never wanted; produces overflow).

### Hanging punctuation (ぶら下がり / burasagari)

Japanese publishing traditionally allows line-ending full stops and commas to "hang" outside the text box rather than creating ragged indentation. The CSS `hanging-punctuation` property:

```css
.ja-body {
  hanging-punctuation: allow-end;
}
```

Browser support for `hanging-punctuation` is in Safari; Chromium has been "under consideration" for years; Firefox partial. Ship with `@supports` and acceptable degradation.

---

## Web / CSS Gotchas

### Variable fonts for Japanese are real but young

- **Source Han Sans Variable** shipped in 2021, wght axis 250–900.
- **Noto Sans CJK Variable** shipped with seven-weight wght axis.
- **BIZ UDPGothic Variable** available.
- Many Japanese webfonts remain static-only (multiple weight files); check before assuming a `wght` axis.

When a variable axis exists, the file-size benefit is large — a single CJK variable font is often 30–50% of the total static-family size.

### Font delivery is bandwidth-critical

See `../contemporary/font-delivery.md` and `../scripts/cjk-han.md`'s subsetting section. Never ship a full Japanese font unsubsetted.

Google Fonts' Japanese delivery uses fine-grained `unicode-range` chunking — the full Noto Sans JP is split into ~100+ chunks, loading only those covering code points on the page. For a marketing site with short text, this can mean a 40-50 KB actual font download instead of 7 MB.

### Browser shaping is uniformly HarfBuzz

All evergreen browsers use HarfBuzz for CJK shaping — no cross-browser shaping drift in practice. The variance is at the property-support level (`text-spacing-trim`, `text-autospace`, `ruby-align`, metric overrides), not at the character-rendering level.

### `font-display` choice matters more for Japanese

Japanese fonts are larger than Latin fonts; a FOIT (flash of invisible text) with `font-display: block` can be painfully long. `font-display: swap` (paint with fallback immediately, swap in when ready) is usually correct for Japanese webfonts — users read the fallback while the real font streams in.

### Synthetic bold destroys kanji

CJK glyphs should never be `font-synthesis: weight` bolded. Add `font-synthesis-weight: none` to `@font-face` rules for CJK families, OR rely on the browser's "real master exists" heuristic. Synthetic italic is also wrong for kanji — Japanese fonts do not traditionally have italic (italic is a Latin concept). If you apply `italic` to a Japanese font with no italic master, the browser's synthetic oblique slants the kanji, which looks broken.

```css
@font-face {
  font-family: "Noto Sans JP";
  src: url(…) format("woff2");
  font-synthesis-weight: none;
  font-synthesis-style: none;
}
```

### `lang="ja"` is not optional

Without it, the browser cannot:
- Pick Japanese regional glyph variants via `locl` (kanji will render in whatever the font declared as default).
- Apply Japanese-specific line-break rules.
- Select Japanese fonts in the `system-ui` / generic-family stack.
- Speak the content correctly in text-to-speech.

---

## Anti-patterns

- **Setting Japanese body without `lang="ja"` on `<html>` or the content root.** Breaks `locl`, line-break, and screen-reader locale.
- **Using `word-break: keep-all` on Japanese body.** Prevents CJK wrapping — get horizontal overflow. The default wraps correctly.
- **Using `word-break: break-all` globally.** Breaks inside Latin words and ignores kinsoku. Almost always wrong.
- **Applying `letter-spacing` to Japanese body.** Destroys the fullwidth grid. Leave to `palt` and `text-spacing-trim`.
- **Setting `line-height: 1.5` or smaller for Japanese body.** Too tight — Japanese body wants 1.7–1.85. See `../scripts/cjk-han.md` on line-height.
- **Pairing a Latin font with a Japanese font without tuning `font-size-adjust` or metric overrides.** The Latin will look undersized or oversized compared to the kanji.
- **Using `text-orientation: sideways` for body vertical.** Stylistic / rare; the correct default is `mixed`. `upright` for single-digit numeral emphasis, `mixed` otherwise.
- **Skipping `<rp>` fallback parentheses in `<ruby>` markup.** Accessibility and plaintext degradation both suffer.
- **Furigana below ~11px rendered size.** Base × 0.5 must stay above accessible floor. Either raise the base or drop the furigana.
- **Using vertical text for UI chrome.** Vertical is for literary prose, manga, ceremony, signage. UIs read horizontal even in Japan.
- **Bundling the full Source Han Sans or Noto Sans CJK without subsetting.** 30+ MB fonts will not ship.
- **Using MS Gothic or MS Mincho in new designs.** These are bitmap-era fallbacks that keep appearing because Windows still includes them. Specify modern families (Yu Gothic, Meiryo, or webfont) explicitly and let the cascade fall back from there.
- **Mixing Japanese and Latin punctuation in the same sentence.** If the sentence is Japanese, punctuation should be Japanese (。、「」). If Latin, Latin (. , "").
- **Assuming Japanese text needs italic emphasis.** Emphasis in Japanese uses katakana (for loanwords / technical terms), bold weight, or wakiten (boten) — small dots placed next to each character. Italicising kanji or kana via synthetic oblique looks broken.
- **Enabling `font-synthesis: weight` for Japanese.** Destroys kanji outlines. Always ship a real weight master or fall back cleanly.
- **Setting Japanese headlines at `font-weight: 300` or lighter and small sizes.** Kanji at light weight and small size fail legibility fast. Medium (500) or Regular (400) is the floor for body; 700 for strong emphasis.
- **Assuming `prefers-color-scheme: dark` behaves the same.** Japanese body in dark mode often wants a *lighter* weight because kanji are ink-dense (see `../science/legibility-vs-readability.md` for the general principle). Drop one weight step under dark backgrounds.

---

## Where to Read Further

- **JLREQ — W3C Requirements for Japanese Text Layout.** Authoritative on line composition, kinsoku shori, ruby, tate-chū-yoko, footnote placement, vertical text. Written bilingually (English + Japanese). https://w3c.github.io/jlreq/?lang=en
- **JLReq-d — Requirements for Japanese Digital Text Layout.** The digital-era follow-up, targeting web-specific concerns. https://github.com/w3c/jlreq-d
- **The Type Project blog** — accessible writing on contemporary Japanese type.
- **Morisawa's typography blog.** In Japanese; translate; best contemporary type-industry perspective.
- **Fontworks Journal** for Fontworks family discussions.
- **Gridded — Robin Rendle's newsletter** occasionally covers Japanese typography from a practitioner angle.
- **Type designers to know:** Ryoko Nishizuka (Adobe, Source Han), Akira Kobayashi (Monotype, Neue Frutiger, FF Clifford, Akko, Zapfino Forte), Kazui Hatono (Type Project, AXIS), Masahiko Kozuka (Adobe Japan, classic), Ryobi Imaging's in-house designers.
- **Foundries:** Morisawa (largest; Shuei, A1, Ryumin, Shin Go, UD Kyokasho), Fontworks, Type Project (AXIS), Iwata, DynaComware, Nihon Typography.
- **For wayō-konshō practice:** search for "和欧混植" (wa-ō-konshō) in Japanese type-industry writing; conversations at Morisawa and Monotype JP regularly cover this.

---

## Sources

- W3C, *Requirements for Japanese Text Layout* (JLREQ). https://w3c.github.io/jlreq/?lang=en
- W3C, *Requirements for Japanese Digital Text Layout* (JLReq-d). https://github.com/w3c/jlreq-d
- MDN Web Docs, `<ruby>`, `<rt>`, `<rp>`, `ruby-position`, `ruby-align`, `text-combine-upright`, `line-break`, `word-break`, `writing-mode`, `text-orientation`, `font-size-adjust`, `hanging-punctuation`. https://developer.mozilla.org/en-US/docs/Web/
- Chrome for Developers blog, *Line-breakable `<ruby>` and CSS `ruby-align` property*. https://developer.chrome.com/blog/line-breakable-ruby
- Adobe, *Source Han Sans* / *Source Han Serif* project pages. https://source.typekit.com/source-han-sans/ ; https://github.com/adobe-fonts/source-han-sans
- Adobe blog, *Source Han Sans goes variable* (2021-04-08). https://blog.adobe.com/en/publish/2021/04/08/source-han-sans-goes-variable
- Google Fonts, Japanese subset index and delivery strategy. https://fonts.google.com/?subset=japanese
- Google / Adobe, Noto CJK project. https://github.com/notofonts/noto-cjk
- Can I Use, `ruby-align`, `ruby-position: alternate`, `text-combine-upright`, `text-spacing-trim`, `hanging-punctuation` browser-support tables. https://caniuse.com/
- JIS X 4051, Japanese Industrial Standard for line composition (referenced via JLREQ).
- Ken Lunde, *CJKV Information Processing*, 2nd ed., O'Reilly Media, 2009. ISBN 978-0-596-51447-1.
