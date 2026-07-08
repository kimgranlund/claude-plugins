# Color Science Materials References

Curated transcripts, notes, and source material for the `color-science-materials` pack — pigment
and mixing physics, print/screen reproduction and measurement, and color naming standards/datasets.
Extracted 2026-07-06 from the `color-science` pack (its own reference corpus split into four
sibling packs: `color-science-spaces`, `color-science-perception`, `color-science-accessibility`,
`color-science-materials`); prior history lives in `color-science-project-files`'s changelog.

**30 files**, organized by ask-axis below. Subdirs preserve the original taxonomy: `historical/`
(4), `contemporary/` (7), `techniques/` (19).

## Pigment & mixing physics — why blue+yellow makes green, not gray

<!-- markdownlint-disable MD060 -->

| File | Summary | Source |
| --- | --- | --- |
| [Kubelka-Munk Single-Constant Mixing](techniques/kubelka-munk-single-constant.md) | Physical pigment mixing — blue+yellow=green via K/S space arithmetic. The model behind every paint-formulation tool. Paired with `src/pigment/kubelka-munk.ts` (in color-science-project-files). | [Kubelka 1948](https://opg.optica.org/josa/abstract.cfm?uri=josa-38-5-448) |
| [Spectral.js](techniques/spectraljs-pigment-mixing.md) | Open-source Kubelka-Munk pigment mixing. Blue+yellow=green. GLSL shaders. | [GitHub](https://github.com/rvanwijnen/spectral.js) |
| [Imaginary Pigments — Mixbox](techniques/imaginary-pigments-mixbox.md) | K-M paths in OKLAB: bend toward CMY, away from RGB. Hello Mixbox tool. | [Color Nerd](https://www.youtube.com/watch?v=o5spI1V3Rss) |
| [FocalPaint](techniques/focalpaint-impossible-pigments.md) | iPad spectral mixing. Kubelka-Munk. Editable waveforms. Metamers. | [focalpaint.com](https://focalpaint.com) |
| [Mixing Paths (Hexaflexagon)](techniques/color-mixing-hexaflexagon-paths.md) | CMY paths curve out (retain chroma), RGB curve in (lose chroma). | [Color Nerd](https://www.youtube.com/shorts/SX-LJuxn4j8) |
| [Color Triangle](techniques/color-triangle-jinjer-markley.md) | CMY at corners, pigments plotted, offset neutral. Straight lines predict mixes. | [Color Nerd](https://www.youtube.com/shorts/AC2LsmSRGTE) |
| [The ColorDisk + Trillium](techniques/colordisk-trillium.md) | Peter Donahue's artist tool for paint mixing and complements. The overlay predicts curved pigment-mixing paths, neutral crossings, tint shifts, and gamut-mask planning better than a flat wheel. | PDF (not shipped; petertdonahue.com) |
| [Skin Tones — Why Black Doesn't Work](techniques/skin-tones-color-mixing-youthforia.md) | Skin tones curve OUTWARD in chroma as they darken (Monk Scale). Adding black → grayer = wrong direction. Use dark+chromatic pigments. Same principle as non-linear mixing paths. | [Color Nerd](https://www.youtube.com/watch?v=TWVjZ4vuku8) |
| [Paint Mixing Lecture (UFV)](techniques/paint-mixing-lecture-ufv.md) | Non-linear mixing. Tinting strength. "Paints are not colors." 51 min. | [Color Nerd](https://www.youtube.com/watch?v=jLSCbbID1ck) |
| [Golden — Paint Making](contemporary/golden-paint-making.md) | Pigment grinding, binders, dispersion, paint formulation. 71 min. | [CSA](https://www.youtube.com/watch?v=UVdPAczWWAI) |
| [Caravaggio's Copper Resinate Greens](historical/caravaggio-copper-resinate-greens.md) | Copper resinate glaze over verdigris ~1600. Spectral cancellation predates complementary color theory. | [Color Nerd](https://www.youtube.com/shorts/RezeYJFTacs) |
| [Atlas of Rare & Familiar Colour](contemporary/atlas-of-rare-familiar-colour.md) | Harvard Art Museums / Forbes Pigment Collection atlas. Connects color to real pigment samples, material history, conservation, and museum context rather than abstract wheel theory. | PDF (not shipped; Harvard Art Museums) |
| [Iridescence / Thin-Film Interference](contemporary/iridescence-thin-film-interference.md) | Angle changes which λ is blocked. Same film, different colors. | [Color Nerd](https://www.youtube.com/shorts/hCGv73cA0yA) |
| [Iridescent Color Math](contemporary/iridescent-color-math.md) | Simultaneous additive + subtractive mixing with iridescent plastic. | [Color Nerd](https://www.youtube.com/shorts/PJUFzgmtOBI) |

<!-- markdownlint-enable MD060 -->

## Reproduction & measurement — print, screen, ICC, and physical gamut

<!-- markdownlint-disable MD060 -->

| File | Summary | Source |
| --- | --- | --- |
| [ICC Profiles — PCS, Rendering Intents, and Color Management](techniques/icc-profile-color-management.md) | Canonical reference for device profiles, the D50 profile connection space, rendering intents, viewing-condition assumptions, and why the same numbers can mean different colors on different devices. | [ICC](https://www.color.org/iccprofile.xalter) |
| [Screen to Print — Colour Fidelity](techniques/screen-to-print-colour-fidelity.md) | ICC profiles, color management workflow. 66 min CSA. | [CSA](https://www.youtube.com/watch?v=DZNY_QOrZZs) |
| [Hunt & Pointer — Measuring Colour](contemporary/hunt-pointer-measuring-colour.md) | Authoritative reference on colorimetry, measurement, illuminants, observers, and reproduction workflows. Strong support for print, photography, proofing, and device characterization questions. | [Archive.org](https://archive.org/details/measuringcoloure00rwgh_0) |
| [Pointer's Gamut — Real Surface Colors](contemporary/pointers-gamut-real-surface-colors.md) | Practical gamut for real diffusely reflecting surfaces. Smaller than the optimal color solid and much more useful for object-color realism, paint datasets, and surface-color references. | [Overview](https://en.wikipedia.org/wiki/Gamut#Pointer's_gamut) |
| [Pointer's Gamut — Math](techniques/pointers-gamut-math.md) | The empirical boundary of real surface colors (~75% of visible). Useful for physical-media palette feasibility checks. Math + data source (no TS; specialized use). | [Pointer 1980](https://onlinelibrary.wiley.com/doi/10.1002/col.5080050308) |

<!-- markdownlint-enable MD060 -->

## Naming standards & datasets — ISCC-NBS, Munsell, Ridgway, and paint-name catalogs

<!-- markdownlint-disable MD060 -->

| File | Summary | Source |
| --- | --- | --- |
| [Color Definitions & Webster/ISCC](historical/color-definitions-webster-iscc.md) | Godlove wrote 3,000 color definitions for Webster's 2nd ed. ISCC-NBS = 319 named blocks. Nickerson took over for 3rd ed. after Godlove died. Kory Stamper _True Color_ (2026). | [Color Nerd](https://www.youtube.com/shorts/e33WEqkaPPQ), [+](https://www.youtube.com/shorts/v4wCvksrR2M) |
| [Munsell — Hue, Value, Chroma](historical/munsell-hue-value-chroma.md) | Direct practical explanation of the Munsell system as three dimensions: hue around a circle, value on the neutral axis, chroma outward from gray. Strong corrective to flat wheel thinking. | [Munsell](https://munsell.com/color-blog/a-grammar-of-color-definition-hue-value-chroma/) |
| [Ridgway — Color Standards (1912)](historical/ridgway-color-standards-1912.md) | 1,115 named colors across 53 plates. Full text from Gutenberg. Systematic nomenclature for naturalists. 36-hue chromatic scale. [Digitized JSON](https://github.com/meodai/Color-Standards-and-Color-Nomenclature). | [Gutenberg](https://www.gutenberg.org/files/63087/63087-h/63087-h.htm) |
| [color-name-lists](techniques/color-name-lists.md) | 18 color naming systems in one package: ISCC-NBS, XKCD, Japanese, Chinese, Werner, Ridgway, RAL, Le Corbusier, X11, HTML, Wada Sanzō, Risograph, more. | [GitHub](https://github.com/meodai/color-name-lists) |
| [Jaffer — Color-Name Dictionaries](techniques/jaffer-color-name-dictionaries.md) | Technical audit of named-color dictionaries. Separates surface-color vs light-source dictionaries, critiques VGA/X11/CSS inheritance, checks gamut realism and dark-tone coverage, and evaluates datasets in RGB and CIELAB space. | [MIT](https://people.csail.mit.edu/jaffer/Color/Dictionaries) |
| [Jaffer — Resene Paint Colours](techniques/jaffer-resene-paint-colours.md) | Jaffer's evaluation of Resene as a strong paint-derived naming system for surface colors: broad CIELAB coverage, physically plausible paint gamut, and better usefulness than most web color dictionaries. | [MIT](https://people.csail.mit.edu/jaffer/Color/Dictionaries) |
| [Jaffer — Winsor-Newton Water-colours](techniques/jaffer-winsor-newton-watercolours.md) | Measured watercolor data in CIE L*a*b\*. Strong evidence that real paint datasets exceed sRGB and make better surface-color references than RGB-grid naming systems. | [MIT](https://people.csail.mit.edu/jaffer/Color/Dictionaries) |
| [colornerd (jpederson)](techniques/colornerd-paint-manufacturer-swatches.md) | 29,875 swatches from 12 manufacturers (Behr, Benjamin Moore, Sherwin Williams, RAL, HKS, TOYO, TRUMATCH...). SCSS/Less/JSON/CSV. Real paint formulations, not theoretical colors. | [GitHub](https://github.com/jpederson/colornerd) |
| [color-description](techniques/color-description-library.md) | Hex → human adjectives ("pale, delicate" or "lush, ablaze, bold"). | [GitHub](https://github.com/words/color-description) |
| [Color Names Across Languages](contemporary/kim-heer-color-naming-across-languages.md) | UW/IDL EuroVis 2019: 79-language color naming dataset. Quantifies translation loss between languages, shows universal vs. language-specific category boundaries (e.g., Russian/Korean mandatory blue split). 8 interactive visualizations. | [GitHub](https://github.com/uwdata/color-naming-in-different-languages) |
| [Digital Color Fidget](techniques/digital-color-fidget.md) | Multi-ring harmony tool + ISCC-NBS Picker, OSA-UCS, Gamut Mask, Spiral Palette. | [Color Nerd](https://www.youtube.com/shorts/CS5T_Z4ac5E) |

<!-- markdownlint-enable MD060 -->

## Cited from color-science-perception (straddle files — live there, never duplicated)

Paint-mixing chapters of the David Briggs scrape carry the *pigment-physics* half of subtractive
mixing; the full scrape (all 14 chapters) lives in `color-science-perception` as one coherent
cited source (splitting a scraped site by chapter would strand its glossary/references/links
files). This pack cites the two chapters directly relevant to paint mixing:

| Chapter (in `color-science-perception`) | Why this pack cites it |
| --- | --- |
| *ch05 — Subtractive Mixing* (huevaluechroma) | Why pigments subtract wavelengths rather than add them — the physical basis under K-M mixing |
| *ch06 — Mixing of Paints* (huevaluechroma) | Practical paint-mixing behavior (tinting strength, non-linear paths) that complements `techniques/kubelka-munk-single-constant.md` |

## Online tools

<!-- markdownlint-disable MD034 -->

| Tool | URL | Description |
| --- | --- | --- |
| color.pizza API | https://api.color.pizza/v1/ | Color naming API: `?values=8a2be2&list=bestOf` → name, hex, RGB, HSL, Lab, luminance, WCAG contrast. 42 lists (31K+ default, bestOf, ridgway, xkcd, multi-language...) |
| 147 Colors | https://147colors.com | Named CSS colors reference |
| ISCC-NBS Centroid Picker | https://petertdonahue.com/ISCC-NBS-Color-Names.html | Pick by ISCC-NBS name |
| handprint.com | https://www.handprint.com | Bruce MacEvoy pigment data |

<!-- markdownlint-enable MD034 -->

## Source PDFs (not shipped with this pack; canonical at the cited archive.org URLs)

Primary sources the reference files transcribe from. No PDFs ship with this pack — fetch them
from the archive.org links, which are canonical.

| Work | Description | Canonical source |
| --- | --- | --- |
| ISCC-NBS Circular 553 (1955) | Color names dictionary | [archive.org](https://archive.org/details/circularofbureau553unse) |
| Kelly & Judd — Color: Universal Language (1976) | ISCC-NBS reference | [archive.org](https://archive.org/details/coloruniversalla00kell) |
| Laurie — Painter's Methods (1926) | Pigments, glazes, copper resinate | [archive.org](https://archive.org/details/paintersmethodsm00lauruoft) |
| Painting Materials handbook | Historical materials | [archive.org](https://archive.org/details/PaintingMaterial) |
| Schweizer — Resinate Pigments (1907) | Resinate chemistry | [archive.org](https://archive.org/details/distillationofre00schwrich) |
