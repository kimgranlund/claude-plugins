---
date: 2026-04-18
coverage: deep
peers:
  - ./legibility-vs-readability.md
  - ./word-shape-vs-parallel-letter.md
  - ../accessibility/dyslexia.md
  - ../accessibility/wcag-type.md
  - ../techniques/measure.md
  - ../scripts/devanagari.md
  - ../scripts/arabic.md
primary_sources:
  - https://www.nature.com/articles/226177a0  # Bouma, "Interaction effects in parafoveal letter recognition", Nature 226:177–178, 1970
  - https://jov.arvojournals.org/article.aspx?articleid=2192655  # Pelli, Palomares & Majaj, "Crowding is unlike ordinary masking", J. Vision 4(12):12, 2004
  - https://jov.arvojournals.org/article.aspx?articleid=2122073  # Pelli, Tillman, Freeman, Su, Berger & Majaj, "Crowding and eccentricity determine reading rate", J. Vision 7(2):20, 2007
  - https://doi.org/10.1016/j.conb.2008.09.008  # Pelli, "Crowding: a cortical constraint on object recognition", Current Opinion in Neurobiology 18(4):445–451, 2008
  - https://doi.org/10.1016/j.visres.2007.12.009  # Levi, "Crowding — an essential bottleneck for object recognition: a mini-review", Vision Research 48(5):635–654, 2008
  - https://doi.org/10.1167/5.1.6  # Martelli, Majaj & Pelli, "Are faces processed like words? A diagnostic test for recognition by parts", J. Vision 5(1):6, 2005
  - https://doi.org/10.1167/9.4.14  # Martelli, Di Filippo, Spinelli & Zoccolotti, "Crowding, reading, and developmental dyslexia", J. Vision 9(4):14, 2009
  - https://doi.org/10.1016/j.neuropsychologia.2011.10.005  # Moores, Cassim & Talcott, "Adults with dyslexia exhibit large effects of crowding…", Neuropsychologia 49(14):3881–3890, 2011
  - https://doi.org/10.1073/pnas.1205566109  # Zorzi et al., "Extra-large letter spacing improves reading in dyslexia", PNAS 109(28):11455–11459, 2012
  - https://doi.org/10.1016/j.learninstruc.2012.04.001  # Perea, Panadero, Moret-Tatay & Gómez, "The effects of inter-letter spacing…", Learning and Instruction 22(6):420–430, 2012
  - https://pubmed.ncbi.nlm.nih.gov/11923275/  # Chung, "The effect of letter spacing on reading speed in central and peripheral vision", IOVS 43(4):1270–1276, 2002
  - https://doi.org/10.1016/j.visres.2008.08.024  # Zhang, Zhang, Xue, Liu & Yu, "Legibility of Chinese characters in peripheral vision…", Vision Research 49(1):44–53, 2009
  - https://www.nature.com/articles/383334a0  # He, Cavanagh & Intriligator, "Attentional resolution and the locus of visual awareness", Nature 383:334–337, 1996
  - https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html  # W3C, Understanding SC 1.4.12 Text Spacing
  - https://legge.psych.umn.edu/book  # Legge, Psychophysics of Reading in Normal and Low Vision, 2007
  - https://doi.org/10.1111/j.1467-9280.2008.02218.x  # Fiset et al., "Features for identification of uppercase and lowercase letters", Psychological Science 19:1161–1168, 2008
notes:
  - Coverage tier is deep — this file is the canonical crowding reference. Peer files (`word-shape-vs-parallel-letter.md`, `legibility-vs-readability.md`) should link here rather than re-derive Bouma's law.
  - Numeric values ("b ≈ 0.5", "~13–20% ALL-CAPS slowdown") are reported as the literature reports them; exact coefficients are font-, observer-, and task-specific.
  - No token values here; derive spacing values inline from this file's research floors (no generator skill is installed) — realizing them as project tokens belongs to the `token-builder` agent.
---

# Crowding — reading science reference

Crowding is the impairment of target identification by the presence of nearby
flanking objects. In reading, a letter that would be easy to identify in
isolation — well above acuity and contrast thresholds — becomes hard or
impossible to identify when embedded in a word or a line. The features of
the target are still available to the visual system; what fails is the
*assignment* of those features to the target rather than to its neighbours.
Crowding is the dominant visual constraint on peripheral reading and a
meaningful, though smaller, constraint on foveal reading as well.

This file covers what crowding is, where it sits in the reading pipeline,
the empirical work that defines its modern theory, the factors that
intensify or relieve it, and the typographic levers — letter-spacing, case,
weight, x-height, script — that interact with it. It does not re-derive
eye-movement basics already in `./legibility-vs-readability.md`, and does
not propose token values.

## Definition

Crowding is a perceptual phenomenon, not a sensory one. When a target
letter is surrounded by flanker letters inside a certain *critical spacing*,
the observer can still detect that something is there and can often
describe which features (strokes, terminals, curves) are present — but
cannot identify which features belong to the target. Pelli, Palomares &
Majaj (2004) formalised the distinction: crowding leaves detection
thresholds essentially unchanged while elevating identification
thresholds, whereas ordinary masking elevates detection itself. In their
framing, crowding is a failure of *feature integration*, not *feature
detection*. Features are registered, but pooled over a region too large to
be assigned to a single object.

Crowding is distinct from acuity. Acuity is the fine-detail limit of the
retina and early visual cortex — the minimum size at which a feature can
be resolved at all. Crowding persists far above the acuity threshold.
Peripheral reading is almost never acuity-limited at normal body sizes;
it is crowding-limited (Pelli, Tillman, Freeman et al. 2007).

## Bouma's Law

The foundational result is Herman Bouma (1970, *Nature* 226:177–178),
"Interaction effects in parafoveal letter recognition." Bouma presented
single letters at various eccentricities with or without flanking
distractors and measured identification as a function of target–flanker
spacing.

**Bouma's law**: the critical spacing for crowding is approximately
proportional to the eccentricity of the target from fixation. The
coefficient — *Bouma's b* — is roughly **0.5**, meaning that at 5°
eccentricity, letters within about 2.5° of each other crowd; at 10°, the
critical zone expands to about 5°. Restated: each point in the visual
field has an isolation field whose radius is ~½ the distance from that
point to the fovea.

Important features:

- **Scale-invariant in the visual field, not in physical space.**
  Critical spacing scales with eccentricity, not with letter size. Pelli,
  Palomares & Majaj (2004) confirmed that critical spacing is independent
  of target size over roughly a decade of sizes at a given eccentricity.
  Simply making letters bigger does not dissolve crowding.
- **Coefficient varies 0.3–0.5 in most studies** depending on criterion
  accuracy, task, stimuli, and whether spacing is measured centre-to-
  centre or edge-to-edge. Zhang et al. (2009) report ~0.23–0.37 for
  Chinese characters. The law holds; the coefficient is not universal.
- **Asymmetric.** Outward-flanker crowding (farther from fixation) is
  stronger than inward; foveal crowding is weaker; upper-visual-field
  crowding is stronger than lower. He, Cavanagh & Intriligator (1996)
  noted the vertical asymmetry and argued it reflects an attentional
  rather than strictly retinal limit.

Bouma's 1970 paper is the citation; the modern canonicalisation — that
Bouma's law generalises across object kinds and that b ≈ 0.5 corresponds
to a specific cortical scale — is largely due to Pelli's 2000s programme.

## Where Crowding Sits in Reading

Crowding, not acuity, is the primary visual bottleneck on how much of a
line a reader takes in from a single fixation. Pelli, Tillman, Freeman, Su,
Berger & Majaj (2007), "Crowding and eccentricity determine reading rate"
(*Journal of Vision* 7(2):20), showed that across conditions of size,
spacing, central and peripheral, ordered and scrambled, reading rate is
proportional to the **uncrowded span** — the number of letters, at the
relevant vertical eccentricity, that fall outside each others' critical
spacing.

The fovea covers ~2° of visual angle, ~7–9 Latin characters at normal
reading distance. Beyond that, acuity is still adequate to resolve letters
— but the letters sit inside each others' crowding zones and cannot be
identified in parallel. The perceptual span in reading (Rayner's term;
see `./legibility-vs-readability.md`) is bounded asymmetrically at ~14–15
character spaces right of fixation in alphabetic LTR reading, not because
the letters are too small but because they are crowded. This is why
reading proceeds by saccades of ~7–9 characters rather than whole-line
snapshots, and why peripheral reading — critical for readers with macular
degeneration — is so much slower than foveal reading even after target
size is scaled up (Chung 2002; Legge 2007).

## The Modern Theoretical Programme

A short list of papers defines the post-2000 crowding literature.

- **Pelli, Palomares & Majaj (2004)**, "Crowding is unlike ordinary
  masking," *J. Vision* 4(12):12. Seminal modern paper. Crowding and
  masking are distinct: masking elevates detection thresholds; crowding
  elevates identification thresholds while leaving detection intact.
  Reports a diagnostic "two-flanker independence" test and shows that
  crowding's spatial extent is proportional to eccentricity and
  independent of flanker size, contrast, font, and flanker number
  beyond ~2.
- **Pelli, Tillman, Freeman et al. (2007)**, "Crowding and eccentricity
  determine reading rate," *J. Vision* 7(2):20. Reading rate is
  proportional to the uncrowded visual span at each vertical
  eccentricity, across central and peripheral conditions. This is the
  dominant contemporary account of why reading rate varies with
  typographic manipulations.
- **Pelli (2008)**, "Crowding: a cortical constraint on object
  recognition," *Current Opinion in Neurobiology* 18(4):445–451. Broader
  synthesis. Crowding's critical spacing maps onto a roughly constant
  cortical distance (~6 mm radial, ~1 mm circumferential in V1); the
  eccentricity dependence in the visual field is largely the retinotopic
  mapping of a fixed cortical "combining field."
- **Levi (2008)**, "Crowding — an essential bottleneck for object
  recognition: a mini-review," *Vision Research* 48(5):635–654.
  Complementary synthesis. Reviews psychophysics, candidate mechanisms,
  and clinical relevance (amblyopia, macular degeneration, developmental
  dyslexia).
- **Martelli, Majaj & Pelli (2005)**, "Are faces processed like words?"
  *J. Vision* 5(1):6. Applies the critical-spacing test to faces and
  shows that faces, like words, are recognised by parts rather than as
  holistic templates. Refutes the view that crowding is letter-specific:
  the same geometry limits face recognition and visual search.
- **He, Cavanagh & Intriligator (1996)**, "Attentional resolution and the
  locus of visual awareness," *Nature* 383:334–337. Earlier but still
  influential. Argues the crowding resolution limit reflects the spatial
  resolution of attention rather than a purely low-level integration.
  The upper-field/lower-field asymmetry fits attentional accounts better
  than V1-anatomy accounts.

## Candidate Mechanisms

The mechanism of crowding remains partially open; the competing theories
converge on a mid-level cortical pooling stage.

- **Inappropriate feature integration** (Pelli and colleagues) — the
  dominant account. Features are detected veridically in early cortex but
  then integrated over a receptive-field-like zone that grows with
  eccentricity. When multiple objects fall inside one integration zone,
  their features are pooled and attribution fails. Identification breaks
  while detection succeeds.
- **Surround suppression in V1/V2/V4** — older low-level account.
  Suppression contributes but does not predict that identification
  suffers while detection is intact, nor that critical spacing is
  proportional to eccentricity in degrees rather than millimetres of
  cortex.
- **Attentional resolution** (He, Cavanagh & Intriligator 1996) —
  crowding reflects the spatial resolution of voluntary attention;
  attention cannot zoom below a certain angular scale, which grows with
  eccentricity. Explains upper-vs-lower-field asymmetries.
- **Mid-level combining fields** (modern refinement) — imaging work
  locates the substrate in V2–V4 rather than V1. Individual differences
  in crowding distance correlate with V4 surface area, consistent with
  crowding as mid-level pooling beyond early orientation filtering.

For typography-facing conclusions, the detail matters less than two
invariants: critical spacing scales with eccentricity, and identification
(not detection) is what fails.

## Factors That Increase Crowding

- **Flanker proximity.** The primary factor, by Bouma's law. Any
  reduction in target-to-flanker spacing below the critical distance
  (~0.5 × eccentricity) triggers crowding. Set typographically by
  letter-spacing, type-design sidebearings, and — at the line level — by
  leading and x-height interacting with vertical glyph extent.
- **Flanker similarity.** Same category, same contrast polarity, same
  font, same case, same colour — all increase crowding. Chung & Mansfield
  (2009) showed that reversing contrast polarity between target and
  flanker reduces but does not eliminate crowding. The feature-
  integration account predicts this directly: more overlapping features
  means more pooling error.
- **Eccentricity.** Crowding scales with distance from the fovea. At 10°
  eccentricity a reader needs ~5° between letters to identify them
  individually — impossible for running text.
- **Number of flankers.** One flanker < two flankers; beyond ~2 flankers
  the effect saturates (Pelli, Palomares & Majaj 2004). Running text is
  effectively worst-case: every letter has flanks on both sides.
- **String length.** The reader's uncrowded span is bounded by the most-
  crowded point. Long dense words with flanks on both sides are harder
  than equivalent letters near line ends or in short words.
- **Task similarity.** Crowding is stronger when target and flankers
  belong to the same task category (letters among letters) than
  heterogeneous (a letter among symbols). This drives the ALL-CAPS
  penalty (§ below).

## Factors That Reduce Crowding

- **Increased spacing.** The direct lever. Every study that increases
  letter-spacing within the range tested by Zorzi et al. (2012) and
  Perea et al. (2012) — roughly +2.5% to +7% of font size — reports
  reduced crowding-limited errors. The benefit is non-monotonic: past
  some point, looser spacing costs reading *rate* because the eye
  saccades further for the same number of letters. Chung (2002) showed
  for central reading that peak rate sits near the standard spacing;
  looser than standard degrades rate even as it reduces crowding.
- **Distinguishing visual features.** Different contrast polarity (Chung
  & Mansfield 2009), different colour, different font, heavier weight,
  bolder outline — any feature-dimension separation between target and
  flankers reduces crowding. This is part of why syntax-highlighted code
  reads more fluently: the colour dimension partitions tokens into
  non-interacting visual categories.
- **Pre-cueing target location.** Attention to the target's position
  before presentation reduces crowding (He, Cavanagh & Intriligator
  1996; Yeshurun and others). Consistent with the attentional-resolution
  account: attention shrinks the integration window around the attended
  location.
- **Familiarity / expertise.** High-frequency words, native-language
  stimuli, frequently-seen layouts produce smaller crowding costs.
  Martelli, Majaj & Pelli (2005) report ~1.5× sensitivity gain for
  familiar over unfamiliar stimuli, independent of eccentricity.
  Familiarity discounts identification cost but does not eliminate
  crowding.

## Typographic Implications

Crowding explains several typographic levers that practitioners already
use. The value of the research-survey is to make the mechanism legible — and
therefore to predict where intuitions break.

### Letter-spacing / tracking

The most direct lever. Adequate spacing keeps letters outside each others'
critical-spacing zones. Excessive tightening at small body sizes raises
crowding-limited errors and lowers reading rate; excessive loosening
lengthens saccades and weakens word grouping, also lowering rate.

Well-designed fonts' default spacing is generally close to optimal for
body text at the sizes the font was designed for. At small UI sizes
(~11–13px on high-DPI), small positive tracking (~+1% to +2% of em,
`letter-spacing: 0.01em`–`0.02em`) often helps slightly because
rendering tends to tighten whitespace at small sizes. At display sizes
(>~24px), negative tracking is often fine because display-size text is
foveally resolved and the crowding cost of tightening is small relative
to the aesthetic gain.

This is not a licence to tighten body text "for density." Tightening
body harms the crowding-limited reading where the margin is tightest.
Both classical (Tinker) and modern (Chung 2002) evidence is that
well-spaced body text reads faster.

### ALL-CAPS

ALL-CAPS running text is read reliably more slowly than mixed-case. The
folklore number is 30%; the empirical literature places the cost at
roughly **13–20%** depending on size, font, and task (Tinker 1963; Paap,
Newsome & Noel 1984; Larson 2004; Arditi & Cho 2007). The older
explanation — that all-caps destroys "word shape" — is no longer
consensus; see `./word-shape-vs-parallel-letter.md`. Modern explanations
converge on interacting causes, with crowding leading:

- **Higher inter-letter similarity.** All-caps letters occupy a more
  uniform rectangle (same height, few ascenders/descenders to
  disambiguate silhouette) and share more low-level features. By the
  flanker-similarity rule, uniform rectangles produce more crowding than
  mixed lowercase at the same physical spacing. Fiset et al. (2008)
  showed uppercase identification relies more on line terminations while
  lowercase exploits more distinct features.
- **Wider footprint per letter.** Capitals occupy more horizontal space
  at the same em, reducing the usable uncrowded-span window.
- **Lower familiarity.** Skilled readers have far more lowercase
  practice; Martelli-style familiarity gains are smaller for all-caps
  simply because it is read less.

Consequence: **ALL-CAPS labels benefit from positive tracking.** The
common recipe — `letter-spacing: 0.05em` for all-caps UI labels, with
0.04–0.1em the practical range — exists for sound reasons. Display
all-caps at large sizes is less crowding-limited and can tolerate
tighter tracking.

### Serif vs sans-serif

No consistent crowding advantage for either at body sizes. Serifs can
act as disambiguating landmarks (extra features that help attribute
strokes to glyphs) or as additional clutter that expands the feature
field of each glyph. Which wins depends on the font, size, and
rendering. At body sizes on modern high-DPI displays, differences
between well-designed serif and sans-serif fonts are small on reading-
speed and comprehension measures (Dyson 2004; Larson 2004; Legge &
Bigelow 2011). The crowding literature does not single out serifs as
beneficial or harmful.

### Font weight

Bolder weights produce slightly worse crowding at small body sizes
because thicker strokes leave less negative space between glyphs, so
pooling has more overlap to resolve. Regular/Medium typically read
fastest for body prose. Bold is a signalling tool; setting everything
bold has no crowding benefit and costs the emphasis affordance.

### X-height

High x-height makes more of each letter visible inside the crowded
region, which helps identification at small sizes — more diagnostic
feature falls into the uncrowded core. Up to a point. At extreme
x-heights, ascenders and descenders compress toward cap-height and
silhouette differences between letters like `h`/`n` or `d`/`a`
disappear, so crowding gets worse. This is a U-shape: moderately high
x-height is best; both very low and very high are worse. No study
publishes a single optimum because it interacts with everything else.

### Measure

Measure interacts with crowding through saccade economics and line-
return errors rather than intra-line crowding per se. But the effects
compound: a very long line (>85 CPL) with tight tracking and dense
body is crowding-limited at fixation and return-error-prone at line
breaks. Short measures (<45 CPL) force more line breaks and more
regressions. See `../techniques/measure.md`; crowding is one reason the
CPL range (~45–75) matters at all.

## Crowding and Dyslexia

Crowding is the most rigorously investigated visual-level account of
dyslexia. The research-survey is not unanimous, but the evidence supports two
claims: (1) many dyslexic readers show measurably larger crowding zones
than age-matched controls, and (2) interventions that reduce crowding
produce the most robust reading improvements in this population of any
purely typographic lever.

**Magnocellular / visual-processing theories.** Stein (2001) and
Livingstone, Rosen, Drislane & Galaburda (1991) argued dyslexia reflects
a magnocellular abnormality that would predict hyper-crowding and
abnormal attentional narrowing. The strong form (a universal
magnocellular deficit) does not survive the evidence; the weaker form (a
subset of dyslexic readers show visual-attention / crowding anomalies)
has consistent support.

**Empirical crowding asymmetries.** Martelli, Di Filippo, Spinelli &
Zoccolotti (2009), "Crowding, reading, and developmental dyslexia"
(*J. Vision* 9(4):14), tested 29 Italian dyslexics and 33 age-matched
controls; dyslexics had larger critical spacing and critical spacing
predicted 40% of the variance in reading speed in the dyslexic group.
Moores, Cassim & Talcott (2011), "Adults with dyslexia exhibit large
effects of crowding…" (*Neuropsychologia* 49(14):3881–3890), showed
dyslexic adults were disproportionately slowed by closely-spaced
distractors, particularly in the left visual field. Multiple follow-ups
replicate enlarged crowding zones in dyslexic samples, with effect
sizes modest at the individual level but consistent across studies.

**Spacing interventions.** Zorzi, Barbiero, Facoetti et al. (2012),
"Extra-large letter spacing improves reading in dyslexia" (*PNAS*
109(28):11455–11459), tested Italian and French dyslexic children and
reported a ~20% reading-speed gain and ~50% error reduction with
increased letter spacing — on the fly, without training. The effect was
specific to the dyslexic group; non-dyslexic controls showed no gain and
no deficit. Perea, Panadero, Moret-Tatay & Gómez (2012), "The effects of
inter-letter spacing in visual-word recognition…" (*Learning and
Instruction* 22(6):420–430), found converging Spanish evidence: slight
spacing increases helped adult skilled readers, more so Grade 2–4
children, most of all dyslexic readers. The Zorzi effect size is at the
upper bound of published results; a PNAS critical commentary by Skottun
& Skoyles (2012) argued it is partially specific to the sample and
spacing values tested. The direction replicates; magnitude varies.

**Practical upshot.** Spacing-based interventions for dyslexia have
stronger and more replicable evidence than dyslexia-specific fonts. See
`../accessibility/dyslexia.md`. A well-set sans-serif with +0.05em–
+0.12em letter-spacing replicates most of the measurable benefit of
dyslexia-labelled fonts (OpenDyslexic, Dyslexie) without their letter-
form trade-offs.

## Crowding in Non-Latin Scripts

Bouma's law is not Latin-specific; it appears in every script examined,
but the coefficient, the asymmetries, and the interactions with script-
specific structure vary.

**Chinese / CJK.** Zhang, Zhang, Xue, Liu & Yu (2009), "Legibility of
Chinese characters in peripheral vision and the top-down influences on
crowding" (*Vision Research* 49:44–53), measured critical spacing for
Chinese characters and reported a scaling factor of ~0.23–0.37 depending
on criterion and measure. Chinese characters are more complex visual
units than Latin letters, so two kinds of crowding operate: *external*
(between-character) and *internal* (within-character, among strokes and
radicals inside one character). Internal crowding is sensitive to stroke
density and character complexity, which is why some complex traditional
characters crowd more severely than simplified counterparts at small
sizes. A meaningful constraint on minimum sizes and tracking for CJK
body text.

**Arabic.** Arabic is cursive: letters in the same word are connected,
taking one of four contextual forms (isolated, initial, medial, final).
Intra-word "spacing" is effectively fixed by letter design; CSS
`letter-spacing` breaks the cursive join. Crowding still operates, but
the relevant unit is often the word or the connected-glyph cluster
rather than the single letter. Research on Arabic crowding is thinner
than Latin; see `../scripts/arabic.md`.

**Devanagari.** Stacked conjuncts, vowel signs (matras) positioned
above/below/left/right of the base consonant, and the shirorekha (head
line) create a crowding profile with no Latin analogue: above-baseline
matras interact with the shirorekha; below-baseline matras interact
with descender-space elements. See `../scripts/devanagari.md`. Generic
Latin "letter-spacing" tools do not map cleanly.

**Cross-script generalisation.** Bouma's law replicates in structure
across scripts. The coefficient, asymmetries, and interactions with
script-specific layout do not. Typographic recipes derived on Latin
data do not automatically transfer.

## Crowding, Low Vision, and Aging

**Macular degeneration / central-vision loss.** Patients must read with
peripheral retina, where crowding is severe. Peripheral reading rates
are typically 5–10× slower than foveal, limited by crowding not acuity
(Legge 2007; Chung 2002). MNREAD (Legge and colleagues) measures
reading acuity and speed under exactly the conditions where crowding is
binding, and is standard in low-vision clinical practice. Fonts designed
for macular degeneration (Maxular Rx, Eido) aim at reducing inter-letter
crowding via increased sidebearings and simplified letterforms; evidence
is partial and improving.

**Amblyopia.** Amblyopic eyes show elevated foveal crowding even after
acuity correction. Levi (2008) reviews the literature. Reinforces the
independence of crowding and acuity.

**Aging.** Crowding zones expand modestly with age. Scialfa et al.
(2013, "Aging and visual crowding," *J. Gerontology B* 68:522–528) and
later work (Kalpadakis-Smith et al.; Stuart et al.) show older adults
exhibit larger crowding zones, particularly peripherally; foveal
crowding is comparatively preserved. Meaningful for reading at small
body sizes and on low-DPI screens. "Make the text bigger for older
readers" is cruder than it appears — spacing matters at least as much.

## Measuring Crowding

Three measurement families dominate.

- **Psychophysical letter-identification thresholds.** Present a target
  (letter, Landolt C, Gabor) at fixed eccentricity with flankers at
  varying spacing; measure accuracy vs spacing; estimate critical
  spacing at a criterion (often 75%). Scale-invariant in the visual
  field; gives precise per-observer, per-eccentricity characterisation.
- **Reading-rate measures.** MNREAD (Legge et al.), IReST
  (Trauzettel-Klosinski & Dietz 2012, *IOVS*), RSVP reading. Reading
  rate as a function of spacing traces a characteristic curve — sharp
  rise from tight spacing to a plateau near the standard, slow decline
  at very loose spacing — that crowding models predict.
- **Eye-tracking.** First-fixation and gaze durations, regression
  rates, saccade-length distributions all move under crowding
  manipulations: fixation durations lengthen and regressions increase
  when tracking is reduced below optimal. Same dependent measures as
  Rayner-style reading research-survey; the crowding contribution is to use
  tracking as the manipulated variable and interpret results through
  the uncrowded-span model (Pelli, Tillman et al. 2007).

For typographic practice, the relevant measure is almost always the
reading-rate curve as a function of letter-spacing.

## Practical Recommendations

- **Do not tighten body text for density.** Negative tracking on body
  prose moves letters closer to neighbours' crowding zones; measurable
  cost at small sizes and on non-high-DPI displays is higher
  misidentification and slower reading. "Density" belongs to measure,
  leading, and size — not tracking.
- **Do not over-loosen body text.** Beyond roughly font default plus a
  few percent, reading rate falls because the eye traverses a longer
  physical line for the same number of letters and word-grouping
  weakens. Body-prose sweet spot is near the type designer's defaults.
- **At small UI sizes, consider mild positive tracking.** 0.01em–0.02em
  (~+1–2% of em) can improve legibility on screens where rendering has
  tightened whitespace below intended values. Font-dependent; test
  against the specific font and rendering.
- **Track ALL-CAPS labels more loosely than mixed-case.** All-caps is
  crowding-worst-case: `letter-spacing: 0.05em` is the common anchor;
  0.04em–0.1em the practical range. Display all-caps at >24px can
  tolerate tighter tracking.
- **Support user-adjustable letter-spacing for accessibility.** WCAG
  2.2 SC 1.4.12 "Text Spacing" (AA) requires content not break when
  users apply `letter-spacing` of at least 0.12 × font-size (plus
  specified line/word/paragraph spacing). Avoid fixed-height containers
  for text, avoid container-clipped ellipses on critical content, and
  verify lines do not over-run bounds when spacing increases.
- **For dyslexia-focused surfaces, use spacing first, font choice
  second.** +0.05em to +0.12em letter-spacing combined with 1.5–2.0
  line-height and 60–75 CPL measure is the best-supported intervention
  set (Zorzi et al. 2012; Perea et al. 2012; see
  `../accessibility/dyslexia.md`). Dyslexia-specific fonts do not
  replicate the effect when spacing is controlled.
- **For CJK, do not apply Latin spacing recipes directly.** CJK
  character spacing defaults come from Han character-grid conventions
  and CJK rendering. Prefer CJK-specific tools (`text-spacing-trim`,
  half-width/full-width punctuation) rather than generic
  `letter-spacing`.
- **For Arabic, do not apply `letter-spacing` at all by default.**
  Cursive connection means `letter-spacing` breaks joined glyphs. Use
  word-spacing and line-spacing, or font-level spacing metrics tuned
  for Arabic by the foundry.

## What Crowding Does Not Explain

It is easy — and wrong — to attribute too much to crowding.

- **Acuity-limited reading at very small sizes.** Below the critical
  print size (Legge 2007), the binding constraint is acuity itself,
  not crowding.
- **Word-level semantic effects.** Frequency, predictability, and
  context effects are cognitive and lexical, not perceptual. Crowding
  is a perceptual integration limit; it does not account for why a
  high-frequency word is read faster than a low-frequency one of equal
  visual difficulty.
- **Regression rates at line breaks.** Regressions from losing the
  next line's start (Tinker; Dyson 2004) are an oculomotor problem of
  measure and leading; crowding is not the relevant mechanism.
- **Comprehension.** Crowding limits *identification* rate.
  Conflating crowding gains with comprehension gains is a common
  overclaim.

## Open Questions

- **Exact cortical locus.** V2, V4, or both? Recent imaging correlates
  crowding distance with V4 surface area; generalisation to all
  crowding kinds is not complete.
- **Learning and plasticity.** Can crowding be reduced by targeted
  perceptual learning to a clinically useful degree? Lab training
  effects exist (Chung 2007; Yehezkel, Sterkin, Lev & Polat 2015);
  real-world transfer is partial.
- **Coefficient variation.** Zhang et al. (2009) report ~0.23 for
  Chinese; Latin clusters around ~0.5. Whether this reflects
  characters-vs-letters as the unit of analysis, or something else,
  is unsettled.
- **Variable-font axes and crowding.** Variable fonts with
  width/weight/opsz axes ought to let designers tune crowding per size
  and density, but published eye-tracking data on variable-font
  crowding effects in running reading is sparse.
- **Screen rendering interactions.** Subpixel antialiasing, grayscale
  rendering, and contrast amplification interact with crowding at
  small sizes in ways the lab literature does not fully simulate.

## Sources

### Primary crowding science

- Bouma, H. (1970). "Interaction effects in parafoveal letter
  recognition." *Nature* 226: 177–178.
  https://www.nature.com/articles/226177a0
- Pelli, D. G., Palomares, M., & Majaj, N. J. (2004). "Crowding is
  unlike ordinary masking: Distinguishing feature integration from
  detection." *Journal of Vision* 4(12): 12, 1136–1169.
  https://jov.arvojournals.org/article.aspx?articleid=2192655
- Pelli, D. G., Tillman, K. A., Freeman, J., Su, M., Berger, T. D., &
  Majaj, N. J. (2007). "Crowding and eccentricity determine reading
  rate." *Journal of Vision* 7(2): 20.
  https://jov.arvojournals.org/article.aspx?articleid=2122073
- Pelli, D. G. (2008). "Crowding: A cortical constraint on object
  recognition." *Current Opinion in Neurobiology* 18(4): 445–451.
  https://doi.org/10.1016/j.conb.2008.09.008
- Levi, D. M. (2008). "Crowding — An essential bottleneck for object
  recognition: A mini-review." *Vision Research* 48(5): 635–654.
  https://doi.org/10.1016/j.visres.2007.12.009
- Martelli, M., Majaj, N. J., & Pelli, D. G. (2005). "Are faces
  processed like words? A diagnostic test for recognition by parts."
  *Journal of Vision* 5(1): 6. https://doi.org/10.1167/5.1.6
- He, S., Cavanagh, P., & Intriligator, J. (1996). "Attentional
  resolution and the locus of visual awareness." *Nature* 383:
  334–337. https://www.nature.com/articles/383334a0

### Spacing, reading, and dyslexia

- Zorzi, M., Barbiero, C., Facoetti, A., Lonciari, I., Carrozzi, M.,
  Montico, M., Bravar, L., George, F., Pech-Georgel, C., & Ziegler, J.
  C. (2012). "Extra-large letter spacing improves reading in
  dyslexia." *PNAS* 109(28): 11455–11459.
  https://doi.org/10.1073/pnas.1205566109
- Perea, M., Panadero, V., Moret-Tatay, C., & Gómez, P. (2012). "The
  effects of inter-letter spacing in visual-word recognition: Evidence
  with young normal readers and developmental dyslexics." *Learning
  and Instruction* 22(6): 420–430.
  https://doi.org/10.1016/j.learninstruc.2012.04.001
- Martelli, M., Di Filippo, G., Spinelli, D., & Zoccolotti, P. (2009).
  "Crowding, reading, and developmental dyslexia." *Journal of Vision*
  9(4): 14. https://doi.org/10.1167/9.4.14
- Moores, E., Cassim, R., & Talcott, J. B. (2011). "Adults with
  dyslexia exhibit large effects of crowding, increased dependence on
  cues, and detrimental effects of distractors in visual search
  tasks." *Neuropsychologia* 49(14): 3881–3890.
  https://doi.org/10.1016/j.neuropsychologia.2011.10.005
- Chung, S. T. L. (2002). "The effect of letter spacing on reading
  speed in central and peripheral vision." *IOVS* 43(4): 1270–1276.
  https://pubmed.ncbi.nlm.nih.gov/11923275/
- Chung, S. T. L., & Mansfield, J. S. (2009). "Contrast polarity
  differences reduce crowding but do not benefit reading performance
  in peripheral vision." *Vision Research* 49(23): 2782–2789.

### Low vision, aging, and clinical

- Legge, G. E. (2007). *Psychophysics of Reading in Normal and Low
  Vision.* Lawrence Erlbaum. https://legge.psych.umn.edu/book
- Scialfa, C. T., Cordazzo, S., Bubric, K., & Lyon, J. (2013).
  "Aging and visual crowding." *Journals of Gerontology B* 68(4):
  522–528. https://pubmed.ncbi.nlm.nih.gov/23009956/

### Case, script, and related

- Fiset, D., Blais, C., Éthier-Majcher, C., Arguin, M., Bub, D., &
  Gosselin, F. (2008). "Features for identification of uppercase and
  lowercase letters." *Psychological Science* 19: 1161–1168.
  https://doi.org/10.1111/j.1467-9280.2008.02218.x
- Arditi, A., & Cho, J. (2007). "Letter case and text legibility in
  normal and low vision." *Vision Research* 47(19): 2499–2505.
- Paap, K. R., Newsome, S. L., & Noel, R. W. (1984). "Word shape's in
  poor shape for the race to the lexicon." *J. Experimental
  Psychology: HPP* 10: 413–428.
- Larson, K. (2004). "The Science of Word Recognition." Microsoft
  Typography.
  https://docs.microsoft.com/en-us/typography/develop/word-recognition
- Zhang, J.-Y., Zhang, T., Xue, F., Liu, L., & Yu, C. (2009).
  "Legibility of Chinese characters in peripheral vision and the
  top-down influences on crowding." *Vision Research* 49(1): 44–53.
  https://doi.org/10.1016/j.visres.2008.08.024

### Standards and practitioner references

- W3C WAI. "Understanding Success Criterion 1.4.12: Text Spacing."
  WCAG 2.2 Understanding.
  https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html

### Peer files

- [./legibility-vs-readability.md](./legibility-vs-readability.md) —
  umbrella reference; this file extends its "Crowding" section.
- [./word-shape-vs-parallel-letter.md](./word-shape-vs-parallel-letter.md)
  — why ALL-CAPS is not explained by "word-shape loss."
- [../accessibility/dyslexia.md](../accessibility/dyslexia.md) —
  dyslexia-specific fonts; spacing interventions here are its
  strongest empirical anchor.
- [../accessibility/wcag-type.md](../accessibility/wcag-type.md) —
  WCAG 2.2 SC 1.4.12 Text Spacing and related criteria.
- [../techniques/measure.md](../techniques/measure.md) — CPL and line
  length; interacts with crowding through saccade economics.
- [../scripts/arabic.md](../scripts/arabic.md) — why `letter-spacing`
  is not a valid Arabic lever.
- [../scripts/devanagari.md](../scripts/devanagari.md) — crowding
  profile of stacked conjuncts and matras.
