---
name: sub-agent
description: >-
  Dispatches unattended via the Agent tool. First token exact-matches a registered agent name →
  that agent's own contract, one completion. No match → the whole $ARGUMENTS is a free-
  instruction charter, spawned as a NAMED continuable clean-context session — addressable by
  name (`SendMessage`, or ask the marshal to relay), result arrives as a notification, resumable
  with follow-ups; say "one-shot"/"quick" for a synchronous single-answer dispatch instead. Run
  /sub-agent {agent-name-or-instructions}. NOT the forked form (`/fork-agent {name}` — background
  fork, registered agents only); NOT the host-adopts-contract form (`/bind-{seat}`); NOT a
  per-seat alias — mints none of its own.
disable-model-invocation: true
user-invocable: true
argument-hint: "{agent-name-or-instructions} [task/charter]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# sub-agent — the `sub-` mechanic, named/parameterized, plus free-instruction dispatch

ADR-0020 D3's third command head: `sub-` names a real, unattended `Agent`-tool dispatch — a
genuinely separate context, not this session and not a fork of it. Every seat in the estate that
already has a standing dispatched twin (`build-leader`, `planning-leader`, `review-leader`,
`product-leader`, `fleet-marshal`, and the rest) was already reachable via the `Agent` tool by
name; this command is the generic, parameterized front door to that same mechanic. Per D4, no
per-seat alias is minted here — `/sub-agent {name-or-instructions}` is the whole surface.

**2026-08-19 amendment (Kim's live ruling).** This skill absorbs the free-instruction dispatch
originally shipped as a separate sibling, `sub-task` (#745/#746, retired same-day, zero adoption)
— `sub-agent` is now dual-mode rather than registered-agent-only. This slightly amends ADR-0020
D3's `sub-` head semantics (D4's no-per-seat-alias rule is untouched); recorded here rather than
in a fresh ADR supersession per Kim's own instruction — escalate to a real supersession only if a
reviewer judges this contract-changing enough to owe one.

## Phase 1 — Resolve the target: registered agent, or free instructions

`$ARGUMENTS`' first token is checked against a registered agent name first.

- **Exact match** (case-sensitive, no fuzzy resolution) against one of the three real agent homes
  — every installed plugin's cache (`~/.claude/plugins/cache/*/*/*/agents/<name>.md`), the current
  project's own `.claude/agents/<name>.md`, and the user's own `~/.claude/agents/<name>.md` — →
  today's registered-agent behavior: everything after the first token is that agent's task/charter.
  Continue at Phase 2a.
- **No exact match** → the WHOLE of `$ARGUMENTS` (not just the tail) is a free-instruction charter
  — no registered agent to name, arbitrary instructions instead. Continue at Phase 2b.
- **Typo guard** (the original hazard that argued against overloading `sub-agent`, now mitigated
  explicitly): before falling through to Phase 2b, check whether the unresolved first token is a
  single kebab-shaped word within edit distance ~2 of a registered agent name found across the
  three homes above. If so, ask ONE confirm via `AskUserQuestion` — "no agent named `<token>` —
  free instructions instead, or did you mean `<candidate>`?" — before doing anything else; never
  silently dispatch either path on a plausible typo. No close candidate → proceed straight to
  Phase 2b, no question asked.

### Phase 2a — Seal and dispatch a registered agent (unchanged)

Invoke the `Agent` tool against the resolved agent, carrying the task/charter as its prompt —
sealed the way any dispatch is: the task stated once, enough context that the agent doesn't have
to guess scope, and nothing this session should have done itself instead. This command's own job
ends at the seal; it does not narrate the dispatched agent's internal turns.

### Phase 2b — Seal and dispatch a free-instruction session (absorbed from `sub-task`)

Seal the whole `$ARGUMENTS` as a self-contained charter — no conversation history, no implicit
"this"/"the above". An unresolved deictic reference gets one inline clarifying question before
dispatch, never a guess; empty `$ARGUMENTS` (once the typo-guard above has already ruled out a
near-miss agent name) → ask what the subtask is, never invent one.

**Default: named and continuable.** One `Agent`-tool call, `subagent_type: general-purpose`,
NAMED — a short kebab slug auto-derived from the charter (e.g. a charter about auditing color
tokens → `subagent-color-audit`), unique via a short random suffix when a collision is plausible
(e.g. `subagent-color-audit-a4f2`) — never `ListAgents` for this: `team-scaffolding`'s own shipped
ruling reserves `ListAgents` for confirming liveness of an already-known name, never for finding
or probing one, and a per-dispatch collision check reads too close to that discouraged "find" use
to risk; the random-suffix path is the resolution, not a fallback. Pin `model: sonnet` per the
ad-hoc-dispatch doctrine (`agent-writing-rules` §Model tiering), unless the charter's own judgment
load plainly earns more — state whichever was chosen.

This naming is the CANON-SANCTIONED deliberate-continuation case, not the fan-out class gh#154/
gh#157 ban: it names a single seat the user explicitly means to resume, never a fanned-out worker
with nowhere to address a report back to — `fleet-rules`' own A3-R1 ("named ONLY when
continuation is needed; never on a fan-out") is exactly this case, distinct from the never-name
rule's own target (`agent-writing-rules`' negative-patterns table row, "Coordinator names a
fanned-out seat it doesn't need to resume").

State the mailbox semantics in the reply, every time: the seat is addressable going forward by
its name (`SendMessage`, or ask the marshal to relay in a fleet context); its actual result
arrives later as a completion notification, not this call's own return; it is continuable with
follow-ups. Carry the A3 caveat too (`fleet-rules`' A3-R4, `agent-writing-rules`' teammate-mode
delivery clause): the seat's own plain-text final does NOT auto-deliver — only its completion
notification, or an explicit `SendMessage`, actually carries a result back.

**One-shot exception.** The charter carrying the literal word "one-shot" or "quick" (or an
equivalent explicit ask for a single synchronous answer, nothing to resume) takes the prior path
instead: UNNAMED, synchronous — this call's own return is the answer, never mailbox-routed,
exactly as the original `sub-task` shipped (#745).

## Phase 3 — Relay the return

- **Registered-agent path (2a).** The `Agent` tool's own completion is the caller's answer — relay
  it, don't re-summarize it away or add unearned framing. Where the dispatched agent is a NAMED
  teammate (long-lived, addressable), its report may instead arrive via `SendMessage`; state which
  delivery path this dispatch used so the caller knows whether to expect a synchronous return or a
  later message.
- **Free-instruction path, default (named).** Relay the dispatch confirmation: the seat's name, a
  one-line charter summary, and the mailbox semantics stated above. There is no synchronous answer
  yet — it arrives later, as that seat's own completion notification or an explicit `SendMessage`
  once addressed.
- **Free-instruction path, one-shot.** Relay the result verbatim-in-substance, findings-first — no
  re-summarizing away the answer, no unearned framing on top of it.

## Failure branches

- **No agent name resolves, and no plausible typo-guard candidate** → falls through to Phase 2b
  (free instructions); this is not a failure, it's the dual-mode design.
- **The name matches more than one installed plugin's `agents/`** → report the collision; never
  guess.
- **Registered-agent path: `$ARGUMENTS` carries no task after the agent name** → report that a
  task/charter is required; never invent one to fill the gap.
- **Free-instruction path: dispatch dies** (no return, an error) → report it, then one re-dispatch
  of the same sealed charter, max — never a silent retry loop.
- **Free-instruction path, one-shot: the result contradicts a stated constraint** (scope, format, a
  stated non-goal) → report the gap plainly; never silently accept a result that misses its own
  brief.
- **This session itself is a nested dispatch and holds no `Agent` tool of its own** → this command
  cannot run at all; report the capability gap plainly rather than attempting a dispatch, and name
  the resume path (return to a session that does hold the tool).
- **This session itself is a nested dispatch AND holds the `Agent` tool, registered-agent path or
  free-instruction one-shot** → the no-nested-wait rule: do not dispatch and then end this turn
  waiting on a background callback — the `Agent` tool's own return is synchronous from this call's
  perspective; act on it directly.
- **This session itself is a nested dispatch AND holds the `Agent` tool, free-instruction default
  (named) path** → the named seat's completion notification routes to the ROOT session, never back
  to this nested seat (`dispatch-ticket`'s own no-nested-wait preamble, verified A4, 2026-08-10) —
  state this plainly in the reply rather than promising a callback this seat structurally cannot
  collect on; whoever holds the root session is who actually sees that seat report in, not this
  dispatcher.

## Done

Done when Phase 1 resolved cleanly (a registered agent, a confirmed typo-guard redirect, or a
free-instruction fallthrough with no plausible near-miss); the matching Phase 2 dispatch sealed
once; and Phase 3's matching relay ran — a synchronous return relayed verbatim (registered-agent
or one-shot), or the named seat's mailbox semantics stated in full (free-instruction default). NOT
done while a dispatch sits unrelayed, a collision or typo-guard candidate was silently resolved by
guessing, or this session narrates a sub-agent's own internal work instead of its return.
