---
doc-type: adr
id: adr-0013
status: accepted
ratified: by Kim, 2026-08-16 (batched confirm — "this observation is the ticket's valid,
  complete result", ruled on the evidence quoted in the Context below)
date: 2026-08-16
owner: kim.granlund
supersedes: adr-0012 (the deployment-prerequisite Consequences bullet only — every other
  Decision and Consequences line of ADR-0012 stands unamended)
intent-refs: idr-0004    # idr-0004's own proof-ref points here directly, the named partial-verification data point
---
# ADR-0013 — ADR-0012's `autoMode.allow` rule: dispatch-tier block observed, merge-tier still unmeasured (partial verification)

## Context

Issue #256 asked for exactly one empirical fact: does the `autoMode.allow` rule (commit
40dd5c3, added 2026-08-14/15) actually clear the Claude Code unattended-permission
classifier's `gh pr merge` block for a dispatched subagent carrying ADR-0012's explicit
`auto-merge: authorized` grant line — the "deployment prerequisite" ADR-0012's own
Consequences section named as unverified? The ticket's Acceptance ruled either outcome
(works / still blocked) a valid, complete record.

Research/spec phase (2026-08-15, LLD `lld-0003-adr-0012-allow-rule-verification.md`,
v0.2.0, landed on `main` at 0e6e1c6) designed the test vector: a feature-kind,
`size:small`, QB0–QB7-eligible dispatch through `teamwork:build-lead` carrying the
literal grant line, run inside an interactive auto-mode coordinator session.

**Observed (2026-08-16, verbatim from the coordinating session's evidence):**
The coordinating session (interactive, auto mode) dispatched exactly that test — an
`Agent` tool call to `teamwork:build-lead` whose sealed prompt carried the
`auto-merge: authorized` grant line. **The `Agent` tool call itself was DENIED by the
Claude Code auto-mode permission classifier before any agent was created** — denial
text: "Permission for this action was denied by the Claude Code auto mode classifier.
Reason: Blocked by classifier." Two sibling dispatches in the same tool-call block
(identical shape, no grant line) launched without incident, isolating the grant line
itself as the trigger for the denial.

## Decision

Record the observed outcome as the current, correct reading of ADR-0012's
"deployment prerequisite" Consequences bullet, replacing its prediction with what was
actually measured:

1. **The block is earlier and stricter than ADR-0012 predicted.** ADR-0012's
   Consequences section predicted the classifier blocks `gh pr merge` at *execution
   time* (stage 2b's merge sequence), with graceful degradation to the
   `auto-merge-denied` branch once that command is attempted. The observed behavior
   instead blocks at *dispatch-creation time*: an interactive auto-mode session's
   classifier denies the `Agent` tool call itself the moment its sealed prompt carries
   the `auto-merge: authorized` grant line — before `dispatch-ticket` ever runs, before
   stage 2b is ever reached, before any `gh pr merge` is ever attempted.
2. **This is a partial verification, not a complete one.** Dispatch-tier: BLOCKED
   (measured, above). Merge-tier — whether the `autoMode.allow` rule (commit 40dd5c3)
   itself would clear `gh pr merge` once a dispatch legitimately reaches stage 2b's
   merge sequence — remains UNMEASURED, because stage 2b was never reached. The
   evidence does not distinguish a `hard_deny` on the grant line from some narrower
   classifier-tier rule; only that the block landed on dispatch creation, not on the
   merge command.
3. **Practical consequence.** ADR-0012's quick-build carve-out (stage 2b) currently
   cannot be exercised at all from an interactive auto-mode coordinator — the grant
   line never survives to reach a dispatched seat. A human-typed invocation path (Kim
   directly running `/build-feature` or `/mobilize-chores auto` from an
   interactive-but-non-auto-mode prompt, or the grant placed by a differently-scoped
   caller) remains untested and is the next fact this record's own gap points at,
   should the carve-out's usability matter enough to chase further.

## Consequences

- ADR-0012's Consequences bullet beginning "Deployment prerequisite, not a design gap:
  the unattended permission classifier blocks `gh pr merge` today…" is superseded by
  this record; every other Decision and Consequences line in ADR-0012 (the QB0–QB7
  predicate, the merge-sequence mechanics, the audit-trail additions, the QB7 TOCTOU
  acceptance) stands exactly as ratified, unamended and unaffected.
  ADR-0012's own status stays `accepted` — this is a narrow, single-bullet
  supersession (ADR-0007's precedent over ADR-0006's frozen-dir clause), not a reversal
  of the mechanism it built.
- Stage 2b remains fail-safe and inert exactly as ADR-0012 designed it — the observed
  block only sharpens *where* in the pipeline it degrades gracefully (dispatch
  creation, not the merge command), which changes no downstream behavior:
  `dispatch-ticket`'s stage 2b code path, `build-lead`'s relay contract, and
  `mobilize-chores`' unattended ceiling all still read exactly as ADR-0012 left them.
- Anyone reading ADR-0012's deployment-prerequisite bullet going forward should read
  this record alongside it for the corrected, measured state — grep `supersedes:
  adr-0012` to find it.
- Issue #256 is closed on this record as its complete, valid result per the ticket's
  own either-outcome acceptance criterion.

## Links

- Supersedes (narrowly): `.claude/docs/adr/0012-quick-build-auto-merge.md`
- Origin ticket: issue #256
- Design: `.claude/docs/lld/lld-0003-adr-0012-allow-rule-verification.md`
- Rule under test: commit 40dd5c3 (`autoMode.allow`)
