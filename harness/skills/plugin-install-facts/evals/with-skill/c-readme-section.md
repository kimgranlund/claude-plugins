# With-skill C — 2026-07-25

## Install

This plugin ships from the `kimgranlund/claude-plugins` marketplace repo. Every channel below
installs the SAME plugin — pick the one that fits your setup. Replace `<plugin-name>` with the
manifest's `name` field (never guess it from the repo or a directory name).

### 1. Standard install (most users)

```
/plugin marketplace add kimgranlund/claude-plugins
/plugin install <plugin-name>@nonoun-plugins
```

Preconditions, in order:
- The repo must contain `.claude-plugin/marketplace.json` at its root — `kimgranlund/claude-plugins`
  already does, so the GitHub shorthand (`owner/repo`) works directly.
- First use prompts for trust — installing is running code; expect and confirm the workspace-trust
  dialog. Trust recurs on every update, not just the first install.
- `<plugin-name>` must match the manifest's `name` field exactly.

### 2. Git URL, as an alternative to the GitHub shorthand

```
/plugin marketplace add git@github.com:kimgranlund/claude-plugins.git
/plugin install <plugin-name>@nonoun-plugins
```

Use the SSH form (`git@…`) over `https://` where possible — this workspace hit repeated HTTPS
host failures (2026-07-22/25). If HTTPS is the working path in your environment, it's a valid
substitute:

```
/plugin marketplace add https://github.com/kimgranlund/claude-plugins.git
/plugin install <plugin-name>@nonoun-plugins
```

Precondition: the `https://` prefix is mandatory on this form — Claude Code v2.1.196+ rejects a
prefix-less URL with an error, and older versions misread it as GitHub shorthand instead.
Append `#ref` (e.g. `…claude-plugins.git#v1.0.0`) to pin a branch or tag; works with both forms.

### 3. Local path — development checkout

For contributing to or testing the plugin from a local clone, two options:

**Session-only** (loads for this session only, writes nothing to settings.json):

```bash
claude --plugin-dir ./claude-plugins/<plugin-name>
```

**Persistent** (survives across sessions, same two-step shape as channel 1):

```
/plugin marketplace add ./claude-plugins
/plugin install <plugin-name>@nonoun-plugins
```

Precondition: point `--plugin-dir` at the plugin's own directory, not the marketplace repo root;
point `marketplace add` at the repo root (or a `marketplace.json` path) for the persistent form.
Trust still applies on first load either way.

### 4. Non-interactive / CI

```bash
claude plugin install <plugin-name>@nonoun-plugins --scope project
```

Precondition: this form does not add the marketplace for you — commit `extraKnownMarketplaces`
in `.claude/settings.json` first (a one-time step, not part of this command), then run the
install above. `--scope` takes `user` (default), `project`, or `local`.

### Not applicable to this plugin

There is no `npx` or `npm install` CLI form for Claude Code plugins — that channel only exists
as a plugin-level `"source": "npm"` entry inside a marketplace catalog, not as a way an end user
installs from the command line. Since this plugin ships from a git-hosted marketplace repo, that
channel doesn't apply here.
