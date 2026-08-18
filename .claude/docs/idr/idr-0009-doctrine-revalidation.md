---
doc-type: idr
id: idr-0009
status: locked
date: 2026-08-18
owner: kim.granlund
proof-ref: https://github.com/kimgranlund/claude-plugins/issues/623#issuecomment-5323801673
provenance: derived-from-evidence
supersedes: null
---
# IDR-0009 — Doctrine truth maintenance: accepted records are re-tested, not just accumulated

> LOCKED 2026-08-18 — ratified by Kim (live AskUserQuestion round, all-six batch gh#622–#627,
> PR #628). Append-only from here: supersede, never edit. The proof-ref points at the named
> instrument seed (the re-validation mode on decision-watcher, gh#623 seed comment) — the proof
> vehicle.

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

Status at ratification (2026-08-18): none of the bullets below were individually ruled in the
all-six batch round; each stays open at ratification, tracked at gh#623.

- Instrument shape: the lean is a **re-validation MODE on decision-watcher**, not a sibling
  seat — a new seat fails idr-0007's job-evidence test until the mode is tried and proves
  insufficient. Named as a follow-up seed in gh#623, deliberately not built in this PR.
- Sampling policy and cadence: lean is sampled (not full-sweep) on a cadence the rhythm ruling
  (idr-0011) assigns. At lock, the "two records lock together" branch FIRED — idr-0011 locked in
  the same 2026-08-18 round, so no interim cadence is minted here; the concrete cadence
  assignment rides idr-0011's calendar ruling round (tracked at gh#626, with this sweep's slot
  tracked at gh#623).
- Untestable-verdict handling: lean is flag-for-rewrite (a ticket against the owning record),
  never silent exemption.
- Who executes a falsified verdict: lean is the sweep files the work item (`file-bug`/
  `file-task`) and the amend/supersede runs through the normal human-ratified path — the sweep
  reports, it never rewrites doctrine.
- Whether fleet-rules canon (a skill, not a doc) is in the first instrument's scope: lean is
  wave two — start where claims carry explicit falsification clauses (IDRs) and enumerable
  Decisions (ADRs).
