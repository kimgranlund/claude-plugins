# Baseline A — no skill — 2026-07-25

To install a Claude Code plugin from a GitHub repo, you first add the repo as a marketplace (or plugin source), then install the plugin from it. Here's the general flow:

1. **Add the GitHub repo as a marketplace source:**

```
/plugin marketplace add owner/repo
```

You can also pass a full URL if it's not on GitHub or you want to be explicit:

```
/plugin marketplace add https://github.com/owner/repo
```

2. **Install the plugin from that marketplace:**

```
/plugin install plugin-name@owner/repo
```

(The `plugin-name` is whatever the plugin is called in its `.claude-plugin/plugin.json` manifest — check the repo's README or marketplace listing if you're not sure of the name.)

3. **Verify it's installed:**

```
/plugin list
```

or just open the plugin manager UI:

```
/plugin
```

### Notes

- If the repository itself *is* a single plugin (not a marketplace with multiple plugins), some setups let you add and install it more directly — but the safest, most universal path is still: add it as a marketplace, then install by name.
- For a private repo, make sure you have `git` access configured (SSH key or a GitHub token) since Claude Code will need to clone it under the hood.
- You can also declare plugins/marketplaces in your `settings.json` (under something like `extraKnownMarketplaces` / `enabledPlugins`) if you want the install to be automatic/checked-in for a team, rather than run interactively via `/plugin` commands.
- After installing, you may need to restart Claude Code (or start a new session) for the plugin's skills, commands, and agents to become available.

If you tell me the specific repo and plugin name, I can give you the exact commands to run.
