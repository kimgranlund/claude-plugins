---
doc-type: idr
id: idr-0009
status: draft
date: 2026-08-18
owner: kim.granlund
proof-ref: gh#623 (truth-maintenance seed; the ticket is the durable record of the 2026-08-18
  estate gap review, conceptual hole #2) + the workspace invariant "falsified claims are
  amended in place with a dated note" (CLAUDE.md, Sources of record flow outward — a duty with
  no initiating mechanism today)
provenance: derived-from-evidence
supersedes: null
---
# IDR-0009 — Doctrine truth maintenance: accepted records are re-tested, not just accumulated

> DRAFT — awaiting Kim's ratification (one batched round with idr-0008/0010/0011 and
> adr-0021/0022, per gh#622–#627). Lock is a human act; this record never self-locks.

## Claim

A monotonically growing doctrine ledger with forward-only classification silently accumulates
falsified claims: 20 ADRs, 7 IDRs, and the fleet-rules canon only ever gain entries, and the one
watcher (decision-watcher) classifies NEW and AMENDED records, never re-reads old ones. The
claim: **every accepted ADR Decision and every locked IDR's falsification clause must be
periodically re-tested against the live estate**, each test ending in a tri-state verdict —
confirmed / falsified / untestable — where a falsified verdict routes to the existing
amend-or-supersede duty with a named owner, and an untestable verdict is itself a doc defect
(a claim written so it cannot be checked). Re-validation is a standing loop of the estate, not
an accident of whoever happens to trip over a stale record.

## Why

Provenance: derived-from-evidence — gh#623 (conceptual hole #2 of the 2026-08-18 estate gap
review; the six tickets gh#622–#627 are the review's durable record). The evidence: the
workspace already carries the duty ("falsified claims are amended in place with a dated note")
but every falsification to date was discovered by accident — e.g. the intake-fork
AskUserQuestion claim falsified 2026-08-17 (gh#541) only because a fork failed live; nothing
would ever have re-read it. decision-watcher's own existence proves the estate believes doctrine
needs watching; it just watches the wrong direction for this failure class. Doubt: re-validation
could become ritual — a sweep rubber-stamping "confirmed" on claims it cannot actually test —
which is why the untestable verdict is first-class rather than folded into confirmed. Family
note: this record, idr-0008 (user signal), and idr-0010 (economy) are one outer-loop family —
and this loop's own firing cost is priced by idr-0010's ledger like any other sweep.

## Proof

Confirms: a sweep run emitting per-claim tri-state verdicts as a machine-readable report; at
least one falsification discovered by the sweep BEFORE an incident discovers it independently.
Falsifies: repeated sweeps returning only "confirmed" while incidents keep independently
falsifying doctrine in the same period (the sweep tests the wrong layer); or the sweep's
measured cost exceeding its yield under idr-0010's worth-firing test across multiple cadences
(truth maintenance that costs more than the drift it prevents). Supersede on falsification,
never edit once locked.

## Open questions

- Instrument shape: the lean is a **re-validation MODE on decision-watcher**, not a sibling
  seat — a new seat fails idr-0007's job-evidence test until the mode is tried and proves
  insufficient. Named as a follow-up seed in gh#623, deliberately not built in this PR.
- Sampling policy and cadence: lean is sampled (not full-sweep) on a cadence the rhythm ruling
  (idr-0011) assigns — the two records lock together or this one carries its own interim cadence.
- Untestable-verdict handling: lean is flag-for-rewrite (a ticket against the owning record),
  never silent exemption.
- Who executes a falsified verdict: lean is the sweep files the work item (`file-bug`/
  `file-task`) and the amend/supersede runs through the normal human-ratified path — the sweep
  reports, it never rewrites doctrine.
- Whether fleet-rules canon (a skill, not a doc) is in the first instrument's scope: lean is
  wave two — start where claims carry explicit falsification clauses (IDRs) and enumerable
  Decisions (ADRs).
