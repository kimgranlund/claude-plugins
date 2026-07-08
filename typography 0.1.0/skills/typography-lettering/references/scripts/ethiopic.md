---
date: 2026-04-18
coverage: stub
peers:
  - ./latin.md
  - ./arabic.md
  - ./devanagari.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/css-text-properties.md
primary_sources:
  - SIL International — Ethiopic writing systems documentation. https://scripts.sil.org/Ethiopic
  - W3C — Ethiopic Layout Requirements (draft, ongoing). https://www.w3.org/International/etlreq/
  - Unicode Consortium — *The Unicode Standard*, Chapter 19: Africa (Ethiopic section). https://www.unicode.org/versions/latest/
  - Unicode Chart — Ethiopic (U+1200–U+137F). https://www.unicode.org/charts/PDF/U1200.pdf
  - Unicode Chart — Ethiopic Supplement (U+1380–U+139F). https://www.unicode.org/charts/PDF/U1380.pdf
  - Unicode Chart — Ethiopic Extended (U+2D80–U+2DDF). https://www.unicode.org/charts/PDF/U2D80.pdf
  - Unicode Chart — Ethiopic Extended-A (U+AB00–U+AB2F). https://www.unicode.org/charts/PDF/UAB00.pdf
  - Google Fonts — Noto Sans Ethiopic specimen. https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic
  - Google Fonts — Noto Serif Ethiopic specimen. https://fonts.google.com/noto/specimen/Noto+Serif+Ethiopic
  - SIL International — Abyssinica SIL font. https://software.sil.org/abyssinica/
  - Writings of Worku Alemu and Daniel Yacob on Ethiopic encoding and typography (primary sources to follow via the EthiopiaTypography / Ge'ez Frontier Foundation archive).
notes:
  - This file is *stub* tier. The writer's direct experience with Ethiopic typography is limited; the content below is a starting overview plus pointers to authoritative sources. Do not treat it as a substitute for consulting SIL, the W3C Ethiopic Layout Requirements draft, or native-reader review when shipping Ethiopic content.
  - Peer script files (./latin.md, ./arabic.md, ./devanagari.md) are the voice model: direction declaration up front, fundamentals, specifics, CSS gotchas, anti-patterns, pointers. This stub follows the pattern but at reduced depth.
---

# Ethiopic script — typography reference (stub)

**Scope disclaimer.** This is a *stub-tier* reference. The writer's exposure to production Ethiopic typography is limited, and the content here is a practitioner-level overview adequate for "don't ship something actively broken" — not adequate for deep editorial typography decisions in Amharic, Tigrinya, or Ge'ez. For depth, consult SIL International's Ethiopic documentation, the W3C Ethiopic Layout Requirements (draft), Unicode Standard Chapter 19, and native-reader review. The *Common traps* and *Anti-patterns* sections capture the mistakes most non-Ethiopic teams actually make; trust them and route editorial decisions to specialists.

**What the script is.** Ethiopic — also called **Ge'ez script** or **Fidel** (ፊደል, "alphabet" / "letter") — is the writing system used for Amharic (አማርኛ), Tigrinya (ትግርኛ), Tigre, Ge'ez (the liturgical language of the Ethiopian Orthodox Tewahedo Church), Oromo (partially), and several other languages of Ethiopia and Eritrea. It is an **abugida** (syllabic alphabet): each character represents a consonant-plus-vowel syllable, with seven vowel forms per base consonant derived by systematic modification of the base glyph.

---

## Script overview

- **Type:** Abugida (syllabic alphabet / alphasyllabary).
- **Direction:** Left-to-right, same as Latin.
- **Connectivity:** Non-cursive. Characters are drawn discretely, without connecting strokes between adjacent syllables. There is no equivalent of Arabic's contextual shaping or Devanagari's conjunct formation.
- **Inventory:** Approximately **270 base characters** in the core Unicode block, expanding to roughly **380** with extended ranges.
- **Unicode blocks:**

  | Block | Range | Contents |
  |---|---|---|
  | Ethiopic | U+1200–U+137F | Core Amharic / Tigrinya / Ge'ez syllables, numerals, punctuation. |
  | Ethiopic Supplement | U+1380–U+139F | Additional characters. |
  | Ethiopic Extended | U+2D80–U+2DDF | Extensions for Sebatbeit and other regional languages. |
  | Ethiopic Extended-A | U+AB00–U+AB2F | Further extensions (Tigrinya and additional African languages). |
  | Ethiopic Extended-B | added in Unicode 14.0 (2021), U+1E7E0 range | Most recent extension. |

- **Numerals:** Ethiopic has a dedicated set of numeric glyphs at U+1369–U+137C, distinct from Western Arabic digits. Traditional Ethiopic numerals do not include a zero; modern usage commonly substitutes Western Arabic digits (0–9) for technical, financial, and scientific contexts.

---

## Origin

Ethiopic evolved from the **South Arabian script** beginning around the 4th century CE, in the **Kingdom of Aksum** (in the territory of modern Ethiopia and Eritrea). The script was codified and standardised under **King Ezana's conversion to Christianity** in the mid-4th century, associated with the missionary activity of Frumentius. Ge'ez as a spoken language ceased to be in wide daily use by roughly the 13th century, but it retained — and retains — a liturgical and literary role in the Orthodox Tewahedo tradition analogous to Latin in Roman Catholicism or Classical Arabic in Islam.

The vowel-modification pattern (seven vowel orders per base consonant) was developed within the Aksumite period and differs from earlier South Arabian practice, which was a pure consonantal abjad. Ethiopic is therefore one of the oldest living scripts with continuous use in religious, literary, and everyday contexts.

---

## Structural features

- **Consonant base + seven vowel orders.** Each of the ~26 primary consonant families appears in seven forms corresponding to the vowels **ä** (inherent / first order), **u**, **i**, **a**, **é**, **ə** (schwa / sixth order), **o**. Vowel distinction is shown by a consistent set of modifications — typically strokes, loops, or small additions at specific positions relative to the base consonant.
- **Labiovelar consonants.** A secondary series adds labialised forms (e.g., *kwa*, *gwa*) that combine a labiovelar consonant with a vowel. These expand the inventory beyond the core 26 × 7.
- **Square syllabic blocks.** Each syllable renders as a visually balanced square-to-rectangular glyph. Unlike Devanagari, there is no head-line (shirorekha); unlike Arabic, there is no cursive join. Each syllable stands alone optically.
- **Punctuation.** Ethiopic has a dedicated punctuation set:

  | Glyph | Unicode | Role |
  |---|---|---|
  | ፡ | U+1361 | Ethiopic word separator ("wordspace") — two vertical dots, historically used between words instead of a blank space. |
  | ። | U+1362 | Full stop — four dots arranged in a square. |
  | ፣ | U+1363 | Comma. |
  | ፤ | U+1364 | Semicolon. |
  | ፥ | U+1365 | Colon. |
  | ፦ | U+1366 | Preface colon — used in lists and to introduce a following clause. |
  | ፧ | U+1367 | Question mark. |
  | ፨ | U+1368 | Paragraph separator / exclamation-adjacent mark. |

- **No case distinction.** Ethiopic does not distinguish uppercase and lowercase; CSS `text-transform: uppercase` / `lowercase` / `capitalize` is a no-op.

---

## Writing direction and word separation

Ethiopic is written **left-to-right**, like Latin. There is no cursive connection between adjacent characters, so there is no shaping complexity comparable to Arabic and no reordering complexity comparable to Devanagari. The base layout engine can treat Ethiopic much like Latin for line-breaking and paragraph wrapping.

**Word separation.** Historically, Ethiopic used the *wordspace* (U+1361, ፡) — two vertical dots — between words, not a blank space. Modern Amharic and Tigrinya writing has largely shifted to conventional Latin-style spaces (U+0020) for word separation, but the wordspace still appears in:

- Religious and liturgical Ge'ez texts.
- Traditional editorial typography.
- Some Eritrean publications.
- Transliteration and scholarly editions.

Modern web content in Amharic and Tigrinya almost always uses plain spaces. If your content pipeline receives text with wordspaces and the target audience expects plain spaces (or vice versa), normalise at the content-processing stage, not in CSS.

---

## Font support landscape (2026-04)

A short list of fonts with competent Ethiopic coverage. As of 2026-04, Ethiopic web-font options remain thinner than for Latin, Arabic, or Devanagari — but the principal production choices are well established.

| Font | Source | Notes |
|---|---|---|
| **Noto Sans Ethiopic** | Google / Monotype | Broad coverage, open source, variable-weight version available. The sane default for web use. |
| **Noto Serif Ethiopic** | Google / Monotype | Serif companion; better for long-form prose. |
| **Abyssinica SIL** | SIL International | Strong diacritical and extended-block support, open licence (SIL OFL). Preferred for scholarly and linguistic work. |
| **Nyala** | Microsoft | Default Ethiopic UI font on Windows since Vista. Adequate for UI, visually dated. |
| **Kefa** | Apple | Default Ethiopic system font on macOS and iOS. Solid for UI. |
| **Ebrima** | Microsoft | Windows 8+ alternative; covers several African scripts including Ethiopic. |
| **Washra (various)** | Various foundries | Traditional-style Ethiopic display faces; rare in web delivery. |

For production use, **Noto Sans Ethiopic** and **Abyssinica SIL** are the usual picks. System fallbacks (Nyala, Kefa) render correctly but produce visually different results across platforms.

---

## CSS considerations

A short list of practitioner rules. The general pattern is closer to Latin than to Arabic or Devanagari — Ethiopic does not require shaping features, does not have case, does not have cursive joins.

```css
:lang(am), :lang(ti), :lang(gez) {
  font-family:
    "Noto Sans Ethiopic",
    "Abyssinica SIL",
    "Nyala",                /* Windows system fallback */
    "Kefa",                 /* macOS system fallback */
    system-ui,
    sans-serif;
  line-height: 1.5;
  letter-spacing: 0;
}
```

**Language attributes.** Use `lang="am"` (Amharic), `lang="ti"` (Tigrinya), or `lang="gez"` (Ge'ez). Setting the correct BCP-47 tag helps the font's `locl` table select appropriate glyph variants where they exist (Noto Sans Ethiopic has some language-specific tuning) and helps screen readers pick the right TTS voice.

**Line-height.** Ethiopic glyphs are visually dense but do not stack diacritics the way Devanagari does, and they do not elongate with kashidas the way Arabic does. Line-height in the 1.4–1.6 range (unitless) is adequate for body prose; more for display. Less stacked-mark pressure than Thai or Devanagari.

**Letter-spacing.** Default or minimal. Ethiopic does not use cursive connections that `letter-spacing` would break (unlike Arabic or Devanagari), and the script is not especially sensitive to tracking adjustments. A small positive letter-spacing is acceptable for headlines but unnecessary for body.

**No shaping hazards.** Unlike Arabic and Devanagari, Ethiopic does not require OpenType shaping features (`init`/`medi`/`fina`/`isol`, `liga`, `rphf`, `akhn`, `cjct`, etc.) to render correctly. Disabling standard ligatures or setting `font-feature-settings: "liga" 0` does not break Ethiopic text the way it breaks Arabic or Devanagari.

**No bidi.** Ethiopic is LTR. No `dir="rtl"`, no bidi complexity. Mixed Ethiopic + Latin content renders straightforwardly via the Unicode Bidirectional Algorithm.

**Use Ethiopic punctuation in Ethiopic content.** Substituting Latin `.` for Ethiopic `።` or Latin `,` for ፣ is a locale-content error visible to readers. Pipelines that produce Ethiopic text should emit the Ethiopic punctuation set unless the target publication's house style explicitly uses Latin punctuation.

---

## Unicode challenges

- **Numerals.** Ethiopic has a dedicated numeric set (U+1369–U+137C). No zero in traditional Ethiopic; the system is not positional in the Indo-Arabic sense. Modern usage almost universally mixes Western Arabic digits for technical, financial, and scientific data; Ethiopic numerals appear in traditional, historical, and religious contexts.
- **Language-specific extensions.** Some characters for Tigrinya, Sebatbeit, and other regional languages live in the Extended blocks (U+2D80+, U+AB00+). Older fonts and older system installations may lack these blocks; verify glyph coverage against your content's actual codepoint set, not against the font's claimed "Ethiopic support."
- **Combining marks.** Some combining marks were added in relatively recent Unicode updates. Older fonts may not position them correctly.
- **Tone marks (for Semitic-language scholarly work).** Limited in the core block; full scholarly-edition support may require specialist fonts.

---

## Why this skill covers Ethiopic as stub

Three reasons:

1. **Writer exposure.** The writer has not shipped production-scale Ethiopic typography and has not conducted native-reader validation on Ethiopic-language content. Stub-tier coverage is honest; pretending deeper coverage would risk propagating misunderstandings.
2. **Global typography obligation.** A typography skill that covers only Latin and a handful of "big" non-Latin scripts (Arabic, Devanagari, CJK) implicitly marginalises readers of other scripts. Stub-tier coverage acknowledges the script as a first-class concern while honestly delimiting the depth of the current reference.
3. **Deference to authoritative sources.** The SIL International / W3C / Unicode authors and Ethiopic-script native researchers (Worku Alemu, Daniel Yacob, others in the Ge'ez Frontier Foundation tradition) are the right references for substantive Ethiopic typography decisions. Pointing readers there is more useful than producing a second-hand summary.

---

## Pointers to deeper external sources

For serious Ethiopic typography work, consult:

- **SIL International's Ethiopic documentation** — https://scripts.sil.org/Ethiopic. The most comprehensive practitioner-level reference, covering encoding, fonts, keyboard layouts, and regional variants.
- **W3C Ethiopic Layout Requirements** (draft, ongoing) — https://www.w3.org/International/etlreq/. The living document for how Ethiopic should render on the web. Edits accumulate; track the latest editor's draft for authoritative guidance.
- **Unicode Standard, Chapter 19 (Africa)** — the primary reference for the encoding rationale, block organisation, and character semantics. https://www.unicode.org/versions/latest/
- **Unicode charts** — https://www.unicode.org/charts/PDF/U1200.pdf (Ethiopic), plus the Supplement / Extended / Extended-A charts linked in the primary sources.
- **Worku Alemu's and Daniel Yacob's writings** — foundational work on Ethiopic Unicode encoding, localisation, and typography. The Ge'ez Frontier Foundation archive and the Ethiopic Research Partnership publications are the principal collections.
- **Ethiopian Software Development Program (Addis Ababa University)** — research-survey and practitioner work on Ethiopic software and typography from within Ethiopia.
- **Abyssinica SIL documentation** — https://software.sil.org/abyssinica/. The font comes with substantial documentation on Ethiopic typographic conventions.
- **Noto Ethiopic specimens** — https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic and the serif counterpart.

---

## Common traps

The mistakes non-Ethiopic teams most often make, in the order they tend to surface:

1. **Treating Ethiopic as "similar to Arabic" because both are Afro-Asiatic Semitic.** Structurally they are unrelated writing systems. Ethiopic is LTR, non-cursive, with no contextual shaping. Arabic is RTL, cursive, with four-form contextual shaping. Don't apply Arabic's CSS rules (`direction: rtl`, Arabic font stacks, bidi handling) to Ethiopic content.

2. **Assuming Noto Sans (the Latin/Cyrillic Noto family) covers Ethiopic.** It does not. Ethiopic is served by a separate Noto family: **Noto Sans Ethiopic**. Include it explicitly in the font stack.

3. **Using Latin period `.` where Ethiopic full stop `።` is expected.** Readers notice; locale pipelines should emit the Ethiopic punctuation set unless house style overrides.

4. **Mixing Ethiopic numerals and Western Arabic digits inconsistently in the same document.** Pick one system and stay consistent within a content region. Technical Amharic content typically uses Western Arabic digits throughout; traditional Ge'ez liturgical content uses Ethiopic numerals.

5. **Omitting `lang` attributes.** `lang="am"`, `lang="ti"`, or `lang="gez"` matters for screen-reader voice selection and for the (few) fonts with Ethiopic `locl` tables. Without `lang`, SRs may try to read Ethiopic with a Latin voice, producing nonsense.

6. **Applying `text-transform: uppercase` globally.** Ethiopic has no case. The transform is a no-op for Ethiopic content but signals that the stylesheet was written Latin-first; scope case transforms to Latin-containing elements.

7. **Hardcoded `letter-spacing` from a Latin-centric UI token.** Ethiopic tolerates small positive letter-spacing better than Arabic or Devanagari, but large values (> 0.05em) still look wrong. Either zero `letter-spacing` for `:lang(am)`, `:lang(ti)`, `:lang(gez)` selectors, or keep the default small.

8. **Assuming a "multilingual" font covers Ethiopic.** Many commercial multilingual fonts cover Latin Extended, Cyrillic, Greek, and sometimes Arabic — but omit Ethiopic. Verify coverage before committing; a pan-African font release is much rarer than a pan-European one.

9. **Shipping without QA by a native reader.** Even competent coverage has pitfalls: regional variant preferences (Ethiopian vs Eritrean), religious-text typographic conventions (Ge'ez liturgical layout), traditional vs modern punctuation. If the content matters, route the typography decisions through an Amharic- or Tigrinya-reading reviewer.

---

## Typographic traditions (briefly)

Traditional Ethiopic calligraphic hands have regional and period variations — **Gondarine**, **Shewan**, and other schools — associated with specific scribal traditions, paper types, and religious uses. Modern printing standardised the letterforms during the 20th century, and digital standardisation via Unicode (1990s onward) further narrowed variation. Contemporary web typography for Amharic and Tigrinya works within the standardised forms; the older calligraphic traditions are matters for specialist scholarly, religious, and artistic work, beyond this stub's scope.

Religious texts in the Orthodox Tewahedo tradition retain a strong hand-calligraphic and illuminated-manuscript style, with specific layout conventions (column structure, rubrication, marginal commentary) that do not translate directly to web typography. Projects working on digital editions of Ge'ez liturgical texts should consult specialist palaeography and Ethiopic manuscript studies.

---

## Sources

Accessed 2026-04-18 where URLs are cited.

- **SIL International.** *Ethiopic / Ge'ez Writing System.* https://scripts.sil.org/Ethiopic
- **SIL International.** *Abyssinica SIL font documentation.* https://software.sil.org/abyssinica/
- **W3C.** *Ethiopic Layout Requirements* (Editor's Draft). https://www.w3.org/International/etlreq/
- **Unicode Consortium.** *The Unicode Standard, Chapter 19: Africa.* https://www.unicode.org/versions/latest/
- **Unicode Consortium.** *Ethiopic (U+1200–U+137F)* chart. https://www.unicode.org/charts/PDF/U1200.pdf
- **Unicode Consortium.** *Ethiopic Supplement (U+1380–U+139F)* chart. https://www.unicode.org/charts/PDF/U1380.pdf
- **Unicode Consortium.** *Ethiopic Extended (U+2D80–U+2DDF)* chart. https://www.unicode.org/charts/PDF/U2D80.pdf
- **Unicode Consortium.** *Ethiopic Extended-A (U+AB00–U+AB2F)* chart. https://www.unicode.org/charts/PDF/UAB00.pdf
- **Google Fonts.** Noto Sans Ethiopic specimen. https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic
- **Google Fonts.** Noto Serif Ethiopic specimen. https://fonts.google.com/noto/specimen/Noto+Serif+Ethiopic
- Writings of **Worku Alemu** and **Daniel Yacob** on Ethiopic encoding, localisation, and web typography (collected across the Ethiopic Research Partnership and Ge'ez Frontier Foundation archives).
- Ethiopian Software Development Program, Addis Ababa University — publications on Ethiopic computing and typography.

Additional depth (not cited inline; recommended as further reading):

- *The Ge'ez Writing System* in standard reference works on Semitic scripts (Daniels & Bright, *The World's Writing Systems*, 1996, Chapter 41).
- Ethiopian Orthodox Tewahedo Church publications on liturgical text layout (traditional / religious scope).
- University of Hamburg *Ethiopian Studies* publications on manuscript traditions (scholarly / palaeographic scope).
