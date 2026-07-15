# Sources — provenance in trust order

Corpus first drafted 2026-07-15 against established HIG knowledge; corrected the same day by a
first research wave (which downgraded several claims to [inferred] after finding no pages); then
re-verified 2026-07-15 by a second, targeted page-location wave (Issue #6) that FOUND current HIG
pages for four of the six gap areas — the first wave had under-searched (it missed pages
reachable directly by slug: /alerts, /action-sheets, /buttons, /lists-and-tables, /search-fields,
and the detent/grabber anatomy on the /sheets page itself). Promotions were applied in the same
change as this note, per the amend-in-place discipline. Re-run a wave for an axis when its canon
moves.

## Trust order

1. **Apple's own HIG, directly cited** (developer.apple.com/design/human-interface-guidelines) —
   see the [verified] list below; every entry carries its page and access date at the claim site.
2. **Ecosystem/platform convention, explicitly marked [inferred]** — used only for the claims in
   the confirmed-gap list below: widely-observed iOS/UIKit conventions stated as design
   heuristics, never presented as "HIG says."

## What is [verified] against live HIG pages (access dates at the claim sites)

- **Tab bars** (first wave, 2026-07-14): navigation-not-actions framing, the toolbar split, the
  stay-visible-except-modal rule, directional tabs-few guidance, More-tab overflow — "Tab bars".
- **Sheets** (first wave, 2026-07-14): the scoped-task definition and the modal-vs-nonmodal
  platform split (always modal on macOS/tvOS/visionOS/watchOS; modal OR nonmodal on iOS/iPadOS).
- **Sheet detents + grabber** (second wave, 2026-07-15): the Sheets page's Anatomy section names
  detents (large automatic, medium opt-in) and the grabber, with design guidance — "Sheets".
- **Alerts vs. action sheets** (second wave, 2026-07-15): both exist as dedicated current pages;
  the escalation distinction is HIG's own sentence ("Use an action sheet — not an alert — to
  offer choices related to an intentional action") — "Alerts", "Action sheets".
- **Grouped vs. plain lists** (second wave, 2026-07-15): the Style section names the grouped
  list and the choose-by-data-and-platform rule — "Lists and tables".
- **Search placement** (second wave, 2026-07-15): the "Search in a navigation hierarchy" section
  names the three placements (tab / toolbar / inline) and the choice criteria — "Search fields".

## Confirmed gaps — kept [inferred] after TWO waves (absence verified, not just unsearched)

- **Button style vocabulary (plain/tinted/filled)** — the HIG "Buttons" page EXISTS (found by the
  second wave) but standardizes different vocabulary: **Style** (visual weight, "prominent") and
  **Role** (Normal/Primary/Cancel/Destructive). The plain/tinted/filled ladder is UIKit
  (`UIButton.Configuration`) / ecosystem convention; the pack discloses the mismatch at the claim
  site and keeps the vocabulary [inferred] while citing the page for the underlying
  one-prominent-action intent.
- **Swipe-action leading/trailing conventions** — no current HIG page; the Lists and tables page
  does not mention swipe actions; targeted searches empty. Ecosystem convention, disclosed.
- **Nav-bar anatomy and the large-title collapse** — no dedicated "Navigation bars" page exists
  (direct slug 404s; the Navigation-and-search hub does not list one); the large-title collapse
  appears on no current HIG page. Ecosystem convention, disclosed.

## Known unverified edges — the standing caveat

Every confirmed-gap item above is a real, disclosed hole in the current HIG, not a temporary
placeholder — if a future wave (or a HIG update) surfaces any of these as a dedicated page,
promote the claim to [verified] with the URL and access date in the SAME change that removes the
[inferred] tag, with a dated note recording the correction (never a silent rewrite). Full
research ledgers for both waves are recorded in the repo's Issue #6 (git-native Findings).
