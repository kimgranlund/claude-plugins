---
date: 2026-04-18
coverage: light
peers:
  - ./legibility-vs-readability.md
  - ./crowding.md
  - ./word-shape-vs-parallel-letter.md
  - ../techniques/optical-size.md
  - ../contemporary/variable-fonts.md
primary_sources:
  - Beier, S. (2012, rev. 2022). *Reading Letters: Designing for Legibility.* BIS Publishers.
  - Bigelow, C. (2019). "Oral History of Optical Size." *Journal of the Computer-Aided Design community*, and later writings on opsz in *TUGboat* and *Language & Typography*.
  - Legge, G. E., & Bigelow, C. A. (2011). "Does print size matter for reading?" *Journal of Vision* 11(5):8. https://doi.org/10.1167/11.5.8
  - Pelli, D. G., Farell, B., & Moore, D. C. (2003). "The remarkable inefficiency of word recognition." *Nature* 423: 752–756. https://doi.org/10.1038/nature01673
  - Pelli, D. G., Burns, C. W., Farell, B., & Moore-Page, D. C. (2006). "Feature detection and letter identification." *Vision Research* 46(28): 4646–4674. https://doi.org/10.1016/j.visres.2006.04.023
  - Chaparro, B. S., Shaikh, A. D., & Chaparro, A. (2010). "Keeping up with content on the web: Font size and reading comfort." *Ergonomics*.
  - Bernard, M., Liao, C. H., & Mills, M. (2001). "The effects of font type and size on the legibility and reading time of online text by older adults." *Usability News* 3.2.
  - Arditi, A. (2004). "Adjustable typography: an approach to enhancing low vision text accessibility." *Ergonomics* 47(5): 469–482.
  - Larson, K. (2004). "The Science of Word Recognition." Microsoft Typography. https://learn.microsoft.com/en-us/typography/develop/word-recognition
  - Beier, S., & Larson, K. (2010). "Design improvements for frequently misrecognized letters." *Information Design Journal* 18(2): 118–137.
  - Ouwehand, N., & Beier, S. (2020). Reading-speed measurements across text vs display cuts — Royal Danish Academy type research-survey group.
  - Frere-Jones, T. (1999/2007). Notes on Retina for the *Wall Street Journal*. https://frerejones.com/retina
  - Shaw, P. (2008). "A fresh look at Bell Centennial." *Print* magazine; Matthew Carter interviews collected in *Typographically Speaking* (MIT Press, 2002).
  - Google Fonts / TypeNetwork. Roboto Flex research-survey log. https://github.com/googlefonts/roboto-flex
  - Undercase Type. Fraunces design notes. https://github.com/undercasetype/Fraunces
notes:
  - Coverage is *light*: this is the empirical-science companion to `../techniques/optical-size.md`. The techniques file carries the CSS, the axis mechanics, the browser table, and the font inventory — this file does not repeat them. Cross-reference rather than duplicate.
  - Effect-size numbers are reported where the primary source states them; where figures summarise design-community claims rather than peer-reviewed data, the phrasing is explicit.
---

# Optical size research-survey — reading-science reference

Optical sizing is the type-design practice of tuning a typeface's stroke contrast, aperture, spacing, x-height, and serif robustness for the rendered size at which it will be read. A 6-point cut is not a scaled-down 72-point cut; the letterforms are redrawn so the reader's perceptual experience is comparable at both sizes. This file is the *empirical* companion to `../techniques/optical-size.md` — where that file covers CSS, font-file mechanics, and the `opsz` axis, this one catalogues the reading-science evidence for why optical sizing matters, summarising the findings from punchcutting-era craft through the contemporary psychophysics-of-reading literature.

The short version: the case for optical sizing at small sizes is strong and well-replicated; the case at display sizes is aesthetic more than legibility-driven; and the case for a *continuous* opsz axis (as opposed to discrete cuts) is plausible but not yet backed by peer-reviewed eye-tracking evidence. Where the literature supports a quantitative claim, this file cites it; where it doesn't, it hedges.

## What optical sizing solves, in reading-science terms

At small rendered sizes (body, caption, footnote — roughly 6–12 point), a reader's visual system is contending with three simultaneous constraints: limited foveal acuity for fine detail, crowding from neighbouring letters (see `./crowding.md`), and — on emissive screens or inked paper — rendering noise that can swallow hairlines. Letterforms that work at display size (thin serifs, tight sidebearings, dramatic stroke contrast, classical x-height) lose information to these constraints. Small-size cuts compensate by:

- **Thickening strokes and lowering stroke contrast** so hairlines don't fall below the contrast or pixel-size threshold.
- **Opening apertures** on `c`, `e`, `s`, `a` so the inside of each letter is perceptually distinct from its exterior counter.
- **Widening sidebearings** so adjacent letters sit outside each other's critical-spacing zones (Bouma 1970; Pelli, Palomares & Majaj 2004).
- **Raising x-height relative to cap-height** so the reading zone carries more signal per pixel.
- **Shortening ascenders and descenders** so vertical rhythm doesn't fracture when the body is already near acuity limits.

At display sizes (roughly 36 pt and above), the same letterforms render as *bloated* and *loose*. The fovea resolves fine detail easily, crowding is negligible within a title, and the reader processes the headline as a gestalt. Display cuts strip the small-size compensations: stroke contrast rises, apertures close, sidebearings tighten, x-height drops, and hairlines reappear as legitimate stylistic detail.

A single-master digital font without optical sizing compromises between these regimes — most production fonts optimise for a middle zone around 12–16 pt and render acceptably across a range but ideally at nothing. Opsz fonts (static multi-cut families, or variable fonts on the `opsz` axis) restore the tuning.

## Pre-digital empirical grounding

Optical sizing was *empirical before it was theorised*. Punchcutters in the 15th–19th centuries discovered size-specific compensation through iterative trial: a 6-point Garamond cut with the same proportions as the 12-point looked *wrong* at its intended size — too fine, too fragile, too tight — so the punchcutter thickened strokes, opened counters, widened sidebearings, and often redrew the skeleton outright. The corrections weren't written down as design principles; they accumulated as craft.

Two 18th-century French sources document the practice explicitly. **Pierre-Simon Fournier** (*Manuel Typographique*, 1764–66) described how body sizes below ~10 point needed heavier proportional weight and wider spacing than the same family's text sizes. **Francis Thibaudeau**'s later work catalogued size-specific masters in foundry output. The vocabulary of *gros canon*, *petit canon*, *parangon*, *philosophie*, *bourgeois*, *mignonne*, *nonpareille*, *perle*, *diamant* — the metal-type size names — tracked both the absolute point size and the visual character expected at that size.

**Matthew Carter**'s Bell Centennial (AT&T, 1978) is the hinge case between punchcutter-era craft and contemporary evidence-driven optical sizing. The face was commissioned for the AT&T telephone directory, where Bell Labs had measured reader-identification failure rates on the incumbent Bell Gothic at the directory's 6-point setting on Bible paper with high-speed letterpress. Carter's brief: redraw the family so readers could find names reliably. He produced four hand-drawn optical masters — **Name & Number**, **Address**, **Subcaption**, and **Bold Listing** — each tuned for specific roles within the 6-point column. The design incorporated ink traps at letter joins to absorb ink-spread on absorbent paper; the x-height was raised; the apertures were opened. This was evidence-driven design without formal reading-science research-survey, informed by the phone company's field data on reader errors. See Shaw (2008) and the Carter interviews collected in Howard 2002.

Tobias Frere-Jones's **Retina** (*Wall Street Journal*, 1999) is a parallel case: a type designed for stock-table listings at 5 pt on newsprint, with ink traps, opened apertures, and spacing tuned empirically against printed proofs. Frere-Jones's design notes on Retina are explicit that the small-size optimisations were tested against actual newsprint output, iteratively — the design methodology is exactly the punchcutter's, using offset-press proofs as the feedback loop.

These are not peer-reviewed findings. They are *evidence-driven design*: craft that accumulated measurable compensations through iteration. The reading-science literature that followed largely confirmed the intuitions these designers had already baked into their small-size cuts.

## Contemporary empirical research-survey

Four research-survey programmes ground the modern evidence base for opsz.

### Research programmes overview

The reading-science evidence base for opsz is distributed across a small set of research-survey programmes that have run in parallel since the late 1990s. Each contributes a different empirical angle; the practitioner-facing picture emerges from their rough convergence.

- **Beier (Royal Danish Academy, c. 2005–present)** — letter-identification thresholds and reading-speed studies on sans-serif designs; direct collaborations with Larson on frequently-misrecognised letters; with Ouwehand on text-vs-display-cut performance. *Reading Letters* (2012, rev. 2022) is the consolidated synthesis.
- **Larson (Microsoft Advanced Reading Technologies, c. 2001–2010)** — ClearType-era empirical work on screen legibility; Poynter Institute collaboration on serif-vs-sans; x-height and aperture-shape effects at body sizes.
- **Legge and colleagues (Minnesota, c. 1985–present)** — psychophysics of reading; critical print size and reading acuity; MNREAD chart; low-vision reading. Legge & Bigelow (2011) is the integration paper for typographers.
- **Pelli and colleagues (NYU, c. 1995–present)** — letter-identification efficiency; crowding theory; feature-integration accounts of reading. Pelli, Palomares & Majaj (2004) on crowding is the most-cited contemporary contribution.
- **Chaparro / SURL (Wichita State, c. 2000–present)** — applied usability studies on reading speed and comprehension at specific sizes and fonts; consumer-rather-than-laboratory focus.
- **Dyson (Reading, c. 1990s–present)** — screen reading, line length, scroll-vs-page, methodology. Less directly opsz-focused but important for the screen-specific evidence.

These programmes have methodological overlaps (Beier's letter-identification paradigm descends from Pelli; Larson's ClearType work draws on Legge's CPS framework; Chaparro and SURL use population-usability methodology closer to applied ergonomics) but they are not a single coordinated research-survey programme. The opsz-relevant evidence is a *synthesis across* rather than *output from* the reading-science community, which is part of why practitioner summaries vary in their specific numeric claims.

### Sofie Beier and *Reading Letters*

Sofie Beier's *Reading Letters: Designing for Legibility* (BIS Publishers, 2012; revised edition 2022) is the consolidated practitioner-facing synthesis of reading science for type-design decisions. Beier's own experimental programme — conducted first at the Royal Danish Academy and continued with collaborators including Kevin Larson and Nicholas Ouwehand — runs letter-identification, reading-speed, and preference studies on specific glyph-shape decisions.

Key findings relevant to optical sizing:

- **Aperture openness is a first-class legibility predictor at small sizes.** Beier's threshold-identification studies at 6-point equivalent sizes show that fonts with open apertures on `c`, `e`, `s`, `a` produce measurably lower identification-error rates than fonts with closed apertures at the same size, controlling for x-height and weight. The exact effect-size numbers vary by experiment; the design-community figure of "12–18% improvement in identification accuracy at 6 pt" circulates in summaries of Beier's work and is consistent with the effect direction she reports, though Beier herself typically reports error-rate differences rather than percent-accuracy shifts.
- **X-height-to-cap-height ratio modulates small-size legibility.** Tall x-height fonts outperform short-x-height fonts at body sizes below ~12 pt on typical displays, consistent with Chaparro et al. below.
- **Crowding is the dominant small-size inhibitor.** Beier's work interacts with Pelli's crowding research-survey — a font's default sidebearings act as built-in de-crowding, and text cuts of optical families ship wider sidebearings by design.
- **Body-text cuts of serif families perform comparably to sans at the same size.** Beier and other researchers find no categorical serif-vs-sans difference at typical sizes when the serif is a dedicated text cut (e.g., ITC New Baskerville Text, Minion Text, Source Serif Small Text) rather than a display cut scaled down.

Beier's work is the closest thing the type-design field has to a consolidated empirical reference for optical-size decisions. The 2022 revision incorporates subsequent research-survey including her collaborations with Nicholas Ouwehand on optical-size compensation.

### Charles Bigelow and the history+rationale literature

Charles Bigelow (co-designer of Lucida, long-time writer on reading and typography) has published a series of papers weaving together the history of optical sizing and the empirical case for it. His 2011 *Journal of Vision* paper with Gordon Legge (cited below) is the most-referenced integration of vision science and typography for practitioners. Subsequent work — including a 2019 article on optical size's history and rationale, and shorter treatments in *TUGboat* — consolidates the argument that optical-size compensation is a design response to measurable perceptual constraints, not merely a stylistic tradition.

Bigelow's work is the right starting point for practitioners who want to understand *why* the optical-size tradition survived from punchcutting into the digital era. It is historical synthesis informed by vision science, not experimental research-survey in itself.

### Kevin Larson and ClearType-era research-survey

Kevin Larson's work at Microsoft's Advanced Reading Technologies group (~2001–2010) produced the empirical base underlying the ClearType type collection — Calibri, Cambria, Candara, Consolas, Constantia, Corbel. Larson's 2004 essay *The Science of Word Recognition* is the canonical short statement of the modern consensus that skilled readers recognise words through parallel letter recognition (see `./word-shape-vs-parallel-letter.md`), which reframes what optical-size compensation is *for*: supporting rapid letter identification at the target size, not supporting a supposed whole-word-shape recognition that the literature doesn't actually support.

Larson's group also sponsored the Poynter Institute study comparing serif and sans screen-reading (finding no robust comprehension difference, consistent with Beier's later work) and conducted internal studies on x-height and aperture-shape effects at ClearType-era screen resolutions (~96–120 ppi). The ClearType faces are *evidence-informed* rather than *evidence-published* — much of the underlying data sat in Microsoft internal reports — but the design direction (tall x-heights, open apertures, generous sidebearings for body; less compensation for display) tracks with the public literature.

### Gordon Legge and the psychophysics of reading

Gordon Legge's Minnesota laboratory has been the centre of psychophysics-of-reading research-survey since the 1980s. Two contributions matter for optical sizing:

**Legge, Pelli, Rubin & Schleske (1985, *Vision Research*)** introduced the *critical print size* (CPS) and *maximum reading speed* framework: reading speed rises with print size up to a threshold (CPS, typically 0.2°–0.5° of visual angle for normally-sighted readers) and plateaus beyond. This is the fundamental psychophysical curve that makes small-size optimisation matter: below CPS, every fraction of a degree of angular size gained back by better glyph tuning is directly recoverable reading speed.

**Legge & Bigelow (2011, *Journal of Vision*)** is the integration paper for typographers. It reviews the psychophysical evidence on print size, contrast, and font choice and draws out implications for type design, including optical-size compensation. The paper is deliberately hedged — it declines to crown a "best" print size or font — but it provides the most defensible summary of what vision science supports about size-specific design decisions. Among its findings relevant to opsz:

- The plateau in reading speed is approached gradually; there is no sharp CPS below which reading fails.
- Individual-reader variance in CPS is large — what is comfortable for one reader may not be for another.
- Font-specific differences in CPS exist and are on the order of 10–30% between a well-designed text cut and a display face at the same point size. (Legge & Bigelow emphasise that this is a *small* effect compared with individual and contextual variance.)

### Chaparro and SURL

Chaparro, Shaikh & Chaparro (2010, *Ergonomics*), conducted at Wichita State's Software Usability Research Laboratory (SURL), measured reading speed and comprehension across sans-serif fonts at 10–14 point screen sizes. The most-cited result: **taller-x-height fonts produce ~7% faster reading speed at body sizes (8–10 pt equivalent) than shorter-x-height fonts at the same point size**, with no comprehension difference. This is the best short quantitative summary available for the x-height effect at small sizes, and it is consistent with Beier's later work.

Bernard, Liao & Mills (2001, *Usability News*) is an earlier Wichita State study in the same tradition, comparing serif and sans-serif online reading for older adults; it found no categorical readability difference but did find measure-and-size-and-font interactions.

### Pelli, Farell, Moore, and letter-identification efficiency

Denis Pelli's letter-identification-efficiency research-survey is the other pillar of the contemporary evidence base. **Pelli, Farell & Moore (2003, *Nature*)** — "The remarkable inefficiency of word recognition" — measured the information-theoretic efficiency of reading at different print sizes. Key finding for opsz: at display sizes (72 pt and above in their experimental conditions), letter-identification efficiency saturates — foveal resolution is no longer the bottleneck, and reader performance does not improve with further glyph tuning. This is the empirical base for the claim that display-size optical compensation is *aesthetic* rather than *functional*: once print size is above the critical range, thin serifs, hairlines, and tight spacing do not hurt legibility.

Pelli, Palomares & Majaj (2004, *Journal of Vision*) — on crowding — is covered in `./crowding.md`; its relevance to opsz is that small-size cuts' wider sidebearings are a direct de-crowding compensation, and its framing of *critical spacing* (~0.5× eccentricity) is what determines how much space a small-size cut needs between its letters.

Pelli, Burns, Farell & Moore-Page (2006, *Vision Research*) measured feature-detection thresholds for letter identification and showed that identification requires detecting roughly 7 visual features per letter — consistent with the idea that small-size cuts, by opening apertures and thickening strokes, make those features individually more detectable.

### Arditi on large-size and low-vision typography

Aries Arditi's research-survey on large-print and low-vision typography (e.g., Arditi 2004, *Ergonomics*) provides the complementary finding for display sizes: at large print sizes, the display-cut stylistic flourishes (hairlines, dramatic contrast) do not hurt legibility, but they also do not help it for readers with normal vision. For low-vision readers reading at enlarged sizes, stroke robustness and aperture openness still matter — which means that a display cut at 36 pt may be *less* usable for some low-vision readers than a text cut at the same rendered size. This is the empirical counter to the "display cuts are always appropriate at display sizes" assumption.

### Ouwehand and Beier on optical-size compensation

Nicholas Ouwehand's research-survey with Sofie Beier at the Royal Danish Academy, around 2020, directly compared reading performance on text-cut vs display-cut masters rendered at the same body size. The practitioner summary: **at a 9-point body-text size, using the text cut of an optical family produced reading-speed improvements of roughly 5–8% over the display cut of the same family**. This is the most directly opsz-relevant finding in the recent literature and corroborates the design intuition that optical-size compensation is functionally, not merely stylistically, valuable at body sizes. Ouwehand and Beier's work has been presented at type-design conferences and published in the *Information Design Journal*; formal peer-reviewed replication in vision-science venues is still developing.

## Specific empirical findings relevant to opsz

A consolidated summary of the quantitative findings most often cited in opsz discussion. Effect-size numbers are reported where the primary source states them; when a figure circulates in design-community summaries but is not precisely attributable to a published experiment, the phrasing makes that explicit.

**Aperture openness at small sizes.** Beier's (2012, 2022) threshold-identification studies and subsequent work with Larson (Beier & Larson 2010) establish that open-aperture glyph forms yield measurably lower identification-error rates at sub-8-point equivalent sizes than closed-aperture forms at the same x-height and weight. The practitioner-facing summary that circulates in opsz writing — "12–18% improvement in identification accuracy at 6 pt for opened apertures" — is consistent with Beier's experimental effect direction, though Beier reports most results as error-rate ratios or threshold-exposure-time shifts rather than accuracy percentages. The underlying effect is robust; the specific number should be treated as an order-of-magnitude claim.

**Taller x-height improves small-size reading speed.** Chaparro, Shaikh & Chaparro (2010) measured reading speed across fonts with varied x-height-to-cap-height ratios at 8–10 pt equivalent screen sizes and found approximately **7% faster reading for tall-x-height over short-x-height fonts**, with no comprehension difference. This is the best-sourced quantitative number in the opsz-adjacent literature. The effect does not scale linearly to display sizes — at 24 pt and above, x-height-to-cap ratio has no measurable speed effect.

**Serif vs sans at small sizes is font-specific, not categorical.** Bernard, Liao & Mills (2001) compared specific serif and sans-serif pairs at online reading sizes and found no categorical advantage for either category. Subsequent work (Beier, Chaparro, the Poynter study sponsored by Microsoft) reaches the same conclusion: a purpose-drawn text cut of a serif family (e.g., ITC New Baskerville Text, Minion Text, Source Serif Small Text) performs comparably to a purpose-drawn sans at the same size. The difference between a display-cut serif scaled down to body and a text-cut sans at the same size is, however, substantial — and tracks with opsz tuning rather than with serif-vs-sans classification.

**Text-cut vs display-cut at body size.** Ouwehand & Beier's direct comparison (c. 2020) reports an approximately **5–8% reading-speed improvement at 9-pt body for the text cut over the display cut of the same optical family**. This is the most directly opsz-relevant quantitative finding in the contemporary literature. Formal peer-reviewed replication of the specific effect size is limited; the finding is presented at type-design venues and in the *Information Design Journal*.

**Display-size legibility is saturated.** Pelli, Farell & Moore (2003) show that letter-identification efficiency plateaus at large print sizes — at 72 pt in their experimental conditions, further size increases do not increase identification accuracy. This is the empirical base for the claim that display-cut optical tuning is aesthetic rather than legibility-driven. Arditi (2004) extends the finding to large-print typography for low-vision readers, where stroke robustness still matters but hairline detail does not hurt performance.

**Transitional-range tuning is under-studied.** Between roughly 18 pt and 48 pt, where neither small-size constraints nor display-saturation conditions apply cleanly, the empirical literature is sparse. Most reading-science work is done at either body sizes (8–14 pt) or display sizes (36 pt+); the intermediate zone (subheads, standfirsts, UI headlines) is covered mainly by design practice and intuition.

## Display-size research-survey

The display-size case is where the reading-science and type-design communities partially disagree. The reading-science evidence (Pelli 2003; Legge & Bigelow 2011; Arditi 2004) is that at large rendered sizes (roughly 36 pt and above for normally-sighted readers), legibility saturates — display-cut hairlines and tight spacing do not hurt measurable reading performance. The type-design community argues that display cuts still *look better* at large sizes — less bloated, more elegant, more tonally refined — and that aesthetic appropriateness is a legitimate reason for optical compensation even in the absence of a legibility gain.

The synthesis: both are true. Display-cut optical compensation is *not functional* in a reading-speed sense at 72 pt+; it is *aesthetically functional* in that a body-cut rendered at 72 pt looks heavier and looser than the reader expects for a headline, and readers integrate that visual cue into their impression of the page. Legibility is saturated; tone is not. The opsz axis at display sizes is tuning for voice, not for identification.

A middle-range question remains open. Between ~18 pt and ~48 pt, the transition between body-tuned and display-tuned rendering happens gradually in a variable opsz axis, and both the reading-science and the type-design communities acknowledge that no sharp breakpoint exists. A discrete optical family with *Text / Subhead / Display* masters imposes steps; the opsz axis spreads the transition. No peer-reviewed evidence currently settles whether a continuous interpolation is perceptually superior to well-chosen discrete masters — see *Caveats* below.

## Crowding interactions with optical size

The crowding literature (see `./crowding.md`) provides the mechanistic story for why small-size cuts widen sidebearings. Bouma's law (1970) gives the critical-spacing rule: for peripheral vision, crowding integrates features over roughly 0.5× the eccentricity. Pelli, Palomares & Majaj (2004) showed that crowding is *not* classical masking — it is a failure of feature integration, and the critical spacing is determined by the flanker positions, not by the flanker brightness or contrast. In foveal reading, crowding is reduced but non-zero, and at small body sizes it becomes a dominant constraint.

The consequence for opsz: **small-size cuts' wider sidebearings are a direct response to crowding**. A text-cut font at 8 pt sets its letters at a spacing that would feel loose at 24 pt but that keeps adjacent letters outside each other's critical-spacing zones at the small size. A display cut at 8 pt, with tighter sidebearings, puts the letters inside each other's critical-spacing zones and produces crowding-limited identification errors.

At display sizes, crowding is negligible *within* the title — the inter-letter spacing is many times the critical spacing at foveal acuity. Display cuts can therefore afford tighter sidebearings with no crowding cost; the tight spacing reads as tonal cohesion.

This means the opsz axis captures two physically distinct phenomena simultaneously: the small-size end is compensating for crowding and for rendering-noise-limited stroke visibility, and the large-size end is adjusting aesthetic tone without a legibility constraint.

## Why the opsz axis works as continuous

The reading-science evidence suggests that optical-size optimisation is *continuous* rather than discrete: reading-performance varies smoothly with rendered size, not step-wise. Beier's identification-threshold measurements, Chaparro's reading-speed data, and Legge's CPS curves all show smooth functions of print size, not plateaus with sharp transitions. A continuous opsz axis — interpolating between designer-authored masters at, say, 8 / 14 / 24 / 72 pt — matches this continuous perceptual function more directly than four discrete cuts.

That said, a few type designers prefer discrete cuts and argue against continuous opsz on practical grounds:

- Interpolation between masters produces glyph shapes the designer did not explicitly draw. A "16-point" master sitting halfway between the 14-point and 24-point designer-drawn masters is a compromise the designer did not verify looks right.
- Most usage is concentrated at a small number of sizes (caption, body, subhead, headline). The "middle" opsz values between body and subhead are rarely actually set, so the interpolation fills a space no reader occupies.
- Static cuts are the legacy interchange format; a variable opsz font is less portable to non-VF-aware pipelines.

These are pragmatic objections to the variable approach, not evidence-based arguments against continuity. The reading-science evidence, insofar as it addresses the question, supports the continuous formulation. Peer-reviewed work directly comparing continuous variable opsz to matched discrete cuts in eye-tracking terms does not yet exist at publication-grade depth.

## Screen-specific considerations

Reading-science research-survey on optical sizing in the digital era has to contend with a complication the punchcutters did not: rendering. Modern displays vary in device pixel ratio (DPR, 1× to 3×+), subpixel-antialiasing support (RGB-stripe horizontal, various vertical on OLED), and gamma handling. An opsz master tuned for 9-point rendering at 96 dpi renders differently at 216 dpi — the hairlines that survive rendering on a retina display may fringe on a 1× monitor.

Practical consequences that the literature alludes to but has not systematically characterised:

- On high-DPR displays, small-size opsz masters work closer to their design intent because sub-pixel positioning resolves the hairlines and sidebearings accurately.
- On low-DPR displays (increasingly rare in 2026 but still present in legacy kiosks, projectors, and budget mobile devices), the small-size masters' stroke robustness becomes more critical — a display-cut rendered at 9 pt on 96 dpi can drop hairlines entirely, while a text-cut renders intact.
- Browser implementation of `font-optical-sizing: auto` converts CSS font-size (reference pixels) to points via the spec-defined 96/72 conversion, but the *rendered* output depends on zoom, DPR, and subpixel rendering — which means the opsz position chosen does not always match the physically rendered size. This drift is usually small (single-digit percent) but can be visible in cross-browser audits. See `../techniques/optical-size.md` §Interaction with zoom for the implementation details.

The reading-science evidence base is predominantly print-derived with a significant body of screen-specific work from the Dyson lab and the ClearType era. The opsz-specific literature has not systematically compared, say, "opsz 9 at 9-point printed paper" to "opsz 9 at 9-point CSS at 2× DPR at 100% zoom." This is a live gap; designers working on opsz typography at production scale should verify rendering on their target devices rather than trust the axis's nominal value to map onto the reader's physical experience.

## Notable research-driven fonts

A short list of fonts whose optical-size design is empirically grounded, either through field data, through the designer's documented research-survey process, or through direct collaboration with reading-science researchers.

| Font | Designer / year | Research base |
|---|---|---|
| **Bell Centennial** | Matthew Carter, 1978 | AT&T / Bell Labs field data on phone-directory reading errors; four hand-drawn cuts for 6-point rendering on Bible paper. |
| **Retina** | Tobias Frere-Jones, 1999 (revised 2016+) | *Wall Street Journal* stock-table reading requirements; ink-trap-equipped small-size cuts iterated against newsprint proofs. |
| **Verdana** | Matthew Carter, 1996 | Microsoft research-survey on screen reading at 10–14 px on low-DPI displays; tall x-height, open apertures, generous sidebearings. |
| **Georgia** | Matthew Carter, 1996 | Same programme as Verdana; serif variant with hinting tuned for 10–14 px screen reading. |
| **ClearType family** (Calibri, Cambria, Candara, Consolas, Constantia, Corbel) | Various, coordinated by Larson at Microsoft, 2004–07 | ClearType Advanced Reading Technologies programme; empirically tuned for DirectWrite subpixel rendering at body sizes. |
| **Chaparral Pro** | Carol Twombly, 2000 | Slab serif with discrete optical cuts (Caption / Regular / Subhead / Display) informed by Adobe's typographic research-survey. |
| **Source Serif (1–4)** | Frank Grießhammer, Adobe, 2014–21 | Open-source; four discrete optical cuts (Caption, Small Text, Text, Subhead, Display), with the 2021 variable release exposing opsz 8–60. |
| **Literata** | TypeTogether, 2015 / variable 2019+ | Commissioned originally for Google Play Books reading; discrete cuts tuned at 7, 12, 36, 72 pt; variable version opsz 7–72. |
| **Fraunces** | Undercase Type, 2020 (variable) | opsz 9–144; design notes document the small-size compensations explicitly — x-height rises, spacing opens, characters widen as opsz decreases. |
| **Roboto Flex** | David Berlow / Google, 2022 | opsz 8–144 as the headline axis; 13 total axes; explicitly positioned by Google Fonts as a parametric research-survey vehicle for optical sizing. |
| **Amstelvar** | David Berlow / TypeNetwork, 2017 onward | The parametric-fonts reference; opsz 8–144 with default 12. |

The Matthew Carter lineage (Bell Centennial → Verdana → Georgia) is the clearest example of evidence-driven optical-size design outside the formal psychophysics literature: each was commissioned against a specific reading failure mode, iterated against empirical output, and produced design decisions that the subsequent reading-science research-survey broadly validated.

## Methodological limitations of the evidence base

The opsz-relevant reading-science literature is consistent in direction but limited in a few specific ways that matter for interpreting the practitioner-facing claims.

**Population homogeneity.** Most studies recruit undergraduate populations (young, normally-sighted, left-to-right Latin-reading, often native English speakers). Findings replicate for readers in this demographic. Generalisation to older readers, low-vision readers, readers whose primary reading language is non-Latin, and readers with reading disabilities is plausible for some findings (x-height, aperture openness are robust across populations) but less clear for others (display-size saturation, specific reading-speed effect sizes).

**Short reading sessions.** Laboratory reading-speed measurements typically run for minutes, not hours. Whether the small-size opsz advantage accumulates across a multi-hour reading session, or whether adaptation reduces the effect, is not well characterised. The print-typography tradition (Carter on Bell Centennial, Frere-Jones on Retina) assumed sustained-reading advantages from small-size tuning, but the empirical evidence for sustained-reading effects specifically is thin.

**Screen-vs-print asymmetry.** Print studies on optical sizing were conducted on specific paper and ink combinations with specific press characteristics. Screen studies are conducted on specific displays at specific DPR with specific rendering (ClearType / DirectWrite / CoreText / FreeType). Cross-medium replication is not routine. A 9-pt opsz advantage measured on newsprint does not automatically translate to a 9-CSS-pt advantage on a 2× DPR OLED display, and vice versa.

**Effect sizes are modest.** The numbers circulating in opsz discussion (7% reading speed, 12% identification accuracy, 5–8% text-vs-display at body) are meaningful but small compared to other reading variables. Individual reader variance, contextual noise (lighting, fatigue, prior familiarity), and measurement noise are all larger than most of the opsz-specific effects. This does not invalidate the findings — a reliable 7% improvement is substantial over many hours of reading — but it does mean opsz is not a first-order reading-performance lever the way, say, moving body size from 8 pt to 14 pt is.

**Publication bias and file-drawer effects.** As with most of applied reading research-survey, null and weak-effect findings are less likely to be published than positive findings. The practitioner-facing literature therefore skews toward confirming opsz benefits; if there are studies in the file drawer showing no opsz advantage at specific sizes or conditions, they are under-represented. The direction of the effect is robust enough across independent programs (Beier, Larson, Chaparro, Legge) that this concern is modest, but it is not zero.

## Caveats and open questions

The literature supports the main claims about optical sizing reasonably well, but several areas remain unsettled.

- **Individual-reader variability is large.** Legge & Bigelow (2011) and Chaparro's SURL work both note that individual CPS, preferred size, and font-specific differences vary substantially across readers. A "7% reading-speed improvement from taller x-height" is a group average; individual readers may show no effect, or twice the effect.
- **Low-vision and dyslexic populations.** Opsz research-survey has been almost entirely conducted on normally-sighted adult readers. Low-vision readers tend to benefit from stroke robustness across sizes (Arditi 2004), which suggests text-cut masters work at display sizes *for them* even though the normally-sighted literature shows display cuts saturate legibility there. Dyslexic readers' needs on opsz specifically are under-studied; the general finding that dyslexia-specific fonts do not robustly outperform good text faces (see `./legibility-vs-readability.md`) extends by default — a well-tuned opsz family is likely as good as a dyslexia-marketed font at the relevant sizes.
- **Non-Latin scripts.** Essentially all opsz research-survey is Latin. CJK has its own size-specific design tradition (e.g., kaitai vs mincho proportions at different sizes; see `../scripts/cjk-han.md`, `../scripts/japanese.md`) but the research-survey base connecting size-specific CJK choices to reading-science measures is thin. Arabic Naskh at body vs display size has qualitative treatment in the *Journal of the Foundation Andalusia* and in Titus Nemeth's *Arabic Type-Making in the Machine Age*, but peer-reviewed experimental opsz work on Arabic is rare. Devanagari, Hebrew, Thai: similar.
- **Screen vs print opsz tuning.** The `opsz` axis numerically maps to typographic points regardless of medium, and browser implementations use the 96/72 CSS-points conversion — which means the same opsz value is applied to a 9-point printed page and to a 9-CSS-point screen rendering. Whether the *perceptual* optimum at those two media is actually the same is not established. Print and screen impose different rendering constraints (ink spread vs subpixel antialiasing; reflective vs emissive), so there is reason to suspect the optimal opsz for 9-point on paper differs from 9-point on an OLED panel at 2× DPR. Production type designers handle this ad hoc; the research-survey literature has not characterised it.
- **Continuous axis vs discrete masters, empirically.** Direct peer-reviewed eye-tracking comparisons of a continuous opsz axis against matched discrete cuts do not yet exist at the depth the variable-fonts industry has begun to claim. The design-intuition case for continuity is strong; the empirical replication is pending. `./legibility-vs-readability.md` lists this as an open question.

## What this means for contemporary designers

From the evidence base, practitioner-level guidance.

1. **Use `font-optical-sizing: auto` on variable fonts with `opsz`.** The axis does what it is designed to do; the browser wires rendered font-size to opsz value via the 96/72 conversion; the design intent is preserved without effort. Don't disable the axis globally.

2. **For non-variable font families, choose discrete opsz cuts where content span demands it.** Long-form editorial work that moves between 10-point body, 14-point intro paragraphs, 24-point subheads, and 72-point headlines benefits tangibly from matching the cut to the size. A single master across that range produces bloated headlines or fragile body.

3. **For UI typography between 13 and 18 px, the opsz benefit is modest.** The type-scale movement within a narrow band of sizes is small; the glyph tuning along a 13–18 pt opsz range is subtle. Roboto Flex at `opsz 10` vs `opsz 14` is a visible difference in specimen sheets; in shipping UI with those sizes interleaved, the difference is perceptible but not a first-order readability gain. Budget opsz attention accordingly.

4. **For editorial long-form body prose (10–12 pt body), opsz tangibly improves reading experience.** Both Ouwehand & Beier's direct comparison and Chaparro's x-height research-survey support this. If the font is available with optical sizing and the content is prose, use it.

5. **For display headlines (72 pt+), treat opsz as tone management rather than legibility.** Legge-Bigelow and Pelli's work show legibility is saturated. The display cut is aesthetic, not corrective. Use it for tonal coherence; override it deliberately when a *brand choice* wants a body-cut chunkiness at headline size.

6. **Pair opsz-equipped fonts with other opsz-equipped fonts, or with static non-opsz fonts held at a single role.** An opsz-tuned display face next to a non-opsz-tuned body face at the same 72 pt headline is an asymmetry readers will feel even if they can't name it. See `../techniques/optical-size.md` §Anti-patterns for the full list of opsz-pairing traps.

7. **Do not design around the pre-Firefox-120 rendering bug.** As of 2026-04, users on bugged pre-120 Firefox builds are a shrinking minority; the bug is fixed in shipping releases. Designing to match the buggy rendering creates regressions when users upgrade.

The short version: opsz compensates measurably for small-size reading constraints the vision-science literature has characterised; it adjusts aesthetic tone at display sizes without a legibility cost; and a continuous axis matches the continuous perceptual function better than discrete cuts, though the peer-reviewed evidence for continuity specifically is still developing.

## Relation to the broader reading-science consensus

Reading the opsz literature in isolation can overstate how much it matters. A fuller picture:

- **Measure, leading, and size dominate over font choice.** Rayner and colleagues' extensive eye-tracking programme (see `./legibility-vs-readability.md`) consistently finds that characters-per-line, line-height, and font size dominate the variance in reading speed and comfort; the gap between well-designed fonts at the same metric settings is smaller than the gap between good and bad metric settings of the same font. Optical-size tuning sits inside that latter, smaller gap.
- **Opsz is a refinement, not a foundation.** Fixing a page's measure (targeting 45–75 CPL for Latin prose) and leading (1.4–1.6 for body) produces larger gains than switching from a single-master font to an opsz variable font at the same size. The "use opsz" advice assumes the other typographic variables are already reasonable.
- **The Larson consensus on parallel letter recognition reframes the goal.** If skilled readers recognise words through parallel letter recognition (see `./word-shape-vs-parallel-letter.md`), then the purpose of opsz compensation is to make individual letter identification as fast and accurate as possible *at the rendered size*. Opsz is not about "preserving word shape"; it is about keeping letter-level identification efficient, which the small-size compensations (open apertures, wider spacing, tall x-height) directly support.
- **Crowding is the mechanistic bridge.** Pelli's crowding work (Pelli, Palomares & Majaj 2004) gives the mechanism by which small-size cuts' wider sidebearings translate to faster reading: adjacent letters are moved outside each other's critical-spacing zones, reducing feature-integration errors. This is the cleanest causal story the literature has for why opsz works at small sizes.
- **Display-size opsz sits outside the reading-speed story.** Once print size is above CPS and crowding is negligible, the remaining typographic choices affect tone but not measurable reading performance. Display-cut opsz is therefore *pursued* by designers for aesthetic coherence, not *required* for legibility. This is a legitimate pursuit, but it should not be framed as an empirical finding from reading science.

The net: opsz is a measurable, small-to-moderate improvement at small sizes, an aesthetic refinement at large sizes, and one component of a larger typographic system where measure, leading, size, and font choice all interact. Treat it as part of a well-tuned system, not as a standalone optimisation.

## Cross-references

- `../techniques/optical-size.md` — the `opsz` CSS/axis/browser mechanics. Font inventory. Anti-patterns.
- `./legibility-vs-readability.md` — the distinction between glyph-identification and running-text measures; the canonical research-survey lineage.
- `./crowding.md` — Bouma's law and Pelli-era crowding; the mechanistic story for why small-size cuts widen sidebearings.
- `./word-shape-vs-parallel-letter.md` — the parallel-letter-recognition consensus; reframes what opsz compensation is supporting.
- `../contemporary/variable-fonts.md` — the broader variable-font axis mechanics `opsz` sits within.

## Sources

(Retrieval dates: all 2026-04-18 where URLs are cited.)

- **Arditi, A.** (2004). "Adjustable typography: an approach to enhancing low vision text accessibility." *Ergonomics* 47(5): 469–482. https://doi.org/10.1080/0014013031000153188
- **Beier, S.** (2012, rev. 2022). *Reading Letters: Designing for Legibility.* Amsterdam: BIS Publishers. https://www.bispublishers.com/reading-letters-revised.html
- **Beier, S., & Larson, K.** (2010). "Design improvements for frequently misrecognized letters." *Information Design Journal* 18(2): 118–137. https://doi.org/10.1075/idj.18.2.03bei
- **Bernard, M., Liao, C. H., & Mills, M.** (2001). "The effects of font type and size on the legibility and reading time of online text by older adults." *Usability News* 3.2. https://usabilitynews.org/
- **Bigelow, C.** (2019). Writings on optical size history and rationale. Collected in *TUGboat* and adjacent publications; see also *Language & Typography*.
- **Chaparro, B. S., Shaikh, A. D., & Chaparro, A.** (2010). "Keeping up with content on the web: Font size and reading comfort." *Ergonomics*. Software Usability Research Laboratory, Wichita State University.
- **Frere-Jones, T.** (2007, with 1999 design). "Retina" — notes and specimen for the *Wall Street Journal* stock-table face. https://frerejones.com/retina
- **Howard, M.** (ed.) (2002). *Typographically Speaking: The Art of Matthew Carter.* Cambridge, MA: MIT Press / Princeton Architectural Press. Interviews including Bell Centennial design notes.
- **Larson, K.** (2004). "The Science of Word Recognition." Microsoft Advanced Reading Technologies. https://learn.microsoft.com/en-us/typography/develop/word-recognition
- **Legge, G. E., Pelli, D. G., Rubin, G. S., & Schleske, M. M.** (1985). "Psychophysics of reading — I. Normal vision." *Vision Research* 25(2): 239–252. https://doi.org/10.1016/0042-6989(85)90117-8
- **Legge, G. E., & Bigelow, C. A.** (2011). "Does print size matter for reading? A review of findings from vision science and typography." *Journal of Vision* 11(5): 8. https://doi.org/10.1167/11.5.8
- **Ouwehand, N., & Beier, S.** (c. 2020). Reading-speed comparison of text vs display opsz cuts at 9-point body. Royal Danish Academy type research-survey group. Presented at Typographics and TypeLab events; partial publication in *Information Design Journal*.
- **Pelli, D. G., Farell, B., & Moore, D. C.** (2003). "The remarkable inefficiency of word recognition." *Nature* 423(6941): 752–756. https://doi.org/10.1038/nature01673
- **Pelli, D. G., Palomares, M., & Majaj, N. J.** (2004). "Crowding is unlike ordinary masking: distinguishing feature integration from detection." *Journal of Vision* 4(12): 12. https://doi.org/10.1167/4.12.12
- **Pelli, D. G., Burns, C. W., Farell, B., & Moore-Page, D. C.** (2006). "Feature detection and letter identification." *Vision Research* 46(28): 4646–4674. https://doi.org/10.1016/j.visres.2006.04.023
- **Shaw, P.** (2008). "A fresh look at Bell Centennial." *Print* magazine / Paul Shaw Letter Design archive. http://www.paulshawletterdesign.com/
- **Google Fonts / TypeNetwork.** Roboto Flex research-survey log and specimen documentation. https://github.com/googlefonts/roboto-flex
- **Undercase Type.** Fraunces specimen and design notes. https://github.com/undercasetype/Fraunces
- **Adobe / Frank Grießhammer.** Source Serif optical-sizes blog post (2021-03-04) and repository. https://blog.adobe.com/en/publish/2021/03/04/source-serif-gets-optical-sizes and https://github.com/adobe-fonts/source-serif
- **Berlow, D. / TypeNetwork.** Amstelvar parametric reference font. https://github.com/googlefonts/amstelvar
