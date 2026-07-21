# PR lifecycle and review mechanics

## Draft PRs: CI runs, review requests don't

[verified, docs.github.com, 2026-07-17] A draft PR **cannot be merged**, and **does not**
automatically request CODEOWNERS review. [verified] CI still runs on it — the `pull_request`
webhook event fires on `opened`/`synchronize`/`reopened` regardless of draft state, plus a
dedicated `converted_to_draft` activity type. Marking a draft "ready for review" is what triggers
the CODEOWNERS request. Net: a draft PR is not a "paused" PR from CI's perspective — checks
already run against it; it's paused only from the human-review-request perspective.

## Review states: only one of three actually gates a merge

[verified, docs.github.com, 2026-07-17] Three submission states: **Comment** (feedback, no
verdict), **Approve**, **Request changes**. [verified] "Request changes" is "purely informational
and will not prevent merging unless a ruleset or classic branch protection rule is configured" to
require it — a reviewer requesting changes has no automatic teeth without a repo-level setting.
[verified] Authors cannot approve their own PRs. [verified] An approval can be dismissed if the PR
changes significantly after it was given, forcing re-review. [verified] Repo owners/admins can
bypass required reviews entirely, including a stale reviewer who left the org.

## CODEOWNERS

[verified, docs.github.com, 2026-07-17] Auto-requested when a PR touches code a CODEOWNERS entry
covers. Can be made a hard merge requirement via branch protection. **Must live on the base
branch** to take effect (a CODEOWNERS file only on a feature branch does nothing). When multiple
owners cover the same code, **any one** of their approvals satisfies the requirement.

## Required status checks

[verified, docs.github.com, 2026-07-17] Configurable per protected branch; a check must have
completed successfully **within the past 7 days** to count as satisfying the requirement (a stale
green check outside that window doesn't count). Job names must be **unique across workflows** —
two workflows using the same job name produce ambiguous status results that can block merges
unpredictably. [unconfirmed] The exact numeric range for "required number of approvals" (the UI
exposes a dropdown; the bound itself wasn't found in docs).

## Merge queue — not the same as "just merging"

[verified, docs.github.com, 2026-07-17] A merge queue processes PRs **FIFO**, grouping each queued
PR's changes into a temporary branch **already rebased against the latest base + everything ahead
of it in queue**, running required checks against that combination — not against the PR's own
stale branch. A PR that develops a conflict or fails a check while queued is **auto-removed** with
a notification. Its main value: the PR author never has to manually update-and-rebase while
waiting — GitHub does it as part of queue processing. Recommended specifically for branches with
high daily merge volume.

## The three merge strategies — mechanically distinct, not just a UI preference

[verified, docs.github.com, 2026-07-17]

| Strategy | What lands on the base branch | History shape |
|---|---|---|
| **Merge commit** (default) | Every source commit + one new merge commit | Preserves branch topology |
| **Squash** | One new commit combining all of the PR's commits | Flattens the branch to a single point; original commit-by-commit history is gone from the base branch |
| **Rebase** | Every source commit, individually, no merge commit | Linear, fast-forward-shaped |

[verified] GitHub's rebase-and-merge is **not identical to `git rebase`**: GitHub's version always
generates **new commit SHAs and updates committer info**, whereas a local `git rebase` on top of an
ancestor commit does not touch committer info. Don't assume SHA continuity survives a GitHub
rebase-merge.

This matters directly for `linking-and-closing-keywords.md`'s unresolved gap: squash's
auto-generated (but user-editable) commit message is the one place a closing keyword could be
silently dropped by an editor before merge — worth a glance before assuming the auto-close fired.
