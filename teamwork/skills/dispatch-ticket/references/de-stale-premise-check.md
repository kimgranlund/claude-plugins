# De-stale premise check — Phase 3.5's full procedure (#611)

Cited from `dispatch-ticket/SKILL.md`'s Phase 3.5 heading rather than restated inline (F6's
split-to-references repair) — this is the phase's actual contract, not optional background.

A parked ticket was written against a repo that has since moved. #583 (`campaign_close.py` C4
unguarded against branch-name reuse) and #584 (decision-watcher prose-form supersession ruled
out-of-contract) were both caught only because someone independently re-checked the ticket's
premise against live state before building. Mechanize that check: enumerate the ticket's own
load-bearing premises — files/paths it names (do they exist in the described shape: `Read`/
`Glob`), issues/PRs it references (in the state assumed: `gh issue view`/`gh pr view`),
current-state claims it makes ("X lacks Y", "Z is unguarded" — still true, checked against the
live file), records it cites (ADR/IDR/RDD superseded?). Bounded to premises the ticket itself
states — a premise audit, never a fresh design review and never a re-size.

- **Every premise verified — or unverifiable but uncontradicted** → write ONE dated Findings
  entry ("de-stale pass: N premises re-verified, M unverifiable (named), proceeding") and
  continue to Phase 4 exactly as today. Only a POSITIVELY falsified premise stales the ticket;
  fail-open on the merely-unverifiable, disclosed in the entry (fail-closed would make every
  parked ticket unbuildable via one ambiguous sentence — the #583/#584 class is positive drift,
  not ambiguity).
- **Any premise positively falsified → `stale-premise`**, a fourth typed outcome alongside
  built / SKIPPED / named blocker: write the evidence as a dated Findings comment (per
  falsified premise: what the ticket asserts, what live state shows, the command or path that
  proves it), release the claim per Phase 3's Release-on-abandonment bullet, tear down the
  worktree per the teardown bullet, and return `stale-premise` carrying the evidence. Never
  build past a falsified premise; never close, relabel, or rewrite the ticket (re-triage is a
  human/planner act on the evidence left behind); never report it as SKIPPED (that means
  under-specified) or as a named blocker (nothing external blocks it — the ticket itself is
  wrong).

Decision, recorded — **`stale-premise` is a NEW fourth outcome class**, not a reuse: SKIPPED
already means "under-specified, clarify and re-run", a named blocker already means "something
external must move first", and both imply the ticket text is still right. A stale premise demands
a different human act (rewrite or retire the ticket), so overloading either existing class would
hide that in the artifact of record.
