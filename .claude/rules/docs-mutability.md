# Functional docs — mutability + refactor-attic handling

**Path scope:** `.claude/docs/**` (ADR/PRD/SPEC/LLD and the rest of the functional-doc tree),
`**/.refactor-attic/**`.

Functional documents follow docs' type contracts and mutability classes — the accepted-ADR
append-only rule (doc_lint T4) was hook-enforced until enforcement retired 2026-08-17 (#466,
remove-all-hooks directive); it now runs only at `docs_check.py`/release-gate time (G10), never
per-write. Supersede, never edit, an accepted ADR.
`.refactor-attic/` directories are the undo for non-git-reversible merges — never deleted
casually.

**Docs-root override (ruled 2026-08-17, issue #514).** docs' `doc-writing-rules` ladder defaults
repo-level records to `docs/ops/`; THIS workspace overrides that at rung 1 — everything stays
under `.claude/docs/`, because the `docs` plugin directory already owns the bare `docs/` path and
a `docs/ops/` root would collide with the plugin's own name.

Split from CLAUDE.md (issue #262, 2026-08-16).
