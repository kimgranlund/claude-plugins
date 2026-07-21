# Color Science — Perception References

Curated transcripts, notes, and source material for the `color-perception-facts` pack — vision
and color-appearance science: what the eye and brain do with light.

**49 files**, organized by ask-axis below: `terminology & dimensions` (2), `vision mechanics` (7),
`appearance science` (10), and the `textbook layer` (30 — Briggs lectures + philosophy/education +
the two whole-site scrapes). Subdirs preserve the original taxonomy: `historical/` (1),
`contemporary/` (47, incl. `huevaluechroma/` and `colorandcontrast/`), `techniques/` (1).

**Extracted 2026-07-06** from the `color-science` pack (split into four: `color-space-facts`,
`color-perception-facts`, `color-contrast-facts`, `physical-color-facts`). Aesthetics,
meaning, and history live in the sibling `color-theory-facts` pack (split 2026-07-02, predates this
extraction); color-theory-facts cites four of this pack's files for the perceptual mechanism under an
aesthetic effect — see **Straddle files**, below.

This `references/INDEX.md` owns the file count (49) — the skill file and changelog cite it rather
than restating independently.

<!-- markdownlint-disable MD060 -->

## Terminology & Dimensions — chroma vs. saturation, lightness vs. brightness

| File | Summary | Source |
| --- | --- | --- |
| [Chroma vs. Saturation](contemporary/chroma-vs-saturation.md) | Chroma = distance from neutral axis. Saturation = angle from white. Not the same. Includes Donahue interactive viz with DIN 6164 saturation, OKLCH chroma, and iso-line morphing. | [Color Nerd](https://www.youtube.com/shorts/IlpD9DXiH-c), [Donahue](https://petertdonahue.com/Saturation-vs-Chroma.html) |
| [Lightness vs. Brightness](contemporary/lightness-vs-brightness.md) | Lightness = contextual (relative to illumination). Brightness = absolute. Cube demo. | [Color Nerd](https://www.youtube.com/shorts/5qbtjJe1V2o) |

## Vision Mechanics — cones, opponent process, afterimages, metamerism, tetrachromacy, JPEG

| File | Summary | Source |
| --- | --- | --- |
| [Albers — Interaction of Color](historical/albers-interaction-of-color.md) | Classic perception-first teaching text on simultaneous contrast and color relativity — the mechanism behind afterimages and context effects. Essential for context effects, but best paired with modern science rather than treated as a full scientific account. | [Archive.org](https://archive.org/details/interactionofcol0000albe) |
| [How Eyes Turn Light into Color](contemporary/how-eyes-turn-light-into-color.md) | Graph paper exercise: cone cells compress spectral info into 3 signals. "Wavelengths don't have color — imbalances cause the sensation." Why metamerism exists. Why color mixing works. | [Color Nerd](https://www.youtube.com/watch?v=u_tQ4UkIPfU) |
| [JPEG & Colour — Computerphile](contemporary/computerphile-jpeg-color.md) | RGB→YCbCr→chroma subsampling. 100× less color = identical. 382K views. | [Computerphile](https://www.youtube.com/watch?v=n_uNPbdenRs) |
| [Bird Hue Circuits & Tetrahedra](contemporary/bird-color-theory-hue-circuits.md) | 4 cones → 4 hue circuits → tetrahedral network. Birds need 4D color. | [Color Nerd](https://www.youtube.com/shorts/_Uq1vb5UtoM) |
| [Bird Complementary Colors](contemporary/bird-complementary-colors-tetrachromacy.md) | 4-cone tetrachromacy: 1+3 or 2+2 complement splits. "Human white" is a color to birds. | [Color Nerd](https://www.youtube.com/shorts/RVPEXrHOiOI) |
| [OLO — "Newly Discovered" Color](contemporary/olo-newly-discovered-color.md) | 488nm laser on individual M-cones. Cone ratio impossible under natural light. 339K views. | [Color Nerd](https://www.youtube.com/shorts/MLG5jjPUwTA) |
| [RGB Shadows / Magical Color Theory](contemporary/magical-color-theory-rgb-shadows.md) | RGB flashlights → white. Object casts CMY shadows. Physical RGB↔CMY proof. 194K views. | [Color Nerd](https://www.youtube.com/shorts/q6l2-l9e50o) |

## Appearance Science — Fairchild, CIECAM02, viewing conditions, MacAdam/JND, Koenderink, warm-cool

| File | Summary | Source |
| --- | --- | --- |
| [Fairchild — Color Appearance Models](contemporary/fairchild-color-appearance-models.md) | Canonical reference for appearance modeling: lightness, brightness, colorfulness, adaptation, surround, and why the same colorimetry can look different under different conditions. | PDF (not shipped; Wiley 2005) |
| [CIECAM02 — Color Appearance Model](contemporary/ciecam02-color-appearance-model.md) | Primary paper for CIECAM02. Useful when viewing conditions, adaptation, and appearance correlates matter more than static coordinates. | [RIT Repository](https://repository.rit.edu/other/143/) |
| [MacAdam Ellipses — Just Noticeable Color Difference](contemporary/macadam-ellipses-jnd.md) | Classic evidence that CIE 1931 xy is not perceptually uniform. Explains local JND regions, LED binning language, and why uniform spaces are needed. | [DOI](https://doi.org/10.1364/JOSA.32.000247) |
| [MacAdam Ellipses — Math](techniques/macadam-ellipses-math.md) | The empirical JND regions in CIE 1931 chromaticity. The non-uniformity that motivated CIELAB, OKLab, and CAM16-UCS. Math + history (no TS; use ΔE_ok / ΔE2000). | [MacAdam 1942](https://opg.optica.org/josa/abstract.cfm?uri=josa-32-5-247) |
| [Koenderink — 3D Metric Field in RGB](contemporary/koenderink-3d-metric-field-rgb.md) | 2026 Koenderink/Gegenfurtner: first dense volumetric empirical measurement of color discrimination across the RGB cube. RGB supports ~1,000 qualitatively distinct regions. Cool side of space is coarser than warm. CIEDE2000 over-elongates ellipsoids. | [bioRxiv DOI](https://doi.org/10.64898/2026.03.09.710376) |
| [Koenderink — Warm/Cool & Well-Tempered Circle](contemporary/koenderink-warm-cool-chromatic-gestalt.md) | Companion series (2022–2024): color circle is not "well tempered" (equal hue angles ≠ equal perceptual steps); warm/cool is a phenomenological axis, not a hue rotation; green and purple are on the warm/cool boundary. Empirical + Gestalt argument. | [Scholar](https://scholar.google.com/citations?hl=en&user=lxW3wvMAAAAJ) |
| [Is Green Warm or Cool?](contemporary/green-warm-or-cool-spectral.md) | Spectral reflectance: green/purple are fundamentally neither warm nor cool. | [Color Nerd](https://www.youtube.com/shorts/WQYLfwa2lAI) |
| [Warm/Cool ≠ Hue](contemporary/warm-cool-color-temperature.md) | Temperature = systematic hue + saturation shift, not just hue rotation. | [Color Nerd](https://www.youtube.com/shorts/XmQ9O4efPrQ) |
| [Color Temperature = Spectral Bias](contemporary/color-temperature-spectral-bias.md) | Which end of spectrum a light favors. Blue scatter fills shadows. | [Color Nerd](https://www.youtube.com/shorts/M3py_iSpuyA) |
| [Pixar Color Science (Khan Academy)](contemporary/pixar-color-science-khan-academy.md) | Full 5-lesson series + bonus. SPD, RGB, HSL, contrast, correction, CIE diagram. | [Khan Academy](https://www.youtube.com/watch?v=T0jzClmP2pc) |

## Textbook Layer — Briggs Lectures & Color Education/Philosophy

| File | Summary | Source |
| --- | --- | --- |
| [Briggs — Colours of Objects & Light](contemporary/briggs-colours-objects-light.md) | Object vs light colours, modes of appearance. 46 min keynote. | [CSA](https://www.youtube.com/watch?v=ii9dWIG9nOY) |
| [Briggs — Elements of Colour](contemporary/briggs-elements-of-colour.md) | Hue/value/chroma, HSB pitfalls, Munsell. 65 min. | [CSA](https://www.youtube.com/watch?v=ZxdVrjWrOqs) |
| [Briggs — Controlling Colour History](contemporary/briggs-controlling-colour-history.md) | Newton → CIE 1931. Trichromacy vs opponency. 39 min. | [CSA](https://www.youtube.com/watch?v=6RUr8MWOpeI) |
| [Briggs — Dimensions of Colour Today](contemporary/briggs-dimensions-of-colour-today.md) | Framework, traditional theory critique, irregular colour solid. 34 min. | [CSA](https://www.youtube.com/watch?v=ZLIIYj2X-Qc) |
| [Briggs — What is a Colour?](contemporary/briggs-what-is-a-colour.md) | Spectral/psychophysical/perceptual levels. Metamerism. CIE. 33 min. | [CSA](https://www.youtube.com/watch?v=mYG9FadbETA) |
| [ISCC/AIC Colour Literacy](contemporary/iscc-aic-colour-literacy-project.md) | Standardizing color education. 19 min. | [CSA](https://www.youtube.com/watch?v=YzARXFlQdx4) |
| [Colour Subjectivisms](contemporary/colour-subjectivisms-philosophy.md) | Philosophy of color perception. 53 min. | [CSA](https://www.youtube.com/watch?v=G0CaskD8Tc0) |
| [Everything TikTok Taught Me (CSA)](contemporary/everything-tiktok-taught-color-theory.md) | 78-min webinar. Integrated mixing (Küppers). Introverted/extroverted octopus. CIECAM02. | [Color Nerd](https://www.youtube.com/watch?v=7dXXlyi__tA) |

## Textbook Layer — David Briggs, "Dimensions of Colour" (huevaluechroma.com, whole scrape)

A scraped site is one cited source with internal coherence — moved and cited whole (never split by
chapter for citation elsewhere), per the pack's D4 rule. **Load discipline:** ch11, ch01, and ch07
each exceed 1000 lines — Grep the chapter for the term first, then Read with an offset; do not read
a chapter start-to-finish for a single-term ask.

| Chapter | File |
| --- | --- |
| 1. Dimensions of Colour | [ch01](contemporary/huevaluechroma/ch01-dimensions-of-colour.md) |
| 2. Light and Shade | [ch02](contemporary/huevaluechroma/ch02-light-and-shade.md) |
| 3. Colour Vision | [ch03](contemporary/huevaluechroma/ch03-colour-vision.md) |
| 4. Additive Mixing | [ch04](contemporary/huevaluechroma/ch04-additive-mixing.md) |
| 5. Subtractive Mixing | [ch05](contemporary/huevaluechroma/ch05-subtractive-mixing.md) (cross-cited from `physical-color-facts` — paint mixing) |
| 6. Mixing of Paints | [ch06](contemporary/huevaluechroma/ch06-mixing-of-paints.md) (cross-cited from `physical-color-facts` — paint mixing) |
| 7. Hue | [ch07](contemporary/huevaluechroma/ch07-hue.md) |
| 8. Lightness and Chroma | [ch08](contemporary/huevaluechroma/ch08-lightness-and-chroma.md) |
| 9. Brightness and Saturation | [ch09](contemporary/huevaluechroma/ch09-brightness-and-saturation.md) |
| 10. Principles of Colour | [ch10](contemporary/huevaluechroma/ch10-principles-of-colour.md) |
| 11. Afterthoughts | [ch11](contemporary/huevaluechroma/ch11-afterthoughts.md) |
| Glossary | [glossary](contemporary/huevaluechroma/glossary.md) |
| References | [references](contemporary/huevaluechroma/references.md) |
| Links (Colour Online) | [links](contemporary/huevaluechroma/links.md) |

## Textbook Layer — Color & Contrast (colorandcontrast.com, whole scrape)

| File | Topics |
| --- | --- |
| [Color Properties](contemporary/colorandcontrast/color-properties.md) | Hue, chroma, lightness, tone, tint, shade |
| [Color Models](contemporary/colorandcontrast/color-models.md) | RGB, RYB, CMYK, additive, subtractive |
| [Color Spaces](contemporary/colorandcontrast/color-spaces.md) | sRGB, P3, LMS, XYZ, CIELAB, OKLAB, CAM16 (cross-cited from `color-space-facts`) |
| [Color Vision](contemporary/colorandcontrast/color-vision.md) | Trichromacy, opponent process, adaptation |
| [Color Effects](contemporary/colorandcontrast/color-effects.md) | Abney, Bezold-Brücke, H-K, Purkinje |
| [Accessibility](contemporary/colorandcontrast/accessibility.md) | APCA, CVD, confusion lines, luminance (cross-cited from `color-contrast-facts`) |
| [UI & Design](contemporary/colorandcontrast/ui-design.md) | Scales, themes, dark mode, interpolation |
| [Publications](contemporary/colorandcontrast/publications.md) | Recommended reading (Fairchild, Hunt, Livingstone...) |

## Straddle files (cited from color-theory-facts — the perceptual mechanism under an aesthetic effect)

`color-theory-facts`'s corpus documents harmony, meaning, and history; five files across the family carry
the *mechanism* under an aesthetic claim it makes and are cited (never duplicated) from its INDEX:
three here — `historical/albers-interaction-of-color.md` (simultaneous contrast — "why do these
colors vibrate side by side"), `contemporary/koenderink-warm-cool-chromatic-gestalt.md` and
`contemporary/green-warm-or-cool-spectral.md` (warm/cool as a perceptual axis, not a hue rotation —
the empirical basis under "warm palette" talk) — plus `opponent-process-color-blindness` in
`color-contrast-facts` (its load-bearing claim is CVD-safe pairs; this pack's scrapes cover
opponent process as vision science) and `goethe-edge-colors-design-hack` in
`color-space-facts` (it is gradient math, not appearance science).

## Online Tools

<!-- markdownlint-disable MD034 -->

| Tool | URL | Description |
| --- | --- | --- |
| Dimensions of Color | https://www.huevaluechroma.com | David Briggs color theory — canonical site for the huevaluechroma scrape above |

<!-- markdownlint-enable MD034 -->

Bruce MacEvoy's pigment-data site (handprint.com) is catalogued in `physical-color-facts`'s
Online Tools table — pigment physics is its primary axis; not duplicated here (D4 cross-cite
discipline).

## Source PDFs (not shipped with this pack; canonical at the cited archive.org URL)

Primary source one reference file transcribes from. The other Source-PDF provenance rows (ISCC-NBS
Circular 553, Kelly & Judd, Laurie, Painting Materials handbook, Schweizer) live in
`physical-color-facts`' INDEX — this pack owns only the Helmholtz row (foundational modern color
science, cited across the vision-mechanics and appearance-science axes above).

| Work | Description | Canonical source |
| --- | --- | --- |
| Helmholtz — Physiologischen Optik (1856–67) | Modern color science foundation | [archive.org](https://archive.org/details/handbuchderphysi00helm) |

<!-- markdownlint-enable MD060 -->

## Third-party notices

`color-science-project-files`'s third-party notices were checked (R4): it carries only a
repository-wide generic notice (original materials vs. third-party-derived reference content under
`references/`) and names no file, domain, or scrape specifically — it does not single out
huevaluechroma.com or colorandcontrast.com for distinct terms. No pack-specific NOTICES rows are
carried here; the generic notice already covers this pack's third-party-derived content and remains
project-files' record.
