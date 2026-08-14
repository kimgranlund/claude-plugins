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

The procedure behind `/build-feature`, the `build-lead` agent, and `/lead-build`'s standing seat
— one engine, three entries. `/build-feature` is `disable-model-invocation: true` (command-only,
unreachable via the Skill tool or agent preload — issue #134/#135's shared defect class), so this
skill carries the actual procedure and both callers invoke it rather than duplicating it.
Generalized from `dispatch-feature` per ADR-0010: one confirmed ticket of ANY kind — feature,
task, or bug — the kind branch below picks the path. Carries no `context: fork` of its own (no
double hop from `/build-feature`, no third hop from `build-lead` — rationale in `/build-feature`'s
body). Seed: $ARGUMENTS.

## Phase 1 — Find or make the record

- `$ARGUMENTS` resolves to a ticket id (`TKT-####`, a bare issue number on the git-native backend,
  or an adapter-native id) → that's the record. Branch on STATE first: `done`/`wontfix`/closed →
  report and stop (reopening is the user's call); otherwise read kind/Size/Scope/Links and
  continue to Phase 2.
- Otherwise sweep the three surfaces `/file-feature`'s dedup names (records, codebase, existing
  docs/corpora): a queued match → build from it; a match that already shipped → report where it
  lives and stop.
- **No match → run the full `/file-feature` intake first** (docs, where installed — opt-in index
  offer rides along; apply its phases inline otherwise: extract → dedup → size/shape → lint-clean
  `kind: feature` ticket, no index offer without docs' template), via the Skill tool, seed prefixed
  `[nested-intake]` — file-feature's own Phase 6 gates its index-bootstrap offer off this marker
  (a nested intake already owes this skill's own ambiguity question plus file-feature's own round;
  a third `AskUserQuestion` in one background run is one too many). A raw seed reaching this skill
  is feature-shaped by its callers' own contracts; the intake's classification still redirects a
  disguised bug or chore. The record exists before any build effort is spent — ticket-first is the
  entire loss-window fix, and it does not move.

A record whose Shape is knowledge (routed to reference/corpus work at intake) is not built here —
report that routing and stop; docs' seats own it.

## Phase 2 — Branch by kind

- **`kind: bug`** → this is `file-bug`'s work; isolate BEFORE handing off (Phase 3's isolate
  bullet runs now — no claim, `file-bug` owns its own record lifecycle), then invoke `file-bug`
  via the Skill tool with the ticket id, seed prefixed `[redirected-from:dispatch-ticket]`
  (file-bug's marker protocol — the round budget was already spent here, and its forked run has
  no other way to know). Safe: a `context: fork` skill invoked inside a worktree-isolated context
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
  ambiguous-match test; `build-lead` has no one to ask — an already-clear ticket needs zero
  rounds). Still not concretely actionable → report SKIPPED with the named gap, never dispatch on
  an unclear brief — no claim taken, since no build effort was ever starting. Otherwise run Phase
  3 (claim, then isolate) first, then dispatch via the `Agent` tool — `subagent_type:
  general-purpose` by default (`team-or-solo-rules`' solo-first/null-unit reasoning: a generic
  task needs no tool restriction, parallelism, or multi-skill preload); a named agent only when
  the clarified brief genuinely needs one of those three. The dispatch prompt is sealed per Phase
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
  comment` naming the claimant (`build-lead`/`dispatch-ticket`), a UTC timestamp, and the branch
  name; file backend — the record's `claimed-by`/`claimed-at` pair; an adapter — its own
  realization. **Re-read the record** (Phase 6's `read` verb) before proceeding: an
  earlier-timestamped competing claim means this caller lost the race (ADR-0005 tie-break: lower
  identity string wins on an exact tie) — abandon immediately, no worktree created, no release
  needed (this claim never landed), report the loss as a named blocker rather than guessing which
  claim is real.
- **Once the claim wins, make it LIST-VISIBLE too (#199)** — the claim comment is durable but
  invisible in the LIST view (Kim: "I cannot tell that Issues are claimed"). Git-native only: `gh
  issue edit --add-label in-flight`. `in-flight` shares hex `FBCA04` with `doing` by coincidence,
  not relation — a shared color is never evidence two labels mean the same; a repo without
  `in-flight` creates it with that name and a distinct hex. Additive to the assignee+comment claim
  (assignee stays required per ADR-0005) — the label only supplies list-visibility.
  **`in-flight` is the ONE canonical claim label — never mint a synonym.** `doing` is a DIFFERENT,
  load-bearing label — the `open`→`doing`→`done` status verb, unrelated to claiming; #192 shows
  the confusion: `doing` applied alongside `in-flight` mid-claim looked like a duplicate but
  wasn't. The two coexist ("is this claimed" vs. "what lifecycle stage") — `doing` is never
  deleted or reused as a claim signal.
  **Label = display, comment = record.** `in-flight` is hand-editable and never the correctness
  gate alone: `mobilize-chores` step 2 may read it as a cheap pre-filter, but the claim comment —
  plus, once a PR exists, that step's own GraphQL PR-linkage check — stays authoritative.
  **Removed on every terminal outcome:** Phase 5 stage 2 removes it the moment a PR opens (the
  open PR becomes the visible signal instead — named explicitly in a task/big-feature dispatch's
  sealed prompt, since the seat opening the PR never loaded this file); the Release-on-abandonment
  bullet removes it on a mid-flight abandon and on Phase 6's recorded-loss ending (as dead as an
  abandonment). A task SKIPPED in Phase 2 never reaches this bullet, so owes no removal. A
  coordinator running a serial chain (`mobilize-chores`) may also carry the pre-existing `queued`
  label (`C5DEF5`) for chain position ahead of its own claim — nothing here touches its lifecycle.
- **Isolate second — now CONDITIONAL, not unconditional (#204).** Decide the branch name FIRST:
  the claim bullet's decided name (feature/task), or a lightweight `bug/<id>` (bug hand-off, no
  claim ran). **Skip isolation only when ALL FOUR hold** — sized `small`; no concurrent mutating
  dispatch exists (checked: no other live entry under `.claude/worktrees/` for this repo right
  now); the host checkout is clean on `main` with nothing in flight (checked: `git status`); no
  isolation-forcing reason applies (a nested dispatch always forces it — #207: the child gets its
  own worktree, or an explicit host-checkout authorization the parent names as its own line in
  Phase 5's sealed dispatch prompt, never an inherited skip). All four hold → build directly in the
  claim/write-back contract stays mandatory regardless. Never a silent revert to pre-#183
  behavior: the skip is its own named branch, and Phase 5 stage 3's environment-clean line states
  which branch was taken.
  **Otherwise, isolate** — check reuse first, keyed on IDENTITY never path shape, both conjuncts
  required or create: (1) cwd is a linked worktree, not the primary checkout (a decided-name match
  IN the primary checkout never licenses reuse — the #180/#182 residue below is exactly a stale
  branch left checked out there); AND (2) that worktree's checked-out branch matches the decided
  name (a resumed `build-lead`/`lead-build` re-entering its own isolation — the name embeds the
  ticket id, so a match is identity, not shape). "cwd sits under `.claude/worktrees/`" alone
  satisfies NEITHER conjunct (#191: a caller's own long-lived worktree for an unrelated purpose,
  e.g. `mobilize-chores`'s, matches that shape too — reusing it on shape alone checks the wrong
  ticket's branch out on top of the caller's tree). Either conjunct fails → create (`git worktree
  add`, off a clean `main` HEAD) and run every remaining step inside it. This isolate-when-used
  rule is what the #180/PR #182 defect fixed (2026-08-12: that build ran in the HOST checkout with
  no worktree and left its branch checked out; the coordinator repaired it by hand) — never build
  in the shared host checkout outside the four-precondition skip above, and never reuse an
  unrelated worktree standing in for one, however deeply nested (#191).
- **Release on abandonment — post-claim exits only.** Only a failure AFTER the claim landed has
  anything to release: a discovered design fork routed back to planner, an unresolved gate
  failure (both mid-flight, Failure branches below), or Phase 6's recorded-loss ending (a
  dispatched agent returned with no Findings, the re-dispatch also came back empty — nothing is
  ever coming back to open a PR, as dead as a mid-flight abandonment). Each releases the claim
  before returning: git-native — `gh issue edit --remove-assignee @me --remove-label in-flight`
  plus a `gh issue comment` naming the release and why; file backend — clear
  `claimed-by`/`claimed-at`; an adapter — its own realization. **The label release is not
  optional** — a dead dispatch never leaves a stale `in-flight` label behind (#199 extends #184's
  release discipline to the label; left standing, it reads as still-claimed to a human scanning
  the list and to `mobilize-chores` step 2's pre-filter). A **pre-claim** exit has nothing to
  release, since Phase 3 never ran: a task SKIPPED in Phase 2 and an ambiguous-match blocker in
  Phase 1 both end before this phase starts. A **lost claim race** also has nothing to release.
  Post-claim release keeps a mid-flight abandonment from permanently blocking the ticket for the
  next sweep — `mobilize-chores` step 2 excludes on an active claim the same way it excludes an
  open in-flight PR.
- **Tear down a no-longer-needed scratch branch/worktree — verified, never raw.** Two cases reach
  this: the abandonment bullet above (claim already released), and Phase 2's bug hand-off, only
  once the post-hand-off read-back (Phase 6's verbs) shows a terminal state (issue closed, or a
  `file-bug` Findings entry marking its own run done) with nothing landed on the branch. Short of
  that, the worktree stays standing, reported as residue — never torn down while `file-bug`'s own
  fork may still be live inside it. Never retire with a raw `git branch -D` plus worktree removal
  — that force-deletes work on this seat's own say-so alone. Feature-detect the host repo's own
  gated reap script (reference shape: gen-ui-kit's `scripts/ops/reap-branches.mjs
  --verify-branch <name>` — a differently-located script counts only if the host repo's own docs
  declare the same 0/1/2 contract) and gate the delete on its exit code alone. Order: `git
  worktree remove` first (refuses on a dirty tree, so nothing is lost on a wrong call), THEN
  `--verify-branch`, THEN — only on exit 0 (a merge-base ancestor of `origin/main`, or an
  exactly-matching MERGED PR) — `git branch -d` (never `-D`, even after a verified 0). Exit 1
  (KEPT/PROPOSED), or either verb refusing outright, → leave standing and report why, never
  force. Exit 2 is a usage error, not a verdict — report it. No such script → fall back to an
  unverified `git worktree remove` then `git branch -d`, never silently — name what went
  unverified.

## Phase 4 — Size the dispatch (solo-first, feature path)

The record's Size class picks the machinery — the seats' own materiality floors, applied from the
caller's side:

- **small** — the host builds it inline, or one sealed fork/agent when isolation or tooling
  demands it (an agent only for tool restriction, parallelism, or multi-skill preload; a fork for
  everything else — harness's fork-vs-agent gate, inline where harness is absent). No planner,
  coordinator, or team. A small build that semantically edits a prompt-carrying artifact (a
  SKILL.md body, an agent definition, a hook prompt) still gets a fresh-context checker pass
  before the loop closes — lint and gates prove mechanics, not semantics (2026-08-11 estate
  audit: every unaudited semantic edit carried a real gap); pure code/config under the repo's own
  test gates needs no checker seat.
- **big** — the delivery seats, each already floored: `planner` authors what the change earns
  (the record's Links may already carry the docs — don't re-author), `builder` implements to the
  approved LLD, `code-checker` grades the slice before merge. The coordinator seat only when the
  chain genuinely spans ≥2 seats across contexts. A `/build-feature`-initiated call makes
  host→fork→coordinator→seats — a third level past `team-or-solo-rules`' default depth ≤2, named
  deliberately: the fork isolates the CALLER's session, the coordinator isolates the multi-seat
  chain — two different things, not one dispatch nested for no reason. Same shape on a
  `build-lead` dispatch, with the agent context taking the fork's place.

## Phase 5 — Dispatch under contract: the four lifecycle stages

Every build dispatch — feature or task alike — owns its full execution lifecycle end to end, not
merely the code change (#183: a dispatch that stops at "code written" leaves the caller to
discover and repair branch/worktree residue by hand):

1. **Isolated execution by default, or the explicit host-checkout skip (#204)** — Phase 3's
   claim-then-isolate (or claim-then-skip), already done before this phase starts.
2. **Branch + commits + PR opened**, per ADR-0002. Commit meaningfully as work lands, push the
   claimed branch, and open exactly one PR against `main` carrying `Closes #<id>` (every id this
   dispatch closes, on a folded campaign), a plain what/why, the gate output for every touched
   plugin, and an integration-notes line naming any known overlap with other open PRs (adopt
   another PR's field wording where one owns it, never mint a competing definition). **The moment
   the PR opens (git-native only), remove the `in-flight` claim label** — the open PR is now the
   visible in-progress signal (#192: its PR once merged and closed the issue with `in-flight`
   still on it, before this step existed — the stale-display defect #199 closes). Claim comment and
   assignee stay untouched — display change only, not a release.
   **2b. Quick-build auto-merge — only on an explicit grant and an all-green predicate (ADR-0012).**
   Read the sealed dispatch prompt for the literal line `auto-merge: authorized`. **Absent → this
   stage does not exist**: skip it silently, change nothing, go to stage 3 as written. Never infer
   the grant from "unattended", from a `size:small` label, or from a coordinator's tone — the
   coordinator sets that field deliberately or it is not set (same doctrine as `mobilize-chores`'
   own `auto` token). Present → evaluate all eight conjuncts, every one a command with an exit
   code, none a judgment call:
   - **QB0 grant** — the literal line, above.
   - **QB1 `size:small`** — `gh issue view <id> --json labels` carries it (file backend: the Size
     field reads `small`). Phase 4's existing materiality floor, reused; no new size taxonomy.
   - **QB2 one plugin** — every path in `git diff --name-only origin/main...HEAD` sits under ONE
     top-level plugin directory. A repo-root path, anything under `.claude/docs/` or `.github/`,
     or a second plugin → out.
   - **QB3 one substantive file** — with R = {`<plugin>/.claude-plugin/plugin.json`,
     `<plugin>/README.md`} (the mandatory version-bump + ledger ride-alongs), `changed \ R` has
     exactly ONE member. Diff-check the ride-alongs too: the `plugin.json` diff's changed lines
     all match `"version"`, and **every changed hunk in `README.md` starts at or below the
     version-ledger heading** (`git diff -U0 … -- <plugin>/README.md`, hunk start line vs. that
     heading's line number). A hunk above it, or no ledger heading found, is indeterminate → out.
   - **QB4 no contract change — an ALLOW-list, fail-closed BY CONSTRUCTION.** The substantive file
     must MATCH one of exactly three classes: (a) `<plugin>/skills/*/SKILL.md` with no changed hunk
     inside the frontmatter block (first line through the closing `---`) — a body-only edit;
     (b) `<plugin>/skills/*/references/*.md`; (c) `<plugin>/scripts/*.{py,mjs,js}`, implementation
     and/or its `selftest`. **Anything that does not match is ineligible because it is unlisted** —
     never because a list of forbidden things happens to name it. Orienting examples only, never
     the rule: `hooks/` (ANY file in it, not just `hooks.json`), `commands/*.md`, `agents/*.md`,
     any `evals.json`, anything under `.claude-plugin/`, any `CLAUDE.md`, anything under
     `.claude/docs/`, and any file carrying a frontmatter block outside class (a). An artifact kind
     invented tomorrow is ineligible the day it appears, with no edit here.
   - **QB5 critic green** — a fresh-context checker ran on THIS change inside THIS dispatch and
     returned zero blocker/major findings. Deliberately stricter than the baseline semantic-edit
     invariant (pure code normally rides its own test gates): auto-merge always pays for a critic.
     No recorded verdict → out; a remembered one is not a recorded one.
   - **QB6 gate green twice** — `release_gate.py <plugin>` exit 0 locally, AND CI green on the PR
     per the bounded watch below. Local green alone never suffices; CI is ADR-0002's own layer.
   - **QB7 no overlapping open PR** — no other OPEN PR touches the same plugin (`gh pr list
     --state open --json number,files`). Overlap → a human merges.

   **Any conjunct that fails, errors, times out, or is indeterminate → NOT eligible.** Name the
   failed conjunct in the stage-4 handoff and continue to stage 3 exactly as today — PR open,
   human merges, nothing else different. Never re-run a conjunct to chase a pass. All eight green
   → run the merge sequence, one attempt each, in order: (1) a BOUNDED `gh pr checks <pr> --watch
   --fail-fast` — the ceiling is a real wrapper with a real exit code, not a promise to watch the
   clock, and the wrapper is **feature-detected, never assumed**: `timeout 900 …` where GNU
   coreutils `timeout` is on PATH (`gtimeout 900 …` on a Homebrew macOS box), otherwise the
   portable `perl -e 'alarm 900; exec @ARGV' gh pr checks <pr> --watch --fail-fast`. Stock macOS
   carries NEITHER `timeout` nor `gtimeout` (measured 2026-08-14) — assuming the GNU spelling
   would make this whole path silently inert. **Exit 0 is the only pass**; every other exit is
   ineligible with no interpretation — 124 (GNU expiry), 142 (SIGALRM expiry), 127 (no wrapper
   found, so the bound could not be ENFORCED — never run an unbounded watch in its place), or any
   failing check. A timeout is NEVER read as an implicit pass; (2) `gh pr merge <pr> --squash`;
   (3) verify by
   re-query, never by trusting the merge command's own print — `gh pr view <pr> --json
   state,mergeCommit` must show `MERGED` and a non-empty SHA; (4) `python3
   harness/scripts/campaign_close.py <pr> --repo <owner/repo> --gate <plugin-root>`; (5) a dated
   Findings write-back carrying the full QB0–QB7 snapshot (each conjunct's OBSERVED value — the
   substantive file's path, the critic's verdict quoted, both gate results), the merge SHA, and
   `campaign_close`'s summary line. A denial at step 2 (the unattended permission classifier still
   blocks `gh pr merge` until Kim arms a scoped allow-rule) or any later failure → the named
   blocker `auto-merge-denied` or `auto-merge-unverified` in the handoff, PR left standing for a
   human, claim NOT re-released (an open linked PR is today's normal end state). Never force,
   never retry past the first denial.
3. **Verified-clean retirement before the seat retires** — never assumed. State three axes: the
   worktree's git status (clean, or N/A when Phase 3 took the host-checkout skip), the local
   feature branch (pushed and named — this seat never merges its own PR, per ADR-0002's
   human-gated merge, **except under stage 2b's ADR-0012 quick-build predicate, when the sealed
   dispatch carried the explicit grant and all eight conjuncts came back green**; on that branch
   the axis reads "auto-merged at `<SHA>`, remote branch verified deleted (campaign_close)"), and
   the host checkout (untouched when isolated; "built directly in host checkout, skip
   preconditions met" when the #204 skip ran instead) — never silently omitted.
4. **A typed retirement handoff proving each step**: the PR URL, the Findings write-back's own
   comment URL on the resolved backend (below), and one explicit environment-clean line naming
   stage 3's three axes by result — never a silent "done". When stage 2b FIRED, three more fields
   ride along: `merge-sha: <sha>` · `campaign-close: <its summary line>` · `qb-snapshot: <the
   eight conjunct results>`. When stage 2b evaluated and MISSED, the handoff names the failed
   conjunct and states the fallback plainly — PR opened, awaiting a human merge, today's behavior
   unchanged. When no grant was present, the handoff says nothing about auto-merge at all.
   `build-lead`'s own return contract (`agents/build-lead.md`) carries these lines through
   verbatim to whatever dispatched it.

Every dispatch is also sealed under the write-back contract already in force: the ticket path +
enumerated inputs + budget + the typed return + stage 2's own `--remove-label in-flight` call at
the moment the PR opens (named explicitly on a task or big-feature dispatch, since the dispatched
agent/seat opening the PR never loaded this file), and a **mandatory dated `## Findings`
write-back at each significant result** (slice built, gate green, PR opened), not only at the
end, so an interrupted build still left evidence. The write-back verb follows the resolved
backend: git-native — the issue number, `gh issue comment`; file backend — the TICKET file's
path, editing its `## Findings` section; an external adapter — its `update` operation. Run under
`/goal` with a try-cap (5, per loop-rules's feature-ticket recipe — the feature path only; task's
single sealed dispatch carries no try-cap wrapper): named stopping predicate, capped tries,
escalate on the same failure twice.

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
- Ambiguous match in Phase 1 (two plausible records) → **with an interactive user present**, ask
  which, one question, then proceed. A `/build-feature`-initiated call counts as having one even
  inside that command's fork — forking relieves the caller's session, it does not remove the
  person, and `AskUserQuestion` still reaches them directly. **No interactive user** (e.g. via
  `build-lead`, from `mobilize-chores`) → report the ambiguity as a named blocker instead — the
  batch confirm already spent the user's one gate for this run, so a mid-dispatch question has
  nowhere sanctioned to land (same discipline as this plugin's other unattended failure branches:
  `close-session`, `mobilize-chores`); never guess which record was meant.
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

Done when the record's `## Findings` carries dated evidence of the shipped work (or the recorded
blocker/skip), status reflects reality, a PR this dispatch opened carries an explicit
environment-clean line proving worktree/branch/host-checkout state (or the #204 skip-branch's own
one-line statement), an abandoned claim was released rather than left standing, and no build
effort was spent before the record existed — or the bug branch isolated first and then handed
over with the redirect marker and the read-back snapshot (state/Findings as of hand-off) relayed;
the fork's own outcome is never something this seat waits on.
