---
name: build-feature
description: >-
  Builds a feature from its durable record, running the /file-feature intake first when none
  exists, then building. /file-feature records and stops; /build-feature guarantees a record
  exists, sizes the dispatch (solo-first), and drives it under a mandatory Findings write-back
  contract. Run /build-feature [what to build, or a TKT- id]. NOT for pure intake with no build
  intended (/file-feature); NOT for bug investigation (file-bug); NOT for finding and
  batch-confirming which open tickets to build in the first place (mobilize-chores); NOT for
  converting this session into the standing build seat (/lead-build) — this command forks ONE
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
final ticket status and what shipped reach the caller. Forking does not remove the human — a
clarifying question raised in this fork's own turn (including `dispatch-ticket` running inline
in it) still reaches the live user directly via `AskUserQuestion`, per `dispatch-ticket`'s own
Phase 1 test. Seed: $ARGUMENTS.

Empty `$ARGUMENTS` is a precondition failure, not an assumption to fill from conversation history
the fork no longer carries: ask via `AskUserQuestion` what to build before invoking
`dispatch-ticket` at all.

This command is the human-typed entry point only. The actual find-record/size/dispatch/close-loop
procedure lives in `dispatch-ticket` (this plugin) — a `disable-model-invocation: true` skill like
this one can't be Skill-tool-invoked or preloaded by anything else (issue #134/#135's shared
defect class), so `dispatch-ticket` carries the procedure and `build-lead` (agent) reaches the
identical logic for a programmatic caller (`mobilize-chores`). Invoke `dispatch-ticket` (Skill
tool) carrying `$ARGUMENTS` verbatim as its own seed, and relay its result as this command's own
output — this IS running the procedure, mechanically, not a restatement of it. `dispatch-ticket`
itself stays un-forked (its own frontmatter carries no `context: fork`): invoked from here it runs
inline inside this command's own fork (no double hop); invoked from `build-lead` it runs inline
inside that agent's already-isolated context (no live user there, so forking again would only add
a needless third hop with nothing to buy); invoked from a `/lead-build` session it runs inline in
that session's own turn (a live user IS present and inline is exactly what keeps the engine's
interactive branches on that user's channel — a fork would push them off it).

`dispatch-ticket`'s own body is the authoritative phase-by-phase contract (find-or-make record,
kind branch, size solo-first, dispatch under contract, close the loop) and its own failure
branches — not duplicated here, so the two entry points can never drift apart. Since ADR-0010
that engine branches by kind: handed a task-kind id, this command runs the clarify-then-dispatch
path; handed a bug-kind id, it hands over to `file-bug` and reports the read-back — the
feature-flavored name marks this command's charter, not the engine's limit.
