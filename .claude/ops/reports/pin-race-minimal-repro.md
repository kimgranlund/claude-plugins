# Minimal reproduction recipe: worktree-isolation pin race (guard redirects a pinned session to another session's worktree)

Suitable for filing against the Claude Code harness (anthropics/claude-code). Distilled from
first-hand captures on 2026-08-17 (estate issue kimgranlund/claude-plugins#490 and the platform
report `pin-race-platform-report-2026-08-17.md`, same directory). This is a recipe, not a live
demonstration — the race requires two or more concurrent interactive Claude Code sessions on one
host, which cannot be spawned from inside a session.

## Environment

- Claude Code **2.1.233**, macOS **26.6.1** (Darwin 25.6.0, build 25G76), zsh.
- One git repo checkout at `/Users/kimba/Projects/nonoun/plugins`; worktrees created by
  `EnterWorktree` land in-repo at `.claude/worktrees/<name>` (gitignored), each on its own
  `worktree-<name>` branch.
- Permission mode: bypassPermissions ("yolo"); **zero user or plugin hooks registered** — the
  previously suspected plugin hook `worktree_prebash_guard` was fully retired (estate #466 /
  PR #472) and a reload confirmed 0 hooks before every 2026-08-17 sighting. The guard emitting
  the messages below is therefore the platform-native session-isolation guard.
- Multiple concurrent Claude Code sessions (interactive + dispatched agents) working the same
  repo, each pinned to its own worktree.

## Bug in one sentence

After `EnterWorktree` pins Session A to worktree `wt-A` (verified via `pwd` +
`git branch --show-current`), the session-isolation guard later validates — and in the worse
case silently *executes* — A's `Bash`/`Edit`/`Write` calls against a **different** concurrent
worktree `wt-B`, observed biased toward the most-recently-created worktree on the host, with no
`EnterWorktree`, `cd`, or path reference to `wt-B` by Session A in between.

## Steps to reproduce

Two terminals, same machine, same repo.

**Session A (victim):**
1. Start `claude` at the repo root.
2. Have it call `EnterWorktree` targeting a new worktree, e.g. `wt-A =
   .claude/worktrees/pin-race-victim`. Confirm the tool reports
   `Entered worktree at .../pin-race-victim on branch worktree-pin-race-victim.`
3. Verify the pin: run `pwd` and `git branch --show-current` — both must name `wt-A`.
4. Begin a sustained write loop: repeated `Edit`/`Write` calls to files inside `wt-A` (absolute
   paths), interleaved with plain `Bash` calls (`git status --short`, and at least one
   multi-line python heredoc with no `cd` — the heredoc form drew the "too complex to verify"
   refusal in Occurrence 1). Keep the loop running for several minutes.

**Session B (trigger), started while A's loop is running:**
5. Start a second `claude` at the same repo root.
6. Have it call `EnterWorktree` targeting a new worktree `wt-B` (e.g.
   `.claude/worktrees/pin-race-trigger`), so `wt-B` becomes the **newest-created** worktree on
   the host, and keep Session B alive and doing occasional `Bash` work in `wt-B` (a live session
   holding the pin appears to matter — see Determinism below).
7. Optionally repeat with a Session C creating `wt-C` a few minutes later, to test whether A is
   redirected to the newest worktree or to a sticky earlier culprit.

**Observe in Session A (the pass/fail check):**
8. Watch A's subsequent tool calls. FAIL (bug reproduced) if any of:
   - An `Edit`/`Write`/`Bash` call is **refused** with a guard message naming `wt-B` (or `wt-C`)
     as "this session's" worktree — a worktree A never entered (verbatim texts below); or
   - `pwd` / `git branch --show-current` in A, with no intervening `EnterWorktree`, return
     `wt-B`'s path/branch — i.e. A's effective state, not merely the message, has flipped; or
   - `git status --short` in A shows another session's uncommitted files (proves writes would
     land in the wrong tree).
   PASS (no bug) if every A call throughout is validated against `wt-A` and `pwd`/branch never
   deviate.
9. Confirm the recovery signature: re-issuing `EnterWorktree` with `wt-A`'s path immediately
   re-pins A (verified via `pwd`/branch) — and the flip can recur minutes later to the same
   culprit worktree even after new worktrees have made it non-newest.

## Expected

The isolation guard validates every one of Session A's tool calls against the worktree A itself
entered (`wt-A`), regardless of worktree creation or `EnterWorktree` activity in concurrent
sessions. A verified-successful `EnterWorktree` durably protects at least the very next call.

## Actual (observed 2026-08-17, twice in one session plus three independent sibling seats)

- Guard refusals naming the wrong worktree, verbatim:
  > `This session is isolated in the worktree /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress, but this command is too complex to verify that it stays inside the worktree; break it into plain, separate commands. Refusing to run it — a worktree-isolated session's git operations must target its own worktree. Run the equivalent from /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress without the redirect.`
  (a `Bash` heredoc in a session pinned to `issue-477-s8-lexicon`), and
  > `This session is isolated in the worktree /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress. Edit the worktree copy of this file instead of the shared-checkout path.`
  (a `Write` using the session's own worktree absolute path, in a session freshly pinned to
  `490-pin-race-report` — the very next call after a verified `EnterWorktree`).
- State, not just message: follow-up `pwd` + `git branch --show-current` (no `EnterWorktree` in
  between) **succeeded and returned the culprit worktree's path and branch**, and
  `git status --short` there showed a different in-flight agent's uncommitted changes.
- Worst independent case (build-477's seat): fresh verified `EnterWorktree`, then **4 of 4
  consecutive `Edit` calls** redirected to `issue-478-479-thinking-intent` — the newest worktree
  extant at the time — with one `Edit` landing correctly between attempts (intermittent).
- Affected call types observed: `Bash`, `Edit`, `Write`. Both failure modes occur: false
  refusal against the wrong pin, and silent execution in the wrong worktree.

## Frequency / determinism conditions

- Requires ≥2 concurrent sessions on one host/repo with worktree churn (new worktrees created
  while others are mid-work). Never observed in a single-session setup.
- Timing: flips observed within one working turn of a peer worktree's creation; the culprit was
  the newest-created worktree in the first sightings (creation +6 min in Occurrence 1;
  timestamps via `ls -ld`). But Occurrence 2 flipped to the **same** culprit ~15 min later even
  though newer worktrees existed by then — consistent with the guard reading/last-writer-winning
  a **shared pin key** held by another still-live session, not a pure "newest worktree" rule. A
  long-lived, actively working Session B is therefore the best trigger.
- Intermittent per call (one correct `Edit` amid four redirected), but in the worst case 100% of
  a seat's writes were blocked for a period. Reproduced 2+ times in a single session and by 3+
  independent sessions in the same hour, so under concurrent load it is reliably reachable.
- Not permanent: re-`EnterWorktree` to the session's real path reliably restores the pin, but
  one re-pin is not durable — the very next call has been misdirected again.

## Workarounds (mitigation only)

1. Re-issue `EnterWorktree` with the session's own path immediately before every write-shaped
   call; verify `pwd` + `git branch --show-current` after each pin and before destructive writes.
2. Absolute paths in every `Bash`/`Edit`/`Write`; never rely on inherited relative cwd.
3. Serialize worktree churn — avoid creating worktrees while peer sessions are mid-write.
4. Treat any refusal naming a never-entered worktree as a flipped pin: re-pin and re-verify,
   never retry past it.

## Suggested regression test

Two+ concurrent sessions each pinned via `EnterWorktree` to distinct worktrees; while all are
alive, one session creates yet another worktree and re-pins. Assert: no other session's next
tool call is validated against (or executed in) any worktree but its own, and a session's own
call immediately following its own successful `EnterWorktree` is never redirected.

## Provenance

- First-hand double capture: `.claude/ops/reports/pin-race-platform-report-2026-08-17.md`
  (this directory) — full timeline, timestamps, and root-cause localization.
- Estate tracking: kimgranlund/claude-plugins#490 (supersedes #448; prior history #359, #363,
  #375, #385 — #385's per-PID pin fix regressed or never covered this path).
- Hook retirement ruling out estate code: #466, PR #472.
