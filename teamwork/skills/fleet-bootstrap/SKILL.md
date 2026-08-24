---
name: fleet-bootstrap
description: >-
  Full one-terminal fleet cold-start (#410 addendum 3, level 2 — composes team-scaffolding + the
  roster): adopts the orchestrator seat, dispatches the product seat to draft the intent layer,
  then HARD-GATES on human ratification of that draft (AskUserQuestion where reachable; no live
  user stops and names the pending gate). Seeds or updates the fleet manifest (roster, tier
  deviations with dated justification, manned-vs-background, live seat state). Run
  /fleet-bootstrap [spawn-list], a comma-separated subset of reviewer,planner (default empty —
  those two are manually operated per #410 addendum 3), always confirmed via one AskUserQuestion
  before spawning — the argument only pre-selects, it never skips that confirm. NOT a single seat's own bootstrap
  (team-scaffolding — reproduced inline here for the orchestrator seat, called directly for
  reviewer/planner spawns; alone correct for a human joining one seat by hand); NOT for redoing the
  gate after ratification (fires once per cold start).
disable-model-invocation: true
user-invocable: true
argument-hint: "[spawn-list - comma-separated subset of reviewer,planner; default empty]"
---

# fleet-bootstrap — one terminal, cold-start the whole fleet

The standing fleet is four seats (`{scope}-marshal` / `{scope}-reviewer` / `{scope}-planner` /
`{scope}-product`), each already reachable one at a time via `/team-scaffolding <role>` (level 1).
This command is level 2: a single terminal drives the whole cold start — adopt orchestrator,
stand up the product seat, gate on human ratification of the intent layer that seat produces, then
spawn whichever remaining seats the human wants running in the background. `$ARGUMENTS`: an
optional comma-separated spawn-list, default empty (see Phase 4).

## Phase 0 — Seed or read the fleet manifest

**Resolve the fleet SCOPE ROOT, symmetric with `fleet-connect` step 1's own rule
(`references/fleet-manifest-schema.md`'s "Location and resolution" section, canonical there,
never re-derived here — #911, supersedes the #906/#909 nearest-`fleet.json` ladder).** Walk from
the current working directory upward looking for the nearest ancestor directory that contains a
`.claude` directory AT ALL — not the nearest one that happens to already hold a `fleet.json`.
That directory is the scope root; the target path is always `<scope root>/.claude/ops/fleet.json`.
An ancestor's `fleet.json` sitting ABOVE the resolved scope root is out of scope for this run —
never consulted, never written, whatever it contains; a nested app with its own `.claude/`
directory always gets its own fleet, even when an ancestor repo-root `fleet.json` already exists.
**`fleet.json` present under the resolved scope root** → that path is THE `fleet.json` for the
rest of this run — every subsequent Phase's read or write targets this same resolved path, never
a bare `.claude/ops/fleet.json` re-derived from cwd or the repo root. Read it now as the record of
who has already joined and at what tier/mode, do not overwrite existing `live_state` entries,
only append.
**Absent under the resolved scope root, but `<scope root>/.claude/ops/fleet-scope.json` present**
(#915's opt-in scope-pointer, canonical rules in `references/fleet-manifest-schema.md` §Location
and resolution — one hop, validity checks there, never re-derived here) → re-resolve the scope
root to the pointed directory first; the present/absent(no-pointer) branches below then run only
against THAT root's `ops/fleet.json` — never re-check the pointed root for a further pointer (one
hop, no chains) — and Phase 6's report names both roots. Unlike #911's forbidden automatic
fallback, this redirect fires only on a deliberately human-seeded pointer file, never on an
ancestor `fleet.json`'s mere existence.
**Absent under the resolved scope root (no pointer)** → this is a virgin SEED at THAT scope root, full stop —
never fall through to an ancestor's `fleet.json` just because one exists farther up the walk, and
never default to the repo root when a nearer `.claude` directory was found. Seed `fleet.json`
there now with the schema in `references/fleet-manifest-schema.md` (seat roster, canonical tier
ladder with today's date as `justification_date` for every seat still at its canonical tier,
`mode: "manual"` for every seat, empty `live_state.joined`) — no interview, matching
`team-scaffolding`'s own rule that an explicit command invocation with no role question asked is
itself the human's act of declining one; running `/fleet-bootstrap` at all is that same explicit
act. **Name the resolved scope root (its basename) and which branch (existing-read vs.
fresh-seed, and for a seed, app-scoped vs. repo-root) in Phase 6's report** — every other ops
record this skill writes (`fleet-roster.md` and the rest) follows this same resolved scope root
for the remainder of the run, never a separately re-derived path. **`{scope}` for the rest of this
run's seat naming (Phase 1's `{scope}-marshal` and every roster row) is the resolved scope root's
own directory basename** — the repo basename when the scope root IS the repo root (the common
case), or the app directory's own basename (e.g. `signup` for `frontend/apps/signup`) when it
isn't; never the repo's basename regardless of where the scope root actually resolved.
**Then run the tier reconcile** (`references/fleet-manifest-schema.md` §"Tier reconcile on every
bind" — canonical there, never re-derived here): diff every `seats.<role>.tier` against the
current canonical ladder; a stale-or-unjustified mismatch is flagged to the human with an
interactive fix-or-keep question, never silently rewritten and never silently passed over.

**Discover or join a standing cross-repo coordination channel.** Read `cross_repo_coordination`
(schema: `references/fleet-manifest-schema.md`) alongside the rest of this Phase's read. A
non-empty array means this repo's fleet already participates in one or more named channels —
print each entry's `participants` (each participant's `repo`, its `app` when sub-app-scoped, and
its `role`) so this session knows which peer marshals it can `SendMessage` cross-repo without
re-establishing anything (`fleet-rules` Section 1's coordination scope ladder: only registered
peers, never an unscoped broadcast). Absent/empty and a human directs this session to stand one up
(or an equivalent instruction relays from a peer repo's marshal, same provenance bar issue #866
itself applied — confirm with the live human before treating a relayed instruction as ratified) →
append a new `cross_repo_coordination` entry naming the `participants` (each repo, its `app` when
the authority is sub-app-scoped, and its `role`), today's date, and who authorized it, in THIS
repo's own `fleet.json` — never write into another repo's copy; each participating repo records
its own entry for the same channel independently.

## Phase 1 — Register this session as the orchestrator seat

This session registers itself as `{scope}-marshal` (role key `agent`) by performing `team-scaffolding`'s own Phase 1–4
mechanics inline — role `agent`, canonical tier, no permission-profile deviation — rather than
running `/team-scaffolding agent` through the Skill tool. That path is structurally blocked:
`team-scaffolding` carries `disable-model-invocation: true` (command-only adoption is deliberate
there — see its own Rejected alternatives), and `/fleet-bootstrap` carries the same flag, so this
composition IS already the one explicit human-typed invocation `team-scaffolding`'s contract
requires; there is no second human turn to wait on (same defect class as #421/#422, team-scaffolding's
own Phase 5 fix — a skill claiming a Skill-tool hand-off against a `disable-model-invocation`
target).

**Run this in a dedicated terminal, not the user's working session (#896).** The marshal's own
tool-use stream (seat wakes, gate holds, routing decisions) runs continuously in that terminal —
`fleet-rules` Section 3's no-op-silence rule caps what of that becomes an explicit user-facing
status line (milestone-only), not the terminal's live activity itself — so a separate terminal
keeps even the capped subset out of the user's working-session feed. The user drops into the
marshal terminal at gates (accept markers, blocked reports, needs-input). **A background/subagent
marshal was considered and REJECTED**: a subagent has no `AskUserQuestion` channel (#541 — a fork
or `Agent`-tool dispatch cannot reach it at all), so it could never hold a live gate or ask a
clarifying question; it also can't be interactively steered mid-run the way a live terminal can;
and relaying its output back through the working session re-adds the hop tax #265 measured for
that same shape.

1. Bind role `agent`. Validate against the `fleet.json` Phase 0 resolved (never a bare
   `.claude/ops/fleet.json` re-derived here). A still-live `agent` entry here
   is a **takeover, not a collision** (not a Failure branch — proceed straight to steps 2 and 5's
   takeover path). This is narrower than `team-scaffolding`'s own role-token collision rule, and
   the distinguishing fact is which caller is at the call site, not how explicitly either command
   was invoked: `team-scaffolding`'s bare/role-token path can be run by ANY session binding ANY
   role, so a live entry there really can be a second, different session double-booking the same
   role — the case its collision guard exists to catch. `/fleet-bootstrap` Phase 1 only ever binds
   THIS running session to `agent`, so the live entry it finds is either this same terminal's own
   earlier registration or a stale entry from a session that never released the seat — never a
   concurrent bind attempt at this call site. This mirrors the accepted-risk framing Phase 5's
   hybrid-swap rule already states for background seats ("replaceable at any time by a human
   running `/team-scaffolding <role>` in their own terminal") — extended here to the orchestrator
   seat itself. **Caveat, stated plainly rather than papered over**: this command has no
   session-identity signal to structurally rule out a genuinely different human re-running
   `/fleet-bootstrap` on the same repo and getting treated as a takeover too — same accepted risk
   the hybrid-swap rule already carries for background seats, not a new one.
2. Print `Seat: {scope}-marshal — takeover` when step 1 found a live entry, `Seat: {scope}-marshal`
   otherwise, and append the roster row to `fleet-roster.md` alongside the `fleet.json` Phase 0
   resolved — same directory, never a separately re-derived path — under that same
   `{scope}-marshal` session name (role key `agent`) — suffixed `(takeover)`
   in the former case (`team-scaffolding` Phase 2).
3. `agent` carries no permission-profile deviation (`team-scaffolding` Phase 3) — state that
   explicitly: `No permission-profile deviation for this role — full write access retained`.
4. Print the comms charter (`team-scaffolding` Phase 4): the `agent` seat tier (sonnet+high,
   the canonical orchestration row since the 2026-08-22 ladder retier — which also keeps this
   seat's unpinnable `context: fork` dispatches at sonnet price, #313), the
   SendMessage-is-a-nudge doctrine, and the peer roster read from `fleet-roster.md`. **Run the
   reality check** (`references/fleet-manifest-schema.md` §"Tier reconcile on every bind" —
   "Reality check" subsection, canonical there, mechanics not restated here): state this session's
   own resolved model and diff it against `seats.agent.tier` just printed, naming any mismatch
   (issue #919).
5. **Resolve this session's real SendMessage address before writing anything**: read it from
   `ListAgents`, matched to THIS session's own transcript/session id (a narrower, deliberate
   exception to the peer-discovery ban in `fleet-rules` Section 1 — that ban is about never using
   `ListAgents` to go find some OTHER session; resolving this session's own already-known identity
   is not a discovery act) — the harness-assigned session name this running session is actually
   reachable at (e.g. `plugins-75`), never the aspirational `{scope}-marshal` label and never left
   null (#902 — the prior omission stranded every peer trying to route back to a live marshal).
   **Fresh join** (no live entry found in step 1): append `live_state.joined` (`role: agent`,
   `mode: manual`, `action: "joined"`, today's date, `agent_name`: the resolved address) in
   `fleet.json`, per Phase 0. **Takeover**: append a fresh `live_state.joined` row too (`role:
   agent`, `mode: manual`, `action: "joined"`, today's date, `agent_name`: the resolved address)
   rather than leaving the prior entry as the only record — the takeover session's own address is
   new information the roster row alone doesn't carry. This produces a `joined` row appended
   directly atop a still-`joined` (never-released) prior row for `agent` — a second, narrower shape
   alongside `references/fleet-manifest-schema.md`'s release-then-rejoin takeover cycle, documented
   there as this step's own citation (never re-derived here); `fleet.json` still never carries two
   rows *read* as distinct live holders, since liveness is always the LATEST row per role.
6. **Adopt `teamwork:bind-team`'s contract inline, by default, as this Phase's own last step** —
   the same inlining mechanic Phase 5 uses for `planner`'s `/bind-planning` contract (read the
   target skill's own body directly, follow its procedure, never a Skill-tool hand-off against a
   `disable-model-invocation` target), extended here to the orchestrator's own standing contract.
   Unlike `planner`'s case, the justification isn't "no human session to hand it to" — this
   session IS a live human session — it's that `/fleet-bootstrap` is already the one explicit
   human-typed invocation cold-starting a WHOLE fleet under orchestration; requiring a *second*
   typed `/bind-team` to hold the discipline that running a fleet cold-start already implies is
   the same needless-extra-turn defect class step 1's own takeover reasoning above already names
   (#421/#422/#850). Run `bind-team`'s Phase 1 and Phase 2 verbatim, right here, with one
   deliberate substitution: bind Phase 1's charter EXPLICITLY as "this fleet's operation, for its
   duration" rather than `bind-team`'s own default (blank) charter — the default only holds for
   the first unit of work and then requires a fresh `/bind-team` per `bind-team`'s own "When this
   rule ends" closing rule (a new charter needs a new invocation); a fleet cold-start needs the
   wider, fleet-scoped charter instead, so this step supersedes that per-charter rebind rule for
   THIS seat by binding a charter that IS the fleet's whole duration up front, never the default.
   Then run Phase 2 unchanged (read `agents/fleet-marshal.md` Priorities 1–8 in full, invoke
   `fleet-rules` and `loop-rules`, print the acknowledgment block naming the substituted charter).
   **This is a `/fleet-bootstrap`-specific default, not a change to `bind-team`'s own invocation
   contract** — `team-scaffolding`'s single-seat join path (any role, not just orchestrator, and
   not necessarily inside a fleet cold-start) still correctly leaves `bind-team` for a separate
   human turn; only this command's own Phase 1 inlines it, because only this command's own premise
   (stand up the whole fleet) already implies wanting it.

This registers the seat AND holds the `bind-team` contract from this point forward, under the
fleet-scoped charter step 6 bound — the routing/gating/budget/rollup discipline in
`agents/fleet-marshal.md`'s Priorities 1–8 governs this session's handling of every subsequent
phase and everything that arrives after Phase 6 reports, closing only on an explicit stand-down
(never on the first unit of work, since step 6 bound the fleet's own duration as the charter, not
`bind-team`'s default) — state a stand-down explicitly rather than letting it go silently
ambiguous. **This command's own remaining phases (2–6) are the seat's bootstrap mechanics —
coordination records (`fleet.json`, `fleet-roster.md`, the reviewer wall) rather than a charter
deliverable — so Priority 1's STRICT-ROUTER/NEVER-BUILDS rule binds incoming work from Phase 6
onward, not these steps themselves.** **Registering the seat is not the same as knowing what to do
with it**: `fleet-rules`' Section 7 ("Route-anything-incoming protocol") is this seat's standing
triage discipline for whatever arrives next — a raw ask, a bug/feature/task report, a handback, a
peer message — already adopted by step 6's own Phase-2 read, cited here, never restated.

## Phase 2 — Dispatch the product seat

Dispatch a synchronous `Agent` call, `subagent_type: teamwork:product-leader` (same-plugin since
issue #433 moved it from `docs/agents/product-leader-agent.md`, dropping the `-agent` suffix — the
prior `docs:product-leader-agent` reference here named no real agent file and was issue #919's own
found defect, degrading this dispatch to an unpinned, session-model-inheriting shape; the "`docs`
not installed" fallback branch that once covered it is retired along with the stale name — this
target is now always reachable whenever `fleet-bootstrap` itself runs) for one charter: "produce
or update the intent layer — product brief / PRD / IDRs — for this repo, then report a summary of
what it proposes, ready for human ratification. Do not treat silence as approval; you are drafting
for someone else's sign-off." **State `model` explicitly on this call, read from `fleet.json`'s
`seats.product.tier`** (canonically sonnet; read from the manifest, not assumed off frontmatter,
since a repo-local model deviation lives only there — issue #919). A plain `Agent` dispatch
cannot vary `effort` per-call — frontmatter is what it always gets (`agent-writing-rules` §Model
tiering) — so a recorded `effort` deviation goes through a Workflow dispatch or a frontmatter
edit instead, never claimed as a param here. Record `live_state.joined`
(`role: product`, `mode: dispatched` — a synchronous `Agent` call, not a live terminal or a
long-lived background seat) once it reports back.

## Phase 3 — HARD GATE: human ratification of the intent layer

This is the one hard gate in the whole command. Present the product seat's proposed intent layer
via `AskUserQuestion` (options: Ratify / Revise — send back to the product seat with feedback /
Reject — stop the cold start here) whenever a live user is reachable.

**No live user reachable** (unattended dispatch, `AskUserQuestion` unavailable or would auto-answer
under momentum): STOP here. Report plainly that the fleet cold start is blocked on this gate, name
it explicitly ("intent-layer ratification — human required"), and do not proceed to Phase 4 or 5 —
mirrors `authorkit:overhaul-execute`'s own no-live-user rule: a run with no reachable human at a
hard gate reports SKIPPED/blocked.

Record the gate's outcome (`ratified` / `revised-and-reratified` / `rejected-stopped-here`) as
`live_state.gate` in `fleet.json` before continuing.

## Phase 4 — Determine and confirm the spawn list

`$ARGUMENTS`, comma-separated, restricted to `reviewer` and `planner` (the only two seats this
phase can spawn — `agent` is already this session, `product` was already dispatched in Phase 2).
**Default (no argument): empty.** Reviewer and planner are, per #410 addendum 3, the
seats Kim drives manually in a terminal — a background agent cannot be interactively steered the
way a live terminal seat can, so defaulting to spawning them would fight the human's own stated
operating mode.

**Read live seat state before offering anything to spawn.** Read the `fleet.json` Phase 0
resolved (never a bare `.claude/ops/fleet.json` re-derived here) for its
`live_state.joined` for `reviewer` and `planner` and take each role's LATEST row's `action`
(absent read as `"joined"` — the schema's own liveness rule, canonical in
`references/fleet-manifest-schema.md`, never re-derived here). A role whose latest row is
`"joined"` is **already held** — drop it from `$ARGUMENTS`' effective list and from the confirm's
offered options entirely; this phase has no takeover path the way Phase 1 does for `agent`; a
spawn here would just double-book a live seat. A role whose latest row is `"released"`, or with no
entry at all, is open and eligible. **Never a silent drop**: if `$ARGUMENTS` named a role dropped
here, say so plainly before presenting the confirm — "`<role>` is already held (joined
`<date>`) — dropped from the spawn list" — and carry the same fact into Phase 6's reported spawn
line rather than letting the filtered list read as if the argument had simply omitted it.

**This command's one confirm** (#410 bare-invocation-UX addendum: "exactly ONE confirm — the
background-seat spawn list before creating them; fan-out is confirmed, never inferred"): present
the resolved list — `$ARGUMENTS`' value after dropping any already-held role, or "none (default)"
— via one `AskUserQuestion` before spawning anything, offering only the OPEN roles as options
(`None` always included; `reviewer`, `planner`, and `reviewer + planner` each appear only if every
role they name is open — an already-held role is never an offered option, mirroring
`team-scaffolding` Phase 1's bare-invocation rule that a held seat is never offered), pre-selected
to match the filtered `$ARGUMENTS`. If both roles are already held, skip the `AskUserQuestion`
entirely — there is nothing left to confirm — and report the spawn phase as "none — reviewer and
planner already held" in Phase 6. The human's answer here is final regardless of what `$ARGUMENTS`
said — an argument sets the pre-selection, it does not skip this confirm. No live user reachable
here — a rarer case than Phase 3's, since an unattended run already stopped at that earlier gate;
this branch only fires if the human became unreachable after ratifying — → do not spawn anything
(an unconfirmed fan-out is not "assume the argument's list"); report the spawn phase as skipped
for the same no-live-user reason, and proceed to Phase 6.

## Phase 5 — Spawn the confirmed seats

For each role in the confirmed list (skip entirely if empty — proceed straight to Phase 6).
**`planner` and `reviewer` now spawn by genuinely different mechanisms (issue #853): an in-process
`Agent`-tool dispatch inherits the parent session's permission mode instead of re-deriving one from
its own cwd, so it can never be a genuinely separate OS process — harmless for `planner` (carries
no wall), disqualifying for `reviewer` (the wall's whole point is structural enforcement, and
issue #852 found the old shared shape produced a false-positive `wall_applied: true`). Branch by
role below.**

### `planner` — in-process `Agent`-tool dispatch, unchanged

1. Dispatch via the `Agent` tool, `name: "{scope}-planner"`, **`model` set explicitly from
   `fleet.json`'s `seats.planner.tier`'s model half** (canonically fable) — this call names no
   `subagent_type` agent file (it inlines bootstrap mechanics instead, below), so it is exactly the
   ad-hoc/no-frontmatter shape that silently rides the session's own model when `model` is left
   unstated (`agent-writing-rules` §Model tiering, issue #313/#919 — a live gap here). A plain
   `Agent` dispatch cannot vary `effort` per-call (same citation) — this call carries no
   `effort` param for that reason, never a claimed one it cannot honor. Prompt instructing it to perform
   `team-scaffolding`'s own Phase 1, 2, and 4 mechanics directly, itself, via ordinary
   `Read`/`Write`/`Edit`/`Bash` tool calls — **never** by invoking `/team-scaffolding planner`
   through the Skill tool, which is structurally blocked for a dispatched agent with no live
   terminal, the same reason Phase 1 above inlines those mechanics for the orchestrator seat rather
   than claiming that hand-off (the #421/#423/#850 class). Quote the role's own steps into the
   dispatch prompt: the naming line (`Seat: {scope}-planner`), the comms charter (Phase 4, including
   point 5's intent-layer self-check), and "no permission-profile deviation for this role" (Phase 3
   never applies to `planner`). Then hold its adopted `/bind-planning` contract for the fleet's
   duration by reading that skill's own body directly and following its procedure (never invoking
   it via the Skill tool either — `team-scaffolding` Phase 5: every `bind-*` target is also
   `disable-model-invocation: true`); state in the dispatch prompt that this is a deliberate
   exception to `bind-*`'s own no-model-routed-adoption stance (`team-scaffolding`'s Rejected
   alternatives), made only because a background seat has no human session to hand the contract to
   instead.
2. **Record the cloud-can't-message-back caveat explicitly in that dispatch's charter text**: "You
   are a background seat — if this session runs remotely, it cannot `SendMessage` back to a peer
   that has since exited. Route anything a peer needs to see through the durable channels
   (`fleet.json`'s live-seat state, `fleet-roster.md`, GitHub Issue/PR comments), never solely
   through a live nudge you cannot guarantee lands."
3. Append `live_state.joined` (`role: "planner"`, `mode: "background"`, `agent_name`, today's
   date) in `fleet.json`, appended by this same dispatched seat (not the orchestrator) since it is
   the one holding the live tool context and carries no wall to work around.

### `reviewer` — a genuine `claude -p` subprocess, spawned by the orchestrator into a pre-walled worktree (issue #853)

The old in-process shape (an `Agent`-tool dispatch that wrote its own wall mid-session) is what
issue #852 found never actually enforces — permission/hook config loads once per OS process and
does not hot-reload, and an `Agent`-tool dispatch inherits the parent's permission mode rather than
re-deriving one from its own cwd, so it was never a genuinely new process either. Issue #853's own
investigation (Findings, this issue) live-tested the fix: a `claude -p` child spawned with cwd
already inside an ALREADY-walled worktree IS correctly denied, from inside a dispatched seat's own
`Bash` tool, even under this machine's global `bypassPermissions` default. This dispatch realizes
that tested shape:

1. **Worktree precondition, run by the ORCHESTRATOR itself** (this session — never a dispatched
   seat). `team-scaffolding` Phase 1's own check against the reviewer's target worktree:
   `git rev-parse --git-common-dir` vs. `--git-dir` — differ only inside a linked worktree. Same
   (shared checkout) → stop here: no wall write and no spawn attempted, and the ORCHESTRATOR itself
   (never a dispatched seat) immediately appends `live_state.joined` (`role: "reviewer"`, `mode:
   "background-subprocess"`, `agent_name: null` — no process was ever spawned, today's date,
   `action: "joined"`, `wall_applied: "blocked-worktree"`, no `wall_verified_via`) — report per
   Phase 6 and name `EnterWorktree` as the fix, same as the manual path.
2. **Write and verify the wall — by the ORCHESTRATOR, entirely BEFORE any spawn.**
   `team-scaffolding` Phase 3's own C1–C1a write (merge `deny: ["Edit","Write"]` plus the
   `gh`/Read/Grep/Glob allow-list; merge the `PreToolUse` `Bash`-gating hook) then C3's own
   re-read-and-grep verify, run directly with this session's own `Read`/`Write`/`Edit`/`Bash` tools
   — this session is not walled, so it can do this cleanly, and the wall must already be ON DISK
   before the child process starts (issue #853's Q1: a wall written before process start enforces;
   a wall a session writes about itself never does, issue #852). Verification fails → stop, report
   the failure (Failure branches), no spawn attempted.
3. **Spawn exactly ONE `claude -p` child**, `--model <seats.reviewer.tier's model> --effort
   <its effort>` (canonically `--model sonnet --effort high`, read from `fleet.json` rather than
   hardcoded) **passed explicitly on the spawn command line** — a separate OS process has no
   dispatching-session frontmatter to inherit; absent these flags its model is just the CLI's own
   configured default, which may have nothing to do with this repo's tier ladder (issue #919, a
   live gap here). Background `Bash` (`run_in_background:
   true`), cwd =
   the pre-walled worktree, stdout+stderr redirected to a log file by THIS SESSION'S OWN shell
   redirect — that redirect is this session's operation, not a tool call the child itself makes, so
   the child's wall never touches it (the exact mechanism this issue's own live round-trip test
   verified: the spawning session's redirect landed cleanly while the child's own in-process
   `Write`/denied-`Bash` attempts were both denied). The child's prompt carries: the naming line
   (`Seat: {scope}-reviewer`), the reviewer's charter (`team-scaffolding` Phase 4 points 1, 4, 6 —
   tier, review-instrument roster, locked-spec self-check — quoted verbatim, no Skill-tool
   hand-off, same reasoning as `planner`'s dispatch above), and one MANDATORY first act before any
   review work: run `lld-0006` I2's own three-probe sequence (a denied `Write`, a denied-pattern
   `Bash`, one allowed `gh`-shaped `Bash`) and print each result to stdout in this EXACT
   three-line, colon-delimited format, one line per probe, no other text on those lines (the
   orchestrator's step 4 parses these literal keys):
   ```
   I2-PROBE write: DENIED|SUCCEEDED
   I2-PROBE bash-denied: DENIED|SUCCEEDED
   I2-PROBE bash-allowed: PASSED|FAILED
   ```
   followed by the quoted denial/pass text on subsequent lines, free-form. **This confirm step's
   own report channel is the child's stdout alone — captured by the orchestrator's own log
   redirect above, never a `gh issue comment` and never a Bash-redirect write to
   `fleet.json`/`fleet-roster.md`.** (Once this child moves on to actual REVIEW work, its output
   channel is the normal one: `gh issue`/`pr comment` on whatever target it's reviewing,
   `bind-review`'s own routing table — a concrete target per review task, unlike this one-shot
   confirm which has no natural GitHub target of its own.) A Bash-redirect write to `fleet.json`
   would additionally hit a confirmed platform gap regardless: this issue's own live build found
   the retirement-only C1a escape hatch's charset structurally excludes `{`/`}` (verified against
   the exact hook regex in `lld-0006-fleet-permission-profile.md` C1a), so a JSON-object append —
   exactly what a structured `fleet.json` entry needs — is denied even when it targets one of the
   three permitted paths; lld-0006's own C1a text already flagged this as a residual gap to widen
   deliberately if ever needed, never silently — filed as follow-up issue #855 rather than widened
   here. The child never attempts a `fleet.json`/roster write at all; step 4 below is the
   orchestrator's job instead.
4. **Monitor and collect, by the ORCHESTRATOR.** Poll the spawned process (bounded budget — ~180s
   default, overridable; this issue's own live round trip completed in 40–48s) until it exits or
   the budget is exhausted, then read the captured log for the I2 verdict in the fixed format the
   prompt required.
   - Process exited AND both denied-probe lines confirm DENIED, with the allowed-probe line
     confirming PASSED → `wall_applied: true`, `wall_verified_via: "subprocess-spawn"`
     (`references/fleet-manifest-schema.md`). Quote both denial texts (from the child's own report)
     in this dispatch's Findings.
   - Process exited but the log doesn't show the expected denial (a probe unexpectedly succeeded,
     or the fixed format is missing/malformed) → `wall_applied: "same-session-unenforced"` — same
     honest label issue #852 named, since the observable outcome (an unwalled write went through)
     is identical regardless of which process shape produced it.
   - Budget exhausted with no exit → `wall_applied: "spawn-unconfirmed"` (issue #853) — the process
     may still be running or may have died silently; name it plainly rather than guessing, and
     leave the background process running (never kill it blind) unless a repeat check later
     confirms it has since exited.
   - **Append `live_state.joined`** in `fleet.json` (`role: "reviewer"`, `mode:
     "background-subprocess"`, `agent_name`: a name identifying the spawned process — there is no
     fleet messaging identity for a subprocess, so its log-file path or PID-at-spawn-time is the
     durable pointer — today's date, `action: "joined"`, `wall_applied` and, when `true`,
     `wall_verified_via`, per the above). **This append is now done by the ORCHESTRATOR, never by
     the spawned child** — a genuinely walled subprocess structurally cannot write it (step 3's own
     finding), so the prior design's "the dispatched seat is its own fleet.json writer" assumption
     no longer holds for `reviewer`.
5. **Ongoing review work — the durable artifact is the wall on disk, not one long-lived process.**
   `claude -p` is one-shot per invocation (this issue's Findings) and cannot itself "hold a seat
   open" the way an interactive terminal does. The wall (step 2) persists in the worktree for the
   fleet's duration regardless of whether any one `claude -p` process is currently running — every
   FUTURE `claude -p` invocation spawned with cwd in that same worktree inherits the same
   structural enforcement for free, with no re-write needed, and does NOT need periodic
   re-verification against that same wall (Kim's ruling, issue #856, 2026-08-21 — a file-on-disk
   artifact does not degrade, so no re-probe after a `/team-scaffolding retire` cycle or on a fixed
   interval). So "holding the reviewer contract" now means: further review tasks are driven by
   fresh, per-task `claude -p` spawns into this same pre-walled worktree, via
   `teamwork/scripts/reviewer_scheduler.py` (issue #856) — one scheduling pass per invocation over
   an explicit `--tasks-file`, handling the spawn/crash-recovery/log-rotation/index mechanics; drive
   its recurring cadence with `/loop` (a live session) or `/schedule` (unattended), never a
   bespoke daemon this plugin reimplements. Full mechanics, the per-task prompt contract, and the
   local index shape: `references/reviewer-scheduler.md`. What #853 itself shipped was the one-shot
   bind-plus-I2-confirm round trip (steps 1–4) that the scheduler's own `verify_wall_present`
   precondition now composes on top of — it refuses to spawn anything against a worktree whose wall
   was never confirmed written.

**Hybrid swap**: any spawned seat (background or background-subprocess) is replaceable at any time
by a human running `/team-scaffolding <role>` in their own terminal — the roster (`fleet.json` +
`fleet-roster.md`) is what a rejoining session reads to discover it's taking over an existing seat,
not starting fresh.

## Phase 6 — Report

One summary: which seats are live and how (manual/background/background-subprocess), the gate's
outcome, the spawn list honored (one of: "none — confirmed default", "reviewer/planner —
confirmed", "none — reviewer and planner already held", or "confirm skipped — no live user,
nothing spawned"), the `fleet.json` path Phase 0 resolved — including which branch it took
(existing record read at that path, a fresh seed — and for a seed, app-scoped-cwd vs. repo-root —
or a pointer-redirected read, reporting both the walk's resolved root and the pointer target, #915)
— as the durable record a later session reads to resume orientation, and confirm the `bind-team`
contract Phase 1 step 6 already adopted is holding — this session runs under `agents/fleet-marshal.md`'s Priorities 1–8 for the fleet's
duration until explicitly stood down; never re-invoke `/bind-team` to start it, it is already
live. **For any spawned
`reviewer` seat, read its `wall_applied` (and, when present, `wall_verified_via`) field back from
`fleet.json` (Phase 5's own append, `references/fleet-manifest-schema.md`) and state the outcome
explicitly** — one of "applied and verified via subprocess spawn" (`wall_applied: true`,
`wall_verified_via: "subprocess-spawn"` — I2's own probe, run inside the spawned `claude -p` child,
denied both a `Write` and a denied-pattern `Bash` attempt), "content-verified but NOT enforced"
(`wall_applied: "same-session-unenforced"` — issue #852/#853), "not yet — worktree isolation
required" (`wall_applied: "blocked-worktree"` — name `EnterWorktree` plus re-running
`/team-scaffolding reviewer` there as the fix), "spawn did not confirm in time" (`wall_applied:
"spawn-unconfirmed"`, issue #853 — name the log path and state whether the background process is
still running), or "unknown — no wall-outcome report received" (field absent) — never omitted and
never assumed applied by default.

**Close with the address roster (Kim's ruling, 2026-08-22) — every seat, one line each, in this
exact shape, so a human knows who can be messaged by name right now:**

```
- `@{scope}-marshal` — this fleet's orchestrator agent (this session; fleet.json role `agent`)
- `@{scope}-planner` — this fleet's planner agent
- `@{scope}-reviewer` — this fleet's review agent
- `@{scope}-product` — this fleet's product agent
```

Each line carries its live addressability, classified from `fleet.json`'s LATEST row for that
role (its `mode` + `action` — `fleet.json` governs, never the roster file, per Phase 4's own
source-of-truth rule) — never assumed from the convention alone, since a printed name that
silently drops messages is worse than no name. Four classes, exactly one per seat:
- **addressable** — a live named `Agent`-tool dispatch (`mode: "background"`, latest action
  `joined`: `planner` spawned this run, or a prior run's still-live one — confirm a prior-run
  seat's liveness via `ListAgents`, the one sanctioned liveness-confirm use), or a live human
  terminal (`mode: "manual"`, latest action `joined`). `{scope}-marshal` is always this session
  and always addressable.
- **not live — returned dispatch** — `mode: "dispatched"` (the `product` seat's Phase 2 call: a
  synchronous, unnamed `Agent` call that has already returned by now; nothing to message).
- **not messageable — subprocess** — `mode: "background-subprocess"` (`reviewer` spawned as a
  `claude -p` child: one-shot, no messaging identity; name its log path as the pointer instead).
- **not live — bind it with `/team-scaffolding <role>`** — no row at all, or latest action
  `released`.

The `@` is a display sigil for the human's eye only; the actual `SendMessage` target is the bare
session name (`plugins-marshal`, never `@plugins-marshal`) — the same bare form every roster row
and `team-scaffolding` introduction uses. A seat with no live holder is listed so the human sees
the gap, not omitted.

## Failure branches

- **No `.claude` directory found anywhere between cwd and the repo root (inclusive), Phase 0**
  (#911) → there is no scope root to resolve at all; stop and report this explicitly rather than
  silently seeding at the repo root or cwd by default — a repo genuinely carrying no `.claude/`
  anywhere is not itself a fleet-shaped case; name `.claude` directory creation (or running from a
  directory that already has one) as the fix.
- **No live user at Phase 3** → stop there per Phase 3; nothing after it runs.
- **`fleet-scope.json` pointer names a dir outside the repo-root boundary or lacking its own
  `.claude/`** (#915) → stop at Phase 0 and report the invalid pointer explicitly
  (`references/fleet-manifest-schema.md` §Location and resolution); never fall back silently to
  the walk-resolved root.
- **`fleet.json` malformed or unwritable** → stop at Phase 0, report the failure; do not proceed
  believing seat state is being tracked when it silently isn't (mirrors `lld-0006`'s C3 verification
  discipline for the reviewer wall).
- **Spawn-list argument names anything other than `reviewer`/`planner`** → report the invalid
  entries and proceed only with the valid ones (never silently drop the whole argument to the
  default).
- **The `reviewer` worktree precondition finds a shared checkout (no isolation, issue #853)** → the
  ORCHESTRATOR's own Phase 5 step 1 check stops there, before any wall write or spawn is attempted
  — never a dispatched seat's own check (the old in-process shape this superseded); this is
  correct behavior, not a defect. The orchestrator itself appends `live_state.joined` immediately
  with `wall_applied: "blocked-worktree"` (Phase 5 step 1); Phase 6 reports the outcome as "not
  yet — worktree isolation required" rather than silently treating the spawn as fully walled.
- **A dispatched `planner` seat never reports back at all** (background dispatch died, or is
  unreachable before this session's own Phase 6 runs) → report its hold outcome as "unknown — no
  report received" rather than assuming success; `fleet.json`'s own `live_state` entries are the
  durable source a later session re-checks.
- **A spawned `reviewer` `claude -p` child never exits within Phase 5 step 4's monitoring budget**
  (issue #853) → `wall_applied: "spawn-unconfirmed"`, never a guessed `true` or
  `"same-session-unenforced"`; leave the background process running (killing it blind can strand a
  half-written report) and name the log path so a later check can resolve it either way.

## Done

Done when Phase 6's report has printed — never when the gate is still pending (a blocked run at
Phase 3 is its own valid terminal state, reported as blocked, not silently abandoned).
