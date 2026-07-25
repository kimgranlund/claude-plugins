# Channel choice — which install path fits which situation

Ask this file: "which install method should I use / recommend?" Distilled from wave 1
(2026-07-25); sources: code.claude.com/docs (discover-plugins, plugins, plugins-reference) +
this workspace's adopt-plugin rulings. All rows [verified] 2026-07-25 unless marked.

## The decision table

| Situation | Channel | Why (the rationale that licenses deviation) |
|---|---|---|
| Solo dev iterating on a plugin checkout | `claude --plugin-dir ./plugin` | Session-only, zero settings pollution, instant reload next launch; persistence would just go stale against the working tree |
| Solo use across projects, stable plugin | user-scope install: `/plugin install name@marketplace` (default `--scope user`) | Lands in `~/.claude/settings.json`, follows you everywhere, no team blast radius |
| Team distribution from a repo | project-scope: `extraKnownMarketplaces` in `.claude/settings.json` (adopt-plugin wires it), contributors get an install prompt on trust | The repo itself carries the declaration; every contributor who trusts it gets the same roster |
| Private repo, any host | git SSH source: `git@host:owner/repo.git` | SSH auth works where HTTPS flaked repeatedly (2026-07-22/25 [incident]); private-repo HTTPS auth adds token friction SSH doesn't |
| Public release, third-party author | community marketplace `anthropics/claude-plugins-community` | Automated validation + safety screening; SHA-pinned catalog, CI bumps the pin; submission via platform.claude.com/plugins/submit (individual) or claude.ai admin (Team/Enterprise org) |
| Public release, hoping for official | official marketplace `claude-plugins-official` | Anthropic-curated, discretionary — no application process; route through community and let quality argue |
| Plugin distributed as an npm package | plugin-level `"source": "npm"` entry in its wrapper marketplace catalog | The ONLY npm involvement that exists; there is no npm-hosted marketplace and no npx install (install-commands.md) |
| One-off try of a hosted archive | `claude --plugin-url https://…/plugin.zip` | No marketplace ceremony for a single evaluation session |

## Defaults this workspace has ruled (deviation doctrine applies)

- SSH `git@` over `https://` for every git source — grounded in the 2026-07-22/25 host-flakiness
  incidents [incident]. Where that rationale doesn't hold (a host whose working auth path IS
  HTTPS), HTTPS is a legal choice, not a violation.
- Team distribution goes through the repo's own settings.json declaration (adopt-plugin), never
  ad-hoc per-teammate marketplace adds — the repo is the source of record for its own tooling
  roster. [inferred from adopt-plugin's charter + ADR-0002's records-in-repo doctrine]

## Anti-recommendations

- Never recommend `npm install <plugin>` / `npx <plugin>` as an install path — no such form
  exists [verified absence, 2026-07-25].
- Never recommend `--plugin-dir` for team or persistent use — session-only by design; the
  persistent local path is a directory-source marketplace.
