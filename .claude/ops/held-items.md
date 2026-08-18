# Held items ledger — kimgranlund/claude-plugins

This file carries two related but distinct human-gate ledgers — both "things only Kim can
decide," kept in one file per idr-0011's (`.claude/docs/idr/idr-0011-estate-rhythm.md`) lean that
Kim's ruling/merge attention batches through a named channel rather than arriving ad hoc. Each
section owns its own entry contract; neither is folded into the other's shape.

## Filing-author holds (`ops-issues`)

The denial/hold ledger for `ops-issues` (`spec-ticketing-watch-triage.md` REQ-007/REQ-009).

An item lands here when its filing author is not on `friendlies.json`'s allow-list — held, never
auto-created, surfaced for an explicit human approve/deny decision. `ops-issues` never approves or
denies its own entries here; only a human decides, and a later dispatch carrying that decision
executes it (mint + grow the allow-list on approval, or mark `denied` on this ledger with no record
and no allow-list change — a denied item is never re-surfaced).

Bootstrapped 2026-07-18T17:33:02Z (first-ever firing): no entries. Every item discovered this
firing (issues #33, #34) was authored by `kimgranlund`, already seeded into `friendlies.json` as
the repo owner/maintainer — nothing held.

## Ledger

*(empty — no items held yet)*

<!--
Entry template (one per held item):

### #<number> — <title>
- Source: github issue|pr
- Author: <login> (not on friendlies.json as of <date>)
- Discovered: <UTC timestamp> (firing report: `.claude/ops/reports/<timestamp>.md`)
- Shape: defect | feature idea | generic task
- Label applied: needs-triage-approval
- Status: held | approved <date> | denied <date>
- Decision note: <filled in by the human decision, and the dispatch that executes it>
-->

## Kim's ruling/merge queue (idr-0011)

The batching channel for human-gate items — a ratification, a PR merge decision, an ambiguous
call a dispatch couldn't resolve unattended — so they reach Kim in a daily digest rather than as
piecemeal interrupts. `teamwork:fleet-rules` Section 3 names this channel as the default landing
spot for anything that would otherwise ping Kim mid-run (cited there, not restated).

**Cadence and channel are idr-0011's own named leans, not yet a ratified ruling** — this section
is the calendar's Kim-queue row (`.claude/ops/calendar.md`) made concrete: daily digest, this
file as the channel; both tunable until the calendar ruling round (gh#626) fires.

Any seat with a genuine human-gate item appends one entry below instead of escalating live
(`fleet-rules`' own never-escalate-straight-to-the-human default) — a stale claim it can't
resolve, a merge decision outside an auto-merge grant, an ADR/IDR ratification round. A daily
pass over this section is the digest; Kim clears an entry by editing its Status line in place
(the durable record stays, per this file's own append-then-resolve shape above).

*(empty — no items queued yet)*

<!--
Entry template (one per queued ruling/merge item):

### <dated>Z — <one-line title>
- Source: <ticket/PR/session that raised it>
- Kind: ratification | merge-decision | ambiguous-claim | other
- Why it's queued here rather than resolved unattended: <reason>
- Status: queued | resolved <date> — <what Kim decided>
-->

