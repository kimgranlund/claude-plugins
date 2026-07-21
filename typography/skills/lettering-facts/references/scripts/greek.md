---
date: 2026-04-18
coverage: medium
peers:
  - ./latin.md
  - ./cyrillic.md
  - ../metrics/metrics-glossary.md
  - ../contemporary/opentype-features.md
  - ../contemporary/variable-fonts.md
primary_sources:
  - https://www.unicode.org/charts/PDF/U0370.pdf
  - https://www.unicode.org/charts/PDF/U1F00.pdf
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_uz
  - https://en.wikipedia.org/wiki/Greek_alphabet
  - https://en.wikipedia.org/wiki/Greek_diacritics
  - https://en.wikipedia.org/wiki/Greek_minuscule
  - https://en.wikipedia.org/wiki/Greek_orthography
  - https://en.wikipedia.org/wiki/Greek_Extended
  - https://en.wikipedia.org/wiki/Greek_numerals
  - https://en.wikipedia.org/wiki/Greek_Font_Society
  - https://en.wikipedia.org/wiki/Aldine_Press
  - https://en.wikipedia.org/wiki/Porson_(typeface)
  - https://leonidas.net/2013/12/01/a-primer-on-greek-type-design/ (Gerry Leonidas, *A Primer on Greek Type Design*, University of Reading / ATypI)
  - https://medium.com/@gerryleonidas/designing-greek-typefaces-eac0de7767cc (Leonidas, *Designing Greek typefaces*)
  - https://irenevlachou.github.io/Polytonic-tutorial/ (Irene Vlachou, *Polytonic Greek: a guide for type designers*)
  - https://www.tiro.com/fonts/brill (John Hudson / Tiro Typeworks, Brill Greek)
  - https://www.opoudjis.net/unicode/punctuation.html (Nick Nicholas on Greek punctuation)
  - https://www.opoudjis.net/unicode/numerals.html (Nick Nicholas on Greek numerals)
  - https://greekfontsociety-gfs.gr/ (Greek Font Society)
---

# Greek script — typographic reference

Greek is the script with the longest continuously-printed tradition in the West — Aldus Manutius cut Greek types in Venice in 1495, before he cut his Latin italic — and yet it is the script where modern designers most often ship Latin with a few extra characters and call it "Greek support." The result is web Greek that renders correctly but feels like transliteration: letterforms lifted from Latin designer habits, accents positioned by approximation, final sigma handled by authoring convention rather than font logic, and polytonic combinations that break on half the corpus they're supposed to serve.

This file covers what a designer, engineer, or typographer needs to know to treat Greek as a first-class script: its orthographic split (monotonic vs polytonic), its letter inventory including numeric-only archaic letters, the final-sigma rule and how Unicode resolves it, the upright/italic divergence that separates Greek from Latin oblique habits, the cluster of glyphs that trip non-Greek readers because they share shape with Latin, and the accent-positioning machinery (`ccmp`, `mark`, `mkmk`) that real polytonic support requires.

**What "Greek support" actually means.** A font claiming Greek needs to cover two Unicode blocks, not one:

| Unicode block | Range | Covers |
|---|---|---|
| Greek and Coptic | U+0370–U+03FF | Basic alphabet, monotonic accents, punctuation, archaic letters, Coptic |
| Greek Extended | U+1F00–U+1FFF | 233 precomposed polytonic letter+accent combinations |

Plus the generic combining marks at U+0300–U+036F used to compose polytonic Greek via canonical decomposition. "Monotonic-only" fonts cover Greek and Coptic and call it done; that is adequate for 99% of modern Greek web content and inadequate for any classical, patristic, liturgical, or scholarly work. "Polytonic" support means both blocks, plus the GPOS machinery to position stacked marks correctly on bases they weren't precomposed against.

---

## Historical origin

Greek is the first alphabet proper — the derivation-from-Phoenician, around the 8th century BCE, that repurposed Phoenician consonant glyphs as vowels. This is the typographic innovation Greek gave the script world: not just the introduction of A/E/I/O/U as distinct letterform slots, but the consequence — alphabets with vowels can spell words phonetically, which flattens the gap between reading and speaking and lets literacy spread beyond a scribal caste. Every alphabetic script the West has inherited — Latin, Cyrillic, Coptic, Armenian, Gothic — descends from this Greek move.

**Inscriptional majuscule** dominated through the 5th–4th century BCE and was stable by the classical period: all-caps, large counters, minimal contrast, carved or painted on stone and pottery, written in scriptio continua (no word spaces). This is the Greek analog to Latin's *Capitalis Quadrata* — the monumental, architectural face that set the Platonic ideal of "capital letter" for a millennium. Modern uppercase Greek is still modeled on these inscriptional forms; capital Α, Β, Ε, Ζ, Η, Ι, Κ, Μ, Ν, Ο, Π, Ρ, Τ, Υ, Χ are effectively unchanged from the stones at Athens.

**Byzantine minuscule** (c. 9th century CE) is where modern lowercase Greek actually comes from. Developed in the scriptoria of Constantinople and the monasteries of Mount Athos — Studios Monastery under Abbot Theodore is the canonical origin — minuscule was a cursive book hand, smaller and faster than uncial, heavily ligatured, with character shapes that let a docs write without lifting the pen. The pure-minuscule early phase lasted about a century; from the late 9th century on, scribes inserted majuscule forms into minuscule text, creating the hybrid "upper + lower" feel that carried into print.

**Aldine Greek (1495 onward).** Aldus Manutius in Venice, with punchcutter Francesco Griffo, cut the first Greek type that was both systematic and calligraphic. First used in *Erotemata* by Constantine Lascaris (March 1495). Aldus made two fateful decisions: (1) to model the type on contemporary scribal cursive rather than older formal manuscript hands, and (2) to cast accents on separate sorts that the compositor combined with the base letter at the forme. The choice to follow cursive meant Aldine Greek was full of ligatures, contractions, and variant forms — over 1,400 sorts in the first font — creating a rich but expensive typesetting tradition that dominated scholarly Greek for the next 200 years. Aldine Greek is not the ancestor of modern Greek lowercase in a direct way — its ligatures were later purged — but it is the origin of "Greek type as cursive-based script," which is still the dominant posture.

**Porson (1808)** and the 19th-century simplification. Richard Austin cut a Greek type for Cambridge University Press based on the handwriting of Richard Porson (the Cambridge classicist). First used 1809–1810. Porson deliberately stripped out the Aldine ligatures and variant forms, reducing Greek type to a clean, single-glyph-per-letter set with one consistent slope for lowercase. By the end of the 19th century Porson was the default British scholarly Greek. Still in use — GFS Porson is the digital revival.

**New Hellenic (1927–1928)** — Victor Scholderer, commissioned by the Society for the Promotion of Hellenic Studies, cut by Lanston Monotype. Upright, near-monoline, modeled on a 1492 Venetian type from Giovanni Rosso. New Hellenic is the main 20th-century alternative to Porson in British classical publishing. GFS Neohellenic is the digital revival; Neo-Hellenic's upright lowercase, with no oblique, is *the* example of Greek-as-upright-lowercase tradition.

**Didot Greek (1805)** — Firmin Didot in Paris cut a Greek under the influence of Bodoni-era Didone proportions: high stroke contrast, rationalized construction, thin hairlines. GFS Didot is the digital revival; the Greek edition of *Bibliotheca Teubneriana* uses a Didot-lineage cut. Didot Greek is the template for "modern" Greek in the Didone sense.

---

## Monotonic vs polytonic

This is the headline split. It is not a style choice; it is a spelling-system split, with corresponding typographic machinery.

### Polytonic

The older system, codifying classical and Koine Greek. Applies three accents and two breathings to vowels; can apply both simultaneously; can add a subscript iota under certain long vowels; and can mark diaeresis over vowel clusters:

| Mark | Name | Unicode (combining) | Shape |
|---|---|---|---|
| Acute | `oxia` / `tonos` | U+0301 | `´` rising |
| Grave | `varia` | U+0300 | `` ` `` falling |
| Circumflex | `perispomeni` | U+0342 | `˜` or `῀` tilde/arch |
| Smooth breathing | `psili` | U+0313 | `᾿` right-opening comma |
| Rough breathing | `dasia` | U+0314 | `῾` left-opening comma |
| Iota subscript | `ypogegrammeni` | U+0345 | `ͅ` small ι under base |
| Diaeresis | `dialytika` | U+0308 | `¨` two dots |

A single vowel can carry up to three of these simultaneously — breathing + accent + diaeresis, or (long vowel) breathing + circumflex + iota subscript. The Greek Extended block U+1F00–U+1FFF encodes 233 precomposed combinations covering the common ones. Anything outside those precomposed slots has to be built from base + combining marks and positioned by font-level GPOS rules.

Used in: **classical Greek** (Homer, Plato, Thucydides), **Koine Greek** (New Testament, patristics), **Katharevousa** (the purist register of Modern Greek used in official writing until 1976), **liturgical texts** of the Greek Orthodox Church, **scholarly editions** of any pre-1976 Greek, and a small but stubborn minority of modern publishers and newspapers — the daily *Estia* is the canonical example.

### Monotonic

Adopted as the official orthography of Greece by Presidential Decree 297/1982 (January 11, 1982), following the 1976 decree that made Demotic Greek the sole official language. Polytonic dropped for everyday use. The monotonic system uses only two marks:

| Mark | Name | Unicode | Shape |
|---|---|---|---|
| Tonos | stress accent | U+0301 (combining) / precomposed in U+03AC–U+03CE | `΄` vertical stroke |
| Dialytika | diaeresis | U+0308 (combining) | `¨` two dots |

Only on stressed syllables in polysyllabic words. The tonos is drawn differently from the polytonic acute — more vertical, shorter, more of a tick — but Unicode canonically unifies them: the precomposed monotonic-accented vowels (ά, έ, ή, ί, ό, ύ, ώ) at U+03AC–U+03CE decompose to base + U+0301 (acute), the same combining character used in polytonic. The distinction is stylistic within the font, not semantic at the codepoint level.

Diaeresis splits a would-be diphthong into separate vowel sounds: `παϊδάκι` vs `πaιδάκι`. Combined with tonos you get ΐ, ΰ — two marks over one base, requiring either a precomposed glyph (U+0390, U+03B0) or `mark`+`mkmk` stacking at shaper level.

### Modern typographic practice

- **Web and UI: 99% monotonic.** Any site serving modern Greek — newspapers, government, retail, social — uses monotonic. Google Fonts' Greek subset since 2017 has required monotonic coverage by default and treats polytonic as an opt-in "Greek Plus" set.
- **Classics, patristics, liturgy, scholarly editions: polytonic.** Anyone publishing pre-1976 text, religious texts, or academic editions keeps the full polytonic machinery.
- **Cyprus and the diaspora diverge.** Cyprus officially follows monotonic but retains polytonic in many ecclesiastical and scholarly contexts. The Greek diaspora (Greek Orthodox Archdiocese of America, for instance) trends more polytonic than the metropolitan mainland.
- **Font coverage has improved dramatically since ~2015.** Pre-2015, "polytonic support" in web fonts was a specialty feature; Noto's comprehensive polytonic coverage (2014 onward) and the Greek Font Society's open-license releases (GFS Didot, GFS Neohellenic, GFS Porson, GFS Complutum) have made polytonic rendering ubiquitous. Many commercial fonts still ship monotonic-only — confirm before committing to a project that needs classics support.

**Practical implication for content pipelines.** If you're setting pre-1982 Greek, keep polytonic. Do not "monotonize" classical quotations in a modern Greek document — it reads as barbaric to a classical reader. Conversely, do not set modern Greek text in polytonic unless you are *Estia* or the church.

---

## Letter inventory

### The 24 standard letters

24 uppercase, 24 lowercase, plus one positional variant:

| Upper | Lower | Name | Upper | Lower | Name |
|---|---|---|---|---|---|
| Α | α | alpha | Ν | ν | nu |
| Β | β | beta | Ξ | ξ | xi |
| Γ | γ | gamma | Ο | ο | omicron |
| Δ | δ | delta | Π | π | pi |
| Ε | ε | epsilon | Ρ | ρ | rho |
| Ζ | ζ | zeta | Σ | σ / ς | sigma |
| Η | η | eta | Τ | τ | tau |
| Θ | θ | theta | Υ | υ | upsilon |
| Ι | ι | iota | Φ | φ | phi |
| Κ | κ | kappa | Χ | χ | chi |
| Λ | λ | lambda | Ψ | ψ | psi |
| Μ | μ | mu | Ω | ω | omega |

### Final sigma

Sigma has two lowercase forms. `σ` (U+03C3) appears everywhere inside a word. `ς` (U+03C2) appears only at the end of a word: `Ὀδυσσεύς`, `κόσμος`, `στάσις`. The uppercase Σ covers both — there is no uppercase final sigma.

**Important**: this is not a typographic feature, it is a *codepoint* distinction. `σ` and `ς` have different Unicode codepoints, so the final-sigma rule is enforced at the content layer, not the font layer, in normal Greek text. The OpenType `fina` feature is *not* how most Greek fonts implement final sigma — the input already carries the correct codepoint from the keyboard, input method, or text source. What the font provides is the drawn glyph for each codepoint.

There is one context where `fina` or equivalent automatic substitution matters: **uppercase-to-lowercase conversion**. When you `text-transform: lowercase` an uppercase Greek word ending in Σ, the browser needs to know whether to output σ or ς. The CSS `text-transform` + browser locale awareness *should* handle this on `lang="el"`, and modern browsers (Chrome, Safari, Firefox since ~2017) do so correctly for Greek word-end detection. Older browsers and non-locale-aware transforms produce `οδυσσευσ` — broken. The same concern applies to JavaScript `toLowerCase()` — use `toLocaleLowerCase('el')` to get correct final-sigma handling.

A secondary context: some fonts ship a `fina` or stylistic-alternate lookup that provides a *final sigma variant* (a more decorative or differently-weighted form) when the codepoint is U+03C2. This is a typographic refinement, not the core rule.

### Archaic letters (numeral-only in modern use)

Five letters survive purely for the alphabetic numeral system:

| Glyph | Unicode | Name | Numeral value |
|---|---|---|---|
| Ϛ / ϛ | U+03DA / U+03DB | stigma | 6 |
| Ϝ / ϝ | U+03DC / U+03DD | digamma / wau | 6 (historical) |
| Ϙ / ϙ | U+03D8 / U+03D9 | koppa (archaic) | 90 |
| Ϟ / ϟ | U+03DE / U+03DF | koppa (numeric) | 90 |
| Ϡ / ϡ | U+03E0 / U+03E1 | sampi | 900 |

Digamma (Ϝ) originally represented the phoneme /w/ and was used in archaic Greek alphabets; by late antiquity it had morphed in handwriting into the shape now encoded as stigma (Ϛ, itself originally a στ-ligature), and the two are often treated as numeral-equivalent glyphs for 6. Koppa originally represented /k/ before back vowels; sampi was the letter for /ss/ or /ts/ in some archaic dialects. In modern Greek typography none of these are letters; they appear only as numerals, and only in ceremonial or traditional contexts — chapter numbers in classical editions, legal document clauses, liturgical readings, monarchical regnal numbers.

### Numerals

Greek has **two numeral systems** in parallel use:

- **Western Arabic digits** (0–9) for every modern quantitative use — dates, prices, addresses, scientific data, UI chrome. Same codepoints as every other Latin-using language.
- **Alphabetic numerals** (the Milesian system) for ceremonial and traditional use. Letters of the alphabet carry numeric values: α=1, β=2, γ=3, ..., ι=10, κ=20, ..., ρ=100, σ=200, ..., with the archaic letters filling the gaps (stigma=6, koppa=90, sampi=900). To distinguish numerals from words, a small acute-like mark called the **keraia** is placed upper-right of the last letter: `αʹ` = 1, `βʹ` = 2. For thousands, a keraia is placed lower-left: `͵α` = 1000. Unicode encodes two keraia codepoints: U+0374 (upper right) and U+0375 (lower left).

Modern typographic contexts for Greek numerals:
- Chapter numbers in classical editions (`κεφάλαιον αʹ` = chapter 1)
- Articles in legal documents and constitutions (`Ἄρθρον βʹ` = Article 2)
- Monarchical regnal numbers (`Κωνσταντίνος ΙΑʹ` = Constantine XI)
- Liturgical cycle markers
- Church fathers' chapter numbering in patristic editions

Not for: UI chrome, data tables, commerce, contemporary dates.

Fonts that cover Greek numerals properly include the keraia glyphs, the archaic letter-numerals, and ideally position the keraia at the correct optical height (slightly above the letter's x-height for upper keraia, below baseline for lower). GFS fonts, Noto Serif Greek, Brill Greek, and Arno Pro cover this fully.

---

## Upright vs italic

Latin italic and Greek italic diverge in history and in visual behavior. Understanding this split matters for any designer pairing Greek with Latin or selecting a Greek face.

### Greek's default is cursive-ish

The modern Greek lowercase descends from Byzantine minuscule, which was itself a book-hand cursive. So the *default* upright Greek lowercase already carries calligraphic movement: α, γ, δ, ε, ζ, ξ, σ, ω all have terminals and inner logic that come from pen-strokes, not from Latin's Roman-capital-based lowercase. Compare the "feel" of Greek lowercase to Latin lowercase in Times New Roman: Times's Greek is visibly more cursive than its Latin, because the historical source is more cursive.

**Practical implication**: a Greek upright is roughly equivalent to a Latin "semi-italic" in terms of calligraphic energy. This is why pairing Greek with Latin is tricky — a Latin + Greek page can feel like the Greek is already leaning forward, even though both are upright.

### Greek italic has distinct glyphs

When you *do* italicize Greek, some lowercase letters shift to entirely different shapes — derived from different calligraphic traditions, not mechanically slanted:

| Letter | Upright form | Italic form (typical) |
|---|---|---|
| α | curved open-bowl (like single-story Latin `a`) | more cursive, often with exit stroke |
| γ | descending y-like | often more of a curl, with a different descender |
| ζ | z-like with descender | more flourished, often with looped descender |
| κ | angular | can become more cursive with rounded junction |
| λ | inverted-V | italic form often has a curled top or different junction |
| φ | circle-with-vertical-stroke | often with more angled axis |
| θ | oval-with-horizontal-stroke | often more compressed, different crossbar angle |

Because the upright is already cursive, and the italic draws from *different* cursive traditions (primarily the 16th-century Aldine/Griffo cursive versus the Porson-era revision), Greek italic differs from upright more visibly than in Latin — but the *direction* of difference is not "more cursive" (they're both cursive) but "differently cursive." Many readers outside the Greek tradition find Greek italic harder to parse than Greek upright; experienced Greek readers treat it as a normal emphasis shift.

**`slnt` vs `ital` for Greek**: same rule as Latin — `slnt` gives you a mechanically oblique roman (which for Greek means a slanted upright with *upright* glyph constructions), `ital` gives you a true italic with the redrawn α, γ, ζ, κ, λ forms. For editorial or scholarly Greek where emphasis matters, prefer families that offer a true italic. For UI chrome in Greek, oblique-only is usually fine because italic emphasis is rare in interface copy.

### Families and their italic status (as of 2026)

| Family | Greek italic type | Notes |
|---|---|---|
| Noto Sans Greek / Noto Serif Greek | True italic (redrawn) | Comprehensive monotonic + polytonic; the ubiquitous baseline. |
| GFS Didot | True italic | Didone-contrast Greek with traditional italic; polytonic. |
| GFS Neohellenic | Upright only, limited italic | Scholderer's New Hellenic was conceived as upright-only; digital version adds a limited italic. |
| GFS Porson | Already slanted (historically-oblique upright) | Porson's handwriting leans ~8°; there is no separate italic because the "upright" already slopes. |
| Brill Greek (Tiro Typeworks) | True italic | Neo-Didot scholarly face; deep polytonic; seven-thousand-glyph family. |
| Inter | Oblique (`slnt`), not true italic | Monotonic only in the core release (as of Inter 4.x). |
| Source Sans 3 / Source Serif 4 | True italic | Monotonic + polytonic; extensive `locl` Greek coverage. |
| Roboto | Oblique | Monotonic; decent baseline coverage; not for classics. |
| Fira Sans / Fira Code | True italic | Monotonic + polytonic; popular with scholarly tech writing. |
| IBM Plex Sans / Serif | True italic | Monotonic + polytonic; solid accent positioning. |
| Times New Roman Greek | True italic (Scholderer-era cut) | Historical Monotype standard; scholarly default for generations. |

---

## Confusable glyphs (Greek-vs-Latin trap)

The single most common amateur error in Greek typography is *setting Greek text using Latin codepoints that look Greek-ish in the current font*. A document that contains "KOSMOS" written with Latin K, O, S, M, O, S looks right but is not Greek — copy-paste breaks, search breaks, screen readers misread, OpenType `locl` can't trigger. The reverse trap exists too: setting a Latin word with a stray Greek codepoint.

| Greek glyph | Unicode | Latin lookalike | Unicode | Tell |
|---|---|---|---|---|
| Α alpha | U+0391 | A | U+0041 | Identical in most fonts; the codepoint differs |
| Β beta | U+0392 | B | U+0042 | Identical |
| Ε epsilon | U+0395 | E | U+0045 | Identical |
| Ζ zeta | U+0396 | Z | U+005A | Identical |
| Η eta | U+0397 | H | U+0048 | Identical |
| Ι iota | U+0399 | I | U+0049 | Identical |
| Κ kappa | U+039A | K | U+004B | Identical |
| Μ mu | U+039C | M | U+004D | Identical |
| Ν nu | U+039D | N | U+004E | Identical |
| Ο omicron | U+039F | O | U+004F | Identical |
| Ρ rho | U+03A1 | P | U+0050 | Identical in upright, sometimes differs in italic |
| Τ tau | U+03A4 | T | U+0054 | Identical |
| Υ upsilon | U+03A5 | Y | U+0059 | Similar; Greek often has slight differences in crotch |
| Χ chi | U+03A7 | X | U+0058 | Identical |
| β beta | U+03B2 | ß eszett | U+00DF | Close — see below |
| ν nu | U+03BD | v | U+0076 | Greek nu has a harder angle, v has softer curves |
| ο omicron | U+03BF | o | U+006F | Identical in most fonts |
| ρ rho | U+03C1 | p | U+0070 | Rho has no ascender; p has ascender/descender |
| χ chi | U+03C7 | x | U+0078 | Chi often descends; x usually doesn't |
| ω omega | U+03C9 | w | U+0077 | Different shape but confusable in low-res |

**β vs ß (the biomedical-writing hazard).** Greek lowercase beta (U+03B2) and German lowercase eszett (U+00DF) have similar shape in most fonts but subtly different construction: beta has a distinct top-loop-then-bottom-loop cursive form; eszett has an s+s ligature origin. In biomedical writing (β-adrenergic receptors, β-carotene, β-glucan), the correct codepoint is U+03B2; when "ß" sneaks in — commonly from autocorrect in German locales or legacy encodings — the text is silently broken. Science editors now treat this as a standard pre-submission check.

**ρ vs p.** In upright Greek, ρ (rho) typically has no ascender — it sits at x-height with a descender, like `p` without the top. Latin `p` has both an ascender region (the bowl sits at x-height and the stem descends) and a distinct construction. In some italic and display faces they become visibly distinct; in default body text they can be confused by non-Greek readers.

**Content-layer defense.** Unicode's UTS39 ("Unicode Confusables") documents these pairs. Tools like `unicode-confusable` npm package or OS-level text validators flag Greek-in-Latin-word mixes. Any CMS editing Greek content should run a confusables-pass before publishing. Browsers already do this for URLs (to prevent homograph phishing); content systems should do it for body text.

**Test string for identifying which codepoint a document contains**: paste `K ≠ Κ ≠ k ≠ κ`. If your font renders all four differently, the codepoints are distinct; if two look identical, you can't tell by eye.

---

## Accent positioning (OpenType machinery)

### Monotonic

Monotonic Greek has three positioning challenges:

1. **Tonos on base vowel** — either a precomposed glyph (ά, έ, ή, ί, ό, ύ, ώ at U+03AC–U+03CE) or base + U+0301 positioned via `mark` GPOS lookup.
2. **Dialytika on base vowel** — ϊ (U+03CA), ϋ (U+03CB), plus decomposed base + U+0308.
3. **Tonos + dialytika together** — ΐ (U+0390), ΰ (U+03B0), plus the decomposed base + U+0308 + U+0301 stack.

The third case is the tricky one. A font needs `mark` (for positioning the dialytika on the base) and `mkmk` (mark-to-mark, for positioning the tonos on top of the dialytika). Fonts that ship monotonic but don't implement `mkmk` correctly put the tonos directly on the base with the dialytika overlapping, yielding a visual collision. This is a common defect in cheap web fonts.

### Polytonic

Polytonic Greek is significantly more intricate. Consider `ᾅ` (alpha with dasia + oxia + iota subscript, U+1F85) or `ᾧ` (omega with dasia + perispomeni + iota subscript, U+1FA7). The Greek Extended block precomposes the common combinations, but:

- Non-standard combinations fall back to combining marks
- Older scholarly editions use combinations not covered by Greek Extended
- Normalization forms (NFC vs NFD) can decompose precomposed to combining-marks at runtime

A font with real polytonic support needs:

- **`ccmp` (Glyph Composition / Decomposition)** to normalize input — both handle precomposed codepoints and compose from combining-marks to correct positioning anchors.
- **`mark`** to position each mark (accent, breathing, subscript, diaeresis) correctly relative to its base.
- **`mkmk`** to position marks relative to other marks when they stack vertically (breathing + accent + diaeresis can all be present).
- **`locl GRK`** (optional) to activate Greek-specific variant forms.

The positioning anchors in a polytonic font are numerous: the base letter has an anchor for breathing, another for accent-atop-breathing, another for diaeresis, another for iota-subscript below. Each mark has anchors for what sits above it. When all wired correctly, `ᾅ` renders as iota-subscript below alpha, with dasia and oxia stacked above, all visually balanced.

**Fonts that get polytonic right**: Noto Serif Greek, Noto Sans Greek, Brill Greek, GFS Didot, GFS Neohellenic, GFS Porson, GFS Complutum, Arno Pro (Adobe), Minion Pro Greek, SBL Greek (Society of Biblical Literature), Cardo, EB Garamond (Greek subset). Many sans-serif web fonts (including older Inter versions and older Roboto) do not cover polytonic; check before committing.

### Leading considerations

Polytonic Greek needs more `line-height` than Latin at the same font-size because the accent stack (breathing + accent + diaeresis) pushes visual content higher than Latin's cap-line. Rule of thumb: add ~10–15% to your baseline `line-height` for polytonic text. Monotonic needs a slight but smaller increase — about 5–8% — because the tonos alone rises less than a polytonic stack.

```css
:root { --body-line-height: 1.5; }

:lang(el) { line-height: 1.58; }                    /* monotonic bump */
:lang(el).polytonic { line-height: 1.68; }          /* polytonic bump */
```

If your typeface's `hhea` / `OS/2` ascent metrics were tuned only for Latin, the default line-box height may clip polytonic marks at the top of each line. Check with a test string like `ᾅγιος Ἀθανάσιος λέγει·` and confirm the breathings and accents sit inside the line-box at default `line-height`.

---

## Math symbols — distinct from prose Greek

Greek letters are used extensively in mathematics, science, and engineering: α as angle, β for beta-decay, γ for Lorentz factor, δ for delta-change, π for the ratio, Σ for summation, Ω for ohm. These are not the same codepoints as Greek letters in running prose.

- **Prose Greek**: U+0370–U+03FF (Greek and Coptic) plus U+1F00–U+1FFF (Greek Extended). Rendered with Greek-specific letterforms designed for body text.
- **Mathematical Greek**: U+1D6A8–U+1D7CB (Mathematical Alphanumeric Symbols block, Greek subset). Encodes bold, italic, bold-italic, sans-serif, sans-bold, sans-italic, sans-bold-italic variants of each Greek letter — distinct codepoints, distinct glyphs, designed to be used in isolation (not connected to other letters).

This matters typographically because:

1. A math expression `σ = √(Σ(x − μ)²)` should use math codepoints (e.g., U+1D70E for italic sigma, U+1D6F4 for italic sigma-as-variance). These render with metrics tuned for inline math, not prose.
2. A prose sentence *discussing* mathematics ("the Greek letter sigma represents standard deviation") uses prose codepoints (σ, U+03C3). These render with Greek-language metrics.
3. The OpenType `mgrk` (Mathematical Greek) feature, when activated, substitutes prose-Greek codepoints with math-Greek variants within a styled run. This is how LaTeX distinguishes `$\sigma$` from `σ` in running Greek text.

The practical implication: **when setting Greek-language content in `<html lang="el">`, ensure your CSS pipeline does not run a math-rendering filter (KaTeX, MathJax, MathML) over the body — it may silently swap prose-Greek codepoints with math-Greek variants, breaking `locl` Greek rendering and yielding inline italic shapes where upright Greek was intended.**

---

## Punctuation

Greek punctuation overlaps Latin but diverges in four places:

### Question mark (erotimatiko)

The Greek question mark is visually identical to an English semicolon: `;`. Unicode encodes a canonical Greek Question Mark at U+037E but canonically equates it to U+003B SEMICOLON — so `U+037E` normalizes to `U+003B` and in practice both render the same. This is a Unicode-level decision: the Greek Question Mark and the Latin Semicolon are the *same* character, just named differently.

**Consequence**: authors don't need to switch input — the semicolon key on a Greek keyboard produces the question-mark glyph in Greek text. But **screen readers and search tools treat `;` in Greek contexts as a question mark**, only if they are locale-aware; otherwise they read it as a semicolon, yielding broken TTS.

### Ano teleia (high dot)

Greek uses a distinct mid-height dot `·` to mark a clause-boundary weaker than a full stop — functionally the Greek semicolon (since the semicolon glyph is already the question mark). Unicode U+0387 (Greek Ano Teleia). Canonically equivalent to U+00B7 MIDDLE DOT; the two normalize to the same character but render at slightly different optical heights: ano teleia is correctly positioned near the top of the x-height (like the top dot of a colon), while generic middle dot sits at the optical x-height center. Real Greek fonts draw the glyph at ano-teleia position when the codepoint appears in `lang="el"` context.

**Practical**: in Greek body text, `·` (middle dot) is the ano teleia. Don't use `;` for this role — `;` is the question mark.

### Full stop and comma

Same as Latin: `.` and `,`. Used identically.

### Quotation marks

Modern Greek uses French-style **«guillemets»** (εισαγωγικά, *eisagogika*) as primary quotes: `«Γεια σου»`. Unicode U+00AB, U+00BB. Spacing inside guillemets follows French convention *loosely* — some Greek typographers add narrow non-breaking spaces inside, others don't; Greek does not have a strict rule like French.

For **nested quotes**, the most common modern convention is `"..."` (U+201C, U+201D) — the English double-curly quotes. Some older typography uses `'...'` (U+2018, U+2019). German-style low-high `„..."` is sometimes seen in academic editions.

**Direct speech in narrative fiction**: Greek often uses the em-dash (U+2015, Horizontal Bar) at the start of each speaker's turn, similar to Spanish and French dialogue convention:

```
―Γεια σου, είπε.
―Πώς είσαι;
```

**Straight ASCII quotes (`"..."` and `'...'`)**: amateur, but prevalent on Greek web forms and social media where input methods default to straight. A Greek editorial pipeline should normalize to guillemets or to curly quotes depending on house style.

### Dashes

- `-` (U+002D) hyphen — compound words, line-break hyphenation. Same as Latin.
- `–` (U+2013) en dash — ranges (`1821–1830`), parenthetical. Same as Latin.
- `—` (U+2014) em dash — rare in running Greek prose; mostly editorial.
- `―` (U+2015) horizontal bar — dialog attribution (as above). More common in Greek than in English prose.

### Ellipsis

`…` (U+2026). Same as Latin. One space after in running prose; often no space before.

---

## Language tagging and CSS

Every Greek text span should carry `lang="el"` at the HTML level — or `lang="grc"` for Ancient Greek, `lang="el-polyton"` for Modern Greek written polytonically. The browser uses this to:

1. Trigger OpenType `locl GRK` substitutions in fonts that have Greek-specific alternates.
2. Apply locale-aware case-mapping (so `text-transform: lowercase` correctly handles final sigma).
3. Drive screen-reader pronunciation.
4. Drive hyphenation (Greek hyphenation rules differ from Latin; `hyphens: auto` on `lang="el"` applies Greek rules).

```html
<html lang="el">                          <!-- Modern Greek, monotonic -->
<p lang="el-polyton">Ἀλλ᾽ ἤτοι μὲν ταῦτα</p>   <!-- Modern Greek, polytonic -->
<p lang="grc">μῆνιν ἄειδε θεά</p>               <!-- Ancient Greek -->
<p lang="grc-x-koine">Ἐν ἀρχῇ ἦν ὁ Λόγος</p>   <!-- Koine Greek specifically -->
```

```css
/* Bump leading for polytonic */
:lang(el-polyton),
:lang(grc) {
  line-height: 1.68;
  font-feature-settings: "mkmk" 1, "mark" 1, "ccmp" 1;
}

/* Monotonic default */
:lang(el) {
  line-height: 1.58;
}

/* Greek often wants a slightly taller cap-height match — size-adjust helps */
@font-face {
  font-family: "Helv Greek Fallback";
  src: local("Helvetica Neue Greek");
  unicode-range: U+0370-03FF, U+1F00-1FFF;
  size-adjust: 102%;
}
```

---

## Notable fonts with strong Greek coverage (as of 2026)

**Foundries / families prioritizing Greek:**

- **Greek Font Society** — non-profit founded 1992 by Michael Macrakis. Open-license releases: **GFS Didot** (Firmin Didot 1805 revival), **GFS Neohellenic** (Scholderer 1927 revival), **GFS Porson** (Porson 1808 revival), **GFS Complutum** (Renaissance-inspired), **GFS Bodoni**, **GFS Artemisia**, **GFS Olga**. Polytonic across the main releases. SIL Open Font License. The canonical open-source Greek type archive.
- **Brill Greek** (Tiro Typeworks, John Hudson with Alice Savoie) — commissioned 2008 by Koninklijke Brill; released 2014 under Brill's scholarly-use license. Deep polytonic, neo-Didot stroke modulation, 7,000+ glyphs per weight covering Greek, Latin, IPA, Cyrillic, and historical letterforms. The scholarly standard.
- **SBL Greek** (Society of Biblical Literature) — free for academic use. Biblical Greek orientation; deep polytonic.

**Pan-script web fonts with competent Greek:**

- **Noto Sans Greek** / **Noto Serif Greek** — Google's Noto project; comprehensive monotonic + polytonic, 127 Greek-and-Coptic glyphs plus 233 Greek Extended glyphs; updated continuously, Unicode 16.0 coverage as of 2024. The baseline.
- **Source Sans 3** / **Source Serif 4** — Adobe open-source; monotonic + polytonic; excellent `locl` hints.
- **Fira Sans** — deep Greek; monotonic + polytonic; popular for scholarly-tech.
- **IBM Plex Sans** / **IBM Plex Serif** — monotonic + polytonic; decent accent positioning.
- **EB Garamond** — open-source Garamond revival; has a Greek subset with polytonic; scholarly editing favorite.
- **Gentium Plus** (SIL International) — purpose-built for minority-language scholarship; deep polytonic and unusual combinations.

**Historical type / commercial:**

- **Porson** (Cambridge, 1808) — historical; revived as GFS Porson.
- **Monotype New Hellenic** (Scholderer 1927) — historical; revived as GFS Neohellenic.
- **Monotype Times New Roman Greek** (Scholderer-era cut) — the Times's Greek is the 20th-century scholarly default, widely used in academic publishing.
- **Monotype Gill Sans Greek** — Eric Gill's sans with a Greek cut; upright-lowercase tradition.
- **Arno Pro** (Robert Slimbach, Adobe) — deep polytonic, Renaissance-inspired, optical-size variants.
- **Minion Pro Greek** (Slimbach, Adobe) — monotonic + polytonic; opsz masters; scholarly workhorse.

**Commercial sans-serif with Greek (Greek is often an afterthought but may be adequate):**

- **Roboto** — monotonic; no polytonic coverage. Not for classics.
- **Inter** — monotonic; polytonic coverage expanding in 4.x releases. Confirm before shipping.
- **Helvetica Neue** — monotonic Greek cut; polytonic absent.
- **Helvetica Now** — monotonic Greek added 2019; polytonic partial.
- **FS Emeric**, **GT Walsheim Greek**, **Founders Grotesk Greek** — commercial Greek cuts of designers; quality varies widely; check polytonic coverage specifically.

---

## Quality indicators — does this font support real Greek?

1. **Polytonic Greek Extended coverage (U+1F00–U+1FFF).** Paste `ᾅ ᾧ ἀ ἐ ἰ ὀ ὐ ὠ ἁ ἑ ἱ ὁ ὑ ὡ ἆ ἶ ὖ ὦ`. Every glyph should render without `.notdef` boxes. If any fall back, the font is monotonic-only — adequate for modern web Greek, inadequate for classics.

2. **Accent stack positioning.** Paste `ΐ ΰ ᾄ ᾅ ᾆ ᾇ`. Verify the diaeresis + tonos / breathing + accent + iota-subscript all sit cleanly without overlap. If the dialytika and tonos collide on ΐ, `mkmk` is broken.

3. **Final sigma.** Type `κόσμος πόλις στάσις` — sigma at word-end should render as ς, internal sigma as σ. If all sigmas render as σ, the input pipeline (not the font) is broken.

4. **Ano teleia and question mark.** Test `Ναί· αλλά είναι; Όχι.` — the ano teleia should sit at x-top, and the `;` should be at baseline. If the ano teleia renders as a low middle dot, the font has not tuned its U+0387 glyph for Greek context.

5. **Archaic numerals.** Paste `ʹ ͵ αʹ βʹ ϛʹ ϟʹ ϡʹ` (keraia + alphabetic numerals with stigma-for-6, koppa-for-90, sampi-for-900). If any fall back, ceremonial Greek text (chapter numbers, legal articles) will render broken.

6. **Italic distinctive forms.** Switch Greek text to italic. The α, γ, ζ, κ, λ forms should visibly differ from the upright — if they look merely slanted, the font has oblique Greek only, not true italic.

7. **Latin pairing proportions.** Set a mixed Latin-Greek paragraph. The x-heights should match within ~2%, the cap-heights within ~3%. If Greek runs visibly taller or shorter than Latin, the font's Greek master was not tuned to match Latin metrics.

8. **`locl GRK` forms.** Confirm `font-feature-settings: "locl" 1` (or `lang="el"`) triggers Greek-specific variant forms if the font ships them. Not all fonts have these; absence is fine for utilitarian text, notable for editorial.

A font passing 1–4 is adequate for modern Greek web. Passing all eight is the mark of a genuinely Greek-first typeface — typically GFS, Noto, Brill, SBL, Gentium, Adobe's Arno / Minion, or a specialty commercial release.

---

## Anti-patterns

1. **Setting Greek words with Latin codepoints.** `KOSMOS` typed with Latin K, O, S, M, O, S looks right, breaks copy, breaks search, breaks screen readers, suppresses `locl`. Always use Greek codepoints for Greek text.

2. **Using `;` as a semicolon in Greek prose.** `;` is the Greek question mark. The Greek semicolon-equivalent is `·` (ano teleia, U+0387). Setting `Ναί; αλλά...` as "yes semi-colon but" yields "yes-question-mark but" to a Greek reader.

3. **"Monotonizing" classical quotations in modern Greek text.** A paragraph of modern Greek that quotes Homer in monotonic looks barbarian. Keep polytonic for classical quotations even in monotonic running text; set the classical span in `lang="grc"` and ensure the font covers polytonic.

4. **Polytonic Greek in a monotonic-only font.** Precomposed polytonic glyphs (Greek Extended) fall back to `.notdef`; combining marks stack wrongly because there are no GPOS anchors. Before shipping any polytonic site, confirm the font has Greek Extended coverage and `mkmk`.

5. **Missing `lang` attribute.** Greek without `lang="el"` gets Latin-default case-mapping, Latin-default hyphenation, Latin-default `locl` (which does nothing for Greek), and Latin TTS pronunciation. `<html lang="el">` at minimum for any primarily-Greek page.

6. **Math-filter over prose Greek.** A MathJax / KaTeX / MathML global style that assumes every Greek letter is math Greek will re-render prose Greek in math-italic shape. Scope math rendering to explicit math contexts only.

7. **Line-height tuned to Latin for polytonic Greek.** `line-height: 1.4` on a polytonic Greek paragraph clips breathings and accents. Bump to ~1.65–1.7 for polytonic, ~1.55 for monotonic.

8. **Treating Greek italic as Latin oblique.** Some designers assume Greek italic is "just slanted upright" and ship oblique. Greek readers experience this as missing emphasis, because the expected italic glyph-shift (α, γ, ζ, κ, λ changing form) doesn't happen.

9. **β-vs-ß confusion in biomedical writing.** `ß-adrenergic` should be `β-adrenergic`. Content-editing tools should flag U+00DF in English-language scientific text as likely a Greek-beta mistake.

10. **Shipping "Greek support" without polytonic for an academic publisher.** Any publisher doing classics, patristics, liturgy, or scholarly editions needs polytonic. A font shop advertising Greek without Greek Extended coverage should not be on the shortlist.

11. **Using straight-ASCII quotes for Greek dialogue.** Modern Greek editorial convention uses guillemets `«...»` or em-dash dialogue `―`. Straight `"..."` signals amateur typesetting.

12. **Composing polytonic text with wrong combining-mark order.** Unicode prescribes base + breathing + accent + iota-subscript (or equivalent). Wrong order (e.g., base + accent + breathing) yields glyphs that look right but break normalization, search, and `ccmp` lookups. Always rely on the input method or canonical normalizer (NFC) to sort.

13. **Ignoring the keraia on Greek numerals.** Writing `Ἄρθρον β` without the keraia (`Ἄρθρον βʹ`) renders as "Article beta" rather than "Article 2." Unicode U+0374 is the numeric keraia; it is not optional.

---

## Sources

- Leonidas, Gerry. *A Primer on Greek Type Design* (1998–2002, revised 2013). University of Reading / ATypI.
- Leonidas, Gerry. "Designing Greek typefaces" on Medium.
- Vlachou, Irene. *Polytonic Greek: a guide for type designers.*
- Hudson, John (Tiro Typeworks) — Brill Greek documentation.
- Macrakis, Michael S. (ed.) *Greek Letters: From Tablets to Pixels* (Oak Knoll Press, 1996).
- Scholderer, Victor. *Greek Printing Types 1465–1927* (London: British Museum, 1927).
- Nicholas, Nick. Greek-in-Unicode background pages (opoudjis.net).
- Barker, Nicolas. *Aldus Manutius and the Development of Greek Script & Type in the Fifteenth Century* (Fordham University Press, 1992).
- Unicode Consortium — Greek and Coptic (U+0370), Greek Extended (U+1F00), Mathematical Alphanumeric Symbols (U+1D400) charts.
- Microsoft Typography — OpenType feature registry (`locl`, `mkmk`, `mark`, `ccmp`, `mgrk`, `fina`).
- Greek Font Society (greekfontsociety-gfs.gr) — GFS Didot, Neohellenic, Porson, Complutum, Bodoni documentation.
- Google Fonts Greek Glyph Sets documentation (Greek Core / Greek Plus).
- Noto Sans Greek / Noto Serif Greek project repositories (notofonts/Noto-LatinGreekCyrillic).
- Wikipedia — Greek alphabet, Greek diacritics, Greek minuscule, Greek orthography, Porson (typeface), Aldine Press, Greek numerals.
