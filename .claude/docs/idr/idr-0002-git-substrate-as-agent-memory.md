---
doc-type: idr
id: idr-0002
status: draft
date: 2026-08-16
owner: kim.granlund
proof-ref: harness/skills/check-state/SKILL.md
supersedes: null
---
# IDR-0002 — The git substrate is the durable memory agents cold-start from

## Claim

The git substrate — Issues, PRs, CI, worktrees, and the ADR ledger — serves as the durable memory
autonomous agents cold-start from: a fresh session can recover work-state, standing decisions, and
next actions from the repo alone, without a human re-explaining context. A session that needs
human re-orientation to proceed, despite these records, is the failure case the Proof measures.

## Why

Provenance: derived-from-evidence — ADR-0002 (Issues as the work-item canon, PRs as the merge
gate, CI mirroring local gates), the ADR-0003/0004/0005 chain (backend generalization, native
issue types, the claim protocol against duplicate agent work), and `harness:check-state`, built
to answer the cold-start question ("catch me up on this repo"); `what-shipped` covers the
adjacent activity-window recovery. The escalating investment in git-native records only pays off
if this belief holds; it has never been written down as the bet it is.

## Proof

Instrument: `harness/skills/check-state/SKILL.md` (the proof-ref). A cold-session orientation
trial: passes if, across at least three cold sessions, every blocked-on-you and ready-to-close
item the human independently identifies appears in the fresh session's `check-state` report with
zero orientation input; fails on any session needing human re-orientation to proceed.
