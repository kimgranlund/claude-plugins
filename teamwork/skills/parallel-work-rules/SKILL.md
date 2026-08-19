---
name: parallel-work-rules
description: >-
  Decide whether concurrent sessions/subagents need git-tree isolation, and what to do
  on collision. Use when overlapping actors may mutate the same tree — "should I work
  in a worktree for this", "should this subagent use isolation: worktree", "design a
  protocol for running several Claude Code terminals against one repo", uncommitted
  shared-file changes, two builders on the same files, a collided build, or committing
  before a risky move. NOT dispatch shape/cost, or the fleet's default coordination/claim/
  comms protocol (fleet-rules); NOT a greenfield design decision (grill-the-ask); NOT
  next-turn timing — /goal, /loop (loop-rules); NOT closing out THIS session's worktree
  (close-session).
disable-model-invocation: false
user-invocable: false
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
   (each worker self-gating its own path) is fleet-rules's own sanctioned default, not a
   risk this skill overrides. Isolation answers the overlap question, not the actor-count question.
2. Isolate when slices overlap, can't be cleanly partitioned, or you can't confirm disjointness at
   all (an actor outside your control — a peer session, an opaque one):
   - Same-session subagents with overlapping/unpartitionable targets → the `Agent` tool's
     `isolation:"worktree"` at dispatch. **A host session already pinned to its own worktree
     poisons its plain-Bash subagents** — they inherit the pin and cannot create a worktree of
     their own from inside it; dispatching with `isolation:"worktree"` sidesteps this because the
     harness creates the child's worktree itself, rather than the child trying to carve one out of
     the parent's pinned cwd. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment 5317746661,
     lesson 11) · 2026-08-17 · [incident]
   - The whole session, working alongside sessions outside your control → `EnterWorktree`. Its own
     contract requires an explicit trigger ("the user
     directly, or... project instructions") — nothing routes a session into it automatically. If
     this project runs concurrent sessions regularly, that trigger belongs in a standing CLAUDE.md
     rule, not a per-invocation reminder — but the rule is a one-line pointer ("this project runs
     concurrent sessions — consult `parallel-work-rules` before dispatching parallel file-mutating
     work"), the skill's own doctrine staying here, in this one file. Copying these steps into
     CLAUDE.md instead creates a second, drift-prone copy the moment this file changes (the
     mechanics of writing the pointer are entry-file-rules'; this skill only requires the
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
3. **Verify independently — never act on either side's self-report, and never on a relay of one.**
   Run `git status`/`git diff`/file mtimes yourself; a report that a task is "done" (from a peer's
   teammate-message or from your own dispatched subagent) is a claim, not ground truth, until you've
   checked it against the tree. This extends to relays: a THIRD party — including your own
   dispatcher — summarizing or even verbatim-copying another agent's report is still not your own
   direct completion for a worker you spawned. Only a completion landing in your own transcript,
   attributed to your own dispatch of that specific worker, counts as ground truth for it.
4. **Escalate by actor type**, not uniformly:
   - Subagent you spawned → resolve directly (you own its brief).
   - Named teammate → `SendMessage` it; ask whether it's finished, and whether the content should
     travel with your operation (e.g. a `git mv` correctly carries a peer's uncommitted edits along
     — losing them is a bug in HOW you resolve, not a reason to avoid resolving).
   - Opaque session → ask the human. Present what you found (which files, whose edits, how old);
     let them confirm sequencing, and proceed once — and only once — they have. In an UNATTENDED
     run (no human to ask), `references/unattended-collision-protocol.md` is the governing branch:
     probe-twice liveness deltas, zero-salvage stand-down on duplicate lanes, the frozen-lane
     adoption bar (clean tree + no holders + quiet past the peer's cadence, then re-gate +
     independent re-review), and the write-fence until one of those verdicts lands.
   - Opaque session whose work lives on a branch/PR/Issue → post a comment there naming the
     dependency, blocker, or finding (e.g. "this PR's version bump collides with #45/#46, land
     first" or "found gap X here, flagging rather than pushing to your branch") — this is in
     addition to, not instead of, asking the human when the coordination is urgent or the comment
     goes unanswered. Git-native surfaces are the durable coordination channel this workspace
     already treats as canonical for work items (ADR-0002); the same surface works for
     inter-agent coordination, not only for recording decisions.
5. Once cleared, re-verify the result — diff before/after to confirm nothing the other actor owned
   was silently dropped, not just that your own change landed.

## Recovery: a live agent's worktree vanished mid-dispatch (#207)

A parent seat idling on a nested dispatch anchored to its OWN worktree can have that worktree
auto-reaped by the harness's idle-unchanged-worktree cleanup while the child is still live in
it — deterministic, not a race: any parent-waits-on-child-in-same-worktree pattern with zero
interim changes triggers it (#207, confirmed live during the #198 build).

1. The child stops and reports rather than self-authorizing into the shared checkout — its
   refusal ("working directory no longer exists... Refusing to run there") is the correct guard
   firing, not a bug to route around.
2. The host recreates the worktree at the EXACT same path on the claimed branch —
   `git worktree add <same-path> <claimed-branch>` (the branch survives the reap; it was created
   at claim time) — falling back to `-b` off `main` only if the claimed branch is gone too.
3. The host verifies clean + correct HEAD before anything else touches it: `git status --short`
   (expect empty) and `git rev-parse HEAD` (expect the claimed branch's own tip).
4. The host then `SendMessage`s the child to resume with an explicit cd-per-Bash-call instruction,
   since its pinned cwd may still be stale even though the path exists again.

Step 2's claimed-branch path is validated recovery (#207 exercised exactly this — the branch
existed from the claim step); the `-b`-off-`main` fallback is untested defensive coverage for the
branch-also-gone case, not something #207 itself exercised — cite #207 for the former only.

## Standing mitigation: cwd races across sibling sessions (#189)

Sibling agent sessions launched from one background job can share host cwd state racily — even
plain Edit/Bash calls from one sibling can intermittently land in a different sibling's worktree
(#189, measured across parallel sessions from one job).

- Serialize writers strictly across siblings of the same job — one sibling writing at a time.
- Verify with `cd <path> && pwd && git status` before every write, not only at task start — the
  only check that catches a silent cwd swap after the fact.
- `worktree-prebash-guard` (teamwork 2.9.4, #198) now flags both directions it can see —
  worktree→primary and sibling→sibling — but its own disclosed blind spots (dynamic `$(...)`
  targets, `sh -c`/`bash -c` wrappers) still pass silently, so the discipline above is
  belt-and-suspenders on top of the guard, never made redundant by it.
- **#359 (2026-08-16) is a recurrence of this exact class, root-caused PLATFORM-side** — the
  same cwd/write-guard identity migration #189 already tracked, corroborated in production a
  second time (write-guard identity hopping worktree→worktree as sibling `build-leader` dispatches
  each created their own tree). Investigated and closed with no estate lever for the RACE itself
  (the CLI's own cwd-pin mechanics, upstream `anthropics/claude-code#86584`) — the estate stays a
  detection-only bystander here, never the source, and never gets a lever inside the platform's
  own pin internals. What #359 DID surface as a genuine estate gap: `worktree-prebash-guard` only
  ever caught an escape WITHIN one compound Bash call (an explicit `cd` chained to a mutating
  follow-on) — a cwd already wrong on a LATER, SEPARATE call, no `cd` anywhere in it, passed
  completely undetected. Issue #363 closed that specific gap with a persisted per-session
  worktree-identity pin (first-call pin-write inside the same PreToolUse(Bash) hook, keyed by the
  event's own `session_id`, ASK on drift, self-heals after flagging once so a legitimate
  Exit/EnterWorktree move doesn't nag forever) — still detection-only, still ASK-never-BLOCK,
  same posture as everything else in this section.

## Batch gate topology — N workers never each run the full suite (#740)

A batch build of many independent slices (a `/batch` run: N workers dispatched, one host desk
merging the result) never has each worker run the FULL gate suite on its own host — each worker
runs a REDUCED gate, targeted only to what it actually touched; the desk runs the ONE full suite,
once, over the merged tree. A reduced per-worker gate catches that worker's own local
regressions cheaply; only the desk's own full run can catch a regression that only exists as a
CROSS-worker interaction, invisible to any single worker's own scoped gate. Worked instance:
agent-ui's 2026-08-18 39-page `/batch` run — nine workers each ran a reduced, targeted gate (all
nine green); the desk's own full suite, run once over the merged tree, caught the one real red
none of the nine reduced runs could see. · agent-ui 2026-08-18 batch run · migrated via
nonoun-plugins#50 · [incident]

## Broadcast re-brief — changing a ship-predicate mid-batch (#740)

A ship-predicate discovered wrong or incomplete MID-BATCH (workers already dispatched and
running) is corrected by `SendMessage` broadcasting the revised predicate to every running
worker — never by letting the stale brief ride to completion and catching the gap only at the
merge desk. A broadcast re-brief changes the predicate cleanly, in place, for every worker still
mid-flight; letting a bad brief ride means re-work discovered late, after workers already built
to the wrong ship bar. · agent-ui 2026-08-18 batch run · migrated via nonoun-plugins#50 ·
[incident]

## Second-lander-owes-recapture — a shared byte-pinned generated artifact (#740)

When two sessions share ownership of a byte-pinned generated artifact (a prompt baseline, a
theme fixture — content whose exact bytes ARE the contract, not just its meaning), the two
sessions agree explicitly, by announce, which one lands SECOND — and the second lander owns
regenerating the artifact from the merged tree, delta-verified as **exactly its own changes** (a
diff against the pre-merge baseline showing only what that session actually changed, nothing the
first lander's own merge already contributed). Serialize by announcing intent, never by polling
for the other side to finish — polling has no reliable signal for when the other announce should
have landed, and a duplicated regeneration is exactly the failure this convention exists to
avoid. Proven twice, 2026-08-19: agent-ui PRs #1303–#1312 (the original batch) and #1404 (a
second, independent recapture instance the same convention resolved cleanly). · migrated via
nonoun-plugins#50 · [verified]

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
| `references/unattended-collision-protocol.md` | No human is reachable (a /goal or scheduled run) and an opaque lane must be judged live vs. dead — liveness deltas, duplicate stand-down, the adoption bar, the write-fence |
| `EnterWorktree` / `ExitWorktree` | Isolating the whole session — requires an explicit trigger (user or CLAUDE.md), never assumed |
| `SendMessage` | The other actor is a named teammate (surfaced a `<teammate-message>`), not silence |
| `gh pr comment` / `gh issue comment` | The other actor's work lives on a branch/PR/Issue but no live `SendMessage` channel reaches it — async, durable, git-native coordination |
| A project's ticket status vocabulary (e.g. `open`/`doing`/`done`) | Cheap pre-flight check before claiming scope — see the project's own doc-writing-rules, where one exists |
| docs' backend-resolver `claim` operation (ADR-0005), where installed | Preventing a duplicate claim on the SAME ticket before any file is touched — a layer beneath this skill's own git-tree collision response, not a replacement for it |
| The Recovery section above | A nested child's worktree got auto-reaped while the parent idled on it (#207) |
| The Standing-mitigation section above | Sibling sessions from one background job share host cwd state racily (#189) |
| The Batch-gate-topology section above | A `/batch` run's N workers need a gate posture (#740) |
| The Broadcast-re-brief section above | A ship-predicate must change mid-batch, workers already running (#740) |
| The Second-lander-owes-recapture section above | Two sessions share a byte-pinned generated artifact (#740) |
| `worktree_prebash_guard.py.retired` (teamwork `scripts/`, hook wiring retired 2026-08-17, #466 — remove-all-hooks directive) | Formerly a mechanical catch for worktree→primary and sibling→sibling cd escapes, PLUS (#363) a persisted per-session identity pin that caught a cwd already wrong on a later separate call with no cd at all — both were always blind to dynamic/wrapped targets, per its own header. No automatic catch remains; this discipline is manual now |
| [[fleet-rules]] | The question is dispatch shape/cost (solo vs. team, how many subagents) — its own disjoint same-tree fan-out is the sanctioned default for genuinely non-overlapping slices, not a risk this skill overrides |
| [[loop-rules]] | The question is when the next turn fires, not who else is touching the tree |
| `entry-file-rules` (harness) | Encoding the resulting rule as a standing CLAUDE.md instruction, once this skill says one is warranted |
| `hook-writing-rules` (harness) | The decision should become a mechanically-enforced guard (e.g. blocking a specific unsafe edit), not just guidance |
| `big-change-git-rules`' silent-failure-catalog (harness) | A dispatched subagent's own `Write`/tool-report of success isn't proof its state landed in the checkout you'll next read — the dispatch-sandbox-redirect entry (issue #125) is this failure at the isolation layer specifically |

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

**A third worked example (a relay mistaken for ground truth):** a coordinating session dispatched
`chore-lead`, which itself dispatched three seats in parallel. Those seats' genuine reports also
broadcast, team-wide, to the coordinating session (not `chore-lead` specifically) — a harness
broadcast behavior, not malice. The coordinating session relayed that content to `chore-lead`,
first paraphrased, then verbatim, each time coaching it to act ("apply this payload," "per your
own procedure step 3"). `chore-lead` refused both times: no completion attributed to ITS OWN
dispatch of those three seats had landed in its own transcript, so a well-formed, even accurate,
secondhand account did not qualify — and it named the relay as a discrepancy in its own report
rather than silently complying. This is the same discipline as the collision-response case above,
applied to report trust instead of file state: verification means checking against YOUR OWN
ground truth (the tree, or your own dispatch's own completion), never against how convincing
someone else's account of it sounds.

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
the matching response, in that order; and — if a worktree vanished mid-dispatch or siblings raced
on cwd — the recreate/verify/resume sequence or the serialize/verify-per-write discipline ran, not
skipped. **NOT done** while "another session might be touching this" is discovered by surprise
mid-edit with no plan for it, or a collision is resolved by trusting a self-report (yours, a
subagent's, or a peer's) instead of checking the tree.
