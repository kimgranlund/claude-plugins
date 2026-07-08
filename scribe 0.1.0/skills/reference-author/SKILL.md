---
name: reference-author
description: >
  Author or review a referential knowledge document (a skill references/ file,
  an @-imported doc, or a Project Knowledge file) to production standard, scoring
  it against the bundled rubric. Use whenever writing or evaluating knowledge /
  ground-truth docs for an agent: "write a reference doc", "structure my project
  knowledge", "name and organize the knowledge files", "is this retrievable",
  "does this reference duplicate a source owned elsewhere", "audit our docs for
  drift". NOT for a knowledge pack / corpus+index (knowledge-author), NOT for a
  docs index (llms-txt-author), NOT for CLAUDE.md standing context (entry-file-author).
disable-model-invocation: false
user-invocable: true
---

# Harness — Reference (Knowledge Doc) Authoring & Review

A reference is ground truth the agent consults — *retrieved, never obeyed*. Author one that retrieves well and resists drift, or review one.

## Operating model (essentials; depth in `references/foundations.md`)
- Referential, not behavioral: it grounds and informs; directives belong in skills/CLAUDE.md.
- Canonical or derived, never a hand-maintained duplicate — duplication is the precondition for drift.
- Write for retrieval: headed, scannable, short declarative statements, one topic.

## Author
1. Scope to one domain; point to siblings rather than sprawl.
2. Head every section; consistent terminology; make it canonical or explicitly derived from a named source.
3. Date/version anything volatile.
4. Self-score (below); fix until every gate dimension (D1, D3, D5) ≥ 3.

## Review
1. Run the mechanical gates: `python scripts/harness_checks.py reference <path>`.
2. Score the `[review]` dimensions against `references/rubric.md`. Check first for a hand-maintained duplicate (the top failure).
3. Findings by severity; gate verdict; top issues with a concrete fix each.

## Improve
Take the review's findings lowest-gate-first (D3 duplication, then D1 retrievability, then D5 freshness). A duplication fix is a de-duplication: pick the canonical home and make the other side cite or derive from it — never harmonize two copies. Re-run the harness and re-score until the gates clear.

## Update
When the source a reference derives from changes, re-derive the reference from that source in the same change — never patch its prose to approximate the new truth. Refresh the date/version marker as part of the re-derivation; an updated body under a stale marker hides exactly the drift D5 exists to catch.

## Output contract (review)
```
Artifact: <reference>  ·  Rubric: rubric-reference
| Dim | Type | Score | Finding | Evidence |
Gate (D1,D3,D5): <pass/fail>   [harness_checks: <pass/fail>]
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `scripts/harness_checks.py reference` | Mechanical gate checks (headings, freshness marker) |
| `references/rubric.md` | The `[review]` dimensions and anchors |
| `references/best-practices.md` | Covers references and llms.txt — canon home here in reference-author; llms-txt-author symlinks in |
| `references/resource-knowledge-naming-conventions.md` | Naming knowledge files, records, and indexes in a corpus (type by mutation semantics first) |
| `references/foundations.md` | When a finding turns on a shared model |

## Generator ≠ critic

A high-stakes reference doc you authored gets an independent pass: dispatch the shared
`doc-reviewer` agent for the fresh-context score against `references/rubric.md`, and the
`linguistics-reviewer` agent for the wording layer — retrieved-never-obeyed is the reference's
*directive* status, but its wording still conditions every model that reads it, so the potency
rubric applies; the maker applies the fix.

**Done** = harness passes, every gate dimension (D1, D3, D5) ≥ 3 with cited evidence, one topic,
canonical or explicitly derived, volatile facts dated. **NOT done** = a hand-maintained duplicate,
behavioral directives posing as ground truth, or an undated fact quietly going stale.
