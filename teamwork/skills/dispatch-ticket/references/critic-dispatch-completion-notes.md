# Critic-dispatch completion notes — full incident history

Cited from `dispatch-ticket/SKILL.md`'s "critic step still stalls the same way" rule rather than
restated inline (F6's split-to-references repair). The operative rule stays inline in SKILL.md;
this file carries the "why" — the two incidents that established and then corrected it.

**Corrected 2026-08-17, issue #554.** Being technically UNNAMED does not stop a seat from treating
the dispatch as if it were NAMED: PR #368 (2026-08-16, the ADR-0014 build) idled on its
`docs:doc-checker` critic call by waiting for a completion notification that routed to the ROOT
session instead, not back to the seat — a real stall; fix it by reading the Agent tool call's own
synchronous return directly.

PR #547's fold falsified this section's ONLY-valid-completion framing, though: its unnamed critic
dispatch ran ASYNC, its all-PASS verdict arriving intact as a background task notification to the
DISPATCHING session (not the root — the TOP-LEVEL-host case, not a nested seat's misrouted
callback). Both paths are real: read a synchronous return if the call gives you one; if a
notification reports completion instead, that notification IS the verdict — accept and relay it
(report-before-idle). Escalate a stall — read the transcript/output file, or flag a coordinator —
only when NEITHER arrives within ~10 minutes.
