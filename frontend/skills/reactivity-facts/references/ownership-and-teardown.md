# Ownership scopes + teardown-inventory-as-a-set

Disposal correctness in a reactive system depends on being able to answer one question with
certainty: "after I tear this down, does anything still hold a live reference into it?" The
grounding corpus shows one clean answer (agent-ui) and one cautionary counter-example
(ultimate-tokens) for the same underlying question.

## The clean pattern: ownership scopes as an inventory Set

agent-ui's `reactive/graph.ts` gives every computed and effect an OWNER — whichever `Scope` was
active (`activeOwner`) at construction time (`ComputedNode`/`EffectNode` constructors call
`activeOwner?.add(this)`, `graph.ts:143,246`) [verified, source read 2026-08-20]. `ScopeImpl` itself
is nothing more than a `Set<Disposable>` plus two methods (`graph.ts:300-318`):
- `run(fn)` — makes this scope the active owner for the duration of `fn`, so anything minted inside
  is automatically inventoried into the scope's Set.
- `dispose()` — iterates the Set once, calls `.dispose()` on every member, then clears the Set.

The module's own header comment states the resulting guarantee directly: *"Ownership scopes make
disposal provable: after `scope.dispose()`, no producer holds a reference to any node created inside
it."* [verified, source comment `graph.ts:5-6`] This is provable specifically BECAUSE membership is
a Set the scope itself owns — there is no separate bookkeeping structure that could drift out of
sync with what was actually minted.

Two escape hatches exist, both deliberate and both documented in-source:
- `untracked(fn)` — read without subscribing the active consumer (`graph.ts:78-86`).
- `unowned(fn)` — mint nodes OUTSIDE any scope, for module-singleton machinery created lazily on
  first touch, so it isn't accidentally adopted by whichever component scope happened to trigger
  that first touch — the header comment names the exact failure this prevents: *"the component's
  disconnect freezes the singleton"* [verified, source comment `graph.ts:88-93`].

## The counter-example: teardown as a hand-maintained list, not a derived set

ultimate-tokens' `app.js` registers several ambient subscriptions in `connectedCallback` — a
matchMedia scheme listener, a keydown handler, a `document.fonts.ready` one-shot, and
`_bindRangeDrag`'s host-level pointerdown listener (`app.js`, per the corpus's mechanism catalog)
[verified, source read via `ultimate-tokens/.claude/docs/reports/reactivity-2026-08-20/
01-core-reactivity.md`, §A]. `disconnectedCallback` tears down the keydown and matchMedia listeners
— but NOT `_bindRangeDrag`'s pointerdown listener [verified, same report, §B6]. The report's own
verdict: *"the teardown set isn't symmetric with what connectedCallback installs."*

This is currently harmless in that specific app (a long-lived singleton element that never
reconnects), but it is exactly the class of bug ownership-scope-as-a-Set structurally prevents:
teardown here is a hand-written list of "the things I remembered to clean up," which can silently
drift from "the things that were actually registered" the moment a new subscription is added and
the teardown list isn't updated in the same change. An owning Set built at registration time (or a
`createScope()`-style container) makes this class of drift structurally impossible instead of
relying on the next author to keep two lists in sync by discipline alone.

## The pattern to carry forward

**Teardown-inventory-as-a-set, not teardown-as-a-remembered-list**: register every disposable
resource into a container that OWNS enumeration (a `Set`, a scope), and have `dispose()`/
`disconnectedCallback()` iterate that container rather than hand-listing what to clean up. The
agent-ui `Scope` is the worked positive instance; the ultimate-tokens asymmetric teardown [verified]
is the negative instance this exact pattern would have prevented — not itself a dated [incident]
(the report finds no live bug from it today), but the failure mode a symmetric-by-construction
teardown structurally closes off.

## Boundary

This file is about DISPOSAL correctness. For the write-loop safety guard that protects against a
reactive graph that never settles (a different failure mode, at write time rather than teardown
time), see `signal-kernels.md`.
