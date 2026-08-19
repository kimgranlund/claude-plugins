---
name: chat-harness-routing-facts
description: >-
  How a chat-agent harness exposes capabilities as load-on-demand skills vs. an always-on cost,
  and how a request finds the right one. Use for skill-vs-hardcode, model- vs user-invoked
  (auto-trigger vs slash-only, user-invocable), what disable-model-invocation does incl. its
  preload interaction, a skill that won't trigger, wrong skill firing, and how to AUTHOR/WRITE a
  NEW held-out adversarial eval corpus so a description actually routes. Grounded in Claude
  Code's mechanics. ANSWERS; does not build. NOT for guardrails (chat-harness-guardrail-facts);
  NOT for multi-agent composition (chat-harness-workflow-facts); NOT for a tool catalog's loading
  (chat-harness-tool-facts); NOT for RE-RUNNING an existing suite's accuracy over repeated real
  runs / judge-noise-vs-regression triage (chat-harness-logging-facts).
disable-model-invocation: false
user-invocable: false
---

# chat-harness-routing-facts — discoverable capabilities and how requests find them

Answers how a chat-agent harness should expose a capability — as a discoverable, load-on-demand
"skill" the model or the user can reach on demand, versus hardcoding it into the harness's own
standing instructions or always-loaded tool surface — and, once something IS a skill, how a
request actually finds the right one. Three axes, one underlying shape (load only what THIS turn
needs, not everything the harness COULD do): **should this be a skill at all** (vs hardcoded),
**which invocation species** (model-invoked, user-invoked, or both), and **how does a request get
routed there, tested against confusable neighbors, and re-measured over time** rather than trusted
on a first draft. Grounded in Claude Code's own skill-loading mechanics (a platform mechanism,
verify against current docs if stale-sensitive) and a real, inspectable worked instance — this
very workspace's own routing-corpus + evals discipline — cited as proof the pattern works, not as
the only valid implementation.

| Ask | Load |
|---|---|
| Skill vs hardcoded feature — "should this be a skill", "why hardcode this instead", "load-on-demand capability" | `references/authoring-a-skill-vs-a-hardcoded-feature.md` |
| Model-invoked vs user-invoked — "should this auto-trigger or need a slash command", "disable-model-invocation", "user-invocable", "preload this into a subagent" | `references/invocation-species-model-vs-user-invoked.md` |
| Routing + adversarial evals — "why did the wrong skill fire", "write a routing corpus", "test skill triggering", "build a held-out adversarial eval suite" | `references/description-routing-and-adversarial-evals.md` |
| Envelope framing / out-of-band signals — "a note vs. a trace vs. content on the same stream", "how do I tell a meta-line from a protocol message", "one bad field shouldn't break the whole envelope" | `references/envelope-framing-and-out-of-band-signals.md` |
| Multi-producer id namespacing — "two producers writing to the same session collide on ids" | `references/multi-producer-namespacing.md` |
| Model-declared routing facts — "the model said route to X but X doesn't exist, now what" | `references/model-declared-routing-integrity-check.md` |
| Client-side auto-attach — "the assistant told the user to tag something it just offered" | `references/client-side-label-auto-attach.md` |
| Provenance — platform mechanic vs this workspace's own convention | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`disable-model-invocation`, `user-invocable`, `routing-corpus`, `adversarial`, …) and Read that
   section — the files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (a platform mechanic, or the
   worked instance's exact `file:line`) + the failure mode it prevents**. A routing or
   invocation-species claim without the failure mode it exists to prevent is half an answer — every
   rule here exists because something goes silently wrong without it (a skill that never fires, a
   context budget taxed forever, a router stealing the wrong neighbor's prompt).
3. **Distinguish "this is how Claude Code's own mechanism behaves" (a platform fact, verify against
   current docs — it is explicitly marked drift-prone in its own source) from "this is how the
   nonoun-plugins workspace chose to structure and test its routing corpora" (a worked convention —
   a consumer's own harness may reasonably differ in schema, as long as the underlying discipline
   — measured, adversarial, re-run over time — still holds).**
4. Route output work at the boundary (see below) — this pack answers; it does not build.

## The core invariants (why these patterns exist)

- **Everything loaded into every turn's context is a standing tax, paid whether or not it's used**
  — a capability baked into the harness's base instructions or always-loaded tool list costs the
  same whether the current request needs it or not; a skill's `description` line is a much smaller
  standing cost, and its full body loads only on the turns that actually need it.
- **A skill's trigger is a match against the user's words, not a guarantee** — model-invocation is
  probabilistic: it depends on the router matching the CURRENT description menu against THIS turn's
  actual phrasing. A behavior that must hold on every single turn regardless of phrasing (a hard
  safety invariant, "never do X") belongs in a standing instruction or a hook, not a skill that
  might simply not get picked that turn.
- **The two invocation dials tell the same story as the content species** — a workflow-with-a-
  contract, a knowledge catalog, and a side-effecting command are different content shapes, and
  each has exactly one coherent invocation-dial setting; setting dials that contradict the content
  (a knowledge catalog left `user-invocable: true`, a command left model-invocable) is a routing
  bug waiting to surface, not a stylistic choice.
- **A routing claim without a measured, adversarial test is a guess dressed as a fact** — "the
  description covers it" is unverified until it's run against near-neighbor prompts designed
  specifically to steal the match, and re-run again later, because a description edit anywhere in
  the menu can silently change what a completely unrelated skill wins.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Author, structure, or lint an actual SKILL.md to a repo's standard** (frontmatter shape, body
  budgets, species templates) → `skill-writing-rules`, where installed (this pack teaches the
  decision of skill-vs-hardcode and model-vs-user-invoked; that skill teaches the file itself).
- **Layer standing instructions and enforced guardrails across a whole harness** (CLAUDE.md
  structure, hooks, what belongs where) → [[chat-harness-guardrail-facts]] (the sibling
  pack in this plugin family).
- **Compose multiple skills, tools, or subagents into a multi-step workflow** (orchestration,
  hand-offs, review gates between seats) → [[chat-harness-workflow-facts]] (the
  sibling pack in this plugin family) — this pack's routing axis stops at "which ONE skill/tool/
  subagent answers this single request," not how several compose across steps.
- **Deferring a large TOOL catalog's own schema-loading** (the analogous "load on demand" shape,
  a different mechanism than a skill's own model-invoked routing) → [[chat-harness-tool-facts]]
  (the sibling pack in this plugin family).
- **Persisting a fact or preference across sessions** (memory, not routing a live request to a
  capability) → [[chat-harness-memory-facts]] (the sibling pack in this plugin family).
- **Measuring routing accuracy AFTER the fact, over repeated real runs** (as opposed to the
  routing mechanism itself) → [[chat-harness-logging-facts]] (the sibling pack in this plugin
  family) — this pack teaches how to WRITE an adversarial eval corpus; that pack teaches how to
  track its results over time and distinguish a real regression from judge noise.
- **Build the routing logic, the SKILL.md, or the eval harness itself in YOUR project** → your
  project's own build seat/agent (this pack has none — it teaches the pattern, it does not own any
  codebase's source).

## Extending this pack

Extension: governed by [[make-pack]]
