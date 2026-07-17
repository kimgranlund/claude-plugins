# Sub-issues vs. task-list checkboxes — decomposing a work item

## Sub-issues is GA, and its Markdown-checkbox predecessor is retired

[verified, github.blog changelog, 2026-07-17] Sub-issues shipped public beta 2024-09-30, public
preview 2025-01-12, REST API support 2024-12-12, and **general availability 2025-04-09** — the same
release wave as Issue Types. It formalizes parent-child hierarchy: up to **8 levels of nesting**,
up to **100 sub-issues per parent** (raised from 50 at GA).

[verified, github.blog changelog, 2026-07-17] The older mechanism — Markdown **tasklist blocks**
(a distinct, richer feature from plain `- [ ]` checkboxes, with `Tracked`/`Tracked by` fields in
Projects) — was **discontinued 2025-04-30**. Past that date tasklist blocks render as raw
Markdown, not interactive checklists. [verified] Plain Markdown checkbox syntax (`- [ ] #123`)
itself still works as ordinary Markdown with GitHub's issue-reference unfurling and
automatic-check-on-linked-close behavior — only the richer *tasklist block* feature was retired.

## The mechanical difference

| | Sub-issues | Task-list checkbox referencing an issue |
|---|---|---|
| Relationship | Formal parent-child hierarchy | Loose reference; no ownership implied |
| Depth | Up to 8 levels | Flat (a list item can reference an issue, not become one) |
| Progress tracking | Native rollup in the parent issue AND in Projects | Manual; checkbox flips when referenced issue closes |
| Cross-org | Supported — a sub-issue can belong to a different org than its parent | N/A (a reference is just a link) |
| API | Full REST + GraphQL: add/remove/reprioritize | None — it's Markdown text |
| Filter syntax | `has:sub-issues-progress`, `has:parent-issue` | None |

[verified, docs.github.com, 2026-07-17] GitHub's own guidance: use sub-issues "when you need
hierarchical, multi-level task breakdown; tasks need to be tracked as individual issues with their
own metadata and discussions." [inferred, from feature design + the tasklist-block retirement] Use
a plain Markdown checkbox only for a lightweight item that doesn't warrant its own issue at all
(and can be promoted to a sub-issue later — GitHub explicitly supports converting a checklist item
directly into a sub-issue).

## Distinct from cross-references / simple issue linking

[verified, docs.github.com, 2026-07-17] A cross-reference (mentioning `#123` anywhere) creates a
loose backlink between two independent issues — no hierarchy, no ownership. Sub-issues are for
decomposition; cross-references are for association. Don't conflate the two: "see also #123" is a
cross-reference; "this is part of #123" is a sub-issue relationship.

## Workspace mapping

TICKET Scope/Open decomposition against sub-issues → `bug-task-feature-mapping-nuances.md`
Finding 3.
