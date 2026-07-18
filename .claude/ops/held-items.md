# Held items ledger — kimgranlund/claude-plugins

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
