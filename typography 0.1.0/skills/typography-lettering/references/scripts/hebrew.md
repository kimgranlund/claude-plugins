---
date: 2026-04-18
coverage: medium
peers:
  - ./arabic.md
  - ./latin.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
primary_sources:
  - https://w3c.github.io/hlreq/
  - https://www.w3.org/International/hlreq/hebr/
  - https://www.unicode.org/charts/PDF/U0590.pdf
  - https://www.unicode.org/charts/PDF/UFB00.pdf
  - https://www.unicode.org/versions/latest/ch09.pdf
  - https://learn.microsoft.com/en-us/typography/script-development/hebrew
  - https://github.com/n8willis/opentype-shaping-documents/blob/master/opentype-shaping-hebrew.md
  - https://culmus.sourceforge.io/opentype/index.html
  - https://www.typotheque.com/articles/designing-hebrew-type
  - https://www.typotheque.com/articles/secondary-style-in-hebrew-typography
  - https://fonts.google.com/specimen/Frank+Ruhl+Libre
  - https://fonts.google.com/specimen/Heebo
  - https://fonts.google.com/specimen/Rubik
  - https://fonts.google.com/specimen/Assistant
  - https://en.wikipedia.org/wiki/Hebrew_numerals
  - https://en.wikipedia.org/wiki/Gershayim
  - https://en.wikipedia.org/wiki/Rashi_script
  - https://hebrewtype.com/the-mysterious-gershayim/
---

# Hebrew Script Typography

**Scope disclaimer.** This is a *practitioner* reference for a web/UI typographer with no prior Hebrew exposure. It covers the typographic surface — what a designer or front-end engineer needs to set Hebrew well and avoid the common mistakes. Scholarly depth on biblical cantillation, Masoretic mark stacking, or scribal STAM tradition lives in the sources linked above (W3C HLReq, n8willis' OpenType shaping notes for Hebrew, Culmus project documentation, Typotheque's Hebrew research-survey essays). Where this file gives a practical rule, assume there is further nuance in those sources.

**Why Hebrew typography is different from Arabic.** Both are right-to-left. Both live under the Unicode Bidirectional Algorithm. But Hebrew is **non-connecting** — each consonant is a discrete, upright, roughly square glyph with its own left and right sidebearings, like Latin or Cyrillic rotated conceptually. There is no four-form shaping, no kashida tradition of any mainstream weight, no cursive flow in standard print. The hard problems Hebrew presents are not shaping; they are (1) nikud (vowel-point positioning above, below, and inside base letters), (2) mark stacking for biblical text (nikud *plus* cantillation), (3) the absence of letter case as a typographic lever, (4) letter disambiguation for similar-shaped characters, and (5) metric harmony with Latin when bilingual.

**What this file covers.** History (Paleo-Hebrew → Aramaic square script → modern Ashuri + Rashi + STAM categories). Direction and bidi (cross-referenced to `arabic.md` — not duplicated). Letter inventory including final forms. The unicameral nature of the script and what it removes from a designer's toolkit. Nikud in depth — positioning, OpenType `mark`/`mkmk`, CSS line-height implications. Cantillation as a separate specialized tier. Letter disambiguation traps. Justification conventions. Numerals (European-Arabic and Hebrew-letter). Punctuation (geresh, gershayim, maqaf). The font landscape: classical (Frank Ruehl, David, Koren), utility (Narkisim), contemporary open (Assistant, Heebo, Rubik, Alef, IBM Plex Hebrew, Noto Hebrew). The italic-or-not question. Bilingual Hebrew+Latin metric design. Gotchas and anti-patterns.

---

## Historical Origin

### Paleo-Hebrew to Aramaic square script

The script modern Hebrew is set in is **not** the original Hebrew script. The ancient Israelites wrote in **Paleo-Hebrew** (a close variant of the Phoenician alphabet) through roughly the 6th century BCE. Following the Babylonian exile, Aramaic became the administrative lingua franca of the region, and Jewish scribes adopted the **Aramaic square script** — known in Hebrew tradition as **K'tav Ashuri** ("Assyrian writing") — for copying sacred texts. By roughly the 5th–4th century BCE, Ashuri had displaced Paleo-Hebrew for religious copying; by the Second Temple period it was universal for Hebrew. The square, upright character of the modern printed Hebrew letter — 22 consonants plus 5 final forms — descends directly from that Aramaic-derived Ashuri.

Paleo-Hebrew survived in marginal use (some Samaritan liturgy, coin legends during the Bar Kokhba revolt) but is essentially extinct for everyday typesetting. When you see "Paleo-Hebrew" font files online, they are specialist scholarly tools, not production faces.

### Rashi script

**Rashi script** (כְּתַב רַשִׁ״י) is a separate typeface tradition based on 15th-century Sephardic semi-cursive handwriting. Rashi himself — the 11th-century French commentator Shlomo Yitzhaki — did not write in it; the script is *named in his honor* and was adopted by early Hebrew printers (notably the Soncino family in the 1470s, followed by Daniel Bomberg in Venice) for typesetting rabbinic commentary alongside the primary text. In a printed Talmud page, the biblical or Mishnaic text is in square Ashuri; Rashi's commentary and Tosafot commentaries are in Rashi script, so the eye can tell at a glance which layer is which.

**Rashi script is not a different alphabet** — it uses the same 22+5 letters, with different shape conventions. Readers who are fluent in square Hebrew can read Rashi with some adjustment. Rashi digital fonts exist (Rashi Libre, SBL Rashi, various commercial ones) but are a specialist tool for rabbinic publishing, Talmud editions, and religious academic work. Do not use Rashi as a body face for general content — it signals "this is commentary on the real text" and will read as either ornamental or disorienting outside that context.

### STAM script

**STAM** (ס״ת — acronym for *Sifrei Torah, Tefillin, Mezuzot*) is the tradition of Hebrew calligraphy used in producing Torah scrolls, the parchment passages inside tefillin (phylacteries), and mezuzah scrolls. It is a **hand-calligraphic** tradition, not a typeface category — scribes (*soferim*) produce each copy by hand with a quill on specially prepared parchment, following strict halakhic rules about letter proportions, spacing, and the **tagin** (תגין) — crown-like flourishes attached to the tops of specific letters. In modern scribal practice, the letters *beit*, *dalet*, *heh*, *chet*, *yod*, and *qof* take one crown; *gimel*, *zayin*, *tet*, *nun*, *ayin*, *tsadi*, and *shin* take three.

STAM is **out of scope for typography**. Fonts that emulate STAM (Stam Ashkenaz, Stam Sefard) exist for digital Torah study materials and signage, but a valid Torah scroll cannot be printed — it must be hand-scribed. The category exists in this file only so readers don't confuse it with typesetting.

---

## Direction and Bidi

Hebrew is written **right-to-left** — characters are stored in logical order (first-typed is first in the byte stream) and rendered in visual order (first-typed is rightmost). This is structurally identical to Arabic. The Unicode Bidirectional Algorithm (UAX #9) handles the mapping. Everything in `./arabic.md` on bidi mechanics — `dir="rtl"`, `dir="auto"` for user-generated content, `<bdi>` for isolated inline switches, `unicode-bidi: isolate` in CSS, logical CSS properties (`margin-inline-start` over `margin-left`), pitfalls with embedded Latin — **applies identically to Hebrew**. See `./arabic.md` §Bidirectional Interaction. Do not re-implement; cross-reference.

**What is different from Arabic:**

- **Numerals.** Hebrew prose uses **European-Arabic digits** (0–9) almost exclusively in modern writing. There is no Hebrew equivalent of Arabic-Indic vs Maghreb digit-set debate. The UBA still renders digits LTR inside RTL context — `1997` in the middle of Hebrew text reads `1997` with the `1` on the left — so bidi ordering bugs *do* occur, just with fewer digit-set permutations. Hebrew-letter numerals (§Numerals) are a separate, non-digit convention.
- **`<bdo>` vs `isolate`.** The same advice as for Arabic holds with extra force: prefer `unicode-bidi: isolate` or `isolate-override` over `<bdo>`. `<bdo>` forces a direction override with no isolation, which is almost never what you want; it mis-orders surrounding neutral characters and fights the UBA.
- **No four-form shaping.** This removes an entire category of CSS gotchas (see `./arabic.md` on `font-feature-settings` disabling `init`/`medi`/`fina`). Hebrew shaping is structurally simpler — the shaper's main job is positioning nikud, not selecting contextual forms.

```html
<html dir="rtl" lang="he">
  <p>טקסט עברי עם מספר <span dir="ltr">2026</span> בתוכו.</p>
</html>
```

```css
html { direction: rtl; unicode-bidi: isolate; }
```

For the full treatment of `dir="auto"`, bidi-isolated inline content, logical properties, and mixed-script pitfalls, see `./arabic.md` §Bidirectional Interaction.

---

## Letter Inventory

Standard Hebrew has **22 consonants**. Five of those letters take a distinct **final form** (*sofit*) when they occur at the end of a word — a visual rather than grammatical distinction, similar to how Greek σ/ς shifts at word-end.

| Letter | Name | Final form | Notes |
|---|---|---|---|
| א | aleph | — | silent / glottal carrier |
| ב | bet | — | stop /b/ or fricative /v/ depending on dagesh |
| ג | gimel | — | /g/ |
| ד | dalet | — | /d/ |
| ה | he | — | /h/ |
| ו | vav | — | /v/; also vowel carrier for /u/, /o/ with nikud |
| ז | zayin | — | /z/ |
| ח | chet | — | /ħ/ fricative |
| ט | tet | — | /t/ |
| י | yod | — | /j/; also vowel carrier for /i/ with nikud |
| כ | kaf | ך (kaf sofit) | /k/ or /χ/ fricative |
| ל | lamed | — | /l/ |
| מ | mem | ם (mem sofit) | /m/ |
| נ | nun | ן (nun sofit) | /n/ |
| ס | samech | — | /s/ |
| ע | ayin | — | silent / pharyngeal |
| פ | pe | ף (pe sofit) | /p/ or /f/ fricative |
| צ | tsadi | ץ (tsadi sofit) | /ts/ |
| ק | qof | — | /k/ |
| ר | resh | — | /r/ |
| ש | shin | — | /ʃ/ or /s/ depending on shin/sin dot |
| ת | tav | — | /t/ |

### Final forms and Unicode

Final forms are **separate Unicode codepoints**, not contextual shaping of the base letter:

- kaf U+05DB → final kaf U+05DA (ך)
- mem U+05DE → final mem U+05DD (ם)
- nun U+05E0 → final nun U+05DF (ן)
- pe U+05E4 → final pe U+05E3 (ף)
- tsadi U+05E6 → final tsadi U+05E5 (ץ)

This means that, unlike Arabic four-form shaping which happens at the shaper inside a single codepoint, Hebrew final-form selection is a **content-level decision** — the author types the final-form character directly, or the input method substitutes it. Some fonts do ship a `fina` OpenType feature that can substitute a final glyph when the shaper sees a non-final codepoint at word-end, but this is *non-standard for Hebrew* and most workflows rely on correctly-typed codepoints. Do not assume a shaper will rescue badly-typed Hebrew.

**Practical consequence.** User-input forms that accept Hebrew names or words must not silently normalize kaf → final-kaf or vice versa; the two are semantically distinct, searches should match both forms (Unicode NFKC does not fold them — a search for "אמא" will not find "אמם" and shouldn't).

---

## Unicameral: No Upper/Lower Case

**Hebrew is unicameral** — the script has a single case. There is no uppercase/lowercase distinction. This is not a decorative absence; it is structural. The consequences for UI and editorial typography:

- **No ALL CAPS treatment.** `text-transform: uppercase` is a no-op on Hebrew text. It is not an error, but it signals a Latin-first stylesheet.
- **No small caps.** `font-variant-caps: small-caps` has no effect. Hebrew fonts do not ship `smcp`/`c2sc` features because there is no uppercase to shrink. Designers occasionally draw a "Hebrew small-cap" equivalent — a second style at a slightly-smaller height — but it is a proprietary convention, not an OpenType standard.
- **No sentence case vs title case distinction.** The convention "capitalize the first letter of a sentence or heading" does not exist. Every sentence begins the same way.
- **No proper-noun capitalization.** Names, place-names, deity names — all written with the same letter forms as common nouns. Disambiguation relies on context, punctuation, or typographic treatment (bold, larger size, a different face) rather than case.
- **`::first-letter` semantics.** `::first-letter` still targets the first character, but without a case-change tool, drop caps are commonly rendered by size alone or by switching to a display face. The "Hebrew initial" tradition in illuminated manuscripts (large decorative first letter) does not map cleanly to CSS `::first-letter` — it was hand-composed.

### Emphasis without case

Because Hebrew can't shout through caps, emphasis moves to other levers:

1. **Weight.** Bold (`font-weight: 700` or heavier) is the primary emphasis mark, as it is in Latin. Hebrew weight-ladder behavior is generally predictable in contemporary families.
2. **Size.** Slight size increases are more visible as emphasis in Hebrew than in Latin because the baseline unicameral rhythm is flatter — no ascender/descender drama to compete with.
3. **Letter-spacing (tracking).** Positive tracking of Hebrew text (`letter-spacing: 0.05em` or more) is a traditional emphasis convention in Israeli editorial design, analogous to German gesperrt. Because Hebrew is **non-connecting**, letter-spacing works cleanly — it does not break joins. This is a real typographic difference from Arabic, where letter-spacing is destructive.
4. **A secondary style.** Some contemporary Hebrew families ship a "secondary" or "alternate" style — a different drawing of the alphabet at the same weight and size, intended to fill the emphasis role that italics fill in Latin. See §Italic for the history of this debate.
5. **Color or weight shift.** Editorial Hebrew commonly uses a color change or weight shift for running-head emphasis rather than italic.

**UI implication.** Emphasis tokens in a bilingual design system need to resolve per-script. Italic emphasis in Latin → bold or tracked in Hebrew. A naïve "emphasized text is italic" rule will render Hebrew as synthetic oblique, which the typographic tradition historically rejects (see §Italic).

---

## Nikud (Vowel Points)

**Nikud** (ניקוד, "pointing") is the system of small marks placed above, below, and inside consonants to indicate vowel sounds. It is the single biggest typographic complication Hebrew presents. Modern unpointed Hebrew text — newspapers, novels, most of the web, UI — is written without nikud; fluent readers infer vowels from context. Pointed text appears in:

- The Tanakh (Hebrew Bible), fully pointed for correct liturgical recitation
- Children's books and early-grade reading materials
- Poetry (sometimes, for meter and disambiguation)
- Dictionaries, language-learning materials, and ulpan textbooks
- Rare words, loanwords, or ambiguous cases in academic or legal prose
- Prayer books (*siddurim*) and liturgical texts

### Mark inventory

The main points (non-exhaustive; the full Unicode Hebrew block U+0590–U+05FF includes additional biblical and archaic marks):

| Mark | Name | Unicode | Position | Value |
|---|---|---|---|---|
| ־ָ | kamatz | U+05B8 | below | /a/ or /o/ |
| ־ַ | patach | U+05B7 | below | /a/ |
| ־ֶ | segol | U+05B6 | below | /e/ |
| ־ֵ | tsere | U+05B5 | below | /e/ |
| ־ִ | chirik | U+05B4 | below | /i/ |
| ־ֹ | cholam | U+05B9 | above-left | /o/ |
| ־ֻ | qubuts | U+05BB | below | /u/ |
| ־ְ | shva | U+05B0 | below | /ə/ or silent |
| ־ׁ | shin dot | U+05C1 | above-right | selects /ʃ/ (shin) |
| ־ׂ | sin dot | U+05C2 | above-left | selects /s/ (sin) |
| ־ּ | dagesh | U+05BC | **inside** | hardens fricative to stop |
| ־ֿ | rafe | U+05BF | above | softens (rare in modern text) |
| ־ֲ | chataf-patach | U+05B2 | below | reduced /a/ |
| ־ֱ | chataf-segol | U+05B1 | below | reduced /e/ |
| ־ֳ | chataf-kamatz | U+05B3 | below | reduced /o/ |

The **dagesh** is structurally unusual: it is a dot placed *inside* the letter, not above or below. It requires a mark-to-base anchor positioned at the center of the glyph's counter. Fonts that get dagesh positioning right — dot centered in the letter's bowl without touching the strokes — signal careful Hebrew type-design attention.

The **cholam** is positioned above-left of the base letter (not centered above), because it frequently combines with vav (ו) to form the vowel combination `וֹ` (cholam-male), where the cholam sits on the vav's upper-left shoulder.

The **shin/sin dot** is a letter-selection mechanism. The consonant ש is phonologically ambiguous; the dot on the upper-right (shin) selects /ʃ/, and the dot on the upper-left (sin) selects /s/. Without either dot, the consonant's reading depends on context (in unpointed text this is the norm). A well-built Hebrew font must handle shin-dot, sin-dot, and shin-with-dagesh-with-nikud stacks simultaneously.

### OpenType positioning

Hebrew nikud rely on the same OpenType mark-positioning features as other complex scripts:

- **`mark` (mark-to-base).** Positions a diacritic mark relative to its base consonant. Anchor points in the font's GPOS table define where the mark attaches on the base. A font without a proper `mark` feature will render marks at default baseline positions — they drift, float in the wrong spot, or overlap.
- **`mkmk` (mark-to-mark).** Positions a mark relative to another mark. Critical for biblical text where a shin-dot, a patach, a dagesh, and a cantillation mark can all stack on a single base; without `mkmk` the marks collide.
- **`ccmp` (glyph composition/decomposition).** Sometimes used to pre-compose letter+dagesh into single glyphs for cleaner rendering.
- **`abvm` / `blwm`.** Indic-origin above-mark / below-mark features; occasionally used by Hebrew fonts but `mark`/`mkmk` are the mainstream.

The shaper (HarfBuzz in every modern browser) runs the Unicode canonical reordering on adjacent marks before applying GPOS, so author-order variation between `consonant + shin-dot + patach` and `consonant + patach + shin-dot` produces the same visual result. Biblical-quality Hebrew fonts may also contain contextual GPOS lookups that shift marks onto alternate anchors when specific combinations occur — notably in Masoretic text where the combination of cantillation with nikud creates edge cases the default anchors don't handle.

Fonts engineered for biblical Hebrew — SBL Hebrew (Society of Biblical Literature), Ezra SIL, Taamey Frank CLM, Taamey David CLM, Cardo — go further than general-use fonts in these contextual GPOS lookups and in cantillation coverage.

### CSS and line-height impact

Pointed Hebrew eats vertical space. Nikud below the baseline collide with the ascenders of the next line; nikud above the baseline collide with the descenders of the previous line. Line-height that works for unpointed Hebrew fails for pointed Hebrew.

Practitioner guidance:

| Content | `line-height` | Notes |
|---|---|---|
| Unpointed Hebrew body (news, UI, novels) | **1.5–1.7** | Close to Latin body — Hebrew is box-shaped and vertically compact when unpointed. |
| Lightly pointed Hebrew (ambiguous-word marks only) | **1.6–1.8** | Small bump to accommodate occasional nikud. |
| Fully pointed Hebrew (children's, poetry, learning) | **1.8–2.0+** | Significant increase — marks need breathing room. |
| Biblical Hebrew with cantillation | **2.0–2.4+** | Full cantillation stack demands dramatic leading. |

Set `line-height` as **unitless** (`line-height: 1.7`), not `1.7em` or pixels — unitless inherits correctly across nested fonts, which matters in bilingual layouts where Hebrew needs more leading than Latin siblings.

```css
:lang(he) { line-height: 1.7; }
:lang(he) .pointed { line-height: 1.9; }
:lang(he) .biblical { line-height: 2.2; }
```

### When to ship nikud

Decision rule: **if the reader needs it to read correctly, include it; otherwise omit.** Adults reading modern Hebrew find fully-pointed text laborious — the marks are visual noise they don't need. Children, learners, and liturgical readers need them. An adult news site that renders every paragraph with full nikud is mis-configured, probably because content was pasted in from a pointed source.

For UI, nikud shows up most often in:
- Brand names and loanwords where pronunciation is ambiguous
- First-occurrence glosses in educational content
- Search-input affordances where the user's query might include nikud

Storage: always store Hebrew content in **NFC** (canonical composition) — ensures marks attach to their correct base. Normalize inputs. Do not strip nikud in storage unless your product policy explicitly does so.

---

## Cantillation (Ta'amim, Trop)

**Cantillation marks** (טעמים, *te'amim*; colloquially *trop* from Yiddish) are a separate tier of marks used *only* in biblical text to indicate chanted recitation. They encode musical phrasing, syntactic grouping, and performance. Examples include etnachta (U+0591), munach (U+05A3), zaqef qaton (U+0594), mercha (U+05A5), atnah (U+0591), pazer, shalshelet, and many more — the full cantillation inventory occupies roughly 30 codepoints in the Hebrew block.

**Cantillation stacks on top of nikud.** A single consonant can carry: a shin-dot + a dagesh + a vowel mark + a cantillation mark — four marks on one base. Mark-to-mark positioning for this density is the hardest challenge in Hebrew font engineering.

**Specialized fonts required.** Most general-purpose Hebrew fonts (Frank Ruehl Libre, Heebo, Rubik, David, Assistant) **do not** cover cantillation marks or cover them poorly. Fonts built for biblical work:

- **SBL Hebrew** (Society of Biblical Literature) — free for academic use; widely considered the reference for scholarly biblical typesetting. Comprehensive `mark`/`mkmk` coverage including contextual Masoretic edge cases.
- **Ezra SIL** and **SBL Biblit** — SIL-produced biblical fonts, free.
- **Taamey Frank CLM** — Frank Ruehl adapted for biblical use with full cantillation; part of the Culmus project (open-source Hebrew font collection).
- **Taamey David CLM** — David adapted for biblical use.
- **Cardo** — David Perry's scholarly multi-script font with strong biblical Hebrew support.
- **Commercial:** Shlomo Stam, Koren-based biblical editions from Koren Publishers.

**UI practitioner rule.** If your content is biblical and includes te'amim, stack-test your chosen font against a known-hard verse — Psalm 18:1 and Genesis 1:1 are traditional stress tests because they combine many mark types. If stacks collide or drift, switch fonts; don't attempt to patch with CSS.

---

## Letter Disambiguation Traps

Hebrew has several letter pairs and triples that are visually similar. Type designers must keep the distinctions crisp; readers (and OCR systems) otherwise confuse them. If your brand-face choice looks elegant but loses these distinctions, you are shipping an accessibility problem to Hebrew readers.

### ב (bet) vs כ (kaf)

Both are C-shaped, open on the left, with a rectangular top and bottom stroke. Distinguished by a **small tick** at the bottom-right of bet that kaf lacks. Blurred in some display faces, fatal in body text. Check: set `בכבכבכ` and confirm the alternation is visible at 14px.

### ה (he) vs ח (chet)

Both are rectangular, roughly square. **He has a gap at the bottom-left** between the left stroke and the top — the left leg is detached. **Chet is closed** — the left leg attaches to the top. At small sizes or in aggressive display faces, the gap disappears and the two collapse visually. Check: `החהחהח` at 13px.

### ד (dalet) vs ר (resh)

Both are L-shaped — a top stroke and a right-descending stroke. **Dalet has a tick** protruding on the upper-right past the corner; **resh is a clean L with a rounded corner**. The tick is the only distinguishing mark and is very small; inexperienced Hebrew body faces lose it. Check: `דרדרדר`.

### ו (vav) vs ז (zayin) vs נ (nun) vs final nun (ן)

Four narrow vertical-stroke letters.

- **Vav (ו)**: a vertical stroke with a small head (cap) at the top, wider than the stem.
- **Zayin (ז)**: a vertical stroke with a wider, overhanging head at the top — wider than vav's cap.
- **Nun (נ)**: a vertical stroke with a *small* bottom foot curving to the right (base serif).
- **Final nun (ן)**: a long vertical stroke with no foot, descending below the baseline.

Confusion between vav and zayin is the classic trap — distinguished entirely by head width. Zayin heads that are drawn too small read as vav. Final nun is easily confused with vav if the descender is short.

### ם (final mem) vs ס (samech)

Both are closed square/round shapes. **Final mem is a hard-edged square** with a small gap at the top-left in most designs (the "opening" of the hidden mem form). **Samech is a fully closed oval or round-cornered square** with no gap. The distinction is subtle and sometimes misrendered in display faces — test `סםסםסם`.

### ת (tav) vs ח (chet)

Both rectangular. **Tav has a foot** (a small serif or tick at the bottom-left of the left leg); **chet is a clean rectangle** with no foot. At low resolution, tav's foot can disappear.

**Practitioner rule.** When evaluating a Hebrew font for body use, test all six disambiguation pairs at your target size. If any pair blurs, the font is display-only at that size — either scale up the font or switch.

---

## Justification

Hebrew typesetting historically and in modern practice **prefers ragged text** (ragged-left, which is the RTL analog of ragged-right — i.e., hard edge on the right, soft edge on the left). Modern Israeli newspapers, book publishers, and digital layouts overwhelmingly set Hebrew ragged rather than justified.

### Hebrew kashida — exists but minor

Some Hebrew fonts implement a **stretched-letter** justification mechanism analogous to Arabic kashida. Specific letters with elongatable horizontal strokes — notably ה (he), ח (chet), ק (qof), and ל (lamed) — have stretched variants in some fonts, invoked contextually to fill a line. Historical biblical printing (17th–19th century Amsterdam Hebrew) used this technique heavily.

In contemporary practice it is **uncommon**. Modern Hebrew fonts that support letter-stretching for justification exist (some Culmus releases, some Monotype Hebrew; Yanek Iontef's foundry Fontef has explored the tradition) but browser-level support for automatic stretch-based Hebrew justification is negligible. Compare Arabic, where kashida-based justification has at least partial and long-debated browser implementation — Hebrew has effectively none.

### Practitioner rules

```css
[dir="rtl"]:lang(he) p {
  text-align: start;        /* resolves to right in RTL — ragged left edge */
  text-wrap: pretty;        /* if supported */
  hyphens: none;            /* Hebrew does not hyphenate words */
}
```

- **Prefer `text-align: start` (ragged).** Do not `text-align: justify` Hebrew body text unless you've proven your font + browser combination produces clean word-space-only justification without tragic rivers.
- **Do not hyphenate.** Hebrew words are not broken across lines in standard typesetting. `hyphens: auto` has no meaningful hyphenation dictionary for Hebrew in most browsers and the convention rejects it.
- **Avoid letter-stretching for justification** in production unless you're intentionally targeting an archaic/biblical aesthetic with a font that genuinely ships the feature.

---

## Numerals

### European-Arabic digits dominate

Modern Hebrew prose uses the digits **0 1 2 3 4 5 6 7 8 9** (European-Arabic set, U+0030–U+0039) for quantities, prices, dates in Gregorian calendar, phone numbers, and statistics. Unlike Arabic (which has a live debate between European and Arabic-Indic digit sets), Hebrew converged on European digits during the 20th century.

Digits render LTR inside RTL context per Unicode bidi rules. `1997` in Hebrew text appears with `1` on the left, `7` on the right — correct behavior, not a bug.

### Hebrew-letter numerals (Gematria)

Hebrew letters double as numerals in traditional contexts: dates of the Hebrew calendar, chapter and verse references to biblical and talmudic texts, numbered lists in religious publications, and numerology (*gematria*). The system is quasi-decimal:

| Letters | Value | Letters | Value |
|---|---|---|---|
| א | 1 | י | 10 |
| ב | 2 | כ | 20 |
| ג | 3 | ל | 30 |
| ד | 4 | מ | 40 |
| ה | 5 | נ | 50 |
| ו | 6 | ס | 60 |
| ז | 7 | ע | 70 |
| ח | 8 | פ | 80 |
| ט | 9 | צ | 90 |
| ק | 100 | ר | 200 |
| ש | 300 | ת | 400 |

Values 500, 600, 700, 800, 900 are formed by additive combinations (ת״ק = 500, ת״ר = 600, etc.).

Numbers are written from highest value to lowest, read right-to-left in the surrounding text. Avoiding the combination יה (10+5 = 15, but these letters form a name of God) and יו (10+6 = 16) — those numbers are written ט״ו (9+6 = 15) and ט״ז (9+7 = 16) by convention.

### Geresh and Gershayim

Two punctuation marks indicate that a letter-sequence represents a number (or an abbreviation) rather than a word:

- **Geresh** (׳, U+05F3) — a single quote-like mark, used after a **single letter** representing a number or abbreviation. Example: א׳ = "1" or "first" when the context is enumerative.
- **Gershayim** (״, U+05F4) — a double quote-like mark, used **before the last letter** of a multi-letter number or abbreviation. Example: תשפ״ו = 5786 (Hebrew year ≈ 2025–26 CE).

**Do not substitute straight ASCII `'` or `"` for geresh and gershayim.** The Hebrew punctuation characters are dedicated codepoints with correct RTL semantics and typographic drawing. ASCII quotes render smaller, sit at a different vertical position, and confuse screen readers. However, in practice ASCII apostrophes are common in casual Hebrew online — treat them as a normalization target in content pipelines that target publication quality.

### CSS and digit styling

`font-variant-numeric` applies to European digits in Hebrew text the same as in Latin — lining vs old-style, tabular vs proportional. Most Hebrew fonts ship only lining proportional digits; old-style digits are a Latin tradition and most Hebrew fonts simply don't include them. Tabular figures are increasingly common for UI-focused Hebrew fonts (Heebo, Assistant, Rubik all ship tabular variants).

`font-variant-numeric` does not convert European digits to Hebrew-letter numerals. Hebrew-letter numerals are a *content* decision — if your UI needs to render "year 5786" in Hebrew-letter form (תשפ״ו), either author the content that way or format via `Intl.NumberFormat("he-IL-u-nu-hebr")` (which targets Hebrew numeric system specifically in a locale-aware way). The `hebr` numbering system is supported in modern `Intl` implementations.

---

## Punctuation

Hebrew shares most punctuation with Latin but diverges in a few characters and mirroring rules.

### Shared with Latin

- **Period (.)**, **comma (,)**, **semicolon (;)**, **colon (:)**, **exclamation (!)**, **question (?)** — all used as in Latin, at the end of the sentence or clause. Under the UBA these render correctly on the visual-left (logical-end) of a Hebrew sentence without special handling.
- **Parentheses and brackets** are **automatically mirrored** by the bidi algorithm. A `(` typed in a Hebrew string renders as `)` visually and vice-versa. Do not pre-swap; the UBA handles it.

### Hebrew-specific

| Character | Unicode | Name | Role |
|---|---|---|---|
| ׳ | U+05F3 | Geresh | Single-letter abbreviation / numeric (see §Numerals) |
| ״ | U+05F4 | Gershayim | Multi-letter abbreviation / numeric |
| ־ | U+05BE | Maqaf | Hebrew hyphen — connects compound words |
| ׃ | U+05C3 | Sof pasuq | Biblical verse terminator (colon-like, liturgical use only) |
| ׀ | U+05C0 | Paseq | Biblical separator mark |
| ׆ | U+05C6 | Nun hafukha | Inverted nun used in specific biblical passages |
| ׳ | (also) | Punctuation geresh | Distinct from U+05F3 combining mark; punctuation form |

### Maqaf

**Maqaf** (־, U+05BE) is the Hebrew hyphen. It connects words into compound expressions — very common in biblical and classical Hebrew, less common in modern prose. Visually it sits **higher than the Latin hyphen baseline** — roughly at x-height level rather than the middle of the lowercase — because Hebrew has no descender line against which to balance. Using the Latin hyphen `-` (U+002D) in Hebrew compounds is common online but technically incorrect; publication-quality Hebrew uses U+05BE.

### Quotation marks

Modern Israeli Hebrew commonly uses:

- **Straight ASCII double quotes** `"..."` in online casual text
- **Gershayim** (״) at word-end when compounding or marking abbreviations — technically a separate mark, not a quote
- **Curly quotes** `"..."` (U+201C / U+201D) in polished editorial work, adopted from English tradition
- **Hebrew punctuation double quote** — traditionally gershayim is repurposed for quotation in some publishers, which means the same glyph can mean "abbreviation mark" or "opening/closing quote" depending on position. This ambiguity is a known gripe in Hebrew typography scholarship (see Mysterious Gershayim essay in sources).

**Practitioner rule.** For modern secular Hebrew content, curly quotes `"..."` for emphasis or direct speech are safe and modern. For traditional or religious content, follow the publisher's convention. Do not use guillemets `«...»` — that is French/Russian/Spanish tradition, not Hebrew.

### Spaces and word boundaries

Hebrew words are separated by regular word-spaces. There is no equivalent of Thai's space-free prose or CJK's character-density approach. Hebrew line-breaking occurs at word-spaces; shaping complications do not affect break points. `white-space: normal` and `word-wrap: break-word` behave as expected.

---

## Font Landscape

Hebrew's font ecosystem is smaller than Latin's but has strong coverage for contemporary work.

### Classical serif

- **Frank Ruehl** — The first modern Hebrew typeface, designed by Rafael Frank (1867–1920), originally issued between 1908–1910 by the C.F. Rühl foundry in Leipzig. Ubiquitous in Hebrew print from the 1920s on; the default Hebrew body face of the 20th century. The open-source **Frank Ruhl Libre** (Google Fonts) is a contemporary revival with a wider weight range.
- **Koren** — Designed by Eliyahu Koren for the Koren Tanakh (1962); a prestigious biblical face with classical proportions and a strong connection to the Koren Publishers tradition. Used for Hebrew Bibles and poetry.
- **David** — Designed by Ismar David in the mid-20th century as a classical sans/semi-serif. More geometric and modernist than Frank Ruehl; widely used for titles.

### Classical sans / utility

- **Narkisim** — Designed by Tzvi Narkiss (1921–2010), whose mid-century work defined the utilitarian Israeli sans. Narkisim and Narkiss Block are workhorse text sans-serif faces; Narkiss Tam is a semi-serif variant. Narkiss' designs drew on ancient archaeological inscription forms then regularized them.
- **Hadassah** — Classical serif sans-serif hybrid, designed by Henri Friedlaender.

### Contemporary open-source (Google Fonts / SIL OFL)

- **Assistant** — Modern sans designed for clarity and web use; good coverage, variable weight axis, clean at UI sizes.
- **Heebo** — A Hebrew+Latin sans designed by Oded Ezer and based on/extending Christian Robertson's Roboto Latin. Strong metric harmony between scripts; excellent default for bilingual UI.
- **Rubik** — Originally a Hebrew-first face by Philipp Hubert and Sebastian Fischer (Hubert & Fischer), extended to Latin and Cyrillic. Rounded grotesque, modern, warm. One of the most-used Hebrew webfonts in 2024–2026. Variable weight.
- **Alef** — Minimalist Hebrew sans, SIL OFL, clean for UI.
- **Secular One, Bellefair, Miriam Libre, David Libre, M PLUS Rounded 1c (limited Hebrew)** — additional Google Fonts options, quality varies.
- **IBM Plex Sans Hebrew** — Part of the IBM Plex family; designed for metric harmony with Plex Sans Latin. Professional quality, variable weight, good for UI and product documentation.
- **Noto Sans Hebrew** and **Noto Serif Hebrew** — Google/Monotype's Noto universal coverage; safe fallback for all scripts; generally workmanlike rather than distinguished.

### Commercial / foundry

- **Masterfont** — Longstanding Israeli foundry (founded 1989); the commercial core of Hebrew type for decades. Large catalog including advertising, editorial, and display.
- **HaGilda** — Contemporary Israeli foundry with modern editorial Hebrew.
- **Fontef** — Yanek Iontef's Tel Aviv foundry (est. 1994), ships Hebrew, Latin, and Arabic faces with strong cross-script design coordination. Iontef received the Rothschild Foundation award for services to the Hebrew letter in 2021.
- **Typotheque** — Netherlands/Czech foundry with a major multi-year Hebrew program (Peter Biľak, Michal Sahar, et al.); publishes scholarly essays on Hebrew type design.
- **Parashar Hebrew Collection** — Commercial Hebrew specialist.
- **Adobe Hebrew** — Ships with Creative Cloud; covers basic needs.

### Biblical / scholarly

- **SBL Hebrew** (Society of Biblical Literature, free) — the reference face for scholarly biblical work; exhaustive cantillation and mark coverage.
- **Ezra SIL** (SIL, OFL) — biblical Hebrew, strong Masoretic edge-case handling.
- **Taamey Frank CLM** and **Taamey David CLM** (Culmus project, OFL) — Frank Ruehl and David adapted for biblical use.
- **Cardo** (David Perry, OFL) — multi-script scholarly font with strong biblical Hebrew.

### Rashi script

- **Rashi Libre** (various open releases) — for commentary typesetting.
- **SBL Rashi** — paired with SBL Hebrew for rabbinic editions.
- **Commercial Rashi fonts** from Masterfont and specialty religious-publishing foundries.

---

## Italic (and Why Hebrew Often Rejects It)

**Hebrew has no native italic tradition.** The Latin italic descends from chancery cursive — a 15th-century Italian script form with its own letter constructions, entirely parallel to the upright roman. Hebrew's own cursive traditions (Rashi script, modern Israeli handwriting) are not typographic italics in this sense — they are separate typefaces used for specific purposes (commentary, handwriting), not emphasis within body text.

Contemporary Hebrew fonts (IBM Plex Hebrew, Rubik, some Fontef releases) do ship **oblique** variants — mechanically slanted versions of the upright letter. These are a recent, Western-influenced convention, not a native Hebrew form. Hebrew readers frequently experience oblique Hebrew as "off" or "leaning" rather than as an emphasis signal, because the tradition has not trained the reader to associate slant with emphasis.

**Typotheque's Michal Sahar** and others in Israeli type scholarship have argued that Hebrew needs a "secondary style" — a second, visually distinct drawing of the alphabet that fills italic's emphasis role without importing Latin's slant convention. Some contemporary Hebrew families now ship such a style, variously labeled "secondary," "alternate," "display," or just "style 2." It works: readers perceive a change of typographic voice without the ambiguity of synthetic slant.

**Practitioner guidance:**

1. **Don't force synthetic oblique on a Hebrew font without a drawn italic or oblique master.** `font-style: italic` on such a font produces mechanical CSS slant, which looks unambiguously wrong.
2. **For emphasis in Hebrew body text, prefer bold or tracking** over oblique. These are native conventions.
3. **If your design system maps italic emphasis in Latin → Hebrew**, wire the mapping per-script. Don't assume `font-style: italic` means the same thing across scripts.
4. **If using a Hebrew family with a drawn oblique** (IBM Plex Hebrew, Rubik, Noto Sans Hebrew Italic) — it's acceptable for emphasis, but understand you're using a Western-influenced convention.

```css
em:lang(he) {
  font-style: normal;
  font-weight: 700;       /* bold emphasis — native convention */
}
/* or */
em:lang(he) {
  font-style: normal;
  letter-spacing: 0.06em;  /* tracked emphasis — native convention */
}
```

---

## Bilingual Metrics: Hebrew + Latin

The most-frequent design challenge: Hebrew and Latin on the same page, in the same line, in the same heading. Getting this right is the mark of a competent bilingual designer.

### The metric mismatch

Hebrew is **unicameral and box-shaped**. Every letter is roughly the height of a Latin uppercase letter — there is no x-height/cap-height distinction because there is no case. So when you set Latin "Hello" next to Hebrew "שלום" in the same font-size, the Hebrew reads visually larger — its letters fill the full box, while Latin lowercase fills only x-height.

Symptom: Latin body set at 16px next to Hebrew body at 16px looks small. Readers (Latin and Hebrew both) experience the Latin as "shrunken" or the Hebrew as "shouting."

### Fixes

1. **Use metric-matched fonts.** Fonts designed with both scripts in mind — **Rubik, Heebo, IBM Plex Sans Hebrew, Noto Sans Hebrew** — resolve this by drawing Hebrew at a height that harmonizes with Latin lowercase, not Latin uppercase. These are the safe choice for bilingual UI.

2. **Use `font-size-adjust` or manual per-script font-size.** If you must pair a Latin face with a separate Hebrew face, you can balance the optical size:

```css
:root {
  font-family: "Inter", sans-serif;
  font-size: 16px;
}
:lang(he) {
  font-family: "Frank Ruhl Libre", "Noto Serif Hebrew", serif;
  font-size: 0.95em;       /* shrink Hebrew ~5% to match Latin optical size */
}
```

The exact ratio depends on the fonts; test with real content. See `../metrics/metrics-glossary.md` and `../contemporary/metric-overrides.md` for the full metric-override recipe.

3. **Use `size-adjust` in `@font-face`** for the Hebrew face, nudging it down without changing the declared `font-size`:

```css
@font-face {
  font-family: "Hebrew Adjusted";
  src: url("frank-ruhl-libre.woff2") format("woff2");
  size-adjust: 95%;
  ascent-override: 90%;
  descent-override: 30%;
}
```

4. **Verify line-box height.** Hebrew's larger box often forces larger line-boxes than the Latin would at the same `font-size`, which *may* be what you want (more leading for Hebrew is correct) or may throw off baseline alignment in a table. Test with mixed content.

### Font-family stacks

```css
/* Bilingual UI — Heebo for Hebrew, metric-matched with Roboto Latin */
:root {
  font-family: "Heebo", "Roboto", system-ui, sans-serif;
}

/* Or split per lang */
:root          { font-family: "Inter", system-ui, sans-serif; }
:lang(he)      { font-family: "Assistant", "Heebo", sans-serif; }
:lang(he) em   { font-style: normal; font-weight: 600; }
```

System Hebrew fallbacks vary by OS:
- macOS / iOS: Arial Hebrew, Times New Roman (has Hebrew glyphs), SF Hebrew (San Francisco) since macOS Monterey+
- Windows: Arial, Tahoma, David, Miriam Fixed — bundled
- Android: Noto Sans Hebrew
- Linux: depends on distro; usually DejaVu Sans or Noto

---

## Diaspora Languages in Hebrew Script

Hebrew script is also used to write **Yiddish** (Central/Eastern European Jewish language, Germanic-family), **Ladino / Judeo-Spanish** (Sephardic, Romance-family, historically written in both Hebrew and Latin scripts), **Judeo-Arabic** (Arabic written in Hebrew letters by Jewish communities from Iraq, Morocco, Yemen, etc.), and historically many other Jewish diaspora vernaculars. Each adds its own orthographic conventions — Yiddish uses nikud differently from Hebrew, introduces digraphs (e.g., וו for /v/, יי for /j/), and includes characters like פֿ (pe with rafe for /f/). Ladino and Judeo-Arabic have their own conventions.

**For typography purposes**, a font labeled "Hebrew" typically covers the standard 22+5 consonant set and nikud but may not cover rare Yiddish digraphs, Ladino diacritics, or Judeo-Arabic extensions. If targeting those languages, verify the font's Unicode coverage against the specific orthographic needs. Open-source coverage is thinnest here; commercial Hebrew foundries like Masterfont and Fontef do better, and SIL fonts (Ezra, SBL) cover academic needs.

This file does not go deeper; see specialized references for each language.

---

## Web/CSS Gotchas

### 1. Don't `letter-spacing` nikud-heavy text aggressively

Unlike Arabic, Hebrew is non-connecting — `letter-spacing` works without breaking anything structural. But if your text carries nikud, aggressive letter-spacing separates marks visually from their base letters (even though the marks are still anchored correctly). Use restraint: `0.02em–0.04em` is safe for unpointed text; for pointed text, `0` or `0.01em` is preferable.

### 2. Unicode Hebrew block coverage

The Hebrew Unicode block is **U+0590–U+05FF** (main) plus **U+FB1D–U+FB4F** (Alphabetic Presentation Forms, including some precomposed ligatures like lamed-yod, alef-lamed, and vav-yod). Most modern Hebrew fonts cover the main block fully; presentation forms coverage is uneven. If your content includes presentation-form ligatures, test.

### 3. Don't strip nikud in normalization unless intentional

Unicode NFC composition keeps base + mark as separate codepoints (no precomposed Hebrew-vowel characters exist for most combinations — unlike Latin where `é` has a precomposed form). Normalizing Hebrew strips nothing by default. But **NFKC** (compatibility decomposition) in *some* implementations has been known to mishandle Hebrew presentation forms. Prefer **NFC** for Hebrew storage.

### 4. Mixed numbers and Hebrew

Digits in Hebrew prose render LTR per bidi — correct but sometimes surprising in UI. Dates, phone numbers, prices: the digit sequence reads left-to-right. Parenthetical wrapping of a digit sequence should use `<bdi>` or `unicode-bidi: isolate` to prevent bidi leakage:

```html
<p>הטלפון <bdi>+972-3-1234567</bdi> פעיל.</p>
```

### 5. `font-variant-caps` is a no-op

Hebrew has no case (§Unicameral). `font-variant-caps: small-caps` has no effect on Hebrew. It is not harmful, just wasted declaration. Scope case-related variants to `:lang(not(he))` in shared component CSS.

### 6. `text-transform: uppercase/lowercase/capitalize` is a no-op

Same reason. Remove from Hebrew-facing component tokens.

### 7. Hyphenation is not standard

`hyphens: auto` has limited Hebrew dictionary coverage. Hebrew prose does not hyphenate words at line breaks — this is a typographic convention, not a technical limitation. Set `hyphens: none` or leave default; do not rely on auto-hyphenation.

### 8. Line-height must be generous

Unitless, per the CSS inheritance rule. For pointed text, 1.8+; for unpointed body, 1.6+; for biblical cantillation, 2.0+. See §Nikud for the table.

### 9. Variable fonts for Hebrew are catching up

Rubik, Assistant, Heebo, Frank Ruhl Libre, IBM Plex Sans Hebrew all ship `wght` axes. `wdth` axes are rarer; `opsz` rarer still. Check family coverage before wiring `font-variation-settings`. Testing shows as of 2026-04 Hebrew variable-font stability is improving but still behind Latin — some weights interpolate cleanly, some have shape-breaking transitions. Test the axis ends you'll actually ship.

### 10. Self-hosting Hebrew webfonts is common

Israeli sites in particular frequently self-host Hebrew webfonts (privacy/GDPR-equivalent concerns, latency from Israeli datacenters vs Google Fonts edges, and editorial control). Google Fonts works fine globally but self-hosting is the pragmatic default for Israeli production. WOFF2 subsetting targeting U+0590–05FF + U+FB1D–FB4F + ASCII gives files around 20–40KB for most faces.

### 11. `::first-letter` and Hebrew drop caps

Works per-codepoint, but without case distinction, drop-caps for Hebrew rely on size alone. Traditional Hebrew manuscript illumination handles initials via a separate large decorative letter, hand-composed. `::first-letter` at a larger size can approximate this but is a blunt instrument; consider a separate inline span for quality work.

### 12. Fallback stacks must include a Hebrew face

```css
:lang(he) {
  font-family:
    "Heebo",                          /* primary */
    "Assistant",                      /* secondary */
    "Arial Hebrew",                   /* macOS */
    "David",                          /* Windows */
    "Noto Sans Hebrew",               /* cross-platform fallback */
    sans-serif;
  line-height: 1.7;
}
```

A Latin-only font stack (e.g., `font-family: "Inter", sans-serif`) on a Hebrew page will *work* — the browser falls back to some system Hebrew font per code-point — but metric mismatch and style divergence result. Declare explicitly.

---

## Accessibility

### Screen readers

- **VoiceOver** (macOS, iOS) — strong Hebrew support with Carmit voice on iOS/macOS; reads nikud-less Hebrew correctly from context, reads pointed Hebrew with correct vowels.
- **NVDA** (Windows) — Hebrew support via eSpeak NG or Microsoft David/Hedda voices. Quality is adequate; nikud handling varies.
- **JAWS** — commercial; Hebrew support solid in recent versions.
- **TalkBack** (Android) — Google TTS Hebrew voices; quality has improved dramatically in 2022–2026 and is now generally production-ready.

**Required.** Set `lang="he"` on the HTML element or on Hebrew sections. Without it, Hebrew reads with a Latin voice — unintelligible. Use `lang="he-IL"` for Israeli Hebrew specifically; screen readers may select different voices for `he-IL` vs generic `he`.

### Nikud and TTS

High-quality Hebrew TTS voices handle fully-pointed text correctly — the vowel marks disambiguate pronunciation. Without nikud, TTS has to infer vowels from context, which works most of the time but occasionally produces wrong readings for ambiguous words. For accessibility content targeting learners or language students, pointing the text improves TTS accuracy.

### Biblical cantillation

Cantillation marks are **recitation guidance, not pronunciation content**. Most TTS engines ignore them, which is correct. A specialized biblical-Hebrew reader (for liturgical apps) may respect them for chanting.

### Contrast and size

WCAG 2.2 contrast rules apply normally. Hebrew body text is often set slightly larger than Latin equivalent — empirically, Hebrew readers prefer ~14–16px minimum for body, similar to Latin. For pointed text (nikud visible), bump up: nikud are small marks that need resolution. 16–18px body is common for pointed educational content.

### Dyslexia and Hebrew

See `../accessibility/dyslexia.md` for the general evidence review. Hebrew-specific note: the letter disambiguation traps (§Letter Disambiguation) are an accessibility concern independent of dyslexia — choose faces that preserve ב/כ, ה/ח, ד/ר distinctions clearly for all readers.

---

## Anti-patterns

1. **"RTL-flip and ship."** Same as Arabic — treating Hebrew as Latin-with-direction-flipped. Misses nikud, unicameral emphasis patterns, metric harmony, letter disambiguation. Surface-level, insulting.

2. **Synthetic italic on a Hebrew font without an oblique master.** Produces mechanically slanted text that Hebrew readers perceive as wrong. Scope italic emphasis to Latin; use bold or tracking in Hebrew.

3. **Latin-only font stack on a Hebrew page.** Falls back to system Hebrew, metric mismatch, style divergence. Always declare an explicit Hebrew face in the stack.

4. **Same `line-height` for Hebrew and Latin.** Hebrew (especially pointed) needs more leading. Unitless line-height with `:lang(he)` overrides solves it.

5. **Pointed text in adult body copy.** Nikud is visual noise for fluent adult readers. Ship pointed text only when pedagogically needed.

6. **Straight quotes and ASCII apostrophes where geresh/gershayim are correct.** In publication-quality Hebrew, substitute U+05F3 and U+05F4.

7. **Latin hyphen in Hebrew compound words.** Use maqaf (U+05BE) for traditional Hebrew; Latin hyphen is acceptable but less correct.

8. **Assuming Hebrew-letter numerals work via `font-variant-numeric`.** They don't. Use `Intl.NumberFormat` with the `hebr` numbering system or author content directly.

9. **Attempting `text-transform: uppercase` for Hebrew emphasis.** No effect; signals Latin-first CSS. Use weight or tracking.

10. **`<bdo>` to force direction.** Use `unicode-bidi: isolate` (or `isolate-override` if you truly need a forced direction inside an isolated context). `<bdo>` is a blunt instrument.

11. **Justified Hebrew body text.** Rivers or crude letter-stretching. Prefer ragged.

12. **Ignoring bilingual metric mismatch.** Hebrew + Latin at the same font-size often looks wrong. Either pick metric-matched families (Heebo, Rubik, IBM Plex, Noto pairs) or use `size-adjust`/`font-size-adjust`.

13. **Using Rashi script for body text.** Rashi is for commentary, signaled as such in reader tradition. Using it for primary text miscommunicates.

14. **Attempting to render Torah scrolls via web type.** STAM is hand-scribed and halakhically constrained. Web renderings are for study/reference only; never ritual use.

15. **Stripping nikud on paste normalization.** If the user pasted pointed text, they likely want the points. Don't strip silently.

---

## Sources

Accessed 2026-04-18:

- W3C — *Hebrew Layout Requirements* (HLReq, draft): https://w3c.github.io/hlreq/
- W3C — Hebrew Script Resources: https://www.w3.org/International/hlreq/hebr/
- W3C — Text Layout and Typography Checklist: https://w3c.github.io/typography/checklist
- Unicode Consortium — Hebrew block (U+0590–05FF): https://www.unicode.org/charts/PDF/U0590.pdf
- Unicode Consortium — Alphabetic Presentation Forms (U+FB00–FB4F): https://www.unicode.org/charts/PDF/UFB00.pdf
- Unicode Consortium — *The Unicode Standard*, Chapter 9 (Middle Eastern Scripts): https://www.unicode.org/versions/latest/ch09.pdf
- Microsoft Typography — *Developing OpenType Fonts for Hebrew Script*: https://learn.microsoft.com/en-us/typography/script-development/hebrew
- n8willis — *OpenType Shaping for Hebrew*: https://github.com/n8willis/opentype-shaping-documents/blob/master/opentype-shaping-hebrew.md
- Culmus Project — OpenType Hebrew font documentation: https://culmus.sourceforge.io/opentype/index.html
- Typotheque / Peter Biľak — *Designing Hebrew Type*: https://www.typotheque.com/articles/designing-hebrew-type
- Typotheque / Michal Sahar — *Secondary Style in Hebrew Typography*: https://www.typotheque.com/articles/secondary-style-in-hebrew-typography
- *I Love Typography* — *Designing Hebrew Fonts*: https://ilovetypography.com/2017/10/19/designing-hebrew-fonts/
- *Hebrew Type* — *The Mysterious Gershayim*: https://hebrewtype.com/the-mysterious-gershayim/
- Wikipedia — Rashi script: https://en.wikipedia.org/wiki/Rashi_script
- Wikipedia — Tag (Hebrew writing) / Tagin: https://en.wikipedia.org/wiki/Tag_(Hebrew_writing)
- Wikipedia — Hebrew numerals: https://en.wikipedia.org/wiki/Hebrew_numerals
- Wikipedia — Gershayim: https://en.wikipedia.org/wiki/Gershayim
- Wikipedia — Unicode and HTML for the Hebrew alphabet: https://en.wikipedia.org/wiki/Unicode_and_HTML_for_the_Hebrew_alphabet
- Open Siddur Project — Hebrew Fonts catalog: https://opensiddur.org/help/fonts/
- Google Fonts — Frank Ruhl Libre, Heebo, Rubik, Assistant specimens: https://fonts.google.com/?subset=hebrew
- Fontwerk — Yanek Iontef designer page: https://fontwerk.com/en/designers/yanek-iontef
- Adobe Fonts — Fontef foundry page: https://fonts.adobe.com/foundries/fontef

Additional depth (not cited inline):

- Ada Yardeni, *The Book of Hebrew Script* (Carta Jerusalem, 2002) — historical script development
- SBL Handbook of Style, 2nd ed. — scholarly biblical-publishing conventions
- Israel Institute of Language guidance on Hebrew typography
- Gerry Leonidas' Reading University MA Typeface Design program — Hebrew student work and thesis archive
- Michael Everson's Unicode proposals for Hebrew script extensions
- *Ot Achat* and other Hebrew typography periodicals
