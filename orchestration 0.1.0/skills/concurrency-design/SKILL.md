---
name: concurrency-design
description: >
  Decide whether concurrent sessions/subagents touching one repo need
  git-tree isolation, and what to do when they collide anyway. Use
  whenever actors may mutate the same tree with overlapping scope: "should
  I work in a worktree for this", "set up this repo so sessions don't
  collide", "another Claude session has uncommitted changes to files I
  need", "should this subagent use isolation: worktree", "two builders
  touching the same files", "should I commit before this risky multi-file
  move", "my build collided with another session's in-progress edits".
  NOT for dispatch shape/cost — solo vs.
  team, how many subagents (orchestration-design); this skill only decides
  whether the chosen shape's targets overlap enough to need isolation, and
  owns cross-session collision entirely. NOT for when the next turn fires
  — /goal, /loop, Stop hooks (loop-design). NOT for authoring the
  hook/agent/entry-file mechanics once a rule is decided
  (hook-authoring-standards / agent-authoring-standards /
  entry-file-standards, forge).
disable-model-invocation: false
user-invocable: true
---

# Harness — Concurrent-Session Isolation Design & Response

**Plane separation**: this skill decides *whether work needs its own workspace* and *what to do
when two workspaces turn out to overlap*, never *what the work itself is* — that's the dispatched
task's own brief. A collision here is a git-tree problem, not a design problem in the work.

## The three actor types (check this first — every baseline gets this wrong)

Before deciding isolation or reacting to a collision, classify what's on the other side. The three
types have different capabilities and different correct responses; collapsing them into "spawned
vs. not" is the single most common mistake:

| Actor | How you know | What you can do |
|---|---|---|
| **Subagent you spawned this session** | You called `Agent`/`Task` for it | Full control: assign scope via `TaskList`, set `isolation:"worktree"` at dispatch, edit its brief directly |
| **Peer session reachable as a named teammate** | It surfaces as a `<teammate-message>` sender in your transcript | Addressable via `SendMessage` — you can ask it directly what it's doing, whether it's done, whether it can commit |
| **Opaque concurrent session** | Uncommitted diffs exist that no known actor claims, or its work lives on a branch/PR/Issue with no addressable owner in-session | **No live channel exists.** You cannot message it, cannot confirm its intent, cannot ask it to pause synchronously. If its work has a PR/Issue home, post a comment there — async, durable, visible to whoever looks next — before or alongside asking the human; a bare uncommitted-diff collision with no such home routes straight to the human. |

A response that treats (b) as unreachable, or treats (c) as if it could be — is wrong before the
rest of the decision even starts.

## Decide (before starting work that mutates files)

1. Will 2+ actors mutate the same repo checkout concurrently, AND do their target files/imports
   actually overlap? Multiple actors alone isn't the trigger — same-session subagents assigned
   genuinely disjoint slices need no isolation at all: dispatching the disjoint same-tree fan-out
   (each worker self-gating its own path) is orchestration-design's own sanctioned default, not a
   risk this skill overrides. Isolation answers the overlap question, not the actor-count question.
2. Isolate when slices overlap, can't be cleanly partitioned, or you can't confirm disjointness at
   all (an actor outside your control — a peer session, an opaque one):
   - Same-session subagents with overlapping/unpartitionable targets → the `Agent` tool's
     `isolation:"worktree"` at dispatch.
   - The whole session, working alongside sessions outside your control → `EnterWorktree`. Its own
     contract requires an explicit trigger ("the user
     directly, or... project instructions") — nothing routes a session into it automatically. If
     this project runs concurrent sessions regularly, that trigger belongs in a standing CLAUDE.md
     rule, not a per-invocation reminder — but the rule is a one-line pointer ("this project runs
     concurrent sessions — consult `concurrency-design` before dispatching parallel file-mutating
     work"), the skill's own doctrine staying here, in this one file. Copying these steps into
     CLAUDE.md instead creates a second, drift-prone copy the moment this file changes (the
     mechanics of writing the pointer are entry-file-standards'; this skill only requires the
     one-line form).
   - A worktree only pays off if it branches from something recent — an isolated worktree branched
     from a long-stale `main` just moves the merge-conflict pain to later. Commit early, commit
     small, per gate-green unit of work, independent of whether you're isolating.
3. Where a project already has ticket status (`open`/`doing`/`done` or equivalent), check it before
   claiming file-level scope — it's a cheaper signal than any git inspection and catches the case
   where the collision hasn't produced a diff yet. Where the backend supports an explicit `claim`
   operation (write identity + re-read to confirm it wasn't outraced, ADR-0005 where installed),
   that's the ticket-layer check to run before starting — this skill's own collision response
   below starts only once a git-tree collision already exists or is imminent; `claim` is the layer
   underneath it that stops two independent agents from starting the *same* ticket in the first
   place. A clean `claim` doesn't retire this skill's own checks: the ticket layer and the
   git-tree layer catch different failures — duplicate work on one ticket vs. two *different*
   tickets that happen to touch the same file, which a clean claim on each side can't prevent and
   this skill's own collision response still has to catch.

## Respond (a collision is discovered mid-task)

1. **Stop touching the contested files exactly where they are.** Route any reconciliation through
   the classify → verify → escalate steps below — treat a read-then-write operation on those files
   as unsafe until the classification below clears it.
2. **Classify the other actor** (table above) before deciding what "verify" even means for it.
3. **Verify independently — never act on either side's self-report.** Run `git status`/`git diff`/
   file mtimes yourself; a report that a task is "done" (from a peer's teammate-message or from your
   own dispatched subagent) is a claim, not ground truth, until you've checked it against the tree.
4. **Escalate by actor type**, not uniformly:
   - Subagent you spawned → resolve directly (you own its brief).
   - Named teammate → `SendMessage` it; ask whether it's finished, and whether the content should
     travel with your operation (e.g. a `git mv` correctly carries a peer's uncommitted edits along
     — losing them is a bug in HOW you resolve, not a reason to avoid resolving).
   - Opaque session → ask the human. Present what you found (which files, whose edits, how old);
     let them confirm sequencing, and proceed once — and only once — they have.
   - Opaque session whose work lives on a branch/PR/Issue → post a comment there naming the
     dependency, blocker, or finding (e.g. "this PR's version bump collides with #45/#46, land
     first" or "found gap X here, flagging rather than pushing to your branch") — this is in
     addition to, not instead of, asking the human when the coordination is urgent or the comment
     goes unanswered. Git-native surfaces are the durable coordination channel this workspace
     already treats as canonical for work items (ADR-0002); the same surface works for
     inter-agent coordination, not only for recording decisions.
5. Once cleared, re-verify the result — diff before/after to confirm nothing the other actor owned
   was silently dropped, not just that your own change landed.

## Output contract (when reporting a decision or a collision)

```
Posture: <isolated | shared-tree — reason>
Actors on the tree: <spawned subagent(s) | named teammate(s) | opaque session(s) | none>
Collision: <none | files: X,Y,Z — actor: <type> — verified via: <git status/diff/mtime>>
Action: <proceeded | escalated to: <teammate name via SendMessage | a PR/Issue comment: URL | the user> | blocked>
```

## References & tools

| Tool / doc | Use when |
|---|---|
| `Agent` tool, `isolation:"worktree"` | Dispatching subagents that mutate files in parallel and could conflict |
| `EnterWorktree` / `ExitWorktree` | Isolating the whole session — requires an explicit trigger (user or CLAUDE.md), never assumed |
| `SendMessage` | The other actor is a named teammate (surfaced a `<teammate-message>`), not silence |
| `gh pr comment` / `gh issue comment` | The other actor's work lives on a branch/PR/Issue but no live `SendMessage` channel reaches it — async, durable, git-native coordination |
| A project's ticket status vocabulary (e.g. `open`/`doing`/`done`) | Cheap pre-flight check before claiming scope — see the project's own doc-authoring-standards, where one exists |
| scribe's backend-resolver `claim` operation (ADR-0005), where installed | Preventing a duplicate claim on the SAME ticket before any file is touched — a layer beneath this skill's own git-tree collision response, not a replacement for it |
| [[orchestration-design]] | The question is dispatch shape/cost (solo vs. team, how many subagents) — its own disjoint same-tree fan-out is the sanctioned default for genuinely non-overlapping slices, not a risk this skill overrides |
| [[loop-design]] | The question is when the next turn fires, not who else is touching the tree |
| `entry-file-standards` (forge) | Encoding the resulting rule as a standing CLAUDE.md instruction, once this skill says one is warranted |
| `hook-authoring-standards` (forge) | The decision should become a mechanically-enforced guard (e.g. blocking a specific unsafe edit), not just guidance |

## Worked example (the incident this skill was minted from)

A builder subagent, dispatched into the shared tree (no isolation — the task hadn't defaulted to
one), was mid-`git mv` on a set of files when it noticed uncommitted diffs on those exact files
that it hadn't made. It stopped before completing the move and reported up instead of guessing.

The orchestrating session then: verified the diffs independently (`git diff`, file mtimes) rather
than trusting the subagent's read of them; identified the other actor as a genuinely opaque
session (no teammate-message, no name) and routed the sequencing question to the human rather than
guessing "probably done"; on confirmation, let the `git mv` proceed (which correctly carried the
other session's uncommitted content along — a rename preserves working-tree content, it doesn't
discard it); and re-diffed afterward to confirm nothing was lost. A second, separate collision
later in the same task WAS a named teammate (a `<teammate-message>` sender) — resolved directly via
`SendMessage`, no human escalation needed, because that actor was addressable.

The reusable lesson isn't "worktrees would have prevented this" (true, but retrospective) — it's
that the stop → classify → verify-independently → escalate-by-type sequence is the same regardless
of whether isolation was set up in advance, and it degrades gracefully when it wasn't.

**A second worked example (async sequencing, no live collision at all):** a repo-orchestrator
session surveyed four open PRs and found three independently bumping the same plugin's version
number from the same base — two of them each still owned by a live background session with no
`<teammate-message>` channel to either. There was no file collision to stop (each PR's own
worktree was clean) — the coordination need was purely about merge ORDER. The fix wasn't asking
the human per PR: it was posting one comment on each affected PR naming the dependency ("this
version bump collides with #45/#46 — land first"), then waiting. Durable, visible to whichever
session or human looks next, and it doesn't consume the human's attention for something two
sessions can resolve async once the dependency is named where both can see it.

**Done** when a concurrency-touching task states its posture (isolated or knowingly shared) before
starting, and — if a collision surfaces — names the actor type, the independent verification, and
the matching response, in that order. **NOT done** while "another session might be touching this"
is discovered by surprise mid-edit with no plan for it, or a collision is resolved by trusting a
self-report (yours, a subagent's, or a peer's) instead of checking the tree.
