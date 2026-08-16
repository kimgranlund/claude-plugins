# Tool grants — verified syntax for the installed harness

Verified against Claude Code as of 2026-08-13. Grant syntax is harness
surface area that evolves; re-verify on harness upgrades and bump
last_updated on this skill when this file changes. The validator checks
grant SEMANTICS (coherence, scoping) against this file's rules; it treats
exact matcher syntax as harness-owned.

## Fields

- Commands: `allowed-tools:` (YAML list or comma string) in frontmatter.
- Agents: `tools:` (comma string) in frontmatter.
- Skills: `allowed-tools:` honored at skill scope on current harness
  versions; where unsupported it is inert and the enclosing session's
  grants apply — declare it anyway; the declaration is the contract.

## Scoping

- `Bash(pattern *)` scopes a shell grant to a command pattern:
  `Bash(git mv *)`, `Bash(python */scripts/validate.py *)`.
- Unscoped `Bash` is banned estate-wide (validator error).
- Write-capable set for coherence checks: Edit, Write, MultiEdit,
  NotebookEdit, unscoped Bash.

## authorkit's own grants (the reference implementation)

| Artifact | Grants | Why |
|---|---|---|
| naming-audit (skill) | Read, Glob, Grep, Bash(validate.py) | read-only diagnostic |
| estate-audit-agent | union of its 4 instruments' read-only script grants | mirrors performs target; parameterized by `instrument` |
| rename-planning | Read, Glob, Grep, Bash(git log *), Bash(git grep *) | read-only + history |
| manifest-authoring | Read, Edit/Write scoped to naming.manifest.json | one file |
| rename-execute | Read, Glob, Grep, Edit, Write, Bash(git mv *), Bash(validate.py) | THE mutation point, behind confirm |
| exemption-retire | orchestrates; grants of what it chains | no independent writes |
