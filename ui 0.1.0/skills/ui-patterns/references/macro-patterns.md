# Macro patterns — page templates and shells

The shell archetypes (productivity-shell, saas-dashboard, marketing-site, mobile-app) are realized
as ASCII wireframes in this pack's `references/archetype-*.md` (applied to concrete screens by
`layout-decompose`) — this file carries the **page templates** that live inside a shell. Each entry: anatomy → when it fits → the failure it invites.

## master-detail
Two panes: a scannable collection (list/table/tree) + a detail surface for the selection.
- **Anatomy:** list pane (search/filter on top, items below) · detail pane (header: identity +
  actions; body: content) · selection state binds them.
- **Fits:** mail, CRM records, admin consoles, file browsers — any "many items, work on one" job.
- **Variants:** list-detail (detail replaces list on narrow viewports — the responsive collapse);
  three-pane (folders → list → detail, e.g. mail); detail-as-drawer (transient inspection).
- **Failure:** selection amnesia — navigating back loses scroll/selection; or the detail pane
  duplicating list actions until the two panes fight over ownership of the verb.

## canvas + inspector
One dominant work surface + property panels framing it (the productivity-shell's page-level form).
- **Anatomy:** canvas (the artifact) · left pane (structure/layers/palette) · right pane (properties
  of the current selection) · toolbar (mode/verb switching) · command palette for the long tail.
- **Fits:** editors of any artifact — design tools, IDEs, DAWs, node graphs.
- **Failure:** inspector sprawl — properties for *everything* rather than *the selection*; verbs
  hidden in menus that belong on the selection (context menu / floating toolbar).

## wizard / stepper
A linear multi-step flow with one decision per screen and explicit progress.
- **Anatomy:** step indicator (numbered, labeled) · one step's form per screen · back/next (next is
  primary; back never loses data) · review step before commit.
- **Fits:** infrequent, high-consequence, or dependency-ordered tasks — onboarding, checkout, setup.
- **Failure:** wizard abuse — chopping a 5-field form into 5 screens (friction without protection);
  or steps that can't be revisited, turning validation errors into restarts.

## settings
Grouped preference panes: category navigation + a form pane per category.
- **Anatomy:** category nav (left or tabs; search above it at scale) · per-category form sections
  with headers · save model (instant-apply with undo, or explicit save per section — pick ONE
  product-wide) · dangerous zone isolated at the bottom.
- **Fits:** any preference surface past ~10 settings.
- **Failure:** mixed save models (some panes instant, some buffered) — the single most common
  settings defect; and burying the one setting users seek (no search, wrong category names).

## feed / timeline
A reverse-chronological or ranked stream of homogeneous-ish items.
- **Anatomy:** composer or filter header · item cards (identity · content · actions · timestamp) ·
  infinite scroll with a "new items" affordance · item-level overflow menu.
- **Fits:** activity, social, notifications, audit logs (chronological variant).
- **Failure:** scroll-position theft when new items prepend; unbounded item-card verb creep (every
  team adds a button until cards are toolbars).

## board (kanban)
Columns as workflow states, cards as work items, drag as the state-change verb.
- **Anatomy:** column headers with counts/WIP limits · cards (title + 2–3 metadata slots max) ·
  add-card affordance per column · card detail opens as overlay, not navigation.
- **Fits:** state-machine work where the *transition* is the primary verb.
- **Failure:** columns as categories rather than states (drag then means nothing); card metadata
  bloat that kills scannability.

## search results
Query refinement + a ranked result set.
- **Anatomy:** persistent query field (editable, not reset) · facet/filter rail with counts ·
  results with query-term highlighting · result-type sections when heterogeneous · zero-results
  state that offers corrections, never a dead end.
- **Failure:** filters that reset the query (or vice versa); facets without counts (blind filtering).

## doc-reader
A long-form content surface with orientation chrome.
- **Anatomy:** content column at readable measure (see typography-lettering) · sticky outline/TOC ·
  in-page anchors · prev/next at the bottom · breadcrumb identity above.
- **Failure:** full-width text (measure > ~90ch); TOC that doesn't track scroll position.

## chat / thread
A conversational exchange surface.
- **Anatomy:** message list (virtualized, anchored to bottom) · composer pinned bottom (grows, never
  scrolls away) · day/section separators · per-message actions on hover/long-press · thread/reply
  affordance where depth exists.
- **Failure:** scroll anchoring broken by async content (images loading shove the view); composer
  state lost on navigation.

## dashboard page
Covered as a shell in the saas-dashboard archetype (this pack's `references/`, applied by
layout-decompose); the page-level rule worth
repeating: a dashboard answers **3–7 questions, each with exactly one chart/stat that answers it** —
a grid of every available metric is a data dump, not a dashboard.

## Choosing between them
The template follows the **primary verb over the primary object**: work *on one of many* →
master-detail; *make an artifact* → canvas+inspector; *complete a task once* → wizard; *monitor* →
dashboard; *converse* → chat; *triage a stream* → feed; *advance work through states* → board.
When two verbs compete, the template serves the frequent one and the other gets a mode or overlay.
