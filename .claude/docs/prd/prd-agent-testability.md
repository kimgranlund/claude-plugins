---
doc-type: prd
id: prd-agent-testability
status: draft
version: 0.1.0
date: 2026-08-17
owner: kim.granlund
---
# PRD — Agent-testability doctrine: every SPEC answers "how does the coding agent autonomously test and use this"

## Problem

Nothing in this estate's doc contracts or intake flows forces the question *"how will the coding
agent autonomously test and use this system?"* to be answered at design time. A SPEC's
`## Acceptance` section requires one criterion per requirement (doc-writing-rules practice 5), but
nothing requires those criteria to be **agent-executable**: a criterion satisfied only by a human
eyeballing a screenshot passes every current check. A feature ticket's `Acceptance` section
(file-feature Phase 5 payload) has the same gap. The result is verification bolted on after the
build instead of designed in — the motivating case (#542) being a Gen-UI chat system whose QA ran
through claude-in-chrome browser automation, screenshots, and human-in-the-loop payload exports,
when most of its verification could have happened programmatically at the pure-JSON payload layer
had a harness been designed with the system. Kim ruled 2026-08-17 (issue #542, re-route): this is
feature-shaped capability/corpus work with two deliverable surfaces — a doctrine/contract surface
in the docs plugin, and a testing-foundation knowledge corpus grounded in the Gen-UI case. This
PRD is the design record for both, mirroring the scoping-PRD shape `prd-idr-framework.md` (#273)
and `prd-rdd-framework.md` (#318) set: decisions and enumerated build scope, not the build.

## Users

**Primary:** the seat authoring a SPEC or minting a feature record — today it can lock intent with
zero thought about how an agent verifies it; after this, the type contract and the intake round
both ask. **Secondary:** the build seat (`/build-feature`, teamwork's builder) that inherits a
verification plan instead of inventing QA post-hoc; `check-doc` reviewers, who gain a named
criterion for "these acceptance lines are un-runnable by an agent"; any repo (the Gen-UI system
first) designing an agent-native verification harness from the corpus this PRD scopes.

## Outcomes

- **OUT-01** — doc-writing-rules' SPEC type contract carries an **`## Agent verification`**
  section: how the coding agent autonomously exercises the system and checks each acceptance
  criterion — which layer it asserts at, with what harness/fixtures, and which criteria (if any)
  genuinely need a human, stated as exceptions (exception form subject to Open question 3).
  Verifiable: the section exists in
  `references/templates/spec.md` and the SKILL.md type-contract row names it.
- **OUT-02** — `doc_lint.py` makes the requirement lint-visible: a new **T9 WARN** on a
  `doc-type: spec` file missing the `## Agent verification` heading — WARN, not FAIL, because
  three existing draft SPECs (`spec-linear-adapter`, `spec-naming-convention`,
  `spec-ticketing-watch-triage`) predate the section and would break on a hard gate (the same
  retrofit-debt reasoning that made T6 a WARN where T7 is a FAIL). Verifiable by selftest fixture
  pair: spec without the heading → T9 WARN; spec with it → silent.
- **OUT-03** — the authoring and review surfaces prompt and judge it: `make-doc` Phase 2's SPEC
  slot asks the agent-verification question in the same batched round as requirements and
  non-goals; `check-doc` gains judgment criterion **J7 (agent-testability)** — every acceptance
  criterion executable by the coding agent without a human in the loop, human-only criteria
  flagged unless explicitly justified. Verifiable by the two SKILL.md edits landing with their
  critic passes.
- **OUT-04** — `file-feature`'s intake asks the question for every big feature: the Phase 5
  payload's Acceptance section carries the agent-verification answer (or an explicit "needs a
  harness first" finding in Scope/Open). Documented-convention tier on tickets, same enforcement
  class as the Rejected-alternatives-at-close rule — not a doc_lint gate. Verifiable:
  file-feature's SKILL.md Phase 2 extraction and Phase 5 payload contract name the question and
  the Acceptance-carried answer form.
- **OUT-05** — a knowledge corpus encodes the testing-foundation framework — how to design
  lower-level, agent-native verification harnesses — with the Gen-UI JSON-payload-layer harness
  as its grounding case. Verifiable: the pack exists, passes `corpus_check.py`, and its INDEX
  answers the five question types enumerated under D5 below.

## Non-goals

- **Not building any of the implementation surface here.** doc_lint T9, template/SKILL edits,
  intake edits, and the corpus are enumerated as waved build scope below — this PRD scopes, the
  waves build, exactly as #273/#318 preceded #316/#332.
- **Not a hard FAIL gate on SPECs.** Retrofit debt is real (three live instances); T9 lands WARN.
  Escalating to FAIL once all instances are retrofitted is a possible future ruling, not scoped.
- **Not extending the contract to PRD.** A PRD is why/what before any how — an agent-verification
  plan there would be premature mechanics in the wrong type (one question per type). LLD gets
  judgment-tier coverage only (J7 applies wherever acceptance-shaped content appears), no new
  required section.
- **Not building the Gen-UI harness itself.** The corpus encodes the method and uses Gen-UI as
  the worked grounding case; the harness build belongs to that system's own repo and tickets.
- **Not retrofitting the three existing SPECs in the doctrine waves.** They warn (expected, the
  T6 pattern) until their own retrofit ticket clears them — enumerated as deferred scope.
- **Not an ADR.** Per the standing ADR-default-no ruling: no architectural fork is ratified —
  the design extends existing mechanics (a T-check, a template section, a judgment criterion, a
  knowledge pack) along patterns each already has a precedent for.

## Design decisions

### D1 — Doctrine home: doc-writing-rules' SPEC contract, not a new home

The doctrine's contract half lives where the SPEC type contract already lives:
`doc-writing-rules` (SKILL.md type-contract table + `references/templates/spec.md`), enforced by
`doc_lint.py`, prompted by `make-doc`, judged by `check-doc`. Rejected: a new standalone doctrine
skill (a second home for SPEC rules is a drift pair with the first); `product-lifecycle-rules`
(it owns the loop/record model, not per-type section contracts — it may gain a one-line pointer,
nothing more).

### D2 — Which types carry it: SPEC required-by-template, TICKET by intake convention, LLD judgment-only

SPEC is the type whose whole purpose is "intent as testable contract" — it carries the section.
Feature TICKETs carry the answer through file-feature's intake round and payload contract
(documented convention, un-gated — work items are freely edited while open and backend-portable,
so a lint gate has no purchase on Option B/C backends anyway). PRD: none (Non-goals). LLD: J7
judgment applies at check-doc time; no template change.

### D3 — Enforcement tier: T9 WARN now, judgment (J7) for substance

Mechanics (`doc_lint.py`) can only see the heading; whether the plan is real — the right assert
layer, runnable criteria — is judgment, so the substance check lands in check-doc J7 and in the
corpus's own rubric, not in a regex. This mirrors the estate's standing split: lint proves
mechanics, critics prove semantics.

### D4 — Corpus shape and home: a harness knowledge pack (recommended), name settled at build time

The framework answers ~5 distinct question types (below) — above the single-reference-doc
threshold, so `/make-pack` (one axis per wave), not `make-reference`. Recommended home:
**harness** — the estate's verification-instrument doctrine already lives there (checking-rules,
script-writing-rules, the G-gates); docs' research-methods is the adjacent method corpus and gets
a cross-link, not the pack. Name candidate: `test-design-rules` (the `*-rules` knowledge family);
final name goes through naming-rules/ADR-0011 at build time. Home and name are Open question 1 —
recommendation given, not silently ruled, since #542 itself flags this as needing a live round.

### D5 — Corpus axes (the five question types)

1. **Assert-layer choice** — where verification runs: pure-data/JSON payload layer vs API vs
   browser/UI vs human review; the cost/fidelity ladder and when each is the floor.
2. **Agent-native harness design** — driver agents with scoped instructions, tools, services,
   and integrations exercising the system as a user would; scenario definition; determinism and
   isolation requirements.
3. **Assertion and fixture grammar** — scenario fixtures, golden payloads, schema asserts,
   property checks; what makes a criterion agent-runnable vs eyeball-only.
4. **Estate mapping** — what a testing foundation concretely is for a plugin estate like this
   one: evals.json trigger suites (routing), bundled-script selftests (G4), release_gate G1–G11,
   `/check-routing` simulation — and the doctrine rule: a SPEC names which existing instrument
   verifies each criterion, or names the harness to build first.
5. **Grounding case: Gen-UI** — the worked example: a fleet of driver agents with custom
   instructions/tools driving chats, scenario verification asserted at the JSON payload layer,
   replacing claude-in-chrome/screenshot/human-in-the-loop QA.

## Implementation surface (waved build scope — enumerated, not built here)

**Wave 1 — docs plugin, contract surface** *(realizes OUT-01..03; one PR, one docs version bump)*
1. `references/templates/spec.md`: add `## Agent verification` with an authoring comment per
   OUT-01's section contract.
2. `doc_lint.py`: T9 WARN (spec missing the heading) + selftest fixtures (missing → WARN,
   present → silent, template self-consistency sweep stays green).
3. `doc-writing-rules` SKILL.md: SPEC row and failure catalog updated. **Note:** the T3 required
   sections list for spec is NOT extended (that would hard-FAIL the three live instances); the
   template carries the section, T9 carries the visibility.
4. `make-doc` Phase 2: SPEC slot gains the agent-verification question.
5. `check-doc`: J7 criterion. Every semantic edit in this wave rides its critic
   (skill-checker/doc-checker) per plugin-authoring.md; description changes, if any, update evals
   in the same change.

**Wave 2 — docs plugin, intake surface** *(realizes OUT-04; can ride Wave 1's PR or its own)*
6. `file-feature`: Phase 2 extraction asks the question for Work-shaped features; Phase 5 payload
   contract states the Acceptance-carried answer and the "needs a harness first" Scope/Open form.
7. `dispatch-ticket` (teamwork) build path: no contract change scoped — its Findings write-back
   already carries verification evidence; re-checked at build time, extended only if Wave 2
   review finds a gap.

**Wave 3 — the corpus** *(realizes OUT-05; gated on Open question 1's ruling)*
8. `/make-pack` the testing-foundation pack in the ruled home, axes per D5, one axis per wave per
   pack-writing-rules; Gen-UI grounding material gathered via fact-finder waves.

**Deferred (not blocking any wave)**
9. Retrofit the three existing SPECs' `## Agent verification` sections; optionally escalate T9
   WARN→FAIL once the estate is clean.
10. `product-lifecycle-rules` one-line pointer to the doctrine (spec-lock gate naming it).

## Gate output

```
$ python3 docs/scripts/doc_lint.py .claude/docs/prd/prd-agent-testability.md
doc_lint · clean · .claude/docs/prd/prd-agent-testability.md
```

No docs-plugin content touched by this PRD's own PR (a workspace doc under `.claude/docs/prd/`,
outside every plugin directory) — no plugin version bump or README ledger entry owed, the same
verified precedent as PRs #304/#318.

## Open questions for Kim

1. **Corpus home and name** (D4): harness `test-design-rules` is the recommendation — accept, or
   route it to docs (beside research-methods), or shrink to a single make-reference doc if the
   five axes read as fewer in the live round?
2. **Wave 2 rider**: fold the intake edits into Wave 1's PR (one docs bump) or keep a separate
   PR for review grain? Recommendation: one PR, two commits.
3. **Human-only criteria**: is the "named exceptions" escape hatch in `## Agent verification`
   acceptable, or should a SPEC with any human-only criterion require an explicit ruling line
   (e.g. `human-verify: justified`) that J7 checks for?
