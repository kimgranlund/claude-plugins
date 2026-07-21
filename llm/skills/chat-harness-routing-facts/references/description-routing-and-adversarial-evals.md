# Routing a request to the right skill/tool/subagent, and testing it adversarially

> Axis: once several skills (or tools, or subagents) exist side by side, how a single request
> finds the correct one, and how that routing is measured rather than assumed. Grounded in
> `harness:skill-writing-rules`'s description-engineering rule (a platform-facing mechanism)
> plus this workspace's own routing-corpus + evals convention — a real, directly-inspectable
> worked instance of the discipline, not a hypothetical.

## The routing mechanism

**Platform fact — the description is matched against the user's own words, not the skill's
content.** `skill-writing-rules/SKILL.md:63` states this as the core rule: "The description
is matched against *the user's words*, not the skill's content... slightly pushy — the documented
bias is under-triggering, not over-triggering." The same source's worked example at `SKILL.md:65-74`
contrasts a description that is a mere label ("Database migration helper" — "never fires") against
one written as a trigger contract (what it does + the verbatim phrasings a user actually types,
front-loaded).

**The identical shape governs subagent routing, not only skills.** **Worked instance, observed
directly in this session's own environment:** the subagent registry this session was given
carries entries such as `a2ui-composer` and `a2ui-builder`, whose descriptions each end with the
exact `NOT for <thing> (<owner>)` fence `skill-writing-rules/SKILL.md:63` names as "a
repellent the router and measurement tooling can both key on" — the same repellent convention,
applied to routing BETWEEN subagents instead of between skills. A request that could plausibly go
to more than one seat is exactly where this fence earns its keep.

## Adversarial negatives — draw them from the dangerous near-neighbor, not a random distractor

**Claim — a routing test proves nothing if its negatives are trivially distinguishable; the
negatives that matter are the ones a naive router could actually confuse with a true positive.**
**Worked instance:** this very plugin's sibling pack, `llm-gateway-facts`, states its own
negative-selection rule verbatim in `scripts/routing-corpus.json`'s `_note` field: "Negatives
drawn adversarially from the dangerous near-neighbors: `llm-streaming-facts` (the sibling pack —
SSE/JSONL wire-format concerns, a DIFFERENT layer), the `agent-protocols` plugin's
`a2ui-chat-agent-facts`... and `a2ui-protocol-facts`..., plus a genuine build/implement ask (this
pack answers, it does not build)." Three distinct kinds of adversarial negative are visible in
that one line, worth naming separately: a **sibling in the same plugin** covering a related but
distinct layer, a **cross-plugin pack** covering the same underlying system from a different
angle, and a **genuine action ask** this skill species must never claim (an ANSWERS-only pack
routing away from anything that sounds like "build" or "implement").

**Failure mode this discipline prevents:** a routing corpus built only from obviously-unrelated
negatives ("how do I bake bread") never exercises the actual failure mode a router experiences in
production — losing a prompt to the ONE other skill that shares real vocabulary with it. A corpus
this pack's own `scripts/routing-corpus.json` follows the identical pattern: negatives drawn from
the parallel sibling packs on instruction-layering and multi-agent orchestration, plus a genuine
build/implement ask, since those are this pack's own dangerous near-neighbors.

## The corpus is a schema in two forms, one content

**Worked instance:** `llm-gateway-facts/scripts/routing-corpus.json` carries `{skill, _note,
positives: [...], negatives: [...]}` — flat prompt-string arrays; the same pack's
`evals/evals.json` carries `{skill, note, cases: [{id, prompt, expect: "trigger"|"no-trigger"}]}`
— the SAME sixteen positives and twelve negatives, re-keyed with per-case IDs so an eval run can
report which specific case regressed. Neither file invents content the other lacks; the two
schemas exist because `scripts/` (a plain corpus a human or a script can scan) and `evals/` (a
structured suite `eval_check.py` and `/check-routing` can execute) serve different consumers of the
identical test set.

## Measure, and re-measure — a corpus is not proof until it has been run

**Claim — writing the corpus is necessary but not sufficient; the discipline is running it, and
running it again after any description edit anywhere in the menu, since an edit to an unrelated
skill can silently change what a request now matches.** **Worked instance, the clearest one in
this workspace:** the `agent-protocols` plugin's `a2ui-chat-agent-facts/evals/evals.json` `note`
field carries a real, dated measurement history, not a write-once assumption: "Blind run
2026-07-09: 33/36 — t14 (validate-then-stream) stolen by a2ui-protocol-facts: the term added verbatim
to this description; t03/t04... chose none DESPITE the phrasing standing verbatim in the
description — judge noise, recorded as first strike, watch for a second." A second, later entry
in the SAME field: "Estate-wide run 2026-07-09: 33/36 — t03/t04 came home (judge-noise cleared)
and t14... proven; n12/n13/n14... leaked to this pack in the estate field — structural: agents are
absent from any skill menu, and this pack's Boundaries perform the handoff, so the two-hop route
is by design." **What this proves, concretely:** a case can regress for reasons that are NOT a bug
in the skill under test — a sibling's description absorbing shared vocabulary, or a structural gap
(no subagent appears in a skill menu, so a two-hop route is sometimes correct, not a defect) — and
the only way to tell the difference is a dated, re-run record, not a first-draft assumption that
the corpus "should" pass.

## Baseline comparison — the check that proves the skill, not just the router

**Platform fact:** `skill-writing-rules/SKILL.md:115` names the check as "a baseline
comparison: a few realistic prompts, each run in a fresh session with the skill available and
again with it disabled (`skillOverrides: "off"`), comparing trigger reliability and output quality
separately — a skill triggering proves Claude found it, not that it worked." A routing corpus
alone answers only "did the router pick the right skill"; a baseline comparison additionally
answers "did having the skill loaded actually change the output" — a distinct question a routing
corpus cannot answer by itself.

## What this file does NOT cover

Deciding whether a capability should be a skill at all before it has a description to route
against — see authoring-a-skill-vs-a-hardcoded-feature. Choosing the invocation species (and
therefore whether a description reaches the model's router at all, as with a Command skill's
menu-only description) — see invocation-species-model-vs-user-invoked. Composing several
skills/subagents into a multi-step workflow once each individual one routes correctly
([[chat-harness-workflow-facts]]).
