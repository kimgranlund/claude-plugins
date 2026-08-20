# Dual sync-vs-async persistence contracts by design

**The judgment call:** finding two non-interoperable persistence answers in one codebase (one
synchronous store surface, one asynchronous storage seam) is not automatically drift — but it is
also not automatically fine. This axis is the test for telling the two apart, on a persistence
survey that found exactly this shape and ruled it legitimate.

## The two ratified layers [verified]

One codebase ratifies two ADR-level persistence contracts at once: an async, signal-backed
CRUD/streaming data seam (resource/mutation/paginated verbs over a gateway client), and a
separate async `StorageAdapter` seam (`get/set/delete/keys`, optional `subscribe`, a localStorage
tier and an IndexedDB tier) meant to replace scattered hand-rolled `localStorage` touch points.
Both are async by contract.

A third, deliberately SYNCHRONOUS surface also exists on top: a settings-store facade consumed
inside render paths where an async read would be awkward. Its own reference implementation
persists data THROUGH the async `StorageAdapter` seam underneath — the sync surface is a facade in
front of async storage, not a second, competing storage mechanism.

## The legitimacy test [verified]

Three conjuncts distinguish a genuinely legitimate dual-contract split from drift:

1. **Each surface is separately ratified** — an ADR or LLD names the sync surface's existence and
   its reason for being sync, rather than it having simply accreted.
2. **The sync surface delegates, it doesn't reimplement.** The sync facade's own reference
   implementation writes THROUGH the async seam for actual persistence rather than talking to
   `localStorage`/IndexedDB directly a second time. Two contracts that both terminate in the same
   underlying storage call are a legitimate split of calling convention; two contracts that both
   independently touch the storage API are the bypass class (see the persistence-audit-shape
   axis), not this one.
3. **Each surface's consumers have a real reason to need that calling convention** — a render-path
   read that cannot await a promise vs. a CRUD operation against a network-backed resource are
   different consumption shapes, not the same need served twice.

All three holding is what makes "we have both a sync store and an async storage seam" a legitimate
design fact rather than a finding to fix.

## What this is NOT — a shipped-but-dead layer isn't a second legitimate contract [verified]

The same survey that found the sync/async split legitimate found the OTHER async seam
(the CRUD/streaming data layer) has **zero real application consumers** — nothing outside its own
package, its own tests, and a documentation demo page calls its actual `resource()`/`mutation()`/
`paginated()`/`DataSource` grammar. That is a different finding entirely: a ratified contract that
was never adopted is not a second legitimate persistence answer coexisting with a first — it is a
layer that doesn't participate in the "dual contracts" picture at all, because nothing routes
through it. Don't count an unadopted layer as evidence for or against this axis; route an
"is this layer actually used, or just built" question to state-model-rules' adoption-verdict
axis instead — that is a judgment about the LAYER's adoption, not about whether two answers by
DESIGN is legitimate.

## The bypass class, for contrast [incident]

Distinct again from both of the above: several site-level modules hand-roll their OWN
`localStorage` reads/writes entirely outside the sanctioned async seam — including one full
duplicate reimplementation of the sync settings-store's own read/write/reset logic, independently,
in a different module. That is not a second legitimate contract and it is not an unadopted layer —
it is a real bypass, the failure mode the persistence-audit-shape axis exists to find and count.

## Sources

`/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/data-persistence-layers.md`
— "Sanctioned layers table", "Other store/state modules (different vocabulary, not persistence
bypasses)", and "Adoption verdict" sections. Reviewed 2026-08-20.
