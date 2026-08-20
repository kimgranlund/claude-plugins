# Signal kernels — two independent implementations, one convergent guard

Two hand-rolled signal libraries were built independently, in different repos, with no shared
lineage — and they converged on the same core shape AND the same specific safety guard.

## The two kernels

**gen-ui-kit's `core/signals.js`** (web-components package) [verified, source read 2026-08-20]:
- `signal()` — a value cell with a subscriber `Set` and an `Object.is` short-circuit on write
  (`core/signals.js:68-76`).
- `computed()` — lazy, **dirty-flag** cached (`core/signals.js:78-98`) — see
  `verification-vs-dirty-flag.md` for how this differs from agent-ui's version-verified equivalent.
- `effect()` — subscribes and reruns on staleness (`core/signals.js:100-109`).
- Batching: `queueMicrotask(flushSigs)` (`core/signals.js:25`), plus `batch()`/`untracked()`
  (`:54-66`).
- **A 100-iteration drain-loop guard with host attribution** (`core/signals.js:30-52`) — added
  specifically for a parent↔child oscillation incident (gh#961) where two components' effects kept
  re-triggering each other and never settled.

**agent-ui's `reactive/graph.ts` + `reactive/scheduler.ts`** [verified, source read 2026-08-20]:
- `signal()`/`computed()`/`effect()` — same three-primitive surface (`graph.ts:323,326,332`), push-
  invalidate/lazy-pull, `Object.is`-cut.
- `computed()` is **version-verified**, not dirty-flag (`ComputedNode#refreshInner`,
  `graph.ts:177-216`) — a structurally different cut mechanism, see `verification-vs-dirty-flag.md`.
- Batching lives in a separate, import-free `scheduler.ts` module — the queue is a `Set` (structural
  dedupe), flushed via `queueMicrotask` (`scheduler.ts:15-27`).
- **The identical guard**: `flush()` counts `waves`, and past 100 it clears the queue and throws
  `'effect write-loop: queue failed to settle in 100 waves'` (`scheduler.ts:36-55`). The module's
  own header comment names this "the ~100-wave write-loop budget" as one of exactly two things the
  scheduler half owns.

## The convergence tell [verified]

Both kernels independently arrived at:
1. The same three-primitive public surface (signal/computed/effect).
2. Microtask-batched flushing, not synchronous or rAF-driven.
3. **The exact same numeric budget — 100 — for a write-loop/oscillation guard**, in two codebases
   with no shared authorship or copy-paste lineage between them (gen-ui-kit is a web-components
   library; agent-ui is a separate component package in a different repo).

This is strong evidence the 100-iteration/wave ceiling is not an arbitrary tuning knob but a
converged-on answer to the same real failure mode: two reactive nodes whose effects re-trigger each
other (a cycle that doesn't resolve to a fixed point) needs a hard ceiling, or the microtask queue
never drains and the tab hangs. gen-ui-kit's own comment ties its guard to a **specific incident**
(gh#961, a parent↔child oscillation) [incident] — agent-ui's guard is undated in-repo but structurally
identical, including the "queue never settles" framing.

## What this means for a new signals-backed component or app-tier store

- **Ship a write-loop ceiling from day one**, not as a reactive add-on after the first oscillation
  incident — both grounding repos needed one, and one of the two only added it after a live bug.
- **Pick a number, don't leave it unbounded.** 100 is the value both independent implementations
  converged on; there's no evidence either tuned it down from something larger or up from something
  smaller — treat it as a reasonable default, not a magic constant to preserve exactly.
- **The guard must clear its own queue before throwing** (both kernels do this) — an oscillation that
  throws but leaves stale entries queued just wedges the next unrelated write instead of failing
  cleanly.

## Boundary

This file is about the **kernel's own internals** — how signal/computed/effect are implemented.
For how a computed decides whether to actually recompute (dirty-flag vs re-verifying source
versions), see `verification-vs-dirty-flag.md`. For the tier a whole app puts ON TOP of a kernel
like this (doc → derive → render), see `tier-split.md`.
