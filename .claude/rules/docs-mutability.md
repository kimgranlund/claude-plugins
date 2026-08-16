# Functional docs — mutability + refactor-attic handling

**Path scope:** `.claude/docs/**` (ADR/PRD/SPEC/LLD and the rest of the functional-doc tree),
`**/.refactor-attic/**`.

Functional documents follow docs' type contracts and mutability classes — the accepted-ADR
append-only rule is hook-enforced (doc_lint T4): supersede, never edit, an accepted ADR.
`.refactor-attic/` directories are the undo for non-git-reversible merges — never deleted
casually.

Moved from the workspace CLAUDE.md's "Docs and ledgers" invariant (issue #262, 2026-08-16) — the
work-items-are-GitHub-Issues fact stayed in CLAUDE.md as always-relevant core (it governs where
any task's own record lives, not just doc-tree edits); this file carries only the part that's
true specifically inside the doc tree or a refactor-attic directory.
