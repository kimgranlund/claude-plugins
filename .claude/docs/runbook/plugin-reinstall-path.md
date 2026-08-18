# Runbook — plugin reinstall path (from a fresh clone of `origin/main`)

Owed-at-lock mitigation for ADR-0022 ("the repo is the backup") exception 2 — plugin
cache/installed-plugin state. Source: `.claude/docs/adr/0022-repo-is-the-backup.md`, seeded at
gh#627's second comment (PR #628's repair pass). No secrets here — this doc names paths and
commands only.

## What is and isn't already reconstructible

The repo's own `.claude/settings.json` is **tracked and committed** (verified: `git ls-files
.claude/settings.json` lists it; `git check-ignore` finds no rule hiding it). It already carries,
declaratively, both pieces a fresh machine needs:

```json
"enabledPlugins": {
  "harness@nonoun-plugins": true,
  "docs@nonoun-plugins": true,
  "teamwork@nonoun-plugins": true,
  "authorkit@nonoun-plugins": true,
  "screens@nonoun-plugins": true,
  "agent-protocols@nonoun-plugins": true,
  "llm@nonoun-plugins": true,
  "design@nonoun-plugins": true
},
"extraKnownMarketplaces": {
  "nonoun-plugins": { "source": { "source": "github", "repo": "kimgranlund/claude-plugins" },
                      "autoUpdate": true }
}
```

So the marketplace registration and the enabled-plugin roster are **committed, not an exception**
— exception 2 is narrower than the ADR's draft framing suggested: only the DOWNLOADED CACHE
ARTIFACTS under `~/.claude/plugins/cache/nonoun-plugins/<plugin>/<version>/` are actually
unrecoverable-from-clone-alone; the declaration of what to install is already in the repo.

## The reinstall path, in order

1. **Clone this repo** onto the fresh machine (`git clone git@github.com:kimgranlund/claude-plugins.git`
   or the HTTPS form — `harness:plugin-install-facts`' `references/channel-choice.md` covers the
   choice).
2. **Open a Claude Code session with this repo as the working directory (or a project scope
   pointed at it).** Claude Code reads the repo's own `.claude/settings.json` — the
   `extraKnownMarketplaces` entry above registers the `nonoun-plugins` marketplace automatically;
   no manual `/plugin marketplace add` is needed for THIS repo's own plugins, because the
   declaration already ships in the clone.
3. **Trust prompt.** First use of any of these 8 plugins in the fresh session prompts for trust
   (installing is running code) — confirm it once per plugin per
   `harness:plugin-install-facts`' `references/install-lifecycle.md`.
4. **Verify the installed set matches the manifest roster** — the 8 plugin directories at this
   repo's root (`harness`, `docs`, `teamwork`, `authorkit`, `screens`, `agent-protocols`, `llm`,
   `design`), each with its own `.claude-plugin/plugin.json`. If a plugin fails to auto-resolve
   from the committed `enabledPlugins` map, install it explicitly:
   ```
   /plugin install <plugin-name>@nonoun-plugins
   ```
   (exact per-plugin command form, and the git/npm/local-path/CI variants: `harness:
   plugin-install-facts`' `references/install-commands.md` — this runbook doesn't restate those
   verified commands, it cites the pack that owns them so this file never goes stale
   independently of that corpus).
5. **`autoUpdate: true`** on the marketplace entry means a subsequent `/plugin` refresh (or the
   platform's own periodic check) pulls each plugin's latest shipped version from `origin/main`
   without a manual bump per plugin — this is the mechanism that keeps a freshly reinstalled set
   converging on what's actually on `main`, not whatever was cached at clone time.

## What this runbook does NOT cover

- The exact install-command syntax per channel (github/git/local/npm/CI) — that's
  `harness:plugin-install-facts`'s own corpus, cited above, never duplicated here (single
  source of truth; this runbook would go stale independently if it forked a copy).
- Anything about *credentials* needed to clone or authenticate — that's the separate
  credential-reissuance runbook (`credential-reissuance-runbook.md`, same directory), exception 3.
- The exact mitigation mechanism for exception 4 (user-scoped `~/.claude`/`~/.config` state
  outside any one repo's plugin roster) — ADR-0022 leaves that mechanism open at ratification;
  this runbook is scoped to exception 2 only.

## Verification

`harness:check-reconstructibility`'s audit script checks for this file's own presence at
`.claude/docs/runbook/plugin-reinstall-path.md` as exception 2's mitigation-doc gate — its
absence is reported as a DEFECT (mitigation owed-at-lock, not shipped); its presence reports
exception 2 as enrolled-with-mitigation, citing this path.
