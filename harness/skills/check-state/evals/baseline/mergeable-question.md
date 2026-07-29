Permission allow rule (.claude/settings.json): Write(.claude/ops/watch-checkpoint.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/watch-checkpoint.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/friendlies.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/friendlies.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/held-items.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/held-items.md) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/reports/*.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/reports/*.md) instead (Edit rules cover all file-editing tools).
Verdict: 12 remote branches are merged and deletable, 1 local branch is deletable, 1 branch must stay (open PR), and this session's worktree stays (it holds live work).

**Deletable — remote branches whose PRs are MERGED** (the known silent-delete-failure class: GitHub merged them but the branches were never cleaned up):

1. `feat/skip-worktree-silent-failure` (#110), `feat/rams-braun-voice-doctrine` (#108), `fix/post-diet-routing-repair` (#107), `fix/corpus-of-record-wording` (#105), `fix/campaign-close-c2-race` (#104)
2. `fix/record-line-detection` (#103), `fix/retire-inert-alias-guard` (#101), `feat/register-alias-guard` (#100), `fix/path-component-guard` (#99)
3. `worktree-rename-migration` (#98), `worktree-plugin-install-facts` (#93), `fix/trim-skill-agent-descriptions` (#92)

**Deletable — local branch:** `fix/trim-skill-agent-descriptions` (PR #92 merged via squash, so `git branch --merged` doesn't list it, but its content is in main). Delete with `git branch -D`.

**Keep:**
- `fix/enabled-plugins-observed-precedence` — PR #109 is still OPEN. Merge or close the PR first.
- Worktree `.claude/worktrees/check-state-skill` + branch `worktree-check-state-skill` — that's this session's worktree, at main's tip with the untracked `harness/skills/check-state/` skill in progress. Removing it now would drop that work.

The repo's own doctrine says the cleanup path is `campaign_close.py <pr#> --repo <owner/repo> --gate ...` per merged PR — it verifies MERGED, deletes the remote branch, and re-verifies the delete actually landed.

State: read-only survey done, nothing touched. Next 2-minute action: say the word and I'll run `campaign_close.py` across the 12 merged PRs (or just batch-delete the branches directly if you'd rather skip the per-PR gates).
