# The ADR-0002 decision tree — solo-main-direct vs. campaign, and what was rejected

## The ratified split

[verified, ratified in ADR-0002, this workspace] Two lanes, chosen by scope, not by how the request feels:

- **Solo, single-file fix** → commit directly to `main`. No branch, no worktree, no PR. The
  overhead of a full campaign for a one-line, one-file change is pure ceremony; ADR-0002
  explicitly preserves this lane.
- **Campaign** (multi-file, multi-session, or work that could collide with a parallel session)
  → branch + git worktree + PR. The PR is the merge gate; CI (`gate.yml`) runs the same
  `release_gate.py` sweep the campaign ran locally, over every plugin, on push/PR.

The dividing line is genuinely "does this touch more than one file, or could it collide with
someone else's in-flight work" — not perceived importance or risk. A one-line fix to a
catastrophic bug is still solo-main-direct if it's genuinely one file; a five-file cosmetic
cleanup is still a campaign if it spans files a parallel session might also be touching.

## Branch protection on `main`: not an ADR-0002 ruling — a reasoned inference from it, recorded

[inferred, this session, 2026-07-17 — NOT part of ADR-0002 itself; `.claude/docs/adr/0002-git-native-execution.md`
ratifies exactly three things (git-native routing, CI enforcement, the style-lint tier) and
mentions branch protection nowhere] Requiring every change to `main` go through a PR (via GitHub
branch protection) was proposed as a follow-up question during this session's own git-workflows
retrospective, reasoned through, and recommended against — never put to the user as a ratified
ADR amendment, so this is NOT a formal "considered and rejected" institutional decision the way
ADR-0002's three rulings are. The reasoning, recorded here so it is not silently re-derived: it
would break the solo-main-direct lane ADR-0002 deliberately preserves, converting every one-line
fix into campaign-weight ceremony for no safety gain CI-on-push doesn't already provide (CI runs
identically on every push, PR or not). If branch protection is proposed again, the honest framing
is "revisit this session's own inference," not "overturn a ratified decision" — and the bar
should be naming a NEW failure class CI-on-push genuinely doesn't cover.

## The close sequence, in order

1. Confirm the PR state is `MERGED` (`gh pr view <n> --json state`) — never proceed on the
   assumption that approving/requesting a merge means it happened.
2. Delete the remote branch and RE-VERIFY it is gone (`merge-semantics.md`'s ten-branch lesson)
   — `campaign_close.py` does both steps atomically with the reverification built in.
3. Gate the touched plugins at the new `HEAD` — a merge landing does not by itself prove the
   result is clean; run the check.
4. `ExitWorktree action:"remove" discard_changes:true` — safe ONLY after step 1 confirmed
   `MERGED` (see `worktree-mechanics.md`'s discard-safety note).
5. `campaign_close.py <pr-number> [--repo owner/repo] [--gate <plugin-root>...]` (forge 1.30.0,
   `ce05fcb`) runs steps 1–3 as one mechanized check, with the exact re-verification step that
   would have caught the ten-branch incident before it accumulated undetected.

## Worked instance: this pack's own campaign

[verified, observed directly in this authoring session, 2026-07-17] Issues #19 and #23 were executed as one campaign in a single worktree
(`worktree-issue-19-23-git-mechanization`), closed with the sequence above, then immediately
dogfooded: `campaign_close.py` was run against its own PR (#26) moments after merge, reporting
`C1 ok / C2 ok (branch already gone, reverified) / C3 ok` — the first real proof the tool
correctly reports "already absent" rather than falsely claiming credit for a deletion `gh` had
already performed.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| A one-line fix is stuck behind campaign ceremony | the solo lane wasn't recognized | if it's genuinely one file and doesn't collide with parallel work, commit directly to main |
| A branch-protection proposal resurfaces | the ADR-0002 rejection wasn't checked first | this file — the decision stands; name a new failure class or drop it |
| A worktree was discarded before confirming the PR actually merged | step ordering skipped | always confirm `MERGED` state before any discard |
