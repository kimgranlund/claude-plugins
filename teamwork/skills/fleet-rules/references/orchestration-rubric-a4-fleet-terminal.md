# Orchestration rubric — A4: fleet terminal seats ({repo}-marshal / reviewer / planner / product)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

## Architecture & intended use

Human-driven terminals + a marshal, registered in `fleet.json`/`fleet-roster.md`. Intended
use: multi-seat campaigns where a human steers seats interactively (#410 addendum 3).

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A4-R1 | Registration discipline: every live seat has a roster row; takeover-vs-collision rule honored | #423 class; `fleet-bootstrap` Phase 1 | mechanizable — built (partial): `orchestration-audit`'s `check_roster_rows` counts `fleet-roster.md`'s own parseable data rows and reports `fail` if none exist — it does NOT yet cross-reference against `git worktree list` or a live-session list (that reconciliation half is **mechanizable — not built**, a real future check) |
| A4-R2 | Record over nudge: `SendMessage` is a nudge, never the record | `fleet-rules` Part A §3 | judgment |
| A4-R3 | Peer scope: messaging only registered fleet seats | fleet-scoped coordination ruling | judgment |
| A4-R4 | Hard gates hold unattended: no-live-user at a ratification gate → blocked, reported | — | judgment |
| A4-R5 | Isolation reality: per-seat worktrees + the #490 pin-race mitigation ladder known and applied | tonight: 3 sessions wedged; scratch-clone + Git-Data-API rungs both exercised | judgment |

**Owning checker for A4:** `wiring-checker` for the arrangement's own composition; A4-R2/A4-R3/
A4-R4/A4-R5 are conduct/judgment calls a human or `fleet-marshal` makes in the moment, never
mechanically graded after the fact.
