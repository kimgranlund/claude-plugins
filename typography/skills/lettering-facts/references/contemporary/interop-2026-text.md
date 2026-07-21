---
date: 2026-04-26
coverage: light
peers:
  - ./css-text-properties.md
  - ./custom-highlights-api.md
  - ./font-delivery.md
primary_sources:
  - https://web.dev/blog/interop-2026
  - https://wpt.fyi/interop-2026
  - https://github.com/web-platform-tests/interop
---

# Interop 2026 — Typography-Relevant Picks

Interop 2026 was published 2026-02-12. It is the annual cross-browser interop priority list, jointly committed by Apple, Google, Mozilla, Microsoft, and Bocoup. The picks below are the typography-relevant items.

## Typography-relevant 2026 priorities

- **Custom Highlights API** — `Highlight` registry + `::highlight()` pseudo-element. Lets authors style arbitrary `Range` objects without DOM markup. See [`custom-highlights-api.md`](./custom-highlights-api.md). Big win for spell-check, search-highlight, annotation, and collaborative-editing presence cursors.
- **`attr()` typed function** — typography uses include pulling label width into CSS, expressing variable-font axis values per element, and threading dataset-typed values into `font-variation-settings`.
- **`contrast-color()`** — typography use is auto-readable text on arbitrary surfaces. Returns black or white only (the algorithm is intentionally unspecified). For richer contrast logic see the expert-color skill's APCA references.

## Carryover watchlist (still progressing)

These were Interop 2024-2025 priorities that have shipped partially or remain works-in-progress:

- **`text-box-trim` / `text-box-edge`** — Chrome 133+ (Feb 2025), Safari 18.2+ (Dec 2024); **Firefox unshipped** (Bugzilla 1816038). Watch for Firefox progress through 2026.
- **COLRv1 in WebKit** — Chrome 98+, Firefox 107+, **Safari unshipped through 26.5**. WebKit standards-positions #415 still open. Not a 2026 Interop priority — likely a 2027 candidate.

## What did NOT make 2026

- **`hanging-punctuation`** beyond its current Safari-only state.
- **`text-spacing-trim`** values beyond `space-all` / `normal` (`trim-both`, `trim-all`, `auto` all unimplemented anywhere).
- **`initial-letter`** full-spec implementation.
- **`font-variant-emoji`** in Safari (Firefox shipped in 141; Safari has it disabled by default in 17.5+).

## Why this file exists

Interop priorities reshape what's worth designing for in any given year. A feature on the Interop list is a feature all four browser engines have committed to driving toward interop — typography work that depends on those features can plan for "shipping by year end" with reasonable confidence. Features absent from Interop are unlikely to reach cross-browser interop within the year regardless of any single engine's progress.

For the current year's priorities, see [web.dev/blog/interop-2026](https://web.dev/blog/interop-2026) and the live scoreboard at [wpt.fyi/interop-2026](https://wpt.fyi/interop-2026).

## Sources

- [web.dev: Interop 2026 (2026-02-12)](https://web.dev/blog/interop-2026)
- [wpt.fyi: Interop 2026 scoreboard](https://wpt.fyi/interop-2026)
- [github.com/web-platform-tests/interop](https://github.com/web-platform-tests/interop) — process repo
- [caniuse: text-box-trim](https://caniuse.com/css-text-box-trim)
- [Bugzilla 1816038 — Firefox text-box-trim](https://bugzilla.mozilla.org/show_bug.cgi?id=1816038)
- [WebKit standards-positions #415 — COLRv1](https://github.com/WebKit/standards-positions/issues/415)
