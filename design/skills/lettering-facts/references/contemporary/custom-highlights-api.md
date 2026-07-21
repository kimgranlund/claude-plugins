---
date: 2026-04-26
coverage: medium
peers:
  - ./css-text-properties.md
  - ./interop-2026-text.md
primary_sources:
  - https://drafts.csswg.org/css-highlight-api-1/
  - https://developer.mozilla.org/en-US/docs/Web/API/Highlight
  - https://developer.mozilla.org/en-US/docs/Web/CSS/::highlight
  - https://developer.chrome.com/articles/css-custom-highlight-api/
---

# Custom Highlights API

A web platform API for styling arbitrary text ranges *without DOM markup*. Author registers a `Highlight`, populates it with `Range` objects, styles via `::highlight(name)` — text is highlighted across the document with no DOM mutation.

## What it is

```js
// 1. Create Range objects pointing at text to highlight
const range = new Range();
range.setStart(node, startOffset);
range.setEnd(node, endOffset);

// 2. Build a Highlight from those ranges
const searchHighlight = new Highlight(range);

// 3. Register it under a name
CSS.highlights.set("search", searchHighlight);
```

```css
/* 4. Style by name */
::highlight(search) {
  background-color: yellow;
  color: black;
}
```

The text covered by `range` is highlighted with the rule. No `<mark>`, no wrapper spans, no DOM mutation, no layout shift.

## Why it matters

Pre-Highlights API, the only way to style arbitrary text ranges was to insert DOM elements (e.g. `<mark>`) wrapping the text. This:

- Mutates DOM unrelated to content (semantically lying about structure).
- Triggers layout/paint and risks breaking selection / cursor position.
- Compounds badly for overlapping highlights (search + spell-check + collaborative cursors all wrapping the same text).
- Loses fidelity at element boundaries (`<mark>` can't span across blocks).

The Custom Highlights API moves highlighting into a parallel "presentation" layer the browser owns. DOM stays untouched. Multiple highlights can overlap. Block boundaries are no obstacle.

## Browser support

Custom Highlights API is part of **Interop 2026** — the four major engines have committed to driving toward cross-browser interop in 2026. As of April 2026: Chrome / Edge shipped (105+), Safari 17.2+, Firefox 140+. Verify current state at [caniuse: ::highlight()](https://caniuse.com/mdn-css_selectors_highlight).

## Typography use cases

- **Search highlighting** — find-in-page, document search, real-time keystroke matching.
- **Spell-check / grammar-check UI** — drawing wavy underlines or color overlays without inserting markup.
- **Annotation rendering** — third-party annotation tools (Hypothesis, Highlights.so) can mark passages without tampering with publisher DOM.
- **Collaborative editing presence** — multi-user cursors and selection ranges rendered without DOM contention between clients.
- **Reading-progress visualization** — fade or color text by scroll position without wrapping every paragraph.
- **Code-editor-style decorations** — diagnostics, errors, lint warnings without injecting `<span>` per token.

## Limitations

- **`::highlight()` cannot style every property.** Spec restricts which CSS properties apply — `background-color`, `color`, `text-decoration*`, `text-shadow`, `text-emphasis*`, and a few others. Layout-affecting properties are excluded by design.
- **`Highlight` is not stylable per-range.** A single `Highlight` styled via `::highlight(name)` applies the same rule to every range it contains. For per-range styling, register multiple `Highlight`s.
- **`Highlight.priority`** controls overlap order — higher priority renders on top of lower for overlapping ranges.
- **Ranges are live but the highlight is not auto-maintained.** If DOM changes invalidate a range, the highlight follows the range's behavior — generally collapses to nothing rather than throwing.
- **Cannot capture pointer events directly.** `::highlight()` is a paint-only pseudo-element — for click-to-act-on-highlight UX, you still need a custom event layer.

## Comparison vs. `::selection` and `<mark>`

| | `::selection` | `<mark>` element | Custom Highlights API |
|---|---|---|---|
| DOM mutation | None (browser-owned) | Yes (wrapper element) | None (parallel registry) |
| Number of distinct styled ranges | One (the user's selection) | Unlimited (one per element) | Unlimited (one per Highlight + Range) |
| Per-range styling | No | Yes (per element) | Yes (per Highlight) |
| Overlap handling | N/A | Manual (split ranges) | Native (`priority`) |
| Property coverage | Limited spec list | All CSS | Limited spec list (similar to `::selection`) |

## Pattern: search-highlight implementation

```js
const searchHighlight = new Highlight();
CSS.highlights.set("search", searchHighlight);

function updateHighlights(query) {
  searchHighlight.clear();
  if (!query) return;

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const text = node.textContent;
    let i = 0;
    while ((i = text.indexOf(query, i)) !== -1) {
      const range = new Range();
      range.setStart(node, i);
      range.setEnd(node, i + query.length);
      searchHighlight.add(range);
      i += query.length;
    }
  }
}
```

```css
::highlight(search) {
  background-color: oklch(80% 0.18 90); /* warm yellow */
  color: black;
}
```

Pre-API, this required wrapping every match in a `<span>` — destructive to existing inline elements, layout-shifting, and brittle.

## Sources

- [W3C drafts.csswg.org: CSS Custom Highlight API Module Level 1](https://drafts.csswg.org/css-highlight-api-1/)
- [MDN: Highlight](https://developer.mozilla.org/en-US/docs/Web/API/Highlight)
- [MDN: ::highlight()](https://developer.mozilla.org/en-US/docs/Web/CSS/::highlight)
- [Chrome for Developers: CSS Custom Highlight API](https://developer.chrome.com/articles/css-custom-highlight-api/)
- [caniuse: ::highlight()](https://caniuse.com/mdn-css_selectors_highlight)
