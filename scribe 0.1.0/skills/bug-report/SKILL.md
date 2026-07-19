---
name: bug-report
description: >-
  Capture a user-reported bug — functional, structural, visual, or subjective — as a durable
  bug-shaped record before any investigation starts, then dispatch under a mandatory write-back
  contract. Use when the user reports something broken,
  gives a repro or wrong output, or flags a regression — "the export button does nothing on
  Safari", "this crashes when I click X", "this used to work and now it doesn't". Runs
  intent-extract and system-decompose during capture, then
  records — doc-forge's TICKET path by default, or the workspace's ruled backend (git-native, or a
  named external adapter) — and dispatches with the record as context. Also runs via /bug-report
  [raw report, or a TKT-/#issue/adapter id]. Writes one record, then one investigation. NOT for
  a feature idea or build request (feature / orchestration's build); NOT for a generic
  chore/follow-up/task (issue); NOT for non-bug documents (doc-forge); NOT for reviewing a doc
  (doc-review); NOT for intent extraction outside a bug (intent-extract).
disable-model-invocation: false
user-invocable: true
argument-hint: "[raw bug report, or a TKT-/#issue/adapter-native id to resume]"
---

# bug-report

bug-report turns a raw bug report into a durable, classified record before any investigation
begins, and supersedes ad hoc `/fork bug-name ...` for bug work — a fork that carries the report
and its findings and nothing else is exactly the failure this replaces. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run):** call doc-authoring-standards' backend resolver
(`references/backend-resolver.md`) once; it returns Option A (local — the file backend, doc-forge's
TICKET path into `docs/tickets/`), Option B (git-native — `gh issue`, an ADR-0002-style ruling), or
Option C (external — a named adapter; Linear's realization: `references/linear-adapter.md`, a
bring-your-own adapter documents its own). No ruling, or the ruled option's adapter is unreachable
→ Option A, exactly as always — consumers of this skill outside a ruled workspace see no change.
Every phase below follows whichever option the resolver returned: "ticket file" reads as "GitHub
Issue" under Option B, or as the named external adapter's own record under Option C — same payload
contract, same ordering, different store.

## Phase 1 — Route: fresh report, or resume by record state

`$ARGUMENTS` contains a record id — `tkt-####`/`TKT-####` (case-insensitive) resolving to a file
in `docs/tickets/`, on the git-native backend `#NN`/a bare issue number resolving via
`gh issue view`, or under Option C an id in the resolved adapter's own native format (Linear:
`TEAM-123`) resolving via that adapter's `read` operation (`references/linear-adapter.md`, REQ-010)
— → this is a resume; branch by that record's own state, never re-dispatch blindly:
- `## Findings` already carries an entry and status is still `open`/`doing` → Phase 6, to close
  the loop on what already came back — not a second investigation chasing the first.
- Extra text follows the id (new detail, a repro that did not exist before) → fold it into the
  ticket's Repro/Classification, then continue to Phase 5.
- Status is `done` or `wontfix` → report the closed state and stop; reopening is the user's call.
- Otherwise (open/doing, no findings yet) → continue directly to Phase 5.

An id that does not resolve (no such file; `gh issue view` errors; Option C's `read` returns
not-found, AC-010) is not a resume: treat it as a fresh report, continue to Phase 2, and say so —
never proceed as if an unresolved id already had a record behind it.

## Phase 2 — Capture

Invoke intent-extract on the raw report: separate the literal complaint from the root cause, and
produce a repro (or the explicit statement "no fixed repro" for an intermittent or subjective
report). Where intent-extract is not installed, apply its discipline inline — one batched round of
clarifying questions, never more, and only when a human is actually present to answer (a sibling
redirect, a subagent dispatch, or a scheduled/unattended firing has no one to ask — skip straight
to capture-with-gaps). Missing detail after the round, or no round at all, does not block capture:
write the ticket with what is known and name the gap in Classification, rather than delaying
persistence for completeness.

## Phase 3 — Classify

Invoke system-decompose (or apply its two-plane lens inline where not installed) to name the axis
the bug lands on — functional, structural, visual, subjective, or another named axis — and the
specific component or plane it implicates. This is not a fixed enum: name the real axis: do not
force-fit one of the four examples.

On the FIRST classification only, the capture reveals no defect at all — a capability request
("it should also do X"), or a generic chore/follow-up with nothing to reproduce → invoke `feature`
or `issue` respectively via the Skill tool, carrying the seed; report which sibling was invoked
and why; bug-report ends there — Phases 4–6 never run for a redirected seed. One hop only (the
siblings' shared redirect rule, `issue`'s SKILL.md): a seed that arrives HERE already redirected
from a sibling is captured regardless of fit — mint the `kind: bug` record anyway, naming the
shape mismatch in Classification, per this skill's own named fallback in the shared rule. This
skill's own redirect (above) never fires on a seed it did not originate the classification for.

## Phase 4 — Record

The payload contract, identical regardless of backend: `kind: bug`, the type's standard
Summary/Acceptance/Links plus Repro, Expected vs actual, Classification, Severity
(`blocker | major | minor | cosmetic` — the one scale doc-authoring-standards' "Bug-shaped
tickets" defines; use it, never invent one per ticket), and an empty Findings section.

- **Option A (local/file backend):** mint or update a TICKET via doc-forge's TICKET path
  (`doc-authoring-standards` references/templates/ticket.md), in `docs/tickets/` of the local or
  target repo — repo-rooted per doc-authoring-standards' location-and-naming rule, never written
  under a plugin's own installed directory. Run `doc_lint.py` on the result — fix and re-run until
  clean.
- **Option B (git-native):** `gh issue create --type Bug` — title = the Summary line; body = the
  same sections as `##` headings; labels `bug` + the severity, and sets the native Issue Type
  `Bug` (ADR-0004; fallback: retry without `--type` if the org's type schema doesn't resolve —
  label alone still lands, note the skipped type in the close-out). `doc_lint.py` validates files,
  not issues — the section contract above is this skill's own gate here: an issue missing a
  required section is not a captured record; edit it before proceeding.
- **Option C (external, e.g. Linear):** the resolved adapter's `create` operation
  (`doc-authoring-standards` references/linear-adapter.md for Linear; a bring-your-own adapter
  documents its own) — the same payload contract mapped onto that backend's native fields. A
  create call that fails partway falls back to the file backend for this operation and reports the
  fallback in the close-out; never leave the report uncaptured because the preferred store was
  unreachable.

The record exists (on disk, or as a created issue whose URL is reported) before Phase 5 starts;
this ordering is the entire fix, and it does not move.

`.github/ISSUE_TEMPLATE/bug.yml` mirrors this contract for a human filing directly on GitHub.

## Phase 5 — Dispatch, or fix inline

Root cause already evident from Phase 2/3 → fix inline; bug-report itself appends the dated
`## Findings` entry naming the fix's location before closing. No investigation to dispatch, but
the ticket-first ordering is unchanged — only the dispatch step is skipped.

Otherwise, decide fork vs. agent: an agent only when the investigation needs tool restriction,
parallelism, or multi-skill preload; a fork for everything else (forge's fork-vs-agent gate; apply
this test inline where forge is not installed). The dispatch prompt is a contract, not a
suggestion: it names the record — the ticket's path, or the issue number + `gh issue comment` as
the write-back verb — and requires a dated `## Findings` entry (file section, or issue comment) at
*each* significant result — repro confirmed, root cause found — not only at the very end, so a
fork killed mid-investigation has still left something behind. Its stopping predicate includes at
least one such entry before the work counts as done.

Where `orchestration`'s `loop-design` is installed, run this dispatch under `/goal` rather than an
open-ended fork — "a dated Findings entry exists" is exactly the verifiable end-state a goal needs,
and a turn cap (5 tries, per loop-design's own recipe) turns a stuck investigation into a reported
blocker instead of a silently abandoned one. Where loop-design is not installed, apply its
discipline inline: name the stopping predicate, cap the tries, escalate on the same check failing
twice.

## Phase 6 — Close the loop

Read the record back on return (`gh issue view --comments` on the git-native backend; the resolved
adapter's own read operation under Option C). Findings gained an entry → advance status — file
backend: frontmatter `open` → `doing`, `done` once shipped, or `wontfix`; git-native: `doing` is a
label, `done` closes the issue, `wontfix` closes with a `wontfix` label; Option C: the resolved
adapter's own status representation (Linear: a state of the mapped type — `doing`/`done`/`wontfix`
→ `started`/`completed`/`canceled`, `references/linear-adapter.md`, Findings-first, same ordering)
— and report the record (path,
issue URL, or adapter-native id) and status. Findings gained no entry and the dispatch was an
agent → one re-dispatch with the contract quoted, then check again.
Still nothing, or the dispatch was a fork that is no longer addressable → append a dated
"investigation returned with no findings recorded" entry (file section, or issue comment), leave
status unchanged, and say so plainly. A fork's conversational summary never substitutes for the
entry it owed the record.

## Failure branches

- Report too vague after one clarifying round → capture anyway (Phase 2); the gap becomes a
  Classification note, not a blocker.
- Classification (Phase 3) finds no defect on the FIRST classification → invoke the correct
  sibling via the Skill tool (Phase 3); never force a bug record onto non-bug work at this step.
  A seed arriving already redirected from a sibling is captured here regardless of fit (the
  one-hop rule's fallback, Phase 3) — this skill's own redirect never fires twice.
- Named id does not resolve (file or issue) → treat as fresh (Phase 1); never proceed as if it
  existed.
- Resume finds unprocessed Findings → Phase 6, not a second dispatch (Phase 1's named branch).
- Resume finds `done`/`wontfix`/closed → report and stop; do not reopen unasked.
- Agent dispatch returns with no Findings entry → one re-dispatch, contract quoted, before
  recording the loss (Phase 6). A fork that is no longer addressable skips straight to recording —
  it cannot be re-dispatched into.
- `doc_lint.py` fails on the drafted ticket → fix and re-run; an unlintable ticket is not a
  captured one (file backend).
- Workspace rules git-native but `gh` fails partway through a run (auth, network) → fall back to the file
  backend for THIS record, say so, and note the migration in the record so it can be re-homed —
  never leave the report uncaptured because the preferred store was unreachable. `--type` not
  resolving is NOT this failure, whether the org's type schema rejects it ("type X not found") or
  an older `gh` doesn't recognize the flag at all ("unknown flag") — it's the ADR-0004 fallback
  (Phase 4): retry the same `gh issue create` without `--type`, stay on git-native, never drop to
  the file backend over a missing Issue Type alone.
- Workspace rules Option C but the adapter operation fails partway (auth, API error, MCP
  disconnect) → same fallback discipline, to the file backend for that operation, noted in the
  record.

Done when a `kind: bug` record exists — a `doc-type: ticket` file on disk, a labeled GitHub Issue,
or an Option-C adapter's record (its native id reported) — carrying the report and classification,
and either bug-report's own
inline fix or the dispatched investigation has left at least one dated `## Findings` entry (file
section or issue comment) — OR the seed was redirected to `feature`/`issue` under the one-hop rule
(first classification only) and the sibling invocation was reported; no bug record is owed on a
redirected seed, and no build is dispatched BY THIS SKILL either way — a sibling reached by
redirect runs its own contract, including its own build/no-build rule.
