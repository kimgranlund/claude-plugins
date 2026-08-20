# Version-verified vs dirty-flag recompute — two different cut strategies

Both grounding kernels mark a computed "possibly stale" the same way (push invalidation on write),
but they diverge on WHEN the computed actually decides to re-run its derivation function — this is
the single clearest structural difference between the two implementations.

## Dirty-flag recompute (gen-ui-kit)

`core/signals.js`'s `computed()` is lazy and **dirty-flag cached** [verified, source read
2026-08-20]: a write to a dependency sets a boolean `dirty = true` on every downstream computed; the
next READ of that computed checks the flag — if dirty, it unconditionally re-runs the derivation
function and clears the flag. There is no secondary check of whether the SOURCE'S VALUE actually
changed vs merely being touched — dirty is a one-bit "something upstream wrote," not "something
upstream's value differs."

## Version-verified recompute (agent-ui)

`reactive/graph.ts`'s `ComputedNode` tracks two things per source: the producer and the **producer's
version number at the time it was read** (`sources: Map<Producer, number>`, `graph.ts:133`)
[verified, source read 2026-08-20]. On a stale read:
1. `markStale()` still just flips a `#dirty` bit and propagates possible-staleness downward
   (`graph.ts:162-166`) — structurally the same push-phase as gen-ui-kit.
2. But `refresh()`'s pull phase does NOT unconditionally re-run. It walks every tracked source,
   calls `src.refresh?.()` to settle nested computeds first, then compares `src.version !==
   seen` (`graph.ts:184-191`). **Only if some source's version actually advanced** does it re-run
   `#fn()`. If every source verifies unchanged, `#dirty` clears and the STALE flag resets without
   ever calling the derivation function.
3. A signal's own `version` only increments when its value fails an `Object.is` equality check on
   write (`SignalNode#set value`, `graph.ts:117-122`) — so "version changed" and "value actually
   changed" are the same event, transitively, all the way up the dependency graph.

The kernel's own header comment states the rationale directly: *"Push possible-staleness, pull
values, cut on equality (version-verified at both computeds AND effects)."* [verified, source
comment `graph.ts:3-4`]

## Why the order inside `ComputedNode#value` matters (a subtlety worth citing)

`graph.ts:145-153`'s own inline comment: *"Settle BEFORE the consumer records our version — track-
first records a stale version and forces one spurious downstream recompute per change."* This is a
verified, reasoned ordering choice, not an oversight — refreshing a computed BEFORE letting a
downstream consumer subscribe to (and record) its current version avoids the downstream consumer
subscribing to a version number that's about to change one line later.

## Consequence: effects get the same cut, one level up

agent-ui's `EffectNode#run()` applies the identical verification before running its body
(`graph.ts:257-268`) [verified] — a scheduled effect whose sources all verify unchanged skips its
body entirely. gen-ui-kit's plain `effect()` re-runs whenever scheduled, with no equivalent
secondary check documented in the corpus for this axis.

## Practical difference this produces

- **Dirty-flag** (gen-ui-kit): a computed whose sources were "touched" but land back on the same
  value still pays a full recompute. Simpler, cheaper to implement, more re-runs.
- **Version-verified** (agent-ui): a computed whose sources verify unchanged skips its own
  recompute AND (transitively) never wakes ITS OWN subscribers, because its own `version` never
  bumps without an `Object.is` failure. Fewer re-runs, more bookkeeping (a `Map<Producer, number>`
  per consumer instead of one boolean).

Neither is a defect — they are different points on the same cut-early-vs-cut-late spectrum, and a
new kernel should pick one deliberately rather than accidentally landing on dirty-flag by default
(the simpler shape to reach for) when the actual requirement is "skip a no-op recompute."

## Boundary

This file is about the RECOMPUTE decision inside a computed/effect. For the kernels' shared
public surface and their convergent write-loop guard, see `signal-kernels.md`. For the higher-level
architectural tier this recompute strategy sits underneath, see `tier-split.md`.
