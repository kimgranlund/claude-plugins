---
date: 2026-04-17
coverage: medium
peers:
  - ./latin.md
  - ./arabic.md
  - ./thai.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
primary_sources:
  - https://www.w3.org/International/ilreq/devanagari/
  - https://w3c.github.io/ilreq/
  - https://www.w3.org/TR/deva-gap/
  - https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-12/
  - https://learn.microsoft.com/en-us/typography/script-development/devanagari
  - https://github.com/n8willis/opentype-shaping-documents/blob/master/opentype-shaping-devanagari.md
  - https://harfbuzz.github.io/opentype-shaping-models.html
  - https://www.type-together.com/devanagari-type-anatomy
  - https://www.typotheque.com/research-survey/regional-forms-of-devanagari-survey-report
  - https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari
  - https://www.indiantypefoundry.com/
---

# Devanagari Script Typography

**Scope disclaimer.** This is a *practitioner-medium* reference for a web/UI typographer who has never set Devanagari before. It covers enough to ship Hindi/Marathi/Nepali body text competently and to diagnose shaping problems, but it is not scholar-depth. Authoritative depth lives in the W3C's *Indic Layout Requirements* (ILReq, Devanagari section), the *Devanagari Gap Analysis*, Unicode Standard Chapter 12, Microsoft Typography's Devanagari script-development guide, the HarfBuzz/USE shaping documents by Nathan Willis, Pooja Saxena's Devanagari Type Anatomy for TypeTogether, and Typotheque's *Regional Forms of Devanagari* survey. Where this file gives a practical rule, assume the scholarly answer is more nuanced.

**Why Devanagari is easy to misread as "just another script."** Devanagari is written left-to-right like Latin, uses spaces between words like Latin, and its Unicode coverage has been stable for decades. It *looks* like a drop-in. It is not. It is an **abugida** (consonant-carries-inherent-vowel), its glyphs **hang from a top-line rather than sit on a baseline**, its vowel marks **reorder between logical and visual order**, and its conjunct system produces hundreds of context-specific glyphs that the shaper assembles at runtime. Teams that treat Devanagari as Latin-with-a-different-font end up with broken conjuncts, visible halants mid-word, and body text that looks clipped because leading was budgeted for x-height.

**What this file covers.** Script fundamentals (abugida, inventory, direction). The shirorekha (head line) and why it's load-bearing. Vowel signs (matras), including the i-matra reordering that surprises every first-timer. Conjuncts: halant/virama, reph, rakar, and the five conjuncts you must see render correctly before you ship. Numerals (Devanagari digits vs ASCII). Punctuation (danda, double danda). Line-height and measure. Differences between Hindi, Marathi, and Nepali typographic conventions. A fonts list organized by genre. Web/CSS gotchas with actionable rules. Source-code concerns (Unicode blocks, logical vs visual order). Accessibility. An anti-patterns list.

---

## Script Overview

### Abugida, not alphabet

Devanagari is an **abugida** (also called an *alphasyllabary*). Each consonant letter carries an **inherent short-`a` vowel** (the *schwa*) unless that vowel is explicitly suppressed or replaced. So the single consonant letter क is not "k" — it is "ka". To write "k" without the inherent vowel, you append the **virama** / **halant** sign (◌्), producing क्. To write "k" with a different vowel, you attach a vowel sign (matra): कि = "ki", की = "kī", कु = "ku", के = "ke", etc.

This has three practical consequences for a typographer:

1. The *typographic syllable* (the shaping unit) is not "one character" — it's a **consonant cluster plus its vowel sign plus any modifiers**, a structure Indic shaping documentation calls an **orthographic syllable** or **cluster**.
2. The visual width of one rendered syllable varies wildly. One cluster might be a single narrow consonant; the next might be a three-consonant conjunct stack with a wide ā-matra on the right and an anusvara dot on top.
3. Measure (line length) cannot be counted in characters the way Latin is. See *Line-height and Measure*.

### Direction

Devanagari is written **left-to-right (LTR)**. No bidi surprises at the word level. You do get bidi complexity when Latin numbers or Latin acronyms are mixed into Hindi text, but the UBA (Unicode Bidirectional Algorithm) handles that the same way it handles mixed-script Latin — no special CSS `direction` attribute needed.

### Inventory

Modern Hindi Devanagari has **46 primary letters**:

- **13 vowels (svara / स्वर):** अ आ इ ई उ ऊ ऋ ए ऐ ओ औ, plus ऌ and ॠ which appear in Sanskrit but are rare in Hindi.
- **33 consonants (vyanjana / व्यंजन):** organized in traditional phonetic rows (velars क ख ग घ ङ, palatals च छ ज झ ञ, retroflexes ट ठ ड ढ ण, dentals त थ द ध न, labials प फ ब भ म, and semivowels/sibilants य र ल व श ष स ह).

Marathi adds ळ (retroflex lateral). Marathi, Nepali, and modern Hindi also use **nukta-modified forms** (क़ ख़ ग़ ज़ ड़ ढ़ फ़) for Perso-Arabic and English loanwords, written either as a precomposed code point or as base consonant + U+093C NUKTA.

### Languages that use Devanagari

Hindi, Marathi, Nepali, Sanskrit (primary modern script), Bodo, Dogri, Konkani, Maithili, Magahi, Bhojpuri, Awadhi, and several regional languages. Sindhi is written in multiple scripts including a Devanagari form used especially in India. Each language has conventions that diverge in small but consequential ways (see *Language Variants*).

---

## Shirorekha (the Head Line)

The single most visually distinctive feature of Devanagari is the **shirorekha** (शिरोरेखा, literally "head-line"): the horizontal stroke along the top of each letter and — critically — **continuous across the letters of a word**. In Devanagari, letters **hang from the head line** the way Latin letters sit on a baseline.

Pooja Saxena and others working on Devanagari anatomy have argued the headline, not the baseline, is the **primary organizing metric** of Devanagari typography. When a user's eye tracks a line of Hindi, it is tracing the shirorekha — a reader can identify a whole word because the shirorekha connects its constituent letters into one visual unit with breaks at spaces.

### Load-bearing, not decorative

Treat the shirorekha as structural. If you set type in a font that renders the shirorekha incorrectly (broken where it should be continuous, or absent), **the reading experience degrades** even when every individual glyph is correct. A word whose shirorekha is broken mid-word reads as two half-words.

Rules of thumb:

- **Body text:** use a font whose shirorekha is continuous within each word. This is the default behavior for essentially all production Devanagari text fonts — just don't override it.
- **Display type:** some contemporary designers deliberately **break** or **thin** the shirorekha for expressive effect (geometric-modern Devanagari, especially from Indian Type Foundry and Typotheque). This is a stylistic choice with implications: display text reads more like a logotype and less like prose. Acceptable for headlines; inappropriate for body.
- **Never `letter-spacing`:** applying CSS `letter-spacing` to Devanagari inserts space between the glyphs that would otherwise share a shirorekha, visually fragmenting the word into disconnected pieces. This is the single most common CSS mistake first-timers make. See *Web/CSS Gotchas*.

### Traditional vertical metrics (for vocabulary)

Mukund V. Gokhale's influential Devanagari metrics vocabulary defines seven horizontal reference lines: *urdhvarekha* (upper-most), **shirorekha** (head), *skandharekha* (shoulder), *nabhirekha* (navel), *zanurekha* (thigh), *padrekha* (foot), *talrekha* (bottom). You do not need to memorize these to ship, but you'll see them in type-foundry specimens and font-design docs.

---

## Vowel Signs (Matras)

When a dependent vowel combines with a consonant, it attaches as a **matra** (मात्रा). Matras are **positional marks** — not separate letters on the baseline. They sit above, below, to the right, or to the left of the base consonant.

### The positions

| Matra | Sound | Position | Example |
|-------|-------|----------|---------|
| ा (U+093E) | ā (long a) | **right** of consonant | क + ा = का (kā) |
| ि (U+093F) | i (short i) | **left** of consonant (see reordering below) | क + ि = कि (ki) |
| ी (U+0940) | ī (long i) | **right** of consonant | क + ी = की (kī) |
| ु (U+0941) | u (short u) | **below** consonant | क + ु = कु (ku) |
| ू (U+0942) | ū (long u) | **below** consonant | क + ू = कू (kū) |
| ृ (U+0943) | ṛ (vocalic r) | **below** consonant | क + ृ = कृ (kṛ) |
| े (U+0947) | e | **above** consonant | क + े = के (ke) |
| ै (U+0948) | ai | **above** consonant (double stroke) | क + ै = कै (kai) |
| ो (U+094B) | o | **above + right** (decomposes into e-mark + ā-mark) | क + ो = को (ko) |
| ौ (U+094C) | au | **above + right** (decomposes into ai-mark + ā-mark) | क + ौ = कौ (kau) |

Additional modifiers:

- **Anusvara** ◌ं (U+0902): nasalization, placed as a dot above the shirorekha.
- **Chandrabindu** ◌ँ (U+0901): nasalization with moon, placed above.
- **Visarga** ◌ः (U+0903): post-vocalic `h`-aspiration mark, placed to the right (two stacked dots).

The above-marks (e-matra, ai-matra, anusvara, chandrabindu) sit **above the shirorekha** — the typographer's equivalent of ascenders. The below-marks (u-matra, ū-matra, ṛ-matra) sit **below the base of the consonant** — like descenders. That's why Devanagari needs more leading than Latin: there are routinely glyphs both above and below each line, and they can stack in sequences like विद्‍वांसों (vidvāṃsõ).

### The i-matra reordering problem

Of the ten primary matras, only ि (short-i, U+093F) is drawn **visually to the left** of the consonant it follows logically. This is the single most important thing to understand about Devanagari text handling.

- **In memory (logical order):** CONSONANT then VOWEL. The user types क then ि. The string is stored as `\u0915\u093F`.
- **On screen (visual order):** the i-matra glyph is rendered **to the left** of the consonant. The reader sees कि with the hook-like i-mark sitting to the *left* of क.

This mismatch is called **pre-base matra reordering**, and it is handled by the OpenType shaping engine at runtime, not by the application or the user. Specifically:

- The font's GSUB tables include a `pres` (pre-base substitution) feature that selects the **width-variant of the i-matra** appropriate to the following consonant (the i-matra "points to" the stem of that consonant, and the matra glyph stretches across its width).
- HarfBuzz's Indic shaper performs the visual reordering: the shaper places the i-matra glyph at the visual position **to the left of the base consonant glyph** in the output glyph stream.

**Practical implications:**

- A byte-level search for the substring "कि" works correctly because it matches logical order.
- A **cursor-movement or caret-positioning algorithm** that doesn't understand Indic clusters will place the caret in visually nonsensical places. Use grapheme-cluster iteration (ICU, Intl.Segmenter with `granularity: 'grapheme'`), never byte-level or codepoint-level iteration for editing Devanagari.
- Copy-paste between applications usually works because it operates on logical order.
- If you see a text string on screen where the i-matra is on the **right** of the consonant, you are looking at unshaped (raw) glyphs. Something is broken in the font, the shaper, or the font loading — often `font-feature-settings` has been overridden, or a non-Devanagari font is being used as a fallback.

### Two- and three-part matras

The o-matra (ो) and au-matra (ौ) are logically single characters but the shaper typically decomposes them into constituent parts (an e-mark above + an ā-mark on the right) during shaping. You usually don't touch this — it's handled — but it matters when auditing a font for coverage: the font needs the decomposed components, not just the precomposed forms.

---

## Conjuncts (Sanyukta Akshara)

When two or more consonants occur with no intervening vowel — e.g., "kt" in Sanskrit-origin words — they form a **conjunct** (संयुक्त अक्षर, *sanyukta akshara*, "joined letter"). Conjunct formation is the single richest and most complex part of Devanagari shaping.

### The halant / virama

The trigger for conjunct formation is the **halant** (हलन्त) / **virama** (विराम) sign, Unicode **U+094D DEVANAGARI SIGN VIRAMA** (◌्). The halant **suppresses the inherent vowel** of the consonant it attaches to, turning a live consonant into a **dead consonant**.

Two possible outcomes when a sequence `CONSONANT₁ + HALANT + CONSONANT₂` is encountered:

1. **Conjunct form.** The shaper finds a ligature (in the font's GSUB tables) for the pair and substitutes a single conjunct glyph. The halant becomes invisible — it's consumed by the ligature. This is the normal outcome for the ~400–600 common conjuncts a production Devanagari font covers.
2. **Visible halant.** If no conjunct glyph exists (rare consonant pair, poorly-covered font, deliberately plain style), the halant is rendered as a visible hook-like stroke below the first consonant. This is **unusual in modern Hindi text** (except for some technical/linguistic contexts) — if you see visible halants in body text, your font coverage is insufficient.

**Rule of thumb:** a good production font has ~400–600 precomposed conjunct glyphs. Fonts intended for Sanskrit scholarship (Chandas, Sahadeva) go well beyond that to handle rare Vedic clusters. Fonts intended for modern Hindi UI can get away with fewer, but visible halants in common words indicate a bad pick.

### Key conjuncts to eyeball before shipping

A sanity check: set these five conjuncts in your chosen font at body size. If any of them render as "two letters with a visible halant between them" instead of as a unified glyph, the font is not production-ready for Devanagari.

| Conjunct | Components | IPA-ish | Notes |
|----------|------------|---------|-------|
| **क्ष** (kṣa) | क् + ष | "ksh" | Very common. Some fonts render as fully merged ligature; others as half-k + sha. |
| **त्र** (tra) | त् + र | "tra" | The second consonant r takes a subjoined "rakar" form. |
| **ज्ञ** (jña) | ज् + ञ | Historically "jña"; in Hindi pronounced "gya" | Visually bears no obvious relation to its components — it's a true ligature. |
| **श्र** (śra) | श् + र | "shra" | Another rakar case; the r attaches as a subjoined stroke. |
| **द्ध** (ddha) | द् + ध | "ddha" | Stacked vertically in most modern fonts — d on top of dha rather than side-by-side. |

If these look right, the font almost certainly handles the long tail of conjuncts correctly as well.

### Reph (superscript r-before)

When the consonant **र (ra)** is followed by a halant **at the beginning of a syllable** (i.e., a word-initial or post-vowel `r + halant + consonant` sequence), the r is not rendered as a full consonant — it becomes a small **hook-like mark positioned above the shirorekha** of the *following* consonant. This is the **reph** (रेफ).

Example: `र् + म + ◌ा` (logical order: r, halant, m, ā-matra) → शर्मा (Śarmā). The र is the small curved mark above the म. The reph reads as "(the following consonant) preceded by r".

**In OpenType:** reph is controlled by the `rphf` (reph form) feature. The shaper identifies the initial `r + halant` and substitutes the reph glyph, moves it to its correct visual position (above the consonant that follows it in the syllable), and the syllable renders as expected.

### Rakar (subjoined r-after)

When **र (ra)** appears *after* another consonant with halant in **medial position** (i.e., `consonant + halant + r`, not word-initial), the r is typically rendered as a **small diagonal stroke below and to the right of the base consonant**. This is the **rakar** (रकार).

Example: `त + ् + र` → त्र. The hook-like mark descending from त is the rakar form of र.

Controlled by the `rkrf` (rakar form) feature in OpenType. Note that in some fonts, the `tra` combination (त्र) is instead handled as a precomposed ligature via `cjct` — implementation choice.

**Reph vs rakar** is a common source of confusion for first-time Devanagari readers (and designers). Both are ways of rendering र when it's in a conjunct; the distinction is purely positional:

- **r *before* the other consonant → reph** (above the *following* letter).
- **r *after* the other consonant → rakar** (below the *preceding* letter).

### Other special conjunct behaviors

- **Half forms.** Many consonants have a "half form" — the full glyph with the rightmost vertical stem removed. The half form appears as the first element of a conjunct when the cluster doesn't ligate into a single glyph. `sk` might render as half-s followed by full k. Controlled by the `half` feature in OpenType; it's why every production Devanagari font ships half-forms for most consonants.
- **Nukta consonants.** क़ ख़ ग़ ज़ फ़ ड़ ढ़ are nukta-modified consonants for Perso-Arabic and English loans. In Unicode they can be encoded as precomposed codepoints (e.g. क़ = U+0958) *or* decomposed as base + nukta (क + ◌़ = U+0915 U+093C). **Most modern content uses the decomposed form**, and the canonical Unicode decomposition goes that direction. The `nukt` OpenType feature handles nukta ligatures. If you see text where nukta-dots appear detached from their consonant, the font probably lacks `nukt` coverage.

### Full OpenType feature pipeline (reference)

For completeness, these are the features a USE-style Indic shaper applies for Devanagari, in order. You don't manipulate these directly — the shaper does — but seeing the pipeline helps when debugging:

```
nukt → akhn → rphf → rkrf → pref → blwf → half → pstf → cjct
  ↓
(reordering)
  ↓
init → pres → abvs → blws → psts → haln
  ↓
calt → liga → (discretionary: dlig, hlig)
```

Stages one through `cjct` are **basic shaping forms**. Stages beginning with `init` are **presentation forms**. Fonts that claim "Devanagari support" but cover only `liga`/`calt` — i.e., standard ligatures — will fail on reph, rakar, and conjuncts. Check specimens for all five key conjuncts above.

---

## Ligatures

Devanagari has two distinct "ligature" concepts and conflating them causes trouble:

1. **Mandatory shaping ligatures.** These are the conjuncts described above (`akhn`, `pres`, `abvs`, `blws`, `psts`, `haln`, `cjct`). They are not optional — disabling them produces broken text. OpenType exposes them via script-specific features, and every modern shaper applies them unconditionally. **Do not touch these via `font-feature-settings` unless you know exactly what you're doing.**
2. **Discretionary stylistic ligatures.** Controlled by `dlig` (discretionary ligatures) and `hlig` (historical ligatures) — rare in Devanagari, but some specimen fonts ship ornate traditional conjunct forms via `dlig`. Useful for display type; irrelevant for body.

If you want to *disable* discretionary ligatures in a display setting, use `font-variant-ligatures: no-discretionary-ligatures;` — never `font-feature-settings: 'liga' off;`, which will turn off standard ligatures and may cascade to break conjuncts.

---

## Numerals

Two digit systems coexist in modern Devanagari usage:

| Devanagari digits | ASCII digits |
|-------------------|--------------|
| ० १ २ ३ ४ ५ ६ ७ ८ ९ | 0 1 2 3 4 5 6 7 8 9 |
| U+0966 – U+096F | U+0030 – U+0039 |

**Which one to use** is a content-level decision, not a typographic one. In contemporary Hindi usage:

- Newspapers, government forms, and traditional prose often use **Devanagari digits**.
- Technical, scientific, educational, and financial contexts increasingly use **ASCII digits** — they're globally recognizable and interoperate with Latin-script data.
- Marathi and Nepali lean similarly.
- Sanskrit scholarly editions prefer Devanagari digits.

### CSS and numerals

- `font-variant-numeric` **does not switch between Devanagari and ASCII** digit systems. It controls within-system features like `tabular-nums`, `oldstyle-nums`, etc. The digit-system choice is a *content* choice.
- To produce Devanagari digits programmatically from a number, use `Intl.NumberFormat('hi-IN-u-nu-deva')` or `'ne-NP-u-nu-deva'`. ASCII by default with `hi-IN` is common; explicit `-u-nu-deva` forces Devanagari.
- **Tabular figures are rare.** Most Devanagari fonts ship proportional digits only. If you need columnar alignment for tables, either pick a font that explicitly claims `tnum` coverage (Noto Sans Devanagari and Mukta both support it at time of writing) or fall back to ASCII digits for the numeric content.

---

## Punctuation

### Danda (।) and double danda (॥)

- **Danda** (दण्ड, "stick") U+0964 — the vertical line `।` — functions as the **end-of-sentence** marker in Sanskrit tradition and still appears regularly in Hindi, Marathi, and Nepali prose. Equivalent to a period.
- **Double danda** U+0965 — `॥` — marks **end of a verse, paragraph, or section**. Common in scriptural and poetic Sanskrit text; rarer in modern prose but used in Hindi poetry and traditional religious text.

### Modern Latin-borrowed punctuation

In modern newspapers, books, and web content:

- **Full stop** is *increasingly* rendered as a Latin period `.` in modern Hindi, especially in journalistic and technical writing. Traditional prose still uses danda.
- **Marathi** is somewhat more conservative and danda persists more visibly than in modern Hindi.
- **Commas, colons, semicolons, question marks, exclamation marks** are all borrowed from Latin (`,`, `:`, `;`, `?`, `!`). Devanagari has no native analog for most of these.
- **Quotation marks** are typically Latin — either straight `" "` or curly `" " ' '`, following the same rules as Latin usage. Some publications use Latin-guillemets `« »`.
- **Hyphens and dashes** are Latin (`-` `–` `—`).

### Stylistic notes

- `।` and `॥` **share the baseline with the shirorekha** — they align with the text line, not sitting underneath it like a Latin period. Respect their vertical metrics; don't substitute Latin `|` which has different metrics and spacing.
- The danda has implicit spacing behavior (usually a full space before AND after in traditional typesetting), but modern Hindi more commonly treats it as equivalent to a period with a single trailing space.

---

## Line-height and Measure

### Why Devanagari needs more leading than Latin

A Latin body letter occupies roughly one x-height above the baseline plus ascender/descender. A Devanagari cluster can routinely occupy:

- the shirorekha and body glyph (analogous to Latin x-height),
- plus an above-mark (e-matra, ai-matra, anusvara, chandrabindu — potentially stacked),
- plus a below-mark (u-matra, ū-matra, ṛ-matra — again potentially stacked in Sanskrit),

...in a single rendered cluster. The vertical stack is higher than Latin on both ends. If you set `line-height: 1.4` — comfortable for Latin body — the above-marks of one line will visually collide with the below-marks of the line above, producing crowded reading.

**Practical leading targets:**

| Context | Latin | Devanagari |
|---------|-------|------------|
| UI / small dense labels | 1.2–1.35 | 1.45–1.55 |
| Body prose | 1.4–1.55 | 1.6–1.75 |
| Generous editorial body | 1.5–1.65 | 1.7–1.85 |
| Display (large sizes) | 1.0–1.15 | 1.15–1.3 |

Rule of thumb: **add roughly 0.15–0.2 to whatever line-height value you'd use for Latin body**. The W3C's Devanagari Layout Requirements and Google Fonts' language-script classification both treat Devanagari as a "Tall" script requiring additional leading.

### Measure

Latin measure (CPL, characters per line) conventions — 45–75 for body text, ~66 ideal — **do not translate directly to Devanagari**. The reason: one Devanagari cluster can be visually a quarter the width of another, depending on conjunct complexity, matra stack, and half-form vs full-form rendering.

**Two practical approaches:**

1. **Measure in words per line.** Hindi body text reads comfortably at roughly 10–14 words per line, which approximates the Latin 45–75 CPL target for most fonts. Mukta, Noto Sans Devanagari, and Hind all produce roughly this density at their recommended body size.
2. **Measure in CSS `ch` units, but adjust.** `1ch` in a Devanagari font is the width of the `0` glyph — which has no direct relation to the rendered width of text. Avoid `max-width: 65ch;` for Devanagari-primary content. Prefer `max-width: 60rem;` or similar rem-based values tuned empirically.

If the text mixes Devanagari with Latin (common in technical Hindi — English loanwords in Roman, product names in Roman), the measure should be tuned for the Devanagari runs, which will automatically give the Latin runs a little extra room.

### Font size

Devanagari tends to **need a slightly larger apparent body size than Latin** to read comfortably, because of the visual density of matras and conjuncts. A Latin 16px body often reads as a Devanagari 17–18px equivalent. This is handled organically by picking a Devanagari font whose *designed x-equivalent* is visually large (Mukta is known for this; some system fonts like Mangal run smaller) — not typically by hand-tuning `font-size` per script.

---

## Language Variants (Hindi, Marathi, Nepali)

The three dominant modern languages written in Devanagari share a core letter inventory but have real typographic differences. A well-built font ships OpenType `locl` (localized forms) tables keyed on the language tag — **set `lang` correctly on your elements** (`lang="hi"`, `lang="mr"`, `lang="ne"`) and the shaper will select the regionally preferred forms automatically.

OpenType language system tags: Hindi = **HIN**, Marathi = **MAR**, Nepali = **NEP**.

### Marathi

- **Additional letter: ळ (Marathi letter LLA, U+0933)** — retroflex lateral. Appears in countless Marathi words (दिवाळी Diwālī, मराठी Marāṭhī). Hindi doesn't use this character. Sanity-check: your font must cover ळ if you're targeting Marathi; many Hindi-only fonts omit it.
- **Eyelash reph.** When र (ra) appears as a conjunct first-member before glides and semivowels (y, v), Marathi and Nepali use a distinct **eyelash-shaped reph form** rather than the standard reph hook. Examples: र्‍य (rya), र्‍व (rva) — note the zero-width joiner U+200D before the halant to trigger the eyelash form in Unicode. Standard Hindi does not use the eyelash form.
- Marathi is somewhat more conservative about punctuation — the danda `।` is still common for sentence-ending where modern Hindi often uses a period.

### Nepali

- **Same inventory as Hindi** for everyday text, plus ळ is *occasionally* seen in Nepali loan contexts.
- **Eyelash reph** is used in the same contexts as Marathi.
- **Loanword handling differs.** Nepali borrows heavily from Nepali-language substrates and differently-stabilized Sanskrit forms. Shaper output is usually identical to Hindi, but some stylistic conjuncts (particularly in religious or formal text) follow different conventions.
- **Digit usage:** Nepali traditional publications use Devanagari digits more persistently than modern Hindi; technical Nepali uses ASCII.

### Hindi

- **Default target** for most Devanagari web content. If you don't know which language variant your content is, Hindi is the sane default and `lang="hi"` is what most OS keyboards produce for unlabeled text.
- Does **not** use ळ or the eyelash reph.
- Uses nukta forms क़ ख़ ग़ ज़ फ़ and ड़ ढ़ for Perso-Arabic and English-derived words; these are ubiquitous in modern Hindi journalism.

### Sanskrit

- Uses the full vowel inventory including ऌ and ॠ.
- Conjunct density is much higher than Hindi — scholarly Sanskrit can stack 3–4 consonants in a single cluster. Requires a font with deep conjunct coverage (Chandas, Sahadeva, Adobe Devanagari, Noto Serif Devanagari).
- Vedic texts need the **Vedic Extensions block (U+1CD0–U+1CFF)** for tone-marks and special signs. Sanskrit-specialist fonts cover it; general Hindi UI fonts don't.

---

## Fonts Available

This is a non-exhaustive genre-organized list. All are available as web-deliverable files (Google Fonts, Adobe Fonts, or direct licenses) unless noted.

### Free, broad coverage (default starting point)

- **Noto Sans Devanagari** — Google's broad-coverage sans. ~922 glyphs per weight cut in the 2025 release. Covers Hindi, Marathi, Nepali, Sanskrit common conjuncts, nukta forms, Vedic extensions via companion fonts. Variable version available (wght + wdth axes). **The sane default.**
- **Noto Serif Devanagari** — serif companion. Better for long-form prose, scholarly work, editorial body.

### Free / open via Google Fonts

- **Mukta, Mukta Vaani, Mukta Mahee, Mukta Malar** — by Ek Type. Mukta is a humanist sans with generous x-height (Devanagari height equivalent); good for UI. Wide weight range.
- **Hind, Hind Siliguri, Hind Vadodara, Hind Madurai** — by Indian Type Foundry, released open. Cleaner-modern Devanagari. Hind is Hindi-leaning; the geographic variants target other Indic scripts in the same style family.
- **Tiro Devanagari Hindi, Tiro Devanagari Marathi, Tiro Devanagari Sanskrit** — by Tiro Typeworks (John Hudson). Language-specific tuning per variant. Excellent scholarship- and body-grade type. Subtly different i-matra and conjunct forms per language.
- **Rozha One** — high-contrast didone-inspired display face. Not for body — designed for headlines.
- **Kalam** — handwritten-style casual face. Informal/personal use; not appropriate for editorial body.
- **Khand** — condensed sans for headlines and tight labels.
- **Eczar** — serif with old-style proportions, suited to literary and editorial prose.

### Commercial (Indian Type Foundry)

- **Kohinoor Devanagari** — low-contrast multi-use family, licensed to major brands including Apple. Body/display flexible. Used widely in Indian UI work.
- **ITF Devanagari** — the foundry's eponymous family by Satya Rajpurohit. 10 styles.
- **Uma**, **Tulika**, **Rasa** — various specialist faces from ITF's large catalog.

### Scholarly / Sanskrit

- **Chandas** — free, exhaustive Sanskrit coverage including Vedic extensions and rare Vedic conjuncts. Not pretty; correct.
- **Sahadeva** — another free Sanskrit-focused face.
- **Sanskrit 2003** — widely used in scholarly PDFs; older but reliable.
- **Adobe Devanagari** — commercial, broad coverage including scholarly conjuncts.

### Microsoft / system

- **Mangal** — Microsoft's default Windows Devanagari font. Ubiquitous in Windows-rendered content but not aesthetically strong. Treat as a last-resort fallback.
- **Utsaah** — newer Microsoft Devanagari face, somewhat more contemporary.
- **Nirmala UI** — Microsoft's UI-optimized Indic family, covers Devanagari plus other Indian scripts.

### Apple / system

- **Kohinoor Devanagari** — ships with macOS and iOS as the default Hindi/Marathi face.
- **Devanagari MT** — legacy Apple Devanagari.

### Font selection heuristic

If you're shipping a generic Hindi/Marathi product and don't have strong brand direction:

1. Start with **Noto Sans Devanagari** (free, well-maintained, excellent conjunct coverage).
2. If typography is a product value (publishing, editorial, premium brand), evaluate **Mukta**, **Hind**, **Kohinoor Devanagari**, or **ITF Devanagari** against your brand.
3. Pair with **Noto Serif Devanagari** or **Eczar** if you need a serif for long-form body.
4. For Sanskrit scholarly work, prefer **Chandas**, **Adobe Devanagari**, or **Tiro Devanagari Sanskrit**.

---

## Web/CSS Gotchas

### HarfBuzz and USE shaping are uniform in 2026

As of 2026-04, HarfBuzz handles Devanagari shaping in all three major browser engines (Blink, Gecko, WebKit) via its Indic shaper (which shares infrastructure with the Universal Shaping Engine). Shaping behavior is **effectively identical** across browsers — a 10-year-old problem is now a non-issue. Devanagari text rendered in Chrome, Firefox, and Safari looks the same given the same font. Edge cases persist at the margins (obscure Vedic signs, experimental `locl` tags) but production Hindi/Marathi/Nepali UI text is consistent.

Microsoft deprecated the legacy `deva` OpenType script tag in 2005 in favor of `dev2`. All production fonts and shapers target `dev2`. You shouldn't need to think about this unless you're auditing a very old font file.

### `letter-spacing: 0` — always, unconditionally

```css
.devanagari {
  letter-spacing: 0;  /* CRITICAL */
}
```

Applying non-zero `letter-spacing` to Devanagari text breaks conjunct rendering in every major browser engine. Space is inserted **between the glyphs that compose a conjunct** (half-consonant + base-consonant, reph + base, rakar + base), visually fragmenting words into disconnected pieces. This has been a longstanding and well-documented issue (see Mozilla bug 202351, W3C *Devanagari Gap Analysis*). It is a **shaping-level constraint**, not a bug per se — CSS `letter-spacing` is defined as inter-character, and Devanagari needs inter-cluster.

If you're setting a Latin-primary stylesheet that uses `letter-spacing`, **scope it away from Devanagari**:

```css
body { letter-spacing: 0.02em; }
:lang(hi), :lang(mr), :lang(ne), :lang(sa) { letter-spacing: 0; }
```

### `word-spacing` is fine (mostly)

`word-spacing` operates on the space character between words and works as expected in Devanagari (space between words, not between glyphs). Use it for readability tuning of body prose if needed.

### `text-align: justify` — with caution

Justification in Devanagari is handled via **inter-word-space expansion** (the normal CSS default), which works but is not how traditional print Devanagari justifies. Print Devanagari uses **shirorekha elongation** — stretching the head line to fill line width — which no browser implements. Practical consequence: justified Devanagari on the web has loose, rivers-prone spacing. Most designers **avoid justification for Devanagari body** and use `text-align: left` (which is `start` in LTR context).

### Font file size

Devanagari fonts are large compared to Latin-only fonts because of the conjunct inventory:

- **Noto Sans Devanagari static cut:** 350–500 KB per weight.
- **Noto Sans Devanagari variable:** ~1.2–1.8 MB.
- **Scholarly fonts (Chandas, Adobe Devanagari):** 1–3 MB for full Sanskrit coverage.

**Subset if you can.** `unicode-range` CSS descriptor lets you load only the Devanagari block for multilingual sites, and further subsetting by language (Hindi-only omits Marathi's ळ, saving a conjunct family) can trim more. Google Fonts automatically subsets by language when you request `&subset=devanagari`.

```css
@font-face {
  font-family: 'Noto Sans Devanagari';
  src: url('noto-sans-devanagari.woff2') format('woff2');
  unicode-range: U+0900-097F, U+A8E0-A8FF, U+1CD0-1CFF;
  font-display: swap;
}
```

### `lang` attributes fire `locl`

Set `lang="hi"`, `lang="mr"`, `lang="ne"`, or `lang="sa"` on the element (or the document root if the whole page is in one language) so the OpenType `locl` feature fires correctly. Without `lang`, the shaper falls back to a default (usually Hindi) — usually fine but gives wrong eyelash-reph behavior in Marathi or Nepali content.

### Fallback stacks

Plan for missing fonts. A reasonable Hindi stack:

```css
font-family:
  'Noto Sans Devanagari',
  'Mukta',
  'Kohinoor Devanagari',  /* macOS/iOS */
  'Nirmala UI',            /* Windows */
  'Mangal',                /* older Windows fallback */
  sans-serif;
```

Since CSS `font-family` fallback is per-character (not per-run), mixed Devanagari + Latin text will fall back cleanly as long as the Latin face and the Devanagari face both appear in the stack in the right order.

### `font-feature-settings` hazards

Avoid `font-feature-settings` for Devanagari text unless you are deliberately targeting a specific OpenType feature. Overriding feature state inadvertently disables features the shaper needs:

- `font-feature-settings: 'liga' 0;` — disables standard ligatures, may cascade to conjunct features.
- `font-feature-settings: 'calt' 0;` — disables contextual alternates; breaks matra-width selection.
- `font-feature-settings: 'kern' 0;` — safe, affects only kerning.

Prefer `font-variant-*` longhand properties which scope changes to Latin-appropriate semantics.

### `text-transform: uppercase` is a no-op

Devanagari has no case distinction — `text-transform: uppercase` (and `capitalize`, `lowercase`) has no visual effect. Safe to leave as a no-op in inherited styles, but don't rely on case as a visual-hierarchy device in Devanagari UI.

### `text-decoration: underline` hazards

Underlines in Devanagari sit below the below-marks (u-matra, ū-matra, ṛ-matra), which means they can appear *far* below the body of the letter — further than they do in Latin. Some readers find this jarring. `text-underline-position: under;` and `text-underline-offset` help tune, but many Devanagari designers use color/weight instead of underlines for emphasis.

---

## Writing in Code

### Unicode blocks

| Block | Range | Contents |
|-------|-------|----------|
| **Devanagari** | U+0900 – U+097F | Core: 13 vowels, 33 consonants, halant, matras, anusvara, chandrabindu, visarga, Devanagari digits 0–9, danda, double danda, plus some additional consonants and signs. 128 codepoints. |
| **Devanagari Extended** | U+A8E0 – U+A8FF | Supplementary signs, accent marks, and less common characters. 32 codepoints. |
| **Vedic Extensions** | U+1CD0 – U+1CFF | Tone marks, nasalization signs, and other characters used for Vedic Sanskrit. Needed only for Vedic scholarly text. 48 codepoints. |

All of Devanagari fits in the Basic Multilingual Plane (BMP), so you don't need to worry about surrogate pairs or UTF-16 supplementary handling. UTF-8 encoding of a Devanagari character is 3 bytes.

### Logical order vs visual order

Store and transmit Devanagari in **logical order** — the order in which characters are typed and spoken. Never try to serialize visual order yourself. Examples:

- Hindi `कि` ("ki") is stored as `\u0915\u093F` (consonant क, then vowel sign i-matra), even though the i-matra renders to the *left* of the consonant.
- Hindi `क्ष` ("kṣa") is stored as `\u0915\u094D\u0937` (ka, halant, sha), even though the rendered glyph is a single ligature.
- Hindi शर्मा ("Śarmā") is stored as `\u0936\u0930\u094D\u092E\u093E` (sha, ra, halant, ma, ā-matra). The r + halant forms the reph mark, which is *visually positioned* above the following `m`, but `r` still appears before `m` in the string.

### Grapheme-cluster iteration

The Unicode concept of **grapheme cluster** approximates the user-perceived character. For Devanagari, one user-perceived character (one "akshara") can span many codepoints — a consonant cluster + halant + consonant + vowel sign + anusvara can be 5+ codepoints rendered as one glyph. **Iterate by grapheme cluster, not by codepoint**, when:

- Positioning a caret.
- Implementing backspace (should delete one cluster, not one codepoint).
- Computing visible character-count for a UI label.
- Truncating strings with ellipsis.

In JavaScript, use `Intl.Segmenter`:

```javascript
const segmenter = new Intl.Segmenter('hi', { granularity: 'grapheme' });
const clusters = [...segmenter.segment('क्षत्रिय')].map(s => s.segment);
// ['क्ष', 'त्रि', 'य']
```

In Python, use `grapheme` (PyPI) or `regex` with `\X`. In Swift, `String.count` on a `Character`-granularity view. In Rust, `unicode-segmentation`.

Note that Unicode's **extended grapheme cluster** algorithm doesn't perfectly represent Indic orthographic syllables — a single extended grapheme cluster in Devanagari typically covers one base + all its marks, but a conjunct spanning multiple bases with halants may segment into multiple clusters. For most UI purposes this is close enough; for stricter Indic syllable segmentation, use an Indic-syllable-aware segmenter (ICU's `BreakIterator` with locale hints, or a custom regex per the W3C Indic Layout Requirements).

### RTL / bidi

Devanagari is LTR. You do **not** need `dir="rtl"`, `direction: rtl`, logical-property fallbacks, or any of the RTL machinery. Bidi only enters when Latin text, Arabic text, or Hebrew text is mixed into Devanagari content — and then the Unicode Bidirectional Algorithm handles it the same way it would for any mixed-script content.

### Input methods

Hindi keyboards on Windows/macOS/Linux commonly produce **logical-order** output (consonant then matra), either via InScript (the default Indian government standard) or Remington-layout keyboards. Transliteration IMEs (Google Input Tools, Quillpad) accept Romanized Hindi and emit Devanagari in logical order. You don't need to know this to render text, but if you're building a text input, assume logical-order input.

---

## Accessibility

### Screen-reader support

- **VoiceOver (macOS/iOS):** Good Hindi TTS quality. Handles common conjuncts. Marathi and Nepali support is weaker — TTS may read Marathi or Nepali in a Hindi voice.
- **NVDA (Windows) + eSpeak NG:** Usable for Hindi. Pronunciation is mechanical but comprehensible. Conjunct handling varies.
- **JAWS:** Hindi support is available and used in professional Indian accessibility contexts. Premium tier.
- **TalkBack (Android):** Google's Hindi TTS is production-grade and widely used.
- **ChromeVox and built-in Chrome reading:** leverages Google's TTS, good Hindi quality.

**Practical implications:**

- Setting `lang="hi"` on elements helps screen readers switch to the correct TTS voice automatically. Without `lang`, SRs may try to read Hindi with a Latin voice, producing garbage.
- Set `lang` on mixed-language spans too: `<span lang="en">English phrase</span>` inside otherwise-Hindi body text lets SRs switch voices mid-sentence.
- `aria-label` and `alt` attributes written in Devanagari work — just use logical-order Unicode.
- Test with a real screen reader in the target language; Hindi SR pronunciation quirks are not always obvious from silent reading.

### Reading-age and pedagogical typography

For children's content and early-reader materials:

- **Expanded inter-cluster spacing** is sometimes used to make individual aksharas visually separable — e.g., for first-year Hindi readers. Do **not** achieve this with CSS `letter-spacing` (breaks shaping). Instead, use a font specifically designed for young readers (Ek Mukta's beginner variants, Pooja Saxena's early-reading types) or insert ZWNJ (zero-width non-joiner U+200C) between clusters to manually prevent conjunct formation — a typographically correct technique for pedagogical material but inappropriate for prose.
- **Larger body size.** 20–24px body text for children's material, vs 16–18px for adult body.
- **Generous leading.** 1.8–2.0 for children's materials.

### Dyslexia-related considerations

There is less research-survey on Devanagari-specific dyslexia typography than on Latin (OpenDyslexic, Lexend, etc.). Current practice transfers Latin dyslexia guidance: generous leading, slightly wider letter spacing *within Latin runs* (not Devanagari), high contrast, and well-proportioned x-height fonts like Mukta. Avoid ornate display faces for dyslexic readers.

### Contrast

Standard WCAG contrast rules apply. Devanagari reads well at the same contrast thresholds as Latin. Note that thin matras (anusvara dot, chandrabindu) can appear to "disappear" at low contrast faster than body strokes because of their small visual footprint — inspect at target contrast before shipping.

---

## Anti-patterns

Things first-time Devanagari implementers frequently get wrong:

1. **Applying `letter-spacing` to mixed-language body text.** Breaks conjuncts. Always scope to Latin: `:lang(en) { letter-spacing: 0.02em; }`.
2. **Using `text-align: justify` for Devanagari body.** Produces rivers and loose spacing because browsers implement word-space justification, not shirorekha elongation. Prefer left-aligned body.
3. **Setting `line-height: 1.4` (Latin default) for Devanagari body.** Stacked above- and below-marks collide. Use 1.6–1.85.
4. **Measuring with `max-width: 65ch`.** `ch` unit is the width of the `0` glyph and doesn't meaningfully map to Devanagari cluster widths. Use `rem`-based measures tuned by eye.
5. **Counting characters via `str.length`.** Logical-order codepoint count has no relationship to user-perceived characters. Use `Intl.Segmenter` with grapheme granularity.
6. **Truncating strings mid-cluster.** A truncation that splits a consonant from its matra or a conjunct from its halant produces ghost glyphs like isolated matras or visible halants.
7. **Disabling `liga` / `calt` via `font-feature-settings`.** These features are the shaper's vehicle for conjunct substitution. Disabling them breaks text. Use `font-variant-*` properties instead.
8. **Shipping without `lang` attributes.** Missing `lang` leaves `locl` unfired, which means Marathi and Nepali text gets rendered with Hindi forms (wrong eyelash-reph behavior, missing ळ-typography tuning).
9. **Using Latin `|` instead of Devanagari danda `।` (U+0964).** Different codepoint, different metrics, different line-break behavior. Always use the real danda.
10. **Treating Mangal as a design choice.** Mangal is a Windows system fallback. It renders Devanagari correctly but is visually dated. Use Mangal only as a last-resort fallback in font stacks, not as the intended design.
11. **Large bold weights for Hindi body.** Google Fonts documentation and native-speaker feedback note that heavy bold reads oppressively in Devanagari body. Prefer Regular + Semibold for emphasis, or use italics-equivalent stylistic variants if the font provides them.
12. **Assuming bold = emphasis.** Devanagari has less typographic tradition of bold-for-emphasis than Latin. Designers often use a contrasting serif/sans or color instead. Weight is still a valid tool; just don't assume it's the only one.
13. **Treating Hindi, Marathi, and Nepali as interchangeable for QA.** They share a script but have different letter inventories, different reph behavior, and different punctuation conventions. Smoke-test each target language separately.
14. **Forgetting that half-forms need the full-form consonant to "complete" them.** A half-form at end-of-line without its subsequent consonant (from an edge case like a soft line break inside a cluster) renders as an incomplete glyph. Normal line-break algorithms prevent this by treating clusters as unbreakable units — but a manual `<wbr>` or `&shy;` in the wrong place can break that.

---

## Sources

**W3C / Unicode primary sources:**

- [W3C Indic Layout Requirements (ILReq)](https://w3c.github.io/ilreq/) — editor's draft, the authoritative layout reference for Indic scripts on the web.
- [W3C Devanagari Layout Requirements](https://www.w3.org/International/ilreq/devanagari/) — published snapshot focused on Devanagari.
- [W3C Devanagari Gap Analysis](https://www.w3.org/TR/deva-gap/) — catalogs where browsers fall short of ILReq's recommendations.
- [Unicode Standard 16.0, Chapter 12](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-12/) — South and Central Asia I: Official Scripts of India. Codepoint-level authoritative source.
- [Unicode FAQ: Indic Scripts and Languages](http://www.unicode.org/faq/indic) — answers common encoding questions.

**Shaping / OpenType:**

- [Microsoft Typography: Developing OpenType Fonts for Devanagari Script](https://learn.microsoft.com/en-us/typography/script-development/devanagari) — the Microsoft implementer's guide. Authoritative for `dev2` shaping behavior.
- [Nathan Willis, *OpenType Shaping Documents: Devanagari*](https://github.com/n8willis/opentype-shaping-documents/blob/master/opentype-shaping-devanagari.md) — detailed, implementer-facing write-up of the shaping pipeline.
- [HarfBuzz OpenType Shaping Models](https://harfbuzz.github.io/opentype-shaping-models.html) — what the dominant browser shaper actually does.

**Type-design resources:**

- [Pooja Saxena, *Devanagari Type Anatomy* (TypeTogether)](https://www.type-together.com/devanagari-type-anatomy) — accessible type-anatomy vocabulary for Devanagari.
- [Typotheque, *Regional Forms of Devanagari Survey Report*](https://www.typotheque.com/research-survey/regional-forms-of-devanagari-survey-report) — how Hindi, Marathi, and Nepali typographic conventions differ.
- [Indian Type Foundry (ITF)](https://www.indiantypefoundry.com/) — foundry site with specimens, including Kohinoor Devanagari and ITF Devanagari.
- [D'Source: Terminology of Devanagari Typefaces](https://dsource.in/tool/devft/en/terminology.php) — terminology reference from India's national design education network.

**Font resources:**

- [Google Fonts: Noto Sans Devanagari](https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari)
- [Google Fonts: Noto Serif Devanagari](https://fonts.google.com/noto/specimen/Noto+Serif+Devanagari)
- [Noto fonts GitHub repo](https://github.com/notofonts/devanagari)

**Further reading (not primary sources but useful):**

- Rathna Ramanathan writings on Indic type design.
- Mohammad Ali, Indic type researcher.
- *Typographic Emphasis in Devanagari* (Universal Thirst Gazette) — on how to mark emphasis when case doesn't exist.
- *Devanagari conjuncts* on Wikipedia — surprisingly thorough practical reference for conjunct shapes.
