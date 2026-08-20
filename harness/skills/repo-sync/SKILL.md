---
name: repo-sync
description: >
  Safe fast-forward-only main sync, feature-branch rebase, PR-merge
  verification, and post-pull dev-freshness (build-tool cache / restart) for
  a shared git checkout. Use for "pull/rebase/merge", "sync to current
  dev", "sync main", "catch up on merges", stale code after a pull, or
  "is it safe to merge this PR". NOT for creating a PR (the host repo's own
  finish-work/PR skill); NOT a host repo's own dev-server pathology
  reference, where one exists; NOT a standing fleet-wide merge watcher
  (`repo-cleaner`, `watch-tickets`).
disable-model-invocation: false
user-invocable: false
---

# Repo sync

This is a **shared checkout**: other sessions' uncommitted work lives in the
same working tree you are about to touch. Every rule below exists because a
plausible-looking git shortcut either destroys someone else's WIP, serves a
stale build as if it were current, or reports success on a merge that never
landed.

## Sync main (shared checkout)

1. **`git fetch origin` first, then read `git rev-list --left-right --count
   HEAD...origin/main`** before acting — you need the ahead/behind counts to
   know whether a plain `pull` is even a fast-forward, not just to see if
   there's anything new.
2. **On main: `git pull --ff-only`, never `pull`/`merge`/`rebase` on the
   shared checkout's main.** A merge commit or rebase on the checkout every
   session shares corrupts the one shared reference point everyone rebases
   against. A non-fast-forward result is a **finding to report**, not
   something to auto-repair by force-pushing or resetting.
3. **Check the working tree BEFORE any pull/merge action.** Untracked files
   are fine to leave alone. **Modified tracked files belong to someone** —
   this is a shared checkout, so a dirty tree is very likely another
   session's live work-in-progress, not scratch state. Never `git stash` or
   `git reset --hard` it away silently; stop and report whose changes look
   present (via `git status` + recent `git log` authorship) instead of
   guessing.

## Feature branch (in a worktree)

- **Rebase onto fresh `origin/main`**, not the last-fetched local copy — a
  rebase against a stale main just re-creates the same drift one commit
  later.
- **A conflict stops and reports** — resolving someone else's rebase
  conflict on their behalf risks silently reordering intent you can't see;
  hand it back with the conflicting files named.
- **Never force-push a branch you don't own.** A force-push to someone
  else's remote branch can discard commits they haven't pulled down yet,
  with no local trace that anything was lost.

## Merging PRs (only when explicitly instructed)

- **Verify `MERGEABLE` and the check rollup with a real read** —
  `gh pr view --json mergeable,statusCheckRollup` — before merging, not
  after.
- **Treat a CANCELLED check from a concurrency group as non-blocking** — a
  superseded run being cancelled is expected churn from a newer push to the
  same branch, not a failure.
- **Verify the merge landed with a state read-back**, `gh pr view --json
  state` showing `MERGED` — **never trust the merge command's exit code
  alone**; a race between two merges, a required-check timing gap, or a
  branch-protection rule can make the command return 0 while the PR is still
  open.

## Dev freshness after a pull

- **If the lockfile changed, or a hoisted UI-kit/dependency version
  changed, clear the front-end build tool's dependency cache** (e.g. `rm -rf
  <app>/node_modules/.vite` for Vite) **and flag that the dev server needs a
  restart** — a stale build-tool cache serves the OLD package graph even
  after the source files on disk are current, which reads to whoever's
  watching as a bug that doesn't exist.
- **Check port ownership before touching any dev server, and never kill one
  this session doesn't own** — it may belong to a different worktree or a
  teammate's session; report the restart command for the human to run
  instead of running it yourself. A pinned dev-server port or an
  auth-provider callback constraint is likely already documented in the host
  repo's own dev-server-ops reference, where one exists — read that first so
  the recipe stays in one place rather than re-deriving it here.

## Never

`git add -A` on a shared checkout · a bare PR-creation command bypassing the
host repo's own PR skill (labeling, ticket-linking) · `--force` on any
branch this session doesn't own · touching another worktree's or session's
files or processes.

## Done / not-done

**Done**: main is fast-forwarded (or its non-ff state is reported, not
repaired) + dev freshness is assessed and any needed restart is named to the
human + any PR merge is confirmed by a state read-back.

**NOT done**: a stash or reset of someone else's uncommitted work, a killed
dev server this session didn't start, or a merge reported as complete on the
strength of an exit code alone.
