# Install commands — the exact form per channel

Ask this file: "what do I type to install a plugin via <channel>?" Distilled from wave 1
(2026-07-25); canonical source code.claude.com/docs (discover-plugins, plugins-reference,
cli-reference). Everything here is [verified] 2026-07-25 unless marked otherwise; install
syntax as a class is [drift-prone] — re-verify at release boundaries.

## The two-step rule (there is no direct install)

No channel installs a plugin in one step from a repo URL. A plugin is always installed FROM a
marketplace; the repo (or directory, or URL) is added as a marketplace first. [verified]
2026-07-25, discover-plugins.

```
/plugin marketplace add <source>
/plugin install <plugin-name>@<marketplace-name>
```

Example (this workspace): `/plugin marketplace add kimgranlund/claude-plugins` then
`/plugin install harness@nonoun-plugins`.

## Step 1 — every accepted `marketplace add` source form

| Source | Exact form | Notes |
|---|---|---|
| GitHub shorthand | `/plugin marketplace add owner/repo` | Repo must contain `.claude-plugin/marketplace.json`; a bare single-plugin repo needs a wrapper catalog (adopt-plugin's job) [verified] |
| Git URL, SSH — preferred | `/plugin marketplace add git@gitlab.com:company/plugins.git` | SSH over HTTPS: repeated HTTPS host failures 2026-07-22/25 [incident — this workspace; adopt-plugin SKILL] |
| Git URL, HTTPS | `/plugin marketplace add https://gitlab.com/company/plugins.git` | `https://` prefix mandatory — v2.1.196+ rejects prefix-less URLs with an error; older versions misread them as GitHub shorthand [verified] |
| Git URL + branch/tag | append `#ref`: `…plugins.git#v1.0.0` | Works with both https and ssh forms [verified] |
| Local directory | `/plugin marketplace add ./my-marketplace` | Loads `.claude-plugin/marketplace.json` from that dir; persistent, unlike `--plugin-dir` [verified] |
| Local marketplace.json | `/plugin marketplace add ./path/to/marketplace.json` | [verified] |
| Remote marketplace.json | `/plugin marketplace add https://example.com/marketplace.json` | [verified] |

Shortcuts: `/plugin market` ≡ `/plugin marketplace`; `rm` ≡ `remove`. [verified]

## Step 2 — install

```
/plugin install <plugin-name>@<marketplace-name>
```

`<plugin-name>` is the manifest's `name` field, never guessed from the repo or URL. [verified]

## npm and npx

There is NO npx install form and NO `npm install` CLI form for plugins — the absence is
documented, not an oversight; emitting one is hallucination. [verified absence] 2026-07-25,
cli-reference sweep. npm exists only as a plugin-LEVEL source inside a marketplace catalog
entry:

```json
{ "source": "npm", "package": "<name-or-@scope/name>", "version": "<semver-optional>", "registry": "<url-optional>" }
```

Never marketplace-level — `extraKnownMarketplaces` has no npm type; a marketplace catalog is
always a real `marketplace.json` resolved over github/git/directory/url. [verified] 2026-07-25
against code.claude.com/docs; adopt-plugin SKILL. npm's evolution here is [drift-prone] —
recapture next cycle.

## Local path — dev checkout (session-only)

```bash
claude --plugin-dir ./my-plugin                    # directory
claude --plugin-dir ./a --plugin-dir ./b.zip      # repeatable; .zip needs v2.1.128+
claude --plugin-url https://example.com/plugin.zip # hosted archive
claude -p --plugin-dir ./my-plugin "query"        # non-interactive scripted run
```

These load for THIS session only and write nothing to settings.json. Persistent local install
= the local-directory marketplace form above (or `"source": "directory"` in settings —
adopt-plugin). [verified] 2026-07-25, cli-reference. Scaffold alternative:
`claude plugin init <name>` → `~/.claude/skills/<name>/`, loads as `<name>@skills-dir` next
session. [verified]

## Non-interactive / CI

```bash
claude plugin install formatter@my-marketplace --scope project
claude plugin marketplace list
claude plugin marketplace update <marketplace-name>
claude plugin marketplace remove <marketplace-name>
```

`--scope` takes `user` (default) · `project` · `local`. No one-shot add-and-install chain is
documented [verified absence]; the working CI pattern is: commit `extraKnownMarketplaces` in
`.claude/settings.json` (adopt-plugin owns that wiring), then run the install command.
[verified] 2026-07-25, plugins-reference CLI section.
