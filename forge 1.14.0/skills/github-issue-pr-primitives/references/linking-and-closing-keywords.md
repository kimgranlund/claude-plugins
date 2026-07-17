# Linking and closing keywords — the `Closes #N` mechanics, and where the docs stop confirming

## The nine keywords and their syntax

[verified, docs.github.com, 2026-07-17] Exactly nine keywords auto-link and auto-close:
`close`/`closes`/`closed`, `fix`/`fixes`/`fixed`, `resolve`/`resolves`/`resolved`. Case-insensitive,
an optional colon is allowed (`Closes: #10` works same as `Closes #10`). Cross-repo:
`owner/repo#N`. Multiple in one description: `Resolves #10, resolves #123, resolves org/repo#100`.

## The one hard gate: default branch only

[verified, docs.github.com, 2026-07-17] "The special keywords... are interpreted only when the
pull request targets the repository's default branch. If the pull request targets any other
branch, then these keywords are ignored, no links are created, and merging the PR has no effect on
the issues." This is the single most important operational fact in this file — a keyword in a PR
against a release branch or a feature-integration branch silently does nothing.

## Linking happens at PR-open time; closing happens at merge time

[verified, docs.github.com, 2026-07-17] These are two separate events: the link (visible in the
Issue's sidebar) forms as soon as a default-branch-targeting PR carries the keyword; the actual
close fires only when that PR is **merged** into the default branch. [verified] Keywords also work
in individual **commit messages**, not just the PR description — closing still fires on merge, but
a commit-message-only keyword does NOT register the PR as a "linked pull request" in the Issue's
sidebar (a real UI/traceability gap between the two placements).

## The merge-strategy gap this pack's own research could NOT close

[unconfirmed, 2026-07-17] GitHub's docs leave one specific question open: for each of the three
merge strategies (merge commit / squash / rebase — see `pr-lifecycle-and-review.md`), does closing
fire identically? No source directly tests all three strategies end-to-end.

[inferred, 2026-07-17] What's independently confirmed and composed here: (a) squash merge produces
an **editable** auto-generated commit message (single-commit PRs inherit that commit's message;
multi-commit PRs get a composed message listing all commits) — if a keyword survives into that
final message, closing should fire, by the same commit-message rule above; (b) a 2025-04-23
changelog entry establishes auto-close is a **repository-level toggle, independent of which merge
strategy is used for any given merge** — strongly implying strategy doesn't gate the behavior.
**Treat "all three merge strategies trigger auto-close identically" as [inferred], not
[verified]** — this is exactly the class of gap that produced two wrong facts elsewhere in this
project the same week; if a decision becomes load-bearing on this specific point, verify it
empirically (a throwaway repo, one PR per strategy) before shipping automation that depends on it.

## Other unconfirmed edges (flagged, not resolved)

[unconfirmed] Whether keywords work in **draft** PRs at all (no doc found either way — the default
branch rule presumably still applies, but this wasn't independently verified). [unconfirmed] The
exact moment linking registers (PR creation vs. first push vs. description edit save).

## Auto-close is a repo-level toggle — don't assume it's always on

[verified, docs.github.com, 2026-07-17] Settings → General → Issues → "Auto-close issues with
merged linked pull requests" — repo admins can disable this entirely. **A workspace's PR-merge-as-
work-item-close assumption (this workspace's own ADR-0002 ruling) depends on this setting being
left at its default-on state** — worth a one-time check per repo the git-native backend is ruled
into, not an assumption.

## Push-access requirement for cross-repo closing

[verified, docs.github.com, 2026-07-17] Closing an issue in a *different* repo via keyword requires
the PR author to have push access to that target repo — a cross-org sub-issue/PR pairing (see
`sub-issues-and-task-lists.md`) can silently fail to auto-close if that access is missing.
