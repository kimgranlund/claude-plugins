# The knowledge base — maturation arc, habits, and what gets measured

Source: `.claude/docs/spec/product-lifecycle-bible.md` Part 5 ("The knowledge base"), Part 6
("The habits"), Part 7 ("What we measure"). [verified] against the committed bible, v1.1.0,
checked 2026-08-16.

## Robust context is grown, not authored

The knowledge base follows a maturation arc, and every stage of it is event-driven rather than
scheduled:

1. **Born as homes** (Kickoff) — structure before content: a place for every kind of fact, nearly
   empty.
2. **Grows by harvest** — captured at the moment a truth surfaces, in the *cheapest durable form*
   (a rough note, an ugly screen recording); refinement is earned by recurrence, never done
   speculatively. Growth follows evidence — a fact enters because someone needed it, not because a
   template had a slot.
3. **Evolves under amendment** — wrong claims get dated corrections; decisions get superseded,
   nothing silently rewritten.
4. **Matures by pruning** — lines that stop changing behavior get deleted. **Robust means small,
   current, and load-bearing — a state you earn over turns of the loop, not a deliverable you
   write.** A growth curve that never bends is rot, not health.

[verified] bible Part 5, checked 2026-08-16.

## The source of truth, actually enforced

Every fact has exactly one home; everything else references it. A restated fact is a copy with no
synchronization protocol — divergence isn't a risk, it's the steady state. This same discipline is
why this file cites the bible by path+part rather than restating it wholesale.

**Searched, not read.** The knowledge base is an index executors pull from just-in-time, never a
payload loaded wholesale — for AI agents this is a hard technical requirement, not a preference.
Author dense; consume sparse.

**The grounding doc.** Every repo carries one (in practice, `CLAUDE.md`/`AGENTS.md`): one screen
that takes an executor from cold to oriented — identity, the never-do invariants, the
trigger→home routing map, how to work here, what done means. It *points* at the knowledge base; it
never *is* the knowledge base. A grounding doc that grows per incident has a routing problem, not a
documentation problem.

**The domain layer.** Short indexed walkthrough videos (3–8 minutes, one topic) · annotated
prototypes (each note marked *hard rule* or *just an example*) · decision records with rejected
alternatives · a living glossary (one home per term) · a failure ledger. **The indexing rule:**
every media artifact gets a one-paragraph text index in the knowledge base, or it's a large file,
not knowledge.

[verified] bible Part 5, remaining sections, checked 2026-08-16.

## The seven habits

1. **Explained it twice? Write it down.** The third telling should already be an edit — a pattern,
   a record, or an automated check.
2. **One home per fact.** Reference, never restate.
3. **Rules that matter become checks.** A convention living only in prose is a promise with a
   half-life of one reorg; machine-checkable rules run automatically and never soften their
   findings to keep a meeting pleasant.
4. **Fix with a date; never erase.** Wrong claims get dated amendments. Decisions get superseded,
   never rewritten — an edited decision is forged institutional memory.
5. **A DRI can explain it.** Checks verify; a named human answers.
6. **Plans die into the archive.** On completion, learnings promote out and the plan archives.
   Nothing stays "active" that isn't.
7. **Prune.** Every line in the knowledge base must change what an executor does — remove it and
   someone's work gets worse — or it gets deleted. A healthy knowledge base is small.

[verified] bible Part 6, checked 2026-08-16.

## What gets measured

- **Relearn rate** — how often the org re-purchases a lesson it already captured. Target: trending
  to zero. *(Being instrumented before external claims are made on it — the bible itself flags this
  as not-yet-proven.)*
- **Turn rates per loop** — healthy products release constantly, re-architect occasionally, pivot
  rarely-but-not-never.
- **Comprehension** — can the people who shipped it explain it? Measured at Verify via
  explain-back; a failing answer is logged as a defect.

[verified] bible Part 7, checked 2026-08-16.

## Boundary

This file states the general maturation model, the seven habits, and what the bible recommends
measuring — portable doctrine. It does not audit whether a specific repo's own knowledge base is
actually healthy by these measures (that reading requires live inspection of the repo's own docs
tree and history) — a `project-docs`-and-beyond question, not this pack's.
