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
context: fork
argument-hint: "[raw work item, or a #NN / TKT-#### / adapter-native id to resume]"
---

# issue — the generic work-item record, minted or resumed

Turns any work item into the smallest durable record that carries it — the sibling of
`file-bug` (defects) and `file-feature` (sized ideas) for everything those two fence out: chores,
follow-ups, research items, debts. One capture replaces the hand-rolled `gh issue create` whose
measured variance (missing labels, drifting section sets, no dedup, contractless closes) is this
skill's baseline evidence. Runs as a background fork (`context: fork`) by default: the fork sees
no conversation history — `$ARGUMENTS` is the only channel in. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0):** resolve once via doc-writing-rules' `references/backend-resolver.md`;
every phase below follows whichever option it returns.

## Phase 1 — Route: fresh item, or resume by id

`$ARGUMENTS` starts with a record id — `#NN`/a bare issue number (git-native, resolved via
`gh issue view`), `tkt-####` (file backend), or under Option C an id in the resolved adapter's own
native format (Linear: `TEAM-123`) resolving via that adapter's `read` operation
(`references/linear-adapter.md`, REQ-010) — → this is a RESUME; branch on what follows the id,
never re-mint. On the git-native backend, apply `doc-writing-rules`' Provenance-tagging
convention (`references/backend-resolver.md`) to the resolved record right here, before any
branch below — every branch that follows exits this phase, so the tag is applied at resolution
time, not deferred to a phase a given resume might never reach.

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
- **New detail** (any other trailing text, including an answer to a close-out's named
  clarifying question) → fold it into the body's matching section, clearing the answered gap
  from Scope/Open once folded (or append a dated `## Findings` comment when it is a result, not a
  scope change), and report the record. To avoid an answer colliding with the status-verb grammar
  above (a one-word `done`/`doing`/`wontfix` answer, or one starting `wontfix `, would otherwise
  read as a status verb), the resume format is `/file-task <id> answer: <text>` — a prefix the
  status grammar can never match (the terse close-out, gh#713, no longer echoes this string; it
  lives here and in Phase 4's own record-payload description).
- **Nothing after the id** → report the record's state, labels, and last Findings entry; stop.

A CLOSED record resumes only as a report — state it and stop; reopening is the user's call
(the siblings' shared rule). An id that does not resolve (no such file; `gh issue view` errors;
Option C's `read` returns not-found, AC-010) is a fresh item — say so, never proceed as if a
record existed. A bare number is an issue id on the git-native backend only; on the file backend
only `tkt-####` resolves; under Option C only the resolved adapter's own native format resolves.

## Phase 2 — Classify the shape (the routing gate)

On the FIRST classification only (the seed carries no `[redirected-from:X]` marker yet): a defect
("X is broken", a repro, a wrong output) → invoke `file-bug` directly via the Skill tool, carrying
the seed prefixed `[redirected-from:file-task]`; report which sibling was invoked and why, never
leave the user to type the command themselves. A feature idea (new capability, needs sizing or may
earn docs) → same move, invoke `file-feature`. Neither — the generic remainder — continues here.

**No live clarify round — the fork has no question channel.** When genuinely ambiguous, do not
attempt a clarifying question as a live `AskUserQuestion` call. **Measured 2026-08-17 (gh#541):**
a `context: fork` background dispatch has no question channel at all — `AskUserQuestion` is
unreachable from inside it (confirmed two ways: two independent thin captures, #1122 and #541's
own filing, both minted clarify-less; and a background dispatch cannot even discover the tool).
This is this skill's only invocation shape (`context: fork` is fixed above), so the round never
runs live, full stop. Capture here as `task` with the ambiguity named in Scope/Open instead
(persistence beats taxonomy), and the close-out (Phase 4) owes the question it couldn't ask live:
it reports the count (0 or 1) in its one-line terse form (gh#713) — the question's own text
already stands in Scope/Open, above, never restated in the close-out; the resume command —
`/file-task <id> answer: <text>` — folds the answer in once a person supplies it (Phase
1's "new detail" fold-in path). Skip naming a clarify question in the close-out when the seed
carries `[redirected-from:X]` (the round budget was already spent upstream) or `[unattended]` (no
live session to report back to at all) — the shared marker protocol below.

A seed carrying a `[redirected-from:X]` marker (naming a DIFFERENT sibling) → captured regardless
of fit: `task` with the mismatch named in Scope/Open, per this skill's own named fallback below.
This skill's own redirect (above) never fires on a seed that already carries the marker — one hop
only, detected from the seed itself, not from history the fork doesn't have.

**The one-hop-only redirect rule (shared by all three siblings):** a sibling reached by redirect
never redirects again — its own classification finding a poor fit is not license to bounce a
second time, only to capture under its own named fallback: **here** (`file-task`), `task` with the
ambiguity in Scope/Open; **`file-bug`**, `kind: bug` with the shape gap named in
Classification; **`file-feature`**, `kind: feature` with the gap named in Scope/Open. One hop resolves
genuine mis-routing; a second hop is thrash, not routing — the receiving skill always ends in a
captured record, never a second redirect.

**Redirect detection, now that all three siblings run forked (`context: fork`):** a forked
receiver carries no conversation history, so it cannot infer "reached by redirect" from context —
the redirecting skill says so in the seed itself. Every redirect invocation prefixes the seed
`[redirected-from:<the redirecting skill's name>]` before the verbatim seed; every genuinely
unattended caller (no live session to ever read a close-out — a scheduled/cron firing, an agent
dispatch with no channel back to a person at all) prefixes `[unattended]`. The two markers answer
different questions and never substitute for each other, restated in close-out terms (no sibling
ever runs a live clarifying round — see the resolved-assumption note below): `[redirected-from:X]`
means the one clarifying question was already named upstream, in the redirecting skill's own
close-out — skip naming it again here, capture regardless of fit; a person may still very well
read this skill's own close-out too (an inline `/file-task`→`/file-bug` redirect mid-conversation
has the same reader throughout, which is why the redirect skip was never really about
reader-absence). `[unattended]` means no reader backs the run at all, full stop — the one case
where naming a question in the close-out has nowhere to land. A seed carrying neither marker gets
the default: a reader is assumed for the close-out, and this skill's own Phase 2 names its one
question there, per the resolved assumption below — never as a live round.

**Assumption resolved (2026-08-09 flag, closed 2026-08-17 per gh#541):** the design used to rest
on an unverified assumption that `AskUserQuestion` reaches a live user from a `context: fork` run.
It doesn't — measured directly (Phase 2, above, carries the finding; not restated here). Every
sibling's Phase 2 assumes this as the default, not a risk to watch for: capture-with-gaps plus a
close-out that counts the unasked question(s) in its one-line terse form (gh#713) and the resume
command that folds an answer in later is the actual contract, not a fallback for a maybe-broken
channel.

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

The record exists before this skill stops; that ordering is the contract. **The close-out is the
terse one-line form (gh#713, uniform across all three intake siblings):** `Filed: <id> ·
kind:task · owed-questions:<N>` — `<id>` is whichever the backend resolved (issue URL, ticket
path, or adapter-native id), `<N>` counts whatever Phase 2 named as an unasked clarifying question
(0 or 1); the question's own full text stays where Phase 2 already wrote it, in Scope/Open, never
restated here. This one line is the head line and the whole close-out in the normal case;
exception notes this skill names elsewhere (a skipped Issue Type, a backend-create fallback)
append as extra lines only when they occur.

`.github/ISSUE_TEMPLATE/task.yml` mirrors this contract for a human filing directly on GitHub —
this template, plus its `bug`/`feature` siblings, IS the feedback intake door idr-0008 names; no
separate door exists or is owed. On Option B, apply `doc-writing-rules`' Provenance-tagging
convention (`references/backend-resolver.md`) at this record's creation — Phase 1 above applies
the same convention on resume.

## Failure branches

The redirect to `file-bug`/`file-feature` and its one-hop rule (Phase 2) are the canonical
statement the sibling skills point back to — nothing to add here.

Every other branch — an unresolved id, a status verb against it, and a closed-record resume
(Phase 1); a shipped/queued dedup hit (Phase 3); `doc_lint.py` and backend-fallback failures
(Phase 4, and doc-writing-rules' backend-resolver.md for the fallback shape) — is handled inline
at its own phase; not restated here.

Done when a `task`-labeled record exists (an issue URL reported, a lint-clean `kind: task`
TICKET on disk, or an Option-C adapter's record with its native id reported) carrying the full
payload contract — or a resume acted on the existing record
(detail folded, Findings appended, or status advanced with its Findings-first close rule) — the
dedup sweep ran, and NO build was dispatched (/build-feature's contract, where installed) — OR the seed
was redirected to `file-bug`/`file-feature` under the one-hop rule and the sibling invocation was
reported; no task record is owed on a redirected seed. NOT done while a close leaves Findings
empty, a duplicate was minted over a dedup hit, or a bug/feature shape was filed here instead of
routed.
