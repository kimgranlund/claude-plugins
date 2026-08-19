---
name: build-feature
description: >-
  Builds a feature from its durable record, running the /file-feature intake first when none
  exists, then building. /file-feature records and stops; /build-feature guarantees a record
  exists, sizes the dispatch (solo-first), and drives it under a mandatory Findings write-back
  contract. Run /build-feature [what to build, or a TKT- id]. NOT for pure intake with no build
  intended (/file-feature); NOT for bug investigation (file-bug); NOT for finding and
  batch-confirming which open tickets to build in the first place (mobilize-chores); NOT for
  converting this session into the standing build seat (/bind-build) — this command forks ONE
  already-known target off the session.
disable-model-invocation: true
user-invocable: true
context: fork
argument-hint: "[what to build, or an existing TKT- id]"
---

# build — no record, no build; a record, then momentum

The dispatch half of the `/file-feature` pair. `/file-feature` ends at a record; `/build-feature` starts from one —
minting it first when it doesn't exist — and ends at shipped work with the record's `## Findings`
carrying the evidence. Runs as a background fork (`context: fork`) by default: the whole
find-or-make/size/dispatch/close-loop chain below executes off the caller's session; only the
final ticket status and what shipped reach the caller. The fork has no question channel:
**measured 2026-08-17 (gh#541)**, a `context: fork` background dispatch cannot reach
`AskUserQuestion` at all — confirmed two ways (two independent thin captures minted clarify-less,
and a background dispatch that could not even discover the tool) — and `dispatch-ticket` running
inline in it inherits the same silence (its own no-live-channel failure branch names this fork
explicitly). So clarify BEFORE forking, or fold answers in afterward by re-running
`/build-feature <id> <answers>` against the record; a gap discovered mid-fork is named in the
record and the close-out, never asked live. Corrected assumption (2026-08-09 text, falsified
2026-08-17 per gh#541, kept here as the dated record of the mistake): the prior claim — "forking
does not remove the human; a clarifying question raised in this fork's own turn still reaches
the live user directly via `AskUserQuestion`" — is wrong. Do not restate it as canon. Seed:
$ARGUMENTS.

Empty `$ARGUMENTS` is a precondition failure, not an assumption to fill from conversation history
the fork no longer carries — and there is no question channel to ask through (gh#541, above). Do
not invoke `dispatch-ticket` at all: proceed capture-with-gaps style — close out naming the
unasked question (what should be built?) and the resume command, `/build-feature <what to build,
or a TKT-/#issue id>`, as this fork's report — the same named-blocker degrade `dispatch-ticket`'s
own no-live-channel branches apply. Never guess a target from history the fork does not have.

This command is the human-typed entry point only. The actual find-record/size/dispatch/close-loop
procedure lives in `dispatch-ticket` (this plugin) — a `disable-model-invocation: true` skill like
this one can't be Skill-tool-invoked or preloaded by anything else (issue #134/#135's shared
defect class), so `dispatch-ticket` carries the procedure and `build-leader` (agent) reaches the
identical logic for a programmatic caller (`mobilize-chores`). Given a non-empty seed resolving to a real ticket id, run `teamwork/scripts/dispatch_envelope.py
<id>` first and fold its JSON into the seed handed to `dispatch-ticket` — `dispatch-ticket`
Phase 3's own "envelope present" branch verifies it by one re-read instead of re-deriving the
slot, branch, and scratch clone (#758). Invoke
`dispatch-ticket` (Skill tool) carrying `$ARGUMENTS` verbatim, and relay its result as this command's own
output — this IS running the procedure, mechanically, not a restatement of it. `dispatch-ticket`
itself stays un-forked (its own frontmatter carries no `context: fork`): invoked from here it runs
inline inside this command's own fork (no double hop); invoked from `build-leader` it runs inline
inside that agent's already-isolated context (no live user there, so forking again would only add
a needless third hop with nothing to buy); invoked from a `/bind-build` session it runs inline in
that session's own turn (a live user IS present and inline is exactly what keeps the engine's
interactive branches on that user's channel — a fork would push them off it).

**A build you started here can come back already merged — plainly stated so it is never a
surprise.** Normally this command ends at an open PR you merge yourself. But when the dispatch
that ran it carried the explicit `auto-merge: authorized` grant line AND the change cleared every
one of ADR-0012's quick-build conjuncts (a `size:small` record, one plugin, one substantive file
from a short allow-list — a SKILL.md body edit, a reference page, or a script — plus a green
critic, a green local gate, green CI, and no overlapping open PR), the seat merges it and reports
back the PR link with a merge SHA. Nothing was skipped to get there: the PR opened, the critic
ran, the gates ran. Only your "merge" reply was pre-authorized. You never granted it implicitly —
the line is set deliberately by whoever dispatched, or the whole stage never runs — and anything
that misses even one conjunct comes back the old way, an open PR waiting on you.

`dispatch-ticket`'s own body is the authoritative phase-by-phase contract (find-or-make record,
kind branch, size solo-first, dispatch under contract, close the loop) and its own failure
branches — not duplicated here, so the two entry points can never drift apart. Since ADR-0010
that engine branches by kind: handed a task-kind id, this command runs the clarify-then-dispatch
path; handed a bug-kind id, it hands over to `file-bug` and reports the read-back — the
feature-flavored name marks this command's charter, not the engine's limit.
