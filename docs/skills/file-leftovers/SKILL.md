---
name: file-leftovers
description: >-
  Sweep the current chat session for work mentioned but not advanced — bugs, feature
  ideas, feedback, chores, unanswered questions — and roll it up into workable tickets:
  one evidence-quoted candidate table, one batched clarification round, then each approved
  item minted through its owning intake skill. Use for "sweep this chat for leftover
  work", "ticket everything we didn't get to", "did we drop anything this session",
  "file the leftovers", "roll up what we mentioned but never did into tickets". NOT for
  decisions needing no ticket (find-open-questions); NOT for one known item
  (file-bug/file-feature/file-task); NOT for repo work-state (harness check-state).
disable-model-invocation: false
user-invocable: true
argument-hint: "[optional scope hint, e.g. 'only the bugs']"
---

# file-leftovers

Turns a session's dropped work into orchestratable tickets without inventing, duplicating,
or silently minting anything. The sweep runs in THIS context — a subagent or fork cannot
see the conversation, so the sweep is never dispatched. Scope hint: `$ARGUMENTS`.

## Phase 1 — Sweep the session

A candidate is anything a participant raised that names doable work and was left
unadvanced: a defect described, a capability wished for, feedback implying a change, a
chore deferred, a question asked and left unanswered. Three exclusions, applied per item with the
evidence for each:
- **Addressed** — the session already did it or decided it.
- **Already recorded** — an open record exists: one light search of whatever store
  doc-writing-rules' backend resolver rules for this repo (issues, `docs/tickets/`, or the
  adapter's search); the sibling's own dedup at mint time stays the authoritative gate.
- **Dropped on purpose** — the user said no, later, or out of scope.

An empty result is a real result: report "no leftovers — everything mentioned was
addressed, ticketed, or dropped" and stop.

## Phase 2 — The candidate table

The table leads the reply — findings before commentary, every row evidenced:

```
| # | Kind (bug/feature/task/question) | Item (≤10 words) | Evidence (verbatim quote, ≤15 words) | Disposition |
```

Dispositions: `ticket` (ready to mint) · `needs-input` (a slot only the user can fill) ·
`discard` (proposed drop, reason in the row). A row with no verbatim quote from the
session does not enter the table — no quote, no candidate.

## Phase 3 — One clarification round

All `needs-input` rows and any contested dispositions batch into ONE AskUserQuestion round
(multiple questions per round is fine; a second round only if the first's answers create
new gaps). Decision-shaped leftovers that need resolving but no ticket route to
`find-open-questions` — they are its territory, not rows here.

## Phase 4 — Mint on approval

Minting is authorized by ONE thing: the user approving the table's rows in this
conversation, after seeing them. The original ask — "ticket everything we didn't get to"
— authorizes the sweep, not the mint; it is the reason the table exists, not a
row-level approval. NEVER mint without a per-run table approval: no interactive channel
(headless, scheduled, unattended) → deliver the table as the report and stop — the table
IS the deliverable there, and minting waits for a session where the user can answer.

On approval (row edits applied, disagreements resolve in the user's favor): per approved
row, invoke the owning intake sibling via the Skill tool with
the row's evidence as seed: defects → `file-bug`, capability ideas → `file-feature`,
everything else (incl. answered-question follow-ups) → `file-task`. The siblings own
backend resolution, dedup, and the TICKET payload contract — minting goes through them;
a raw `gh issue create` or hand-written ticket file here is a defect. Question rows whose answer
arrived in Phase 3 mint only if the answer created work; otherwise they close in the
report as resolved.

## Report

Minted ids first (`#NN`/`tkt-####` + kind, one line each), then discards with one-line
reasons, then the not-minted remainder (resolved questions, find-open-questions
handoffs). The ids are the deliverable — ready for /build-feature, chore-planner, or
whatever orchestrates next.

## Failure branches

- The user discards everything → report the discards; an all-discard run is a success.
- A sibling mint fails partway → its own fallback discipline governs (file backend
  fallback, noted in its record); this skill reports the sibling's close-out verbatim
  rather than re-minting around it.
- `$ARGUMENTS` scopes the sweep ("only the bugs") → out-of-scope candidates still appear,
  collapsed to one summary row, so the user sees what the scope excluded.

Done when every table row carries a terminal disposition — a minted record id, a
find-open-questions handoff, a resolved-in-round note, or a reasoned discard — and the
report is delivered. NOT done while any approved row lacks its record id, or any question
was asked as scattered prose instead of the batched round.

## Example

Good (a candidate row):
`| 3 | bug | Login form drops session on refresh | "the login thing still logs me out randomly" | ticket |`

Counter-example — do not imitate:
`| 3 | bug | Various login issues discussed earlier | (mentioned at some point) | ticket |`
(no verbatim quote, vague item — unfalsifiable rows mint garbage tickets).
