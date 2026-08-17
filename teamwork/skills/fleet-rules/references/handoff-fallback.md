# The eight-field handback fallback

Cited by every teamwork agent that reports back to a coordinator or the host, for the case
harness's `write-handoff` isn't installed. Canonical copy — an agent body cites this path
(`${CLAUDE_PLUGIN_ROOT}/skills/fleet-rules/references/handoff-fallback.md`) rather than
hand-restating the block; the six ported agents (`team-lead`, `builder`, `planner`,
`docs-writer`, `code-checker`, `wiring-checker`) each carried their own inline copy before this
consolidation (teamwork README's Construction note; #382).

When harness IS installed, use `[[write-handoff]]` instead — it is the fuller contract (field
how-tos, the mechanical `handoff_check.py` gate, and the sealed-vs-messaging channel rule below).
This file is the minimum viable shape for when it isn't.

**Which channel carries it** — resolved once in `write-handoff`'s "Sealed vs. messaging" note,
restated here so a harness-absent agent still gets it right: a sealed, record-first dispatch (no
`name:`, no mailbox — e.g. `dispatch-ticket`'s Findings write-back) carries this block's
routing-relevant subset (at minimum Status, Summary, Evidence, Recommended next action) inside
the durable record's dated Findings entry — there is no separate return message. A named
(teammate-mode) seat sends the full block as a message to its coordinator or the host.

## The block — exactly these fields, in order

Status / Summary / Files changed / Tests/checks run / Evidence / Risks / Open questions /
Recommended next action.

- **Status** — `done | partial | blocked(reason)`, first line, nothing else on it.
- **Summary** — what was done, in 1–3 sentences. The outcome, not the process.
- **Files changed** — each path touched (created / edited / deleted), one per line.
- **Tests/checks run** — the gates run and their result, by command; a gate you didn't run is
  `UNMEASURED`, stated, never silently omitted.
- **Evidence** — what a reviewer can verify without re-doing the work: exit codes, counts,
  `file:line` citations.
- **Risks** — what could be wrong or fragile, max ~5.
- **Open questions** — unresolved decisions needing a human or another role, max 3.
- **Recommended next action** — the single best next step and who owns it.
