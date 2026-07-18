# Baseline — assertion 3 (steelman self-review before filing)

Prompt: "Write a short code review for this function... Give me your final review report, ready to
post as a PR comment" (a `_remote_branch_exists` helper).

## Fresh-session output (no skill), 2026-07-18

Verdict: needs changes. Two blocking findings, both sourced against the real GitHub REST API docs
and git-ls-remote(1):

1. (Blocking) Wrong GitHub endpoint — the plural `refs/heads/{branch}` path is a prefix-matching
   list endpoint, not an exact match; `_remote_branch_exists("issue-39", ...)` would return True
   merely because `issue-39-reviewer-discipline` exists. Fix: the singular `git/ref/heads/{branch}`
   endpoint.
2. (Blocking) Any check failure (network blip, rate limit, expired auth) collapses to "branch
   absent" in both code paths — traced through the real caller in campaign_close.py to show this
   can silently skip a delete OR falsely report "deleted and reverified gone."

Plus one minor (no `timeout=` on either subprocess call) and one explicitly-checked non-issue
(argv-list interpolation isn't shell-injectable).

## Note on this baseline

This is the clean "before" case — no visible self-check step. The report goes straight from reading
the function to a confident, fully-formed verdict with two blocking findings; there is no stated
attempt to imagine what the function's author would say back before filing (e.g. "the author might
argue the plural endpoint is fine because branch names in this repo are never prefixes of each
other — is that true?" is exactly the kind of anticipated-rebuttal check that could have either
strengthened finding #1 with that caveat addressed, or surfaced it as a real open question instead
of an unqualified "blocking"). The findings themselves look sound on inspection, but nothing in the
transcript shows the reviewer checking its OWN claims against a rebuttal before treating them as
final — this is the gap assertion 3 targets, and this baseline shows it plainly.
