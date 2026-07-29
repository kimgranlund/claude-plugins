Permission allow rule (.claude/settings.json): Write(.claude/ops/watch-checkpoint.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/watch-checkpoint.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/friendlies.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/friendlies.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/held-items.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/held-items.md) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/reports/*.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/reports/*.md) instead (Edit rules cover all file-editing tools).
**Verdict: 🟢 healthy overall — 2 decisions blocked on you, plus 12 merged branches waiting on cleanup.**

## Blocked on you

1. **PR #109** (plugin-install-facts enablement fix) — open, gate green, no review recorded. Needs your merge call. ~2 min.
2. **`github_mcp_offer` decision** — ops plan entry 1: every unattended issue-sorter run has re-deferred it; needs one interactive `/issue-sorter` round (or a direct ruling) to land in `friendlies.json`. ~10 min.
3. **This worktree's forge** — the `check-state` skill (which, fittingly, is the skill for exactly the question you just asked) is mid-`/make-skill`: P0–P1 passed, P2 evals in progress (`evals.json` + baseline exist, gate not marked), P3–P5 pending. Blocked only on continuing the session.

## Ready to close (zero risk)

- **All 12 non-main remote branches have MERGED PRs** (#92–#110 range) — the known silent-delete-failure class. Owner: `campaign_close.py` / repo-cleaner sweep.
- Local branch `fix/trim-skill-agent-descriptions` (PR #92 MERGED) — deletable.

## Drift / attention 🟡

- **`adr-checkpoint.json` stale** — tracks ADR-0001–0005 only; 0006/0007/0008 ratified but never swept. Owner: `decision-watcher` (ops plan entry 2).
- **Issue #96** (bug, minor) — "2 errors during load" from /reload-plugins, root cause unconfirmed, open since 07-27.
- Ops plan entry 3 flags a stale cloud-routine dispatch prompt (`ops-issues.md`).

## Raw counts

Open PRs: 1 · Open issues: 1 · Worktrees: 2 (main + this one, both clean) · Stashes: 0 · Working tree: only the untracked `check-state` skill-in-progress.

**State: mid-forge on check-state, estate otherwise quiet. Next 2-min action: merge PR #109 (`gh pr merge 109 --squash`) — then a repo-cleaner sweep can clear all 12 dead branches in one pass.**
