---
name: dispatch-ticket
description: >-
  Use when invoked by name from /build-feature's own body or the build-lead agent — never from a
  direct user ask. Given one already-known ticket id of any kind, finds or mints its record, then
  branches by kind: feature → size solo-first and build under a mandatory Findings write-back
  contract; task → clarify with one find-intent round, then dispatch under the same contract;
  bug → hand to file-bug with the redirect marker. One shared procedure for all callers
  (ADR-0010, generalized from dispatch-feature). NOT a trigger for a
  raw "build this" ask (/build-feature or /file-feature own that); NOT for finding or
  batch-confirming which tickets to build (mobilize-chores).
disable-model-invocation: false
user-invocable: false
---

# dispatch-ticket

The procedure behind `/build-feature` and the `build-lead` agent, factored out so it has two
reachable entry points instead of one. `/build-feature` itself is `disable-model-invocation:
true` — command-only, unreachable via the Skill tool or agent preload (issue #134/#135's shared
defect class: a flag meant to keep a command human-typed also blocks every programmatic path to
the same logic). This skill carries the actual procedure; `/build-feature`'s body and the
`build-lead` agent both invoke it rather than each carrying their own copy. Generalized from
`dispatch-feature` per ADR-0010: one confirmed ticket of ANY kind — feature, task, or bug — the
kind branch below picks the path. This skill deliberately carries no `context: fork` of its own —
rationale in `/build-feature`'s body (no double hop from that caller, no needless third hop from
`build-lead`). Seed: $ARGUMENTS.

## Phase 1 — Find or make the record

- `$ARGUMENTS` is a resolvable ticket id (`TKT-####`, a bare issue number on the git-native
  backend, or an adapter-native id) → that's the record — branch on its STATE first:
  `done`/`wontfix`/closed → report the closed state and stop (reopening is the user's call);
  otherwise read its kind, Size/Scope/Links, and continue to Phase 2.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names — records (`docs/tickets/`,
  ROADMAP/PLAN, or the resolved backend's open issues), the codebase, and existing docs/corpora:
  a queued match → build from it; a match that already shipped → report where it lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — its opt-in
  project-docs index offer rides along; apply its phases inline where not: extract → dedup →
  size/shape → lint-clean `kind: feature` ticket, no index offer without docs' template), invoked
  via the Skill tool with the seed prefixed `[nested-intake]` — file-feature's own Phase 6 gates
  its index-bootstrap offer off this marker, since a nested intake already owes this skill's own
  ambiguity question and file-feature's Phase 2 round; a third `AskUserQuestion` from one
  background run is one too many. A raw seed reaching this skill is feature-shaped by its
  callers' own contracts; the intake's own classification still redirects a disguised bug or
  chore per its rules. The record exists on disk before any build effort is spent — ticket-first
  is the entire loss-window fix, and it does not move.

A record whose Shape is knowledge (routed to reference/corpus work at intake) is not built
here — report that routing and stop; docs' seats own it.

## Phase 2 — Branch by kind

- **`kind: bug`** → this is `file-bug`'s work: invoke it via the Skill tool carrying the ticket
  id, seed prefixed `[redirected-from:dispatch-ticket]` (file-bug's own marker protocol — the
  round budget was already spent here, and file-bug's forked run has no other way to know).
  The RECORD is the return channel, not the fork's transcript: `file-bug` runs `context: fork`,
  and whether a fork invoked from inside an agent dispatch returns synchronously is an
  unverified platform assumption (the same flagged class as file-task Phase 2's) — so after the
  hand-off, read the ticket back (Phase 5's verbs) and report "handed to `file-bug`; read-back
  shows <state/Findings>". A conversational result that did arrive is a bonus to relay, never
  the thing waited on. Phases 3–5 never run for a bug.
- **`kind: task`** → **clarify, then dispatch — never blind.** Tasks carry no fixed execution
  verb the way features do (`file-task`'s own scope is deliberately heterogeneous: chores,
  follow-ups, research items, debts), so run `find-intent` (harness, where installed; its
  discipline inline otherwise) on the ticket's full body first — ONE batched clarifying round
  maximum, and only when something is genuinely ambiguous AND an interactive user is present
  (the same interactive-user test the Phase 1 ambiguous-match failure branch applies; a
  `build-lead` dispatch has no one to ask — a ticket that's already clear proceeds with zero
  rounds either way). Still not concretely actionable (no clear "what would done look like") →
  report SKIPPED with the named gap, never dispatch on an unclear brief. Otherwise dispatch via
  the `Agent` tool — `subagent_type: general-purpose` as the default (`team-or-solo-rules`'
  solo-first/null-unit reasoning: a generic task needs no tool restriction, parallelism, or
  multi-skill preload); a specific named agent only when the clarified brief genuinely needs one
  of those three properties. The dispatch prompt is sealed per Phase 4's contract — the
  CLARIFIED BRIEF (the round's answers travel in the seal; the dispatched agent cannot see the
  clarify conversation), the record, the write-back verb per the resolved backend, a dated
  Findings-equivalent entry at each significant result. A task is ONE sealed dispatch — Phase
  4's `/goal` try-cap wrapper is the feature path's, not inherited here (matching the absorbed
  original). Then close the loop per Phase 5, including its status verbs (`doing`/`done`+close/
  `wontfix`+close, per the backend) and its one-re-dispatch rule.
- **`kind: feature`**, a record minted fresh in Phase 1, and the default arm — a pre-existing
  record carrying no kind, or an unrecognized one → continue: Phases 3–5 (the pre-ADR-0010
  behavior: anything neither bug- nor task-kinded nor closed takes the feature path — `/build-feature`
  can be handed any id, and an unlabeled issue builds rather than falls through undefined).

## Phase 3 — Size the dispatch (solo-first, feature path)

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
  separate, not one dispatch nested inside another for no reason. The same justification holds
  on a `build-lead` dispatch — the agent context takes the fork's place as the layer isolating
  the caller; host→agent→coordinator→seats is the identical shape.

## Phase 4 — Dispatch under contract

Every dispatch is sealed: the ticket path + enumerated inputs + budget + the typed return — and a
**mandatory dated `## Findings` write-back at each significant result** (slice built, gate green,
merged), not only at the end, so an interrupted build still left evidence. The write-back verb
follows the resolved backend: git-native — the issue number, `gh issue comment`; file backend —
the TICKET file's path, editing its `## Findings` section; an external adapter — its `update`
operation. Run under `/goal` with a try-cap (5, per loop-rules's feature-ticket recipe): named
stopping predicate, capped tries, escalate on the same failure twice.

## Phase 5 — Close the loop

Read the ticket back (git-native: `gh issue view --comments`; file backend: re-read the file; an
adapter: its `read` operation). Findings gained entries and the work shipped → advance status
(`open`→`doing`→`done`; git-native `done` closes the issue, `wontfix` closes with the label and a
reason comment — matching `file-bug`'s own Phase 6 status verbs) and report path + status + what
shipped. An agent that returned without its Findings entry → one re-dispatch with the contract
quoted, then record the loss with a dated entry and say so plainly; a fork no longer addressable
skips straight to recording — it cannot be re-dispatched into. A conversational summary never
substitutes for the entry the record was owed.

## Failure branches

- Ambiguous match in Phase 1 (two plausible records) → **with an interactive user present**, ask
  which, one question, then proceed. A `/build-feature`-initiated call counts as having an
  interactive user present even though it runs inside that command's fork (`context: fork`) —
  forking relieves the caller's session, it does not remove the person, and `AskUserQuestion`
  still reaches them directly. **Dispatched with no interactive user** (e.g. via `build-lead`,
  from `mobilize-chores`) → report the ambiguity as a named blocker instead of asking — the batch
  confirm already spent the user's one gate for this run, so raising a second, mid-dispatch
  question has nowhere sanctioned to land regardless of what the channel can technically reach —
  same discipline as this plugin's other unattended failure branches (`close-session`,
  `mobilize-chores`); never guess which record was meant.
- A raw (recordless) seed that is bug-shaped → `file-bug` (docs) owns it from intake, not a
  build; the Phase 2 bug branch covers a ticket that already exists.
- A task's clarify round exhausts without a clear brief → SKIPPED with the named gap (Phase 2);
  a skipped task is a reported outcome, not a failure.
- Build blocked mid-flight by a discovered design fork → escalate to the record (a dated Findings
  entry naming the fork) and, for big work, back to planner — never silently edit the
  contract.
- Gates fail at the wave boundary → the failure routes to the seat that caused it; the ticket
  stays `doing` with the failure recorded.

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker/skip), status reflects reality, and no build effort was spent before the record existed —
or the bug branch handed over and `file-bug`'s own result was relayed.
