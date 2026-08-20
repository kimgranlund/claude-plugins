# Campaign close + main sync mechanics

**Path scope:** the act of closing a merged campaign PR, or pulling parallel-session work into a
dirty `main` — not a file path.

- **Close every campaign PR with
  `python3 harness/scripts/campaign_close.py <pr-number> --repo <owner/repo> --gate <plugin-root>...`**
  — verifies the PR is MERGED, deletes the remote branch and REVERIFIES it is gone (the
  ten-branch silent-delete-failure class, 2026-07-16), and runs the release gate on every touched
  plugin. Never hand-verify a delete by the command's own print.
- **A dirty `main` before pulling parallel-session work: `python3 harness/scripts/sync_main.py
  --repo-root <path>`** — quarantines local dirt as a named stash, `--ff-only` pulls, and
  reverifies HEAD by SHA. Never trust a command's print alone; the SHA re-read is the check.
- EnterWorktree worktrees live in-repo at `.claude/worktrees/` (gitignored). Retiring a path a
  `.gitignore` rule names: `.claude/rules/gitignore-repair.md`.

Split from CLAUDE.md's campaign row (entry-file overhaul, 2026-08-19).
