---
date: 2026-04-17
coverage: medium
peers:
  - ./latin.md
  - ./hebrew.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
primary_sources:
  - https://www.w3.org/International/alreq/
  - https://www.w3.org/TR/alreq-gap/
  - https://www.w3.org/TR/arab-ur-lreq/
  - https://www.unicode.org/versions/latest/ch09.pdf
  - https://fonts.google.com/noto/specimen/Noto+Naskh+Arabic
  - https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu
  - https://www.amirifont.org/
  - https://29lt.com/
  - https://research-survey.reading.ac.uk/typoarabic/
---

# Arabic Script Typography

**Scope disclaimer.** This is a *practitioner* reference for a web/UI typographer who has never set Arabic before. It is not scholar-depth. Authoritative depth lives in Titus Nemeth's *Arabic Type-Making in the Machine Age*, the W3C's *Arabic & Persian Layout Requirements* (ALReq), Unicode Standard Chapter 9, and the TypoArabic research-survey group at Reading. Where this file gives a practical rule of thumb, assume the scholarly answer is more nuanced.

**Why Arabic is hard to "just support" in a product.** Arabic is not Latin-with-a-direction-flip. It is a connecting script whose letters change shape contextually, whose text rhythm is fundamentally horizontal-calligraphic rather than box-of-boxes, whose tradition of justification uses letter elongation (kashida) rather than space expansion, and whose most widely used calligraphic style (Nastaliq, used for Urdu) breaks essentially every assumption CSS line layout makes. RTL is the easy part. Shaping, baseline, and justification are where teams lose months.

**What this file covers.** Fundamentals (RTL, four forms, 28 letters). The three type styles you will actually meet on the web (Naskh, Nastaliq, Kufi) plus a handful of formal hands (Thuluth, Diwani, Ruqah). Typographic specifics (kashida, vertical ligatures, diacritics, numerals, punctuation, leading, measure). Bidi behavior. Available fonts. CSS gotchas with snippets. Source-code and IDE concerns. Accessibility. A short anti-patterns list.

---

## Fundamentals

### Direction

Arabic is written **right-to-left**. Characters are stored in *logical* order (first-typed = first in memory) and rendered in *visual* order (first-typed = rightmost on screen). The Unicode Bidirectional Algorithm (UBA, UAX #9) handles the transform. This distinction matters when you debug — a string that looks wrong on screen may be correct in memory, and vice versa.

Arabic numerals within Arabic text read left-to-right even though the surrounding prose reads right-to-left. This is correct Unicode behavior, not a bug.

### Connecting script

Arabic is *cursive in print as well as handwriting*. Letters within a word connect to their neighbors (with a defined set of exceptions — six letters only connect on their right side, never their left, which forces a break in the word's join). This is not an optional stylization: disconnected Arabic text looks as wrong as "H E L L O" looks in English.

Because the script is cursive, each letter has up to **four contextual forms**:

| Form | When it appears |
|------|-----------------|
| **Isolated** (ـ) | Letter stands alone (end of a six-non-left-joiners word, start of document, around punctuation) |
| **Initial** | Start of a join sequence (right side of the first letter in a connected run) |
| **Medial** | Middle of a join sequence |
| **Final** | End of a join sequence (left side of the last connected letter) |

These four forms are *not* four separate Unicode code points. They are a single code point (e.g. U+0628 ARABIC LETTER BEH) whose rendered glyph is selected by the shaping engine at runtime. **HarfBuzz** is the shaper used by every modern browser (Chrome/Blink, Firefox/Gecko, Safari/WebKit all ship HarfBuzz or equivalent OpenType shapers). It reads the font's OpenType tables — specifically the `init`, `medi`, `fina`, `isol` features in GSUB — and substitutes the right glyph. You get this for free with a correctly built Arabic font and a modern browser. You *lose* it if you mangle the features list with `font-feature-settings` (see Gotchas).

### Number of letters

**28 letters** in standard Arabic. Persian (Farsi) adds 4 (پ چ ژ گ = 32). Urdu adds more and uses different contextual forms for some. Pashto, Kashmiri, Uyghur, Sindhi each extend the alphabet further. When you pick a font for "Arabic", verify it covers the *language* you need — a font that covers Quranic Arabic may omit Persian `پ` or Urdu `ٹ`.

### Joining classes (brief)

Not all letters join on both sides. Unicode assigns each letter a *joining class*:

- **Dual-joining** (most letters) — joins left and right
- **Right-joining** — joins only on the right; six letters: ا د ذ ر ز و (and the non-letter ة is similar)
- **Non-joining** (rare, mostly punctuation)
- **Transparent** (marks and diacritics — don't affect join)

The practical consequence: a word like "داود" (David) has internal join breaks because د and و are right-joining. The shaper handles this; you just need to understand that "word = one unbroken glyph chain" is not true.

---

## Type Styles

### Naskh

**The default body style.** Horizontal-rhythm, legible at text sizes, descends from the manuscript Naskh hand codified in the 10th–11th centuries by Ibn Muqla and Ibn al-Bawwab. It is what you are reading in most Arabic newspapers, most Arabic novels, most Arabic web pages, and essentially every printed Quran for the last several hundred years.

**When to use Naskh:** body text in Arabic, Persian, Urdu (for running prose — though Urdu literary tradition prefers Nastaliq), Pashto, Malay. Default choice for UI body unless a brand says otherwise.

**Go-to web fonts:**
- **Noto Naskh Arabic** (Google/Monotype, open) — broad coverage, SIL-style safe default
- **Amiri** (Khaled Hosny, SIL OFL) — high-quality Naskh based on Bulaq Press types; also ships Amiri Quran for vocalized religious text
- **Lateef** (SIL) — Naskh tuned for Southeast Asian languages (Sindhi, Balochi)

Naskh is where Arabic web typography *works without heroics*. Set `font-family: "Noto Naskh Arabic", serif`, set `line-height: 1.7`, set `direction: rtl`, and you have readable Arabic.

### Nastaliq

**The calligraphic diagonal-slope style used for Urdu.** Also used for Persian poetry, Kashmiri, Pashto (some), and historical Persian prose. A Nastaliq word is *hung* — letters cascade diagonally from upper-right to lower-left along a sloping baseline, with dramatic height variation within a single line.

**Why Nastaliq is hard on the web:**

1. **No flat baseline.** CSS line-height assumes a flat baseline per line. Nastaliq lines have a *baseline region* that slopes; glyphs sit at many different vertical positions along it. Setting `line-height` the way you would for Latin gives cramped or absurdly gappy results.
2. **Height varies wildly within a line.** A short word might be 1em tall; a long word with compound stacks might be 2.5em tall. Fixed leading *clips or floats* content.
3. **Justification doesn't work.** Nastaliq is traditionally ragged-left (because RTL). Browsers that attempt `text-align: justify` on Nastaliq tend to produce unacceptable results — word-spacing balloons, kashida insertion is crude if present at all.
4. **No CSS generic for it.** Until `generic(nastaliq)` from CSS Fonts 4 lands everywhere (not yet widely shipped as of 2026-04), there is no `font-family: cursive-nastaliq` fallback. You must explicitly name the font. If you set Urdu without naming a Nastaliq font, the browser falls back to a Naskh face — which Urdu readers find jarring and, for longer texts, tiring.

**Go-to web fonts:**
- **Noto Nastaliq Urdu** (Google/Monotype, open) — the free option; most users have seen it
- **Jameel Noori Nastaleeq** — widely used in Pakistani publishing; free for personal use, licensing varies commercially
- **Mehr Nastaliq** — Indian Nastaliq, open license, common for Urdu web
- **Awami Nastaliq** (SIL) — covers Pashto and less-common languages

**When to use Nastaliq:** Urdu UI/content, Persian poetry (but *not* Persian prose — Persian prose uses Naskh; Nastaliq for Persian is reserved for poetry and titling by convention), Kashmiri. For Arabic (as in, Arabic-language content), Nastaliq is wrong.

**Practical `line-height`:** start at **2.0–2.4** for Nastaliq body text and adjust up. Yes, really. Compare with Naskh's 1.6–1.8 and Latin's 1.4–1.5.

### Kufi

**Geometric, angular, historically monumental.** The earliest Quranic manuscripts (7th–10th century) were written in Kufi, which has squared, architectural letterforms without the cursive flow of Naskh. It is the *display* style of Arabic: signage, titles, logos, brand marks.

**When to use Kufi:** headings, UI chrome, logos, display sizes. Not for body — it is genuinely hard to read at text sizes.

**Go-to web fonts:**
- **Noto Kufi Arabic** (Google/Monotype, open) — default geometric Kufi
- **Cairo** (Mohamed Gaber, SIL OFL) — modern geometric Arabic display sans with Variable axis for `wght`; pairs with Latin sans like Source Sans
- **Reem Kufi** (Khaled Hosny) — Kufi derivative with softer curves, good for headlines

### Thuluth, Diwani, Ruqah (briefly)

Three formal/calligraphic hands you will occasionally meet:

- **Thuluth** — the monumental inscriptional style (mosque walls, certificates). Extremely ornate. Digital Thuluth fonts exist (Aref Ruqaa covers adjacent territory) but are for display only. No sane body text.
- **Diwani** — Ottoman chancery hand. Elaborately interlocked, diagonal, heavily contextual. Used for titling and diplomas.
- **Ruqah** — the everyday Ottoman cursive hand; now widely used for *titling* in Arab newspapers. Short, compact, pragmatic. A good Ruqah (e.g. Aref Ruqaa) is usable for headings and some UI.

---

## Typographic Specifics

### Kashida (tatweel, U+0640)

A horizontal-elongation character (ـ) inserted between two dual-joining letters to stretch their connection. In print, kashida is the traditional way Arabic handles justification — rather than expanding word-spaces (the Latin approach), stretch the ligatures.

**In Unicode terms:** U+0640 ARABIC TATWEEL is a dual-joining character with explicit width. In high-quality typesetting, typographers hand-place kashidas at specific letter joins that tradition permits (not every join is eligible — there are conventional "good" places and "bad" places).

**In CSS:** support is *patchy*.

- `text-align: justify` on Arabic *may* insert kashidas; behavior depends on browser, font (whether it has good kashida handling in GSUB), and dialect.
- `text-justify: kashida` (once proposed, now largely abandoned in CSS 3 Text) is not reliable.
- `text-justify: inter-character` is primarily for CJK.
- WebKit bug 6203 ("Use Kashida for full justification in Arabic scripts") has been open for years; as of 2026-04, full kashida-aware justification is **not** reliably cross-browser.

**Practitioner rule.** Prefer ragged-left (the RTL equivalent of ragged-right) for Arabic paragraphs. Use `text-align: start` (which resolves to right in RTL) and do not justify. For titles that *must* be justified, a designer-placed tatweel in the copy itself is more predictable than asking the browser for it.

**Do not** insert literal U+0640 characters into dynamic body text to fake justification. They will fail to re-justify on resize/zoom, break search, break copy-paste, and look wrong when the reflow changes.

### Vertical ligatures

Arabic fonts frequently stack letters vertically. The `ل` + `م` pair can produce a vertical stack `لم` → one ligature glyph. The Lam-Alef ligature `لا` (mandatory, not stylistic) is the most famous. Quality fonts encode these via GSUB `liga` (required), `rlig` (required ligatures — *do not disable*), `calt` (contextual alternates), and `dlig` (discretionary ligatures).

**CSS practitioner rule.** `font-variant-ligatures` defaults are fine for Arabic body. Do **not** set `font-variant-ligatures: none` globally — you will destroy `rlig` required ligatures and render nonsense for Arabic/Urdu/Persian users. If you must disable ligatures (e.g. for a monospaced code font), scope narrowly.

### Diacritics (tashkeel / harakat)

Short-vowel marks that appear above or below base letters. Arabic is normally written *unvocalized* — diacritics are omitted from body text because fluent readers don't need them. They reappear in:

- The Quran (fully vocalized, essential for correct recitation)
- Children's books and language-learning material
- Disambiguating unusual words in academic or legal text
- Poetry (sometimes)
- Any place the meaning could be ambiguous

The main marks:
- Fatha (َ), Damma (ُ), Kasra (ِ) — short vowels
- Shadda (ّ) — consonant doubling
- Sukun (ْ) — absence of vowel
- Tanwin ( ً  ٍ  ٌ ) — doubled vowels (nunation)

Plus madda, hamza-above, hamza-below, and a large set of Quranic marks (cantillation, pause signs, etc.).

**OpenType.** Diacritics are positioned by the `mark` (mark-to-base) and `mkmk` (mark-to-mark, for stacking tanwin + shadda) features. Good Naskh fonts have dense, accurate `mark`/`mkmk` tables. Older fonts may position diacritics poorly — they drift, overlap, or collide with ascenders above.

**Line-height implication.** Diacritics eat vertical space. If your content is vocalized (Quranic, educational), your leading needs to grow. Start 1.8–2.0 for vocalized Naskh body.

### Numerals

Three digit systems are in use:

| System | Digits | Where |
|--------|--------|-------|
| **European digits** (also called "Western Arabic") | 0 1 2 3 4 5 6 7 8 9 | Maghreb (Morocco, Algeria, Tunisia, Libya), mixed use elsewhere, most of the web |
| **Arabic-Indic digits** ("Hindi digits" colloquially in Arabic) | ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ (U+0660–0669) | Mashriq (Egypt, Saudi Arabia, Levant, Gulf) |
| **Extended Arabic-Indic** ("Eastern Arabic-Indic") | ۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ (U+06F0–06F9) | Persian, Urdu, Pashto |

**Locale-driven, not CSS-driven.** `font-variant-numeric` does **not** switch between these sets — it switches figure style (lining / oldstyle / tabular / proportional) within a set. Switching digit systems is a *content* or *locale* concern: either author the content with the target digits, or use `Intl.NumberFormat` with an Arabic/Persian locale to format numbers into the correct digit set at runtime.

Both sets render LTR even inside RTL text (per Unicode); the most-significant digit is always on the left.

### Punctuation

Arabic uses several punctuation characters that differ from Latin:

| Character | Unicode | Name |
|-----------|---------|------|
| ، | U+060C | Arabic comma |
| ؛ | U+061B | Arabic semicolon |
| ؟ | U+061F | Arabic question mark (mirrored relative to Latin `?`) |
| ٪ | U+066A | Arabic percent sign |
| ٫ | U+066B | Arabic decimal separator |
| ٬ | U+066C | Arabic thousands separator |
| ٭ | U+066D | Arabic five-pointed star (asterisk-like) |
| ؉ | U+0609 | Arabic-Indic per mille sign |

Quotation conventions vary by dialect and publisher. French-style guillemets «» are common in Arabic and Persian; curly quotes "" show up too. Straight ASCII quotes are acceptable online but look amateur in print-quality work. For Persian, guillemets are the dominant printed convention.

**Common bug.** Mixing Latin `?` with Arabic prose: the `?` renders LTR (correct by bidi rules) but looks wrong to an Arabic reader because it curves the wrong way. Use `؟` (U+061F) in Arabic text.

### Line-height and measure

**Line-height.** Arabic needs more leading than Latin. The reasons compound:

1. Diacritics float above/below base letters (when present)
2. Descender + ascender extents are larger (Arabic letters frequently descend below a Latin descender line)
3. The vertical density of the script is higher — glyphs pack more ink vertically than Latin does

Rough practitioner guidance for body text:
- **Naskh, unvocalized:** 1.6–1.8
- **Naskh, vocalized** (Quran, pedagogical): 1.8–2.2
- **Kufi (when used for body, rare):** 1.6–1.8
- **Nastaliq (Urdu):** 2.0–2.4 or more

Set `line-height` as *unitless* (e.g. `1.7`, not `1.7em` or `27px`) so it inherits correctly across nested fonts. This matters especially for bilingual documents.

**Measure.** For comparable visual rhythm to Latin's 45–75 CPL, Arabic generally wants *fewer* characters per line — Arabic letters average wider and the eye-tracking pattern is different. Target roughly 30–60 characters per line for Naskh body. Nastaliq is more of a word-count concept than CPL because word widths vary so dramatically.

---

## Bidirectional Interaction

Mixing Arabic with Latin (names, URLs, code, numbers) is the normal case, not the exception. Get this right with `dir` and trust the UBA.

### HTML `dir` attribute

```html
<html dir="rtl" lang="ar">
```

Sets the base direction for the whole document. Preferred over CSS `direction: rtl` because it composes with form controls and content-editable correctly.

For mixed content — a comment thread where some posts are Arabic and some English — use:

```html
<article dir="auto">...</article>
```

`dir="auto"` tells the browser to determine direction from the first *strong* character in the content. This is usually what you want for user-generated content. Do not assume every Arabic user's environment is RTL — if they are posting English, you want the block to be LTR.

For isolated inline switches:

```html
Title: <bdi>لبنان</bdi>
```

`<bdi>` isolates bidi context so the embedded Arabic name doesn't mirror surrounding Latin punctuation incorrectly.

### CSS `direction` and `unicode-bidi`

```css
html {
  direction: rtl;
  unicode-bidi: isolate;
}
```

**Prefer `dir` in HTML to `direction` in CSS.** HTML is the semantic authority; CSS should reflect, not define, direction. That said, CSS `direction` is necessary when you are styling without markup control (e.g. a component library that must RTL-flip itself).

`unicode-bidi` modes:
- `normal` — no special behavior
- `embed` — creates an embedding level; deprecated in favor of `isolate`
- `isolate` — modern default; isolates the bidi context so interior text doesn't leak direction
- `bidi-override` — forces a direction; rarely correct, mostly a hack
- `plaintext` — like `dir="auto"` in CSS form

**Practitioner rule.** Use `isolate` in CSS for any block that mixes scripts. Trust it to do the right thing.

### Logical properties

Use *logical* CSS properties, not physical ones, for any layout meant to support RTL:

| Physical | Logical |
|----------|---------|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |
| `left: 0` | `inset-inline-start: 0` |

A component authored with logical properties flips itself when `dir="rtl"` is applied. A component hardcoded with `left`/`right` requires RTL-specific overrides.

### Mixed RTL/LTR pitfalls

1. **Phone numbers, dates, and codes in Arabic text.** These should render LTR inside RTL. The UBA handles this correctly if the digits are untagged. If they look wrong, check whether some framework has injected `dir="rtl"` on the span.
2. **URLs.** Should be LTR. Wrap with `<bdi>` or `<span dir="ltr">`.
3. **Emoji and symbols.** Unicode classifies most emoji as neutral; they inherit surrounding direction. Usually correct, occasionally surprising.
4. **CSS `::before` / `::after` content.** Content inserted by pseudo-elements does not inherit `dir` semantics well. Test.

**Cross-ref.** `../../ui-verify-i18n` (peer skill) covers the full bidi algorithm and locale-formatting layer. This file covers only the typographic surface.

---

## Fonts Available

Short practitioner list, genre-organized. All are free or widely available; all ship with usable OpenType tables.

**Naskh (body):**
- Noto Naskh Arabic — default safe choice
- Amiri — high-quality Naskh; Amiri Quran variant for vocalized religious text
- Lateef — Naskh tuned for Southeast Asian languages
- IBM Plex Sans Arabic — sans-leaning Naskh, good for UI
- Adobe Arabic — commercial, ships with Creative Cloud
- Greta Arabic (Type Together) — premium editorial Naskh

**Kufi / geometric display:**
- Noto Kufi Arabic — default
- Cairo — variable weight, pairs with Latin sans
- Reem Kufi — softer Kufi
- Tajawal — modern sans with Kufi character
- Aref Ruqaa — closer to Thuluth/Ruqaa for display

**Nastaliq (Urdu / Persian poetry):**
- Noto Nastaliq Urdu — default
- Jameel Noori Nastaleeq — publishing standard
- Mehr Nastaliq — open-license alternative

**Calligraphic / display:**
- Aref Ruqaa — Ruqah-ish display
- Mirza — Persian display
- Tasmeem — Persian/Arabic elaborate display
- Diwani Letter — Diwani-style display (commercial)

**Commercial foundries to know.** 29LT (Lebanon), Arabic Type (Pascal Zoghbi), TPTQ Arabic (Kristyan Sarkis), Rosetta Type, Type Together, Typotheque. These publish the high-end commercial Arabic used in publications and serious branding. Go here when Noto is not good enough.

---

## Web/CSS Gotchas

### 1. Don't disable Arabic shaping features

Wrong:

```css
body {
  font-feature-settings: "liga" 0, "calt" 0;
}
```

`liga` and `calt` are *structural* for Arabic. Disabling them produces broken, disconnected letters. If you have a specific feature you want to toggle, toggle that one, not "all features off".

Also safe rule: the shaper reads `init`/`medi`/`fina`/`isol` *automatically*. You almost never need to mention them in `font-feature-settings`. Do not attempt to force them on or off — the shaper will mis-select forms if you interfere.

### 2. Never `letter-spacing` Arabic

```css
/* WRONG */
.headline {
  letter-spacing: 0.05em;
}
```

Arabic letters *connect*. Adding letter-spacing inserts a gap between every pair of letters, breaking joins and producing disconnected, visually broken text.

If your stylesheet applies letter-spacing globally, scope it:

```css
.headline {
  letter-spacing: 0.05em;
}
:lang(ar) .headline,
:lang(fa) .headline,
:lang(ur) .headline,
:lang(ps) .headline {
  letter-spacing: 0;
}
```

Or, better, only apply `letter-spacing` in Latin-specific selectors.

### 3. `text-transform: uppercase` is a no-op but a smell

Arabic has no letter case. `text-transform: uppercase` changes nothing. It is not an error — it is wasted cognition and signals the stylesheet was written Latin-first. Remove it from shared component CSS; apply it only to Latin-scoped styles.

### 4. Justification: prefer ragged

Do not set `text-align: justify` for Arabic body text expecting good kashida behavior. Browser support is spotty (2026-04); most engines justify by expanding word-space only, producing rivers, or insert crude tatweel. Use:

```css
[dir="rtl"] p {
  text-align: start;           /* = right in RTL */
  text-wrap: pretty;           /* if supported */
}
```

For headlines that need visual justification, do it in the design tool and ship the finished artwork (or a `font-variation-settings: "wdth"` width-axis micro-adjustment, if the font has a width axis).

### 5. Line-height: unitless, generous

```css
:lang(ar) { line-height: 1.7; }
:lang(fa) { line-height: 1.7; }
:lang(ur) { line-height: 2.2; }   /* Nastaliq */
```

Unitless inheritance is essential for bilingual documents.

### 6. Variable-font support for Arabic is uneven

Cairo Variable has `wght`. Some newer Arabic families ship `wght` and `slnt` or `wght` and `wdth`. The variable-font story is *not* as mature for Arabic as for Latin (2026-04). When in doubt, use the static-weight family.

### 7. Digit locale switching is a content decision

If your product shows "١٢٣" or "123" is not a CSS setting. Format numbers with `Intl.NumberFormat("ar-EG", { ... })` (Arabic-Indic) or `Intl.NumberFormat("ar-MA", { ... })` (European, Maghreb default) depending on the audience. Or, store the target digit system with the content.

### 8. Watch out for `white-space: nowrap` on Arabic

Combined with Nastaliq's wide-word-height behavior, `nowrap` can produce rows whose visual height is 3× neighbor rows. Verify that `nowrap` is genuinely what you want for the RTL locale.

### 9. Cross-script fallback stacks

```css
:lang(ar) {
  font-family:
    "Noto Naskh Arabic",           /* primary */
    "Amiri",                       /* secondary */
    /* system Arabic fallbacks: */
    "Geeza Pro",                   /* macOS */
    "Tahoma",                      /* Windows */
    sans-serif;
  line-height: 1.7;
}
```

Ordering matters. Browsers walk the stack until they find a glyph for each code point. A stack that lists a Latin font *before* an Arabic font will still use the Arabic font for Arabic code points (good) — but cap/x-height mismatches in fallback hurt. Prefer separate `:lang()`-scoped families.

### 10. `::first-letter` and `initial-letter`

These work per code point, but "first letter" of an Arabic word is the rightmost letter visually, not the first char in memory. Drop-caps for Arabic have a deep typographic tradition (particularly in illuminated Qurans) that does not map cleanly to `::first-letter`. Hand-craft display initials if you need them.

### 11. `generic(nastaliq)` is coming but not here

CSS Fonts 4 defines `generic(nastaliq)` for Urdu-language content. Not widely shipped in 2026-04 — progressively enhance, don't rely on it.

---

## Writing in Code

### Encoding

**UTF-8 always.** Any other encoding of Arabic content is a decade-old mistake. Make sure source files, HTTP responses, and database columns are all UTF-8.

### Logical vs visual order

Arabic is stored in *logical* order: the first typed/read character is first in the byte stream, even though it renders on the right. This matches how screen readers and search engines process text.

**Pitfall.** Some legacy systems stored Arabic in *visual* order (literally reversing the bytes so the first-rendered character is first in memory). This is wrong, still exists in the wild, and must be normalized before display. Indicators: text looks correct only when copied into a non-bidi-aware context; RTL markup renders it backwards.

### IDEs and editors

VS Code, JetBrains IDEs, and modern text editors handle bidi correctly. Watch for:

1. **Caret direction.** In a mixed-direction line, the caret jumps visually when you cross a direction boundary, even though it is walking the logical order. This is correct behavior but disorienting the first time.
2. **Line reversal on copy.** Copying a selection that crosses direction boundaries can produce visually reordered results on paste depending on the target app's bidi handling. Paste into a bidi-aware editor (not Notepad).
3. **Selection boundaries.** Selection in mixed-direction text can look discontinuous. Again, correct per UBA.
4. **Arabic in comments / source strings.** Safe and UTF-8; but be wary of RTL override characters (U+202E LEFT-TO-RIGHT OVERRIDE and friends) injected into code — a class of security issue ("Trojan Source", CVE-2021-42574). Most linters now flag these.

### Source strings (i18n)

Use ICU MessageFormat or equivalent for Arabic/Persian/Urdu plurals — these languages have plural rules different from English (Arabic has 6 plural categories: zero, one, two, few, many, other; Persian has 2; Urdu has 2). Do not concatenate strings; do not assume "plural = +s". Cross-ref `../../ui-verify-i18n`.

---

## Accessibility

### Screen readers

- **VoiceOver** (macOS, iOS) — strong Arabic support; switches voices based on `lang` attribute if Arabic voices are installed
- **NVDA** (Windows) — Arabic support via eSpeak or Microsoft voices; requires a language pack
- **JAWS** — commercial; Arabic support depends on installed language packs
- **TalkBack** (Android) — relies on Google TTS; Arabic voice quality has improved but varies by device

**Required for screen readers to work well.** Set `lang="ar"` (or `lang="fa"`, `lang="ur"`) on the HTML element or section. Without it, the reader either reads Arabic with a Latin voice (nonsense) or fails silently. Use the correct BCP-47 subtag for dialect when it matters (`ar-EG` Egyptian, `ar-SA` Saudi, `ar-MA` Moroccan) — voice quality and pronunciation differ.

### Diacritics and cantillation

Vocalized Quranic text includes cantillation marks (tajweed) that indicate recitation rules. Screen readers typically ignore these (they are pronunciation guidance, not phonetic content), which is usually correct for accessibility — but in a Quranic app, you may need a specialized reader that respects them.

Vocalized educational text (children's books, language-learning) expects the reader to pronounce the short vowels. Most high-quality Arabic TTS voices handle vocalized text correctly.

### Contrast and size

WCAG contrast rules apply normally, but Arabic's thin horizontal strokes (especially in connecting segments) can fall below readable contrast faster than Latin at the same measured ratio. Err on the side of higher contrast and slightly larger size for Arabic — empirically, Arabic readers are comfortable with text set a bit larger than its Latin equivalent.

### Quranic text as a special case

Quran presentation has its own typographic tradition (specific layouts, page turns at verse boundaries, marked divisions into hizb/juz, verse-number glyphs). For Quranic apps, use a proper Quran-aware library or ship images of a typeset edition (e.g. the King Fahd Complex Mus'haf). Don't roll it yourself from bare Unicode.

---

## Anti-patterns

Named failure modes to watch for in a codebase or review.

- **"RTL flip."** Treating Arabic support as "swap all the left-margins to right-margins" and declaring victory. Misses shaping, leading, fonts, numerals, punctuation, and is insulting.
- **Letter-spacing leak.** A designer sets `letter-spacing: 0.02em` on body/heading tokens; Arabic breaks in production; nobody notices until an Arabic user complains. Prevent by scoping `letter-spacing` to `:lang(latin)` or similar, or zeroing it in RTL branches.
- **Ligature nuke.** Somebody sets `font-variant-ligatures: none` or `font-feature-settings: "liga" 0` at the root for a "clean" look; Arabic loses required ligatures (Lam-Alef most visibly).
- **Justify-and-hope.** `text-align: justify` applied globally; Arabic paragraphs develop rivers or crude tatweel. Prefer ragged.
- **Nastaliq served as Naskh.** No Nastaliq font declared; browser falls back to Naskh; Urdu content looks wrong to Urdu readers. Diagnose by checking the rendered font in DevTools.
- **Tatweel injection as cosmetic stretching.** Inserting U+0640 characters into content to "stretch" a word in a heading. Breaks search, breaks copy-paste, breaks reflow.
- **Arabic numerals assumed Arabic-Indic.** Hardcoding "use ١٢٣ for Arabic" without considering Maghreb (which uses European digits) or Persian (which uses U+06F0–06F9). Route through `Intl.NumberFormat`.
- **`?` in Arabic content.** Using ASCII `?` instead of `؟` in user-visible Arabic strings. Looks foreign to readers.
- **Font stack with no Arabic coverage.** `font-family: "Helvetica Neue", sans-serif` on an Arabic page: the browser falls back to some system Arabic font (which differs per OS, often poorly matching the Latin face). Declare an Arabic font explicitly.
- **`direction: rtl` without `lang="ar"`.** Visual direction flips but screen readers still read in English. Both are needed.
- **Fixed pixel line-heights on body copy.** `line-height: 22px` set for Latin; Arabic clips ascenders and diacritics. Use unitless line-height.
- **Hardcoded physical CSS properties.** `margin-left: 16px` everywhere means the RTL side of the product is "mostly right" and full of exceptions. Use logical properties from day one.

---

## Sources

Accessed 2026-04-17:

- W3C — *Arabic & Persian Layout Requirements* (ALReq): https://www.w3.org/International/alreq/
- W3C — *Arabic Script Gap Analysis*: https://www.w3.org/TR/alreq-gap/
- W3C — *Urdu Layout Requirements* (retired, points to arab-lreq): https://www.w3.org/TR/arab-ur-lreq/
- Unicode Consortium — *The Unicode Standard*, Chapter 9: Middle Eastern Scripts: https://www.unicode.org/versions/latest/ch09.pdf
- Google Fonts — Noto Naskh Arabic, Noto Kufi Arabic, Noto Nastaliq Urdu specimens: https://fonts.google.com/noto
- Amiri project — Khaled Hosny: https://www.amirifont.org/
- 29LT (Pascal Zoghbi): https://29lt.com/
- TypoArabic research-survey group, University of Reading: https://research-survey.reading.ac.uk/typoarabic/
- Titus Nemeth, *Arabic Type-Making in the Machine Age* (Brill, 2017) — book, not URL
- Khatt Foundation — *The Big Kashida Secret*: https://www.khtt.net/en/page/1821/the-big-kashida-secret
- Wikipedia — Kashida (corroborated against ALReq): https://en.wikipedia.org/wiki/Kashida
- WebKit Bug 6203 — Kashida justification: https://bugs.webkit.org/show_bug.cgi?id=6203

Additional depth (not cited inline):
- Hrant Papazian's writings on Nastaliq
- Mohamed Zakariya's essays on Arabic calligraphy and justification
- Adobe's Arabic and Hebrew type guide
- Monotype's Arabic design articles
