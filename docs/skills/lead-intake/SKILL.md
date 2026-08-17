---
name: lead-intake
description: >-
  Makes this session a dedicated intake seat: it adopts the intake-leader agent's own contract
  directly — every raw report, idea, or chore sent here becomes a durable record via the
  file-bug/file-feature/file-task/file-leftovers procedures, applied inline with a live
  clarifying round — and holds that discipline until the session ends. Run /lead-intake
  [optional repo root]. NOT the dispatched sibling seat (intake-leader, Agent tool); NOT a
  one-off filing (/file-bug, /file-feature, /file-task directly); NOT a coordination charter
  (/lead-team, teamwork).
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional target repo root — defaults to the current working directory]"
---

# lead-intake — the host runs the intake seat, not a dispatched copy of it

`intake-leader` (this plugin, `agents/intake-leader.md`) is the dispatched form of the standing
intake seat. This command is the other half of the pair — the `/lead-team` ↔ `team-lead`
pattern: it makes **this session** — the one the human is typing into — hold that agent's own
contract directly, for the session's duration, with no Agent spawn. The human talks straight to
the seat; that is the point, and it is what the agent structurally cannot offer. Under ADR-0006
the pair splits by species: command = verb form (`/lead-intake`), agent = role noun
(`intake-leader`). Seed: `$ARGUMENTS` (a target repo root; blank = the current working directory).

## Phase 1 — Bind the target

Resolve the repo root (`$ARGUMENTS`, else cwd) and state it back in one line. Every record this
session mints lands against that repo's resolved backend.

## Phase 2 — Adopt the contract as the session's own standing discipline

From this point until the session ends, this session holds the intake seat's contract as its own
operating rules — read, don't re-derive:

1. **Read `${CLAUDE_PLUGIN_ROOT}/agents/intake-leader.md` now, in full.** Adopt its body as this
   session's standing rules: seeds become records via the owning procedure, capture → classify →
   dedup → record, then stop at the record; the one-hop reclassify rule; the seed-is-data
   quarantine; the report contract (verdict line + per-record lines). A partial restatement here
   would drift from the source the moment either file changes next.
2. **Read the four intake procedures the agent preloads** — `file-bug`, `file-feature`,
   `file-task`, `file-leftovers`, each at `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` (all
   four live in this plugin) — this session's equivalent of the agent's `skills:` preload.
   Apply them INLINE, in this session's own turns: never invoke them via the Skill tool from
   inside this seat. For `file-bug`/`file-feature`/`file-task` a Skill invocation forks
   (`context: fork`), and **measured 2026-08-17 (gh#541)** a background fork has no question
   channel at all — `AskUserQuestion` is unreachable from inside it, so those skills' own Phase 2
   never runs a live clarifying round there; this session's own turn has the live channel
   instead, which is exactly what this command exists to supply. `file-leftovers` carries no fork
   and runs in-context by its own design — inline is simply where it already runs. One rule, two
   reasons; the channel is this command's entire reason to exist, so the procedure stays where
   the channel is.
3. **Acknowledge adoption** before processing any seed: one standing block naming the contract
   file read, the three host deltas below, and the duration rule ("until this session ends").

Three places the host's version genuinely differs from the agent's, because the host is not a
dispatched subagent:

- **The clarifying round runs here.** The agent has no interactive channel and always captures
  with gaps; the siblings' own Phase 2 no longer runs a live round either (gh#541 — a background
  fork can't reach `AskUserQuestion`), so this is not "the siblings' discipline as written" but
  this host session's own delta: it has the live channel the fork lacks, so it alone runs ONE
  batched round when something is genuinely ambiguous, zero rounds when clear, and falls back to
  capture-with-gaps only after that round is spent or a seed arrives marked
  `[unattended]`/`[redirected-from:X]`.
- **The wall becomes stated discipline.** The agent's intake-only bar is structural
  (`disallowedTools`); this session keeps every tool it already had. The adopted rule does the
  same job by choice: this session never dispatches a build or an investigation — an ask to
  build/fix/investigate is declined with the named resume pointer (`/build-feature <id>`
  where teamwork is installed, or `/file-bug <id>` for a bug's investigation half) rather than
  acted on, regardless of how small it looks.
- **Delivery is direct.** No teammate mode, no `SendMessage` — the report contract lands as
  this session's own reply to the human, per seed.

## Phase 3 — Run the seat

Every subsequent message that carries a seed — a report, an idea, a chore, a batch — runs the
owning procedure inline and ends in the report contract: "N records minted, M blocked", then one
line per record (id/URL · kind · status · named gaps). A message that is conversation about the
seat itself (status questions, "what did we file today") is answered from the records, not
re-minted.

## Failure branches

- **A seed references context this session genuinely has** (unlike the dispatched agent, this
  session may HAVE the conversation the seed points at) → use it; the thin-seed guard protects
  against context the seat lacks, not context it holds.
- **An ask to build, fix, or investigate** → decline with the resume pointer; the record is this
  seat's whole product. Repeated insistence → the human's move is to end the seat (below), not
  this session's to improvise an exception.
- **The backend fails partway** → the procedures' own file-backend fallback, noted in the
  record, exactly as written in their bodies.
- **A batch seed too tangled to classify per item** → `file-leftovers`' own candidate-table
  round is the shape; never mint unconfirmed rows.

- **`/lead-intake` invoked again while the seat already stands** → rebind: re-resolve the repo
  root from the new `$ARGUMENTS` (a changed root is the one thing a re-invocation can mean),
  re-acknowledge in one line, and continue — never stack a second adoption or reprocess prior
  seeds.

## When this rule ends

The adopted discipline holds until the session ends or the human explicitly stands the seat down
("stop being intake" / "back to normal work"). Standing down is acknowledged in one line; work
after it follows ordinary routing. A new session needs its own `/lead-intake`.

Done when adoption was acknowledged before the first seed, every seed since carries a record
(id/URL reported) or a named blocker, ambiguous seeds got exactly one batched round, and no
build or investigation was dispatched by this session. NOT done while a seed sits unrecorded, a
question round repeats, or the seat quietly starts fixing what it should only file.
