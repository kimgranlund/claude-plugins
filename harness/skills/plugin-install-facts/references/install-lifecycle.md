# Install lifecycle — trust, scope, updates, uninstall

Ask this file: "what happens around the install — prompts, where it lands, why an update never
arrived, how to remove it?" Distilled from wave 1 (2026-07-25); canonical source
code.claude.com/docs (plugins-reference, discover-plugins, settings) + this workspace's
plugin-writing-rules/adopt-plugin. All claims [verified] 2026-07-25 unless marked.

## Scope — where an install lands

| Scope | Settings file | Audience |
|---|---|---|
| `user` (default) | `~/.claude/settings.json` | Personal, all projects |
| `project` | `.claude/settings.json` | Team, shared via git |
| `local` | `.claude/settings.local.json` | Personal, this repo, gitignored |
| `managed` | Managed settings | IT-deployed, read-only |

Precedence: Managed > Local > Project > User — for settings generally. Enablement
(`enabledPlugins`, key form `"<plugin-name>@<marketplace-id>": true`) is read from ALL four
scopes, but does NOT follow that strict override chain in practice: observed 2026-07-29
(Claude Code v2.x, two independent plugins on one machine), an **enable in any scope beats a
disable in another** — a user-scope-installed plugin with user `true` stayed enabled against a
project-scope `false`, while another plugin with user `false` was enabled by a project/local
`true`. To disable a plugin, remove or flip the entry in the scope that holds the `true`
(`/plugin disable <plugin> -s <scope>`); a `false` added in a different scope is not sufficient.
[verified — observed behavior 2026-07-29; contradicts a plain reading of plugins-reference
§User configuration, which orders scopes without stating enablement merge semantics]
`pluginConfigs` is unchanged: read ONLY from user settings, `--settings` flag, and managed —
project/local entries are ignored for it. [verified] plugins-reference §User configuration.

Related tell: an `enabledPlugins` entry naming a marketplace absent from
`known_marketplaces.json` degrades to the unexplained "1 error during load" in
`/reload-plugins` — check for dangling `@<marketplace>` suffixes before chasing deeper.
[verified 2026-07-29]

## Trust — the gates that fire

- Installing is running code: project-scope plugins load only after the workspace-trust dialog;
  MCP servers get per-server approval; LSP servers start only after trust; background monitors
  do NOT load at project scope. Personal-scope plugins skip these restrictions. [verified]
- Trust RECURS on every update — not a one-time gate. [verified; canonical rule and rationale:
  plugin-writing-rules §Trust — cite it, don't restate it]

## Updates — and why one never arrives

- **The version field is the update cache key** — a re-ship under the same version arrives
  nowhere. The canonical rule and its gate enforcement live in plugin-writing-rules §Release
  discipline [verified]; this pack keeps only the symptom mapping: an installed plugin's
  "update didn't arrive" → check the publisher bumped the version, before debugging anything
  else. (The AUTHOR-side ask — "why isn't my re-shipped update picked up" — routes to
  plugin-writing-rules, not here.)
- Installed plugins are COPIES in `~/.claude/plugins/cache`, one directory per version; on
  update/uninstall the old version is orphaned and auto-deleted after ~14 days (grace for
  concurrent sessions still on it). [verified] plugins-reference §Plugin caching.
- `autoUpdate` is per-marketplace (`extraKnownMarketplaces[<id>].autoUpdate`): official
  Anthropic marketplaces default ON, third-party/local default OFF. `DISABLE_AUTOUPDATER=1`
  kills all auto-updates globally. [verified] discover-plugins §Configure auto-updates.

## Enable · disable · uninstall

```
/plugin enable <plugin> [-s scope]        # enables; declared dependencies enable transitively
/plugin disable <plugin> [-s scope]       # disables without removing
/plugin uninstall <plugin> [-s scope] [--keep-data] [--prune]
/plugin update <marketplace-name>         # refreshes a marketplace's listings
```

Uninstall deletes `${CLAUDE_PLUGIN_DATA}` unless `--keep-data` is passed — warn before
suggesting a bare uninstall to someone with per-plugin state. [verified] plugins-reference
§CLI commands.

Ship-state: a plugin may declare `"defaultEnabled": false` (v2.1.154+) to install disabled;
precedence for effective state: user's `enabledPlugins` entry > dependency requirement >
`defaultEnabled`. [verified] plugins-reference §Default enablement.
