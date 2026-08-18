# Orchestration rubric — A3: named background seats (teammate/mailbox mode)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

**Priority axis G1** (2026-08-18 fold-in): A3 previously had no review surface for live
mailbox CONDUCT — authoring text only. Resolved conduct-evidence source: **primary = the
durable channels, which ARE the record** — `fleet.json`/`fleet-roster.md` rows and GitHub
Issue/PR comment trails. `agent-*.jsonl` transcript reads are the deep-dive tier for a
FLAGGED incident only, never the sweep's default (cost + privacy of full transcripts). A3-R2
below realizes this as the mechanizable READER — it locates and parses the durable channels;
whether the conduct they show was GOOD is still judgment, same split as every other archetype.

## Architecture & intended use

`Agent` with `name:`, mailbox continuation via `SendMessage`, completion notifications.
Intended use: long-lived seats that genuinely need continuation across turns.

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A3-R1 | Naming is deliberate: named ONLY when continuation is needed; never on a fan-out | — | judgment |
| A3-R2 | **(G1)** Durable-channel evidence reader: charters carry the cloud-can't-message-back caveat; anything a peer must see goes to `fleet.json`/roster/GitHub, never solely a nudge — the READER locates and parses these channels as the primary conduct-evidence source | 2026-08-18 fold-in ruling on #666; `fleet-rules` Part A §3 | **mechanizable** — `orchestration-audit`'s `scripts/audit.py` `a3-durable-channel` check: confirms `.claude/ops/fleet.json` parses as JSON and `.claude/ops/fleet-roster.md` exists and has ≥1 data row; reports which named seats in the roster have NO matching durable comment trail as a named gap, never a silent pass |
| A3-R3 | Recovery path known: idle-notification-only seats recovered via `agent-*.jsonl` transcript reads — the DEEP-DIVE tier only, for a flagged incident, never the sweep default | the estate's own recovery memory; 2026-08-18 fold-in | judgment |
| A3-R4 | Reports land: completion routes to the root session; no stranded mailbox | verified A4, 2026-08-10 | judgment |

**Owning checker for A3:** no dedicated conduct checker exists yet — A3-R1/A3-R3/A3-R4 are
judgment-queued to a human read of the durable-channel evidence A3-R2's reader surfaces; X-R3
reports this as a named gap (no file to check for), not a silent pass.
