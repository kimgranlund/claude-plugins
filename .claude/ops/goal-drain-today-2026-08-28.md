# /goal drain-today's-filings run — 2026-08-28

Started by plugins-marshal (plugins-c4), turn 1. Cap: 20 turns or 3 hours.

Scope (frozen snapshot, never a live query): #964 #973 #974 #977 #978 #979 #980.

Plugin per ticket (title-inference failed for all 7 via dispatch_envelope.py — resolved manually
from ticket body/title):
- 964 harness | 973 teamwork | 974 docs | 977 teamwork | 978 cross-cutting (no single plugin —
  touches workspace .claude/docs/adr/, not owned by the docs plugin's own directory per this
  repo's docs-root override) | 979 teamwork | 980 teamwork

4 teamwork tickets means serializing those across waves (never 2 same-plugin concurrent).

Wave plan (max 2 concurrent):
- Wave 1: 964 (harness) + 973 (teamwork)
- Wave 2: 974 (docs) + 977 (teamwork)
- Wave 3: 978 (cross-cutting, no version slot) + 979 (teamwork)
- Wave 4: 980 (teamwork) alone

All dispatches carry `auto-merge: authorized`, no `accept-grant: authorized` (same as the
drain-the-board run — marshal runs the real accept-marker round each time). 978 dispatched with
the goal's own SPECIAL CASE latitude (too-big-for-one-build is a legitimate SKIPPED/BLOCKED
outcome, not forced into the single-PR shape).

## Status (updated each turn)

| Ticket | Plugin | Build seat | Dispatched | Status | PR | Merged |
|---|---|---|---|---|---|---|
| 964 | harness | build-964 | turn 1 | PR #981 open, awaiting claude-review | #981 | no |
| 973 | teamwork | build-973 | turn 1 | dispatched | — | — |
| 974 | docs | build-974 | — | queued (wave 2) | — | — |
| 977 | teamwork | build-977 | — | queued (wave 2) | — | — |
| 978 | cross-cutting | build-978 | — | queued (wave 3) | — | — |
| 979 | teamwork | build-979 | — | queued (wave 3) | — | — |
| 980 | teamwork | build-980 | — | queued (wave 4) | — | — |

## Findings this run

## Spend-ledger rows appended this run

(see .claude/ops/spend-ledger.csv, event_kind=build for each dispatch, event_kind=merge for each
close)
