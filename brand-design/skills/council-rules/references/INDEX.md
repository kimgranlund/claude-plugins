# Council rules — reference index

7 axes, 7 files. Grep the term first, then Read the matching section — these are catalogs, not a
linear read. Every file below appears in the top-level skill file's consult table; every
consult-table row names a real file here.

**Provenance:** generalized 2026-08-20 from `check-brand-council`'s own machinery (S3 of the
brand-design "council-as-platform" overhaul, `#826`) — the brand instance's fan-out/severity/
voting/synthesis logic already existed; this pack extracts the domain-neutral shape of it once so
`check-brand-council` becomes a configuration of this machinery instead of the machinery's only
copy, and so the forthcoming `make-council`/`make-critic` (S4) have something to mint against.

## Roster & personas

- `roster-and-personas.md` — what a persona/critic contract is, what a roster is, how sub-councils
  group a roster, the "full" union convention
- `roster-file-contract.md` — the roster FILE schema: a per-instance roster data file's table +
  `## Groups` shape, handle↔persona-file bijection, `VACANT`-lead-is-a-warning, why seating a
  critic is a data edit

## Fan-out mechanics

- `blind-fanout-mechanics.md` — the unnamed/synchronous dispatch shape, same-turn concurrency,
  bounded rejection, why a further-nested named dispatch strands its report

## Severity & voting

- `severity-and-voting.md` — the four-tier severity taxonomy, 2-of-3 contested-finding voting,
  the hung-vote case

## Synthesis

- `synthesis-shapes.md` — the five synthesis shapes (convergence, highest severity, productive
  tension, blind spot, verdict) a council's collected findings resolve into

## Calibration

- `calibration-discipline.md` — why a council needs planted-defect fixtures, the promoted-script
  pattern, what a fixture proves and does not prove

## Two-phase model

- `two-phase-model.md` — blind first, deliberation second: the anchoring/groupthink rationale for
  the order, the chair's collection contract, the Project single-context degraded mode
