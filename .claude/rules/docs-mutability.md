# Functional docs — mutability + refactor-attic handling

**Path scope:** `.claude/docs/**` (ADR/PRD/SPEC/LLD and the rest of the functional-doc tree),
`**/.refactor-attic/**`.

Functional documents follow docs' type contracts and mutability classes — the accepted-ADR
append-only rule (doc_lint T4) was hook-enforced until enforcement retired 2026-08-17 (#466,
remove-all-hooks directive); it now runs only at `docs_check.py`/release-gate time (G10), never
per-write. Supersede, never edit, an accepted ADR.
`.refactor-attic/` directories are the undo for non-git-reversible merges — never deleted
casually.

Moved from the workspace CLAUDE.md's "Docs and ledgers" invariant (issue #262, 2026-08-16) — the
work-items-are-GitHub-Issues fact stayed in CLAUDE.md as always-relevant core (it governs where
any task's own record lives, not just doc-tree edits); this file carries only the part that's
true specifically inside the doc tree or a refactor-attic directory.
