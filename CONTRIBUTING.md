# Contributing

This repo hosts eight Claude Code plugins. Read the root [`CLAUDE.md`](CLAUDE.md) first — it's
the routing table for which command owns which job, and the operating rules for working *on*
these plugins rather than just installing them. Each plugin's own `CLAUDE.md` and README footer
ledger carry its per-plugin invariants and version history.

## Workflow (ADR-0002 — git-native execution)

- **Work items are GitHub Issues.** File a bug, feature, or chore as an Issue (`.github/ISSUE_TEMPLATE/`
  has forms for each). `docs/tickets/` is retired for new work in this workspace.
- **A campaign runs on its own branch + git worktree, a PR is the merge gate.** Opt into a
  worktree for multi-session or parallel work; a solo single-file fix may commit straight to
  `main`. See [`.claude/docs/adr/0002-git-native-execution.md`](.claude/docs/adr/0002-git-native-execution.md)
  for the full decision record.
- **Ship only through the gate.** Before opening a PR, run:

  ```bash
  python3 harness/scripts/release_gate.py <plugin-root>
  ```

  for every plugin your change touches. This runs manifest/structure checks, the full lint
  sweep, bundled selftests, an eval-suite check, and docs-freshness (G1–G11) — the same checks
  CI runs in [`.github/workflows/gate.yml`](.github/workflows/gate.yml) on every push and PR.
  Never hand-edit `dist/` — it's gate output.
- **Close a campaign with:**

  ```bash
  python3 harness/scripts/campaign_close.py <pr-number> --repo <owner/repo> --gate <plugin-root>...
  ```

  It verifies the PR merged, deletes the remote branch and re-verifies it's gone, and re-gates
  every touched plugin.
- **A drifted local `main` before pulling parallel work:**

  ```bash
  python3 harness/scripts/sync_main.py
  ```

  Quarantines local dirt as a named stash, `--ff-only` pulls, and reverifies `HEAD` by SHA.

## Invariants

- Bump the version and log it in the plugin's README footer ledger on every change — the
  version is the update cache key, and a version is never re-shipped.
- A description edit that affects routing (a skill/command/agent's model-invocable text)
  updates that plugin's `evals/evals.json` in the same change.
- Every bundled `scripts/*.py|mjs|js` carries a `selftest` mode that stays green.
- No plugin name or skill name contains `claude` or `anthropic` anywhere — the install
  rejects it and the whole plugin fails to load.

These are enforced by `release_gate.py` and CI, not by review discipline alone.
