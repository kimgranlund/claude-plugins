---
doc-type: idr
id: idr-0010
status: locked
date: 2026-08-18
owner: kim.granlund
proof-ref: gh#624 (economy seed; the ticket is the durable record of the 2026-08-18 estate gap
  review, conceptual hole #3) + gh#265 (the sole prior cost measurement — the ~1.92×/~3.6× hop
  tax that retired chore-lead) + idr-0007 (the coordination-tax rule this record prices)
provenance: derived-from-evidence
supersedes: null
---
# IDR-0010 — Estate economy: recurring spend is priced, or it grows until it eats its yield

> LOCKED 2026-08-18 — ratified by Kim (live AskUserQuestion round, all-six batch gh#622–#627,
> PR #628). Append-only from here: supersede, never edit.

## Claim

Loops have token budgets; the estate has none. A single day now runs on the order of five sweep
firings (~200k tokens each) plus a dozen 150–400k-token builds — figures that are
order-of-magnitude estimates, unmeasured, itself an instance of the very gap this record names —
with no ledger, no cost-per-outcome notion, and no doctrine for when a firing is worth its
tokens. The claim: **every recurring
firing class — sweeps, dispatched builds, standing seats — must be priced**: a per-firing ledger
row carrying at minimum tokens-spent and outcome, and a worth-firing test any recurring
automation must pass to keep its cadence. Unpriced automation grows monotonically until it
consumes its own value, and idr-0007's rule that every seat must buy its coordination tax is
unenforceable while nothing measures the tax. The pricing doctrine is qualitative first
(worth-firing as a judgment against the row history), numeric bands only after the ledger has
data to derive them from.

## Why

Provenance: derived-from-evidence — gh#624 (conceptual hole #3 of the 2026-08-18 estate gap
review; the six tickets gh#622–#627 are the review's durable record). The strongest single datum:
the estate has run exactly ONE cost measurement in its history (gh#265, the measured seat-chain
hop tax) and that one measurement retired an entire coordination seat (chore-lead, gh#266) and
seeded a locked founding claim (idr-0007) — proof that in this estate, measuring cost changes
composition decisions, which makes the absence of any standing measurement the gap. Doubt: token
counts may be hard to obtain accurately per firing (no named instrument exists), and a ledger
nobody reads is pure overhead — the falsification clause below makes that failure mode the test.
Family note: this record, idr-0008 (user signal), and idr-0009 (truth maintenance) are one
outer-loop family; the ledger prices the other two loops' instruments the way it prices
everything else.

## Proof

Confirms: ledger rows accumulating per firing in the ruled shape; a SECOND measurement-driven
decision in gh#265's mold — a sweep retired, re-scoped, or re-cadenced explicitly citing its
rows. Falsifies: a maintained ledger whose data changes no decision across multiple review
cycles (the accounting is overhead — the economy doctrine must price itself, and retire itself
if it fails its own test); or per-firing token counts proving unobtainable at useful accuracy,
leaving rows that are guesses (a ledger of estimates nobody trusts is worse than no ledger).
Supersede on falsification, never edit once locked.

## Open questions

Status at ratification (2026-08-18): none of the bullets below were individually ruled in the
all-six batch round; each stays open at ratification, tracked at gh#624.

- Ledger scope and columns: lean is sweeps + dispatched builds first (not every fork), one row
  per firing — date, event-kind, seat/command, tokens, outcome, verdict — shaped like
  `attention-trend.csv` and living under `.claude/ops/`. Named as a follow-up seed in gh#624
  (the ledger instrument + its selftest-bearing schema check), deliberately not built in this PR.
- Token-count source — the hard part, unresolved and carried: transcript-jsonl accounting vs
  harness-reported usage vs declared estimate; the instrument choice decides the ledger's
  trustworthiness.
- Write path: lean is a close-out convention (each seat/sweep appends its own row; all hooks
  retired 2026-08-17, #466, so no hook may own this) with a periodic collector as fallback.
- Whether fleet-rules and loop-rules each gain a pricing bullet citing this record at lock time
  (gh#624's acceptance says yes; the bullets land with the instrument wave, not this draft).
- Ticket-claim discrepancy, recorded rather than resolved: gh#624's charter note says intake
  already placed a roadmap row, but origin/main's roadmap file carries no such row and gh#624
  bears no `roadmap` label as of this draft — unaddressed in the all-six ratification round,
  carried at gh#624.
