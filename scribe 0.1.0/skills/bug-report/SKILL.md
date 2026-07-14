---
name: bug-report
description: >-
  Capture a user-reported bug — functional, structural, visual, or subjective — as a durable
  bug-shaped TICKET before any investigation starts, then dispatch the investigation (fork or
  agent) under a mandatory write-back contract. Closes the loss window raw `/fork bug-name ...`
  leaves open: report + findings lived only in the fork's context and vanished with it. Runs intent-extract (literal report vs. root cause and repro) and
  system-decompose (which part of the system is implicated) during capture, then doc-forge's
  TICKET path to record it, then dispatches with the ticket path as context. Run
  /bug-report [raw report, or an existing TKT- id to resume], e.g. "/bug-report the export button
  does nothing on Safari" or "/bug-report TKT-0031". Human-timed; writes one ticket, then one
  investigation. NOT for a feature idea or build request (feature / orchestration's build);
  NOT for non-bug documents (doc-forge); NOT for reviewing a doc
  (doc-review); NOT for intent extraction outside a bug (intent-extract).
disable-model-invocation: true
user-invocable: true
argument-hint: "[raw bug report, or an existing TKT- id to resume]"
---

# bug-report

bug-report turns a raw bug report into a durable, classified TICKET before any investigation
begins, and supersedes ad hoc `/fork bug-name ...` for bug work — a fork that carries the report
and its findings and nothing else is exactly the failure this replaces. Seed: `$ARGUMENTS`.

## Phase 1 — Route: fresh report, or resume by ticket state

`$ARGUMENTS` contains a ticket id (`tkt-####` / `TKT-####`, case-insensitive) resolving to a file
in `docs/tickets/` → this is a resume; branch by that ticket's own state, never re-dispatch
blindly:
- `## Findings` already carries an entry and status is still `open`/`doing` → Phase 6, to close
  the loop on what already came back — not a second investigation chasing the first.
- Extra text follows the id (new detail, a repro that did not exist before) → fold it into the
  ticket's Repro/Classification, then continue to Phase 5.
- Status is `done` or `wontfix` → report the closed state and stop; reopening is the user's call.
- Otherwise (open/doing, no findings yet) → continue directly to Phase 5.

An id that does not resolve to a file is not a resume: treat it as a fresh report, continue to
Phase 2, and say so — never proceed as if an unresolved id already had a record behind it.

## Phase 2 — Capture

Invoke intent-extract on the raw report: separate the literal complaint from the root cause, and
produce a repro (or the explicit statement "no fixed repro" for an intermittent or subjective
report). Where intent-extract is not installed, apply its discipline inline — one batched round of
clarifying questions, never more. Missing detail after that round does not block capture: write
the ticket with what is known and name the gap in Classification, rather than delaying
persistence for completeness.

## Phase 3 — Classify

Invoke system-decompose (or apply its two-plane lens inline where not installed) to name the axis
the bug lands on — functional, structural, visual, subjective, or another named axis — and the
specific component or plane it implicates. This is not a fixed enum: name the real axis: do not
force-fit one of the four examples.

## Phase 4 — Record

Mint or update a TICKET via doc-forge's TICKET path (`doc-authoring-standards`
references/templates/ticket.md), in `docs/tickets/` of the local or target repo — repo-rooted per
doc-authoring-standards' location-and-naming rule, never written under a plugin's own installed
directory — with `kind: bug` in frontmatter, carrying the
type's standard Summary/Acceptance/Links plus Repro, Expected vs actual, Classification, Severity
(`blocker | major | minor | cosmetic` — the one scale doc-authoring-standards' "Bug-shaped
tickets" defines; use it, never invent one per ticket), and an empty Findings section. Run
`doc_lint.py` on the result — fix and re-run until clean. The ticket exists on disk before Phase 5
starts; this ordering is the entire fix, and it does not move.

## Phase 5 — Dispatch, or fix inline

Root cause already evident from Phase 2/3 → fix inline; bug-report itself appends the dated
`## Findings` entry naming the fix's location before closing. No investigation to dispatch, but
the ticket-first ordering is unchanged — only the dispatch step is skipped.

Otherwise, decide fork vs. agent: an agent only when the investigation needs tool restriction,
parallelism, or multi-skill preload; a fork for everything else (forge's fork-vs-agent gate; apply
this test inline where forge is not installed). The dispatch prompt is a contract, not a
suggestion: it names the ticket's path, and requires a dated `## Findings` entry at *each*
significant result — repro confirmed, root cause found — not only at the very end, so a fork
killed mid-investigation has still left something behind. Its stopping predicate includes at least
one such entry before the work counts as done.

Where `orchestration`'s `loop-design` is installed, run this dispatch under `/goal` rather than an
open-ended fork — "a dated Findings entry exists" is exactly the verifiable end-state a goal needs,
and a turn cap (5 tries, per loop-design's own recipe) turns a stuck investigation into a reported
blocker instead of a silently abandoned one. Where loop-design is not installed, apply its
discipline inline: name the stopping predicate, cap the tries, escalate on the same check failing
twice.

## Phase 6 — Close the loop

Read the ticket back on return. Findings gained an entry → advance status (`open` to `doing`,
`done` once shipped, or `wontfix` for "will not fix" / "could not reproduce, not chasing further")
and report the ticket path and status. Findings gained no entry and the dispatch was an agent → one
re-dispatch with the contract quoted, then check again. Still nothing, or the dispatch was a fork
that is no longer addressable → append a dated "investigation returned with no findings recorded"
entry, leave status unchanged, and say so plainly. A fork's conversational summary never
substitutes for the entry it owed the ticket.

## Failure branches

- Report too vague after one clarifying round → capture anyway (Phase 2); the gap becomes a
  Classification note, not a blocker.
- Named id does not resolve to a file → treat as fresh (Phase 1); never proceed as if it existed.
- Resume finds unprocessed Findings → Phase 6, not a second dispatch (Phase 1's named branch).
- Resume finds `done`/`wontfix` → report and stop; do not reopen unasked.
- Agent dispatch returns with no Findings entry → one re-dispatch, contract quoted, before
  recording the loss (Phase 6). A fork that is no longer addressable skips straight to recording —
  it cannot be re-dispatched into.
- `doc_lint.py` fails on the drafted ticket → fix and re-run; an unlintable ticket is not a
  captured one.

Done when a `doc-type: ticket, kind: bug` file exists on disk carrying the report and
classification, and either bug-report's own inline fix or the dispatched investigation has left at
least one dated `## Findings` entry.
