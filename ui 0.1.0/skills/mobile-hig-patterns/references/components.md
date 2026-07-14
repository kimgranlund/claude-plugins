# Buttons, lists, and swipe actions

Researched 2026-07-15; amended 2026-07-15 — a dedicated research wave against live HIG pages
found no dedicated, current HIG page for button-style vocabulary, list grouping, or swipe-action
conventions specifically. Everything below is downgraded to [inferred]/ecosystem convention
rather than presented as a direct HIG citation; re-run the wave if a specific HIG page for any of
these is later found. See `sources.md`.

## Button style vocabulary [inferred — no dedicated current HIG page found this wave]

Ecosystem/platform convention frames button styles along a visual-weight spectrum — plain
text-only (lowest weight, for lower-priority or repeated actions), tinted (colored text/icon, no
fill, more present than plain but still light), filled/prominent (solid background fill, the
heaviest weight, reserved for a screen's single primary action). The commonly-observed guiding
rule: **one filled/prominent action per screen or contextual grouping** — more than one defeats
the purpose of signaling which action matters most; none leaves the user to guess.

## Primary vs. secondary action placement [inferred]

The primary action conventionally gets the heavier visual weight and the most reachable/default
position for the context; secondary/cancel actions use a visually lighter style so they read as
clearly subordinate — the same "one primary, clearly marked" rule `ui-patterns`' own footer
conventions state at the cross-platform level.

## Grouped vs. plain lists [inferred — no dedicated current HIG page found this wave]

A grouped list visually clusters related rows into sections with visible separation; a plain list
runs rows edge-to-edge with minimal section chrome. Commonly-observed guidance: group when rows
fall into distinct categories worth separating (a Settings screen's sections); keep plain for a
single homogeneous collection where grouping would add visual noise without adding real category
information.

## Swipe actions — leading vs. trailing [inferred — no dedicated current HIG page found this wave]

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

Everything in this file is convention-level, not a confirmed HIG citation — a genuine gap this
pack discloses rather than papering over. If a dedicated current HIG page for buttons, lists, or
swipe gestures is found in a later wave, promote the relevant claims to [verified] with the page
URL and access date; until then, treat this file's claims as directional, not authoritative.
