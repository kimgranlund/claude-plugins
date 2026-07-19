# Baseline — busy session, no skill installed

## Setup
A session has been working in a git worktree: fixed a real bug (uncommitted, gate-clean), found
a second unrelated issue worth filing separately, and along the way repeated a correction about a
convention it had already been told twice before this session. Prompted with the user's own
prior, unassisted phrasing: "write any new issues or PR otherwise prepare to close this session."

## Observed behavior (no skill)
Claude states in prose that it will "write up the issue and open a PR," opens a PR for the bug fix
(reasonable), but:
- Never checks whether the PR it opened is gate-clean or whether CI actually ran — it's stated as
  done immediately after the `gh pr create` call returns a URL, with no re-read.
- Files the second, unrelated issue as a comment inside the SAME PR rather than its own Issue,
  because "write any new issues or PR" was read as one combined action, not two decisions per
  finding.
- Does not surface the repeated correction as a knowledge-harvest candidate at all — it isn't
  named as a category, so nothing prompts noticing the pattern's third occurrence.
- Ends with "I've wrapped up the session, let me know if there's anything else" — no verdict
  naming what was captured, no confirmation the writes actually landed, and no distinction between
  "I checked and there's nothing else" and "I didn't check."

## Gap this baseline demonstrates
The old prompt gets *something* written, but with no verification loop, no per-finding decision
(bug vs. follow-up vs. durable knowledge each want a different record), and no way for the user to
tell whether the close-out was thorough or just performative.
