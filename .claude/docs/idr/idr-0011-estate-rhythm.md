---
doc-type: idr
id: idr-0011
status: draft
date: 2026-08-18
owner: kim.granlund
proof-ref: gh#626 (rhythm seed; the ticket is the durable record of the 2026-08-18 estate gap
  review, conceptual hole #5) + the brief's own `review-cadence: monthly` frontmatter (a stated
  cadence nothing fires)
provenance: derived-from-evidence
supersedes: null
---
# IDR-0011 — Estate rhythm: standing loops carry ruled cadences; the human gate is a managed queue

> DRAFT — awaiting Kim's ratification (one batched round with idr-0008/0009/0010 and
> adr-0021/0022, per gh#622–#627). Lock is a human act; this record never self-locks.
> Record-type note (builder-of-record call, gh#626 left it open): IDR, not ADR — the CLAIM
> (loops need ruled cadences; the human gate is a queue) is a testable founding hypothesis,
> while the cadence VALUES themselves are living state that will be tuned continually; an
> append-only ADR would owe a supersession per cadence tweak. Per the standing ADR-default-no
> ruling, no contract binding specific artifacts is minted here.

## Claim

An estate whose standing loops fire only on human impulse under-runs its own doctrine: sweeps
run when someone types them, decision-watcher is re-armed per session, the ratified brief
declares `review-cadence: monthly` and has never been review-fired. The claim: **every standing
loop of this estate carries a ruled cadence recorded in living state, and the operator's
ratification/merge attention — the scarcest resource in the system — is managed as an explicit
queue that batches**, never as ad-hoc interrupts. A missed cadence is a detectable defect, not
an invisible non-event; a ruling request arrives in a digest, not as a ping.

## Why

Provenance: derived-from-evidence — gh#626 (conceptual hole #5 of the 2026-08-18 estate gap
review; the six tickets gh#622–#627 are the review's durable record). The evidence: the tooling
for rhythm already exists unowned (CronCreate session crons, cloud `/schedule` routines,
`.claude/ops/plan.md` + `held-items.md` as a proto-queue) while the concept doesn't — session
crons die with their sessions and nothing re-arms them by rule; and every gap-review sibling
ends at the same human gate, making Kim's queue the estate's true bottleneck with no queue
discipline. Doubt: rhythm imposed on a one-human estate can become bureaucracy — schedules
firing work nobody wanted — which idr-0010's pricing test and this record's own falsification
clause guard against. Cross-link: idr-0009's re-validation sweep is the first new loop whose
cadence this ruling would assign.

## Proof

Confirms: standing loops firing on schedule without a human typing them, across session
boundaries; ruling/merge items reaching Kim in batches with a visible queue record; a missed
cadence surfacing as a flagged defect rather than silence. Falsifies: a maintained calendar the
estate routinely ignores with no measured loss over multiple cycles (rhythm was not
load-bearing here — retire the concept, not just the file); or scheduled firings whose ledger
rows (idr-0010) show recurring cost with no outcome, i.e. rhythm manufacturing work. Supersede
on falsification, never edit once locked.

## Open questions

- Which loops are IN the first calendar and at what cadences (candidates: daily board drain,
  weekly doctrine re-validation sample per idr-0009, monthly brief review, release-boundary
  snapshot refresh) — this is the ratification round's core question; the draft deliberately
  rules the CONCEPT, not the timetable.
- Calendar canon location — lean: a living-state ops file (`.claude/ops/calendar.md`), one
  canonical copy with an owner, per the living-state class; not the IDR (ledger), not fleet.json
  (a roster, not a schedule). Open per gh#626.
- First standing schedule mechanics — lean: a cloud `/schedule` routine (survives sessions) over
  a re-arm-on-open convention; named as a follow-up seed in gh#626, deliberately not built in
  this PR.
- Kim-queue batching: cadence (daily digest lean), channel (`held-items.md` vs PushNotification),
  and priority order — needs the ruling round.
