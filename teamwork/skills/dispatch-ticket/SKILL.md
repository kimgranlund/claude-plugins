---
name: dispatch-feature
description: >-
  Use when invoked by name from /build-feature's own body or the feature-lead agent — never from
  a direct user ask. Given one already-known feature-ticket id, finds or mints its record, sizes
  the build solo-first, drives it under a mandatory Findings write-back contract, closes the
  loop. Exists so both callers share one procedure instead of duplicating it. NOT a trigger for a
  raw "build this feature" ask (/build-feature or /file-feature own that); NOT for finding or
  batch-confirming which tickets to build (mobilize-chores).
disable-model-invocation: false
user-invocable: false
---

# dispatch-feature

The procedure behind `/build-feature`, factored out so it has two reachable entry points instead
of one. `/build-feature` itself is `disable-model-invocation: true` — command-only, unreachable
via the Skill tool or agent preload (issue #134/#135's shared defect class: a flag meant to keep a
command human-typed also blocks every programmatic path to the same logic). This skill carries
the actual procedure; `/build-feature`'s body and the `feature-lead` agent both invoke it rather
than each carrying their own copy. This skill deliberately carries no `context: fork` of its
own — rationale in `/build-feature`'s body (no double hop from that caller, no needless third hop
from `feature-lead`). Seed: $ARGUMENTS.

## Phase 1 — Find or make the record

- `$ARGUMENTS` is a resolvable `TKT-####` → that's the record — branch on its STATE first:
  `done`/`wontfix` → report the closed state and stop (reopening is the user's call);
  `kind: bug` → this is file-bug's work, hand it over via the Skill tool, seed prefixed
  `[redirected-from:dispatch-feature]` (file-bug's own marker protocol — the round budget was
  already spent here, and file-bug's forked run has no other way to know); otherwise read
  Size/Scope/Links and continue.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names — records (`docs/tickets/`,
  ROADMAP/PLAN), the codebase, and existing docs/corpora: a queued match → build from it; an already-shipped match → report where
  it lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — its opt-in
  project-docs index offer rides along; apply its phases inline where not: extract → dedup →
  size/shape → lint-clean `kind: feature` ticket, no index offer without docs' template), invoked
  via the Skill tool with the seed prefixed `[nested-intake]` — file-feature's own Phase 6 gates
  its index-bootstrap offer off this marker, since a nested intake already owes this phase's own
  ambiguity question and file-feature's Phase 2 round; a third `AskUserQuestion` from one
  background run is one too many. The record exists on disk before any build effort is spent —
  ticket-first is the entire loss-window fix, and it does not move.

A record whose Shape is knowledge (routed to reference/corpus work at intake) is not built
here — report that routing and stop; docs' seats own it.

## Phase 2 — Size the dispatch (solo-first)

The record's Size class picks the machinery — the same materiality floors the seats themselves
carry, applied from the caller's side:

- **small** — the host builds it inline, or one sealed fork/agent when isolation or tooling
  demands it — an agent only for tool restriction, parallelism, or multi-skill preload; a fork
  for everything else (harness's fork-vs-agent gate, applied inline where harness is absent). No planner, no
  coordinator, no team: a task one context can hold is the host's own.
- **big** — the delivery seats, each already floored: `planner` authors what the change
  earns (the record's Links may already carry the docs — don't re-author), `builder`
  implements to the approved LLD, `code-checker` grades the slice before merge. The coordinator
  seat only when the chain genuinely spans ≥2 seats across contexts. On a `/build-feature`-initiated
  call this makes host→fork→coordinator→seats, a third level past team-or-solo-rules' default
  depth ≤ 2 — named justification, not an accident: the fork isolates the CALLER's session
  (`context: fork` on `/build-feature`), the coordinator isolates the multi-seat delivery chain
  (planner/builder/code-checker each need their own turn) — two different things being kept
  separate, not one dispatch nested inside another for no reason.

## Phase 3 — Dispatch under contract

Every dispatch is sealed: the ticket path + enumerated inputs + budget + the typed return — and a
**mandatory dated `## Findings` write-back at each significant result** (slice built, gate green,
merged), not only at the end, so an interrupted build still left evidence. Run under `/goal` with a
try-cap (5, per loop-rules's feature-ticket recipe): named stopping predicate, capped tries,
escalate on the same failure twice.

## Phase 4 — Close the loop

Read the ticket back. Findings gained entries and the work shipped → advance status
(`open`→`doing`→`done`) and report path + status + what shipped. An agent that returned without
its Findings entry → one re-dispatch with the contract quoted, then record the loss with a dated
entry and say so plainly; a fork no longer addressable skips straight to recording — it cannot
be re-dispatched into. A conversational summary never substitutes for the entry the record
was owed.

## Failure branches

- Ambiguous match in Phase 1 (two plausible records) → **with an interactive user present**, ask
  which, one question, then proceed. A `/build-feature`-initiated call counts as having an
  interactive user present even though it runs inside that command's fork (`context: fork`) —
  forking relieves the caller's session, it does not remove the person, and `AskUserQuestion`
  still reaches them directly. **Dispatched with no interactive user** (e.g. via `feature-lead`,
  from `mobilize-chores`) → report the ambiguity as a named blocker instead of asking — the batch
  confirm already spent the user's one gate for this run, so raising a second, mid-dispatch
  question has nowhere sanctioned to land regardless of what the channel can technically reach —
  same discipline as this plugin's other unattended failure branches (`close-session`,
  `mobilize-chores`); never guess which record was meant.
- The ask is bug-shaped → `file-bug` (docs), not a feature build.
- Build blocked mid-flight by a discovered design fork → escalate to the record (a dated Findings
  entry naming the fork) and, for big work, back to planner — never silently edit the
  contract.
- Gates fail at the wave boundary → the failure routes to the seat that caused it; the ticket
  stays `doing` with the failure recorded.

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker), status reflects reality, and no build effort was spent before the record existed.
