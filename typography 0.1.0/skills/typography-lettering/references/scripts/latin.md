---
date: 2026-04-17
coverage: deep
peers:
  - ./cyrillic.md
  - ./greek.md
  - ./arabic.md
  - ../metrics/metrics-glossary.md
  - ../metrics/anatomy.md
  - ../contemporary/opentype-features.md
  - ../techniques/figures.md
  - ../techniques/small-caps.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/featuretags
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-locl
  - https://www.unicode.org/charts/PDF/U0080.pdf
  - https://www.unicode.org/charts/PDF/U0100.pdf
  - https://www.unicode.org/charts/PDF/U0180.pdf
  - https://www.unicode.org/charts/PDF/U1E00.pdf
  - https://www.unicode.org/charts/PDF/U0300.pdf
  - https://www.w3.org/International/questions/qa-html-language-declarations
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-alternates
  - https://www.w3.org/TR/css-fonts-4/#font-rend-opentype
  - https://type.today/en/journal (Indra Kupferschmid writings)
  - https://ilovetypography.com/2008/01/17/typographic-illustration-small-caps/
  - Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012)
  - Highsmith, Cyrus. *Inside Paragraphs* (Font Bureau / Princeton Architectural Press, 2020)
  - Lupton, Ellen. *Thinking with Type* (2nd ed., Princeton Architectural Press, 2010)
  - Hochuli, Jost. *Detail in Typography* (Hyphen Press, 2008)
  - Hardwig, Florian. *Fonts In Use* editorial (fontsinuse.com)
  - https://rsms.me/inter/ (Inter specimen — Latin Extended coverage)
  - https://fonts.google.com/knowledge/glossary/opentype
---

# Latin Script Typography

Latin is the default script of the modern web, the script most UI libraries are built around, and the script against which every other script's metrics are implicitly compared. It is also the script whose typographic conventions are most often taken for granted — designers ship "Latin support" that covers English and miss Polish, Vietnamese, or Romanian, because the ASCII subset renders correctly and the failure only shows up in content the team doesn't test.

This file is the deep reference for Latin-specific typographic decisions: classical vs modern proportion voice, the true-italic / oblique distinction, numeral styles and when each wins, small caps that aren't embarrassing, punctuation the font actually supports, pan-European diacritic coverage, `locl` language-specific variant forms, and the spacing conventions that separate competent multilingual type from English-only output. It assumes a Western-Latin primary audience who wants to handle extended Latin (Vietnamese, Turkish, Central European, Nordic, Celtic) correctly.

**What "Latin" actually includes.** Unicode splits Latin into seven blocks that you should understand you are shipping or not shipping:

| Unicode block | Range | Covers |
|---|---|---|
| Basic Latin | U+0020–U+007F | ASCII — English only |
| Latin-1 Supplement | U+0080–U+00FF | Western European (é, ñ, ü, ß, æ, etc.) |
| Latin Extended-A | U+0100–U+017F | Central/Northern European (ą, č, ę, ł, ő, ř, ș, ș, ť, ů, ž) |
| Latin Extended-B | U+0180–U+024F | Rare African, historical, IPA-adjacent |
| Latin Extended Additional | U+1E00–U+1EFF | Vietnamese + extra combining forms |
| Latin Extended-C / D / E | U+2C60+, U+A720+, U+AB30+ | Medievalist, phonetic, minority |
| Combining Diacritical Marks | U+0300–U+036F | Floating accents composed onto base letters |

"We support Latin" in practice almost always means "we support Latin-1 Supplement." That excludes every Polish, Czech, Romanian, Hungarian, or Vietnamese user. A font claiming multilingual Latin support should cover **Basic Latin + Latin-1 Supplement + Latin Extended-A + Latin Extended Additional (full Vietnamese)**, ideally + the `locl` features below. Anything less is English-adjacent, not pan-European.

---

## Proportions

Latin letterforms sit on a small set of horizontal reference lines — baseline, x-line, cap-line, ascender-line, descender-line — and the *ratios* between those lines are the single largest lever a type designer has over the typeface's personality and the single largest lever a typographer has over perceived size at a given point size. See `../metrics/metrics-glossary.md` for the full measurement vocabulary; this section is about ratio conventions.

### Uppercase height

Cap-height typically falls between **~0.66 × em** (classical, 1500s–1700s book faces) and **~0.72 × em** (modern). A few display designs push to 0.74–0.76. Above that, the uppercase starts crowding its own ascender-line and the typeface begins to feel cramped at text sizes; below 0.65, the face looks miniature against surrounding UI chrome.

"Em" here means the font's UPM (units-per-em) as declared in `head.unitsPerEm` — typically 1000 (PostScript/CFF convention) or 2048 (TrueType) — which the browser normalizes to `1em` at whatever `font-size` the CSS sets. So `cap-height: 0.7em` when `font-size: 16px` renders roughly 11.2px of visible uppercase.

A distinct trap: **cap-height is not always equal to the height of every uppercase glyph**. Flat-topped letters (`H`, `I`, `T`, `E`, `F`, `L`, `Z`) sit on the cap-line. Round-topped (`O`, `C`, `G`, `Q`) and pointed-topped (`A`, `V`, `W`) letters *overshoot* the cap-line by typically 1–2% of em so they perceive as the same height. "Uppercase height" in casual speech conflates these; in type design they are separate metrics.

### Lowercase x-height

X-height is where era and UI/prose orientation split most visibly.

| X-height range | Era / character | Examples |
|---|---|---|
| 0.35–0.45 × em | Classical / Renaissance / historic revivals | Garamond Premier, Centaur, Adobe Jenson |
| 0.45–0.50 × em | Transitional / early modern | Baskerville, Caslon, Times New Roman |
| 0.50–0.55 × em | Modern text, most contemporary sans | Helvetica, Futura (despite geometric claims), Source Sans 3, Inter |
| 0.55–0.70 × em | Screen-first / UI-optimized / grotesque | Inter, Roboto, IBM Plex Sans (especially at its lower optical sizes), Helvetica Now Micro |
| 0.70+ | Display, advertising faces | ITC Avant Garde in display cut, most logo faces |

The UI-driven convention of the last twenty years is **taller x-heights** — to make text scanable at 14–16px on a low-DPI screen, you want the counters of `e`, `a`, `o`, `s` to be as large as possible. The cost is: the ascenders of `h`, `l`, `k`, `b`, `d` grow shorter relative to the cap-line, the descenders of `g`, `y`, `p`, `q` grow shorter relative to the baseline, and the overall "texture" — the vertical rhythm Bringhurst calls the "colour" of the text — flattens toward a stripe of x-height with little protrusion above or below. A high-x-height face reads as *crisp and even at small size* and *airless at large size*. A low-x-height face reads as *elegant and spacious at large size* and *cramped and illegible at small size*.

Practical rule for a UI designer: **if body text is under 16px, pick an x-height in the 0.52–0.60 range**. Below 0.48 is a mistake for sub-16px body; above 0.64 is a mistake for editorial long-form.

### Ascender and descender height

Ascender-line sits above the cap-line by a small amount (in classical designs, ascenders are noticeably taller than caps; in modern UI designs, ascenders and caps often coincide or caps slightly exceed). Descender-line sits below the baseline.

**Ascender : x-height** in typical proportions:

| Ratio | Reads as | Example |
|---|---|---|
| 1.4–1.6 | Classical, spacious | Adobe Garamond, Minion |
| 1.2–1.4 | Contemporary text | Source Sans, Charter |
| 1.0–1.2 | UI / condensed | Inter, SF Pro, Roboto |

**Descender : x-height** similarly: 0.6–0.8 is typical for text; 0.4–0.5 is UI-short.

Why it matters beyond aesthetics: the OpenType `hhea`/`OS/2` ascent/descent metrics drive the browser's default line-box height. A typeface with generous ascenders/descenders forces larger line-boxes *even at the same `font-size`*, which changes perceived line-height. This is why swapping Georgia for SF Pro at the same `font-size` silently shifts the rhythm of the whole page — the line-boxes are different sizes. See `../metrics/metrics-glossary.md` on `hhea` vs `OS/2` vs `typo` metric divergence.

### Why high-x-height fonts dominate UI

Interface text lives at 12–16px, below the threshold where classical proportion works. A 0.45 × em x-height at 13px font-size yields **5.85px** of rendered lowercase body — below what sub-pixel anti-aliasing can cleanly resolve on many screens. A 0.55 × em x-height at the same 13px yields 7.15px — a 22% increase in effective body-signal area, at no cost in `font-size`. This is the single largest reason Inter, Roboto, SF Pro, Segoe UI, and Helvetica Now exist: they are *the same point size* as older faces but feel larger because the resolved body-height is larger.

The sacrifice: at 24–48px headings and above, the same faces look squat and untextured compared to Garamond, Sabon, Janson. Editorial long-form magazines that push back against UI-default typography (The New Yorker, the current Matter/Medium-aspirant reading views) specifically choose low-x-height faces because they carry better at size.

---

## Italic Traditions

Latin italic is the one place where "italic" is not a stylistic synonym for "slanted" — it is (when done right) an entirely separate script tradition grafted onto Roman type.

### True italic

The canonical italic descends from **chancery cursive** — a handwriting style developed in 15th-century Italy for papal correspondence, formalized by Aldus Manutius in 1501 and cut by Francesco Griffo. It is a *script* form, with its own letter constructions, its own internal logic, and its own rhythm. Real italic has:

- Different letter shapes, not just slanted versions. `a` in roman is usually double-story; `a` in italic is typically **single-story** (like a handwritten `a`). `e` has a different crossbar angle and counter. `f` often grows a **descender** in italic (it goes below the baseline) even when it has no descender in the roman.
- A different proportion. Italic is usually narrower than roman.
- A cursive slope, typically 8–14°, though the slope is not the defining feature — you could have an upright italic (Bringhurst cites examples) and it would still be italic.
- Different terminals. Italic `n`, `m`, `h` often have entry strokes on the left (vestigial pen-in-motion); roman doesn't.
- Separately designed glyphs throughout — the italic is *drawn*, not generated.

Recognize real italic by the single-story `a` and by the `f` descender. If both are present, it's a true italic. If neither is present, it's almost certainly oblique.

### Oblique (slanted roman)

An **oblique** is a roman typeface that has been mechanically slanted — each glyph is the roman glyph tipped 8–14° to the right, with optical compensation (corner redrawing, balance adjustments) but the same underlying letter construction. Oblique `a` is still double-story. Oblique `f` does not grow a descender. The letters have the same width and proportion as their roman counterparts.

Oblique is the house style of the **geometric sans** tradition (Futura's "italic" is oblique), the **grotesque/neo-grotesque** tradition (Helvetica, Akzidenz-Grotesk, Univers — all oblique despite being labeled "italic"), and most industrial sans before the 2010s. It is a legitimate choice for display faces where script-flavor would feel out of place, and it is a *fraud* in text faces where readers expect the reading-contrast signal of real italic.

### The `slnt` vs `ital` variable axis distinction

Variable fonts formalize this. OpenType defines two axes for "going italic":

- **`slnt` (slant)**: a continuous numeric axis, typically 0 to -10 or -12, that applies a slant transform (or interpolates pre-authored slanted masters). `slnt` is *oblique*. The glyph set does not change — you get the same letter constructions mechanically slanted.
- **`ital` (italic)**: a binary axis (0 or 1) that selects a true italic. `ital=1` typically loads an entirely different glyph set with single-story `a`, descending `f`, humanist `e`, etc.

A well-designed variable family that takes italic seriously will expose **both**: `ital` as a binary selector between roman and true italic, and optionally `slnt` within the italic master for a small further slope adjustment. Most families expose only one. When a family offers only `slnt`, the "italic" is oblique — know that before using it in editorial settings.

### Who provides which

| Family | Italic type | Notes |
|---|---|---|
| Helvetica (Neue, Now) | **Oblique** | The "italic" in Helvetica is slanted roman. Helvetica Now Display adds subtle optical tuning but remains oblique in construction. |
| Inter | **Has `slnt` only** → oblique | Rasmus Andersson's Inter ships oblique as `slnt`; the italic is not a separate cursive. |
| Source Sans 3 | **True italic** | Paul D. Hunt's Source Sans 3 Italic is a drawn cursive — single-story `a`, humanist `e`. `ital` axis. |
| SF Pro | **Oblique** | Apple's SF Pro Italic is a slanted roman. |
| Roboto | **Oblique** (mechanical slant) | Roboto's italic is slanted; single-story `a` present in some weights, but construction is oblique. |
| IBM Plex Sans | **True italic** | Plex Sans Italic is drawn cursive. |
| Helvetica Now Variable | Exposes `slnt` (no `ital`) | Consistent with Helvetica house style — oblique. |
| Recursive | **Both axes** | Stephen Nixon's Recursive exposes `slnt` continuous plus `CASL` (casual), combines oblique with substantive shape changes. |
| Times New Roman | **True italic** | A drawn cursive; single-story `a`, different `e`. |
| Georgia | **True italic** | Matthew Carter's Georgia Italic is a drawn cursive. |
| Bodoni, Didot | **True italic** | Traditional. |

**When building editorial prose**, prefer true italic families — the reading-eye shift from roman to italic is a meaningful emphasis signal, and oblique doesn't carry it as strongly. **When building UI chrome or interface text**, oblique is usually fine because italic is used sparingly and ornamentally. **Never mix within a single typeface**: if Helvetica's italic is oblique, don't use it in a long-form editorial footnote and expect it to read as cursive emphasis — it won't.

### CSS

```css
/* Binary — selects whichever italic the font offers, oblique or true */
.em { font-style: italic; }

/* Explicit angle — only works for variable fonts with slnt */
.slanted { font-style: oblique -10deg; }

/* Variable font with both axes */
.true-italic {
  font-family: "Recursive";
  font-variation-settings: "slnt" 0, "CASL" 0;
  font-style: italic;  /* triggers ital=1 if the family has that axis */
}
```

`font-style: italic` will select a true italic if one exists and fall back to oblique if only that exists. `font-style: oblique` explicitly requests slant and will synthesize one if the font has no italic at all — which yields the worst of all worlds. See `../contemporary/variable-fonts.md` for the full axis-wiring recipe.

---

## Numerals

Latin has four numeral styles, formed by two independent axes: **height** (lining vs old-style) and **width** (proportional vs tabular). The 2×2 of those two axes is the complete space.

### Lining figures

Also called **titling figures** or **modern figures**. All numerals sit on the baseline and rise to roughly cap-height. They read as uppercase — visually matching the capitals, visually contrasting lowercase.

```
0 1 2 3 4 5 6 7 8 9   ← lining, roughly cap-height, uniform top and bottom
```

Default for most 20th-century and later typefaces, default for every UI sans, default for tables and data. Introduced in the late 18th century (the Didone era) and dominant since.

### Old-style figures

Also called **text figures**, **oldstyle figures**, **non-lining figures**, **lowercase figures**. Numerals have varied height: some sit at x-height (0, 1, 2), some ascend (6, 8 — sometimes), some descend (3, 4, 5, 7, 9 — sometimes; varies by foundry). They read as lowercase — blending with surrounding prose.

```
0 1 2 3 4 5 6 7 8 9   ← variable height; 3, 4, 5, 7, 9 descend; others sit at x-height
```

Originally the *only* numerals in European typography before the 18th century, then displaced by lining, then revived by Morris and the Arts & Crafts movement for body text. Still the correct choice in:

- Running prose where numerals appear mid-sentence: "he was born in 1897". Lining figures "he was born in 1897" intrude because they visually shout; old-style "he was born in 1897" blend.
- Literary books, editorial magazines, academic texts.
- Anywhere the numeral is a quantity *mentioned*, not a quantity *measured*.

### Tabular figures

Each numeral occupies the same horizontal advance-width — `1` takes the same space as `8`. Essential when numerals stack vertically and alignment matters: financial tables, data grids, timestamps in logs, counters that update in place, Monaco-for-numerals territory.

```
  1,234.56
     45.00
 12,345.67    ← columns align when tabular; misalign when proportional
```

Tabular figures sacrifice proportion — the `1` has extra whitespace around it because the glyph is narrow but the advance-width is widened to match — for alignment. At small point sizes the extra whitespace around `1` is almost invisible and feels correct; at headline sizes it looks sparse.

### Proportional figures

Each numeral has its natural width — `1` is narrow, `8` is wide. The default for running prose; proportional figures read more smoothly in flowing text because they don't introduce ragged whitespace.

### The 2×2

```
                        PROPORTIONAL                  TABULAR
                   ┌──────────────────────┬─────────────────────────┐
    LINING         │ Prose with numerals, │ Data tables, financial, │
                   │ UI chrome, default   │ CSV-rendered grids      │
                   ├──────────────────────┼─────────────────────────┤
    OLD-STYLE      │ Editorial body prose │ Rare — scholarly        │
                   │ with numbers in run  │ footnote tables, some   │
                   │ (novels, magazines)  │ classical typesetting   │
                   └──────────────────────┴─────────────────────────┘
```

- **Lining proportional** — the default. Data-friendly fonts like Inter, Roboto, SF Pro ship this as the default numeral set.
- **Lining tabular** — tables, forms, timestamps, any vertical alignment.
- **Old-style proportional** — editorial body text. Garamond, Minion, Source Serif, Charter's text cut.
- **Old-style tabular** — genuinely rare. Old-style figures vary in height, which fights vertical alignment; tabularizing them is a compromise. Use only for scholarly footnote tables in classically-set books.

### CSS

```css
/* height axis */
.prose { font-variant-numeric: oldstyle-nums; }
.ui    { font-variant-numeric: lining-nums; }   /* usually the default */

/* width axis */
.data  { font-variant-numeric: tabular-nums; }
.prose { font-variant-numeric: proportional-nums; }

/* combined */
.ledger { font-variant-numeric: oldstyle-nums tabular-nums; }
.chart  { font-variant-numeric: lining-nums tabular-nums; }

/* Escape hatch: direct OpenType feature settings */
.escape { font-feature-settings: "tnum" 1, "onum" 1; }
```

The `font-variant-numeric` property is the modern API; it compiles to `font-feature-settings` internally but composes correctly with other font-variant shorthand. Avoid `font-feature-settings` directly unless you need a feature `font-variant-*` doesn't expose — `font-feature-settings` is *additive per declaration* and a later declaration resets all features, which bites people in cascade. See `../contemporary/opentype-features.md` for the full list of feature tags and composition rules.

**Dynamic counters and timers must use tabular figures.** A countdown timer rendering `1:02 → 1:01 → 1:00 → 0:59` with proportional numerals appears to twitch horizontally as character widths change. Lining tabular numerals keep the numbers glyph-locked to a column. The same rule: every stepper, every numeric input, every live-updating metric.

**Data tables must use tabular figures.** A table of currency that misaligns its decimal points because the numerals are proportional is a bug, not a style choice.

**Body prose should prefer proportional.** Old-style if the design is editorial; lining if it's newsy / utilitarian. Forced tabular in prose produces pedantic whitespace around `1`s.

---

## Small Caps

Small caps — uppercase letterforms drawn at roughly lowercase height — are the typographer's tool for emphasis-that-doesn't-shout, for acronyms in prose, for author bylines, and for running heads.

### True small caps

A proper small-cap glyph is drawn deliberately: roughly x-height + overshoot tall, with stem weights *matched to the lowercase stems* (not the uppercase stems), with proportions that sit comfortably in a line of lowercase. A page of `this sentence is set in small caps` should read with even colour — the SCs should carry the same visual weight as the surrounding prose.

Type designers who take small caps seriously draw them as a separate, weight-matched set covering the uppercase alphabet plus often diacritics (ÁÉÍÓÚ small-cap), punctuation (tuned for the SC's height), and sometimes small-cap numerals (old-style figures at small-cap height — for SC tabular). Delivered via OpenType `smcp` (small caps) and `c2sc` (capitals-to-small-caps).

### `smcp` vs `c2sc` vs `smcp+c2sc`

- **`smcp`** — "small caps": converts *lowercase* letters to small caps. `the url` → `THE URL` at small-cap size.
- **`c2sc`** — "capitals to small caps": converts *uppercase* letters to small caps. `The URL` → `The URL` at small-cap size.
- **`smcp` + `c2sc`** — converts everything to small caps regardless of original case. `The URL` → `THE URL` with even SC height throughout.

The important case: you have an acronym in running prose, `the URL endpoint`, and you want the URL to set at small-cap height to match the prose weight *without shouting uppercase*. Turn on `c2sc` only: `the URL endpoint` — the lowercase stays lowercase, the uppercase `URL` shrinks to SC. This is the correct convention for acronyms in professionally set body text.

### Fake small caps

When a font does not ship `smcp`/`c2sc`, the browser will synthesize small caps via `font-variant: small-caps`. Synthesis is *not drawn* — it's a mechanical scale-down of the existing uppercase glyphs. That means the stems of the fake SC are *lighter* than the surrounding lowercase stems — because uppercase stems are already slightly lighter than lowercase at the same weight, and scaling a uppercase glyph down further lightens it still. The result: the SC run looks anemic against the prose colour.

Always check before shipping. Open the browser, set a paragraph in small-caps, put your eye two inches from the screen, and look for unevenness of colour. If the SC feels lighter or smaller than the lowercase stems, the font doesn't have `smcp` and the browser synthesized it. Either switch to a font with real SCs, or abandon the small-cap treatment.

### CSS

```css
/* High-level, preferred — selects true smcp if available, synthesizes if not */
.author { font-variant-caps: small-caps; }        /* = smcp */
.acronym { font-variant-caps: all-small-caps; }   /* = smcp + c2sc */
.petite { font-variant-caps: petite-caps; }       /* smaller than SC — rare */
.unicase { font-variant-caps: unicase; }          /* blends upper+lower as one */
.titling { font-variant-caps: titling-caps; }     /* caps drawn for large size */

/* Fallback / explicit */
.acronym-explicit {
  font-feature-settings: "smcp" 1, "c2sc" 1;
}
```

### When to use

- **Acronyms in running prose**: `c2sc` only. `The URL request returned` becomes `The URL request returned`.
- **Lead-in run**: first few words of a section set in SC, a century-old editorial convention. `This article explores...` — the "This article explores" sets in small caps, then the rest of the paragraph resumes regular.
- **Running heads, folios, author bylines**: SC as a marker of the editorial meta-layer, distinct from body.
- **Letter-spaced emphasis**: `font-variant: small-caps; letter-spacing: 0.05em;` is the Bringhurst-approved alternative to italic for quiet emphasis. Less shouty than all-caps, less reading-speed-cost than italic on many faces.
- **Not for**: UI button labels (use regular capitals), for emphasis inside UI copy (use semantic `<em>`), for decorative display (use a proper display face).

See `../techniques/small-caps.md` for the full small-cap recipe and composition with letter-spacing and tracking.

---

## Punctuation

Punctuation is the single most visible place where "Latin typography" becomes "English typography" if you don't pay attention. Every language the reader sets has its own conventions; every font has its own coverage.

### Dashes

Four distinct horizontal lines, each with a semantic role:

| Character | Unicode | Typical role |
|---|---|---|
| Hyphen `-` | U+002D | Joins compound words: `state-of-the-art`, `twenty-one`. Also line-break hyphenation. |
| En dash `–` | U+2013 | Ranges (`1999–2012`), compound modifiers where the components are themselves multi-word (`New York–London flight`), and some parenthetical use in British English. Width ≈ one N-glyph. |
| Em dash `—` | U+2014 | Parenthetical break in American English — like this — marking interrupted thought or aside. Width ≈ one M-glyph. |
| Horizontal bar `―` | U+2015 | Speech attribution in some European conventions (Spanish, Russian dialogue). Rare in English. |

The modern US convention is **em dash with no surrounding spaces** (`like this—an em dash`). The British convention is **en dash with spaces** (`like this – an en dash`). Both are valid; pick one and stay consistent.

**Never use a hyphen for an em dash.** `like this - bad` looks amateur. The glyph is visibly shorter and it carries the wrong semantic weight.

**Never use two hyphens for an em dash.** `like this -- very bad` is a typewriter convention, dead since variable-width type became universal. If your content pipeline emits `--`, transform it to em-dash in your Markdown → HTML stage (most processors do this; `smartypants` plugin handles `--` → `–` and `---` → `—`).

### Quote marks

Straight quotes (`"`, `'`) are typewriter / ASCII artifacts. Typographic quotes are directional:

| Character | Unicode | Role |
|---|---|---|
| `'` | U+2018 | Left single quote / opening |
| `'` | U+2019 | Right single quote / closing + apostrophe |
| `"` | U+201C | Left double quote / opening |
| `"` | U+201D | Right double quote / closing |

English uses `"..."` for primary and `'...'` for nested: `She said, "I heard him say 'no' clearly."`

Other languages differ:

| Language | Primary | Secondary | Notes |
|---|---|---|---|
| English (US/UK) | `"..."` | `'...'` | U+201C/U+201D + U+2018/U+2019 |
| German (de-DE) | `„..."` | `‚...'` | Low-then-high: U+201E bottom, U+201C top |
| Swiss German (de-CH) | `«...»` | `‹...›` | French-style guillemets |
| French (fr-FR) | `«\u202F...\u202F»` | `"..."` | Guillemets with narrow non-breaking space inside |
| Spanish (es-ES) | `«...»` or `"..."` | alt | Guillemets traditional, curly quotes common in modern text |
| Italian (it-IT) | `«...»` or `"..."` | alt | Same dual-convention as Spanish |
| Polish (pl-PL) | `„..."` | `«...»` | Low-then-high primary, guillemets secondary |
| Czech (cs-CZ) | `„..."` | `‚...'` | Same as German pattern |
| Swedish (sv-SE) | `"..."` | `'...'` | High-high on both sides |
| Dutch (nl-NL) | `'...'` | `"..."` | Single-quotes as primary (Bringhurst-era convention) |
| Japanese | `「...」` | `『...』` | CJK brackets, not Latin quotes |
| Russian | `«...»` | `„..."` | Guillemets primary, German-style nested |

The naïve approach: "use curly quotes." The correct approach: match the reader's language. A French-language page using `"..."` instead of `«\u202F...\u202F»` looks like auto-translated content to a French reader. The `lang` attribute on the HTML element should drive rendering where possible; Markdown-to-HTML processors (like Pandoc with `smart` extension, or `typogr.js`) can substitute correctly per language.

**Apostrophe (U+2019) vs prime (U+2032).** Measurements use the prime (`5\u2032 11\u2033` = five feet eleven inches), not the apostrophe (`5' 11"` is a coarser, typewriter-era rendering). The prime glyph is drawn like a tick mark; the apostrophe is a small-ball or comma-shape. Mixing them in running prose makes the `'` for apostrophe and the `'` for minutes visually indistinguishable, which is why Unicode separates them.

### Ellipsis

The ellipsis character `…` (U+2026) renders as three dots at the glyph-designer's chosen spacing — typically with tighter-than-period spacing and no baseline break. The three-periods rendering `...` renders as three independent full stops with regular word-spacing and can line-break between the dots, producing `..\n.` at a column break.

Use **`…`** for the ellipsis as a punctuation mark (mid-sentence trail-off, elision of quoted text, UI "load more" indicator). Use three periods only when you specifically want the three-periods treatment (rare in prose).

**Spacing around ellipsis.** English convention: no space before, one space after when mid-sentence; a space on each side when used as a pause mark. French convention: ellipsis replaces the trailing punctuation, no narrow-space before. Chicago Manual of Style and Oxford Style Guide disagree on whether to use `. . .` (period-space-period-space-period) in scholarly quotations — which is a different beast from the Unicode ellipsis. Pick your house style.

### Semicolon and colon

Visually these are two marks stacked; typographically their positioning matters. The colon sits on the baseline + cap-height (two dots, vertically aligned, upper dot at about cap height). The semicolon is colon-top-plus-comma-bottom.

**In French (and some continental conventions): a narrow non-breaking space precedes `?`, `!`, `:`, `;`, and sits *inside* guillemets.** The narrow non-breaking space is U+202F. Modern browsers on `lang="fr"` should apply this automatically via font or locale rules, but in practice you have to author it:

```html
<p lang="fr">Et voilà&#8239;? «&#8239;Bonjour&#8239;»&#8239;!</p>
```

Spanish uses inverted `¿` (U+00BF) and `¡` (U+00A1) at the start of interrogative / exclamatory clauses, paired with the upright version at the end: `¿Qué pasa?` and `¡Hola!`.

### Guillemets and bracket variants

French / Italian / Spanish / Russian use **«...»** as primary quotes (U+00AB, U+00BB). Single-guillemet variants `‹...›` (U+2039, U+203A) are for nested quotes in French. German typography historically used **»...«** (reversed guillemets pointing inward) but now commonly uses the low-high pattern `„..."`.

A font claiming pan-European Latin support must cover guillemets; plenty of older Anglo-centric fonts omit them.

---

## Diacritics

The Latin Extended repertoire. A font that supports "Latin" is only supporting some fraction of this. Check coverage before committing.

### Western European (Latin-1 Supplement)

The ones an English designer mostly remembers:

- **ä ö ü** (German, Swedish, Finnish umlaut)
- **é è ê ë** (French acute, grave, circumflex, diaeresis)
- **à â æ** (French)
- **í ï î** (Spanish, French)
- **ó ò ô ö õ ø** (Spanish, French, Portuguese, Dutch, Danish)
- **ú ù û ü** (Various)
- **ñ** (Spanish tilde-n)
- **ç** (French/Portuguese/Catalan cedilla)
- **ß** (German sharp s, lowercase-only in most traditions; since 2017 Unicode added `ẞ` capital sharp s, U+1E9E)
- **å** (Nordic)

If your font handles this and nothing else, you're shipping "Latin-1" — adequate for Western European but not for Poland, Czech Republic, Hungary, Romania, the Baltics, or Vietnam.

### Central and Eastern European (Latin Extended-A)

**Polish**: `ą`, `ę` (nasal vowels with ogonek), `ł`, `Ł` (barred L — a distinct phoneme, not a decoration), `ń` (acute n), `ó` (acute o — not the same sound as unaccented o in Polish), `ś`, `ź`, `ż` (acute and dot-above s/z).

**Czech / Slovak**: `č`, `š`, `ž`, `ř`, `ň`, `ť`, `ď` (háček / caron), `ů` (ring-above u — distinct from `u` in Czech), `ě` (caron e).

**Hungarian**: `ő`, `ű` (double acute), plus `é`, `á`, `í`, `ó`, `ö`, `ü`.

**Romanian**: `ă`, `â`, `î`, `ș`, `ț`. Romanian's `ș` and `ț` are **comma-below**, not cedilla — more on this in `locl` below.

**Baltic**: Latvian `ā`, `ē`, `ī`, `ō`, `ū` (macrons); Lithuanian `ą`, `ę`, `į`, `ų` (ogoneks) + `č`, `š`, `ž`; Estonian `õ`, `ä`, `ö`, `ü`.

### Nordic

- **æ** (Norwegian, Danish, Faroese, Icelandic) — a distinct letter, not a ligature
- **ø** (Norwegian, Danish, Faroese) — a distinct letter
- **å** (Swedish, Norwegian, Danish)
- **ð** (Icelandic, Faroese — "eth")
- **þ** (Icelandic — "thorn")

These are letters in their respective alphabets, sorting at specific positions — not decorated variants of `a`, `o`, `d`, `p`. They are often missing from fonts aimed at Southern European markets.

### Vietnamese (Latin Extended Additional)

Vietnamese stacks up to two diacritics on a single base vowel — one *quality* mark (circumflex, breve, horn) plus one *tone* mark (acute, grave, hook-above, tilde, dot-below). The five tone marks modify meaning:

| Tone | Mark | Example |
|---|---|---|
| Level | (no mark) | `ma` (ghost) |
| Falling | `\u0300` grave | `mà` (that/which) |
| Rising | `\u0301` acute | `má` (mother/cheek) |
| Dipping-rising | `\u0309` hook-above | `mả` (tomb) |
| Creaking-rising | `\u0303` tilde | `mã` (horse in Chinese loanword sense) |
| Falling-creaking | `\u0323` dot-below | `mạ` (rice seedling) |

And quality marks stack on top of those:

- `ă` (breve-a) → `ằ`, `ắ`, `ẳ`, `ẵ`, `ặ` (breve-a + each tone)
- `â` (circumflex-a) → `ầ`, `ấ`, `ẩ`, `ẫ`, `ậ`
- `ơ` (horn-o) → `ờ`, `ớ`, `ở`, `ỡ`, `ợ`
- `ư` (horn-u) → `ừ`, `ứ`, `ử`, `ữ`, `ự`
- `ê` (circumflex-e) → `ề`, `ế`, `ể`, `ễ`, `ệ`

This yields ~130 precomposed Vietnamese vowel-with-diacritic glyphs across Latin Extended Additional. Each needs to be drawn (or correctly composed via mark-to-base GPOS positioning) such that the two stacked marks don't collide with each other or with ascenders of adjacent letters.

**Fonts that ship competent Vietnamese**: Inter, IBM Plex Sans, Source Sans 3, Noto Sans, Roboto, Public Sans, Fira Sans (recent versions), Sarabun (for SEA-region pairing). Fonts that *look* like they ship Vietnamese but drop or crudely stack marks include many commercial 2010-era webfonts that claimed "European support" without extended-Latin QA.

### Turkish

**Turkish has a dotted-vs-dotless distinction for the letter `i`:**

- `i` (dotted, U+0069) ↔ `\u0130` (`İ`, dotted capital)
- `\u0131` (`ı`, dotless) ↔ `I` (dotless capital, U+0049)

In English, uppercase of `i` is `I` (dot disappears). In Turkish, uppercase of `i` is `İ` (dot retained) and lowercase of `I` is `ı` (no dot). This is **not** a diacritic decoration — it's a case-mapping rule that requires locale-aware `toLocaleUpperCase('tr')` / `toLocaleLowerCase('tr')` at the application level.

### The pan-European completeness checklist

Before claiming a font "supports Latin Extended":

- [ ] Latin-1 Supplement: all Western European glyphs including `æ`, `ß`, `ñ`, `ç`, `ø`, `å`
- [ ] Latin Extended-A: Polish `ąęłńóśźżĄĘŁŃÓŚŹŻ`, Czech `čšžřěňťďůČŠŽŘĚŇŤĎŮ`, Hungarian `őűŐŰ`, Romanian `ăâîșțĂÂÎȘȚ`, Baltic macrons and ogoneks
- [ ] Nordic extras: `ð`, `þ`, `Ð`, `Þ`
- [ ] Latin Extended Additional: Vietnamese precomposed combinations — all ~130 glyphs
- [ ] Combining Diacritical Marks (U+0300–U+036F) with correct mark-to-base positioning for any vowel-mark combo not precomposed
- [ ] Capital sharp s `ẞ` (U+1E9E) if targeting German since 2017
- [ ] Small cap forms of all accented glyphs, if the font has `smcp`
- [ ] Lining and old-style figures both, if the font claims both
- [ ] Currency: `€`, `£`, `¥`, `¢`, `₹` (Indian rupee), `₽` (Russian rouble), `₩` (Korean won), `\u20AA` (Israeli shekel), `\u20BF` (Bitcoin, since 2017)
- [ ] Ellipsis, em-dash, en-dash, typographic quote marks for every locale above
- [ ] Guillemets: `«`, `»`, `‹`, `›`
- [ ] Inverted Spanish: `¿`, `¡`
- [ ] Non-breaking space and narrow non-breaking space (U+00A0, U+202F)

---

## `locl` Variants

The OpenType `locl` feature substitutes locale-specific glyph variants based on the text's declared language. In CSS, this is triggered by the `lang` attribute on the containing HTML element — *not* by the `:lang()` pseudo-class alone, and *not* by JavaScript locale detection. The browser must read `lang` on the document tree.

```html
<html lang="en"> ... </html>                    <!-- triggers locl ENG -->
<p lang="tr">Türkçe metin</p>                   <!-- triggers locl TRK -->
<p lang="nl">IJsselmeer</p>                     <!-- triggers locl NLD -->
<p lang="ca">ŀla paraula</p>                    <!-- triggers locl CAT -->
<p lang="pl">Łódź</p>                           <!-- triggers locl PLK -->
<p lang="ro">Iași</p>                           <!-- triggers locl ROM -->
```

If the font has `locl` tables for the declared language, the shaper substitutes the appropriate glyphs. If not, the default form renders. This is why `lang` is not optional — without it, a Dutch site's `ij` digraph renders as English-default `ij` with two independent dots instead of the Dutch `IJ` where the dots of `i` and `j` share a tittle region.

### Dutch IJ

Dutch treats the digraph `IJ` as a single letter, capitalized as `IJ` (both glyphs uppercase) when starting a proper noun: `IJmuiden`, `IJsselmeer`, `IJssel`, the given name `IJ`. The digraph is not the ligature `Ĳ` (U+0132, `IJ`) though that glyph exists and some older sources use it. Modern Dutch typography uses two separate characters `I` + `J` *rendered* with locale-specific adjustments.

Key typographic details:

- Dots on the `ij` lowercase: in Dutch, the tittles of `i` and `j` align — sometimes touching, sometimes merged into a single over-wide dot, sometimes separated but positioned identically. In non-Dutch rendering, the `j` tittle sits slightly higher and to the right.
- Capital IJ: both letters full-height, no gap wider than within a word.
- At the start of `IJmuiden`-style proper nouns, *both* letters capitalize together (not just `Ij`).

```html
<p lang="nl">IJsselmeer — ijsbeer</p>
```

With `locl NLD` the font emits the adjusted `ij`/`IJ` forms. Fonts that ship this: TheMix/TheSans (LucasFonts), MarkSimonson's Proxima Nova, Lato, Source Sans 3, Inter.

### Turkish i

Covered above under Diacritics. The key `locl` interaction: fonts with `locl TRK` ensure that sort-adjacent glyphs (dotted/dotless capital/lowercase) carry correct widths and diacritic positioning.

**Application-level requirement**: case-conversion of `i` ↔ `İ` and `I` ↔ `ı` must use Turkish locale. In JavaScript:

```js
'istanbul'.toUpperCase()           // → "ISTANBUL" — WRONG for Turkish
'istanbul'.toLocaleUpperCase('tr') // → "İSTANBUL" — correct
'BILGI'.toLocaleLowerCase('tr')    // → "bilgi" — correct
```

The page `lang="tr"` triggers the typographic `locl`; the application code must also be locale-aware for text transformation.

### Catalan ŀl (punt volat)

Catalan has a geminate-L convention — `ŀl` with a middle-dot — to indicate that the two `l` letters are pronounced separately (geminate L) rather than as the Catalan palatal L (`ll`, a single phoneme like a soft "ly"). Examples: `col·lecció`, `il·lusió`, `al·lèrgia`.

In Unicode, `l` + U+00B7 MIDDLE DOT + `l` is the spelling. `locl CAT` ensures the middle-dot is positioned *between* the two l-stems (not floating below the baseline as U+00B7 usually renders) and at the correct vertical level to read as an L-punt-volat rather than a generic middle dot.

```html
<p lang="ca">col·lecció il·lusió</p>
```

A font without `locl CAT` renders `l·l` with the middle-dot too low and misaligned. Catalan readers find this unmistakably wrong.

### Polish kreska accents

The Polish acute accent (`ć`, `ń`, `ó`, `ś`, `ź`) is drawn **steeper than the Czech acute** in Polish typographic tradition — closer to vertical, short, and set higher above the letter. In Czech, the acute (`á`, `é`, `í`, `ó`, `ú`, `ý`) is drawn more horizontally and somewhat longer.

A font with `locl PLK` substitutes the steeper kreska for Polish text; under `locl CSY` or `locl SKY` it substitutes the flatter Czech acute. Fonts that get this right are disproportionately made by designers from the region — Michał Jarociński's work, TypeTogether (Veronika Burian / José Scaglione), some Rosetta Type Foundry releases.

Practical consequence: in pure English-world testing, you might not notice whether Polish acute is drawn as the Polish kreska or as an English-default acute. Polish readers notice immediately.

```html
<p lang="pl">Łódź miasto — ściana</p>
<p lang="cs">Říká se mu Ostrava — hvězda</p>
```

### Romanian comma below

Romanian `ș`, `ț` (`ş`, `ţ` in older encodings) use a **comma-below**, not a cedilla. The distinction:

- **Comma-below**: a free-floating comma shape suspended below the baseline (`ș`, `ț`, U+0219, U+021B)
- **Cedilla**: a hook-shape *attached* to the letter (`ş`, `ţ`, U+015F, U+0163)

Pre-Unicode 3.0 (and in many legacy encodings), Romanian was set with cedilla because that was the available glyph — even though typographically the comma-below is correct. Windows-1250, ISO 8859-2, and older Unicode versions mapped Romanian to cedilla forms, which means a huge corpus of Romanian text on the web uses the wrong code points.

Modern Romanian fonts with `locl ROM` substitute the cedilla-encoded glyph (`ş`, `ţ`) with the comma-below form, so legacy content still renders correctly. Newer content should use `ș`, `ț` directly. Either way, the font needs both forms.

```html
<p lang="ro">Iași — începe — România</p>
```

### Bulgarian Cyrillic (cross-script note)

Bulgarian uses distinctive Cyrillic forms — the lowercase `в`, `г`, `д`, `п`, `т`, `ш`, `щ` have specifically Bulgarian shapes that differ from Russian defaults. This is not a Latin concern but worth noting for pan-European work: a site targeting EU audiences including Bulgaria needs `locl BGR` on its Cyrillic font. See `./cyrillic.md` for Cyrillic-side treatment.

### Icelandic accents

Icelandic `á`, `é`, `í`, `ó`, `ú`, `ý` use slightly different acute positioning than Continental forms. `locl ISL` tunes this. Minor visually — but Icelandic editorial houses will notice and care.

### Serbian / Macedonian Cyrillic italic locl

Again cross-script; Serbian italic `б`, `г`, `д`, `п`, `т` differ from Russian italic forms. `locl SRB` or `locl MKD` selects.

---

## Spacing Conventions

### French: narrow non-breaking space before double-character punctuation

French typography inserts a **narrow non-breaking space** (U+202F) before `?`, `!`, `:`, `;` — and inside guillemets:

```
Français : «\u202FBonjour\u202F» — est-ce vrai\u202F?
```

vs.

```
English: "Hello" — is it true?
```

The narrow non-breaking space prevents line-break before the punctuation *and* provides visible separation. A regular non-breaking space (U+00A0) is too wide; a regular space breaks lines. Only U+202F is both narrow and non-breaking.

Browsers on `lang="fr"` *should* insert this automatically via locale rules, but in practice most don't. Content pipelines for French sites typically run a post-processor that converts `? `, `! `, `: `, `; ` into `\u202F?`, `\u202F!`, `\u202F:`, `\u202F;` and `\u00AB `, ` \u00BB` into `\u00AB\u202F`, `\u202F\u00BB`.

### Spanish: inverted punctuation at clause start

`¿` (U+00BF) opens interrogatives; `¡` (U+00A1) opens exclamations. Paired with `?` / `!` at the end:

```
¿Cómo estás?
¡Hola!
Dijo: «¿Qué pasa?» — y se fue.
```

This is scoped to the *clause*, not the sentence. `Si vienes mañana, ¿vamos al cine?` — only the interrogative clause gets the inverted question mark. Spanish content pipelines don't usually need to auto-insert these; content authors write them. UI needs to ensure `¿` and `¡` are present on the keyboard and render.

### Modern: one space after a period

Two spaces after a period is a **monospace-typewriter** convention — on a typewriter, every character has the same width, and a period has as much whitespace around it as any other character, so a double-space was needed to signal sentence-end. On variable-width type, periods already have widened spacing built into the font's metrics; a second space creates excessive gap.

Pandoc, Chicago Manual of Style (since the 16th edition), APA, MLA, and every contemporary style guide: **one space**. AP Style: one space. Government style guides (US Government Printing Office): one space. The only remaining holdouts are some legal-office conventions and personal habit.

If your content comes from a source that inserts double-spaces, collapse them in preprocessing. If your content comes from legal boilerplate and you have no authority to change it, let it render — in variable-width type the extra space is barely visible and signals nothing that matters.

### Word-spacing and letter-spacing

Default word-spacing (`word-spacing: 0` in CSS) uses the space-glyph from the font — a specifically tuned width for that typeface. Don't adjust unless you have a reason; the font designer tuned the space for the surrounding glyphs' optical rhythm.

**Letter-spacing for all-caps**: always add positive letter-spacing (tracking) to all-caps text. The glyphs are drawn with spacing tuned for mixed-case; setting them in all-caps with no tracking yields a cramped rendering. Conventional: `text-transform: uppercase; letter-spacing: 0.05em;` for UI labels.

**Letter-spacing for small caps**: similar — positive tracking helps small caps breathe.

**Letter-spacing for lowercase body text**: leave at `0`. Type designers draw lowercase sidebearings for no extra tracking. Positive tracking on body text is an amateur signal; negative tracking on text is a cramp.

---

## Quality Indicators — Does This Font Support Pan-European Latin?

When evaluating a font's claim of Latin / Latin Extended / European support:

1. **Does it include Latin Extended-A?** Type a string like `Polish: łódź żółć ściana — Czech: řeka hvězda sůva — Hungarian: tőtől útig — Romanian: Iași începe`. If any glyph shows as `.notdef` (a box, or replacement glyph), the font doesn't cover that range.

2. **Is Vietnamese present and correctly stacked?** Type `Ứng dụng mạnh mẽ hỗ trợ ngôn ngữ Việt Nam`. Check that the tone + quality marks stack cleanly on each vowel — no collision between the circumflex and the tone mark above it, no collision with preceding letters' ascenders.

3. **Are the diacritics placed optically?** Put `í` next to `l` (as in `íl`): the acute of `í` should not clip into the stem of the preceding `l`. Put `ÁRBOL` in all-caps: the acute of the cap-A should sit above the cap-line without ballooning the line-box. If accents collide or if the acute looks like a pencil mark stuck on, the font's diacritic positioning is amateur.

4. **Is the capital sharp s `ẞ` (U+1E9E) present?** As of 2017, German officially uses `ẞ` as the capital form of `ß`. Pre-2017 fonts lack it and substitute `SS`. Modern fonts claiming German support include `ẞ`.

5. **Are `locl` features present for the languages you need?** Open the font in a tool like Wakamaifondue (<https://wakamaifondue.com>) or FontDrop, check the GSUB feature table. For each `locl NLD`, `locl TRK`, `locl ROM`, `locl CAT`, `locl PLK` you want support for, look for the lookup. Absence ≠ bad font, but it does mean you won't get language-specific rendering on `lang="xx"`.

6. **Are tabular figures present and correctly spaced?** Type `12345\n67890\n99999` in a tabular-nums setting. Each column of digits should align perfectly. If tabular-nums isn't available (no `tnum` in GPOS), the font is text-only — not data-ready.

7. **Are there small-cap glyphs (`smcp`) or are they synthesized?** Set a paragraph in small-caps, compare the SC stem weight to the surrounding lowercase stem weight. If the SC runs lighter (or appears anemic), the font lacks true SCs.

8. **Are old-style figures available?** Set `font-variant-numeric: oldstyle-nums`; if nothing changes, the font has no old-style set — body text will look overly busy at x-height with lining digits.

9. **Are currency symbols covered?** `€ £ ¥ ¢ ₹ ₽ ₩` at minimum. If you need to render crypto, `₿`. If any are missing, the browser substitutes a fallback font for just that glyph, which visibly breaks.

10. **Typographic punctuation vs ASCII.** Confirm the curly quotes, the em-dash, the en-dash, the ellipsis, the guillemets all render from the same family — not from a Windows fallback.

A font that fails two or more of these is adequate for English and little else. A font that passes all ten is rare and is typically either a professional foundry release with decades of investment (Arno, Minion, TheSans, FF Meta, Adelle) or a well-curated open-source release with a dedicated community (Inter, IBM Plex, Source Sans 3, Noto, Public Sans).

---

## Anti-patterns

1. **Shipping ASCII-only and calling it "Latin support."** English is a subset of Latin. "Supports Latin" to a Polish, Vietnamese, or Romanian user means "supports my alphabet." Verify before claiming.

2. **Mixing straight and curly quotes in the same document.** `"A straight" 'in curly'` — this happens when content comes from multiple sources and no preprocessing normalizes. Run all content through a smartypants-style processor and commit to one style.

3. **Two spaces after a period.** Kill it in preprocessing. The typewriter is over.

4. **Using a hyphen where you need an em-dash.** `she said - no`. If you see this in a design mockup, it's a content error, not a typographic choice. Convert `--` to em-dash in Markdown pipelines.

5. **Setting all-caps with no tracking.** `CONTACT US` set in a standard sans with 0 letter-spacing looks cramped — the glyph sidebearings are designed for mixed-case. Always add 0.03–0.08em tracking on all-caps.

6. **Using `font-feature-settings` instead of `font-variant-numeric`.** `font-feature-settings: "tnum" 1` *resets all other features*. Use `font-variant-numeric: tabular-nums` which composes. The same for `font-variant-caps`. See `../contemporary/opentype-features.md`.

7. **Forcing tabular figures in prose.** `1` with extra whitespace on either side looks pedantic in running text. Tabular belongs in tables and counters; proportional belongs in prose.

8. **Fake small-caps for editorial emphasis.** If `font-variant: small-caps` synthesizes because the font has no `smcp`, the SC run looks lighter than the surrounding body. Switch fonts or use a different emphasis treatment.

9. **Omitting `lang` attributes.** A Dutch site without `lang="nl"` gets English-default `ij` rendering. A Turkish site without `lang="tr"` gets English-default `i` case-mapping. A French site without `lang="fr"` gets English quotation rendering and no auto-narrow-space. The `lang` attribute is not optional for multilingual sites; set it on `<html>` at minimum and override per-element where content language differs.

10. **Stacking Vietnamese marks via CSS transforms.** If your font doesn't ship precomposed Vietnamese, some developers try to build them with CSS transforms layering diacritic glyphs. Don't. Use a font that ships Vietnamese precomposed (Inter, Plex, Source Sans, Noto, Roboto). Layered CSS diacritics break at every zoom level, every screen-reader reading, every print rendering.

11. **Using cedilla-encoded Romanian when you have comma-below available.** Pre-Unicode-3.0 Romanian set `ş`, `ţ` because that's what was in the encoding. Modern Romanian is `ș`, `ț`. Content pipelines should normalize new text to comma-below; legacy content can stay as-is if the font has `locl ROM` to substitute.

12. **Mistaking oblique for italic and specifying `font-style: italic` in editorial prose with a font that has only oblique.** The emphasis signal reads weaker. Pick a family with a true italic if italic emphasis matters.

13. **Ignoring `opsz` optical sizing for display Latin.** Faces like Source Serif 4, Recursive, Roboto Flex, Helvetica Now carry an `opsz` axis. At display sizes, `opsz` thins the stems and tightens spacing. Not wiring it means you're using the text-optimized master for a 72px headline — which looks clunky. See `../contemporary/variable-fonts.md`.

14. **Not including German `ẞ` capital sharp-s.** A page with `STRASSE` in all-caps is pre-2017 German. Post-2017 spelling is `STRAẞE`. Fonts shipping pre-2017 look dated.

15. **Claiming Latin Extended coverage without testing with native-language content.** Run a multilingual sample through the font. If your team doesn't read Polish, ask a Polish reader. If you don't test, you don't know.

---

## Sources

- Bringhurst, Robert. *The Elements of Typographic Style* (4th ed.) — ch. 3 (Harmony and Counterpoint) on italics; ch. 2 (Rhythm and Proportion) on x-height and numeral styles; ch. 5 on small caps
- Highsmith, Cyrus. *Inside Paragraphs* — on text rhythm and what x-height does to reading
- Lupton, Ellen. *Thinking with Type* (2nd ed.) — anatomy primer with excellent section on numeral styles and small caps
- Hochuli, Jost. *Detail in Typography* — micro-typographic treatment, especially spacing around punctuation
- Kupferschmid, Indra — writings on type.today and kupferschrift.de on multilingual type and `locl`
- Hardwig, Florian — *Fonts In Use* editorials on European typography
- Microsoft Typography — OpenType feature registry, `locl` documentation
- Unicode Consortium — Latin Extended-A / B / Additional charts (primary sources linked above)
- W3C Internationalization — `lang` attribute and locale-driven rendering
- MDN — `font-variant-numeric`, `font-variant-caps`, `font-variant-alternates`
- Inter specimen (rsms.me/inter) — reference for pan-European sans coverage
- IBM Plex project and Source Sans / Source Serif 3 — reference for open-source faces with deep Latin
