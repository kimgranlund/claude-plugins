# llm — portable LLM-integration and chat-agent-harness knowledge

Eight knowledge packs teaching general, project-agnostic technique — never one repo's
implementation. Two families: **the LLM-integration two** answer HOW to call a model safely and
stream its output correctly, distilled FROM `@agent-ui/a2ui`'s live-agent system (a real, shipped,
tested instance); **the chat-harness six** answer how to construct a mini/portable chat-agent
harness AROUND that call — instructions/guardrails, skills/routing, orchestration/workflows,
knowledge/memory, tools/resources/services, observability — distilled from Claude Code's own
live, current harness plus this very workspace's own conventions. Every claim in both families is
grounded either in a platform/vendor/harness fact (verify against current docs if stale-sensitive)
or cited to a real worked instance as proof-of-concept, never as the only valid implementation.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/llm-provider-gateway` | Knowledge pack | model-only | The swappable multi-provider gateway pattern: one adapter interface per vendor (secrets injected via factory, never module-scope), a registry as the single source of truth for both a picker UI and a server-side allowlist, the `resolvePair` trust-boundary check, the dev-only proxy pattern (server-side key custody), the bundler env-inlining footgun (Vite's `VITE_*` and its analogues), and the stateless-proxy + client-held-session + pure-turn-reducer conversation model |
| `skills/llm-jsonl-streaming` | Knowledge pack | model-only | Streaming structured output safely: the general SSE chunk-buffering technique (partial-frame handling across `fetch` reads, blank-line event framing per spec), Anthropic's Messages API SSE contract as a fully worked instance, an error-sentinel technique for async generators, and validate-then-stream (never emit invalid output, bounded self-correct rounds feeding structured failures back to the model, halt-and-report on exhaustion) |
| `skills/chat-harness-instructions-and-guardrails` | Knowledge pack | model-only | Layering instructions (global < project < session precedence, a safety-floor exception), the closed instruction-source boundary (tool/file/web output is DATA never a command — prompt-injection defense), action risk tiers + confirmation gates, deterministic rule enforcement (hooks/lint) vs. prompted guidance, config precedence, and reproducible setup/install |
| `skills/chat-harness-skills-and-routing` | Knowledge pack | model-only | Authoring a capability as a describe-to-route, load-on-demand skill vs. a hardcoded feature; the model-invoked vs. user-invoked species dial; description-based routing measured against a held-out adversarial eval corpus, not a felt sense |
| `skills/chat-harness-orchestration-and-workflows` | Knowledge pack | model-only | Decomposing a large task across multiple specialized agents with a clear chain of command (coordinator/planner/builder/reviewer, generator≠critic); verifiable typed hand-off contracts; deterministic scripted pipelines (fan-out/fan-in) as a distinct alternative to ad hoc dispatch |
| `skills/chat-harness-knowledge-and-memory` | Knowledge pack | model-only | Authoring a knowledge base as a cited, retrieval-by-search corpus (never prose dumped wholesale into context); durable cross-session memory (typed, with a hard exclusion list and a verify-before-trusting caveat) distinct from ephemeral within-conversation task state |
| `skills/chat-harness-tools-resources-and-services` | Knowledge pack | model-only | The tool/skill/resource three-way distinction; typed tool schemas; deferring a large tool catalog's loading until needed (search-to-load); read-only resources; routing the external-service-integration axis to `llm-provider-gateway` rather than duplicating it |
| `skills/chat-harness-observability` | Knowledge pack | model-only | Hook-based logging/tracing distinguishable from user input; measuring routing/skill accuracy against a held-out adversarial suite over repeated runs (judge-noise vs. a real regression vs. a structural leak); background-task notification vs. polling, and the distinct case of polling genuinely external state |

All eight packs are `user-invocable: false` — model-only, routed by description. Each carries a
`scripts/routing-corpus.json` (positives/negatives, adversarial near-neighbors named explicitly)
and an `evals/evals.json` (this workspace's `eval_check.py` schema, converted 1:1 from the same
cases) so both the legacy and forge-native eval tooling can regress the same suite.

## Two families, two decompositions

The LLM-integration two came from the user's own framing — "Anthropic LLM gateways and JSONL"
names two genuinely distinct concerns (who you're allowed to call and how the secret stays safe,
versus how you correctly consume what comes back) — confirmed by a `system-decompose` pass
(technical-architecture domain, `coverage_check.py` clean: 7 leaf reference files, 11 actions,
zero unhosted, zero unjustified) before either was authored.

The chat-harness six came from a SECOND, larger `system-decompose` pass over "everything learned
about mini/portable chat-agent harnesses" — 6 nodes, 21 actions, 21 hosts, zero unhosted, zero
unjustified. The six cluster along a genuine structural seam (what governs behavior, what the
agent can invoke, how multiple agents compose, what it remembers, what it can reach outside its
own context window, and how its behavior is measured) — not an arbitrary split of the user's own
named list. `chat-harness-tools-resources-and-services` deliberately routes its
external-service-integration axis to `llm-provider-gateway` rather than re-deriving it, so the two
families interlock instead of duplicating.

## Cross-plugin seam

Neither LLM-integration pack owns `@agent-ui/a2ui`'s OWN shipped system as a repo-specific answer —
that's the `agentic-ui` plugin's `a2ui-conversational-agent` pack (dated, `file:line`-cited against
a single snapshot). `agentic-ui`'s `a2ui-conversational-agent` also carries a THIRD reference,
`anthropic-sse-wire-contract.md`, documenting the same Anthropic contract as THAT repo's own dated
answer — the two packs describe the same underlying facts from two different postures (portable
pattern vs. this-repo's-current-state) and should stay consistent, not merge. The chat-harness six
similarly do not own Claude Code's own docs as a versioned reference — they teach the pattern,
citing this session's own observed, current mechanics and flagging where a tool name may drift
across harness versions (the portable claim is the two-mechanism SHAPE, not one exact tool name).

v0.2.1 · assembled 2026-07-14 · 0.2.1: displayName 'LLM' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.2.0 · assembled 2026-07-13 · the chat-harness six added: a second `system-decompose` pass (6
nodes/21 actions, `coverage_check.py` clean) built into 6 parallel-authored knowledge packs
covering the mini/portable chat-agent-harness construction layer, folded into this plugin rather
than a new one (a chat harness is built ON TOP OF the LLM-integration layer this plugin already
taught). Grounded in Claude Code's own live, current harness mechanics (the instruction-source
boundary, the three-tier action-risk model, hooks, `ToolSearch` deferred-tool loading,
background-task notification, the four-type auto-memory system) plus this workspace's own
conventions (routing-corpus/evals discipline, `handoff-compose`, the `orchestration` plugin's
agent roster, `knowledge-forge`, a real dated eval-run history). One authoring convention error
caught and fixed across the batch: `[[double-bracket]]` handles are for cross-SKILL links only —
a same-skill sibling reference file is named in plain, unbracketed prose. `release_gate.py`: clean.
· 0.1.0 · assembled 2026-07-13 · initial: distilled from `@agent-ui/a2ui`'s live-agent system
(`packages/agent-ui/a2ui/tools/agent/`) via a `system-decompose` pass (technical-architecture
domain, `coverage_check.py` clean) into two skills, generalized as portable technique rather than
ported as a repo-specific answer pack.
