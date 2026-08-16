---
doc-type: idr
id: idr-0004
status: locked
date: 2026-08-16
owner: kim.granlund
proof-ref: .claude/docs/adr/0013-adr-0012-automode-allow-verification.md
provenance: derived-from-evidence
supersedes: null
---
# IDR-0004 — Autonomy scales through gates, not around them

## Claim

The estate routes every irreversible promotion — merge, ship, ratify — through a pre-authorized
all-green predicate or a human gate, and this gating raises safe autonomous throughput rather
than capping it. If the gates' overhead exceeds the rework they prevent, or autonomous throughput
stalls at the gate instead of growing through it, the claim fails.

## Why

Provenance: derived-from-evidence — ADR-0012 (quick-build auto-merge: the predicate is the
authorization; the PR stays), ADR-0013 (partial verification: dispatch-tier blocked, merge-tier
unmeasured), the "ship only through the gate" invariant, and mobilize-chores' PR-opened ceiling
with ADR-0012's single carve-out. Faced with the autonomy/safety trade repeatedly, the estate
consistently chose "add a gate, then automate through it" over "remove the human" — a pattern,
never a stated claim. Open counter-evidence, disclosed: ADR-0013's measured dispatch-tier block
is the "stalls at the gate" failure condition live today; the Proof's data collection must first
get past it.

## Proof

ADR-0012 carve-out outcome data — post-merge defect rate of predicate-merged PRs vs human-merged
ones, and dispatch-to-merged throughput before vs after the carve-out — collectible only once
ADR-0013's dispatch-tier block is cleared (its Decision 3 names the untested human-typed
invocation path). Interim observable, measurable today: the human-merged path's gate overhead vs
the rework its gates prevent.
