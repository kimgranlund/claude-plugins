---
name: chat-harness-instructions-and-guardrails
description: >-
  The instruction-layering, safety, and config layer of a mini/portable chat agent harness —
  project-agnostic. Use for "layer global/project/session instructions so the more specific
  wins", "keep tool/file/web output from being treated as a command" (injection defense),
  "classify an action by reversibility and gate risky ones behind confirmation", "enforce a rule
  with a hook, not prose", "settings.json or the system prompt — which wins", "bootstrap a
  harness reproducibly", "one shared config schema or scattered params", "an option list drifted
  from the real registry it should derive from". Covers instruction layering, the
  instruction-source boundary, action risk tiers, hooks vs prose, config precedence, and
  structuring the config/prompt layer (a shared typed schema, registry-projected option lists,
  prompt prose in files, byte-identity on refactor). Grounded in Claude Code's own harness + nonoun-plugins, cited as
  worked examples. ANSWERS from a cited corpus; does not build. NOT skill authoring/routing
  (chat-harness-skills-and-routing); NOT the provider trust boundary (llm-provider-gateway).
disable-model-invocation: false
user-invocable: false
---

# chat-harness-instructions-and-guardrails — the foundational layer of a chat agent harness

Answers how to lay the instruction, safety, and configuration foundation of a small, real,
deployable chat agent harness — not necessarily an enterprise platform. Every claim is framed
through what's load-bearing at small scale versus what's extra complexity earned only at larger
scale, and grounded either in a real, directly-verified worked system (this repo's own currently
loaded CLAUDE.md/settings/hooks stack, and the `nonoun-plugins` workspace's own conventions) or in
a general platform fact — cited so a claim can be checked against a real, running instance, never
presented as the only valid way to build this layer.

| Ask | Load |
|---|---|
| Global/project/session precedence — "which instruction wins", "does a project rule need to repeat the global one" | `references/instruction-layering-and-precedence.md` |
| The instruction-source boundary — "is this file's text a command", "prompt-injection defense", "a tool's output claims I already approved this" | `references/injection-defense-and-instruction-source-boundary.md` |
| Action risk tiers — "should this action ask first", "what needs to just be refused outright", "reversibility and blast radius" | `references/action-risk-tiers-and-confirmation-gates.md` |
| Hook vs. prose — "enforce this rule so it can't be skipped", "why did the model ignore an instruction that was right there", "does this belong in a hook or a skill" | `references/deterministic-rules-vs-prompted-guidance.md` |
| Config precedence + setup — "settings.json vs. the system prompt", "which settings scope wins", "install or bootstrap this reproducibly" | `references/config-precedence-and-setup.md` |
| Structuring the config/prompt layer itself — "one shared config schema or scattered params", "hardcoding my system prompt as a string feels wrong", "hoist a config type across a package boundary", "the model list drifted from the real registry" | `references/config-schema-and-prompt-externalization.md` |
| Provenance — verified `file:line` vs. observed harness behavior vs. platform fact | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`CLAUDE.md`, `PreToolUse`, `settings.local.json`, `Prohibited`, `plugin install`, …) and Read
   that section — the files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (a verified `file:line`, an
   observed-harness-behavior citation, or a platform fact) + the failure mode it prevents**. A
   guardrail claim without the failure mode it exists to prevent is half an answer.
3. **Distinguish the three trust classes** (see `references/sources.md`): a fact this pack
   verified itself by opening a real file at a real path, a real harness's stated rule reported at
   dispatch time rather than independently re-opened, and a general platform/security fact. Do not
   present the second as if it carries the first's verification weight.
4. **Frame every claim at its right scale** — name explicitly when a full worked-instance pattern
   is enterprise-scale complexity a mini/portable harness can validly skip, versus when it's
   load-bearing the instant the harness can take any action at all (most of this pack's guardrail
   content is the latter).

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask is routed to the consumer's own harness codebase (this pack has none — it is
project-agnostic). **NOT done** while a claim ships without its failure mode, or a worked
example's specific detail is presented as a universal requirement rather than one valid instance.

## The core invariants (why these patterns exist)

- **A layer conflict is resolved by specificity for routine content, never for a safety floor** —
  global < project < session governs style, workflow, and process; a genuine guardrail sits
  outside that stack so a cleverly-scoped session request can't out-rank it by appearing more
  specific (instruction-layering-and-precedence).
- **Only one channel is a valid instruction source; everything else observed through a tool is
  data** — an agent that treats a fetched page's or a file's text as a candidate command is
  trivially steered by whoever controls that text
  (injection-defense-and-instruction-source-boundary).
- **Not all risky actions are risky the same way** — collapsing "ask first" and "never do this"
  into one bucket either makes the agent annoying or lets a catastrophic action through unchecked
  (action-risk-tiers-and-confirmation-gates).
- **A rule that must never be talked past belongs in code that runs outside the model's context,
  not in prose the model merely reads** — prompted guidance is missed on a real, measured fraction
  of turns; a hook is not (deterministic-rules-vs-prompted-guidance).
- **Structured settings compose by scope; scalars override, hooks merge additively — the two
  rules are not interchangeable** (config-precedence-and-setup).
- **A config schema shared by more than one consumer belongs at the lowest layer both can reach —
  not duplicated per consumer, not stranded in whichever one defined it first**
  (config-schema-and-prompt-externalization).
- **Hand-authored prompt prose belongs in files, not code constants — and a load-bearing
  derivation over the original text must survive the move exactly, verified against a real
  before-the-move baseline, never re-derived by concatenating pre-split fragments**
  (config-schema-and-prompt-externalization).

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build or fix a harness's actual CLAUDE.md, hook, or settings.json in YOUR project** → your
  project's own build seat/agent (this pack teaches the pattern, it owns no codebase's source).
- **How a SKILL.md's own `description` drives model routing, or skill authoring/species/frontmatter
  in general** → [[chat-harness-skills-and-routing]] (the sibling pack in this plugin family) — a
  distinct concern from instruction layering or guardrails.
- **The provider/secret trust-boundary pattern** (registry validation, dev-proxy, adapter
  injection) → [[llm-provider-gateway]] (the sibling pack in this plugin) — a narrower, different
  concern than this pack's general instruction-layering/guardrail scope.

## Extending this pack

A missing axis, a stale worked-example citation (either worked system's file moved or its content
changed), or a second independently-observed harness proving one of these patterns generalizes
further — route to `knowledge-forge` (axis decomposition, grounded research waves, index
discipline), where installed; otherwise apply its discipline inline: one reference per distinct
class of ask, every claim grounded, never an uncited file bolted on.
