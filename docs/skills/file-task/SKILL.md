---
name: file-task
description: >-
  Capture a work item that's neither bug- nor feature-shaped — a chore, follow-up, or debt —
  as a durable record, then resume by id, fold new detail, append dated Findings, or advance
  status. Use for "note this down as a follow-up", "log this technical debt", "track this for
  later", "file a task for X", or /file-task #NN / tkt-#### to resume. NOT for bug-shaped
  reports (file-bug); NOT for feature ideas (file-feature).
disable-model-invocation: false
user-invocable: true
argument-hint: "[raw work item, or a #NN / TKT-#### / adapter-native id to resume]"
---

# issue — the generic work-item record, minted or resumed

Turns any work item into the smallest durable record that carries it — the sibling of
`file-bug` (defects) and `feature` (sized ideas) for everything those two fence out: chores,
follow-ups, research items, debts. One capture replaces the hand-rolled `gh issue create` whose
measured variance (missing labels, drifting section sets, no dedup, contractless closes) is this
skill's baseline evidence. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run):** call doc-writing-rules' backend resolver
(`references/backend-resolver.md`) once; it returns Option A (local — the file backend, make-doc's
TICKET path, repo-rooted per doc-writing-rules), Option B (git-native — `gh issue`, an
ADR-0002-style ruling), or Option C (external — a named adapter; Linear's realization:
`references/linear-adapter.md`, a bring-your-own adapter documents its own). No ruling, or the
ruled option's adapter is unreachable → Option A, exactly as always. Every phase below follows
whichever option the resolver returned: "ticket file" reads as "GitHub Issue" under Option B, or as
the named external adapter's own record under Option C — same payload contract, same ordering,
different store. Canonical statement: `file-bug`'s SKILL.md — this is the same seam, not a
second one; a drift between this paragraph and that one is a bug in this file, never the other way
round.

## Phase 1 — Route: fresh item, or resume by id

`$ARGUMENTS` starts with a record id — `#NN`/a bare issue number (git-native, resolved via
`gh issue view`), `tkt-####` (file backend), or under Option C an id in the resolved adapter's own
native format (Linear: `TEAM-123`) resolving via that adapter's `read` operation
(`references/linear-adapter.md`, REQ-010) — → this is a RESUME; branch on what follows the id,
never re-mint:

- **A status verb** — fires ONLY when the entire trailing text is one token from
  `done` · `doing` · `wontfix` (case-insensitive), with the single exception
  `wontfix <reason>` — anything else is new detail, even if it starts with a verb
  (`/file-task #19 done deal — see the PR` folds, never closes). Advance the record: git-native
  `doing` = a label, `done` = close (a dated Findings entry recording what shipped lands
  first), `wontfix` = close + `wontfix` label with the reason as a comment (file backend: the
  reason lands as the dated Findings entry; the frontmatter `status` field moves; Option C: the
  resolved adapter's own status representation — Linear: a state of the mapped type —
  `doing`/`done`/`wontfix` → `started`/`completed`/`canceled`, `references/linear-adapter.md`,
  Findings-first, same ordering). Closing a
  record with an EMPTY Findings section takes the close-out line as its first entry — a record
  never closes silent.
- **New detail** (any other trailing text) → fold it into the body's matching section (or append
  a dated `## Findings` comment when it is a result, not a scope change) and report the record.
- **Nothing after the id** → report the record's state, labels, and last Findings entry; stop.

A CLOSED record resumes only as a report — state it and stop; reopening is the user's call
(the siblings' shared rule). An id that does not resolve (no such file; `gh issue view` errors;
Option C's `read` returns not-found, AC-010) is a fresh item — say so, never proceed as if a
record existed. A bare number is an issue id on the git-native backend only; on the file backend
only `tkt-####` resolves; under Option C only the resolved adapter's own native format resolves.

## Phase 2 — Classify the shape (the routing gate)

On the FIRST classification only: a defect ("X is broken", a repro, a wrong output) → invoke
`file-bug` directly via the Skill tool, carrying the seed verbatim; report which sibling was
invoked and why, never leave the user to type the command themselves. A feature idea (new
capability, needs sizing or may earn docs) → same move, invoke `feature`. Neither — the generic
remainder — continues here. When genuinely ambiguous AND a human is present to ask, ONE
clarifying question; no interactive channel (a sibling redirect, a subagent dispatch, a
scheduled/unattended firing) or still ambiguous after asking → capture here as `task` with the
ambiguity named in Scope/Open (persistence beats taxonomy, and a question nobody can answer is
not a gate).

A seed arrives HERE already redirected from a sibling → captured regardless of fit: `task` with
the mismatch named in Scope/Open, per this skill's own named fallback below. This skill's own
redirect (above) never fires on a seed it did not originate the classification for.

**The one-hop-only redirect rule (shared by all three siblings):** a sibling reached by redirect
never redirects again — its own classification finding a poor fit is not license to bounce a
second time, only to capture under its own named fallback: **here** (`file-task`), `task` with the
ambiguity in Scope/Open; **`file-bug`**, `kind: bug` with the shape gap named in
Classification; **`file-feature`**, `kind: feature` with the gap named in Scope/Open. One hop resolves
genuine mis-routing; a second hop is thrash, not routing — the receiving skill always ends in a
captured record, never a second redirect.

## Phase 3 — Dedup: it may already exist

Sweep before minting, report what's found: open records (`gh issue list --search`, `docs/tickets/`,
or under Option C the resolved adapter's own `dedup-search` operation —
`references/backend-resolver.md` REQ-005), then the codebase/docs for the item's nouns. Already
queued → resume it (Phase 1 semantics); already done → report where and stop.

## Phase 4 — Record

The payload contract, identical regardless of backend and shared with the sibling commands —
doc-writing-rules' TICKET contract is the canon, this line its instantiation: **Summary ·
Acceptance (one checkable done-condition — a task without one gets "done when <the artifact>
exists", never nothing) · Links (the ID spine to any owning docs/PRs) · Scope/Open (named gaps,
when any) · an empty `## Findings` section** for dated write-backs.

- **Option A (local/file backend):** mint the TICKET via make-doc's TICKET path — frontmatter
  `doc-type: ticket, kind: task` — and run `doc_lint.py` until clean; an unlintable record is not
  a captured one.
- **Option B (git-native):** `gh issue create` (no `--type`) — title = the Summary line; body =
  the sections as `##` headings; labels `task` + `size:small`/`size:big` where the size is clear
  (unsized is legal for tasks). Once created, a second call — `gh issue edit <id> --type Task`
  (ADR-0004) — attempts the native Issue Type; if it fails (the org's type schema doesn't resolve,
  or `gh` doesn't recognize `--type`), the issue already exists with the label alone, note the
  skipped type in the close-out — never retry the create itself over a type failure (two separate
  calls, never combined: a combined `gh issue create --type` was found to create the issue and
  only then fail the type step, so treating that error as "nothing created" would mint a
  duplicate). Missing labels in the repo are created once (`gh label create`), not worked around.
  The section contract is this skill's own gate here: an issue missing a required section is not
  a captured record.
- **Option C (external, e.g. Linear):** the resolved adapter's `create` operation
  (`doc-writing-rules` references/linear-adapter.md for Linear; a bring-your-own adapter
  documents its own) — the same payload contract mapped onto that backend's native fields, `size`
  (where clear) carried as a label. A create call that fails partway falls back to the file
  backend for this operation and reports the fallback in the close-out; never leave the item
  uncaptured because the preferred store was unreachable.

The close-out reports the issue URL, ticket path, or adapter-native id — the record exists before
this skill stops; that ordering is the contract.

`.github/ISSUE_TEMPLATE/task.yml` mirrors this contract for a human filing directly on GitHub.

## Failure branches

- Backend ruled git-native but `gh` fails partway → fall back to the file backend for THIS
  record, say so, note the migration in the record (the shared sibling rule). A failed
  `gh issue edit --type` (Phase 4) is not this failure — the record already exists by the time
  that call runs; it never triggers the file-backend fallback, only the skipped-type note.
- Backend ruled Option C but the adapter operation fails partway (auth, API error, MCP
  disconnect) → same fallback discipline, to the file backend for that operation, noted in the
  record.
- The item is really a bug or feature in disguise → invoke the correct sibling (Phase 2) via the
  Skill tool with the seed; never force-file it as a task to save a hop.
- Resume finds the record closed → report its state; reopening is the user's explicit call.
- A status verb on an unresolved id → report the failed resolution; nothing is created.
- Dedup finds it shipped or queued → report, stop or resume; never a duplicate record.

Done when a `task`-labeled record exists (an issue URL reported, a lint-clean `kind: task`
TICKET on disk, or an Option-C adapter's record with its native id reported) carrying the full
payload contract — or a resume acted on the existing record
(detail folded, Findings appended, or status advanced with its Findings-first close rule) — the
dedup sweep ran, and NO build was dispatched (/build-feature's contract, where installed) — OR the seed
was redirected to `file-bug`/`feature` under the one-hop rule and the sibling invocation was
reported; no task record is owed on a redirected seed. NOT done while a close leaves Findings
empty, a duplicate was minted over a dedup hit, or a bug/feature shape was filed here instead of
routed.
