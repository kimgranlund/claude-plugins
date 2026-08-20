# Below-element reactivity + render-clock coexistence

A single component tree can legitimately run more than one reactivity/scheduling regime at once —
gen-ui-kit's web-components package is the clearest grounding instance, coexisting THREE distinct
mechanisms deliberately, plus one place where two clocks compete unintentionally.

## Per-part effects — reactivity below the element boundary

Most of gen-ui-kit's ~125 components render imperatively inside one element-level `effect()` (the
base `UIElement`'s single render effect touches every prop signal, then calls the instance's own
`render()` — `core/element.js:227-241`) [verified, source read 2026-08-20]. But ~12 components use
a tagged-template style (`html`\`…\`\`, `core/template.js`) whose `update()` step wraps each
function- or signal-valued interpolation in its OWN per-part `effect()`
(`core/template.js:507-517`) [verified] — reactivity below the whole-element level, so a single
changed interpolation re-runs only its own part's effect rather than the element's entire render
function.

## Keyed reconciliation — a third, list-specific mechanism

Two components (`tabs`, `pagination`) use `UIElement.reconcile(parent, items, keyFn, stampFn)` — a
keyed diff against a per-parent key map (`core/element.js:416-439`) [verified]. Template-style
components have their own parallel `repeat()` directive for keyed lists
(`core/template.js:519-556`). The corpus's own inconsistency note names this as "the same job,
three list mechanisms" — keyed `reconcile()`, template `repeat()`, and outright hand-rolled loops —
with the package's single largest list renderer (`table-ui`) using NONE of the shared infrastructure
[verified, `01-primitives-reactivity.md` §"Inconsistencies worth flagging" item 1].

## A second render clock: rAF alongside the microtask flush

The base signal system batches via `queueMicrotask` (see `signal-kernels.md`). `table-ui` bypasses
signals for its own internal state (`#data`/`#sortState`/`#filters`/`#page` as plain private
fields) and instead calls a **rAF-batched** `#requestRender()` on every setter
(`table.class.js:466-473`) [verified] — the only scheduler of its kind in the package. The corpus's
own finding names the consequence directly: *"table prop writes and signal-prop writes coalesce on
different clocks"* [verified, `01-primitives-reactivity.md` §"Inconsistencies worth flagging" item
2] — a component that mixes a signal-backed prop with `table-ui`'s internal state has no guarantee
the two settle in the same tick, because one clock is a microtask and the other is a paint-aligned
callback.

This is the one UNINTENTIONAL clock mismatch in the corpus (contrast with `tier-split.md`'s
`liveRefresh()`, which is a DELIBERATE, documented rAF fast path layered ON TOP of a synchronous
`doc` mutation) — worth naming as a hazard: two clocks coexisting by accident, in the same package,
with no cited reason for the split.

## Connect-time untracked discipline

`connectedCallback` replays every attribute for SSR/shim upgrade (`core/element.js:189-215`),
wrapped in `untracked()` specifically to prevent subscription leaks into a parent's render effect
[verified, source read 2026-08-20]. This matters because connect-time is exactly when a component's
own signals are first being populated from attributes — reading them normally (tracked) during that
replay would make the PARENT's render effect (if one happens to be active on the call stack at
attach time) subscribe to a child's internal signal, a leak with no natural teardown point. Wrapping
the replay in `untracked` is the same discipline agent-ui's `graph.ts` names generically (see
`ownership-and-teardown.md`'s `untracked`/`unowned` pair) — two independent codebases converging on
"initialization reads must not be tracked reads."

## Practical guidance

- **Fine-grained (per-part) effects are worth it exactly where whole-element re-render is
  measurably too coarse** — the template-style components chose it deliberately, most components
  don't need it.
- **A second scheduler alongside the primary one needs a stated reason.** rAF for pointer/paint-
  aligned work is legitimate (table's own batched setter, ultimate-tokens' `liveRefresh` in
  `tier-split.md`) — but every instance in the corpus that's WORKING correctly documents why; the
  one that doesn't (table vs signal-prop clock mismatch) is flagged as unexplained.
- **Wrap connect-time/initialization reads in `untracked`** whenever a component's own setup could
  run while a caller's tracking context is active on the stack.

## Boundary

This file covers reactivity granularity BELOW the element and scheduling-clock coexistence. The
kernel's own primitives are `signal-kernels.md`; the architecture-level tier question (does an app
even use a signals kernel) is `tier-split.md`.
