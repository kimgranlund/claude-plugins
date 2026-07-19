---
name: plugin-authoring-standards
description: >-
  Standards for authoring and releasing Claude Code plugins — the distribution unit. Use when the
  user asks how to structure a plugin, write plugin.json, package or release a plugin, version it,
  ship hooks or agents or MCP servers in one, why an INSTALLED plugin fails to load, why an update
  isn't picked up, where a plugin's state or config lives, or how plugin namespacing and trust
  work. NOT for declaring a plugin/marketplace in settings.json so it's installable in the first
  place, or a just-declared plugin not yet appearing in /plugin (plugin-onboard). Carries the
  verified load, reload, and versioning semantics (July 2026), including the three load-failure
  classes this plugin hit.
disable-model-invocation: false
user-invocable: false
---

# Plugin Authoring Standards

A plugin is one versioned unit carrying skills, agents, hooks, and MCP config — and it loads **atomically**: one malformed file fails the whole plugin, so the release gate is not a nicety but the difference between shipping and shipping an error screenshot. This is the standard `/plugin-release` gates against and `/harness-audit` scores against; `skill_lint.py` (P-rules) and `release_gate.py` enforce the checkable slice.

## Structure — verified 2026-07 [drift-prone]

```
plugin-name/
├── .claude-plugin/plugin.json    # ONLY the manifest lives here
├── skills/<name>/SKILL.md        # components at the ROOT, never inside .claude-plugin/
├── agents/<name>.md
├── hooks/hooks.json              # outer "hooks" wrapper mandatory in plugins
├── scripts/                      # shared executables, referenced via ${CLAUDE_PLUGIN_ROOT}
├── .mcp.json
└── README.md
```

`plugin.json`: `name` (kebab-case) is required; `version` (semver) is effectively required because **the version is the update cache key** — an edited plugin re-shipped under the same version is skipped by `/plugin update` as already installed. Change without bump = a release nobody receives. `displayName` (optional, Claude Code ≥2.1.143; verified 2026-07-14) is the human-facing name in the /plugin UI — any casing/spaces, never used for namespacing or lookup, falls back to `name` (which the UI otherwise title-cases: `llm` renders as "Llm"); marketplace.json plugin entries carry the same field. House rule: Title Case, acronyms uppercased (`UI`, `LLM`).

## The three load-failure classes — this plugin's own ledger

Each shipped exactly once here before its lint rule existed; each fails the *entire* plugin load:

| Class | Mechanism | Guard |
|---|---|---|
| Bare multi-line frontmatter content | An agent's `<example>` at column 0 parses as a YAML key → parse error | A2: block scalars (`description: \|`), indented |
| Bare settings-style `hooks.json` | Missing outer `"hooks"` wrapper → registers silently never (or fails load) | H2 |
| Reserved words in a skill name/dir | `claude` / `anthropic` rejected at install | F8 |

The general law they instantiate: knowledge that lives only in a document does not bind at the moment of authoring — every load-failure class found becomes a lint rule the same day (the three-strikes rule, collapsed to one strike for load failures, because the blast radius is total).

## Namespacing and naming

Installed skills invoke as `/plugin-name:skill-name`; unqualified names keep working where unambiguous. Plugin names and domain prefixes are **different taxonomies** — a plugin named after its domain prefix stutters (`/ui:ui-review`); pick a distribution-scoped name disjoint from every domain prefix it ships (this plugin: `forge` over `skill-`). Names are APIs: no renames without a deprecation path, no version numbers in names, no reuse of a retired name for a different artifact type.

## Paths and state

- `${CLAUDE_PLUGIN_ROOT}` — the install directory; substitutes in skill bodies, hook commands, and MCP config. **Wiped on every update**: nothing written here survives.
- `${CLAUDE_PLUGIN_DATA}` — persistent per-plugin state that survives updates; caches, installed dependencies, ledgers.
- A hardcoded home path anywhere in the plugin is a plugin that works on one machine (lint H5 catches the hooks.json case).

## Reload semantics — the edit-invisibility trap

`SKILL.md` edits are live-detected within a session. **Everything else is not**: `hooks/`, `agents/`, `.mcp.json`, and `output-styles/` changes require `/reload-plugins` or a restart. "I edited the hook and nothing changed" is this rule, not a bug — the second most common false bug report after the version-cache-key skip.

## Trust — installing is running code

Plugin hooks execute shell commands; MCP servers are processes; bundled executables enter the PATH — and the trust decision **recurs on every update**, because an update is arbitrary new code with the same credentials. Third-party sources pin to exact commit SHAs; your own releases carry explicit versions and a changelog; project-scope skills-dir plugins load only after the workspace trust dialog. Adopting a plugin is adopting a dependency; give it the same rigor.

## Release discipline

Every release runs the same gate, in order — `scripts/release_gate.py <plugin-root>` automates all of it and `selftest` proves its checks bite:

1. Manifest: valid JSON, kebab name, semver version, **version bumped** (a same-version dist artifact fails the gate — the cache-key rule).
2. Structure: manifest alone in `.claude-plugin/`; every `skills/*` dir carries a `SKILL.md`.
3. Full lint: every SKILL.md, agent, hooks.json, and plugin.json through `skill_lint.py`; any FAIL fails the gate.
4. Bundled-script selftests: every `scripts/*.py` exposing a `selftest` mode must exit 0 — an untested shipped script is a flake with distribution.
5. Phantom sweep: `[[handle]]` references in live markdown are unresolved routing — warned, counted, and read.
6. Package: `dist/<name>-<version>.plugin`, excluding `dist/` itself and OS litter.

Gate clean → bump recorded in the README footer (the human-readable ledger) → ship → `/reload-plugins` on the consuming side.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Same-version re-release | Version is the update cache key; update skipped as current | Bump on every change; the gate refuses a same-version dist |
| Components inside `.claude-plugin/` | Only the manifest is read there; components silently missing | Components at plugin root |
| One bad file | Plugin load is atomic | The release gate before every ship, no exceptions |
| State in `${CLAUDE_PLUGIN_ROOT}` | Updates wipe the install dir | `${CLAUDE_PLUGIN_DATA}` for anything that must survive |
| Edited hook, no effect | Hooks/agents/MCP are not live-reloaded | `/reload-plugins`; only SKILL.md hot-reloads |
| Plugin name = domain prefix | `/ui:ui-review` stutter; packaging becomes a rename | Distribution taxonomy ≠ domain taxonomy |
| Unpinned third-party plugin | Every update is unreviewed code on your machine | SHA pinning; re-vet on update |
| Manual release ritual | Steps skipped under time pressure; the skipped one ships the incident | `/plugin-release` runs the gate; humans approve, scripts check |

## Provenance

Structure, cache-key, reload, and trust semantics verified against code.claude.com/docs/en/plugins-reference and this plugin's own three build incidents, 2026-07; all mechanics [drift-prone]. Skill-side rules: `skill-authoring-standards`. Hook-side: `hook-authoring-standards`. Agent-side: `agent-authoring-standards`.
