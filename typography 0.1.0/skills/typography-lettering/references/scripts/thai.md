---
date: 2026-04-18
coverage: medium
peers:
  - ./devanagari.md
  - ./cjk-han.md
  - ./latin.md
  - ../metrics/metric-compatibility.md
  - ../contemporary/css-text-properties.md
  - ../contemporary/opentype-features.md
primary_sources:
  - https://www.unicode.org/charts/PDF/U0E00.pdf
  - https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-16/
  - https://www.w3.org/International/sealreq/ (W3C Southeast Asian Layout Requirements)
  - https://www.w3.org/TR/sea-gap/ (W3C Southeast Asian Gap Analysis)
  - https://www.orst.go.th/ (Royal Society / Royal Institute of Thailand)
  - https://www.cadsondemak.com/ (Cadson Demak foundry)
  - https://www.unicode.org/reports/tr14/ (UAX #14 Line Breaking)
  - https://unicode-org.github.io/icu/userguide/boundaryanalysis/ (ICU BreakIterator)
  - https://learn.microsoft.com/en-us/typography/script-development/thai (Microsoft Thai shaping)
  - https://fonts.google.com/noto/specimen/Noto+Sans+Thai
  - Gerry Leonidas, *Thai typography — a preliminary survey* (University of Reading, Department of Typography)
  - Virunpath Vacharaprusadee / Cadson Demak writings on modern Thai type
---

# Thai Script Typography

**Scope disclaimer.** This is a *practitioner-medium* reference for a web/UI typographer who has never set Thai before. It covers enough to ship Thai body text competently and to diagnose the common rendering and spacing mistakes, but it is not scholar-depth. Authoritative depth lives in the W3C's *Southeast Asian Layout Requirements* and *Gap Analysis*, the Unicode Standard Chapter 16, Microsoft Typography's Thai script-development guide, and Gerry Leonidas's Reading-department survey of Thai type. The Royal Society (former Royal Institute) of Thailand remains the orthographic authority for Thai itself.

**Why Thai is easy to misread as "Latin with exotic letters."** Thai is LTR, its Unicode block has been stable since Unicode 1.0, and it uses spaces (for clauses, not words) — so naive implementations assume Latin-ish text and ship. They ship broken. Thai glyphs stack up to three levels vertically above the base consonant, Thai has **no word spaces** so line-breaking needs dictionary segmentation, and Thai is acutely sensitive to `letter-spacing` because positive tracking destroys the intra-syllable mark-to-base relationship. The common failure mode is a Thai line-height that clips the top row of tone marks — invisible to the Latin-native developer, instantly broken to a Thai reader.

**What this file covers.** Script origin (Sukhothai 1283 and the Brahmic pedigree). Inventory (consonants, vowel signs, tone marks, digits). The three-level mark stack and why line-height budgets matter. Loop vs loopless style traditions. The word-segmentation problem and UAX #14 / ICU / browser behavior. Mixing Thai with Latin (metric-matched pairings). Notable fonts by role. CSS recipes. Common traps.

---

## Origin

Thai script first appears in the **Ramkhamhaeng Inscription** of 1283 CE, a stone stele from the kingdom of Sukhothai conventionally attributed to King Ramkhamhaeng. The script is a localization of **Old Khmer**, which in turn descends from **Pallava**, a South Indian Brahmic script that spread across mainland and maritime Southeast Asia with Indic religious and administrative culture in the first millennium CE. Thai therefore sits in a typological family with Khmer, Lao, Burmese (Myanmar), Balinese, Javanese, and Devanagari — all **Brahmi-derived abugidas**, all with consonant-carries-inherent-vowel logic, all with stacked vowel and diacritic marks.

The modern printed form stabilized in the **mid-19th century** as Thai presses (beginning with D. B. Bradley's 1836 press in Bangkok) standardized the letter shapes now considered "traditional." The Royal Society of Thailand (ราชบัณฑิตยสภา, formerly the Royal Institute) publishes the official dictionary and orthography and remains the prescriptive authority for Thai spelling, romanization, and approved abbreviations.

Two script-family notes that matter for typography:

- **Shared descender/ascender budget.** Thai, Khmer, Lao, and Myanmar all demand larger line-height than Latin because they stack marks above and (sometimes) below the consonant. Designing a Latin+Thai hybrid layout requires budgeting for Thai's three-level stack even if the Latin itself doesn't need it.
- **Shared no-word-space convention.** Thai, Lao, and Khmer write without spaces between words; Burmese is mixed. Line-breaking in all these scripts requires dictionary segmentation.

Cross-reference: `./devanagari.md` on the broader Brahmic-abugida logic (inherent vowels, matras, halant/virama). Thai diverges in that it writes vowels *around* the consonant without a halant-style suppression marker — the abugida logic is there but the encoding is different from Devanagari's.

---

## Inventory

Thai Unicode lives in the block **U+0E00–U+0E7F** (128 codepoints; U+0E00 is unassigned, a well-known historical artifact of keeping Thai and Lao at parallel offsets). Coverage:

| Category | Count | Unicode range | Examples |
|----------|-------|---------------|----------|
| Consonants (พยัญชนะ) | 44 (42 in modern use; 2 obsolete: ฃ ฅ) | U+0E01–U+0E2E | ก ข ค ง จ ฉ ช ซ ญ ฎ ฏ ฐ ฑ ฒ ณ ด ต ถ ท ธ น บ ป ผ ฝ พ ฟ ภ ม ย ร ล ว ศ ษ ส ห ฬ อ ฮ |
| Vowel signs (สระ) | 18 dependent + 10 independent-ish; ~28 including compound forms | U+0E30–U+0E4E (mixed with other marks) | ะ า ิ ี ึ ื ุ ู เ แ โ ใ ไ |
| Tone marks (วรรณยุกต์) | 4 | U+0E48–U+0E4B | ◌่ (mai ek) ◌้ (mai tho) ◌๊ (mai tri) ◌๋ (mai chattawa) |
| Other diacritics | 4 | U+0E4C–U+0E4F | ◌์ (thanthakhat / karan, silencer) ◌ํ (nikhahit, nasalization) ◌๎ (yamakkan, rare Pali) ๏ (fongman, ornamental) |
| Digits (เลขไทย) | 10 | U+0E50–U+0E59 | ๐ ๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙ |
| Symbols | 5 | U+0E2F, U+0E3F, U+0E46, U+0E5A, U+0E5B | ฯ (paiyannoi) ฿ (baht) ๆ (mai yamok) ๚ (angkhan) ๛ (khomut) |

**Typological label.** Thai is formally an **abugida**: each consonant carries an inherent short-`a` (or short-`o` depending on phonological context), and vowels modify that inherent sound. Unlike Devanagari, Thai does not use a single halant/virama; vowel-suppression is handled by spelling conventions and by the **thanthakhat** silencer ◌์ which marks a final consonant as unpronounced (typical in loanwords like เบนซ์ "Benz").

**Two obsolete consonants.** ฃ (U+0E03, kho khuat) and ฅ (U+0E05, kho khon) are historical letters no longer used in modern Thai; they appear only in dictionaries and historical linguistic literature. Fonts still ship them — Unicode slots are permanent.

**Unicameral.** Thai has no case distinction. `text-transform: uppercase | lowercase | capitalize` has no visual effect. Do not rely on case as an emphasis or hierarchy device.

**Bidi.** Thai is LTR. No special `direction` handling. Bidi only enters when Arabic or Hebrew content is mixed in — handled by the Unicode Bidirectional Algorithm the same as for Latin.

---

## The Three-Level Mark Stack

This is the single structural feature that separates Thai typography from Latin-like scripts in practical terms.

A Thai syllable can stack up to three levels of marks vertically above the base consonant, plus one level below. The four-level total is what determines line-height requirements.

### The levels

1. **Base level (on the body-line).** Consonant + in-line vowels (ะ, า, ำ, อ, ๐–๙ digits). These occupy the consonant's "x-height" zone plus a small ascender for consonants with vertical risers (ป, ฝ, ฟ, ฬ).
2. **Above-base (first level up).** Upper vowels ◌ิ ◌ี ◌ึ ◌ื (short-i, long-ii, short-ue, long-uue) and the nikhahit ◌ํ.
3. **Above-base (second level up).** Tone marks ◌่ ◌้ ◌๊ ◌๋ and the thanthakhat ◌์. When an upper vowel is also present, the tone mark **raises** to sit above the vowel — this is where OpenType positioning does the work.
4. **Below-base.** Lower vowels ◌ุ ◌ู (short-u, long-uu) and the phinthu ◌ฺ (rare, Pali).

### Example

The syllable **กิ่** (ko kai + short-i + mai ek) logically encodes as `U+0E01 U+0E34 U+0E48`. In rendering:

- ก sits on the baseline
- ิ (short-i) sits above the shirorekha-equivalent of ก
- ่ (mai ek) sits *above* ิ — raised to clear the vowel

Without the vowel, **ก่** (`U+0E01 U+0E48`) would place the tone mark directly above ก — one level up. With the vowel intervening, the tone mark moves to the second level. This is controlled by the OpenType **`mark`** and **`mkmk`** GPOS positioning tables: `mark` positions the first diacritic to the base, `mkmk` positions a diacritic relative to another diacritic. Any production Thai font implements both; absence of `mkmk` produces colliding marks.

### Line-height consequence

This is the most common Thai typography bug on the web. The top of a tone mark sits roughly **one x-height above the consonant body** — sometimes more, depending on font. Latin-default `line-height: 1` or even `line-height: 1.2` *clips the top row of marks on the first line of any block*, because the line-box height allocated by the browser doesn't accommodate what the font actually renders.

Practical targets:

| Context | Latin | Thai |
|---------|-------|------|
| UI chrome / small labels | 1.2–1.35 | 1.5–1.6 |
| Body prose | 1.4–1.55 | 1.6–1.8 |
| Generous editorial body | 1.5–1.65 | 1.75–2.0 |
| Display (large sizes) | 1.0–1.15 | 1.3–1.5 |

**WCAG 2.2 SC 1.4.12 specifies a minimum 1.5× line-height floor.** For Thai, treat 1.5 as the absolute floor — not a target. 1.6–1.8 is the working range for readable body. See `../accessibility/wcag-type.md` for the accessibility framing.

A classic symptom of under-budgeted line-height in Thai: on a multi-line paragraph, the *first* line's tone marks appear clipped but subsequent lines render correctly. This is because the browser's first line-box is constrained by the containing element's content-box, while subsequent lines get the full `line-height` allocation. Setting `line-height: 1.7` (unitless) on the containing block fixes both.

---

## Font Metrics and Latin Pairing

Thai fonts typically declare a **larger ascender region** in their `hhea`/`OS/2` tables than Latin equivalents, precisely to accommodate the stacked marks. This has second-order consequences when mixing Thai with Latin:

- A Thai x-height-equivalent (the height of the consonant body) is roughly the height of a Latin lowercase — so Thai "feels" as tall as Latin lowercase at the same point size. But the marks above push the perceived height higher, and Latin caps sit *between* Thai consonant-top and Thai upper-vowel-top. The result: Latin can look small next to Thai at the same `font-size`.
- Conversely, a Thai sized to match Latin cap-height will feel oversized because of the mark-stack above.

The design answer is **metric-matched Latin companions**. A well-built Thai type family ships a Latin cut whose cap-height and x-height are tuned to sit comfortably alongside the Thai at the same point size. Examples:

- **Noto Sans Thai** pairs with **Noto Sans** (shared design language, shared metrics).
- **Sarabun** (the Thai government's body-text font) ships matched Latin weights.
- **IBM Plex Sans Thai** pairs with **IBM Plex Sans**.
- **Prompt** (Cadson Demak) pairs with a matched Latin sans.
- **Bai Jamjuree** and **K2D** (Cadson Demak loopless cuts) ship Latin companions.

When pairing is not metric-matched, use `@font-face` **`size-adjust`** and **`ascent-override`** to harmonize. See `../contemporary/metric-overrides.md` for the computation. A common recipe when Latin looks small next to Thai:

```css
@font-face {
  font-family: "Inter Thai-Matched";
  src: local("Inter");
  size-adjust: 108%;           /* bump Latin to Thai's apparent size */
  ascent-override: 92%;         /* normalize line-box */
  descent-override: 24%;
}
```

Cross-ref: `../metrics/metric-compatibility.md` on measuring and overriding.

---

## Loop vs Loopless (Classical vs Modern)

Thai type splits into two stylistic camps, and mixing them in a single body text reads as a typographic mistake to Thai readers — the equivalent of mixing a serif and a sans for body prose in Latin.

### Loop style (มีหัว — "with heads")

The traditional and dominant form. Most Thai letters have small **circular loops** at one or more stroke termini — typically at the stroke entry point. These loops are the visual anchor that readers use to segment the character stream in the absence of word spaces, and Thai reading research-survey (Leonidas and others) treats them as load-bearing features rather than decoration.

Loop style is:

- The **default for body text**. Nearly all Thai newspapers, books, and government documents set in loop-style fonts.
- **Preferred by older readers** and for formal / educational contexts. The Thai Ministry of Education's preferred fonts are all loop-style.
- Slower to scan at display sizes but sustained at body sizes.

Examples: **Sarabun, Kanit** (with its loop-ful weights), **Angsana New, Cordia New, DilleniaUPC, EucrosiaUPC, FreesiaUPC, IrisUPC, JasmineUPC** (the UPC family, widely preinstalled on Windows), **Thonburi** (macOS/iOS system), **Ayuthaya**, **CS Chat Thai**, **TH Sarabun PSK** (another government-standard variant), **PSL Kanda**.

### Loopless style (หัวไม่มีห่วง — "without loop-heads")

Also called **modern**, **geometric**, or **display Thai**. The loops are absent; stroke terminals are cleanly cut, often aligned with Latin sans design language. The form emerged in the 1960s–70s for advertising and branding and accelerated from the 2000s as Thai type foundries began to build families that harmonize with Latin sans grotesques.

Loopless style is:

- **Common in display and contemporary branding**. Most new startup and lifestyle brands use loopless.
- **Harder for older readers**. Primary-school materials rarely use loopless; literacy researchers have argued the loops aid recognition at reading-novice stages.
- **Well-suited to small UI chrome** where readers scan rather than read, and where the Latin-sans-like appearance harmonizes with Latin UI.
- Associated with **youth-targeted, modern-branded, tech** content.

Examples: **Bai Jamjuree, K2D, IBM Plex Sans Thai** (the 2022 loopless cut), **Anakotmai, Prompt, Kanit** (its loopless cuts), **Noto Sans Thai Looped** vs **Noto Sans Thai** (Google ships both; the default Noto Sans Thai is loopless).

### Mixing is a mistake

A paragraph that sets its Thai body in loopless and a Thai callout in loop (or vice versa) reads as visually inconsistent — in the same way a Latin paragraph with a serif headline and a sans body-with-occasional-serif-word would. Pick one tradition per text role. If a product wants both a classical editorial voice and a modern UI voice, choose two *different* families within one tradition, not one family from each.

---

## Typographic Tradition and Legibility

The Royal Institute / Royal Society of Thailand's *Dictionary of the Royal Institute* (พจนานุกรม ฉบับราชบัณฑิตยสถาน, most recent major edition 2011 with rolling updates) is the authoritative orthographic reference — analogous to Oxford / Merriam-Webster for English. For type questions it is not a style guide per se, but it enforces spelling and hyphenation conventions that downstream affect line-breaking.

### Body size

Thai body text is typically set **slightly larger than its Latin counterpart** for equivalent perceived clarity. The reason: the marks (vowels, tones) are small relative to the consonant body, and at Latin-equivalent sizes the marks can become illegible on low-DPI screens. A 14–16px Latin body often requires 15–17px Thai body to feel equally scanable.

### Thai body font size practical rules

- Web UI body: 15–17px Thai (vs 14–16px Latin).
- Mobile UI body: 14–16px Thai minimum. Below 13px, mark legibility collapses for many readers.
- Editorial body: 16–18px Thai. Long-form online reading (news sites) often sets Thai at 18px.

This is tunable per font — Sarabun at 14px reads larger than many commercial Thai faces at 16px, because Sarabun's consonant body is drawn generously.

### Letter-spacing is toxic

More on this in *CSS Gotchas* below, but the principle: do not apply positive `letter-spacing` to Thai body text. The space between characters is where tone marks and upper vowels logically "belong to" the preceding consonant. Positive `letter-spacing` inserts gaps that the shaper interprets as intra-syllable boundaries, breaking the visual mark-to-base relationship. `letter-spacing: 0` is the only correct value for Thai body. Zero — never positive.

---

## Digits

Two digit systems coexist in modern Thai usage:

| Thai digits | Western (Arabic) digits |
|-------------|-------------------------|
| ๐ ๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙ | 0 1 2 3 4 5 6 7 8 9 |
| U+0E50 – U+0E59 | U+0030 – U+0039 |

**Western Arabic digits dominate modern Thai** — financial, technical, scientific, everyday commercial, and most journalism. **Thai digits survive in**:

- Formal / ceremonial contexts (royal, religious, traditional).
- Buddhist-era year notation on government documents (e.g., พ.ศ. ๒๕๖๙ = B.E. 2569 = 2026 CE).
- Some newspaper mastheads, calendars, and decorative usage.
- Traditional / historical publishing.

Thai digits render **slightly taller** than surrounding consonant bodies in most fonts — visibly taller when mixed inline with Latin digits, which can produce awkward rhythm. For mixed content (Thai paragraph with English loanwords containing numbers), default to Western digits throughout.

### CSS and Thai digits

- `font-variant-numeric` does **not** switch between Thai and Western digit systems — that is a content choice, not a typographic one.
- To produce Thai digits programmatically: `Intl.NumberFormat('th-TH-u-nu-thai')` or `toLocaleString('th-TH-u-nu-thai')`. Default `th-TH` uses Western digits in modern browser implementations.
- Tabular figures: most Thai fonts support `tnum` for their Western-digit set; few support `tnum` for Thai digits. For Thai-digit tables, expect non-tabular behavior unless you have verified the font.

### Currency

**Thai baht ฿ (U+0E3F).** This is a Thai-block character, not Latin. Fonts that advertise Thai support cover it; Latin-only fonts do not. The glyph is a B-shape with a vertical bar through it.

---

## Punctuation

Thai has adopted almost all Latin punctuation for modern use.

### Western punctuation (borrowed and now default)

- **`, . : ; ? ! " '` ( ) [ ]** — all Western, standard usage.
- **Em-dash, en-dash, ellipsis** — Western conventions, same as Latin.
- **Quotation marks** — typically straight `"` or curly `"…"` depending on publication style; no native Thai quote marks in modern use.

The period `.` marks sentence end in contemporary prose. In **formal / legal / traditional** text, sentence end is marked by **space** (the same convention as clause separation — see *Word-spacing and segmentation* below).

### Thai-specific punctuation (rare in modern text)

- **ฯ (paiyannoi, U+0E2F).** Abbreviation mark — marks truncated forms (like `เป็นต้น` → `ฯลฯ`, "etc.").
- **ๆ (mai yamok, U+0E46).** Repetition mark — duplicates the preceding word. `เด็ก ๆ` = "children" (multiple). Very common in contemporary writing.
- **๚ (angkhan khu, U+0E5A).** Section or stanza marker; rare outside traditional / classical texts.
- **๛ (khomut, U+0E5B).** End-of-text marker; rare outside traditional texts.
- **๏ (fongman, U+0E4F).** Paragraph-start ornamental mark; rare, traditional.

### Spacing around punctuation

Western punctuation in Thai follows Western spacing conventions — no space before `,` `.` `:` `;` `?` `!`, one space after. The exception is in highly formal Thai where a *single* space is sometimes placed before and after punctuation for visual breathing, but this is a typographer's choice, not a rule.

---

## Word-Spacing and Segmentation

This is the second structural difference from Latin (after the mark stack).

**Thai does not use spaces between words.** A Thai paragraph is a continuous stream of characters. Spaces appear **between clauses or sentences**, not between words.

Example (with `[space]` marking the actual space characters):

```
ผมชอบอ่านหนังสือภาษาไทย[space]หนังสือที่ดีมีหลายเล่ม
```

"I like to read Thai books. There are many good books."

The single space in the middle is the clause/sentence boundary. Within `ผมชอบอ่านหนังสือภาษาไทย` ("I like to read Thai books"), there are **seven** separate Thai words — the reader segments them mentally.

### Line-breaking implications

Line-break algorithms cannot break at the space-character level alone: a 40-word Thai sentence with only 1–2 spaces produces near-unbreakable lines. Two approaches exist:

1. **Dictionary-based segmentation.** Maintain a Thai-word dictionary; at line-break time, find the best segmentation and break at word boundaries. This is how professional Thai typesetting has always worked.
2. **Character-level wrapping.** Break anywhere. Produces bad breaks mid-syllable (splitting a consonant from its tone mark is the worst case; splitting a syllable from its vowel is bad enough). Unacceptable for quality typesetting.

### Browser behavior

Modern browsers implement dictionary-based segmentation for Thai:

- **Safari** (WebKit) — uses macOS/iOS platform segmenter (CoreText + CFStringTokenizer); high-quality. Covers most Thai text correctly.
- **Chrome** (Blink) — uses ICU's `BreakIterator` with the Thai word-boundary locale. Very good segmentation quality since Chrome ~60 (2017 onward); solid by 2026.
- **Firefox** (Gecko) — historically the weakest on Thai segmentation, but improved significantly in 2021–2024. As of 2026 Firefox uses ICU's BreakIterator and matches Chrome reasonably well.

The canonical segmentation engine is **ICU's `BreakIterator`** with `Locale.THAILAND`. Its word-boundary dictionary ships inside ICU's data; any browser or server that bundles modern ICU inherits it.

### CSS controls

```css
.thai {
  word-break: normal;        /* default; respects dictionary */
  line-break: strict;        /* uses dictionary for CJK+Thai */
  overflow-wrap: break-word; /* only break mid-word if no better option */
}
```

`line-break` values for Thai:

- **`strict`** (default in most browsers for CJK and Thai) — uses dictionary, breaks at word boundaries.
- **`normal`** — similar to strict, slightly more permissive.
- **`loose`** — permits more break opportunities; can produce mid-syllable breaks. Avoid for body.
- **`anywhere`** — breaks at any character boundary. **Wrong for Thai** — breaks consonant-from-tone, vowel-from-base. Never use for Thai body.
- **`auto`** — browser's default, typically dictionary-backed.

For UI chrome where short strings must not wrap awkwardly, `word-break: keep-all` prevents breaking within a run entirely; combine with `overflow-wrap: anywhere` as a last-resort fallback.

**UAX #14 (Unicode Line Breaking Algorithm)** defines the abstract behavior; for Thai, it defers to external dictionary segmentation. See `https://www.unicode.org/reports/tr14/` and the accompanying `sea-gap` document for Southeast Asian layout issues.

### Input-method consequence

Thai keyboards produce logical-order Thai without spaces. Users type continuous strings; segmentation happens at render time. If your UI applies any kind of word-count to Thai input, count by grapheme cluster or use ICU's word-boundary analysis — never by space count.

---

## Notable Fonts

### Free / open, broad coverage

- **Noto Sans Thai / Noto Serif Thai** (Google, SIL OFL). Comprehensive, well-maintained, metric-matched to Noto Sans / Noto Serif Latin. Variable-font cuts available (wght axis; wdth in newer releases). Default sane choice for generic Thai web content.
- **Noto Sans Thai Looped** (Google). The loop-style variant for traditional / editorial body contexts.
- **Sarabun** (designed by Supalerk Ratanawilai; commissioned by the Thai government). Adopted as the **official Thai government body font** in 2013 and widely used across Thai public-sector publications. Covers Thai + Latin with careful metric harmonization. Free via Google Fonts.
- **Kanit, Prompt, Mitr, Bai Jamjuree, K2D, Taviraj, Charm, Krub, Niramit, Pridi** (Cadson Demak; Google Fonts). Cadson Demak is the premier Thai foundry and their open-source releases on Google Fonts form the de-facto modern Thai open-source canon. Mix of loop and loopless cuts.
- **IBM Plex Sans Thai / IBM Plex Sans Thai Looped** (IBM + Cadson Demak, 2022). Part of the IBM Plex family; metric-matched to Plex Sans Latin. Modern loopless cut is the default.
- **Chakra Petch** (Cadson Demak; display / tech / sci-fi aesthetic).

### System-preinstalled

- **macOS / iOS:** Thonburi (sans, loop), Ayuthaya (display), Krungthep (rounded). Thonburi is the default system Thai for most UI contexts.
- **Windows:** Leelawadee UI (modern sans, loop), Cordia New (traditional loop, legacy), Angsana New (serif-adjacent loop, legacy), Tahoma (surprisingly: Tahoma ships with Thai glyphs and has been the default in many Windows Thai localizations since XP).
- **Android:** System fonts vary by vendor; Google's Noto Sans Thai is the AOSP default.

### Commercial foundries

- **Cadson Demak** (Bangkok) — the dominant Thai foundry, founded 2002. Publishes most of the notable open-source Thai families and a premium commercial catalog.
- **Katatrad** (Bangkok) — contemporary Thai foundry.
- **Pixelbowl / Typomotion** — smaller specialist foundries.
- **Sanctuary** (Bangkok) — premium display and branding Thai.
- **CS Chat Thai** — Thai Royal Institute-associated font.

### PSL / TH / UPC families (legacy commercial)

- **PSL Kanda, PSL Display**, and the large **PSL** catalog — commercial Thai faces widely licensed to Thai publishers since the 1990s.
- **TH Sarabun PSK / TH Sarabun New** — Thai government-standard family (a Sarabun variant).
- **UPC family** (Cordia, Angsana, Browallia, Dillenia, Eucrosia, Freesia, Iris, Jasmine, Kinnari, Lilly, Norasi) — the classic Windows / printing-industry standard Thai faces. Widely preinstalled; aesthetically dated but compatible.

### Font selection heuristic

1. **Generic Thai web content:** start with **Noto Sans Thai** (loopless default) or **Noto Sans Thai Looped** (traditional). Free, reliable, well-maintained.
2. **Government / formal / editorial:** **Sarabun** is the strongest open-source choice. Loop-style, Thai-government-standard.
3. **Modern / startup / UI-first:** **IBM Plex Sans Thai**, **Prompt**, **Kanit**, **Bai Jamjuree** (all loopless, Cadson Demak).
4. **Traditional / long-form body:** loop-style — **Sarabun, Noto Sans Thai Looped**, or **Taviraj** (serif-adjacent).
5. **System-only (no webfont load):** fallback stack of **Thonburi, Leelawadee UI, Tahoma**.

---

## Mixed Thai + Latin

In Thai documents the common pattern is **Thai-dominant prose with Latin interruptions** — English loanwords, technical terms, brand names, acronyms, product SKUs. Typography needs to handle this cleanly because it is the norm, not an edge case.

### Metric harmony

Use a font family that ships both Thai and Latin with matched metrics (Noto Sans Thai + Noto Sans, Sarabun's Latin, IBM Plex Sans Thai + IBM Plex Sans, Cadson Demak families with their Latin cuts). When stacking separate families, use `@font-face` overrides to harmonize — see `../metrics/metric-compatibility.md`.

### Font-stack direction

Because Thai consonant bodies render at roughly Latin lowercase height, a Thai font sets Latin that looks *small* relative to what a Latin-native reader expects. The correction: specify the **Thai font first** in `font-family` and let Latin fall back to a metric-matched companion, not the reverse.

```css
/* Thai-first stack (correct for Thai-dominant content) */
.thai-body {
  font-family:
    "Noto Sans Thai",    /* primary — Thai and Latin */
    "Sarabun",
    "Noto Sans",         /* Latin fallback */
    system-ui,
    sans-serif;
  font-size: 16px;
  line-height: 1.7;
  letter-spacing: 0;
}

/* Do NOT do this for Thai content */
.wrong {
  font-family: "Inter", "Noto Sans Thai", sans-serif;
  /* Inter's Thai coverage is limited; Thai glyphs fall through
     to Noto Sans Thai but metrics no longer align */
}
```

### Baseline

Thai and Latin **share a baseline**. No vertical-align tricks needed. The top of a Latin capital and the top of a Thai consonant body sit at approximately the same height (though the Thai tone marks rise above that).

### Bidi

Thai is LTR, so mixing Thai and Latin (also LTR) requires no bidi handling. Only Arabic, Hebrew, or other RTL content triggers the Unicode Bidirectional Algorithm.

---

## CSS Recipes

### Baseline Thai body styling

```css
:lang(th) {
  font-family: "Noto Sans Thai", "Sarabun", system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.7;         /* floor at 1.6; 1.7–1.8 comfortable for body */
  letter-spacing: 0;        /* critical — never positive */
  word-spacing: 0;
}
```

### Dark mode / color

No Thai-specific considerations — Thai behaves the same as Latin with regard to `color-scheme`, `light-dark()`, and theme wiring.

### Scoping letter-spacing away from Thai

If a Latin-primary stylesheet applies positive `letter-spacing` for some effect (caps tracking, display headers), scope it away from Thai content:

```css
body {
  letter-spacing: 0.01em;
}
:lang(th) {
  letter-spacing: 0;
}
```

### Line-breaking for UI chrome

```css
.nav-item {
  word-break: keep-all;
  overflow-wrap: anywhere;  /* last-resort only */
}
```

This prevents mid-word breaks in short navigation labels. For body paragraphs, omit `word-break: keep-all` and rely on the browser's dictionary segmentation.

### Fallback overrides (when Latin fallback looks small)

```css
@font-face {
  font-family: "Inter Thai-Matched";
  src: local("Inter");
  size-adjust: 108%;
  ascent-override: 92%;
  descent-override: 24%;
}
```

Use when a Latin face falls back inside Thai body and looks undersized.

### Thai digits (if content authored in Thai digits)

Nothing CSS-specific; the font renders the digits the content contains. To generate Thai digits from a JavaScript number:

```javascript
(2569).toLocaleString('th-TH-u-nu-thai')
// → "๒,๕๖๙"
```

---

## Common Traps

1. **`line-height: 1` or `line-height: 1.2` on Thai body.** Clips the top row of tone marks on the first line (and sometimes on every line). Set 1.6–1.8 for body. Test at the **top** of a block, not the middle — the clipping appears on the first line under the content-box constraint.

2. **Positive `letter-spacing` on Thai.** Breaks the mark-to-base visual relationship. Inserts gaps that visually detach tone marks and vowels from their base consonants. Always `letter-spacing: 0` for Thai. If a Latin-primary stylesheet applies tracking, scope it away with `:lang(th) { letter-spacing: 0; }`.

3. **`text-transform: uppercase | lowercase | capitalize`.** No effect — Thai is unicameral. Harmless in cascade, but don't rely on case as a visual device.

4. **`line-break: anywhere`.** Breaks Thai at any character boundary, splitting consonants from their marks. Never use for Thai content. Use `line-break: strict` (or default) to invoke dictionary segmentation.

5. **Mixing loop and loopless Thai in one body text.** Reads as a typographic mistake, like mixing serif and sans for body in Latin. Pick one tradition per role.

6. **Latin-first font stacks for Thai content.** Places a Latin-only font ahead of the Thai-capable one; Thai glyphs fall through to the Thai font with mismatched metrics. Specify the Thai font first.

7. **Treating Thai digits as Western for counting / formatting.** `toString()` on numbers produces Western digits by default; to get Thai digits you must specify the `-u-nu-thai` locale extension. And tabular-figure support for Thai digits is inconsistent — assume non-tabular unless verified.

8. **Assuming space-counting = word-counting.** A Thai paragraph with two spaces has 15+ words. Never compute word count for Thai from space delimiters. Use ICU word-boundary analysis or an explicit Thai segmenter.

9. **Using Latin `|` or `/` as a separator in Thai UI.** Renders fine but reads as foreign. Thai publications conventionally use space, comma, or (in traditional text) the paiyannoi `ฯ`. For UI pipes, Latin `|` is acceptable if the product is tech-leaning; avoid in government or traditional registers.

10. **Ignoring `lang="th"` attributes.** Without `lang`, browsers may not invoke Thai-specific line-break rules (dictionary segmentation), and screen readers may read Thai in a Latin voice. Set `lang="th"` on the root or content-containing element.

11. **Not testing with real Thai content.** A Latin-native team commonly ships Thai support verified with short test strings ("สวัสดี" — hello). Real Thai body text is much longer, denser, and has more tone-mark and vowel combinations. Test with an actual paragraph from a Thai source (government forms, Wikipedia articles, Pantip posts) before shipping.

12. **Using `TH Sarabun New` when you mean `Sarabun`.** The two are related but distinct — TH Sarabun is the government-bundled variant with slightly different metrics; Sarabun (on Google Fonts) is the widely-used open-source release. Don't substitute silently.

13. **Thai `ำ` (sara am) treated as a single combining mark when it is actually precomposed.** ำ (U+0E33) is a precomposed "nikhahit + sara a" sequence — it contains both the above-dot and the following -am vowel. Fonts render it correctly, but text-manipulation code that decomposes assumes `nikhahit + aa` as two marks; `ำ` is one codepoint. Use NFC (or NFD with explicit Thai handling) for normalization.

14. **Synthetic bold / italic for Thai.** `font-synthesis: weight` on Thai produces thickened stems that destroy the mark-base balance — like CJK synthetic bold (see `./cjk-han.md`). Ship a real weight master. Italic synthesis is even worse: Thai has no italic tradition, and slanting breaks the mark-stack alignment. `font-synthesis: none` is defensible on Thai `@font-face`.

---

## Sources

**Unicode / W3C primary sources:**

- [Unicode Chart: Thai](https://www.unicode.org/charts/PDF/U0E00.pdf) — the code chart.
- [Unicode Standard 16.0, Chapter 16 — Southeast Asia](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-16/) — Thai alongside Lao, Khmer, Burmese.
- [W3C Southeast Asian Layout Requirements (sealreq)](https://www.w3.org/International/sealreq/) — the authoritative layout reference for Thai and other SEA scripts.
- [W3C Southeast Asian Gap Analysis (sea-gap)](https://www.w3.org/TR/sea-gap/) — where browsers fall short.
- [Unicode UAX #14: Line Breaking Algorithm](https://www.unicode.org/reports/tr14/) — the abstract line-break rules; Thai segmentation is deferred to dictionary.
- [ICU User Guide: Boundary Analysis](https://unicode-org.github.io/icu/userguide/boundaryanalysis/) — how Thai word-boundary detection works in practice.

**Shaping / OpenType:**

- [Microsoft Typography: Developing OpenType Fonts for Thai Script](https://learn.microsoft.com/en-us/typography/script-development/thai) — implementer's guide to Thai GSUB/GPOS tables and the `mark`/`mkmk` requirement.
- [HarfBuzz shaping documentation for Thai](https://harfbuzz.github.io/shaping-use.html) — the dominant shaper's behavior.

**Thai-specific authoritative sources:**

- [Royal Society of Thailand / Office of the Royal Society](https://www.orst.go.th/) — orthography, approved spellings, royal-institute dictionary.
- Gerry Leonidas, *Thai typography — a preliminary survey*, University of Reading Department of Typography — the English-language starting point for Thai typographic research-survey.
- Virunpath Vacharaprusadee (Cadson Demak) — writings on modern Thai type design.

**Type-design resources:**

- [Cadson Demak](https://www.cadsondemak.com/) — the foundry. Specimen + writings.
- [Google Fonts: Noto Sans Thai](https://fonts.google.com/noto/specimen/Noto+Sans+Thai)
- [Google Fonts: Sarabun](https://fonts.google.com/specimen/Sarabun)
- [Google Fonts: Noto Sans Thai Looped](https://fonts.google.com/specimen/Noto+Sans+Thai+Looped)
- [IBM Plex Sans Thai project notes](https://www.ibm.com/plex/) — Plex Thai design notes (2022).

**Further reading:**

- *Thai Printing: A brief history* — Thai-language sources on the 19th-century Bradley press and subsequent Thai printing history.
- Noto CJK and Noto SEA GitHub repos — `notofonts/thai` tracks issues and improvements.
- Pantip / Manager / Thai Rath online — real-world corpus for testing against contemporary Thai prose.
