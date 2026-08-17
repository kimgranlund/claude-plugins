---
name: fleet-rules
description: >-
  Default fleet protocol, AND how skills/subagents/teams compose: coordination, claim-guard,
  comms, version-slot, session-death, pin-race, incoming-item triage, sealed dispatch,
  `skills:` frontmatter. Use for "which peers can
  this orchestrator talk to", "orchestrator died mid-build", "cwd pin stuck", "subagent or team",
  "review my wiring", "where does this bug report go". NOT isolation/collisions
  (parallel-work-rules); NOT next-turn timing (loop-rules); NOT mobilizability (mobilize-chores);
  NOT stacked-PR (big-change-git-rules); NOT corpus audits (check-all-agents/-skills); NOT one
  agent or its return block (agent-writing-rules/write-handoff); NOT abstract decomposition
  (break-down-problem).
disable-model-invocation: false
user-invocable: false
---

# fleet-rules — the fleet's default operating protocol, and how it composes

**Two joined questions, one skill (ADR-0020 D5, 2026-08-17: merged from `team-or-solo-rules`).**
Sections 1–7 state the DEFAULT a fleet seat starts from before a run — the fleet-operations
doctrine, asked at run time, by a bound seat. Sections 8–10 (Design/Review/Improve/Update) answer
the design-time substrate question anyone can ask before a seat exists at all: should this be a
skill, a subagent, or a team, and is the wiring right? Different questions, different readers,
different moments, joined here because `team-or-solo-rules`' natural family name collided with
this skill's existing name (full history: ADR-0020 D5). Each section cites its canonical mechanics
rather than restating them, and names the incident it closes. Isolation/collision response is
`[[parallel-work-rules]]`'s, next-turn timing is `[[loop-rules]]`'s, and which tickets are
mobilizable is `mobilize-chores`'s.

## Part A — Fleet operating protocol

Minted from the `#373` overnight campaign (~20 PRs merged, 2026-08-17): every rule below was
improvised at least once in that one session, meaning it was paid for once already and would
otherwise be paid for again on the next unattended run.

### 1. Coordination scope ladder

**Default: this repo's registered fleet only.** A seat's coordination surface is
`.claude/ops/fleet.json` + `fleet-roster.md` plus its own spawned subagents — never `ListAgents` for
discovery (that surfaces arbitrary unregistered peers: other repos' sessions, other worktrees —
issue #429 explicitly rules these out as introduction/coordination targets). `ListAgents` stays
legitimate for one narrow use: confirming liveness of a session ALREADY named in the roster,
never for finding one.

- **Same-user seats in other repos** (Kim's 2026-08-17 amendment): a status-only reply is allowed
  when one of the user's seats in another repo polls this one — never a claim, never a dispatch,
  never scope creep into that repo's own work.
- **Truly global coordination** (across repos, beyond a status reply) fires only on the user's
  explicit instruction — never inferred from "it would help" or from a peer's own request.
- **Out-of-scope polls get silence or a status-only reply.** A poll from an unregistered or
  out-of-scope sender is not routed to a claim or a dispatch regardless of how it's phrased.
- **Two-host fleets need an explicitly RATIFIED lane split, written into both records** — which
  PRs/seats/files each host never touches, plus per-host merge authority (one host's auto-merge
  grant does not extend to the other without a fresh operator utterance). The split survives a
  host process restart because seats resume from on-disk worktree state plus the ledger, not from
  memory. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 12) · 2026-08-17 ·
  [incident]

Canonical worked mechanic: `team-scaffolding`'s Phase 4 point 7 (introduction) and
`fleet-bootstrap`'s Phase 1 realize this exact ladder already — this entry is the ladder's
general statement, cited there rather than restated.

### 2. Work-claim protocol

**Default: claim before effort, guard before dispatch — two different checks, both mandatory.**

1. **Claim** (ADR-0005, `docs:doc-writing-rules`' `references/backend-resolver.md` — its seventh
   operation): write identity + a timestamped comment, then re-read to confirm the write wasn't
   outraced. `[[dispatch-ticket]]` (this plugin) Phase 3 is the first real caller and stays the
   canonical realization — cited here, not re-derived.
2. **Guard** — the four-layer double-dispatch guard any orchestrator runs before dispatching:
   `in-flight` label pre-filter (#199), `assignees`/`claimed-by` correctness gate (#184), open-PR
   check (#184's GraphQL requirement), open `Blocked-by:` dependency (#193) — all four
   independent, none subsumes another. Canonically defined in `mobilize-chores` step 2, including
   its own mechanical caveats (the flattened open-PR query form's silent lie); cited here, never
   re-derived per caller.

- **Write every claim assuming a guard-skipping peer may act on it.** A claim comment naming the
  branch is a lock, but a live fleet has hosts that read claims as work signals — put enough brief
  in the claim (or the record it sits on) that a duplicate build is at least a CORRECT build, and
  name the branch every time so a duplicate detects itself at checkout, not at PR time
  (`parallel-work-rules` `references/unattended-collision-protocol.md` §2 owns the stand-down that
  follows) · agent-ui #1150/PR #1161 · 2026-08-17 · [worked instance].

**Stale-claim handling stays `repo-cleaner`'s** (harness) — this protocol only states when to
claim and what to check before dispatching, never how to detect or clear an abandoned one.

- **Remote-visible absence never proves a claim stale.** No open PR, no remote branch, no pushed
  worktree only proves nothing was *pushed* — declaring a claim abandoned needs either a
  local-work check (the claimant's own worktree `git status`/reflog timestamps, a local-only
  branch) or an explicit kill confirmation from the claiming session; absent both, propose a reap
  and let a human or `repo-cleaner` confirm, never execute one on remote silence alone. · gen-ui-kit
  fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 8) · 2026-08-17 · [verified]

### 3. Communication routing

**Default: durable records carry truth; `SendMessage` is a liveness nudge, never the channel of
record.**

- Truth lives in Issues/PRs/`fleet.json`/`fleet-roster.md` — never solely in a transcript or a
  notification, which dies with the session that saw it ("the return channel doesn't survive the
  session" doctrine, Part B).
- A dispatched seat reports (Findings write-back, or its typed return) **before** going idle. A
  report supersedes any nudge sent after it — an idle ping arriving post-report is a no-op, not a
  second request (~15 stale idle pings arrived after their own reports during the #373 run,
  purely from pinging on a stale liveness read rather than re-checking the record first).
- Seats never escalate straight to the human — the coordinator relays outcomes, unless the
  coordinator is confirmed gone (no live entry in `fleet.json`'s `live_state.joined` for the
  orchestrator role), in which case the durable record (a PR/Issue comment) is the fallback
  channel, exactly as `[[parallel-work-rules]]`'s own escalation for an opaque actor already
  prescribes.
- The teammate-mode delivery mechanics (`name:`-dispatched seats must `SendMessage`, plain text
  is silently dropped; a `teammate_id="team-lead"` sender may be the root session's own generic
  identity, not a real coordinator) are `harness:agent-writing-rules`' own authoring contract for
  encoding this into an agent file — cited there, not restated here.
- **A dead mailbox is not a dead agent.** `SendMessage` reporting a target unreachable is a
  transport fact, not a liveness fact — check the target's worktree reflog/commit timestamps
  before treating its lane as abandoned; a recently-active worktree (a recent commit, a running
  probe process) is a live owner — hand the item back rather than rebuilding it. · gen-ui-kit
  fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 9) · 2026-08-17 · [verified]
- **A ruling is scoped to the utterance that made it, never generalized past it.** A blanket
  instruction ("ratify all proposed X") binds only what it actually names; a peer-held narrower
  ruling on an adjacent item stays in force until its own fresh utterance changes it. Enumerate
  standing rulings explicitly in the ledger before going unattended (`/goal`), so a judgment call
  has something to cite instead of inferring scope. · gen-ui-kit fleet-ops harvest (agent-ui#1115,
  comment 5317746661, lesson 15) · 2026-08-17 · [incident]
- **One decision, one channel.** A decision that belongs to the user — an ADR ratification, a
  ruling, a batched confirm — is put to them through exactly ONE session/channel, never fanned
  out to more than one on the assumption that redundancy is safer. Three clauses:
  1. **One channel per user-decision.** Whichever session/channel reaches the user first with a
     given decision owns putting it to them; no second session opens a parallel ask for the same
     decision on its own initiative.
  2. **A session that discovers the same decision already pending elsewhere STOPS and routes to
     the first asker**, rather than re-asking the user itself — this section's own
     never-escalate-straight-to-the-human bullet above, applied to one decision instead of one
     outcome.
  3. **A ruling is superseded only by an explicit later ruling that names the earlier one**
     (the tie-break) — never by a second, parallel answer arriving through a different channel.
     An answer that doesn't cite what it's overriding isn't a supersession, it's a collision.

  Minted from the 2026-08-17 crossed-ruling evidence in #518: ADR-0020 was rejected in one
  session at 16:03 and ratified in a second, parallel session one minute later at 16:04 — the
  same decision put to the user through two channels at once, requiring a consolidated tie-break
  round to repair. This rule is what that repair would have made unnecessary.
- **A duty report always gets a work order back — never a bare hold-idle.** When a seat reports
  for duty (or reports done and asks what's next) to the coordinator, the reply names either work
  or a condition — one of three arms, never an unstructured "hold idle"/"stand by" with no named
  slice or trigger: an immediate assignment; an explicit QUEUED assignment naming both the slice
  and the trigger condition that activates it ("hold as reserve; on X landing, you take Y"); or,
  if the queue is genuinely empty, that fact stated explicitly plus the next check-in condition.
  Minted 2026-08-17: a fresh seat reported in, the queue was drained, and the seat sat in an
  unstructured holding pattern for several message rounds before a queued-slice promise finally
  emerged (#539).

### 4. Version-slot + merge-order rules

**Default: one version-bumping build per plugin at a time, hand-assigned before dispatch.**

- A coordinator dispatching 2+ concurrent builds against plugins that might overlap assigns each
  build's target plugin version SLOT explicitly before dispatch, rather than letting each
  discover its version from a possibly-stale `main` at claim time — the informal mitigation that
  held zero-collision across ~19 PRs immediately after issue #290
  (`harness:big-change-git-rules`' `references/who-ships-what.md`, "What actually stopped the
  collisions"). A coordinator's dispatch prompt names the version slot explicitly (e.g. "number
  from N+1 — a sibling PR already claims N") rather than leaving each build to discover it late.
- `[[dispatch-ticket]]`'s Phase 3/5 mechanize the check this rule depends on:
  `version_claim_check.py` (the CLAIM race — a sibling OPEN PR already on the target version) AND
  a re-read of the touched plugin's `plugin.json` straight off `origin/main` immediately before
  PR-open (the VALUE race, #445 — a version already MERGED since branch-cut, which the claim
  check alone can't see). Re-derive neither here; both live in `dispatch-ticket` already.
- **Merge order**: for a stacked PR chain, retarget and rebase every open child onto `main` before
  deleting the parent's branch — never after (#443). `harness:big-change-git-rules`'
  `references/merge-semantics.md` owns the full retarget-then-delete sequence and its worked
  failure mode (PR #437); cited, not reproduced here.
- **Merge-on-green verifies each check's CONCLUSION individually — never the watch command's exit
  code alone.** `gh pr checks <pr> --watch --fail-fast` was found to exit 0 on non-terminal/failed
  states, and this bit three live merges (#530, #546, #549) before a human caught it (#551). The
  watch's exit 0 is advisory only — a green light to go verify, not the verification itself. The
  actual pass condition: `gh api repos/<owner>/<repo>/commits/<sha>/check-runs` against the PR's
  head SHA, with every returned run's own `conclusion` reading `success` (or `neutral`/`skipped`
  for a run branch protection doesn't require) — any `status` still `in_progress`/`queued`, or a
  `conclusion` of `failure`/`cancelled`/`timed_out`/`action_required`, is NOT eligible regardless
  of what the watch exited. `dispatch-ticket`'s quick-build merge sequence (step 1b) mechanizes
  this; cited, not reproduced here.
- **Serialize vs. parallelize**: tickets touching the same file serialize; disjoint named targets
  parallelize — Part B Design step 5's own disjoint-fan-out default, restated here only as the
  one-line rule this area needs, its mechanics staying there.
- **A hot shared file doesn't force strict serialization.** Merge-then-rebase-next (each writer
  fetches and rebases immediately before opening its own PR, ≥1 rebase pass treated as normal, not
  a defect) is the steady state for one file under heavy concurrent write pressure. This refines
  rather than contradicts the same-file-serializes rule above: serialize the DECISION to start
  touching the file if you can, but once several legitimately already are, rebase-next absorbs the
  overlap instead of forcing a queue. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment
  5317746661, lesson 6) · 2026-08-17 · [incident]
- **A repo that commits derived/generated artifacts degrades multi-PR throughput to a
  human-attended serial merge marshal** the moment two PRs touch the same generated file — resolve
  by re-running the generator on the merged source, never by picking a side or hand-merging the
  diff (a rider file like a CHANGELOG is the one keep-both exception). The durable cure is a class
  split at the artifact level: regen-on-main for anything reproducible from source (a freshness
  gate leaves PR CI, one bot PR per drift event), stays-committed-and-PR-blocking for anything
  whose bytes ARE the contract (e.g. a published bundle) — this workspace's own `dist/`
  (`.claude/rules/dist-output.md`) is already the latter class by the same reasoning. A merge queue
  is not a substitute for either: it validates a synthetic commit read-only, and regen output has
  nowhere to land inside it. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment 5317746661,
  lessons 1–3, 5; ADR-0069) · 2026-08-17 · [verified]
- **Credentialed steps don't run inside a seat's own worktree.** A regen or build step needing a
  secret absent from seat contexts either no-ops or writes an empty/red stub there — the pattern is
  an admin merge first, then the host or CI (which holds the credential) regenerates. Never read a
  seat-context red on a credentialed step as a real regression. · gen-ui-kit fleet-ops harvest
  (agent-ui#1115, comment 5317746661, lesson 19) · 2026-08-17 · [verified]
- **A worktree's own installer shapes its build bytes** — a locally-bootstrapped worktree can
  produce meaningfully different bundle bytes than CI's own install path, so a freshness/parity
  gate comparing the two needs the SAME install path on both sides, not just the same source;
  `harness:big-change-git-rules`' worktree-mechanics reference is the canonical home for
  worktree bootstrap mechanics generally — cited rather than re-derived here. · gen-ui-kit
  fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 18) · 2026-08-17 · [verified]

### 5. Session-death resilience

**Default: an orchestrator that resumes after a session death (its own, or a seat it dispatched)
inventories from durable state, never from memory.**

- **Reset orphaned in-flight seats.** A successor orchestrator session finds a ticket claimed
  (Section 2) with no corresponding open PR and no live dispatch holding it → treat as orphaned:
  release the claim per `dispatch-ticket`'s own abandonment bullet (never leave a stale claim or
  `in-flight` label standing for the next sweep to misread as active) and re-dispatch if the work
  still matters. The #373 run's orchestrator did this three times in one night for orphaned seats
  — resetting is the default response to a dead claim with no PR, not an escalation. Subject to
  Section 2's staleness bar above: "no open PR and no live dispatch holding it" is itself the
  local-work check for a TICKET claim (no worktree exists to inspect once none is holding it) —
  this bullet and Section 2's don't conflict, they're the same bar applied to two different
  resources (the claim here, a worktree there).
- **Name the worktree/branch at claim time, every time** (Section 2's claim comment already
  carries this) — the durable record a successor reads to inventory: `git worktree list` for
  what's physically checked out, cross-referenced against each ticket's claim comment for what
  SHOULD be there. A worktree with no matching claim, or a claim with no matching worktree, is
  the drift a successor session is inventorying for.
- **Commit early, commit small, per gate-green unit of work** — `[[parallel-work-rules]]`'s own
  rule (Decide step 2), restated here only because it is this area's load-bearing precondition: a
  worktree that survives its own agent's death is one that already has committed work in it, not
  one banking on a final commit that never lands.
- **A session reaps only its OWN worktrees/branches after its own merge — never a peer's**,
  however idle-looking; a peer's own worktree may hold uncommitted-but-live local work that a
  missing remote signal can't reveal (Section 2's staleness bar above governs whether a peer's
  CLAIM, as opposed to its worktree, may be reaped at all). · agent-ui#1115 v2's "Scope-conformant
  revision" Excluded-list, unnumbered (repo-ops worktree/branch hygiene item) · 2026-08-17 ·
  [verified]
- **Overnight/unattended runs on a machine that can sleep need an explicit keep-awake** (e.g.
  `caffeinate` on macOS) — machine sleep kills in-flight subagent calls outright; record the
  keep-awake process's own PID and its kill instruction in the ledger so a successor can clean it
  up. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 22) · 2026-08-17 ·
  [incident]
- **A durable fleet ledger is resumable-from-alone**: per-item status, a timestamped merge log,
  operator rulings recorded verbatim, incidents, and a roll-up naming every residual item's own
  owner. This elaborates the bullet above rather than restating it — it's the ANATOMY of the
  record a successor inventories from, not just the instruction to keep one; this exact shape let
  one campaign survive ≥3 host process restarts and a second host joining mid-run with no work
  lost. · gen-ui-kit fleet-ops harvest (agent-ui#1115, comment 5317746661, lesson 25) · 2026-08-17 ·
  [verified]

### 6. Pin-race playbook

**Default: `EnterWorktree` re-pin is the standard unblock for a stuck cwd pin — never a manual
`cd`-and-hope.** A builder whose absolute-path writes keep landing in the wrong worktree (or in
the primary checkout) re-invokes `EnterWorktree` on its own claimed path rather than trying to
out-cd the platform-level pin drift; `[[parallel-work-rules]]`'s own "Standing mitigation: cwd
races across sibling sessions" section (#189, #359, #363) is the canonical citation for WHY this
class of drift happens and what detection exists (ASK-only, never a hard block) — this entry adds
only the missing UNBLOCK step, not a restatement of the detection mechanics:

1. Re-run `EnterWorktree` on the exact claimed path — this re-pins the session's cwd identity
   without recreating anything.
2. Verify with one compound call — `pwd && git status && git rev-parse --abbrev-ref HEAD` — before
   the next write, not only at task start (`[[parallel-work-rules]]`'s own rule, restated because
   this is the check that actually catches a silent post-repin swap).
3. Prefer absolute-path Bash writes and single-call compound git operations over any multi-step
   sequence that gives the pin another chance to drift between calls.
4. `#448` closed with the reason "stale hook," not as "fixed" — the platform-level cwd drift this playbook
   answers persisted after the hook that used to flag it was retired (2026-08-17, #466); this
   playbook is the manual discipline standing in its place, not a mechanical guard.
5. **Last resort**, only once 1–3 have failed to land a write where it belongs: a `gh api` call
   (issue/PR comment, label edit) never depends on a local cwd pin at all — landing a durable
   record via the API sidesteps the git-write path entirely when the pin itself won't cooperate.

### 7. Route-anything-incoming protocol

Minted from #577 (2026-08-17): `fleet-bootstrap` Phase 1 registers the host session as "the
orchestrator seat" but nothing gave that seat a standing protocol for what to do with whatever
arrives next — no triage discipline, no routing precedence, no enforcement posture. This section
closes that gap. It binds both doors of the same seat identically (`fleet-rules`' own Part B
"Seat-access doors" — the dispatched `agents/fleet-marshal.md` form and the host-adopted
`/bind-team` form): same discipline, cited from each, never re-derived per door.

**Enforcement posture: STRICT ROUTER, NEVER BUILDS.** The orchestrator routes every incoming item
to an owning seat/skill/door within one turn; it never absorbs the work itself, however small —
no "just this one small fix inline" latitude, no exception for a one-line change. Small-fix
latitude belongs to the seat the item routes TO (e.g. `[[dispatch-ticket]]`'s own solo-first
sizing), never to the router itself.

**Triage-within-one-turn.** Every incoming item — a raw user ask, a bug/feature/task report with
no record yet, a handback from a dispatched seat, a peer message from another fleet session, an
overdue report — gets classified and routed in the SAME turn it arrives, never deferred to "I'll
look into this later" or left to accumulate in context. A turn that receives an item and does
nothing but acknowledge it has not routed it.

**Routing precedence** (first match wins — check in this order, never skip ahead on a guess):
1. **A malformed or incomplete handback from a seat this orchestrator dispatched** → bounce it
   back to that same seat immediately, naming the contract it failed (`harness:write-handoff`'s
   own typed fields, or `[[dispatch-ticket]]`'s Findings-write-back contract) — never silently
   patch the gap yourself, never route it onward as if it were complete.
2. **A peer message from another session** → Section 1's coordination scope ladder (fleet-scoped
   only, unless a same-user cross-repo status poll or an explicit global-coordination instruction)
   — never absorbed as this orchestrator's own work regardless of what it asks for.
3. **An item already carrying a ticket/record id** (a `TKT-####`, a bare issue number, an
   adapter-native id) → `[[dispatch-ticket]]` (one confirmed ticket, any kind) or, for a batch,
   `mobilize-chores`.
4. **A raw report with no record yet** → route by shape to its owning intake skill, never guessed
   at inline: a bug report → `docs:file-bug`; a feature idea → `docs:file-feature`; a chore/task/
   follow-up → `docs:file-task`; several dropped items surfaced at once → `docs:file-leftovers`.
   The orchestrator names which intake skill and hands off — it does not classify further than
   shape-matching, and it never drafts the record's content itself.
5. **A decision that belongs to the user** (a ratification, a batched confirm, an ADR call) →
   Section 3's one-decision-one-channel rule: put it to the user through this session if this
   session is the one that reached them first with it; a session that discovers the same decision
   already pending elsewhere stops and routes to the first asker instead of re-asking.
6. **Anything else genuinely ambiguous after 1–5** → the same unattended failure branches
   `[[dispatch-ticket]]`'s own Phase 1/2 already name (report a named blocker on an ambiguous
   match; report SKIPPED on a task that isn't concretely actionable) — never guessed at, and never
   absorbed as a default catch-all.

**Escalation.** An overdue handback — a dispatched seat that owed a report and hasn't produced one
within its stated budget — gets CHASED, not silently re-queued or forgotten: re-check the seat's
own durable state first (Section 5's own default of inventorying from durable state — a live worktree/branch
with recent commits is still working; nothing durable and no live dispatch is orphaned, per
Section 5's reset-orphaned-seats bullet), then either re-dispatch under the same sealed contract
or escalate the locus per the discovered-reality loop. A chase is itself an incoming item and
re-enters this same triage — it does not get a side channel. Escalation to the human never skips
the coordinator (Section 3's never-escalate-straight-to-the-human default) except when the
coordinator itself is confirmed gone.

Chain-of-command across parallel sessions, overdue-handback chasing, and budget/rollup discipline
at fleet scope are this protocol's worked realization in `agents/fleet-marshal.md`'s own
Priorities and `bind-team`'s host-adopted mirror of them — cited there, not restated here as a
second copy of the same rules.

## Part B — Composition & wiring design/review

Design how capabilities compose, or review an arrangement. The unit is chosen by task shape: skill (procedure), subagent (result-only delegation), team (collaboration).

### 8. Operating model (essentials; depth in `references/foundations.md`)
- Discovery (descriptions select, every turn) vs continuation (`/goal`,`/loop`,hooks decide when the next turn fires) — never conflated.
- Descriptions are the connective tissue: the orchestrator routes on them, not on file cross-references.
- Static vs dynamic wiring: `skills:` preload hard-wires standing expertise; leave the rest to discovery.
- Composition is planes, not a pipeline: authority flows down, artifacts flow up, verdicts flow sideways — a failed verdict routes to the plane that caused it (loop mechanics live in `[[loop-rules]]`).
- Every dispatch is a sealed contract: charter + enumerated inputs + budget + typed return (`references/best-practices.md` "The dispatch is a sealed contract"); the worker never sees the host's deliberation or sibling transcripts.
- The return channel is session-bound, durable state isn't: a completion notification reaches only the live session that made that dispatch, and dies with it. A durable-effect dispatch (PR, branch, ticket) must be discoverable from that state alone by a later session — never solely from having witnessed the notification (`references/best-practices.md` "The return channel doesn't survive the session").

#### Seat-access doors

A seat's own contract (what `dispatch-ticket` and its kin actually do) is one thing; HOW a
caller reaches it is a separate design question this skill owns too — three structurally
different doors, none a synonym for another, and nothing in a bare seat name reveals which one a
given caller gets:

1. **Session adoption** — a `/bind-*` command (`/bind-build`, `/bind-team`, `/bind-planning`) and
   its skill-as-command shape make the CURRENT session hold a standing agent's contract
   in-place, with no `Agent` spawn and no fork. Nothing left the session, so its interactive
   branches — a live clarifying question, an `AskUserQuestion` round — stay reachable turn after
   turn for as long as the session runs. Pick this door when a human is going to feed the seat
   more than one target in a row.
2. **`context: fork` execution** — a `disable-model-invocation: true`, `user-invocable: true`
   command (`/build-feature`) runs its target's procedure as a fork (background by default) off
   the caller's own session, one target at a time. Forking relieves the CALLER's context, not the
   human: a fork can still reach the live user directly via `AskUserQuestion` mid-run. Pick this
   door for one known target, right now, from a session that wants to stay clean for whatever
   comes next.
3. **`Agent`-tool dispatch via a `*-leader` agent** (`build-leader`, `planning-leader`,
   `review-leader`) — the only door open to a genuinely unattended, programmatic caller with no
   live user at all: a coordinator, `mobilize-chores`, a `/goal` loop. No clarify round is
   possible here, so the dispatched engine's own unattended failure branches take over instead
   (report a named blocker, report SKIPPED) rather than asking anyone.

**Why three doors exist instead of one command serving every caller.** A
`disable-model-invocation: true` command is invisible to the `Skill` tool (issue #134/#135's
shared defect class) and to any agent's `skills:` preload (the same platform rule
`skill-writing-rules` names). That combined mechanical fact is why a door-2 command can never BE
door 3: nothing with `Agent`-tool access can reach it directly. So
the actual procedure lives once in a plain, Skill-tool-reachable skill (e.g. `dispatch-ticket`),
and each door is a thin wrapper invoking that same engine inline — this is the **`*-leader` twin
rationale**: every command shaped like door 2 earns a same-shaped `*-leader` agent as door 3, not
because the two ever duplicate logic, but because a command's own `disable-model-invocation` flag
structurally forecloses the one door a programmatic dispatcher needs. Confusing the doors is a
recorded defect class, not a hypothetical: #134/#135 is the mechanical unreachability itself, and
the pattern recurs anywhere a new standing seat is designed without asking which callers need
which door. Rejected as a naming fix (ADR-0020, gh#518): renaming the doors doesn't change which
one a given caller can structurally use — the fix is knowing the three exist and picking by who's
calling, not a vocabulary change.

### 9. Design
1. **Solo-first — the host inline is the null unit and wins by default.** A seat must buy
   something the host cannot provide: isolation (fresh context), parallelism (genuinely
   concurrent slices), or independence (generator≠critic on a high-stakes artifact). A team must
   buy it twice. A dispatch that costs more context and latency than doing the work inline is
   over-orchestration, whatever the task's step count — then match the unit to the task and
   justify team fan-out by genuine parallel value.
   **The job-evidence test (new seats/flows only) — modeled directly on `plan-plugin-split`'s
   job-evidence rule, same shape, same rigor:** before a NEW coordination seat or multi-seat flow
   is added, its design records the evidence for why the main loop plus at most one
   Explore/checker dispatch cannot hold the job. Evidence is a concrete, named gap — an isolation
   need the host provably lacks (its own context is polluted or must stay clean for a later step),
   a genuinely concurrent slice competing for the same turn, or a generator≠critic split a
   high-stakes artifact requires — a template default ("systems eventually get a
   coordinator") or the step count alone ("it's multi-step, so it needs orchestration") is a
   question, not evidence (#4 already rejects that reasoning for depth, this test rejects it for
   existence). No cited gap → the seat/flow doesn't earn a place; the solo-first default above
   stands. This test gates
   NEW seats and flows going forward only — an existing seat already in an estate is not
   retroactively re-justified by it.
   **A worked precedent for a high-consequence serial operation:** a package-release cut run
   under a single-authorization model, INLINE in the operator's own session, spent real time on
   interactive consent relays that produced zero additional safety, while every actual protection
   (a pre-cut docs gate, a named trip-wire, a one-tag-per-push rule, a registry-verify step) fired
   deterministically regardless of who was watching. A dispatched form of a release-shaped seat
   earns its place only for a genuinely unattended context, and stays serial even there — a
   resumed dispatch continues the SAME cut, never starts a parallel one. · gen-ui-kit fleet-ops
   harvest (agent-ui#1115, comment 5317746661, lesson 14) · 2026-08-17 · [verified]
2. Each description a precise interface; `tools` scoped, `model` to task class, `skills:` only for standing expertise; verify keys against the installed build.
3. Keep teammate roles as subagent definitions (teams compose them at runtime).
4. Dispatch sealed and shallow: enumerate inputs, state the budget, name the typed return; depth ≤ 2 (host → specialist) — a third level needs justification, a fourth means the decomposition under-cut.
5. For a parallel BUILD team, dispatch the disjoint same-tree fan-out (`references/best-practices.md`): file- and import-disjoint slices concurrently in one tree, each worker self-gating its own path, the host running the whole-tree gate + negative controls at the wave boundary; worktrees only when slices must mutate overlapping files. **Precondition — the HOST owns git; workers only edit files.** A worker that drives its own branch/commit/PR lifecycle (e.g. a `build-lead`/`dispatch-ticket` dispatch) is outside this shape entirely: two such workers race on the shared index/HEAD regardless of file disjointness, so they take per-worker worktree isolation whenever concurrent — file-disjointness licenses parallel timing there, never same-tree sharing (incident 2026-08-11: this step's conclusion copied without the precondition shipped a blocking same-tree race in a sibling skill).
6. Self-score (below); fix until every gate dimension (D2, D4) ≥ 3.

### 10. Review
1. This skill's gates are systemic judgment, not a single-file mechanical check — there is no `harness_checks` subcommand: D2 is judgment because whether a description is a precise interface only shows against the sibling set (no string test sees it); D4's YAML-validity half IS mechanizable — its checker is queued, not built — so until it lands, score D4 by inspection and mark uninspected fields skipped-not-passed. Score against `references/rubric.md`, citing evidence on the 1–5 anchors.
2. Check plane separation first (the top failure: expecting `/goal` to select capabilities).
   For any NEW seat or multi-seat flow in the arrangement, check the job-evidence test (Design
   #1) was actually recorded — a cited gap, not an assumed one; an unjustified new seat is a D1
   finding.
3. Findings by severity; gate verdict; top issues with a concrete fix each. **Generator ≠ critic:** for a high-stakes system dispatch the independent **`wiring-checker`** (fresh context, scores this same rubric by inspection) rather than grading your own arrangement.

### Improve (repair an arrangement)
Review first, then close the gap — plane separation and connective tissue before polish. Fix the wiring, re-score, finalize only when every gate dimension (D2, D4) ≥ 3. (Improve = review + targeted redesign.)

### Update (re-sync after drift)
Wiring drifts two ways. The BUILD moves: frontmatter keys and `skills:` preload semantics change — re-verify every field against the installed build (the rubric's D4 "verified against build" anchor is the check). The CAPABILITY SET moves: a skill or agent is added, renamed, or retired — re-review every description, preload, and fence that referenced it. Either change re-opens the gate dimensions.

### Output contract (review)
```
Artifact: <system/frontmatter>  ·  Rubric: rubric-orchestration
| Dim | Type | Score | Finding | Evidence |
Gate (D2,D4): <pass/fail>
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `[[parallel-work-rules]]` | Deciding whether work needs git-tree isolation, or resolving a live collision once discovered — Section 6's own citation for the cwd-race detection mechanics this playbook unblocks; also: a relayed report needs the same independent-verification discipline as a self-report, extended to any intermediary including your own dispatcher |
| `[[loop-rules]]` | When the next turn fires — this skill never governs continuation timing |
| `mobilize-chores` (this plugin) | The canonical four-layer double-dispatch guard Section 2 cites; also owns which tickets are mobilizable in the first place |
| `[[dispatch-ticket]]` | The canonical ADR-0005 claim realization (Section 2) and the version-collision re-checks (Section 4) |
| `harness:big-change-git-rules` | The stacked-PR retarget-then-delete sequence and the version-slot evidence (Section 4) — cross-plugin soft mention, degrades gracefully where harness isn't installed |
| `harness:agent-writing-rules` | Encoding the teammate-mode delivery clause and the generic-identity caveat (Section 3) into an actual agent file |
| `team-scaffolding` / `fleet-bootstrap` (this plugin) | The worked realization of Section 1's coordination scope ladder (fleet-scoped introduction, #429) |
| `.claude/ops/fleet.json` / `fleet-roster.md` | The durable records Sections 1, 3, and 5 all read from and write to |
| `agents/fleet-marshal.md` / `bind-team` (this plugin) | Section 7's worked realization on the seat's two doors — the dispatched and host-adopted forms of the same route-anything-incoming discipline |
| `docs:file-bug` / `docs:file-feature` / `docs:file-task` / `docs:file-leftovers` | Section 7's owning intake skills for a raw report with no record yet — cross-plugin soft mentions, degrade gracefully where docs isn't installed |
| `references/rubric.md` | Scoring dimensions and anchors for Part B's Review (judgment-based) |
| `references/best-practices.md` | Part B design guidance / explaining a finding |
| `references/foundations.md` | When a Part B finding turns on a shared model (discovery vs continuation) |
| `harness:write-handoff` | The return contract a composed agent hands back — the other half of composition; its "Sealed vs. messaging" note states which channel carries the block (a sealed dispatch's Findings entry, or a named teammate's mailbox message) — never re-derive that split here |
| `references/handoff-fallback.md` | The inline eight-field fallback for an agent body when `write-handoff` isn't installed — the one referenced copy every teamwork agent cites instead of hand-restating the block |

**Done** when a fleet seat states its coordination scope before polling anyone, claims and
guard-checks before dispatching, reports before going idle and treats a report as superseding any
later nudge, names its plugin version slot before a build starts, leaves worktree/branch state a
successor can inventory, answers a stuck pin with `EnterWorktree` re-pin rather than manual cd
repair, routes every incoming item to its owning seat/skill/door within the turn it arrived rather
than absorbing it, AND every unit matches its task shape (the null unit respected — no seat doing
host-inline work), every description is a precise fenced interface, frontmatter is verified
against the build, dispatches are sealed and typed, both Part B gate dimensions (D2, D4) score
≥ 3, and a high-stakes arrangement carries its independent wiring-checker pass. **NOT done** while
any of the seven Part A areas is being re-derived from first principles mid-run instead of applied
as the default it already is, while an orchestrator absorbs a "just this once" small fix instead
of routing it, or while a Part B description starves the router, a fence is one-way, a dispatch
leaks history or lacks a budget, planes are conflated, or the only score an arrangement has is its
designer's.
