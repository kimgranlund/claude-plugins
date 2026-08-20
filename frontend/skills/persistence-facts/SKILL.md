---
name: persistence-facts
description: >-
  Answers client-persistence FACTS from a cited field-report corpus — storage discipline tiers
  (schemaVersion/rename-map vs ad-hoc JSON.parse vs cache-buster keys; the rename-without-migration
  data-loss class), when a sync store next to an async storage seam is legitimate design vs. bypass
  drift, the persistence-specific bypass-inventory audit shape (grep by storage-key namespace, not
  just importing module), and URL-state sync (PHI exclusion, push vs. replace, multi-value
  encode/decode). Use for "does this storage need a schemaVersion", "will renaming this field drop
  saved data", "is a sync store next to our async adapter a bypass or legitimate", "audit our
  persistence code for bypasses", "should this search param be in the URL", "PHI in a URL param",
  "push vs replace for a filter change". ANSWERS persistence FACTS; NOT app-tier state architecture
  judgment generally (state-model-rules), NOT reactivity mechanism (reactivity-facts).
user-invocable: false
disable-model-invocation: false
---

# persistence-facts — client-persistence world model

Answers how client-side persistence actually behaves and what it owes — storage discipline tiers,
legitimate-vs-drifted dual contracts, the bypass-inventory shape specific to storage, and
URL-state synchronization — from a corpus grounded in real field reports across four repos
(ultimate-tokens, agent-ui, gen-ui-kit, adia-v2), not general storage-library folklore.

| Ask | Load |
|---|---|
| Does this persisted key need schemaVersion/migration rigor, or is ad-hoc JSON.parse enough | `references/discipline-tiers.md` |
| A field rename might silently drop saved data — is that risk real here | `references/discipline-tiers.md` |
| A sync store sits on top of an async storage seam — bypass or legitimate design | `references/dual-contracts.md` |
| How to run a bypass audit specifically for storage/persistence code | `references/persistence-audit-shape.md` |
| Should this filter/search param live in the URL; PHI exclusion; push vs. replace | `references/url-state-sync.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask against the four axes above; load only the matching reference (or
   `sources.md` for provenance). Hunting one specific claim inside a file: Grep for the term first
   rather than reading the whole file.
2. Answer on the contract: **claim + cited file:line/report + the grounding marker
   ([verified]/[incident])**. Worked shape:
   > *"We're about to rename a field this store persists — do we need a migration?"* →
   discipline-tiers ask → `discipline-tiers.md` — check which tier the key is in: a tier-1
   (schemaVersion + RENAME_MAPS) store already has a translate-forward path; a tier-2 (ad-hoc
   JSON.parse) store does not, and the exact failure this axis names — a rename shipped without a
   matching translate-forward entry — silently dropped every user's override on their next
   save/reload [incident].
3. State which axis the answer draws from, and its grounding marker — never present a corpus
   citation as live-verified-today code if `sources.md`'s own disclosure says otherwise.
4. Route architecture-judgment or reactivity-mechanism work at the boundary (below) — this pack
   answers persistence facts, it never judges app-tier state architecture generally or explains a
   reactivity kernel.

## Boundaries

- **This skill answers client-PERSISTENCE facts; it does not judge app-tier state ARCHITECTURE
  generally.** "Why is our state a mix of implementations", "is this store actually used or just
  built", "did we ever revisit this decision", "two places both claim to own this field" are
  `state-model-rules`' law — that pack's `audit-technique.md` already teaches the general
  bypass-inventory METHOD reusable across any sanctioned seam (routing, DI, data-fetching, or
  storage); this pack's `persistence-audit-shape.md` is the narrower, storage-specific checklist
  of what to grep for once the seam in question is specifically persistence — cite the parent
  method there rather than re-deriving it. A question naming a specific storage key, a rename, a
  schemaVersion, or a URL param is this pack's; a question naming stacked generations, adoption of
  a non-storage layer, or a doctrine/practice gap across a whole app is `state-model-rules`'.
- **This skill does not explain reactivity MECHANISM.** "Why did this effect refire twice",
  "computed vs signal vs effect", "guard a stale async response" are `reactivity-facts`' law —
  this pack explains what gets WRITTEN to storage and when that's disciplined; `reactivity-facts`
  explains the kernel that decides WHEN a write fires. A question naming a kernel primitive
  (signal/computed/effect/scope/sequence token) is `reactivity-facts`'.
- **UI pattern naming and the screen-state grammar** (loading/empty/error) stay
  `ui-pattern-facts`' law — unrelated territory.
- **How data gets CONNECTED to a UI element or across a bridge belongs to `data-wiring-facts`** —
  the attribute-driven streaming stack, the postMessage bridge protocol, no-DI substitutes, and the
  need→pattern wiring menu. That pack answers how data gets wired in; this pack answers what gets
  WRITTEN once it's there. A question naming a stream, a bridge message, or a wiring pattern is
  `data-wiring-facts`'; a question naming a storage key, schemaVersion, or URL param is this
  pack's.
- **Production storage code, a migration script, or a URL-state module from scratch** → no owning
  builder skill in this plugin (the same gap `reactivity-facts`/`state-model-rules` name for their
  own territory) — derive the implementation inline against whichever axis file names the
  failure mode to avoid.

## Extending this pack

Extension: governed by [[make-pack]]
