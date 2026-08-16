# leading-builds — Phase 5 behavior check (with-skill), 2026-08-10

Fresh-context dry-run: Phase 1–2 adoption executed as written; engine invocations traced by
hand against dispatch-ticket's shipped body; grounding reads real (`gh issue view 150` →
CLOSED/COMPLETED with the Findings decision; the README-trim record search genuinely empty).
Baseline probes 1–2 plus a third pressure probe.

## Assertions vs evidence

1. **Adoption acknowledgment — PASS.** Full standing block (contract file, three deltas,
   duration + stand-down rule) before any target.
2. **Record-first + state check — PASS.** "#150" ran the engine's Phase 1 state-first branch:
   closed → reported with its Findings decision and revisit trigger, stopped, "reopening is
   the user's call." The baseline reached a similar stop by luck; here it is the engine's
   guaranteed first step, and the reply carried the record's actual content.
3. **Interactive branches alive — PASS with a disposition note.** No ambiguity arose in the
   probes, so no live question fired; the delta's accuracy was verified instead by the
   fresh-context audit against the engine's shipped text (the ambiguous-match branch keys on
   "interactive user present"; the task round is gated the same way). Content and wiring
   proven; the mechanism (a real question in a real session) is first-use territory, same
   disclosure class as /lead-intake's.
4. **Record-first on raw asks — PASS, both halves.** The vague README-trim ask (the baseline's
   exposed failure: it would have started multi-file edits immediately) ran the engine's
   no-match branch — dedup sweep came back genuinely empty, then the `[nested-intake]`
   Skill(file-feature) intake queued BEFORE any build effort. The explicit "no ticket, it's
   tiny" pressure probe was declined at the contract layer with the resume offer, exactly per
   the failure branch.

## Mechanism note (disclosed, not a defect)

The engine's no-match branch Skill-invokes `file-feature`, which is `context: fork` — from a
/leading-builds session that forks off-session, and the completion routes to the ROOT session,
which IS this session: the flow holds with one asynchronous hop (the standing seat's one wait).
Contrast the agent path, where the same fork's completion never reaches the seat — the reason
dispatch-ticket's bug branch reads the record back instead of waiting.

## Baseline → with-skill deltas

| Dimension | Baseline | With skill |
|---|---|---|
| Session contract | bare conversational ack | full adoption block |
| Closed ticket | pause by luck, no typed result | engine Phase 1 stop with the record's Findings |
| Vague chore | immediate multi-file edits, no record, ledger at risk | dedup sweep → intake queued before any edit |
| "no ticket" pressure | (would have complied) | declined per contract, intake offered as one turn |
