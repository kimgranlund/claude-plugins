---
doc-type: adr
id: adr-0009
status: accepted
ratified: by Kim
date: 2026-07-30
owner: kim.granlund
supersedes: adr-0006 (the find-the-ask row of its member rename map only)
---
# ADR-0009 — Rename find-the-ask to find-intent

## Context

ADR-0006 renamed `forge:intent-extract` to `harness:find-the-ask` (2026-07-21). On
2026-07-30 Kim ruled the colloquial noun reads as "too weird" in daily use and asked for
the old clarity back. The originally proposed `extract-intent` fails naming-rules test 3 —
`extract` is a retired synonym of the registry verb `find` — so the canon-compliant form
of the same intent is `find-intent`: registry verb, plain noun, verb-first runnable shape.
Kim chose `find-intent` over keeping `find-the-ask` and over un-retiring `extract`
(AskUserQuestion round, this date).

## Decision

1. `harness:find-the-ask` is renamed `harness:find-intent`. The verb registry is
   unchanged — `extract` stays retired under `find`.
2. Execution follows the rename-execution playbook's eight-item same-change contract
   (ADR-0007 Decision 2 binds it): frontmatter+path together, live references rewritten,
   reciprocal fences re-closed, blind eval-run before and after at parity or better,
   MAJOR bump for harness, bump+ledger for every touched sibling, gates clean, and
   `renames.json` re-derived — never hand-edited — in the same PR.
3. Historical records keep `find-the-ask` and `intent-extract` byte-identical: ADR-0006,
   README footer ledgers, `estate-rename-map.md`, `.claude/ops` records.

## Consequences

- The rename chain `intent-extract → find-the-ask → find-intent` is representable in the
  derived manifest; consumer repos migrate via `fix-old-names`, which chains multi-hop
  renames.
- `grill-the-ask` (teamwork) keeps its name — "the ask" remains legal vocabulary where it
  IS the term being grilled; this ADR renames one member, not the noun estate-wide.
- Doctrine pointers naming `find-the-ask` outside this repo (the user-scope CLAUDE.md
  pointer block) go stale on merge and are repaired alongside, disclosed in the PR.
