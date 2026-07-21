# Typed hand-off contracts — verifiable, not narrative

> Axis: how a subagent hands work back to whoever dispatched it (a coordinator, or the host
> itself) on a shape the recipient can *check* rather than merely trust. Grounded in forge's
> `handoff-compose` skill (`/Users/kimba/Projects/nonoun/plugins/forge 1.14.0/skills/handoff-compose/`)
> and this session's own Agent tool description.

## Why a hand-off must be checkable, not narrated

**Claim — a dispatched agent runs in fresh context and is stood down after it reports; the
dispatcher never watches the work happen and can only act on what comes back.** A hand-off that
forces the recipient to re-open files and re-derive the result to know if the work is real has
failed, however true its prose turns out to be. **Grounding — this session's own Agent tool
description states the exact failure mode this contract exists to prevent, verbatim, as the
justification for checking a subagent's work:** "Trust but verify: an agent's summary describes
what it intended to do, not necessarily what it did... check the actual changes before reporting
the work as done." **Worked instance:** `handoff-compose/references/foundations.md` §1: "the
handoff must let the next step *confirm the work without re-doing it*. That is the whole purpose
of Evidence and Tests/checks run: gate exit codes, file:line citations, and counts are checkable
in seconds; 'I tested it and it works' is not."

## The block — exactly these fields, in order

**Pattern — one fixed, ordered field set every agent hands back, so the recipient parses instead
of re-reading prose:** Status · Summary · Files changed · Tests/checks run · Evidence · Risks ·
Open questions · Recommended next action. **Worked instance, quoted verbatim from
`handoff-compose/SKILL.md`:**

- **Status** — `done | partial | blocked(reason)`, first line, nothing else on it — "the enum the
  coordinator routes on — outcome state never lives only in Summary prose."
- **Summary** — "what was done, in 1–3 sentences. The outcome, not the process."
- **Files changed** — "each path touched (created / edited / deleted), one per line."
- **Tests/checks run** — "the gates run and their result, *by command*... Name the command + its
  verdict — `pass | fail | UNMEASURED — skipped-not-passed`... a gate you didn't run is UNMEASURED,
  stated, never silently omitted."
- **Evidence** — "the proof a reviewer can verify *without re-doing the work*: gate exit codes,
  counts, `file:line` citations."
- **Risks** — "what could be wrong or fragile, the assumptions made, the blast radius — max ~5,
  each with its suspected locus (`execution | spec | plan`)... Honest, not reassuring."
- **Open questions** — "unresolved decisions needing a human or another role; max 3, each
  decision-shaped."
- **Recommended next action** — "the single best next step **and who owns it**."

Keep each tight; write `(none)` when a field is empty rather than omitting it. **Failure mode this
fixed order prevents:** a coordinator (or eval gate) that has to hunt through free-form prose for
whether a gate passed, or infer an owner for the next step, is doing work the contract exists to
remove.

## Consumer-as-critic — the recipient IS the review

**Claim — the field set's critic is its own consumer:** the coordinator's gate, or the host,
reading the block fresh is a deliberate, sanctioned form of independent review, not a missing
reviewer seat. **Worked instance:** `handoff-compose/SKILL.md`: "Its critic is the block's
consumer: the recipient... is fresh-context by construction (**consumer-as-critic**, a deliberate
form the standard sanctions, not a missing reviewer seat)." This is why Evidence and Tests/checks
run are written *for the critic specifically* (`foundations.md` §2: "Write those two fields *for
the critic*: name the command and its result, cite the proof. If the critic can't grade it from
the block, the block is underspecified.") — a hand-off that can't be graded from the block alone
has failed this contract regardless of whether the underlying work was actually fine.

## Write-once, and gate ≠ commit

**Pattern — a shipped hand-off is never edited in place; a correction is a re-dispatch and a fresh
block, because the recipient may already have routed on the version it read.** **Worked instance:**
`handoff-compose/SKILL.md`: "A handoff is **write-once**: once shipped it is never edited in
place — the recipient may already have routed on it; repair = re-dispatch + re-compose." A
second, related discipline: a green gate is not a landed change — read the gate output, *then*
commit as a separate step, never chained with `&&` onto the test run, "or a regression rides in on
a gate whose output was never read" (`SKILL.md` "Gate ≠ commit"). **Failure mode each prevents:** an
in-place edit silently invalidates a decision already made on the earlier version; a chained
commit lands code whose gate result nobody actually read.

## Drain the inbox before composing

**Pattern, for a hand-off from an agent running inside a messaging team rather than a sealed
one-shot dispatch: read every still-pending message before composing the block.** **Worked
instance:** `handoff-compose/SKILL.md`: "In a messaging team, drain your full inbox first. Read
every still-pending message before you compose — a handoff written one message behind is already
wrong the moment it ships." A **sealed subagent has no inbox** — its world was enumerated at
dispatch, so for it "freshness means consistency with the inputs it was handed," not draining a
queue that doesn't exist for it. **Failure mode this prevents:** a block that re-asks an already-
answered question, re-edits an artifact a teammate already committed, or retracts a finding a
newer commit already fixed.

## The mechanical gate

**Worked instance:** `handoff-compose/scripts/handoff_check.py` — "Mechanical H1 gate — field
presence, order, `(none)` markers, Status enum — run before any rubric judgment"
(`handoff-compose/SKILL.md`'s own references table). `team-lead.md` names the same
script as the coordinator's own most-mechanizable check: "run forge's `handoff_check.py`... against
every INBOUND handoff where forge is installed; otherwise check the block by hand against the
[same eight fields]." The mechanical pass (field presence/order) runs before any judgment call
about whether the content is actually good — the two are separate steps.

## What this file does NOT cover

The chain of command that decides WHO a hand-off routes to and when a builder should escalate
rather than hand back a normal report (multi-agent-decomposition-and-chain-of-command.md) · the
scripted-pipeline alternative, where a workflow script's own return value plays a similar
"checkable, not narrated" role for a fan-out of many agents at once
(deterministic-workflows-vs-ad-hoc-dispatch.md).
