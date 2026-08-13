---
name: file-bug
description: >-
  Capture a user-reported bug as a durable record, then dispatch the investigation. Use when the
  user reports something broken, gives a repro or wrong output, flags a regression, or phrases it
  as "file a github issue for this crash" / "open an issue about this bug". /file-bug [raw
  report, or a TKT-/#issue/adapter id] resumes. NOT for a feature idea (file-feature); NOT for a
  chore/task (file-task); NOT for platform questions (github-facts).
disable-model-invocation: false
user-invocable: true
context: fork
argument-hint: "[raw bug report, or a TKT-/#issue/adapter-native id to resume]"
---

# file-bug

file-bug turns a raw bug report into a durable, classified record before any investigation
begins, and supersedes ad hoc `/fork bug-name ...` for bug work — a fork that carries the report
and its findings and nothing else is exactly the failure this replaces. Runs as a background fork
(`context: fork`) by default: the whole flow below executes off the caller's session, and the
record — not the fork's transcript — is what the report and findings live in, so this stays the
fix `/fork bug-name` lacked even though the skill itself now runs forked. The fork sees no
conversation history — `$ARGUMENTS` is the only channel in; Phase 2 covers what a thin seed owes.
Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run):** call doc-writing-rules' backend resolver
(`references/backend-resolver.md`) once; it returns Option A (local — the file backend, make-doc's
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

Invoke find-intent on the raw report: separate the literal complaint from the root cause, and
produce a repro (or the explicit statement "no fixed repro" for an intermittent or subjective
report). Where find-intent is not installed, apply its discipline inline — one batched round of
clarifying questions, never more, asked via `AskUserQuestion`. A live user is the default
assumption — running forked (`context: fork`) does not change it: forking relieves the caller's
session, it does not remove the person, and the fork still reaches the user directly. Skip
straight to capture-with-gaps only when the seed itself carries one of the two shared markers
(canonical statement: `file-task`'s Phase 2): `[redirected-from:X]` — the one-batched-round
budget was already spent upstream; a live user may well still be present, this only means don't
ask twice — or `[unattended]` — no live user backs the run at all. A seed that references context
the fork cannot see ("the crash above", "that test", "what we discussed") is itself a gap, not a
reason to guess: ask for the actual evidence via the same round — `$ARGUMENTS` is the fork's only
channel in, it carries no conversation history. Missing detail after the round, or no round at
all, does not block capture: write the ticket with what is known and name the gap in
Classification, rather than delaying persistence for completeness.

## Phase 3 — Classify

Invoke break-down-problem (or apply its two-plane lens inline where not installed) to name the axis
the bug lands on — functional, structural, visual, subjective, or another named axis — and the
specific component or plane it implicates. This is not a fixed enum: name the real axis: do not
force-fit one of the four examples.

On the FIRST classification only (the seed carries no `[redirected-from:X]` marker yet), the
capture reveals no defect at all — a capability request ("it should also do X"), or a generic
chore/follow-up with nothing to reproduce → invoke `file-feature` or `file-task` respectively via
the Skill tool, carrying the seed prefixed `[redirected-from:file-bug]`; report which sibling was
invoked and why; file-bug ends there — Phases 4–6 never run for a redirected seed. One hop only
(the siblings' shared redirect rule, `file-task`'s SKILL.md): a seed that already carries a
`[redirected-from:X]` marker (naming a DIFFERENT sibling) is captured regardless of fit — mint the
`kind: bug` record anyway, naming the shape mismatch in Classification, per this skill's own named
fallback in the shared rule. This skill's own redirect (above) never fires on a seed that already
carries the marker — one hop only, detected from the seed itself, not from history the fork
doesn't have.

## Phase 4 — Record

The payload contract, identical regardless of backend: `kind: bug`, the type's standard
Summary/Acceptance/Links plus Repro, Expected vs actual, Classification, Severity
(`blocker | major | minor | cosmetic` — the one scale doc-writing-rules' "Bug-shaped
tickets" defines; use it, never invent one per ticket), and an empty Findings section.

- **Option A (local/file backend):** mint or update a TICKET via make-doc's TICKET path
  (`doc-writing-rules` references/templates/ticket.md), in `docs/tickets/` of the local or
  target repo — repo-rooted per doc-writing-rules' location-and-naming rule, never written
  under a plugin's own installed directory. Run `doc_lint.py` on the result — fix and re-run until
  clean.
- **Option B (git-native):** `gh issue create` (no `--type`) — title = the Summary line; body =
  the same sections as `##` headings; labels `bug` + the severity. Once created, a second call —
  `gh issue edit <id> --type Bug` (ADR-0004) — attempts the native Issue Type; if it fails (the
  org's type schema doesn't resolve, or `gh` doesn't recognize `--type`), the issue already exists
  with the label alone, note the skipped type in the close-out — never retry the create itself
  over a type failure (two separate calls, never combined: a combined
  `gh issue create --type` was found to create the issue and only then fail the type step, so
  treating that error as "nothing created" would mint a duplicate). `doc_lint.py` validates files,
  not issues — the section contract above is this skill's own gate here: an issue missing a
  required section is not a captured record; edit it before proceeding.
- **Option C (external, e.g. Linear):** the resolved adapter's `create` operation
  (`doc-writing-rules` references/linear-adapter.md for Linear; a bring-your-own adapter
  documents its own) — the same payload contract mapped onto that backend's native fields. A
  create call that fails partway falls back to the file backend for this operation and reports the
  fallback in the close-out; never leave the report uncaptured because the preferred store was
  unreachable.

The record exists (on disk, or as a created issue whose URL is reported) before Phase 5 starts;
this ordering is the entire fix, and it does not move.

`.github/ISSUE_TEMPLATE/bug.yml` mirrors this contract for a human filing directly on GitHub.

## Phase 5 — Dispatch, or fix inline

Root cause already evident from Phase 2/3 → fix inline; file-bug itself appends the dated
`## Findings` entry naming the fix's location before closing. No investigation to dispatch, but
the ticket-first ordering is unchanged — only the dispatch step is skipped. **An inline fix that
semantically edits a prompt-carrying artifact — a SKILL.md body, an agent definition, a hook
prompt — gets a fresh-context checker pass (the matching `*-checker` agent) before the issue
closes**, the same gate make-skill's P5 applies at forge time: lint and release gates prove
mechanics, not semantics, and a 2026-08-11 estate audit found every recent unaudited inline
semantic edit carrying a real gap. A pure code/config fix under the repo's own test gates needs
no checker seat.

Otherwise, decide fork vs. agent: an agent only when the investigation needs tool restriction,
parallelism, or multi-skill preload; a fork for everything else (harness's fork-vs-agent gate; apply
this test inline where harness is not installed). The dispatch prompt is a contract, not a
suggestion: it names the record — the ticket's path, or the issue number + `gh issue comment` as
the write-back verb — and requires a dated `## Findings` entry (file section, or issue comment) at
*each* significant result — repro confirmed, root cause found — not only at the very end, so a
fork killed mid-investigation has still left something behind. Its stopping predicate includes at
least one such entry before the work counts as done.

Where teamwork's `loop-rules` is installed, run this dispatch under `/goal` rather than an
open-ended fork — "a dated Findings entry exists" is exactly the verifiable end-state a goal needs,
and a turn cap (5 tries, per loop-rules's own recipe) turns a stuck investigation into a reported
blocker instead of a silently abandoned one. Where loop-rules is not installed, apply its
discipline inline: name the stopping predicate, cap the tries, escalate on the same check failing
twice.

**Retiring a scratch branch this step used — verified, never raw.** `dispatch-ticket`'s Phase 3
owns teardown for the branch it creates when it isolates ahead of a hand-off here — file-bug
creates no isolation of its own for that case. This clause covers only a branch file-bug itself
is responsible for retiring: the inline fix above, once its PR is gone (merged or closed) and the
branch is no longer needed, or a dispatched fork/agent's own investigation branch once abandoned
with nothing landed. Either way, never delete it with a raw `git branch -D` plus worktree removal
— that force-deletes work with no proof it's safe to lose. Feature-detect the host repo's own
gated reap script (the reference shape: gen-ui-kit's `scripts/ops/reap-branches.mjs
--verify-branch <name>`). Order matters: `git worktree remove` first — a branch still checked out
in a worktree reads as KEPT regardless of merge state, so removing the worktree first is what
makes the merge check meaningful, and the removal itself refuses on a dirty tree, so nothing is
lost even on a wrong call — THEN `--verify-branch`, THEN, only on exit 0 (provably merged: a
merge-base ancestor of `origin/main`, or an exactly-matching MERGED PR), `git branch -d` (never
`-D`, even after a verified 0). Exit 1 (KEPT/PROPOSED), or either verb refusing outright, → leave
the branch standing and report why, never escalate to a force flag. Exit 2 is a usage error, not
a keep/delete verdict — report it rather than guessing. Where the host repo ships no such script
at that path, fall back to an unverified `git worktree remove` then `git branch -d`, but never
silently — name in the close-out exactly what went unverified.

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
  never leave the report uncaptured because the preferred store was unreachable. A failed
  `gh issue edit --type` (Phase 4) is not this failure — the record already exists by the time
  that call runs; it never triggers the file-backend fallback, only the skipped-type note.
- Workspace rules Option C but the adapter operation fails partway (auth, API error, MCP
  disconnect) → same fallback discipline, to the file backend for that operation, noted in the
  record.

Done when a `kind: bug` record exists — a `doc-type: ticket` file on disk, a labeled GitHub Issue,
or an Option-C adapter's record (its native id reported) — carrying the report and classification,
and either file-bug's own
inline fix or the dispatched investigation has left at least one dated `## Findings` entry (file
section or issue comment) — OR the seed was redirected to `file-feature`/`file-task` under the one-hop rule
(first classification only) and the sibling invocation was reported; no bug record is owed on a
redirected seed, and no build is dispatched BY THIS SKILL either way — a sibling reached by
redirect runs its own contract, including its own build/no-build rule.
