# The persistence-specific bypass-inventory audit shape

**Fence first:** `state-model-rules`' `audit-technique.md` already teaches bypass inventory as a
general, cross-domain METHOD — for ANY sanctioned seam (routing, dependency injection, data
fetching, persistence, or anything else with a "the one seam every consumer reaches for"
contract), list real consumers vs. bypasses and state an adoption verdict per layer. That method
is the parent; cite it, don't restate it. This axis is narrower: what to grep for and how to read
the results once the sanctioned seam in question is specifically a STORAGE seam.

## What the general method misses if applied to persistence without adaptation [verified]

A plain "grep the import graph for the sanctioned module" pass (the general method's own
recommended first step) under-counts persistence bypasses, because a storage bypass rarely imports
anything at all — it just calls `localStorage.setItem`/`getItem` or `indexedDB`/`clientStorage`
directly with a literal string key. There is no import edge to grep for. The persistence-specific
adaptation is:

1. **Grep for the literal storage-backend calls themselves**
   (`localStorage.`, `sessionStorage.`, `indexedDB`, `clientStorage.`) across the whole tree first
   — not for imports of the sanctioned adapter — since every bypass necessarily makes one of these
   calls directly while a sanctioned consumer only calls the adapter's own wrapper.
2. **Cluster the hits by KEY-NAME PREFIX, not by file.** Reading bypasses file-by-file hides the
   real tell; reading them clustered by literal key/namespace string surfaces it immediately.
3. **Screen out non-product noise before counting.** A test harness's own `localStorage.clear()`
   call, or a doc-page's illustrative dead code, is not a bypass — exclude it explicitly rather
   than let it inflate the count, exactly as a real survey of this kind disclosed doing.

## The namespace-collision tell [incident]

Clustering by key-name prefix is what surfaces the single strongest persistence-specific signal:
**near-identical UI regions that each invented their own storage namespace instead of sharing
code.** One survey found sidebar collapse/resize state persisted THREE separate times across
three near-identical shell regions (an admin sidebar, a chat sidebar, an editor sidebar) — each
under its own distinct literal key prefix, each with its own hand-rolled drag-handle/resize
internals, one of the three delegating resize to an inner shared pane component while the other
two did not. Nothing about any single sidebar's code looks wrong in isolation; the finding only
surfaces once the three literal key-prefix strings are laid next to each other and read as one
question — "why does the identical UI behavior need three different storage identities?" — rather
than three separate small implementations each read on their own merits.

## Extra columns worth adding to the sanctioned-vs-bypass table, persistence-specific [verified]

Beyond `state-model-rules`' generic table shape (Home / What it stores / real-consumer-or-bypass),
a persistence audit specifically benefits from two more columns:

- **Does the bypass also reimplement validation, not just read/write?** A bypass that duplicates
  an entire hand-rolled store implementation — its own get/set/remove plus a manual key-prefix
  scan for version/modified markers — is a heavier finding than a bypass that merely reads/writes
  a single key directly; the first is a full parallel implementation of the sanctioned seam's own
  job, the second is a narrower, easier-to-migrate gap.
- **Is the same literal key/attribute name targeted by both an automatic (document-level) starter
  and a manual bypass at once?** This is a double-write/double-fetch hazard distinct from ordinary
  drift — worth flagging as its own severity tier when found, since it can corrupt state rather
  than merely duplicate code.

## Running it

Grep the four literal backend calls tree-wide → cluster by key-name prefix → screen out
test/ops noise → for each cluster, name real-consumer-or-bypass, whether it reimplements
validation, and whether it collides with an automatic starter → roll up a persistence-specific
adoption verdict (built-but-unadopted / load-bearing-with-bypasses / genuinely clean) per
sanctioned seam, feeding the same verdict vocabulary `state-model-rules`' `adoption-verdict.md`
already defines.

## Sources

`/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/data-persistence-layers.md`
— "Bypass inventory" table and its screened-out test-harness row;
`/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/02-web-modules-state.md`
— "Inconsistencies" #1 (`data-stream-src` double ownership) and #3 (sidebar collapse/resize/persist
implemented three times); cross-referenced against
`/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
("F8 — Three sidebar persistence implementations"). Reviewed 2026-08-20.
