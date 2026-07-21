# Buttons, lists, and swipe actions

Researched 2026-07-15; amended 2026-07-15 (first wave downgraded everything to [inferred] after
finding no dedicated HIG pages); amended again 2026-07-15 (second wave, Issue #6) — targeted
page-hunting FOUND current HIG pages for buttons and lists that the first wave missed, so this
file now carries a real per-section split: lists promoted to [verified], buttons grounded on a
real page with a disclosed vocabulary mismatch, swipe actions confirmed absent from HIG and kept
[inferred]. See `sources.md`.

## Button style vocabulary [inferred vocabulary, verified page — see note]

[The HIG "Buttons" page EXISTS and is current
(developer.apple.com/design/human-interface-guidelines/buttons, accessed 2026-07-15) — but it
does NOT use the plain/tinted/filled vocabulary. HIG's own terms are **Style** ("a visual style
based on size, color, and shape"; "use a prominent button style" to draw attention; "use style —
not size — to visually distinguish the preferred choice") and **Role** (Normal, Primary, Cancel,
Destructive) as a separate semantic layer. The plain/tinted/filled ladder below remains
ecosystem/UIKit convention (`UIButton.Configuration`), kept [inferred].]

Ecosystem/platform convention frames button styles along a visual-weight spectrum — plain
text-only (lowest weight, for lower-priority or repeated actions), tinted (colored text/icon, no
fill, more present than plain but still light), filled/prominent (solid background fill, the
heaviest weight, reserved for a screen's single primary action). The commonly-observed guiding
rule: **one filled/prominent action per screen or contextual grouping** — more than one defeats
the purpose of signaling which action matters most; none leaves the user to guess. This rule IS
HIG-aligned: the Buttons page's prominent-style and style-not-size guidance carries the same
intent under its own vocabulary.

## Primary vs. secondary action placement [inferred]

The primary action conventionally gets the heavier visual weight and the most reachable/default
position for the context; secondary/cancel actions use a visually lighter style so they read as
clearly subordinate — the same "one primary, clearly marked" rule `ui-pattern-facts`' own footer
conventions state at the cross-platform level. [The HIG Buttons page's Role layer (Primary,
Cancel, Destructive) is adjacent grounding for the semantics, but the placement guidance itself
remains convention.]

## Grouped vs. plain lists [verified, HIG "Lists and tables" — promoted 2026-07-15]

[Promoted from [inferred]: developer.apple.com/design/human-interface-guidelines/lists-and-tables,
accessed 2026-07-15 — its Style section explicitly names the **grouped list**, states that "some
styles use visual details to help communicate grouping and hierarchy or to provide specific
experiences", and directs "choose a table or list style that coordinates with your data and
platform"; API realizations linked from the page: SwiftUI `ListStyle`, UIKit
`UIListContentConfiguration`.]

A grouped list visually clusters related rows into sections with visible separation; a plain list
runs rows edge-to-edge with minimal section chrome. Group when rows fall into distinct categories
worth separating (a Settings screen's sections); keep plain for a single homogeneous collection
where grouping would add visual noise without adding real category information.

## Swipe actions — leading vs. trailing [inferred — absence CONFIRMED by the 2026-07-15 second wave]

[The second wave searched the Lists and tables page (no mention of swipe actions or
leading/trailing placement), the Gestures page, and targeted site queries — no current HIG page
covers swipe-action conventions. This is now a confirmed absence, not an unsearched gap.]

List rows commonly support swipe-revealed actions on either edge, with a widely-observed
convention assigning different intent per side: **trailing swipe** (from the right) for
DESTRUCTIVE/negative actions (delete, archive) — the more commonly used, more discoverable side;
**leading swipe** (from the left) for affirmative/status-changing, non-destructive actions (mark
as read/unread, flag, pin) — a secondary, less-expected gesture reserved for actions without
data-loss risk.

**The failure this explains:** putting a destructive action behind the less-expected leading
swipe increases the chance of an unsafe-feeling accidental discovery-and-tap; burying a
frequently-used non-destructive action behind the edge users associate with delete has the
opposite problem.

## What this file cannot yet cite

After the 2026-07-15 second wave, the remaining convention-level claims are: the
plain/tinted/filled VOCABULARY (the Buttons page exists but standardizes Style/Role instead),
primary/secondary placement, and the swipe-action side conventions (confirmed absent from HIG).
These are disclosed gaps, stated as directional convention — never as "HIG says."
