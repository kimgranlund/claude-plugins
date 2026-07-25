# Baseline B — no skill — 2026-07-25

Short answer: no, not directly. Claude Code plugins aren't installed with `npx` or `npm install` — they're installed from inside Claude Code itself, through its plugin/marketplace system.

**How Claude Code plugins actually get installed:**

1. Add a marketplace (a git repo or URL that lists available plugins), then install a plugin from it, using the `/plugin` command inside a Claude Code session:
   ```
   /plugin marketplace add <owner>/<repo>
   /plugin install <plugin-name>@<marketplace-name>
   ```
   or, for a marketplace hosted at a URL:
   ```
   /plugin marketplace add https://example.com/path/to/marketplace.json
   ```

2. Alternatively, a plugin (or its marketplace) can be declared directly in `.claude/settings.json` (or the user-level settings file), typically under something like `extraKnownMarketplaces` / `enabledPlugins`, so that it's installed automatically when Claude Code loads that config.

**Where npm/npx DOES come in:**

- `npm`/`npx` is how you install and run *Claude Code itself* (the CLI), e.g.:
  ```
  npm install -g @anthropic-ai/claude-code
  ```
  or a one-off run via:
  ```
  npx @anthropic-ai/claude-code
  ```
- But once Claude Code is running, its *plugins* (which bundle skills, agents, hooks, slash commands, etc.) are a Claude-Code-specific concept, distributed via git-based marketplaces, not published as npm packages. There isn't an `npm install <claude-plugin>` or `npx <claude-plugin>` command for installing a Claude Code plugin.

If you have a specific plugin in mind, the exact steps depend on how its author distributes it (a GitHub repo you add as a marketplace being the most common pattern), but the install verb is always `/plugin marketplace add …` + `/plugin install …` inside Claude Code, not `npm`/`npx`.

(Caveat: I'm answering from general knowledge of Claude Code's plugin system as I understand it; if Anthropic's current docs describe a different or newer install flow, those docs should take precedence over this answer.)
