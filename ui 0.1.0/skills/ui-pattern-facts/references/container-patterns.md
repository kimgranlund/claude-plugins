# Container patterns — the Header · Body · Footer anatomy

Researched 2026-07-15 (NN/g, Designing Interfaces 3rd ed., Material Design 3 component
conventions — see `sources.md`). Same shape as `micro-patterns.md`: anatomy → behavior contract →
the failure it invites. This file answers what a bounded content container (card, panel, dialog,
drawer, sheet) puts in each of its three zones; `micro-patterns.md`'s "overlays" entry answers
WHICH container (dialog vs drawer vs popover) to reach for in the first place — load that one for
the choice, this one for the anatomy once chosen.

## card / panel — the base shape

- **Anatomy:** a **Header** (title, optionally an icon/avatar, optionally a close or overflow-menu
  action) · a **Body** (the content proper — a feed, a form, plain text, media) · a **Footer**
  (contextual actions, a status/system note, or both). Not every card carries all three — a
  content-only card (an image tile, a stat) has no header or footer; the anatomy names the slots a
  RICHER card fills, not a mandatory checklist.
- **Contract — the Header:** carries identity (what this is) and escape (how to close/collapse it)
  when the container is dismissible; an icon in the header signals category or state, never
  decoration alone. Headers are commonly **sticky** relative to the body when the body scrolls
  independently — the header stays the fixed anchor a user orients by while content moves under it.
- **Contract — the Body:** owns its own scroll region when content can exceed the container's
  available height; the header and footer stay pinned outside that scroll boundary so identity and
  actions remain reachable regardless of scroll position. A body with no independent scroll region
  forces the WHOLE container (and often the page behind it) to scroll to reach a footer action —
  the single most common container defect (see Failure, below).
- **Contract — the Footer:** the action zone — primary action right/bottom-aligned, secondary
  action beside it (never stacked as visually equal weight — see `micro-patterns.md`'s form
  entry for the same primary/destructive-separation rule), a system note (status, last-saved,
  a count) left-aligned when both share the footer. House lock (ruled 2026-07-16, Issue #9):
  always exactly `1` visually-prominent action per footer/action group; never `2`+ equal-weight
  primaries (the user is left to guess which action matters — two primaries signal none), never
  `0` where the container poses a decision (an undecidable modal) — an inline-commit (autosave)
  container poses no footer decision, so the `0` clause doesn't fire there. *Exception: a read-only
  container's status-only footer has zero actions by design — that is the status-bar sentence that follows in this entry,
  not a violation.* A footer with only a system note and no
  actions is a status bar, not a dead footer — still worth the fixed zone so it doesn't scroll
  away with the body.
- **Failure:** an unreachable footer (buttons scroll out of view because the body has no own
  scroll boundary — the container scrolls as one block instead); a header that grows with content
  (a subtitle or breadcrumb pushes the close button around instead of staying fixed height); a
  footer with two-plus actions of equal visual weight (no primary signaled).

## dialog / sheet — the same anatomy, modal contract layered on top

- **Anatomy:** identical three zones, with the Header's close affordance now load-bearing (Escape
  = the header's close action) and the Footer's primary action named for the consequence
  ("Delete 3 files", never "OK" — the same naming rule `micro-patterns.md`'s overlay entry states
  for the dialog's primary button).
- **Contract:** the Body is where a dialog most often violates the pattern — a dialog authored for
  a short confirmation, then grown to hold a whole settings form, without ever giving the Body its
  own scroll region; the Header and Footer were never re-checked for the taller content.
- **Failure:** the same unreachable-footer defect as the base card, but worse in a modal — the user
  cannot dismiss by scrolling away from it, so a stuck footer with no visible primary action can
  strand the whole flow.

## drawer — the base anatomy, but the Footer is often optional

- **Anatomy:** Header (title + close, since a drawer is dismissible by definition) · Body
  (inspection/edit content, scrollable independent of the page behind it) · Footer, OPTIONAL —
  many drawers commit changes inline (autosave, blur-commit per `micro-patterns.md`'s form entry)
  and never need a persistent action zone at all.
- **Contract:** when a drawer DOES carry a footer (a multi-field edit form with an explicit
  Save/Cancel pair rather than autosave), the same pinned-footer contract applies as the card — the
  footer stays reachable regardless of body scroll position.
- **Failure:** a drawer with both autosave AND a stale "Save" button in the footer — two save
  models on one surface (the same mixed-save-model failure `ui-pattern-facts`' own macro `Consult
  procedure` example names for the settings template, recurring here at the module level).

## nested containers — don't double the chrome

- **Contract:** a card inside a card (a list-item card inside a page-level card, a summary panel
  inside a dashboard widget) should drop the INNER container's header/footer chrome unless the
  inner item genuinely needs its own dismiss/action zone — two headers stacked (the outer card's
  title bar directly above an inner card's near-identical title bar) reads as one container
  wrapping a decoration, not two distinct things.
- **Failure:** "card-in-a-card" — visually redundant nesting where the inner boundary adds no
  information the outer one didn't already give, just doubled padding and a second faint border.
  (The *spacing* math of that doubled padding — why two same-scale insets compose additively
  rather than collapsing — is `size-and-shape-rules`' `composable-spacing.md`; this file names the
  chrome-redundancy defect, not the spacing arithmetic behind it.)

## Boundary

This file names container anatomy and its failure modes. WHICH container to reach for (dialog vs
drawer vs sheet vs popover) is `micro-patterns.md`'s "overlays" entry; the geometry math behind
composed padding at nested boundaries is `size-and-shape-rules`; building the container as a real
component is `make-component`; placing it within a page's region map is `break-down-layout`.
