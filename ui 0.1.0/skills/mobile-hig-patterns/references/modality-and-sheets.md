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

[inferred — NOT found on a current HIG page in this wave.] "Detent" is UIKit
(`UISheetPresentationController`) API terminology for a sheet's resting heights (commonly a
**medium** and a **large** detent) with a drag-to-resize **grabber** affordance — this is
FRAMEWORK documentation, not confirmed HIG guidance under that name. Treat "detent" as the
correct technical term for the mechanism, but do not cite it as "HIG says" without a HIG page to
point at — this wave found none. See `sources.md`.

## Alerts vs. action sheets vs. sheets — the escalation ladder

[inferred — NOT independently confirmed against a current HIG page in this wave; the "Sheets"
page does not itself cover alerts or action sheets.] The escalation logic below is ecosystem
convention this pack states as a reasonable, widely-observed pattern, not a verified HIG citation:

- **Alert:** the most interruptive, reserved for critical information or a decision the user must
  make before doing anything else — conventionally minimal text (a short title, an optional short
  message) and few actions.
- **Action sheet:** presents a set of two or more choices related to the current context, typically
  sliding up from the bottom — appropriate when the user needs to choose AMONG options rather than
  simply acknowledge information the way an alert does.
- **Sheet** (per the corrected definition above): the right escalation when the task needs real
  content and interaction (a form, a multi-field composer) rather than a short choice or a pure
  acknowledgment.

**The failure this explains (still a reasonable design heuristic, even where not HIG-cited):**
reaching for a full sheet for a simple binary confirmation over-engineers the interruption;
reaching for an alert to hold real interactive content starves that content of the space it needs.
