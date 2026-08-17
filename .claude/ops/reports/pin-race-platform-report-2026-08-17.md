# Platform bug report: worktree-isolation pin race redirects a pinned session to a different worktree

**Status:** open, unresolved on the platform side. Filed from estate issue #490 (supersedes #448, prior history #375/#385/#359/#363).

**Audience:** Claude Code platform/harness team. Forward as-is.

## Summary

A session pinned to worktree A by `EnterWorktree` (verified via `pwd`/`git branch --show-current` immediately after) later has its effective working directory and git branch silently reassigned to worktree B — observed biased toward the most-recently-created worktree on the host — with no `EnterWorktree` call, `cd`, or any other action by the session in between. Tool calls (`Bash`, `Edit`, `Write`) then either execute against B while the session still believes it is in A, or are refused with a message naming B as "this session's" worktree. Either way, the guard's own pin state — not just its enforcement — is wrong.

This is a correctness and safety defect: a session can write to a directory it never entered, or have valid same-worktree commands refused because the guard is comparing against the wrong worktree.

## Reproduction (first-hand, captured live and TWICE in one session, 2026-08-17)

This was captured directly in a working session while producing this very report, not reconstructed after the fact.

### Occurrence 1

1. Session enters worktree via `EnterWorktree`, target `.claude/worktrees/issue-477-s8-lexicon`. Tool confirms: `Entered worktree at .../issue-477-s8-lexicon on branch worktree-issue-477-s8-lexicon.`
2. Several `Bash`/`gh` calls run correctly against that worktree (no `cd`, absolute-path-free) for roughly the length of one working turn.
3. A later, unrelated `Bash` call (a multi-line python heredoc, no `cd`, no worktree reference in the command text) is refused with:
   > `This session is isolated in the worktree /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress, but this command is too complex to verify that it stays inside the worktree; break it into plain, separate commands. Refusing to run it — a worktree-isolated session's git operations must target its own worktree. Run the equivalent from /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress without the redirect.`
4. Follow-up `Bash` calls (`pwd`; `pwd && git branch --show-current`) — run with **no** command-text change, no `EnterWorktree`, nothing from this session pointing at `build-494-research-methods-stress` — **succeeded** and returned:
   ```
   /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress
   worktree-build-494-research-methods-stress
   ```
   i.e. the guard did not merely misreport the session's location in an error string — the session's actual effective cwd/branch had flipped to worktree B and stayed there across multiple subsequent calls.
5. `git status --short` inside that state showed uncommitted changes belonging to a **different, in-flight agent's work** (`modified: docs/skills/research-methods/SKILL.md` — the `build-494-research-methods-stress` ticket's own file), confirming this was not a display artifact: any `Edit`/`Bash` write issued in that window would have landed in the wrong worktree, potentially corrupting a peer session's uncommitted work.
6. Re-issuing `EnterWorktree` with the original path (`.claude/worktrees/issue-477-s8-lexicon`) immediately and successfully re-pinned the session; `pwd` and `git branch --show-current` confirmed correct state afterward, and it held for the remainder of that turn.

**Newest-worktree bias, confirmed by timestamps:** at the moment of this misdirection, `build-494-research-methods-stress` was the most recently created worktree directory on the host (`ls -ld` mtime 2026-08-17 05:44Z), created 6 minutes after the session's own worktree (`issue-477-s8-lexicon`, 05:37Z) and 1 minute after the next-newest (`issue-488-g8-phantom-handles`, 05:43Z).

### Occurrence 2 — same session, ~15 minutes later, different target worktree, same culprit worktree

7. Session deliberately created and entered a *new, third* worktree, `.claude/worktrees/490-pin-race-report`, specifically to author this report in isolation from the #477 work. `EnterWorktree` confirmed success; `pwd`/`git branch --show-current` verified correct pin.
8. The very next state-changing call — a `Write` of this report file, using the worktree's own absolute path — was refused:
   > `This session is isolated in the worktree /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-494-research-methods-stress. Edit the worktree copy of this file instead of the shared-checkout path.`
   Note this is the **same** culprit worktree (`build-494-research-methods-stress`) as Occurrence 1, even though a brand-new worktree had been created and entered in between, and even though `build-494-research-methods-stress` was by then no longer the newest worktree on the host (the session's own `490-pin-race-report`, created seconds prior, was newer). This weakens a pure "always redirects to the single newest worktree" theory in favor of "the guard's pinned-worktree value is being read from some other session's still-live EnterWorktree state and does not get updated/invalidated promptly," with `build-494-research-methods-stress`'s value apparently sticky once written.
9. `pwd`/`git branch --show-current` immediately after, again with no `EnterWorktree` in between, confirmed the session's actual state had flipped to `build-494-research-methods-stress` (not just the message).
10. Re-issuing `EnterWorktree` with the session's actual target path (`.claude/worktrees/490-pin-race-report`) immediately and successfully re-pinned the session again; verified via `pwd`/branch, and the report write then succeeded from the correct location.

Two independent flips to the identical culprit worktree, ~15 minutes apart, spanning two different intended targets (`issue-477-s8-lexicon` then `490-pin-race-report`) and two different call types (`Bash` and `Write`), is strong evidence this is a live, ongoing, reproducible platform condition as of this filing — not a one-off fluke.

## Signature (what to grep for)

- Refusal text patterns:
  - `This session is isolated in the worktree <PATH>, but ... Refusing to run it — a worktree-isolated session's git operations must target its own worktree.`
  - `This session is isolated in the worktree <PATH>. Edit the worktree copy of this file instead of the shared-checkout path.`
- The `<PATH>` named in the refusal is **not** the worktree the session actually entered; it is a different worktree that exists concurrently on the same host — sometimes the newest one, but (Occurrence 2) can persist as a specific worktree's value even after newer worktrees exist, suggesting sticky/stale shared state rather than a pure recency rule.
- The condition is not permanent for the session — a subsequent identical or simpler command can succeed, but against the *wrong* worktree (state, not just message, is wrong): confirmed via `pwd`/`git branch --show-current` returning the wrong worktree's values, not just the error text naming it.
- Re-issuing `EnterWorktree` with the session's original/actual path immediately and reliably restores correct pinning — confirmed twice in this session, independently corroborated as the standing mitigation in #490/#480 and by build-477's session.
- No user-space cause: no `cd`, no shared-checkout redirect, no compound command, and in Occurrence 2 not even a fresh `EnterWorktree` triggers correct behavior on the very next call. Plugin-side `worktree_prebash_guard` (teamwork) was fully retired before all 2026-08-17 sightings (#466/PR #472, host reload showed 0 hooks) — the guard enforcing this is platform-native, not an installed hook.

## Timeline

- **2026-08-16 and earlier:** prior sightings of the same class — #359, #363, #375 (closed on landing PR #385, "per-agent/PID-keyed pin + no-cd carve-out"), #448 (closed 2026-08-16, verdict: "stale pre-#385 hook load; remedy = reload").
- **2026-08-17, overnight campaign:** #448's remedy (reload, confirmed 0 hooks registered) does not resolve the class. build-477's session: fresh `EnterWorktree` confirms correct worktree via `pwd`+branch, then 4 of 4 consecutive `Edit` calls are redirected to `issue-478-479-thinking-intent`, the newest worktree extant at that time; one `Edit` lands correctly between attempts (intermittent, not deterministic-always). Sibling seats on #475 and #478-479 hit the same class the same hour and adopt an `EnterWorktree`-immediately-before-every-write workaround.
- **2026-08-17 12:31 UTC:** #490 filed, superseding #448 (falsified), root-cause reassigned to the platform-side session-isolation guard.
- **2026-08-17, this session, Occurrence 1 (~05:37–05:44 local, worktree `issue-477-s8-lexicon`):** session flips to `build-494-research-methods-stress` (the newest worktree at that instant), state (not just the error message) is wrong for at least two subsequent tool calls, self-heals on re-`EnterWorktree`.
- **2026-08-17, this session, Occurrence 2 (~15 min later, worktree `490-pin-race-report`, created fresh specifically for this report):** immediately after a verified-successful fresh `EnterWorktree`, the very next write is refused/misdirected to the *same* culprit worktree (`build-494-research-methods-stress`) from Occurrence 1, despite it no longer being the newest worktree on the host. Self-heals again on re-`EnterWorktree`.

## Root cause (best available localization, not confirmed by platform-side logs)

The isolation guard's "which worktree is this session pinned to" state is being read from — or overwritten by — a value shared across concurrently running sessions/processes on the same host/repo, rather than a value scoped per session (or per PID, which #385 was believed to have fixed for a narrower case). Occurrence 1 and the independent build-477 sighting both show a bias toward the *most recently created* worktree at the time of the flip. Occurrence 2, ~15 minutes later in the same session, flips to the *same* culprit worktree even though it is no longer the newest on the host — consistent with a shared value keyed to a specific still-live session (`build-494-research-methods-stress`'s own session appears to have remained active and re-asserted or held a shared pin lock) rather than a purely time-ordered "most recent worktree" computation. Either mechanism is consistent with: last-writer-wins on a shared key, or a stale/incorrectly-scoped read where this session's lookup resolves to another live session's pin record instead of its own.

This is not an estate-code defect: `worktree_prebash_guard` (the plugin-side hook that used to implement a related check) was fully retired (#466/PR #472) before every 2026-08-17 sighting, and the reload immediately prior showed zero hooks registered. The refusal messages' own wording and mechanism (blocking compound commands and shared-checkout writes) match the platform's built-in session-isolation guard, not any plugin.

## Impact

- **Major.** Observed worst case (build-477) blocked 100% of a build seat's writes for a period, forcing a workaround of re-`EnterWorktree`-before-every-call. This report's own authoring session hit the same class twice while producing it.
- **Data-safety risk, not just availability.** Occurrence 1 shows the failure is not limited to false-refusals: a session can silently believe itself correctly pinned to A while every subsequent call actually executes in B, including against B's uncommitted, in-flight changes belonging to a different agent. In a permissive/yolo permission mode with no confirm-before-write, this could apply an Edit intended for worktree A directly into worktree B's working tree.
- **Persistence beyond a single re-pin cycle.** Occurrence 2 shows the race is not reliably cleared by simply entering a new worktree once — a session can be flipped again shortly after a verified-correct re-pin, to the same culprit as before.

## Mitigations (estate-side, already adopted — does not fix the platform bug)

Recorded as the standing protocol in #480 (fleet-protocol-rules pack) and cross-linked from #490:

1. Call `EnterWorktree` (with the session's own path) immediately before any write-shaped tool call, not just once at session start — treat the pin as perishable, not durable.
2. Verify `pwd` and `git branch --show-current` after every `EnterWorktree`, and again opportunistically before a destructive or hard-to-reverse write — and again immediately if any tool call in between was refused or looked slow/unusual, since Occurrence 2 shows even a call immediately after a verified pin can still misdirect.
3. Prefer absolute paths in every `Bash`/`Edit`/`Write` call; never rely on an inherited relative cwd.
4. Serialize concurrent worktree churn where possible — avoid creating new worktrees while other sessions are mid-write; worktree creation appears to be a trigger event for peer sessions' misdirection, though Occurrence 2 shows the culprit can also be an older, already-live session, not only the newest creation.
5. If a refusal names a worktree the session never entered, do not treat it as a false positive to retry past — re-`EnterWorktree` to the session's real target and re-verify state before continuing. Do not assume one successful re-pin is durable for the rest of the turn; re-verify before the next write too.

None of these prevent the underlying shared-state race; they only shrink the window and make excursions detectable per-call.

## Suggested platform-side fix directions (not prescriptive — platform team's call)

- Key the isolation guard's "session → pinned worktree" state strictly per session id (or per PID plus session id, since #385's PID-keyed fix apparently regressed or never covered this path), never by a value that can be overwritten by, or accidentally read from, a *different* session's `EnterWorktree` call or pin record.
- Make the guard's refusal message and its actual enforcement state provably consistent with each other (Occurrence 1 shows a case where a later successful call proved the "wrong worktree" belief was real internal state, not just a stale message) — add a getter/assertion that the enforcement path and the message path read the same value at the same instant.
- Investigate why a fresh, verified-successful `EnterWorktree` does not durably protect even the very next tool call (Occurrence 2) — the pin write itself may be racing with a concurrent session's read/write of the same shared key.
- Add a regression test: two (or more) concurrent sessions each pinned via `EnterWorktree` to distinct worktrees; while all are alive, have one session create yet another worktree and re-`EnterWorktree`; assert no *other* session's next tool call is redirected to any worktree but its own, and that a session's own immediately-following call after its own successful `EnterWorktree` is never redirected.

## Cross-links

- Estate tracking issue: #490 (this report is filed as its Findings comment and as this file).
- Superseded: #448 (closed "stale hook / reload" — falsified by post-reload, post-hook-retirement sightings including this capture).
- Prior history: #359, #363, #375, #385 (partial/regressed fix).
- Estate-side mitigation protocol home: #480 (`teamwork/skills/fleet-rules` pack, work-claim/coordination-scope/communication-routing doctrine) — this incident's mitigations (above) belong there, not here; here is evidence and signature only.
- Hook retirement ruling out estate-code cause: #466, PR #472.
