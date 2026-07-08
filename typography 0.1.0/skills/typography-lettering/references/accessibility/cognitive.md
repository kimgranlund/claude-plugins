---
date: 2026-04-18
coverage: light
peers:
  - ./dyslexia.md
  - ./low-vision.md
  - ./wcag-type.md
  - ../techniques/measure.md
  - ../science/legibility-vs-readability.md
primary_sources:
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html
  - https://www.w3.org/WAI/cognitive/
  - https://www.w3.org/TR/coga-usable/
  - https://www.gov.uk/guidance/style-guide/a-to-z-of-gov-uk-style
  - https://www.gov.uk/guidance/content-design/writing-for-gov-uk
  - https://webaim.org/articles/cognitive/
  - https://link.springer.com/article/10.1007/s11881-018-0154-1  # Kuster et al. 2018
  - https://www.plainlanguage.gov/
---

# Cognitive accessibility — typography reference

**Peers:** [dyslexia evidence](./dyslexia.md) covers the specific population where the font-level research-survey is thickest; [low-vision typography](./low-vision.md) shares the measure, spacing, and size recommendations from a different clinical angle; [WCAG 2.2 type success criteria](./wcag-type.md) grounds the legal floor. [`../techniques/measure.md`](../techniques/measure.md) explains why 45–60 CPL is the specific band cognitively-loaded readers benefit from. [`../science/legibility-vs-readability.md`](../science/legibility-vs-readability.md) distinguishes letter-level legibility (rarely the bottleneck for this population) from sustained readability (where the gains are).

"Cognitive accessibility" covers populations for whom reading is cognitively costly in ways unrelated to retinal acuity or colour perception: dyslexia, ADHD, autism spectrum, intellectual disability, traumatic brain injury, age-related cognitive decline, non-native-language readers, low-literacy readers. The populations differ; the typographic levers that help them overlap considerably. This file is light coverage — it maps the territory and points to the peer files where the evidence is thicker. Specifically, it does **not** re-derive the dyslexia-font evidence (see [`./dyslexia.md`](./dyslexia.md)) or the WCAG SC mechanics (see [`./wcag-type.md`](./wcag-type.md)).

---

## Part 1 — Scope

### Populations covered

The following have documented typographic-adjacent needs, with varying research-survey density:

- **Dyslexia** — strongest research-survey base; see [`./dyslexia.md`](./dyslexia.md).
- **ADHD** — sustained-attention and working-memory deficits; overlaps with dyslexia on ~25–40% of diagnoses.
- **Autism spectrum** — sensory sensitivity; literal reading; strong preferences for consistency.
- **Intellectual disability** — broad category; typography is a supporting role to plain-language content.
- **Traumatic brain injury (TBI) and post-concussion syndrome** — often includes photophobia (overlap with [`./low-vision.md`](./low-vision.md)), reduced working memory, reading fatigue.
- **Age-related cognitive decline and dementia** — overlaps with low-vision, adds memory and hierarchy needs.
- **Non-native (L2) readers** — reading rate in a second language is meaningfully slower; letterform familiarity matters more.
- **Low-literacy adults** — ~16% of US adults read at or below a 5th-grade level per the Program for the International Assessment of Adult Competencies (PIAAC, 2017, reaffirmed 2023).
- **Situational cognitive load** — sleep deprivation, stress, multi-tasking, hostile environments. Temporary but universally experienced.

### What this file is not

- Not a dyslexia reference — see [`./dyslexia.md`](./dyslexia.md).
- Not a low-vision reference — see [`./low-vision.md`](./low-vision.md).
- Not a plain-language content guide. Plain language (Hemingway, GOV.UK style guide, Plain Writing Act) operates at the *content* layer; this file covers the typographic layer that supports plain content.
- Not a legal compliance reference. WCAG 2.2 contains no SC that prescribes specific typography for cognitive accessibility. See §9.

---

## Part 2 — Cognitive load from typography

Typography can actively consume cognitive resources a reader could otherwise spend on comprehension. The mechanism is not mysterious: decorative, unfamiliar, or rhythmically irregular text demands more working-memory cycles to decode.

### Load-adding patterns

- **Decorative, script, and high-contrast display fonts.** Each letter takes longer to recognise. Acceptable for display and branding; corrosive for body.
- **All-caps body runs.** ~13–20% reading-rate cost (Tinker 1963; Paap, Newsome & Noel 1984; Arditi & Cho 2007). See [`../science/crowding.md`](../science/crowding.md) for the crowding-based explanation.
- **Small caps for body.** Real small-caps (OpenType `smcp`) are less costly than faux `text-transform: uppercase; font-size: 0.8em` but still worse than mixed case for sustained reading.
- **Italic for long passages.** Slower for all readers (Rello & Baeza-Yates 2013); worse for dyslexic readers. Italic belongs on occasional words, not paragraphs.
- **Mixed-case emphasis.** "THIS is IMPORTANT" breaks reading rhythm.
- **Stacked emphasis.** Bold + italic + colour stacked on one span signals "something is wrong with the writer." One mode of emphasis at a time.
- **Justified prose without hyphenation.** Rivers of whitespace and uneven word-spacing disrupt rhythm and increase regressions. Standard web browsers' `text-align: justify` without `hyphens: auto` and a real H&J engine produces exactly this.
- **Centred prose.** Irregular line-starts force the eye to re-find the left margin every line. Acceptable for short headlines; harmful for body.
- **Unfamiliar fonts.** Familiarity gain is real (Martelli, Majaj & Pelli 2005); readers recognise letters faster in familiar faces. Switching the body font every section costs comprehension.

### Load-reducing patterns

- **Predictable rhythm.** Consistent line-height, paragraph spacing, heading hierarchy.
- **Clear hierarchy.** Readers can skim before reading; the skim scaffolds the read.
- **Short paragraphs.** Working memory holds a paragraph-sized chunk; walls of text exceed it.
- **Whitespace.** Page margins, paragraph breaks, list spacing are cognitive rest.
- **Consistent typography within a document.** One body font; one or two heading faces; a small set of weights.

---

## Part 3 — Readability vs legibility for cognitive populations

See [`../science/legibility-vs-readability.md`](../science/legibility-vs-readability.md) for the full distinction.

For most cognitive-accessibility work, **readability** (sustained reading comfort, comprehension, re-reading rate) is the variable that moves — not legibility (individual letter identification). Cognitive-accessibility readers can usually identify letters; the cost is in integrating words into sentences into meaning.

Typographic implications:
- **Letter-form distinctness** (the legibility lever) matters mostly for dyslexic readers at the letter-recognition stage and for L2 readers unfamiliar with Latin-letter variants (see [`./dyslexia.md §5`](./dyslexia.md#part-5--font-choices-that-are-well-defended)).
- **Rhythm, measure, spacing, hierarchy** (the readability levers) matter for all cognitive-accessibility populations.

A well-set Verdana reads better than a poorly-set Atkinson Hyperlegible. Font choice is less important than spacing and layout once the font is "clean enough."

---

## Part 4 — Evidence-based recommendations

Most recommendations here come from dyslexia research-survey (stronger evidence base) and generalise to cognitive-accessibility populations by analogy. Where generalisation is contested, it is flagged.

### Font choice

- **Sans-serif for body.** Rello & Baeza-Yates (2013, 2017) for dyslexic adults; generalises across cognitive-load populations by preference data. The effect is small on comprehension; strong on subjective preference. Practitioner: default to sans-serif unless a specific editorial reason demands serif.
- **High x-height** aids letter recognition at small sizes. Good defaults: Verdana, Atkinson Hyperlegible, Open Sans, Inter, Source Sans 3, Lexend. See [`./dyslexia.md §5`](./dyslexia.md#part-5--font-choices-that-are-well-defended).
- **Avoid decorative, script, and high-contrast fonts for body.** Use them for display only.
- **Avoid thin weights** for body text. Regular (400) minimum; Medium (500) better.

### Line height

- **1.5–1.8** for body. WCAG 1.4.8 AAA minimum is 1.5. BDA recommends 1.5 for dyslexic audiences. Higher (1.7–1.8) helps reduce tracking load for ADHD and TBI readers.

### Measure

- **45–60 CPL** for cognitive-load-sensitive surfaces. Shorter than general typography's 60–75 sweet spot because line-tracking load falls disproportionately on this population.
- **Never exceed 75–80 CPL** for prose. WCAG 1.4.8 AAA ceiling is 80.
- See [`../techniques/measure.md`](../techniques/measure.md).

### Size

- **16 CSS px minimum**; **18 CSS px preferred** for cognitive-accessibility surfaces. Larger sizes reduce the cognitive cost of letter identification by bringing more diagnostic features into the foveal resolution range. Overlaps heavily with [`./low-vision.md`](./low-vision.md).

### Paragraph spacing

- **≥2× font-size** per WCAG 1.4.12 override tolerance; ≥2.25× font-size for AAA 1.4.8 equivalence.
- Generous paragraph breaks give working memory a rest point and provide navigation anchors for skimming.

### Alignment

- **Left-aligned, ragged right** for LTR scripts (`text-align: start`). Right-aligned for RTL.
- **Never justify** body prose without a real hyphenation engine. Even with one, justified prose is flagged as harmful by the British Dyslexia Association and supported as a WCAG 1.4.8 AAA recommendation.
- **Never centre** body prose. Centred headlines (short, 1–2 lines) are fine.

### Emphasis

- **Bold for emphasis.** Single mode; avoid italic on long runs.
- **Avoid underline for emphasis.** Conflicts with link affordance.
- **Avoid colour-only emphasis** — fails SC 1.4.1.
- **Avoid stacked emphasis** (bold + italic + colour). Signals "I don't know how to emphasise this."

### Consistency

- **One body font** throughout a document.
- **One to two heading fonts**, consistent across the document.
- **Predictable heading hierarchy** — `h1` → `h2` → `h3` without skipping levels.
- **Consistent spacing.** Paragraph spacing, list spacing, heading margins should be formulaic.

---

## Part 5 — Plain language intersections

Typography supports plain language; it does not substitute for it.

- **Plain Writing Act (US, 2010)** requires US federal agencies to use plain language in public-facing communication. https://www.plainlanguage.gov/
- **GOV.UK Service Manual** is the canonical practitioner resource for plain-language content design. The style guide emphasises short sentences, common words, active voice, meaningful link text. https://www.gov.uk/guidance/style-guide
- **ISO/IEC 23859** (Plain language, published 2023) formalises international principles: reader-centred, clear, organised, verified.
- **Simplified Technical English (STE, ASD-STE100)** — controlled language for technical documentation; a precedent for constrained vocabulary.
- **Common European Framework (CEFR)** reading levels — A1 (beginner) through C2 (proficient). Not a measurement formula but a useful framing for L2 audiences.

### Reading-level tools

- **Flesch Reading Ease / Flesch-Kincaid Grade Level** — English-centric; sentence-length and syllable-count proxies. Target F-K ~8–9 for general-audience content; F-K ~6 for cognitive-accessibility audiences.
- **Hemingway Editor** — flags long sentences, passive voice, adverbs. Live grade-level scoring. Useful as a drift-detection tool, not a target.
- **Dale-Chall** — uses a familiar-word list; better for catching jargon.
- **LIX** (Scandinavian), **Wiener Sachtextformel** (German), **Fernández Huerta** (Spanish) — localised equivalents where F-K doesn't apply.

See [`./wcag-type.md §SC 3.1.5`](./wcag-type.md#sc-315-reading-level--level-aaa) for the WCAG reading-level criterion.

### What typography adds

Plain content rendered in small, tight, justified type in a cluttered layout is not cognitively accessible. Typography's job is to ensure that once you've done the content-level work, it reads at the ease level the content implies.

Specifically:
- **Short sentences** need short lines. 45–55 CPL renders short sentences as nearly-one-line units.
- **Simple vocabulary** deserves readable size and contrast so readers don't have to work to decode letters on top of decoding meaning.
- **Clear hierarchy** maps to typographic hierarchy (h1 / h2 / h3 with distinct size and weight).

Dyslexia-friendly fonts (OpenDyslexic, Dyslexie) do not substitute for plain content. A complex sentence in OpenDyslexic is still a complex sentence.

---

## Part 6 — Autism spectrum considerations

Research specifically on typography for autistic readers is thinner than for dyslexia. The following are consensus practitioner recommendations grounded in reported preferences and sensory-sensitivity research-survey:

- **Predictable rhythm and layout.** Inconsistent typography increases cognitive load; autistic readers often report strong preferences for unchanging patterns within and across pages.
- **Avoid sensory-overwhelming contrast borders.** Heavy borders, large decorative elements, and strobing animations can trigger sensory overload. Respect `prefers-reduced-motion`.
- **Literal language.** Autistic readers (particularly at the literal end of the spectrum) benefit from typography that doesn't signal irony or figurative intent (avoid heavy ironic quotation marks, sarcastic italics).
- **Clear hierarchy.** Heading levels map to content hierarchy reliably; typography should reinforce rather than obscure the structure.
- **Flexible but non-jarring.** Avoid sudden typographic changes (different font per section) within a document.

For literal-information contexts (medical, legal, administrative) where autistic readers and other literal-reading populations are disproportionately affected, prioritise clear hierarchy and restrained typographic vocabulary over editorial flair.

---

## Part 7 — ADHD considerations

ADHD affects ~5–8% of children and ~2.5–4% of adults globally (APA, DSM-5-TR 2022). The reading-relevant deficits are sustained attention, working memory, and task-maintenance.

Typographic accommodations:
- **Short paragraphs** — ideally 2–5 sentences. Walls of text exceed working-memory budget.
- **Clear headings every few paragraphs** — serve as attention anchors.
- **Bulleted lists** for enumerations. List items are independently attentionable in a way that comma-separated clauses are not.
- **Generous whitespace** — page margins, paragraph spacing, list spacing. Dense layouts are exhausting.
- **`text-wrap: pretty`** (Chromium 117+ shipped 2023, Safari 17.4+ shipped 2024, Firefox 152+ unshipped as of 2026-04). Balances the last few lines of a paragraph to avoid orphans and awkward line-break positions that cause re-reading. Incremental improvement at the readability layer.
- **Avoid auto-playing video or moving text.** Animated backgrounds, kinetic typography, marquees — all drain attention. Respect `prefers-reduced-motion`.
- **Progress indicators** for long documents. Readers benefit from knowing how much remains.

Cognitive-load reduction via typography is a per-paragraph gain; ADHD readers often abandon long-form content regardless of typography. The typography's job is to make abandonment less likely, not to eliminate it.

---

## Part 8 — Ageing and age-related cognitive decline

Overlaps significantly with [`./low-vision.md`](./low-vision.md) — many age-related reading difficulties have both visual and cognitive components. Typographic recommendations converge:

- **Larger body** (18 CSS px minimum, 20 better).
- **Higher line-height** (1.6–1.8).
- **Clearer hierarchy** — heading size differences should be emphatic (headings markedly larger than body).
- **Shorter paragraphs.**
- **Avoid demanding interactive patterns.** Hover-reveal tooltips (particularly if the hover is brief), modal dialogs, time-limited content, and complex multi-step flows all compound working-memory load.
- **Link affordances should be obvious.** Colour alone is insufficient; underlines plus colour is the safe default. See [`./low-vision.md §4`](./low-vision.md#part-4--contrast-polarity-and-colour).
- **Avoid low-contrast body text.** Contrast-sensitivity decline is typical; design to WCAG AAA / APCA Lc 75 for audiences skewing older.

Dementia-specific design (for readers with moderate cognitive decline) adds:
- **Prominent orientation cues** — page title visible; "you are here" breadcrumbs.
- **Simple, consistent navigation.**
- **Avoid unnecessary typographic flourish** — caps, stylised decorations, unusual layouts all impose load.

---

## Part 9 — Non-native and low-literacy readers

### L2 readers

Second-language reading is meaningfully slower than L1 — typically 30–60% slower for proficient L2 readers in controlled studies (Koda 2005; Grabe 2009). The slowdown is primarily at the word-recognition and lexical-access stages; sentence-integration is less affected for proficient L2 readers.

Typographic implications:
- **High x-height fonts aid letter recognition** for readers less fluent with Latin letterforms or with regional letterform variants.
- **Avoid decorative and script fonts** — L2 readers have thinner familiarity margins; stylised letterforms cost more than they cost L1 readers.
- **Avoid italic for emphasis.** L2 readers read italic more slowly than L1 readers; the gap is larger than for roman.
- **Offer font-choice toggle** for multilingual audiences. A reader of Cyrillic/Latin bilingual content may have stronger preferences in their primary script's native foundry.
- **Respect `lang` attributes.** Correct `lang` tells the browser to select the right font-variant tables, hyphenation, and (for screen readers) voice. See [`./wcag-type.md §lang`](./wcag-type.md#lang-attribute-sc-311--screen-reader-correctness--reading-level-tools).

### Low-literacy readers

~16% of US adults read at or below a 5th-grade level (PIAAC 2017, reaffirmed 2023); similar figures apply across OECD countries. Low-literacy readers benefit from:

- **Sans-serif body** — preference data supports sans over serif; comprehension-level effects are weak.
- **Larger size and line-height.**
- **Short sentences and paragraphs** (content lever).
- **Clear hierarchy.**
- **Visual supports** — icons, images, diagrams alongside text. (Typography-adjacent.)

Typography supports content simplification; it does not replace it. If your audience skews low-literacy and the content is at a 10th-grade reading level, the typography fix is to rewrite the content, not to upsize the type.

---

## Part 10 — WCAG 2.2 cognitive-adjacent success criteria

No WCAG 2.2 SC prescribes specific typography values for cognitive accessibility. The closest criteria:

- **SC 3.1.5 Reading Level — AAA.** When text requires reading ability more advanced than lower secondary education, provide a supplemental version. Content-level, not typography.
- **SC 3.1.4 Abbreviations — AAA.** Expansion or definition of abbreviations.
- **SC 3.1.3 Unusual Words — AAA.** Mechanism for identifying the meaning of unusual words or phrases.
- **SC 3.2.1 On Focus — A.** Components don't initiate unexpected change when focused.
- **SC 3.2.2 On Input — A.** Changing input value doesn't initiate unexpected context change.
- **SC 3.2.3 Consistent Navigation — AA.** Navigational mechanisms repeated across pages appear in consistent order.
- **SC 3.2.4 Consistent Identification — AA.** Components with the same functionality are identified consistently.
- **SC 3.3.x Error Identification / Prevention.** Clear, accessible error messages.
- **SC 2.2.x Timing.** User-controllable timing; no surprise timeouts.

The **COGA (Cognitive and Learning Disabilities Accessibility) Task Force** publishes supplementary guidance on W3C.org (*Making Content Usable for People with Cognitive and Learning Disabilities*, latest edition 2024-03 as a W3C Note). Non-normative but useful practitioner reference: https://www.w3.org/TR/coga-usable/

WCAG 3.0 (Working Draft) plans more cognitive-accessibility coverage, but as of 2026-04 it remains non-normative. See [`./wcag-type.md Part 2`](./wcag-type.md#part-2--wcag-30-directions-as-of-2026-04).

---

## Part 11 — What doesn't work (common myths)

### "Dyslexie / OpenDyslexic fixes dyslexia"

Controlled research-survey shows null-to-weak empirical support. See [`./dyslexia.md §3`](./dyslexia.md#part-3--the-evidence-review). Offer as a user preference; do not ship as default; do not market as "proven."

### "Serif fonts are harder to read for dyslexic / cognitively-loaded readers"

No reliable evidence. Rello & Baeza-Yates (2013) found a small preference for sans-serif but the effect was weak and trace-able to familiarity rather than serif-ness itself. **At body sizes on modern displays, the difference between a well-set serif and a well-set sans-serif is negligible for most readers.** The practitioner-safe default is sans-serif because it matches preference data, not because serif is harmful.

### "Comic Sans is the most readable font for cognitive accessibility"

Preference signal, not comprehension signal. Comic Sans's letter differentiation is good (not a joke — `b`/`d`, `p`/`q`, `a`/`e` are all clearly distinct), which is why some dyslexic readers genuinely prefer it. But Comic Sans is not empirically superior to other well-differentiated sans-serifs (Verdana, Atkinson Hyperlegible, Lexie Readable). If you want Comic Sans's legibility profile without the signalling cost, use Lexie Readable or a similar humanist sans-serif.

### "Centred text is friendlier"

Opposite: irregular line-starts increase tracking load. Left-aligned ragged right is the accessible default for LTR content.

### "Justified text looks more professional"

Justified prose without a real hyphenation engine produces rivers of whitespace and irregular word-spacing — harmful for dyslexic readers specifically and for rhythm-sensitive readers generally. The "professional" look is a print-design convention that doesn't transfer to the web's renderer. Default to ragged right.

### "Coloured overlays / tinted backgrounds fix dyslexia"

Contested. Meares-Irlen syndrome (the claimed condition that coloured overlays treat) is not consistently recognised as a distinct clinical entity by the UK NHS or the American Academy of Pediatrics. See [`./dyslexia.md §4`](./dyslexia.md#coloured-overlays--backgrounds--contested). Offer as a user preference; do not market as treatment.

### "Bionic Reading improves comprehension"

Viral 2022 technique that bolds the first syllables of each word. **No peer-reviewed evidence of comprehension benefit.** Preliminary studies (2023–2024) have largely found null effects or small positive effects on very short reading tasks that do not generalise. Offer as a user preference if demand exists; do not market as evidenced.

### "More accessibility means more features"

A preferences panel with 47 toggles is harder to navigate than a well-set default plus 4–5 genuinely useful toggles. Cognitive-accessibility design often means **less**, not more: less visual noise, less chrome, less switching.

---

## Part 12 — Design recommendations summary

A single-surface recipe for a cognitive-accessibility-friendly reading product:

- **Font family** — sans-serif with high x-height; Atkinson Hyperlegible, Verdana, Inter, Open Sans, or Source Sans 3.
- **Body size** — 1.0625rem to 1.125rem (17–18 CSS px at default root).
- **Line-height** — 1.5 to 1.75 unitless.
- **Measure** — `max-width: 60ch` for cognitive-accessibility surfaces; `65ch` for general audiences.
- **Alignment** — `text-align: start` (left in LTR). Never justify. Never centre body.
- **Paragraph spacing** — ≥1em between paragraphs; ≥1.5em for spacious reading.
- **Heading hierarchy** — `h1` > `h2` > `h3` with emphatic size differences (ratio ≥1.25 between adjacent levels).
- **Emphasis** — bold for strong; italic for occasional sparing use. No stacking.
- **Contrast** — AA minimum; AAA or APCA Lc 75 for reading-heavy surfaces.
- **Colour** — never colour-alone for information; always paired with text, icon, or structure.
- **Text-wrap: pretty** where supported; `hyphens: auto` for languages that benefit.
- **Respect user preferences** — `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-motion`, `forced-colors`.
- **Structural robustness** — `rem`-based sizing, `min-height` over `height`, no `overflow: hidden` on text containers, no `!important` on font-size.
- **Offer a reading-preferences panel** — font family (small curated list), size, spacing, background colour. Surfaces user control without building 47 toggles.

---

## Anti-patterns

- **Decorative body fonts.** Script, brush, hand-lettered, high-contrast display faces for running text.
- **All-caps paragraphs.** Cognitive cost without benefit.
- **Italic emphasis on long runs.** Slower for everyone, worse for dyslexia.
- **Stacked emphasis** (bold + italic + colour + size). Signals confusion.
- **Justified prose without a hyphenation engine.** Rivers and uneven spacing.
- **Centred body prose.** Irregular line-starts increase tracking load.
- **Walls of text.** Paragraphs exceeding 5–6 sentences.
- **Walls of bullets.** Bulleted lists exceeding 5–7 items without grouping.
- **Dense layouts with no whitespace.** "Every pixel must be used."
- **Inconsistent typography** across sections or pages of one document.
- **Colour-alone information.** Fails SC 1.4.1.
- **Reading-level tools used as targets.** Rewriting to hit a specific F-K number flattens prose without improving comprehension.
- **Dyslexia-font default.** Evidence does not support it; many readers find it uncomfortable.
- **Coloured-overlay marketing.** Contested evidence base.
- **Bionic Reading as default.** No evidence of benefit.
- **Hover-only tooltips for essential content.** Cognitive-load and input-modality barrier.
- **Time-limited content** without opt-out. Fails WCAG SC 2.2.1.
- **Auto-advancing carousels.** Attention drain; pacing mismatch.
- **Preferences panels with 47 toggles.** Paradox-of-choice failure.

---

## Sources

### Standards and guidelines

- **W3C.** *WCAG 2.2* (2023). https://www.w3.org/TR/WCAG22/
- **W3C.** *Making Content Usable for People with Cognitive and Learning Disabilities* — COGA Task Force Note, 2024. https://www.w3.org/TR/coga-usable/
- **W3C WAI.** Cognitive Accessibility. https://www.w3.org/WAI/cognitive/
- **ISO/IEC 23859** — Plain language (2023).
- **Plain Writing Act of 2010** (USA). https://www.plainlanguage.gov/
- **GOV.UK Service Manual.** https://www.gov.uk/guidance/content-design/writing-for-gov-uk
- **Federal Plain Language Guidelines** (USA, 2011, reaffirmed). **Simplified Technical English** (ASD-STE100).

### Research

- **Kuster et al.** (2018). "Dyslexie font does not benefit reading in children with or without dyslexia." *Annals of Dyslexia* 68(1): 25–42.
- **Rello & Baeza-Yates** (2013, 2017). "Good fonts for dyslexia"; "How to present more readable text for people with dyslexia."
- **Tinker, M. A.** (1963). *Legibility of Print.*
- **Paap, Newsome & Noel** (1984). "Word shape's in poor shape for the race to the lexicon."
- **Martelli, Majaj & Pelli** (2005). "Are faces processed like words?"
- **Koda, K.** (2005). *Insights into Second Language Reading.* **Grabe, W.** (2009). *Reading in a Second Language.*
- **APA.** *DSM-5-TR* (2022).
- See [`./dyslexia.md`](./dyslexia.md) for the full dyslexia bibliography.

### Reading-level tools and statistics

- **DuBay, W. H.** (2004). *The Principles of Readability.*
- **Flesch, R.** (1948). "A new readability yardstick." *J. Applied Psychology* 32(3): 221–233.
- **Hemingway Editor.** https://hemingwayapp.com/ — **Readable.io.** https://readable.com/
- **OECD PIAAC** (2017, reaffirmed 2023). https://www.oecd.org/skills/piaac/
- **WebAIM.** "Cognitive Disabilities." https://webaim.org/articles/cognitive/
- **Autistica** (UK). https://www.autistica.org.uk/

### Peer files

- [`./dyslexia.md`](./dyslexia.md) — dyslexia typography (the strongest evidence base here).
- [`./low-vision.md`](./low-vision.md) — low-vision typography (overlap on size, contrast, spacing).
- [`./wcag-type.md`](./wcag-type.md) — WCAG 2.2 text success criteria.
- [`../techniques/measure.md`](../techniques/measure.md) — CPL math.
- [`../science/legibility-vs-readability.md`](../science/legibility-vs-readability.md) — the distinction that grounds this work.
- [`../science/crowding.md`](../science/crowding.md) — spacing interventions and the crowding-based all-caps explanation.
