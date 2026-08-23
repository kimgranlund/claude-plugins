---
date: 2026-08-23
topic: >
  Plugin/skill/MCP-server packaging contracts of the Pi and Hermes agent harnesses, gathered so a
  build step can emit each harness's manifest from a Claude Code plugin source of truth
  (`.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, `agents/<name>.md`, `hooks/hooks.json`,
  `.mcp.json`). Companion to a sibling team's already-verified Codex contract
  (`.codex-plugin/plugin.json`, `skills/` pointer, `agents/openai.yaml`, `.agents/plugins/marketplace.json`).
sources:
  - https://pi.dev/docs/latest/packages
  - https://pi.dev/packages
  - https://github.com/earendil-works/pi (packages/coding-agent/docs/{packages,extensions}.md)
  - https://github.com/badlogic/pi-skills
  - https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
  - https://github.com/NousResearch/hermes-agent (website/docs/user-guide/features/{plugins,mcp}.md)
status: draft — self-scored below; not yet independently doc-checker'd
---

# Harness packaging research — Pi and Hermes

Method note: every row below was produced either from a direct `WebFetch` of a named primary URL
(marked `[verified]` when the fetch returned a verbatim quote I could cite) or from a `WebSearch`
cross-snippet aggregation that was **not** independently re-fetched (marked `[inferred]` or
`[drift-prone]`, per this deliverable's confidence vocabulary — never upgraded to `[verified]`
just because the underlying page is itself primary, since the aggregation step is a second point
of possible distortion this session didn't independently close).

Novelty scope (stated once, applies to every row's `new-to-corpus` flag): repo-wide `Grep` for
`Pi coding agent|Hermes Agent|NousResearch|pi\.dev|earendil-works` across
`/Users/kimba/Projects/nonoun/plugins` (0 hits) and `Glob` for `**/research/**` under
`.claude/docs` (no prior `research/` directory existed) — both run 2026-08-23, before this file
was written.

## Disambiguation

- **"Pi"**: the open-source coding-agent CLI at `pi.dev`, built by Mario Zechner (GitHub handle
  `badlogic`, org `earendil-works`), npm-published as `@earendil-works/pi-coding-agent` /
  `@mariozechner/pi-coding-agent`. Multi-provider (Anthropic/OpenAI/Google), TypeScript-built,
  MCP + skills + extensions capable. **Not** the "Pi Network" cryptocurrency project or the "PI
  API MCP Server" (an unrelated financial-data MCP server) that also surfaced in search results —
  those are name collisions, not the same product. This is the harness that matches the dispatch's
  context (a coding-agent CLI with SKILL.md-compatible skills).
- **"Hermes"**: `hermes-agent`, built by Nous Research, GitHub `NousResearch/hermes-agent`,
  self-described "the self-improving AI agent" / "the agent that grows with you." General-purpose
  (chat, coding assistance, scheduling, cross-platform messaging bots), not narrowly a coding
  agent. Nous Research also ships a separate "Hermes" **model** family (fine-tuned LLM weights) —
  a second name collision within the same org. This research is about the **agent harness**
  (the CLI/plugin system), confirmed as the dispatch's intended "NousResearch's Hermes agent"
  reading.

---

## Pi (pi.dev / earendil-works)

### (a) What Pi is / who ships it

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Pi is an open-source, multi-provider coding-agent CLI at pi.dev, built by Mario Zechner (`earendil-works`/`badlogic` on GitHub), installed via `curl -fsSL https://pi.dev/install.sh \| sh`; distinct from unrelated "Pi Network"/"PI API MCP" name collisions found in the same search sweep. | fact | https://pi.dev/ ; https://github.com/earendil-works/pi | 2026-08-23 | [verified] | Label any generated comparison doc/table header as "Pi (pi.dev, earendil-works coding-agent CLI)" to pre-empt the name collision. | new-to-corpus — repo grep for `pi\.dev\|earendil-works` etc., 2026-08-23, 0 hits (see Novelty scope note above) |

### (b) Plugin/extension packaging format

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Pi reuses `package.json` itself as the manifest — no separate `plugin.json`/`plugin.yaml` file. A `"pi"` key declares resource arrays: `{"pi": {"extensions": ["./extensions"], "skills": ["./skills"], "prompts": ["./prompts"], "themes": ["./themes"]}}`; paths are relative to package root, arrays accept globs and `!exclusions`; a `"keywords": ["pi-package"]` entry is what makes the package discoverable on the pi.dev gallery. | fact | https://pi.dev/docs/latest/packages (WebFetch, quoted) + https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md (WebFetch, quoted, cross-corroborating) | 2026-08-23 | [verified] | Build step emits a `package.json` with a `"pi"` key mapping the Claude Code plugin's `skills/` dir straight across (`"skills": ["./skills"]`); no distinct manifest filename to generate. | new-to-corpus — same scope as above |
| MCP servers are **absent** as a declarable resource type in the `"pi"` package manifest — only `extensions`/`skills`/`prompts`/`themes`/gallery-metadata (`video`/`image`) are documented fields. MCP is handled entirely outside the package manifest (see (d)). | fact | Same two sources as row above | 2026-08-23 | [verified] | Build step must NOT try to fold an `.mcp.json` server entry into Pi's `package.json` — route it to the separate MCP config surface instead, or drop it with a named gap if that surface is out of scope for pass 1. | new-to-corpus — same scope |

### (c) Skill discovery

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Skills are `SKILL.md` files with YAML frontmatter (`name`, `description`) plus an instructions body, recursively discovered under a package's `skills/` directory (or auto-discovered without any manifest at all). A companion skills package (`badlogic/pi-skills`) states explicitly this is "the pi/Claude Code format" and is compatible with Claude Code, Codex CLI, Amp, and Droid — i.e. Pi's skill format is a near-direct SKILL.md passthrough. | fact | https://pi.dev/docs/latest/packages (auto-discovery, WebFetch quoted) + https://github.com/badlogic/pi-skills/blob/main/README.md (WebFetch quoted) | 2026-08-23 | [verified] | Build step for Pi's skills output = copy `skills/<name>/SKILL.md` byte-for-byte from the Claude Code source of truth; frontmatter needs no field remapping for `name`/`description`. | new-to-corpus — same scope |
| Beyond the package-bundled path, Pi also reads skills from user-level `~/.pi/agent/skills/<name>/SKILL.md` and project-level `.pi/skills/<name>/SKILL.md`, per the pi-skills README's stated install locations. | fact | https://github.com/badlogic/pi-skills/blob/main/README.md (WebFetch quoted) | 2026-08-23 | [inferred] — only sourced from a companion third-party skills repo, not independently cross-confirmed against a pi.dev primary-docs page naming these exact paths. | If the build step needs to write skills directly to disk rather than via a package, target `.pi/skills/<name>/SKILL.md` for project scope — but re-verify this path against primary pi.dev docs before relying on it in an automated pipeline. | new-to-corpus — same scope |

### (d) MCP server config

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| MCP servers are configured at the runtime/config level, not the package level — candidate config paths surfaced (project `.mcp.json`, global `~/.config/mcp/mcp.json`, Pi-specific `~/.pi/agent/mcp.json` / `$PI_CODING_AGENT_DIR/mcp.json`, tool-agnostic `~/.agents/mcp.json`) with a `mcpServers` object keyed by server name, each entry carrying `command`/`args` (or presumably a remote-URL form, unconfirmed). | fact | WebSearch aggregate only (LobeHub pi-mcp-adapter/pi-mcp-setup pages, nicobailon/pi-mcp-adapter repo) — **not independently WebFetched from a single primary pi.dev docs page in this session** | 2026-08-23 | [drift-prone] — reason: multiple partially-conflicting candidate paths came only from secondary aggregator pages; no primary pi.dev/docs MCP page was directly fetched and quoted to settle which one is canonical. | Prefer targeting project-local `.mcp.json` first, since that name is a direct file-name match for Claude Code's own `.mcp.json` — but flag this row's path list for re-verification against pi.dev's own docs before the build step trusts it unattended. | new-to-corpus — same scope |

### (e) Subagents / hooks / slash commands

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Slash commands ARE native (`pi.registerCommand()` inside a TypeScript extension) and lifecycle events ARE native (`pi.on(event, handler)` across "dozens of lifecycle points," functioning as Pi's hook-equivalent) — but **both require writing TypeScript extension code**; there is no declarative `hooks.json`-style file and no declarative `commands/*.md` file format. There is **no built-in agents/persona/subagent concept at all** in core Pi — the primary extensions doc states this outright; subagent behavior exists only via third-party community extensions (`nicobailon/pi-subagents`, `tintinweb/pi-subagents`) layered on top of session management. | unique-insight | https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md (WebFetch, quoted for the "no native agents concept" + registration-API claims) | 2026-08-23 | [verified] for the "no declarative hooks file / no native subagents" claim (direct primary-doc quote); the two named community-extension repos are [inferred] (surfaced by WebSearch listing, not independently WebFetched) | This is THE Pi degradation-table entry: a Claude Code plugin's `agents/*.md` has **no** target in Pi at all (drop it, or flag it as an unsupported primitive) and `hooks/hooks.json` has no declarative target either — any hook-carrying behavior would need hand-written TS extension codegen, likely out of scope for a first-pass build step. | new-to-corpus — same scope |

### (f) Marketplace / registry / install

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| `pi.dev/packages` is the public gallery, populated by any npm or git package carrying the `"pi-package"` keyword — there is no separate static registry/marketplace manifest file (nothing analogous to Codex's `.agents/plugins/marketplace.json`). Install forms: `pi install npm:<pkg>[@version]`, `pi install git:<host>/<repo>[@ref]`, `pi install <url>`, `pi install <local-path>`; a `-l` flag scopes install to the project. | fact | https://pi.dev/docs/latest/packages (WebFetch, quoted for install syntax) + https://pi.dev/packages (WebSearch site listing) | 2026-08-23 | [verified] for install-command syntax (direct doc quote); [inferred] for the `-l` flag writing specifically to `.pi/settings.json` (surfaced once via WebFetch summary, not independently re-confirmed) | Nothing for the build step to generate for Pi's "marketplace" — publishing = pushing the package to npm or git with the right keyword; no registry file to author, unlike Codex's `marketplace.json`. | new-to-corpus — same scope |

### (g) Version / update semantics

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| npm-sourced packages are pinned at the installed semver and are **not** auto-upgraded by `pi update`; git-sourced packages are pinned at a tag/commit ref and are similarly untouched by `pi update --extensions`/`--all`. A new version only lands via an explicit re-install naming a new version/ref (`pi install npm:pkg@newversion` or `pi install git:host/repo@newref`). | fact | https://pi.dev/docs/latest/packages + https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md (both WebFetch, quoted, consistent) | 2026-08-23 | [verified] | Build-step version signal for Pi = the semver string already in `package.json` (npm channel) or the git tag (git channel) — this is a straight passthrough of Claude Code's own `plugin.json` `version` field; "new version" detection in CI is a plain string diff, no Pi-side version-check endpoint exists to poll. | new-to-corpus — same scope |

---

## Hermes (NousResearch/hermes-agent)

### (a) What Hermes is / who ships it

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Hermes Agent is built by Nous Research (`NousResearch/hermes-agent` on GitHub), self-described "the self-improving AI agent... the only agent with a built-in learning loop" — general-purpose (conversation, coding assistance, scheduling, cross-platform bot deployment via Telegram/Discord/Slack/WhatsApp/Signal), not narrowly a coding agent. Distinct from Nous Research's separately-shipped "Hermes" fine-tuned LLM model family — a second name collision within the same org, worth flagging in any generated doc. | fact | https://github.com/NousResearch/hermes-agent (WebFetch, quoted) | 2026-08-23 | [verified] | Label generated output "Hermes (NousResearch/hermes-agent CLI)" to disambiguate from the Hermes model weights. | new-to-corpus — same scope |

### (b) Plugin/extension packaging format

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Manifest file is `plugin.yaml`, located at `~/.hermes/plugins/<plugin-name>/plugin.yaml` (or a bundled-equivalent path for built-ins). Required fields: `name`, `version`, `description`. A companion `__init__.py` with a `register(ctx)` function does the actual wiring (tools/hooks/skills/commands via `ctx.register_*` calls) — the manifest alone is inert. Optional fields: `requires_env`, `capabilities` (privileged surfaces needing consent, e.g. `tools.override`), `kind`. A `manifest_version: 2` schema adds `api_version`, `requires_plugins`, `python_dependencies`, `config_schema`, `license`, `homepage`, `tags`; unknown fields are ignored for forward compatibility. | fact | https://hermes-agent.nousresearch.com/docs/developer-guide/plugins (WebFetch, quoted) + https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md (WebFetch, quoted, cross-corroborating) | 2026-08-23 | [verified] | Build step emits `plugin.yaml` (name/version/description minimum) **plus** a stub `__init__.py` calling `register(ctx)` — unlike Claude Code's inert `plugin.json`, a Hermes plugin needs executable glue even for a skills-only package; a codegen pass must template that stub. | new-to-corpus — same scope |

### (c) Skill discovery

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Plugin-bundled skills live at `skills/<skill-name>/SKILL.md` inside the plugin directory and must be explicitly registered in `register(ctx)` via `ctx.register_skill(skill_name, path_to_skill_md)`; resulting skills are namespaced `plugin-name:skill-name` and read-only (won't clash with built-ins). Separately, a standalone `hermes skills` CLI / `/skills` slash command targets a public "Skills Hub" spanning four registries (built-in/optional/community/…), installable independent of the plugin system via `hermes skills install owner/repo/skills/<name>` or `hermes skills install official/<category>/<name>`. | fact | https://hermes-agent.nousresearch.com/docs/developer-guide/plugins (WebFetch, quoted, for the plugin-bundled path + `ctx.register_skill`) | 2026-08-23 | [verified] for the plugin-bundled SKILL.md path and registration call | Build step should target the plugin-bundled path (`skills/<name>/SKILL.md` + a generated `ctx.register_skill()` line in the stub `__init__.py`) — do NOT conflate this with the separate Skills Hub publishing flow, which this build step doesn't own. | new-to-corpus — same scope |
| The public Skills Hub is reported to span ~652 skills across 4 registries (72 built-in / 59 optional / 521 community), hosted at a domain resembling `agentskills.io`. | fact | WebSearch aggregate only (DeepWiki summary, OpenClaw Launch guide) — **not independently WebFetched** | 2026-08-23 | [inferred] — stat and domain both surfaced only via secondary aggregator summaries in this session; treat the exact count and domain as likely to drift or be imprecise. | Not load-bearing for the build step (Skills Hub is out of scope per the row above) — no action beyond not citing this count as authoritative. | new-to-corpus — same scope |

### (d) MCP server config

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| User-level MCP servers are declared under `mcp_servers:` in `~/.hermes/config.yaml` — stdio form (`command`/`args`/`env`) or HTTP form (`url`/`headers`, `auth: oauth`), plus `timeout`/`connect_timeout`/`enabled`/`tools` include-exclude filters. Separately, a curated, Nous-approved MCP catalog is stored **inside the hermes-agent repo itself** at `optional-mcps/<name>/manifest.yaml` — "presence in that directory means Nous approval" — installed via `hermes mcp install <name>`; ad hoc manual entries go through `hermes mcp add <name>`. | fact | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/mcp.md (WebFetch, quoted directly, including the `optional-mcps/` line) | 2026-08-23 | [verified] for `config.yaml` shape and the `optional-mcps/` catalog's existence + path | Build step emitting a Hermes MCP entry from a Claude Code plugin's `.mcp.json` should target `config.yaml`'s `mcp_servers:` block — field names differ (`mcpServers`→`mcp_servers`) but the command/args vs. url/headers shape is a near 1:1 remap; the curated `optional-mcps/` catalog is a separate, PR-gated path this build step doesn't own. | new-to-corpus — same scope |
| The curated catalog manifest's own field list (`name`, `version`, `manifest_version`, `source`, `transport`, `auth`) was surfaced but not re-quoted verbatim from a directly fetched `optional-mcps/<name>/manifest.yaml` example in this session. | fact | WebSearch aggregate only (initial query summary) | 2026-08-23 | [inferred] — field list not independently re-confirmed by fetching an actual example manifest file. | If the build step ever needs to target the curated catalog (not just user `config.yaml`), fetch one real `optional-mcps/<name>/manifest.yaml` example first to confirm this field list before generating one. | new-to-corpus — same scope |

### (e) Subagents / hooks / slash commands

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| Hooks ARE native: lifecycle events `pre_tool_call`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `on_session_start`, `on_session_end`, wired via `ctx.register_hook("hook_name", callback)` in the plugin's Python `__init__.py` — still code, not a declarative `hooks.json`. Slash commands ARE native: `ctx.register_command(name, handler, description)` registers an in-session `/name` command; a separate `ctx.register_cli_command(...)` registers a `hermes plugin-name <sub>` CLI subcommand. Subagents have **no** plugin-defined-agent file format — the primary doc states outright "Subagents are invoked through the `delegate_task` tool, not directly via plugins," i.e. no Hermes equivalent of a Claude Code `agents/<name>.md` frontmatter file. | unique-insight | https://hermes-agent.nousresearch.com/docs/developer-guide/plugins (WebFetch, quoted directly for all claims in this row) | 2026-08-23 | [verified] | THE Hermes degradation-table entry: `agents/*.md` has no target (drop or flag as unsupported, same shape as Pi's gap). Unlike Pi, Hermes's hook event names (`pre_tool_call`/`post_tool_call`) are closer lexical analogs to Claude Code's own hook vocabulary (`PreToolUse`/`PostToolUse`) — worth a dedicated event-name mapping pass before attempting hook codegen, since this is the one harness of the two where hook passthrough might be more than a stub. | new-to-corpus — same scope |

### (f) Marketplace / registry / install

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| No centralized plugin marketplace — plugins install straight from GitHub repos or PyPI: `hermes plugins install owner/repo` (optionally `--enable`), `hermes plugins search <term>`, `hermes plugins pack install ./hermes-pack.yaml` (a multi-plugin bundle/pack format, distinct from a single plugin), `hermes plugins enable <name>` to opt in post-install, `hermes plugins list` / `hermes plugins doctor` for discovery/manifest validation. Community promotion is informal (a Discord channel), not a registry site. | fact | https://hermes-agent.nousresearch.com/docs/developer-guide/plugins (WebFetch, quoted) | 2026-08-23 | [verified] | No static registry manifest to author for Hermes either (mirrors Pi's gap vs. Codex's `marketplace.json`) — the build step's Hermes output is just the plugin directory pushed to any git host; nothing else to generate for "marketplace" support. | new-to-corpus — same scope |

### (g) Version / update semantics

| Finding | Category | Source | Access-date | Confidence | Actionable-note | Novelty |
|---|---|---|---|---|---|---|
| `plugin.yaml` carries a literal `version` string field (docs example shows `version: "1.0"` — not confirmed as strictly-enforced semver); `manifest_version` is a separate number identifying which manifest **schema** (v1 vs v2) the file follows, not the plugin's own version. Hermes exposes no global `PLUGIN_API_VERSION` gate — a plugin using only documented `PluginContext` methods is expected to keep working across Hermes host upgrades (no forced version bump tied to host release). | fact | WebSearch aggregate cross-referencing `plugins.md` + `cli-commands.md` snippets — **not independently re-fetched as a single primary-page quote in this session** | 2026-08-23 | [inferred] — reason: this synthesis came from the WebSearch tool's own cross-snippet aggregation rather than a direct WebFetch quote against one confirmed primary URL. | Build-step version signal for Hermes = a plain string diff on `plugin.yaml`'s `version` field, same pattern as Pi/Codex — but do not assume semver validation is enforced; pass Claude Code's own `plugin.json` `version` value through verbatim rather than attempting to reformat it. | new-to-corpus — same scope |

---

## Codex comparison

Derived synthesis from the rows above plus the dispatch-supplied, already-verified Codex facts —
not a new sourced claim in its own right; each cell traces back to a row above or the dispatch
context.

| Contract element | Codex (given, verified by sibling team) | Pi | Hermes |
|---|---|---|---|
| Manifest file | `.codex-plugin/plugin.json` | `package.json` (`"pi"` key) — no separate manifest file | `plugin.yaml` + a `__init__.py` `register(ctx)` stub (manifest alone is inert) |
| Skills pointer | `"skills": "./skills/"` in manifest | Auto-discovered `skills/` dir, or declared via `"pi": {"skills": [...]}"` | Declared per-skill via `ctx.register_skill(name, path)` in `register(ctx)` |
| Skill format | SKILL.md-compatible, optional `agents/openai.yaml` interface block | SKILL.md, explicitly "pi/Claude Code format" — near-direct passthrough | SKILL.md, namespaced `plugin-name:skill-name`, read-only |
| MCP config | (not detailed in dispatch context for Codex) | Separate runtime config (`.mcp.json`/`~/.config/mcp/mcp.json` — path unsettled, see (d)); NOT part of the package manifest | `~/.hermes/config.yaml`'s `mcp_servers:` block; separate curated `optional-mcps/<name>/manifest.yaml` catalog in-repo |
| agents/ (subagents) | NOT supported (per dispatch) | NOT supported natively — third-party extensions only | NOT supported as a plugin-defined file — routed through the built-in `delegate_task` tool instead |
| hooks/ | NOT supported (per dispatch) | Programmatic only (`pi.on(event, handler)` in TS extensions) — no declarative file | Programmatic only (`ctx.register_hook(...)` in Python) — no declarative file, but event names map closer to Claude Code's own vocabulary |
| commands/ (slash commands) | NOT supported (per dispatch) | Programmatic only (`pi.registerCommand()` in TS extensions) — no declarative file | Programmatic only (`ctx.register_command(...)` in Python) — no declarative file |
| Marketplace/registry | `.agents/plugins/marketplace.json` | None — gallery is an npm/git keyword scrape (`"pi-package"`), no registry file | None — GitHub/PyPI-distributed, no registry file; Skills Hub is a separate skills-only registry |
| Enablement | `~/.codex/config.toml` | `pi install npm:\|git:\|<url>\|<path>` (+ `-l` for project scope) | `hermes plugins install owner/repo` → `hermes plugins enable <name>` |
| Version signal | (not detailed in dispatch context) | npm semver pin or git tag/ref pin — passthrough of source version string | `plugin.yaml`'s `version:` string — passthrough, no enforced semver |

**Shared cross-harness pattern** (the one genuinely synthesized insight this research adds beyond
individual facts): **both Pi and Hermes match Codex on the `agents/`/`hooks/`/`commands/` gap** —
none of the three non-Claude harnesses researched so far has a declarative equivalent for Claude
Code's `agents/<name>.md`, and neither Pi nor Hermes has a declarative `hooks.json` equivalent
either (both require host-language code — TypeScript for Pi, Python for Hermes). A build step
targeting all three harnesses can treat "no subagents, no declarative hooks" as a **structural
degradation, not a per-harness quirk** — the emission contract only needs one shared "unsupported
primitive" branch for `agents/` and `hooks/`, not three separate ones.

---

## Open questions (unverified — flagged rather than guessed)

1. **Pi's canonical MCP config path.** Multiple candidate paths surfaced (`.mcp.json`,
   `~/.config/mcp/mcp.json`, `~/.pi/agent/mcp.json`, `~/.agents/mcp.json`) only via secondary
   aggregator pages (LobeHub, community repos) — no primary pi.dev docs page was directly fetched
   to settle which is canonical vs. which are read-fallbacks. Search run: `WebSearch` for
   `pi.dev docs mcp.json mcpServers pi coding agent configuration file`, 2026-08-23 — returned only
   secondary sources; a follow-up should `WebFetch` `pi.dev/docs/latest/mcp` (or equivalent) directly.
2. **Pi's `-l` install flag target.** Reported to write to `.pi/settings.json` for project-scope
   installs, sourced from a single WebFetch summary, not independently re-confirmed.
3. **Hermes `optional-mcps/<name>/manifest.yaml` exact field list.** `name`/`version`/
   `manifest_version`/`source`/`transport`/`auth` surfaced via WebSearch aggregation only; no
   actual example file was fetched and quoted in this session.
4. **Hermes `plugin.yaml` version-field semver enforcement.** Whether `version` is validated as
   semver or accepted as opaque text is unconfirmed — inferred from cross-snippet WebSearch
   aggregation, not a direct primary quote.
5. **Hermes Skills Hub stat (~652 skills / `agentskills.io`).** Not independently WebFetched;
   flagged as likely to drift and not load-bearing for the build step regardless (out of scope,
   per (c) row 2's actionable-note).
6. **Event-taxonomy overlap for hook codegen.** Whether Hermes's `pre_tool_call`/`post_tool_call`/
   `pre_llm_call`/`post_llm_call`/`on_session_start`/`on_session_end` and Pi's full `pi.on(event,…)`
   event list overlap closely enough with Claude Code's own hook event names (`PreToolUse`,
   `PostToolUse`, etc.) for real 1:1 codegen, versus just a stub-emission — not evaluated in this
   pass; needs a dedicated follow-up dispatch reading both harnesses' full event lists side by side
   with Claude Code's `hooks.json` schema.

---

## Rubric self-score

Scored against `references/rubric.md` (research-rules skill), all four axes `[review]`:

| Axis | Score (1/3/5) | Why |
|---|---|---|
| K1 — Knowledge | **3** | Findings are substantive and specific (exact file paths, field names, command syntax — not generic restatement), and two rows are tagged `unique-insight` (the "no declarative hooks, no native subagents" pattern per harness, and the cross-harness synthesis in the Codex-comparison closing paragraph). Honest gap: this topic is a packaging-contract lookup, so no `real-result`, `case-study`, or `practitioner-conversation` entries exist or were forced in — a 5 would require evidence this research genuinely doesn't have (e.g. a team's actual experience building a Pi/Hermes emitter), so 3 is the honest ceiling here, not a shortfall in effort. |
| A1 — Actionable | **4** | Nearly every row's `actionable-note` names a concrete next step for the build step (exact file to emit, exact field to remap, exact gap to flag) rather than restating the finding. A couple of notes ("re-verify against primary docs before shipping") are process-caution rather than a build action — that's what keeps this at 4, not 5. |
| G1 — Grounding | **4** | Every `[verified]` marker in this file traces to an actual `WebFetch` of a named primary URL with a quoted claim; every claim sourced only through `WebSearch` aggregation was marked `[inferred]` or `[drift-prone]`, never upgraded. Not a 5 because two Pi/Hermes surfaces ((d) Pi's MCP path, (g) Hermes version semantics) never got a primary-page WebFetch in this pass — flagged honestly in Open Questions rather than left unmarked. |
| N1 — Novelty | **5** | A real repo-wide `Grep` (across all plugin dirs) plus `Glob` for an existing `research/` directory ran before any row was written, both returned zero hits, and the exact search pattern/scope is stated once at the top and referenced from every row — checkable by re-running the same two commands. |

**Gate check:** K1=3, A1=4, G1=4, N1=5 — all ≥ 3, deliverable clears the accept gate.

**Findings recorded:** 9 (Pi) + 7 (Hermes) = 16 finding rows, plus 1 comparison table and 1 closing
cross-harness synthesis paragraph.

**Questions left unanswered:** 6, listed in full above (Pi MCP canonical path, Pi `-l` flag
target, Hermes curated-MCP manifest field list, Hermes version-field semver enforcement, Hermes
Skills Hub stat accuracy, hook event-taxonomy overlap for codegen).

**Sources to re-fetch before this record is treated as final:** a primary pi.dev MCP-config docs
page (question 1), one real `optional-mcps/<name>/manifest.yaml` example from the hermes-agent
repo (question 3), and the specific `plugins.md`/`cli-commands.md` pages for Hermes version
semantics (question 4) — all three currently rest on `WebSearch` aggregation rather than a
directly quoted primary fetch.
