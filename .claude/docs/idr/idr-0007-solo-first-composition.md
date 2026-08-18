---
doc-type: idr
id: idr-0007
status: locked
date: 2026-08-18
owner: kim.granlund
proof-ref: gh#265 (measured hop tax, 2026-08-16 Findings) + teamwork/skills/fleet-rules/SKILL.md (Part B Design rule 1 — the solo-first gate and its job-evidence test)
provenance: derived-from-evidence
supersedes: null
---
# IDR-0007 — Solo-first composition: teams are escalations, not defaults

## Claim

Composition cost is real and compounding — every added seat re-pays the context-gathering phase
the host loop already paid, and coordination overhead grows with chain depth — so one context
holding the work is this estate's default unit, and every added seat must buy its coordination
tax with something the host provably cannot provide: isolation (fresh context), parallelism
(genuinely concurrent slices), or independence (generator≠critic on a high-stakes artifact).
Teams are escalations, not defaults. This elevates the HOW-grain doctrine already operating in
teamwork (`fleet-rules` Part B Design rule 1 — the solo-first gate and job-evidence test, merged
2026-08-17 from `team-or-solo-rules` per ADR-0020 D5) to a WHY-grain intent claim: the default
is not a style preference but a consequence of measured composition economics, and it binds
every future orchestration design in this estate, not only the skills that currently state it.

## Why

Provenance: derived-from-evidence — three convergent records. (1) gh#265's bounded experiment
(scorer fixed first, identical repo state, Findings recorded 2026-08-16): the same chore sweep
run solo-in-one-context vs. through the real seat chain (`chore-lead` → three parallel seats →
`chore-planner`) measured ≈1.92× output tokens and ≈3.6× wall-clock for the chain at equivalent
outcome quality — and the `mobilize-chores`/`sweep-chores` wrapper layers above the measured
chain were explicitly NOT counted, so the real flagship-flow tax is higher. (2) gh#266's build
outcome: held against that measurement and `script-writing-rules`' code-instead-of-prose
doctrine, `chore-lead` retired OUTRIGHT rather than shrinking — every step of its procedure
checked against genuine judgment content and found fully mechanical (reasoning recorded in
`harness/skills/sweep-chores/SKILL.md`'s Retirement note); an entire coordination seat proved to
be composition cost with no judgment content. (3) ADR-0010 (accepted 2026-08-10): the estate
collapsed per-kind dispatch logic and two adjacent seats into one uniform build seat rather than
growing the roster — the same economics acting on seat count before it was measured. Doubt would
come from the evidence base being one measured run on one repo state, and from the possibility
that platform changes (cheaper context assembly, native workflow primitives) shrink the tax.

## Proof

Confirms: repeat measurements in gh#265's shape agreeing in direction (chain materially more
expensive than solo at equivalent outcome quality); retired coordination seats staying retired
(no `chore-lead` re-mint); every new seat admitted under `fleet-rules`' job-evidence test citing
a concrete, named gap. Falsifies: a measured run in the same shape where an added coordination
seat delivers materially better outcomes at comparable-or-lower total cost WITHOUT buying
isolation, parallelism, or independence; or a recurring pattern of job-evidence-rejected seats
later proving necessary (the default systematically rejecting seats reality vindicates); or
hop-tax measurements trending to parity as the platform changes. Any of these means composition
cost is not real-and-compounding as claimed — supersede this record at that point, never edit it
in place once locked.
