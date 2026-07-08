---
date: 2026-04-17
coverage: medium
peers:
  - ./crowding.md
  - ./word-shape-vs-parallel-letter.md
  - ./optical-size-research.md
  - ../techniques/measure.md
  - ../accessibility/dyslexia.md
primary_sources:
  - https://docs.microsoft.com/en-us/typography/develop/word-recognition  # Larson, "The Science of Word Recognition", Microsoft Typography, 2004
  - https://www.jneurosci.org/content/22/19/RC221  # Pelli, Palomares, Majaj-adjacent crowding literature in J. Neurosci.
  - https://jov.arvojournals.org/article.aspx?articleid=2192635  # Pelli, Palomares, Majaj, "Crowding is unlike ordinary masking", J. Vision 4(12):12, 2004
  - https://pubmed.ncbi.nlm.nih.gov/9849112/  # Rayner, "Eye movements in reading and information processing: 20 years of research-survey", Psych. Bulletin 124(3), 1998
  - https://doi.org/10.1177/1529100615623267  # Rayner, Schotter, Masson, Potter, Treiman, "So much to read, so little time", Psychological Science in the Public Interest 17(1), 2016
  - https://doi.org/10.1080/00140139.2004.11953001  # Dyson, "How physical text layout affects reading from screen", Behaviour & Information Technology 23(6), 2004
  - https://pubmed.ncbi.nlm.nih.gov/28165590/  # Galliussi et al., meta-analytic review touching dyslexia fonts
  - https://doi.org/10.1371/journal.pone.0240242  # Wery & Diliberto / Kuster et al. Dyslexie font evaluation (null/weak readability effects)
  - https://www.informationdesignjournal.org/  # IDJ — Sofie Beier publication venue
  - https://link.springer.com/article/10.3758/BRM.41.4.1149  # Legge & Bigelow, "Does print size matter for reading? A review of findings from vision science and typography", J. Vision 11(5):8, 2011
  - https://pubmed.ncbi.nlm.nih.gov/12613669/  # Sheedy et al., fonts and fatigue / accommodative load
  - https://archive.org/details/legibilityofprin0000tink  # Tinker, Legibility of Print (1963) — archive
notes:
  - Peer files (./crowding.md, ../techniques/measure.md, etc.) may not yet exist on disk; cross-references are forward-looking per the skill's planned structure.
  - This file is tier=medium: cite where evidence is strong, hedge where it is contested, and avoid manufacturing numeric precision the literature does not support.
---

# Legibility vs Readability

In everyday speech and in most typography writing, "legibility" and "readability"
are used interchangeably. In the reading-science literature they are not the
same thing, they are measured differently, and they can move in opposite
directions within the same typeface. A font can be highly legible (easy to
identify each glyph) and poorly readable (tiring or slow for long-form prose),
and vice versa. The distinction matters whenever someone is asked to evaluate a
typeface, tune a running-text setting, justify a dyslexia-specific font, or
decide whether a "readability improvement" claim is supported by evidence.

This note summarises how the experimental literature draws the line between the
two, what each phenomenon is measured with, which research-survey programs have
shaped current consensus, and — importantly — which widely repeated
typographic claims the evidence either does not support or actively
contradicts. It does not pick a "best font." The literature doesn't support
that kind of verdict, and part of the job of this file is to make that
restraint visible.

## Definitions

The cleanest definitions come from vision science rather than from design
writing.

**Legibility** is a glyph-level property: how easily and quickly a reader
correctly identifies a single character, or distinguishes between a pair of
characters that could be confused. It is a property of letter forms and of the
conditions under which they are viewed — size, distance, contrast, rendering,
crowding, visual field position. It applies equally to any script, though
nearly all of the rigorous experimental work has been done on the Latin
alphabet, with smaller bodies of research-survey on Arabic, Hebrew, and CJK.

Legibility is routinely framed in terms of **letter confusability**. A well
studied set in Latin includes the "I l 1", "O 0", "b d p q", "rn / m",
"cl / d", and "vv / w" pairs. At small sizes, at low pixel densities, or
inside crowded strings, confusability is the dominant failure mode.

**Readability** is a text-level property: how efficiently and comfortably a
reader extracts meaning from connected, running text over time. Readability is
a property of the page (or screen), not of a single glyph — it depends on
font, size, weight, tracking, measure (characters per line), leading, colour,
background, rendering, reading medium, purpose of reading, and the reader's
expertise with the content and the script. It is explicitly about
comprehension and effort over sustained reading, not about naming an isolated
letter. Tinker (1963) already used this contrast, though under slightly
different terminology; modern usage follows roughly the Legge & Bigelow (2011)
framing.

The two are related but dissociable. High legibility is usually necessary for
high readability — if the reader cannot identify letters, they cannot read —
but it is not sufficient. Some fonts that are very legible at the glyph level
(e.g. Comic Sans, most "dyslexia-friendly" fonts) are not demonstrably more
*readable* for long-form text, because readability at the paragraph level is
constrained mostly by spacing, measure, rhythm, and word-level processing, not
by disambiguating individual glyphs.

## How Each Is Measured

### Legibility

Experimental psychology measures legibility with **letter-identification
tasks** under constrained viewing:

- **Tachistoscopic presentation / threshold SOA (stimulus-onset asynchrony).**
  A single letter is flashed for a very short duration, often followed by a
  mask. Accuracy is measured as a function of exposure time. The shorter the
  SOA at which accuracy is reliably above chance, the more legible the
  letter. Variants of this paradigm go back to Cattell (1886) and are still
  used.
- **Contrast threshold.** Stimuli are presented at reduced contrast; the
  contrast level at which identification falls to chance indexes legibility.
- **Crowding tasks.** A target letter is flanked by distractor letters; the
  minimum flanker spacing at which the target is still identifiable measures
  peripheral (and foveal) crowding.
- **Distance / acuity threshold.** The smallest angular size at which a letter
  is correctly named ("critical print size"). Legge and colleagues (e.g.
  Legge & Bigelow 2011) use this extensively.
- **Confusion matrices.** Participants report letters under noise or
  low-contrast conditions, and the error pattern is tabulated. This is how
  classical confusability pairs were formalised (see Bouma's 1971 letter
  confusion work).

Beier (2012, *Reading Letters*) extended these paradigms systematically across
sans-serif designs, showing that specific glyph-shape decisions — aperture
openness, terminal shape, ascender/descender length — measurably shift
identification thresholds for the letters they affect.

### Readability

Readability is measured at a different scale and with different tools:

- **Reading speed.** Words per minute or characters per minute on a passage,
  sometimes combined with comprehension scoring to penalise speed-accuracy
  trade-offs.
- **Comprehension scores.** Post-reading questions on passage content.
- **Eye-tracking.** First-fixation duration, gaze duration, total fixation
  time per word, saccade length, regression rate (backwards saccades),
  skipping rate. This is the methodology most associated with Rayner and
  colleagues from the 1970s onward. It is the canonical evidence base for
  what changes when text is "easier" or "harder" to read.
- **Subjective fatigue.** Self-reports of tiredness, strain, discomfort, often
  combined with objective measures of blink rate, accommodation, or
  symptomatic eye strain after sustained reading. Sheedy and colleagues at
  the Pacific University Vision Performance Institute have worked in this
  register.
- **Critical print size and reading acuity.** The smallest letter size at
  which reading speed reaches its asymptotic maximum. Introduced by Legge,
  Pelli, Rubin, Schleske (1985) and elaborated in Legge's subsequent work.
  This sits between legibility and readability: it uses running text but
  extracts a threshold size.
- **MNREAD charts.** A standardised test developed by Legge and colleagues;
  widely used clinically.

The two measurement regimes are largely non-overlapping. A font change that
moves letter-identification thresholds does not automatically move eye-tracking
regression rate, and vice versa. This is one empirical reason to keep the two
concepts separate.

## Canonical Research Lineage

A short, non-exhaustive lineage of the work that shapes current consensus:

- **Miles Tinker (1930s–1960s).** Large empirical program summarised in
  *Legibility of Print* (1963). Introduced much of the vocabulary
  ("legibility," typographic variables as independent variables) and ran
  hundreds of comparisons of size, leading, measure, type style, colour,
  paper, and combinations thereof. Methodologically it predates modern
  statistical controls, counterbalancing, and eye-tracking, and many specific
  numerical recommendations do not replicate. It is cited chiefly as the
  historical anchor of the field.
- **Keith Rayner and colleagues (1970s–2010s).** The canonical eye-tracking
  program. Rayner's reviews — especially Rayner (1998) *Psychological
  Bulletin* and Rayner, Schotter, Masson, Potter & Treiman (2016) — are the
  reference for how the eye actually moves in reading, what fixations and
  saccades do, and how perceptual span and parafoveal preview work. Nearly
  every contemporary claim about "how reading works" traces back to this
  program.
- **Denis Pelli and colleagues (2000s–).** The modern theory of **crowding**
  — why letters in peripheral and even foveal vision become hard to identify
  when flanked by other letters — is built on Pelli, Palomares & Majaj
  (2004, *Journal of Vision*) and subsequent work. This is arguably the most
  important 21st-century addition to legibility theory for typography. See
  `./crowding.md`.
- **Gordon Legge and colleagues (1980s–).** Low-vision reading and the
  "psychophysics of reading" framework: critical print size, reading acuity,
  MNREAD, and the comparative study of print sizes, contrast, and fonts.
  Legge & Bigelow (2011, *Journal of Vision*) is a particularly useful
  integration for typographers.
- **Kevin Larson and Microsoft Advanced Reading Technologies (2000s).**
  Larson's 2004 essay *The Science of Word Recognition* is the clearest
  short statement of the modern consensus that word recognition proceeds by
  parallel letter recognition, not by whole-word-shape recognition. His
  group also sponsored the Poynter Institute study comparing serif and sans
  readouts on screen, which found no robust comprehension advantage for
  either.
- **Mary C. Dyson (1990s–2010s).** Work on reading from screen, line length,
  scroll vs page presentation, and methodological standards in reading
  research-survey. Dyson (2004, *Behaviour & Information Technology*) is a
  frequently cited review of measure and layout effects on screen.
- **Sofie Beier (2000s–).** *Reading Letters* (2012) and subsequent
  publications systematically link specific letter-shape decisions to
  measurable legibility differences, particularly in sans-serifs. Her work
  is one of the few that bridges type-design practice and experimental
  psychophysics at the glyph level.
- **James Sheedy and Pacific University VPI (2000s–).** Clinical research-survey on
  reading fatigue, accommodative and vergence load, and the ergonomics of
  extended screen reading.
- **Bouma (1971, 1973).** Foundational letter-confusability and
  reading-perception work that anchors later crowding and legibility
  research-survey.

This is a Western/Latin-script-heavy list. Equivalent depth of research-survey does
not exist for most non-Latin scripts; see *Open Questions* below.

## The Word-Shape Debate

A persistent claim in design writing, especially older writing, is that
readers recognise whole **word shapes** — the "bouma" silhouette of
ascenders, descenders, and x-height — rather than individual letters, and
that this is why lowercase is more readable than ALL CAPS.

Historically, this idea goes back to James Cattell's 1886 experiments
suggesting whole-word superiority at brief exposures, and was reinforced by
later reading-instruction theory (notably Healy and related writers) and the
"bouma" terminology. The image of the word-silhouette "envelope" was widely
taught to designers in the mid-20th century.

The modern consensus, summarised accessibly in Larson (2004) and backed by a
large experimental literature, is that **skilled readers recognise words
primarily through parallel letter recognition**: each letter in the fixation
window is processed roughly in parallel, and word identification follows from
the activated letter identities, not from an outline shape. Word-shape
information exists and contributes, but as a secondary cue, not as the
primary route.

Several lines of evidence converge on this view:

- Word-superiority effects can be reproduced with pseudowords that have no
  learned shape, which would be unexpected if the shape itself were primary.
- Changing individual letter identities (while keeping the outline roughly
  constant) strongly disrupts recognition.
- Eye-tracking shows that fixation on a word scales with letter-level
  difficulty, not just outline complexity.
- Models of visual word recognition that process letters in parallel (e.g.
  interactive-activation models) account for a wide range of reading
  phenomena.

Hedge: the exact weighting of letter vs. word-shape information is still
debated, and some cues like word length or envelope do help parafoveal preview
and word skipping. But "readers read word shapes, not letters" is not a
supportable summary of the literature.

The practical implication for **ALL CAPS** is worth stating carefully,
because the usual explanation is wrong:

- The reason all-caps running text is slower and more tiring is **not that
  the word shape disappears**. That framing presupposes the word-shape
  theory.
- The empirically better explanations are: (1) capital letters have more
  uniform outer contours and fewer distinguishing features (no ascenders or
  descenders to break the rectangle), which increases letter-level
  confusability; (2) letter-width variation is compressed, increasing
  crowding at typical tracking; (3) skilled readers have vastly more
  practice with lowercase prose than with all-caps prose, so all-caps is
  less fluent for reasons of exposure alone. Tinker and others reported the
  reading-speed deficit for all-caps running text as early as the mid-20th
  century; the mechanistic explanation shifted later.

This is a case where the practical advice ("don't set long blocks in
all-caps") is correct but the textbook reason usually given for it is
outdated.

## Crowding

Crowding is the phenomenon in which a target letter that would be easily
identifiable in isolation becomes hard or impossible to identify when it is
flanked by other letters. It is the dominant limit on peripheral reading, and
it constrains foveal reading more than classical theories assumed.

Pelli, Palomares & Majaj (2004, *Journal of Vision*) is the most cited
modern statement. Key points relevant to typography:

- **Crowding is not ordinary masking.** Features of the flankers interfere
  with identification of the target even when the flankers don't overlap it
  visually. It is, in Pelli's framing, a failure of feature integration, not
  a failure of feature detection.
- **Bouma's law** (Bouma 1970): the critical spacing for crowding in the
  peripheral field is roughly half the eccentricity. In practice, the
  visual system tolerates much less space than a designer's naive intuition
  suggests before crowding degrades identification.
- **Foveal crowding is small but non-zero** at normal reading distances, and
  can matter at small body sizes or at tight tracking.

Typographic implications that follow from this literature (not from aesthetic
preference):

- **Letter-spacing (tracking).** Tight tracking compresses glyphs into each
  other's critical-spacing zone. For body text this increases crowding-limited
  errors, especially at small sizes and on low-DPI displays. Conversely,
  setting body text unusually loose costs reading speed because the eye has
  to move further.
- **Measure (characters per line).** While measure is usually discussed in
  terms of saccade-return economics (Tinker's work, Dyson 2004, and others),
  crowding is the reason letter-spacing *within* a line interacts with the
  legibility floor. A very narrow measure at a very tight tracking can fail
  worse than either problem alone.
- **X-height and aperture.** Shapes with more open counters and apertures
  resist crowding better, because their diagnostic features are less likely
  to be integrated with flanker features. This is one of Beier's recurring
  findings.

See `./crowding.md` (peer reference) for the extended treatment.

## What the Evidence Actually Supports

Taking the experimental literature at face value — with appropriate hedging
— the following practitioner-facing guidance is reasonably well supported for
Latin-script long-form prose.

**Size / critical print size.**
- There is a critical print size below which reading speed drops sharply and
  above which it plateaus. For typical adult normally-sighted readers at
  typical distances, the plateau starts around roughly 0.3° of visual angle
  and above — which for a 50–60 cm screen distance corresponds to body sizes
  that most designers already use (roughly 14–18px in CSS for modern screens).
- Legge & Bigelow (2011) give a range; the exact number depends on font,
  reading condition, and individual. Quoting a single pixel value as "the"
  minimum is overclaiming.

**X-height.**
- At a given em-size, higher x-height generally helps legibility, especially
  at small sizes on screen. This is well established for letter-identification
  tasks.
- The effect is not monotonic at all sizes. Extremely high x-height
  proportions compress extenders and reduce the shape differentiation
  between letters like h/n, and can hurt readability in running text. There
  is a practical middle ground; the literature does not give a single
  optimum because it depends on the rest of the design.

**Counter openness / aperture.**
- Open apertures (humanist sans designs) reduce confusability between pairs
  like c/e/o at small sizes compared with closed apertures (geometric
  sans). Beier's work is the clearest source.
- This matters most at interface scales (small UI labels, dense data
  displays) and less at typical body-text screen sizes on a high-DPI display.

**Stroke contrast.**
- Moderate, readable contrast is fine for body text. Extreme-contrast
  display faces (thin-and-thick transitional or Didone designs) suffer at
  small sizes because the thinnest strokes drop below the contrast or
  rendering threshold, especially on lower-DPI displays and in suboptimal
  lighting. This is established in low-vision and screen research-survey and is
  consistent with the contrast-threshold legibility measures.

**Weight.**
- Regular or Book weight is near the reading-optimum for body in most serif
  and sans designs. Very light weights fail at low contrast and low DPI.
- Bold is useful for emphasis but is not "more readable" in continuous
  prose; reading speed for all-bold running text is similar to or slightly
  worse than regular, and the signalling value of bold is lost when
  everything is bold.

**Measure (characters per line).**
- The commonly cited 45–75 CPL range for Latin running prose originates
  partly from Tinker and is consistent with later eye-tracking work. It is a
  *range*, not a target.
- Under ~45 CPL induces more line breaks per paragraph, more return-saccade
  work, and often regressions (Dyson and others).
- Over ~75–85 CPL increases "loss of place" — readers have trouble finding
  the next line's start — and regression rate climbs.
- The exact comfort range depends on font, size, leading, and reader.

**Leading (line-height).**
- For body prose at typical sizes, something near 1.3–1.6× the font size is
  broadly supported, with the upper part of that range more commonly
  recommended for sans-serifs with tall x-height or for wider measures.
- Too tight and lines crowd vertically, which increases misalignment
  saccades and regression.
- Too loose and the paragraph fragments perceptually; comprehension may
  suffer.

**Tracking.**
- Near-default tracking — what the font designer specified — is almost
  always best for body. Tight tracking increases crowding; loose tracking
  slows saccades and weakens word grouping.

**Spacing interventions for struggling readers.**
- Increased letter spacing and line spacing have more empirical support as a
  readability intervention for dyslexic and beginning readers than
  dyslexia-specific font designs do (Zorzi et al. 2012 and follow-ups).
  This is a live area; effect sizes are debated.

**Alignment.**
- Left-aligned (ragged right) Latin text is as readable as or slightly more
  readable than fully justified text when hyphenation and h&j are poor, and
  roughly equivalent when h&j are high-quality. The differences are small.

Everything above is framed for Latin prose at typical adult reading
conditions. It does not automatically transfer to Arabic, CJK, Devanagari, or
any other script with different metric conventions, letter structures, and
reading strategies.

## Common Myths and Where They Came From

A number of claims in the wider typography literature are either unsupported
or weakly supported by the reading-science evidence. Naming them is part of
the job.

**"Serifs guide the eye along the line."**
- Origin: widely repeated in mid-20th-century design writing, partly
  rationalising existing typographic practice.
- Evidence: not supported. Eye-tracking shows saccades skip from fixation
  to fixation over roughly seven to nine characters at a time; the eye does
  not smoothly track along letter bottoms. Rayner's work makes this clear.
  Serifs have legibility effects — plausibly through glyph disambiguation
  and letter spacing — but not via eye-guidance.

**"Sans-serifs are harder to read in long-form."**
- Origin: a mix of print tradition, mid-20th-century studies with serif
  print books as a baseline, and the Poynter study being reported
  ambiguously in the trade press.
- Evidence: weak. Multiple studies, including the Microsoft/Poynter work
  and subsequent comparisons, show no robust comprehension or reading-speed
  advantage for either serifs or sans-serifs at typical sizes on modern
  displays. Preference effects dominate the differences people report. At
  very small or low-DPI sizes, the winner depends on the specific designs.

**"Times New Roman is optimal for reading."**
- Origin: Times and Times New Roman were the Word / default serif for
  decades and became a reference point by exposure.
- Evidence: Times New Roman is a *newspaper* face, designed for narrow
  columns and tight setting. It has high stroke contrast and relatively
  low x-height; at body sizes on screens it tends to be crowding-limited
  compared with screen-optimised text faces like Georgia, Charter, or
  Source Serif. There is no study showing it is generally optimal. It is
  familiar, which is its own small readability asset.

**"Dyslexia-specific fonts objectively improve reading for dyslexic readers."**
- Origin: design-led products (Dyslexie, OpenDyslexic) with strong
  marketing.
- Evidence: weak to null for comprehension and reading speed. Kuster et al.
  (2018, *PLOS ONE*) and subsequent meta-analytic reviews find that
  dyslexia-specific fonts do not produce reliable reading-speed or
  comprehension gains over standard typefaces for dyslexic readers. Some
  small effects show up on letter-level tasks, which is consistent with the
  legibility-vs-readability distinction: the designs target confusable pairs,
  which is a legibility move, but sustained reading is constrained by other
  factors (spacing, measure, familiarity, individual differences).
- What does help, more robustly: larger type, wider letter and line spacing,
  shorter measure, high contrast, and reader control over layout. These are
  general readability interventions, not font-shape interventions.

**"Comic Sans helps dyslexic readers."**
- Origin: an anecdote that some dyslexia advocacy groups picked up.
- Evidence: thin. Comic Sans is relatively legible at the glyph level
  (open apertures, irregular shapes that reduce symmetric confusability),
  which is plausibly why some readers prefer it. Reading-speed and
  comprehension evidence at the passage level is not strong.

**"Centre-aligned body text is fine for long prose."**
- Origin: design preference.
- Evidence: not supported. Inconsistent line-start positions force the eye
  to locate each new line's start with a guided saccade, increasing
  regression rates and slowing reading. Centre-aligning a single-sentence
  display line is fine; centring a paragraph of prose is a readability
  regression.

**"High-contrast (pure black on pure white) is always best."**
- Origin: crude accessibility heuristics.
- Evidence: overstated. Legibility rises with contrast up to a point, but
  extreme contrast on emissive screens in low-light environments is
  associated with higher glare-fatigue reports (Sheedy et al.). Many
  reading apps and OS dark modes exist partly in response to this.
  WCAG-level contrast minima are floors, not targets; exceeding them is
  generally good, but "pure black on pure white" is not the optimum for
  every reading condition.

**"There is a scientifically optimal font."**
- Origin: headline-grabbing studies and marketing copy.
- Evidence: not supported. The literature consistently shows that at
  typical reading sizes and conditions, differences between well-designed
  fonts are small, highly context-dependent, and often swamped by
  individual-reader and task variance.

## Screen vs Print

Reading from screen has accumulated its own body of research-survey, most of it
post-1990, a good deal of it by Mary Dyson and her collaborators, and more
recently by HCI and reading groups across Europe and North America.

Key findings relevant to legibility and readability:

- **Low-DPI screen rendering was historically a meaningful legibility
  handicap.** On screens below ~120 ppi with imperfect hinting, small body
  sizes (roughly below 14px CSS) showed measurable crowding and stroke
  dropout. Hinting systems (TrueType hinting, ClearType, DirectWrite,
  FreeType's subpixel and greyscale modes, Apple's rendering via CoreText)
  mitigate this, each with its own trade-offs. See
  `../contemporary/hinting-and-rendering.md` when that file exists.
- **At ~2× DPI and above**, on modern phones and laptops, the legibility
  gap between typical screen and print largely closes for body sizes.
  Differences that remain are more about rendering decisions (subpixel
  positioning, gamma, contrast amplification) than about fundamental
  optics.
- **Line length (measure) on screen often defaults to too long**, because
  layout engines let text fill the available width. This is one of the
  strongest practical findings from Dyson and others: constrain measure on
  screen, not just in print.
- **Scroll vs paging.** Paged presentations (one screen at a time) tend to
  produce slightly better comprehension than continuous scrolling in some
  studies, particularly for long and complex material; the effect is
  modest and not always replicated.
- **E-ink vs LCD/OLED.** E-ink reduces glare and refresh artifacts and is
  preferred for sustained reading by many readers; comprehension
  differences versus good LCD/OLED are small when confounds are
  controlled. The usual subjective fatigue reports favour e-ink; objective
  reading-speed or comprehension advantages are less clear.
- **Dark mode.** Evidence is mixed. For participants with normal vision in
  well-lit rooms, light backgrounds tend to preserve reading speed
  slightly better. In dim environments, or for readers with specific
  photophobia, dark mode reduces fatigue reports. "Dark mode is better for
  reading" as a universal claim is not supported.

The practical through-line from Dyson's work is that measure, line length,
and layout matter more to screen readability than the choice between serif
and sans-serif, which means typographic attention is better spent there than
on font swapping.

## Open Questions

Several questions remain genuinely unsettled, and the skill should not
pretend otherwise.

- **Is there a robust "font personality" effect on readability beyond
  preference?** Some studies suggest readers perform slightly better with
  fonts they prefer, but it is hard to separate preference from familiarity
  from actual readability. The direction of causation is murky.
- **How much does measure interact with font weight and x-height
  specifically?** There is consensus that CPL matters and that x-height
  matters; the interaction between them, and whether a wider measure
  tolerates a smaller x-height or vice versa, is not crisply characterised.
- **How do variable fonts with an `opsz` (optical size) axis compare to
  multi-cut families (e.g. classical text / display cuts) in eye-tracking
  terms?** There is design-side theory and plausible legibility benefit,
  but the peer-reviewed eye-tracking literature on variable fonts
  specifically is young and sparse.
- **Cross-cultural generalisation.** Almost everything above is Latin-script
  research-survey. Similar-depth work exists for some scripts (e.g. Chinese
  character-recognition research-survey is substantial) but is not as easily
  integrated into typographic practice. For scripts like Arabic (highly
  contextual), Devanagari (complex conjuncts and shirorekha), Thai (no
  word-spacing), and smaller-corpus scripts (Ethiopic, Khmer, Lao), the
  research-survey base is thinner. The safe default is that Latin findings do not
  transfer without re-verification. See the `scripts/` references.
- **Long-term reading and fatigue.** Most experimental sessions are short
  (tens of minutes). Sustained multi-hour reading fatigue, and whether
  typographic choices affect it, is under-studied with modern methods.

## Anti-patterns for Claims

When writing or reviewing typographic advice that cites reading science, a
short list of red flags for overclaiming:

- **"Studies show that X font is more readable."** Usually collapses
  legibility into readability, usually elides effect sizes, and usually
  ignores the Rayner-Pelli-Dyson consensus that between-font differences in
  well-designed text are small.
- **Single-study citations of dramatic comprehension gains.** The most
  robust findings are repeatedly replicated, hedged, and modest.
- **Graphical illustrations of word-shape as "why lowercase is more
  readable."** Word-shape theory is the old consensus, not the current one.
- **Invocation of "scientifically optimal" values** for x-height, CPL,
  leading, or similar without specifying the reading condition, reader
  population, and measurement.
- **Claims about dyslexia-specific fonts** without citing the meta-analytic
  work. The pattern of null-to-weak effects is clear enough that not
  acknowledging it is an overclaim.
- **Cross-script generalisation.** Latin reading-research findings should
  not be applied to Arabic/CJK/Devanagari without qualification. The
  generalisation goes in neither direction automatically.
- **Print-era numbers applied to screen.** Many of Tinker's specific
  recommendations are period-bound (paper type, photo-engraving, specific
  hot-metal faces) and do not transfer cleanly to high-DPI screens.

The stance this file recommends: describe legibility and readability
separately, cite evidence where strong, hedge where weak, and decline to
crown a single "best" font on empirical grounds — because the evidence
does not crown one.

## Sources

(Dates are publication dates; retrieval via DOI or archival link where
available.)

- Beier, S. (2012). *Reading Letters: Designing for Legibility.* BIS
  Publishers. Linked work in *Information Design Journal*.
  https://www.informationdesignjournal.org/
- Bouma, H. (1971). "Visual recognition of isolated lower-case letters."
  *Vision Research* 11(5): 459–474.
  https://doi.org/10.1016/0042-6989(71)90087-3
- Cattell, J. M. (1886). "The time it takes to see and name objects."
  *Mind* 11(41): 63–65.
- Dyson, M. C. (2004). "How physical text layout affects reading from
  screen." *Behaviour & Information Technology* 23(6): 377–393.
  https://doi.org/10.1080/00140139.2004.11953001
- Galliussi, J., Perondi, L., Chia, G., Gerbino, W., & Bernardis, P.
  (2020). "Inter-letter spacing, inter-word spacing, and font with
  dyslexia-friendly features: testing text readability in people with and
  without dyslexia." *Annals of Dyslexia.*
  https://doi.org/10.1007/s11881-020-00194-x
- Kuster, S. M., van Weerdenburg, M., Gompel, M., & Bosman, A. M. T.
  (2018). "Dyslexie font does not benefit reading in children with or
  without dyslexia." *Annals of Dyslexia* 68: 25–42.
  https://doi.org/10.1007/s11881-017-0154-6
- Larson, K. (2004). "The Science of Word Recognition." Microsoft
  Typography.
  https://docs.microsoft.com/en-us/typography/develop/word-recognition
- Legge, G. E., Pelli, D. G., Rubin, G. S., & Schleske, M. M. (1985).
  "Psychophysics of reading — I. Normal vision." *Vision Research*
  25(2): 239–252. https://doi.org/10.1016/0042-6989(85)90117-8
- Legge, G. E., & Bigelow, C. A. (2011). "Does print size matter for
  reading? A review of findings from vision science and typography."
  *Journal of Vision* 11(5): 8.
  https://doi.org/10.1167/11.5.8
- Pelli, D. G., Palomares, M., & Majaj, N. J. (2004). "Crowding is unlike
  ordinary masking: distinguishing feature integration from detection."
  *Journal of Vision* 4(12): 12.
  https://doi.org/10.1167/4.12.12
- Rayner, K. (1998). "Eye movements in reading and information
  processing: 20 years of research-survey." *Psychological Bulletin* 124(3):
  372–422.
  https://pubmed.ncbi.nlm.nih.gov/9849112/
- Rayner, K., Schotter, E. R., Masson, M. E. J., Potter, M. C., &
  Treiman, R. (2016). "So much to read, so little time: how do we read,
  and can speed reading help?" *Psychological Science in the Public
  Interest* 17(1): 4–34.
  https://doi.org/10.1177/1529100615623267
- Sheedy, J. E., Subbaram, M. V., Zimmerman, A. B., & Hayes, J. R.
  (2005). "Text legibility and the letter superiority effect." *Human
  Factors* 47(4): 797–815.
  https://pubmed.ncbi.nlm.nih.gov/16553067/
- Tinker, M. A. (1963). *Legibility of Print.* Ames, IA: Iowa State
  University Press.
  https://archive.org/details/legibilityofprin0000tink
- Zorzi, M., Barbiero, C., Facoetti, A., et al. (2012). "Extra-large
  letter spacing improves reading in dyslexia." *PNAS* 109(28):
  11455–11459. https://doi.org/10.1073/pnas.1205566109
