---
doc-type: idr
id: idr-0008
status: draft
date: 2026-08-18
owner: kim.granlund
proof-ref: gh#622 (user-signal-path seed; the ticket is the durable record of the 2026-08-18
  estate gap review, conceptual hole #1) + idr-0005 (the external-audience hypothesis this
  record gives a sense organ)
provenance: derived-from-evidence
supersedes: null
---
# IDR-0008 — A user signal path: the estate must be able to hear anyone using it

> DRAFT — awaiting Kim's ratification (one batched round with idr-0009/0010/0011 and
> adr-0021/0022, per gh#622–#627). Lock is a human act; this record never self-locks.

## Claim

Every feedback loop this estate runs today is self-referential — incidents, release gates, and
routing evals measure process health, never use — so IDR-0005's locked hypothesis (external
audience, portable products) currently has no sense organ and is therefore untested rather than
confirmed. The claim: **user signal** is any trace originating from a party other than this
estate's own seats acting on a shipped artifact — (a) adoption signal (install/clone/star of a
published plugin), (b) foreign-repo feedback (an issue, PR, or report arriving from outside this
workspace), (c) a direct report from a human who is not the operator — and when such signal
arrives it enters through the **existing intake spine** (`file-bug`/`file-feature`/issue-sorter
with the friendlies gate), not a new door: reuse is the default and a new door owes job evidence
under the anti-matrix rule. Until at least one instrument carries nonzero user signal, no
prioritization argument in this estate may cite "users" as evidence.

## Why

Provenance: derived-from-evidence — gh#622 (conceptual hole #1 of the 2026-08-18 estate gap
review; the six gap-review tickets gh#622–#627 are that review's durable record, there is no
separate review file). The evidence: IDR-0005 locked an external-audience bet, yet an inventory
of the estate's live loops finds only process-health instruments — incident recurrence
(idr-0006), routing evals (idr-0003), release gates (idr-0001) — with no install/adoption
signal, no feedback intake from any foreign repo, and no definition of user signal at all.
Doubt would come from IDR-0005's own "low urgency" clause: if the external audience is
deliberately deferred, a signal path may be premature instrumentation. The counter is that the
definition and the door are near-zero-cost while their absence makes the hypothesis permanently
unfalsifiable. Family note: this record, idr-0010 (economy), and idr-0009 (truth maintenance)
are one outer-loop family — signal coming in, spend accounted, doctrine re-tested — the three
loops that point outward or backward where everything prior pointed inward.

## Proof

Confirms: the first foreign-origin record arriving and routing through the existing intake spine
without a new door being minted; an adoption probe reporting a nonzero count that visibly
changes a prioritization decision (a roadmap row, a ticket priority) citing it. Falsifies: an
instrument live for two review cycles with zero signal — which indicts IDR-0005's audience
hypothesis or this record's instrument choice, and forces that re-examination explicitly; or
user signal arriving that the intake spine structurally cannot ingest (that is the job evidence
a new door would need). Supersede on falsification, never edit once locked.

## Open questions

- Which first instrument ships: the lean is the **feedback-intake door** (an issue template +
  routing into issue-sorter's friendlies gate) over an adoption probe — it reuses the spine
  wholesale and is the smaller build; the probe becomes wave two if the door stays silent.
  Named as a follow-up seed in gh#622, deliberately not built in this PR.
- The assert layer verifying the instrument itself (needs the instrument chosen first).
- Whether "adoption signal" (clause a) is measurable at all without publishing infrastructure
  the estate doesn't yet have — may reduce the definition to clauses (b) and (c) at lock time.
