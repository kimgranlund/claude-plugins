---
date: 2026-04-17
coverage: deep
peers:
  - ./dyslexia.md
  - ../../expert-color/references/contrast.md
  - ../../expert-color/references/apca.md
primary_sources:
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/TR/wcag-3.0/
  - https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/
  - https://readtech.org/ARC/tests/
  - https://eur-lex.europa.eu/eli/dir/2019/882/oj
  - https://www.w3.org/WAI/WCAG22/Understanding/
  - https://www.w3.org/WAI/WCAG22/Techniques/
  - https://apcacontrast.com/
---

# WCAG 2.2 Success Criteria for Type, and the WCAG 3.0 Direction

**Peers:** [dyslexia-specific typography evidence](./dyslexia.md) — for why "low-vision SCs" and "dyslexia-friendly font" are different problem spaces. Color-contrast numerics live in `expert-color` — see `../../expert-color/references/contrast.md` (WCAG 2.x luminance model) and `../../expert-color/references/apca.md` (WCAG 3.0 perceptual-contrast proposal).

This file catalogues every WCAG 2.2 success criterion that constrains type, walks each one down to a concrete CSS/HTML implementation check, and then maps the direction WCAG 3.0 is heading — particularly APCA, which would replace the 2.x luminance-ratio contrast model entirely. A practitioner-oriented reference: the SC numbers appear verbatim because legal and procurement documents reference them by number.

---

## Orientation — three facts to hold in mind

1. **WCAG 2.2 is the in-force normative standard.** Published as a W3C Recommendation in October 2023, it is the successor to WCAG 2.1. It is the version referenced by EN 301 549 (the European harmonised standard), Section 508 (after the 2024 refresh), and most national laws. WCAG 2.2 is what you are audited against in 2026.
2. **WCAG 3.0 is still a Working Draft.** First published in January 2021, it has not reached Candidate Recommendation. Its guidelines, methods, and conformance model — including APCA — are non-normative. Treat WCAG 3.0 material as directional, not compliance-ready.
3. **Type accessibility is not reducible to contrast.** Contrast (1.4.3, 1.4.6) is the most-audited SC, but **resize** (1.4.4), **reflow** (1.4.10), **text spacing** (1.4.12), and **visual presentation** (1.4.8) all constrain the typographic system independently. A design can pass 1.4.3 on every pair and still fail 1.4.12 the moment a user applies the spacing bookmarklet.

---

## Part 1 — WCAG 2.2 text-related success criteria

Ordered roughly by practical weight (what fails in real audits), not by SC number.

### SC 1.4.3 Contrast (Minimum) — Level AA

**Text says:** Visual presentation of text and images of text has a contrast ratio of at least **4.5:1**, with the following exceptions:
- **Large text** — 18pt (≈24 CSS px) or 14pt bold (≈18.66 CSS px bold) — requires only **3:1**.
- **Incidental text** — inactive UI, pure decoration, invisible text, or text within a picture that is incidental — is exempt.
- **Logotypes** are exempt.

**Measurement model (2.x).** WCAG 2.x contrast is computed as `(L1 + 0.05) / (L2 + 0.05)` where `L1` is the relative luminance of the lighter and `L2` of the darker, each derived from sRGB channels with a standard gamma-inversion and the Rec. 709 coefficients (`0.2126 R + 0.7152 G + 0.0722 B`). It is symmetric (same ratio regardless of which color is fg/bg) and does not distinguish light-on-dark from dark-on-light. This model is the origin of the **1.4.3 "dark-mode problem"**: the equation under-penalises light text on dark backgrounds at small sizes, which APCA (below) corrects.

**How it fails in practice.**
- Placeholder text in inputs at `color: #999` on `background: #fff` — 2.84:1, fails for any non-large size.
- Disabled buttons are often inherited from a tokenised `--color-fg-muted` that only meets 3:1, then used for non-disabled secondary text too.
- Brand-color CTAs against white: many "accessible" brand blues dip to 3.8:1 at body sizes.

**Cross-link:** for the pair-expansion, OKLCH ramp design, and how to guarantee the 4.5:1 floor across theme × scheme × contrast, see `../../expert-color/references/contrast.md` and the `ui-verify-color` composition skill.

### SC 1.4.6 Contrast (Enhanced) — Level AAA

Same structure, higher floors: **7:1** normal, **4.5:1** large. Target for editorial/long-form products and medical/government surfaces. Not required for compliance but often a good default for reading-heavy surfaces — and it happens to align roughly with APCA ~Lc 75.

### SC 1.4.4 Resize Text — Level AA

**Text says:** Except for captions and images of text, text can be resized without assistive technology up to **200%** without loss of content or functionality.

**What this means operationally.**
- The **user** applies browser zoom (or "increase text size" in OS settings). Your layout must still be usable.
- "Loss of functionality" means buttons no longer reachable, essential content hidden, critical overflow clipped, focus order broken.
- Horizontal scrolling caused by 200% zoom is **allowed** under 1.4.4 alone, but SC 1.4.10 (Reflow) generally constrains that further at 320 CSS px widths.

**Implementation.**
- Declare text sizes in **relative units**: `rem`, `em`, or `%`, not `px`.
- Avoid fixed-height text containers with `overflow: hidden` — line-height grows with zoom and clips.
- Avoid `font-size: 16px !important;` on body — the `!important` disables user-agent scaling.
- Test by applying `<html>{font-size: 200%}` or browser zoom and checking every critical flow.

**Caveat.** Ctrl-+ zoom in modern browsers scales the entire viewport, so even `px` text scales. The SC predates this behaviour. The more restrictive interpretation — also honoured by WAI — is that **text-only zoom** (Firefox "Zoom → Zoom Text Only") must also work. This is what catches `px`-based typography.

### SC 1.4.10 Reflow — Level AA

**Text says:** Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions at:
- A width equivalent to **320 CSS px** for vertical-scrolling content
- A height equivalent to **256 CSS px** for horizontal-scrolling content

**Exceptions** where two-dimensional scroll is allowed: parts of content requiring two-dimensional layout for usage or meaning — tables, maps, code samples, video, games, diagrams.

**Operational translation.** Take a desktop viewport, narrow it to 320 CSS px (or apply 400% zoom on a 1280px viewport — equivalent). Everything except exempt content must reflow. No horizontal scrollbar at the page level.

**What this breaks.**
- Fixed-width components without `max-width: 100%`.
- Tables used for layout rather than tabular data.
- Horizontally-laid-out forms (label beside input) that don't collapse.
- Nav bars with overflow:scroll that hide items behind scrolls without an affordance.

**Interaction with type.** Narrow measures below 320 CSS px can produce ragged line lengths of 2–4 words — less a compliance issue than a legibility one, but related. See [the dyslexia file](./dyslexia.md) for why very short measures also hurt.

### SC 1.4.12 Text Spacing — Level AA

**Text says:** In content implemented using markup languages that support the following text-style properties, no loss of content or functionality occurs when the user sets all of the following, and by changing no other style property:
- **Line height (line spacing)** to at least **1.5** times the font size
- **Spacing following paragraphs** to at least **2** times the font size
- **Letter spacing (tracking)** to at least **0.12** times the font size
- **Word spacing** to at least **0.16** times the font size

**This is not a design floor. This is an override tolerance.**

The SC does not require your design to *use* 1.5 line-height. It requires that when a user applies a text-spacing bookmarklet (Adrian Roselli's and Steve Faulkner's bookmarklets are the canonical test tools), nothing clips, overflows, or becomes unreachable.

**Testing protocol.**
1. Apply the "WCAG 1.4.12 text spacing" bookmarklet (or the `user-stylesheet` approach).
2. Scroll the full page.
3. Check for:
   - Text clipped at the bottom of a fixed-height container.
   - Buttons or links running off the side of their container.
   - Overlapping text.
   - Essential content pushed below a fold that has `overflow: hidden`.

**Patterns that fail.**
- Buttons with `height: 40px` and `line-height: 40px` — once line-height becomes 1.5, the text pushes out.
- Hero sections with `height: 100vh` and centered text — increasing line height can push text past the bottom.
- Single-line truncated card titles (`white-space: nowrap; overflow: hidden; text-overflow: ellipsis`) — these are usually accepted by auditors since the truncation is pre-existing, but only if the full text is available elsewhere (tooltip, expanded state).

**Implementation guidance.**
- Prefer `min-height` over `height` for text-containing elements.
- Let line-height cascade from the body (don't set explicit line-heights per component unless necessary).
- Use **unitless** `line-height` values (e.g. `line-height: 1.5`) so the value multiplies the element's own font-size rather than inheriting a fixed distance.

### SC 1.4.8 Visual Presentation — Level AAA

This is the one most-often-ignored SC, and the richest typographic guidance WCAG 2.x offers. It is AAA, so compliance is optional, but it is the closest thing to a W3C-endorsed typesetting spec.

**Text says:** For the visual presentation of blocks of text, a mechanism is available to achieve the following:
1. Foreground and background colors can be selected by the user.
2. Width is no more than **80 characters or glyphs** (40 if CJK).
3. Text is not justified (aligned to both left and right margins).
4. Line spacing (leading) is at least **space-and-a-half within paragraphs** (1.5×), and paragraph spacing is at least **1.5 times larger** than the line spacing.
5. Text can be resized without assistive technology up to **200%** in a way that does not require the user to scroll horizontally to read a line of text on a full-screen window.

**The items individually.**

**80-character measure.** The "CPL" (characters per line) cap. Web typography tradition cites 45–75 as optimal (Bringhurst); WCAG's 80 is a generous upper bound. Above 80, the eye loses the next-line target more often ("doubling"). In CSS: `max-width: 65ch` — `ch` is the advance width of `0` in the current font, a practical approximation of CPL. `70ch` is a good default cap; `80ch` is the WCAG ceiling.

**No justified prose.** `text-align: justify` creates rivers of white space and — especially without hyphenation — produces uneven word spacing that damages reading. Justified text is a failure mode for many dyslexic readers specifically (see [dyslexia.md §4](./dyslexia.md#what-does-help-stronger-evidence-base)). The SC allows justified text *if* there is a mechanism to turn it off, but simpler: don't justify prose. Reserve justified for book-style editorial contexts with proper H&J engines.

**Line height 1.5× within paragraphs, paragraph spacing 1.5× greater than line spacing.** For body at 16px with line-height 1.5 (24px), paragraph spacing would be at least 36px — about 2.25× the font size. This matches the 1.4.12 override numbers for line spacing but goes slightly further for paragraph spacing.

**User-adjustable colors.** Rarely provided as a first-class feature, but many sites satisfy this indirectly via light/dark modes, high-contrast modes, and user stylesheets. The SC technically wants an *in-product* mechanism.

**Why the SC matters even though it's AAA.** The numbers — 80 CPL, 1.5 line-height, 1.5× paragraph spacing — are the closest thing the W3C has to a readability floor, and they're congruent with typographic tradition and with the dyslexia literature. Use 1.4.8 as a **design target for editorial and documentation surfaces** even if you're only contractually held to AA.

### SC 1.4.13 Content on Hover or Focus — Level AA

Not strictly type, but relevant: tooltips and popovers triggered by hover/focus must be **dismissible** (via Escape), **hoverable** (pointer can move into them without them disappearing), and **persistent** (they remain until the trigger is removed, the user dismisses, or the information is no longer valid). Hover-revealed text (e.g., help text on form fields) counts; make sure your tooltip doesn't vanish when the user tries to read it.

### SC 3.1.5 Reading Level — Level AAA

**Text says:** When text requires reading ability more advanced than the **lower secondary education level** (roughly 7th–9th grade; age 13–14 completion), a supplemental version or mechanism is available.

**Operational translation.** The prose itself should read at roughly an 8th–9th grade level (US), or the equivalent in other systems — or provide a "plain language" alternative.

**Measurement.** This SC names no specific formula. Common tools:
- **Flesch-Kincaid Grade Level** — weights sentence length and syllable count; gives a US grade.
- **Flesch Reading Ease** — 0–100 scale, higher = easier; 60–70 is plain English.
- **Dale-Chall** — compares against a list of ~3,000 common words.
- **SMOG** — simplified measure of gobbledygook; estimates years of education needed.
- **Coleman-Liau, ARI, Gunning Fog** — variants.

**Limitations.**
- **English bias.** All formulas above were developed on English corpora; direct translation to German, French, Japanese is unreliable. Syllable-counting misbehaves on agglutinative or logographic languages.
- **Sentence-length proxy.** Long sentences aren't always hard; short sentences aren't always easy. A staccato sequence of technical terms can score "easy" while being opaque.
- **No semantics.** Formulas don't know that "leverage synergies" is jargon.
- **Tokenisation artifacts.** Abbreviations, URLs, and em-dashes trip sentence splitters.

**Practical tools.**
- **Hemingway App** — in-browser; flags long sentences and adverbs; gives a grade level.
- **Readable.io** — bulk analysis, API.
- **Microsoft Word / Google Docs** — both expose Flesch scores under document statistics.

**Takeaway.** The reading-level SC is a loose constraint. The evidence-backed play is shorter sentences, plainer vocabulary, and a clear hierarchy — not chasing a specific F-K number. And crucially: if you serve non-English audiences, use a formula validated for that language (e.g., LIX for Scandinavian, Wiener Sachtextformel for German, Fernández Huerta for Spanish).

### SC 1.4.5 Images of Text / SC 1.4.9 Images of Text (No Exception) — AA / AAA

Images of text must be avoided except for logos and where a specific presentation is essential. This is more a type-in-CSS mandate than a typography SC: stop shipping hero headlines as JPEGs. Once text is in CSS, everything above becomes reachable — zoom, spacing override, contrast toggles.

### SC 2.4.8 / 2.4.11 / 2.4.13 Focus — related

Not body-text SCs, but they constrain interactive type:
- **2.4.11 Focus Not Obscured (Minimum)** — AA, new in 2.2. The focused item must not be entirely hidden behind sticky headers/footers.
- **2.4.13 Focus Appearance** — AAA, new in 2.2. Focus indicator must be at least a 2-CSS-px perimeter with 3:1 contrast against adjacent colors.

These matter for typography because link focus rings, button focus rings, and input focus rings are typographic surface features. See the `ui-verify-focus` composition skill for full recipes.

### SC 2.5.8 Target Size (Minimum) — AA, new in 2.2

Interactive targets must be at least **24 × 24 CSS px**, with exceptions for inline targets in sentences (e.g., text links inside a paragraph) and where a minimum is essential. This is new in WCAG 2.2 and replaces the previous AAA 44 × 44 minimum (2.5.5, still AAA).

Typographic implication: inline text links that open important flows may be too small. Consider increasing hit area with `padding` or the `::before` `position: absolute; inset: -8px;` trick — without altering visual size.

---

## Part 2 — WCAG 3.0 directions (as of 2026-04)

### Status

WCAG 3.0 is a **W3C Working Draft**, not a Recommendation. Key dates:
- **January 2021** — first Working Draft published
- **2023–2025** — successive Working Drafts; incremental edits to guidelines, outcomes, methods
- **2026 Q1** — still Working Draft; no Candidate Recommendation target announced as of April 2026

The practical consequence: **do not conform to WCAG 3.0 instead of WCAG 2.2**. Conform to 2.2. If you want to use WCAG 3.0 thinking as a *design direction* or for internal targets, that is reasonable — but legal and procurement obligations still reference 2.x.

### Structural differences

| Axis | WCAG 2.2 | WCAG 3.0 (draft) |
|---|---|---|
| Conformance | Pass/fail per SC | Graduated (bronze / silver / gold) with outcome scores |
| Testability | Human-testable, binary | Mixture of automatic, human-evaluated, and outcomes-based |
| Scope | Web content | Web, apps, tools, authoring, content-generation |
| Contrast | Luminance-ratio 1.4.3 / 1.4.6 | APCA-based, see below |
| Structure | Principle → Guideline → SC | Guideline → Outcome → Method |

### APCA — Accessible Perceptual Contrast Algorithm

**What it is.** A perceptually-weighted contrast model developed by Andrew Somers (Myndex Research) intended to replace WCAG 2.x's luminance-ratio model. APCA accounts for:
- **Direction** of contrast (dark-on-light vs light-on-dark) — the two are not symmetric.
- **Font weight and size** — thin 12px text needs more contrast than 700-weight 24px.
- **Polarity-specific corrections** for perceived lightness.

**Output.** A signed Lc ("lightness contrast") value from roughly –108 to +106.
- Positive Lc = dark text on light background.
- Negative Lc = light text on dark background.
- |Lc| increases with visual contrast.

**Rough thresholds (non-normative, from the APCA "Bronze Simple Mode" proposals).**
- **Lc 75** — minimum for body text (≈16px/400 weight).
- **Lc 60** — minimum for large text or bold body.
- **Lc 45** — minimum for non-text UI / large headings.
- **Lc 30** — minimum for decorative / fluent elements / non-critical text.
- **Lc 15** — absolute floor below which no text should be placed.

These are not WCAG 2.x ratios; you cannot convert one to the other with a simple multiplier. APCA's conformance tables are conditional on font weight and size (the `APCA Readability Criterion`).

**What APCA gets right that 2.x doesn't.**
- **Dark mode honesty.** Light text on dark needs more optical contrast than dark text on light at equivalent luminance ratio. 2.x says they're equal; APCA disagrees (correctly).
- **Thin-type penalty.** A 300-weight 14px label needs more contrast than a 700-weight 48px headline — 2.x uses a flat threshold.
- **Stops rewarding ultra-dim pairs.** 2.x's `(L+0.05)/(L+0.05)` formula has a floor that makes `#000 on #111` pass easily (21:1 because black is black). APCA down-weights this regime.

**What's contested.**
- **Adoption status.** APCA is referenced in WCAG 3.0 drafts but has not been ratified as normative. The WCAG 3 task force has gone through multiple iterations — at times replacing APCA with alternative proposals (Visual Contrast Algorithm, others) and then re-adopting APCA. As of 2026-04, APCA is the lead candidate, but the final WCAG 3.0 contrast method is not frozen.
- **Tool support.** Chrome DevTools and several contrast checkers (including Colour Contrast Analyser) now offer APCA alongside 2.x ratios. Automated scanners (axe, Pa11y) still run on 2.x by default.
- **Legal status.** No jurisdiction currently enforces APCA. All compliance audits still use 2.x.

**Practitioner posture for 2026.**
- **Conform to WCAG 2.2 (SC 1.4.3 AA)** for audits, procurement, and legal defensibility.
- **Use APCA as an internal secondary check** — especially for dark-mode designs where 2.x under-penalises, and for thin-weight type where 2.x over-permits.
- **Flag APCA failures as design smells** even when 2.x passes.

**Cross-link:** `../../expert-color/references/apca.md` — the deep APCA primer with the Lc table and pair-design recipes.

### Visual contrast guidelines reframing (WCAG 3.0)

Beyond APCA, WCAG 3.0 drafts reframe contrast as one of several **readability outcomes**:
- **Text Contrast** — APCA-based.
- **Non-text Contrast** — adjacent-color discrimination, expanded from 2.x's 1.4.11.
- **Readable Text** — outcome combining contrast, size, line-height, measure, and language complexity.
- **Customizable Text** — user can override type styling (analogous to 1.4.12 but broader).

The shift is from **per-SC binary passes** to **outcomes the content must achieve**. A page could satisfy "Readable Text" through multiple routes: higher APCA, shorter measure, larger size, or more generous line-height. This mirrors the real trade-offs designers already make; it is also what makes WCAG 3.0 harder to mechanically audit.

### Status of WCAG 3.0 in 2026

- **Not normative.** Working Draft.
- **No certification path.** No conformance claim can be made against WCAG 3.0.
- **Active development.** The AG Working Group publishes updates roughly quarterly.
- **Expect several more years.** The gap between first Working Draft (2021) and a Candidate Recommendation is already 5 years; a W3C Recommendation would likely be 2027 at the earliest, more realistically 2028–2029 given the outcomes model's testability challenges.

---

## Part 3 — EU Web Accessibility Directive and the European Accessibility Act 2025

### Directive 2016/2102 (Web Accessibility Directive) — public sector

In force since 2016; required EU member states to transpose by 2018. Applies to **public-sector bodies** — national, regional, local government, hospitals, universities, public broadcasters.

- Applies to websites (from 2019) and mobile apps (from 2021).
- Requires **EN 301 549** conformance, which in turn references **WCAG 2.1 AA** (being updated to 2.2 via EN 301 549 v3.2.1, expected rollout 2024–2026).
- Requires an **accessibility statement** on each covered site.

### European Accessibility Act — Directive (EU) 2019/882

Often just "the EAA". Transposition deadline was **2022-06-28**; **most requirements in force 2025-06-28**.

**Scope (far broader than the 2016 directive).** Private-sector products and services including:
- E-commerce
- Banking services
- E-books and reading software
- Passenger transport services (ticketing, websites, apps)
- Telecommunications services
- Audiovisual media services (consumer-facing)
- ATMs, ticketing machines, self-service terminals

**Conformance reference.** EAA articles reference functional accessibility requirements; in practice the harmonised standard is again **EN 301 549**, which references **WCAG 2.1 AA** (transitioning to 2.2).

**Exemptions.** Microenterprises (<10 employees, <€2M turnover) supplying services are exempt. "Disproportionate burden" clauses exist but are subject to national oversight.

**Enforcement.** National market-surveillance authorities in each member state. Italy, Germany, France, Spain have active bodies.

### Italy / Germany: WCAG-adjacent case law or enforcement (2024–2026)

Relatively little case law specifically on typography — enforcement actions tend to cite broad non-conformance rather than individual SCs. A few landmark items:

- **Germany: BFIT-Bund** — the federal monitoring body published periodic reports under the 2016 directive, naming non-conforming public-sector sites. Typography-related findings (small font sizes, insufficient contrast) routinely appear in monitoring reports. No notable 2024–2026 *court* case centered on type.
- **Italy: AgID** — Agenzia per l'Italia Digitale is the monitoring body. In 2024–2025, enforcement focused on banking and e-commerce readiness for the EAA 2025 deadline. Typography-related corrective orders (contrast, resize) have been issued but not litigated to appeal.
- **Spain: UNE-EN 301 549** is directly incorporated; Cerm'ax-type rulings are pending. No landmark judgments specific to type.
- **France: Défenseur des droits** — the ombudsman has issued recommendations under RGAA (the French WCAG transposition). Enforcement remains largely administrative.

**Honest read.** WCAG-type case law is thin in civil-law Europe because most enforcement is administrative and settles before adjudication. US ADA litigation (under Title III) is where public case law on web accessibility is thickest — but US courts generally defer to WCAG 2.x AA as the industry standard without relitigating individual SCs.

---

## Part 4 — Testing protocols

### What automated tools catch and miss

**axe / axe-core (Deque), Pa11y, Lighthouse, WAVE.**

| Type-related SC | Caught by automated tools? |
|---|---|
| 1.4.3 Contrast | Yes — but only for simple cases (solid bg, simple fg); fails on gradient/image backgrounds, `color-mix()`, `currentColor` chains |
| 1.4.4 Resize | Partially — flags absolute units; can't verify functional preservation |
| 1.4.10 Reflow | No — requires viewport-sized DOM traversal, not standard |
| 1.4.12 Text Spacing | No — requires applying the override and re-rendering |
| 1.4.8 Visual Presentation | No — requires judgment on block-level text decisions |
| 3.1.5 Reading Level | Partial — some tools run F-K on content |
| 2.5.8 Target Size | Yes — bounding-box check |
| 2.4.11 Focus Not Obscured | No — requires interaction |
| Images of text | Sometimes — OCR-based detection |

**Takeaway.** Automated tools catch ~30–40% of real WCAG violations (this is a widely cited figure from Deque's own research-survey). The rest requires manual review and user testing. For typography specifically, automation handles the contrast numerics and nothing else.

### Manual testing protocol for type

A **20-minute checklist** per page:

1. **200% zoom test** (SC 1.4.4). In Firefox, enable "Zoom Text Only" (View → Zoom → Zoom Text Only), then Ctrl-+ to 200%. Walk every major flow. Note clipping, overlap, lost functionality.
2. **400% viewport zoom test** (SC 1.4.10). In Chrome DevTools, set viewport to 1280 × 800, zoom to 400% (effective viewport ~320 CSS px). Verify no horizontal page-level scroll except in exempt content.
3. **Text-spacing override** (SC 1.4.12). Apply the WCAG text-spacing bookmarklet (Steve Faulkner's or Adrian Roselli's). Scroll every major section. Note clipping, overflow.
4. **Contrast sweep** (SC 1.4.3). Run axe or a similar checker. Log passes and fails. Spot-check with a human eye — any text that *looks* faint, measure it manually.
5. **Disable CSS** (progressive-enhancement sanity). Firefox View → Page Style → No Style. Content should remain readable and structured (this is an A-level concern under 1.3.1 but catches type-as-image surprises).
6. **Tab through interactive elements** (SC 2.4.7 / 2.4.11 / 2.4.13). Every focus indicator visible, not obscured, 3:1 contrast, ≥2px perimeter.
7. **Read a paragraph aloud.** Rough check on reading level and sentence rhythm. Formulaic check if needed.
8. **Font-size audit.** Is body at least **16px** (or 1rem with a 16px root)? Smaller than 14px is a smell regardless of SC compliance.
9. **Measure check.** Is any prose block wider than **80 characters per line**? Is any narrower than **~45**?
10. **Line-height check.** Body line-height should be ≥1.4; 1.5 for longer passages. Headlines can drop to 1.1–1.2.

### User testing with low-vision and dyslexic participants

Automated and heuristic checks miss the *feel* of reading. For any product where reading is the primary task, a user-testing round with:

- **Low-vision participants** (AMD, diabetic retinopathy, uncorrected refractive error). Tests screen magnification interaction, contrast at 200–400% zoom, feedback from real assistive-tech chains (ZoomText, Windows Magnifier, macOS Zoom).
- **Dyslexic participants.** See [dyslexia.md](./dyslexia.md) for the full evidence base. Brief summary: they benefit most from generous spacing, clear sans-serif, shorter measures — not from dyslexia-specific fonts.
- **Screen-reader users.** Not "typography" per se, but text structure (headings, lists, lang attributes) is read aloud and determines whether the text is navigable.

A recruiting-friendly approach: **Fable**, **UserTesting with accessibility filters**, or the local Blind Association (in Italy, UICI; in Germany, DBSV). Budget: 5–8 participants per round is sufficient for pattern discovery.

---

## Part 5 — Reading-level tooling

### Formula survey

| Formula | Inputs | Output | Works on |
|---|---|---|---|
| **Flesch-Kincaid Grade Level** | Words/sentence, syllables/word | US grade | English (fair), localised variants exist |
| **Flesch Reading Ease** | Same as F-K | 0–100 score | English |
| **Dale-Chall** | Familiar-word ratio, sentence length | US grade | English |
| **SMOG** | Polysyllable count over 30 sentences | Years of education | English |
| **Gunning Fog** | Long words, sentence length | US grade | English |
| **LIX** | Long-word ratio | Readability index | Scandinavian, German (adapted) |
| **Wiener Sachtextformel** | Long words, long sentences, mono-syllables | Austrian school grade | German |
| **Fernández Huerta** | F-K adapted | Spanish scale | Spanish |
| **Lix-J (Japanese)** | Kanji density, sentence length | Grade | Japanese |

**All formulas are proxies.** They correlate roughly with perceived difficulty on the populations they were fitted to (often 20th-century schoolchildren on printed-text corpora). They do not measure comprehension.

### Practical tooling

- **Hemingway Editor** — desktop app and web. Flags adverbs, passive voice, complex sentences. Grade reading in real time.
- **Readable.io** — API-driven; batch-analyses URLs; outputs F-K, Dale-Chall, SMOG, etc.
- **Grammarly Premium** — passive voice and clarity hints; not an F-K reporter by default.
- **Microsoft Word / Google Docs** — enable via "Proofing" / "Review" options.
- **`textstat` Python library** — for build-pipeline integration.
- **LanguageTool** — open-source, multi-language; grammar-focused but includes readability metrics.

### Limitations to always disclose

1. **Language-specific formulas are rare outside English.** Translating content and running F-K on the translation is not reliable.
2. **Domain vocabulary skews scores.** "HIV-negative" reads as hard; "bro" reads as easy. Neither reflects actual comprehension burden.
3. **Sentence length is a weak proxy for complexity.** A chain of short sentences can be opaque ("The box is the thing. The thing is the box. The box thinks.") and a long sentence with clear structure can be accessible.
4. **No formula captures typography.** Dense small-type set in a justified paragraph at 800 CPL is harder than the same content at 65 CPL, 1.5 line-height. SC 3.1.5 speaks only to the linguistic layer.

The defensible practice: use formulas as a **sanity backstop**, not as a target. Write for the audience, review with the audience, and measure with the formula only to catch drift.

---

## Part 6 — Implementation recipes in CSS/HTML

### Relative units (SC 1.4.4 Resize)

```css
:root {
  /* 16px anchor — respects user's browser default */
  font-size: 100%;
}

body {
  /* Inherit root; scale with user setting */
  font-size: 1rem;
  line-height: 1.5;
}

h1 { font-size: 2rem; }    /* 32px at default */
h2 { font-size: 1.5rem; }  /* 24px at default */

.caption {
  font-size: 0.875rem;     /* ≈14px — edge of legible */
}
```

Avoid `font-size: 14px`, `font-size: 10pt` — these resist text-only zoom in stricter interpretations of 1.4.4.

### `lang` attribute (SC 3.1.1 / screen-reader correctness / reading-level tools)

```html
<html lang="en-GB">
  <!-- ... -->
  <blockquote lang="it">
    Il linguaggio è il vestito del pensiero.
  </blockquote>
</html>
```

`lang` is required at the root (`html`) and should be updated at any block containing content in another language. Screen readers use it to select the right voice and pronunciation; reading-level tools use it to pick the right formula.

### Avoiding justified prose (SC 1.4.8)

```css
article p {
  text-align: start;     /* logical — respects RTL */
  hyphens: auto;         /* allowed even if not justified */
  text-wrap: pretty;     /* modern: balances ragged edge */
}
```

`text-wrap: pretty` (Chrome 117+, Safari 17.4+) improves the ragged edge on left-aligned prose by avoiding orphans and runty last lines — more sophisticated than `balance`, which is better for short headings.

### Measure cap (SC 1.4.8, and general readability)

```css
.prose {
  max-width: 65ch;       /* ~65 characters per line */
  margin-inline: auto;
}

.prose-wide {
  max-width: 80ch;       /* WCAG 1.4.8 ceiling */
}
```

`ch` is the advance width of `0` in the current font; it's an approximation, and varies by typeface (a wide monospace gives a different `ch` than a narrow sans). For precise CPL, combine with `font-size-adjust` to normalise x-height.

### Line-height inheritance (SC 1.4.12 compatibility)

```css
/* Good — unitless inherits as a multiplier */
body { line-height: 1.5; }

/* Bad — fixed px line-height doesn't scale with font-size override */
body { line-height: 24px; }
```

Unitless line-heights cascade by multiplying the descendant's own font-size. Fixed-value line-heights (px, em) inherit as computed values and break when children have different sizes.

### `text-spacing-trim` (modern, 2024+)

```css
:root {
  text-spacing-trim: trim-start;  /* Chinese/Japanese punctuation trim */
}
```

Not a WCAG SC directly, but relevant for CJK: trims redundant half-width space around CJK punctuation. Improves CPL compliance in CJK where SC 1.4.8 halves the measure to 40.

### Minimum target size (SC 2.5.8)

```css
.text-link-button {
  /* Text-sized link with expanded hit area */
  position: relative;
  padding-block: 0.125em;  /* visual spacing */
}

.text-link-button::before {
  content: "";
  position: absolute;
  inset: -0.5em;           /* hit-area expansion */
}
```

Keeps visual footprint tight while exposing a ≥24 × 24 CSS px target.

### Skip-link for reading-long-content (2.4.1)

```html
<a href="#main" class="skip-link">Skip to main content</a>
```

```css
.skip-link {
  position: absolute;
  inset-inline-start: 1rem;
  inset-block-start: 1rem;
  transform: translateY(-200%);
  transition: transform 120ms;
}

.skip-link:focus {
  transform: translateY(0);
}
```

Not a type SC, but cheap and expected on any long-form surface.

---

## Anti-patterns

- **`font-size: 12px` on body text.** Fails the 16px practical floor; fails text-only zoom intent.
- **`height: 40px; line-height: 40px;` buttons.** Fails SC 1.4.12 the moment line-height is overridden.
- **`overflow: hidden` on text containers without `min-height`.** Catastrophic under text-spacing override.
- **`color: #ccc` on `#fff`.** 1.61:1 — fails AA for any body text.
- **Using `px` for all font-sizes.** Unnecessarily fragile under user scaling; unnecessary given `rem` is universally supported.
- **`text-align: justify` on body prose without a hyphenation engine.** Rivers, irregular spacing, SC 1.4.8 failure.
- **`width: 1200px` containers without `max-width: 100%`.** Breaks SC 1.4.10 reflow at 320 CSS px.
- **Shipping headlines as SVG/PNG without live-text fallback.** SC 1.4.5 failure; loses zoom, selection, copy, translate.
- **Claiming WCAG 3.0 conformance.** Not a valid claim — WCAG 3.0 is a Working Draft.
- **Using APCA as your only contrast check for 2026 audits.** Auditors check 2.x ratios. APCA is a supplement, not a replacement — yet.
- **Reading-level tools as a target.** Chasing F-K 8 rewrites can flatten prose without improving comprehension. Write for humans; measure to catch drift.
- **No `lang` attribute on the root.** Silent SC 3.1.1 failure; breaks screen-reader voice selection and confuses reading-level tools.
- **`line-height: 18px` on body.** Fixed-value line-height breaks inheritance and override compliance.
- **Hiding focus rings** (`outline: none` without a replacement). Breaks 2.4.11 / 2.4.13 and orphan users of keyboard navigation.
- **Disabling browser zoom via `<meta viewport user-scalable=no>`.** Mobile platforms used to honour this; most now ignore it. Still: flagged as a 1.4.4 failure pattern.

---

## Sources

- **W3C. "Web Content Accessibility Guidelines (WCAG) 2.2" (2023).** Recommendation. https://www.w3.org/TR/WCAG22/
- **W3C. "Understanding WCAG 2.2."** https://www.w3.org/WAI/WCAG22/Understanding/
- **W3C. "Techniques for WCAG 2.2."** https://www.w3.org/WAI/WCAG22/Techniques/
- **W3C. "W3C Accessibility Guidelines (WCAG) 3.0" Working Draft.** https://www.w3.org/TR/wcag-3.0/
- **W3C. "WCAG 3 Introduction."** https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/
- **Somers, A. "APCA — Accessible Perceptual Contrast Algorithm."** Myndex Research. https://apcacontrast.com/ and https://readtech.org/ARC/
- **Somers, A. "APCA Readability Criterion (ARC)."** https://readtech.org/ARC/tests/
- **EUR-Lex. "Directive (EU) 2019/882 — European Accessibility Act."** https://eur-lex.europa.eu/eli/dir/2019/882/oj
- **EUR-Lex. "Directive (EU) 2016/2102 — Web Accessibility Directive."** https://eur-lex.europa.eu/eli/dir/2016/2102/oj
- **ETSI EN 301 549** "Accessibility requirements for ICT products and services" v3.2.1.
- **Roselli, A. "Text Spacing Bookmarklet."** https://adrianroselli.com/
- **Faulkner, S. "WCAG 1.4.12 Text Spacing Bookmarklet."** https://www.tpgi.com/
- **Deque Systems. "Automated Accessibility Testing: What Can It Catch?"** research-survey note; industry figure of ~30–40% automated coverage.
- **DuBay, W. H. (2004). "The Principles of Readability."** Impact Information. Overview of Flesch, Dale-Chall, and SMOG.
- **Bringhurst, R. "The Elements of Typographic Style"** — on the 45–75 CPL rule. Hartley & Marks, various editions.
- **BFIT-Bund (Germany).** https://www.bfit-bund.de/ — federal monitoring body reports.
- **AgID (Italy).** https://www.agid.gov.it/ — monitoring and enforcement under the 2016 directive.
- **Silktide / Level Access / Deque blogs** — practitioner guidance on 2.2 SC interpretation and APCA adoption.
- **Peer file**: [dyslexia.md](./dyslexia.md) — dyslexia-specific typographic interventions.
- **Peer files in `expert-color`**: `../../expert-color/references/contrast.md` and `../../expert-color/references/apca.md` — numerical contrast models, pair design, ramp construction.
