---
date: 2026-04-18
coverage: deep
peers:
  - ./crowding.md
  - ./legibility-vs-readability.md
  - ../accessibility/dyslexia.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/develop/word-recognition  # Larson, "The Science of Word Recognition", Microsoft Advanced Reading Technology, 2004
  - https://stanford.edu/~jlmcc/papers/RumelhartMcClelland82.pdf  # Rumelhart & McClelland, interactive-activation Part 2, Psych. Review 89(1), 1982
  - https://psycnet.apa.org/record/1981-31825-001  # McClelland & Rumelhart, "An interactive activation model of context effects in letter perception, Part 1", Psychological Review 88(5), 1981
  - https://pubmed.ncbi.nlm.nih.gov/9849112/  # Rayner, "Eye movements in reading and information processing: 20 years of research-survey", Psychological Bulletin 124(3), 1998
  - https://www.nature.com/articles/nature01516  # Pelli, Farell & Moore, "The remarkable inefficiency of word recognition", Nature 423:752–756, 2003
  - https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2011.00054/full  # Grainger & Ziegler, "A dual-route approach to orthographic processing", Frontiers in Psychology 2:54, 2011
  - https://www.college-de-france.fr/media/stanislas-dehaene/UPL60522_Chicago_1_ReadingInTheBrain_VWFA.pdf  # Dehaene, "The visual word form area: myth or reality?", Chicago lectures companion to Reading in the Brain, 2009
  - https://pubmed.ncbi.nlm.nih.gov/21592844/  # Dehaene & Cohen, "The unique role of the visual word form area in reading", Trends in Cog. Sci. 15(6), 2011
  - https://pubmed.ncbi.nlm.nih.gov/6242416/  # Paap, Newsome & Noel, "Word shape's in poor shape for the race to the lexicon", JEP:HPP 10(4), 1984
  - https://pubmed.ncbi.nlm.nih.gov/9293635/  # Mayall, Humphreys & Olson, "Disruption to word or letter processing? The origins of case-mixing effects", JEP:LMC 23(5), 1997
  - https://www.uv.es/~mperea/shapePP.pdf  # Perea & Rosa, "Does whole-word shape play a role in visual word recognition?", Perception & Psychophysics 64(5), 2002
  - https://pubmed.ncbi.nlm.nih.gov/26010560/  # Perea et al., "Resolving the locus of cAsE aLtErNaTiOn effects: evidence from masked priming", Neuropsychologia 73, 2015
  - https://www.mrc-cbu.cam.ac.uk/people/matt.davis/cmabrigde/  # Davis, "Reading jumbled texts: the Cmabrigde Uinervtisy meme explained"
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11532128/  # Pitts & Guest, "The Reicher–Wheeler paradigm in word-recognition research-survey: a cautionary note", Frontiers in Psychology, 2024
  - https://link.springer.com/article/10.1007/s11881-017-0154-6  # Kuster, van Weerdenburg, Gompel & Bosman, "Dyslexie font does not benefit reading in children with or without dyslexia", Annals of Dyslexia 68, 2018
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5629233/  # Wery & Diliberto, "The effect of a specialized dyslexia font, OpenDyslexic, on reading rate and accuracy", Annals of Dyslexia 67, 2017
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC2016788/  # Arditi & Cho, "Letter case and text legibility in normal and low vision", Vision Research 47(19), 2007
  - https://doi.org/10.1111/j.1467-9280.2008.02218.x  # Fiset et al., "Features for identification of uppercase and lowercase letters", Psychological Science 19, 2008
notes:
  - Coverage tier is deep — this file is the canonical reference for the word-shape vs parallel-letter-recognition debate. Peer files `crowding.md` and `legibility-vs-readability.md` link here rather than re-derive the debate. `accessibility/dyslexia.md` depends on this file for the "why dyslexia-font premise is wrong" argument.
  - Numeric values (Tinker's 9.5–19% all-caps slowdown, Paap's 15%/19%/8%/10% proofreading rates, boundary-study 210/240/280/300 ms) are reproduced as the original studies report them.
  - "Bouma shape" is used by type designers as aesthetic shorthand; this file is not a polemic against the term, only against presenting it as the mechanism of reading.
  - No token values; the typographic levers here (case, spacing, weight) are derived inline where needed — realizing them as project tokens is the `token-builder` agent's seat.
---

# Word-shape vs parallel-letter recognition — reading science reference

The most widely repeated "scientific" story in design writing about reading is
that readers identify words by the silhouette the ascenders, descenders, and
x-height strokes trace — the *bouma*, the word envelope. The corresponding
practical claim is that lowercase is more readable than ALL CAPS because
capitals erase the silhouette. The story is tidy, visual, and wrong in its
mechanism: the experimental literature from ~1977 onward converges on
**parallel letter recognition** (PLR) — readers identify multiple letters in
parallel during each fixation, word identity falls out of letter identities
plus context, and word-shape is at best a weak supplementary cue.

This file lays out the two models, Larson's 2004 canonical synthesis, the
supporting evidence, modern consensus, and what this means for typography —
ALL CAPS, mixed-case, dyslexia fonts, font-design priorities. It assumes
`./crowding.md` on the crowding mechanism and
`./legibility-vs-readability.md` on the glyph-vs-text distinction.

## The two competing models

### Word-shape model

The word-shape model — sometimes called *holistic word recognition*, the
*bouma model*, or the *outline model* — claims that skilled readers recognise
words as single visual patterns. A word's ascending, descending, and neutral
letters produce a characteristic silhouette, or envelope; the reader matches
that silhouette against stored templates, and letter-level processing
follows (or is bypassed) rather than precedes word identification.

Foundational results are pre-cognitive-revolution:

- **Cattell (1886)**, "The time taken up by cerebral operations," *Mind*
  11. Tachistoscopic presentation at 5–10 ms; subjects were more accurate
  at identifying a word than an isolated letter. Cattell inferred words
  are unitary perceptual wholes — the first Word Superiority Effect and
  the birth of word-shape theory.
- **Woodworth (1938)**, *Experimental Psychology*. Lowercase running text
  is read faster than uppercase. Received reading: lowercase exposes
  word-shape, uppercase flattens it.
- **Smith (1969)** and **Fisher (1975)** replicated lowercase-faster;
  typically a 5–10% reading-speed deficit for ALL CAPS.
- **Haber & Schindler (1981)** / **Monk & Hulme (1983)**. Misspellings
  consistent with word shape (*tesf* for *test*) were missed ~twice as
  often as inconsistent ones (*tesc*), 13% vs 7% in Haber & Schindler.
- **Mixed-case disruption** (Smith 1969; Adams 1979; Mason 1978;
  Pollatsek, Well & Schindler 1975; Meyer & Gutschera 1975). mIxEd CaSe
  text slows reading, naming, and matching — interpreted as disrupted
  bouma silhouette.

"Bouma" as a term for this silhouette was popularised by Paul Saenger's
1997 *Space Between Words*, which treats "Bouma shape" as established
psychological terminology. Saenger borrowed it from 1970s designer-
adjacent literature; Herman Bouma, whom the term honours, never
formulated a word-shape model. Larson (2004) calls this a "grand
misunderstanding" (see also Davis 2003 on the related Cambridge meme).

### Parallel-letter-recognition (PLR) model

The PLR model claims that readers identify the letters in a word roughly
simultaneously — in parallel across the fixation window — and that word
identity is derived from the letter identities together with top-down
context. Shape exists as a low-level image feature but is not what the
reader's word-recognition machinery operates on.

Foundational results span cognitive psychology, computational modelling,
and neuroscience:

- **Adams (1979)**, "Models of word recognition," *Cognitive Psychology* 11.
  Pseudowords (*mave*) suffer the same case-alternation cost as real
  words. Pseudowords have no learned shape, so shape cannot be what
  case-alternation disrupts.
- **McClelland & Rumelhart (1981)** / **Rumelhart & McClelland (1982)**,
  the Interactive-Activation Model (IAM) in *Psychological Review* 88 and
  89. Three processing levels (visual features → letters → words) with
  excitatory and inhibitory connections running bottom-up and top-down.
  The IAM reproduces the Word Superiority Effect, letter-confusability
  patterns, and context effects without any holistic word template.
- **McClelland & Johnson (1977)**, *Perception & Psychophysics* 22.
  Letters are identified faster inside pseudowords (*mave*) than inside
  random strings (*amve*); advantage comes from regular letter
  combinations, not word shape.
- **Paap, Newsome & Noel (1984)**, "Word shape's in poor shape for the
  race to the lexicon," *JEP:HPP* 10. Direct empirical attack on
  Haber & Schindler. Separating word-shape from letter-shape in the
  misspelling task produced 15% / 19% / 8% / 10% error across the four
  cells; letter-shape did all the work, word-shape did none.
- **Pelli, Farell & Moore (2003)**, "The remarkable inefficiency of word
  recognition," *Nature* 423:752–756. Even the five most frequent
  three-letter English words are recognised at letter-by-letter efficiency
  — no holistic shortcut detectable in psychophysics.
- **Rayner (1998)**, *Psychological Bulletin* 124. Fixations land on letter
  positions; perceptual span is ~15 letters right of fixation in
  alphabetic LTR reading; saccades cover 7–9 letters; parafoveal preview
  accumulates letter-level, not shape-level, information.
- **Dehaene (2009)**, *Reading in the Brain*; **Dehaene & Cohen (2011)**.
  The VWFA activates for letter strings including pseudowords and
  consonant strings, not just real words with learned shapes. The
  substrate is letter-string-selective, not shape-template-selective.

## Larson 2004: the canonical synthesis

The typography community's accessible summary is Kevin Larson's 2004 "The
Science of Word Recognition," presented first as an ATypI 2003 talk and
published by Microsoft's Advanced Reading Technology group. Larson, a
cognitive psychologist on the ClearType team, wrote it after finding that
typographers around him assumed the word-shape model was settled psychology,
while no reading psychologist he knew still worked within it.

Larson lays out the three historical models (word shape, serial letter
recognition [Gough 1972; rejected early], parallel letter recognition),
presents the evidence each marshalled, and re-examines the word-shape
evidence under better-controlled follow-ups. His conclusion: every piece of
evidence the word-shape model rested on has been reinterpreted as either
(a) confounded with letter-shape, (b) a practice / familiarity effect, or
(c) better explained by letter combinations and interactive activation.

Key rebuttals:

- **Word Superiority Effect is not shape-based.** McClelland & Johnson
  (1977) showed the effect extends to pseudowords. Since pseudowords have
  no previously-seen shape, the facilitation cannot come from shape
  templates; it comes from regular letter combinations interacting with
  the lexicon.
- **Lowercase-faster is a practice effect.** Kolers & Perkins (1975)
  demonstrated that readers can be trained to read mirror-reversed text
  at near-normal rate; readers asymptote on whatever form they practise.
  Skilled readers read lowercase at >99% of the time; the ~10% speed
  deficit for ALL CAPS is the expected cost of low exposure, not of
  silhouette loss.
- **Proofreading errors track letter shape, not word shape.** Paap,
  Newsome & Noel (1984) factorially crossed word-shape and letter-shape
  preservation and found a statistically reliable main effect of
  letter-shape (more misses with matching letter shape, independent of
  word shape) and no reliable word-shape main effect. The trend in the
  word-shape dimension was in the opposite direction from the
  word-shape model's prediction.
- **Case-alternation disrupts pseudowords as much as words.** Adams
  (1979): if the disruption came from silhouette mismatch, it should
  spare pseudowords (which have no learned silhouette). It does not.
- **Eye-tracking contradicts shape-prediction.** Moving-window studies
  (McConkie & Rayner 1975) show reading rate is a linear function of
  how many **letters** are available around fixation, not of whether
  whole-word envelopes are preserved. Boundary studies (Rayner 1975)
  show that when the word to the right of fixation is replaced during
  the saccade with a string preserving shape but changing letters
  (*chart* → *ebovf*), post-boundary fixation time is 300 ms — worse
  than a string that preserves letters but destroys shape (*chart* →
  *chyft*, 280 ms), and much worse than the identical control (210 ms).
  If readers preview shape, shape-matched strings should have helped
  more than letter-matched strings. They helped less.
- **All-uppercase preview works as well as lowercase preview.** Rayner
  (1975) further tested *chart* → *CHART* as the boundary condition.
  Post-boundary fixation time matched the identical control — 210 ms —
  despite completely different shape. Letter identity, not shape,
  transfers across saccades.

Larson's conclusion, sharper than design writers usually reproduce:
"Word shape is no longer a viable model of word recognition. … The
readability and legibility of a typeface should not be evaluated on its
ability to generate a good bouma shape."

## Further evidence lines for parallel-letter recognition

Beyond Larson's synthesis, four independent lines converge on PLR.

### Masked priming and case independence

A briefly-flashed lowercase prime (*table*) accelerates recognition of
an uppercase target (*TABLE*) as much as an uppercase prime does. This
case-independent priming is the strongest single source of evidence
that what crosses the prime-target gap is an *abstract letter
identity*, not a visual shape. Documented by Evett & Humphreys (1981),
replicated in Bowers (2000), Kinoshita & Lupker (2003), and recap in
Perea, Vergara-Martínez & Gomez (2015, *Neuropsychologia* 73). Case
alternation at the prime (*tAbLe*) also produces full identity priming
to the target — lexical access does not care about case-mixed shape
disruption in the prime, even though case alternation in the target
disrupts reading.

Nuance: recent work (Perea et al. 2016, 2020) shows case-*dependent*
priming for abbreviations (*DNA*, *CIA*), where the uppercase form is
canonical. The default route is case-abstract; the lexicon stores some
form-specific entries where cultural use forces it.

### Transposed-letter effects

Transposing two internal letters (*jugde* / *judge*) impairs recognition
far less than replacing those letters with visually similar but
different ones (*jupce*). *Jugde* primes JUDGE nearly as well as JUDGE
primes JUDGE. Replicated across Spanish (Perea & Lupker 2003, 2004),
French (Schoonbaert & Grainger 2004), and Japanese kana (Perea, Nakatani
& van Leeuwen 2011, *Memory & Cognition* 39).

This rules out both strict position-specific letter coding *and*
whole-word-shape coding in a single stroke. The shape of *jugde* and
*judge* differ — ascender positions shift when `d` and `g` swap — yet
the words prime interchangeably. What the reader computes is neither a
rigid letter-position grid nor a silhouette.

The viral "Cmabrigde Uinervtisy" email (2003) dramatised this result
but got its provenance wrong: not Cambridge research-survey, but traced to a
1976 Nottingham PhD by Graham Rawlinson (Davis 2003). The actual
literature is narrower than the meme — longer words, multiple
transpositions, or consonant-vowel/morphological-boundary transpositions
disrupt tolerance — but the core point holds: letter identity is coded
robustly enough to tolerate moderate positional noise.

### Neural evidence — the Visual Word Form Area

The VWFA (left lateral occipitotemporal sulcus) activates comparably
for real words, pseudowords (*florp*), consonant strings (*btrk*), and
individual letters, but weakly for non-linguistic visual controls of
comparable visual complexity. This is the opposite of what a holistic
word-template account predicts — a shape-template system should fire
preferentially for previously-seen words whose templates exist. The
pattern fits Dehaene's "neuronal recycling" account: a ventral visual
region repurposed for letter-string processing during literacy
acquisition (Dehaene 2009; Dehaene & Cohen 2011, *TiCS* 15(6)). VWFA
responds to sub-letter shape features that disambiguate visually similar
letters (`n` / `h`, `c` / `e`) rather than to whole-word silhouettes;
single-trial MVPA decodes letter identity with higher fidelity than
word identity in early VWFA responses.

### Reading-speed and pseudoword evidence

Skilled readers read pseudowords at 70–85% of word-reading speed in
lexical decision, closer in serial-list reading. If shape drove
recognition, pseudowords — which have no learned shape — should be
dramatically slower. The residual gap fits the top-down lexical-context
benefit real words accrue, not shape-template matching.

Pelli, Farell & Moore (2003, *Nature*) used noise-masking psychophysics
to estimate word-recognition *efficiency* relative to optimal
parts-based recognition. For every word they tested — up to the most
frequent three-letter English words — efficiency matched letter-by-
letter ("recognition by parts"), not the holistic prediction. The title
is pointed: "*The remarkable inefficiency of word recognition*." A
billion letters of practice does not yield any holistic shortcut.

## Interactive-activation and its descendants

The McClelland & Rumelhart Interactive-Activation Model (IAM) set the
computational frame for modern word-recognition theory. Its successors
— Seidenberg & McClelland (1989) *Psychological Review* 96:523; Plaut,
McClelland, Seidenberg & Patterson (1996) *Psychological Review*
103:56; the Coltheart DRC model; Grainger & Ziegler (2011) dual-route
orthographic-processing framework in *Frontiers in Psychology* 2:54 —
vary in how they encode position, phonology, and learning, but none
posits a whole-word-shape template as a functional unit.

Grainger & Ziegler's 2011 dual-route proposal distinguishes a
**coarse-grained** route (letter combinations most diagnostic of word
identity, open-bigram style) from a **fine-grained** route (sublexical
units tied to phonological and morphological representations). Both
routes operate over letter-level inputs; neither is shape-based.

"Parallel-letter recognition" is a family of related models
distinguished by how they handle position coding, phonology, and
training dynamics. What the family shares is the claim that the unit of
input is the letter identity (or sublexical letter combination), not
the word silhouette.

## What happened to word-shape

The word-shape model's residual presence sits in four places.

- **Popular-science writing.** Blog posts and design-trade explainers
  still teach the bouma model because it is visually intuitive and
  because Saenger's *Space Between Words* (1997) legitimised the term.
  The 2003 "Cmabrigde Uinervtisy" email inadvertently reinforced it
  despite being about transposition — casual readers took it as
  evidence for "reading by shape."
- **Dyslexia-font marketing.** OpenDyslexic, Dyslexie, Sylexiad, Lexie
  Readable and kin market via a word-shape rationale — weighted
  bottoms to "preserve orientation," distinguished ascenders/descenders
  to "protect the silhouette." See `../accessibility/dyslexia.md` for
  null-to-weak empirical support (Kuster et al. 2018; Wery & Diliberto
  2017).
- **Legibility folklore in design education.** Older handbooks still
  teach the bouma as established reading science; the vocabulary
  persists ("poor word-shape discrimination") even where prescriptive
  advice is sound.
- **Type-designer aesthetic vocabulary.** "Word-shape" as a descriptive
  term for silhouette balance, coherence, and typeset colour is
  legitimate aesthetic language. It is a bad theory of reading
  mechanism. "This word looks well-shaped" (aesthetic) is not the same
  claim as "readers identify words by their shapes" (mechanism).

Academic psycholinguistics has had consensus on PLR in the descendant-
of-IAM sense since ~1990. Isolated dissenting work resurfaces — Mayall,
Humphreys & Olson (1997) argued case-mixing disrupts a supra-letter
processing stage and left room for some shape-like contribution — but
subsequent reanalysis (Perea & Rosa 2002, using size alternation to
dissociate shape from letter-processing; Perea, Vergara-Martínez &
Gomez 2015) attributes such effects to perceptual-grouping disruption
and letter-integration cost, not to a whole-word-shape template. No
active research-survey programme revives word-shape as the primary recognition
mechanism.

## What this means for typography

### The ALL CAPS slowdown is not about word-shape loss

The empirical fact — ALL CAPS running text reads slower than mixed-case
— is robust. Tinker (1955) reported 9.5–19% slower for 5–10 min reading,
13.9% over 20 min. Paap, Newsome & Noel (1984), Arditi & Cho (2007,
*Vision Research* 47:2499), Fiset et al. (2008, *Psychological Science*
19:1161), and the crowding literature (`./crowding.md`) converge on
10–20% slower depending on font, size, task, and familiarity. The
folklore 30% number is not supported.

Word-shape loss is not the mechanism. Modern explanations, broadly
additive:

- **Reduced inter-letter distinguishability.** Capitals share a uniform
  rectangle and fewer diagnostic features, raising confusability
  (`I` / `l` / `1`, `O` / `Q` / `0`). Fiset et al. (2008) showed
  uppercase identification relies more on line terminations; lowercase
  exploits a richer feature set including ascender / descender
  signatures. Fewer features → worse identification under crowding.
- **Higher flanker similarity → stronger crowding.** Same height, same
  weight, fewer extenders: ALL CAPS strings resemble their neighbours
  more than mixed-case does, raising critical-spacing demands. ALL
  CAPS is crowding-worst-case, which is why positive tracking
  (+0.04–0.1 em) is conventionally applied to it.
- **Wider letter footprint per em.** Capitals occupy more horizontal
  space, reducing the uncrowded visual-span window per fixation.
- **Lower familiarity.** Skilled readers have overwhelmingly more
  lowercase practice. Kolers & Perkins (1975): reading speed
  asymptotes on whatever form is practised. Martelli, Majaj & Pelli
  (2005): ~1.5× familiarity-driven efficiency gain for common stimuli.
  ALL CAPS accrues neither.

Practical advice — do not set long blocks in ALL CAPS — stays correct.
The textbook explanation for it is wrong.

### Title Case vs sentence case

Evidence is thin; any effect is small. Title Case leaves lowercase
interiors intact and does not trigger the crowding / feature-
distinguishability cost ALL CAPS does. No study finds a reliable
reading-speed deficit for Title Case over sentence case. Differences
attributed to the choice are dominated by measure, leading, word-
spacing, and CPL — not by capitalisation. For headings (short strings,
large sizes, foveally resolved), the case choice is primarily a
register / branding decision with negligible legibility impact.

### Mixed case (StUdLy cApS, RaNsOm NoTe)

Mixed-case text is reliably slower than either pure case —
typically ~20–30% slower than lowercase (Smith 1969; Mason 1978; Adams
1979; Mayall, Humphreys & Olson 1997). The mechanism, per Adams's
pseudoword control and Paap et al.'s letter-shape separation, is **not**
disrupted word-shape. Candidate mechanisms: perceptual-grouping
disruption (Mayall, Humphreys & Olson 1997, reinterpreted in Perea &
Rosa 2002); letter-identification cost as each letter must be mapped to
its case-independent identity; height / feature irregularity raising
flanker-similarity cost under crowding. Practical upshot: mixed case in
running text is a legibility regression for no gain; usable for
stylistic emphasis in short strings where speed is not the target.

### Dyslexia-specific fonts

OpenDyslexic, Dyslexie, Sylexiad, Lexie Readable and kin are premised
on word-shape-protection: weighted bottoms "preserve orientation,"
distinguished ascenders/descenders "protect the silhouette," unique
letterforms prevent flipping confusion. The mechanistic premise is
wrong: dyslexic readers read by parallel-letter recognition, not by
shape matching. Interventions that "preserve shape" target a mechanism
that is not the bottleneck.

- **Kuster et al. (2018)**, *Annals of Dyslexia* 68. Two experiments
  with 170 and 147 Dutch primary-school children. Dyslexie produced no
  reliable speed or accuracy advantage over Arial or Times New Roman;
  most children preferred Arial. Conclusion: "The Dyslexie font
  neither benefits nor impedes the reading process of children with
  and without dyslexia."
- **Wery & Diliberto (2017)**, *Annals of Dyslexia* 67. Single-subject
  alternating-treatment design comparing OpenDyslexic to Arial and
  Times New Roman on letter-naming, word-reading, and nonsense-word
  reading. No improvement in rate or accuracy, individually or as a
  group.

What helps empirically: letter-spacing interventions (Zorzi et al. 2012
*PNAS*; Perea et al. 2012), larger body sizes, higher contrast, shorter
measure, and reader-controlled layout — general crowding / readability
levers, not shape-protection. See `./crowding.md` and
`../accessibility/dyslexia.md`.

### x-height, aperture, and letter-feature distinguishability

Moderately higher x-height renders small body text more legibly — more
diagnostic letter-feature information falls inside the uncrowded core
region at small angular sizes. This is a letter-feature-information
effect, not a word-shape effect. Open apertures, differentiated
skeletons for similar-glyph pairs (I / l / 1, O / 0, b / d, r / n),
and unambiguous terminal shapes all reduce letter-identification
errors under crowding (Beier 2012, *Reading Letters*).

Font-design priority for text type: **letter-level distinguishability**
over word-level silhouette distinctiveness. The bottleneck is letter
identity under crowding, not word-outline matching. Practical levers:
open apertures; skeleton differentiation on confusable pairs; stroke-
contrast modulation calibrated to target size (too-high contrast loses
fine strokes in crowded positions, too-low mushes features); moderate
x-height; consistent metrics across weights / widths / optical-size
cuts. For display type, where foveal resolution is ample and crowding
is weak, word-shape as aesthetic descriptor — silhouette balance,
typeset colour, line rhythm — is fine. It stops being fine when
offered as the mechanism of reading.

## Common misuses of word-shape

- **"Serif fonts are more readable because they create better word
  shapes."** Serif-vs-sans differences in continuous text are small,
  font-specific, and often null (Dyson 2004; Legge & Bigelow 2011;
  Larson 2004's Poynter study). Where effects appear, glyph features
  and spacing explain them, not word-shape signatures. "Serifs guide
  the eye" is related folklore; eye-tracking shows saccades, not
  smooth pursuit (Rayner 1998).
- **"Dyslexia fonts preserve word shape for struggling readers."** The
  premise is wrong; the intervention misses. Null-to-weak results
  (Kuster 2018; Wery & Diliberto 2017) fit the prediction.
- **"ALL CAPS is 30% slower because word-shape is destroyed."**
  Slowdown is ~10–20%, and the mechanism is crowding + letter-feature
  homogeneity + lower practice — not shape loss.
- **"Only first and last letters matter."** The Cambridge transposition
  meme overstates. Longer words, content words, consonant-cluster and
  morphological-boundary transpositions all disrupt tolerance. Correct
  form: letter *identity* is coded more robustly than letter
  *position*, within limits.
- **"Skilled readers read whole words at a glance."** Eye-tracking
  shows ~7–9-letter saccades and ~200–250 ms fixations; Pelli, Farell
  & Moore (2003) show even the most frequent words read with
  parts-based efficiency.

## Edge cases and caveats

- **Skimming vs reading.** Under skimming, eye movements shift —
  longer saccades, more skipping, shorter fixations (Rayner et al.
  2016, *PSPI* 17; Strukelj & Niehorster 2018). Gestalt cues — word
  length, outline, punctuation silhouette — may contribute more to
  skim-mode processing than to comprehension reading. Evidence is
  mixed and mostly indirect. Typography for sustained reading
  targets comprehension, not skimming.
- **Non-Latin scripts.** *Chinese / kanji* characters are
  higher-information visual units (typically morpheme or word); native
  readers show genuine within-character holistic processing (Hsiao &
  Cottrell 2009; Wong et al. 2021) — not Latin-style word-shape, but
  not single-letter-as-unit either. Multi-character word superiority
  effects exist (Zhang et al. 2018, *Applied Psycholinguistics*).
  *Arabic* cursive connection produces shape directly through
  contextual letter forms; the visual unit is often the ligature
  cluster. Arabic is unicameral, so Latin ALL-CAPS arguments do not
  apply. See `../scripts/arabic.md`. *Devanagari* shirorekha creates a
  consistent horizontal band; matras and stacked conjuncts form
  two-dimensional glyph clusters that disrupt single-letter-as-unit
  assumptions (`../scripts/devanagari.md`). Do not transplant PLR *or*
  word-shape conclusions across script families without
  re-verification.
- **Word-length as a parafoveal cue.** Within alphabetic reading, word
  length — a coarser length-and-shape signature visible in the
  parafovea — helps *where the next fixation lands*, not word
  identification (Pollatsek & Rayner 1982; Rayner 1998). This is a
  weak envelope cue that fits inside PLR, not an alternative to it.
- **Individual differences.** Some readers show residual
  shape-sensitivity effects (Hall, Humphreys & Cooper 2001 on
  case-specific reading in patients; Lavidor 2011 on dyslexia).
  Population-level PLR is consistent with individual variability in
  residual-shape-signal use. Typography upshot unchanged: designing
  for shape-protection is not a replicable intervention.

## Key citations

### Word-shape model (historical)

- Cattell, J. (1886). "The time taken up by cerebral operations."
  *Mind* 11: 277–282, 524–538.
- Woodworth, R. S. (1938). *Experimental Psychology.* New York: Holt.
- Smith, F. (1969). "Familiarity of configuration vs. discriminability
  of features in the visual identification of words." *Psychonomic
  Science* 14: 261–262.
- Haber, R. N., & Schindler, R. M. (1981). "Errors in proofreading."
  *JEP:HPP* 7: 573–579.
- Monk, A. F., & Hulme, C. (1983). "Errors in proofreading: Evidence
  for the use of word shape in word recognition." *Memory and
  Cognition* 11: 16–23.
- Saenger, P. (1997). *Space Between Words.* Stanford University Press.

### Parallel-letter recognition and interactive activation

- Adams, M. J. (1979). "Models of word recognition." *Cognitive
  Psychology* 11: 133–176.
- McClelland, J. L., & Johnson, J. C. (1977). "The role of familiar
  units in perception of words and nonwords." *Perception &
  Psychophysics* 22: 249–261.
- McClelland, J. L., & Rumelhart, D. E. (1981). *Psychological Review*
  88: 375–407. https://psycnet.apa.org/record/1981-31825-001
- Rumelhart, D. E., & McClelland, J. L. (1982). *Psychological Review*
  89: 60–94.
- Paap, K. R., Newsome, S. L., & Noel, R. W. (1984). "Word shape's in
  poor shape for the race to the lexicon." *JEP:HPP* 10: 413–428.
  https://pubmed.ncbi.nlm.nih.gov/6242416/
- Seidenberg, M. S., & McClelland, J. L. (1989). *Psychological Review*
  96: 523–568.
- Plaut, D. C., McClelland, J. L., Seidenberg, M. S., & Patterson, K.
  (1996). *Psychological Review* 103: 56–115.
- Grainger, J., & Ziegler, J. C. (2011). "A dual-route approach to
  orthographic processing." *Frontiers in Psychology* 2: 54.
  https://doi.org/10.3389/fpsyg.2011.00054

### Canonical synthesis / eye movements

- Larson, K. (2004). "The Science of Word Recognition." Microsoft ATG.
  https://learn.microsoft.com/en-us/typography/develop/word-recognition
- Rayner, K. (1998). "Eye movements in reading and information
  processing: 20 years of research-survey." *Psychological Bulletin* 124:
  372–422. https://pubmed.ncbi.nlm.nih.gov/9849112/
- Rayner, K., Schotter, E. R., Masson, M. E. J., Potter, M. C., &
  Treiman, R. (2016). "So much to read, so little time." *PSPI* 17(1):
  4–34.

### Word Superiority Effect, masked priming, transposition

- Reicher, G. M. (1969). *Journal of Experimental Psychology* 81:
  275–280.
- Wheeler, D. D. (1970). *Cognitive Psychology* 1: 59–85.
- Pitts, B., & Guest, O. (2024). "The Reicher–Wheeler paradigm… a
  cautionary note." *Frontiers in Psychology*.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC11532128/
- Evett, L. J., & Humphreys, G. W. (1981). *QJEP* 33A: 325–350.
- Bowers, J. S. (2000). *Psychonomic Bulletin & Review* 7: 83–99.
- Perea, M., Vergara-Martínez, M., & Gomez, P. (2015). "Resolving the
  locus of cAsE aLtErNaTiOn effects." *Neuropsychologia* 73.
  https://pubmed.ncbi.nlm.nih.gov/26010560/
- Perea, M., & Lupker, S. J. (2003). "Transposed-letter confusability
  effects in masked form priming." In Kinoshita & Lupker (eds.),
  *Masked Priming.*
- Perea, M., Nakatani, C., & van Leeuwen, C. (2011). *Memory &
  Cognition* 39: 700–707.
- Davis, M. H. (2003). "Reading jumbled texts: the Cmabrigde
  Uinervtisy email explained." MRC CBU Cambridge.
  https://www.mrc-cbu.cam.ac.uk/people/matt.davis/cmabrigde/

### Whole-word shape re-evaluation

- Mayall, K., Humphreys, G. W., & Olson, A. (1997). *JEP:LMC* 23(5):
  1275–1286. https://pubmed.ncbi.nlm.nih.gov/9293635/
- Perea, M., & Rosa, E. (2002). "Does 'whole-word shape' play a role
  in visual word recognition?" *Perception & Psychophysics* 64(5):
  785–794. https://www.uv.es/~mperea/shapePP.pdf

### Neural / psychophysics

- Dehaene, S. (2009). *Reading in the Brain.* Viking.
- Dehaene, S., & Cohen, L. (2011). *Trends in Cognitive Sciences*
  15(6): 254–262. https://pubmed.ncbi.nlm.nih.gov/21592844/
- Pelli, D. G., Farell, B., & Moore, D. C. (2003). "The remarkable
  inefficiency of word recognition." *Nature* 423: 752–756.
  https://www.nature.com/articles/nature01516

### Case, letter features, dyslexia fonts

- Tinker, M. A. (1955). *Journal of Applied Psychology* 39: 444–446.
- Tinker, M. A. (1963). *Legibility of Print.* Iowa State UP.
- Arditi, A., & Cho, J. (2007). *Vision Research* 47(19): 2499–2505.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2016788/
- Fiset, D., et al. (2008). *Psychological Science* 19: 1161–1168.
  https://doi.org/10.1111/j.1467-9280.2008.02218.x
- Kolers, P. A., & Perkins, D. N. (1975). *Cognitive Psychology* 7:
  228–267.
- Kuster, S. M., et al. (2018). *Annals of Dyslexia* 68: 25–42.
  https://doi.org/10.1007/s11881-017-0154-6
- Wery, J. J., & Diliberto, J. A. (2017). *Annals of Dyslexia* 67:
  114–127. https://pmc.ncbi.nlm.nih.gov/articles/PMC5629233/

### Non-Latin holistic / word-based processing

- Hsiao, J. H., & Cottrell, G. W. (2009). *Psychological Science*
  20(4): 455–463.
- Wong, A. C.-N., et al. (2021). "Holistic processing of Chinese
  characters in college students with dyslexia." *Scientific
  Reports*. https://www.nature.com/articles/s41598-021-81553-5
- Zhang, H., Yao, P., Zhao, J., & Wang, S. (2018). *Applied
  Psycholinguistics* 39(6): 1319–1346.

### Peer files

- [./crowding.md](./crowding.md) — crowding mechanism behind the
  ALL-CAPS and mixed-case slowdowns.
- [./legibility-vs-readability.md](./legibility-vs-readability.md) —
  umbrella concept-distinction; this file extends the Word-Shape
  Debate section.
- [../accessibility/dyslexia.md](../accessibility/dyslexia.md) —
  dyslexia-specific fonts; this file supplies the theoretical basis
  for why the shape-protection premise fails.
