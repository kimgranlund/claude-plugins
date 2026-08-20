---
name: reactivity-facts
description: >-
  Answers how UI reactivity/state-propagation works, from a cited corpus —
  signal/computed/effect kernels, version-verified vs dirty-flag recompute, ownership-scope
  teardown, stale-response guards, below-element reactivity vs render-clock coexistence. Use
  for "why did this effect refire twice", "computed vs signal vs effect", "guard a stale async
  response", "per-part reactivity vs whole-component re-render", "ownership scope disposal",
  "rAF vs microtask clash", "parametric doc + derive-then-render vs fine-grained signals".
  ANSWERS the reactivity MECHANISM; NOT anatomy/API (make-component), pattern naming
  (ui-pattern-facts), or state ARCHITECTURE judgment (state-model-rules).
user-invocable: false
disable-model-invocation: false
---

# reactivity-facts — the UI reactivity/state-propagation world model

Answers why a reactive UI actually behaves the way it does — signal kernels, recompute strategy,
disposal, async-staleness guards, and scheduling-clock coexistence — from a corpus grounded in real
field reports across four repos (gen-ui-kit, agent-ui, ultimate-tokens, adia-v2), not general
signals-library folklore.

| Ask | Load |
|---|---|
| Signal/computed/effect kernel internals, the write-loop safety ceiling | `references/signal-kernels.md` |
| Framework signals vs a product-tier `doc → derive → render` architecture | `references/tier-split.md` |
| Does a computed re-run unconditionally on staleness, or verify its sources first | `references/verification-vs-dirty-flag.md` |
| Disposal correctness — ownership scopes, teardown symmetry | `references/ownership-and-teardown.md` |
| Guarding a stale/out-of-order async response | `references/sequence-tokens.md` |
| Per-part effects, keyed reconcile, rAF vs microtask clocks, connect-time untracked reads | `references/below-element-reactivity.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask against the six axes above; load only the matching reference (or `sources.md`
   for provenance). Hunting one specific claim inside a file: Grep for the term first rather than
   reading the whole file.
2. Answer on the contract: **claim + cited file:line/report + the grounding marker
   ([verified]/[incident])**. Worked shape:
   > *"Why did my effect run twice for one write?"* → recompute-strategy ask →
   `verification-vs-dirty-flag.md` — a dirty-flag kernel (gen-ui-kit's `core/signals.js`)
   re-runs unconditionally once flagged stale; a version-verified kernel (agent-ui's `graph.ts`)
   re-checks whether any source's VALUE actually changed first and skips the re-run if not. Which
   one you're on determines whether "twice" is expected.
3. State which axis the answer draws from, and its grounding marker — never present a corpus
   citation as live-verified-today code if the pack's own `sources.md` disclosure says otherwise.
4. Route derivation/build/pattern-naming work at the boundary (below) — this pack explains
   reactivity mechanism, it never emits component code or names a UI pattern.

## Boundaries

- **This skill answers reactivity/state-propagation mechanics; it does not derive a component's own
  anatomy, API surface, or build anything.** A control's tiers/API/geometry are `make-component`'s
  law — this pack explains the substrate a component's own signal-backed properties run on top of,
  not what the component's props should be.
- **UI pattern naming, archetypes, and the screen-state grammar (loading/empty/error) belong to
  `ui-pattern-facts`** — a "reactive state" ask (signals/effects) and a "screen state" ask
  (empty/loading/error UX) share vocabulary but are different axes; `tier-split.md`'s own boundary
  section names this split explicitly.
- **App-tier state ARCHITECTURE judgment belongs to `state-model-rules`** — stacked-generations
  pathology, a shared name masking two live facts, built-but-unadopted vs load-bearing layers,
  never-pulled re-evaluation triggers, doctrine-vs-practice divergence, and one-name-two-owners
  contract collisions. This pack explains why an EFFECT or COMPUTED behaves a certain way at the
  kernel level; `state-model-rules` judges whether the STORE, LAYER, or CONVENTION around that
  kernel is architecturally coherent. A "why is our app a mix of implementations" ask is
  `state-model-rules`'; a "why did this specific effect refire twice" ask is this pack's.
- **Client-persistence facts — storage discipline tiers, dual sync/async persistence contracts,
  the storage-specific bypass-inventory shape, URL-state sync — belong to `persistence-facts`.**
  What gets WRITTEN to storage and when that's disciplined is that pack's law; this pack explains
  the kernel that decides WHEN an effect or computed re-runs, unrelated to whether the resulting
  value gets persisted anywhere. A question naming a storage key, schemaVersion, or a URL param is
  `persistence-facts`'; a question naming a kernel primitive is this pack's.
- **How data gets CONNECTED to a UI element or across a bridge belongs to `data-wiring-facts`** —
  the attribute-driven streaming stack, the postMessage bridge protocol, no-DI substitutes, and the
  need→pattern wiring menu. That pack answers what gets wired and how; this pack explains the
  kernel that decides WHEN the resulting effect or computed re-runs, unrelated to whether the value
  arrived via a stream, a bridge, or a plain property assignment. A question naming a stream, a
  bridge message, or a wiring pattern is `data-wiring-facts`'; a question naming a kernel primitive
  is this pack's.
- **Which STAMPING STRATEGY a component uses, and the DOM-child mechanics around it (keyed
  reconcile, the display:contents trap, adopt-or-stamp) belong to `web-component-facts`** — that
  pack owns the stamping mechanism itself; this pack explains the kernel that decides WHEN a
  re-stamp fires in the first place, unrelated to which of the three strategies produced the
  stamped DOM. A question naming a stamping strategy, a slot trap, or a keyed-list mechanism is
  `web-component-facts`'; a question naming a kernel primitive (signal/computed/effect/scope) is
  this pack's.
- **Production component code** → `make-component` — this pack explains why a kernel behaves a
  certain way; it does not write the kernel or the component consuming it.
- **Building a signals kernel or an app-tier store from scratch has no owning builder skill in
  this plugin** — `make-component` owns a COMPONENT's own anatomy/API, not a reactivity kernel or a
  standalone store, so that ask is not silently routed there; derive the implementation inline
  against this pack's mechanism grounding (e.g. `signal-kernels.md`'s write-loop-guard shape) rather
  than treating either sibling as its build owner.

## Extending this pack

Extension: governed by [[make-pack]]
