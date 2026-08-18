---
name: make-doc
description: >-
  Author a functional document — ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK, IDR, or RDD —
  through gated phases: route, capture intent, draft, validate. Use it to write, draft, author,
  record, or spec out a document — "write the PRD for this feature", "mint the founding IDR for
  this project", "lock in the RDD for this release". Runs via /make-doc [type and intent]. NOT for
  the rules themselves (doc-writing-rules); NOT for reviewing (check-doc); NOT for feature intake
  (file-feature); NOT for building a rendered Artifact/report page from a design system
  (make-artifact).
disable-model-invocation: false
user-invocable: true
argument-hint: "[type] [one-line intent]"
---

# make-doc

make-doc produces one document that its own validator accepts and its consumers — human, agent,
and hook — can read. Seed: `$ARGUMENTS`; invoked with none (a model-triggered ask, not a typed
`/make-doc`), take the type and intent straight from the conversation instead. Invoke
`doc-writing-rules` now; the classes, practices, and type contracts below are its, not
restated here.

## Phase 1 — Route the type

Map the intent to the question being answered (the standards' routing table). Challenge the asked
type once if the intent mismatches it: "record why we chose X" asked as a SPEC is an ADR; a "plan"
listing requirements is a SPEC. A document answering two questions becomes two documents joined by
IDs — say so and forge them in dependency order.

## Phase 2 — Capture intent

One batched round covering the type's load-bearing slots: for a SPEC, the testable requirements,
the non-goals, and — same round, not a follow-up — how the coding agent will autonomously verify
each requirement without a human in the loop (the `## Agent verification` section; a genuinely
human-only criterion is named as an exception, not left silent); for a PRD, the outcomes, the
non-goals, and the same question at Outcome grain — how an agent would tell each Outcome was
achieved; for an LLD, the components/interfaces and which existing instrument (evals suite, script
selftest, release-gate check) already verifies the design, or what harness this build must create
first; for an ADR, the alternatives actually considered; for a PLAN, each step's done-when; for a
TICKET, what it traces to; for an IDR, the admission test — "would two reasonable
builds differ on it?" — same spirit as ADR's own "a choice someone will later ask why about" gate;
a claim that fails it isn't an IDR, and the round ends there rather than minting one; for an RDD,
the Scope admission test — "could two reasonable teams ship different releases from this roadmap
line?" — a line that fails it doesn't earn its own RDD, and the round ends there before minting
one, same as IDR's own gate. Consult docs' `agent-harness-rules` for how to choose the assert layer or design the harness —
this phase only asks the question, that pack answers how. Where the harness plugin's find-intent and break-down-problem are
installed, use them here; where not, apply
their discipline inline — ambiguities surfaced as multiple-choice, structure before prose.

## Phase 3 — Draft from the template

Copy `references/templates/<type>.md` (in doc-writing-rules) and fill it — the template is
the contract, not a suggestion: frontmatter complete, required sections present, head-first
ordering, IDs minted where the type carries them (REQ-, OUT-, step numbers), substrate referenced
never restated. Instance filename per the standards: type, number/date, slug, in the type's
directory, per doc-writing-rules' canonical map (`docs/adr/`, `docs/spec/`, ...).

## Phase 4 — Language pass

Requirements phrased so they can fail; statuses as enums, never sentences; examples marked
NORMATIVE or ILLUSTRATIVE; non-goals concrete enough to block scope creep. Where
prompt-wording-rules is installed, run its pass; otherwise apply this paragraph as the checklist.

## Phase 5 — Validate

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doc_lint.py" <file>` — fix and re-run until clean. Report:
type, id, path, the IDs minted, and the documents it links (a contract's consumers, a ticket's
spec). Done when the lint is clean and every link resolves. NOT done if a section was deleted to
satisfy the linter instead of written — an empty required section is a finding for the user, not
a formatting problem.
