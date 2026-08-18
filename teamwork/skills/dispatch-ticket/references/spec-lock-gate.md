# Spec-lock gate — Phase 3.6's full procedure (#655 decision 3, ratified 2026-08-18)

Cited from `dispatch-ticket/SKILL.md`'s Phase 3.6 heading rather than restated inline (the same
F6 split-to-references pattern as Phase 3.5's `de-stale-premise-check.md`) — this is the phase's
actual contract, not optional background.

## Why this gate exists

A build dispatched against a ticket whose earned upstream record is still `draft`/`proposed` is
building on a moving target — the same class of risk Phase 3.5 catches for a stale PREMISE, here
caught for a stale CONTRACT: the record the ticket cites hasn't finished its own review loop yet,
so a build against it may be re-litigated the moment that record locks. And a ticket whose
materiality already earns a rung of the ladder (`docs:doc-writing-rules`' Owed chain: ticket only
→ +LLD (`size:big`) → +ADR (contract-changing) → +SPEC (externally-consumed) → +PRD entry
(product-visible) → +RDD (release-grain)) but carries no citation for it at all was never sized
against that record — an LLD-owing `size:big` ticket built with no LLD in evidence is exactly the
gap the ladder exists to close.

## Trigger A — a cited upstream is itself unlocked

1. Read the record's own `## Links` section (git-native: the issue body; file backend: the
   TICKET/TASK file's Links section) for any doc id it names — `idr-NNNN`, `adr-NNNN`,
   `spec-<slug>`, `rdd-NNNN` (LLD is excluded from this trigger — an LLD is the ticket's OWN design
   doc, still being authored during the same build, not an upstream lock target; PRD is checked
   under Trigger B only, since a PRD entry has no independent lock state of its own to test here).
2. For each cited id, resolve the file (`.claude/docs/{adr,idr,spec,rdd}/...` per
   `doc-writing-rules`' docs-root convention) and read its own frontmatter `status:` field —
   **frontmatter only**; a status mentioned in that document's own prose (its Context/Why section)
   is advisory, never authoritative for this gate.
3. Any cited id whose `status:` is a pre-lock value (`draft` for IDR/RDD, `proposed` for ADR,
   `draft` for SPEC — never a doc type's terminal `locked`/`accepted`/`approved`) → the gate fires.
4. A citation this dispatch cannot resolve (dangling id, file missing) is reported alongside the
   trigger as its own named gap — never silently treated as clean.

## Trigger B — the owed ladder names a rung with no citation at all

1. Determine the record's owed rungs from Phase 4's own materiality signals (the same read Phase 1
   already did): `size:big` label → owes `+LLD`; a contract-changing signal → owes `+ADR`; an
   externally-consumed-surface signal → owes `+SPEC`; a product-visible-capability signal → owes
   `+PRD entry`; a release-grain-commitment signal → owes `+RDD`. Each rung is additive (a
   release-grain ticket owes all five, not RDD alone).
2. For each owed rung, the record's `## Links` section must name at least one id of that doc type.
   Zero ids of an owed type → the gate fires for that rung, named explicitly (never a bare
   "something's missing" — the report names which rung and why the ticket's own signals earn it).
3. A rung with no signal present is simply not owed — silence on a rung nothing earns is the
   healthy default, not a finding.

## Outcome

Either trigger → **a named blocker report** (the same class Phase 1's ambiguous-match blocker
already reports through — never a new outcome type; unlike Phase 3.5's ticket-is-wrong
`stale-premise`, a spec-lock hit means the ticket is right but something upstream isn't ready
yet, which is what a blocker already means). The report names: which trigger fired, the specific
citation or missing rung, and — for Trigger A — the unlocked document's own id and `status:`
value as read. **This is post-claim** (Phase 3.6 runs after Phase 3's claim): release the claim
per Phase 3's Release-on-abandonment bullet and tear down the worktree per its teardown bullet (or
N/A when Phase 3 took the #204 host-checkout skip — no worktree exists to tear down) before
returning the blocker, exactly as any other post-claim mid-flight exit.

## Worked fixtures

**Fixture 1 — Trigger A (a cited upstream is unlocked).** A `size:big` ticket's Links section
reads `Links: adr-0099 (this ticket's contract), lld-example-feature`. `adr-0099`'s own
frontmatter carries `status: proposed`. The gate fires: "Phase 3.6 blocker — Trigger A: this
ticket cites adr-0099, whose own frontmatter reads `status: proposed` (not yet `accepted`) —
build blocked until adr-0099 locks or the citation is dropped."

**Fixture 2 — Trigger B (an owed rung carries no citation).** A `size:big` ticket's Links section
reads `Links: (none)` — no doc id of any kind. The owed ladder requires `+LLD` for `size:big`; zero
`lld-*` ids are cited. The gate fires: "Phase 3.6 blocker — Trigger B: this ticket is `size:big`,
which owes `+LLD` per the owed ladder (`docs:doc-writing-rules`' Owed chain); no `lld-*` id
appears in Links — build blocked until an LLD is authored and cited, or the ticket's own size is
corrected."

Both fixtures are text-presence proof of the gate's two trigger conditions, not executable
harnesses — `dispatch-ticket` carries no bundled script (a prose procedure has none to run), so
the mechanized proof this gate owns is the trigger logic itself standing here in enough detail
that a builder or a checker can trace a real ticket against it and get the same verdict.
