---
name: sub-agent
description: >-
  Dispatches unattended via the Agent tool. First token exact-matches a registered agent name, or
  a registered skill name (bare or `plugin:skill`-qualified) → that target's dispatch, optionally
  NAMED via the literal marker `as NAME` — named stays continuable (`SendMessage`), no name
  given is one-shot and synchronous; skill/free-instruction dispatches default to sonnet (name a
  model in the task to override; agent targets keep their own pins). No target match → the whole
  $ARGUMENTS is a free-instruction charter, spawned NAMED by default (auto-derived slug)
  — say "one-shot"/"quick" for synchronous instead. Run
  /sub-agent {agent-or-skill-name} [as name] {task}, or /sub-agent {free-instructions}. NOT the
  forked form (`/fork-agent {name}` — background fork, registered agents only); NOT the
  host-adopts-contract form (`/bind-{seat}`); NOT a per-seat alias; NOT batch find-and-confirm
  across many tickets (`/mobilize-chores` — this command is one ad-hoc target, not a queue).
disable-model-invocation: true
user-invocable: true
argument-hint: "{agent-or-skill-name} [as name] {task}, or {free-instructions}"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# sub-agent — the `sub-` mechanic: named/parameterized target dispatch, plus free-instruction dispatch

ADR-0020 D3's third command head: `sub-` names a real, unattended `Agent`-tool dispatch — a
genuinely separate context, not this session and not a fork of it. Every seat in the estate that
already has a standing dispatched twin (`build-leader`, `planning-leader`, `review-leader`,
`product-leader`, `fleet-marshal`, and the rest) was already reachable via the `Agent` tool by
name; every skill in the estate is reachable via the `Skill` tool or, wrapped, the `Agent` tool.
This command is the generic, parameterized front door to both. Per D4, no per-seat alias is
minted here — `/sub-agent {target} [as name] {task}` is the whole surface.

**2026-08-19 amendment (Kim's live ruling).** This skill absorbs the free-instruction dispatch
originally shipped as a separate sibling, `sub-task` (#745/#746, retired same-day, zero adoption)
— `sub-agent` is dual-mode, target-dispatch or free-instruction. This slightly amends ADR-0020
D3's `sub-` head semantics (D4's no-per-seat-alias rule is untouched); recorded here as an inline
dated note rather than a fresh ADR supersession, per Kim's own explicit 2026-08-19 ruling.

**2026-08-22 amendment (Kim's live ruling): skill targets and explicit naming.** Registered-target
dispatch (Phase 2a) was agent-only and always unnamed; it now also resolves a registered SKILL
name, and either target kind accepts an explicit name via the literal `as <name>` marker. **The naming
default for a KNOWN target is the opposite of the free-instruction path's**: omit the name → the
dispatch is UNNAMED, one-shot, synchronous — Kim's own framing, "when you give it a name it
stays," reads the converse as the default. This is deliberately asymmetric against Phase 2b's
already-shipped named-by-default free-instruction path (2026-08-19 ruling above, untouched) — a
known target is usually a quick, bounded ask; a free-instruction charter is usually substantial
enough to need follow-up. Motivating case: `teamwork:mobilize-chores` step 5 (2026-08-21 ruling)
found an unnamed `build-leader` dispatch cannot be nudged once its one synchronous return has been
relayed — the plan-approval write-gate's accept-marker round trip depends on a resumable seat.

**Naming-default (free-instruction path) is a deliberate, Kim-ruled deviation from `fleet-rules`
A3-R1 (2026-08-19), not an oversight.** A3-R1 asks whether continuation is genuinely needed PER
CHARTER before naming a dispatch; Phase 2b instead defaults every no-match dispatch to named,
demoting the unnamed/synchronous form to an explicit opt-out (the literal word "one-shot" or
"quick" in the charter). A fresh-context skill-checker pass flagged this as a live tension against
A3-R1's own per-instance-judgment posture; Kim's ruling (interactive, 2026-08-19) was to keep the
default-to-named design as drafted. Read this paragraph as that ruling's own citation, not a
routing ambiguity to resolve independently later.

## Phase 1 — Resolve the target: registered skill, registered agent, or free instructions

`$ARGUMENTS`' first token is checked, in order, against a registered skill name, then a registered
agent name.

- **Skill match** — the token exact-matches (case-sensitive) an installed skill: bare form (e.g.
  `mobilize-chores`) searched across every installed plugin's `skills/<name>/` directory plus the
  project's own `.claude/skills/<name>/` and the user's `~/.claude/skills/<name>/`; or
  `plugin:skill`-qualified form (e.g. `teamwork:mobilize-chores`), which resolves directly with no
  ambiguity risk. A BARE name matching more than one installed plugin's `skills/` directory is a
  collision — report it and ask for the qualified `plugin:skill` form; never guess which one was
  meant. One match → continue at Phase 2a-skill.
- **No skill match, exact agent match** (case-sensitive, no fuzzy resolution) against one of the
  three real agent homes — every installed plugin's cache (`~/.claude/plugins/cache/*/*/*/agents/<name>.md`),
  the current project's own `.claude/agents/<name>.md`, and the user's own `~/.claude/agents/<name>.md`
  — → continue at Phase 2a-agent.
- **No match on either** → the WHOLE of `$ARGUMENTS` (not just the tail) is a free-instruction
  charter — no registered target to name, arbitrary instructions instead. Continue at Phase 2b.
- **Typo guard** (mitigates the original hazard that argued against overloading `sub-agent`):
  before falling through to Phase 2b, check whether the unresolved first token is a single
  kebab-shaped word within edit distance ~2 of a registered skill OR agent name found across the
  homes above. If so, ask ONE confirm via `AskUserQuestion` — "no skill or agent named `<token>` —
  free instructions instead, or did you mean `<candidate>`?" — before doing anything else; never
  silently dispatch either path on a plausible typo. No close candidate → proceed straight to
  Phase 2b, no question asked.

**Explicit name marker (both target paths).** A name is given with the literal marker `as`: once
a skill or agent target resolves, the dispatch is NAMED iff the next two tokens read
`as <name>` — the token after `as` is the name (a kebab slug, `^[a-z][a-z0-9-]*$`; anything else
after `as` is a malformed name, a Failure branch, never silently folded into the task) — and
everything after those two tokens is the task (which cannot be empty). No leading `as` → no name:
the whole remainder is the task, unnamed dispatch. A shape heuristic was considered and rejected
(fresh-context checker, 2026-08-22): no shape rule can distinguish a name slug from a
kebab-shaped task-opening verb — `.../build-leader ship ticket #240` and
`.../build-leader fix-the-bug now` both misparse under any "bare word then more text" rule; the
literal marker is the only unambiguous grammar. Examples: `/sub-agent mobilize-chores as
plugins-chores-agent run the ops sweep` — target `mobilize-chores` (skill), name
`plugins-chores-agent`, task "run the ops sweep", NAMED. `/sub-agent build-leader ship ticket
#240` — no `as`, task is the whole remainder, unnamed. A task that itself begins with the word
"as" (rare) still parses per this rule — quote or rephrase the task, or accept the parse; the
marker is absolute, never guessed around.

### Phase 2a-agent — Seal and dispatch a registered agent

Invoke the `Agent` tool against the resolved agent, `subagent_type` the agent's own name, carrying
the task as its prompt — sealed the way any dispatch is: the task stated once, enough context that
the agent doesn't have to guess scope, and nothing this session should have done itself instead.
**Explicit name given** → `name: "<the given name>"`; state the mailbox semantics in the reply
(addressable via `SendMessage`, result arrives as a completion notification, continuable) exactly
as Phase 2b's default path does. **No name given** → unnamed, synchronous; this call's own return
is the answer. This command's own job ends at the seal; it does not narrate the dispatched agent's
internal turns.

### Phase 2a-skill — Seal and dispatch a registered skill, wrapped in an Agent call

A skill target is never run inline via the `Skill` tool from this command — it is wrapped in an
`Agent` dispatch (`subagent_type: general-purpose`, sealed prompt instructing it to invoke the
named skill with the given task) so it gets the identical background/isolation treatment as the
agent path, never blocking this session or skipping isolation the skill's own contract might
assume. **This command performs no isolation of its own** — worktree isolation, if the target
needs it, is that skill's own responsibility (e.g. `dispatch-ticket`'s unconditional Phase 3), the
same "out of scope, left to the dispatched target" posture as the agent path. Naming follows
Phase 2a-agent's rule identically: explicit name → `name:` set, mailbox semantics stated; no name
→ unnamed, synchronous.

**Model default (Kim's ruling, 2026-08-22): pin `model: sonnet` on this wrap.** `general-purpose`
carries no frontmatter pin, so without this the dispatch silently inherits the SESSION model — a
fable session prices every routine skill run at fable, the exact leak this default closes. The
task text naming a model ("use opus", "on fable", "haiku is fine") overrides the pin; the
registered-AGENT path (2a-agent) is untouched — a resolved agent's own frontmatter tier IS its
model, never overridden or defaulted here. Effort cannot be set on a plain `Agent` dispatch
(`agent-writing-rules`' dispatch-time mechanics — frontmatter or Workflow only), so no effort
claim is made; state the chosen model in the reply.

### Phase 2b — Seal and dispatch a free-instruction session (absorbed from `sub-task`)

Seal the whole `$ARGUMENTS` as a self-contained charter — no conversation history, no implicit
"this"/"the above". An unresolved deictic reference gets one inline clarifying question before
dispatch, never a guess; empty `$ARGUMENTS` (once the typo-guard above has already ruled out a
near-miss target name) → ask what the subtask is, never invent one.

**Default: named and continuable.** One `Agent`-tool call, `subagent_type: general-purpose`,
NAMED — a short kebab slug auto-derived from the charter (e.g. a charter about auditing color
tokens → `subagent-color-audit`), unique via a short random suffix when a collision is plausible
(e.g. `subagent-color-audit-a4f2`) — never `ListAgents` for this: `team-scaffolding`'s own shipped
ruling reserves `ListAgents` for confirming liveness of an already-known name, never for finding
or probing one, and a per-dispatch collision check reads too close to that discouraged "find" use
to risk; the random-suffix path is the resolution, not a fallback. Pin `model: sonnet` per the
ad-hoc-dispatch doctrine (`agent-writing-rules` §Model tiering) — the same session-model-inherit
leak Phase 2a-skill's model default closes — unless the charter itself names a model (the user's
override) or its judgment load plainly earns more; state whichever was chosen. The judgment-load
escalation channel is THIS path's alone (an unbounded free charter can genuinely earn a higher
tier); Phase 2a-skill deliberately has no such clause — a bounded skill run overrides only by the
user naming a model, never by self-escalation, or the fable leak reopens by the back door.

This naming is the CANON-SANCTIONED deliberate-continuation case, not the fan-out class gh#154/
gh#157 ban: it names a single seat the user explicitly means to resume, never a fanned-out worker
with nowhere to address a report back to — `fleet-rules`' own A3-R1 ("named ONLY when
continuation is needed; never on a fan-out") is exactly this case, distinct from the never-name
rule's own target (`agent-writing-rules`' negative-patterns table row, "Coordinator names a
fanned-out seat it doesn't need to resume").

State the mailbox semantics in the reply, every time a NAMED dispatch fires (Phase 2a-agent,
2a-skill, or 2b's default): the seat is addressable going forward by its name (`SendMessage`, or
ask the marshal to relay in a fleet context); its actual result arrives later as a completion
notification, not this call's own return; it is continuable with follow-ups. Carry the A3 caveat
too (`fleet-rules`' A3-R4, `agent-writing-rules`' teammate-mode delivery clause): the seat's own
plain-text final does NOT auto-deliver — only its completion notification, or an explicit
`SendMessage`, actually carries a result back.

**One-shot exception (Phase 2b only).** The charter carrying the literal word "one-shot" or
"quick" (or an equivalent explicit ask for a single synchronous answer, nothing to resume) takes
the unnamed/synchronous path instead — exactly as the original `sub-task` shipped (#745). This
exception is specific to the free-instruction path's own named-by-default posture; Phase 2a-agent
and 2a-skill are already unnamed by default, so "one-shot"/"quick" in the task text has no special
meaning there.

## Phase 3 — Relay the return

- **Registered-target path (2a-agent/2a-skill), no name given.** The `Agent` tool's own
  completion is the caller's answer — relay it, don't re-summarize it away or add unearned
  framing.
- **Registered-target path (2a-agent/2a-skill), NAMED.** Relay the dispatch confirmation: the
  seat's name, a one-line task summary, and the mailbox semantics stated above. There is no
  synchronous answer yet — it arrives later, as that seat's own completion notification or an
  explicit `SendMessage` once addressed.
- **Free-instruction path, default (named).** Same as the registered-target NAMED case above.
- **Free-instruction path, one-shot.** Relay the result verbatim-in-substance, findings-first — no
  re-summarizing away the answer, no unearned framing on top of it.

## Failure branches

- **No skill or agent name resolves, and no plausible typo-guard candidate** → falls through to
  Phase 2b (free instructions); this is not a failure, it's the dual-mode design.
- **A bare skill or agent name matches more than one installed plugin's home** → report the
  collision, name every match, and (for a skill) suggest the `plugin:skill`-qualified form; never
  guess.
- **Registered-target path: `$ARGUMENTS` carries no task after the target name (and any
  `as <name>` marker)** → report that a task is required; never invent one to fill the gap.
- **Registered-target path: `as` is present but the following token is not a kebab slug
  (`^[a-z][a-z0-9-]*$`), or nothing follows it** → malformed name; report the expected
  `as <kebab-slug> <task>` grammar and stop — never silently fold the marker into the task.
- **Free-instruction path: dispatch dies** (no return, an error) → report it, then one re-dispatch
  of the same sealed charter, max — never a silent retry loop.
- **Free-instruction path, one-shot: the result contradicts a stated constraint** (scope, format, a
  stated non-goal) → report the gap plainly; never silently accept a result that misses its own
  brief.
- **This session itself is a nested dispatch and holds no `Agent` tool of its own** → this command
  cannot run at all; report the capability gap plainly rather than attempting a dispatch, and name
  the resume path (return to a session that does hold the tool).
- **This session itself is a nested dispatch AND holds the `Agent` tool, any UNNAMED path**
  (registered-target with no name, or free-instruction one-shot) → the no-nested-wait rule: do not
  dispatch and then end this turn waiting on a background callback — the `Agent` tool's own return
  is synchronous from this call's perspective; act on it directly.
- **This session itself is a nested dispatch AND holds the `Agent` tool, any NAMED path**
  (registered-target with an explicit name, or free-instruction default) → the named seat's
  completion notification routes to the ROOT session, never back to this nested seat
  (`dispatch-ticket`'s own no-nested-wait preamble, verified A4, 2026-08-10) — state this plainly
  in the reply rather than promising a callback this seat structurally cannot collect on; whoever
  holds the root session is who actually sees that seat report in, not this dispatcher.

## Done

Done when Phase 1 resolved cleanly (a registered skill, a registered agent, a confirmed typo-guard
redirect, or a free-instruction fallthrough with no plausible near-miss); any `as <name>` marker
was parsed per its own literal grammar; the matching Phase 2 dispatch
sealed once, named or unnamed per the resolved rule; and Phase 3's matching relay ran — a
synchronous return relayed verbatim (any unnamed path, or free-instruction one-shot), or the named
seat's mailbox semantics stated in full (any named path). NOT done while a dispatch sits
unrelayed, a collision or typo-guard candidate was silently resolved by guessing, an `as <name>`
marker was folded into the task text (or a malformed one silently accepted), or this session
narrates a sub-agent's own internal work instead of its return.
