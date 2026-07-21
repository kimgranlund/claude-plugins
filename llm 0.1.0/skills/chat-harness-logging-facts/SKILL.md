---
name: chat-harness-logging-facts
description: >-
  How a chat-agent harness makes its own behavior legible. Use for "log what the harness did,
  not what the user typed", "distinguish an enforced hook block from the model just deciding not
  to act", "measure whether skill routing is actually accurate", "build a held-out adversarial
  suite for a skill's description", "is this routing regression real or judge noise", "notify on
  task completion instead of polling". Covers hook logging/tracing (PreToolUse/PostToolUse vs
  the transcript), routing-accuracy via a held-out adversarial suite (judge noise vs regression
  vs structural leak), and notification vs polling. Grounded in this harness's verified
  hook/tool mechanics + a dated eval-run history. ANSWERS from a cited corpus; never builds. NOT
  agents that DO the work (chat-harness-workflow-facts); NOT the routing MECHANISM
  (chat-harness-routing-facts); NOT implementing or building any of this — a logging
  pipeline, eval-suite runner, or notification webhook to write is the project's own build seat.
disable-model-invocation: false
user-invocable: false
---

# chat-harness-logging-facts — making a harness's own behavior legible

Answers how a chat-agent harness proves what it actually did, rather than what it merely said it
did: **deterministic tracing** (a hook firing around a real tool-call event, vs. the unstructured
conversation transcript), **measured routing accuracy** (a held-out adversarial eval suite scored
over repeated runs, vs. a felt sense that "routing seems fine"), and **completion signaling**
(automatic notification for work the harness itself dispatched, vs. deliberately-paced polling for
state the harness cannot track). This is a PATTERN pack: every claim is grounded either in this
harness's own currently-verified mechanics (a hook registration, a tool's own governing
instructions) or in a real, dated worked instance from this workspace's own skill corpus (an actual
eval-run history, a genuinely blind judge agent) — cited so a claim can be checked against a real
file, never presented as "the only way to do this."

| Ask | Load |
|---|---|
| Deterministic logging/tracing — "log what the harness did, not what the user typed", "trace a tool call", "a hook fired vs. the transcript says" | `references/logging-and-tracing.md` |
| Routing-accuracy measurement — "measure skill routing accuracy", "held-out adversarial eval suite", "is this a real regression or judge noise", "a blind routing judge" | `references/routing-accuracy-evals.md` |
| Background-task notification vs. polling — "notify instead of poll", "task-notification vs. an external CI/deploy check", "why shouldn't I sleep-loop on a background agent" | `references/background-task-notification.md` |
| Provenance — this harness's own verified mechanics vs. this workspace's own measured, dated worked instance | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`PostToolUse`, `eval-judge`, `task-notification`, `Monitor`, …) and Read that section — the
   files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (this harness's own currently-
   verified mechanic, or the worked instance's exact file/quote) + the failure mode it prevents**.
   A claim without the failure mode it exists to prevent is half an answer — every pattern here
   exists because of a specific, real observability gap, and the gap is the point.
3. **Distinguish "this is how the harness currently behaves" (a platform fact, verify against
   current tool/hook docs if this pack has aged) from "this is a real, dated measurement this
   workspace happened to produce" (a worked instance — proof the discipline works, not a mandate
   that every project must reproduce these exact numbers or tool names).**
4. Route output work at the boundary (see below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask (an actual logging pipeline, eval runner, or notification integration) is routed to the
consumer's own build seat. **NOT done** while a claim ships without the failure mode it prevents,
or a single dated measurement/tool name is presented as a universal requirement rather than one
real instance of the underlying discipline.

## The core invariants (why these patterns exist)

- **A transcript proves what was said; only a structured signal proves what happened.** A chat
  harness that only offers "read back the conversation" as its observability story cannot answer
  "did the enforcement mechanism actually fire" without re-interpreting prose — a hook bound to a
  matcher, firing deterministically on a real event class, answers that in one line, every time.
- **Routing accuracy is a number tracked over repeated runs, not an impression formed from
  whichever prompts happened to come up.** A felt sense that "the skill seems to trigger fine"
  cannot distinguish a one-off judge flip from a real regression from a structural leak that will
  recur every time — only a held-out suite, re-run and compared, can.
- **The measurer of routing accuracy must see no more than the real router sees.** A judge that can
  read a skill's full body, its suite's expected answers, or other skills' internals is answering
  an easier question than the one that actually determines routing — a router decides from
  descriptions alone, sight-unseen, and a contaminated judge's score stops predicting real routing
  behavior.
- **If the harness dispatched the work, the harness will announce it; do not poll for what you
  will be told anyway.** Polling for something the harness already tracks wastes effort and risks
  racing the real completion signal; conversely, assuming a genuinely external system (a CI run, a
  deploy) will announce itself the way harness-tracked work does produces a silent, indefinite
  wait, because nothing external is wired to notify anyone — the two cases need opposite habits.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Compose or orchestrate the agents that DO the work being observed** (a build team, a
  multi-agent workflow) → [[chat-harness-workflow-facts]] (the sibling pack in this
  plugin — a related but distinct concern from measuring or logging what that composed work did).
- **The routing MECHANISM itself** — how a skill actually gets selected at discovery time, as
  opposed to how its accuracy is measured after the fact → [[chat-harness-routing-facts]] (the
  sibling pack in this plugin).
- **The rule a hook ENFORCES** (blocking or transforming a tool call before it runs) →
  [[chat-harness-guardrail-facts]] (the sibling pack in this plugin) — this pack only
  covers the SAME hook mechanism used the other way: as an observation/logging point, never as the
  enforcement rule itself.
- **Build or fix an actual logging pipeline, eval harness, or notification integration in YOUR
  project** → your project's own build seat/agent (this pack has none — it teaches the discipline,
  it does not own any codebase's source).

## Extending this pack

A missing axis, a stale citation (a cited hook, tool, or eval-run number that no longer matches
current reality), or a second worked instance from a different workspace proving the discipline
generalizes — route to `pack-forge` (axis decomposition, grounded research waves, index
discipline), where installed; otherwise apply its discipline inline: one reference per distinct
class of ask, every claim grounded, never an uncited file bolted on.
