# nonoun-plugins

Eight Claude Code plugins: `harness` and `docs` are the authoring toolchain — they build and
validate everything else, including each other — and `authorkit` is the estate-governance kit
(naming grammar, audits, renames, whole-estate overhauls). The other five are domain plugins;
most were partitioned out of a legacy personal skill/agent corpus (61 skills, 19 agents) via a
`plan-plugin-split` analysis run by `harness` itself (six at first, consolidated to five when
ADR-0008 merged the color/typography/design-kit members into `design`), and `llm` was authored
fresh via `break-down-problem` (distilled from `@agent-ui/a2ui`'s live-agent implementation,
generalized as portable technique).

Directory names align with each plugin's current name, no version suffix, no spaces (ADR-0007) —
see `CLAUDE.md` for the workspace's own operating rules if you're working *on* these plugins
rather than just installing them.

[MIT licensed](LICENSE).

## Plugins

| Plugin | What it does |
|---|---|
| [`harness`](<harness/README.md>) | Author and validate Claude Code skills, agents, hooks, bundled scripts, entry files, and plugins themselves — the toolchain every other plugin here was built and gated through. |
| [`docs`](<docs/README.md>) | Author functional documents (ADR/PRD/SPEC/LLD/PLAN/ROADMAP/TICKET/TASK), capture bug reports durably before dispatching an investigation, research methods & rubrics, markdown↔markup conversion, knowledge/reference authoring. |
| [`agent-protocols`](<agent-protocols/README.md>) | Knowledge packs for the A2UI wire protocol, renderer, catalog design, and training corpus. |
| [`llm`](<llm/README.md>) | Portable LLM-integration knowledge (the swappable-provider gateway pattern, streaming structured output safely) plus a six-layer mini/portable chat-agent-harness family (instructions/guardrails, skills/routing, orchestration/workflows, knowledge/memory, tools/resources/services, observability). |
| [`design`](<design/README.md>) | Color science and OKLCH palettes, the 11-voice typography system, Material Design tokens, and the design-system export bundles (Claude Design/Figma Make/Google Stitch). |
| [`screens`](<screens/README.md>) | UI structure (layouts, flows, components, patterns), the design/UI knowledge layer (spacing-scale theory, CSS box-model/flow mechanics, Apple HIG semantics, motion), and non-functional verification (focus, i18n, perf, safety, live-artifact checks). |
| [`teamwork`](<teamwork/README.md>) | Decision-deriving, composition/continuation design, and a multi-agent feature-delivery team (planner, builder, coordinator, reviewers). |
| [`authorkit`](<authorkit/README.md>) | Estate governance: the ratified naming grammar (ADR-0011) with its manifest + validator, naming/bloat audits, blast-radius-planned renames with an exemption ratchet, and the end-to-end estate-overhaul driver (`/overhaul-execute`: discovery → your scope gate → audits → plan → gated waved execution → routing proof). |

Each plugin's own `README.md` carries its full component map and a dated version ledger in the
footer — that's the source of truth for what changed and why, not this file.

## Install

As a marketplace (recommended — lets you install only the plugins you want):

```bash
claude plugin marketplace add kimgranlund/claude-plugins
claude plugin install harness@nonoun-plugins
claude plugin install docs@nonoun-plugins
# ...and so on for any of the eight
```

For local development against a working copy instead:

```bash
claude --plugin-dir "/path/to/nonoun-plugins/harness"
```

After installing or updating, run `/reload-plugins`; into a large existing skill library, follow
with `/doctor` — descriptions share a 1%-of-context listing budget across everything installed.

## Provenance

`harness` and `docs` predate the rest. The other six were designed by running `harness`'s own
`plan-plugin-split` skill against a legacy `~/.claude/skills` + `~/.claude/agents` corpus, then
built by porting each cluster's content, converting every cross-plugin hard preload (`skills:`
frontmatter, hardcoded script paths) into a soft mention with an inline fallback — the same
pattern `docs` already used for its own dependency on `harness`. Two real gaps surfaced during
that migration and were closed rather than left as silent capability loss: `check-all-agents` and
`check-all-skills` (deep-review campaigns against each estate's own standard-of-excellence, ported
into `harness` with their gate scripts) and `wiring-checker` (ported into `teamwork`).

`authorkit` arrived differently (2026-08-13/14): hand-authored in a parallel session around a
naming-convention spec, then ratified as ADR-0011 (superseding ADR-0006's grammar half), landed
through the gate (#196), and grown live — its own overhaul instruments were designed, critiqued,
and dogfooded against this very repo before shipping, and its first external run found and fixed
two of its own bugs the same day (#252/#253).

Every plugin validates clean against both `harness/scripts/release_gate.py` and the product's own
`claude plugin validate`.
