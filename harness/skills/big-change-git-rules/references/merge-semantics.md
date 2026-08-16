# Merge semantics — squash safety, remote-branch verification, CI as the gate

## Squash-merge makes the local worktree branch a safe-to-discard duplicate

[verified, standard git squash-merge semantics, applied in this workspace's own campaigns] A
squash merge folds every commit on the campaign branch into ONE commit on `main`. Once that
lands, the worktree's own branch — even with its full, unsquashed commit history — is a
duplicate: nothing on it is reachable from `main` that isn't already there in squashed form. This
is what makes `ExitWorktree`'s `discard_changes:true` safe, but the safety is CONDITIONAL on the
merge having actually landed — confirm state first (see `campaign-decision-tree.md`).

## The remote branch does not delete itself just because `gh` says it will

[incident, 2026-07-16, ten instances in one week] `gh pr merge --squash --delete-branch`
reported success on every one of ten worktree-campaign merges, but the remote branch survived
all ten — undetected until a manual `git branch -r` sweep. The mechanism was never fully
diagnosed (plausibly the same checkout-collision class as `worktree-mechanics.md`'s post-merge
error interfering with the delete step); the fix is not diagnosing the CLI's internals but
**never trusting the delete claim** — re-verify the branch is actually gone. `campaign_close.py`
(harness, issue #23, landed `ce05fcb`) mechanizes exactly this: delete, then re-check
`git ls-remote --heads`, and FAIL loudly if the branch is still there. Its own selftest carries
this exact scenario as a negative control (`verify_branch_deleted(existed_before=True,
exists_after=True, ...)` must return `False`).

## CI is the merge gate, not a courtesy check

[verified, ratified in ADR-0002] `.github/workflows/gate.yml` runs the same `release_gate.py` sweep locally
and in CI, over every plugin, on every push and PR — no CI-only logic. A PR is not "campaign
complete" until CI reads green on the PR itself, not just on a local pre-push run; local and CI
can diverge (a file staged locally but not pushed, an environment difference) and only the CI
run proves what the merge will actually contain.

## Auth-path consistency when closing a PR from outside its own checkout

[incident, 2026-07-17, caught pre-ship by a fresh-context audit] `campaign_close.py`'s first
draft checked remote-branch existence with an anonymous `git ls-remote` but performed the delete
with an authenticated `gh api` call. On a private repo closed via `--repo owner/repo` (i.e., not
from inside a clone of the target), the anonymous existence check fails closed (empty result,
misread as "already absent"), silently skipping the delete and reporting false-clean — the
ten-branch incident's failure mode, reincarnated through an auth-path seam instead of a CLI-tool
quirk. Fixed by routing both the existence check and the delete through the same authenticated
path when `--repo` is supplied (forge 1.30.0, `ce05fcb`).

## Squash-merging a parent with `--delete-branch` auto-closes its stacked children

[incident, 2026-08-16, PR #437 auto-closed as child of #424, re-opened as PR #439] In a stacked
PR chain (a child PR's base branch is the PARENT's campaign branch, not `main`), squash-merging
the parent with `--delete-branch` makes GitHub auto-CLOSE every open child PR whose base was that
now-deleted branch — and a PR closed this way, with its base branch gone, cannot be reopened
cleanly; it must be re-created as a new PR number (#437 became #439). Squash-merge also orphans
the child's own copy of the parent's commits (the parent's commits on the child branch are not
the same commits as the one squashed commit now on `main`), so a base retarget alone is not
enough — the child needs its history rebuilt against `main`, not just repointed at it.

**The rule for closing out a stacked chain, in order:**

1. Merge the parent (squash is fine).
2. Retarget every open child PR's base to `main`.
3. Rebase each child onto the parent's new squashed commit: `git rebase --onto origin/main
   <parent-old-tip> <child-branch>` — this drops the child's now-duplicate copies of the
   parent's commits and replays only the child's own commits on top of `main`.
4. Only THEN delete the parent's branch (`campaign_close.py`'s C2, or `--delete-branch`) — deleting
   it before step 2–3 is what triggers the auto-close.

Skipping the retarget-and-rebase and merging/deleting the parent first is the failure mode; doing
the rebase after the auto-close still recovers the work, but costs a PR renumbering and a lost
PR-comment thread.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| A worktree campaign branch survives on the remote after a reported successful merge | `gh`'s delete step failed silently — the ten-branch class | `campaign_close.py <pr> [--repo ...]`; never trust the merge command's own report |
| A branch check reports "already absent" but was never actually deleted | mismatched auth paths between the existence check and the delete (private repo, `--repo` invocation) | ensure both operations use the same authenticated client |
| A merge looked clean locally but CI is red on the PR | local and CI environments/state diverged | CI is the gate — do not treat a local pass as sufficient |
| A stacked chain's child PR auto-closes right after the parent merges, and can't be reopened | parent's branch (the child's base) got deleted before the child was retargeted+rebased | retarget child to `main` + `git rebase --onto origin/main <parent-old-tip>` BEFORE deleting the parent branch; if already closed, re-create as a new PR |
