# Worktree mechanics — placement, gitignore, and the checkout-collision trap

## EnterWorktree places worktrees IN-repo, not out

[verified, this workspace's own tool contract, 2026-07-15] Claude Code's `EnterWorktree` creates
worktrees inside the current repo at `.claude/worktrees/<name>/`, on a fresh branch from
`origin/<default-branch>` by default. This falsified an earlier documented assumption in this
workspace (harness's clean-repo razor originally claimed worktrees live "outside the repo
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

## A fresh worktree is a fresh checkout, not a bootstrapped one — run the host repo's own step

[ruled, gh#498, 2026-08-17 — gen-ui-kit gh#1389 residual] Both `EnterWorktree` and a hand-run `git
worktree add` produce a bare checkout: no `node_modules`, no built artifacts, nothing a host
repo's own setup step would normally install. A build that skips straight to `npm run check` (or
any lint/test/build command) inside that fresh worktree gets a **false red** from the missing
dependency tree, not a real regression — this bit gen-ui-kit (gh#1389) until seats learned to run
`node scripts/dev/bootstrap-worktree.mjs` by hand first; its in-repo half (a front-door `--check`
gate that fails loudly instead of silently) shipped as gen-ui-kit PR #1410. Isolating a worktree at
the ENGINE level (the Agent tool's `isolation: "worktree"`, or `EnterWorktree` itself) is a
platform mechanism this estate's own skills cannot reach into — no plugin hook fires on worktree
creation. The estate-side half is a manual convention, carried by whoever creates the worktree:

- **Detect, then run, immediately after `git worktree add`/`EnterWorktree` lands and before any
  gate or check runs inside it.** Convention: `scripts/dev/bootstrap-worktree.mjs` at the host
  repo's root (or wherever that repo's own docs declare it — a differently-located script counts
  only if the host repo's own docs name the same contract, the same feature-detect discipline this
  file already applies to the branch-reap script above). Absent → nothing to run, proceed as
  before; present → run it unconditionally before treating any subsequent gate result as real.
  Idempotent by convention (safe to re-run on an already-bootstrapped tree), and a `--check` mode
  where the host repo provides one distinguishes "already bootstrapped, verified" from "just
  bootstrapped now" for a caller that wants to log which branch it took.
  A gate that goes red in a worktree that was never bootstrapped is not evidence of a regression —
  bootstrap first, re-run, THEN trust the result.
- **This workspace's own repo carries no such script today** (a plain-Python/Markdown estate,
  nothing to `npm install`) — the rule is dormant here but binds the moment any plugin's own repo,
  or a downstream repo this estate's agents operate in (gen-ui-kit, adia-\* estates), declares one.
  `dispatch-ticket`'s Phase 3 isolate bullet (teamwork plugin) names this step explicitly at its
  own call site rather than restating it — this file is the source of record.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| `.claude/worktrees/` contents show up in `git status` on main | the placement-assumption error, or a missing/stale ignore rule | run `gitignore_check.py`; add the rule if absent |
| `gh pr merge` reports the post-checkout error | expected — `main` is checked out in the primary working directory while the worktree also references it | ignore the checkout error specifically; verify merge state independently |
| `ExitWorktree` refuses to discard | uncommitted work, or commits diverged from what was actually merged | never override with force before confirming MERGED state — see `campaign-decision-tree.md` |
| A fresh worktree's gate/check goes red on the first run, no code change explains it | missing `node_modules`/build output — the worktree was never bootstrapped | run the host repo's `scripts/dev/bootstrap-worktree.mjs` (or its declared equivalent) first, then re-run the gate |
