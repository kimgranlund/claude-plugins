---
name: make-doc
description: >-
  Author a functional document — ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, or TASK — through
  gated phases: type routing (often not the type asked for), intent capture, draft from the
  template, language pass, doc_lint validation. Use when the user wants to write, draft, author,
  or record a document directly — "write the PRD for this feature", "draft an ADR about the
  database choice", "author a new SPEC for this system directly", "spec out the checkout flow",
  "write the PLAN for this migration". Also runs via /make-doc [type and intent]. Human-timed;
  writes one document. NOT for the rules themselves (doc-writing-rules); NOT for reviewing
  a document (check-doc); NOT for feature intake (feature — routes here for the TICKET); NOT for
  migrating docs into the canonical layout (tidy-docs); NOT for a bug investigation
  end-to-end (file-bug, which calls this skill's TICKET path internally); NOT for a generic
  chore or follow-up record (file-task).
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

One batched round covering the type's load-bearing slots: for a SPEC, the testable requirements
and the non-goals; for an ADR, the alternatives actually considered; for a PLAN, each step's
done-when; for a TICKET, what it traces to. Where the harness plugin's find-the-ask and
break-down-problem are installed, use them here; where not, apply their discipline inline —
ambiguities surfaced as multiple-choice, structure before prose.

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
