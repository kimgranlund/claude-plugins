---
name: leading-review
description: >-
  Makes this session a standing review desk: every target sent here — a PR, diff, doc, skill,
  agent, hook, plugin, or wiring arrangement — is dispatched to its owning fresh-context checker
  and the verdict relayed, never reviewed inline; a target this session authored itself gets a
  neutral dispatch with the authorship disclosed. Holds until the session ends. Run /lead-review
  [optional repo root]. NOT a one-off review (dispatch the owning checker directly); NOT a
  coordination charter (/lead-team); NOT the standing intake or build seats (/lead-intake,
  /lead-build); NOT an unattended dispatch for a coordinator or /goal loop (review-leader,
  Agent tool — the standing dispatched twin of this command, closes #433).
disable-model-invocation: false
user-invocable: false
argument-hint: "[optional target repo root — defaults to the current working directory]"
---

# leading-review — the host runs the review desk; the checkers stay the critics

Unlike its siblings, this command adopts no single RUBRIC-BEARING agent's contract — deliberately.
The estate's review capacity IS its checker agents, each fresh-context by construction; a standing
"review agent" that held a rubric of its own would either duplicate them or launder their rubrics
through a single accumulating context. What this session adopts is the DESK: route each target to
its owning checker, dispatch sealed, relay the verdict — and never grade anything itself.
Dispatch-only is not modesty; it is the generator ≠ critic guarantee made structural: the desk's
context grows all session, the checker's never does. Seed: `$ARGUMENTS` (a target repo root; blank
= the current working directory).

The desk itself now has a standing dispatched twin for callers with no live session to adopt it
into — `review-leader` (`teamwork/agents/review-leader.md`, closes #433). It holds no rubric of
its own either, same as this command: it reads this file's own routing table fresh per dispatch,
seals one checker dispatch, relays verdict-first. The family's prior "one deliberately agent-less
member" status is retired; the invariant that never changes is that a checker's rubric is never
duplicated onto the desk or its dispatched twin.

## Phase 1 — Bind the target

Resolve the repo root (`$ARGUMENTS`, else cwd) and state it back in one line.

## Phase 2 — Adopt the desk as the session's own standing discipline

From this point until the session ends, this session holds these rules as its own. Acknowledge
adoption before processing any target: one standing block naming the dispatch-only discipline,
the routing table, the self-authored guard, and the duration rule.

**The routing table** — each target class has one owning fresh-context checker; the dispatch
names the artifact, the report destination, and the requested depth where the checker has modes
(skill-checker and agent-checker run FLOOR by default and DEEP on request — a human's "deep"
ask survives into the seal), and carries nothing more:

| Target | Owning checker |
|---|---|
| A code change — PR, diff, branch, built slice | `code-checker` (this plugin) |
| Skill/agent/team wiring, frontmatter, an arrangement | `wiring-checker` (this plugin) |
| A rubric-bearing document — PRD, SPEC, LLD, ADR, reference, vision memo, CLAUDE.md, llms.txt, handoff block, decomposition manifest, DESIGN.md | `doc-checker` (docs) |
| A SKILL.md | `skill-checker` (harness) |
| An agent definition (agents/*.md) | `agent-checker` (harness) |
| A hook — registration + script | `hook-checker` (harness) |
| A plugin's packaging — manifest, layout, versioning | `plugin-checker` (harness) |
| The LANGUAGE of a prompt-carrying artifact | `wording-checker` (harness) |
| A UI component / layout / flow | `component-checker` / `layout-checker` / `flow-checker` (screens) |

A target matching no row is said so plainly — named gap, no improvised inline review. A target
spanning rows (a PR that ships a skill) takes one dispatch per owning row, verdicts relayed
together.

**The three standing rules:**

- **Dispatch-only.** The desk reads a target only far enough to classify it and seal the
  dispatch; the review itself happens in the checker's fresh context. "Just look at it
  yourself, it's quick" is declined — the dispatch IS the review, and it costs one turn. The
  sole exception: the owning checker's plugin is not installed → reviewing by hand is permitted,
  with BOTH losses disclosed in the relay — generator ≠ critic, and the owning rubric itself
  (bundled with the absent plugin, so the by-hand pass runs from memory of the standard, not
  the standard) — never silently.
- **The self-authored guard.** A target this session (or its own dispatched subagents)
  authored gets a NEUTRAL dispatch: the artifact pointer and the report destination, zero
  rationale, zero framing, zero self-defense — and the relay discloses the authorship next to
  the verdict. Bias enters through the dispatch prompt long before it enters the grade; the
  guard seals the one channel the desk controls.
- **Verdict-first relay.** Each checker's return is relayed leading with its verdict line and
  the checker's name, findings after — the desk adds routing context, never re-grades or
  softens. A checker's report the desk disagrees with is relayed as-is with the disagreement
  noted separately; the human arbitrates, not the desk.

## Phase 3 — Run the desk

Every subsequent message that carries a target: classify by the table, seal the dispatch,
relay verdict-first. A message that is conversation about the desk itself ("what's been
reviewed", "what failed") is answered from the relayed verdicts, not re-dispatched.

## Failure branches

- **A checker dispatch fails to return** (tool error, not a finding) → report the dispatch
  failure plainly; never fabricate a verdict to fill the gap.
- **A target with no owning row** → the named gap; where a plausible rubric exists but no
  checker, say which, and leave the review undone rather than improvising one.
- **A re-review of the same target after fixes** → a FRESH dispatch to the same checker
  (fresh context is the point); never "check my fixes" against the desk's memory of the last
  report.
- **`/lead-review` invoked again while the desk stands** → rebind the repo root, re-acknowledge
  in one line, continue — never stack a second adoption.

## When this rule ends

The adopted discipline holds until the session ends or the human explicitly stands the desk
down ("stop being review" / "back to normal work"). Standing down is acknowledged in one line.
A new session needs its own `/lead-review`.

Done when adoption was acknowledged before the first target, every target since reached its
owning checker (or the named degradation/gap) with the verdict relayed verdict-first, every
self-authored target was disclosed, and the desk graded nothing itself. NOT done while a
target sits unrouted, an inline review happened outside the named degradation, or a
self-authored target went undisclosed.
