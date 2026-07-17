---
name: issue
description: >-
  Capture ANY work item — a chore, follow-up, research item, debt, or task that is neither
  bug-shaped nor a feature idea — as a durable, labeled record, and drive that record's whole
  lifecycle: resume by id, fold new detail, append dated Findings, advance status. Records land
  on the workspace's ruled backend — a GitHub Issue (`kind: task` label + optional size) where
  the entry file rules git-native, a `kind: task` TICKET file everywhere else — with the same
  payload contract either way. Run /issue [raw item, or an id to resume], e.g. "/issue tighten
  the allowlist comments", "/issue #19 done", "/issue #19 also cover negated rules",
  "/issue TKT-0044". Human-timed; writes one record set, then stops. NOT for bug-shaped reports
  (bug-report — repro/dispatch); NOT for feature ideas that need sizing into docs (feature);
  NOT for building anything (/build, orchestration); NOT for other document types (doc-forge).
disable-model-invocation: true
user-invocable: true
argument-hint: "[raw work item, or a #NN / TKT-#### id to resume]"
---

# issue — the generic work-item record, minted or resumed

Turns any work item into the smallest durable record that carries it — the sibling of
`bug-report` (defects) and `feature` (sized ideas) for everything those two fence out: chores,
follow-ups, research items, debts. One capture replaces the hand-rolled `gh issue create` whose
measured variance (missing labels, drifting section sets, no dedup, contractless closes) is this
skill's baseline evidence. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run — bug-report's rule, shared verbatim):** the
record's home is the **file backend** (doc-forge's TICKET path, repo-rooted per
doc-authoring-standards) unless the hosting workspace's entry file routes work items to a
**git-native backend** (a routing-table row naming `gh issue`, an ADR-0002-style ruling) AND
`gh` is available — then every "ticket file" below reads "GitHub Issue": same payload contract,
same ordering, different store.

## Phase 1 — Route: fresh item, or resume by id

`$ARGUMENTS` starts with a record id — `#NN`/a bare issue number (git-native, resolved via
`gh issue view`) or `tkt-####` (file backend) — → this is a RESUME; branch on what follows the
id, never re-mint:

- **A status verb** — fires ONLY when the entire trailing text is one token from
  `done` · `doing` · `wontfix` (case-insensitive), with the single exception
  `wontfix <reason>` — anything else is new detail, even if it starts with a verb
  (`/issue #19 done deal — see the PR` folds, never closes). Advance the record: git-native
  `doing` = a label, `done` = close (a dated Findings entry recording what shipped lands
  first), `wontfix` = close + `wontfix` label with the reason as a comment (file backend: the
  reason lands as the dated Findings entry; the frontmatter `status` field moves). Closing a
  record with an EMPTY Findings section takes the close-out line as its first entry — a record
  never closes silent.
- **New detail** (any other trailing text) → fold it into the body's matching section (or append
  a dated `## Findings` comment when it is a result, not a scope change) and report the record.
- **Nothing after the id** → report the record's state, labels, and last Findings entry; stop.

A CLOSED record resumes only as a report — state it and stop; reopening is the user's call
(the siblings' shared rule). An id that does not resolve is a fresh item — say so, never
proceed as if a record existed. A bare number is an issue id on the git-native backend only;
on the file backend only `tkt-####` resolves.

## Phase 2 — Classify the shape (the routing gate)

A defect ("X is broken", a repro, a wrong output) → stop and point: report the shape and name
the command to run (`/bug-report <the seed>`) — both siblings are user-invoked commands this
skill cannot invoke for you. A feature idea (new capability, needs sizing or may earn docs) →
same move, `/feature <the seed>`. Neither — the generic remainder — continues here. When genuinely ambiguous, ONE clarifying question; still ambiguous → capture
here as `task` with the ambiguity named in Scope/Open (persistence beats taxonomy).

## Phase 3 — Dedup: it may already exist

Sweep before minting, report what's found: open records (`gh issue list --search`, or
`docs/tickets/`), then the codebase/docs for the item's nouns. Already queued → resume it
(Phase 1 semantics); already done → report where and stop.

## Phase 4 — Record

The payload contract, identical on both backends and shared with the sibling commands —
doc-authoring-standards' TICKET contract is the canon, this line its instantiation: **Summary ·
Acceptance (one checkable done-condition — a task without one gets "done when <the artifact>
exists", never nothing) · Links (the ID spine to any owning docs/PRs) · Scope/Open (named gaps,
when any) · an empty `## Findings` section** for dated write-backs.

- **Git-native backend:** `gh issue create` — title = the Summary line; body = the sections as
  `##` headings; labels `task` + `size:small`/`size:big` where the size is clear (unsized is
  legal for tasks). Missing labels in the repo are created once (`gh label create`), not worked
  around. The section contract is this skill's own gate here: an issue missing a required
  section is not a captured record.
- **File backend:** mint the TICKET via doc-forge's TICKET path — frontmatter `doc-type: ticket,
  kind: task` — and run `doc_lint.py` until clean; an unlintable record is not a captured one.

The close-out reports the issue URL (or ticket path) — the record exists before this skill
stops; that ordering is the contract.

`.github/ISSUE_TEMPLATE/task.yml` mirrors this contract for a human filing directly on GitHub.

## Failure branches

- Backend ruled git-native but `gh` fails partway → fall back to the file backend for THIS
  record, say so, note the migration in the record (the shared sibling rule).
- The item is really a bug or feature in disguise → stop and point at the sibling command
  (Phase 2); never force-file it as a task to save a hop.
- Resume finds the record closed → report its state; reopening is the user's explicit call.
- A status verb on an unresolved id → report the failed resolution; nothing is created.
- Dedup finds it shipped or queued → report, stop or resume; never a duplicate record.

Done when a `task`-labeled record exists (an issue URL reported, or a lint-clean `kind: task`
TICKET on disk) carrying the full payload contract — or a resume acted on the existing record
(detail folded, Findings appended, or status advanced with its Findings-first close rule) — the
dedup sweep ran, and NO build was dispatched (/build's contract, where installed). NOT done
while a close leaves Findings empty, a duplicate was minted over a dedup hit, or a bug/feature
shape was filed here instead of routed.
