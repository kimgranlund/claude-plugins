# Sources — provenance in trust order

Corpus first drafted 2026-07-15 directly against established HIG knowledge, THEN corrected the
same day by a dedicated research wave against live HIG pages (developer.apple.com/design/
human-interface-guidelines). This is the honest, current state after that correction — several
claims were downgraded from an implied-HIG-citation to explicitly [inferred]/ecosystem-convention
once the wave found no current, dedicated HIG page to cite. Re-run the wave for an axis when its
canon moves, or when a page this wave couldn't find gets located.

## Trust order

1. **Apple's own HIG, directly cited** (developer.apple.com/design/human-interface-guidelines) —
   confirmed for: the "Tab bars" page (navigation-vs-action framing, item-count guidance,
   overflow/More-tab behavior, tab-bar visibility rule) and the "Sheets" page (the scoped-task
   definition, and the critical modal-vs-nonmodal platform split this pack's first draft missed).
2. **Ecosystem/platform convention, explicitly marked [inferred]** — used for every claim the
   research wave could NOT locate a current, dedicated HIG page for (see the gap list below).
   These are widely-observed iOS/UIKit conventions this pack states as a reasonable design
   heuristic, never presented as "HIG says."

## What the 2026-07-15 research wave confirmed [verified]

- Tab bars: the navigation-not-actions framing, the "use a toolbar instead" split, the
  stay-visible-except-modal rule, the directional (not numeric) tabs-few guidance, and the
  More-tab overflow mechanism — all from HIG's own "Tab bars" page.
- Sheets: the scoped-task definition, and — the load-bearing correction — that a sheet is ALWAYS
  modal on macOS/tvOS/visionOS/watchOS but can be modal OR NONMODAL on iOS/iPadOS (HIG's own
  example: Notes' nonmodal text-formatting sheet).

## What the wave could NOT find a current HIG page for (kept as [inferred], not silently asserted)

- **Sheet detents** (medium/large resting heights, the grabber affordance) — this is UIKit
  (`UISheetPresentationController`) API documentation, not a page found on the HIG site itself
  under that name.
- **Alerts vs. action sheets** as a distinct escalation ladder — the "Sheets" page does not cover
  alerts or action sheets; no separate current HIG page for either was found.
- **Button style vocabulary** (plain/tinted/filled) — no dedicated current HIG "Buttons" page
  with this vocabulary was found.
- **Grouped vs. plain lists, and swipe-action leading/trailing conventions** — no dedicated
  current HIG page for either was found.
- **Detailed nav-bar anatomy and the large-title collapse behavior** — only the toolbar-vs-tab-bar
  split is directly HIG-cited (from the "Tab bars" page); the rest of navigation-bar composition
  is ecosystem convention here, not independently re-confirmed against a dedicated page.
- **Search placement in a navigation hierarchy** — no dedicated current HIG page found.

## Known unverified edges — the standing caveat

Every item in the gap list above is a real, disclosed hole in this pack's grounding, not a
temporary placeholder — if a future wave locates any of these pages, promote the claim to
[verified] with the URL and access date in the SAME change that removes the [inferred] tag,
per this workspace's amend-in-place discipline (never silently rewrite; a dated note records
the correction).
