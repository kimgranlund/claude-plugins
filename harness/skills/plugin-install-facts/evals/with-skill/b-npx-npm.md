# With-skill B — 2026-07-25

**No.** There is no `npx` install form and no `npm install` CLI form for Claude Code plugins — this is a documented absence, not a gap (`references/install-commands.md`, [verified absence] 2026-07-25, cli-reference sweep).

npm only appears as a plugin-LEVEL *source* inside a marketplace catalog entry (a `marketplace.json` object), never as a marketplace-level or CLI-level install form:

```json
{ "source": "npm", "package": "<name-or-@scope/name>", "version": "<semver-optional>", "registry": "<url-optional>" }
```

Every plugin install still goes through the same two-step sequence — add the marketplace, then install from it — regardless of what backs the marketplace catalog:

```
/plugin marketplace add <source>
/plugin install <plugin-name>@<marketplace-name>
```

**Precondition/failure mode:** `extraKnownMarketplaces` has no npm type — a marketplace itself is always a real `marketplace.json` resolved over github/git/directory/url; npm can only sit *inside* one of those catalogs as a per-plugin source, never stand in for the marketplace itself. Emitting a bare `npx`/`npm install` command for a plugin would be hallucination against this corpus.

Cited file: `references/install-commands.md`. npm's install form is marked `[drift-prone]` in the corpus — re-verify at the next release boundary.
