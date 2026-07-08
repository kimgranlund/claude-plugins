# Plugin workspace — entry file

Each child directory here is one Claude Code plugin, named `<manifest-name> <version>` (e.g.
`forge 1.14.0`, `scribe 0.1.0`) — quote the path, it contains a space. **forge is the toolchain**:
its commands and standards govern work on every plugin in this workspace, including forge itself.
Work on a plugin happens in its directory; decisions that span plugins happen here.

## Route the job before doing the job

| Job | Owner |
|---|---|
| New plugin from a domain | `/plugin-forge` (never hand-scaffold) |
| Partition or merge existing plugins, gap analysis | `/plugin-decompose` |
| New skill / agent / hook / entry-file work | `/skill-forge` · `/agent-forge` · `/hook-forge` · `/entry-file-audit` |
| Fill or grow a knowledge corpus | `/pack-forge` (one axis per wave) |
| Split or merge a pack; execute the verdict | `/skill-decompose` · `/skill-synthesize` → `/skill-refactor` |
| Functional docs (ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK) | scribe: `/doc-forge` · `/doc-review` |
| A user reports a bug | scribe: `/bug-report` — never raw `/fork` for bug work; it drops the report on exit |
| Research methods, rubrics, knowledge/reference docs, llms.txt, vision memos, markdown↔markup | scribe (folded in, not a separate plugin) — browse `scribe 0.1.0/README.md`'s Map |
| A2UI protocol / renderer / catalog / training-corpus knowledge | `agentic-ui` — scoped for future A2A content too, none built yet |
| Color science, palette design, contrast/CVD verification | `color` |
| Typography system design, pairing, tokens | `typography` |
| Design-system export bundles (Claude Design/Figma Make/Google Stitch) + Material Design tokens | `design-systems` |
| UI structure (layouts, flows, components, patterns) or non-functional verification (focus/i18n/perf/safety) | `ui` |
| Multi-agent feature-delivery team (plan → build → review → coordinate), composition/continuation design | `orchestration` |
| Routing proof after description edits | `/eval-run <plugin>` |
| Periodic health sweep | `/harness-audit` |
| Ship | `/plugin-release <plugin>` — the only way anything ships |

## Common commands

No installed harness required; every check is a plain script. Run from the workspace root, and
quote plugin paths (the version suffix contains a space).

- **Prove a script's own counters:** `python3 "forge 1.14.0/scripts/skill_lint.py" selftest`
  (same pattern for `release_gate.py`, `eval_check.py`, `docs_check.py`, `corpus_check.py`, and
  `scribe 0.1.0/scripts/doc_lint.py`).
- **Full pre-ship gate for a plugin:** `python3 "forge 1.14.0/scripts/release_gate.py"
  "scribe 0.1.0" [--package]` — plugin-agnostic (works on forge or scribe or any future plugin);
  runs manifest/structure checks, the full lint sweep, bundled selftests, a phantom-`[[handle]]`
  sweep, eval-suite validation, and docs-freshness (G10), in that order; `--package` additionally
  writes `<plugin>/dist/<name>-<version>.plugin`.
- **Lint one file by hand** (what the PostToolUse hook runs automatically on every `Write`/`Edit`):
  `python3 "forge 1.14.0/scripts/skill_lint.py" <path-to-SKILL.md-or-agent.md-or-hooks.json>`.
- Once a plugin is installed, prefer its slash commands over raw script calls inside a session:
  `/plugin-release`, `/eval-run`, `/harness-audit`. The commands above are for scripting, CI, or
  a plugin that isn't installed yet.

## Invariants (all plugins, no exceptions)

- **Ship only through the gate.** `release_gate.py <plugin-root> --package` (see Common commands
  above) is plugin-agnostic; artifacts land in `<plugin>/dist/`. Never hand-zip. Never re-ship a
  version — the version is the update cache key; bump every change and log it in that plugin's
  README footer ledger. `dist/` is gate output: read-only.
- **Incident → infrastructure, same day.** A load failure, false positive, or skipped step becomes
  a lint rule, gate check, or selftest fixture before the fix ships. Every `scripts/*.py` in every
  plugin carries a `selftest` mode and it stays green.
- **Descriptions are the routing surface.** Any model-invocable description edit updates its
  `evals/evals.json` in the same change, closes reciprocal fences in sibling suites, and gets an
  `/eval-run` after boundary changes.
- **Plugin boundaries are hard for preloads and `${CLAUDE_PLUGIN_ROOT}` paths, soft for mentions.**
  Cross-plugin handoffs are named mentions that degrade gracefully when the other plugin isn't
  installed; an agent preload or script path crossing plugins is a defect (`surface_map.py check`
  kills it).
- **Naming:** plugin names are distribution-scoped, disjoint from member domain prefixes (no
  `/ui:ui-review` stutter), and never contain `claude` or `anthropic` anywhere in a skill name or
  directory — the install rejects it and the whole plugin fails to load.
- **Docs and ledgers:** functional documents follow scribe's type contracts and mutability classes
  (accepted ADRs are append-only — supersede, never edit; the hook enforces it).
  `.refactor-attic/` directories are the undo for non-git-reversible merges — never deleted
  casually.
- **Sources of record flow outward.** Standards skills in the plugins are canonical; corpus
  snapshots and project-knowledge copies refresh *from* them at release boundaries, never the
  reverse. Falsified claims are amended in place with a dated note.

## When starting anything

Read the target plugin's own `CLAUDE.md` and README footer ledger first (per-plugin invariants and
version history live there, not here). If a task has no owner in the routing table above, that
absence is a finding: check it against the anti-matrix rule (job evidence required) before
building anything new.
