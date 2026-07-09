# Composition patterns — the tier ladder's recipe library (COMPOSE A4 / A5)

This is the **composition** half of component-forge: where the family files (`family-controls.md`,
`family-overlays.md`) are the recipe library for a **single component**, this file is the recipe library for
**how components nest + wire** up the tier ladder (**primitive → component → module**) — the COMPOSE axis's
A4 Composition / A5 Coherence rungs, mechanized by `scripts/composition-check.py`.

Each pattern is a tier with a fixed shape: **anatomy** (the containment tree), **seam** (how it wires its
pieces — slots / slot-presence grid / overflow), **state** (what flows and where it lives), **adaptation** (how
it reshapes). Match the UI to a pattern, then grade it on both axes (`decomposition-method.md`).

**The three tiers** (A4's first decision, `composition-check.py`'s tier-consistency gate):

| Tier | What it is | Owned by |
|---|---|---|
| **Primitive** | an atomic control — composes no other `x-*` (button · input · checkbox · select / menu · spinner) | a single **contract card** (`family-controls.md` / `family-overlays.md`, the REALIZE geometry law) |
| **Component** | a composition of primitives + a **seam** (slots, a slot-presence grid, an overflow mechanism) | this file — the **component** patterns below |
| **Module** | a whole embedded **workflow** — components in regions, with cross-component state | this file — the **module** patterns below; its **app shell / page hands UP to layout-decompose** |

A **primitive** is the leaf: cite its contract card (anatomy · attributes-as-API · FACE · the `(h−glyph)/2`
geometry) and don't re-derive it inside a composition. The **module** is the largest thing this axis owns; the
*app shell / page region grid* it sits inside is **layout-decompose's** (the A4→shell up-handoff). This file
covers the **component** and **module** tiers — the seams between pieces.

## Component tier — a composition of primitives + one seam

### Toolbar + overflow
- **Anatomy:** `toolbar → [ action-group(button…) · flexible-spacer · overflow-trigger → menu(item…) ]`.
- **Seam:** a **priority-ordered overflow** — actions render inline in priority order until they don't fit the
  available width, then collapse *lowest-priority-first* into the overflow menu. The menu items and the inline
  buttons are the **same action list**, projected — never two hand-kept copies.
- **State:** the overflowed set is *derived* from `available-width` (a resize observer / container query), not
  authored. One source of truth: the action list + each action's priority.
- **Adaptation:** on resize it re-partitions inline ↔ overflow; every action stays reachable (the overflowed
  ones live in the menu); at the narrowest it may become a single overflow trigger.
- **Smell:** a static `···` opening a hardcoded menu whose actions don't match the inline ones — boxed but
  inert (fails the A4 seam gate; the cross-component state note on REALIZE B3).

### Card (header / body / footer + actions)
- **Anatomy:** `card → [ header(title · ?meta · ?actions) · body(content) · ?footer(?actions) ]`.
- **Seam:** **named slots** with a **slot-presence grid** — `header / body / footer` are slots; the grid rows
  exist only for the slots that are filled (`:has()`-driven), so a card with no footer leaves no empty footer
  band. `slot-grid header,body` → two rows; `header,body,footer` → three.
- **State:** usually stateless (a projection of its content); actions emit events up to the module.
- **Adaptation:** the slot-presence grid reshapes; the body scrolls or clamps; an empty body shows an
  empty-state slot, not a collapsed box.
- **Smell:** `header / body / footer` baked in as required children with a permanent empty footer band when
  there's no footer — no slot-presence (fails the A4 seam gate; the slot-presence → grid generator in
  `composition-check.py`).

### Modal / drawer (an overlay component)
- **Anatomy:** `modal → [ ?backdrop · surface( header(title · close) · body · ?footer(actions) ) ]`.
- **Seam:** named slots (`title / body / actions`) + the **open-state** seam (a single `open` reflecting prop /
  event) + focus-trap & dismiss wired once. The *geometry* of the surface and the close button is the
  single-component REALIZE concern (`family-overlays.md`); A4 owns *which slots*, *the open seam*, and *the
  dismiss contract* — how this overlay composes into its host module.
- **State:** `open` is owned by the **parent** (the module decides when it's open) and reflected down; dismiss
  emits up. Never two opens (a local `open` AND a parent `open` fighting).
- **Adaptation:** the body scrolls within the surface (the surface never grows the page); responsive → a
  full-screen sheet on narrow.
- **Smell:** the modal owns its own `open` boolean *and* the parent owns one → they desync (the cross-component
  state defect, REALIZE B3).

## Module tier — components in regions + cross-component state

### Settings (left-nav + content)
- **Anatomy:** `settings-module → [ region:nav(nav-list) · region:content(panel-for-selection) ]`.
- **Seam:** the regions are slots / areas; the **selection** is the cross-component seam — the nav emits
  `select(section)`, the content renders the panel for the current section. One selection, two projections.
- **State:** `selected-section` lives at the **module** (the lowest common parent of nav + content), not in
  either component. Nav highlights it; content reflects it; the URL may mirror it.
- **Adaptation:** narrow → the nav collapses to a top tab-bar or a drawer; the content is the elastic region.
- **Smell:** the nav holds its own "active" state AND the content holds its own "current section" → they
  disagree on which section is open (the duplicated cross-component state defect, REALIZE B3 — and the module
  fails to cohere as one workflow, A4).

### Master-detail
- **Anatomy:** `module → [ region:list(item…) · region:detail(detail-for-selection) ]`.
- **Seam:** the **selected item** — list emits `select(id)`, detail renders for `id`; the breadcrumb / title
  reflect it too (one selection, many agreeing projections).
- **State:** `selected-id` at the module; loading / empty / error states for the detail are designed.
- **Adaptation:** narrow → list and detail become two stacked views with a back affordance.

### Wizard / stepper-flow
- **Anatomy:** `module → [ stepper(step…) · region:step-body(panel-for-current-step) · region:footer(back · next) ]`.
- **Seam:** the **current step** + the **step validity** — next is gated on the current step's validity; the
  stepper reflects progress; back / next move the step.
- **State:** `current-step` + per-step validity at the module; the step panels are dumb projections.
- **Adaptation:** the footer's next is disabled until valid; a long flow scrolls the body, never the chrome.

---

## Using the patterns

- **DECOMPOSE:** match the UI to a pattern, then check its *seam* and *state* against the recipe — most
  real-world failures are a missing seam (the A4 seam gate) or duplicated cross-component state (REALIZE B3) the
  recipe names. Run `composition-check.py lint` over the composition card.
- **DESIGN:** start from the pattern's seam + state, then set the boundary + containment (A4) around it and give
  it zero outer margin (A5). The recipe is the skeleton; the rubric grades the flesh.
- A pattern is a **starting grammar, not a cage** — real modules hybridise (a settings module whose content
  region is itself a master-detail). Name the dominant pattern, then note the graft.

## The boundaries — leaf DOWN, app shell UP

The composition tier sits between two boundaries the family keeps sharp (folded in from the ladder):

- **DOWN — the leaf (a primitive).** Anything *inside* one custom element's boundary — its parts, its padding,
  its ARIA, its keyboard map, the `(height − glyph)/2` geometry law — is the **single-component** concern of this
  same skill (the REALIZE axis + `family-controls.md` / `family-overlays.md`). A composition **cites** a
  primitive's contract card and stops; it does not re-derive a button's pixels or a select's ARIA. The seam
  *between* two elements is where A4 begins.
- **UP — the app shell (the frame).** A **module** is the largest thing this axis owns: components in regions
  with cross-component state. But the *page* that hosts the module — the fixed app shell, the
  header / nav / canvas / footer region grid, which archetype it is — is **layout-decompose's**. A4's coherence
  check asks only *"does this module cohere as one workflow and fit the slot the shell hands it"*; it does **not**
  design the shell. A module that fights its frame (it sets its own page margin, it assumes a width the shell
  doesn't give) is an A5 finding here **and** a hand-up to layout-decompose for the frame.

> Rule of thumb: anything *inside* one element is REALIZE (the leaf); the *seams between* elements up to the
> module are A4 / A5; anything that fills the **viewport** and never scrolls away — the frame, the regions — is
> **layout-decompose's**.
