---
name: llms-txt-forge
description: >
  Author or review an llms.txt (and llms-full.txt) — the agent-facing map of a
  documentation corpus — to the standard shape, scoring it against the bundled
  rubric. Use whenever the user mentions llms.txt, an AI-facing docs index, agent
  discovery of docs ("agents can't discover where our documentation lives"),
  "make our docs agent-readable / discoverable", "generate an llms.txt", "review
  our llms.txt", or an llms.txt that is a list of concepts with no links. NOT for
  the docs themselves (reference-forge).
disable-model-invocation: false
user-invocable: true
---

# Harness — llms.txt Authoring & Review

`llms.txt` is the curated index that tells agents where a corpus's authoritative content lives. Author one to the standard shape, or review one.

## Operating model (essentials; depth in `references/best-practices.md`)
- Index, not content delivery: `/llms.txt` is the lean table of contents; `/llms-full.txt` carries the full corpus.
- Descriptions are what the agent routes on — one accurate sentence per link beats coverage.
- Serve at root so tools discover it without prior knowledge.
- The corpus it indexes is authored with `[[reference-forge]]` (knowledge / ground-truth docs) and a repo's docs-site skill (agent-ui carries `docs-author` repo-locally — the published site); this maps what they produce.

## Author
1. Standard shape: H1 project name → blockquote summary → H2 sections, each a list of links with a one-line description.
2. Curate to authoritative content; exclude chrome; ensure links resolve to markdown; split the heavy corpus into `llms-full.txt`.
3. Self-score (below); fix until every gate dimension (D1, D2, D6) ≥ 3.

## Review
1. Run the mechanical gates: `python scripts/harness_checks.py llms-txt <path/to/llms.txt>`.
2. Score the `[review]` dimensions against `references/rubric.md`. The top failure is a list of concepts with no links.
3. Findings by severity; gate verdict; top issues with a concrete fix each.

## Improve
Take the review's findings lowest-gate-first (D2 dead or missing links, then D1 shape, then D6 placement). A link fix is a curation decision — resolve it, replace it, or cut the entry; never leave a concept unlinked. Re-run the harness and re-score until the gates clear.

## Update
An llms.txt is a derived view of its docs corpus — when the corpus moves (pages added, renamed, restructured), re-derive the index from the corpus rather than patching entries: re-walk the authoritative pages, regenerate the sections and descriptions, and rebuild `llms-full.txt` in the same pass. A hand-patched index over a moved corpus is exactly the drifted map this skill exists to prevent.

## Output contract (review)
```
Artifact: <llms.txt>  ·  Rubric: rubric-llms-txt
| Dim | Type | Score | Finding | Evidence |
Gate (D1,D2,D6): <pass/fail>   [harness_checks: <pass/fail>]
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `scripts/harness_checks.py llms-txt` | Mechanical gate checks (H1 + blockquote + H2 + links) |
| `references/rubric.md` | The `[review]` dimensions and anchors |
| `references/best-practices.md` | Covers references and llms.txt — canon home: reference-forge; this bundle symlinks in |
| `references/foundations.md` | When a finding turns on a shared model |

## Generator ≠ critic

A high-stakes llms.txt you authored gets an independent pass: dispatch the shared
`doc-reviewer` agent for the fresh-context score against `references/rubric.md`, and the
`linguistics-reviewer` agent for the wording layer (the link descriptions are what agents route
on; potency rubric); the maker applies the fix.

**Done** = harness passes, every gate dimension (D1, D2, D6) ≥ 3 with cited evidence, every entry
linked and described in one accurate routing sentence, served at root. **NOT done** = concepts
without links, an index that dumps content, or an llms.txt that lags the corpus it maps.
