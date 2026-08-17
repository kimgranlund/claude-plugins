# Capability availability tiering — keep ambient disclosure cheap while switchable

> Axis: how a chat product discloses a user's saved capabilities/personas to the model without
> paying their full content cost on every turn regardless of use. A distinct concern from THIS
> pack's own knowledge-pack retrieval axis (a corpus of reference facts) — here the "capability"
> being disclosed is a persisted, user-controllable roster entry, not a fact corpus. Grounded in a
> worked instance: `@agent-ui/a2ui`'s ADR-0190.

## Three-tier reach, two axes never collapsed into one

**Claim — ever-present · invocable-only · off are three distinct reach tiers, built from two axes
(`enabled` × `availability`) that are never collapsed into one flag.** Ever-present entries
contribute ambiently every turn; invocable entries contribute ZERO ambient bytes until express
invocation; disabled entries are absent from active rosters but still LISTED in the menu — a
global off-switch a user cannot flip back on is not a switch. The persistent switch and the
per-turn typeahead are different mechanisms over ONE store of truth, never a second source of
truth. · ADR-0190 Decision (Kim's ruling, verbatim in Context) · 2026-08-14 · [verified]

## Index lines, not full content, cut ambient cost ~77-80%

**Claim — one index line per entry (label + description) bounds ambient cost by count × one
line, instead of unbounded full-content blocks.** Measured on realistic agents: full-content
ambient capability blocks run 10-16 KB (28-45× the persona they ride behind, unbounded in entry
count/size); one index line runs 65-102 B vs 218-504 B full — full content rides only the express-
invocation path. The model is TOLD the index is an index and how entries load, so it knows to
invoke rather than assume it already has the whole thing. · `capability-availability-tagging.spec.md`
§12 byte survey (SPEC-R14/R15) · 2026-08-14 · [verified]

## What this file does NOT cover

The corpus/retrieval-index pattern for a fact-shaped knowledge base (a different kind of "index",
answering a different question — how a REFERENCE CORPUS is entered by search, not how a user's
own capability roster is disclosed): `knowledge-packs-and-cited-retrieval.md`. The non-destructive
write law for a MODEL-authored patch to this same kind of persisted store:
`model-authored-memory-patch-non-destructive-writes.md`.
