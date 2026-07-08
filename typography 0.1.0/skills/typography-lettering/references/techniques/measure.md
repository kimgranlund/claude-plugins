---
date: 2026-04-17
coverage: deep
peers:
  - ../science/legibility-vs-readability.md
  - ../science/crowding.md
  - ./modular-scale.md
  - ./vertical-rhythm.md
  - ../scripts/japanese.md
  - ../scripts/cjk-han.md
primary_sources:
  - https://practicaltypography.com/line-length.html
  - https://betterwebtype.com/articles/2018/10/15/rules-of-responsive-web-typography/
  - https://betterwebtype.com/articles/2019/09/16/rule-1-of-responsive-web-typography/
  - https://baymard.com/blog/line-length-readability
  - https://pubmed.ncbi.nlm.nih.gov/9849112/  # Rayner, "Eye movements in reading and information processing: 20 years of research-survey", Psych. Bulletin 124(3), 1998
  - https://doi.org/10.1167/4.12.12  # Pelli, Palomares, Majaj, "Crowding is unlike ordinary masking", J. Vision 4(12):12, 2004
  - https://doi.org/10.1080/00140139.2004.11953001  # Dyson, "How physical text layout affects reading from screen", Behaviour & Information Technology 23(6), 2004
  - https://doi.org/10.1167/11.5.8  # Legge & Bigelow, "Does print size matter for reading?", J. Vision 11(5):8, 2011
  - https://archive.org/details/legibilityofprin0000tink  # Tinker, Legibility of Print (1963)
  - https://www.w3.org/TR/css-values-4/#ch  # CSS Values 4: `ch` unit definition
  - https://www.w3.org/TR/css-contain-3/  # CSS Containment 3: container query length units (cqi/cqb/cqw/cqh/cqmin/cqmax)
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_values_and_units  # MDN CSS values & units
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap  # MDN text-wrap
  - https://tiro.com/John/Tschichold_MeasureOfTheBook.pdf  # Tschichold, "The Form of the Book"
  - https://en.wikipedia.org/wiki/Line_length  # secondary, for historical cross-references
notes:
  - Peer files (../science/crowding.md, ./modular-scale.md, ./vertical-rhythm.md) may not yet exist on disk; cross-references are forward-looking per the skill's planned structure. ../science/legibility-vs-readability.md and ../scripts/japanese.md and ../scripts/cjk-han.md are present.
  - This file is tier=deep: the CSS recipes should be copy-pasteable, the numbers should be honest ranges not false precision, and every "science says" claim should be traceable to the sources above.
---

# Measure (Characters Per Line)

Measure is the single most discussed typographic lever for readability, and it is the one most often quietly wrong on the web. For Latin running prose, the literature converges on a comfort range of roughly **45–75 characters per line, with about 60–66 as the center of the target**. The rule is old (Bringhurst codified it, Tschichold argued a similar case, Tinker ran empirical comparisons), and modern eye-tracking work (Rayner) and screen-specific studies (Dyson) are broadly consistent with it, though the evidence is a *range* rather than an optimum.

This file covers: what measure is and how to count it, where the canonical ranges came from, why they shift with size and leading and x-height and audience, the modern CSS recipes, and the honest exceptions where the rule doesn't apply. Vertical CJK measure is cross-referenced, not duplicated, in `../scripts/japanese.md` and `../scripts/cjk-han.md`.

## Definition

**Measure** is the length of a line of text, counted in **characters per line (CPL)**. In design practice, CPL is counted with a representative sample of the running font — usually lowercase body characters — because that is the alphabet the reader is actually scanning through. In most sources, including Bringhurst, CPL is reported as an average over a passage of prose, not a max.

Two physical senses coexist:

- **Average character width at the running size.** This is the right mental model. If the body font is set at 16px and the average lowercase glyph advances at around 8.5px (roughly 0.53 em for many humanist sans-serifs and serifs at body sizes), then a 65-character line is about `65 × 8.5px = 552px` wide.
- **Width of the digit `0`.** This is what CSS measures with the `ch` unit (see below). The `0` glyph is close to, but not identical to, the lowercase-average in most Latin text faces.

### The `ch` unit, honestly

The CSS `ch` unit is defined by the W3C ([CSS Values 4](https://www.w3.org/TR/css-values-4/#ch)) as the **advance width of the `0` (zero) glyph of the element's font**. This makes `ch` the ergonomic unit for "measure me in characters," but it has quirks:

- In most Latin proportional text faces, the digit `0` is wider than the lowercase average but narrower than an `m` or `w`. Setting `max-width: 65ch` will *typically* yield a line that contains **somewhat more than 65 lowercase characters** — often 70–80. That is usually fine; it lands inside the 45–75 band.
- In **tabular-digit (`tnum`) fonts** or **monospace** fonts, the `0` advance is wider than the lowercase average, so `ch` *over-estimates* line length — `65ch` gives a visually narrower column than you'd expect from 65 characters of prose.
- In **narrow-digit display fonts** (some condensed or heavily designed numerals), `ch` under-estimates.
- When a web font is still loading, `ch` resolves against the fallback font's `0`, which may differ. With good metric-compatible fallbacks (see `./fallback-stacks.md`), the difference is small.

### `em`-based approximation

If you want a font-independent estimate without trusting `ch`, use:

```
max-width ≈ (CPL × average-lowercase-advance-in-em) × 1em
```

For typical Latin text faces the average lowercase advance is about **0.5–0.55 em**. So:

- 65 CPL × 0.5 em ≈ **32em**
- 65 CPL × 0.55 em ≈ **36em**
- 66 CPL × 0.55 em ≈ **36em** (Bringhurst's 66, roughly)

`max-width: 36em;` or `max-width: 32em;` are reasonable font-agnostic approximations. For a 16px base this is about **512–576px**.

You'll see practitioners use `max-width: 70ch;` as the "safe" value, `65ch` as the conventional default, and `60ch` when the body font has a wider-than-typical `0` or when the prose is information-dense. All three are inside the honest range.

## The Norms and Where They Came From

The "about 60–66 characters, within 45–75" rule is not one person's opinion; it is a convergence of print tradition, early empirical reading research-survey, and modern eye-tracking. Knowing where the numbers come from helps you know when to deviate.

### Bringhurst's 66

In *The Elements of Typographic Style* (1992, Ch. 2, "Rhythm & Proportion"), Robert Bringhurst states:

> "Anything from 45 to 75 characters is widely regarded as a satisfactory length of line for a single-column page set in a serifed text face in a text size. The 66-character line (counting both letters and spaces) is widely regarded as ideal."

Two observations worth flagging:

- Bringhurst counts **letters and spaces** in the 66. That means the lowercase-character count is around 55–58 in practice; the 66 is the printable-character count including spaces.
- The "ideal" framing is editorial, not experimental. Bringhurst is synthesizing what classical book setting had arrived at through generations of practice. The empirical literature supports a *range*, not a single number.

### Tschichold and the book-page tradition

Jan Tschichold's *The Form of the Book* (1975, essays from the 1950s) argued from proportions (the golden section, the van de Graaf canon) toward similar measures for book pages. Tschichold's numbers arrive at roughly the same place: around 60 characters per line for octavo-format prose. This is convergent evidence from a pre-experimental tradition that had strong incentive to get it right — readers don't buy books that are hard to read.

### Tinker's mid-century experiments

Miles Tinker (*Legibility of Print*, 1963, and decades of earlier *Journal of Applied Psychology* papers) ran hundreds of reading-speed comparisons at different line lengths. Tinker's bottom line: comprehension and speed were roughly flat across a mid-range of line lengths, degraded at very short measures (line-break thrash, saccade regressions) and very long measures (difficulty finding the next line). Tinker's specific numerical recommendations (often cited as "about 4 inches" / "~60 characters") are period-bound — hot-metal-set print on paper, with no screen reading — but the *shape* of the curve (flat in the middle, degraded at extremes) has held up. See `../science/legibility-vs-readability.md` for the standard caveats about Tinker's methodology.

### Rayner's eye-tracking consensus

Keith Rayner's research-survey program (reviewed in Rayner 1998, *Psych. Bulletin*; Rayner et al. 2016, *Psych. Science in the Public Interest*) is the modern mechanistic basis for why line length matters. Skilled readers fixate at roughly **7–9 characters at a time**, saccade forward to the next fixation, and at line-ends execute a **return sweep** to the start of the next line. The return sweep is a large, imprecise saccade followed by corrective micro-saccades; the longer the line, the more imprecise the return sweep, and the higher the rate of **regressions** (backward saccades) spent relocating the line start.

At very short measures, the reader spends a disproportionate share of saccades on return sweeps rather than forward progress — you pay too much overhead. At very long measures, the line-start-finding task gets harder. The comfort zone is where these two costs are both small.

Rayner's work does not itself crown a CPL; it explains *why* there is a comfort zone.

### Pelli's crowding and letter-level measure

Denis Pelli, Palomares & Majaj's 2004 work on **crowding** (see `../science/crowding.md`) is a distinct but related lever: the visual system fails to integrate letter features when flankers are too close, so letter spacing and x-height affect the legibility floor independent of line length. Crowding implies that measure interacts with tracking: very narrow measure at very tight tracking compounds the two problems. Practical upshot: treat measure and tracking as coupled, not independent.

### Baymard on screens

The [Baymard Institute's UX research-survey](https://baymard.com/blog/line-length-readability) recommends **50–75 characters for screen reading** for usability-critical prose (product descriptions, terms, forms, long-form article content). Their recommendation is slightly tighter on the high end than Bringhurst's 45–75 for print, and tighter on the low end than print tradition — consistent with the finding that screens tend to be glare-loaded, scroll-interrupted, and read by less-committed readers than books.

### Dyson on screen line length

Mary Dyson's 2004 review in *Behaviour & Information Technology* ([DOI](https://doi.org/10.1080/00140139.2004.11953001)) synthesized the screen-reading literature through the early 2000s. Key findings relevant here:

- On low-DPI screens, longer measures (80+ CPL) caused measurable comprehension degradation.
- Very short measures (< ~40 CPL) caused reading-speed loss that didn't recover even at 2x the line count.
- The comfort zone for screen was narrower than for print: roughly **55–75 CPL** rather than **45–75**.
- Measure matters more than the choice of serif vs sans-serif for sustained reading comfort — which means typographic attention is better spent here than on font swaps.

These four sources — Bringhurst's editorial ideal, Tinker's experimental range, Rayner's mechanism, Dyson's screen-specific refinement — converge on: **45–75 comfortable, 60–66 optimal center, 55–75 for screen-weighted audiences**.

## Recommended Ranges by Content Type

The rule is context-sensitive. Below are the ranges the literature and editorial tradition together support, with the caveat that every one is a *range*, not a target:

| Content type | Recommended CPL | Notes |
|---|---|---|
| **Body prose (article, long-form web)** | 55–75 (target ~65) | The workhorse range. Use `max-width: 65ch`. |
| **Body prose (print book)** | 55–70 (target ~66) | Tighter upper bound; print allows more concentrated reading. |
| **Column-narrow prose (editorial sidebar)** | 35–50 | Short aside, margin note, blockquote in column. Below 35 forces unnatural break cadence. |
| **Caption / figure text** | 35–55 | Treated as fragments; readability demands less depth. |
| **Pull quote** | 30–55 | Often intentionally wider or narrower for visual effect; measure-rule is secondary to visual weight. |
| **Data table cells** | 20–40 | Scanning, not reading. Column width is set by data, not readability. |
| **UI chrome — button labels** | N/A | Word-sized; measure-rule doesn't apply. |
| **UI chrome — form field labels** | N/A | Short phrase; measure-rule doesn't apply. |
| **Navigation items** | N/A | One or two words. |
| **List items (bullet, product list)** | 40–70 | Treat as prose below 7 words, as fragment above. |
| **Headlines (display size ≥ 32px)** | 35–50 | Big type needs narrower measure for same eye-movement comfort; see "Factors" below. |
| **Subheadings (20–28px)** | 45–65 | Transitional; closer to body. |
| **Poetry** | line breaks are semantic | Do not wrap. Use `white-space: pre-line` or explicit `<br>`; overflow with horizontal scroll or size reduction. |
| **Song lyrics, stage directions** | semantic | Same as poetry. |
| **Code listings (monospace)** | 80–120 | Wraps are harmful to comprehension of code structure. Horizontal scroll is typically better than soft-wrap. |
| **Pre-formatted ASCII tables / logs** | as wide as content | Wrap breaks the visual grid; allow horizontal scroll. |
| **Terminal output, console log** | 80–160 | Not prose — use monospace full width. |
| **Chat messages (messaging UI)** | 35–55 | Shorter than article body because messages are scanned in a stream, not read deeply. |

Numbers above are Latin-script. CJK vertical text uses an entirely different accounting (see "Vertical Text" below).

## Factors That Shift the Optimal

The 60–66 center is for a *typical* body font at *typical* size with *typical* leading. Each of the following shifts the optimal:

### Font size

**Bigger body size → narrower measure.** Reasoning: the reader's fixation window is roughly 7–9 *characters*, not a fixed visual angle. When characters get bigger, the fixation window covers less horizontal screen distance, so the number of saccades per line increases. To keep saccades-per-line roughly constant, the CPL should drop.

In practice:

- 14–15px body: measure can creep toward 70–75 CPL before regression rate climbs.
- 16–18px body: the standard 60–66 window.
- 20–24px body ("comfortable reading" mode, e.g. Medium-style): 50–60 CPL.
- 28–36px display (pull quote): 35–50 CPL.
- 40px+ headlines: 25–40 CPL.

### Line-height (leading)

**Looser leading tolerates longer measure; tighter leading needs narrower.** At the line-end return sweep, the eye has to re-acquire the next line's start. If lines are packed (line-height 1.2, tight for body), the next-line target is close to the current line, and eye-movement imprecision is more likely to land on the wrong line — a visible regression. Widening the leading (line-height 1.5–1.7) makes the target unambiguous at the cost of page density.

Rules of thumb:

- `line-height: 1.3–1.4` → stay closer to 55–65 CPL.
- `line-height: 1.5–1.6` → 60–70 CPL is comfortable; up to 75 CPL on high-DPI.
- `line-height: 1.7+` → editorial, ragged ease; 65–75 CPL tolerated.

### x-height

Higher x-height → longer measure tolerated at the same em, because more of each character's ink is in the reading zone. This is a secondary effect; don't rely on it to justify deviating much from the 60–66 center. See `../metrics/metrics-glossary.md`.

### Weight

Heavier weight crowds at the letter level (narrower counters, tighter apparent spacing) and so pulls the optimal measure down. Body weights (400–500) are the reference; Medium to Bold body (600+) suggests tightening CPL by 5–10 characters. This is rarely invoked because body is rarely set in bold.

### Audience: age, reading proficiency, and accessibility

- **Young readers, beginning readers.** Shorter measure + looser leading is repeatedly recommended. 40–55 CPL is typical for children's editorial.
- **Dyslexic readers.** There is no robust evidence that dyslexia-specific fonts help (see `../science/legibility-vs-readability.md`), but there *is* evidence that **increased letter-spacing, line-spacing, and shorter measure** do help (Zorzi et al. 2012, *PNAS*). Treat measure reduction as a first-class accessibility intervention. Aim 45–55 CPL.
- **Low-vision readers.** Often increase font size via browser controls; the measure adjusts proportionally *if* you used a relative unit. `max-width: 65ch` scales correctly with user font-size preferences; a `max-width: 540px` does not. See `../accessibility/wcag-type.md` (pending).
- **ESL / unfamiliar-content readers.** Shorter measure reduces cognitive load; 50–60 CPL is friendlier than 70–75.
- **Older readers (presbyopic).** Larger body + relative measure via `ch` accommodates well; no separate CPL rule applies.

### Reading context and medium

- **Phone vertical (portrait, < 420px viewport).** Measure is bounded by viewport. Expect 35–50 CPL at 16px; accept it.
- **Tablet / ereader.** 55–75 CPL achievable and comfortable.
- **Desktop wide viewport.** CPL bounds are the design constraint, not the viewport. Always cap.
- **Projected / presentation display.** Viewing distance affects the eye's angular fixation span. Large screens read at 5–10 meters may need 30–45 CPL.

## CSS Implementation

### The canonical recipe (2026-04)

```css
.prose {
  max-width: 65ch;
  line-height: 1.55;
  text-wrap: pretty;
}
```

This is the single recipe to know:

- `max-width: 65ch` caps measure in character-units of the running font.
- `line-height: 1.55` gives the leading headroom to tolerate a measure toward the upper end of the range.
- `text-wrap: pretty` (see `../contemporary/css-text-properties.md`) improves line-break quality so the last line isn't a runt and short-word orphans are reduced. As of 2026-04 this is supported in Chrome 117+ and Safari 26+; Firefox has not shipped it. When absent it degrades gracefully to the default greedy line-breaker — the measure cap still applies.

### Variant: font-agnostic em-based

If you prefer to not depend on the running font's `0` width:

```css
.prose {
  max-width: 36em;   /* ~65 CPL for typical Latin text faces */
  line-height: 1.55;
  text-wrap: pretty;
}
```

This scales with the element's own `font-size` and is immune to digit-width quirks. It is *slightly* less honest about character count — a display font with wide letters will produce fewer CPL than a typical font — but the error is small.

### Variant: `rem`-based

```css
.prose {
  max-width: 36rem;   /* ~65 CPL at default 16px root */
  line-height: 1.55;
  text-wrap: pretty;
}
```

`rem` is font-size-invariant at the element level but scales with the user's root font-size preference, which is the accessibility-correct behavior. Use this when the body's `font-size` might vary (e.g. nested components with their own type scale) but you want a consistent column width across all of them.

### Container queries and `cqi`

As of 2026-04, container query length units are well-supported ([Baseline 2023](https://www.w3.org/TR/css-contain-3/)). The useful units:

- `cqi` — 1% of the query container's inline size
- `cqb` — 1% of the query container's block size
- `cqw`, `cqh`, `cqmin`, `cqmax` — other containment-relative

When the paragraph's *container* (not viewport) should drive measure:

```css
.card {
  container-type: inline-size;
  container-name: card;
}

.card .prose {
  /* For containers 45rem+ wide, use 65ch; for narrower containers, fill. */
  max-width: min(65ch, 100cqi);
  line-height: 1.55;
  text-wrap: pretty;
}
```

This is the right tool when the same prose component appears in multiple layout contexts (full-bleed article, sidebar aside, card, modal) and measure should adapt to the inline space rather than the viewport.

### Combined recipe with hyphens

```css
.prose {
  max-width: 65ch;
  line-height: 1.55;
  text-wrap: pretty;
  hyphens: auto;
  /* Tighten the hyphenation rules to avoid ladder-of-hyphens */
  hyphenate-limit-chars: 8 4 4;  /* min word length, min-before, min-after */
  hyphenate-limit-lines: 2;      /* max consecutive lines ending in hyphens */
}
.prose:lang(en) { /* ensure lang is set — hyphenation is language-dependent */ }
```

`hyphenate-limit-chars` and `hyphenate-limit-lines` (WebKit-only for the latter as of 2026-04; Chrome supports `-chars` since 109; Firefox 137+) bring hyphenation closer to InDesign-quality. See `../contemporary/css-text-properties.md` for current support.

### Gotchas

- **Don't put `max-width` on the container; put it on the text element.** A `section { max-width: 65ch; }` caps the section width, which typically wastes viewport on the right. Keep the container flexible (e.g. a grid column) and cap the `<p>`, `<h1>`, `<li>` text elements. Or center a typographic column with `.prose { max-width: 65ch; margin-inline: auto; }`.
- **Don't cap measure on `<code>` or `<pre>`.** Code is monospace and is not prose; it often needs 80–120 columns.
- **Don't apply measure to `<figcaption>` without testing.** Captions are fragments; a 65ch cap is usually too wide.
- **Beware inherited `max-width` in nested article layouts.** If your article framework already caps at 65ch and you wrap a `<blockquote>` in a narrower container, the blockquote ends up double-capped and can look pinched. Use `max-inline-size` and let it be `unset` where appropriate.
- **`ch` changes with `font-size`.** If you nest a smaller-size aside inside a prose block, its `65ch` will be a smaller pixel width than the surrounding prose's `65ch`. Usually correct; occasionally surprising.
- **`ch` is the `0`, not the average.** Already discussed; revisit when your body font has unusual digit width.

### Recommended default component

For a "prose content" component in a design system, the minimum:

```css
/* Use a cascade layer to set defaults that component-level styles can override. */
@layer typography.prose {
  .prose {
    max-width: 65ch;
    margin-inline: auto;
    line-height: 1.55;
    text-wrap: pretty;
    hyphens: auto;
  }

  .prose :is(h1, h2, h3) {
    /* Headings use balance, not pretty */
    text-wrap: balance;
    line-height: 1.2;
  }

  .prose :is(h1) { max-width: 20ch; }  /* big headings narrower */
  .prose :is(h2) { max-width: 30ch; }
  .prose :is(h3) { max-width: 45ch; }

  .prose blockquote {
    max-width: 50ch;  /* editorial sidebar feel */
    font-style: italic;
  }

  .prose figcaption {
    max-width: 50ch;
  }

  .prose pre,
  .prose code {
    max-width: none;  /* allow horizontal scroll */
  }
}
```

This is the "`.prose` class" convention used by Tailwind Typography, GOV.UK's frontend, and most design-system prose plugins. The key moves are: (1) cap body; (2) **narrow headings further** (rule-of-thumb: heading max-width inversely correlates with heading size); (3) release the cap on code.

## Legitimate Exceptions

Context where the 45–75 range does not apply:

### Data-dense content

Spreadsheets, log viewers, tabular data, and scanning-oriented UI care about *grid alignment* and *scanning speed*, not about reading prose. Column width is dictated by data. Apply `max-width` per column only if it prevents overflow, not to conform to measure. See "Code listings" below for a parallel case.

### Poetry, lyrics, stage directions

Line breaks are semantic — the author chose them to mean something. Preserve them with `white-space: pre-line` or explicit `<br>`, and let the measure fall where it falls. If the poem overflows, size down or horizontal-scroll; never soft-wrap.

```css
.poem {
  white-space: pre-line;
  max-width: none;
}
```

### Short impact statements, pull quotes

These are visual set pieces, not prose. Designers often go *wider* (70–90 CPL for a pull quote across a two-column grid) or *narrower* (25–35 CPL for a centered statement) for visual effect. The measure rule is subordinate to the visual hierarchy. Ensure the statement is short enough that CPL barely matters (one to three lines).

### Monospace code

80–120 columns is the long-standing convention in programming (the 80-column Hollerith card is the origin; modern style guides like PEP 8 go 79 or 88 or 99; Google's Java style goes 100; most others allow 100–120). Soft-wrapping code breaks visual parsing of structure (indentation levels, alignment of tokens); horizontal scroll is usually the lesser evil.

```css
pre, code {
  max-width: none;
  overflow-x: auto;
  font-family: var(--font-mono);
  tab-size: 2;  /* or whatever the project uses */
}
```

Apply `white-space: pre` on `<pre>`, `white-space: pre-wrap` only if soft-wrap is acceptable for the content.

### Advertising / promotional display typography

Marketing hero blocks, billboard-style type, and conversion-oriented copy frequently violate the measure rule on purpose — the goal is attention, not sustained reading. A 90-character cap across three 28px lines is "wrong" per the rule and right for the purpose.

## Multi-column Prose

CSS multi-column layout (`columns`) is an honest alternative to a long single measure when viewport width is abundant and the content is print-like (long-form essay, book-chapter, printed newsletter).

```css
.multi-col {
  columns: 2;
  column-gap: 2rem;
  column-fill: balance;  /* default; both columns fill to roughly equal height */
  max-width: 75rem;      /* cap total width so each column is still in range */
  hyphens: auto;
}
```

With two columns at 75rem total and 2rem gap, each column is roughly `(75rem - 2rem) / 2 = 36.5rem`, which is ~65 CPL. The measure rule holds per column.

### When multi-column works

- **Print-like long-form reading.** Essays, reports, newsletters with a print aesthetic. Wall Street Journal, NYT Magazine, Harper's, Atlantic — when done with care, these work.
- **Pages where the user will not scroll mid-content**. A two-column block that fits in the viewport is fine; the reader scans column 1 top-to-bottom, then column 2.
- **Printed pages.** `@media print` with multi-column is idiomatic.

### When multi-column fails

- **Scrolling mid-column is awkward.** If the reader has to scroll to finish column 1 and then scroll *back up* to start column 2, the flow is broken. This is the single largest reason multi-column is rare on the web: most content exceeds one viewport.
- **Short content with a fixed image or quote inside.** Multi-column creates awkward reflows.
- **Dynamic content where line counts vary.** Column rebalancing on content change causes visible shifts.
- **Narrow viewports.** Below ~800px, two columns at 65ch each doesn't fit.

Rule of thumb: use multi-column only if the content fits in the viewport, or only in print. For web long-form, prefer a single ~65ch column.

### `column-fill: balance` vs `auto`

- `balance` (default): both columns fill to roughly equal height. Good for bounded content.
- `auto`: columns fill greedily — column 1 fills, then column 2 starts. Good for cases where the container height is the constraint (e.g. a multi-column list that overflows).

### Responsive fallback

```css
.multi-col {
  columns: 1;
  column-gap: 2rem;
  max-width: 65ch;
  margin-inline: auto;
}

@media (min-width: 64rem) {
  .multi-col {
    columns: 2;
    max-width: 75rem;
  }
}
```

At small viewports, fall back to a single column with measure cap. At wide viewports, widen and split.

## Vertical Text (CJK)

For Japanese tategaki and Chinese vertical text, "measure" is counted in **fullwidth characters per column (行) / line**, and the dominant CSS lever is the inline-size of the writing-mode block, not `max-width` in `ch`.

A column of Japanese prose typically runs **30–45 full-width characters** (kanji, kana, or fullwidth punctuation, each on the em-grid). Classic tategaki book typesetting often targets about 35–42 characters per column. Newspapers use narrower columns (15–20 characters). Modern web tategaki follows similar conventions; see `../scripts/japanese.md` for the specifics of `writing-mode: vertical-rl`, `text-orientation`, and tate-chū-yoko.

The CSS `ic` unit (width of the `水` glyph or equivalent CJK ideograph's advance) is the vertical-equivalent of `ch` for CJK. It is supported in Chrome 110+, Safari 15.4+, Firefox 87+:

```css
.tategaki {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  max-inline-size: none;    /* don't cap inline size */
  max-block-size: 40ic;     /* cap column length — about 40 fullwidth chars */
  line-height: 1.75;        /* CJK tolerates looser leading */
}
```

Note that in vertical writing modes, `max-block-size` controls column length (the Japanese "measure" in the reading direction), and `max-inline-size` controls the column's width perpendicular to reading. The mental model flips.

For mixed-script Japanese (kanji + kana + romaji + digits), the 35–45 full-width-char target still applies, with the understanding that Latin segments occupy less than one em each. See `../scripts/japanese.md` for how tate-chū-yoko handles short Latin runs and how `word-break: auto-phrase` interacts with measure.

Cross-reference: `../scripts/cjk-han.md` for Chinese-specific conventions (Simplified PRC vs Traditional Taiwan vs Hong Kong differ), `../scripts/japanese.md` for Japanese-specific tategaki and ruby.

## Testing in Production

Measure is invisible until the page is rendered in the reader's actual context. The following testing moves catch most problems.

### Chrome DevTools per-element inspect

- Right-click on a `<p>` → Inspect.
- The Computed tab shows the resolved `max-width` in pixels.
- In the Layout panel, box-model shows actual width.
- Counting characters manually on one line gives a ground-truth CPL.

For a faster ground-truth measurement, paste this into the console on any prose page:

```js
// Count characters in the first few lines of the hovered paragraph.
const el = $0;  // after right-click → Inspect on a <p>
const style = getComputedStyle(el);
const width = el.clientWidth;
const avgCharWidthPx = parseFloat(style.fontSize) * 0.5;  // rough
console.log(`~${Math.round(width / avgCharWidthPx)} CPL at ${style.fontSize}`);
```

This is an approximation — for precision, use a canvas-measured `measureText` pass — but it's fast enough to audit a dozen paragraphs in a minute.

### Multi-viewport "monkey test"

Render the prose at a set of standardized viewport widths:

- **320px** (smallest mobile; below this, prose is constrained by viewport)
- **390px** (modern phone portrait)
- **768px** (tablet portrait)
- **1024px** (tablet landscape / small laptop)
- **1280px** (standard laptop)
- **1440px** (modern laptop / compact desktop)
- **1920px** (desktop wide)
- **2560px+** (ultrawide)

At each, check: does measure stay inside 45–75? At 320px, 50 CPL may be the best you can do; that's fine. At 2560px, the prose should not fill the width — it should cap and center.

DevTools device toolbar (cmd-shift-M on macOS Chrome) cycles through these quickly. Playwright or Puppeteer in CI can snapshot at each.

### Monospace measurement substrate

A classic trick for establishing ground-truth CPL: render the target prose in a monospace font at the target size, inside the target width. In monospace, every character is the same advance — counting is trivial.

```html
<p style="font-family: monospace; font-size: 16px; max-width: 65ch; line-height: 1.55;">
  The quick brown fox jumps over the lazy dog. The quick brown fox jumps over
  the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown
  fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.
</p>
```

Count the characters per line directly. If you want to know "what CPL does my 65ch actually produce in the deployed font?", swap the font-family back to your running font and compare. The shift tells you how far off `ch`-based estimate is for your specific font.

### Ruler overlay bookmarklet

Keep one of these handy for casual auditing:

```js
javascript:(()=>{const style=document.createElement('style');style.textContent=`*{outline:1px solid rgba(255,0,0,0.15)!important}p,li,h1,h2,h3,h4,h5,h6{outline-color:rgba(0,0,255,0.4)!important}`;document.head.appendChild(style)})();
```

Pasted as a bookmarklet, it highlights every text element. Visually scan for any block that runs the full viewport width — those are your measure failures.

### Lighthouse / axe

Lighthouse does not flag measure directly, but its "accessibility" section flags contrast, font size, and line-height issues that often co-occur with measure problems. axe-core similarly doesn't have a "measure too long" rule; this remains a human-visual audit.

## Anti-patterns

Named failure modes that recur often enough to watch for:

### Full-viewport prose

Setting `<p>` with no `max-width` cap on a page where the viewport is ever > ~720px. At 1440px the line length is ~180 CPL and regression rate spikes. The single most common typographic bug on the web.

### Over-tight cap

`max-width: 40ch` or below for what is actually body prose. Forces ~6-word lines, line-break thrash, and hyphenation-limit exhaustion. Blog platforms that auto-apply a "mobile-first" narrow cap even on desktop are the usual offender.

### Cap on wrong element

`article { max-width: 65ch; }` instead of `article p { max-width: 65ch; }`. Caps the whole `<article>` — including images, code blocks, figures, and anything else — at prose-narrow width. Those should either fill the viewport or be capped at their own width.

### Double-cap

Applying `max-width: 65ch` on the prose element *and* having the parent container also apply a max-width. Causes the prose to be narrower than intended and often pinched.

### Measure via `max-width: 600px`

Absolute-pixel caps that don't scale with user font-size preferences. A user who sets their browser to 200% text will get the same 600px column — which at 32px body is ~35 CPL, below the comfort range. Prefer `ch`, `em`, or `rem`.

### No cap on wide-viewport hero

Hero blocks, about-us statements, landing-page intros often use `font-size: 28px` and fill the viewport. 28px at 1440px viewport is ~70 CPL — inside the range but at the upper end; at 1920px it's ~95 CPL, well over. Apply measure caps to hero prose too.

### Uniform measure across all headings and body

Using the same `max-width: 65ch` on `h1` through body. Large headings at 65ch wrap to 3–5 lines; visually, they fragment. Narrow headings (`h1 { max-width: 20ch }`; `h2 { max-width: 30ch }`) look deliberate.

### Measure ignored in multi-column

Setting `columns: 3` inside a 65rem container gives each column a ~22rem width, which at 16px body is ~40 CPL — below the comfort range. Multi-column arithmetic must preserve per-column measure.

### Caption-too-wide

Figure captions inheriting the prose cap at 65ch. Captions are fragments; 50ch is more appropriate.

### "I'll justify it; then long measure is fine"

Full justification does not fix the line-start-re-acquisition problem that Rayner identifies. It also introduces river effects and hyphenation stretching. Long measure is long measure regardless of alignment. If you're justifying, enable `hyphens: auto`, `hyphenate-limit-chars`, and constrain measure first.

### Ignoring measure in Japanese/Chinese contexts

Using `max-width: 65ch` on CJK blocks. `ch` measures the `0` glyph, which for most CJK fonts is a narrow digit, so `65ch` produces a line of ~60–65 fullwidth characters in CJK — almost double the 35–45 comfort range. For CJK, use `max-inline-size` (horizontal) or `max-block-size` (tategaki) sized in `ic` or `em`.

## Sources

(Retrieval dates: all 2026-04-17 except where noted.)

- **Bringhurst, R. (2012).** *The Elements of Typographic Style.* 4th ed., Hartley & Marks. Ch. 2, "Rhythm & Proportion," esp. 2.1.2 "Choose a comfortable measure." The 45–75 / 66-character formulation.
- **Tschichold, J. (1991).** *The Form of the Book: Essays on the Morality of Good Design.* Hartley & Marks. (Original essays 1950s–1970s.) On classical proportions and measure in book setting.
- **Tinker, M. A. (1963).** *Legibility of Print.* Ames, IA: Iowa State University Press. https://archive.org/details/legibilityofprin0000tink — chapter on line length.
- **Rayner, K. (1998).** "Eye movements in reading and information processing: 20 years of research-survey." *Psychological Bulletin* 124(3): 372–422. https://pubmed.ncbi.nlm.nih.gov/9849112/
- **Rayner, K., Schotter, E. R., Masson, M. E. J., Potter, M. C., & Treiman, R. (2016).** "So much to read, so little time: how do we read, and can speed reading help?" *Psychological Science in the Public Interest* 17(1): 4–34. https://doi.org/10.1177/1529100615623267
- **Pelli, D. G., Palomares, M., & Majaj, N. J. (2004).** "Crowding is unlike ordinary masking: distinguishing feature integration from detection." *Journal of Vision* 4(12): 12. https://doi.org/10.1167/4.12.12
- **Dyson, M. C. (2004).** "How physical text layout affects reading from screen." *Behaviour & Information Technology* 23(6): 377–393. https://doi.org/10.1080/00140139.2004.11953001
- **Legge, G. E., & Bigelow, C. A. (2011).** "Does print size matter for reading? A review of findings from vision science and typography." *Journal of Vision* 11(5): 8. https://doi.org/10.1167/11.5.8
- **Zorzi, M., Barbiero, C., Facoetti, A., et al. (2012).** "Extra-large letter spacing improves reading in dyslexia." *PNAS* 109(28): 11455–11459. https://doi.org/10.1073/pnas.1205566109
- **Baymard Institute (2024, rev.).** "Readability: The Optimal Line Length." https://baymard.com/blog/line-length-readability
- **Butterick, M.** *Practical Typography*, "Line length." https://practicaltypography.com/line-length.html
- **Koch, M.** *Better Web Type*, Ch. 4, "Responsive Web Typography." https://betterwebtype.com/articles/2019/09/16/rule-1-of-responsive-web-typography/
- **W3C CSS Values 4.** `ch` unit definition. https://www.w3.org/TR/css-values-4/#ch
- **W3C CSS Containment 3.** Container query length units (`cqi`, `cqb`, `cqw`, `cqh`, `cqmin`, `cqmax`). https://www.w3.org/TR/css-contain-3/
- **MDN.** `text-wrap`. https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
- **MDN.** CSS values and units. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_values_and_units
