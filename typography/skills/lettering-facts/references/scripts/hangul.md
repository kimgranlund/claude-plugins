---
date: 2026-04-18
coverage: light
peers:
  - ./cjk-han.md
  - ./japanese.md
  - ./latin.md
  - ../metrics/metric-compatibility.md
  - ../contemporary/css-text-properties.md
primary_sources:
  - https://www.unicode.org/charts/PDF/UAC00.pdf
  - https://www.unicode.org/charts/PDF/U1100.pdf
  - https://www.unicode.org/charts/PDF/U3130.pdf
  - https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-18/
  - https://korean.go.kr/ (National Institute of Korean Language)
  - https://www.w3.org/TR/klreq/ (W3C Requirements for Korean Text Layout — drafts)
  - https://github.com/orioncactus/pretendard (Pretendard)
  - https://source.typekit.com/source-han-sans/ (Adobe Source Han Sans)
  - https://fonts.google.com/noto/specimen/Noto+Sans+KR
  - https://learn.microsoft.com/en-us/typography/script-development/hangul
  - Gerry Leonidas writings on Korean type (University of Reading)
  - Hunminjeongeum (훈민정음) 1446, King Sejong — foundational document
---

# Hangul Script Typography

**Scope disclaimer — light coverage.** This is a light/entry-level reference for a web/UI typographer who has never set Korean before. It covers enough to set Korean body text competently, pair Hangul with Latin, and avoid the most common rendering mistakes — but it is not scholar-depth. Authoritative depth lives in the Unicode Standard Chapter 18, the W3C *Korean Layout Requirements* (klreq, in drafts as of 2026-04), the National Institute of Korean Language (국립국어원), Source Han Sans / Noto CJK KR project documentation, and the Pretendard specimen. For CJK-wide mechanics (fullwidth/proportional punctuation, vertical text, subsetting), see `./cjk-han.md` — this file does not duplicate them.

**Why Hangul is easy to underestimate.** Korean looks visually uniform — square syllable blocks in a grid — and shares the CJK Unicode space, so teams treat it as "another CJK" and reach for Noto Sans CJK JP. Wrong: Korean is linguistically and typographically distinct, the Korean cut of Noto is a specific glyph set that `lang="ko"` selects, and Korean has its own style traditions (Myeongjo vs Gothic), its own system fonts (Apple SD Gothic Neo, Malgun Gothic), and its own modern open-source canon (Pretendard) that competes with the Noto/Source Han stack. Rendering Korean in a Japanese font emits rough-approximation glyphs that a Korean reader identifies as wrong immediately.

**What this file covers.** Origin (Hunminjeongeum 1446). Jamo inventory and syllable-block composition. Font typology (Myeongjo / Gothic / Graphic / Handwriting). Notable fonts, with Pretendard as a 2021+ reference point. Mixing Hangul with Latin — including metric compatibility to Inter. Line-breaking rules. Brief notes on North-vs-South orthography and Hanja mixing. CSS recipes. Common traps.

---

## Origin

Hangul is the only major world script whose invention is **documented, dated, and accompanied by an explicit linguistic rationale**. Created in 1443 CE by **King Sejong the Great** (세종대왕) and promulgated in 1446 CE as **Hunminjeongeum** (훈민정음, "The Correct Sounds for Instructing the People"), Hangul was designed from the ground up to be learnable by commoners — explicitly as a populist literacy instrument against the dominance of Classical Chinese among the educated elite.

The Hunminjeongeum document articulates the design rationale:

- **Consonants** are shaped after the articulation anatomy — ㄱ (k/g) represents the tongue touching the back of the palate; ㄴ (n) represents the tongue touching the upper teeth; ㅁ (m) represents the closed lips. The five basic consonants (ㄱ ㄴ ㅁ ㅅ ㅇ) map to the five places of articulation; additional consonants are derived by adding strokes to indicate additional phonetic features.
- **Vowels** are constructed from three primal elements representing **heaven (·, a dot), earth (ㅡ, a horizontal line), and human (ㅣ, a vertical line)** — a Confucian cosmological frame overlaid onto a pragmatic phonological system. Vowels combine these elements to indicate position and rounding.

Hangul existed alongside **Hanja** (Chinese characters, see `./cjk-han.md`) for five centuries. Hanja remained the prestige script for scholarly and official writing until the 20th century. Hangul's rise to sole-script dominance is a 20th-century phenomenon — North Korea abolished Hanja from general use shortly after 1949; South Korea progressively reduced Hanja through the 1970s–1990s, and contemporary Korean prose is effectively all-Hangul except for specific scholarly, legal, and traditional contexts.

---

## Jamo: Letters

Hangul has 19 consonant letters + 21 vowel letters = **40 jamo** (자모, "mother-letters"). These are the atomic units; syllable blocks compose from them.

### Consonants

**Basic (14):**
ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
(k/g, n, t/d, l/r, m, p/b, s, null/ng, j, ch, k-aspirated, t-aspirated, p-aspirated, h)

**Tense forms (5):**
ㄲ ㄸ ㅃ ㅆ ㅉ
(double-k, double-t, double-p, double-s, double-j — sometimes called "fortis" or "glottalized" consonants)

**Notable:** ㅇ (ieung) is unique — at the **start** of a syllable it is silent (a placeholder when a vowel has no initial consonant); at the **end** of a syllable it is pronounced "ng".

### Vowels

**Basic (10):**
ㅏ ㅑ ㅓ ㅕ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ
(a, ya, eo, yeo, o, yo, u, yu, eu, i)

**Compound / diphthong (11):**
ㅐ ㅒ ㅔ ㅖ ㅘ ㅙ ㅚ ㅝ ㅞ ㅟ ㅢ
(ae, yae, e, ye, wa, wae, oe, weo, we, wi, ui)

### Unicode encoding of jamo

Three distinct Unicode blocks cover Hangul jamo, reflecting historical encoding decisions:

| Block | Range | Size | Purpose |
|-------|-------|------|---------|
| **Hangul Jamo** (combining) | U+1100–U+11FF | 256 | "Modern" conjoining jamo used for dynamic composition into syllable blocks via Unicode's Hangul Syllable Composition algorithm. |
| **Hangul Syllables** (precomposed) | U+AC00–U+D7A3 | 11,172 | Every possible modern Korean syllable block as a precomposed codepoint. What essentially all modern Korean text uses. |
| **Hangul Compatibility Jamo** (standalone) | U+3130–U+318F | 96 | Standalone display of jamo as individual symbols, for linguistic examples and keyboard displays. Not used for composing actual words. |

**In practice**, modern Korean content is stored as **Hangul Syllables** (U+AC00–U+D7A3) — a single codepoint per syllable block. A Korean paragraph encoded this way is both compact and unambiguous; the shaper does not need to compose on the fly.

The combining **Hangul Jamo** block exists for edge cases: historical Korean texts using obsolete jamo, certain North Korean orthographic variants, linguistic description, and cases where initial/medial/final positions need explicit encoding.

---

## Syllable Block Composition

This is the distinctive structural feature of Hangul. Unlike Latin (letters in a row), Thai (base + mark stack), or CJK Han (one character per glyph), Korean composes multiple jamo into a **2-dimensional syllable block** — called **음절** (umjeol) — that occupies a single square visual cell.

### Structure

A Korean syllable block has **2 or 3 components**:

1. **Initial consonant** (초성, choseong) — required. Always a consonant. For syllables that phonetically start with a vowel, use ㅇ (ieung) as a silent placeholder.
2. **Medial vowel** (중성, jungseong) — required. Always a vowel.
3. **Final consonant** (종성, jongseong) — optional. One consonant, or (rarely) two consonants as a cluster.

### Examples

- **한** (han) = ㅎ (h) + ㅏ (a) + ㄴ (n). Initial top-left, medial top-right, final at the bottom.
- **국** (guk, "country") = ㄱ (g) + ㅜ (u) + ㄱ (k). Initial top, medial bottom, final bottom.
- **어** (eo) = ㅇ (silent initial) + ㅓ (eo), no final. Initial left, medial right.
- **읽** (ilk, "read") = ㅇ + ㅣ + ㄹㄱ. A consonant cluster at the final position.
- **한국어** (hangugeo, "Korean language") = three syllable blocks: 한, 국, 어.

### 2D layout rules

The position of each jamo within the block depends on the **vowel type**:

- **Vertical vowels** (ㅏ ㅑ ㅓ ㅕ ㅣ — those with a vertical stroke) → initial **left**, vowel **right**, final at **bottom** if present.
- **Horizontal vowels** (ㅗ ㅛ ㅜ ㅠ ㅡ — those with a horizontal stroke) → initial **top**, vowel **middle**, final at **bottom** if present.
- **Wrapping vowels / diphthongs** (ㅘ ㅚ ㅙ ㅝ ㅢ etc.) → more complex arrangements, often with the initial top-left and the compound vowel occupying top-right and middle.

Font designers define a glyph shape for each jamo × position × context combination. A jamo has different shapes when it appears as initial vs final, and different shapes when it pairs with a horizontal vs vertical vowel. A comprehensive modern Korean font ships hundreds of contextual forms.

### Modern vs traditional block layout

Two philosophies:

- **Uniform / fully-square.** Every syllable block occupies exactly one em-square cell, regardless of whether it has a final consonant. The traditional / calligraphic ideal, carried into most system fonts (Malgun Gothic, Apple SD Gothic Neo) and editorial fonts. Maintains CJK-grid compatibility when Korean is mixed with Hanja or CJK text.
- **Width-variant / "wide-tall".** Syllable blocks with a final consonant render wider (or taller) than blocks without. Gives the text a more natural visual rhythm, closer to Latin proportional type. Some modern Korean display faces adopt this; Pretendard has a subtle width variance.

Most UI typography in Korean uses uniform-square blocks. Width-variance is a display-style choice, not a body-text default.

### Unicode Hangul Syllable Composition

The Unicode algorithm composes jamo into syllable codepoints:

```
syllable codepoint = 0xAC00 + (initial_index × 588) + (medial_index × 28) + final_index
```

...where initial_index is 0–18 (19 initials), medial_index is 0–20 (21 medials), and final_index is 0–27 (28 finals, including "no final" as index 0). Total: 19 × 21 × 28 = **11,172 syllable blocks**, exactly the size of the Hangul Syllables block.

You rarely compute this by hand — store content as precomposed Hangul Syllables and trust the font to render. NFC normalization on Korean text converts combining jamo sequences to the precomposed form.

---

## Font Typology

Korean type divides into several style genres, parallel to but distinct from Chinese and Japanese equivalents.

### Myeongjo / Song (명조 / 송)

The traditional printed form — ink-brush-inspired, with stroke contrast, tapered terminals, and calligraphic finish. Analogous to Chinese Song/Ming and Japanese Mincho. Used for:

- **Body text in formal printed publications** (literary fiction, scholarly books, newspapers in traditional layout).
- **Long-form editorial** where a calligraphic register suits the content.

Examples: **Noto Serif KR, Source Han Serif KR**, Yoon Myeongjo, Sandoll Myeongjo, older system Batang.

### Gothic / Dotum (고딕 / 돋움)

The sans-serif category — uniform stroke width, no contrast, modern construction. Analogous to Chinese Hei and Japanese Gothic. Used for:

- **Screens, UI, digital publications.**
- **Headlines, branding, contemporary design.**
- Most modern Korean body text on the web.

Examples: **Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR, Source Han Sans KR, Pretendard, Nanum Gothic, Spoqa Han Sans Neo**.

Within Gothic, some foundries distinguish **Dotum** (돋움, "raised" — a specific sans subgenre with certain construction choices) from generic Gothic, but in contemporary casual use the terms overlap.

### Graphic (그래픽)

Display-oriented contemporary type — experimental, editorial, often used for branding and titling. No Latin direct equivalent; closest analog is display-face.

### Handwriting (손글씨 / Sonssi)

Cursive, brush, marker, or pen-script style. Used for informal, decorative, casual contexts. Google Fonts carries several: **Nanum Pen Script, Black Han Sans, Gaegu, Gugi**, etc.

### Roundness / Maru

Some Korean sans fonts ship **rounded** variants (마루, maru) — softer corners on stroke terminals. Parallel to Japanese Maru Gothic. Used for approachable, friendly UI; common in children's content.

---

## Notable Fonts

### Ships with the OS

- **macOS / iOS:** Apple SD Gothic Neo (sans, system default), Nanum Myeongjo (preinstalled), Nanum Gothic (preinstalled), Apple Myungjo.
- **Windows:** Malgun Gothic (sans, system default), Batang (serif/myeongjo), Gulim (sans, legacy), Dotum (sans, legacy).
- **Android:** Noto Sans CJK KR / Noto Sans KR as AOSP default; vendor skins substitute (Samsung OneUI uses SamsungOne, MIUI uses its own family).

### Pan-CJK open families

- **Noto Sans KR / Noto Serif KR** (Google/Adobe, SIL OFL). The Korean regional subfamily of Noto CJK. Variable-font cuts available (wght axis). See `./cjk-han.md` for CJK-wide context.
- **Source Han Sans KR / Source Han Serif KR** (Adobe/Google, SIL OFL). Same underlying project as Noto CJK — Korean name: **본고딕** (bon-godik) for Sans, **본명조** (bon-myeongjo) for Serif.

### Modern Korean open-source (2015+)

- **Pretendard** (Kil Hyung-jin, MIT license, 2021–present). The breakout modern Korean sans. Pretendard was specifically designed with **metric-matched Latin to Inter** (Rasmus Andersson's Inter) — same x-height, cap-height, and weight ladder. A bilingual Korean+English product can use **Pretendard for Korean and Pretendard Std / Inter for Latin** (or just Pretendard for both, since Pretendard ships its own Latin) and get visually coherent metrics without overrides. Variable font available. Has rapidly become the de-facto default for Korean startups and product UI in 2022–2026.
- **Nanum Gothic, Nanum Myeongjo, Nanum Pen Script, Nanum Gothic Coding, Nanum Brush Script** (Naver-sponsored, SIL OFL). The earlier-generation open-source Korean family, widely preinstalled and still used for body.
- **Spoqa Han Sans Neo** (Spoqa, OFL, 2015 with updates). A Korean-and-numeric sans optimized for UI; popular in Korean startups pre-Pretendard.
- **Gmarket Sans** (Gmarket, free for commercial use) — display-leaning.
- **GongGothic / GongMyeongjo** (various municipal governments' free-release fonts).

### Commercial Korean foundries

- **Sandoll** (산돌) — one of the largest Korean foundries; extensive catalog covering Gothic, Myeongjo, display.
- **Yoon Design** (윤디자인) — Yoon Gothic, Yoon Myeongjo families, long-standing foundry.
- **AG Typography** (AG타이포그라피연구소) — editorial and display.
- **Studio 1-to-1, Typefaces of Korea** — contemporary independent foundries.

### Other notable

- **IBM Plex Sans KR** (2019+) — the Korean cut of IBM Plex, metric-matched to IBM Plex Sans Latin.
- **LXGW WenKai KR** — open-source pan-CJK kaishu style covering Korean.

### Font selection heuristic

1. **Modern Korean UI:** **Pretendard** (with its matched Latin) is the 2026 default for any product targeting Korean users with a contemporary brand posture.
2. **Bilingual Korean+English product:** **Pretendard** — the Inter-matched metrics save you from `size-adjust` gymnastics. Alternate: **IBM Plex Sans KR + IBM Plex Sans**.
3. **Generic fallback / guaranteed availability:** **Noto Sans KR** (free, via Google Fonts or self-hosted).
4. **System-only stack:** `"Apple SD Gothic Neo", "Malgun Gothic", sans-serif`.
5. **Editorial / long-form prose:** **Noto Serif KR** or **Source Han Serif KR**, or a commercial Myeongjo (Sandoll, Yoon).

---

## Mixing Hangul with Latin

Korean body text routinely mixes in Latin — English loanwords, brand names, technical terms, acronyms, URLs. The Korean-Latin pairing problem is one of metric harmony.

### The metric problem

Korean syllable blocks are designed to occupy roughly a square cell — so the perceived "x-height" of a block is close to its cap-height. Latin lowercase at the same `font-size` sits inside roughly half that visual area. A Korean font's bundled Latin cut is typically drawn with a larger x-height and smaller ascender/descender than a Latin-native face, to harmonize with Korean.

When a Korean font's Latin companion is used: looks balanced. When a Latin-only font falls through to render the Latin portion: looks undersized next to the Korean.

### Pretendard and Inter

Pretendard specifically solved this by matching Inter's metrics. Using Pretendard for Korean and Inter for Latin (or Pretendard for both) gives visually unified metrics. This is why bilingual Korean product teams adopt Pretendard: the metric-matching is done.

### Apple SD Gothic Neo and Malgun Gothic

Both are system defaults, but their **Latin companions differ between platforms** — a page rendered with Apple SD Gothic Neo on macOS looks different from the same page rendered with Malgun Gothic on Windows, even though both are "system Korean sans." If cross-platform consistency matters, self-host a webfont (Pretendard, Noto Sans KR) instead of relying on system fonts.

### Typical 2024+ bilingual font stack

```css
.bilingual {
  font-family:
    "Pretendard Variable",
    "Pretendard",
    "Apple SD Gothic Neo",
    "Malgun Gothic",
    "Helvetica Neue",
    Arial,
    system-ui,
    sans-serif;
}
```

### Baseline

Hangul and Latin share a baseline. No vertical-align handling needed. Bidi is trivial — both are LTR.

---

## Line-Height

Korean line-height demands are **lower than Thai or Devanagari** because Hangul syllable blocks stack their jamo *within* a single square cell — no marks extend above or below the block's box. There is no cross-line stacking to budget for.

Typical line-height:

| Context | Korean `line-height` (unitless) |
|---------|----------------------------------|
| Body prose | 1.5–1.7 |
| UI chrome | 1.4–1.5 |
| Headlines | 1.2–1.4 |
| Mixed Korean + Latin body | 1.5–1.65 |

This is closer to Latin conventions than to other CJK norms — Korean does not need the 1.7–1.8 that Japanese and Chinese body typically wants (see `./cjk-han.md`), because Korean's syllable blocks are less visually dense per cell than Japanese (which mixes kanji + kana at varying densities).

---

## Digits and Punctuation

### Digits

**Western Arabic digits (0–9) are standard** in modern Korean — including in financial, scientific, journalistic, and everyday commercial contexts. There are Korean-native numerals (일 이 삼 사 오 — for numbers 1–5), but these are *word-form* numerals used in prose, not a digit system used in place of Arabic digits for quantities. A Korean date of 2026-04-18 is written with Arabic digits.

### Punctuation

**Western punctuation is default** in modern Korean:

- `, . : ; ? ! " ' ( ) [ ]` — all standard.
- Em-dash `—`, en-dash `–`, ellipsis `…` — same as Latin conventions.

**Fullwidth CJK punctuation** (`。 、 ，` etc.) appears occasionally in:

- Traditional / literary publications.
- Vertical-text contexts (rare in modern Korean).
- Formal contexts where CJK-grid aesthetic is maintained.

Modern Korean prose uses Western punctuation. Do not default to CJK punctuation for Korean content unless the target register demands it.

### Vertical writing

Korean can be set vertically (top-to-bottom, columns advancing right-to-left) using `writing-mode: vertical-rl` — mechanically the browser supports it. But **Korean vertical writing is largely anachronistic in 2026**. It appears in:

- Calligraphy and art contexts.
- Some traditional signage (temple signs, restaurant menus in traditional registers).
- Historical document reproductions.

Everyday digital Korean is **horizontal LTR**. If you are reaching for `writing-mode: vertical-rl` for Korean content, verify it matches the register — otherwise it reads as a costume. See `./cjk-han.md` on CJK vertical-text conventions generally. Korean vertical technically works with `writing-mode: vertical-rl + text-orientation: mixed`, but unlike Japanese, Korean syllable blocks rotate awkwardly — the convention when Korean does appear vertically is `text-orientation: upright`, keeping each block upright.

---

## Line-Breaking

Korean uses **spaces between words**, unlike Chinese and Japanese. This makes line-breaking structurally easier than CJK — browsers break at word-boundary spaces. No dictionary segmentation needed.

### CSS controls

```css
:lang(ko) {
  word-break: keep-all;       /* don't break mid-syllable-block */
  overflow-wrap: break-word;  /* last-resort if a word is longer than the line */
}
```

**`word-break: keep-all`** is the most important rule for Korean — it prevents breaks from occurring in the middle of a syllable-block sequence (which CJK-style dictionary breakers might otherwise do). Koreans read word-by-word separated by spaces, so word-boundary breaks are what's expected.

**`word-break: break-all`** breaks at any character boundary, including inside Korean words. Do not use for Korean body.

**`line-break: strict | normal | loose`** affects some punctuation-adjacent behaviors but Korean doesn't have the same kinsoku-shori (line-composition) complexity as Japanese. The default typically suffices.

---

## North vs South Korean Orthography

Both Koreas use Hangul, but with differences:

- **Jamo ordering.** South Korea orders jamo traditionally: ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ... North Korea orders them differently (putting tense consonants at the end, and reordering several letters).
- **Hanja.** North Korea abolished Hanja from general use in 1949; South Korea retains Hanja for some scholarly, legal, and traditional contexts.
- **Spelling differences** exist for some words (북한말 vs 남한말 — North vs South lexicon).
- **Font form differences.** Some North Korean orthographic variants have distinct jamo shapes in certain positions.

**Practical guidance: default to South Korean** unless the content specifically targets North Korea. Noto Sans KR, Pretendard, Apple SD Gothic Neo, and all mainstream open-source Korean fonts are South Korean-standard. Fonts targeting North Korean forms exist in specialized contexts (Unicode research-survey, academic linguistics) but are not webfont-delivered for normal product use.

---

## Mixing Hanja

**Hanja** (한자 / 漢字) is Chinese-character script used historically in Korean. In 2026, Hanja appears in:

- **Scholarly texts** on classical literature, Buddhism, Confucian philosophy.
- **Legal documents** — some Korean legal conventions use Hanja for precise terms.
- **Academic papers** citing classical sources.
- **Newspapers** — occasional Hanja for disambiguation of homophones (though rare in mainstream journalism as of 2020s).
- **Traditional / ceremonial contexts** — temple signs, calligraphy, family genealogies.
- **Surnames and personal names** — Korean names often have a registered Hanja form alongside Hangul.

### Font coverage

Most Korean-only fonts (Pretendard, Spoqa, Nanum) do **not** cover Hanja — they ship Hangul-only glyph sets. Noto Sans KR **does** cover Hanja (via the CJK Unified Ideographs block it inherits from the Noto CJK project). If you need Hanja, use Noto Sans KR / Source Han Sans KR, or a commercial family that explicitly covers CJK Ideographs.

### Ruby / furigana for Hanja

When Hanja is used inline with Hangul, the Hangul pronunciation is often annotated as ruby above the Hanja — the same mechanism as Japanese furigana. Use `<ruby>` HTML:

```html
<ruby>漢字<rt>한자</rt></ruby>
```

See `./japanese.md` on `<ruby>` markup, `ruby-position`, and `ruby-align` CSS — the Korean case works identically.

---

## CSS Recipes

### Baseline Korean body styling

```css
:lang(ko) {
  font-family:
    "Pretendard Variable",
    "Pretendard",
    "Apple SD Gothic Neo",
    "Malgun Gothic",
    "Noto Sans KR",
    system-ui,
    sans-serif;
  font-size: 15px;            /* Korean UI body; tolerates slightly smaller than Latin */
  line-height: 1.6;
  letter-spacing: 0;          /* avoid positive tracking; breaks syllable blocks */
  word-break: keep-all;
  overflow-wrap: break-word;
}
```

### `lang="ko"` for correct CJK glyph selection

When using pan-CJK fonts (Noto Sans CJK, Source Han Sans), the `lang` attribute drives `locl` substitution for Korean-specific glyph forms:

```html
<html lang="ko">...</html>
<!-- Or per-element: -->
<p lang="ko">한국어 텍스트</p>
```

Without `lang="ko"`, a Noto Sans CJK font loaded for mixed content may render Korean with Japanese or Chinese glyph forms (often subtle, but visible for shared Hanja characters).

### Font-size

Korean readers tolerate slightly smaller body text than Latin:

- Korean UI body: **14–16px** (vs 14–16px Latin, similar range but tolerant of 14).
- Mobile body: 14–16px. 13px is a floor, below which legibility degrades.
- Editorial body: 16–18px.

### Letter-spacing: zero

Korean syllable blocks are designed with internal spacing tuned to each block. Positive `letter-spacing` inserts gaps **between** blocks that are visually large relative to the block size — the result looks distressingly loose. `letter-spacing: 0` is the correct default for Korean body. Negative `letter-spacing` is equally wrong (crowds the blocks).

For Korean **display** headings, a small negative letter-spacing (-0.01em to -0.02em) is sometimes used to tighten — but with caution, and never for body.

---

## Common Traps

1. **Using a Latin-only font for Korean content.** Korean jamo fall through to the next font in the stack or render as `.notdef` boxes. Always include a Korean font (Pretendard, Noto Sans KR, system Korean) in the `font-family` stack.

2. **Treating all CJK fonts as interchangeable.** Noto Sans CJK JP is *not* the same as Noto Sans CJK KR — the Korean subfamily renders Korean-specific glyph forms, the Japanese subfamily renders Japanese forms. Set `lang="ko"` and/or load the Korean-specific family explicitly.

3. **Positive `letter-spacing` on Korean body.** Inserts gaps between syllable blocks that read as distressingly loose. Keep `letter-spacing: 0` for body.

4. **`text-transform: uppercase | lowercase | capitalize` on Korean.** No effect — Korean is unicameral. Harmless in cascade, but don't rely on case for hierarchy.

5. **`word-break: break-all` for Korean content.** Breaks mid-syllable — nonsensical for Korean readers. Use `word-break: keep-all` to break at word boundaries (spaces).

6. **Using fullwidth CJK punctuation (`。 、 ，`) in Korean prose.** Reads as foreign / over-formalized. Modern Korean uses Western punctuation. Use fullwidth only for traditional/literary register, not default UI.

7. **Assuming Hanja support from all Korean fonts.** Pretendard, Spoqa, Nanum, and most Korean-dedicated fonts cover *Hangul only*. Use Noto Sans KR or a CJK-coverage family if Hanja must render.

8. **Vertical writing for modern Korean UI.** `writing-mode: vertical-rl` is technically available but reads as costume-y for contemporary Korean content. Reach for it only for explicit calligraphy, traditional signage, or historical reproduction.

9. **Not testing cross-platform with system fonts.** Apple SD Gothic Neo (macOS) and Malgun Gothic (Windows) render the same `lang="ko"` text differently — different metrics, different weight ladders, subtle different jamo shapes. Self-host Pretendard or Noto Sans KR for consistency.

10. **Using `font-synthesis: weight` or synthesizing italic for Korean.** Synthetic bold on Korean produces outline-outset artifacts that clog the syllable-block construction, like CJK synthetic bold (see `./cjk-han.md`). Italic synthesis is worse — Korean has no italic tradition, and slanting breaks jamo alignment within blocks. `font-synthesis: none` is defensible.

11. **Counting by character / codepoint for Korean.** A syllable block is one visible character but *can be* multiple codepoints when encoded as combining jamo. Use NFC normalization to precomposed syllables and `Intl.Segmenter('ko', { granularity: 'grapheme' })` for correct visible-character counting.

12. **Forgetting that Korean uses spaces.** Unlike Chinese and Japanese, Korean has word-boundary spaces. Line-breaking is straightforward if `word-break: keep-all` is set. Don't apply CJK dictionary-segmentation logic designed for Japanese/Chinese — Korean doesn't need it.

---

## Sources

**Unicode primary sources:**

- [Unicode Chart: Hangul Syllables (U+AC00–U+D7AF)](https://www.unicode.org/charts/PDF/UAC00.pdf)
- [Unicode Chart: Hangul Jamo (U+1100–U+11FF)](https://www.unicode.org/charts/PDF/U1100.pdf)
- [Unicode Chart: Hangul Compatibility Jamo (U+3130–U+318F)](https://www.unicode.org/charts/PDF/U3130.pdf)
- [Unicode Standard 16.0, Chapter 18 — East Asia](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-18/) — covers Hangul.

**W3C / layout references:**

- [W3C Korean Layout Requirements (klreq)](https://www.w3.org/TR/klreq/) — drafts as of 2026-04; the canonical web-platform reference for Korean layout once stabilized.

**Korean authoritative sources:**

- [National Institute of Korean Language (국립국어원)](https://korean.go.kr/) — South Korean orthographic authority, equivalent of a royal-institute or Académie.
- Hunminjeongeum (훈민정음) 1446 — the foundational document. English annotated editions available in scholarly Korean linguistics literature.

**Font projects:**

- [Pretendard GitHub](https://github.com/orioncactus/pretendard) — the modern Korean open-source reference. Specimen, design rationale, Inter metric-matching notes.
- [Adobe Source Han Sans project](https://source.typekit.com/source-han-sans/) — Korean subfamily documentation.
- [Noto Sans KR on Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
- [Noto CJK GitHub (notofonts/noto-cjk)](https://github.com/notofonts/noto-cjk)

**Shaping / OpenType:**

- [Microsoft Typography: Developing OpenType Fonts for Hangul Script](https://learn.microsoft.com/en-us/typography/script-development/hangul) — implementer's guide.
- [HarfBuzz Hangul shaping](https://harfbuzz.github.io/) — for shaper behavior specifics.

**Further reading:**

- Gerry Leonidas (University of Reading Department of Typography) — writings on Korean type in English-language typography research-survey.
- Ken Lunde, *CJKV Information Processing*, 2nd ed., O'Reilly, 2009 — encoding and script chapters cover Hangul in depth.
- Korean Wikipedia entries on 한글 (Hangul), 글꼴 (font), 명조 (Myeongjo), 고딕 (Gothic) — practical reference for Korean-language terminology.

**Peer references:**

- `./cjk-han.md` — for CJK-wide mechanics (subsetting, vertical text, fullwidth/proportional) not duplicated here.
- `./japanese.md` — for `<ruby>` markup and furigana mechanics, identical for Hanja annotation.
