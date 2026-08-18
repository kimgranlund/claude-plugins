# The organizing axis: who holds the plan

Cited from `SKILL.md`'s Part B, right before Design step 1 (F6 split: the table + tree below
don't fit the 500-line body cap) — a design-step aid, consulted before picking a unit, never a
scoring rubric. The per-archetype rubrics' own X-R4 criterion
(`orchestration-rubric-a{1-8}-*.md`, cited from each file's own header) scores whether an
arrangement's design actually worked this table and tree out, never assumes it (issue #671,
2026-08-18 — harvested substance, never authority, from an external agent-classes doc; the cost
gradient below cites `authorkit:spend-audit`'s own measured #673 figures, never that doc's
[reported] folklore numbers).

Every unit differs on one primary axis — *who holds the plan* — plus three secondary axes:
worker↔worker comms, file isolation, and lifetime.

| Unit (this estate's archetype) | Plan holder | Worker↔worker comms | File isolation | Lifetime |
|---|---|---|---|---|
| Solo host, inline skills (A1) | Host, turn-by-turn | N/A — no workers | None; host's own tree | Within session |
| Unnamed fan-out (A2) | Host, single dispatch step | None — report to caller only | Same tree when slices are file-disjoint and the host owns git (Design step 5); worktree per worker only when a worker drives its own branch/commit lifecycle | Within session |
| Named background seats (A3) | Host, negotiated turn by turn | Direct `SendMessage` + mailbox | Ownership partition — never shared-write | Cross-session, coordinated |
| Fleet terminal seats (A4) | The human, via the marshal | Peer messaging + `fleet.json`/roster ledger | Per-seat worktree/branch | Cross-session, human-steered |
| Forked intake (A5) | The fork itself, one-shot | None | None — runs in the host's own tree | Within the fork's own run |
| Scheduled routines / `/goal` loops (A6) | The loop/schedule, unattended | None beyond the durable record | Per-run worktree | Recurring, unattended |
| Workflow scripts (A7) | The script | None — the script routes data | Script's own responsibility | One scripted run |
| `/batch` (A8) | Host, after a plan-approval gate | None — units are peer-independent | Per-unit worktree, always | Within one batch wave |

Authorship weight shifts the same direction down this table as it does across the whole estate:
solo/subagent units are agent-heavy (who the worker is carries the weight), workflow/batch units
are artifact-heavy (what the plan is carries the weight) — the same shift `authorkit:spend-audit`'s
own #673 measured cost gradient prices for this estate (cited there, never re-derived here).

## The 6-line topology decision tree

A design-step aid, not a scoring rubric — run it before picking a unit, not after grading one.
First match wins, same discipline as `SKILL.md` Section 7's routing precedence: never skip ahead
on a guess, and never let a template default reach for a heavier unit than the tree names.

```
Workers need to negotiate/coordinate directly?       → Named seats (A3) / fleet terminal (A4)
Plan is a repeatable script, scale past ~10 workers? → Workflow scripts (A7)
Work outlives your attention, artifact = done?       → Scheduled loop (A6) / forked intake (A5)
Units independent + enumerable up front?             → Unnamed fan-out (A2) / `/batch` (A8)
One bounded side-quest, result-only?                 → A single subagent dispatch, no fan-out
None of the above (sequential, same-file, chatty)    → Solo host, inline (A1)
```
