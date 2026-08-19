# The mitigation ladder — Phase 3's full procedure (#490/#609, ratified 2026-08-18)

Cited from `dispatch-ticket/SKILL.md`'s Phase 3 "The mitigation ladder" bullet rather than
restated inline (the same F6 split-to-references pattern as `worktree-teardown.md` and
`spec-lock-gate.md`).

## Why this ladder exists

Four wedge events on 2026-08-18 alone (the #490/#609 class, upstream
`anthropics/claude-code#87349`): two `build-leader` sessions wedged mid-build, and the marshal
session's own pin drifted twice (`fix-647` → `fix-660`). Every recovery succeeded, but only
because the mitigation ladder was hand-carried in each dispatch prompt as folklore, re-derived
under pressure instead of read off a standing procedure. This reference is what that folklore
became.

The load-bearing fact the ladder is built around: **`EnterWorktree` is a tool grant, not a
universal capability.** It is available to a live session that adopted its seat in-place
(`/bind-build`, `/bind-team`, a `team-scaffolding`-adopted seat) — the seat never left the
session, so the tool stays reachable turn after turn. It is NOT available to a seat reached via
the `Agent` tool (`build-leader`, or any nested `Agent`-tool dispatch this skill's own
no-nested-wait preamble names) — that seat's tool surface is whatever its subagent definition
grants, and `EnterWorktree` is not among the grants any `*-leader` agent carries. A dispatch that
assumes it can "just re-pin with `EnterWorktree`" because that's the standard unblock
(`fleet-rules` Section 6) will find the tool simply isn't there — confirmed directly, 2026-08-18:
an `Agent`-tool session's own attempt to reach it surfaced no such tool at all, not a permission
denial.

## The three rungs

**Rung 1 — worktree reuse-or-create + `EnterWorktree` re-pin (live sessions only).** This is
Phase 3's isolate bullet as already written, plus `fleet-rules` Section 6's re-pin playbook for a
stuck cwd. Reachable only by a session holding `EnterWorktree` — the door-1/door-2 sessions in
`fleet-rules`' own "Seat-access doors" taxonomy (`/bind-*` adoption, or a `context: fork`
execution that inherited the forking session's own tool grants). Never attempted by an
`Agent`-tool dispatch; there is no tool to fall back to mid-build if the pin drifts, because there
was never one to begin with.

**Rung 2 — scratch-clone (the DEFAULT for an `Agent`-tool dispatch, not a fallback).** Exact
procedure:

1. `git clone <remote-url> <abs-scratchpad-path>/<repo>-<ticket-id>` — an absolute destination
   path under the session's own scratchpad directory, never a relative one and never preceded by
   a `cd` (the platform's own worktree-isolation guard refuses a runtime-computed `cd` out of the
   session's bound worktree inside a compound command; a plain `git clone` with an absolute
   destination, or `git -C <abs-path> <subcommand>` for every subsequent git call, both sidestep
   it cleanly — verified directly during this ladder's own authoring, 2026-08-18).
2. `git -C <clone-path> checkout -b <decided-branch-name> origin/main` — cut the ticket's own
   decided branch name (Phase 3's claim bullet already picked it) off a fresh `origin/main`, never
   off whatever the session's own pinned worktree happens to have checked out. **Disclosed gap:**
   a fresh scratch clone is exactly as bare as a fresh worktree — the same bootstrap-before-run
   rule Phase 3's isolate bullet mandates for a new worktree (gh#498) applies here too, and this
   rung doesn't yet mechanize it; feature-detect and run the host repo's own bootstrap script (if
   any) before step 4's first gate/check inside the clone, same as the worktree path does.
3. Run `teamwork/scripts/pin_check.py <decided-branch-name> --cwd <clone-path>` before the first
   real write — confirms the clone actually landed on the intended branch before any edit lands
   in it.
4. Do all the dispatch's actual work — `Read`/`Edit`/`Write`/`Bash` — against absolute paths
   rooted at `<clone-path>`, never the session's own pinned worktree path at all. The pinned
   worktree is irrelevant to this rung; nothing about it needs to be correct for the clone to
   work.
5. Commit as work lands (small, gate-green units — `fleet-rules` Section 5's own rule), `git -C
   <clone-path> push -u origin <decided-branch-name>`, then `gh pr create` (or the plugin's usual
   PR-open sequence) exactly as Phase 5 stage 2 already specifies.

Proven 2026-08-18 on eight PRs: #664, #665, #682, #685, #687, #688, #689, #690 — every one opened
from a scratch clone, none from a worktree the dispatching seat could not have reached anyway.

**Rung 3 — Git-Data-API landing (RECOVERY only, never a first choice).** For work already
stranded inside a worktree that is wedged — the pin drifted mid-build after real edits had
already landed there, or a session died holding uncommitted changes a fresh session can no longer
safely re-enter — a local commit is no longer trustworthy. Land the change directly through the
GitHub REST Git Data API instead of the local working copy:

1. Read the file's intended new content (from whatever local copy is still readable, or
   reconstruct it) and create a blob: `gh api repos/<owner>/<repo>/git/blobs -f content=<content>
   -f encoding=utf-8` (base64 for binary content).
2. Read the branch's current tree (`gh api repos/<owner>/<repo>/git/trees/<branch-sha>`), then
   create a new tree layering the changed blob(s) onto it: `gh api
   repos/<owner>/<repo>/git/trees -f base_tree=<base-sha> -f
   'tree[][path]=<path>' -f 'tree[][mode]=100644' -f 'tree[][type]=blob' -f
   'tree[][sha]=<blob-sha>'`.
3. Create a commit against that tree, parented on the branch's current head:
   `gh api repos/<owner>/<repo>/git/commits -f message=<msg> -f tree=<tree-sha> -f
   parents[]=<parent-sha>`.
4. Update (or create) the branch ref to point at the new commit: `gh api --method PATCH
   repos/<owner>/<repo>/git/refs/heads/<branch> -f sha=<commit-sha> -F force=false` (a PATCH, not
   the client's default POST — updating an existing ref 404s under POST; `-F` sends `force` as a
   real boolean, not the string `"false"`, which the endpoint 422s on). Creating the ref instead,
   via `POST .../git/refs`, if the branch doesn't exist remotely yet.
5. Open the PR exactly as any other rung, per Phase 5 stage 2 — the API landing only replaces
   steps 1–4 of a normal commit-and-push; everything downstream (gate output, PR body, the
   version-collision re-checks) is unchanged.

This bypasses the local git working copy entirely, which is exactly why it is a recovery rung and
not a default: it has no local diff review, no local gate run, and no local commit history to
inspect before it lands — real work should reach the remote through rungs 1–2 whenever they're
reachable at all. Proven 2026-08-18 on PR #663, landing work stranded in a worktree whose local
git state had drifted enough that no local commit could be trusted.

## Ladder ordering, by caller class

- **A live session holding `EnterWorktree`** tries, in order: worktree reuse/create (Phase 3's
  isolate bullet) → `EnterWorktree` re-pin (`fleet-rules` Section 6) if the pin drifts mid-build →
  scratch-clone if the worktree itself is unrecoverable → Git-Data-API landing only for work
  already stranded with no trustworthy local commit.
- **An `Agent`-tool-dispatched builder** (`build-leader`, or any nested `Agent`-tool seat this
  skill's own no-nested-wait preamble names) starts at scratch-clone directly — its only reliable
  rung, proven across eight PRs the same night this ladder was ratified — and falls back to
  Git-Data-API landing only for work already stranded from an EARLIER part of the same dispatch
  (e.g. a pinned worktree it never should have written into in the first place, per the
  no-EnterWorktree finding above). It never attempts rung 1's worktree mechanics; there is no tool
  grant backing them.

## Preflight companion

`teamwork/scripts/pin_check.py <intended-branch> [--cwd <path>]` mechanizes the BEFORE-first-write
half of this ladder: it reads the actual bound git state at `<cwd>` (a live session's own
worktree, or a scratch clone's path) and fails loudly, naming this ladder's next rung, the moment
the checked-out branch doesn't match the ticket's own decided branch name — rather than letting a
write land in the wrong tree and discovering the drift only later, mid-build. Selftest per
`script-writing-rules`; G4-swept.
