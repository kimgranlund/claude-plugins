---
date: 2026-04-17
coverage: medium
peers:
  - ./wcag-type.md
primary_sources:
  - https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide
  - https://link.springer.com/article/10.1007/s11881-018-0154-1
  - https://dl.acm.org/doi/10.1145/2461121.2461126
  - https://journals.sagepub.com/doi/10.1177/0956797612457377
  - https://lexend.com/
  - https://opendyslexic.org/
  - https://dyslexiaida.org/
---

# Dyslexia-Specific Fonts: An Evidence Review

**Peers:** [WCAG 2.2 type SCs and WCAG 3.0 directions](./wcag-type.md) — for the baseline typographic floors (SC 1.4.3, 1.4.4, 1.4.8, 1.4.12) that apply to all readers, dyslexic or not. The two files are complementary: WCAG defines the floor; this file asks what — beyond the floor — actually helps dyslexic readers, and whether the "dyslexia-friendly" fonts marketed for that purpose hold up to the evidence.

Honest summary upfront: **the evidence for dyslexia-specific fonts (OpenDyslexic, Dyslexie, Lexie Readable) is weak and largely negative.** Spacing, measure, and size interventions have stronger support. The prudent practitioner offers dyslexia-fonts as a user preference — never as the default — and invests design budget in the spacing/measure/contrast work that has better-backed returns.

---

## Part 1 — What dyslexia is, and isn't

### Definition and prevalence

**Developmental dyslexia** is a neurobiologically-based specific learning difference characterised by difficulties with accurate and/or fluent word recognition, poor spelling, and decoding abilities — typically in the presence of adequate intelligence, instruction, and sensory acuity. The operational definition comes from the **International Dyslexia Association** (IDA, 2002) and is widely adopted in research-survey.

**Prevalence estimates vary with diagnostic strictness:**
- **5–10%** — strict operational definitions (Lyon, Shaywitz & Shaywitz, 2003)
- **10–15%** — broader definitions including "reading difficulties" more generally
- **17–20%** — when including all "struggling readers" (Shaywitz 1998 epidemiological estimates)

The spread matters: practitioner materials often cite "1 in 10" or "1 in 5", and both are defensible depending on which criteria you accept. **Roughly 10%** is the conservative, widely-cited figure.

### What dyslexia is not

Dyslexia is distinct from — but sometimes co-occurs with — several other conditions that affect reading:

- **Low vision / visual impairment.** Uncorrected refractive error, macular degeneration, diabetic retinopathy. Typographic needs: higher contrast (WCAG 2.2 SC 1.4.3 and beyond), larger sizes, higher APCA. See [wcag-type.md](./wcag-type.md).
- **Visual stress / Meares-Irlen syndrome.** Contested construct; clusters of symptoms (print glare, letter movement, after-images) sometimes treated with coloured overlays. See §4 below; evidence is disputed.
- **Attention difficulties (ADHD).** Can produce reading errors that resemble dyslexia but respond to different interventions.
- **Acquired reading disorders** (pure alexia, hemi-neglect alexia) — post-stroke or post-trauma. Distinct clinical picture.
- **English-as-second-language reading difficulty.** Lower reading rate and higher error rate in L2; not dyslexia. Different intervention space.
- **General cognitive-load issues** — complex vocabulary, dense layout, distractions. Addressed by WCAG SC 3.1.5 and information-design choices, not by typographic interventions specific to dyslexia.

**Dyslexia is a spectrum.** The subtypes most discussed in the design literature:
- **Phonological dyslexia** — difficulty mapping graphemes to phonemes; the most common form.
- **Surface dyslexia** — difficulty with whole-word recognition; over-reliance on phonological decoding.
- **Visual dyslexia** — letter reversals, word-order errors. Contested as a distinct subtype; many researchers treat visual errors as downstream effects of phonological issues.

The marketing around dyslexia-specific fonts overwhelmingly targets the **visual-dyslexia** theory — the idea that dyslexic readers rotate, flip, or reverse letters and would benefit from a font that disambiguates rotation-similar pairs. This theory is not the consensus in contemporary cognitive neuroscience of reading, which attributes most dyslexic errors to phonological decoding problems, not visual-processing problems. See §3.

### Literatures: English vs other orthographies

Research on dyslexia is heavily skewed toward **alphabetic scripts**, primarily **English**, secondarily other European languages (Italian, Spanish, German, Dutch, Finnish). Findings do not transfer cleanly to:

- **CJK (Chinese, Japanese, Korean).** Logographic and mixed scripts; dyslexia in these scripts appears to involve different sub-skills (visuospatial memory of character forms, morphological awareness). Font interventions tested on English have no prima facie applicability.
- **Arabic, Hebrew, other RTL Semitic scripts.** Consonantal roots, diacritical vowels, cursive connection in Arabic. Specific dyslexic patterns in these scripts are under-researched.
- **Devanagari, Thai, Tibetan.** Abugida/syllabic logic. Again, very different.

Practitioner rule: **do not cite Anglo-Dutch dyslexia research-survey to justify typographic decisions in CJK or Arabic contexts.** The literatures are not commensurable.

---

## Part 2 — The dyslexia-specific fonts

### OpenDyslexic (Abelardo González, 2011–present)

**Design brief.**
- **Weighted bottom** — letters have extra visual mass on the baseline half, on the theory that this resists rotation and flipping. Each letter has an asymmetric "heavy foot."
- **Unique letter shapes** — `b`, `d`, `p`, `q` are more differentiated than in most sans-serifs.
- **Wider inter-letter spacing** at default.
- **Italic variant.**
- **Monospaced variant** for code.

**Distribution.** Free under SIL Open Font License (as of 2024; earlier versions MIT). Available on Google Fonts and opendyslexic.org.

**Uptake.** Wide in advocacy circles — school accessibility services, some government toolkits. Amazon Kindle offers it as a built-in display option. Instapaper and several long-form readers include it.

### Dyslexie (Christian Boer, 2008)

**Design brief.** Boer (who has dyslexia himself) designed the font as a graduation project at the Utrecht School of the Arts. The design principles:
- Weighted baseline
- Enlarged apertures on `e`, `a`, `o`
- Slanted letters (i.e., `s`, `z`) to reduce mirroring confusion
- Enlarged letter spacing
- Taller ascenders and descenders
- Wider, heavier strokes

**Distribution.** **Proprietary.** Free for home/personal use; paid for education, institutional, and commercial licensing.

**Uptake.** Many Dutch educational institutions in the 2010s; interest has cooled since the Kuster et al. (2018) negative result (see §3).

### Lexie Readable (K-Type foundry, Keith Bates)

**Design brief.** Formerly "Lexia Readable." A humanist sans-serif designed for readability; not weighted-bottom; emphasises letter distinctness (especially `a`, `g`, `I`/`l`). More conservative visual style than Dyslexie or OpenDyslexic — more like a "careful sans-serif."

**Distribution.** Commercial, K-Type. Free for personal use; paid commercial license.

### Sylexiad (Robert Hillier, 2006)

A research-based typeface — Hillier's PhD thesis at Anglia Ruskin included user studies. Not commercially distributed; primarily an academic artifact. Shares the weighted-bottom principle with Dyslexie and OpenDyslexic.

### Design claims common across all four

1. **Letter rotation resistance** (weighted bottom).
2. **Increased inter-letter spacing** (reduces crowding).
3. **Differentiated mirror-confusable pairs** (b/d, p/q, a/e).
4. **Open counters** (the enclosed white space in `o`, `e`, `a`, `d`).
5. **Consistent letter heights** / taller ascenders.

**On their face**, several of these claims are sensible. Inter-letter spacing and letter distinctness are independently supported in the literature (§4). The weighted-bottom claim rests on the visual-dyslexia model that mainstream cognitive neuroscience does not strongly endorse.

---

## Part 3 — The evidence review

Here the picture turns. The headline empirical studies:

### Kuster, van Weerdenburg, Gompel & Bosman (2018)

**"Dyslexie font does not benefit reading in children with or without dyslexia."** *Annals of Dyslexia*, 68(1), 25–42.

A controlled study comparing Dyslexie with Arial on reading rate and accuracy in Dutch children. **N = 170** (including dyslexic and non-dyslexic children). Tasks: word reading, text reading, error analysis.

**Finding:** No statistically significant advantage of Dyslexie over Arial on any measure. Effects that *did* appear trace to the **font's generous default letter spacing**, not to the letter-shape design — an effect that Arial replicates if set with equivalent spacing.

This is **the most-cited rebuttal** of the weighted-bottom dyslexia-font theory. Its significance: it was a well-powered, peer-reviewed study conducted on the native language (Dutch) of the font's designer, using dyslexic children, with Arial as a reasonable control. The null result is hard to dismiss as a methodological quirk.

### Wery & Diliberto (2017)

**"The effect of a specialized dyslexia font, OpenDyslexic, on reading rate and accuracy."** *Annals of Dyslexia*, 67(2), 114–127.

A controlled study (**N = 48** children aged 7–11, with and without dyslexia) comparing OpenDyslexic with Arial and Times New Roman on reading rate and accuracy.

**Finding:** No significant advantage of OpenDyslexic over either control font. Reading accuracy was comparable; reading rate showed minor trends without statistical significance. Subjective preference was mixed.

### Rello & Baeza-Yates (2013, 2017)

**Rello, L. & Baeza-Yates, R. (2013). "Good fonts for dyslexia."** *Proceedings of ASSETS '13*, 14:1–14:8. https://doi.org/10.1145/2513383.2513447

Eye-tracking study (**N = 48** Spanish adults with dyslexia) comparing **Arial, Times New Roman, Verdana, Courier, Helvetica, Computer Modern Unicode, Myriad, Garamond, Arial Italic, Courier Italic, OpenDyslexic, OpenDyslexic Italic**. Measures: reading time, fixation duration, subjective comfort.

**Findings:**
- **Sans-serif > serif** in reading speed, small effect.
- **Verdana and Courier** emerged as the best performers on reading time.
- **Italic fonts slower** for everyone — especially OpenDyslexic Italic.
- **OpenDyslexic did not lead on any measure.**

**Rello & Baeza-Yates, "How to present more readable text for people with dyslexia" (2017).** *Universal Access in the Information Society*, 16(1), 29–49.

A broader synthesis from the same research-survey programme. Recommendations:
- Use **sans-serif** fonts (Arial, Verdana, Helvetica, Computer Modern Unicode), or **monospaced** (Courier).
- **14pt+** font size.
- **1.4–1.5** line spacing.
- **Increased letter spacing** (~7–14% of font size).
- **Left-aligned, not justified.**

Notable: they **do not recommend OpenDyslexic or Dyslexie**. Their evidence supports spacing and choice of a clear sans-serif, with **Verdana** as a well-supported default.

### Other studies, briefly

- **Marinus et al. (2016).** Dutch child study on Dyslexie — modest positive effect on reading fluency when Dyslexie was used; not replicated in later work.
- **Pijpker (2013).** Dyslexie thesis study — positive effects reported, but the study used the designer's own recruitment and was not independent.
- **Duranovic, Senka & Babic-Gavric (2018).** On Bosnian dyslexic children — mixed effects; the intervention that worked was increased letter spacing, not Dyslexie itself.
- **De Leeuw (2010).** Early Dyslexie research-survey — positive effects; not replicated by independent groups.

**Aggregate pattern.** Positive effects for dyslexia-specific fonts cluster in early, often not-independent studies. The better-controlled, independent, peer-reviewed replications (Kuster, Wery & Diliberto, Rello) find null or weak effects. The effects that *do* appear usually trace to **letter spacing**, which is a design attribute, not a letter-shape attribute — and is replicable in any font.

### British Dyslexia Association guidance

The **British Dyslexia Association Style Guide** (latest revision 2023, 2024 updates online) gives practitioner guidance grounded in consultation with dyslexic adults and the research-survey literature:

- **Use sans-serif fonts** — Arial, Verdana, Tahoma, Century Gothic, Trebuchet, Calibri, Open Sans. **Avoid italic.**
- **Font size 12–14pt minimum**, larger is better.
- **Line spacing 1.5** in long-form reading.
- **Left-aligned**, never justified.
- **Short line lengths** — they recommend 60–70 CPL.
- **Avoid underlining** for emphasis (conflicts with link convention; use bold instead).
- **Use background other than pure white** — cream, soft yellow, pale pastels — **when feasible and user-preferred**.
- **Use dark text on light background** (not the reverse).

**The BDA does not endorse dyslexia-specific fonts.** Their guidance mentions OpenDyslexic and Dyslexie but stops short of recommending them, noting that the evidence is mixed and that user preference matters. Their positive recommendations are about **spacing, measure, size, weight, and clear sans-serif choice** — exactly the interventions that have stronger evidence.

### International Dyslexia Association

Similar posture. The IDA's **fact sheet on fonts and readability** (2019, reaffirmed 2023) notes:

> "While some fonts have been specifically designed for dyslexic readers, research-survey has not consistently shown them to be more effective than other fonts. Good practices for text readability — spacing, size, contrast, and consistent letter shapes — benefit dyslexic readers regardless of specific font choice."

### Honest conclusion

The dyslexia-specific fonts are **not demonstrably better than a well-set Arial or Verdana** for reading performance in dyslexic readers. Their central visual-dyslexia premise (letter rotation) is not the primary mechanism of dyslexic reading errors. The measurable gains trace to generous letter spacing — which any font can have.

User-preference data is mixed: some dyslexic readers prefer OpenDyslexic and report subjective comfort. This is real and matters — see §6.

**What you can honestly say to a client:**
- "These fonts are offered and widely used; they don't harm reading."
- "Controlled research-survey does not show them outperforming plain sans-serif fonts like Arial or Verdana."
- "If your users prefer them, offering them as an option is a legitimate courtesy."
- "The bigger legibility wins are in spacing, size, contrast, and measure — not in the font identity."

**What you can't honestly say:**
- "OpenDyslexic has been shown to help dyslexic readers." (The evidence is mixed at best; recent independent studies show null.)
- "Dyslexie improves reading for 80% of users." (Such claims trace to company-commissioned or designer-involved research-survey; not replicated.)
- "Use Dyslexie by default for accessibility." (Contradicts BDA and IDA posture.)

---

## Part 4 — What does help (stronger evidence base)

These interventions have better-supported evidence for improving reading performance in dyslexic readers.

### Increased letter spacing

**Zorzi, Barbiero, Facoetti, Lonciari, Carrozzi, Montico, Bravar, George, Pech-Georgel & Ziegler (2012).** "Extra-large letter spacing improves reading in dyslexia." *Proceedings of the National Academy of Sciences*, 109(28), 11455–11459.

**N = 94** Italian and French dyslexic children. Tested text with increased letter spacing (+2.5% to +4% of font size) vs normal.

**Finding:** A robust 20% increase in reading speed and a 50% reduction in errors in dyslexic children — *specifically* — with no cost to non-dyslexic controls. A strongly positive, high-profile, well-powered result.

**Perea, Panadero, Moret-Tatay & Gómez (2012).** "The effects of inter-letter spacing in visual-word recognition: Evidence with young normal readers and developmental dyslexics." *Learning and Instruction*, 22(6), 420–430.

Spanish children, **N = 48** dyslexic + **N = 48** typically-developing matched. Same pattern: increased letter spacing helped dyslexic readers' word recognition.

**Replication pattern.** Extra letter spacing reliably helps dyslexic readers in alphabetic scripts. The effect is of moderate size — not a cure — but it is real.

**Operational values.** The studies tested **+2.5% to +7%** of font size in extra tracking. In CSS:

```css
.long-form {
  letter-spacing: 0.05em;  /* ~5% — middle of studied range */
}

/* For dyslexia-preference surface */
body.dyslexia-pref {
  letter-spacing: 0.07em;
  line-height: 1.75;
}
```

### Increased line spacing

Less specifically studied for dyslexia than letter spacing, but robustly supported in general low-vision and reading-comfort research-survey. **Line-height 1.5 or greater** for extended prose is the BDA recommendation and the WCAG 1.4.8 AAA target.

### Shorter measure (characters per line)

**45–60 CPL** for comfortable reading; **60–80 CPL** acceptable. Above 80 CPL, eye-return errors increase (the "doubling" problem), and this pattern is amplified in dyslexic readers.

CSS: `max-width: 60ch` is a good dyslexia-friendly default; `65ch` is the general-readership sweet spot.

### Clear sans-serif with differentiated letters

Letter pairs that look similar are a known problem — especially:
- `b` and `d`
- `p` and `q`
- `a` and `e` (in some fonts)
- `I` (capital i), `l` (lowercase L), and `1`
- `O` and `0`

**Good defaults (differentiated forms):**
- **Verdana** (Rello/Baeza-Yates recommendation)
- **Arial**, **Helvetica** (generally OK; I/l/1 can be indistinguishable in some cuts — Helvetica Now improves this)
- **Open Sans** — Google Fonts; open source
- **Atkinson Hyperlegible** — Braille Institute, 2020; explicitly designed for low-vision; well-differentiated letter forms; freely licensed
- **Lexend** — see §5
- **Comic Sans** — much derided, but the character differentiation is good; some dyslexic readers genuinely prefer it. Don't ship it as default, but don't mock users who pick it.

**Fonts to watch out for:**
- **Ultra-geometric sans-serifs** (Avenir, Century Gothic) — can have nearly identical `o`, `c`, `e` shapes.
- **Some monolinear fonts** with near-identical `b`/`d`/`p`/`q` curvature.
- **Italic at small sizes** — OpenDyslexic's own italic performed *worse* in Rello & Baeza-Yates.

### Larger body size

**14pt+** for body text (the BDA default; ≈18.66 CSS px at standard 96 DPI). WCAG's `16px` recommendation is the floor; 18px is a friendlier default for dyslexic and older readers.

### Reading rulers and selective highlighting

Non-typographic but evidence-supported:
- **Physical or digital reading rulers** (a colored strip that isolates one or two lines) — some support for reducing line-tracking errors.
- **Reader-view modes** that offer serial presentation or focus highlighting — anecdotal positive reports, less formal evidence.
- **Bionic Reading** (launched 2022) — bolds the first syllables of each word. Viral popularity; **no peer-reviewed evidence of benefit**. Rello-like studies on this remain to be done.

### Coloured overlays / backgrounds — contested

**Irlen syndrome / Meares-Irlen visual stress** is the claimed condition: reading discomfort with pure-white backgrounds and high-contrast black text, relieved by coloured filters.

**Evidence status:** deeply contested. Wilkins and colleagues (UK, 2000s–2010s) published positive results showing subjective benefit. Independent replications have been mixed. The UK NHS and the American Academy of Pediatrics have at various points questioned whether Irlen syndrome is a distinct clinical entity or whether the coloured-overlay effect is a placebo and/or a low-vision intervention mislabeled.

**Practitioner takeaway:**
- **Don't sell coloured overlays as dyslexia treatment.** The claim is contested.
- **Offering non-pure-white backgrounds** (e.g., a subtle cream or pale blue) is a low-cost courtesy with mild positive evidence. BDA endorses this.
- **Let users choose.** A "reading preferences" panel with a handful of background options is more defensible than one fixed non-white background.

---

## Part 5 — Font choices that are well-defended

Here is a practitioner-defensible shortlist, ordered by evidence strength.

### Verdana

**Status.** Recommended by Rello & Baeza-Yates's eye-tracking studies. Widely available; system font on Windows and macOS. Good letter differentiation. Generous inherent spacing.

**License.** Microsoft core font; freely distributed as system/web-safe. For custom web use, self-hosting is straightforward.

**Use as.** Default body text on reading-heavy surfaces where a practitioner-safe dyslexia choice is desired.

### Arial, Helvetica, Tahoma

**Status.** BDA-listed safe defaults. Arial in particular is the control font against which most dyslexia-font studies are compared — and it holds up.

**Caveat.** Arial and Helvetica can have indistinguishable `I`/`l`/`1`. Verify with your content (especially for typography involving serial numbers, addresses, code). Helvetica Now and Helvetica Neue's more recent cuts improve this somewhat.

### Atkinson Hyperlegible (Braille Institute, 2020)

**Status.** A relatively new typeface (2019–2020) designed specifically to improve character recognition for low-vision readers. Strongly differentiated letter shapes: each letter is distinct in both form and counter. Well-regarded in the accessibility community.

**License.** Free (SIL OFL).

**Use as.** Good choice for accessibility-focused products. Less well-tested on dyslexic readers specifically than Verdana, but its design intent and letter-form differentiation match dyslexia-friendly principles.

### Lexend (Thomas Jockin & Bonnie Shaver-Troup, 2018–2020)

**Status.** Variable-font family explicitly designed around the **Shaver-Troup formulation** — a hypothesis that reading proficiency improves when letter spacing is individually tuned (the variable axis widens letters progressively). Bonnie Shaver-Troup, an educational therapist, led the conceptual design; Thomas Jockin drew the type. The project has some early positive-effect data from Shaver-Troup's own practice; **independent peer-reviewed validation is still thin** as of 2026.

**License.** Free (SIL OFL). Google Fonts.

**The variable axis.** Lexend has a `wght` axis and, more distinctively, the **`LEXD`** axis (Expansion) — which widens letters and letter-spacing together. Users (or designers) can tune the axis per individual preference. The idea is legitimate — individual tuning may matter more than any single font choice — but the empirical base is currently weaker than for plain Verdana.

**Use as.** A reasonable offering for a "reading preferences" panel where the user can tune the Expansion axis. Not dishonest to include; don't oversell the empirical support.

### Open Sans

**Status.** Humanist sans-serif, open source, widely available, generally well-differentiated letters. Safe default.

**License.** Free (SIL OFL). Google Fonts.

### OpenDyslexic — offer as preference, not default

**Status.** Despite the weak/null empirical support in controlled studies, **some dyslexic users report subjective preference and comfort with OpenDyslexic.** Preference matters for sustained reading — a font the reader *likes* may be read for longer even if line-level speed doesn't differ.

**Use as.** A "dyslexia font" option in a reading-preferences panel. Label honestly ("Some dyslexic readers prefer this font"). Don't ship as default. Don't claim performance benefit in marketing.

### Fonts to avoid

- **Thin weights** (100–300) at small sizes — poor contrast, character blurring.
- **Geometric sans-serifs** with near-identical `o`, `c`, `e` — Avenir, Century Gothic at small sizes.
- **Italic for body** — slows all readers; worse for dyslexic readers (Rello & Baeza-Yates).
- **Decorative / display fonts** for body text — obviously. Hand-lettered, brush, slab-dense all cause problems.
- **Any font with ambiguous mirror pairs** — test `b`/`d`/`p`/`q` yourself before committing.

---

## Part 6 — Practitioner takeaways

### Defaults

1. **Body font**: a clear sans-serif at 16–18px with 1.5 line-height and 60–65 CPL measure.
2. **Dyslexic-friendly default picks**: Verdana, Atkinson Hyperlegible, Open Sans, or a well-vetted Helvetica/Arial cut.
3. **Line spacing**: `line-height: 1.5` (unitless) minimum.
4. **Letter spacing**: consider `letter-spacing: 0.025em` (subtle) for long-form prose; up to `0.05em` in dyslexia-preference mode.
5. **Measure**: `max-width: 65ch` for prose; `60ch` for dyslexia-preference mode.
6. **Alignment**: `text-align: start` (left in LTR); never `justify` on prose.
7. **Contrast**: WCAG 2.2 AA minimum (see [wcag-type.md §SC 1.4.3](./wcag-type.md#sc-143-contrast-minimum--level-aa)); consider AAA for reading-heavy surfaces.

### Offering dyslexia-specific fonts

**Do:**
- Expose them in a **reading preferences** panel.
- Include OpenDyslexic (free) at minimum. Lexend's Expansion axis is a thoughtful addition.
- Let users tune spacing, size, and background colour as independent controls — spacing and measure will help more than any font switch.
- Label honestly. "Some dyslexic readers prefer this." Not "scientifically proven to help."

**Don't:**
- Ship OpenDyslexic or Dyslexie as the default reading font for everyone.
- Market dyslexia-fonts as "proven" or "accessible by default." The evidence doesn't support that claim.
- Replace other accessibility work (contrast, spacing, size) with a dyslexia-font switch.

### Investing design budget

In roughly descending order of evidence-weight-per-dollar, spend on:

1. **Contrast and color** — WCAG 2.2 SC 1.4.3 / 1.4.6; APCA-secondary check. Foundational.
2. **Spacing (line and letter)** — best-supported dyslexia intervention.
3. **Measure and size** — 60–65 CPL, 16–18px body.
4. **Font choice** — Verdana, Atkinson Hyperlegible, a clean sans-serif. Lower marginal return than spacing once font is "clean enough."
5. **User-adjustable preferences panel** — lets the user own the final settings. Highest honest return.
6. **Offering dyslexia-specific fonts as an option** — cheap to add; don't oversell.

### What beats any single font

**User-adjustable type controls** beat every single font choice, including the dyslexia-specific ones. A reading-preferences panel exposing:
- Font family (from a curated shortlist)
- Size (14–24px range)
- Line spacing (1.3–2.0 range)
- Letter spacing (0 to +0.1em)
- Background color (white, cream, pale yellow, pale blue, high-contrast)
- Measure (45–85 CPL)

…gives each user the configuration that works for them. This is also aligned with **WCAG 1.4.8 AAA** ("a mechanism is available") and the **WCAG 3.0 Customizable Text** direction (see [wcag-type.md Part 2](./wcag-type.md#part-2--wcag-30-directions-as-of-2026-04)).

### Don't extrapolate across scripts

Dyslexia research-survey in English, Dutch, Italian, and Spanish does **not** transfer to CJK, Arabic, Devanagari, Thai, Hebrew. If you are building for those scripts, start from the research-survey in those scripts (which is thinner), consult native experts, and do not assume an OpenDyslexic-equivalent intervention exists or is needed.

### Don't weaponise dyslexia for design decisions

A common anti-pattern: designers or PMs invoke "but dyslexic users!" to justify predetermined choices (comic sans-seeking, accommodation-theater, etc). The honest play is to:
- Know the evidence base.
- Offer real controls.
- Measure actual usage (which preferences users select) and refine.

---

## Anti-patterns

- **Shipping OpenDyslexic as the default body font** for a whole site. The evidence does not support it; other readers may find it uncomfortable.
- **Claiming "dyslexia-friendly" because you shipped Dyslexie.** Not a defensible claim.
- **Using a dyslexia-font switch as a substitute** for fixing contrast, size, measure, and spacing.
- **Italic body text.** Slower for everyone, worse for dyslexic readers.
- **Justified prose without hyphenation engine.** Rivers and uneven spacing damage reading; dyslexic readers bear a larger cost.
- **Color-only treatments** (pale yellow filter, pastel background) marketed as dyslexia interventions without allowing the user to turn them off.
- **Bionic Reading as default.** Viral but not evidenced.
- **Coloured-overlay / Irlen claims** pitched as established science. The literature is contested.
- **Using English-language dyslexia research-survey** to justify design choices for CJK, Arabic, or Devanagari readers.
- **"1 in 5" citation inflation.** Conservative prevalence is roughly 10%; the 20% figure trades on the broadest definition of "reading difficulty."
- **Assuming all dyslexic readers need the same thing.** Spectrum of preferences; individual variation dominates.
- **Hiding the dyslexia-preferences panel behind deep settings.** If you offer it, surface it where readers can find it.
- **Not offering a way out of dyslexia-preferences.** Users should be able to revert.
- **Removing the user's ability to resize text** in the name of dyslexia — some sites apply fixed heights that break under WCAG 1.4.4 / 1.4.12 overrides. See [wcag-type.md SC 1.4.4](./wcag-type.md#sc-144-resize-text--level-aa) and [SC 1.4.12](./wcag-type.md#sc-1412-text-spacing--level-aa).

---

## Sources

### Primary studies (peer-reviewed)

- **Kuster, S. M., van Weerdenburg, M., Gompel, M., & Bosman, A. M. T. (2018).** "Dyslexie font does not benefit reading in children with or without dyslexia." *Annals of Dyslexia*, 68(1), 25–42. https://link.springer.com/article/10.1007/s11881-018-0154-1
- **Wery, J. J., & Diliberto, J. A. (2017).** "The effect of a specialized dyslexia font, OpenDyslexic, on reading rate and accuracy." *Annals of Dyslexia*, 67(2), 114–127.
- **Rello, L., & Baeza-Yates, R. (2013).** "Good fonts for dyslexia." *Proceedings of the 15th International ACM SIGACCESS Conference on Computers and Accessibility* (ASSETS '13). https://dl.acm.org/doi/10.1145/2513383.2513447
- **Rello, L., & Baeza-Yates, R. (2017).** "How to present more readable text for people with dyslexia." *Universal Access in the Information Society*, 16(1), 29–49.
- **Zorzi, M., Barbiero, C., Facoetti, A., Lonciari, I., Carrozzi, M., Montico, M., Bravar, L., George, F., Pech-Georgel, C., & Ziegler, J. C. (2012).** "Extra-large letter spacing improves reading in dyslexia." *PNAS*, 109(28), 11455–11459. https://www.pnas.org/doi/10.1073/pnas.1205566109
- **Perea, M., Panadero, V., Moret-Tatay, C., & Gómez, P. (2012).** "The effects of inter-letter spacing in visual-word recognition: Evidence with young normal readers and developmental dyslexics." *Learning and Instruction*, 22(6), 420–430.
- **Marinus, E., Mostard, M., Segers, E., Schubert, T. M., Madelaine, A., & Wheldall, K. (2016).** "A special font for people with dyslexia: Does it work and, if so, why?" *Dyslexia*, 22(3), 233–244.
- **Duranovic, M., Senka, S., & Babic-Gavric, B. (2018).** "Influence of increased letter spacing and font type on the reading ability of dyslexic children." *Annals of Dyslexia*, 68(2), 218–228.
- **Lyon, G. R., Shaywitz, S. E., & Shaywitz, B. A. (2003).** "A definition of dyslexia." *Annals of Dyslexia*, 53, 1–14. The IDA operational definition.
- **Shaywitz, S. E. (1998).** "Dyslexia." *New England Journal of Medicine*, 338, 307–312.

### Guidelines and advocacy

- **British Dyslexia Association.** "Dyslexia Style Guide" (2023, online updates 2024). https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide
- **International Dyslexia Association.** "Definition of Dyslexia" (2002, reaffirmed). https://dyslexiaida.org/definition-of-dyslexia/
- **International Dyslexia Association.** "Fact Sheet on Fonts and Readability" (2019, reaffirmed 2023).
- **Bureau of Internet Accessibility / Deque / Level Access** — practitioner summaries of the font evidence.

### Fonts

- **OpenDyslexic** (Abelardo González, 2011–). https://opendyslexic.org/
- **Dyslexie** (Christian Boer, 2008). https://www.dyslexiefont.com/
- **Lexie Readable / K-Type** (Keith Bates). https://www.k-type.com/
- **Lexend Project** (Thomas Jockin & Bonnie Shaver-Troup, 2018–). https://lexend.com/
- **Atkinson Hyperlegible** (Braille Institute, 2020). https://www.brailleinstitute.org/freefont
- **Verdana** (Matthew Carter, Microsoft, 1996). System font.

### Contested areas (Irlen / Bionic Reading)

- **Wilkins, A. J.** — body of work on visual stress and coloured overlays.
- **UK National Health Service / American Academy of Pediatrics** — skeptical position statements on Irlen syndrome.
- **Bionic Reading** — https://bionic-reading.com/ — note the absence of peer-reviewed efficacy studies.

### Peer files

- **[wcag-type.md](./wcag-type.md)** — WCAG 2.2 text-related success criteria and WCAG 3.0 directions. For the baseline floor (contrast, resize, reflow, text spacing) that applies to all readers.
