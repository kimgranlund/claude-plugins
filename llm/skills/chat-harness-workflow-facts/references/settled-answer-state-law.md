# Editing a settled answer — append, never rewind; answered is not disabled

> Axis: once a form/questionnaire answer in a chat product is "settled" (submitted, accepted by
> the agent), what happens when the user wants to change it — both at the transcript level (what
> the agent reasons over) and the UI level (what the control looks/behaves like). Grounded in a
> worked instance: `@agent-ui/a2ui`'s ADR-0196 and ADR-0191.

## Amendment appends; the transcript never rewinds

**Claim — editing a settled answer appends an amendment turn ("Changed: X → Y") the agent
reconciles FORWARD; prior turns are never rewritten or removed.** Rewind falsifies the record the
agent reasons over; removal orphans the Edit affordance's own anchor. Re-confirming the same
answer appends nothing. · ADR-0196 cl.5 (`.claude/docs/adr/0196-…`) · 2026-08-17 · [verified]

**Why this matters:** a transcript an agent reasons over is only trustworthy if it is a strict,
append-only history of what was actually said, in order — a rewind or deletion is not "cleaning
up the record," it is corrupting the one thing downstream reasoning depends on being true.

## "Answered" is a visual state, not a disabled control

**Claim — settling a form/question by hard-disabling its inputs reads as broken or forbidden and
forecloses correction; the fix is a dedicated answered/settled visual state that keeps the
control focusable and routes changes through an explicit Edit affordance.** Precedence:
`disabled > pending > answered > affordance states` — an answered control must not repaint to
live-entry colors on hover, or the UI re-advertises interactivity the settle flow deliberately
removed. · ADR-0196 cl.1-4 (GH #805, a shipped-and-retired posture) · 2026-08-17 · [verified]

## Stale-while-revalidate needs one fleet-wide pending convention

**Claim — async surfaces keep rendering the last settled value DIMMED (one opacity token, one
host state) while a new answer streams in, rather than each component inventing its own pending
treatment.** Opacity, not a color repoint, because stale content is arbitrary unknown-depth DOM a
token repoint can't reach. One state law per axis; new axes compose with, never reopen, closed
tables. · ADR-0191; trait at `packages/agent-ui/components/src/traits/pending-computed.ts` ·
2026-08-16 · [verified]

## What this file does NOT cover

The host-side plan/execute/synthesize loop a model's own declared plan rides through
(`model-declared-plan-vs-host-execution.md`) · the self-correct retry loop's own feedback design
(`self-correct-feedback-design.md`) · the settled-answer's own PROTOCOL-level framing as a new
user turn on the wire (a distinct, session-model concern) — [[llm-gateway-facts]]'s
`stateless-session-and-turn-model.md`.
