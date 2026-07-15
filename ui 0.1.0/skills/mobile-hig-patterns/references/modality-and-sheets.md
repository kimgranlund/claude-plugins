# Modality, sheets, and detents

Researched 2026-07-15; amended 2026-07-15 after a dedicated research wave against live HIG pages
found this file's original draft had generalized past what the current site actually states in
two places — corrected in place per this workspace's grounding discipline (the wrong claim is
struck and replaced with a dated note, not silently rewritten). See `sources.md` for the full
verified/inferred split.

## What "modality" means in HIG's own framing — and the modal/nonmodal split this file first missed

[verified] HIG defines a sheet as a technique that "helps people perform a scoped task closely
related to their current context," presenting content in a dedicated mode. (HIG, "Sheets" —
developer.apple.com/design/human-interface-guidelines/sheets, accessed 2026-07-14.)

[verified] **Correction (2026-07-15):** this file originally treated every sheet as modal-with-
partial-visibility. HIG's own platform split is narrower and more specific than that: on **macOS,
tvOS, visionOS, and watchOS a sheet is ALWAYS modal** — it prevents interaction with the parent
view until dismissed. On **iOS and iPadOS a sheet can be either modal OR NONMODAL** — a nonmodal
sheet lets the person use its functionality to affect the parent view WITHOUT dismissing the
sheet first (HIG's own example: Notes on iPhone/iPad uses a nonmodal sheet so text-formatting
options can be applied to a selection while the note stays live and editable behind/around it).
(HIG, "Sheets" — accessed 2026-07-14.) This is the load-bearing fact the original draft lacked:
"is this sheet modal" is a real per-platform, per-use-case question HIG itself splits on, not a
given.

**The failure this explains:** assuming a sheet always blocks the parent view (true on
macOS/tvOS/visionOS/watchOS, not guaranteed on iOS/iPadOS) — an iOS sheet built as if it were
unconditionally modal may fight against a design that actually wants live, nonmodal interaction
with the content behind it.

## Full-screen modal vs. sheet vs. popover

- **Full-screen modal:** covers the entire screen, used for a self-contained task substantial
  enough to warrant the user's complete attention (e.g. a multi-step composer) — the heaviest form
  of interruption in this family. [inferred — general ecosystem convention; HIG's own "Sheets"
  page does not itself name a separate "full-screen modal" pattern by that exact term, see
  `sources.md`.]
- **Sheet:** [verified, HIG "Sheets"] "useful for requesting specific information from people or
  presenting a simple task that they can complete before returning to the parent view" — and
  whether it blocks that parent view depends on the platform/modal-vs-nonmodal split above, not a
  single fixed behavior.
- **Popover:** a transient, anchored presentation (pointing at the control that triggered it,
  typically on larger/regular-width layouts) for lighter-weight content. [inferred — general
  ecosystem/platform convention; not independently confirmed against a current HIG page in this
  wave, see `sources.md`.]

## Sheet detents

[verified, HIG "Sheets" — promoted 2026-07-15 from [inferred]; the second wave found this on the
Sheets page's own Anatomy section, which the first wave missed:
developer.apple.com/design/human-interface-guidelines/sheets, accessed 2026-07-15.] A sheet's
resting heights are **detents** — HIG's own term, not just UIKit's: "Sheets automatically support
the large detent"; adding the **medium** detent lets the sheet rest at a lower height for
progressive disclosure. A resizable sheet expands when people scroll its contents or drag the
**grabber** — "a small horizontal bar" — and HIG's guidance is to include a grabber in a
resizable sheet. The API realization is `UISheetPresentationController.detents` /
`prefersGrabberVisible` (linked from the HIG page itself).

## Alerts vs. action sheets vs. sheets — the escalation ladder

[verified, HIG "Alerts" + "Action sheets" — promoted 2026-07-15 from [inferred]; the second wave
found both as current, dedicated pages the first wave missed:
developer.apple.com/design/human-interface-guidelines/alerts and …/action-sheets, both accessed
2026-07-15. The distinction is HIG's own words: "Use an action sheet — not an alert — to offer
choices related to an intentional action" (Alerts page, linking to Action sheets).]

- **Alert:** [verified] "gives people critical information they need right away" — the most
  interruptive form, used sparingly, for information to acknowledge or a decision that can't wait;
  conventionally minimal text (a short title, an optional short message) and few actions.
- **Action sheet:** [verified] "a modal view that presents choices related to an action people
  initiate" — appropriate when the user needs to choose AMONG options rather than simply
  acknowledge information the way an alert does.
- **Sheet** (per the corrected definition above): the right escalation when the task needs real
  content and interaction (a form, a multi-field composer) rather than a short choice or a pure
  acknowledgment.

**The failure this explains (still a reasonable design heuristic, even where not HIG-cited):**
reaching for a full sheet for a simple binary confirmation over-engineers the interruption;
reaching for an alert to hold real interactive content starves that content of the space it needs.
