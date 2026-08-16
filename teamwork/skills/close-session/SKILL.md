---
name: close-session
description: >-
  Wraps up a session at the moment it's ending: captures a real finding, verifies writes landed,
  states one verdict on THIS session's own worktree. Use for the closing MOMENT, whatever verb
  names the ask — "wrap up this session", "close this out, check for anything left to capture",
  "before you exit/stop, make sure nothing's left uncaptured or unfiled", "check if there's a PR
  or issue to file before you stop". NOT for a peer session's
  worktree (parallel-work-rules), unresolved conversational questions (find-open-questions),
  removal mechanics (ExitWorktree), or sweeping the whole conversation for MANY dropped items into
  tickets, any time — even at a session's end (docs:file-leftovers).
disable-model-invocation: false
user-invocable: true
---

# close-session

close-session wraps up a session's own work in a git worktree before it ends, turning an
unverified "write anything, then close" prompt into a checked sequence: capture what's real, name
what isn't, and account for every finding in a stated verdict.

## Procedure

1. **Check the mechanical state.** `git status --porcelain` (uncommitted or untracked changes),
   whether the current branch carries commits still unpushed to its upstream, and whether an
   already-open PR from this session exists and needs finishing. Clean on all three → skip step 2
   (there's no git-side capture to make); steps 3-5 still run — a read-only session can still carry
   a repeated correction or a ratified decision worth the save-lessons scan.
   **A multi-seat session's own residue is a fourth axis, not covered by the three above:** a
   session that spawned worktree seats leaves other local branches (task branches, per-agent
   placeholder branches), merged-PRs' remote branches still undeleted, and extra worktrees — none of which
   `git status`/current-branch/open-PR checks ever see (found live, 2026-08-08: a session verdicted
   "clean on all three" while 19 merge-verified-but-undeleted local branches and a stale remote
   branch from its own seats sat unaccounted for). Where the host repo ships a gated reaper script
   (e.g. `scripts/ops/reap-branches.mjs --dry`, exit-coded, dry-run first), run it and list its
   REAP rows in the verdict as residue, not silently captured. Where no such script exists, fall
   back to `git worktree list` (extra worktrees beyond the primary) and `git branch --merged`
   (merged-but-undeleted local branches) — plain counts, reported the same way. This axis is
   ALWAYS checked and ALWAYS named in the verdict (residue found, or explicitly "no session-spawned
   branch/worktree residue") — never silently folded into the three-axis "clean" claim, since the
   verdict's own hard gate is only as true as what was actually verified.
2. **Judge what's real — via `file-leftovers`' systematic sweep.** Invoke `file-leftovers` (Skill
   tool) to sweep the session for everything raised but left unadvanced — bugs, feature ideas,
   feedback, chores, unanswered questions — rather than relying on this step's own ad hoc read
   alone. Its own contract already covers what this step used to do by hand: an evidence-quoted
   candidate table, one batched clarification round for `needs-input`/contested rows, then each
   approved row minted through its owning intake skill (`file-bug`/`file-feature`/`file-task`,
   which supply their own dedup sweep and payload contract) — no separate
   `file-bug`/`feature`/`issue` call is needed here. Its minted ids feed step 5's verdict as
   captured items. In-progress work that's gate-clean still earns a push and a PR from this step
   directly (the existing open one, updated, when there is one, so the count of open PRs from this
   session stays one) — `file-leftovers` tickets ideas and defects, it does not push code. Work
   that's genuinely unfinished gets named as such, plainly, rather than forced into a premature PR.
3. **Scan for durable knowledge.** A correction repeated, a ratified decision never captured, a
   high-impact convention this session surfaced → hand off to `save-lessons` (Skill tool) for
   its own detection pass, confirm gate, and placement judgment — this step's job ends at
   triggering the scan at the right moment.
4. **Verify before counting.** Read back every write this step just made — `git log`, `gh issue
   view`, `gh pr view` — and count it as captured only once that read-back confirms it landed.
5. **State the verdict.** One of two shapes: a concrete list of what was captured (Issue URL, PR
   URL, knowledge-pack path) plus what remains open, or a single "nothing to capture — clean, safe
   to close" line.

## Output contract

A verdict block, always: either the captured-items list or the single clean line from step 5,
PLUS step 1's branch/worktree residue line (found residue, named; or explicitly none found) —
never omitted, even on an otherwise-clean verdict.

## Failure branches

- Dispatched in an unattended or scheduled context (no interactive user to answer an
  AskUserQuestion-gated confirm) → step 2's own capture skill (`file-leftovers`, whose
  clarification round AND mint gate both require an interactive user — its own contract: no
  interactive channel → deliver the candidate table as the report and stop, minting waits) and
  step 3's save-lessons confirm gate are both named as deferred in the verdict rather than
  attempted; steps 1, 4, and 5 still run on their own — the residue axis is read-only (a reaper
  script's `--dry` flag, plain `git` reads) and never blocked by the absence of a human, so it
  always runs and reports even here.
- No gated reaper script exists AND `git worktree list`/`git branch --merged` themselves fail
  (not a git repo, detached state) → the residue axis reports UNMEASURED with the reason, same
  discipline as any other unreachable check; never silently omitted from the verdict.
- Not inside a git repo at all → the single clean-verdict shape applies, with the reason stated
  ("nothing to capture — no git context here"); this is not a second verdict shape, just the
  existing one with its reason filled in.
- Uncommitted state exists but reads as mid-thought scratch or a deliberate WIP still being shaped,
  not finished work → name it in the verdict as left open, since capturing is a judgment call on
  each diff, not a blanket action across all of them.
- A write in step 2 or 3 fails partway (network, auth) → the verdict states the failure plainly;
  only a write step 4 actually confirmed counts as captured.

Done when the verdict block has been stated: a "nothing to capture" line on a genuinely clean
session counts exactly as much as a full captured-items list on a busy one. It is NOT done while
the skill exits with no verdict at all, a real finding goes unmentioned, a write is claimed
without step 4's read-back confirming it landed, or a "clean" verdict is stated without step 1's
branch/worktree residue axis actually having been checked — the one hard gate this skill enforces:
a verdict is only as true as what was actually verified, and "clean" now covers four axes, not
three.

## Example

Good (verdict names both captures and the gap):
```
Captured: Issue #61 (a repro found for the flaky test), PR #62 (the fix, gate-clean, open).
save-lessons: declined — nothing crossed the bar this session.
Remaining: the flaky test's root cause is still unconfirmed, noted in Issue #61.
```

Bad (counter-example — do not imitate): "I've wrapped things up, let me know if you need
anything else!" — a closing pleasantry standing in for a verdict, with no evidence anything was
actually checked or captured.

## References

| Path | Use when |
|---|---|
| `file-leftovers` (docs) | Step 2's own systematic sweep — candidate table, clarification round, mint-on-approval — invoked, not restated |
| `file-bug` / `feature` / `issue` (docs) | Invoked indirectly, via `file-leftovers`' own Phase 4 mint step — not called directly by this skill |
| `save-lessons` (harness) | Step 3's detection pass and its own confirm-before-mint gate |
| `parallel-work-rules` (this plugin) | The question is a PEER session's worktree, not this session's own close-out |
| `repo-cleaner` (harness), or a host repo's own gated reaper script | Step 1's own branch/worktree residue axis — its dry-run/exit-coded pattern is the model when a host repo has no reaper script of its own |
| `ExitWorktree` | The actual removal step, once this skill's verdict says it's safe |
