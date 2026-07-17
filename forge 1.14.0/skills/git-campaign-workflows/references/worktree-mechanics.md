# Worktree mechanics — placement, gitignore, and the checkout-collision trap

## EnterWorktree places worktrees IN-repo, not out

[verified, this workspace's own tool contract, 2026-07-15] Claude Code's `EnterWorktree` creates
worktrees inside the current repo at `.claude/worktrees/<name>/`, on a fresh branch from
`origin/<default-branch>` by default. This falsified an earlier documented assumption in this
workspace (forge's repo-alignment razor originally claimed worktrees live "outside the repo
root by default") within hours of that claim shipping — amended in place the same day
(commit `e192f01`, forge 1.26.4: "the worktree-placement claim, falsified and amended same-day").
The corrected rule: **verify the ignore
rule exists; never assume placement.**

## The consequence: `.gitignore` must cover the worktree path, always

[incident, 2026-07-15] Because worktrees are in-repo, a missing `.claude/worktrees/` rule in
`.gitignore` means a stray `git add -A` in the main checkout would stage every open worktree's
contents. This workspace's own `.gitignore` gained the rule the same day the placement claim was
corrected — see `gitignore_check.py` (mechanized 2026-07-17, `forge/scripts/gitignore_check.py`,
issue #19) for the standing check that would have caught an unignored worktree dir before it bit.

## The post-merge checkout error is expected, not a failure signal

[verified, observed harness behavior repeated across every squash-merge this workspace ran] After
`gh pr merge --squash --delete-branch` from inside a worktree, `gh`'s attempted post-merge
`git checkout main` fails with `'main' is already used by worktree at '<main-checkout-path>'`.
This is **harmless** — the merge itself already succeeded remotely; the checkout attempt is
`gh`'s own convenience step colliding with the fact that `main` is checked out elsewhere. Verify
success independently (`gh pr view --json state` == `MERGED`), never by the checkout command's
own exit code.

## ExitWorktree discard-safety

[verified, this workspace's own tool contract] `ExitWorktree action:"remove" discard_changes:true`
refuses to run if the worktree holds uncommitted files or commits not on the original branch —
correct, since a squash-merge means the worktree's own commit history is now a duplicate of what
landed on main, safe to discard, but ONLY after independently confirming the PR state is
`MERGED` first (see `campaign-decision-tree.md` for the full sequencing). Discarding before that
confirmation risks losing work that never actually shipped.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| `.claude/worktrees/` contents show up in `git status` on main | the placement-assumption error, or a missing/stale ignore rule | run `gitignore_check.py`; add the rule if absent |
| `gh pr merge` reports the post-checkout error | expected — `main` is checked out in the primary working directory while the worktree also references it | ignore the checkout error specifically; verify merge state independently |
| `ExitWorktree` refuses to discard | uncommitted work, or commits diverged from what was actually merged | never override with force before confirming MERGED state — see `campaign-decision-tree.md` |
