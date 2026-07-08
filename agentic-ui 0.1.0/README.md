# agentic-ui — A2UI protocol, catalog, agent, and corpus knowledge

Four knowledge packs that answer how `@agent-ui/a2ui` works, cited from the repo corpus — they
explain, they do not build. Named `agentic-ui` rather than `a2ui` on purpose: this plugin is scoped
to host both the existing A2UI (agent-to-UI protocol) content below and any future A2A (Agent2Agent
protocol) material, even though no A2A skill content exists yet anywhere in the source corpus.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/a2ui-protocol` | Knowledge pack | model-only | The wire protocol + zero-dependency renderer: message lifecycle, the Binding union, dynamic lists, two-way input, checks, the function-call vs `callFunction` RPC split, the two-code error taxonomy, version pinning |
| `skills/a2ui-catalog-design` | Knowledge pack | model-only | How a catalog is designed and extended: the definition contract, the factory/resolution pattern, the naming law, two-tier extensibility, the security allowlist + conformance, and coverage policy |
| `skills/a2ui-conversational-agent` | Knowledge pack | model-only | The live-agent system: the AgentTransport isolation seam, the Turn/Session/TurnInput model, the produce() generate-heal-validate-self-correct loop, the multi-provider seam and trust boundary, the in-chat switcher, and the open ADR-0088 gap |
| `skills/a2ui-training-corpus` | Knowledge pack | model-only | The curated training-corpus subsystem: record schema, the two-tier admission gate + healer, the judge/verdict adapter, canonicalization + dedup, retrieval, and the version-change repair loop |

All four are `disable-model-invocation: false` / `user-invocable: false` — model-only knowledge
packs the router picks up from their descriptions, not slash commands. Each carries a
`scripts/routing-corpus.json` (the original routing corpus, kept as-is) alongside an
`evals/evals.json` (this workspace's `eval_check.py` schema, converted 1:1 from the same
positives/negatives) so both the legacy and the forge-native tooling can regress the same cases.

## Cross-plugin seam

`a2ui-protocol`'s re-sync gate is soft, by design: where forge is installed, run its `skill_lint.py`
to a clean pass before the independent `skill-reviewer` + `linguistics-reviewer` critics; otherwise
apply forge's skill-authoring standard by hand. No hard edge crosses the plugin boundary.

v0.1.0 · assembled 2026-07-07 · initial: ported from ~/.claude/skills (a2ui-*) as part of a
plugin-decompose partition; scoped for future A2A content
