---
doc-type: idr
id: idr-0001
status: locked
date: 2026-08-16
owner: kim.granlund
proof-ref: harness/scripts/release_gate.py
provenance: derived-from-evidence
supersedes: null
---
# IDR-0001 — A mechanized incident class stays gone

## Claim

Once an incident class this estate hits — a load failure, a false positive, a silently skipped
step — has been converted into a lint rule, gate check, or selftest fixture in the self-hosted
gates (harness's own gates governing every plugin, including harness itself), that class does not
recur. A ledger entry re-fixing a previously-mechanized class after its gate landed falsifies the
claim.

## Why

Provenance: derived-from-evidence — the workspace CLAUDE.md ("harness is the toolchain: its
commands and standards govern work on every plugin in this workspace, including harness itself"),
whose "Incident → infrastructure, same day" invariant is the supporting practice built on this
belief; the "Ship only through the gate" and CI-mirrors-the-local-gates invariants (CLAUDE.md;
`.github/workflows/gate.yml`); and `.claude/rules/scripts.md` (every bundled script carries a
green selftest). The estate has operated on this belief since inception, but no record states it
as a falsifiable claim. Doubt would come from incident classes that resist mechanization, or
mechanized checks that rot without ever catching anything.

## Proof

`harness/scripts/release_gate.py` (the full gate set) plus the per-plugin README footer ledgers:
falsified by a ledger entry re-fixing a previously-mechanized incident class, dated after that
class's gate landed.
