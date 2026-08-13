---
name: dispatch-ticket
description: >-
  Use when invoked by name from /build-feature's body, the build-lead agent, or a /lead-build
  session driving its targets — never model-routed from a raw ask. Finds or mints the target's
  record, then branches by kind: feature → size solo-first and build under a mandatory Findings
  write-back contract; task → clarify with one find-intent round, then dispatch under the same
  contract; bug → hand to file-bug with the redirect marker. One shared procedure for all
  callers (ADR-0010). NOT a trigger for a raw "build this" ask (/build-feature or /file-feature
  own that); NOT for finding or batch-confirming which tickets to build (mobilize-chores).
disable-model-invocation: false
user-invocable: false
---

# dispatch-ticket

The procedure behind `/build-feature`, the `build-lead` agent, and a `/lead-build` session's
standing seat — one engine, three reachable entries. `/build-feature` itself is `disable-model-invocation:
true` — command-only, unreachable via the Skill tool or agent preload (issue #134/#135's shared
defect class: a flag meant to keep a command human-typed also blocks every programmatic path to
the same logic). This skill carries the actual procedure; `/build-feature`'s body and the
`build-lead` agent both invoke it rather than each carrying their own copy. Generalized from
`dispatch-feature` per ADR-0010: one confirmed ticket of ANY kind — feature, task, or bug — the
kind branch below picks the path. This skill deliberately carries no `context: fork` of its own —
rationale in `/build-feature`'s body (no double hop from that caller, no needless third hop from
`build-lead`). Seed: $ARGUMENTS.

## Phase 1 — Find or make the record

- `$ARGUMENTS` is a resolvable ticket id (`TKT-####`, a bare issue number on the git-native
  backend, or an adapter-native id) → that's the record — branch on its STATE first:
  `done`/`wontfix`/closed → report the closed state and stop (reopening is the user's call);
  otherwise read its kind, Size/Scope/Links, and continue to Phase 2.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names — records (`docs/tickets/`,
  ROADMAP/PLAN, or the resolved backend's open issues), the codebase, and existing docs/corpora:
  a queued match → build from it; a match that already shipped → report where it lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — its opt-in
  project-docs index offer rides along; apply its phases inline where not: extract → dedup →
  size/shape → lint-clean `kind: feature` ticket, no index offer without docs' template), invoked
  via the Skill tool with the seed prefixed `[nested-intake]` — file-feature's own Phase 6 gates
  its index-bootstrap offer off this marker, since a nested intake already owes this skill's own
  ambiguity question and file-feature's Phase 2 round; a third `AskUserQuestion` from one
  background run is one too many. A raw seed reaching this skill is feature-shaped by its
  callers' own contracts; the intake's own classification still redirects a disguised bug or
  chore per its rules. The record exists on disk before any build effort is spent — ticket-first
  is the entire loss-window fix, and it does not move.

A record whose Shape is knowledge (routed to reference/corpus work at intake) is not built
here — report that routing and stop; docs' seats own it.

## Phase 2 — Branch by kind

- **`kind: bug`** → this is `file-bug`'s work, but isolate BEFORE handing off (per Phase 3's own
  scoping below) — its Phase 5 can fix a root-cause-evident bug inline (real tree mutation), so
  this dispatch is what has to guarantee containment, not the skill it hands off to: run Phase 3's
  isolate bullet now (no claim — `file-bug` owns its own record lifecycle, so none is taken here
  on its behalf), THEN invoke `file-bug` via the Skill
  tool carrying the ticket id, seed prefixed `[redirected-from:dispatch-ticket]` (file-bug's own
  marker protocol — the round budget was already spent here, and file-bug's forked run has no
  other way to know). This is what makes the inline-fix path safe: MEASURED (2026-08-11 live
  probe) that a `context: fork` skill invoked from inside a worktree-isolated context executes
  entirely inside that worktree, never escaping to the host checkout — so the isolation just
  established contains whatever `file-bug`'s own fork does next.
  The RECORD is the return channel, not the fork's transcript — VERIFIED (A4 smoke test,
  2026-08-10): a `context: fork` skill invoked from inside an agent
  dispatch runs as a background fork, and its completion notification routes to the ROOT
  session, not the invoking seat — a seat that waits on the fork's return strands idle forever.
  So after the hand-off, read the ticket back (Phase 6's verbs) and report "handed to
  `file-bug`; read-back shows <state/Findings>"; never wait on the fork's transcript. Phase 3's
  claim, Phase 4's sizing, and Phases 5–6 never run for a bug — only Phase 3's isolate bullet
  does, and only right here.
- **`kind: task`** → **clarify, then dispatch — never blind.** Tasks carry no fixed execution
  verb the way features do (`file-task`'s own scope is deliberately heterogeneous: chores,
  follow-ups, research items, debts), so run `find-intent` (harness, where installed; its
  discipline inline otherwise) on the ticket's full body first — ONE batched clarifying round
  maximum, and only when something is genuinely ambiguous AND an interactive user is present
  (the same interactive-user test the Phase 1 ambiguous-match failure branch applies; a
  `build-lead` dispatch has no one to ask — a ticket that's already clear proceeds with zero
  rounds either way). Still not concretely actionable (no clear "what would done look like") →
  report SKIPPED with the named gap, never dispatch on an unclear brief — no claim is taken on a
  SKIPPED task, since no build effort was ever going to start. Otherwise run Phase 3 (claim, then
  isolate) first, then dispatch via the `Agent` tool — `subagent_type: general-purpose` as the
  default (`team-or-solo-rules`' solo-first/null-unit reasoning: a generic task needs no tool
  restriction, parallelism, or multi-skill preload); a specific named agent only when the
  clarified brief genuinely needs one of those three properties. The dispatch prompt is sealed
  per Phase 5's contract — the CLARIFIED BRIEF (the round's answers travel in the seal; the
  dispatched agent cannot see the clarify conversation), the record, the write-back verb per the
  resolved backend, a dated Findings-equivalent entry at each significant result. A task is ONE
  sealed dispatch — Phase 5's `/goal` try-cap wrapper is the feature path's, not inherited here
  (matching the absorbed original). Then close the loop per Phase 6, including its status verbs
  (`doing`/`done`+close/`wontfix`+close, per the backend) and its one-re-dispatch rule.
- **`kind: feature`**, a record minted fresh in Phase 1, and the default arm — a pre-existing
  record carrying no kind, or an unrecognized one → continue: Phases 3–6 (the pre-ADR-0010
  behavior: anything neither bug- nor task-kinded nor closed takes the feature path — `/build-feature`
  can be handed any id, and an unlabeled issue builds rather than falls through undefined).

## Phase 3 — Claim, then isolate

Runs once Phase 2 resolves to real tree-mutating effort — never for a Phase 1 stop
(closed/shipped-elsewhere/knowledge-routed: no build effort is about to start, so there is
nothing to claim or isolate). Its two bullets have different scopes: **claim** is the build
path's own — the feature path (fresh-minted or pre-existing, before Phase 4's sizing) and task's
actionable branch (after `find-intent`'s round, once concretely actionable, before its Agent
dispatch) — never for the bug hand-off, since `file-bug` owns its own record lifecycle and takes
whatever claim it needs on its own terms, not this skill's to take on its behalf. **Isolate** is
broader: every tree-mutating path runs it, including the bug hand-off in Phase 2 above —
`file-bug`'s own body carries no worktree mechanics of its own, so this phase is what actually
contains its inline-fix path, not an assumption that the hand-off target handles it.

- **Claim first.** Decide the branch name now — an issue-mapped name (`<id>-<short-slug>`, or this
  repo's own `<domain>/<id>-<slug>` convention where one is established) — then take ADR-0005's
  `claim` operation (`doc-writing-rules`' `references/backend-resolver.md`, its seventh operation;
  this dispatch is its first real caller, not a new mechanism invented here): git-native — `gh
  issue edit --add-assignee @me` plus a `gh issue comment` naming the claimant
  (`build-lead`/`dispatch-ticket`), a UTC timestamp, and the decided branch name; file backend —
  the record's `claimed-by`/`claimed-at` frontmatter pair; an adapter — its own realization.
  **Re-read the record** (Phase 6's `read` verb) before proceeding: a claim comment timestamped
  earlier than this one, from a run that isn't this one, means this caller lost the race (tie-break
  per ADR-0005: lower identity string wins on an exact timestamp tie) — abandon immediately, no
  worktree created, no release needed (this claim never landed), and report the loss as a named
  blocker (someone else's in-flight work) rather than guessing which claim is real.
- **Once the claim wins the race, make it LIST-VISIBLE too (#199).** The claim comment above is
  durable but invisible in the GitHub issue LIST view — Kim's own report: "I cannot tell that
  Issues are claimed or in some kind of 'doing' state." Git-native only: `gh issue edit --add-label
  in-flight`. This repo's own `in-flight` already carries `FBCA04` — the same hex `doing` uses, a
  coincidence from when it was created, not a signal the two labels are related; never treat a
  shared color as evidence two labels mean the same thing. A repo that doesn't carry `in-flight`
  yet creates it with that exact name, but a hex distinct from whatever its own `doing`-equivalent
  already uses — never invent a different NAME, and never pick a color collision fresh when one
  isn't already load-bearing. This is additive to the assignee+comment claim mechanic
  above, not a replacement for it: assignee stays required exactly as ADR-0005 already ratifies it
  (`backend-resolver.md`) — this skill's own addition sits deliberately outside that operation,
  since #199's own ask is list-visibility, which the label now supplies, not a redesign of the
  claim operation itself.
  **`in-flight` is the ONE canonical claim label — never mint a synonym.** `doing` is a DIFFERENT,
  pre-existing, load-bearing label: the git-native status vocabulary `file-bug`/`file-task`/this
  skill's own Phase 6 already use for the `open`→`doing`→`done` status verb (`backend-resolver.md`'s
  `update` operation), unrelated to claiming — a live incident (#192) shows the confusion this
  invites: that dispatch applied `doing` alongside `in-flight` mid-claim, which read like an
  accidental duplicate but wasn't. The two legitimately coexist on one issue at once — "is this
  claimed" and "what lifecycle stage is this at" are different questions — so `doing` is never
  deleted, never reused as a claim signal, and no label is ever minted to duplicate what
  `in-flight` already says.
  **Label = display, comment = record — never the reverse.** `in-flight` is hand-editable and
  therefore NEVER the correctness gate on its own: `mobilize-chores` step 2 (below) may read it as
  a cheap pre-filter, but the claim comment — plus, once a PR exists, `mobilize-chores` step 2's
  own GraphQL PR-linkage check — stays the authoritative source of whether a ticket is actually
  claimed. **Removed on every
  terminal outcome, never left stale:** Phase 5 stage 2 removes it the moment a PR opens (the open
  PR becomes the visible signal instead — see that stage; on a task or big-feature dispatch this
  is one more line the sealed prompt names, since the seat opening the PR never loaded this
  SKILL.md itself); the Release-on-abandonment bullet below removes it on a mid-flight abandon,
  and on the recorded-loss ending too (Phase 6: a dispatched agent that never returns its Findings
  and can't be re-dispatched — that dead end releases the same way an abandonment does, since
  nothing else ever will). A task SKIPPED in Phase 2 never reaches this bullet at all
  (no claim is taken on an inactionable task), so it never had the label applied and owes no
  removal either — the same pre-claim/post-claim split Phase 3's own scoping already draws. Cheap,
  optional, not this skill's to manage: a coordinator running a serial chain (`mobilize-chores`)
  may also carry the pre-existing `queued` label (`C5DEF5`) to mark a ticket's place in that chain
  ahead of its own claim — nothing here touches `queued`'s lifecycle, only leaves it alone.
- **Isolate second.** Decide the branch name FIRST: the claim bullet's own decided name, when one
  ran (feature/task) — or, when isolate runs alone with no claim before it (the bug hand-off), a
  lightweight name of its own (`bug/<id>`, decided here since no claim bullet named one). Only
  then check reuse, and key it off IDENTITY, never path shape, on BOTH of these conjuncts — either
  one missing means create, never reuse: (1) the cwd is a linked worktree, not this repo's primary
  checkout (the #180/#182 residue this file already cites below is exactly a stale branch left
  checked out IN the primary checkout — a decided-name match there must never license reuse, since
  reusing the primary checkout for a build is the very failure Phase 5's environment-clean line
  exists to catch); AND (2) that linked worktree's already-checked-out branch matches the name
  just decided (a resumed `build-lead`/`lead-build` re-entering its own isolation for the same
  ticket — the decided name embeds this ticket's own id, so a branch match against it is identity,
  not path shape). A bare "cwd sits somewhere under `.claude/worktrees/`" is NEITHER conjunct and
  is never sufficient by itself — the #191 fix: a caller's own long-lived worktree for an unrelated
  purpose (`mobilize-chores`'s own dedicated worktree, say) also matches that path shape, and a
  nested dispatch that reuses it on path shape alone checks the wrong ticket's branch out on top of
  the caller's own tree. Either conjunct fails → create one now (`git worktree add`,
  off a clean `main` HEAD) and run every remaining step inside it. **Isolation itself is
  unconditional — even for a single serial dispatch with no concurrent sibling** — worktree
  *creation* is the only conditional part (reuse vs. create). This is the fix for the #180/PR
  #182 defect (2026-08-12: that build ran in the HOST checkout with no worktree at all and left
  its feature branch checked out on return; the coordinator repaired it by hand). Never build in
  the host's shared checkout, regardless of how many other dispatches are running — and never reuse
  an unrelated worktree standing in for one, regardless of how deeply nested the dispatch is
  (#191).
- **Release on abandonment — post-claim exits only.** Only a failure that happens AFTER this
  claim landed can have anything to release: a discovered design fork routed back to planner, a
  gate failure recorded but unresolved (both mid-flight, per the Failure branches below), or
  Phase 6's recorded-loss ending (a dispatched agent that returned with no Findings entry, the
  one re-dispatch also came back empty, and the loss gets recorded rather than chased further —
  nothing is ever coming back to open a PR, so this is exactly as dead as a mid-flight abandonment)
  — every one of these releases the claim before returning: git-native — `gh issue edit
  --remove-assignee @me --remove-label in-flight` plus a `gh issue comment` naming the release and
  why; file backend —
  clear `claimed-by`/`claimed-at`; an adapter — its own release realization. **The label release is
  not optional** — a dead dispatch must never leave a stale `in-flight` label behind (#199 extends
  #184's release-discipline to the label the same way it already covers the assignee and comment;
  a label left standing after abandonment reads as still-claimed to both a human scanning the issue
  list and `mobilize-chores` step 2's own pre-filter). A **pre-claim** exit has
  nothing to release, because Phase 3 never ran for it: a task SKIPPED in Phase 2 (no claim taken
  on an inactionable task, per Phase 2's own text) and an ambiguous-match blocker in Phase 1 (the
  record was never even confirmed) both end the dispatch before this phase starts. A **lost claim
  race** (above) also has nothing to release — that claim never landed either. Post-claim release
  is what keeps a mid-flight abandonment from permanently blocking the ticket for the next sweep —
  `mobilize-chores` step 2 excludes on an active claim the same way it already excludes on an
  open in-flight PR.
- **Tear down a no-longer-needed scratch branch/worktree — verified, never raw.** Two cases reach
  this: the abandonment bullet above (a design fork or unresolved gate failure, once the claim is
  already released), and Phase 2's bug hand-off — and there ONLY once the post-hand-off read-back
  (Phase 6's verbs) shows a terminal state: the issue closed, or a `file-bug` Findings entry marking
  its own run done, with nothing landed on the branch this dispatch created for it. Short of that
  observable, the worktree stays standing, reported as residue — never torn down while `file-bug`'s
  own fork may still be live inside it (Phase 2's own text: never wait on that fork, but never guess
  it has finished either). Either case: never retire the branch with a raw `git branch -D` plus
  worktree removal — that force-deletes work on nothing more than this seat's own say-so. Feature-
  detect the host repo's own gated reap script (the reference shape: gen-ui-kit's exact path
  `scripts/ops/reap-branches.mjs --verify-branch <name>` — a differently-located script counts only
  if the host repo's own docs declare the same 0/1/2 contract) and gate the delete on its exit code
  alone, never on this skill's own judgment. Order matters: `git worktree remove` first (it refuses
  on a dirty tree, so nothing is lost even on a wrong call), THEN `--verify-branch`, THEN — only on
  exit 0 (provably merged: a merge-base ancestor of `origin/main`, or an exactly-matching MERGED
  PR) — `git branch -d` (never `-D`, even after a verified 0). Exit 1 (KEPT/PROPOSED), or either
  verb refusing outright (a dirty worktree, an unmerged `-d`), → leave the branch standing and
  report why, never escalate to a force flag. Exit 2 is a usage error, not a keep/delete verdict —
  report it rather than treating either guess as the answer. Where the host repo ships no such
  script at that path, fall back to an unverified `git worktree remove` then `git branch -d`, but
  never silently — name in the report exactly what went unverified (no merge-base or MERGED-PR
  check ran before this delete).

## Phase 4 — Size the dispatch (solo-first, feature path)

The record's Size class picks the machinery — the same materiality floors the seats themselves
carry, applied from the caller's side:

- **small** — the host builds it inline, or one sealed fork/agent when isolation or tooling
  demands it — an agent only for tool restriction, parallelism, or multi-skill preload; a fork
  for everything else (harness's fork-vs-agent gate, applied inline where harness is absent). No planner, no
  coordinator, no team: a task one context can hold is the host's own. A small build that
  semantically edits a prompt-carrying artifact (a SKILL.md body, an agent definition, a hook
  prompt) still gets a fresh-context checker pass (the matching `*-checker` agent) before the
  loop closes — lint and gates prove mechanics, not semantics (the 2026-08-11 estate audit found
  every recent unaudited semantic edit carrying a real gap); pure code/config under the repo's
  own test gates needs no checker seat.
- **big** — the delivery seats, each already floored: `planner` authors what the change
  earns (the record's Links may already carry the docs — don't re-author), `builder`
  implements to the approved LLD, `code-checker` grades the slice before merge. The coordinator
  seat only when the chain genuinely spans ≥2 seats across contexts. On a `/build-feature`-initiated
  call this makes host→fork→coordinator→seats, a third level past team-or-solo-rules' default
  depth ≤ 2 — named justification, not an accident: the fork isolates the CALLER's session
  (`context: fork` on `/build-feature`), the coordinator isolates the multi-seat delivery chain
  (planner/builder/code-checker each need their own turn) — two different things being kept
  separate, not one dispatch nested inside another for no reason. The same justification holds
  on a `build-lead` dispatch — the agent context takes the fork's place as the layer isolating
  the caller; host→agent→coordinator→seats is the identical shape.

## Phase 5 — Dispatch under contract: the four lifecycle stages

Every build dispatch — feature or task alike — owns its full execution lifecycle end to end, not
merely the code change (the #183 fix: a dispatch that stops at "code written" leaves the caller to
discover and repair branch/worktree residue by hand):

1. **Isolated execution by default** — Phase 3's claim-then-isolate, already done before this
   phase starts.
2. **Branch + commits + PR opened**, per ADR-0002. Commit meaningfully as work lands (not one
   giant commit at the end), push the claimed branch, and open exactly one PR against `main`
   carrying `Closes #<id>` (every id this dispatch closes, on a folded campaign), a plain
   what/why, the gate output for every touched plugin, and an integration-notes line naming any
   known overlap with other open PRs — adopt another PR's already-defined shared field wording
   where one owns it, never mint a competing definition. **The moment the PR opens (git-native
   only), remove the `in-flight` claim label** — `gh issue edit --remove-label in-flight` — the
   open PR itself is now the visible in-progress signal, so the claim label's job is done; leaving
   it on past this point is exactly the stale-display defect #199 exists to close (#192 is the live
   example: its PR merged and closed the issue with `in-flight` still sitting on it, because this
   step didn't exist yet). The claim comment and assignee stay untouched here — this is a display
   change only, not a release; nothing about the ticket's ownership record changes.
3. **Verified-clean retirement before the seat retires** — never assumed. State the result on
   three axes explicitly: the worktree's own git status (clean, nothing uncommitted left behind),
   the local feature branch (pushed and named — this seat never merges its own PR, per ADR-0002's
   human-gated merge), and the host checkout (untouched — Phase 3's isolation makes this the
   normal case, not a hoped-for one; still stated, never inferred from "no error happened").
4. **A typed retirement handoff proving each step**, not just an outcome: the PR URL, the
   Findings write-back's own comment URL on the resolved backend (below), and one explicit
   environment-clean line naming stage 3's three axes by result — never a silent "done".
   `build-lead`'s own return contract (`agents/build-lead.md`) carries this line through
   verbatim to whatever dispatched it.

Every dispatch is also sealed under the write-back contract already in force: the ticket path +
enumerated inputs + budget + the typed return + stage 2's own `--remove-label in-flight` call at
the moment the PR opens (the sealed prompt names this explicitly on a task or big-feature
dispatch, since the dispatched agent/seat opening the PR never loaded this SKILL.md itself and has
no other way to know the label needs clearing), and a **mandatory dated `## Findings` write-back
at each significant result** (slice built, gate green, PR opened), not only at the end, so an
interrupted build still left evidence. The write-back verb follows the resolved backend:
git-native — the issue number, `gh issue comment`; file backend — the TICKET file's path, editing
its `## Findings` section; an external adapter — its `update` operation. Run under `/goal` with a
try-cap (5, per loop-rules's feature-ticket recipe — the feature path only; task's single sealed
dispatch, per Phase 2's own text, carries no try-cap wrapper): named stopping predicate, capped
tries, escalate on the same failure twice.

## Phase 6 — Close the loop

Read the ticket back (git-native: `gh issue view --comments`; file backend: re-read the file; an
adapter: its `read` operation). Findings gained entries and the work shipped → advance status
(`open`→`doing`→`done`; git-native `done` closes the issue, `wontfix` closes with the label and a
reason comment — matching `file-bug`'s own Phase 6 status verbs) and report path + status + what
shipped, plus Phase 5's environment-clean line — stated, never inferred from silence. An agent
that returned without its Findings entry → one re-dispatch with the contract quoted, then record
the loss with a dated entry and say so plainly; a fork no longer addressable skips straight to
recording — it cannot be re-dispatched into. Either way, recording the loss is itself a terminal
outcome with nothing left to come back and open a PR, so it releases the claim right there — the
Release-on-abandonment bullet's own full release (Phase 3: `--remove-assignee @me --remove-label
in-flight`, PLUS the release comment naming why — never just the flags with no comment, since
comment stays the durable record even when the label is what a human notices first). A
conversational summary never substitutes for the entry the record was owed.

## Failure branches

- Claim lost the race in Phase 3 (an earlier-timestamped competing claim found on re-read) →
  report as a named blocker (someone else's in-flight work) and stop; never overwrite the winning
  claim, never guess which run owns the ticket. The `in-flight` label is only ever applied AFTER
  the race check confirms a win, so a losing claim never had one to remove.
- Ambiguous match in Phase 1 (two plausible records) → **with an interactive user present**, ask
  which, one question, then proceed. A `/build-feature`-initiated call counts as having an
  interactive user present even though it runs inside that command's fork (`context: fork`) —
  forking relieves the caller's session, it does not remove the person, and `AskUserQuestion`
  still reaches them directly. **Dispatched with no interactive user** (e.g. via `build-lead`,
  from `mobilize-chores`) → report the ambiguity as a named blocker instead of asking — the batch
  confirm already spent the user's one gate for this run, so raising a second, mid-dispatch
  question has nowhere sanctioned to land regardless of what the channel can technically reach —
  same discipline as this plugin's other unattended failure branches (`close-session`,
  `mobilize-chores`); never guess which record was meant.
- A raw (recordless) seed that is bug-shaped → `file-bug` (docs) owns it from intake, not a
  build; the Phase 2 bug branch covers a ticket that already exists. This dispatch never invokes
  `file-bug` directly for a recordless seed itself (Phase 1's nested-intake hand-off does, ahead
  of any kind branch) — no isolate call is owed here on top of it.
- A task's clarify round exhausts without a clear brief → SKIPPED with the named gap (Phase 2);
  a skipped task is a reported outcome, not a failure.
- Build blocked mid-flight by a discovered design fork → escalate to the record (a dated Findings
  entry naming the fork) and, for big work, back to planner — never silently edit the
  contract.
- Gates fail at the wave boundary → the failure routes to the seat that caused it; the ticket
  stays `doing` with the failure recorded.

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker/skip), status reflects reality, a PR this dispatch opened carries an explicit
environment-clean line proving worktree/branch/host-checkout state, an abandoned claim was
released rather than left standing, and no build effort was spent before the record existed —
or the bug branch isolated first and then handed over with the redirect marker and the read-back
snapshot (state/Findings as of hand-off) relayed; the fork's own outcome is never something this
seat waits on.
