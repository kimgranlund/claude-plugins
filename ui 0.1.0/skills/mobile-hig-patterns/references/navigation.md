# Navigation — tab bars, navigation stacks, and placement

Researched 2026-07-15; amended 2026-07-15 with a dedicated research wave's findings against live
HIG pages — the Tab Bars section below is now directly cited; sections the wave could not find a
current HIG page for are marked [inferred] rather than presented as HIG's own stated rule. See
`sources.md` for the full verified/inferred split.

## Tab bars — verified against HIG's own "Tab bars" page

[verified] "A tab bar lets people navigate between top-level sections of your app." Tab bars help
people understand the different types of information or functionality an app provides and let
them quickly switch between sections while PRESERVING each section's own navigation state. (HIG,
"Tab bars" — developer.apple.com/design/human-interface-guidelines/tab-bars, accessed 2026-07-14.)

[verified] "Use a tab bar to support navigation, not to provide actions. Use a toolbar instead for
controls that act on elements in the current view." This is HIG's own stated separation between
the two zones — a tab bar is for MOVING, a toolbar is for DOING. (HIG, "Tab bars" — accessed
2026-07-14.)

[verified] The tab bar should stay visible when navigating between sections; the one named
exception is a modal view covering it, "because a modal is temporary and self-contained." (HIG,
"Tab bars" — accessed 2026-07-14.)

[verified] On tab-bar item count, HIG's own wording is directional rather than a hard number:
"Use the appropriate number of tabs required to help people navigate your app. It's generally
easier to navigate among fewer tabs." For apps with a complex information structure, HIG suggests
considering "a sidebar or a tab bar that adapts to a sidebar" as an alternative. **Correction
(2026-07-15):** this file previously called out only that HIG "leans toward keeping tabs few" —
the wave confirms this is HIG's actual phrasing (directional, no fixed ceiling stated), so no
specific number should ever be attributed to HIG as a rule. (HIG, "Tab bars" — accessed
2026-07-14.)

[verified] On overflow, HIG names the exact mechanism: when horizontal space limits visible tabs,
the trailing tab becomes a **More** tab revealing the rest in a separate list — and HIG frames
this as a cost to minimize ("harder for people to reach and notice content on hidden tabs"), not a
first-choice pattern. (HIG, "Tab bars" — accessed 2026-07-14.)

## Navigation stacks (push/pop, "drill-down")

[inferred — general iOS/UIKit navigation-model convention; this wave did not find or confirm a
single current HIG page dedicated to navigation-stack semantics the way "Tab bars" is dedicated
and citable.] A navigation stack presents a HIERARCHY — each pushed screen is a child of the one
before it, reachable only by drilling in, and the back button/edge-swipe returns exactly one level
up. Appropriate for content with real parent-child structure, where tab-bar-style peer navigation
doesn't apply because the destinations aren't equally-ranked siblings.

**The failure this explains:** using tabs for what is actually a linear drill-down (flattening
hierarchy into a peer list loses the "how did I get here" context a stack's back button
preserves), or using a stack for what is actually peer content (forcing users to back out through
screens that were never really "above" each other).

## Nav bar, toolbar, and the large-title collapse

[verified, partial] HIG's own "Tab bars" page confirms the toolbar/tab-bar split directly:
"[If you need to provide] controls that act on elements in the current view, use a toolbar
instead" of a tab bar. (HIG, "Tab bars" — accessed 2026-07-14.)

[inferred — the large-title collapse behavior and the specific "title/back-button/trailing-
actions" nav-bar anatomy below were NOT independently re-confirmed against a current, dedicated
HIG page in this wave; treat as widely-observed iOS convention, not a cited HIG rule, until a
specific page is found.] The navigation bar hosts the screen's title, the automatic back button,
and trailing actions specific to the current screen; a large title (oversized, left-aligned) is
commonly documented as collapsing to a smaller, centered inline title as the user scrolls content
below it.

## Search placement in a navigation hierarchy

[inferred — NOT found on a current, dedicated HIG page in this wave; treat as ecosystem
convention, not a cited HIG rule.] Search is commonly integrated into the navigation bar of the
screen it searches (rather than a dedicated separate search screen/tab) for content naturally
scoped to that screen's list; a dedicated search TAB is reserved for apps where search is itself a
primary, first-class destination.
