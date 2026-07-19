# Playbook: running multiple coding agents in parallel, in one repo, unaware of each other

This is portable guidance — it does not assume this workspace's own tooling or scripts. It applies
to any repo where you want several independent coding-agent workers making progress on the same
codebase at the same time, without those workers ever talking to each other directly.

## The core problem

You have N coding agents (Claude Code sessions, CI-triggered bots, scheduled fleets — anything that
can check out a repo, edit files, and run git). None of them share a session, a message channel, or
even necessarily a clock. They must:

1. Never do the same work twice.
2. Never silently clobber each other's changes.
3. Leave a trail a human (or another agent) can audit after the fact.

With no live channel between them, the **only** thing two agents can coordinate through is what they
both can read: the ticket backend (GitHub Issues, Linear, Jira, …) and the git history itself. The
whole playbook follows from that one constraint — every rule below exists because "ask the other
agent" is not an available move.

This is a different problem from *dispatching subagents within one session* (that has a supervisor
who can assign disjoint scopes up front) or *noticing a live collision with another open session*
(that agent might be reachable — you can check its state, or a human can). Here, the other agent
might not even exist yet, or might have finished and shut down hours ago. Coordination has to be
durable, not live.

## The three ingredients

| Ingredient | Job |
|---|---|
| **Ticket backend** (Issues, Linear, …) | The shared, durable coordination surface. A ticket's state (open/claimed/in-review/done) is the only signal agents exchange. |
| **Git worktree per claim** | Physical isolation. Each agent gets its own checkout, on its own branch, so uncommitted work never sits in a tree another agent might touch. |
| **PR as merge gate** | The only door into shared history. Nothing lands on the trunk branch except through a PR that ran CI and got merged — this is also where two agents' overlapping edits finally get compared. |

None of the three is optional. Tickets without worktrees means two agents can still stomp on one
shared checkout. Worktrees without a ticket-claim protocol means two agents cleanly, independently,
duplicate the same work in two different branches. A PR gate without the other two just tells you
*after the fact* that a collision happened, with no record of who thought they owned what.

## Backend-agnostic vocabulary

Whatever backend you use, an agent needs exactly these operations on a ticket:

- **discover** — list tickets matching a filter (e.g. "open, unclaimed, label:agent-ready").
- **dedup-search** — before creating anything, check nothing equivalent already exists.
- **claim** — write your agent identity onto the ticket and move it to an in-progress state.
- **read** — fetch one ticket's current state and its comment/history trail.
- **update** — post progress (a comment, a state change, a linked PR).
- **close** — mark it done, with a findings/result note — never a silent close.

GitHub realizes this as: search/list, `gh issue list --search`, assignee + label, `gh issue view
--comments`, a comment or label change, and closing the issue (ideally via the PR's closing
keywords). Linear realizes the same six operations as: its issue search, assignee + workflow state,
`read` via its API/MCP, a comment, and a state transition. The protocol below is written in the
abstract operations; substitute your backend's concrete call for each one.

## The claim protocol (the part that doesn't exist by default)

The failure mode unique to "agents unaware of each other" is two agents claiming the same ticket in
the same few seconds. Assignment in most backends is a read-then-write, not atomic — so a race
window always exists. Treat it as inevitable and cheap to resolve, rather than trying to eliminate
it:

1. **Discover** candidate tickets (open, unclaimed, matching whatever readiness label/state your
   repo uses).
2. **Dedup-search** — confirm no other ticket already covers this, and no existing open PR already
   references it.
3. **Claim, then immediately re-read.** Write your agent identity as assignee, move the ticket to
   "in progress," and post a claim comment carrying: your agent id, a timestamp, and the branch
   name you're about to create. Then **read the ticket back** — don't trust your own write. If you
   see a second claim comment with an earlier timestamp (or, on an exact tie, a lower agent id —
   pick one deterministic tie-break rule and use it everywhere), you lost the race: abort, unclaim,
   pick a different ticket. A wasted worktree is cheap; a duplicate PR is not.
4. **Only after the claim survives step 3**, create the worktree and branch and start real work.

**Staleness.** A ticket claimed by an agent that then crashes or times out must not stay locked
forever. Pick one durable rule (a claim older than N hours with no linked PR and no update comment
is stale) and enforce it the same way every time: any agent doing a `discover` pass may reclaim a
stale ticket, but must post a comment saying so before doing it — the previous claimant's work, if
it exists, is still on its branch and isn't lost, just no longer exclusive.

## Worktree and branch conventions

- **One worktree per active claim.** Never point two claims at the same working directory, and
  never let a second claim reuse a worktree that still has uncommitted work from a different claim
  in it.
- **Branch name encodes the ticket id** — `issue-142-...` or `eng-421-...` — so any human or agent
  looking at `git branch -a` or the worktree list can trace worktree → branch → ticket with no extra
  lookup.
- **A worktree only pays off branched from something recent.** A worktree branched off a
  long-stale trunk just moves the merge-conflict pain to PR time instead of preventing it — sync
  the base branch before branching, not just before opening the PR.
- **Commit early, commit small**, independent of isolation. Small, frequent commits make the
  eventual PR diff (and any conflict inside it) legible instead of a single opaque blob.
- **Clean up after merge.** Remove the worktree and delete the branch once its PR merges. Don't
  leave merged-branch worktrees lying around — they're the thing a later `discover` pass has to
  wade through to figure out what's still actually in flight.

## PR discipline

- **Every claim ends in a PR that references its ticket** — GitHub's closing keywords
  (`Closes #142`) or Linear's branch-name-based linking. This is what makes the ticket
  auto-transition to done instead of needing a manual close, and it's what lets a *human* or another
  agent doing a `discover` pass see "already has an open PR" as a cheap, no-clone signal that a
  ticket isn't actually free even if its claim looks stale.
- **CI is the real gate, not local state.** Local checks can be skipped, bypassed, or simply not run
  by an agent that never had them configured. If the trunk branch is protected and only accepts
  merges that passed CI, every agent's work gets checked the same way regardless of how it was
  produced — this is the mechanism that catches an overlapping-file collision that the claim
  protocol didn't prevent (claim protocol prevents duplicate *ticket* work; it does nothing about
  two different tickets that happen to touch the same file).
- **Never trust a command's own success report.** "Merged," "branch deleted," "issue closed" are
  claims a tool prints, not verified state. After a merge, re-list the branch and re-read the ticket
  to confirm the state you expect actually landed — a command that silently no-ops still exits 0.
- **Prefer rebase over merge-commits** for keeping the trunk's history linear enough that a
  real conflict is visible as a conflict, not buried inside a merge commit nobody reads.

## Handling a genuine overlapping-file collision

The claim protocol stops two agents from doing the *same ticket* twice. It cannot stop two
*different* tickets from touching the same file — that's a normal, expected event in any real
repo, not a bug in the protocol. When it happens:

- It surfaces at PR/CI time as a merge conflict or a failing rebase — by design, this is the
  latest and cheapest point to catch it, since neither agent could have known about the other
  ticket in advance.
- Resolve by whichever PR is smaller/simpler rebasing onto whichever merged first — don't try to
  merge both simultaneously.
- Optional mitigation, not a requirement: if your ticket backend supports a free-text or label
  field, have claims note the files/modules they expect to touch. A `discover` pass can then use
  that as a soft signal ("another in-progress ticket already touches this module") to reduce
  collision odds — it is a hint, not a lock, and does not replace the PR-time check.

## Trigger models

The protocol above is identical regardless of what launches an agent:

- **Human-launched** — someone opens several terminals/sessions, each pointed at a different
  ticket. The claim happens because a human told that session which ticket to pick up (or the
  session ran a `discover` pass itself).
- **Scheduler-fired** — a cron-triggered or event-triggered agent wakes up, runs a `discover` pass
  over open tickets, and claims one on its own. This is the same protocol, just with the discover
  step happening automatically instead of by human instruction.

Neither trigger model changes the claim/worktree/PR mechanics — only who or what decides *when* an
agent starts a `discover` pass.

## Worked example

**Clean run, no collision.** Agent A discovers ticket #101 ("open," unclaimed), dedup-searches
(nothing else covers it), claims it (assignee=agent-a, state=in-progress, comment with timestamp
and branch name `issue-101-fix-timeout`), re-reads and confirms the claim survived, creates a
worktree on that branch, commits in small steps, opens a PR with `Closes #101`, CI passes, the PR
merges, the ticket auto-closes, the branch is deleted and the deletion is re-verified, the worktree
is removed.

**Near-collision, caught.** Agent B discovers the same ticket #101 nine seconds after Agent A
claimed it. Agent B writes its own claim, then re-reads per step 3 above and sees Agent A's earlier
timestamp already on the ticket. Agent B posts nothing further, unclaims, and moves to the next
candidate ticket from its `discover` list. No duplicate branch, no duplicate PR — the cost was one
wasted read.

**Stale claim, reclaimed.** Ticket #87 was claimed by Agent C six hours ago; the staleness window
for this repo is two hours; no PR and no update comment exists. Agent D's `discover` pass flags it
as stale, posts a comment noting the reclaim with a timestamp, and claims it. If Agent C's work
still exists on its original branch, it isn't deleted — only its exclusive claim is superseded;
recovering or discarding that branch is a decision for whoever notices it, not something this
protocol does automatically.

## Quick-reference checklist

- [ ] Every agent has a stable, consistent identity string used for assignee/comments/commit
      author — traceability depends on this.
- [ ] `discover` → `dedup-search` → `claim` → **re-read to confirm the claim survived** → only then
      start real work.
- [ ] One worktree per active claim; branch name encodes the ticket id.
- [ ] Staleness window defined and enforced the same way by every agent.
- [ ] Every PR references its ticket via a closing keyword or the backend's native link.
- [ ] Trunk branch protected; merge only through CI-gated PRs.
- [ ] After any merge/close/delete, re-read the actual state — never trust the command's own
      success message.
- [ ] Overlapping-file conflicts are expected and resolved at PR time, not prevented up front.
