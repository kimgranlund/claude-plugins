---
date: 2026-04-17
coverage: deep
peers:
  - ./metrics-glossary.md
  - ../classification/bringhurst.md
  - ../classification/vox-atypi.md
  - ../historical/humanist-renaissance.md
  - ../contemporary/opentype-features.md
primary_sources:
  - https://en.wikipedia.org/wiki/Typeface_anatomy
  - https://www.fonts.com/content/learning/fontology/level-1/type-anatomy/type-anatomy-part-1
  - https://fontforge.org/docs/design-with/dwd-anatomy.html
  - https://typographica.org/on-typography/type-terms-and-anatomy/
  - https://betterwebtype.com/articles/2019/11/20/the-anatomy-of-typography/
  - https://www.typetogether.com/blog/letter-anatomy-for-type-nerds
  - https://www.myfonts.com/pages/fontscom-learning-fontology-level-1-type-anatomy
  - Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012), ch. 1–3
  - Cheng, Karen. *Designing Type* (2nd ed., Yale University Press, 2020)
  - Noordzij, Gerrit. *The Stroke: Theory of Writing* (Hyphen Press, 2005)
---

# Letterform Anatomy

A named parts catalog for Latin-script letterforms. Anatomy is what a typeface *is made of*; **metrics** (see `./metrics-glossary.md`) are what it *measures*. Every part below is both a formal feature a type designer draws and a signal a reader can decode — stroke modulation, historical era, foundry style, optical tuning. Names are stable across Bringhurst, Cheng, Noordzij, FontForge, Glyphs, and FontLab with a handful of synonyms called out inline.

This file is the master reference for **part names**. When a metric (cap-height, x-height, sidebearing, overshoot) appears in this document it is linked to `./metrics-glossary.md` where measurement and tooling live.

---

## Master Anatomy Table

Grouped by usage tier. Rows read: `term | definition | letters where visible | what it signals`.

### Basic (every Latin typeface has these)

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **stem** | Principal vertical (or dominant) stroke of a glyph | `I` `l` `h` `n` `m` `T` `B` `D` `E` `F` `H` `K` `L` `M` `N` `P` `R` | Stroke modulation: uniform (sans) vs thick/thin (serif) vs reverse-contrast (display) |
| **hairline** | Thinnest stroke in a contrasting design | `O` `Q` `C` `G` `A` diagonals, Didone minor axis | High contrast = Modern (Didone); low contrast = Humanist |
| **bowl** | Fully enclosed curved stroke of a letter | `O` `D` `P` `Q` `B` `b` `d` `p` `q` | Width ratio = proportion voice (condensed vs wide) |
| **counter** | Negative (empty) space enclosed or partially enclosed by a glyph | `o` `a` `e` `g` `d` `q` `P` `D` `B` | Open counters = text-friendly; closed = display |
| **aperture** | Opening where a counter meets the outside — the "mouth" of `c` `e` `s` `a` | `c` `e` `s` `a` `g` `n` `h` | Open aperture = legibility at small size (Frutiger, Source Sans); closed = neutral (Helvetica) |
| **crossbar** | Horizontal stroke connecting two stems or crossing a stem | `A` `H` `f` `t` `e` `E` `F` | `e` crossbar slope = humanist (slanted) vs geometric (horizontal) |
| **arm** | Horizontal or upward-diagonal stroke attached at one end only | `E` `F` `L` `T` `Y` `K` | Serif terminations on arms define Transitional vs Modern |
| **leg** | Downward-diagonal stroke attached at one end | `K` `R` `k` (lower diagonal), `Q` tail if diagonal | Leg angle differentiates `R` personalities (straight vs kicked) |
| **tail** | Descending stroke or flourish | `Q` `R` `K` `y` `j` `g` (single-story) | Q-tail is a primary fingerprint — Bodoni vs Garamond vs Futura |
| **ascender** | Part of a lowercase letter that extends above the x-line | `b` `d` `f` `h` `k` `l` `t` | Ascender height vs cap-height is a style choice (see `./metrics-glossary.md#ascender-height`) |
| **descender** | Part of a lowercase letter that extends below the baseline | `g` `j` `p` `q` `y` | Long descenders = editorial; short = UI/screen |
| **shoulder** | Curved stroke emerging from a stem | `h` `m` `n` `u` (inverted) | Humanist shoulders have a distinct "entry" arc; geometric shoulders are pure arcs |
| **terminal** | End of a stroke that has no serif | `a` `c` `e` `f` `j` `r` `s` `t` `y` | Ball, beak, teardrop, sheared — each a foundry voice |
| **spine** | Central curving stroke of `S` and `s` | `S` `s` | Backbone — angle and weight distribution are highly expressive |
| **apex** | Point where two diagonal strokes meet at the top | `A` `M` `N` | Flat / pointed / extended apex = era signal |
| **vertex** | Point where two diagonal strokes meet at the bottom | `V` `W` `M` (lower), `v` `w` | Sharpness or blunting; "crotch" denotes the interior angle |
| **crotch** | Interior angle where two strokes meet | `V` `W` `Y` `v` `w` `y` `K` | Acute crotches feel crisp; obtuse feel quieter |
| **baseline** | The invisible line on which most letters sit | All — see `./metrics-glossary.md#baseline` | Canonical zero of the coordinate system |
| **x-line** (mean line) | The invisible line at the top of most lowercase letters | `x` `n` `m` `o` `a` (non-ascending) | x-height ratio → see `./metrics-glossary.md#x-height` |

### Dot-and-mark anatomy

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **tittle** | The dot above `i` and `j` | `i` `j` (lowercase) | Round (classical) / square (geometric, Futura) / rectangular (grotesque) |
| **diacritic** | Mark added above/below/through a letter to change pronunciation | `á` `à` `â` `ã` `ä` `å` `ç` `ñ` etc. | Diacritic height conflicts with ascenders — cause of crowded leading (see `./metrics-glossary.md#leading`) |
| **umlaut / diaeresis** | Two dots above a vowel | `ä` `ö` `ü` `ë` `ï` | In tight leading, collides with line above |
| **cedilla** | Hook below `c` | `ç` `ş` `ț` | Conflicts with descender zone — see `./metrics-glossary.md#descender-depth` |
| **ogonek** | Hooked mark below a vowel | `ą` `ę` `į` `ų` | Polish, Lithuanian; frequently broken in Latin-only stacks |
| **macron** | Horizontal bar above a vowel | `ā` `ē` `ī` `ō` `ū` | Latin transliteration, Māori, Latvian, long-vowel marking |
| **caron / háček** | "V"-shaped mark above | `č` `š` `ž` `ň` `ř` | Czech, Slovak, Slovene; diacritic stacking risk over ascenders |

### Serif-specific

Structural parts that exist only on serif faces, or only matter for them.

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **serif** | Finishing stroke at the end of a main stroke | All serif-face glyphs | Bracketed / unbracketed / slab / hairline = classification pillar |
| **bracket** | Curved connection between a serif and the main stem | `H` `I` `T` `E` (serif varieties) | Bracketed serifs = Humanist/Transitional; unbracketed = Modern/Didone |
| **foot** | Serif at the base of a stem; also the base stem-serif junction | `I` `H` `M` `N` `h` `n` `m` | Foot treatment differentiates text vs display cuts |
| **beak** | Sharp, beak-shaped serif finial | `E` `F` `T` `a` `r` (arm terminal) | Named in Bringhurst; characteristic of Roman inscriptional lineage |
| **barb** | Half-serif on an arm terminal pointing upward or outward | `C` `G` `S` (sometimes) | Old-style voice — Jenson, Centaur |
| **spur** | Small projection at the junction of a stem and a curve | `G` (base of the vertical), sometimes `b` `p` `q` | Defines the "G-with-spur" — Frutiger, Myriad use spurs; Futura does not |
| **ball terminal** | Circular or teardrop terminal on a stroke | `a` `c` `f` `j` `r` `y` (ends of) | Hallmark of Bodoni, Didot, Scotch Roman; never in geometric sans |
| **teardrop terminal** | Teardrop-shaped terminal, asymmetric | `a` `c` `f` `j` `r` `y` | Humanist (Garamond, Jenson); softer than ball |
| **sheared terminal** | Diagonally-cut terminal | `e` `c` `a` (stems) | Transitional / Didone / some modern sans (Museo Sans) |
| **hook** | Curved projection at the top or end of a stroke | `f` `j` `y` `r` (arm) | Softer, humanist; absent in rationalized geometrics |
| **crook** | Curved terminal (often synonymous with hook) | same as hook | Synonym — FontLab uses "hook", Glyphs uses "crook" |
| **slab** | Rectangular serif with no bracket | Slab-serif face glyphs | Egyptian / Clarendon / Geometric-slab classifications |

### Script- and humanist-specific

Parts that only appear (or only matter) in certain classes.

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **ear** | Small stroke projecting from the bowl of a double-storey `g` | `g` (double-storey only) | Shape of ear distinguishes Garamond from Baskerville from Helvetica |
| **eye** | Enclosed counter in the upper part of a double-storey `g` | `g` (double-storey only) | Size of eye tunes legibility at small size |
| **link** (neck) | Connecting stroke between the upper and lower bowls of a double-storey `g` | `g` (double-storey only) | Thin link = Humanist; thick = slab; absent = single-storey |
| **loop** | Lower closed counter of a double-storey `g` | `g` (double-storey only) | Closed loop is canonical "text-g"; open loop is "display-g" or single-storey |
| **single-storey g** | `g` built with one bowl + a descending tail (vs double-storey) | `g` in Futura, Avenir, DIN, Century Gothic | Geometric voice; less legible at small size in body text |
| **double-storey a** | `a` with an upper arc + lower bowl (vs single-storey) | `a` in most text faces | Standard for body; single-storey `a` is a display/geometric voice (Futura, Avenir) |
| **single-storey a** | `a` built from one bowl + a small tail | `a` in Futura, VAG Rounded, handwriting scripts | Signals informal / geometric / educational |
| **swash** | Extended decorative flourish, usually on caps or italic | Italic caps `A` `M` `N` `Q`, some lowercase `y` `k` | Display / editorial / signals historical italic (Garamond Italic, Zapfino) |
| **flourish** | Ornamental extension beyond the structural stroke | Display caps, calligraphic scripts | Excess beyond function — reserved for titling and identity work |
| **finial** | Tapered or curved end of a stroke where no serif is present (often synonymous with terminal) | `a` `c` `e` `f` `r` `y` `g` (tail) | Bringhurst differentiates "finial" (curved/tapered) from "terminal" (flat/sheared); Cheng uses "terminal" as the umbrella |

### Axis, contrast, and construction

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **axis** (stress) | Imaginary line through the thinnest points of a curved stroke | `O` `o` `e` `c` `d` `p` | Vertical axis = Modern/Didone/Geometric; backslanted = Humanist (Jenson, Centaur, Garamond) |
| **stress** | Synonym for axis; direction of the contrast | same | Bringhurst and Cheng both use "axis"; many foundry catalogs say "stress" |
| **contrast** | Ratio of thick to thin stroke width | Any letter with modulation | Zero = monoline (Futura); extreme = Didone (Bodoni); moderate = Transitional (Baskerville) |
| **modulation** | The pattern by which stroke weight changes along a stroke | Throughout glyph | Synonym for contrast, used more often in calligraphic contexts (Noordzij) |
| **stroke** | A primary structural path (before being drawn as a filled outline) | All glyphs | In Noordzij's *The Stroke*, stroke precedes letterform — the entire taxonomy of writing derives from stroke mechanics |

### Decorative / display / titling

Parts that appear primarily in display, titling, or ornamental typefaces.

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **inline** | White line running inside a stroke | Engraved caps (Castellar, Smaragd) | Titling / ceremonial voice |
| **outline** | Letterform built only from its outer contour, with open interior | Display "outline" typefaces | Poster / novelty |
| **shadow** | Secondary offset stroke suggesting dimensionality | Display (Gothic shadow, chromatic fonts) | 19th-century woodtype revival |
| **ornament** (pi element) | Non-letter decorative glyph in a font | Pi fonts, ornament sets | Editorial flourishes |
| **fleuron** | Flower-shaped typographic ornament | Ornament sets, Adobe Caslon Pro, Requiem | Classical editorial |
| **ligature (decorative)** | Merged glyph for aesthetic rather than functional reason | `ct` `st` `fi` `fl` in revival faces | Historical revival voice — activate with OpenType `dlig` / `hlig` |
| **flourish stroke** | Calligraphic extension in scripts | Zapfino, Feel Script | Hand/script identity |

### Historical-only / inscriptional

Terms preserved for scholarly accuracy — rarely used in contemporary design briefs but essential when discussing classification or revivals.

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **calligraphic axis** | The angle of the pen that produced historical letterforms | All humanist serif (manifested, not drawn) | Anchor of Jenson / Griffo / Garamond axis |
| **pen angle** | Held-angle of broadnib pen in manuscript sources | Historical models for current designs | ~30° flat pen = humanist minuscule; 0° = uncial |
| **uncial** | Rounded majuscule script of late antiquity | Historical — revived in display (Rialto) | Pre-lowercase era |
| **humanist minuscule** | 15th-c. manuscript hand that became roman lowercase | Historical — conceptual parent of all roman lowercase | Source of the "normal" we take for granted |
| **carolingian minuscule** | 9th-c. script, ancestor of humanist | Historical | The grandparent lowercase |
| **trajan capital** | Inscriptional Roman majuscule proportions | Trajan Pro, Centaur caps | Classical proportion canon |
| **blackletter stroke classes** | Textura / rotunda / schwabacher / fraktur / kurrent constructions | Blackletter faces | Medieval/early-print voice |
| **majuscule / minuscule** | Capital / lowercase | Scholarly usage | Correct historical terminology before "uppercase/lowercase" entered via typecase geography |

### Italic-specific

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **true italic** | A structurally distinct cursive companion to a roman | Italic cut of a serif family, or a variant italic companion | Designed letterforms; calligraphic heritage; single-storey `a`, distinct `e` construction |
| **oblique** | Slanted roman letterforms — same skeleton, tilted | Most sans italics (Helvetica Italic is technically oblique) | Computed slant; no structural variance from roman — see `./metrics-glossary.md#slnt-vs-ital-axis` |
| **slant angle** | The angle of italic rise | Italic cuts | 8–12° is typical; the `slnt` variable-font axis exposes this |
| **entry stroke** | Lead-in stroke on humanist italic lowercase | Italic `a` `m` `n` `h` `i` | Calligraphic heritage, absent in oblique |
| **exit stroke** | Lead-out stroke | Italic lowercase endings | Paired with entry — defines italic rhythm |

### Figure-specific

Numerals carry specific anatomy beyond shared letter parts. See `../techniques/figures.md` for figure-style choices.

| Term | Definition | Where it appears | What it signals |
|------|------------|------------------|-----------------|
| **lining figures** | Digits that sit on the baseline and rise to cap-height | Default in most UI fonts | UI / modern / tabular contexts |
| **old-style figures (text figures)** | Digits with ascenders (`6` `8`) and descenders (`3` `4` `5` `7` `9`) | Editorial, body text | Blend with lowercase — body prose default in classical typography |
| **tabular figures** | All digits share the same advance width | Data tables, financial UIs | Column alignment — activate via OpenType `tnum` |
| **proportional figures** | Digits have variable width, like letters | Prose | Natural rhythm — activate via OpenType `pnum` |

---

## Cross-Letter Anatomy Fingerprints

The fingerprint letters — if you can only look at a few glyphs to identify a typeface, these are the most revealing:

| Fingerprint | What it reveals |
|-------------|-----------------|
| `a` construction | Single- vs double-storey → geometric vs humanist |
| `g` construction | Single- vs double-storey; ear/link/eye/loop shapes → the single richest-signal glyph |
| `e` crossbar | Slanted (humanist) vs horizontal (geometric) vs raised (modern); aperture size |
| `Q` tail | Length, angle, interior/exterior path — most expressive cap |
| `R` leg | Straight, curved, kicked — signature of foundry voice |
| `t` top | Flat (grotesque) vs angled (humanist) vs hooked (transitional) |
| `f` descender or no | Descending `f` = editorial / humanist; flat-footed `f` = grotesque |
| `I` serifs | Presence of serifs at all; foot vs bracket; plays with the `l` vs `I` confusion |
| `&` (ampersand) | Designers' playground; most variation of any single glyph |
| Italic `a` | Single-storey (true italic) vs double-storey (oblique) |

---

## Stroke-Modulation Axes (Noordzij)

Gerrit Noordzij's *The Stroke* (2005) systematizes all writing into two axes, which orient most anatomy:

| Axis | Continuum | Example at each pole |
|------|-----------|----------------------|
| **Translation** | Broad-nib pen held at constant angle — contrast arises from pen direction | Humanist roman (Jenson) |
| **Expansion** | Pointed pen with pressure variation — contrast arises from pressure | Modern / Didone (Bodoni) |

Most typefaces are hybrids; locating a design on these axes is the fastest way to explain its modulation.

---

## Anti-patterns and Common Confusions

### Terminal vs finial

- **Bringhurst** and **Cheng** sometimes use "finial" for the tapered/curved ends (e.g., the tapered end on Garamond's `a`) and "terminal" for the flatter or sheared ends.
- **FontLab**, **Glyphs**, and most foundry glossaries collapse them — "terminal" is the umbrella term.
- **Practitioner guidance:** use "terminal" as the umbrella; say "ball terminal" or "teardrop terminal" when you need specificity.

### Axis vs stress

- Same concept. Bringhurst and academic sources prefer "axis". Foundry marketing and informal sources prefer "stress".
- "Stress" has a secondary meaning in phototype-era discourse ("stressed" strokes) — avoid unless the audience is clear.

### Hook vs crook

- FontLab calls curved stroke ends "hooks". Glyphs calls some of these "crooks". There is no canonical difference — they are regional/tool synonyms.
- The `f` hook, `j` hook, and `r` arm hook are all "hooks" in common usage.

### Arm vs leg

- **Arm** is horizontal or upward-diagonal (`E`, `L`, `T` horizontals; `K` upper diagonal).
- **Leg** is downward-diagonal (`K` lower, `R` lower).
- The `Q` tail is a tail, not a leg.

### True italic vs oblique vs slant

- A **true italic** has a different letterform construction (single-storey `a`, distinct `e`, entry/exit strokes). Most serif italics are true italics.
- An **oblique** is a slanted roman — same skeleton, tilted. Most sans "italics" (Helvetica Italic) are oblique.
- The **`slnt` variable-font axis** expresses slanted roman; the **`ital` axis** toggles between two structurally different cuts. See `./metrics-glossary.md#slnt-vs-ital-axis`.

### Aperture vs counter

- **Counter** = the negative space inside/around a letter.
- **Aperture** = the *opening* where the counter meets the outside (the "mouth" of `c`, `e`, `a`, `s`).
- A large counter can still have a tiny aperture (closed-aperture designs like Helvetica). This distinction matters for small-size legibility.

### Serif vs slab

- A **serif** is bracketed (curved join to the stem). A **slab** is unbracketed (rectangular, crisp 90° join).
- Some classifications treat slabs as a serif sub-type; others (DIN 16518) call them a separate class ("Mécanes / Slab"). See `../classification/vox-atypi.md`.

### Majuscule/minuscule vs uppercase/lowercase

- **Majuscule / minuscule** are correct historical terms. "Upper case / lower case" come from the physical position of metal type drawers in the compositor's typecase, a 19th-c. convention.
- Use majuscule/minuscule in scholarly writing, uppercase/lowercase in UI/product copy.

---

## Cross-references

- For **measurement quantities** (UPM, x-height, cap-height, ascender, descender, sidebearing, advance width, kerning, overshoot, leading, baseline positioning) see the companion glossary: `./metrics-glossary.md`.
- For **optical corrections** (overshoot, ink traps, size-specific tuning) see `./metrics-glossary.md#overshoot` and `../techniques/optical-size.md`.
- For **classification** (how anatomy maps to era and class) see `../classification/bringhurst.md` and `../classification/vox-atypi.md`.
- For **per-letter detail** on each fingerprint letter, see `../scripts/latin.md` (planned).
- For **italic and oblique treatment**, see `./metrics-glossary.md#slnt-vs-ital-axis` and `../contemporary/variable-fonts.md`.

---

## Sources

- Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012). Canon for anatomy names and historical context.
- Cheng, Karen. *Designing Type* (2nd ed., Yale University Press, 2020). Most complete per-glyph anatomy reference.
- Noordzij, Gerrit. *The Stroke: Theory of Writing* (Hyphen Press, 2005). Translation/expansion axes.
- FontForge docs — anatomy section (https://fontforge.org/docs/design-with/dwd-anatomy.html, accessed 2026-04-17).
- Fonts.com / Monotype Fontology — Type Anatomy Part 1 (https://www.fonts.com/content/learning/fontology/level-1/type-anatomy/type-anatomy-part-1, accessed 2026-04-17).
- Typographica — "Type Terms and Anatomy" (https://typographica.org/on-typography/type-terms-and-anatomy/, accessed 2026-04-17).
- Better Web Type — "The Anatomy of Typography" (https://betterwebtype.com/articles/2019/11/20/the-anatomy-of-typography/, accessed 2026-04-17).
- TypeTogether — "Letter Anatomy for Type Nerds" (https://www.typetogether.com/blog/letter-anatomy-for-type-nerds, accessed 2026-04-17).
- Wikipedia — Typeface Anatomy (https://en.wikipedia.org/wiki/Typeface_anatomy, accessed 2026-04-17).
