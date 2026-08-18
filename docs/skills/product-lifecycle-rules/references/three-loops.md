# The three nested loops — scope, cadence, authority

Source: `.claude/docs/spec/product-lifecycle-bible.md` Part 2 · "The three loops" — the general
model. This file distills it for retrieval; read the source directly for the full prose.
[verified] against the committed bible, v1.1.0, checked 2026-08-16.

Product work runs as three nested loops. Nesting is semantic — scope, cadence, and authority all
follow from loop depth, not just visual containment.

| Loop | Focus | Objective | Alignment doc | Turn cadence |
|---|---|---|---|---|
| **North star** (outer) | Intent capture · domain/market knowledge · core-loop hypotheses · the POC · the knowledge base itself | Validate the product thesis with a running proof of concept | **IDR** — index: the product brief | Slowest (yearly-ish); a superseded hypothesis is a **pivot** |
| **Foundation** (inner) | Applied design · foundational systems/services · test/CI/enforcement backbone · engineering patterns | Turn validated hypotheses into production-grade architecture — quality structural, not supervisory | **ADR** — index: the architecture overview | Quarterly-ish; re-architecture within a standing thesis |
| **Releases** (innermost) | Deployment & ops · shipped releases · feedback intake · the roadmap | Serve users, learn from production, compound the roadmap from what ships | **RDD** (this repo's realization of the bible's PRP — see `alignment-record-types.md`) — index: the roadmap | Weekly/continuous; a release |

[verified] bible Part 2, source table, checked 2026-08-16.

**IDR's scope binding (ruled #652, 2026-08-18):** the North star loop's alignment doc is IDR
because the loop's own Focus/Objective are whole-product — the product thesis, not one feature or
component of it. This is not incidental: an IDR minted at feature or component grain does not
belong to this loop at all, whatever its falsifiability, because the North star loop itself never
turns on a feature-grain claim — that evidence belongs to the Releases loop's RDD/roadmap
machinery instead (see "Escalation" below). A feature/component-grain hypothesis is PRD/SPEC
territory in the Releases loop, never an IDR promoted "up" a loop it doesn't actually occupy.

## Loop mechanics

- **Containment.** Inner loops work inside the outer loops' standing decisions and never edit them
  directly — they emit evidence outward.
- **Escalation.** Evidence that stays in scope iterates the current loop. Evidence breaking an
  assumption held one loop out climbs to that loop as a new record version, reason attached. A
  release finding that breaks a design assumption triggers a Foundation turn; foundation
  experience falsifying a product hypothesis climbs to the North star as a recorded pivot. This is
  the general mechanic behind "escalation rides the citations" (see `alignment-record-types.md`).
- **Version triple.** Outer turn ≈ major, inner ≈ minor, innermost ≈ patch. "Thesis 2, architecture
  2.3, release 2.3.17" is a complete status report in three numbers.
- **Concurrency.** Loops differ in emphasis, never exclusivity — all three run at once once a
  product is live. An outer loop that never turns is dogma; one that turns monthly is churn.

[verified] bible Part 2, "Loop mechanics" bullets, checked 2026-08-16.

## The POC boundary

The North star's first turn ends with a fairly complete proof of concept that functionally proves
the core hypotheses. The POC's *code is evidence, not product*. The Foundation loop inherits the
**validated hypotheses plus the knowledge base — never the POC codebase** — and rebuilds to the
contract at production grade. Keep the knowledge; regenerate the artifact. This is the bible's
answer to the classic throw-away-the-prototype debate: it makes the question a non-question,
because the codebase was never the thing being kept.

[verified] bible Part 2, "The POC boundary," checked 2026-08-16. Named anti-pattern for skipping
this step: "POC ossification" (see `knowledge-base-habits.md` and `anti-patterns-glossary.md`).

## Deliverables by loop

- **North star:** product brief, IDRs with proof references, the POC, the domain & market layer
  (glossary, indexed walkthrough videos, failure ledger, annotated prototype), the knowledge base
  stood up at kickoff.
- **Foundation:** design docs and ADRs, foundational services and platform code (the first loop
  where code *is* the product), the test/CI/enforcement backbone, promoted engineering patterns.
- **Releases:** RDDs (release commitments, the bible's PRP) with acceptance criteria, specs that
  point at the source of truth, shipped releases and changelogs, the living roadmap, feedback
  routed as evidence, the ops layer (dashboards, runbooks).

Each loop's headline deliverable is the next loop's starting context — an inner loop is handed the
outer loop's *record*, never its *work*.

[verified] bible Part 2, "Deliverables by loop," checked 2026-08-16.

## Boundary — general doctrine only

This file states the GENERAL three-loop model, portable to any project. It does not track which
loop or turn a specific project is currently in — that reading requires live signals (this repo's
own ADR/IDR/RDD state, roadmap position). As of 2026-08-16, `docs:check-stage` answers that
live-placement question (issue #336, `prd-lifecycle-stage-awareness.md`) — see `SKILL.md`'s
Boundaries section for the pointer.
