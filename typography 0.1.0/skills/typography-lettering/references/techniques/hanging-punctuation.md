---
date: 2026-04-18
coverage: light
peers:
  - ../contemporary/css-text-properties.md
  - ./measure.md
  - ./figures.md
  - ./small-caps.md
primary_sources:
  - https://drafts.csswg.org/css-text-4/#hanging-punctuation-property
  - https://www.w3.org/TR/css-text-3/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation
  - https://caniuse.com/css-hanging-punctuation
  - https://chromestatus.com/feature/5692933251497984
  - https://bugs.chromium.org/p/chromium/issues/detail?id=41425321
  - https://bugzilla.mozilla.org/show_bug.cgi?id=1253615
  - https://practicaltypography.com/hanging-quotes.html
  - https://webtypography.net/2.1.7
  - https://adactio.com/journal/21027
  - https://clagnut.com/blog/2445
  - https://css-tricks.com/almanac/properties/h/hanging-punctuation/
  - https://www.pagedjs.org/
  - https://www.princexml.com/
notes:
  - This file is the practitioner reference for the `hanging-punctuation` property. Full coverage of the CSS Text L3/L4 property surface is in `../contemporary/css-text-properties.md` §`hanging-punctuation`; this file goes deeper on the decade-long browser-support stall, manual workarounds, and editorial rationale.
---

# Hanging punctuation — technique reference

**Coverage tier**: light
**Last verified**: 2026-04-18
**Sources**: W3C CSS Text Module Level 3 and Level 4 (ED, 2026), MDN `hanging-punctuation` (retrieved 2026-04-18), caniuse 2026-04, Bringhurst *Elements of Typographic Style* 4e, Butterick *Practical Typography* §hanging quotes, Rutter *Web Typography* §2.1.7, Chromium issue tracker, Mozilla Bugzilla.
**Peer files**: `../contemporary/css-text-properties.md`, `./measure.md`, `./figures.md`, `./small-caps.md`.

Covers the `hanging-punctuation` CSS property, its specification history, the long-running cross-browser-support stall, manual techniques for non-supporting browsers, and the editorial contexts where the effect is worth the effort. Out of scope: the broader CSS Text property surface (see `../contemporary/css-text-properties.md`); measure and line-length tradeoffs (see `./measure.md`).

---

## What Hanging Punctuation Is

In traditional letterpress typography, punctuation marks at the start or end of a line — opening quotation marks, closing periods and commas, em-dashes, hyphens — are set slightly outside the body's text block, so that the *visible* left and right edges of the text align with the body lettering rather than with the punctuation. A paragraph that opens with a quotation mark has the quote hanging to the left of the margin; the first letter of the actual text sits flush with every other line's first letter. Closing periods and commas at the right edge of a justified column hang out into the right margin so the last word's rightmost letter aligns with the column edge.

The effect is editorial polish: a prose block that starts with a quote doesn't gain a visible indent from the quote glyph's width; justified columns look cleaner at the right edge because the stops and commas don't interrupt the flush rectangle. Bringhurst's formulation (*Elements of Typographic Style*, Ch. 5 §3): the appearance of justification is weakened unless punctuation is hung into the margin. Jan Tschichold and other early-20th-century book designers treated hanging punctuation as a required move for fine book typesetting; most of the canonical book designs from the Renaissance through the 20th century hang their opening quotes in printed editions.

On the web, this effect has been specified in CSS Text Module Level 3 since approximately 2012, has been implemented in Safari since 2016, and has *not* been implemented in either Chromium or Firefox as of April 2026 — a decade-long stall that is among the longest-running CSS interoperability gaps.

---

## The CSS Property

```
hanging-punctuation = none | [ first || [ force-end | allow-end ] || last ]
```

### Values

- `none` — the default. No hanging.
- `first` — opening punctuation at the start of a line hangs outside the line's inline-start edge. Applies to opening quotation marks (`"` U+0022, `'` U+0027, `"` U+201C, `'` U+2018, `«` U+00AB, `„` U+201E, and the Unicode open-bracket / open-paren classes).
- `last` — closing punctuation at the end of a line hangs outside the line's inline-end edge. Specified; **unimplemented in every engine** as of 2026-04.
- `allow-end` — closing punctuation at the end of a line *may* hang outside the inline-end edge if it fits within the margin without requiring rewrapping. Applies to full-stops and commas; the browser decides case-by-case whether to hang or include in the line's word-break calculation.
- `force-end` — closing punctuation at the end of a line *always* hangs, even if the wrapping algorithm must adjust the rest of the line to accommodate.

Multiple values can combine: `hanging-punctuation: first force-end` hangs opening punctuation at the start and forces closing punctuation to hang at the end.

### What it applies to

Per spec, the property applies to block containers and lets text inside them break lines with punctuation hung outside. The punctuation characters that are eligible for hanging are a Unicode-derived list: opening quotes, closing quotes, stops, commas, opening and closing brackets, and a few related classes. The exact list is in CSS Text 4 Appendix A.

---

## Browser Support (2026-04)

| Engine | Support | Since | Notes |
|---|---|---|---|
| **Safari (WebKit)** | Partial | macOS Safari 10 (2016-09), iOS 10 | Supports `first`, `allow-end`, `force-end`. Does **not** support `last`. No browser does. |
| **Chrome / Chromium (Blink)** | **Unsupported** | — | No stable build has ever shipped `hanging-punctuation`. Chromium issue #41425321 open since 2016; *Intent to Prototype* filed mid-2025. Named in the Interop 2026 focus areas. |
| **Edge (Chromium)** | **Unsupported** | — | Follows Blink. |
| **Firefox (Gecko)** | **Unsupported** | — | Bugzilla #1253615 open since 2016. No public roadmap as of April 2026. |
| **Samsung Internet** | **Unsupported** | — | Follows Blink. |

**Global support:** approximately 18% (caniuse, 2026-04 snapshot) — Safari desktop and iOS Safari only.

**The shape of the stall.** `hanging-punctuation` appeared in CSS Text Level 3 drafts around 2011–2012. WebKit implemented the partial set (everything except `last`) in Safari 10, shipped September 2016. In the nine-plus years since, neither Blink nor Gecko has implemented it. This is the longest-running Safari-only typography property — longer than any other prose-rendering gap. The Chromium `Intent to Prototype` filed in mid-2025 is the first movement on that side since the issue opened. The Mozilla bug remains unscheduled.

**Reasons commonly cited** for the long stall: interaction with bidirectional (RTL) and CJK layout edge cases, the complex Unicode character-class lookup that must run at line-break time, and the perceived low priority against the backlog of other CSS Text features. The counter-argument — voiced by Richard Rutter, Jeremy Keith, and others in the typography community — is that "decade-long" is not "hard"; other engines have had time.

**Safari's partial implementation remains the only path** for now. A site that targets Chromium or Firefox for primary traffic and treats Safari as secondary will see no hanging punctuation in production. A site that lives in a Safari-heavy audience (iOS app webviews, macOS editorial publications) can ship `hanging-punctuation: first` and see real effect for the majority of readers.

---

## Usage

### Basic

```css
article p {
  hanging-punctuation: first;
}
```

Opening quotes at the start of a paragraph hang outside the inline-start edge. The first letter of actual text aligns with every other line's first letter. No effect in Chromium or Firefox; full effect in Safari.

### Justified with closing-punctuation hanging

```css
.justified {
  text-align: justify;
  hanging-punctuation: first allow-end;
}
```

`allow-end` lets closing periods and commas hang at the right edge *if* hanging doesn't force rewrapping. In justified text, this reduces the amount of word-spacing stretch the browser must apply — a hung period takes less horizontal space from the line, so adjacent word-spaces don't need to expand as much to justify. Net: less visible gappiness in justified columns.

### Forcing closing hang

```css
.editorial {
  hanging-punctuation: first force-end;
}
```

`force-end` always hangs, even if the line must be rewrapped to accommodate. More aggressive than `allow-end`; use in editorial contexts where hanging is the design intent.

### Interaction with `text-indent`

Hanging punctuation and `text-indent` both affect the first-line appearance. Setting both can produce compounded or conflicting results — the indent shifts the text right, the hanging quote shifts punctuation left of the margin. Test visually. Bringhurst-tradition book typesetting uses hanging punctuation *without* first-line indent on the opening paragraph, and *with* first-line indent on subsequent paragraphs (where the opening quote is unlikely to occur).

### Interaction with `text-wrap: pretty`

`text-wrap: pretty` (see `../contemporary/css-text-properties.md`) is a broader line-break polish feature; hanging punctuation is a sub-feature focused on edge-alignment. Combining both in the same engine is fine — `pretty` does line-break optimization, `hanging-punctuation` does edge glyph positioning. They are orthogonal.

---

## Manual Workarounds for Non-Supporting Browsers

When cross-browser consistency matters more than the editorial polish, none of the options below are truly equivalent — they approximate.

### Negative first-line `text-indent`

```css
article p {
  text-indent: -0.45em;
}
```

Pulls the first character of the paragraph left into the margin. Works for opening quotation marks specifically, as long as the quote character is the first character. Measurements vary by quote style: `"` U+201C around 0.35–0.45em; `"` U+0022 around 0.30em; `«` U+00AB around 0.55em.

**Limits:** works only for the *very first character* of the paragraph — any text before the quote (an opening tag, a whitespace, a small-cap first word) shifts the offset. Only pulls the first line — cannot help closing punctuation at the end of every line. Fragile across font changes because the character width depends on the font.

### CSS containment with `::first-letter`

```css
article p::first-letter {
  margin-left: -0.4em;
}
```

Similar effect via `::first-letter` pseudo-element. `::first-letter` has longstanding support but the `margin-left` negative shift is the real technique; semantics are identical to the `text-indent` approach.

### Inline span with negative margin

```html
<p><span class="hang">"</span>The opening quote goes here...</p>
```

```css
.hang { margin-left: -0.4em; }
```

Explicit. Requires authoring the span; not retrofit-safe. Adaptable per character (different offset for `"` vs `«`). Works cross-browser. The labor cost is the blocker at scale.

### JavaScript text-measuring libraries

Projects like `hanging-punctuation.js` (small polyfills, various authors) measure the first character of each paragraph and apply a calculated negative offset. Precise across fonts because the offset is measured, not guessed. Heavyweight: adds script to the critical path and recalculates on resize. Rarely worth it outside high-craft editorial projects.

### CSS Houdini Layout API

In principle, a custom layout worklet using the CSS Houdini Layout API Level 2 could implement hanging punctuation on non-Safari browsers. In practice, Layout API Level 2 has **not shipped in any stable browser** as of April 2026 — the API is still being specified, and even in Chromium's experimental builds it has been demoted from the active work queue. Not a viable production option.

### The accept-the-degradation option

The most common production stance: ship `hanging-punctuation: first` for Safari users and accept that Chromium and Firefox users see the slight indent of an opening quote. The effect is subtle enough that most readers do not consciously notice; the effort required to achieve cross-browser parity is disproportionate for most projects.

---

## Quote Character Choices

Hanging works best with directional "smart" quotes:

- **English:** `"` U+201C (opening), `"` U+201D (closing), `'` U+2018, `'` U+2019.
- **French:** `«` U+00AB, `»` U+00BB (with thin-space padding inside by convention).
- **German:** `„` U+201E (opening, below baseline), `"` U+201C (closing).
- **Russian:** `«` U+00AB, `»` U+00BB in literary typesetting, `„` / `"` in typewriter tradition.
- **Japanese:** `「` U+300C, `」` U+300D full-width brackets. Hanging them has different conventions — see `../scripts/japanese.md`.
- **Chinese:** `「` / `」` traditional, `"` U+201C / `"` U+201D simplified. Cross-refer `../scripts/cjk-han.md`.

**Straight quotes (`"` U+0022, `'` U+0027)** exist as characters but are typographic placeholders used in code, not in edited prose. They can hang (Safari's implementation applies to the Unicode "Pi" / "Pf" quote classes, which include straight quotes), but the visual effect is less convincing because the glyph is symmetric and doesn't read as directional punctuation.

---

## When Hanging Punctuation Is Worth the Effort

### Where it matters

- **Long-form editorial** — New Yorker-style digital magazines, literary journals, personal essay sites. The reader is on the page for minutes and notices micro-typography.
- **Quote-heavy articles** — interviews, book reviews, history writing where block-quoted passages are common. Opening quotes on every block benefit from hanging.
- **Pull-quotes and block-quotes** — these are explicitly designed objects where visual edge alignment is part of the design language. Hanging removes the "quote-shaped indent" from the layout.
- **Traditional book design** — digital editions of books; paged-CSS output (see below). Hanging is a readership expectation in this genre.
- **Justified text blocks** — right-edge hanging reduces gappiness, improves the justified rectangle.

### Where it doesn't

- **Dashboards, forms, data tables, administrative UI** — punctuation is rare, and the reader is scanning rather than reading continuously. Hanging adds no value.
- **Social-feed-style content** — posts are short, readers scroll fast. Micro-typography below the resolution of attention.
- **Chat and messaging** — bubbles, variable widths, no continuity between messages. Hanging is meaningless.
- **Marketing landing pages** — large display type rarely hits the wrap boundary where hanging matters.

### Paged-CSS output

Paged-CSS tools — **Paged.js** (open-source), **Prince** (commercial), **Vivliostyle** — which generate print-quality PDF from HTML + CSS, generally support `hanging-punctuation` in their rendering engines. If you're producing a book-like PDF from HTML, `hanging-punctuation: first allow-end` will be honored by these tools. Paged-CSS output is where the property delivers the most visible value, because the output is a fixed page where edge alignment is load-bearing and the reader has classical-typography expectations.

---

## Accessibility

No accessibility implication. Screen readers ignore layout — the DOM text is the same whether the opening quote hangs or not. Text selection works through hung characters normally in every engine (Safari included). WCAG 2.2 has no SC that targets hanging punctuation.

Printed output from the browser's print CSS: Safari's `hanging-punctuation` applies to paginated output too, so printing a Safari page with hanging enabled produces a paginated PDF with hung quotes. Chromium and Firefox, having no implementation at all, produce no hanging in print either.

---

## Common Traps

- **Relying on `last`.** Specified in the CSS Text L3/L4 property grammar; implemented in *no engine*, including Safari. Do not author `hanging-punctuation: last` expecting any effect. Use `force-end` (Safari only) for closing-punctuation hanging.
- **Expecting cross-browser consistency.** The property works only in Safari (as of 2026-04). Authoring a design that *depends* on hanging across browsers will fail outside Safari — the punctuation will sit inside the margin as normal.
- **Conflicts with `text-indent`.** Setting both `text-indent: 1em` and `hanging-punctuation: first` produces compounded first-line effects: the quote hangs left of the margin, but the non-quote text is still indented. In Safari. In Chromium and Firefox, just the indent. Usually not what you want for book-style paragraphs; pick one or commit to testing both engines.
- **Using `hanging-punctuation: allow-end` without `text-align: justify`.** `allow-end` is primarily valuable when justification is active — it's the interaction that reduces visible word-space stretch. On ragged-right text, the end-of-line punctuation hangs (in Safari), but there's no justification benefit; the effect is cosmetic only.
- **Forgetting that `hanging-punctuation` is progressive enhancement.** Ship it, know it works only in Safari, accept that the fallback is fine. Non-supporting browsers render the paragraph without hanging; nothing visibly breaks. This is one of the safest opt-in typography features in CSS — there is no negative case.
- **Combining with hand-rolled negative `text-indent`.** If you set both `text-indent: -0.45em` (as a manual workaround) and `hanging-punctuation: first` (for Safari), Safari compounds them — the quote shifts left of the margin *and* the first-line text shifts, producing a double-indent that wasn't intended. Gate one branch behind `@supports (hanging-punctuation: first)`:

  ```css
  @supports not (hanging-punctuation: first) {
    article p { text-indent: -0.45em; }
  }
  @supports (hanging-punctuation: first) {
    article p { hanging-punctuation: first; }
  }
  ```

---

## Value Judgment

For most web UI: not worth doing. The effort-to-effect ratio is poor — only Safari users see the effect at all, and the visual improvement is subtle. Skip.

For editorial long-form: worth doing as progressive enhancement. `hanging-punctuation: first` is one line of CSS; Safari users get the book-grade polish; Chromium and Firefox users see no change. There is no cost.

For paged-CSS book output: worth the effort. Paged.js and Prince honor the property, and book-grade output is where hanging punctuation materially improves the reading experience. Spend the time.

For cross-browser parity at scale: not worth doing with manual workarounds. The negative `text-indent` hack works for the first character only and fragiles on font changes. JavaScript text-measuring libraries are heavy. Accept the asymmetry until Chromium and Firefox ship.

---

## Sources

- W3C CSS Working Group. "CSS Text Module Level 3." [w3.org/TR/css-text-3](https://www.w3.org/TR/css-text-3/) — original specification of `hanging-punctuation`. Retrieved 2026-04-18.
- W3C CSS Working Group. "CSS Text Module Level 4." Editor's Draft. [drafts.csswg.org/css-text-4/#hanging-punctuation-property](https://drafts.csswg.org/css-text-4/#hanging-punctuation-property). Retrieved 2026-04-18.
- MDN Web Docs. "hanging-punctuation." [developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation](https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation). Retrieved 2026-04-18.
- caniuse.com. "CSS hanging-punctuation." [caniuse.com/css-hanging-punctuation](https://caniuse.com/css-hanging-punctuation). 2026-04 snapshot.
- Chromium Issue Tracker. #41425321 "Implement `hanging-punctuation`." (Formerly Chromium bug 41425321.) Open since 2016; *Intent to Prototype* filed mid-2025.
- Mozilla Bugzilla. #1253615 "Implement CSS `hanging-punctuation`." Open since 2016.
- ChromeStatus.com. "hanging-punctuation." [chromestatus.com/feature/5692933251497984](https://chromestatus.com/feature/5692933251497984). Retrieved 2026-04-18.
- Butterick, M. *Practical Typography* — "Hanging quotes." [practicaltypography.com/hanging-quotes.html](https://practicaltypography.com/hanging-quotes.html). Retrieved 2026-04-18.
- Richard Rutter. *Web Typography* §2.1.7 — "Hanging punctuation." [webtypography.net/2.1.7](https://webtypography.net/2.1.7). Retrieved 2026-04-18.
- Richard Rutter. "Interop 2026 typography requests." [clagnut.com/blog/2445](https://clagnut.com/blog/2445). Retrieved 2026-04-18.
- Jeremy Keith. "Hanging punctuation in CSS." [adactio.com/journal/21027](https://adactio.com/journal/21027). Retrieved 2026-04-18.
- Bringhurst, R. *The Elements of Typographic Style*, 4th edition. Hartley & Marks, 2013. (Chapter 5 §3 on hanging punctuation; Chapter 2 on justification.)
- Paged.js. [pagedjs.org](https://www.pagedjs.org/). Retrieved 2026-04-18.
- PrinceXML. [princexml.com](https://www.princexml.com/). Retrieved 2026-04-18.
- CSS-Tricks Almanac. "hanging-punctuation." [css-tricks.com/almanac/properties/h/hanging-punctuation](https://css-tricks.com/almanac/properties/h/hanging-punctuation/). Retrieved 2026-04-18.
