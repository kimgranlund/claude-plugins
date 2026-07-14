# Durable memory vs. ephemeral task state

> Axis: persisting facts and preferences so they survive past the current session, kept distinct
> from a task's in-session state. Grounded in Claude Code's own auto-memory system — a platform
> fact, quoted directly from the dispatching session's own memory instructions, observed
> 2026-07-13; verify against Anthropic's current Claude Code documentation if this pack ages,
> since a shipped product's own system instructions can change between versions.

## The core distinction — future sessions vs. this conversation

**Claim — memory is reserved for information a FUTURE session will need; a Plan (aligning on an
approach before a big change) and a Task list (tracking in-progress work within the CURRENT
conversation) are explicitly NOT memory**, even though both look like "things worth writing
down." **Grounding (worked instance, quoted verbatim):** "memory should be reserved for
information that will be useful in FUTURE conversations" — and the two named non-memory
mechanisms get their own explicit call-out: "If you are about to start a non-trivial
implementation task and would like to reach alignment with the user on your approach you should
use a Plan rather than saving this information to memory... When you need to break your work in
current conversation into discrete steps or keep track of your progress use tasks instead of
saving to memory." **Failure mode this prevents:** collapsing all three into one bucket either
pollutes future-session memory with information nobody outside the current task will ever need
again, or loses in-progress task state by mis-filing it as a "memory" that gets treated as
settled fact rather than live, mutable work.

## Four memory types, each load-bearing for a different reason

**Claim — a memory system that distinguishes only "important" from "unimportant" under-serves
the actual shapes worth persisting; Claude Code's own system names four, each answering a
different future question:**

- **user** — facts about the human's role, goals, responsibilities, and knowledge, so future work
  tailors itself to who they are, not just what they asked. Worked instance, quoted: "I'm a data
  scientist investigating what logging we have in place" saves as "user is a data scientist,
  currently focused on observability/logging."
- **feedback** — corrections AND confirmations of approach. The instance is explicit that
  confirmations matter as much as corrections: "record from failure AND success: if you only save
  corrections, you will avoid past mistakes but drift away from approaches the user has already
  validated." A correction alone teaches what not to do; a confirmation alone is what keeps a
  validated, non-obvious choice from being silently re-litigated next time.
- **project** — ongoing work, decisions, or constraints not derivable from the code or git
  history itself (a deadline, a stakeholder ask, the reason a rewrite is happening).
- **reference** — a POINTER to where information lives in another system (a Linear project, a
  Slack channel, a dashboard URL), not the information itself — the memory is "look here," not
  "here is the answer as of today."

**Failure mode a missing type causes:** without the `feedback` type's success-confirmation half,
a memory system trends toward pure caution — accumulating "don't do X" without ever
re-confirming "yes, keep doing Y" — which drifts the agent away from approaches the user already
validated as correct.

## The technique: convert relative dates to absolute at save time

**Claim — a `project`-type memory must convert any relative date in the triggering message to an
absolute date BEFORE saving**, because the memory will be read back at some unknown future point
when "Thursday" or "next week" no longer resolves to anything. Worked instance, quoted: "we're
freezing all non-critical merges after Thursday" saves as "merge freeze begins 2026-03-05 for
mobile release cut" — the relative "Thursday" converted to the absolute date at write time.
**Failure mode this prevents:** a memory that stores the ORIGINAL relative phrasing becomes
silently misleading the moment enough time passes that a fresh reader can no longer tell what
"Thursday" meant — the memory looks precise but has actually gone stale in a way that is
invisible until acted on.

## The hard exclusion list is as load-bearing as the inclusion rules

**Claim — a memory system that saves everything plausible is exactly as broken as one that saves
nothing; an explicit exclusion list is required.** The worked instance's excluded categories:
code patterns, conventions, architecture, or file paths (derivable by reading the current project
state) · git history or who-changed-what (`git log`/`git blame` are authoritative) · debugging
solutions or fix recipes (the fix lives in the code; the commit message carries the context) ·
anything already documented in a project's own entry file. **Why this matters:** each excluded
category already has an authoritative live source that can drift out of sync with a saved copy —
a memory duplicating derivable state is a second, unsynchronized copy of a fact whose real answer
is one `grep` or `git log` away, and the copy is the one that goes stale first.

## The single most load-bearing caveat: verify before trusting a recalled memory

**Claim — a memory that names a specific function, file, or flag is a claim that the thing
existed WHEN THE MEMORY WAS WRITTEN, not a claim that it exists now; before acting on a recalled
memory (not merely discussing it), the referenced file/function/flag must be re-checked against
current reality** (does the file still exist, does a grep for the function still find it).
Worked instance, quoted directly: "'The memory says X exists' is not the same as 'X exists
now.'" **Failure mode this prevents:** a stale memory that is technically well-formed (specific,
confident, citing a real-sounding symbol) is more dangerous than an absent one, because it looks
authoritative right up until the moment a recommendation built on it fails against a codebase
that moved on. This generalizes past Claude Code's own system: ANY durable memory naming a
concrete artifact needs the same re-verification step before it drives an action, regardless of
which harness or storage mechanism holds it.

## What this file does NOT cover

Organizing a body of already-true reference facts into a retrieval-by-search corpus (the sibling
knowledge-packs-and-cited-retrieval reference file in this same skill) · a curated, admitted,
judged TRAINING corpus as a different and heavier persistence shape entirely (covered there,
under "a heavier flavor") · routing a live request to a capability, a distinct harness concern
this skill does not own · the mechanics of any OTHER agent harness's memory system, which may
differ from Claude Code's four-type shape.
