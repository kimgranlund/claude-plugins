# Instruction layering — narrower scope refines, never silently replaces

> Axis: how a chat-agent harness composes several instruction sources (a global default, a
> project/deployment layer, a live session layer) so the more specific one wins for routine
> style and process, without accidentally letting it override a safety floor that isn't part of
> this stack at all. Grounded in Claude Code's own real, currently-loaded layering — verified
> directly in this authoring session, 2026-07-13.

## The layering shape — general, then project, then session

**Pattern — three nested scopes, each narrower than the last, each ADDING or refining rather than
replacing the wider one wholesale:** a global layer (every deployment/project this install ever
touches), a project layer (this one codebase/deployment), and a session layer (this one live
conversation's own instructions). **Worked instance:** this exact stack is loaded into this
authoring session right now — `/Users/kimba/.claude/CLAUDE.md` (the global, user-scoped
"Engineering Operating Contract," 23 lines) plus `/Users/kimba/Projects/nonoun/agent-ui/CLAUDE.md`
(70 lines, checked into that repo, scoped to it alone). The project file never restates the global
one's conventions (root-cause debugging, stale-context-is-a-defect); it adds repo-specific facts a
global rule cannot know — package layout, the `erasableSyntaxOnly` tsconfig constraint, the exact
`npm run check` gate. **Why narrower wins for this kind of content:** the project layer has more
concrete context about the actual constraints of the work than the global layer possibly can, and
the session layer (a direct instruction, a teammate's dispatch brief) has the most context of all —
each layer is closer to the ground truth of what's actually being built right now.

## A second, structurally identical instance — workspace vs. member

**Claim — the same precedence law recurs at a different grain, not just global/project/session:**
the `nonoun-plugins` workspace's own `CLAUDE.md` governs people working ON its plugins (routing
table, ship discipline), while each plugin's own `README.md`/`CLAUDE.md` governs that plugin's
runtime behavior once installed elsewhere — a strictly narrower, sibling concern. **Worked
instance:** `/Users/kimba/Projects/nonoun/plugins/CLAUDE.md`'s own closing instruction states this
explicitly: "Read the target plugin's own `CLAUDE.md` and README footer ledger first (per-plugin
invariants and version history live there, not here)" — a workspace-level document naming its own
narrower siblings as the more specific authority for their own scope, the same shape as
project-CLAUDE.md not restating global-CLAUDE.md.

## Precedence is a routine-content law, not a safety law

**The load-bearing caveat:** "more specific overrides more general" governs style, workflow, and
process content — it does **not** describe how a genuine safety/guardrail rule relates to a more
specific instruction. A safety floor stated at the broadest layer is not one more rung a session
instruction can out-rank by being "more specific" — it sits outside this stack entirely and is
covered by a different axis (see below), precisely so that a cleverly-scoped session-level request
can never talk its way past it by appearing more specific.

## Small-scale calibration

A minimal, single-deployment chat harness may validly run only two layers — a static system
prompt and a per-session config — and skip a "project" tier entirely; the third layer earns its
complexity only once the same harness install serves genuinely distinct deployments that need
different defaults (a multi-repo CLI, a multi-tenant bot). Naming the collapse explicitly ("this
harness has no project layer; global and session only") is preferable to a phantom middle tier
that's never populated.

## What this file does NOT cover

Which SOURCES of instruction are even valid candidates to enter this stack at all — a file a tool
just read is not a session-layer instruction no matter how it's worded
(injection-defense-and-instruction-source-boundary) · what happens once a specific ACTION is about
to be taken, regardless of which layer requested it (action-risk-tiers-and-confirmation-gates) ·
enforcing a layering rule as code rather than prose
(deterministic-rules-vs-prompted-guidance) · how structured settings-file layers (not prose
CLAUDE.md layers) compose and which one wins for a scalar value versus a hook registration
(config-precedence-and-setup).
