# nonoun-plugins

Nine Claude Code plugins: `forge` and `scribe` are the authoring toolchain — they build and
validate everything else, including each other. The other seven are domain plugins; six were
partitioned out of a legacy personal skill/agent corpus (61 skills, 19 agents) via a
`plugin-decompose` analysis run by `forge` itself, and `llm` was authored fresh via
`system-decompose` (distilled from `@agent-ui/a2ui`'s live-agent implementation, generalized as
portable technique).

Directory names carry a version suffix (`forge 1.14.0`, `scribe 0.1.0`, ...) — quote the path, it
contains a space. See `CLAUDE.md` for the workspace's own operating rules if you're working *on*
these plugins rather than just installing them.

[MIT licensed](LICENSE).

## Plugins

| Plugin | What it does |
|---|---|
| [`forge`](<forge 1.14.0/README.md>) | Author and validate Claude Code skills, agents, hooks, bundled scripts, entry files, and plugins themselves — the toolchain every other plugin here was built and gated through. |
| [`scribe`](<scribe 0.1.0/README.md>) | Author functional documents (ADR/PRD/SPEC/LLD/PLAN/ROADMAP/TICKET/TASK), capture bug reports durably before dispatching an investigation, research methods & rubrics, markdown↔markup conversion, knowledge/reference authoring. |
| [`agentic-ui`](<agentic-ui 0.1.0/README.md>) | Knowledge packs for the A2UI wire protocol, renderer, catalog design, and training corpus. |
| [`llm`](<llm 0.1.0/README.md>) | Portable LLM-integration knowledge (the swappable-provider gateway pattern, streaming structured output safely) plus a six-layer mini/portable chat-agent-harness family (instructions/guardrails, skills/routing, orchestration/workflows, knowledge/memory, tools/resources/services, observability). |
| [`color`](<color 0.1.0/README.md>) | Color science (accessibility, materials, perception, spaces), OKLCH palette design, contrast/CVD verification. |
| [`typography`](<typography 0.1.0/README.md>) | Typography systems, pairing, tokens, lettering knowledge. |
| [`design-systems`](<design-systems 0.1.0/README.md>) | Design-system export bundles (Claude Design, Figma Make, Google Stitch) and the Material Design token grammar. |
| [`ui`](<ui 0.1.0/README.md>) | UI structure (layouts, flows, components, patterns), the design/UI knowledge layer (spacing-scale theory, CSS box-model/flow mechanics, Apple HIG semantics, motion), and non-functional verification (focus, i18n, perf, safety, live-artifact checks). |
| [`orchestration`](<orchestration 0.1.0/README.md>) | Decision-deriving, composition/continuation design, and a multi-agent feature-delivery team (planner, builder, coordinator, reviewers). |

Each plugin's own `README.md` carries its full component map and a dated version ledger in the
footer — that's the source of truth for what changed and why, not this file.

## Install

As a marketplace (recommended — lets you install only the plugins you want):

```bash
claude plugin marketplace add kimgranlund/claude-plugins
claude plugin install forge@nonoun-plugins
claude plugin install scribe@nonoun-plugins
# ...and so on for any of the nine
```

For local development against a working copy instead:

```bash
claude --plugin-dir "/path/to/nonoun-plugins/forge 1.14.0"
```

After installing or updating, run `/reload-plugins`; into a large existing skill library, follow
with `/doctor` — descriptions share a 1%-of-context listing budget across everything installed.

## Provenance

`forge` and `scribe` predate the rest. The other six were designed by running `forge`'s own
`plugin-decompose` skill against a legacy `~/.claude/skills` + `~/.claude/agents` corpus, then
built by porting each cluster's content, converting every cross-plugin hard preload (`skills:`
frontmatter, hardcoded script paths) into a soft mention with an inline fallback — the same
pattern `scribe` already used for its own dependency on `forge`. Two real gaps surfaced during
that migration and were closed rather than left as silent capability loss: `agents-audit` and
`skills-audit` (deep-review campaigns against each estate's own standard-of-excellence, ported
into `forge` with their gate scripts) and `orchestration-reviewer` (ported into `orchestration`).
Every plugin validates clean against both `forge/scripts/release_gate.py` and the product's own
`claude plugin validate`.
