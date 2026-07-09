# Micro patterns — the module catalog

Each entry: anatomy → behavior contract → the failure it invites. Building any of these as a
component routes to `component-forge`; their interaction invariants route to the verifier family.

## data table
- **Anatomy:** column headers (sortable marked, sorted indicated) · rows · selection column ·
  row-level overflow menu · toolbar (bulk actions, appear on selection) · footer (pagination or
  count) · column controls (show/hide, resize, pin) at scale.
- **Contract:** sort is single-column by default, stable, indicated with direction; filters compose
  with AND across columns and show as removable chips; bulk actions operate on the *filtered*
  selection and confirm scope ("all 240 matching" vs "12 on this page" — the classic trap);
  inline edit commits on blur/Enter with per-cell validation; empty-after-filter ≠ empty-table
  (different states, different copy).
- **Pagination vs infinite scroll vs virtualization:** paginate when items are destinations users
  return to (URLs per page); infinite-scroll only feeds; virtualize whenever row count is unbounded.
- **Failure:** the do-everything table — sort+filter+group+edit+expand in one surface without a
  view-configuration escape hatch; and bulk-action scope ambiguity (acting on rows the user can't
  see).

## form
- **Anatomy:** single column by default · labels above fields · grouped sections with headers ·
  required marked (or better: optional marked, when most fields are required) · primary action
  right/bottom, destructive far away · field-level help below, errors adjacent.
- **Validation timing:** validate on blur, re-validate on change *after* first error (reward
  correction immediately); never on first keystroke; the submit button stays enabled — a disabled
  submit hides *why* (run the error summary instead, linking to fields).
- **Length control:** past ~7 fields, group into sections; past ~3 sections, consider the wizard
  (macro) — but see wizard abuse.
- **Failure:** premature validation (red before the user finishes typing); placeholder-as-label
  (label vanishes on input); save-model ambiguity on settings forms.

## navigation modules
- **Tabs:** peer views of one object; selection is exclusive and persistent; never for actions.
  Overflow: scrolling tabs, never a "More" tab holding primary destinations.
- **Sidebar nav:** the saas-dashboard spine — collapsible, current item marked at every depth,
  max two levels visible (deeper = section landing pages).
- **Breadcrumbs:** location, not history; every ancestor clickable; current page unlinked.
- **Command palette (⌘K):** the long-tail router — verbs AND destinations, fuzzy matched, recent
  first. It supplements visible nav; it never excuses hiding primary verbs.
- **Failure:** nav duplication (same destination in tabs, sidebar, AND breadcrumb acting
  differently); tab-as-button (a "tab" that performs an action).

## pickers
- **Select / dropdown:** ≤ ~15 options; past that, combobox with type-ahead. Groups for natural
  categories; recent/frequent on top when history exists.
- **Combobox:** input + filtered listbox; free-text either allowed (tagged as new) or refused
  (validation) — decide and signal, never silently coerce.
- **Date/time:** typed input first (with format hint), calendar as assist, never calendar-only;
  ranges get presets (Today, Last 7 days) before custom.
- **Failure:** dropdown for two options (radio does it in zero clicks); calendar-only date entry
  (keyboard users, distant dates).

## toolbar + overflow
- **Anatomy:** frequent verbs inline (icon+label beats icon-only), the rest behind "⋯" overflow;
  priority order declared so collapse is lowest-priority-first; verbs grouped by object.
- **Contract:** the overflow seam is the module's load-bearing part — see
  `component-forge/references/composition-patterns.md` for the mechanism.
- **Failure:** icon-only toolbars past ~5 verbs (labels are the affordance); overflow hiding the
  primary verb at common widths.

## overlays: dialog · drawer · sheet · popover · toast
- **Modal dialog:** interrupts for a decision the flow cannot proceed without. Focus-trapped,
  Escape closes (= Cancel), primary action named for the consequence ("Delete 3 files", never "OK").
- **Drawer:** detail/edit beside context — inspection without navigation; non-modal by default.
- **Sheet (mobile):** the thumb-reachable dialog/drawer; full-screen sheet only for sub-flows.
- **Popover:** transient, anchored, dismisses on outside-click; owns no critical state.
- **Toast:** transient confirmation + undo vehicle (see safety-verify); never for errors that need
  action — those belong inline or in a dialog.
- **Failure:** modal-for-everything (interruption as default); nested modals (redesign the flow);
  toast errors that vanish before reading.

## search module
Input (persistent, editable) → suggestions (recent · completions · direct hits, keyboard-navigable)
→ results (see macro search-results). Scope control adjacent to the input when multiple corpora
exist. **Failure:** suggestion list that hijacks Enter (typed query vs highlighted suggestion).

## detail panel / property inspector
Selection-driven: header (identity + primary verb) · grouped read/edit fields · activity/meta
collapsed by default. Empty selection shows *how to select*, not a blank pane. **Failure:** the
inspector that edits a stale selection after the canvas moved on (bind by ID, show the binding).

## notification center
Bell + badge (count of *unread that needs action*, not everything) · list grouped by
day/type · per-item: source, summary, timestamp, jump-to-context · mark-all-read · settings link to
per-type controls. **Failure:** notification inflation — informational events badged like
actionable ones until the badge means nothing.

## onboarding modules
Checklist (persistent, dismissible, progress-marked) beats tour; tour (max 3–5 stops) only for
spatial orientation; empty states carry the per-surface onboarding load (see state-patterns).
**Failure:** the mandatory multi-stop tour before first value; coach marks over a UI the user
hasn't tried to use yet.

## carousel / media gallery
- **Anatomy:** viewport (one slide focal) · visible position indicator (dots to ~8 items,
  thumbnails/count past that, always clickable for direct access) · prev/next arrows.
- **Contract:** never autoplay past the first user interaction (and pause on hover/focus); swipe,
  arrows, and keyboard (←/→) advance it with full parity; position always visible; honors
  reduced-motion (crossfade or jump, never a forced slide).
- **Failure:** the carousel as burying ground — content nobody sees past slide 1; a rotating hero
  is where stakeholders park what the page couldn't prioritize.

## data-viz module
Chart-in-product, not a BI canvas: **one question per chart** — the title states the question, the
mark answers it.
- **Contract:** axis honesty — bar charts baseline at zero (length is the encoding; a truncated
  axis belongs only on line charts, flagged); direct-label the series when < 5 (legend only past
  that); empty/insufficient-data is a distinct state from a true zero (a flatline at 0 *is* data).
- **Failure:** the dashboard-grid data dump — every available metric charted at equal weight; see
  the dashboard page rule in macro-patterns.md (3–7 questions, one chart each).

## map module
- **Anatomy:** map canvas · search / search-this-area · result pins (clustered at density) ·
  detail card + result list bound to the canvas.
- **Contract:** list↔map selection sync both ways (selecting a list item highlights its pin and
  vice versa); everything a pin conveys is reachable by keyboard through the list — the map is an
  accelerator, never the only path.
- **Failure:** map-only information — results, prices, or availability that exist solely as pins,
  unreachable without a pointer and gone when the map fails to load.

## marketing modules
- **Hero:** one message + one primary CTA (a secondary *link* at most); the headline states the
  value, not the category.
- **Pricing table:** column-per-plan, exactly one plan highlighted (the intended default), feature
  rows scannable across columns, CTA repeated per column.
- **Social proof:** attributed (name, role, company) and specific (a result, not an adjective);
  logos-without-claims beat claims-without-names.
- **Failure:** the hero carrying three competing CTAs — when everything is primary, the visitor's
  first decision becomes the page's navigation problem.
