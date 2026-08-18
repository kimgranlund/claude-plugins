# Bug hand-off claim provenance (gh#608)

Phase 2's `kind: bug` bullet in the main SKILL.md points here for the marker form used when a
claim already sits on the record at the moment of hand-off — full mechanism and the rejected
alternative live in this one place rather than inline, to keep the SKILL.md body under its line
cap (skill-writing-rules F6).

## The defect this closes

Live repro 2026-08-18, adiahealth/gen-ui-kit#1593: `dispatch-ticket`'s bug branch never claims a
ticket on its own account (Phase 3's claim bullet is unreachable for `kind: bug`) — but a claim
can still be present at hand-off time regardless, most often a coordinator's own claim comment
posted ON BEHALF OF the very dispatch that is redirecting here (`fleet-rules`' Section 2
amendment: "a claim posted by a coordinator ON BEHALF OF a build it is dispatching NAMES the
dispatched builder"). `docs:file-bug`'s Phase 5 read that pre-existing claim/assignee/`in-flight`
label as a competing seat and stood down — permanently, since nothing was ever coming back to
retry. The lane deferred to file-bug, file-bug deferred to the lane's own claim, and nobody
built (gh#608's Classification).

## The fix: verified claim provenance in the marker

Before invoking `file-bug`, read the record's own current claim trail (`gh issue view
--comments` git-native; the resolved adapter's `read` operation under Option C; the file
backend's `claimed-by`/`claimed-at` frontmatter).

- **No claim present at all** → the bare `[redirected-from:dispatch-ticket]` marker, unchanged.
  Nothing to vouch for.
- **A claim comment is present AND it explicitly names this dispatch as its beneficiary** (the
  fleet-rules Section 2 on-behalf-of wording, or an equivalent explicit statement — never inferred
  from the mere presence of a claim) → carry that exact comment's URL forward:
  `[redirected-from:dispatch-ticket claim:<comment-url>]`. `file-bug`'s Phase 5 reads the record's
  own claim trail and compares: the named comment is still the record's most recent claim → same
  lane resuming its own hand-off, proceed under it, never re-claim, never stand down. The named
  comment is missing, superseded by a later claim, or the trail shows a different claimant →
  dedup applies exactly as before — a genuine third party, stand down and report the conflict.
- **A claim is present but does NOT name this dispatch as its beneficiary** → never carry its URL
  forward. This is the case a first draft of this fix got wrong (caught by a fresh-context
  `skill-checker` pass, gh#608's own build): blindly vouching for any pre-existing claim — without
  checking whom it actually names — would launder a genuine third-party claim into apparent
  authorization, reopening the double-dispatch class from the other side instead of closing it.
  The bare marker stands in this case; `file-bug`'s own dedup runs unmodified against whatever it
  finds, exactly as it would with no marker at all.

## Rejected alternative

**Defer this skill's own claim until after `file-bug` adopts the record**, instead of (or in
addition to) the marker fix. Rejected: this skill's bug branch already claims nothing of its own
to defer — Phase 3's claim bullet never runs for `kind: bug` — so an ordering fix inside this
skill cannot repair a claim it never makes and does not control the timing of (the actual claim,
when one exists, is posted upstream by a coordinator, per the fleet-rules amendment cited above).
Reordering would also reopen the exact double-dispatch window Phase 3's claim-then-isolate
discipline exists to close (#183/#184) — trading a dedup false-positive for a worse race. The
marker-carries-verified-provenance fix is additive prose only, in the two narrow spots that
actually need it (this file plus `docs:file-bug`'s Phase 5), with no phase-ordering change to
either skill.
