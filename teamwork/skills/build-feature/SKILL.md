---
name: build
description: >-
  Builds a feature from its durable record, running the /file-feature intake first when none
  exists, then building. /file-feature records and stops; /build-feature guarantees a record
  exists, sizes the dispatch (solo-first), and drives it under a mandatory Findings write-back
  contract. Run /build-feature [what to build, or a TKT- id]. NOT for pure intake with no build
  intended (/file-feature); NOT for bug investigation (file-bug).
disable-model-invocation: true
user-invocable: true
argument-hint: "[what to build, or an existing TKT- id]"
---

# build — no record, no build; a record, then momentum

The dispatch half of the `/file-feature` pair. `/file-feature` ends at a record; `/build-feature` starts from one —
minting it first when it doesn't exist — and ends at shipped work with the record's `## Findings`
carrying the evidence. Seed: `$ARGUMENTS`.

## Phase 1 — Find or make the record

- `$ARGUMENTS` is a resolvable `TKT-####` → that's the record — branch on its STATE first:
  `done`/`wontfix` → report the closed state and stop (reopening is the user's call);
  `kind: bug` → this is file-bug's work, hand it over; otherwise read Size/Scope/Links and
  continue.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names — records (`docs/tickets/`,
  ROADMAP/PLAN), the codebase, and existing docs/corpora: a queued match → build from it; an already-shipped match → report where
  it lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — its opt-in
  project-docs index offer rides along; apply its phases inline where not: extract → dedup →
  size/shape → lint-clean `kind: feature` ticket, no index offer without docs' template). The record
  exists on disk before any build effort is spent — ticket-first is the entire loss-window fix,
  and it does not move.

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
  seat only when the chain genuinely spans ≥2 seats across contexts.

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

- Ambiguous match in Phase 1 (two plausible records) → ask which, one question, then proceed.
- The ask is bug-shaped → `file-bug` (docs), not a feature build.
- Build blocked mid-flight by a discovered design fork → escalate to the record (a dated Findings
  entry naming the fork) and, for big work, back to planner — never silently edit the
  contract.
- Gates fail at the wave boundary → the failure routes to the seat that caused it; the ticket
  stays `doing` with the failure recorded.

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker), status reflects reality, and no build effort was spent before the record existed.
