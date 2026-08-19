---
name: dispatch-ticket
description: >-
  Use when invoked by name from /build-feature's body, the build-leader agent, or a /bind-build
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

The procedure behind `/build-feature`, the `build-leader` agent, and `/bind-build`'s standing seat
— one engine, three entries. `/build-feature` is `disable-model-invocation: true` (command-only,
unreachable via the Skill tool or agent preload — issue #134/#135's shared defect class), so this
skill carries the actual procedure and both callers invoke it rather than duplicating it.
Generalized from `dispatch-feature` per ADR-0010: one confirmed ticket of ANY kind — feature,
task, or bug — the kind branch below picks the path. Carries no `context: fork` of its own (no
double hop from `/build-feature`, no third hop from `build-leader` — rationale in `/build-feature`'s
body). Seed: $ARGUMENTS.

**No nested wait.** A seat already running as a nested dispatch (`build-leader`, via the `Agent`
tool — not `/bind-build`'s own standing seat, which spawns no Agent and isn't nested) performs
Phase 3's isolate work and Phase 4's `small` build DIRECTLY in its own tree (worktree or scratch-clone, per Phase 3's ladder), never a
further nested `context: fork` or NAMED `Agent`-tool dispatch for that core work: a
background/mailbox dispatch from inside an already-dispatched agent completes to the ROOT
session, never back to the dispatching seat (Phase 2's bug hand-off cites the same finding,
verified A4, 2026-08-10) — the callback structurally never arrives, stalling the seat until a
coordinator re-dispatches it (four measured incidents: #257, #282, #269, #280 — #282 additionally
raced a duplicate build). This narrows Phase 4's `small` "one sealed fork/agent" clause to a
TOP-LEVEL host only, and makes Phase 2's task-kind dispatch always UNNAMED — its synchronous
tool-result IS the return value, not mailbox-routed. Not a rule against dispatching generally: an
UNNAMED, single-shot review dispatch (Phase 4's checker, Phase 5 stage 2b's critic) isn't this
failure, since completion is normally the tool call's own synchronous result — one dated exception below.

**The critic step still stalls the same way — read the return value yourself, but a notification
can be the real verdict too.** Read a synchronous return if the call gives you one; if a
notification reports completion instead, that notification IS the verdict — accept and relay it
(report-before-idle). Escalate a stall only when NEITHER arrives within ~10 minutes. Full incident
history (issue #554's correction, PR #368 and PR #547) lives in
`references/critic-dispatch-completion-notes.md` (F6 split) — read it once for the "why", not
needed to apply the rule above.

## Phase 1 — Find or make the record

- `$ARGUMENTS` resolves to a ticket id (`TKT-####`, a bare issue number on the git-native backend,
  or an adapter-native id) → that's the record. Branch on STATE first: `done`/`wontfix`/closed →
  report and stop (reopening is the user's call); otherwise read kind/Size/Scope/Links/labels and
  continue to Phase 2.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names (records, codebase, existing
  docs/corpora): a queued match → build from it; a match that already shipped → report where it
  lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — opt-in index
  offer rides along; apply its phases inline otherwise: extract → dedup → size/shape → lint-clean
  `kind: feature` ticket, no index offer without docs' template), via the Skill tool, seed prefixed
  `[nested-intake]` — file-feature's own Phase 6 gates its index-bootstrap offer off this marker
  (a nested intake already owes this skill's own ambiguity question plus file-feature's own Phase
  2 round; neither runs live past this point — `file-feature` invoked here runs inside whatever
  fork or dispatch this skill itself is already running under, and a `context: fork` background
  dispatch has no `AskUserQuestion` channel at all, gh#541 — so both are capture-with-gaps, and
  the marker exists to stop a third capture-with-gaps close-out from piling redundant unasked-
  question noise onto the same record, not to protect a live round budget). A raw seed reaching
  this skill
  is feature-shaped by its callers' own contracts; the intake's classification still redirects a
  disguised bug or chore. The record exists before any build effort is spent — ticket-first is the
  entire loss-window fix, and it does not move.

A record whose Shape is knowledge (routed to reference/corpus work at intake) is not built here —
report that routing and stop; docs' seats own it.

## Phase 2 — Branch by kind

- **`kind: bug`** → this is `file-bug`'s work; isolate BEFORE handing off (Phase 3's isolate
  bullet runs now — no claim, `file-bug` owns its own record lifecycle), then invoke `file-bug`
  via the Skill tool with the ticket id, seed prefixed `[redirected-from:dispatch-ticket]` — or the
  verified form `references/bug-claim-provenance.md` names, if a claim sits on the record. Safe: a
  `context: fork` skill invoked inside a worktree-isolated context
  never escapes it (measured 2026-08-11) — so file-bug's fork stays contained. The RECORD is the
  return channel, not the transcript: a fork invoked from inside an agent dispatch runs in the
  background and its completion routes to the ROOT session, not the invoking seat (verified A4,
  2026-08-10) — waiting on it strands idle forever. After hand-off, read the ticket back (Phase
  6's verbs) and report "handed to `file-bug`; read-back shows <state/Findings>" — never wait on
  the transcript. Phase 3's claim, Phase 4's sizing, and Phases 5–6 never run for a bug — only
  Phase 3's isolate bullet does, and only here.
- **`kind: task`** → **clarify, then dispatch — never blind.** Tasks carry no fixed execution verb
  (`file-task`'s scope is deliberately heterogeneous), so run `find-intent` (harness, where
  installed; inline otherwise) on the ticket's full body first — ONE batched clarifying round
  maximum, only when genuinely ambiguous AND an interactive user is present (Phase 1's
  ambiguous-match test; `build-leader` has no one to ask — an already-clear ticket needs zero
  rounds). Still not concretely actionable → report SKIPPED with the named gap, never dispatch on
  an unclear brief — no claim taken, since no build effort was ever starting. Otherwise run Phase
  3 (claim, then isolate) first, then Phase 3.5, then dispatch via the `Agent` tool — `subagent_type:
  general-purpose` by default (`fleet-rules`' solo-first/null-unit reasoning: a generic
  task needs no tool restriction, parallelism, or multi-skill preload); a named `subagent_type`
  only when the clarified brief genuinely needs one of those three. Never a NAMED (teammate-mode,
  the Agent tool's `name:` field) dispatch here regardless of `subagent_type` choice: the caller
  only needs this seat's one final report, so a `name:` buys mailbox routing with nothing to
  address it to (`agent-writing-rules`' fanned-out-naming rule) — and when the caller is itself
  already nested (the no-nested-wait rule above), that misdirected mailbox delivery is a callback
  the caller structurally cannot collect on at all. The dispatch prompt is sealed per Phase
  5's contract — the CLARIFIED brief (the dispatched agent never sees the clarify conversation),
  the record, the write-back verb per backend, a dated Findings-equivalent entry at each
  significant result. A task is ONE sealed dispatch — Phase 5's `/goal` try-cap wrapper is the
  feature path's, not inherited here. Close the loop per Phase 6, including its status verbs
  (`doing`/`done`+close/`wontfix`+close) and its one-re-dispatch rule.
- **`kind: feature`**, a freshly minted Phase-1 record, and the default arm — a pre-existing
  record carrying no kind, or an unrecognized one — → continue: Phases 3–6 (the pre-ADR-0010
  behavior: anything neither bug- nor task-kinded nor closed takes the feature path;
  `/build-feature` can be handed any id, and an unlabeled issue builds rather than falling
  through undefined).

## Phase 3 — Claim, then isolate (or skip, under #204's preconditions)

Runs once Phase 2 resolves to real tree-mutating effort — never for a Phase 1 stop
(closed/shipped-elsewhere/knowledge-routed: nothing to claim or isolate). **Claim** and
**isolate** have different scopes. Claim is the build path's own — the feature path (before
Phase 4's sizing) and task's actionable branch (before its Agent dispatch) — never the bug
hand-off, since `file-bug` owns its own record lifecycle and takes whatever claim it needs on its
own terms. Isolate is broader: every tree-mutating path runs it (or evaluates the skip below),
including the bug hand-off — `file-bug` carries no worktree mechanics of its own, so this phase
is what actually contains its inline-fix path.

- **Claim first.** Decide the branch name now (issue-mapped `<id>-<short-slug>`, or this repo's
  established `<domain>/<id>-<slug>` convention), then take ADR-0005's `claim` operation
  (`doc-writing-rules`' `references/backend-resolver.md`, its seventh operation; this dispatch is
  its first real caller): git-native — `gh issue edit --add-assignee @me` plus a `gh issue
  comment` naming the claimant (`build-leader`/`dispatch-ticket`), a UTC timestamp, and the branch
  name; file backend — the record's `claimed-by`/`claimed-at` pair; an adapter — its own
  realization. **Re-read the record** (Phase 6's `read` verb) before proceeding: an
  earlier-timestamped competing claim means this caller lost the race (ADR-0005 tie-break: lower
  identity string wins on an exact tie) — abandon immediately, no worktree created, no release
  needed (this claim never landed), report the loss as a named blocker rather than guessing which
  claim is real.
  **A ticket claim is not a plugin-version claim — check the narrower resource too.** This
  workspace's own convention bumps the target plugin's version on nearly every merge
  (`CLAUDE.md`'s "never re-ship a version" rule), so two DIFFERENT tickets both landing on the
  same plugin race on the version field even when neither's ticket claim collided (the #284/#285/
  #290 cluster, each colliding with mid-flight-merged #289 or its authorkit sibling, 2026-08-16:
  `harness/skills/big-change-git-rules/references/who-ships-what.md`'s "Cross-PR version-claim
  coordination" section — one version-bumping build in flight per plugin at a time). Where
  `harness` is installed, run its `version_claim_check.py` (this workspace: `harness/scripts/
  version_claim_check.py <plugin-root>`) against every plugin this build is about to touch, right
  after the ticket claim lands — a sibling open PR already claiming that plugin's next version
  means rebase-and-rebump onto it rather than racing it, the same discipline as a lost
  ticket-claim race above. Re-run it before the PR opens (Phase 5 stage 2) too, since a sibling
  can appear mid-build. Where harness isn't installed, this check is skipped — named as such,
  never silently assumed clean, with the manual equivalent named in its place: `gh pr list
  --state open --json files` filtered to the plugin's own `.claude-plugin/plugin.json`.
  **A second, distinct race survives even a clean `version_claim_check.py` result: the VALUE
  race.** That check only catches a sibling OPEN PR claiming the same next version; it says
  nothing about a version already MERGED to `origin/main` since this branch was cut (issue #445 —
  two same-night PRs both shipped the same version because each bumped from its own stale
  branch-cut number, with no competing open PR to catch it — G14's monotonicity check now
  mechanizes this at the gate, but that fails LATE, at the gate, not before the PR is opened). So
  the Phase 5 stage-2 re-run (below) does two things, not one: re-run `version_claim_check.py` for
  the claim race, AND fetch + re-read every touched plugin's `plugin.json` straight off
  `origin/main` and bump from THAT value — never from the branch-cut version — carrying its
  README ledger line along with the same rebumped number. Doc spine ids race identically (#633) — `references/spine-id-value-race.md`.
- **Once the claim wins, make it LIST-VISIBLE too (#199)** — the claim comment is durable but
  invisible in the LIST view. Git-native only: `gh issue edit --add-label in-flight` (additive to
  the assignee+comment claim, never a substitute for it — `doing` is a separate, load-bearing
  status label, never reused as a claim signal). Removed the moment a PR opens (Phase 5 stage 2)
  or on any abandonment/recorded-loss ending. Full rationale — the color-coincidence note, the
  label-vs-comment authority split, `mobilize-chores`'s own `queued` label — lives in
  `references/in-flight-label-semantics.md` (F6 split).
- **Isolate second — now CONDITIONAL, not unconditional (#204).** Decide the branch name FIRST:
  the claim bullet's decided name (feature/task), or a lightweight `bug/<id>` (bug hand-off, no
  claim ran). **Skip isolation only when ALL FOUR hold** — sized `small`; no concurrent mutating
  dispatch exists (checked: no other live entry under `.claude/worktrees/` for this repo right
  now); the host checkout is clean on `main` with nothing in flight (checked: `git status`); no
  isolation-forcing reason applies (a nested dispatch always forces it — #207: the child gets its
  own isolation per the mitigation ladder below, or an explicit host-checkout authorization the
  parent names in Phase 5's sealed dispatch prompt, never an inherited skip). All four hold → build directly in
  the host checkout; the claim/write-back contract stays mandatory regardless. Never a silent
  revert to pre-#183 behavior: the skip is its own named branch, and Phase 5 stage 3's
  environment-clean line states which branch was taken.
  **Otherwise, isolate** — check reuse first, keyed on IDENTITY never path shape, both conjuncts
  required or create: (1) cwd is a linked worktree, not the primary checkout (a decided-name match
  IN the primary checkout never licenses reuse — the #180/#182 residue below is exactly a stale
  branch left checked out there); AND (2) that worktree's checked-out branch matches the decided
  name (a resumed `build-leader`/`bind-build` re-entering its own isolation — the name embeds the
  ticket id, so a match is identity, not shape). "cwd sits under `.claude/worktrees/`" alone
  satisfies NEITHER conjunct (#191: a caller's own long-lived worktree for an unrelated purpose,
  e.g. `mobilize-chores`'s, matches that shape too — reusing it on shape alone checks the wrong
  ticket's branch out on top of the caller's tree). Either conjunct fails → create (a live
  `EnterWorktree` session: `git worktree add` off clean `main`; an `Agent`-tool dispatch:
  scratch-clone per the ladder below, never a worktree), **then bootstrap before running anything else inside it**: a
  fresh worktree is a bare checkout, not a built one (gh#498, gen-ui-kit gh#1389) — feature-detect
  the host repo's `scripts/dev/bootstrap-worktree.mjs` (or its own declared equivalent) and run it
  unconditionally when present before any gate or check inside the new worktree, or a missing
  `node_modules`/build tree reads as a false-red regression (full mechanics, failure catalog, and
  why this can't be closed at the platform's own `EnterWorktree`/Agent-tool isolation layer:
  `big-change-git-rules`' `references/worktree-mechanics.md`). No such script → nothing to run,
  proceed as before. This isolate-when-used rule is what the #180/PR #182 defect fixed
  (2026-08-12: that build ran in the HOST checkout with no worktree and left its branch checked
  out; the coordinator repaired it by hand) — never build in the shared host checkout outside the
  four-precondition skip above, and never reuse an unrelated worktree standing in for one, however
  deeply nested (#191).
- **The mitigation ladder (#490/#609, ratified 2026-08-18)** — an `Agent`-tool dispatch has NO `EnterWorktree` reach, so scratch-clone is its DEFAULT rung, never a worktree; run `teamwork/scripts/pin_check.py <decided-branch-name>` first. Ladder + evidence: `references/isolation-ladder.md` (F6 split); read before isolating.
- **Release on abandonment — post-claim exits only.** Only a failure AFTER the claim landed has
  anything to release: a discovered design fork routed back to planner, an unresolved gate failure
  (both mid-flight, Failure branches below), a stale-premise exit (Phase 3.5), a spec-lock blocker
  (Phase 3.6), or Phase 6's recorded-loss ending (a dispatched agent returned with no Findings, the re-dispatch also came
  back empty — nothing is ever coming back to open a PR, as dead as a mid-flight abandonment).
  Each releases the claim before returning: git-native — `gh issue edit --remove-assignee @me --remove-label in-flight` plus a `gh issue comment` naming the release and why; file backend —
  clear `claimed-by`/`claimed-at`; an adapter — its own realization. **The label release is not
  optional** — a dead dispatch never leaves a stale `in-flight` label behind (#199 extends #184's
  release discipline to the label; left standing, it reads as still-claimed to a human scanning
  the list and to `mobilize-chores` step 2's pre-filter). A **pre-claim** exit has nothing to
  release, since Phase 3 never ran: a task SKIPPED in Phase 2 and an ambiguous-match blocker in
  Phase 1 both end before this phase starts. A **lost claim race** also has nothing to release.
  Post-claim release keeps a mid-flight abandonment from permanently blocking the ticket for the next
  sweep — `mobilize-chores` step 2 excludes on an active claim the same way it excludes an open in-flight PR.
- **Tear down a no-longer-needed scratch branch/worktree — verified, never raw.** Two cases reach
  this: the abandonment bullet above (claim already released), and Phase 2's bug hand-off, only
  once its post-hand-off read-back shows a terminal state with nothing landed on the branch. Short
  of that, the worktree stays standing, reported as residue. Never retire with a raw `git branch
  -D` — full procedure (the reap-script feature-detect, its exit-code gating, the unverified
  fallback) lives in `references/worktree-teardown.md` (F6 split); read it before tearing anything
  down.

## Phase 3.5 — De-stale a parked ticket (backlog/roadmap labels only)

Runs between Phase 3 and Phase 4's sizing (feature path), or between Phase 3 and the Agent
dispatch (task path, named verbatim in Phase 2 above). **Trigger:** the record carries `backlog`
or `roadmap` (#611; git-native: labels Phase 1 already read; file backend: N/A there, no parking
realization yet — disclosed in the seat's report, never silent). Label absent → this phase does
not exist, skip silently. The Phase 2 bug hand-off never runs it (`file-bug` owns its own
lifecycle). Full procedure — the premise-check algorithm, the
proceed/`stale-premise` outcome branches, and the outcome-class rationale — lives in
`references/de-stale-premise-check.md` (F6 split); read it in full before running this phase.

## Phase 3.6 — Spec-lock gate (draft/unlocked upstream, or a missing owed citation)

Runs immediately before Phase 4's sizing, feature path only, sibling to Phase 3.5. **Trigger,
either independently (ratified 2026-08-18):** a Links-cited upstream IDR/SPEC/ADR/RDD whose own
frontmatter `status:` is still pre-lock (a prose-only mention in the ticket never triggers), or
the owed ladder (`docs:doc-writing-rules`' Owed chain, full chain in
`references/spec-lock-gate.md`, cited not restated here) naming a rung with no citation at all.
Either → a named blocker, never a build — Phase 1's ambiguous-match class, not a new outcome
type. Full algorithm: `references/spec-lock-gate.md` (F6 split); read it before running this
phase.

## Phase 4 — Size the dispatch (solo-first, feature path)

**The owed upstream-doc ladder** — the record's Size/materiality signals also fix which upstream
doc types it owes beyond the ticket itself (ratified #655 decision 2; canon owned by
`docs:doc-writing-rules`' Owed chain, full chain in `references/spec-lock-gate.md`). Phase 3.6,
just before this phase, already gated a missing/unlocked citation against it.

The record's Size class picks the machinery — the seats' own materiality floors, applied from the
caller's side:

- **small** — the host builds it inline, or one sealed fork/agent when isolation or tooling
  demands it (an agent only for tool restriction, parallelism, or multi-skill preload; a fork for
  everything else — harness's fork-vs-agent gate, inline where harness is absent) — **but only
  when the host is a TOP-LEVEL session**; a host that is itself already a nested dispatch takes
  the inline branch unconditionally, per the no-nested-wait rule above. No planner, coordinator,
  or team. A small build that semantically edits a prompt-carrying artifact (a
  SKILL.md body, an agent definition, a hook prompt) still gets a fresh-context checker pass
  before the loop closes — lint and gates prove mechanics, not semantics (2026-08-11 estate
  audit: every unaudited semantic edit carried a real gap); pure code/config under the repo's own
  test gates needs no checker seat. **Dispatch that checker UNNAMED and synchronous — a named
  dispatch strands the report** (a fix fork's own checker dispatched `chk667` stranded its
  verdict at the root session, 2026-08-18 — the gh#154/#157 class, re-proven), per harness's
  `agent-writing-rules` never-name rule (cited, not restated) — the same discipline the skill's
  own no-nested-wait preamble above already names.
- **big** — the delivery seats, each already floored: `planner` authors what the change earns
  (the record's Links may already carry the docs — don't re-author), `builder` implements to the
  approved LLD, `code-checker` grades the slice before merge. The coordinator seat only when the
  chain genuinely spans ≥2 seats across contexts. A `/build-feature`-initiated call makes
  host→fork→coordinator→seats — a third level past `fleet-rules`' default depth ≤2, named
  deliberately: the fork isolates the CALLER's session, the coordinator isolates the multi-seat
  chain — two different things, not one dispatch nested for no reason. Same shape on a
  `build-leader` dispatch, with the agent context taking the fork's place.

## Phase 5 — Dispatch under contract: the four lifecycle stages

Every build dispatch — feature or task alike — owns its full execution lifecycle end to end, not
merely the code change (#183: a dispatch that stops at "code written" leaves the caller to
discover and repair branch/worktree residue by hand):

1. **Isolated execution by default, or the explicit host-checkout skip (#204)** — Phase 3's
   claim-then-isolate (or claim-then-skip), already done before this phase starts.
2. **Branch + commits pushed — held, then a plan-approval accept opens the PR** (ADR-0002's
   PR-open contract, now gated per ADR-0023 decision (c) — `lld-0022-fleet-native-write-gate.md`).
   Commit meaningfully as work lands and push the claimed branch; the pushed-but-not-yet-open
   state is stage 2a's own HOLD point, immediately below — a draft PR already counts as PR-open
   here (ADR-0023's own "visible/mergeable outside" test).

   **2a. Plan-approval write-gate (ADR-0023 (c)) — hold, then accept, then PR-open.** Unconditional
   on every dispatch, never gated by ADR-0012's grant (2b composes on top, never bypasses).
   **Accepting seat:** the marshal (`fleet-rules` §7 — never the live human by default, never the
   dispatching seat itself) releases the hold via an **accept marker**: a durable comment naming
   the pushed branch's HEAD SHA. **No live marshal → FAIL-CLOSED** — report `write-gate-blocked`
   (Failure branches), branch stays pushed for a later run to resume. Full mechanics, SHA-staleness
   rule, dry-run traces: `references/plan-approval-write-gate.md`, `references/
   write-gate-dry-run.md` (F6 split) — read before this stage's first live firing.

   **Immediately before opening the PR** (once 2a's accept marker has landed), run
   Phase 3's version-collision re-checks — both of them: re-run `version_claim_check.py` (the
   CLAIM race) AND fetch + re-read every touched plugin's version off `origin/main` and bump from
   THAT value (the VALUE race, #445) — see Phase 3 for why one check doesn't catch the other.
   Open exactly one PR against `main` carrying `Closes #<id>` (every id this
   dispatch closes, on a folded campaign), a plain what/why, the gate output for every touched
   plugin, an integration-notes line naming any known overlap with other open PRs (adopt
   another PR's field wording where one owns it, never mint a competing definition), a
   **rejected-alternatives line** naming what was deliberately NOT done and why (docs
   doc-writing-rules' TICKET contract, `## Rejected alternatives`; same enforcement tier as the
   Findings write-back below — a bare "nothing rejected" is a valid entry when the path was
   uncontested, an absent line at PR-open is not), and **the accept marker's own comment URL**
   (the PR body cites what authorized its own opening). **The moment the accept-triggered PR
   opens (git-native only), remove the `in-flight` claim label** — same removal point as before
   this stage existed (#192/#199), just gated by one more precondition now (`lld-0022` Resolution
   4). Claim comment and assignee stay untouched — display change only, not a release.
   **Gate-run time budget — the local aggregate run ONCE, never ground, under a bounded wrapper
   (~900s default, overridable).** Full mechanics, the exhaustion/partially-run handling, and the
   incidents this closes: `references/gate-run-time-budget.md` (F6 split).
   **2b. Quick-build auto-merge — only on an explicit grant and an all-green predicate (ADR-0012),
   composing ON TOP of stage 2a's write-gate, never bypassing it** (strict one-way ordering: 2a's
   accept → PR-open → this stage's eight-conjunct evaluation). Read the sealed dispatch prompt for
   the literal line `auto-merge: authorized`. **Absent → this stage does not exist**: skip it
   silently, go to stage 3 as written — never infer the grant from "unattended", a `size:small`
   label, or tone. Present → evaluate all eight conjuncts (QB0 grant · QB1 `size:small` · QB2 one
   plugin · QB3 one substantive file · QB4 no contract change, an allow-list · QB5 critic green ·
   QB6 gate green twice · QB7 no overlapping open PR), then, if all green, the merge sequence
   (bounded CI-watch + check-runs API verify → squash-merge → re-query MERGED → `campaign_close.py`
   → dated Findings write-back). Any conjunct failing/indeterminate → NOT eligible, name it in the
   handoff, continue to stage 3 unchanged. Full mechanics — every conjunct's exact test, the grant
   non-inheritance/injection-immunity rules, and the five-step merge sequence — live in
   `references/quick-build-auto-merge-predicate.md` (F6 split); read before this stage's first
   live firing.
3. **Verified-clean retirement before the seat retires** — never assumed. State three axes: the
   worktree's git status (clean, or N/A when Phase 3 took the host-checkout skip), the local
   feature branch (pushed and named — this seat never merges its own PR, per ADR-0002's
   human-gated merge, **except under stage 2b's ADR-0012 quick-build predicate, when the sealed
   dispatch carried the explicit grant and all eight conjuncts came back green**; on that branch
   the axis reads "auto-merged at `<SHA>`, remote branch verified deleted (campaign_close)"), and
   the host checkout (untouched when isolated; "built directly in host checkout, skip
   preconditions met" when the #204 skip ran instead) — never silently omitted.
4. **A typed retirement handoff proving each step**: the PR URL, **the accept marker's own comment
   URL (stage 2a)**, the Findings write-back's own comment URL on the resolved backend (below),
   and one explicit environment-clean line naming
   stage 3's three axes by result — never a silent "done". When stage 2b FIRED, three more fields
   ride along: `merge-sha: <sha>` · `campaign-close: <its summary line>` · `qb-snapshot: <the
   eight conjunct results>`. When stage 2b evaluated and MISSED, the handoff names the failed
   conjunct and states the fallback plainly — PR opened, awaiting a human merge, today's behavior
   unchanged. When no grant was present, the handoff says nothing about auto-merge at all. When
   stage 2a never released (`write-gate-blocked`), no PR/accept-marker URL exists — name the
   blocker instead (Failure branches). `build-leader`'s own return contract carries these lines
   verbatim to whatever dispatched it.

Every dispatch is also sealed under the write-back contract already in force: the ticket path +
enumerated inputs + budget + the typed return + stage 2a's **accept-marker requirement
(ADR-0023 (c))** + stage 2's own `--remove-label in-flight` call,
its **`version_claim_check.py` re-run (the CLAIM race)**, and its **origin/main version
re-read-and-rebump (the VALUE race)** at
the moment the PR opens (all four named explicitly on a task or big-feature dispatch, since the dispatched
agent/seat opening the PR never loaded this file), and a **mandatory dated `## Findings`
write-back at each significant result** (slice built, gate green, PR opened), not only at the
end, so an interrupted build still left evidence — the entry that closes the ticket
(`doing`→`done`/`wontfix`) additionally states the **rejected alternatives**: what was deliberately
NOT done and why, same tier as the rest of this contract, mirroring the PR-body line above onto
the record itself. The write-back verb follows the resolved
backend: git-native — the issue number, `gh issue comment`; file backend — the TICKET file's
path, editing its `## Findings` section; an external adapter — its `update` operation. Run under
`/goal` with a try-cap (5, per loop-rules's feature-ticket recipe — the feature path only; task's
single sealed dispatch carries no try-cap wrapper): named stopping predicate, capped tries,
escalate on the same failure twice.

**Optional review-path line for a dispatched critic.** The sealed prompt handed to any
fresh-context checker this dispatch spawns (Phase 4's small-build checker, Phase 5 stage 2b's QB5
critic) may carry one optional line — `review path: start at X, then Y` — naming a reading order
when the change has a non-obvious one (a schema before its consumers, a contract before its
implementation); omit it when the diff has one natural entry point. Same optional field,
`write-handoff`'s own contract (harness) — named here so the critic dispatch, not just the
handback, can carry it.

## Phase 6 — Close the loop

Read the ticket back (git-native: `gh issue view --comments`; file backend: re-read the file; an
adapter: its `read` operation). Findings gained entries and the work shipped → advance status
(`open`→`doing`→`done`; git-native `done` closes the issue, `wontfix` closes with the label and a
reason comment — matching `file-bug`'s own Phase 6 verbs) and report path + status + what shipped,
plus Phase 5's environment-clean line — stated, never inferred from silence. **When stage 2b
merged the PR, `Closes #<id>` already closed the record**: the read-back CONFIRMS that closure
rather than performing it — a closed issue here is the expected end state, not Phase 1's
stop-and-report condition (which reads state at INTAKE, before any work) — and stage 2b's QB
snapshot is the shipped-work evidence. An agent that
returned without its Findings entry → one re-dispatch with the contract quoted, then record the
loss with a dated entry and say so plainly; a fork no longer addressable skips straight to
recording — it cannot be re-dispatched into. Either way, recording the loss is a terminal outcome
with nothing left to come back and open a PR, so it releases the claim right there — the
Release-on-abandonment bullet's full release (Phase 3: `--remove-assignee @me --remove-label
in-flight`, PLUS the release comment naming why — never just the flags with no comment, since the
comment stays the durable record even when the label is what a human notices first). A
conversational summary never substitutes for the entry the record was owed.

## Failure branches

- Claim lost the race in Phase 3 (an earlier-timestamped competing claim on re-read) → report as
  a named blocker and stop; never overwrite the winning claim, never guess which run owns the
  ticket. `in-flight` is only ever applied AFTER the race check confirms a win, so a losing claim
  never had one to remove.
- Ambiguous match in Phase 1 (two plausible records) → only `/bind-build`'s own standing seat runs
  this procedure in the live host session itself (the "No nested wait" section's not-nested case
  above, no `Agent`-tool
  hop and no fork) — there, and only there, ask which via `AskUserQuestion`, one question, then
  proceed. Every other caller has no question channel to reach: a `/build-feature`-initiated call
  runs this procedure INSIDE that command's own `context: fork` (`build-feature/SKILL.md`'s
  frontmatter), and a `context: fork` background dispatch has no `AskUserQuestion` channel at all —
  measured 2026-08-17 (gh#541): the tool is unreachable from inside one, confirmed two ways (two
  independent thin captures minted clarify-less, and a background dispatch that could not even
  discover the tool). The 2026-08-09 claim this line used to carry — "forking relieves the
  caller's session, it does not remove the person, and `AskUserQuestion` still reaches them
  directly" — is that falsified assumption; don't restate it. `build-leader` (`Agent`-tool
  dispatch, same no-channel finding) and `mobilize-chores` (the batch confirm already spent the
  user's one gate for this run) have no live question channel either. **No live question channel**
  (`/build-feature`'s fork, `build-leader`, `mobilize-chores`) → capture-with-gaps: report the
  ambiguity as a named blocker naming both candidate ids, plus the resume path — re-invoke this
  procedure with the explicit ticket id once a person picks one (Phase 1's ticket-id branch takes
  precedence over the sweep, so a resolved id skips the ambiguity entirely) — same discipline as
  this plugin's other unattended failure branches (`close-session`, `mobilize-chores`); never guess
  which record was meant.
- A raw (recordless) seed that is bug-shaped → `file-bug` (docs) owns it from intake, not a build;
  the Phase 2 bug branch covers a ticket that already exists. This dispatch never invokes
  `file-bug` directly for a recordless seed (Phase 1's nested-intake hand-off does, ahead of any
  kind branch) — no isolate call owed here on top of it.
- A task's clarify round exhausts without a clear brief → SKIPPED with the named gap (Phase 2); a
  skipped task is a reported outcome, not a failure.
- Build blocked mid-flight by a discovered design fork → escalate to the record (a dated Findings
  entry naming the fork) and, for big work, back to planner — never silently edit the contract.
- Gates fail at the wave boundary → the failure routes to the seat that caused it; the ticket
  stays `doing` with the failure recorded.
- Stage 2b's predicate misses, or its merge sequence fails part-way (`auto-merge-denied` on a
  blocked `gh pr merge`, `auto-merge-unverified` on a merge whose SHA never confirmed) → **not a
  build failure**: the PR is open and linked, which is this dispatch's ordinary successful end
  state. Name the failed conjunct or the blocker in the handoff, leave the PR for a human, keep
  the claim as-is, and never retry the sequence or widen the predicate to get past it.
- Phase 3.5 finds a falsified premise → `stale-premise` is a reported outcome, not a failure: claim released, evidence on the record, ticket left open for re-triage.
- Phase 3.6 fires → a named blocker, never a build: claim released, worktree torn down (or N/A
  under the #204 skip), evidence named on the record exactly like any other blocker — never a
  new outcome type, never silently patched by authoring the missing doc inline.
- Phase 5 stage 2a's write-gate holds with no live marshal (ADR-0023 (c)) → `write-gate-blocked`
  is a reported outcome, not a failure: pushed branch stays as-is, Phase 3 claim stays held (an
  ordinary in-progress wait), report names the missing accepting seat + branch/SHA awaiting
  acceptance; a later run resumes from the pushed branch rather than restarting. Never auto-accept
  or infer acceptance from silence — `references/plan-approval-write-gate.md`.

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker/skip/stale-premise/`write-gate-blocked` report), status reflects reality, a PR this dispatch opened carries an explicit
environment-clean line proving worktree/branch/host-checkout state (or the #204 skip-branch's own
one-line statement), an abandoned claim was released rather than left standing, and no build
effort was spent before the record existed — or the bug branch isolated first and then handed
over with the redirect marker and the read-back snapshot (state/Findings as of hand-off) relayed;
the fork's own outcome is never something this seat waits on.
