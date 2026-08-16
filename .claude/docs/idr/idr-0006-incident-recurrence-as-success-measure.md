---
doc-type: idr
id: idr-0006
status: locked
date: 2026-08-16
owner: kim.granlund
proof-ref: per-plugin README footer ledgers + `harness/scripts/release_gate.py` (the gate set) cross-read against git log; harness/skills/check-routing/SKILL.md (routing-eval matrix trend)
provenance: decided-by-human
supersedes: null
---
# IDR-0006 — Incident-recurrence rate is the estate's primary success measure

## Claim

Tracking incident-recurrence rate (primary) and the `/check-routing` routing-eval trend
(secondary) is sufficient to judge whether the estate is succeeding as a product, without any
other instrument — installs, autonomous-merge rate, and other candidate measures raised during
the ratification round are deliberately excluded as primary/secondary signal (they may still
inform idr-0005's adoption-signal question, a separate concern). This is a sufficiency claim, not
merely a preference: if a DRI review finds the estate healthy or unhealthy in a way these two
readouts do not reflect — e.g. a real quality regression with a flat-or-improving ledger×gate
readout, or vice versa — the claim fails and a broader measure set is owed.

## Why

Provenance: decided-by-human — Kim's 2026-08-16 ratification answer (live `AskUserQuestion`,
ratification round) closed the brief's "what is the estate's success measure as a product" open
question directly, naming both the primary and secondary measure explicitly. The choice reuses
instrumentation the estate already runs for other reasons (idr-0001's ledger discipline,
idr-0003's routing-eval matrix) rather than standing up new measurement — consistent with the
estate's standing preference for gates and ledgers already in place over new dashboards.

## Proof

At each `brief-nonoun-plugins.md` monthly review (its own `review-cadence`), compare the DRI's
independent read of estate health against what the two readouts show: the ledger×gate incident-
recurrence readout (proof-ref) and the `/check-routing` matrix trend (proof-ref) release over
release. Confirms if they keep agreeing. Falsifies on the first review where they disagree —
DRI-judged health moving one way while both readouts hold flat or move the other — or where the
primary readout cannot actually be computed from the ledgers as claimed; either failure mode
means these two signals alone are not sufficient, and the measure set needs revisiting via a
superseding IDR.
