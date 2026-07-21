# Multi-agent decomposition and chain of command

> Axis: how to split a task too large for one context across several specialized agents with a
> clear chain of command, so a builder never grades its own work and a broken assumption gets
> repaired at its source instead of ground against by the same worker repeatedly. Grounded in this
> harness's own Agent tool mechanics + the `orchestration` plugin's five-seat delivery team
> (`agents/team-lead.md`, `agents/planner.md`, `agents/builder.md`
> in `/Users/kimba/Projects/nonoun/plugins/teamwork/`).

## Solo-first — a team is not the default unit

**Claim — the null unit is the host working inline; a subagent or team must buy something the
host alone cannot: isolation (fresh context), parallelism (genuinely concurrent slices), or
independence (generator≠critic on a high-stakes artifact).** A task one context can hold is the
host's own — multi-step alone does not earn a team. **Worked instance:**
`team-or-solo-rules/SKILL.md` (the same plugin family) states this as Design step 1:
"Solo-first — the host inline is the null unit and wins by default... A dispatch that costs more
context and latency than doing the work inline is over-orchestration, whatever the task's step
count." `team-lead.md`'s own description states the same floor for itself: "Use
PROACTIVELY only when the work genuinely needs two or more seats... Solo-first: a task one context
can hold is the host's own; multi-step alone does not earn a team." **Why this matters (the
failure mode it prevents):** reflexive multi-agent ceremony on a task the host could finish in one
pass burns tokens and latency for a coordination cost nobody needed — the pattern in this file is
for work that genuinely doesn't fit one context, not a default posture.

## The chain — route by task shape, dispatch sealed

**Pattern — a coordinator/apex seat holds the chain of command and routes work by shape (design →
a planner seat, build-to-plan → a builder seat, adversarial review → a reviewer seat), and never
does the design or build work itself.** Each dispatch is a **sealed contract**: a charter,
enumerated inputs (never the coordinator's own deliberation or a sibling's transcript), a budget,
and a typed return. **Worked instance:** `team-lead.md` priority 1: "Route by
shape, dispatch sealed. Design / decomposition / doc work → planner. Build-to-plan /
enforcement work → builder... Adversarial review of a design doc → doc-checker;
adversarial review of a built change → code-checker" — each dispatch runs "on fresh context as a
sealed contract: charter, enumerated inputs... its budget, and the return contract." The
coordinator's own charter explicitly scopes its writes: "authoring docs and writing code are
planner's and builder's seats, not yours."

**Also directly verifiable in this session's own harness:** the Agent tool this exact reply is
using carries a `subagent_type` parameter naming a persona + tool-allowlist preset (a narrow
read-only reviewer vs a broad general-purpose builder) and an `isolation` option (e.g.
`"worktree"` for a build seat that must not collide with sibling edits) — the same sealed-dispatch
shape the worked example names in prose, expressed as the actual tool schema available to the
dispatching model right now.

## Generator ≠ critic — the reviewer is never the maker

**Claim — a maker's own closing summary is never the verdict; a distinct agent, in its own fresh
context, scores the artifact against a named standard.** **Worked instance:**
`planner.md` priority 4: "Report, don't grade. Return a concise design-status summary to
the coordinator. Your docs are reviewed by the doc-checker seat; you leave your own output for
that reviewer to score (generator ≠ critic)." `team-lead.md` priority 3 states the
coordinator's own limit on this: "the review verdict is theirs [doc-checker/code-checker] to
render, not yours to assign." **Why this ordering, not the reverse:** a coordinator (or a builder)
that certifies its own work has removed the one check that catches a plan the builder silently
deviated from, or a doc that reads as done to the person who just wrote it. **Failure mode this
prevents:** a rubber-stamped hand-off that looks complete because the same seat wrote both the
artifact and its own passing grade.

## The escalation loop — a repeated failure indicts the contract, not the seat

**Pattern — when a build seat discovers the plan it was given doesn't match reality, it escalates
UP to the seat that owns the broken document rather than silently deviating or being re-dispatched
to try again.** **Worked instance:** `team-lead.md` priority 4-5: "The same finding
failing twice indicts the contract, not the seat — escalate the locus instead of re-dispatching...
Run the discovered-reality loop. When builder... escalates a constraint, engage
planner to repair the OWNING doc and record the decision; ratify it; then let it propagate
down. Repair the owner — downstream copies are regenerated, not patched." **Why this matters (the
failure mode it prevents):** re-dispatching the same worker against the same wall a third time
wastes budget on a problem re-dispatch cannot fix — the plan itself is wrong, and only its owner
(the planner seat) can repair it. Routing the repair to the artifact's owner, once, is what lets
the loop actually converge instead of oscillating.

## Model/effort tiering by role — planning is not sized like execution

**Claim (a design choice worth naming, NOT a universal law the worked instance below actually
argues against): model/effort tier should be assigned deliberately, per role, and REVISITED as the
team's understanding of each role's real cognitive load shifts — not fixed once and left alone.**
**Worked instance, quoted exactly (the citation the earlier draft of this file got wrong — see the
correction note below):** the `orchestration` plugin's own changelog records its most recent
re-tiering as "planner opus+xhigh→fable+high, builder sonnet+high→opus+xhigh,
team-lead opus→sonnet (deliberate reclassification: routing/gating is coordination,
not judgment)" (`README.md`, v0.7.0 entry, 2026-07-12). Read plainly, this is the OPPOSITE of
"planning gets the stronger tier": the PLANNING seat was moved to a CHEAPER tier, the seat that
BUILDS against an already-ratified plan was moved to a MORE expensive one, and coordination/routing
was cut cheaper still on the grounds that it's "coordination, not judgment." **The honest lesson
this worked instance actually teaches:** don't assert a fixed rule ("planning always gets the
expensive model") from first principles — measure where the real judgment load sits in YOUR
system, and be willing to move a seat's tier in either direction as that assessment changes; this
same team's OWN prior tiering (visible in the changelog's earlier entries) had planning at a
higher tier before this very re-tiering moved it down.

**Correction note:** an earlier draft of this reference misquoted this same v0.7.0 line as
"planner sonnet+high→opus+xhigh" (the builder half of the real quote, misattributed
to planner) and used it to argue planning gets the stronger tier — a citation error caught
on independent review and fixed here; the quote above is the real, complete v0.7.0 entry.

## What this file does NOT cover

The exact fields and shape of the block a seat hands back when it reports (typed-handoff-
contracts.md) · the scripted, deterministic alternative to a coordinator deciding each dispatch
turn by turn (deterministic-workflows-vs-ad-hoc-dispatch.md) · how to design the wiring itself —
which unit, which frontmatter keys, `skills:` preloads — for a specific project (routed to that
project's own team-or-solo-rules seat, out of this pack's scope).
