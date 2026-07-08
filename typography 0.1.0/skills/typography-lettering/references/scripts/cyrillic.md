---
date: 2026-04-18
coverage: medium
peers:
  - ./latin.md
  - ./greek.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
  - ../techniques/pairing.md
primary_sources:
  - https://www.unicode.org/charts/PDF/U0400.pdf
  - https://www.unicode.org/charts/PDF/U0500.pdf
  - https://www.unicode.org/charts/PDF/U2DE0.pdf
  - https://www.unicode.org/charts/PDF/UA640.pdf
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-locl
  - https://type.today/en/journal/bulgarian
  - https://type.today/en/journal/quotes
  - https://www.myfonts.com/a/font/content/cyrillic-script-variations-and-the-importance-of-localisation
  - https://typejournal.ru/en/articles/Civil-Type
  - https://en.wikipedia.org/wiki/Cyrillic_script
  - https://en.wikipedia.org/wiki/Bulgarian_alphabet
  - https://en.wikipedia.org/wiki/Serbian_Cyrillic_alphabet
  - https://en.wikipedia.org/wiki/Civil_Script
  - https://en.wikipedia.org/wiki/PT_Fonts
  - https://localfonts.eu/typography-basics/fonts-the-importance-of-localisation/local-features/serbian-cyrillic-feature-locl/
  - https://localfonts.eu/typography-basics/fonts-the-importance-of-localisation/local-features/macedonian-cyrillic-feature-locl/
  - https://pimpmytype.com/russian-typography/
  - Maxim Zhukov — writings on Cyrillic typography and the Russian civil type
  - Gerry Leonidas — Reading writings on Cyrillic and Greek type design
  - Krista Radoeva — writings on Bulgarian Cyrillic (Fontsmith / TypeTogether)
  - Andrey V. Panov — research-survey on Serbian Cyrillic italic forms
---

# Cyrillic script — typographic reference

**Scope disclaimer — practitioner-medium.** This is enough to set Russian, Ukrainian, Bulgarian, Serbian, Macedonian, and Belarusian body and display type correctly, pair Cyrillic with Latin without embarrassment, and specify `locl` so the right letterforms render for the right language. It does not cover Old Church Slavonic typesetting, Cyrillic in non-Slavic languages of the former USSR in full, or the history of metal Cyrillic punchcutting. For scholar-depth, go to Maxim Zhukov's essays on the civil type and on Cyrillic design, Yuri Gordon's *Книга про буквы от Аа до Яя*, Vladimir Yefimov's writings on the 20th-century Russian type tradition, and the ParaType archive.

**Why Cyrillic is the most-often-misread non-Latin script in Western UI work.** It *looks* like Latin. Many letters are visually identical (А, В, Е, К, М, Н, О, Р, С, Т, Х — Cyrillic characters that share shapes with Latin capitals, though with different phonetic values). This visual overlap tempts designers to treat "Cyrillic support" as "glyph coverage in the right Unicode block" and ship — but the result is almost always *Russian-default* Cyrillic rendered for Bulgarian, Serbian, or Macedonian readers, which they experience as wrong in the same way a French reader experiences English `"..."` quotes instead of `« »`. The headline problem in Cyrillic typography is not coverage; it's `locl` — specifically the Bulgarian lowercase and the Serbian/Macedonian italic forms.

**What this file covers.** Historical origin and Peter the Great's 1708 reform. Letter inventories (Russian core, Ukrainian, Belarusian, Bulgarian, Serbian, Macedonian, non-Slavic extensions). The `locl`-mandatory section: Bulgarian lowercase variants, Serbian/Macedonian italic variants, what happens when a font lacks them. Italic traditions (why Cyrillic italic diverges from roman more than Latin italic does). Weight and spacing norms. Numerals, quotation marks, dashes, and punctuation. Notable fonts with strong Cyrillic coverage. Anti-patterns. Modern state (2024–2026) including the Ukrainian post-2022 type scene.

---

## Historical Origin

### Glagolitic → Cyrillic (9th–10th century)

Two scripts sit behind modern Cyrillic.

- **Glagolitic** — the older of the two. Traditionally attributed to Saints Cyril and Methodius around 863 CE for the Slavic liturgical translations of the Byzantine mission to Great Moravia. Its letterforms were original constructions, unrelated to Greek or Latin shape-space. Still used liturgically in parts of Croatia into the modern era; essentially dead as a secular script by the Middle Ages.
- **Cyrillic** — developed in the First Bulgarian Empire in the late 9th / early 10th century, attributed to students of Cyril and Methodius (Clement of Ohrid traditionally). Built by grafting **Greek uncial** letterforms onto a phonetic inventory covering Slavic sounds, with new letters invented for Slavic phonemes Greek didn't have (Б, Ж, Ц, Ч, Ш, Щ, Ъ, Ь, Ю, Я and their forerunners). Named *after* Cyril but designed by his successors — Cyril himself almost certainly designed Glagolitic.

Medieval Cyrillic — **ustav** (formal upright uncial) and later **poluustav** (semi-uncial, 14th–17th c.) — was the Slavic ecclesiastical standard. Letterforms were calligraphic, heavily decorated, with superscript abbreviation marks (*titla*) and a narrow/tall proportion. A reader today would find it legible but unmistakably medieval — closer to blackletter-era Latin than to anything we'd call modern type.

### Peter the Great's civil type reform (1708)

The single most consequential event in Cyrillic typography.

**Motivation.** Peter I returned from the Grand Embassy (1697–98) determined to Westernize Russian print. The existing Cyrillic (*poluustav*) looked archaic next to contemporary Dutch Baroque roman — visually foreign to Western readers and, Peter concluded, to the project of modernizing Russia.

**The reform.** Between 1708 and 1710, Peter commissioned *гражданский шрифт* (*grazhdanskiy shrift*, "civil type"), designed to resemble Dutch Baroque roman of the late 17th century. Peter personally sketched proposed letterforms and struck out proposed glyphs he rejected. First book: *Geometry of Slavic Land Survey*, March 1708.

**What changed structurally:**

- **Latinized shapes.** Characters shared with Greek/Latin (А, В, Е, К, М, Н, О, Р, С, Т, У, Х) were redrawn to Baroque-roman proportions — same x-height-to-cap-height relationship as Latin, same stress axis, same serif detailing.
- **Bicameral case introduced** — the poluustav had limited case differentiation; Peter's reform formalized upper/lower case.
- **Archaic letters abolished** — Ѯ (ksi), Ѱ (psi), Ѡ (omega), S (dzelo) among others.
- **New letters added** — Я (replacing Ѧ "little yus"), Э; И and Й adjusted to modern forms.
- **Accent marks removed** from secular text.
- Letter count dropped to ~38; the 1917–18 reform trimmed further to the modern 33.

**Consequence.** Modern Cyrillic is *structurally a Baroque roman with Slavic phonemes*. This is why Cyrillic and Latin sit together acceptably in the same typeface — Peter engineered the visual compatibility. It is *also* why Bulgarian, Serbian, and Macedonian conventions diverge: those traditions never accepted the full Petrine Latinization for lowercase forms, preserving handwriting-derived shapes Russian abandoned. See `locl` below.

**Church Slavonic typography** (descendant of poluustav) persists for Russian Orthodox liturgical texts — so religious Russian content may include pre-reform letter shapes (Ѣ yat', Ѵ izhitsa, Ѳ fita, І decimal-i) set in Church Slavonic types like Irmologion or Orthodox Slavonic.

---

## Letter Inventories

### Russian (33 letters)

The modern Russian alphabet as standardized by the 1917–18 orthographic reform:

```
А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я
```

**Gotchas:**

- **Ё (U+0401, ё U+0451)** is officially a separate letter from Е/е, but in running Russian prose it is *almost always written as plain Е* — the dots are treated as optional disambiguation, rendered only in pedagogy, children's books, and disambiguating context (e.g. `всё` vs `все`). A font that doesn't cover Ё is broken for Russian even though Ё appears rarely.
- **Ъ (hard sign)** and **Ь (soft sign)** are not vowels or consonants but modifying signs. They carry no independent phonetic weight but are case-sensitive letters.
- **Й (short-i, with breve)** is a distinct letter, not И with a floating diacritic. Sort-adjacent but independent.

### Ukrainian extensions

Ukrainian adds four letters and omits three Russian ones. Critical for any product targeting Ukrainian users — rendering Russian-default Cyrillic for Ukrainian content is a category error.

| Added | Code point | Notes |
|-------|------------|-------|
| **І і** | U+0406, U+0456 | Dotted I. In Ukrainian, *the* letter for the /i/ sound. Visually identical to Latin I/i — requires correct Unicode code point, not a Latin substitution. |
| **Ї ї** | U+0407, U+0457 | I-with-diaeresis, /ji/ sound. |
| **Є є** | U+0404, U+0454 | Reversed E, /jɛ/ sound. |
| **Ґ ґ** | U+0490, U+0491 | G-with-upturn, the non-palatalized /g/ (native Cyrillic Г in Ukrainian represents /ɦ/). |

Ukrainian *does not use* Russian Ё, Ъ, or Ы. A font shipping "Cyrillic" that covers only the 33 Russian letters is missing Ukrainian, Belarusian, and South Slavic coverage. Verify presence of **І, Ї, Є, Ґ** before claiming Ukrainian support.

### Belarusian extensions

Belarusian adds **Ў ў** (U+040E, U+045E, *short u* / non-syllabic u — a U with a breve, analogous to Й). It also uses **І і** (not Russian И). Belarusian does not use Щ. Three letters = three required glyphs for a Belarusian-capable font: Ў, І, Ї-adjacent handling.

### Bulgarian inventory

Bulgarian uses 30 letters (the Russian 33 minus Ё, Ы, Э). Critically, **Bulgarian's lowercase forms are typographically distinct from Russian's** — same Unicode code points, different preferred glyph shapes. See the `locl` section below; this is where Cyrillic typography becomes non-trivial.

### Serbian and Macedonian (South Slavic)

Serbian Cyrillic uses 30 letters including six not in Russian — **Ђ ђ** (U+0402, U+0452), **Ј ј** (U+0408, U+0458), **Љ љ** (U+0409, U+0459), **Њ њ** (U+040A, U+045A), **Ћ ћ** (U+040B, U+045B), **Џ џ** (U+040F, U+045F). Drops Russian Ё, Й, Щ, Ъ, Ы, Ь, Э, Ю, Я.

Macedonian is similar: shares Ј, Љ, Њ, Џ with Serbian; adds **Ѓ ѓ** (U+0403, U+0453) and **Ќ ќ** (U+040C, U+045C) for Macedonian-specific palatal consonants; adds **Ѕ ѕ** (U+0405, U+0455) for /dz/.

Both Serbian and Macedonian have **italic forms that differ substantially from Russian italic** for several lowercase letters (б, г, д, п, т). Critical `locl` territory — see below.

### Non-Slavic Cyrillic

Cyrillic is the written script of ~50 non-Slavic languages across the former Soviet territory and beyond: Kazakh (with Ә, Ғ, Қ, Ң, Ө, Ұ, Ү, Һ, І — transition to Latin delayed multiple times, mixed use as of 2026), Mongolian (with Ө, Ү), Kyrgyz, Tajik, Tatar, Bashkir, Chuvash, Yakut, Buryat, Abkhaz, Ossetian, Chechen, and others. Each adds letters beyond the Russian 33.

Unicode covers these via **Cyrillic Supplement** (U+0500–U+052F), **Cyrillic Extended-A** (U+2DE0–U+2DFF, combining marks for historical Cyrillic), **Cyrillic Extended-B** (U+A640–U+A69F, obsolete and rare), and **Cyrillic Extended-C** (U+1C80–U+1C8F). Broad Cyrillic coverage for "languages of Russia" must include Supplement plus selected Extended-B glyphs — ParaType's PT Sans/PT Serif are the canonical open-license reference (designed to cover all 54 titular languages of the Russian Federation).

---

## `locl` — the Bulgarian and Serbian/Macedonian Variants

This is the headline section. Read it before anything else if you're shipping multilingual Cyrillic.

**The premise.** Unicode encodes Cyrillic *characters* by phonetic identity, not by regional letterform tradition. The same code point U+0434 Cyrillic Small Letter De represents Russian `д`, Bulgarian `д`, and Serbian `д` — but those three glyphs are drawn differently in their respective national typographic traditions. The OpenType `locl` (localized forms) feature is the mechanism by which a font provides regional variants for the same code point and the shaping engine selects between them based on the declared language.

If the font lacks `locl` for the reader's language, the reader sees the default form — almost always the **Russian form** — and immediately perceives the text as foreign-set.

### Bulgarian lowercase variants

Bulgarian typographic tradition (rooted in 19th-century Bulgarian letterpress, preserved through the 20th century despite Russian typographic dominance during the Soviet era) prefers **handwriting-derived lowercase forms** for a cluster of letters. The Russian default descended from Peter's Latinizing reform; the Bulgarian tradition descended from the pre-reform calligraphic models. Both are legitimate; both are in use.

The letters whose Bulgarian forms differ noticeably from Russian:

| Letter | Russian default | Bulgarian form |
|--------|-----------------|----------------|
| **в** | Doubled-bowl — looks like reduced Latin `B` | Looks closer to Latin `b` — single-story with an ascender to the cap-line |
| **г** | Shallow hook / truncated Greek gamma | Taller, straight-stemmed, approaching inverted Latin `r` or short-descender form |
| **д** | Boxy with horizontal feet — like reduced capital Д | Looks like Latin `g` (descender loop) — handwriting-derived |
| **ж, з, и, й, к, л, п, ц, ш, щ, ъ** | Cap-derived or Latinized shapes | Handwriting-derived, more humanist / less uniform |
| **т** | Cap-derived — like reduced Т | Looks like **Latin `m`** — completely different construction |

**Krista Radoeva's summary** (Fontsmith / TypeTogether, widely cited): the three characters most misread are **в, г, д** — treat Latin `b` as the visual reference, and keep the construction logic consistent across all three.

**The visual result.** A Russian-set page of Bulgarian prose looks to a Bulgarian reader like a Bulgarian-set page of Russian prose would look to a Russian reader — recognizable but visibly foreign, with a specific *wrong-tradition* feel. Not unreadable. Wrong.

### Serbian and Macedonian italic variants

The `locl` problem with the most dramatic visual consequences, because the divergence is concentrated in italic forms where Russian italic collides with Latin letters in ways Serbian readers cannot parse.

| Italic letter | Russian form | Serbian/Macedonian form |
|---------------|--------------|-------------------------|
| **т** | Three-stemmed top-bar italic | **Looks like Latin italic `m`** — three stems with overline |
| **п** | Italicized Π | Single-stem hook with overline — looks like Latin italic `n` with a bar above |
| **г** | Italicized Cyrillic hook | Looks like Latin italic `g` (mirrored, with descender) |
| **д** | Italicized boxy д | Has a descender and loops — cursive-g-like with different stem |
| **б** | Italicized б | Slightly different; least critical |

The Serbian italic forms descended from a connected-script cursive where overlines distinguished adjacent three-stem letters (и, ш, м, т, п). **Andrey Panov's research-survey** argues these are not merely stylistic — they are legibility-critical; Serbian readers parse them as structural, not decorative.

Where this goes wrong: a Western foundry ships a Cyrillic font with one italic per letter — the Russian default. A Serbian reader opens the page, sees Russian italic т where Serbian italic т is expected, and perceives the text as translated-from-Russian or carelessly set.

### How `locl` resolves

OpenType's `locl` feature is the delivery mechanism. The shaping engine reads the declared language and substitutes the localized glyph for the default:

```html
<html lang="ru">             <!-- Russian forms -->
<html lang="bg">             <!-- Bulgarian forms -->
<html lang="sr">             <!-- Serbian forms -->
<html lang="sr-Cyrl">        <!-- Explicit: Serbian in Cyrillic script -->
<html lang="mk">             <!-- Macedonian forms -->
<html lang="uk">             <!-- Ukrainian — usually Russian-default forms, but some families offer Ukrainian-specific tuning -->
<html lang="be">             <!-- Belarusian — ditto -->
```

```css
.body {
  font-feature-settings: "locl" 1;   /* usually default-on, but state it for clarity */
}
```

In CSS, `locl` is **enabled by default** in all modern browsers/shapers (per spec), but stating it costs nothing and avoids accidental disabling via cascade. The `lang` attribute on an ancestor (or the element itself) is the *trigger* — the shaper reads `lang` from the document tree and chooses the `locl` variant accordingly. JavaScript-set locale or Accept-Language headers do not trigger `locl`; only the declared `lang` attribute does.

**When the font has no Bulgarian or Serbian `locl`:** default Russian forms render. No error is raised. The text is rendered "successfully" — with wrong letterforms. Detectable only by visual inspection by a native reader, by auditing the font's GSUB table, or by the designer having heard of the problem.

### Fonts with `locl` support

Not exhaustive — these are well-known examples that ship real variants (not just glyph coverage):

- **Bulgarian `locl BGR`**: Fira Sans (canonical case study), Source Sans 3, PT Sans/Serif, Noto Sans/Serif, Adelle / Adelle Sans (TypeTogether), FF Meta, Roboto (recent), Inter (v3+), all Fontfabric families.
- **Serbian/Macedonian italic `locl SRB` / `locl MKD`**: Fira Sans, Source Sans 3, Noto Sans/Serif (post-2019), PT Sans/Serif (recent), Adelle, Fedra, and Serbian-native foundries (Typonine, Tipometar, Tipoteka).

### The three-way trap

A single font may not contain all three `locl` sets (Russian default + Bulgarian + Serbian/Macedonian). A font that ships Bulgarian `locl` but not Serbian italic `locl` will render Serbian italic text with Russian italic forms — the "italic т looks like Latin m" problem disappears for the Serbian reader (because they get Russian т instead of Serbian т) and is replaced by the older "Cyrillic letters don't look Serbian" problem.

**Practitioner rule.** For a pan-Cyrillic product (Russian + Bulgarian + Serbian + Macedonian + Ukrainian + Belarusian audiences), pick a font whose specimen *explicitly* documents `locl BGR`, `locl SRB`, and `locl MKD` support, and audit the font file to confirm (Wakamai Fondue, FontDrop, or equivalent will show the GSUB lookups). Noto Sans/Serif, Fira Sans, Source Sans 3, Adelle, and PT Sans/Serif are the safest broad picks.

---

## Italic Tradition

Cyrillic italic diverges from Cyrillic roman *more than Latin italic diverges from Latin roman*. This is the second-most-surprising fact (after `locl`) for designers approaching Cyrillic from a Latin background.

**Why the divergence is larger.** Latin italic descends from the Aldine chancery cursive (1501), grafted onto Latin roman typography and tamed toward visual consistency with its accompanying roman. Cyrillic italic descended from Russian *handwriting cursive* — скоропись (*skoropis'*) — a distinct script tradition that preserved older Slavic cursive forms even as the roman (civil type) Latinized. When Peter's reform produced an upright Cyrillic modeled on Dutch Baroque roman, the italic was drawn from Russian handwriting, not from the roman's construction. Result: Cyrillic italic letters often look radically different from their roman counterparts.

| Letter | Upright | Italic |
|--------|---------|--------|
| **т** | Т-shaped — like reduced Latin T | Three-legged — **looks like Latin italic `m`** |
| **п** | Π-shaped | Looks like Latin italic `n` |
| **г** | L-reversed / short hook | Humanist hook form |
| **д** | Boxy with horizontal feet | Has a descender (or not, per regional variant) |

### The Russian italic т trap

The most reliably confusing glyph in Cyrillic typography for a Western reader is **italic Russian т, which in many fonts looks identical to Latin italic `m`**. Both are three-stemmed and occupy the same visual slot. Italicized mixed Russian-Latin text contains "m"-looking glyphs that are actually `т`; the reader cannot tell scripts apart at a glance.

Mitigations:
- **`locl SRB`** fixes Serbian by adding the overline — trivially distinguishes Serbian italic т from Latin italic m.
- **For Russian**, there is no mitigation — the form is correct. Designers who find it confusing are, in Russian typographic tradition, the ones who need to adapt.
- **Font choice** affects conspicuousness. A sans where italic is oblique (merely slanted, not true italic) has a Russian italic т that looks more like slanted upright т (clearly Cyrillic). A true italic — handwriting-derived — has maximum collision with Latin italic m.

### True italic vs oblique

The Latin distinction (true italic as separate drawn cursive vs oblique as mechanical slant) applies to Cyrillic with twists:

- **True italic** is *required* to look visually different from upright — the handwriting-derived forms (т, п, г, д) are what Russian readers expect. A Cyrillic font whose italic is just a slanted upright looks "not italic" to a Russian reader.
- **Oblique** (mechanical slant) is acceptable in geometric sans families where Latin italic is also oblique (Futura). But the shaped italic glyphs for т, п, г, д should still be substituted.
- **Variable fonts with `ital` axis** must switch the shaped glyphs, not merely slant. Inter, Source Sans 3, and Noto Sans do; some 2010s webfonts with "italic" axes do not.

See `./latin.md` for the `ital` vs `slnt` OpenType distinction. Rules apply, but stakes are higher in Cyrillic because upright–italic divergence is larger.

---

## Weight and Spacing Norms

### The "Cyrillic looks darker than Latin" phenomenon

At the same declared weight, the same font typically renders Cyrillic text visually heavier than Latin. Compounding reasons:

1. **More vertical stems per letter.** Cyrillic averages more vertical strokes per glyph. "Hello world" has ~11 stems; "Привет мир" has ~14. More ink per x-height.
2. **Fewer open-counter letters.** Latin has many large-counter letters (o, c, e, s, a). Cyrillic has proportionally more closed multi-stem letters (ш, щ, м, н, и, п, т) with less internal whitespace.
3. **Fewer ascenders/descenders.** Cyrillic lowercase is almost entirely x-height-bound — only б has an ascender; only р, у, ф descend. Latin has many of both. Cyrillic produces a more uniform "stripe of ink" texture.

**Practitioner consequences:** at body size, Cyrillic often reads one weight step heavier than Latin at the same `font-weight`. Some designers compensate by setting Cyrillic lighter (Latin 400, Cyrillic 350 via variable axis) — controversial; some Russian typographers reject this as "making Cyrillic look thinner than it should." At display size, Cyrillic headlines often benefit from a lighter weight than the Latin equivalent. Metric-override `size-adjust` can equalize paired families but applies uniformly when the same font supplies both scripts.

### Letter-spacing

Unlike Arabic or Devanagari, Cyrillic accepts `letter-spacing` adjustment the same way Latin does — the script is non-connecting, each glyph has independent advance width, and small positive tracking (especially on all-caps) reads correctly.

However:

- **All-caps Cyrillic** generally wants *more* letter-spacing than all-caps Latin, because the uppercase letters are visually denser. `letter-spacing: 0.06–0.10em` for Cyrillic all-caps is often correct where 0.04–0.06em works for Latin.
- **Italic Cyrillic** with `letter-spacing > 0` can break the cursive connection-adjacent feel (Cyrillic italic forms don't physically connect, but the reading eye expects rhythm). Keep italic tracking conservative.

### Measure

Cyrillic letters average somewhat wider than Latin at the same x-height (the doubled-bowl letters like в, the three-stemmed ш, щ, м, the wide ж). A comfortable Russian body measure is roughly **50–70 characters per line** — lower end of Latin's 45–75 range, because Cyrillic characters average wider.

Ukrainian and Bulgarian track similarly. Serbian and Macedonian, with their Љ, Њ (two-letter-wide glyphs) and Џ, may read slightly wider still.

### Line-height

Cyrillic needs only slightly more leading than Latin in practice. Because the script is largely x-height-only with few ascenders/descenders, the visual line-stripe is flatter and can tolerate somewhat tighter leading than a matched Latin. Common practice:

- **Body prose:** `line-height: 1.4–1.55` for Cyrillic body, comparable to Latin.
- **Vocalized educational or religious Church Slavonic text:** more generous, 1.6–1.8, to accommodate superscript marks and titla.

---

## Numerals

Cyrillic uses **European digits** (0–9) essentially universally in modern text. There is no separate Cyrillic digit system in active use (unlike Arabic-Indic, Devanagari, or CJK fullwidth).

Historically, Church Slavonic and pre-Petrine Cyrillic used **Cyrillic numerals** — a Greek-derived alphabetic numbering system where letters represented digit values (А = 1, В = 2, Г = 3, ... under a titla mark). Unicode encodes the system at U+2DE0+ (Cyrillic Extended-A) and U+A640+ (Cyrillic Extended-B) for its historical range. Used today essentially only in liturgical printing.

### Figure styles

The 2×2 from Latin applies to Cyrillic: lining vs old-style × proportional vs tabular. But:

- **Most Cyrillic-covering fonts ship only lining figures.** Old-style figures are rare in Cyrillic-design practice — the Russian design tradition inherited the lining convention and most type designers have not drawn old-style alternates. Source Serif 4, Charter, and a handful of editorial typefaces ship old-style; most Cyrillic sans do not.
- **Tabular figures are common** in UI-oriented fonts (Inter, Roboto, PT Sans, Source Sans 3) and essential for data display. `font-variant-numeric: tabular-nums` works for Cyrillic-set contexts because it affects only the digit glyphs, which are Latin-derived.
- **Old-style tabular** is vanishingly rare in Cyrillic. If you need it, the font choice collapses to a few editorial serifs.

Practical: if your Cyrillic editorial body text mixes digits mid-prose ("Родился в 1897 году"), lining figures will intrude visually the same way they do in English prose. If your font lacks old-style, either accept the lining or pick a different font.

### CSS

```css
.ru-prose { font-variant-numeric: oldstyle-nums; }    /* if font has them */
.ru-ui    { font-variant-numeric: lining-nums; }      /* default */
.ru-data  { font-variant-numeric: tabular-nums; }     /* tables, timers */
```

No Cyrillic-specific numeric handling is required. See `./latin.md` for the full numeral framework.

---

## Quotation Marks

Russian typographic convention uses **two distinct quote-mark systems** depending on primary vs nested context, and both coexist with the sloppy straight-quote habit that looks amateur.

### Primary quotes — French guillemets `« »`

The canonical Russian (and Ukrainian, Belarusian, Bulgarian) primary quotation convention is **French-style guillemets**, with the angle tips pointing outward:

```
«цитата» — correct
```

Code points: **U+00AB** (left-pointing) and **U+00BB** (right-pointing). No space inside — content butts directly against the mark (unlike French, which uses narrow non-breaking space).

```
Russian:  «Привет»
French:   «\u202FBonjour\u202F»      (with narrow non-breaking space)
```

The guillemets are the primary — they have been since the 19th century, standardized in Russian typographic practice, and remain the default in all serious Russian editorial work.

### Nested quotes — German-style low-high `„ "`

When a quote is nested inside another quote, Russian typography uses **German-style quotes** — low-bottom opening and high-top closing:

```
«Он сказал: „спасибо" и ушёл»
```

Code points: **U+201E** (double low-9 quote) as opening, **U+201C** (left double quote) as closing. Note: this is the *opposite* of the English curly-quote convention; in Russian, U+201C is the closing form, not opening.

Native Russian speakers and editors pay close attention to this. Using `" "` (English-style curly, high-open high-close) for either primary or nested Russian quotes is the unmistakable sign of an Anglo-centric content pipeline that didn't implement locale-aware quote substitution.

### Other regional conventions

- **Bulgarian** uses primarily **„ "** (German-style low-high) as primary, not guillemets. Different from Russian. Verify before assuming.
- **Serbian** uses primarily **„ "** as well, with nested `' '` or guillemets. Different again from Russian.
- **Ukrainian** follows Russian — guillemets primary, German-style nested.

### Straight quotes — the amateur signal

`"straight quotes"` `'straight apostrophes'` in Russian content are the Russian equivalent of unfixed typewriter quotes in English prose — immediately legible as a content-pipeline failure. Any mature Russian editorial system has SmartyPants-adjacent pre-processing that maps straight quotes to guillemets (primary) and German-style (nested).

### CSS / HTML

```html
<p lang="ru">Он написал: «тест», — а потом добавил: „важно".</p>
```

Content pipelines: Pandoc with `smart` extension + Russian locale, or `typogr.js` with Russian rules, or `remark-smartypants` with a Russian-configured plugin. Auto-substitution is language-aware; the `lang="ru"` attribute (on containing element) is usually enough for the pipeline to know which quote system to apply.

---

## Dashes

Russian typography uses the **em dash (—, U+2014) with spaces on both sides** as standard, distinct from English's em-dash-without-spaces convention.

### The Russian em dash

```
Москва — столица России.
(Moscow — is the capital of Russia.)
```

Note the spaces. In English:

```
Moscow—the capital of Russia—has 12 million people.    (no spaces, American)
Moscow – the capital – has 12 million people.          (en dash with spaces, British)
```

In Russian, it's always em-dash *with* spaces. Em dash without spaces in Russian prose looks wrong to a Russian reader.

### The dash-as-verb

A distinctive Russian convention: the em dash substitutes for the verb "to be" in the present tense, because Russian grammatically omits the copula in present tense. Where English has "Moscow is the capital," Russian has "Москва — столица" — the dash carries the copula.

This is *the* most common use of the em dash in Russian prose, and is why Russian-set text has far more em dashes per paragraph than English prose.

### Dialogue dash

Russian dialogue is traditionally set with **em dash opening each speaker's line**, not with quotation marks — common in fiction:

```
— Вы идёте?
— Да, конечно.
```

Modern Russian fiction mixes this with guillemet-quoted dialogue depending on editorial style.

### En dash, hyphen, horizontal bar

**En dash** for ranges (`1999–2012`); no spaces inside ranges. **Hyphen** for compound words (`северо-восточный`), same as Latin. **Horizontal bar** (U+2015) exists but most fonts don't distinguish it from em dash. Content pipelines should auto-convert `--` → en dash and `---` → em dash per language; `lang="ru"` signals em-dash-with-spaces convention to locale-aware processors.

---

## Other Punctuation

Cyrillic uses essentially the same punctuation as Latin — period, comma, colon, semicolon, question mark, exclamation mark, parentheses, brackets — with these notes:

- **Period / comma / colon / semicolon** — identical to Latin usage and identical glyphs.
- **Question mark** — standard `?` (U+003F), not mirrored (unlike Arabic).
- **Exclamation mark** — standard `!` (U+0021).
- **Parentheses** — standard `( )`. Some Russian editorial styles use square brackets for editorial interpolation the same way English does.
- **Ellipsis** — `…` (U+2026) standard. Russian convention: no space before, one space after, same as English. Three periods `...` is accepted but not preferred.
- **Slash** — `/` as in Latin. Some Soviet-era documents used `\` but this is not a typographic convention so much as a technical artifact.

Russian does not use Spanish-style inverted punctuation, French-style narrow spaces before double-character punctuation, or any other locale-specific punctuation-placement rules beyond the dash-and-quote conventions above.

---

## Notable Fonts with Strong Cyrillic Coverage

### Open-source / Google Fonts canon

- **PT Sans / PT Serif / PT Mono** (ParaType, 2009–2010, SIL OFL). Commissioned by Rospechat (Russian Ministry of Communications) for the 300th anniversary of the Petrine civil type reform; designed by Alexandra Korolkova, Olga Umpeleva, under Vladimir Yefimov. Covers **all 54 titular languages of the Russian Federation** — the broadest open-license Cyrillic coverage in existence. Default for broad-Cyrillic or minority-language work.
- **Noto Sans / Noto Serif** — Google / Monotype. Broad coverage with Bulgarian and Serbian italic `locl`. Safe default for multilingual global work.
- **Source Sans 3 / Source Serif 4** (Adobe, SIL OFL). Full Cyrillic including Bulgarian and Serbian `locl`.
- **Fira Sans** (Spiekermann / Carrois / bBox). Widely cited model case for multi-Cyrillic `locl` execution.
- **Inter** (Rasmus Andersson). Cyrillic added in v3; Bulgarian `locl` in recent versions. Strong for UI.
- **Roboto** — Cyrillic in base; Bulgarian `locl` added in later revisions.
- **IBM Plex Sans / Serif / Mono**, **Public Sans**, **Open Sans**, **Lato**. Cyrillic coverage present; `locl` support varies — verify.

### Russian foundries

- **CSTM Fonts** (Ilya Ruderman, Yury Ostromentsky) — contemporary Cyrillic+Latin, high editorial quality.
- **type.today** — curated catalog / distribution arm; strong editorial voice.
- **3type** (Moscow, ~2017) — contemporary display and text.
- **ParaType** — Yefimov's legacy foundry; broad catalog of Russian classics.

### Ukrainian foundries (post-2022)

Ukrainian type design has grown dramatically in visibility since 2022. Product work targeting Ukrainian users should default to Ukrainian-designed or Ukrainian-supportive typefaces — both for accuracy (Ukrainian-specific `locl` tuning) and for cultural signal.

- **Kyiv Type Foundry** (Yevgeniy Anfalov, Oleś Gergun). Known for **Kyiv Metro Fonts** — typefaces revived from 1960s–70s Kyiv metro signage, free to Ukrainians and by donation during the war.
- **Mint Type** (founded by Andriy Konstantynov, 2004; Oleh Lishchuk joined 2016). First Ukrainian foundry on the international digital market.

### Bulgarian / Serbian / Macedonian foundries

- **Fontfabric** (Sofia, Svetoslav Simov) — Bulgarian-native `locl` in all families.
- **Typonine** (Nikola Đurek), **Tipometar** (Belgrade) — Serbian-native design.

### Historical / classic Cyrillic cuts

- **Academy** (1910 Russian Academy cut digitization), **Lazursky**, **Peterburg** (Yefimov) — canonical Russian literary serifs.
- **ITC Charter, Minion, Arno** — Latin originals with strong Cyrillic extensions.
- **Bodoni / DIN / Futura** — historical families with Cyrillic cuts of varying quality. Helvetica's Cyrillic has been criticized by Russian typographers for weak proportion tuning and minimal `locl` execution.

### Rough pick-a-font heuristics

| Need | Safe default |
|------|--------------|
| UI sans, multi-Cyrillic | Inter, Noto Sans, PT Sans, Source Sans 3 |
| Editorial body serif | Source Serif 4, Noto Serif, PT Serif, Charter, Adelle |
| Broad minority-language Cyrillic | PT Sans / PT Serif (the reference) |
| Bulgarian-specific execution | Fontfabric families, Adelle, Fira Sans |
| Serbian-specific italic `locl` | Typonine families, Fira Sans, Source Sans 3 |
| Ukrainian | Kyiv Type Foundry families, Mint Type, or international with `locl` UKR |
| Display / branding | CSTM Fonts, 3type, type.today catalog |

---

## Web/CSS Gotchas

### 1. Always set `lang` correctly

Without `lang="bg"`, Bulgarian text renders with Russian `locl` forms. Without `lang="sr"`, Serbian italic renders with Russian italic forms. Without `lang="uk"`, some Ukrainian-specific tuning won't fire. `lang` is the trigger; never assume the font will figure it out.

```html
<html lang="ru">...</html>
<p lang="bg">...</p>
<span lang="sr-Cyrl">...</span>   <!-- Explicit script tag for Serbian in Cyrillic -->
```

For Serbian, note that Serbian uses both Cyrillic and Latin scripts interchangeably (Cyrillic is official; Latin is widely used). `lang="sr"` without script suffix is ambiguous — prefer `lang="sr-Cyrl"` for Cyrillic content, `lang="sr-Latn"` for Latin content.

### 2. Don't disable `locl`

```css
/* WRONG — kills locl */
body { font-feature-settings: "locl" 0; }

/* WRONG — resets all features including locl */
body { font-feature-settings: "tnum" 1; }   /* silently disables locl */
```

`font-feature-settings` is *additive per declaration* and a later declaration resets *all* features. If you turn on tabular figures without restating `locl`, you've disabled `locl` for that element. Use `font-variant-numeric: tabular-nums` (which composes correctly) rather than `font-feature-settings: "tnum" 1`.

For explicit safety, the equivalent `font-variant-alternates` approach is cleaner:

```css
body { font-variant-numeric: tabular-nums; }   /* composes with locl */
```

### 3. Verify `locl` coverage in the font

A font can claim "Cyrillic support" without shipping Bulgarian or Serbian `locl`. Always inspect:

- Open the font in Wakamai Fondue (<https://wakamaifondue.com>) or FontDrop.
- Navigate to the GSUB table / Features list.
- Look for `locl` lookups tagged `BGR`, `SRB`, `MKD`, `UKR`.
- If none are listed, the font has only default Russian forms — adequate for Russian, wrong for Bulgarian/Serbian/Macedonian.

### 4. Test text including Bulgarian's distinctive letters

Smoke test for Bulgarian `locl` presence: set this phrase in the font with `lang="bg"`, compare to `lang="ru"`:

```
Добър ден, как сте днес? Това е тест на шрифта.
```

If the в, г, д, п, т, ш, щ, ъ letters look identical in both languages, the font has no Bulgarian `locl`. If they differ (b, taller г, descending д, etc.), the `locl` is firing.

Serbian italic equivalent:

```
Добар дан, како сте данас? Ово је тест. <i>Ово је курзив: беба пита какаве тешки.</i>
```

If italic т looks like Russian italic т (three-legged no overline), no Serbian `locl`. If italic т looks like Latin italic m (with overline), `locl` is firing correctly.

### 5. Font stacks

```css
:lang(ru), :lang(uk), :lang(be) {
  font-family: "Inter", "PT Sans", "Source Sans 3", system-ui, sans-serif;
}
:lang(bg) {
  font-family: "Fira Sans", "Source Sans 3", "Inter", system-ui, sans-serif;
  /* Prioritize fonts with strong Bulgarian locl */
}
:lang(sr), :lang(mk) {
  font-family: "Source Sans 3", "Fira Sans", "Noto Sans", system-ui, sans-serif;
  /* Prioritize fonts with Serbian italic locl */
}
```

System-ui fallback matters: macOS has San Francisco with decent Cyrillic, Windows has Segoe UI Cyrillic. Android/ChromeOS/Linux default to Noto Sans (good) or DejaVu (serviceable).

### 6. Mixing Cyrillic and Latin

Cyrillic and Latin coexist cleanly in most modern Cyrillic-covering fonts (all the Google Fonts canon does this). Metrics match; x-heights match; no tuning needed.

*But:* if you pair two separate families (a Cyrillic-only and a Latin-only), apply metric overrides or `font-size-adjust` so x-heights match. See `../contemporary/metric-overrides.md` and `../techniques/pairing.md`.

### 7. `letter-spacing` on Cyrillic

Safe to use, unlike Arabic or Devanagari. All-caps Cyrillic benefits from more tracking (0.06–0.10em) than all-caps Latin. Italic Cyrillic is sensitive — keep tracking conservative.

### 8. Synthetic bold / italic

Cyrillic needs real italic masters for correct italic form substitution. Synthetic oblique (produced by the browser when the font has no italic master) slants the upright Cyrillic glyphs — which is *wrong* because Russian italic is not a slanted upright, it's a different script-derived glyph set. Synthetic oblique Cyrillic reads as "typographic laziness" to a Russian reader.

```css
@font-face {
  font-family: "CustomCyrillic";
  src: url(…) format("woff2");
  font-synthesis-style: none;   /* disable synthetic italic */
}
```

If the font has a real italic master, the browser uses it. If not, disable synthesis rather than shipping fake italic.

### 9. `text-transform` works

Cyrillic is bicameral (has upper and lower case). `text-transform: uppercase`, `lowercase`, `capitalize` all work correctly. No Turkish-style dotted-i locale gotchas (Russian's І-vs-И doesn't interact with case mapping the way Turkish i-dotted does).

### 10. `hyphens: auto`

Browser hyphenation for Russian exists but quality varies — Chromium and Safari are reasonable, Firefox historically weaker. Set `lang="ru"` to enable. For serious editorial work, pre-process content with a Russian hyphenation-patterns library and insert `\u00AD` at morpheme boundaries.

---

## Anti-patterns

1. **Shipping Russian-default glyphs for Bulgarian content.** Common in Anglo-centric pipelines that ship a font with Cyrillic coverage, declare "Bulgarian support," and skip `locl` verification. The Bulgarian reader sees the text as foreign-set.
2. **Shipping Russian italic for Serbian italic content.** Same pattern; worse visual consequence (the italic т / italic m collision). Serbian readers immediately clock the font as not Serbian-native.
3. **Missing `lang` attribute.** Without `lang="bg"`, `lang="sr"`, `lang="uk"`, etc., `locl` never fires. Browsers do not guess from content.
4. **Using `"..."` (English curly quotes) for Russian prose.** Russian primary is `«...»`; nested is `„..."`. English-curly is unmistakably anglophone.
5. **Em dash without spaces in Russian.** `Москва—столица` looks Anglo-set. Russian convention is `Москва — столица` with spaces.
6. **Using `ch` units for Russian measure.** `1ch` is the width of `0`, no relation to rendered Cyrillic density. Use `rem`.
7. **Synthetic oblique instead of true italic.** `font-style: italic` on a Cyrillic font with no italic master produces a slanted upright, which Russian readers read as "not italicized."
8. **Assuming "Russian" covers Ukrainian.** Missing І, Ї, Є, Ґ → Ukrainian text renders with `.notdef`. Verify Ukrainian letter coverage.
9. **Using Latin `i` for Ukrainian і.** Visually identical at small sizes, different code points (U+0069 vs U+0456). Sorting, search, text-processing all break.
10. **Assuming "Cyrillic" covers minority languages.** A font covering only U+0400–U+04FF may lack Supplement glyphs needed for Kazakh Ә, Bashkir Ҙ, etc. PT Sans/Serif is the reference for minority-language work.
11. **Disabling `locl` globally.** Usually unintended via `font-feature-settings` resets. Kills Bulgarian/Serbian variants silently.
12. **Ignoring weight perception.** Setting Cyrillic body at the same `font-weight` as Latin can produce visually heavy Russian body — the "Cyrillic looks darker" phenomenon.
13. **Pipeline quote-mark substitution without language awareness.** Auto-substituting `"..."` → English curly on Russian content produces English-curly-in-Russian-prose errors.
14. **Using Helvetica's Cyrillic for editorial Russian.** Criticized by Russian typographers for weak proportion tuning and minimal `locl` execution. Prefer Inter, PT Sans, Source Sans, Fira Sans, or a Russian-native family.

---

## Modern State (2024–2026)

**Ukrainian type sovereignty.** Since February 2022, a visible shift in the Ukrainian design community: designers have increasingly rejected Russian typographic norms as a cultural-political matter and are building Ukrainian type design as an independent tradition. Outputs: Kyiv Metro Fonts (Kyiv Type Foundry, 2022–), Ministype, Mint Type's continuing output, increased attention to Ukrainian-specific tuning for ї, є, ґ, and a public rejection of "Cyrillic = Russian" as a default assumption. For product work targeting Ukrainian users, preference-order is now Ukrainian-designed families first, international families with strong Ukrainian tuning second, Russian-designed families third (not inappropriate but politically marked).

**Bulgarian `locl` awareness** has risen sharply since the mid-2010s — driven by Fira Sans, localfonts.eu documentation, type.today's editorial focus on Extended Cyrillic, and Radoeva's writings. Any 2024+ release from a reputable foundry should include Bulgarian variants.

**Serbian italic `locl`** is now expected in serious new releases. Macedonian rides along. Unicode discussions from the 2010s about separate encoding for Serbian variants settled into `locl`-only as the consensus solution.

**Variable fonts in Cyrillic** have matured: PT Sans variable, Inter variable, Noto Sans, Roboto Flex, Source Sans 3 — all provide `wght` across full Cyrillic coverage. `opsz` optical-size axes are less common; the Cyrillic design tradition has fewer optical-size masters historically.

**Kazakh Latinization** has been delayed multiple times since the 2017 announcement. As of 2026-04, mixed use continues — Cyrillic dominant in government and education, Latin in some new signage and branding. Plan for both scripts.

---

## Sources

Accessed 2026-04-18:

- Unicode Consortium — *The Unicode Standard*, Cyrillic blocks U+0400–U+04FF, U+0500–U+052F, U+2DE0–U+2DFF, U+A640–U+A69F.
- Microsoft Typography — OpenType feature registry, `locl` tag documentation.
- type.today — *Manual: Extended Cyrillic — Bulgarian*, *Manual: Quotation Marks*. <https://type.today/en/journal/>
- MyFonts / Krista Radoeva — *Cyrillic script variations and the importance of localisation*. <https://www.myfonts.com/a/font/content/cyrillic-script-variations-and-the-importance-of-localisation>
- Type Journal — *Civil Type and Kis Cyrillic* (Maxim Zhukov / Vladimir Yefimov). <https://typejournal.ru/en/articles/Civil-Type>
- Presidential Library of Russia, National Library of Russia — Peter the Great's 1708 civil type, primary-source digitizations.
- localfonts.eu — *Serbian Cyrillic Feature Locl*, *Macedonian Cyrillic Feature Locl*. <https://localfonts.eu/>
- Pimp my Type — *How to use Quotes and Dashes in Russian Typography*. <https://pimpmytype.com/russian-typography/>
- Fontfabric — *The Typographic Journey of the Bulgarian Cyrillic*. <https://www.fontfabric.com/blog/>
- Nostalgic Dolphin Studio — *Serbian Cyrillic Part 2: True Italic*. <https://nostalgicdolphin.com/blog-post-3/>
- Kyiv Type Foundry, Mint Type — project documentation. <https://kyivtypefoundry.com/>, <https://minttype.com/>
- It's Nice That — *Kyiv Type Foundry is conserving the architectural heritage of Ukraine*.
- Liberation Fonts GitHub — Cyrillic `locl` discussion for Macedonian and Serbian (issue #10).
- Luc Devroye — *Typography in Ukraine*.
- Wikipedia — *Cyrillic script*, *Bulgarian alphabet*, *Serbian Cyrillic alphabet*, *Civil Script*, *PT Fonts*.

**Additional depth (by reference, not cited inline):**

- Yuri Gordon, *Книга про буквы от Аа до Яя* (Russian-language reference on Cyrillic letter shapes and history).
- Vladimir Yefimov — writings on 20th-century Russian type design (Type Journal, ParaType).
- Maxim Zhukov — essays on Cyrillic typography.
- Gerry Leonidas (Reading) — multi-script type design including Cyrillic.
- Krista Radoeva — Bulgarian Cyrillic treatment (TypeTogether, Fontsmith).
- Andrey V. Panov — Serbian Cyrillic italic research-survey.
