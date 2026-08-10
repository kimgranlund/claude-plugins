---
doc-type: adr
id: adr-0010
status: accepted
ratified: by Kim
date: 2026-08-10
owner: kim.granlund
---
# ADR-0010 — Generalize feature-lead to build-lead, dispatch-feature to dispatch-ticket

## Context

Designing the `/lead-*` session-priming family (2026-08-10) surfaced a duplication risk: the
planned `build-lead` agent — the standing build seat `/lead-build` adopts and `/init-repo`
spawns — would preload the same `dispatch-feature` procedure that `teamwork:feature-lead`
(shipped 1.3.0, issue #135) already preloads, and drive nearly the same job. The anti-matrix
rule requires a boundary answer before a new agent is built beside an existing one doing the
same work.

Simultaneously, `mobilize-chores` step 5 carries per-kind dispatch logic inline — `kind: task`
tickets get a hand-built clarify-then-dispatch path (find-intent round → `general-purpose`
agent → Findings contract) inside the sweep command itself, while `kind: feature` routes to
`feature-lead` and `kind: bug` to `file-bug`. The sweep owning per-kind execution logic was
always a smell: dispatch belongs to the seat.

Kim ruled (AskUserQuestion rounds, 2026-08-10): one build seat, managing every confirmed
ticket kind.

## Decision

1. `teamwork:feature-lead` is renamed **`build-lead`** and generalized: dispatched with one
   confirmed ticket id of ANY kind (`feature`, `task`, `bug`).
2. `teamwork:dispatch-feature` is renamed **`dispatch-ticket`** and generalized to branch by
   the record's kind: `feature` keeps the existing find-or-make/size/dispatch/close-loop path
   unchanged; `task` absorbs the clarify-then-dispatch logic previously inline in
   `mobilize-chores` step 5 (one owner — that logic is deleted at its old site in the same
   change); `bug` keeps the existing hand-off to `file-bug` with the `[redirected-from:]`
   marker.
3. `mobilize-chores` step 5 collapses to a uniform dispatch: every confirmed ticket →
   `Agent(subagent_type: "teamwork:build-lead")`, regardless of kind.
4. `/build-feature` keeps its name and feature-flavored charter (its body reference moves to
   `dispatch-ticket`); renaming the command was considered and deferred — its description
   already fences bugs to `file-bug`, and expanding the human-typed entry's scope is a
   separate decision from generalizing the programmatic seat.
5. Execution follows the rename-execution playbook (ADR-0007 Decision 2, as exercised by
   ADR-0009): `git mv` for path renames with frontmatter moved in the same change (lint
   F9/A6), live references rewritten, ledger history untouched, `fix_old_names.py derive`
   re-run — never hand-edited — in the same PR, version bumps and ledger entries for every
   touched plugin (teamwork MAJOR — names are APIs; docs and harness patch — pointer sweeps),
   gates clean.

## Rejected alternatives

- **`chores-lead`** (Kim's first candidate): one letter from harness's shipped `chore-lead` —
  a naming-rules test-5 (loud-contrast) failure across a plugin boundary — and misnames the
  job: the seat drives confirmed tickets to built, it does not sweep ops chores.
- **A new `build-lead` agent alongside `feature-lead`**: two seats preloading the same
  procedure with adjacent charters is exactly the duplication the anti-matrix rule exists to
  block; the general seat subsumes the narrow one.
- **Keeping per-kind dispatch inline in `mobilize-chores`**: leaves the task-kind execution
  contract owned by a sweep command instead of a seat, and every future kind grows the sweep
  instead of the seat's own procedure.

## Consequences

- One dispatch surface for "drive this confirmed ticket": human one-shot (`/build-feature`),
  programmatic (`Agent(teamwork:build-lead)`), and — planned — session-adopted
  (`/lead-build`, which reads `build-lead`'s contract; the `/lead-*` family ADR-less per the
  standing ADR-default-no ruling, this ADR covers only the rename fork).
- `mobilize-chores` shrinks: kind-routing knowledge leaves the sweep; a new buildable kind is
  a `dispatch-ticket` change only.
- `feature-lead` and `dispatch-feature` become retired names — `fix-old-names` detects them
  via the re-derived manifest; ledger and ADR history keep them as record.
- Issue #151's verification (feature-lead's live dispatch path, never fired) transfers to the
  renamed seat: the acceptance now reads build-lead, noted on the issue when this ships.
