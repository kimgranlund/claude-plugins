# Overhaul run — 2026-08-19 (target: CLAUDE.md)

Driver: plugins-marshal. Argument `CLAUDE.md` resolves to the workspace-root entry-file estate:
the root CLAUDE.md (~10.8k chars / 111 lines, loaded EVERY turn of EVERY session) plus its
pointer targets `.claude/rules/*.md` (5 files, ~4.8k chars, loaded only when followed).

## Scope (Phase 0 — pending gate 1)

| root | markers | classification | recommended | why |
|---|---|---|---|---|
| workspace root CLAUDE.md | entry file, every-turn resident | governed (entry-file-rules canon; /check-entry-file owns the audit) | IN | the named target; ~2.7k tokens billed per turn per session |
| .claude/rules/*.md (5) | path-scoped pointer targets | governed | IN | CLAUDE.md's own down-stack; trims usually move content here |

Instrument note: naming/attention audits don't apply to an entry file — the owning instruments
are harness `/check-entry-file` (classification against entry-file-rules) + authorkit
bloat-audit (ceremony/restatement). Doctrine axis: root manifest edges D01–D13 — none names
CLAUDE.md; absent. Pattern axis: absent (no pattern named).

## Gates
- Gate 1 (scope): PENDING
