---
doc-type: brief
id: brief-nonoun-plugins
status: active
date: 2026-08-16
owner: kim.granlund
review-cadence: monthly
---
# BRIEF — nonoun-plugins

## Thesis

An agent-authoring estate compounds when it is self-governing: skills, agents, and docs are
living records gated by their own toolchain, every decision is a citable record, and autonomous
agents take on an increasing share of the work behind human ratification gates. The eight-plugin
estate is the working test of that bet.

## Confirmed

- Self-governing toolchain, mechanized incident classes stay gone → `idr-0001`.
- Git substrate (Issues/PRs/CI/worktrees/ADR ledger) is the durable cold-start memory → `idr-0002`.
- Routing quality is a measurable, governable property of names/descriptions → `idr-0003`.
- Autonomy scales through gates, not around them → `idr-0004`.
- External audience, low urgency; portability machinery kept as-is at zero further investment → `idr-0005`.
- Success measure: incident-recurrence rate (primary), routing-eval trend (secondary) → `idr-0006`.
- Roster growth is deliberate strategy, not accretion — ratified 2026-08-16 (Kim, ratification
  round): `harness:plan-plugin-split`'s anti-matrix rule (a distinct domain surface per plugin)
  is confirmed as a binding gate on every roster addition, including the planned
  `product-management` / `brand-design` migrations. Home: `harness:plan-plugin-split`'s own
  anti-matrix contract — this ruling scopes an existing gate rather than minting a new claim, so
  no IDR.

- Solo-first composition is a WHY-grain claim: teams are escalations, not defaults — `idr-0007`
  (locked 2026-08-18, ratified by Kim; grounded in gh#265's measured hop tax, gh#266's
  chore-lead retirement, ADR-0010's uniform build seat).
- User signal is defined (any non-estate party's trace on a shipped artifact) and enters via the
  existing intake spine; until an instrument carries nonzero signal, idr-0005 is untested —
  `idr-0008` (locked 2026-08-18, ratified by Kim; gh#622).
- Accepted doctrine is periodically re-tested tri-state (confirmed/falsified/untestable);
  falsified routes to the amend/supersede duty with a named owner — `idr-0009` (locked
  2026-08-18, ratified by Kim; gh#623).
- Every recurring firing class is priced: per-firing ledger rows plus a worth-firing test;
  idr-0007's coordination tax is unenforceable unmeasured — `idr-0010` (locked 2026-08-18,
  ratified by Kim; gh#624).
- Standing loops carry ruled cadences in living state; the operator's ratification/merge
  attention is a managed, batching queue — `idr-0011` (locked 2026-08-18, ratified by Kim;
  gh#626).
- Trust tiers ride author provenance (T0 operator / T1 registered seats / T2 record text,
  quote-not-obey / T3 foreign), channel only ever lowers — `adr-0021` (accepted 2026-08-18,
  ratified by Kim; gh#625).
- The repo is the backup: everything operationally load-bearing is reconstructible from
  origin/main, with four named exceptions and mitigations — `adr-0022` (accepted 2026-08-18,
  ratified by Kim; gh#627).

## Open Questions

- When does a real release-grain commitment land? Until then, releases-loop homes (a `roadmap`
  index, a first RDD) stay unminted — deferred 2026-08-16 (Kim, ratification round), not an
  oversight.
- 2026-08-18 (Kim, resolved via find-intent, gh#611): the HOMES half of the line above is lifted —
  the `roadmap` index is minted at `.claude/docs/roadmap/roadmap-nonoun-plugins.md` and the
  RDD↔Issue binding rule is recorded in docs' `doc-writing-rules` (RDD section). The question
  itself stays open in its remaining half: no release-grain commitment is locked yet — the first
  `locked` RDD (which lands in the roadmap's Now) closes this bullet whole.
- CLOSED 2026-08-21 (verified against repo state): all six 2026-08-18 gap-review instruments have
  landed — gh#622–#627 are all CLOSED and each named instrument exists — feedback-intake door
  (`lld-0017-feedback-intake-door.md`), decision-watcher's re-validation mode (idr-0009, wired in
  `harness/agents/decision-watcher.md`), the cost ledger (`lld-0018-estate-economy-ledger.md`,
  `.claude/ops/spend-ledger.csv`), the standing schedule + calendar (`lld-0015-estate-rhythm-
  instrument.md`, `.claude/ops/calendar.md`), the trust-tier ruling (`adr-0021-trust-tiers-and-
  threat-model.md`, fleet-rules' quoting bullet), and the reconstructibility audit
  (`lld-0014-reconstructibility-audit.md`, `harness:check-reconstructibility`). Per-record open
  questions, if any remain, live in the records themselves. The user+economy+truth trio
  (idr-0008/0010/0009) is confirmed as one outer-loop family with all first instruments in place.
