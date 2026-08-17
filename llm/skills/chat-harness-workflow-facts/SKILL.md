---
name: chat-harness-workflow-facts
description: >-
  How a chat-agent harness composes MULTIPLE agents for work too large for one context —
  project-agnostic. Use for chain-of-command decomposition (plan vs build vs review, escalate a
  discovered constraint), when work earns a team of agents instead of staying inline, a typed hand-off a coordinator can
  verify, not trusted prose — what fields a subagent hands back when it finishes, and
  scripted pipelines (parallel/barrier) vs turn-by-turn dispatch. Grounded in this harness's own
  mechanics + a shipped team; answers, no build. NOT one skill's routing
  (chat-harness-routing-facts); NOT measuring a run (chat-harness-logging-facts).
disable-model-invocation: false
user-invocable: false
---

# chat-harness-workflow-facts — composing multiple agents for one job

Answers how a chat-agent harness gets work done that is too large for one agent's context: split
it across several specialized agents with a clear chain of command, hand work between them on a
contract the next step can *check* rather than merely trust, and — where the shape of the work is
known in advance — run it as a deterministic script instead of an agent deciding dispatch
turn-by-turn. This is a PATTERN pack: every claim is grounded either in this harness's own,
directly-inspectable Agent/Workflow tool mechanics or in a real shipped instance of the pattern
(the `orchestration` plugin's five-seat delivery team; harness's `write-handoff` skill) — cited as
a worked example so a claim can be verified against a real file, never as "the only way to do
this."

| Ask | Load |
|---|---|
| Chain of command — "who plans vs who builds vs who reviews", "decompose across a team", "the builder found the plan is wrong, now what" | `references/multi-agent-decomposition-and-chain-of-command.md` |
| The typed hand-off — "what fields go in a report back", "make this hand-off verifiable", "the coordinator can't tell if the build actually passed" | `references/typed-handoff-contracts.md` |
| Deterministic pipelines — "script this instead of dispatching ad hoc", "fan out and fan back in", "parallel vs pipeline", "when does a barrier belong" | `references/deterministic-workflows-vs-ad-hoc-dispatch.md` |
| Self-correct retry feedback design — "the model keeps repeating the same mistake on retry", "what should the feedback actually say", "the retry note leaked internal process to the user" | `references/self-correct-feedback-design.md` |
| Editing a settled answer — "the user wants to change an already-submitted answer", "answered vs disabled", "stale-while-revalidate for an async surface" | `references/settled-answer-state-law.md` |
| A model's own declared plan — "let the model propose a plan without letting it execute one" | `references/model-declared-plan-vs-host-execution.md` |
| Provenance — platform mechanic vs worked-example source | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`team-lead`, `Status`/`Evidence`, `agent(`/`parallel(`/`pipeline(`, …) and Read
   that section — the files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (this harness's own tool
   mechanics, or the worked example's `file:line`/named construct) + the failure mode it
   prevents**. A composition claim without the failure mode it exists to prevent is half an
   answer — every pattern here exists because ad hoc, undisciplined multi-agent dispatch fails in
   a specific, observable way, and the failure mode is the point.
3. **Distinguish "this is a mechanic of the harness itself" (a platform fact — verify against
   current docs if this pack has aged) from "this is how the worked example chose to structure
   it" (a design choice — a consumer's own team may reasonably differ in seat names or file
   layout, as long as the invariant the pattern protects still holds).**
4. Route output work at the boundary (see below) — this pack answers; it does not build.

## The core invariants (why these patterns exist)

- **A dispatch the host cannot verify is a dispatch the host cannot trust.** A subagent is stood
  up in fresh context, does work, and reports back — the dispatcher never watches it happen. If
  the only thing that comes back is prose ("I fixed it, tests pass"), the dispatcher has nothing
  to check the claim against. Every mechanism in this pack — the typed hand-off, the review gate
  between phases, the deterministic pipeline's structured per-item schema — exists to replace "I
  did the thing" with something the next step can confirm without redoing the work.
- **A maker never grades its own output (generator ≠ critic).** A chain of command that lets the
  same seat build a thing and also certify it is done is not a chain of command, it is a rubber
  stamp with extra steps. The reviewer role must be a distinct dispatch, in its own fresh context,
  scored against a named standard — never the builder's own closing summary.
- **A repeated failure indicts the contract, not the seat.** When a build seat hits the same wall
  twice, re-dispatching it a third time to try harder is not a fix — the plan, spec, or LLD it was
  given was wrong, and only the seat that owns that document can repair it. The escalation loop
  exists specifically to route a discovered constraint UP to the owner of the broken assumption,
  not to grind the same worker against it.
- **A scripted pipeline and an agent deciding dispatch turn-by-turn are different tools for
  different shapes of work.** When the fan-out shape is known before anything runs (audit these N
  files, review this diff from 4 lenses), a pre-written script is reproducible, reviewable before
  it executes, and pays no per-step model-deliberation cost. When the shape of the work depends on
  what the first agent finds, only an agent deciding the next dispatch can adapt — scripting a
  shape you don't yet know is premature structure, not discipline.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Design or review the wiring itself — which unit (skill/subagent/team), frontmatter, `skills:`
  preloads** in YOUR project → your project's own fleet-rules seat/skill (this pack
  teaches the composition PATTERN across agents; it does not own any project's frontmatter).
- **One skill's own trigger/description routing** (why a single skill triggers or doesn't, how to write
  its trigger phrases) → [[chat-harness-routing-facts]] (the sibling pack in this plugin) —
  that is a one-skill concern, this pack is about composing several AGENTS.
- **Logging, tracing, or measuring what a run actually did** (token spend, latency, which tool
  fired) → [[chat-harness-logging-facts]] (the sibling pack in this plugin) — that pack answers
  what happened; this one answers how the work was structured to happen in the first place.
- **Build or fix a coordinator, a hand-off block, or a workflow script in YOUR project** → your
  project's own orchestration seat/build seat (this pack has none — it teaches the pattern, it
  owns no codebase's source).

## Extending this pack

Extension: governed by [[make-pack]]
