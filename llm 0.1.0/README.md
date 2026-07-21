# llm — portable LLM-integration and chat-agent-harness knowledge

Nine knowledge packs teaching general, project-agnostic technique — never one repo's
implementation. Two families plus one cross-cutting taxonomy: **the LLM-integration two** answer
HOW to call a model safely and stream its output correctly, distilled FROM `@agent-ui/a2ui`'s
live-agent system (a real, shipped, tested instance); **the chat-harness six** answer how to
construct a mini/portable chat-agent harness AROUND that call — instructions/guardrails,
skills/routing, orchestration/workflows, knowledge/memory, tools/resources/services,
observability — distilled from Claude Code's own live, current harness plus this very workspace's
own conventions; **`agent-residency-facts`** sits above both families, classifying which of the
two the finding at hand actually belongs to (a CLI-harness Resident Agent vs. a hosted-chatbot
Ephemeral Agent) before a claim from one gets written into the other's corpus. Every claim in all
three groups is grounded either in a platform/vendor/harness fact (verify against current docs if
stale-sensitive) or cited to a real worked instance as proof-of-concept, never as the only valid
implementation.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/llm-gateway-facts` | Knowledge pack | model-only | The swappable multi-provider gateway pattern: one adapter interface per vendor (secrets injected via factory, never module-scope), a registry as the single source of truth for both a picker UI and a server-side allowlist, the `resolvePair` trust-boundary check, the dev-only proxy pattern (server-side key custody), the bundler env-inlining footgun (Vite's `VITE_*` and its analogues), and the stateless-proxy + client-held-session + pure-turn-reducer conversation model |
| `skills/llm-streaming-facts` | Knowledge pack | model-only | Streaming structured output safely: the general SSE chunk-buffering technique (partial-frame handling across `fetch` reads, blank-line event framing per spec), Anthropic's Messages API SSE contract as a fully worked instance, an error-sentinel technique for async generators, and validate-then-stream (never emit invalid output, bounded self-correct rounds feeding structured failures back to the model, halt-and-report on exhaustion) |
| `skills/chat-harness-guardrail-facts` | Knowledge pack | model-only | Layering instructions (global < project < session precedence, a safety-floor exception), the closed instruction-source boundary (tool/file/web output is DATA never a command — prompt-injection defense), action risk tiers + confirmation gates, deterministic rule enforcement (hooks/lint) vs. prompted guidance, config precedence, and reproducible setup/install |
| `skills/chat-harness-routing-facts` | Knowledge pack | model-only | Authoring a capability as a describe-to-route, load-on-demand skill vs. a hardcoded feature; the model-invoked vs. user-invoked species dial; description-based routing measured against a held-out adversarial eval corpus, not a felt sense |
| `skills/chat-harness-workflow-facts` | Knowledge pack | model-only | Decomposing a large task across multiple specialized agents with a clear chain of command (coordinator/planner/builder/reviewer, generator≠critic); verifiable typed hand-off contracts; deterministic scripted pipelines (fan-out/fan-in) as a distinct alternative to ad hoc dispatch |
| `skills/chat-harness-memory-facts` | Knowledge pack | model-only | Authoring a knowledge base as a cited, retrieval-by-search corpus (never prose dumped wholesale into context); durable cross-session memory (typed, with a hard exclusion list and a verify-before-trusting caveat) distinct from ephemeral within-conversation task state |
| `skills/chat-harness-tool-facts` | Knowledge pack | model-only | The tool/skill/resource three-way distinction; typed tool schemas; deferring a large tool catalog's loading until needed (search-to-load); read-only resources; routing the external-service-integration axis to `llm-gateway-facts` rather than duplicating it |
| `skills/chat-harness-logging-facts` | Knowledge pack | model-only | Hook-based logging/tracing distinguishable from user input; measuring routing/skill accuracy against a held-out adversarial suite over repeated runs (judge-noise vs. a real regression vs. a structural leak); background-task notification vs. polling, and the distinct case of polling genuinely external state |
| `skills/agent-residency-facts` | Knowledge pack | model-only | Classifies a conversational agent as a Resident Agent (a CLI harness — persistent filesystem/git/shell host) or an Ephemeral Agent (a hosted chatbot — per-conversation sandbox, function-calling tool surface) across five axes (host/persistence, context assembly, tool use, orchestration/concurrency, trust boundary); routes to which existing pack owns each tier's actual guidance, and names the check to run before writing a cross-tier finding into either |

All nine packs are `user-invocable: false` — model-only, routed by description. Each carries a
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
named list. `chat-harness-tool-facts` deliberately routes its
external-service-integration axis to `llm-gateway-facts` rather than re-deriving it, so the two
families interlock instead of duplicating.

## Cross-plugin seam

Neither LLM-integration pack owns `@agent-ui/a2ui`'s OWN shipped system as a repo-specific answer —
that's the `agent-protocols` plugin's `a2ui-chat-agent-facts` pack (dated, `file:line`-cited against
a single snapshot). `agent-protocols`'s `a2ui-chat-agent-facts` also carries a THIRD reference,
`anthropic-sse-wire-contract.md`, documenting the same Anthropic contract as THAT repo's own dated
answer — the two packs describe the same underlying facts from two different postures (portable
pattern vs. this-repo's-current-state) and should stay consistent, not merge. The chat-harness six
similarly do not own Claude Code's own docs as a versioned reference — they teach the pattern,
citing this session's own observed, current mechanics and flagging where a tool name may drift
across harness versions (the portable claim is the two-mechanism SHAPE, not one exact tool name).

## ADR-0006 transition table (renamed 2026-07-21)

Old handles remain greppable only in ledgers, CHANGELOGs, ADRs, and attics.

| Old name | New name |
|---|---|
| `agent-residency-taxonomy` | `agent-residency-facts` |
| `chat-harness-instructions-and-guardrails` | `chat-harness-guardrail-facts` |
| `chat-harness-knowledge-and-memory` | `chat-harness-memory-facts` |
| `chat-harness-observability` | `chat-harness-logging-facts` |
| `chat-harness-orchestration-and-workflows` | `chat-harness-workflow-facts` |
| `chat-harness-skills-and-routing` | `chat-harness-routing-facts` |
| `chat-harness-tools-resources-and-services` | `chat-harness-tool-facts` |
| `llm-jsonl-streaming` | `llm-streaming-facts` |
| `llm-provider-gateway` | `llm-gateway-facts` |

v1.0.3 · assembled 2026-07-21 · 1.0.3: ADR-0006 docs-rename sweep — live references rewritten; pointer updates only · v1.0.2 · assembled 2026-07-21 · 1.0.2: ADR-0006 teamwork-rename sweep — live references rewritten (chat-harness-workflow-facts' team-lead citations, agent-residency-facts' teamwork:parallel-work-rules pointers); pointer updates only · v1.0.1 · assembled 2026-07-21 · 1.0.1: ADR-0006 agent-protocols-rename sweep — live references to agentic-ui's old plugin/member handles rewritten (streaming/gateway fences); pointer updates only · v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0006 rename PR 3/9 — all nine members take the simple paradigm's -facts shape (transition table above); the plugin name keeps `llm` under ADR-0006 Decision 7's term-of-art shelf exception. MAJOR bump — breaking. Workspace sweep (52 files, ledger history excluded); 282-case pre-rename baseline captured, post-rename re-measure in the campaign PR · v0.5.0 · assembled 2026-07-20 · 0.5.0: `skills/agent-residency-taxonomy` added — a ninth, cross-cutting pack classifying a conversational agent as a Resident Agent (CLI harness) or an Ephemeral Agent (hosted chatbot) across five axes, routing to which existing pack owns each tier's guidance and naming the check to run before writing a cross-tier finding into either. Grounded in a real 2026-07-20 incident (CLI-harness dispatch findings written into chat-harness-instructions-and-guardrails as if they were hosted-chat-agent facts, caught and reverted mid-task) plus a baseline test showing the underlying reasoning already exists in the abstract — the pack's value is a named, cheap-to-invoke checkpoint under real dispatch load, stated honestly rather than as a missing-fact claim. Reciprocal fence landed both directions with chat-harness-instructions-and-guardrails (Boundaries section + evals n13). skill_lint.py + potency_lint.py clean; skill-auditor FLOOR review PASS. release_gate.py: clean · v0.4.1 · assembled 2026-07-19 · 0.4.1: knowledge-pack factory-route convention repointed from scribe's retired `knowledge-forge` to forge's `pack-forge` (workspace-wide rename campaign) — every chat-harness-* skill's reference to its authoring factory updated; no functional/behavior change, a naming correction only. · v0.4.0 · assembled 2026-07-17 · 0.4.0: chat-harness-instructions-and-guardrails gains a seventh axis — references/multi-turn-validation-and-state-seeded-gates.md (a per-payload validator in a multi-turn loop must judge the state the consumer will hold; the two-contradictory-gates deadlock; persistent model "misbehavior" is a harness question first; catch cross-payload violations producer-side as a self-correct round), grounded in agent-ui TKT-0081 as a directly verified worked instance (validateA2ui sessionSeed, file:line at commit c8aee65); description + consult table + invariants route it; corpus +3 positives (plus 3 config-schema positives the 0.3.0 axis never got), evals t22–t24; the ADR-0137 tools/agent→src/agent move re-verified across sources.md and config-schema-and-prompt-externalization.md (one missed line-number pair fixed after an independent skill-audit flagged it). release_gate.py: clean · v0.3.2 · assembled 2026-07-16 · 0.3.2: chat-harness-instructions-and-guardrails and chat-harness-observability descriptions re-budgeted under the 1024 cap (the 0.3.1 eval tunings had pushed both over) — triggers preserved; instructions' generic does-not-build fence replaced by a NAMED-artifact fence after the post-trim judge leaked three build asks (the #8 lesson: name the artifacts) — re-judge 33/33; observability 31/31 · v0.3.1 · assembled 2026-07-15 · 0.3.1: /eval-run tuning (254/258 → 258/258 on the re-judged suites): chat-harness-instructions-and-guardrails gains the registry-drift trigger phrase (t20 was dead — the registry-projection claim lived only in the reference body); chat-harness-observability's does-not-build fence strengthened after three build-ask leaks (n07/n08/n09), with "build a held-out adversarial suite" added verbatim when the stronger fence overcorrected t09 to dead — blind re-judges confirm both suites clean · v0.3.0 · assembled 2026-07-15 · 0.3.0: chat-harness-instructions-and-guardrails gains a sixth axis — references/config-schema-and-prompt-externalization.md (one typed shared config schema over scattered params; prompt prose in files, never string constants; option lists projected from the real registry; byte-identity on refactor), grounded in agent-ui ADR-0135 as a directly verified worked instance (sources.md extended to three instances); description + consult table route the new axis; evals t18–t21 cover it · v0.2.1 · assembled 2026-07-14 · 0.2.1: displayName 'LLM' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.2.0 · assembled 2026-07-13 · the chat-harness six added: a second `system-decompose` pass (6
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
