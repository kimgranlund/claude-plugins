# Orchestration rubric — A6: scheduled routines + `/goal` loops (unattended continuation)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

## Architecture & intended use

Cron/cloud routine or goal loop fires with no live user. Intended use: recurring drains and
bounded overnight work.

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A6-R1 | Verifiable end-state + turn caps | `loop-rules` rubric | judgment |
| A6-R2 | Explicit unattended grant: the literal `auto` token / `auto-merge: authorized` line — set by the dispatcher, never inferred | ADR-0012 | mechanizable — built: `orchestration-audit`'s `check_grant_literal` confirms BOTH doctrine strings appear verbatim in the canon skills that state this rule (`dispatch-ticket`'s `auto-merge: authorized` line, `mobilize-chores`' `/mobilize-chores auto` line) — checked as two genuinely INDEPENDENT literal presences, never one as a substring of the other. This proves the DOCTRINE TEXT still states the rule; it does not (yet) inspect any one LIVE dispatch prompt for inferred-grant language — that half stays **mechanizable — not built** |
| A6-R3 | Ceiling discipline: PR-opened default; the quick-build carve-out predicate in FULL | ADR-0012's eight QB conjuncts | mechanizable — not built (would grep the calling skill for evaluation of all eight QB0–QB7 conjuncts before any merge sequence, flagging a partial-predicate short-circuit) |
| A6-R4 | No-live-user branches: gates report blocked rather than auto-answering | `fleet-bootstrap` Phase 3 pattern; `find-open-questions`' unattended skip | judgment |
| A6-R5 | Environment verified: the cloud runtime actually has the plugins/tools the routine needs | the daily-board-drain `enabled_plugins`-empty risk — still an open first-run watch | judgment |
| A6-R6 | Duplicate-firing guard | `sweep_guard`'s marker protocol | mechanizable — not built (would grep the routine's own script for the guard-marker check before its main body runs) |

**Owning checker for A6:** `loop-rules` itself is the design-time rubric (Design/Review
gates D2/D4 ≥ 3); no separate runtime checker exists — A6-R1/A6-R4/A6-R5 stay judgment-queued
to a human review of an actual run's transcript/ledger.
