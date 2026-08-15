---
name: naming-conventions
kind: skill
description: >
  The harness artifact naming convention — grammar, frontmatter schema (incl.
  the allowed-tools/tool-grant syntax), folder layout, and migration rules
  for .claude/ estates. Consult when parsing or judging any artifact name,
  authoring frontmatter or its tool-grant syntax, deciding where content
  lives in a skill folder, or resolving one artifact's rename/migration
  rule. NOT for planning or generating an estate-wide
  overhaul/reshape/merge/split campaign across many members
  (overhaul-planning); NOT for naming something new or simplifying a name in
  plain English, pre-ADR-0011 (harness's naming-rules). Single authority the
  authorkit skills cite; never restate its rules from memory.
author: kim
created: 2026-08-13
last_updated: 2026-08-14
disable-model-invocation: false
user-invocable: false
---

# naming-conventions

Reference corpus. This skill has no procedure — its body is the index below.
Load only the file whose *read-when* condition fires; never bulk-load.

Core commitments, for orientation before any file loads:

- **Three kinds, partitioned by invoker.** Command = user (`/name`), skill =
  model (description match), agent = delegated. Knowledge is a content
  pattern (reference-shaped skill), not a kind, subtype, or suffix.
- **One reserved head:** `-agent`. Kind is decided by directory; the grammar
  corroborates; frontmatter must agree and never decides.
- **One canonical name** everywhere: folder == file stem == frontmatter name.
- **Relations live in frontmatter** of the depending artifact; the graph is
  compiled, never hand-maintained.

## References

| File | Read when |
|---|---|
| GRAMMAR.md | parsing, classifying, or minting any artifact name; resolving lexicon or ObjectVocab questions; judging a name violation |
| FRONTMATTER.md | authoring or checking frontmatter fields, relations, invocation policy, tool grants, or provenance |
| LAYOUT.md | deciding where a file belongs inside a skill folder; authoring a reference index; judging layout violations; organizing corpora, templates, schemas, or procedures |
| MIGRATION.md | auditing a legacy estate; managing the exemptions array; planning or sequencing renames |
| TOOL-GRANTS.md | writing or validating allowed-tools / tools declarations; checking grant syntax against the installed harness version |
| MANIFEST-TEMPLATE.json | seeding naming.manifest.json into a new target estate (copy, then edit lexicons and AuthorRegistry) |
