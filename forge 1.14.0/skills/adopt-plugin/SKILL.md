---
name: adopt-plugin
description: >-
  Declares an external Claude Code plugin or plugin marketplace in a repo's
  .claude/settings.json so any contributor who trusts the repo is prompted to install it — no
  operator-local assumption. Use when the user asks to add a plugin repo so contributors can
  install it, declare a plugin marketplace in settings.json, set up extraKnownMarketplaces, wire
  up a list of skill/plugin URLs as installable dependencies, or asks why a plugin they just
  added to `enabledPlugins`/a marketplace declaration isn't showing up in /plugin. NOT for
  general settings.json edits with no plugin/marketplace object — permissions, env vars, model
  choice, hooks (`update-config`, where installed). NOT authoring a NEW plugin's manifest, or why
  an ALREADY-DECLARED plugin fails to load once Claude Code tries to read it
  (plugin-writing-rules). NOT building a plugin's skill/agent content (make-plugin). NOT
  deciding how an existing local surface should partition (plan-plugin-split).
disable-model-invocation: false
user-invocable: true
argument-hint: "[plugin/marketplace URL or list of URLs]"
---

# adopt-plugin

Produces a project-scoped `.claude/settings.json` (and, when needed, a self-hosted
`.claude-plugin/marketplace.json` wrapper) that makes one or more external plugin repos
installable by every contributor who trusts the project, portable past the authoring machine.

## Procedure

1. **Classify each URL.** Fetch `.claude-plugin/` at the repo root (`gh api
   repos/{owner}/{repo}/contents/.claude-plugin --jq '.[].name'`, or the raw path for non-GitHub
   hosts).
   - `marketplace.json` present → **marketplace repo**, go to step 2.
   - Only `plugin.json` present, no `marketplace.json` → **single-plugin repo**, go to step 3.
   - Neither present → report it as not a valid plugin source, exactly as classified.

2. **Marketplace repos → declare directly.** Add one `extraKnownMarketplaces` entry per repo:
   ```json
   "extraKnownMarketplaces": {
     "<marketplace-id>": {
       "source": { "source": "github", "repo": "<owner>/<repo>" },
       "autoUpdate": true
     }
   }
   ```
   If `marketplace.json` is not at the repo root, add `path` (pointing at it) and `sparsePaths`
   (the containing directory, keeping the clone sparse):
   ```json
   "source": {
     "source": "github", "repo": "<owner>/<repo>",
     "path": "sub/dir/.claude-plugin/marketplace.json",
     "sparsePaths": ["sub/dir"]
   }
   ```
   Other `source.source` values: `"git"` (needs `url`), `"directory"` (needs `path`, local
   only). There is no `"source": "settings"` inline-marketplace type — a marketplace's plugin
   list always lives in a real `marketplace.json` file at a real address, never inlined into
   `settings.json` itself.

3. **Single-plugin repos → wrap, never reference directly.** `extraKnownMarketplaces` cannot
   point at a bare plugin repo. Add the repo as one more entry in **one shared** self-hosted
   catalog at `.claude-plugin/marketplace.json` in the consuming repo itself:
   ```json
   {
     "name": "<your-catalog-id>",
     "owner": { "name": "<you or your org>" },
     "metadata": { "description": "Repo-hosted catalog wrapping single-plugin repos that have no marketplace.json of their own." },
     "plugins": [
       { "name": "<plugin-name>", "source": { "source": "github", "repo": "<owner>/<repo>" }, "description": "<one line>" }
     ]
   }
   ```
   Multiple single-plugin URLs are multiple `plugins[]` entries in this one file, not one
   wrapper file each. Because the file lives in the consuming repo, it needs no
   `extraKnownMarketplaces` entry of its own — checking out the repo is enough.

4. **Enable each plugin.** In every case, `enabledPlugins` takes `"<plugin-name>@<marketplace-id>"`.
   `<plugin-name>` is the `name` field from that plugin's **own** `plugin.json` (marketplace
   entries repeat it in `plugins[].name`) — never guessed from the repo or URL. `<marketplace-id>`
   is the key you chose in `extraKnownMarketplaces`, or your self-hosted catalog's own `name`.
   ```json
   "enabledPlugins": {
     "<plugin-name>@<marketplace-id>": true
   }
   ```

5. **Verify.** State the check as part of the output: `/reload-plugins` (or a restart) re-reads
   `settings.json`; `/plugin` should show each declared plugin with an install prompt (or
   already installed if `autoUpdate` fired); `~/.claude/plugins/installed_plugins.json` gets a
   new entry once a contributor accepts. A missing plugin's first suspect is the `<plugin-name>`
   match from step 4.

If the same marketplace already has an `extraKnownMarketplaces` entry, skip step 2/3 and only
add the new plugin's `enabledPlugins` line.

## Output contract

- The full `.claude/settings.json` diff (or new keys, if the file is being created).
- The full `.claude-plugin/marketplace.json` wrapper contents, if step 3 fired.
- One line per URL stating which path it took (direct marketplace vs. wrapped) and why.
- The verification steps from step 5, stated explicitly, not implied.

## Failure branches

- URL has neither `plugin.json` nor `marketplace.json` → report it as not a valid plugin
  source, exactly as classified.
- `<plugin-name>` can't be confirmed (manifest unreadable) → say so and leave the
  `enabledPlugins` line as a TODO, sourced only from a confirmed manifest read.
- Repo is private/unreachable for the classification fetch → ask for the manifest contents
  directly rather than assuming a shape.

Done when every URL has a `settings.json` (and, if needed, `marketplace.json`) entry that
matches its real classification, and the verification steps are stated in the output.

## Example

```
Bad  (fabricated shape — the failure mode this skill exists to prevent):
  "extraKnownMarketplaces": {
    "some-tools": {
      "source": {
        "source": "settings",
        "plugins": [{ "name": "some-plugin", "source": {"source": "github", "repo": "owner/some-plugin-repo"} }]
      }
    }
  }
  — "settings" is not a valid source type; this marketplace shape does not exist.

Good (wrapper catalog — the real mechanism for a repo confirmed single-plugin, step 1):
  .claude-plugin/marketplace.json:
    { "name": "your-catalog", "plugins": [
      { "name": "some-plugin", "source": {"source": "github", "repo": "owner/some-plugin-repo"} }
    ]}
  .claude/settings.json:
    "enabledPlugins": { "some-plugin@your-catalog": true }
```

Repo classification is a live fact, not a stable label — a repo can gain a `marketplace.json`
between one check and the next (verified live, 2026-07-15: a repo cited as single-plugin in an
earlier authoring pass had since added one). Step 1's fetch is the source of truth every time,
current at the moment it runs, not a memory of what the repo used to be.
