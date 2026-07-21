# Changelog

## 1.2.0 — 2026-07-05 — Voice Axis: Neutral vs. Distinctive Typeface Personality

### Added (2 new files)

- **`references/voice/neutral-by-design.md`** (medium) — why widely-used UI grotesques
  (Helvetica/Arial, Roboto, Open Sans, Lato, San Francisco, Inter) read as neutral by deliberate
  design brief, not accident; when neutrality is the correct choice vs. when distinctiveness is.
- **`references/voice/distinctive-and-impactful.md`** (medium) — what structurally makes a
  typeface read as distinctive/impactful, grounded in verified design history for five
  contemporary faces (Fraunces, Bricolage Grotesque, Space Grotesk, Playfair Display, Newsreader).

### Changed

- **`references/techniques/pairing.md`** — extended (not duplicated) with a "Contrast Intensity
  and Perceived Intentionality" subsection; 3 new primary_sources, each dated per-entry.
- **`SKILL.md`** — new consult-table row for `references/voice/`; identity line corrected
  (61→63 files, nine→ten axes, ~29k→~30k lines); Boundaries' stale "no type-scale generator is
  installed" dead-end replaced with a real route to the new sibling skill `typography-tokens`;
  description re-triggered ("why does this font look boring / generic") and its type-scale/tokens
  NOT-for fence corrected to point at `typography-tokens`.
- **`references/INDEX.md`** — new `voice/` manifest section; corrected a pre-existing pairing-name
  error (FF Din + Freight → FF Din + FF Dax, matching `pairing.md`'s own text).

### Note on name history

The `## 1.1.1` entry below claims a rename to `ref-typography` — that name did not stick; this
skill's current, correct name is `typography-lettering` (from the 2026-07-01 corpus-wide naming
sweep). The intermediate rename is not reconstructed here; flagged rather than left to mislead.

## 1.1.1 — 2026-05-07 — Improved Naming Convention

- Renamed from `expert-typography` to `ref-typography` per the ref- domain/verb convention.
- All cross-references updated.

## 0.2.0 — 2026-05-07 — Naming Convention Rename

- Renamed from `typography-expert` to `expert-typography` per the `expert-` domain/phase convention.
- All cross-references in downstream/upstream skills updated.

## [1.1.0] — 2026-04-26 — Refresh: Interop 2026 + Custom Highlights API

### Added (2 new files)

- **`references/contemporary/interop-2026-text.md`** (light) — Interop 2026 typography-relevant picks: Custom Highlights API, `attr()` typed function, `contrast-color()`, plus the carryover watchlist (text-box-trim Firefox unshipped per Bugzilla 1816038, COLRv1 Safari unshipped per WebKit standards-positions #415).
- **`references/contemporary/custom-highlights-api.md`** (medium) — `Highlight` registry + `::highlight()` pseudo-element. Use cases: search highlighting, spell-check, annotations, collaborative-editing presence cursors. Comparison vs `::selection` and `<mark>`. Search-highlight implementation pattern.

### Fixed

- **`SKILL.md` Status block bug.** Was still labeling itself "v0.1.0 skeleton, reference files planned but not yet authored" despite the skill having shipped v1.0.0 with all 59 reference files. Now reads "v1.0.0 (2026-04-18). All 59 planned reference files shipped."

### Verified-current (Apr 2026, no changes needed)

Browser-support claims spot-checked against caniuse:
- `text-wrap: pretty` — Firefox unshipped through 153 (correct)
- `text-box-trim` — Firefox unshipped (correct)
- `text-spacing-trim` — Chrome 123+ only (correct)
- `font-variant-emoji` — Firefox 141+, Safari disabled by default (correct)
- COLRv1 — Safari unshipped through 26.5 (correct)
- OpenType registered axes — still wght/wdth/ital/slnt/opsz only (correct)

### Bookkeeping

- `skill.json` → v1.1.0; `files[]` extended with 2 new paths.

---

## [1.0.0] — 2026-04-18 — Wave 5 references / complete

### Added

Sixteen final reference files across seven parallel web-research agents, closing the planned scope:

| File | Coverage | Lines |
|------|----------|-------|
| `references/historical/blackletter.md` | medium | 403 |
| `references/historical/transitional.md` | medium | 404 |
| `references/historical/modern.md` | medium | 413 |
| `references/historical/slab-egyptian.md` | medium | 415 |
| `references/historical/humanist-sans.md` | medium | 449 |
| `references/historical/geometric-sans.md` | medium | 550 |
| `references/historical/neo-grotesque.md` | medium | 544 |
| `references/historical/phototype-era.md` | light | 260 |
| `references/historical/desktop-publishing.md` | light | 319 |
| `references/historical/variable-era.md` | medium | 407 |
| `references/classification/din-16518.md` | light | 273 |
| `references/classification/thibaudeau.md` | stub | 155 |
| `references/science/optical-size-research.md` | light | 304 |
| `references/scripts/ethiopic.md` | stub | 237 |
| `references/foundries/canon-designers.md` | deep | 626 |
| `references/foundries/contemporary-foundries.md` | medium | 509 |

Wave 5 total: **~6,268 lines**. **Cumulative: ~29,080 lines across 59 reference files.** All planned reference files shipped.

### Notable findings

- **Blackletter**: Four-way sub-tradition split (Textura/Rotunda/Schwabacher/Fraktur); Gutenberg's 1455 B42 used ~290 sorts + 83 ligatures + 92 manuscript abbreviations; 1941 Normalschrifterlass banned Fraktur via fabricated "Schwabacher Judenlettern" claim — actual motive was occupation-territory communication bandwidth; Kurrent + Sütterlin handwriting branch distinct; capital ß (U+1E9E) officially adopted 2017 German orthography reform.
- **Transitional**: Romain du Roi (Grandjean 1702, Académie Bignon grid-designed) → Fournier (1764–68 *Manuel Typographique* + Fournier point ~0.345mm) → Baskerville (1757 Virgil, hot-pressed paper, Whatman wove); Mrs Eaves (Licko/Emigre 1996, x-height ~0.37em) named for Sarah Eaves, Baskerville's housekeeper-wife; Times New Roman (Morison/Lardent 1932) Plantin + Baskerville sourced.
- **Modern correction**: Didot point established **1783 by François-Ambroise Didot** (not Pierre-Louis, not 1770s). HTF Didot 7 opsz cuts are **6/11/16/24/42/64/96** (not 7-base). ITC Bodoni 6/12/72 released **1994** at ATypI San Francisco (not 1995), Stone/Goldsmith/Parkinson/Fishman/Strizver/Haley working group.
- **Slab correction**: Memphis designer is **Rudolf Wolf** (not Weiss). Caslon IV 1816 "Two Lines English Egyptian" is caps-only display specimen, never commercially used. Courier (Howard Kettler IBM Selectric 1961) is a monospaced slab — its slab nature often not noticed due to monospace framing.
- **Humanist Sans**: ClearType project 2001–2004 commissioned Calibri + Candara + Corbel + Cambria + Consolas + Constantia; Calibri shipped as Word 2007 default (Jan 30, 2007); **Aptos** (Matteson 2023) replaced Calibri. Inter v4 (2023) added `opsz` axis integrating former Inter Display. Aperture ratio ~0.45–0.60 (humanist) vs ~0.25–0.35 (neo-grotesque) offered as programmatic classification metric.
- **Geometric Sans correction**: **Paul Renner was actively anti-Nazi** (dismissed and Gestapo-arrested 1933 for *Kulturbolschewismus?* essay) — corrects sometimes-circulated false Futura/fascism association. Futura on Apollo 11 plaque (1969) confirmed.
- **Neo-Grotesque NYC subway nuance**: Per Paul Shaw 2011, many stations used **Standard Medium (Akzidenz licensing)** for decades, not Helvetica — "Helvetica subway" is partly legend. Helvetica Now 2019 three-opsz (Micro/Text/Display). Söhne (Sowersby/KLIM 2019) derives from Akzidenz-Grotesk halbfett 36pt.
- **Phototype era** (1949 Intertype Fotosetter → 1980s): single-master scaling lost metal's size-specific refinements; tight-tracking aesthetic (Lubalin/Avant Garde); **ITC Garamond (Tony Stan 1977) is widely regarded as poor revival** — metric-unreliable digitizations of phototype-era ITC faces persist into 2020s.
- **Desktop Publishing** (1984–2000): PostScript 1984 + Macintosh 1984 + PageMaker 1985 + LaserWriter 1985 formed the complete stack; Core Fonts for the Web (Verdana + Georgia + Comic Sans, Carter + Connare, 1996); NYC typesetting profession collapsed from ~15,000 workers to functions embedded in apps.
- **Variable era**: OpenType 1.8 standardized **2016-09-14 ATypI Warsaw** (Apple/MS/Google/Adobe joint announcement); **IFT W3C Candidate Recommendation Draft 2025-11-18**; COLRv1 Safari still unshipped per caniuse 2026-04.
- **DIN 16518** still at 1964 issue through 2026-04 (never substantively revised); most granular blackletter taxonomy anywhere (five-way Gotisch/Rundgotisch/Schwabacher/Fraktur/Fraktur-Varianten); Gruppe VI (all sans) has no sub-classification — BS 2961's four-way Lineal split fills the gap.
- **Thibaudeau 1921 → Vox 1954 → ATypI 1962 → BS 2961 1967 → DIN 1964** forms 15-year classification cascade; Thibaudeau is acknowledged ancestor of all.
- **Optical size research-survey**: Beier 2012 *Reading Letters*, Chaparro SURL 2010 (~7% reading-speed improvement for tall x-height at small sizes), text-vs-display opsz cut at 9pt ~5–8% improvement (Ouwehand & Beier); screen-vs-print opsz requires different tuning; most reading science is Latin-alphabet-only.
- **Canon designers**: Garamond/Jannon untangled per Beatrice Warde's 1926 *Fleuron* V — authentic-source Garamond digitals are Stempel/Sabon/Adobe Garamond/Garamond Premier (ATF/Monotype/ITC/Simoncini are Jannon-line). Eric Gill's abuse flagged per MacCarthy 1989; Penguin 2003 + BBC 2017 Reith Sans institutional moves noted. Hoefler/Frere-Jones 2014 lawsuit + confidential settlement + Frere-Jones departure + **2021 Monotype acquisition of Hoefler & Co**.
- **Contemporary foundries**: Monotype consolidation timeline — FontShop 2014, Fontworks 2020, Hoefler&Co 2021. Custom-commission vs retail business-model economics ($150–500 retail vs $50K–500K custom) explains foundry business-model divergence.

### Bumped

- `skill.json` → **v1.0.0**, status `wave-4-complete` → `complete`, `files[]` lists all **59 reference files**, `tags[]` expanded (transitional, modern, slab-serif, blackletter, humanist-sans, geometric-sans, neo-grotesque, phototype-era, desktop-publishing, variable-era, canon-designers, bringhurst, din-16518, ethiopic).
- `references/INDEX.md` — flipped ⬜ → ✅ on all 16 Wave 5 rows.

### Final state

- **59 reference files, ~29,080 lines** across 9 axes (contemporary, historical, scripts, techniques, classification, science, accessibility, metrics, foundries).
- **No dangling cross-refs remaining** from any wave.
- **No outstanding ⬜ rows** in `references/INDEX.md`.
- All claimed browser/software-shipping dates verified against caniuse, W3C specs, or foundry primary sources where applicable.

---

## [0.5.0] — 2026-04-18 — Wave 4 references

### Added

Fifteen more reference files across three bundle-dispatches and five single-file agents (8 parallel web-research agents total):

| File | Coverage | Lines |
|------|----------|-------|
| `references/science/word-shape-vs-parallel-letter.md` | deep | 629 |
| `references/contemporary/color-fonts.md` | medium | 754 |
| `references/contemporary/font-palette.md` | light | 350 |
| `references/metrics/metric-compatibility.md` | medium | 581 |
| `references/accessibility/low-vision.md` | medium | 532 |
| `references/accessibility/cognitive.md` | light | 396 |
| `references/classification/vox-atypi.md` | medium | 413 |
| `references/classification/bringhurst.md` | medium | 350 |
| `references/scripts/thai.md` | medium | 539 |
| `references/scripts/hangul.md` | light | 493 |
| `references/historical/humanist-renaissance.md` | deep | 590 |
| `references/historical/sans-grotesque.md` | medium | 622 |
| `references/techniques/figures.md` | medium | 376 |
| `references/techniques/small-caps.md` | light | 255 |
| `references/techniques/hanging-punctuation.md` | light | 280 |

Wave 4 total: **~7,160 lines across 15 files**. Cumulative: **~22,808 lines across 43 files** (78% of planned 55).

### Notable findings

- **Word-shape vs parallel-letter-recognition (PLR)**: Larson 2004 is the canonical synthesis. Four evidence lines against word-shape — masked priming case-independence (Paap/Newsome/Noel 1984), transposed-letter effects, VWFA neural activation, Pelli/Farell/Moore 2003 psychophysics. Every historical word-shape pillar overturned. ALL-CAPS ~13–20% slowdown mechanism is crowding + feature-homogeneity, not shape loss. Dyslexia-font premise (shape protection) fails both theoretically and empirically (Kuster 2018, Wery & Diliberto 2017). Bounded to Latin-alphabetic: CJK holistic processing (Hsiao & Cottrell 2009), Arabic cursive, and Devanagari shirorekha differ.
- **Safari COLRv1 unshipped**: per caniuse `colr-v1`, Safari has never shipped COLRv1 rendering through Safari 26.5 (2026-04). Chromium 98+ (Feb 2022), Firefox 107+ (Nov 2022), Edge 98+. For Safari coverage, ship COLRv1 + COLRv0 fallback layered in the same font (standard emoji-font pattern). Apple Color Emoji uses sbix independently.
- **`font-palette` Baseline 2022**: Safari 15.4 (Mar 2022), Chromium 101 (Apr 2022), Firefox 107 (Nov 2022). Safari shipped `font-palette` first but its usefulness on that engine is limited to COLRv0 fonts since Safari lacks COLRv1 rendering.
- **Metric compatibility**: Capsize algorithm is canonical — extract OS/2 typo-metrics, normalize by UPM, compute `size-adjust = P.xHeight / F.xHeight`. Impact-ranked metric precedence: x-height > cap-height > ascender/descender > advance widths > line-gap > UPM. Modernfontstacks.com curated OS-font stacks give "close enough" pairings without explicit overrides. Incremental Font Transfer (IFT) Chrome-flagged as of 2026-04, will reduce the compatibility problem once Baseline.
- **Low-vision typography**: central-scotoma AMD readers benefit more from letter-spacing and shorter measure than from raw size increase (crowding-limited, not acuity-limited, per Pelli 2007). APCA Lc 75 / Lc −75 catches light-on-dark failures the WCAG 2.x 4.5:1 ratio approves; not yet a conformance target. AMD vs photophobia have opposing scheme preferences — respect `prefers-color-scheme`.
- **Cognitive accessibility**: readability (sustained comfort) is the bottleneck, not legibility (letter identification). Sans-serif + 1.5+ line-height + 45-60ch measure + generous paragraph spacing + consistent typography; avoid justify, ALL-CAPS, decorative/script. Comic Sans / centered text / Dyslexie comprehension are all debunked myths.
- **Vox-ATypI 2010 update added Étrangères** (foreign/non-Latin) as acknowledgment that scripts beyond Latin don't fit the 1954 taxonomy; BS 2961:1967 subdivides Lineales into Grotesque/Neo-Grotesque/Geometric/Humanist. Canonical disagreements: Optima (Humanist sans vs Incise), Caslon (Garalde vs Réales), Copperplate Gothic (Incise vs Linéale), Times New Roman (contested).
- **Bringhurst's historical-era taxonomy** (Renaissance/Baroque/Neoclassical/Romantic/Realist/Geometric Modernist/Lyrical Modernist/Expressionist/Postmodern) is essayistic, non-exclusive, suited to design thinking rather than inventory. Rutter 2005 (webtypography.net) adapted Bringhurst's chapters to CSS; Butterick 2010 (practicaltypography.com) is the looser web version.
- **Thai mark-stack clipping is the #1 Thai web-typography bug**: `line-height < 1.5` clips tone marks on first line — invisible to Latin-native developers. Floor at 1.6, target 1.7–1.8. Positive `letter-spacing` destroys mark-to-base binding. Thai line-breaking requires ICU dictionary segmentation (no word spaces).
- **Pretendard (2021+) is the de-facto Korean UI default** because of explicit Inter metric-matching, eliminating the Latin-pairing overrides that Noto/Apple SD Gothic Neo require. `word-break: keep-all` is the standard Korean line-break recipe.
- **Garamond/Jannon confusion**: Monotype, ATF, Simoncini, and ITC "Garamond" are all Jean Jannon 1621 revivals, not Garamond's own 1540s work — untangled by Beatrice Warde (pseud. Paul Beaujon) in *The Fleuron* V, 1926. Genuine Garamond-source digitals are Stempel, Sabon, Adobe Garamond, Garamond Premier.
- **Caslon IV 1816 "Two Lines English Egyptian"** is arguably the first modern sans-serif type — but caps-only, never-commercially-used display spec. The real 19th-c. sans market opens with Figgins and Thorowgood 1820s–30s.
- **Helvetica directly descends from Akzidenz-Grotesk 1898** — Eduard Hoffmann's Haas scrapbook shows proof-by-proof comparison. "Neue Haas Grotesk" and "Helvetica" are the same 1957 Miedinger design renamed for Linotype's 1960 international licensing.
- **Renaissance x-heights (~0.38–0.48 × em)** are incompatible with contemporary UI defaults (~0.53–0.56) without `size-adjust` — a metric-override requirement for anyone pairing Adobe Jenson or Garamond Premier with system sans.
- **`font-variant-numeric` longhands merge** across ancestry per CSS Fonts L4 §7.2.2; `font-feature-settings` declarations **replace**, not merge. Prefer longhands. Inter's slashed zero ships as `ss02` not `zero` — `font-variant-numeric: slashed-zero` is a no-op on Inter.
- **`hanging-punctuation` decade-long Safari-only stall**: Safari shipped 2016; Chromium + Firefox tickets open 10+ years, Chromium Intent-to-Prototype mid-2025; the `last` value unimplemented anywhere including Safari.
- **`font-synthesis-small-caps: none`** (Baseline since 2022) as publication-QA tool — explicit disable catches font-feature gaps that would silently render synthetic small caps.

### Corrections

- **Safari COLRv1 claim in color-fonts.md and font-palette.md**: an initial agent draft asserted Safari shipped COLRv1 in 16.4 (March 2023), citing WebKit Bug 241691. Verification against caniuse (`colr-v1`) and WebKit Bugzilla showed Bug 241691 is about WebAuthn cable→hybrid rename, not COLRv1. Caniuse confirms Safari has not shipped COLRv1 through Safari 26.5. All incorrect claims in both files and fabricated citations removed; tables and summary prose updated to "Safari not shipped through 26.5 per caniuse".

### Bumped

- `skill.json` → v0.5.0, status `wave-3-complete` → `wave-4-complete`, `files[]` lists all 43 references, `tags[]` expanded (color-fonts, cognitive-accessibility, classification, vox-atypi, word-recognition, low-vision, metric-compatibility, humanist-renaissance, thai, hangul).
- `references/INDEX.md` — flipped ⬜ → ✅ on 15 Wave 4 rows; upgraded coverage tier for `science/word-shape-vs-parallel-letter.md` from `medium` to `deep`.

### Known gaps

- Still ⬜: historical/ (10 remaining — blackletter, transitional, modern, slab-egyptian, humanist-sans, geometric-sans, neo-grotesque, phototype-era, desktop-publishing, variable-era), `scripts/ethiopic.md` (stub), `science/optical-size-research.md`, classification/ (2 remaining — `din-16518.md`, `thibaudeau.md`), foundries/ (2 — `canon-designers.md`, `contemporary-foundries.md`).
- No dangling cross-refs remaining from Waves 1–4.

---

## [0.4.0] — 2026-04-18 — Wave 3 references

### Added

Eight more reference files, produced by 8 parallel web-research agents:

| File | Coverage | Lines |
|------|----------|-------|
| `references/scripts/cyrillic.md` | medium | 645 |
| `references/scripts/greek.md` | medium | 516 |
| `references/scripts/hebrew.md` | medium | 734 |
| `references/techniques/vertical-rhythm.md` | deep | 779 |
| `references/techniques/optical-size.md` | deep | 492 |
| `references/science/crowding.md` | deep | 679 |
| `references/metrics/units.md` | deep | 651 |
| `references/contemporary/hinting-and-rendering.md` | deep | 698 |

Wave 3 total: **5,194 lines**. Cumulative reference content: **~15,648 lines across 28 files** (Wave 1 + 2 + 3).

### Notable findings

- **`cap` unit reached Baseline mid-2025** (Chromium 133 Feb 2025, Safari 16.3, Firefox 97). Earlier "Chrome lags" references are outdated.
- **Small/large/dynamic viewport units (`svh`/`lvh`/`dvh` family)** reached Baseline Widely Available June 2025. Progressive-enhancement recipe: `100vh` → `100svh` → `100dvh`.
- **CSS stepped-value math (`round`/`mod`/`rem`)** Baseline 2024 — useful for snapping fluid type to line-height grids.
- **`ch` unit trap quantified**: `65ch` yields 70–80 Latin characters per line because `0` glyph is ~20% wider than lowercase average. Workarounds: `32em`/`36em`, `calc()` correction factor, `ic` for CJK, or accept approximation.
- **Bouma's Law (1970) + Pelli programme (2004–2008)**: crowding is the primary bottleneck on reading speed, not acuity. Feature-pooling in V2–V4, not masking. Critical spacing ≈ 0.5 × eccentricity (Latin); Chinese coefficient is 0.23–0.37 (Zhang et al. 2009).
- **ALL-CAPS slowdown is ~13–20%, not the folklore 30%**. Mechanism is crowding + reduced inter-letter distinguishability (Tinker 1963, Paap et al. 1984, Arditi & Cho 2007, Fiset et al. 2008), not "word-shape loss".
- **Zorzi et al. 2012 (PNAS) + Perea et al. 2012**: letter-spacing interventions improve dyslexic reading measurably — stronger evidence than dyslexia-specific fonts.
- **WCAG 2.2 SC 1.4.12** (+0.12em letter-spacing tolerance) is the crowding-informed accessibility floor that falls directly out of the science.
- **`text-box-trim` / `text-box-edge`**: Safari 18.2 (Dec 2024), Chromium 133 (Feb 2025), Firefox unshipped as of 2026-04. Shorthand: `text-box: trim-both cap alphabetic`. Transforms vertical rhythm from approximate to achievable where supported.
- **`line-height-step` is deprecated/abandoned**; `baseline-source` (Chromium 111+) is inline alignment only, not grid establishment.
- **Vertical-rhythm mathematical drift quantified**: ascent/descent ratios from Inter/Arial/Georgia produce ~0.26 px drift per line, ~10 px over 40 lines — strict rhythm is unachievable pre-2025 without `text-box-trim` or JS-measured Capsize-style negative margins.
- **Opsz fonts inventory (2026-04)**: Roboto Flex 8–144, Amstelvar 8–144, Literata 7–72, Source Serif 4 8–60, Fraunces 9–144, Inter 4.0 14–32 (added 2023). Recursive, IBM Plex, DM Serif do NOT have `opsz` despite common misconception.
- **Opsz CSS precedence trap**: any `font-variation-settings` declaration that omits `"opsz"` silently drops it to default, overriding `font-optical-sizing: auto`. Prefer `font-optical-sizing` property over `font-variation-settings`.
- **Firefox Bugzilla 1856035** (variable fonts rendering at max opsz) fixed in Firefox 120 (Nov 2023) — relevant for pre-120 ESR audiences.
- **Hinting and rendering philosophical split**: Windows (DirectWrite + ClearType) prioritizes hinting over fidelity; macOS (CoreText) prioritizes fidelity over hinting and removed sub-pixel AA in macOS 10.14 Mojave (2018). Linux FreeType configurable, most distros follow macOS approach since ~2020.
- **`-webkit-font-smoothing: antialiased` on body text is an anti-pattern on low-DPI Windows** — thins strokes to near-illegibility. Use only on display-size text if needed.
- **Cyrillic Peter-the-Great 1708 civil-type reform** is the origin of modern Cyrillic letterforms' Latin-like shapes. Bulgarian lowercase `locl BGR` and Serbian/Macedonian italic `locl SRB`/`MKD` are mandatory for correct rendering — Fira Sans is the reference `locl BGR` case study.
- **"Italic т looks like Latin m" trap**: the Russian italic Cyrillic letter т (te) is the single most confusing glyph for Western readers. Mitigation: `locl SRB` Serbian italics, which redraw these forms.
- **Greek monotonic vs polytonic** is orthographic, not stylistic. Monotonic adopted Greece 1982 (Presidential Decree 297/1982). Final sigma σ/ς is a Unicode codepoint distinction (U+03C3/U+03C2), not an OpenType `fina` feature.
- **Greek Question Mark U+037E is canonically equivalent to U+003B** (semicolon); Greek "semicolon-function" is ano teleia U+0387 — reverse of naive assumption.
- **Hebrew is unicameral** — no ALL CAPS treatment available, no small-caps applicable, no "title case" distinction. Emphasis must come from weight/size/spacing, not case.
- **Hebrew+Latin bilingual metric-harmony**: Heebo, Rubik, IBM Plex Hebrew, Noto Sans/Serif Hebrew designed with coordinated x-height/cap-height; mismatched metrics the #1 bilingual design failure; `size-adjust` can compensate partially.

### Bumped

- `skill.json` → v0.4.0, status `wave-2-complete` → `wave-3-complete`, `files[]` lists all 28 references, `tags[]` expanded to include `crowding`, `css-units`, `vertical-rhythm`, `optical-size`, `hinting`, `rendering`, `hebrew`, `cyrillic`, `greek`.
- `references/INDEX.md` — flipped ⬜ → ✅ on 8 Wave 3 rows; upgraded coverage tier for `science/crowding.md`, `techniques/vertical-rhythm.md`, `techniques/optical-size.md` from `medium` to `deep` (content warranted it).

### Known gaps

- Still ⬜: `contemporary/color-fonts.md`, `contemporary/font-palette.md`, all historical/ entries (12 files), remaining scripts (Thai, Hangul, Ethiopic), `techniques/small-caps.md` / `figures.md` / `hanging-punctuation.md`, all classification/ (4 files), remaining science (`word-shape-vs-parallel-letter.md`, `optical-size-research.md`), accessibility/ (`low-vision.md`, `cognitive.md`), `metrics/metric-compatibility.md`, foundries/ (2 files).
- Peer cross-refs still dangling: `science/word-shape-vs-parallel-letter.md`. All Wave 4 candidates.

---

## [0.3.0] — 2026-04-17 — Wave 2 references

### Added

Ten more reference files, produced by 8 parallel web-research agents:

| File | Coverage | Lines |
|------|----------|-------|
| `references/contemporary/opentype-features.md` | deep | 542 |
| `references/contemporary/font-delivery.md` | deep | 758 |
| `references/contemporary/metric-overrides.md` | medium | 657 |
| `references/techniques/measure.md` | deep | 597 |
| `references/techniques/modular-scale.md` | medium | 235 |
| `references/scripts/latin.md` | deep | 731 |
| `references/scripts/devanagari.md` | medium | 632 |
| `references/accessibility/wcag-type.md` | deep | 574 |
| `references/accessibility/dyslexia.md` | medium | 477 |

Cumulative reference content: **~10,454 lines across 20 files** (Wave 1 + Wave 2).

### Notable findings

- **CSS precedence rule** between `font-variant-*` and `font-feature-settings`: longhands merge across ancestry; `font-feature-settings` declarations *replace*, don't merge. Reach for longhands first; `font-feature-settings` only for tags variant properties don't cover (ss01–ss20, cv01–cv99, case, cpsp, East Asian halt/palt/vert).
- **`font-variant-emoji`** only shipped in Chromium 125 (June 2024); pre-2024 requires Unicode variation selectors (U+FE0E / U+FE0F).
- **`@font-feature-values`** Chromium 111 (2023). Late arrival — most production code still writes `font-feature-settings: "ss01"` directly.
- **Font delivery defaults (2026-04)**: WOFF2 only + self-hosted + `unicode-range` splits + `font-display: swap` + metric overrides. IFT still Chrome-flagged; no Baseline yet. HTTP/2 server push for fonts removed in Chrome 106 (2022). `fetchpriority` reached Baseline 2024.
- **EU privacy rulings** (Munich 2022, Garante 2023, CNIL 2024) make Google Fonts CDN a consent-gated third-party for EU-facing sites; self-host or use Bunny Fonts.
- **`ch` gotcha**: `65ch` yields 70–80 lowercase characters, not 65 — `ch` is the `0` glyph's advance, wider than lowercase average. Use `em`-based approximations for font-agnostic measure, `ic` for CJK.
- **Default measure recipe for Latin prose**: `max-width: 65ch; line-height: 1.55; text-wrap: pretty;`
- **Default modular ratio for general UI**: 1.25 (major third).
- **Latin `locl` variants most often missed**: Vietnamese stacked-mark clipping, Polish kreska vs Czech acute (PLK), Romanian comma-below vs cedilla (ROM). `TRK` requires fix in both font and `toLocaleUpperCase('tr')`.
- **Devanagari**: `letter-spacing: 0` is the cardinal CSS rule. Shirorekha is load-bearing, i-matra has pre-base reordering, halant (U+094D) triggers conjunct formation. Marathi + Nepali differ from Hindi in specific letters (Marathi's ळ, eyelash reph).
- **metric-overrides** — Capsize-style algorithm: extract OS/2 typo-metrics, normalize by UPM, `size-adjust = P.xHeight / F.xHeight`, `ascent-override = P.ascent_em / size-adjust`. Use `size-adjust` (face-level, fixes CLS) with `font-size-adjust` (per-element safety net) together.
- **WCAG**: conform to 2.2 for audits; 2.2 SCs 1.4.3, 1.4.4, 1.4.8, 1.4.10, 1.4.12 carry text weight. WCAG 3.0 / APCA is Working Draft — secondary internal check only; no valid conformance claim.
- **Dyslexia fonts**: Kuster 2018, Wery & Diliberto 2017, Rello & Baeza-Yates 2013/17 — null-to-weak support for weighted-bottom fonts. Zorzi 2012 and Perea 2012 show letter spacing, line spacing, measure, and size interventions have stronger evidence. Offer dyslexia-fonts as user preference; invest design budget in spacing.

### Bumped

- `skill.json` → v0.3.0, status `wave-2-complete`, `files[]` lists all 20 references.
- `references/INDEX.md` — flipped ⬜ → ✅ on 10 Wave 2 rows.

### Known gaps

- Still ⬜: `contemporary/color-fonts.md`, `contemporary/font-palette.md`, `contemporary/hinting-and-rendering.md`, all historical/ entries, remaining scripts (Cyrillic, Greek, Hebrew, Thai, Hangul, Ethiopic), `techniques/vertical-rhythm.md` / `optical-size.md` / `small-caps.md` / `figures.md` / `hanging-punctuation.md`, all classification/, three of four science/ files, accessibility/low-vision.md + cognitive.md, metrics/metric-compatibility.md + units.md, foundries/.
- Peer cross-refs that still dangle from Wave 1+2 files: `science/crowding.md`, `science/word-shape-vs-parallel-letter.md`, `contemporary/hinting-and-rendering.md`, `techniques/vertical-rhythm.md`, `metrics/units.md`. All Wave 3 candidates.

---

## [0.2.0] — 2026-04-17 — Wave 1 references

### Added

Ten Phase-2 reference files, produced in parallel by 8 web-research agents, totaling ~5,250 lines of useful content:

| File | Coverage | Lines |
|------|----------|-------|
| `references/contemporary/css-text-properties.md` | deep | 743 |
| `references/contemporary/variable-fonts.md` | deep | 424 |
| `references/metrics/anatomy.md` | deep | 269 |
| `references/metrics/metrics-glossary.md` | deep | 448 |
| `references/techniques/fallback-stacks.md` | deep | 884 |
| `references/techniques/pairing.md` | deep | 309 |
| `references/scripts/arabic.md` | medium | 539 |
| `references/scripts/cjk-han.md` | medium | 416 |
| `references/scripts/japanese.md` | medium | 585 |
| `references/science/legibility-vs-readability.md` | medium | 634 |

### Notable findings surfaced during authoring

- **`text-wrap: pretty`** still unshipped in Firefox 152 (2026-04); Firefox is the sole holdout among evergreens.
- **`text-box-trim`** landed in Chromium 133 (Feb 2025) and Safari 18.2 (Dec 2024); Firefox unshipped.
- **`hanging-punctuation`** remains Safari-only after a decade; `last` specced but no engine implements it.
- **`avar 2.0`** warping originated in HarfBuzz's Boring Expansion Spec, not directly in OT 1.9.1's `avar` page — a real discrepancy worth flagging.
- **Variable fonts** ≈ 95.9% global support; **COLRv1** ≈ 78% (Safari still unimplemented through 26.5).
- **`text-spacing-trim`**: Chromium-only for `space-all`/`normal`; `trim-both`/`trim-all`/`auto` unimplemented anywhere as of 2026-04.
- **Kashida justification** for Arabic remains unreliably supported — prefer ragged-left for RTL.
- **Dyslexia-specific fonts**: meta-analyses show null-to-weak comprehension effects (Kuster et al. 2018 and follow-ups); spacing + measure interventions have stronger support.
- **ALL-CAPS slowdown** attributable to reduced inter-letter distinguishability + crowding, not to "word-shape loss" (Larson 2004 consensus).

### Bumped

- `skill.json` → v0.2.0, status `wave-1-complete`, `files[]` lists all 10 new references.
- `references/INDEX.md` — flipped ⬜ → ✅ on 10 rows.

### Known gaps (to be addressed in Wave 2 / 3 / 4)

- All `contemporary/opentype-features.md`, `contemporary/font-delivery.md`, `contemporary/metric-overrides.md`, `contemporary/color-fonts.md`, `contemporary/font-palette.md`, `contemporary/hinting-and-rendering.md` still planned.
- Historical era files, remaining scripts (Latin deep-dive, Cyrillic, Greek, Hebrew, Devanagari, Thai, Hangul, Ethiopic), remaining techniques, classification, science (crowding, word-shape, opsz), accessibility, foundries — all planned.
- Three Wave 1 files reference peers that do not yet exist (`./crowding.md`, `./word-shape-vs-parallel-letter.md`, `../contemporary/hinting-and-rendering.md`, `../accessibility/dyslexia.md`). Cross-refs resolve to 404 until those land; flagged at `notes:` top of files that carry them.

---

## [0.1.0] — 2026-04-17 — Skeleton

### Added

- Directory scaffold: `expert-typography/` with `references/` subdirectory.
- `SKILL.md` — flat-prose entry file with frontmatter, "How to Read This Skill", and seven quick-reference tables (task → reference; metrics; CSS text surface; variable-font axes; script depth declaration; classifications; composition). Tables are stubs; content lands in v0.2.0 as reference files are authored.
- `skill.json` — v0.1.0 manifest. Status `skeleton`. Composition declares peers (`ui-sys-typography`, `ui-verify-i18n`, `expert-color`, `ui-sys-icons`) and consumers (`ui-audit-quality`, `ui-schema-ui`, `ui-build-theme`, `ui-schema-brand`). Invariants declared (answers-not-generators, flat-prose entry, dated claims, declared script-depth, cited sources).
- `references/INDEX.md` — full reference manifest: 55 planned files across nine axes (`contemporary`, `historical`, `scripts`, `techniques`, `classification`, `science`, `accessibility`, `metrics`, `foundries`) with status markers, coverage tiers, and per-file purpose. Four-wave Phase-2 research-survey plan.

### Design notes

- Structure mirrors `meodai/skill.expert-color` (flat SKILL.md + tiered `references/` by axis). Extends with a dedicated `scripts/` axis — script-specific typographic norms — which has no expert-color analog. Latin deep; Cyrillic/Greek/Arabic/Hebrew/Devanagari/Thai/CJK/Japanese medium; Hangul light; Ethiopic stub.
- Intentionally does **not** include generation. Peers with `ui-sys-typography` for that.
- All reference files are planned to ship with a date header and coverage tier so staleness is visible and depth claims are honest.

### What's next (Phase 2)

Wave 1 (first parallel dispatch): `contemporary/css-text-properties.md`, `contemporary/variable-fonts.md`, `metrics/anatomy.md` + `metrics/metrics-glossary.md`, `techniques/fallback-stacks.md`, `techniques/pairing.md`, `scripts/arabic.md`, `scripts/cjk-han.md` + `scripts/japanese.md`, `science/legibility-vs-readability.md`. See `references/INDEX.md` § Phase-2 Research Wave Plan.

## 2026-07-01 — ported into the user-scope corpus
Moved from the nonoun-skills design-skills plugin to ~/.claude/skills (domain-verb naming; bin/ -> scripts/; dead ui-dev peer handles repointed or prose-ified). Plugin copy is now legacy.

## 2026-07-02 — net-new entry surface (knowledge-pack template)
Legacy ~230-line port-era body replaced in place with a ~90-line typed retrieval index (identity → axis consult table → Grep-first consult procedure with worked example → boundaries). Kept: verbatim frontmatter description, the Honesty rule, fallback-stack + font-size-adjust pinned routes, per-script routing, and the token-builder / component-author / i18n-verify / color-science boundaries (no owned type-scale generator — stated, not implied). Killed: the seven inline quick-reference tables (metrics cheat sheet, CSS text surface, VF axes, script tiers, classification comparison, composition, not-in-scope) — that content lives in, and is now retrieved from, `references/`.

## 2026-07-03 — bookkeeping true-up + ghost-peer purge (deep-review batch 4)
- **Naming record corrected**: the actual current name is `typography-lettering` — the `ref-typography` name (1.1.1 above) lasted only until the 2026-07-01 port into the user-scope corpus, which adopted domain-verb naming; that rename was never logged. It is now.
- **`skill.json` removed** at the 2026-07-01 port (plugin-manifest artifact; the corpus has no manifest layer). "Bookkeeping: skill.json → vX" lines in entries above are historical. Manifest duties live in `references/INDEX.md` + this changelog.
- **Ghost-peer purge**: 8 live lines routed token computation to `ui-sys-typography` / `ui-build-tokens` — peers declared at 0.1.0 that never shipped. Rewritten per SKILL.md's dead-end doctrine: computation derived inline; token-layer realization → the `token-builder` agent. Their names survive only in the historical entries above.
- **INDEX**: retitled to the pack's real name; `custom-highlights-api.md` + `interop-2026-text.md` folded from the appendix into the contemporary/ table with tier + purpose; the stale Phase-2 wave plan deleted — that history is the Wave 1–5 entries above.
