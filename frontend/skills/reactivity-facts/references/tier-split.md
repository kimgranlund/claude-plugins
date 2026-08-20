# The tier split — framework signals vs product-tier doc→derive→render

Two structurally different reactivity shapes coexist across the grounding corpus, at two different
altitudes, and both are legitimate for what they own — this is a tier distinction, not a
"which one is right" question.

## Tier 1: framework/component-library signals

gen-ui-kit (`core/signals.js` + `core/element.js`) and agent-ui (`reactive/graph.ts` +
`reactive/scheduler.ts`) both build fine-grained, per-value reactive PRIMITIVES: a signal is one
mutable cell, a computed derives from other cells, an effect re-runs a side-effecting function when
its tracked sources change [verified, source read 2026-08-20]. This tier is about **how one value
becomes many derived values inside a component or a small object graph** — see `signal-kernels.md`.

## Tier 2: product-tier `doc → derive → render`

ultimate-tokens' editor app (`src/ui/app.js` + section files) does NOT use a signals library at all
— it has no `signal()`/`computed()`/`effect()` anywhere in its own code. Instead the whole
application is one parametric document object (`this.doc`), a pure derivation step
(`projectView(doc)` / `_typeScaleFor` / `_geomScaleFor` — mode-aware pure functions of `doc`), and a
full-subtree `render()` that rebuilds the DOM from the derived view [verified, source read
2026-08-20, corpus `ultimate-tokens/.claude/docs/reports/reactivity-2026-08-20/00-synthesis.md` +
`01-core-reactivity.md`]. The commit ladder (`edit()`/`commit()`/`editDrag()`) is the only sanctioned
mutation path; every place that bypasses it carries an inline comment explaining why
(`01-core-reactivity.md` verdict, §D) — this is documented ARCHITECTURE, not accidental drift.

The one deliberate fast path in this tier is `liveRefresh()` — a rAF-coalesced partial repaint used
ONLY for the color section's live drag feedback; Type/Geometry drags mutate `doc` synchronously but
the DOM lags until pointer-up, a stated, intentional asymmetry (`01-core-reactivity.md` §B5)
[verified].

## Why the split is real, not accidental

- **Different unit of change.** Tier 1 reacts to one signal's value changing. Tier 2 re-derives an
  entire projected view from one parametric document on every edit — there is no per-field
  granularity to react to, because the "reactive unit" is the whole document.
- **Different consumer shape.** Tier 1 serves many small, independently-lifecycled DOM elements
  (a component tree). Tier 2 serves one long-lived singleton editor shell, so a full re-render's
  cost is bounded and predictable in a way it wouldn't be across hundreds of components.
- **Neither tier reaches for the other's mechanism where it shouldn't.** ultimate-tokens never
  imports or hand-rolls a signals library for its per-field state; gen-ui-kit and agent-ui never
  collapse their component trees into one document-diff loop.

## Where product-tier code SHOULD look like tier 1 instead

The one place `doc → derive → render` gets expensive is when a caller wants FINE-GRAINED
reactivity below the render boundary — e.g. gen-ui-kit's `core/template.js` per-part effects
(see `below-element-reactivity.md`) exist precisely because a whole-subtree re-render is too coarse
for some templates. If a product-tier app finds itself hand-building a per-field diff/patch layer on
top of its `doc→render` loop, that is the signal it has outgrown tier 2 and should adopt (or build
toward) a tier-1 kernel for that slice — not a reason to abandon tier 2 everywhere.

## Boundary

This file distinguishes the two ARCHITECTURAL tiers. For how tier 1's own computed nodes decide
whether to recompute, see `verification-vs-dirty-flag.md`. This file does not cover UI presentation
states (loading/empty/error) — those are `ui-pattern-facts`' `state-patterns.md`, a different axis
entirely (screen-state grammar, not data-reactivity mechanics).
