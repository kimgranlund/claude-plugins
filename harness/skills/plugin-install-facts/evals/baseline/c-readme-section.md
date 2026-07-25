# Baseline C — no skill — 2026-07-25

## Installation

This plugin is distributed via the `kimgranlund/claude-plugins` marketplace repo. There are a few ways to install it, depending on whether you're a user or a developer working on the plugin itself.

### Option 1: Install from the marketplace (recommended)

From within Claude Code, add the marketplace and then install the plugin:

```
/plugin marketplace add kimgranlund/claude-plugins
/plugin install <plugin-name>@claude-plugins
```

You can also browse and install interactively:

```
/plugin
```

This opens the plugin manager UI, where you can search the added marketplace(s) and install plugins without typing the exact name.

### Option 2: Install directly from the GitHub repo

If you don't want to register the whole marketplace, you can point Claude Code at the repo directly:

```
/plugin marketplace add https://github.com/kimgranlund/claude-plugins
```

or, using the SSH form:

```
/plugin marketplace add git@github.com:kimgranlund/claude-plugins.git
```

Then install the specific plugin as in Option 1.

### Option 3: Local-path install (for development)

If you're developing the plugin locally (e.g., you've cloned the repo or are editing it in place), you can add the marketplace from a local directory instead of GitHub. This lets Claude Code pick up your changes without publishing anything:

```
/plugin marketplace add /absolute/path/to/claude-plugins
```

or, if you're already inside the repo:

```
/plugin marketplace add .
```

Then install the plugin from that local marketplace the same way:

```
/plugin install <plugin-name>@claude-plugins
```

Because it's a local path, Claude Code reads the plugin's manifest and files directly from disk — useful for iterating on a plugin before pushing it, since you can edit files and reload/reinstall to see changes without a git round-trip.

### Verifying installation

After installing, confirm the plugin is active:

```
/plugin
```

List installed plugins and marketplaces from this menu, or check your Claude Code settings file (typically `~/.claude/settings.json` or the project's `.claude/settings.json`) for an `enabledPlugins` / marketplace entry referencing this plugin.

### Updating

To pick up new versions after installing from a marketplace:

```
/plugin marketplace update kimgranlund/claude-plugins
/plugin update <plugin-name>
```

For a local-path install, updates are picked up automatically (or via a reload/reinstall) since the marketplace points straight at your working directory.

### Uninstalling

```
/plugin uninstall <plugin-name>
```

### Notes

- Replace `<plugin-name>` with this plugin's actual name as declared in its manifest.
- Marketplace names default to the repo name unless the marketplace manifest specifies otherwise — double check the `@<marketplace-name>` suffix matches what `/plugin marketplace add` reports back.
- If you maintain multiple Claude Code profiles or work across several projects, note that plugin installs can be scoped globally (user settings) or per-project — check which scope you intend before installing.
