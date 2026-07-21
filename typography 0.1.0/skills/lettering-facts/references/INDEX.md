# lettering-facts — Reference Index

This index is the manifest for the `references/` tree. It is authoritative: every file listed here is either present (✅) or planned (⬜). If you add a file, add it here first. If you remove a file, update this index and note it in the top-level CHANGELOG.

**Conventions:**
- Every reference file opens with a metadata block: date (`YYYY-MM-DD`), coverage tier (deep / medium / light / stub), peer references, and primary sources.
- Claims that depend on spec or browser support state must carry a date inline.
- Subjective or contested material is framed as "camp A vs camp B", not as fact.
- Cross-references cite paths relative to `references/` (e.g., `metrics/anatomy.md`).

---

## Status Legend

- ✅ — present, reviewed, current
- 🟡 — present but needs update or review
- ⬜ — planned, not yet authored
- ❌ — removed (with note in CHANGELOG)

**Coverage tiers:**
- **deep** — canonical, exhaustive; quote freely
- **medium** — solid practical coverage; edge cases may need external lookup
- **light** — entry-level orientation; always cite that more exists elsewhere
- **stub** — names exist, points to authoritative external source

---

## contemporary/ — Modern type technology and CSS surface

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `contemporary/css-text-properties.md` | deep | Modern CSS text surface with dated browser support: `text-wrap` (pretty/balance), `text-box` / `text-box-trim` / `text-box-edge`, `leading-trim` (deprecated name), `initial-letter`, `hanging-punctuation`, `text-spacing-trim`, `word-break: auto-phrase`, `hyphens`, `font-size-adjust`, `font-synthesis-*`, `letter-spacing` vs `word-spacing` vs `text-spacing`. |
| ✅ | `contemporary/variable-fonts.md` | deep | Registered axes (wght/wdth/ital/slnt/opsz); custom axes; interpolation semantics; `font-variation-settings` vs high-level properties; HVAR/MVAR/gvar tables; axis naming conventions; when `slnt` is not a substitute for `ital`. |
| ✅ | `contemporary/opentype-features.md` | deep | Feature tag catalog: liga, dlig, hlig, kern, onum, lnum, pnum, tnum, frac, sups, subs, ss01–20, cv01–99, locl, cpsp, swsh, calt, salt, titl, nalt, c2sc, smcp. CSS mapping via `font-feature-settings` and `font-variant-*`. When each matters. |
| ✅ | `contemporary/font-delivery.md` | deep | Formats (SFNT, CFF, CFF2, TrueType, OpenType, WOFF, WOFF2); subsetting; `unicode-range` split strategies; `font-display` (swap/fallback/optional/block/auto) tradeoffs; `<link rel="preload">` for critical fonts; FOIT/FOUT/FOFT behaviors by strategy. |
| ✅ | `contemporary/metric-overrides.md` | medium | `@font-face` overrides: `ascent-override`, `descent-override`, `line-gap-override`, `size-adjust`. How to compute from target+fallback metrics. Relationship to `font-size-adjust`. |
| ✅ | `contemporary/color-fonts.md` | medium | Four formats (COLRv0 universal, COLRv1 Chromium/Firefox/Edge shipped 2022 — Safari not shipped through 26.5 per caniuse, sbix Apple-ecosystem, CBDT/CBLC legacy, SVG-in-OT dead); ship COLRv1 + COLRv0 fallback for Safari coverage; Apple Color Emoji uses sbix; animation via `font-variation-settings` on COLRv1 variable fonts; accessibility + tooling (Glyphs 3, FontLab 8, FontTools). |
| ✅ | `contemporary/font-palette.md` | light | `font-palette: normal \| light \| dark \| <custom>`; `@font-palette-values` at-rule with `base-palette` + `override-colors`; Baseline 2022 (Chromium 101, Safari 15.4, Firefox 107); discrete palette transitions (not interpolatable); `prefers-color-scheme` recipe; `currentColor` trick for tintable monochrome; no-op on sbix (Apple Color Emoji) and on COLRv1 in Safari (engine lacks COLRv1 rendering through 26.5). |
| ✅ | `contemporary/hinting-and-rendering.md` | deep | Rendering pipeline (HarfBuzz + rasterizers); TrueType/PostScript/unhinted hinting models; ttfautohint + AFDKO autohinters; OS-specific rendering (DirectWrite, CoreText, FreeType, Skia); ClearType and sub-pixel AA (removed from macOS 10.14); `-webkit-font-smoothing` + `font-smooth` controls; variable-font hinting; `text-rendering`; cross-platform gotchas and practical recommendations. |
| ✅ | `contemporary/custom-highlights-api.md` | medium | `Highlight` registry + `::highlight()` pseudo-element. Use cases: search highlighting, spell-check, annotations, collaborative-editing presence cursors. Comparison vs `::selection` and `<mark>`. Search-highlight implementation pattern. |
| ✅ | `contemporary/interop-2026-text.md` | light | Interop 2026 typography-relevant picks: Custom Highlights API, `attr()` typed function, `contrast-color()`, plus the carryover watchlist (text-box-trim Firefox unshipped per Bugzilla 1816038, COLRv1 Safari unshipped per WebKit standards-positions #415). |

---

## historical/ — Eras and technology waves

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `historical/blackletter.md` | medium | Textura/Rotunda/Schwabacher/Fraktur four-way sub-tradition; Gutenberg 1455 B42 used ~290 sorts + 83 ligatures + 92 manuscript abbreviations; Kurrent (German cursive) and Sütterlin (Ludwig Sütterlin 1911, schools 1915–1941) branches; 1941 Normalschrifterlass banned Fraktur via fabricated "Schwabacher Judenlettern" claim (real motive: occupation-territory communication); Mathematical Fraktur Unicode U+1D504+ accessibility anti-pattern for decorative German; long-s (`ſ`) rules via `calt` with ZWNJ for compound words; capital ß (U+1E9E) officially adopted 2017. |
| ✅ | `historical/humanist-renaissance.md` | deep | Jenson 1470 Venice roman; Aldus Manutius + Griffo 1495 Bembo + 1501 first italic; Claude Garamond 1540s Paris; the Garamond/Jannon 1621 confusion untangled (Beatrice Warde 1926); authentic-source digitals (Stempel, Sabon, Adobe Garamond, Garamond Premier) vs Jannon-line revivals (Monotype, ATF, ITC, Simoncini); low contrast + oblique axis + bracketed serifs + small x-height (0.38–0.48 em) make Renaissance revivals metric-incompatible with contemporary UI defaults without `size-adjust`. |
| ✅ | `historical/transitional.md` | medium | Romain du Roi (Grandjean 1702, Académie Bignon grid design) → Fournier (1764/68 *Manuel Typographique* + Fournier point ~0.345mm) → Baskerville (1757 Virgil, hot-pressed paper, Whatman wove); Caslon Old Face = Garalde boundary case; Times New Roman (Morison + Lardent 1932, Plantin + Baskerville sources); Mrs Eaves (Licko/Emigre 1996, x-height ~0.37em) named for Sarah Eaves, Baskerville's housekeeper-wife; canonical contemporary revivals (Miller, Lyon, Tiempos). |
| ✅ | `historical/modern.md` | medium | Firmin Didot + Bodoni + Walbaum; Didot point established 1783 by François-Ambroise Didot (not Pierre-Louis); stroke contrast 1:10+ (vs transitional 1:4–6); HTF Didot (Hoefler 1992, 7 opsz cuts 6/11/16/24/42/64/96) commissioned for Harper's Bazaar; ITC Bodoni 6/12/72 released 1994 ATypI SF (Stone/Goldsmith/Parkinson/Fishman/Strizver/Haley); fashion+luxury branding canon (Vogue, Harper's, Tiffany, Armani); hairline fragility on low-DPI + body-text anti-pattern without opsz text cut. |
| ✅ | `historical/slab-egyptian.md` | medium | Figgins/Thorne/Thorowgood 1815–1820 "Egyptian" display slabs; Clarendon (Besley/Fann Street 1845, Register of Designs); Ionic No. 5 (Griffith/Linotype 1925 for newspapers); Courier (Howard Kettler IBM Selectric 1961) monospace slab; Memphis (Rudolf Wolf, not Weiss, Stempel 1929); Rockwell (Monotype 1934); humanist text slabs PMN Caecilia (Noordzij KABK 1990), Arnhem (Smeijers 1998), Sentinel (H&FJ 2009); NPS Clarendon nuanced (pre-2000 standard, replaced by NPS Rawlinson Roadway); Clarendon: Mécanes in Vox. |
| ✅ | `historical/sans-grotesque.md` | medium | Caslon IV 1816 "Two Lines English Egyptian" as first modern sans (caps-only display); 19th-c. Figgins/Thorne/Thorowgood grotesques; Akzidenz-Grotesk 1898 Berthold lineage → Helvetica 1957 (Miedinger/Hoffmann Haas, same design as Neue Haas Grotesk); Univers 1957 Frutiger systematic family; Futura 1927 + Erbar 1922 geometric Bauhaus; Gill Sans 1928 humanist (Eric Gill reputation flagged); FF Meta 1991 Spiekermann humanist; 21st-c. humanist revival (San Francisco 2015, Inter 2016+, Söhne 2019, Geist 2023). |
| ✅ | `historical/humanist-sans.md` | medium | Edward Johnston 1916 London Underground + Eric Gill 1928 Gill Sans (Gill reputation flagged per MacCarthy 1989); Optima (Zapf 1958, Incise/Humanist classification contested); Frutiger (1975 Roissy CDG, 1976 Linotype); FF Meta (Spiekermann 1991 orig Bundespost); ClearType humanist sans commissioned 2001–2004 (Calibri/Candara/Corbel/Cambria/Consolas/Constantia); Calibri shipped Word 2007 default, Aptos (Matteson 2023) replaced it; 21st-c. screen-first (San Francisco 2015, Inter 2016+ with opsz 2023, Source Sans 2012, IBM Plex 2017, Söhne 2019, Geist 2023); aperture ratio 0.45–0.60 metric for humanist vs 0.25–0.35 neo-grotesque. |
| ✅ | `historical/geometric-sans.md` | medium | Bauhaus + Herbert Bayer's 1925 Universal experiment; Paul Renner + Futura (1927 Bauer; Renner anti-Nazi, Gestapo-arrested 1933; NASA Apollo 11 plaque 1969); Erbar 1922 (predates Futura); Rudolf Koch + Kabel 1927; Avant Garde (Lubalin/Carnase ITC 1970); Avenir (Frutiger 1988); Gotham (Frere-Jones H&Co 2000, Obama 2008 adoption mid-campaign after Slabyk/Thomas hire); Circular (Brunner/Lineto 2013 Spotify); Montserrat (Ulanovsky 2011, 2017 Le Bailly redesign); Geist (Vercel 2023); perfect-circle letter-similarity tires body readers — display-preferred. |
| ✅ | `historical/neo-grotesque.md` | medium | Akzidenz-Grotesk 1898 foundation; Helvetica (Miedinger/Hoffmann Haas 1957, renamed from Neue Haas Grotesk for Linotype 1960) vs Univers (Frutiger 1957 systematic 21-weight family prefigured variable fonts); Arial (Nicholas/Saunders Monotype 1982 Helvetica-compatible metrics for Windows 3.1 1992); NYC subway "Helvetica legend" nuanced (Paul Shaw 2011: many stations used Standard Medium/Akzidenz for decades); Söhne (Sowersby/KLIM 2019 Akzidenz halbfett 36pt source); Helvetica Now 2019 three opsz; 21st-c. revivals (Neue Haas Grotesk 2010, GT America 2016, ABC Diatype, Söhne). |
| ✅ | `historical/phototype-era.md` | light | Phototype 1949 Intertype Fotosetter → dominant 1960s–1980s → displaced by PostScript 1984; single-master scaling lost metal's size-specific refinements; tight-tracking aesthetic (Lubalin/Avant Garde); Letraset 1959 rub-on; ITC (1970) licensing dominated — ITC Garamond (Tony Stan 1977) widely regarded as poor revival; metric unreliability of phototype-era ITC digitizations persists into 2020s; why contemporary authentic revivals explicitly skip this era. |
| ✅ | `historical/desktop-publishing.md` | light | PostScript (Adobe 1984) + Macintosh 1984 + PageMaker 1985 + LaserWriter 1985; TrueType (Apple+MS 1991) as PostScript alternative; OpenType (1996 spec, 2001 OT 1.4); Emigre (Licko/VanderLans 1984) first Mac-native foundry; FontShop (Spiekermann 1989, acquired Monotype 2014); Hoefler&Co 1989; Core Fonts for Web (Verdana+Georgia+Comic Sans, Carter+Connare, 1996); Adobe Originals (Slimbach+Twombly 1989–2010); typesetting profession collapse (~15K NYC typesetters to embedded-in-apps). |
| ✅ | `historical/variable-era.md` | medium | OpenType 1.8 standardized 2016-09-14 ATypI Warsaw (Apple/MS/Google/Adobe joint announcement); pre-history via Multiple Masters (1991–98) + TrueType GX; browser ship Chrome 62 (Oct 2017), Safari 11.1 (Mar 2018), Firefox 62 (Sept 2018); first-gen releases Decovar/Amstelvar/Roboto Flex/Recursive/Inter; IFT W3C Candidate Recommendation Draft 2025-11-18; COLRv1 Safari still unshipped 2026-04; open-source variable-first policy (Google Fonts 2022+, IBM Plex 2017+); 21st-c. foundry roster (Klim, Commercial Type, Grilli Type, Dinamo, Pangram Pangram, Displaay, Production Type, Sharp, OH no). |

---

## scripts/ — Per-script typographic norms

> **Depth tiers are declared up-front.** Latin is deep; Cyrillic, Greek, Arabic, Hebrew, Devanagari, Thai, CJK, Japanese are medium; Hangul is light; Ethiopic is a stub pointing to external sources. Do not pretend equal coverage.

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `scripts/latin.md` | deep | Cap/small-cap/lowercase proportions, italic traditions, x-height norms, numeral styles, punctuation, OpenType `locl` for national variants (Dutch IJ, Turkish i, Catalan ŀl). |
| ✅ | `scripts/cyrillic.md` | medium | Glagolitic → Cyrillic origin + Peter the Great's 1708 civil type reform; letter inventories (Russian, Ukrainian, Belarusian, Bulgarian, Serbian/Macedonian, non-Slavic); Bulgarian lowercase `locl BGR` and Serbian/Macedonian italic `locl SRB`/`MKD`; italic divergence from upright; weight/spacing darker-than-Latin phenomenon; Russian quotation (`«»`, `„"`) and em-dash-with-spaces conventions; font canon (PT Sans, Fira Sans, Source Sans 3, Noto, Inter, Kyiv Type Foundry, Fontfabric, Typonine); Ukrainian post-2022 type sovereignty. |
| ✅ | `scripts/greek.md` | medium | Monotonic vs polytonic orthography (1982 Pres. Decree 297/1982); final sigma σ/ς as Unicode codepoint distinction not `fina`; Byzantine minuscule origins of lowercase; Greek italic redrawn α/γ/ζ/κ/λ (not slanted); Greek Question Mark U+037E ↔ U+003B equivalence + ano teleia U+0387 as semicolon-function; polytonic `ccmp`+`mark`+`mkmk` GPOS requirements; font canon (GFS, Noto, Brill, SBL, Gentium). |
| ✅ | `scripts/arabic.md` | medium | Four contextual forms (isolated, initial, medial, final), nastaliq vs naskh vs kufi, connecting-script rules, vertical ligatures, kashida, RTL bidirectional nesting. |
| ✅ | `scripts/hebrew.md` | medium | Ashuri square script + Rashi/STAM scoped; unicameral consequences (no ALL CAPS, no small-caps); nikud + cantillation line-height demand; letter-disambiguation traps (ב/כ, ה/ח, ד/ר, ו/ז/נ, ם/ס); Hebrew numerals + geresh/gershayim/maqaf; no-native-italic debate + Typotheque secondary-style approach; bilingual Latin+Hebrew metric-harmony recipes (Heebo, Rubik, IBM Plex Hebrew, Noto Hebrew with `size-adjust`); cross-refs `scripts/arabic.md` for shared bidi. |
| ✅ | `scripts/devanagari.md` | medium | Shirorekha (head line), vowel signs (matras) above/below/left/right, conjuncts/ligatures, Hindi/Marathi/Nepali variants. |
| ✅ | `scripts/thai.md` | medium | Brahmi-derived abugida (Ramkhamhaeng 1283 → Royal Institute today); three-level mark stack (base + upper vowel + tone); no word spaces (line-break via ICU dictionary + UAX #14); Loop (หัว/traditional) vs Loopless (modern/display) style split; line-height ≥ 1.6 mandatory to avoid mark clipping (#1 Thai web-type bug); `letter-spacing` destroys mark-to-base binding; unicameral (no `text-transform: uppercase` effect); canonical fonts (Noto Sans/Serif Thai, Sarabun, IBM Plex Sans Thai, Cadson Demak foundry). |
| ✅ | `scripts/cjk-han.md` | medium | Simplified vs Traditional (PRC vs Taiwan vs Hong Kong), five stroke classes, full-width vs proportional punctuation, vertical text (`writing-mode`). |
| ✅ | `scripts/japanese.md` | medium | Kanji + hiragana + katakana + romaji mixing, ruby (furigana), tategaki (vertical), common font families (Noto Sans CJK JP, Hiragino, Yu Gothic). |
| ✅ | `scripts/hangul.md` | light | King Sejong 1443/1446 documented invention; 19+21 jamo compose into ~11,172 pre-composed syllable blocks (Unicode U+AC00–U+D7A3); 2D block layout with position-dependent glyph variants; Myeongjo/Gothic/Graphic/Handwriting typology; Pretendard (2021+) the de-facto Korean UI default via Inter metric-matching; `letter-spacing` breaks syllable blocks; `word-break: keep-all` the standard line-break recipe; unicameral. |
| ✅ | `scripts/ethiopic.md` | stub | Ge'ez script overview (abugida, ~270 base characters × 7 vowel orders); Unicode blocks U+1200–U+137F + U+1380–U+139F + U+2D80–U+2DDF + U+AB00–U+AB2F; LTR no-cursive; dedicated punctuation (፡ ። ፧ ፨); font landscape (Noto Sans/Serif Ethiopic, Abyssinica SIL, Nyala, Kefa, Ebrima); `lang="am"`/`ti"`/`gez"` directive; pointers to SIL / W3C ETLReq draft / Unicode Standard Ch. 19; explicit scope disclaimer (stub tier). |

---

## techniques/ — Composition, pairing, rhythm

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `techniques/modular-scale.md` | medium | Ratio choices (1.125/1.2/1.25/1.333/1.414/1.5/1.618); when even vs musical ratios win; anchor selection. *(Computation derived inline; token realization → `token-builder` agent.)* |
| ✅ | `techniques/vertical-rhythm.md` | deep | Baseline-grid tradition (Bringhurst → Rutter → web); mathematical trap (ascent/descent ratios produce sub-pixel drift ~0.26px/line); `text-box-trim` / `text-box-edge` ship status (Safari 18.2 Dec 2024, Chrome 133 Feb 2025, Firefox unshipped 2026-04) and `text-box: trim-both cap alphabetic` shorthand; `line-height-step` deprecated; `baseline-source` inline-only; four working recipes (pre-2025 tolerance, text-box-trim + `@supports`, grid-auto-rows + subgrid, Capsize negative-margin); honest "does rhythm matter" per Rayner/Dyson — no controlled comprehension evidence. |
| ✅ | `techniques/measure.md` | deep | CPL (characters per line) norms: 45–75 body, 35–50 column-narrow, exceptions (caption, UI chrome, poetry). `ch` vs `em` approximations. Crowding research-survey link. |
| ✅ | `techniques/pairing.md` | deep | Contrast school vs harmony school. Heuristics: x-height match, weight-ladder parity, width parity, optical-size alignment, and contrast intensity as a signal of perceived intentionality (weight-axis span, classification-distance span; cross-refs `../voice/`). Historical pairings (Garamond + Helvetica; FF Din + FF Dax). |
| ✅ | `techniques/optical-size.md` | deep | Punchcutting → Multiple Master (1991–99) → OpenType `size` (2000) → variable `opsz` (2016); CSS precedence trap (`font-variation-settings` without `"opsz"` drops opsz to default, overrides `font-optical-sizing: auto`); inventory of opsz-equipped open-source fonts with ranges (Roboto Flex 8–144, Amstelvar 8–144, Literata 7–72, Source Serif 4 8–60, Fraunces 9–144, Inter 4.0 14–32); Firefox 120 bug-fix Nov 2023; role-based vs size-based opsz mapping; coexists orthogonally with `font-size-adjust` / `size-adjust` / `ascent-override`. |
| ✅ | `techniques/fallback-stacks.md` | deep | Metric-compatible stacks per genre. Adobe Fonts / Google Fonts overrides recipe. `system-ui` caveat. Dated table of recommended `ascent-override` / `descent-override` / `size-adjust` per popular family. |
| ✅ | `techniques/small-caps.md` | light | Real (`smcp`/`c2sc`/`pcap`/`c2pc`/`titl`/`unic` OpenType features via `font-variant-caps`) vs synthetic fallback; real-vs-fake stroke-weight test; `font-synthesis-small-caps: none` to catch font-feature gaps; editorial use (acronyms, centuries, honorifics, running heads); `letter-spacing: 0.05-0.08em` compensation recipe; Google Fonts canon with real small-caps noted. |
| ✅ | `techniques/figures.md` | medium | Four combinations (lining/old-style × tabular/proportional) with use-case mapping; `font-variant-numeric` longhands + OpenType tags (`lnum`/`onum`/`tnum`/`pnum`/`zero`/`frac`/`sups`/`subs`/`ordn`); `font-feature-settings` replace-not-merge precedence trap; Inter's slashed-zero ships as `ss02` not `zero` (CSS property is a no-op); `<time datetime>` semantic pairing for tabular timestamps. |
| ✅ | `techniques/hanging-punctuation.md` | light | `hanging-punctuation: first \| last \| allow-end \| force-end` — Safari-only since 2016 (Chromium + Firefox tickets open 10+ years, Chromium Intent-to-Prototype mid-2025); the `last` value unimplemented anywhere including Safari; manual workarounds (negative `text-indent`, sibling margin hacks, JS measuring); editorial vs UI value judgment; interaction with `text-align: justify` and `text-wrap: pretty`. |

---

## voice/ — Neutrality, distinctiveness, and typeface personality

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `voice/neutral-by-design.md` | medium | Why widely-used UI grotesques (Helvetica/Arial, Roboto, Open Sans, Lato, San Francisco, Inter) read as "neutral" by deliberate design brief, not accident — tall x-height, moderate apertures, restrained contrast, broad script coverage as a forcing function (Noto's "no more tofu" brief cited as the extreme case); cross-refs `historical/neo-grotesque.md` and `historical/humanist-sans.md` rather than re-narrating their history. When neutrality is the correct choice (dense data, accessibility-first, heavy multi-script/i18n, task-based products — Apple HIG + Material Design guidance quoted, snippet-corroborated) vs. when distinctiveness is the goal instead. |
| ✅ | `voice/distinctive-and-impactful.md` | medium | What structurally makes a typeface read as distinctive/impactful — unusual proportions, historical-revival quirks, high-contrast stroke modulation, deliberate irregularity, wide variable-axis span — grounded in verified design history for five contemporary faces (Fraunces, Bricolage Grotesque, Space Grotesk, Playfair Display, Newsreader) with sources named per claim; flags general-classification framing separately from typeface-specific verified fact. |

---

## classification/ — Named systems and where they disagree

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `classification/vox-atypi.md` | medium | Vox 1954 → ATypI 1962 → BS 2961:1967 → ATypI 2010 with Étrangères addition; all 11 buckets (Humanes/Garaldes/Réales/Didones/Mécanes/Linéales/Incises/Scriptes/Manuaires/Fractures/Étrangères); BS 2961 four-way Lineal subdivision; 14-row disagreements table (Optima, Caslon, Copperplate Gothic, Times New Roman, Fraunces, Recursive, Tiempos, Inter) showing where classification breaks. |
| ✅ | `classification/bringhurst.md` | medium | Robert Bringhurst *Elements of Typographic Style* (1992, 4th ed. 2013); historical-era taxonomy vs Vox's taxonomic sorting — Renaissance/Baroque/Neoclassical/Romantic/Realist/Geometric Modernist/Lyrical Modernist/Expressionist/Postmodern; essayistic not mutually-exclusive; Rutter 2005 webtypography.net adapted to CSS; Butterick 2010 practicaltypography.com looser web version; authority-dogmatism trap noted. |
| ✅ | `classification/din-16518.md` | light | German-industrial DIN standard issued 1964 Beuth Verlag, never substantively revised through 2026-04; 11 groups (Gruppen I–XI); most granular blackletter taxonomy anywhere (Gotisch/Rundgotisch/Schwabacher/Fraktur/Fraktur-Varianten); Gruppe VI (all sans) has no sub-classification (BS 2961's four-way Lineal split fills the gap); Gruppe XI Fremde Schriften foreshadows Vox 2010 Étrangères; cross-ref to Vox where they disagree (Baroque III straddling, Optima contested). |
| ✅ | `classification/thibaudeau.md` | stub | Francis Thibaudeau (1860–1925) *La Lettre d'Imprimerie* 1921; four categories (Elzévir/Didot/Égyptienne/Antique) by terminal silhouette ("empattement"); direct precursor to Vox 1954 (extended 4→9 categories); Thibaudeau 1921 → Vox 1954 → ATypI 1962 → BS 2961 1967 → DIN 1964 forms 15-year classification cascade; reductionist (ignores stroke contrast, axis, proportion) and superseded by Vox. |

---

## science/ — Reading research-survey

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `science/legibility-vs-readability.md` | medium | Two distinct concepts: letter identification (legibility) vs sustained reading comfort (readability). Rayner, Larson, Pelli citations. |
| ✅ | `science/crowding.md` | deep | Bouma 1970 critical-spacing law (~0.5 × eccentricity); Pelli programme (Pelli/Palomares/Majaj 2004, Pelli 2008); mechanisms (feature pooling V2–V4, not masking); ALL-CAPS ~13–20% slowdown (Tinker/Paap/Arditi/Fiset) explained via crowding + inter-letter similarity, not word-shape loss; dyslexia spacing interventions (Zorzi 2012 PNAS, Perea 2012) with Skottun/Skoyles hedge; non-Latin crowding coefficients (Zhang 2009: Chinese 0.23–0.37 vs Latin ~0.5); WCAG 2.2 SC 1.4.12 +0.12em as the crowding-informed accessibility floor. |
| ✅ | `science/word-shape-vs-parallel-letter.md` | deep | Cattell 1886 → Smith 1969 word-shape tradition vs Adams 1979 / McClelland & Rumelhart 1981 / Larson 2004 parallel-letter-recognition; four evidence lines (masked priming case-independence, transposition effects, VWFA neural, Pelli/Farell/Moore 2003 psychophysics); ALL-CAPS 10-20% slowdown via crowding + feature-homogeneity (not shape loss); dyslexia-font premise-failure in theory + empirics (Kuster 2018, Wery & Diliberto 2017); Latin-scope bounded (CJK holistic processing per Hsiao & Cottrell 2009, Arabic cursive, Devanagari shirorekha differ). |
| ✅ | `science/optical-size-research.md` | light | Reading-science evidence base for opsz: Beier 2012 *Reading Letters*, Bigelow 2019 JCAD, Chaparro SURL 2010, Pelli/Farell/Moore 2003 *Nature*, Larson ClearType; quantified effects (tall-x-height ~7%, text-vs-display cut at 9pt ~5–8%, aperture accuracy at 6pt order-of-magnitude); continuous axis rationale vs discrete cuts; screen-vs-print opsz considerations; companion to `techniques/optical-size.md` (which covers CSS + font-file mechanics). |

---

## accessibility/ — Type accessibility

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `accessibility/wcag-type.md` | deep | WCAG 2.2 text SCs: 1.4.4 (resize), 1.4.8 (visual presentation), 1.4.12 (text spacing), 3.1.5 (reading level). Current legal status. |
| ✅ | `accessibility/dyslexia.md` | medium | Evidence review: OpenDyslexic, Dyslexie, Lexie Readable. Meta-analyses. Honest conclusion (weak effect; individual variability; spacing matters more than forms). |
| ✅ | `accessibility/low-vision.md` | medium | WHO definition (20/70+ uncorrected), US ~7M prevalence; central-scotoma AMD is crowding-limited not acuity-limited → letter-spacing > size for AMD; APCA Lc 75/−75 as the low-vision-honest model (2.x under-penalises light-on-dark); AMD vs photophobia opposing polarity preferences; "low-vision fonts" (Atkinson Hyperlegible, Maxular Rx, Eido) evidence-thin — offer as preference not default; WCAG 1.4.3/1.4.4/1.4.8/1.4.10/1.4.12/1.4.13 SCs; user-preference media queries `prefers-contrast`/`prefers-color-scheme`/`prefers-reduced-motion`/`forced-colors`. |
| ✅ | `accessibility/cognitive.md` | light | Cognitive populations (dyslexia, ADHD, autism, TBI, aging, L2, low literacy); readability > legibility is the bottleneck; sans-serif + 1.5+ line-height + 45-60ch measure + generous paragraph spacing + consistent typography; avoid justify/ALL-CAPS/decorative/script; plain-language intersections (Plain Writing Act, GOV.UK, Hemingway/Flesch); myths debunked (Comic Sans, centered text, Dyslexie comprehension); WCAG 3.1.4/3.1.5/3.2.x cognitive-adjacent SCs. |

---

## metrics/ — Anatomy and measurement

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `metrics/anatomy.md` | deep | Stem, apex, vertex, bowl, counter, aperture, spur, ear, eye, tail, terminal, finial, crossbar, crotch, shoulder, link, loop, spine, arm, leg, tittle. Per-letter map. |
| ✅ | `metrics/metrics-glossary.md` | deep | UPM, x-height, cap height, ascender, descender, overshoot, sidebearing, advance width, kerning, tracking. How they relate. |
| ✅ | `metrics/metric-compatibility.md` | medium | Impact-ranked metrics table (x-height → cap-height → ascender/descender → advance widths → line-gap → UPM); measurement tools (Capsize, Wakamai Fondue, FontDrop, Samsa, TTX, Fontaine, fontpie, Next.js `next/font`); selection guidance per task; script-specific notes for Latin, CJK (ideographic-box / punctuation-width / baseline), Arabic (mid-letter baseline), Devanagari (shirorekha alignment), Hebrew (unicameral / nikud); Modernfontstacks.com curated OS-font stacks; Incremental Font Transfer (IFT) emerging status 2026-04. |
| ✅ | `metrics/units.md` | deep | Absolute (cm/mm/Q/in/pc/pt) + reference-px; font-relative (em/rem/ex/ch/cap/ic/lh/rlh) with Baseline dates — `cap` Baseline mid-2025 (Chromium 133, Safari 16.3, Firefox 97); `ch` trap (65ch yields 70–80 Latin CPL because `0` is wider than lowercase avg) with workarounds; viewport small/large/dynamic variants Baseline June 2025; container-query units; stepped math (`round`/`mod`/`rem`) Baseline 2024; `font-size-adjust` two-value syntax Baseline 2024; WCAG 1.4.4 / 1.4.10 zoom-compatibility implications. |

---

## foundries/ — People and foundries

| Status | File | Coverage | Purpose |
|--------|------|----------|---------|
| ✅ | `foundries/canon-designers.md` | deep | Biographical profiles from Jenson/Griffo/Garamond through Baskerville/Bodoni/Didot to Morris/Goudy/Gill/Renner/Tschichold/Zapf/Frutiger/Miedinger/Carter/Licko/Hoefler/Frere-Jones/Twombly/Slimbach/Spiekermann/Sowersby/Schwartz; Garamond/Jannon untangled per Beatrice Warde 1926 *Fleuron* V; Paul Renner flagged as anti-Nazi (Gestapo-arrested 1933 for *Kulturbolschewismus?*); Eric Gill abuse per MacCarthy 1989 + institutional moves (Penguin 2003, BBC Reith Sans 2017); Hoefler/Frere-Jones 2014 lawsuit + 2021 Monotype acquisition; under-represented designer corrective (Zapf von Hesse, Calvert, Chahine, Ross, Burian, Kare, Warde). |
| ✅ | `foundries/contemporary-foundries.md` | medium | 30+ active foundries profiled: Emigre, FontShop (Monotype 2014), Hoefler&Co (Monotype 2021), Frere-Jones Type, Commercial Type, KLIM, Grilli Type, Dinamo, Pangram Pangram, Displaay, Production Type, Colophon, Sharp Type, Swiss Typefaces, Signal, ohno, Milieu Grotesque, Mass-Driver, Latinotype, Typotheque, Underware, Dalton Maag (custom BMW/Vodafone/eBay/Airbnb), Monokrom, Playtype; custom vs retail business-model economics ($150–500 retail vs $50K–500K custom); Monotype consolidation timeline (FontShop 2014, Fontworks 2020, Hoefler 2021). |

---

## Open Questions

Open decisions carried from the research waves (history in the top-level CHANGELOG), tracked here so they are resolved on contact rather than discovered in production:

- **Which commercial fonts may be named in examples?** Default stance: name only for categorical illustration ("Helvetica as the canonical neo-grotesque"), never as recommendation without context.
- **Fallback-stack table — static doc or generated TSV?** Generated TSV (in `techniques/fallback-stacks.tsv`) is more useful but harder to keep current. Punted; revisit on demand.
- **Depth upgrade for Hangul?** Current plan is light. Revisit if a Hangul-facing project comes up.
- **Arabic script coverage — unify nastaliq/naskh/kufi in one file or split?** Current plan: one file with sub-sections. If each grows beyond 400 lines, split.
- **Science section — peer-reviewed only or include industry blogs?** Current plan: peer-reviewed for claims, industry blogs for citations of conventions.
- **Historical vs classification split.** Some files could live in either (humanist serif is both a historical era and a classification bucket). Current plan: historical has the era narrative; classification has the cross-era taxonomy. Cross-link.

---
